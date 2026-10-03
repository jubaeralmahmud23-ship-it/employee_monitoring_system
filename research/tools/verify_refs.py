#!/usr/bin/env python3
"""Verify bibliographic records against Crossref, OpenAlex and arXiv.

Usage:
    python verify_refs.py titles.txt            # one title per line
    python verify_refs.py --md path/to/area.md  # extract titles from evidence-table rows
    python verify_refs.py --self-test           # check that the APIs are reachable

Output: a markdown table (stdout) with, per title, the best Crossref match
(DOI, venue, year, type), the best OpenAlex match (venue, year, open-access
status, cited-by count), an arXiv match when the title is on arXiv, and a
similarity score between the queried title and the matched title. A score
below 0.85 means the match must be checked by hand before it is cited.

Only standard-library modules are used so the script runs in any environment.
Requests are polite (User-Agent with contact, small delays). Nothing is
cached across runs; results are printed so they can be pasted into the
records with the date.
"""
import argparse
import difflib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date

UA = "research-records-verify/0.1 (academic use; contact via repository owner)"
TIMEOUT = 25


def _get(url, retries=4):
    """GET with exponential backoff on 429/5xx (polite to rate-limited APIs)."""
    delay = 2.0
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < retries:
                time.sleep(delay)
                delay *= 2
                continue
            raise


def _norm(s):
    return re.sub(r"[^a-z0-9 ]+", " ", (s or "").lower()).strip()


def similarity(a, b):
    return round(difflib.SequenceMatcher(None, _norm(a), _norm(b)).ratio(), 3)


def crossref(title):
    q = urllib.parse.urlencode({"query.title": title, "rows": 3, "select": "DOI,title,container-title,issued,type,author"})
    try:
        items = json.loads(_get(f"https://api.crossref.org/works?{q}"))["message"]["items"]
    except Exception as e:  # noqa: BLE001
        return {"error": f"crossref: {e}"}
    best = None
    for it in items:
        t = (it.get("title") or [""])[0]
        sc = similarity(title, t)
        if best is None or sc > best["score"]:
            yr = (it.get("issued", {}).get("date-parts") or [[None]])[0][0]
            best = {"score": sc, "title": t, "doi": it.get("DOI"), "venue": (it.get("container-title") or [""])[0],
                    "year": yr, "type": it.get("type"),
                    "first_author": (it.get("author") or [{}])[0].get("family", "")}
    return best or {"error": "crossref: no items"}


def openalex(title):
    q = urllib.parse.urlencode({"search": title, "per-page": 3,
                                "select": "id,title,doi,publication_year,type,open_access,cited_by_count,primary_location"})
    try:
        res = json.loads(_get(f"https://api.openalex.org/works?{q}"))["results"]
    except Exception as e:  # noqa: BLE001
        return {"error": f"openalex: {e}"}
    best = None
    for it in res:
        sc = similarity(title, it.get("title") or "")
        if best is None or sc > best["score"]:
            loc = it.get("primary_location") or {}
            src = loc.get("source") or {}
            best = {"score": sc, "title": it.get("title"), "doi": it.get("doi"), "year": it.get("publication_year"),
                    "type": it.get("type"), "venue": src.get("display_name"), "is_oa": (it.get("open_access") or {}).get("is_oa"),
                    "cited_by": it.get("cited_by_count"), "openalex_id": it.get("id")}
    return best or {"error": "openalex: no results"}


def arxiv(title):
    q = urllib.parse.urlencode({"search_query": f'ti:"{title}"', "max_results": 3})
    try:
        xml = _get(f"https://export.arxiv.org/api/query?{q}")
        root = ET.fromstring(xml)
    except Exception as e:  # noqa: BLE001
        return {"error": f"arxiv: {e}"}
    ns = {"a": "http://www.w3.org/2005/Atom"}
    best = None
    for e in root.findall("a:entry", ns):
        t = " ".join((e.findtext("a:title", default="", namespaces=ns) or "").split())
        sc = similarity(title, t)
        if best is None or sc > best["score"]:
            ident = e.findtext("a:id", default="", namespaces=ns)
            best = {"score": sc, "title": t, "id": ident, "published": (e.findtext("a:published", default="", namespaces=ns) or "")[:10],
                    "journal_ref": e.findtext("{http://arxiv.org/schemas/atom}journal_ref", default="") or "",
                    "doi": e.findtext("{http://arxiv.org/schemas/atom}doi", default="") or ""}
    return best or {"error": "arxiv: no entries"}


def semantic_scholar(title):
    q = urllib.parse.urlencode({"query": title, "limit": 3, "fields": "title,year,venue,externalIds,citationCount,publicationTypes"})
    try:
        data = json.loads(_get(f"https://api.semanticscholar.org/graph/v1/paper/search?{q}")).get("data") or []
    except Exception as e:  # noqa: BLE001
        return {"error": f"s2: {e}"}
    best = None
    for it in data:
        sc = similarity(title, it.get("title") or "")
        if best is None or sc > best["score"]:
            ext = it.get("externalIds") or {}
            best = {"score": sc, "title": it.get("title"), "year": it.get("year"), "venue": it.get("venue"),
                    "doi": ext.get("DOI"), "arxiv": ext.get("ArXiv"), "cited_by": it.get("citationCount"),
                    "types": ",".join(it.get("publicationTypes") or [])}
    return best or {"error": "s2: no results"}


def extract_titles_from_md(path):
    """Pull the Link column's neighbouring citation text is unreliable; instead take
    quoted or bold titles and any table cell that looks like a title."""
    titles = []
    for line in open(path, encoding="utf-8"):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        for c in cells:
            m = re.search(r"\*\*(.+?)\*\*|\"(.+?)\"|“(.+?)”", c)
            if m:
                t = next(g for g in m.groups() if g)
                if len(t) > 25 and t not in titles:
                    titles.append(t)
    return titles


def verify(titles, delay=1.0):
    rows = []
    for t in titles:
        c, o, a, s2 = crossref(t), openalex(t), arxiv(t), semantic_scholar(t)
        rows.append((t, c, o, a, s2))
        time.sleep(delay)
    return rows


def to_markdown(rows):
    out = [f"Verification run {date.today().isoformat()} via Crossref, OpenAlex, arXiv and Semantic Scholar APIs. Scores below 0.85 need manual review.", "",
           "| Queried title | Crossref (score, DOI, venue, year, type) | OpenAlex (score, venue, year, OA, cited-by) | arXiv (score, id, published, journal-ref/DOI) | Semantic Scholar (score, venue, year, DOI/arXiv, cited-by, types) |",
           "|---|---|---|---|---|"]
    for t, c, o, a, s2 in rows:
        cs = c.get("error") or f"{c['score']} · {c.get('doi')} · {c.get('venue')} · {c.get('year')} · {c.get('type')}"
        os_ = o.get("error") or f"{o['score']} · {o.get('venue')} · {o.get('year')} · OA={o.get('is_oa')} · cited {o.get('cited_by')}"
        as_ = a.get("error") or f"{a['score']} · {a.get('id')} · {a.get('published')} · {a.get('journal_ref') or a.get('doi') or '-'}"
        ss = s2.get("error") or f"{s2['score']} · {s2.get('venue')} · {s2.get('year')} · {s2.get('doi') or s2.get('arxiv') or '-'} · cited {s2.get('cited_by')} · {s2.get('types')}"
        out.append(f"| {t} | {cs} | {os_} | {as_} | {ss} |")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source", nargs="?", help="text file with one title per line")
    ap.add_argument("--md", help="markdown file; titles are taken from bold or quoted strings in table rows")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        rows = verify(["Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"], delay=0)
        print(to_markdown(rows))
        ok = sum(1 for r in rows for i in (1, 2, 3, 4) if not r[i].get("error")) >= 3
        sys.exit(0 if ok else 2)
    if args.md:
        titles = extract_titles_from_md(args.md)
    elif args.source:
        titles = [l.strip() for l in open(args.source, encoding="utf-8") if l.strip()]
    else:
        ap.error("give a titles file, --md, or --self-test")
    print(to_markdown(verify(titles)))


if __name__ == "__main__":
    main()
