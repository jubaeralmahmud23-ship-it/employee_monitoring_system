#!/usr/bin/env python3
"""Scan the ACLU 'Auditing the Audits' R code for any statistical-inference computation.

Stopping-rule criterion 1 for idea 4, Part 1: does the ACLU code already compute a sampling
interval, standard error, simulation or significance test for the impact ratios?

The scan is a keyword search over every file in --code-dir. It complements (does not replace)
the manual line-by-line reading recorded in research/06_stage4/idea04/README.md.

Usage:
  python -I check_aclu_code.py --code-dir <dir> --out <csv>
"""
import argparse
import csv
import hashlib
import os
import re

# Each pattern targets one family of inference code in R (base, stats, boot, binom, DescTools, ...).
PATTERNS = {
    "binomial test / interval": r"binom|clopper|wilson|agresti|jeffreys",
    "proportion / chi-square / Fisher test": r"prop\.test|chisq|fisher|mcnemar|z[._-]?test",
    "bootstrap / resampling": r"\bboot|resampl|\bsample\(|replicate\(|replicat",
    "random number generation / simulation": r"\brbinom|\brnorm|\brunif|\brbeta|\brmultinom|simulat|set\.seed|monte",
    "normal / beta quantiles": r"\bqnorm|\bpnorm|\bqbeta|\bpbeta|\bqt\(",
    "standard error / variance": r"std\.?err|standard error|\bse\b\s*=|\bsd\(|\bvar\(",
    "confidence / credible interval": r"confint|conf\.int|confidence|credible|interval",
    "p-value / significance": r"p\.value|p-value|pvalue|signific",
    "Bayesian posterior": r"bayes|posterior|\bprior\b",
}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--code-dir", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    files = sorted(
        os.path.join(args.code_dir, f)
        for f in os.listdir(args.code_dir)
        if os.path.isfile(os.path.join(args.code_dir, f))
    )
    rows = []
    for path in files:
        with open(path, encoding="utf-8", errors="replace") as fh:
            lines = fh.read().splitlines()
        n_hits = 0
        for family, pat in PATTERNS.items():
            rx = re.compile(pat, re.IGNORECASE)
            for i, line in enumerate(lines, start=1):
                if rx.search(line):
                    n_hits += 1
                    rows.append({
                        "file": os.path.basename(path),
                        "file_sha256": sha256(path),
                        "n_lines": len(lines),
                        "family": family,
                        "line": i,
                        "text": line.strip()[:160],
                    })
        if n_hits == 0:
            rows.append({
                "file": os.path.basename(path),
                "file_sha256": sha256(path),
                "n_lines": len(lines),
                "family": "(no hit in any family)",
                "line": "",
                "text": "",
            })
    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["file", "file_sha256", "n_lines", "family", "line", "text"])
        w.writeheader()
        w.writerows(rows)
    hits = [r for r in rows if r["line"] != ""]
    print(f"scanned {len(files)} files; {len(hits)} keyword hits")
    for r in hits:
        print(f"  {r['file']}:{r['line']} [{r['family']}] {r['text']}")


if __name__ == "__main__":
    main()
