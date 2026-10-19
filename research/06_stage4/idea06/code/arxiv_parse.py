"""Print id, date, title, comment, journal_ref and abstract for each entry of an
arXiv API Atom response.

Usage:
  python -I arxiv_parse.py <atom.xml> [--short]
Standard library only.
"""
import sys
import xml.etree.ElementTree as ET

NS = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}


def main():
    root = ET.parse(sys.argv[1]).getroot()
    short = "--short" in sys.argv
    tot = root.find("{http://a9.com/-/spec/opensearch/1.1/}totalResults")
    if tot is not None:
        print("totalResults", tot.text)
    for e in root.findall("a:entry", NS):
        title = " ".join((e.find("a:title", NS).text or "").split())
        c = e.find("x:comment", NS)
        j = e.find("x:journal_ref", NS)
        print("ID", e.find("a:id", NS).text, "|", (e.find("a:published", NS).text or "")[:10])
        print("T", title)
        if not short:
            print("C", c.text if c is not None else "", "| J", j.text if j is not None else "")
            print("A", " ".join((e.find("a:summary", NS).text or "").split()))
        print()


if __name__ == "__main__":
    main()
