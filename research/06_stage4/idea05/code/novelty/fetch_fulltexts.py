#!/usr/bin/env python3
"""Fetch the 'full texts to read first' named in research/02_candidate_ideas.md section 4.2
(idea 5) when an open copy is reachable, plus Crossref records for every item.

Usage:
  python -I fetch_fulltexts.py <download_root> <results_dir>

Each download goes into its own new directory <download_root>/<key>/ ; PDFs are converted
with `pdftotext -layout` (pages separated by form feeds) and HTML pages are reduced to text
with the standard-library HTML parser. Nothing in the downloads is executed.
Writes <results_dir>/fulltext_manifest.csv (key, url, http status, bytes, sha256, text chars,
pages) and <results_dir>/crossref_records.csv (DOI, title, container, year, reference count
deposited). Raw Crossref JSON is kept next to the downloads, not in the repository.
"""
import csv
import hashlib
import html
import html.parser
import json
import os
import subprocess
import sys
import time
import urllib.parse

UA_POLITE = "idea05-novelty-check/1.0 (mailto:jubaeralmahmud23@gmail.com)"
UA_BROWSER = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

# key, url, kind (pdf|html), user agent, DOI of the work
TARGETS = [
    ("adams2010_nejm_pmc", "https://pmc.ncbi.nlm.nih.gov/articles/PMC2878194/", "html", UA_BROWSER, "10.1056/nejmsa0906323"),
    ("adams2012_rhq_pmc", "https://pmc.ncbi.nlm.nih.gov/articles/PMC4945285/", "html", UA_BROWSER, "10.7249/rhq-02-01-03"),
    ("gu_koenker_arxiv", "https://arxiv.org/pdf/2012.12550", "pdf", UA_POLITE, "10.3982/ecta19304"),
    ("nakatumba2010_author", "https://www.vdaalst.com/publications/p585.pdf", "pdf", UA_BROWSER, "10.1007/978-3-642-12186-9_8"),
    ("goldstein1996_bristol", "https://www.bristol.ac.uk/media-library/sites/cmm/migrated/documents/limitations-of-league-tables.pdf", "pdf", UA_BROWSER, "10.2307/2983325"),
    ("kelemen2022_oa", "https://ejournals.facultas.at/index.php/ocgcp/article/download/2098/1753", "pdf", UA_BROWSER, "10.24989/ocg.v335.41"),
    ("martin_beerepoot2024_springer", "https://link.springer.com/article/10.1007/s12599-024-00894-3", "html", UA_POLITE, "10.1007/s12599-024-00894-3"),
    ("saisana2005_oup", "https://academic.oup.com/jrsssa/article-abstract/168/2/307/7084307", "html", UA_POLITE, "10.1111/j.1467-985x.2005.00350.x"),
    ("papay2011_sage", "https://journals.sagepub.com/doi/10.3102/0002831210362589", "html", UA_POLITE, "10.3102/0002831210362589"),
]

CROSSREF_ONLY = [
    "10.1145/3041218",  # Pika et al. 2017 (seed for forward chasing)
]


class _Text(html.parser.HTMLParser):
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


def curl(url, ua, dest):
    p = subprocess.run(["curl", "-sS", "-L", "--max-time", "180", "-A", ua, "-o", dest,
                        "-w", "%{http_code}|%{content_type}|%{url_effective}", url],
                       capture_output=True, text=True)
    try:
        code, ct, final = p.stdout.split("|", 2)
        return int(code), ct, final, p.stderr.strip()
    except ValueError:
        return -1, "", url, p.stderr.strip()


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    root, res = sys.argv[1], sys.argv[2]
    os.makedirs(res, exist_ok=True)
    rows = []
    for key, url, kind, ua, doi in TARGETS:
        d = os.path.join(root, key)
        os.makedirs(d, exist_ok=True)
        raw = os.path.join(d, "source." + ("pdf" if kind == "pdf" else "html"))
        code, ct, final, err = curl(url, ua, raw)
        time.sleep(3)
        size = os.path.getsize(raw) if os.path.exists(raw) else 0
        txt = os.path.join(d, "text.txt")
        chars, pages, note = 0, "", ""
        if code == 200 and size > 0:
            with open(raw, "rb") as f:
                head = f.read(5)
            if head.startswith(b"%PDF"):
                subprocess.run(["pdftotext", "-layout", raw, txt], check=False)
                if os.path.exists(txt):
                    t = open(txt, encoding="utf-8", errors="replace").read()
                    chars, pages = len(t), t.count("\f") + 1
            else:
                b = open(raw, encoding="utf-8", errors="replace").read()
                if "Client Challenge" in b[:3000] or "Just a moment" in b[:3000]:
                    note = "bot challenge page"
                p = _Text()
                p.feed(b)
                t = html.unescape("".join(p.out))
                t = "\n".join(line.strip() for line in t.splitlines() if line.strip())
                open(txt, "w", encoding="utf-8").write(t)
                chars = len(t)
        else:
            note = err[:120]
        rows.append([key, doi, url, final, code, ct, size, sha256(raw) if size else "", chars, pages, note])
        print(rows[-1][:2], code, size, chars, pages, note)
    with open(os.path.join(res, "fulltext_manifest.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["key", "doi", "url", "final_url", "http_status", "content_type", "bytes", "sha256",
                    "text_chars", "pages", "note"])
        w.writerows(rows)

    # Crossref records (metadata, reference-list deposit) for every DOI
    crow = []
    dois = [t[4] for t in TARGETS] + CROSSREF_ONLY
    for doi in dois:
        url = "https://api.crossref.org/works/" + urllib.parse.quote(doi) + "?mailto=jubaeralmahmud23@gmail.com"
        dest = os.path.join(root, "crossref_" + doi.replace("/", "_") + ".json")
        code, ct, final, err = curl(url, UA_POLITE, dest)
        time.sleep(1.5)
        if code != 200:
            crow.append([doi, code, "", "", "", "", "", ""])
            continue
        m = json.load(open(dest, encoding="utf-8"))["message"]
        title = (m.get("title") or [""])[0]
        cont = "; ".join(m.get("container-title") or [])
        year = ((m.get("issued") or {}).get("date-parts") or [[None]])[0][0]
        nref = m.get("reference-count", "")
        ndep = len(m.get("reference") or [])
        has_abs = "yes" if m.get("abstract") else "no"
        crow.append([doi, code, title, cont, year, nref, ndep, has_abs])
    with open(os.path.join(res, "crossref_records.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["doi", "http_status", "title", "container", "year", "reference_count",
                    "references_deposited", "abstract_deposited"])
        w.writerows(crow)
    for r in crow:
        print(r)


if __name__ == "__main__":
    main()
