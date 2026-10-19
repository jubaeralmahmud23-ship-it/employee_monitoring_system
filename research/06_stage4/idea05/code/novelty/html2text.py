#!/usr/bin/env python3
"""Reduce a downloaded HTML page to plain text (standard library only).
Usage: python -I html2text.py <in.html> <out.txt>"""
import html
import html.parser
import sys


class T(html.parser.HTMLParser):
    SKIP = {"script", "style", "noscript", "svg", "nav", "header", "footer"}

    def __init__(self):
        super().__init__()
        self.out, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
        if tag in ("p", "div", "br", "h1", "h2", "h3", "h4", "li", "tr", "section", "table"):
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


p = T()
p.feed(open(sys.argv[1], encoding="utf-8", errors="replace").read())
t = html.unescape("".join(p.out))
t = "\n".join(line.strip() for line in t.splitlines() if line.strip())
open(sys.argv[2], "w", encoding="utf-8").write(t)
print(len(t))
