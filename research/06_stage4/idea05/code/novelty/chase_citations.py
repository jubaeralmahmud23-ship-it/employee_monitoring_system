#!/usr/bin/env python3
"""Backward and forward citation chasing for the idea 5 deep novelty check
(research/02_candidate_ideas.md section 4.2, 'Chasing').

Usage:
  python -I chase_citations.py <raw_dir> <results_dir>

Seeds and legs (plan): Pika et al. 2017 forward (abstract level); Martin and Beerepoot
BISE 2024 backward; Saisana et al. 2005, Adams et al. 2010 and Nakatumba and van der Aalst
2010 forward. One extra leg not in the plan: Pika et al. CAiSE 2014 forward (the earlier
version of the resource-profile framework).

Tools per leg: OpenAlex (work lookup -> referenced_works or the cites: filter, with
abstract_inverted_index) and Semantic Scholar (/citations or /references with abstracts).
Calls are paced >= 3.5 s apart; on HTTP 429 or a network error the call waits 30, 45, then
60 s; a call is tried at most three times and the leg is then recorded as 'not done'.
Backward legs also read the Crossref 'reference' list.

Outputs (results_dir): chase_log.csv (every HTTP call), chase_summary.csv (one row per
seed x direction x tool), chase_works.csv (every work returned: seed, direction, tool, id,
doi, title, year, venue, abstract_available). Abstract text is written only to raw_dir
(abstracts.jsonl), outside the repository. Standard library only.
"""
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

MAILTO = "jubaeralmahmud23@gmail.com"
UA = "idea05-novelty-check/1.0 (mailto:%s)" % MAILTO
PACE = 3.5
BACKOFF = [30, 45, 60]

SEEDS = [
    # key, DOI, legs
    ("pika2017", "10.1145/3041218", ["forward"]),
    ("martin_beerepoot2024", "10.1007/s12599-024-00894-3", ["backward"]),
    ("saisana2005", "10.1111/j.1467-985x.2005.00350.x", ["forward"]),
    ("adams2010", "10.1056/nejmsa0906323", ["forward"]),
    ("nakatumba2010", "10.1007/978-3-642-12186-9_8", ["forward"]),
    ("pika2014_extra", "10.1007/978-3-319-07881-6_38", ["forward"]),
]

_last = [0.0]


def get(url):
    """GET with pacing; up to three attempts. Returns (status, body or None, attempts)."""
    status = None
    for i in range(3):
        wait = PACE - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.status, r.read().decode("utf-8", "replace"), i + 1
        except urllib.error.HTTPError as e:
            status = e.code
            if e.code == 404:
                return 404, None, i + 1
        except Exception as e:
            status = "ERR:" + type(e).__name__
        if i < 2:
            time.sleep(BACKOFF[i])
    return status, None, 3


def inv_to_text(inv):
    if not inv:
        return ""
    pos = []
    for w, idx in inv.items():
        for k in idx:
            pos.append((k, w))
    return " ".join(w for _, w in sorted(pos))


class Run:
    def __init__(self, raw, res):
        self.raw, self.res = raw, res
        self.log, self.summary, self.works = [], [], []
        self.abs_f = open(os.path.join(raw, "abstracts.jsonl"), "w", encoding="utf-8")

    def save(self, name, body):
        with open(os.path.join(self.raw, name), "w", encoding="utf-8") as f:
            f.write(body)

    def add(self, seed, direction, tool, wid, doi, title, year, venue, abstract):
        self.works.append([seed, direction, tool, wid, (doi or "").replace("https://doi.org/", ""),
                           (title or "").replace("\n", " "), year, venue or "", "yes" if abstract else "no"])
        self.abs_f.write(json.dumps({"seed": seed, "direction": direction, "tool": tool, "id": wid,
                                     "doi": doi, "title": title, "year": year, "venue": venue,
                                     "abstract": abstract}) + "\n")

    # ---------------- OpenAlex ----------------
    def oa_lookup(self, key, doi):
        url = ("https://api.openalex.org/works/doi:" + urllib.parse.quote(doi)
               + "?select=id,display_name,publication_year,referenced_works,cited_by_count&mailto=" + MAILTO)
        st, body, n = get(url)
        self.log.append([key, "lookup", "OpenAlex", url, st, n])
        if body is None:
            return None
        self.save(f"oa_{key}_work.json", body)
        return json.loads(body)

    def oa_list(self, key, direction, filt):
        got, cursor, page = 0, "*", 0
        sel = "id,doi,display_name,publication_year,primary_location,abstract_inverted_index"
        while cursor and page < 20:
            url = ("https://api.openalex.org/works?filter=" + filt + "&select=" + sel
                   + "&per-page=200&cursor=" + urllib.parse.quote(cursor) + "&mailto=" + MAILTO)
            st, body, n = get(url)
            self.log.append([key, direction, "OpenAlex", url[:220], st, n])
            if body is None:
                return None
            self.save(f"oa_{key}_{direction}_p{page}.json", body)
            d = json.loads(body)
            for w in d.get("results", []):
                src = ((w.get("primary_location") or {}).get("source") or {}) or {}
                self.add(key, direction, "OpenAlex", w.get("id"), w.get("doi"), w.get("display_name"),
                         w.get("publication_year"), src.get("display_name", ""),
                         inv_to_text(w.get("abstract_inverted_index")))
                got += 1
            cursor = d.get("meta", {}).get("next_cursor")
            page += 1
            if not d.get("results"):
                break
        return got

    def oa_refs(self, key, refs):
        got = 0
        for i in range(0, len(refs), 50):
            ids = "|".join(r.rsplit("/", 1)[-1] for r in refs[i:i + 50])
            r = self.oa_list(key, "backward", "openalex:" + ids)
            if r is None:
                return None
            got += r
        return got

    # ---------------- Semantic Scholar ----------------
    def s2(self, key, doi, direction):
        ep = "citations" if direction == "forward" else "references"
        field = "citingPaper" if direction == "forward" else "citedPaper"
        got, offset = 0, 0
        while True:
            url = ("https://api.semanticscholar.org/graph/v1/paper/DOI:" + urllib.parse.quote(doi, safe="/")
                   + f"/{ep}?fields=title,abstract,year,venue,externalIds&limit=500&offset={offset}")
            st, body, n = get(url)
            self.log.append([key, direction, "SemanticScholar", url, st, n])
            if body is None:
                return None if got == 0 else got
            self.save(f"s2_{key}_{ep}_{offset}.json", body)
            d = json.loads(body)
            for row in d.get("data", []):
                p = row.get(field) or {}
                ext = p.get("externalIds") or {}
                self.add(key, direction, "SemanticScholar", p.get("paperId"), ext.get("DOI") or "",
                         p.get("title"), p.get("year"), p.get("venue"), p.get("abstract") or "")
                got += 1
            nxt = d.get("next")
            if nxt is None or not d.get("data"):
                break
            offset = nxt
            if offset >= 9000:
                break
        return got

    # ---------------- Crossref reference list ----------------
    def crossref_refs(self, key, doi):
        url = "https://api.crossref.org/works/" + urllib.parse.quote(doi) + "?mailto=" + MAILTO
        st, body, n = get(url)
        self.log.append([key, "backward", "Crossref", url, st, n])
        if body is None:
            return None
        self.save(f"cr_{key}_work.json", body)
        refs = json.loads(body)["message"].get("reference") or []
        for r in refs:
            title = r.get("article-title") or r.get("volume-title") or r.get("unstructured") or ""
            self.add(key, "backward", "Crossref", r.get("key"), r.get("DOI", ""), title,
                     r.get("year", ""), r.get("journal-title", ""), "")
        return len(refs)

    def run(self):
        for key, doi, legs in SEEDS:
            w = self.oa_lookup(key, doi)
            for leg in legs:
                if w is None:
                    self.summary.append([key, doi, leg, "OpenAlex", "not done (lookup failed)", ""])
                elif leg == "backward":
                    refs = w.get("referenced_works") or []
                    g = self.oa_refs(key, refs) if refs else 0
                    self.summary.append([key, doi, leg, "OpenAlex",
                                         ("done (%d referenced_works)" % len(refs)) if g is not None else "not done", g if g is not None else ""])
                else:
                    short = w["id"].rsplit("/", 1)[-1]
                    g = self.oa_list(key, "forward", "cites:" + short)
                    self.summary.append([key, doi, leg, "OpenAlex",
                                         ("done (cited_by_count=%s)" % w.get("cited_by_count")) if g is not None else "not done", g if g is not None else ""])
                g = self.s2(key, doi, leg)
                self.summary.append([key, doi, leg, "SemanticScholar", "done" if g is not None else "not done", g if g is not None else ""])
                if leg == "backward":
                    g = self.crossref_refs(key, doi)
                    self.summary.append([key, doi, leg, "Crossref", "done" if g is not None else "not done", g if g is not None else ""])
        self.abs_f.close()
        for name, header, rows in [
            ("chase_log.csv", ["seed", "direction", "tool", "url", "http_status", "attempts"], self.log),
            ("chase_summary.csv", ["seed", "doi", "direction", "tool", "status", "n_works"], self.summary),
            ("chase_works.csv", ["seed", "direction", "tool", "id", "doi", "title", "year", "venue", "abstract_available"], self.works),
        ]:
            with open(os.path.join(self.res, name), "w", newline="", encoding="utf-8") as f:
                wr = csv.writer(f)
                wr.writerow(header)
                wr.writerows(rows)


def main():
    raw, res = sys.argv[1], sys.argv[2]
    os.makedirs(raw, exist_ok=True)
    os.makedirs(res, exist_ok=True)
    t0 = time.time()
    r = Run(raw, res)
    r.run()
    print("elapsed_s", round(time.time() - t0, 1))
    for s in r.summary:
        print(s)


if __name__ == "__main__":
    main()
