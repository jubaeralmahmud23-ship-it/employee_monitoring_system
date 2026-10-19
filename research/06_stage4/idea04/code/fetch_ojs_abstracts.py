"""Fetch abstracts for the AIES 2026 article pages listed in a titles JSON (from the OJS issue pages).

Usage: python -I fetch_ojs_abstracts.py --in <titles.json> --out <with_abstracts.json>
Paces requests 2 s apart; retries a page at most 3 times (30 s wait after HTTP 429/503).
"""
import argparse
import html
import json
import re
import time

import requests

UA = {"User-Agent": "stage4-novelty-check/1.0 (research script; no contact)"}


def get(url):
    for attempt in range(3):
        try:
            r = requests.get(url, headers=UA, timeout=60)
        except requests.RequestException:
            time.sleep(10)
            continue
        if r.status_code == 200:
            return r.text
        time.sleep(30 if r.status_code in (429, 503) else 5)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    recs = json.load(open(args.inp, encoding="utf-8"))
    missing = 0
    for rec in recs:
        t = get(rec["url"])
        time.sleep(2)
        if t is None:
            missing += 1
            continue
        m = re.search(r'<section class="item abstract">(.*?)</section>', t, re.S)
        if m:
            rec["abstract"] = html.unescape(re.sub(r"<[^>]+>|\s+", " ", m.group(1))).replace("Abstract", "", 1).strip()
        a = re.search(r'<meta name="citation_author" content="([^"]+)"', t)
        rec["first_author"] = a.group(1) if a else ""
    json.dump(recs, open(args.out, "w", encoding="utf-8"))
    print(f"records={len(recs)} pages_missing={missing} with_abstract={sum(1 for r in recs if r.get('abstract'))}")


if __name__ == "__main__":
    main()
