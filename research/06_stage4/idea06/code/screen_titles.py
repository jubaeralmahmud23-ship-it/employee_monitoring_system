"""Screen AIS eLibrary proceedings titles for possible meta-research on LLM
evaluation practice.

Usage:
  python -I screen_titles.py <out_csv> <titles_csv> [<titles_csv> ...]

Each input CSV has columns proceedings, track, url, title. A title is flagged
  A: LLM term AND methods/meta-research term;
  B: methods/meta-research term AND review/audit/meta term (any topic), to catch
     field-level audits of research practice that do not name LLMs.
Writes flagged rows with their flag and matched terms, and prints per-
proceedings totals (titles, LLM-term titles, A, B).
Standard library only.
"""
import csv
import re
import sys
from collections import Counter

LLM = re.compile(r"large language model|\bllms?\b|chatgpt|\bgpt|generative ai|genai|generative artificial intelligence|"
                 r"language model|foundation model|llm-as-a-judge|ai judge", re.I)
META = re.compile(r"reporting|reproducib|replicab|replication|error bar|confidence interval|uncertaint|statistical|"
                  r"significance|inter-?rater|inter-?coder|intercoder|kappa|krippendorff|agreement|validity|validation|"
                  r"rigou?r|methodolog|guideline|checklist|meta-?analy|meta-?research|audit|transparen|"
                  r"research practice|evaluation practice|benchmark|evaluat|reliab", re.I)
REVIEW = re.compile(r"review|audit|meta-?analy|meta-?research|state of|landscape|how .* research|research practice|"
                    r"literature|stocktak|taking stock|retrospective|bibliometric|scientometric|we examine .* papers", re.I)
STRICT_META = re.compile(r"reporting|reproducib|replicab|replication|error bar|confidence interval|statistical|"
                         r"inter-?rater|inter-?coder|intercoder|kappa|krippendorff|rigou?r|methodolog|research practice|"
                         r"evaluation practice|meta-?research|guideline|checklist|audit|validity", re.I)


def main():
    out = sys.argv[1]
    rows = []
    for path in sys.argv[2:]:
        with open(path, encoding="utf-8") as f:
            rows.extend(csv.DictReader(f))
    tot, llm_n, a_n, b_n = Counter(), Counter(), Counter(), Counter()
    flagged = []
    for r in rows:
        t = r["title"]
        p = r["proceedings"]
        tot[p] += 1
        has_llm = bool(LLM.search(t))
        if has_llm:
            llm_n[p] += 1
        meta = sorted(set(m.group(0).lower() for m in META.finditer(t)))
        strict = sorted(set(m.group(0).lower() for m in STRICT_META.finditer(t)))
        rev = sorted(set(m.group(0).lower() for m in REVIEW.finditer(t)))
        flag = []
        if has_llm and meta:
            flag.append("A")
            a_n[p] += 1
        if strict and rev:
            flag.append("B")
            b_n[p] += 1
        if flag:
            flagged.append([p, r["track"], r["url"], t, "+".join(flag), ";".join(meta + rev)])
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["proceedings", "track", "url", "title", "flag", "terms"])
        w.writerows(flagged)
    print("proceedings,titles,llm_titles,flag_A,flag_B")
    for p in sorted(tot):
        print(f"{p},{tot[p]},{llm_n[p]},{a_n[p]},{b_n[p]}")
    print("total", sum(tot.values()), sum(llm_n.values()), sum(a_n.values()), sum(b_n.values()))


if __name__ == "__main__":
    main()
