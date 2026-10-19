#!/usr/bin/env python3
"""Keyword-in-context with PDF page numbers for pdftotext output (pages split by form feeds).
Usage: python -I kwic.py <text.txt> <regex> [width]
Prints page<TAB>line<TAB>context for every match (case-insensitive)."""
import re
import sys

path, pat = sys.argv[1], re.compile(sys.argv[2], re.I)
width = int(sys.argv[3]) if len(sys.argv) > 3 else 160
text = open(path, encoding="utf-8", errors="replace").read()
page, lineno = 1, 0
for page_text in text.split("\f"):
    for line in page_text.split("\n"):
        lineno += 1
        if pat.search(line):
            print(f"p{page}\tL{lineno}\t{' '.join(line.split())[:width]}")
    page += 1
