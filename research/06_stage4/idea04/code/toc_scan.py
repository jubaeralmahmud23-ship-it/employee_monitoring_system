"""Keyword screen of a proceedings table of contents for the idea-4 deep novelty check.

Input: a CSV with at least a title column (and optionally an abstract column), or a JSON list of
{title, abstract, url} records. Output: a CSV of records that match at least one keyword family,
with the families matched, for manual reading. Also prints the number of records scanned.

Usage:
  python -I toc_scan.py --in <file> --format csv|json --title-col Title --abstract-col Abstract \
      --source "FAccT 2026" --out <csv>
"""
import argparse
import csv
import json
import re
import sys

FAMILIES = {
    "ll144": r"local law 144|\bll ?144\b|new york city|\bnyc\b|bias audit",
    "hiring": r"hiring|recruit|employment|job applicant|applicant|selection procedure|personnel|automated employment|aedt",
    "fourfifths": r"four[- ]fifths|4/5|80 ?% rule|eighty percent|adverse impact|disparate impact|impact ratio|selection rate",
    "uncertainty": r"confidence interval|uncertaint|sampling|sample size|small sample|statistical power|significance|hypothesis test|bootstrap|bayesian|posterior|error bar",
    "audit_rules": r"audit|exclusion|aggregat|pool|intersectional|threshold|manipulat|gaming|d-hacking|cherry",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--format", choices=["csv", "json"], default="csv")
    ap.add_argument("--title-col", default="Title")
    ap.add_argument("--abstract-col", default="Abstract")
    ap.add_argument("--source", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    csv.field_size_limit(sys.maxsize)
    if args.format == "csv":
        with open(args.inp, newline="", encoding="utf-8") as fh:
            recs = [{"title": r.get(args.title_col, ""), "abstract": r.get(args.abstract_col, ""),
                     "id": r.get("Paper ID", "")} for r in csv.DictReader(fh)]
    else:
        with open(args.inp, encoding="utf-8") as fh:
            recs = json.load(fh)
    comp = {k: re.compile(v, re.I) for k, v in FAMILIES.items()}
    rows = []
    for r in recs:
        text = f"{r.get('title') or ''} {r.get('abstract') or ''}"
        fams = [k for k, rx in comp.items() if rx.search(text)]
        # keep records touching the core of idea 4: LL 144 / hiring / four-fifths, or uncertainty together with audits
        core = ("ll144" in fams) or ("fourfifths" in fams) or ("hiring" in fams and ("uncertainty" in fams or "audit_rules" in fams))
        if core:
            rows.append([args.source, r.get("id", ""), (r.get("title") or "").strip(), ";".join(fams), r.get("url", "")])
    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh)
        wr.writerow(["source", "id", "title", "families", "url"])
        wr.writerows(rows)
    print(f"{args.source}: scanned={len(recs)} matched={len(rows)}")


if __name__ == "__main__":
    main()
