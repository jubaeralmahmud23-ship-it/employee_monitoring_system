#!/usr/bin/env python3
"""Machine assistance for the pilot coder: keyword-in-context with PDF page indices.

Reads a pdftotext -layout file (pages separated by form feeds) and prints, for each
codebook item, the lines that match the item's keyword pattern, with the 1-based PDF page
index and section-like headings seen on that page. The coder reads these hits (and the
surrounding pages) and decides the codes; this script decides nothing.

Usage: python -I kwic.py <paper.txt> [--item ITEM] [--context N] [--max M]
"""
import argparse
import re

PATTERNS = {
    "n_items": r"\b(test (set|split)|held[- ]out|\d[\d,]* (examples|samples|instances|questions|queries|items|documents|cases|dialogues|conversations|tasks|images|pairs|participants|users|prompts))\b",
    "runs_seeds": r"\b(seed|seeds|runs?\b|repeated|averaged over|mean of|five times|three times|\d+ trials|standard deviation|std\.?|±)",
    "decoding": r"(temperature|top[- _]?p\b|top[- _]?k\b|greedy|nucleus|beam size|max(imum)?[ _]?(new[ _])?tokens|do_sample|sampling)",
    "model_version": r"(gpt-?[345][\w\.\-]*|gpt-4o[\w\-]*|claude[\w\-\. ]*|gemini[\w\-\. ]*|llama[\w\-\. ]*|qwen[\w\-\. ]*|mistral[\w\-\. ]*|mixtral[\w\-\. ]*|deepseek[\w\-\. ]*|phi-?\d[\w\-]*|bert[\w\-]*|t5[\w\-]*|accessed|snapshot|checkpoint)",
    "prompts": r"(prompt template|prompts? (are|is) (shown|provided|listed|given)|appendix|system prompt|few-shot|zero-shot|instruction)",
    "uncertainty": r"(confidence interval|\bCI\b|standard error|\bSE\b|error bar|p\s*[<=>]\s*0?\.\d|p-value|significan|t-test|wilcoxon|bootstrap|mcnemar|permutation test|±|\+/-|credible)",
    "llm_judge": r"(llm[- ]as[- ]a[- ]judge|as a judge|judge|gpt-4 (eval|as)|g-eval|auto(matic)? evaluat|llm-based evaluat|evaluator)",
    "human_validation": r"(human (evaluation|annotat|judg|rater|expert)|annotators?|inter[- ]?(rater|annotator)|agreement|kappa|krippendorff|alpha|correlat|spearman|pearson|kendall)",
    "contamination": r"(contaminat|leak|training data (overlap|cutoff)|knowledge cutoff|memori[sz])",
    "code_data": r"(github|huggingface|hugging face|zenodo|osf\.io|available at|open[- ]source|release[ds]?|publicly available|upon request|on request)",
    "headline": r"(outperform|improv|accuracy|achiev|increase|reduc|better than|compared to|vs\.?|surpass|gain|%)",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("txt")
    ap.add_argument("--item", default="all")
    ap.add_argument("--max", type=int, default=25)
    ap.add_argument("--pages", default="", help="e.g. 1-2 to restrict pages")
    a = ap.parse_args()
    text = open(a.txt, encoding="utf-8", errors="replace").read()
    pages = text.split("\f")
    lo, hi = 1, len(pages)
    if a.pages:
        lo, hi = (int(x) for x in a.pages.split("-"))
    items = PATTERNS if a.item == "all" else {a.item: PATTERNS[a.item]}
    for name, pat in items.items():
        rx = re.compile(pat, re.I)
        n = 0
        print(f"=== {name}")
        for pi in range(lo - 1, min(hi, len(pages))):
            for line in pages[pi].splitlines():
                if rx.search(line):
                    n += 1
                    if n <= a.max:
                        flat = re.sub(r"\s+", " ", line).strip()[:220]
                        print(f"  p.{pi+1}: {flat}")
        print(f"  ({n} matching lines)")


if __name__ == "__main__":
    main()
