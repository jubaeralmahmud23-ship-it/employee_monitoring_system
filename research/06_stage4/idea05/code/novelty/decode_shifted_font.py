#!/usr/bin/env python3
"""Repair pdftotext output whose embedded font maps glyphs to ASCII code minus 29
(seen in the Kelemen 2022 OCG PDF: ',QWURGXFWLRQ' -> 'Introduction').
Lines with few lowercase letters are shifted back by +29; other lines are kept.
Usage: python -I decode_shifted_font.py <in.txt> <out.txt>"""
import sys

out = []
for line in open(sys.argv[1], encoding="utf-8", errors="replace").read().split("\n"):
    letters = [c for c in line if c.isalpha()]
    low = sum(c.islower() for c in letters)
    if len(letters) >= 6 and low / len(letters) < 0.2:
        line = "".join(chr(ord(c) + 29) if (c not in " \f\t" and 0 < ord(c) + 29 < 127) else c for c in line)
    out.append(line)
open(sys.argv[2], "w", encoding="utf-8").write("\n".join(out))
