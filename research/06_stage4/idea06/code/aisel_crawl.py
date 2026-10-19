"""Crawl AIS eLibrary proceedings track pages and list paper titles.

Usage:
  python -I aisel_crawl.py <out_dir> <slug> [<slug> ...]
  e.g. slugs icis2023 icis2024 icis2025 ecis2023 ecis2024 ecis2025 ecis2026

The AIS eLibrary full-text search endpoint (/do/search/) answers HTTP 403 to
automated clients, so this sweep enumerates the public browse pages instead:
the proceedings landing page -> each track page -> the paper entries
(<p class="summary"> or <p class="article-listing"> links). It follows
index.N.html pagination links when present. One request every 1.5 s with a
browser User-Agent. Raw HTML goes to <out_dir>/raw/, titles to
<out_dir>/aisel_titles.csv, fetch log to <out_dir>/aisel_fetch_log.csv.
Standard library only.
"""
import csv
import html
import os
import re
import sys
import time
import urllib.error
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
BASE = "https://aisel.aisnet.org/"
DELAY = 1.5
SKIP = ("announcements", "awards", "Awards", "index.", ".html", "panels", "pdw", "paperathon",
        "keynote", "doctoral", "TREOs", "treos", "workshops")
_last = [0.0]


def fetch(url, log):
    for attempt in range(1, 4):
        w = DELAY - (time.time() - _last[0])
        if w > 0:
            time.sleep(w)
        _last[0] = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                body = r.read().decode("utf-8", "replace")
                log.append([url, r.status, attempt, len(body)])
                return body
        except urllib.error.HTTPError as e:
            log.append([url, e.code, attempt, 0])
            if e.code in (403, 404):
                return None
            time.sleep(10 * attempt)
        except Exception as e:
            log.append([url, "ERR:" + type(e).__name__, attempt, 0])
            time.sleep(10 * attempt)
    return None


ENTRY = re.compile(r'<p class="(?:summary|article-listing)"[^>]*>\s*<a href="([^"]+)"[^>]*>(.*?)</a>', re.S)


def main():
    out = sys.argv[1]
    slugs = sys.argv[2:]
    os.makedirs(os.path.join(out, "raw"), exist_ok=True)
    log, rows = [], []
    for slug in slugs:
        landing = fetch(BASE + slug + "/", log)
        if landing is None:
            continue
        with open(os.path.join(out, "raw", f"{slug}__landing.html"), "w", encoding="utf-8") as f:
            f.write(landing)
        tracks = sorted(set(re.findall(r'href="https://aisel\.aisnet\.org/' + slug + r'/([A-Za-z0-9_\-]+)/?"', landing)))
        tracks = [t for t in tracks if not any(s in t for s in SKIP)]
        for t in tracks:
            pages = [BASE + f"{slug}/{t}/"]
            seen = set()
            while pages:
                u = pages.pop(0)
                if u in seen:
                    continue
                seen.add(u)
                body = fetch(u, log)
                if body is None:
                    continue
                name = re.sub(r"[^A-Za-z0-9]+", "_", u[len(BASE):])
                with open(os.path.join(out, "raw", name + ".html"), "w", encoding="utf-8") as f:
                    f.write(body)
                for href, title in ENTRY.findall(body):
                    title = html.unescape(re.sub(r"<[^>]+>", "", title)).strip()
                    rows.append([slug, t, href, title])
                for p in set(re.findall(r'href="(https://aisel\.aisnet\.org/' + slug + "/" + t + r'/index\.\d+\.html)"', body)):
                    if p not in seen:
                        pages.append(p)
    # de-duplicate by URL
    uniq, seenu = [], set()
    for r in rows:
        if r[2] in seenu:
            continue
        seenu.add(r[2])
        uniq.append(r)
    with open(os.path.join(out, "aisel_titles.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["proceedings", "track", "url", "title"])
        w.writerows(uniq)
    with open(os.path.join(out, "aisel_fetch_log.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["url", "status", "attempt", "bytes"])
        w.writerows(log)
    from collections import Counter
    c = Counter(r[0] for r in uniq)
    for k in slugs:
        print(k, c.get(k, 0))


if __name__ == "__main__":
    main()
