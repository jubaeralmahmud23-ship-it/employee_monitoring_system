#!/usr/bin/env python3
"""Screen the citation-chasing results (abstracts.jsonl written by chase_citations.py).

Usage:
  python -I screen_chase.py <abstracts.jsonl> <results_dir>

Flags (title + abstract, case-insensitive), fixed before reading the hits:
  WORK   worker/employee/staff/personnel/workforce/clerk/agent(s) (call centre)/resource(s)
         (process mining sense)/event log/process mining/organi[sz]ational mining/people analytics
  PROF   individual-professional profiling analogues: physician/surgeon/doctor/teacher/nurse/
         provider profiling/value-added
  STAB   rank/ranking/league table/stability/sensitivity/robust/reliab/misclassif/multiverse/
         specification curve/uncertainty
  PERF   performance/productivity/efficiency/cost profile/quality measure/indicator/score
A work is a 'hit' when (WORK or PROF) and STAB and PERF hold. Every hit is then read by hand
(title and abstract) and classified in the novelty file; non-hits are not read individually.
Writes <results_dir>/chase_screen.csv (seed, direction, tool, doi, title, year, venue,
abstract_available, WORK, PROF, STAB, PERF, hit) and prints counts per seed.
"""
import csv
import json
import os
import re
import sys
from collections import Counter

WORK = re.compile(r"\b(workers?|employees?|staff|personnel|workforce|clerks?|call[- ]cent(er|re)|agents? performance|"
                  r"human resources?|resources? (behaviou?r|performance|profil|productivity)|event logs?|process mining|"
                  r"organi[sz]ational mining|people analytics|workplace|algorithmic management)\b", re.I)
PROF = re.compile(r"\b(physicians?|surgeons?|doctors?|teachers?|nurses?|provider profiling|value[- ]added|clinicians?)\b", re.I)
STAB = re.compile(r"(\brank|league table|stabil|sensitiv|robust|reliab|misclassif|multiverse|specification curve|uncertaint)", re.I)
PERF = re.compile(r"(performance|productivity|efficien|cost profil|quality measure|indicator|score)", re.I)


def main():
    src, res = sys.argv[1], sys.argv[2]
    rows, cnt, hits = [], Counter(), Counter()
    for line in open(src, encoding="utf-8"):
        d = json.loads(line)
        text = (d.get("title") or "") + " " + (d.get("abstract") or "")
        w, p, s, f = (bool(r.search(text)) for r in (WORK, PROF, STAB, PERF))
        hit = (w or p) and s and f
        key = (d["seed"], d["direction"], d["tool"])
        cnt[key] += 1
        hits[key] += hit
        rows.append([d["seed"], d["direction"], d["tool"], (d.get("doi") or "").replace("https://doi.org/", ""),
                     (d.get("title") or "").replace("\n", " "), d.get("year"), d.get("venue") or "",
                     "yes" if d.get("abstract") else "no", int(w), int(p), int(s), int(f), int(hit)])
    with open(os.path.join(res, "chase_screen.csv"), "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh)
        wr.writerow(["seed", "direction", "tool", "doi", "title", "year", "venue", "abstract_available",
                     "WORK", "PROF", "STAB", "PERF", "hit"])
        wr.writerows(rows)
    for k in cnt:
        print(k, "works", cnt[k], "hits", hits[k])


if __name__ == "__main__":
    main()
