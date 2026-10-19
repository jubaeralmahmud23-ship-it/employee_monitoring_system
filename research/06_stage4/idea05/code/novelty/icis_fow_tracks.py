#!/usr/bin/env python3
"""List the papers in the ICIS 'future of work' tracks 2022-2025 from the public AIS eLibrary
browse pages and screen their titles (plan section 4.2: 'the ICIS "IS and the Future of
Work" track listings').

Track slugs, read from the proceedings landing pages on 2026-10-19:
  icis2022/is_futureofwork, icis2023/techandfow, icis2024/digtech_fow, icis2025/is_transformwork
(ICIS 2026 takes place in December 2026; no proceedings were online on 2026-10-19.)

Usage:
  python -I icis_fow_tracks.py <download_dir> <results_dir>
Follows index.N.html pagination; one request every 2 s with a browser User-Agent (the
eLibrary's search endpoint refuses automated clients, its browse pages do not).
Title screen (fixed before reading): monitor|surveil|algorithmic management|people analytics|
performance (evaluat|measur|metric|scor|rating)|productiv|rating|scor|evaluat|track|process mining|
event log|metric|quantif|datafic|workplace analytics|HR analytics.
Writes <results_dir>/icis_fow_titles.csv (year, track, title, url, screen_hit) and prints hits.
"""
import csv
import html
import os
import re
import sys
import time
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
TRACKS = [("2022", "icis2022/is_futureofwork"), ("2023", "icis2023/techandfow"),
          ("2024", "icis2024/digtech_fow"), ("2025", "icis2025/is_transformwork")]
SCREEN = re.compile(r"(monitor|surveil|algorithmic management|people analytics|productiv|rating|\bscor|evaluat|"
                    r"track|process mining|event log|metric|quantif|datafic|workplace analytics|hr analytics|"
                    r"control|measur|performance)", re.I)
ENTRY = re.compile(r'<p class="(?:summary|article-listing)"[^>]*>\s*<a href="([^"]+)"[^>]*>(.*?)</a>', re.S)


def fetch(url, dest):
    time.sleep(2)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            body = r.read().decode("utf-8", "replace")
    except Exception as e:
        print("ERR", url, e)
        return None
    open(dest, "w", encoding="utf-8").write(body)
    return body


def main():
    out, res = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    rows = []
    for year, slug in TRACKS:
        page, seen = 1, set()
        while True:
            url = f"https://aisel.aisnet.org/{slug}/" + ("" if page == 1 else f"index.{page}.html")
            body = fetch(url, os.path.join(out, slug.replace("/", "_") + f"_{page}.html"))
            if not body:
                break
            new = 0
            for href, t in ENTRY.findall(body):
                title = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t))).strip()
                if href in seen:
                    continue
                seen.add(href)
                new += 1
                rows.append([year, slug, title, href, int(bool(SCREEN.search(title)))])
            if f"index.{page + 1}.html" not in body or new == 0:
                break
            page += 1
        print(year, slug, len(seen), flush=True)
    with open(os.path.join(res, "icis_fow_titles.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["year", "track", "title", "url", "screen_hit"])
        w.writerows(rows)
    for r in rows:
        if r[4]:
            print(r[0], "|", r[2][:160], "|", r[3])


if __name__ == "__main__":
    main()
