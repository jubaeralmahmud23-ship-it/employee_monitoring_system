#!/usr/bin/env python3
"""Fetch pilot full texts and Springer landing pages (idea 6). Standard library + pdftotext.

1. For each pilot paper (results/pilot/pilot_sample.csv) download the PDF into its own new
   directory <papers-root>/<pilot_id>/paper.pdf and convert it with `pdftotext -layout`
   (pages are separated by form feeds, so page numbers are recoverable).
2. For each CC-licensed Springer term hit (results/frame/springer_oa_term_hits.csv) fetch
   the article landing page into <landing-root>/<doi-slug>.html and extract the abstract
   (meta dc.description) for inclusion screening. Abstracts stay outside the repository.
Downloads are untrusted data: nothing in them is executed; paths are passed as arguments.
"""
import argparse
import csv
import hashlib
import html
import os
import re
import subprocess
import sys
import time

UA = "idea06-pilot/1.0 (academic research pilot; curl)"


def get(url, tries=3, delay=2.0):
    """GET via curl (link.springer.com serves a JavaScript 'Client Challenge' page to
    python-urllib but the article or PDF to curl; observed 2026-10-19)."""
    last = b""
    for i in range(tries):
        time.sleep(delay)
        p = subprocess.run(["curl", "-sS", "-L", "--max-time", "120", "-A", UA,
                            "-w", "\n%{http_code}|%{content_type}|%{url_effective}", url],
                           capture_output=True)
        body, _, meta = p.stdout.rpartition(b"\n")
        try:
            code, ct, final = meta.decode("utf-8", "replace").split("|", 2)
            code = int(code)
        except ValueError:
            code, ct, final = -1, "", url
        if code == 200 and b"<title>Client Challenge</title>" not in body[:3000]:
            return code, ct, final, body
        last = body[:200] or p.stderr
        print(f"  retry {i+1} {url}: http {code}", file=sys.stderr)
        time.sleep(10 * (i + 1))
    return -1, "", url, last


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot-csv", required=True)
    ap.add_argument("--springer-oa-csv", required=True)
    ap.add_argument("--papers-root", required=True)
    ap.add_argument("--landing-root", required=True)
    ap.add_argument("--manifest-out", required=True)
    ap.add_argument("--abstracts-out", required=True, help="CSV outside the repository")
    a = ap.parse_args()
    man = []
    for r in csv.DictReader(open(a.pilot_csv, encoding="utf-8")):
        d = os.path.join(a.papers_root, r["pilot_id"])
        os.makedirs(d, exist_ok=True)
        pdf = os.path.join(d, "paper.pdf")
        t0 = time.time()
        if not os.path.exists(pdf):
            st, ct, final, body = get(r["fulltext_url"])
            if st == 200 and body[:4] == b"%PDF":
                open(pdf, "wb").write(body)
        else:
            st, ct, final = 200, "application/pdf (cached)", r["fulltext_url"]
        ok = os.path.exists(pdf)
        pages = ""
        if ok:
            subprocess.run(["pdftotext", "-layout", pdf, os.path.join(d, "paper.txt")], check=True)
            txt = open(os.path.join(d, "paper.txt"), encoding="utf-8", errors="replace").read()
            pages = txt.count("\f")
        man.append({"pilot_id": r["pilot_id"], "url": r["fulltext_url"], "http": st, "content_type": ct,
                    "final_url": final[:200], "bytes": os.path.getsize(pdf) if ok else 0,
                    "sha256": hashlib.sha256(open(pdf, "rb").read()).hexdigest() if ok else "",
                    "pdf_pages_by_formfeed": pages, "fetch_seconds": round(time.time() - t0, 1)})
        print(man[-1]["pilot_id"], st, man[-1]["bytes"], pages, file=sys.stderr)
    with open(a.manifest_out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(man[0].keys()))
        w.writeheader()
        w.writerows(man)

    os.makedirs(a.landing_root, exist_ok=True)
    out = []
    for r in csv.DictReader(open(a.springer_oa_csv, encoding="utf-8")):
        slug = r["doi"].replace("/", "_")
        p = os.path.join(a.landing_root, slug + ".html")
        if not os.path.exists(p):
            st, ct, final, body = get("https://link.springer.com/article/" + r["doi"])
            if st == 200:
                open(p, "wb").write(body)
        h = open(p, encoding="utf-8", errors="replace").read() if os.path.exists(p) else ""
        m = re.search(r'<meta name="dc.description" content="([^"]*)"', h)
        abstract = html.unescape(m.group(1)) if m else ""
        art_type = re.search(r'<meta name="citation_article_type" content="([^"]*)"', h)
        out.append({"doi": r["doi"], "journal": r["journal"], "year": r["year_issued"], "title": r["title"],
                    "article_type_meta": html.unescape(art_type.group(1)) if art_type else "",
                    "abstract_source": "springer landing dc.description" if abstract else "none",
                    "abstract": abstract,
                    "landing_sha256": hashlib.sha256(h.encode("utf-8", "replace")).hexdigest() if h else ""})
    with open(a.abstracts_out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    print(f"landing pages: {len(out)}; with abstract: {sum(1 for o in out if o['abstract'])}", file=sys.stderr)


if __name__ == "__main__":
    main()
