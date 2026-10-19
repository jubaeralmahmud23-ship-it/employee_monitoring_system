#!/usr/bin/env python3
"""Proceedings sweep for the idea 5 deep novelty check (research/02_candidate_ideas.md
section 4.2: ICPM, BPM, CAiSE and Process Science papers 2022-2026 on resource
performance stability, sensitivity, ranking or reliability).

dblp answered every request with an Anubis 'Making sure you're not a bot!' page on
2026-10-19, so the sweep enumerates the venues through Crossref instead:
  * Springer proceedings volumes by ISBN (filter isbn:<ISBN>, type book-chapter), the
    volume list being the Crossref book records found on 2026-10-19 (VOLUMES below);
  * IEEE ICPM main-conference proceedings 2022-2025 by exact container-title
    (query.container-title + prefix 10.1109, post-filtered on the exact title);
  * the Springer journal Process Science by ISSN 2948-2178.
Abstracts: Crossref when deposited; otherwise Semantic Scholar's POST /paper/batch
(500 DOIs per call), then OpenAlex (filter doi:..., 50 per call) for the remainder. Pacing
3.5 s; on 429 wait 30/45/60 s; at most three attempts per call.

Usage:
  python -I proceedings_sweep.py <raw_dir> <results_dir> [--no-enrich]

Outputs (results_dir): sweep_volumes.csv (volume, ISBN, items found), sweep_papers.csv
(venue, year, doi, title, abstract_source, screen flags), sweep_log.csv (HTTP calls).
Abstract text is kept in raw_dir/sweep_abstracts.jsonl only. Standard library only.
"""
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "idea05-novelty-check/1.0 (academic use; contact via repository owner)"
PACE = 3.5
BACKOFF = [30, 45, 60]

# venue label, volume title, publication year in Crossref, both ISBNs (print, electronic)
VOLUMES = [
    ("BPM", "Business Process Management (BPM 2022)", 2022, ["9783031161025", "9783031161032"]),
    ("BPM", "Business Process Management (BPM 2023)", 2023, ["9783031416194", "9783031416200"]),
    ("BPM", "Business Process Management (BPM 2024)", 2024, ["9783031703959", "9783031703966"]),
    ("BPM", "Business Process Management (BPM 2025)", 2026, ["9783032028662", "9783032028679"]),
    ("BPM", "Business Process Management (BPM 2026)", 2027, ["9783032377760", "9783032377777"]),
    ("BPM Forum", "Business Process Management Forum 2022", 2022, ["9783031161704", "9783031161711"]),
    ("BPM Forum", "Business Process Management Forum 2023", 2023, ["9783031416224", "9783031416231"]),
    ("BPM Forum", "Business Process Management Forum 2024", 2024, ["9783031704178", "9783031704185"]),
    ("BPM Forum", "Business Process Management Forum 2025", 2026, ["9783032029287", "9783032029294"]),
    ("BPM Forum", "Business Process Management Forum 2026", 2027, ["9783032378767", "9783032378774"]),
    ("BPM Workshops", "BPM Workshops 2021 (published 2022)", 2022, ["9783030943424", "9783030943431"]),
    ("BPM Workshops", "BPM Workshops 2022", 2023, ["9783031253829", "9783031253836"]),
    ("BPM Workshops", "BPM Workshops 2023", 2024, ["9783031509735", "9783031509742"]),
    ("BPM Workshops", "BPM Workshops 2024", 2025, ["9783031786655", "9783031786662"]),
    ("BPM Workshops", "BPM Workshops 2025", 2026, ["9783032134257", "9783032134264"]),
    ("BPM other forums", "BPM Blockchain, RPA and CEE Forum 2022", 2022, ["9783031161674", "9783031161681"]),
    ("BPM other forums", "BPM Blockchain, RPA and Educators Forum 2023", 2023, ["9783031434327", "9783031434334"]),
    ("BPM other forums", "BPM Blockchain, RPA, CEE, Educators and PM Forum 2024", 2024, ["9783031704444", "9783031704451"]),
    ("BPM other forums", "BPM Responsible BPM, Process Technology, Educators Forum 2025", 2026, ["9783032029355", "9783032029362"]),
    ("BPM other forums", "BPM Responsible BPM, Process Technology, Educators Forum 2026", 2027, ["9783032367099", "9783032367105"]),
    ("CAiSE", "Advanced Information Systems Engineering (CAiSE 2022)", 2022, ["9783031074714", "9783031074721"]),
    ("CAiSE", "Advanced Information Systems Engineering (CAiSE 2023)", 2023, ["9783031345593", "9783031345609"]),
    ("CAiSE", "Advanced Information Systems Engineering (CAiSE 2024)", 2024, ["9783031610561", "9783031610578"]),
    ("CAiSE", "Advanced Information Systems Engineering (CAiSE 2025, part 1)", 2025, ["9783031945687", "9783031945694"]),
    ("CAiSE", "Advanced Information Systems Engineering (CAiSE 2025, part 2)", 2025, ["9783031945731", "9783031945717"]),
    ("CAiSE", "Advanced Information Systems Engineering (CAiSE 2026, part 1)", 2026, ["9783032281098", "9783032281104"]),
    ("CAiSE", "Advanced Information Systems Engineering (CAiSE 2026, part 2)", 2026, ["9783032281166", "9783032281173"]),
    ("CAiSE Workshops", "CAiSE Workshops 2022", 2022, ["9783031074776", "9783031074783"]),
    ("CAiSE Workshops", "CAiSE Workshops 2023", 2023, ["9783031349843", "9783031349850"]),
    ("CAiSE Workshops", "CAiSE Workshops 2024", 2024, ["9783031610028", "9783031610035"]),
    ("CAiSE Workshops", "CAiSE Workshops 2025", 2025, ["9783031949302", "9783031949319"]),
    ("CAiSE Workshops", "CAiSE Workshops 2026", 2026, ["9783032281593", "9783032281609"]),
    ("CAiSE Forum", "Intelligent Information Systems (CAiSE Forum 2022)", 2022, ["9783031074806", "9783031074813"]),
    ("CAiSE Forum", "Intelligent Information Systems (CAiSE Forum 2023)", 2023, ["9783031346736", "9783031346743"]),
    ("CAiSE Forum", "Intelligent Information Systems (CAiSE Forum 2024)", 2024, ["9783031609992", "9783031610004"]),
    ("CAiSE Forum", "Intelligent Information Systems (CAiSE Forum 2025)", 2025, ["9783031945892", "9783031945908"]),
    ("CAiSE Forum", "Intelligent Information Systems (CAiSE Forum 2026)", 2026, ["9783032279965", "9783032279972"]),
    ("ICPM Workshops", "Process Mining Workshops (ICPM 2021)", 2022, ["9783030985806", "9783030985813"]),
    ("ICPM Workshops", "Process Mining Workshops (ICPM 2022)", 2023, ["9783031278143", "9783031278150"]),
    ("ICPM Workshops", "Process Mining Workshops (ICPM 2023)", 2024, ["9783031561061", "9783031561078"]),
    ("ICPM Workshops", "Process Mining Workshops (ICPM 2024)", 2025, ["9783031822247", "9783031822254"]),
]
ICPM_IEEE = [
    ("ICPM", "2022 4th International Conference on Process Mining (ICPM)", 2022),
    ("ICPM", "2023 5th International Conference on Process Mining (ICPM)", 2023),
    ("ICPM", "2024 6th International Conference on Process Mining (ICPM)", 2024),
    ("ICPM", "2025 7th International Conference on Process Mining (ICPM)", 2025),
]
PROCESS_SCIENCE_ISSN = "2948-2178"

# ---- screening terms (fixed before the sweep was run) ----
PLAN_TERMS = ["resource", "performance", "stability", "sensitivity", "ranking", "reliability"]
R_ACTOR = re.compile(r"\b(resource|resources|worker|workers|employee|employees|staff|human|humans|actor|actors|"
                     r"people|personnel|workforce|clerk|clerks|agent productivity|organi[sz]ational mining|"
                     r"organi[sz]ational perspective|performer|performers|user behaviou?r|team|teams)\b", re.I)
R_MEASURE = re.compile(r"(performance|productivity|efficien|workload|utili[sz]ation|behaviou?r|profil|"
                       r"evaluat|assess|indicator|kpi|metric|measure)", re.I)
R_ROBUST = re.compile(r"(stabil|sensitiv|reliab|robust|ranking|\brank|misclassif|multiverse|uncertaint|"
                      r"fair|bias|discriminat|validity|valid\b|consisten|agree)", re.I)

_last = [0.0]
LOG = []


def http(url, data=None):
    for i in range(3):
        wait = PACE - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        hdr = {"User-Agent": UA, "Accept": "application/json"}
        if data is not None:
            hdr["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=data, headers=hdr)
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                LOG.append([url[:200], r.status, i + 1])
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            LOG.append([url[:200], e.code, i + 1])
            if e.code == 404:
                return None
        except Exception as e:
            LOG.append([url[:200], "ERR:" + type(e).__name__, i + 1])
        if i < 2:
            time.sleep(BACKOFF[i])
    return None


def clean(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", s).strip()


def crossref_items(filters, extra=""):
    items, cursor = [], "*"
    while cursor:
        url = ("https://api.crossref.org/works?filter=" + filters + extra + "&rows=1000&cursor="
               + urllib.parse.quote(cursor) + "&select=DOI,title,container-title,issued,type,abstract,author,page"
              )
        body = http(url)
        if body is None:
            return None
        m = json.loads(body)["message"]
        items.extend(m["items"])
        if len(m["items"]) < 1000:
            break
        cursor = m.get("next-cursor")
    return items


def main():
    raw, res = sys.argv[1], sys.argv[2]
    enrich = "--no-enrich" not in sys.argv
    os.makedirs(raw, exist_ok=True)
    os.makedirs(res, exist_ok=True)
    papers, vols = {}, []

    def add(venue, vol, year, it):
        doi = it["DOI"].lower()
        if doi in papers:
            return
        title = clean((it.get("title") or [""])[0])
        papers[doi] = {"venue": venue, "volume": vol, "year": year, "doi": doi, "title": title,
                       "abstract": clean(it.get("abstract", "")), "abstract_source": "crossref" if it.get("abstract") else ""}

    for venue, vol, year, isbns in VOLUMES:
        found = None
        for isbn in isbns:
            items = crossref_items("isbn:" + isbn + ",type:book-chapter")
            if items:
                found = (isbn, items)
                break
        n = 0
        if found:
            for it in found[1]:
                add(venue, vol, year, it)
                n += 1
        vols.append([venue, vol, year, found[0] if found else "|".join(isbns), n])
        print(vol, n, flush=True)

    for venue, cont, year in ICPM_IEEE:
        url = ("https://api.crossref.org/works?query.container-title=" + urllib.parse.quote(cont)
               + "&filter=prefix:10.1109,type:proceedings-article&rows=1000&select=DOI,title,container-title,issued,type,abstract")
        body = http(url)
        n = 0
        if body:
            for it in json.loads(body)["message"]["items"]:
                if (it.get("container-title") or [""])[0] == cont:
                    add(venue, cont, year, it)
                    n += 1
        vols.append([venue, cont, year, "container-title exact", n])
        print(cont, n, flush=True)

    items = crossref_items("issn:" + PROCESS_SCIENCE_ISSN)
    n = 0
    for it in items or []:
        yr = ((it.get("issued") or {}).get("date-parts") or [[None]])[0][0]
        add("Process Science", "Process Science (journal)", yr, it)
        n += 1
    vols.append(["Process Science", "Process Science (journal)", "2024-2026", "issn:" + PROCESS_SCIENCE_ISSN, n])
    print("Process Science", n, flush=True)

    # ---- abstract enrichment ----
    if enrich:
        missing = [d for d, p in papers.items() if not p["abstract"]]
        for i in range(0, len(missing), 500):
            chunk = missing[i:i + 500]
            body = http("https://api.semanticscholar.org/graph/v1/paper/batch?fields=title,abstract,year,venue",
                        json.dumps({"ids": ["DOI:" + d for d in chunk]}).encode())
            if body is None:
                continue
            for d, rec in zip(chunk, json.loads(body)):
                if rec and rec.get("abstract"):
                    papers[d]["abstract"] = clean(rec["abstract"])
                    papers[d]["abstract_source"] = "semanticscholar"
        missing = [d for d, p in papers.items() if not p["abstract"]]
        for i in range(0, len(missing), 50):
            chunk = missing[i:i + 50]
            url = ("https://api.openalex.org/works?filter=doi:" + "|".join(urllib.parse.quote(d, safe="/") for d in chunk)
                   + "&select=doi,abstract_inverted_index&per-page=50")
            body = http(url)
            if body is None:
                continue
            for w in json.loads(body).get("results", []):
                inv = w.get("abstract_inverted_index")
                d = (w.get("doi") or "").replace("https://doi.org/", "").lower()
                if inv and d in papers:
                    pos = sorted((k, t) for t, ks in inv.items() for k in ks)
                    papers[d]["abstract"] = " ".join(t for _, t in pos)
                    papers[d]["abstract_source"] = "openalex"

    # ---- screening ----
    rows = []
    with open(os.path.join(raw, "sweep_abstracts.jsonl"), "w", encoding="utf-8") as f:
        for p in papers.values():
            text = p["title"] + " " + p["abstract"]
            low = text.lower()
            plan_hits = [t for t in PLAN_TERMS if t in low]
            actor = bool(R_ACTOR.search(text))
            measure = bool(R_MEASURE.search(text))
            robust = bool(R_ROBUST.search(text))
            stage_a = actor and measure
            stage_b = actor and measure and robust
            title_b = bool(R_ACTOR.search(p["title"])) and bool(R_MEASURE.search(p["title"]) or R_ROBUST.search(p["title"]))
            rows.append([p["venue"], p["volume"], p["year"], p["doi"], p["title"], p["abstract_source"] or "none",
                         ";".join(plan_hits), int(stage_a), int(stage_b), int(title_b)])
            f.write(json.dumps(p) + "\n")
    rows.sort(key=lambda r: (r[0], str(r[2]), r[4]))
    with open(os.path.join(res, "sweep_papers.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["venue", "volume", "year", "doi", "title", "abstract_source", "plan_terms_present",
                    "stage_a_actor_and_measure", "stage_b_actor_measure_robustness", "title_actor_and_measure_or_robust"])
        w.writerows(rows)
    with open(os.path.join(res, "sweep_volumes.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["venue", "volume", "crossref_year", "isbn_or_filter", "items"])
        w.writerows(vols)
    with open(os.path.join(res, "sweep_log.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["url", "http_status", "attempt"])
        w.writerows(LOG)
    n = len(rows)
    print("papers", n, "with abstract", sum(r[5] != "none" for r in rows),
          "stage_a", sum(r[7] for r in rows), "stage_b", sum(r[8] for r in rows), "title_b", sum(r[9] for r in rows))


if __name__ == "__main__":
    main()
