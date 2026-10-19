#!/usr/bin/env python3
"""Fetch abstracts for the sweep and chase works selected for reading (title-screen hits
and pre-2022 near neighbours), from public landing pages and APIs.

Usage:
  python -I fetch_abstracts.py <doi_list.txt> <download_root> <out_jsonl>

doi_list.txt: one DOI per line (comments after '#'). Order of sources per DOI:
  1. Crossref abstract (api.crossref.org/works/<doi>);
  2. Springer landing page (link.springer.com/chapter|article/<doi>, meta 'dc.description'
     or the Abs1 section), for 10.1007 DOIs;
  3. Semantic Scholar /paper/DOI:<doi>?fields=title,abstract (3 attempts, 30/45/60 s waits).
Each landing page is saved under <download_root>/<doi-slug>.html (untrusted data, not run).
Writes one JSON line per DOI: doi, title, abstract, source. Abstracts stay outside the
repository; the novelty file quotes at most short phrases. Standard library + curl.
"""
import html
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse

UA = "idea05-novelty-check/1.0 (academic use; contact via repository owner)"


def curl(url, dest=None):
    args = ["curl", "-sS", "-L", "--max-time", "90", "-A", UA, "-w", "\n%{http_code}"]
    if dest:
        args += ["-o", dest]
    p = subprocess.run(args + [url], capture_output=True)
    out = p.stdout.decode("utf-8", "replace")
    body, _, code = out.rpartition("\n")
    if dest:
        code = out.strip()
        body = open(dest, encoding="utf-8", errors="replace").read() if os.path.exists(dest) else ""
    try:
        code = int(code)
    except ValueError:
        code = -1
    return code, body


def clean(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def main():
    lst, root, out = sys.argv[1:4]
    os.makedirs(root, exist_ok=True)
    dois = [l.split("#")[0].strip() for l in open(lst, encoding="utf-8")]
    dois = [d for d in dois if d]
    with open(out, "w", encoding="utf-8") as f:
        for doi in dois:
            rec = {"doi": doi, "title": "", "abstract": "", "source": "", "notes": []}
            code, body = curl("https://api.crossref.org/works/" + urllib.parse.quote(doi))
            time.sleep(1.5)
            if code == 200:
                m = json.loads(body)["message"]
                rec["title"] = clean((m.get("title") or [""])[0])
                if m.get("abstract"):
                    rec["abstract"], rec["source"] = clean(m["abstract"]), "crossref"
            rec["notes"].append(f"crossref {code}")
            if not rec["abstract"] and doi.startswith("10.1007/"):
                kind = "chapter" if re.search(r"978-", doi) else "article"
                dest = os.path.join(root, re.sub(r"[^A-Za-z0-9._-]", "_", doi) + ".html")
                code, page = curl(f"https://link.springer.com/{kind}/{doi}", dest)
                time.sleep(2)
                rec["notes"].append(f"springer {code}")
                m = re.search(r'<meta name="dc.description" content="([^"]+)"', page) or \
                    re.search(r'<section[^>]*data-title="Abstract"[^>]*>(.*?)</section>', page, re.S) or \
                    re.search(r'id="Abs1-content"[^>]*>(.*?)</div>', page, re.S)
                if m:
                    rec["abstract"], rec["source"] = clean(m.group(1)), "springer page"
            if not rec["abstract"]:
                for i, wait in enumerate([30, 45, 60]):
                    code, body = curl("https://api.semanticscholar.org/graph/v1/paper/DOI:" + doi + "?fields=title,abstract,venue,year")
                    rec["notes"].append(f"s2 {code}")
                    if code == 200:
                        d = json.loads(body)
                        if d.get("abstract"):
                            rec["abstract"], rec["source"] = clean(d["abstract"]), "semanticscholar"
                        break
                    if code == 404:
                        break
                    if i < 2:
                        time.sleep(wait)
                time.sleep(3.5)
            f.write(json.dumps(rec) + "\n")
            print(doi, rec["source"] or "NONE", "|", rec["title"][:90], "|", ";".join(rec["notes"]), flush=True)


if __name__ == "__main__":
    main()
