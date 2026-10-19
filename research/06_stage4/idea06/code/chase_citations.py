"""Backward and forward citation chasing for the idea 6 deep novelty check.

Usage:
  python -I chase_citations.py <out_dir>

For each seed the script tries OpenAlex (work lookup, referenced_works, cited_by
query) and Semantic Scholar (/citations, /references). Calls are paced at least
3.5 s apart; on HTTP 429 it waits 30, 45, then 60 s; each leg is tried at most
three times and then recorded as 'not done'. Raw JSON pages are written to
<out_dir>/raw/, and a leg log is written to <out_dir>/chase_log.csv, with
<out_dir>/chase_works.csv listing every work returned (seed, direction, tool,
id, title, year, venue).
Standard library only.
"""
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

import os as _os
# Contact for API "polite pools": set the MAILTO environment variable to your own address.
# It is deliberately not hardcoded (redacted 2026-10-19).
MAILTO = _os.environ.get("MAILTO", "")
UA = "idea06-novelty-check/1.0" + (" (mailto:%s)" % MAILTO if MAILTO else "")
PACE = 3.5
BACKOFF = [30, 45, 60]

SEEDS = [
    # key, arXiv id or DOI, legs requested by the plan
    ("christodoulou2025", "arxiv", "2505.04720", ["backward", "forward"]),
    ("bean2025", "arxiv", "2511.04703", ["forward"]),
    ("gross2020", "doi", "10.1007/978-3-030-55958-8_1", ["forward"]),
    ("dewynter_awes2024", "arxiv", "2408.15409", ["backward", "forward"]),
    ("miller2024", "arxiv", "2411.00640", ["forward"]),
    ("bowyer2025", "arxiv", "2503.01747", ["forward"]),
]

_last = [0.0]


def get(url):
    """GET with pacing and up to three attempts. Returns (status, body or None, attempts)."""
    attempts = 0
    status = None
    for i in range(3):
        wait = PACE - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        attempts += 1
        _last[0] = time.time()
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.status, r.read().decode("utf-8", "replace"), attempts
        except urllib.error.HTTPError as e:
            status = e.code
            if e.code == 429 and i < 2:
                time.sleep(BACKOFF[i])
                continue
            if e.code == 404:
                return 404, None, attempts
            if i < 2:
                time.sleep(BACKOFF[i])
                continue
        except Exception as e:  # network errors
            status = "ERR:" + type(e).__name__
            if i < 2:
                time.sleep(BACKOFF[i])
                continue
    return status, None, attempts


def save(out, name, body):
    with open(os.path.join(out, "raw", name), "w", encoding="utf-8") as f:
        f.write(body)


def oa_work(out, key, kind, ident, log):
    if kind == "arxiv":
        doi = "10.48550/arxiv." + ident
    else:
        doi = ident
    url = ("https://api.openalex.org/works/doi:" + urllib.parse.quote(doi)
           + "?select=id,display_name,publication_year,referenced_works,cited_by_count,cited_by_api_url,locations"
           + "&mailto=" + MAILTO)
    st, body, n = get(url)
    log.append([key, "lookup", "OpenAlex", url, st, n, ""])
    if body is None:
        return None
    save(out, f"oa_{key}_work.json", body)
    return json.loads(body)


def oa_cited_by(out, key, wid, log, works):
    short = wid.rsplit("/", 1)[-1]
    rows = []
    cursor = "*"
    page = 0
    while cursor and page < 10:
        url = ("https://api.openalex.org/works?filter=cites:" + short
               + "&select=id,display_name,publication_year,primary_location,doi&per-page=200&cursor="
               + urllib.parse.quote(cursor) + "&mailto=" + MAILTO)
        st, body, n = get(url)
        log.append([key, "forward", "OpenAlex", url, st, n, ""])
        if body is None:
            return None
        save(out, f"oa_{key}_citedby_p{page}.json", body)
        d = json.loads(body)
        for w in d.get("results", []):
            venue = ((w.get("primary_location") or {}).get("source") or {}) or {}
            rows.append([key, "forward", "OpenAlex", w.get("id"), w.get("doi") or "",
                         w.get("display_name"), w.get("publication_year"), venue.get("display_name", "")])
        cursor = d.get("meta", {}).get("next_cursor")
        page += 1
        if not d.get("results"):
            break
    works.extend(rows)
    return len(rows)


def oa_refs(out, key, refs, log, works):
    """Resolve referenced_works ids to titles in batches of 50."""
    got = 0
    for i in range(0, len(refs), 50):
        ids = "|".join(r.rsplit("/", 1)[-1] for r in refs[i:i + 50])
        url = ("https://api.openalex.org/works?filter=openalex:" + ids
               + "&select=id,display_name,publication_year,primary_location,doi&per-page=50&mailto=" + MAILTO)
        st, body, n = get(url)
        log.append([key, "backward", "OpenAlex", url[:200], st, n, ""])
        if body is None:
            return None
        save(out, f"oa_{key}_refs_{i}.json", body)
        for w in json.loads(body).get("results", []):
            venue = ((w.get("primary_location") or {}).get("source") or {}) or {}
            works.append([key, "backward", "OpenAlex", w.get("id"), w.get("doi") or "",
                          w.get("display_name"), w.get("publication_year"), venue.get("display_name", "")])
            got += 1
    return got


def s2(out, key, kind, ident, direction, log, works):
    pid = ("arXiv:" + ident) if kind == "arxiv" else ("DOI:" + ident)
    ep = "citations" if direction == "forward" else "references"
    field = "citingPaper" if direction == "forward" else "citedPaper"
    url = ("https://api.semanticscholar.org/graph/v1/paper/" + urllib.parse.quote(pid, safe=":")
           + f"/{ep}?fields=title,year,venue,externalIds&limit=1000")
    st, body, n = get(url)
    log.append([key, direction, "SemanticScholar", url, st, n, ""])
    if body is None:
        return None
    save(out, f"s2_{key}_{ep}.json", body)
    d = json.loads(body)
    c = 0
    for row in d.get("data", []):
        p = row.get(field) or {}
        ext = p.get("externalIds") or {}
        works.append([key, direction, "SemanticScholar", p.get("paperId"), ext.get("DOI") or ext.get("ArXiv") or "",
                      p.get("title"), p.get("year"), p.get("venue")])
        c += 1
    return c


def main():
    out = sys.argv[1]
    os.makedirs(os.path.join(out, "raw"), exist_ok=True)
    log, works, summary = [], [], []
    t0 = time.time()
    for key, kind, ident, legs in SEEDS:
        w = oa_work(out, key, kind, ident, log)
        if w is None:
            for leg in legs:
                summary.append([key, leg, "OpenAlex", "not done (lookup failed)", ""])
        else:
            if "backward" in legs:
                refs = w.get("referenced_works") or []
                if not refs:
                    summary.append([key, "backward", "OpenAlex", "done (0 referenced_works deposited)", 0])
                else:
                    g = oa_refs(out, key, refs, log, works)
                    summary.append([key, "backward", "OpenAlex", "done" if g is not None else "not done", g if g is not None else ""])
            if "forward" in legs:
                g = oa_cited_by(out, key, w["id"], log, works)
                summary.append([key, "forward", "OpenAlex",
                                ("done (cited_by_count=%s)" % w.get("cited_by_count")) if g is not None else "not done", g if g is not None else ""])
        for leg in legs:
            g = s2(out, key, kind, ident, leg, log, works)
            summary.append([key, leg, "SemanticScholar", "done" if g is not None else "not done", g if g is not None else ""])
    with open(os.path.join(out, "chase_log.csv"), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["seed", "direction", "tool", "url", "http_status", "attempts", "note"])
        wr.writerows(log)
    with open(os.path.join(out, "chase_summary.csv"), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["seed", "direction", "tool", "status", "n_works"])
        wr.writerows(summary)
    with open(os.path.join(out, "chase_works.csv"), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["seed", "direction", "tool", "id", "doi_or_arxiv", "title", "year", "venue"])
        wr.writerows(works)
    print("elapsed_s", round(time.time() - t0, 1))
    for s in summary:
        print(s)


if __name__ == "__main__":
    main()
