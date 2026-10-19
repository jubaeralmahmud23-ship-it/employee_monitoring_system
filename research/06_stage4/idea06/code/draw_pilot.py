#!/usr/bin/env python3
"""Draw the 20-paper pilot sample (idea 6) from the frozen frame.

Rule (fixed before any paper was read):
  rng = random.Random(20261015)
  springer = rng.sample(<CC-licensed Springer term hits sorted by DOI>, 10)
  acl      = rng.sample(<all ACL industry papers in the 7 planned volumes, sorted by anthology_id>, 10)
The same generator is used for both draws, in this order. No inclusion screening is applied
before the draw (the plan draws from the term-hit stratum); the pilot coding records inclusion.
"""
import argparse
import csv
import random


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--springer-oa", required=True, help="results/frame/springer_oa_term_hits.csv")
    ap.add_argument("--acl", required=True, help="results/frame/acl_industry_papers.csv")
    ap.add_argument("--seed", type=int, default=20261015)
    ap.add_argument("--k", type=int, default=10)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    sp = sorted(csv.DictReader(open(a.springer_oa, encoding="utf-8")), key=lambda r: r["doi"])
    acl = sorted(csv.DictReader(open(a.acl, encoding="utf-8")), key=lambda r: r["anthology_id"])
    rng = random.Random(a.seed)
    s_pick = rng.sample(sp, a.k)
    a_pick = rng.sample(acl, a.k)
    rows = []
    for i, r in enumerate(s_pick, 1):
        rows.append({"pilot_id": f"S{i:02d}", "stratum": "Springer-OA IS", "key": r["doi"],
                     "venue": r["journal"], "year": r["year_issued"], "title": r["title"],
                     "fulltext_url": f"https://link.springer.com/content/pdf/{r['doi']}.pdf",
                     "landing_url": f"https://link.springer.com/article/{r['doi']}",
                     "license": r["cc_license_urls"]})
    for i, r in enumerate(a_pick, 1):
        rows.append({"pilot_id": f"A{i:02d}", "stratum": "ACL industry", "key": r["anthology_id"],
                     "venue": r["volume"], "year": r["year"], "title": r["title"],
                     "fulltext_url": r["pdf_url"], "landing_url": f"https://aclanthology.org/{r['anthology_id']}/",
                     "license": "CC BY 4.0 (ACL Anthology policy; not re-verified per paper)"})
    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"frame sizes: springer_oa={len(sp)} acl={len(acl)}; seed={a.seed}")
    for r in rows:
        print(r["pilot_id"], r["key"], r["year"], r["title"][:90])


if __name__ == "__main__":
    main()
