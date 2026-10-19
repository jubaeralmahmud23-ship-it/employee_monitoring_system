#!/usr/bin/env python3
"""Idea 6 (error-bar audit): enumerate the sampling frame with a frozen sampling date.

Standard library only. Two sources:

1. Crossref REST API (api.crossref.org): every record of type journal-article with a
   publication date between --from-date and --freeze-date in the 11 IS journals that
   the feasibility file (research/03_challenge/06-...__feasibility.md, section 1) swept
   on 2026-10-05, queried by ISSN exactly as research/tools/assessment_2026-10-05/idea06/
   crossref_counts.py did. The term filter is that script's regular expression, applied
   to title and title+abstract. Unlike the 2026-10-05 script, markup tags (JATS, <scp>)
   are stripped before matching (the 2026-10-05 recount, crossref_recount_scp.json, showed
   that "Generative <scp>AI</scp>" was missed otherwise); the raw, unstripped count is
   kept too so the two can be compared. The Creative-Commons licence field is recorded.
   The Springer stratum is BISE, ISF and Electronic Markets (the three Springer journals
   the feasibility file names as open-access-eligible).

   A second, unbounded leg repeats the 2026-10-05 query (no upper publication date) so the
   difference between the two dates can be decomposed (--compare-unbounded).

2. ACL Anthology volume pages (aclanthology.org/volumes/<id>/): the industry-track volumes
   named in the plan (02_candidate_ideas.md section 4.1 and the feasibility file):
   EMNLP 2024, NAACL 2025, ACL 2025, EMNLP 2025 (the four named volumes), ACL 2026
   (addition) and EMNLP 2023, NAACL 2024 (optional 2023-2024 anchor). Paper entries are
   parsed from the HTML; the volume's front matter (paper number 0) is excluded. The
   volume .bib file is fetched as a cross-check of the count. Further industry volumes
   are probed and reported but are not part of the planned frame (--probe-volumes).

Raw API responses and HTML pages are cached, with sha256, in --raw-dir (outside the
repository). Small derived CSV/JSON files are written to --out-dir.

No contact e-mail is sent to Crossref (the author has not provided one); the User-Agent
identifies the script.
"""
import argparse
import csv
import datetime as dt
import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "idea06-sampling-frame/1.0 (academic research pilot; python-urllib; no contact address supplied)"

JOURNALS = {  # name -> ISSNs, as in crossref_counts.py of 2026-10-05
    "Business & Information Systems Engineering": ["2363-7005", "1867-0202"],
    "Information Systems Frontiers": ["1387-3326", "1572-9419"],
    "Electronic Markets": ["1019-6781", "1422-8890"],
    "Information & Management": ["0378-7206"],
    "Decision Support Systems": ["0167-9236"],
    "MIS Quarterly": ["0276-7783", "2162-9730"],
    "Information Systems Research": ["1047-7047", "1526-5536"],
    "Journal of Management Information Systems": ["0742-1222", "1557-928X"],
    "Journal of the Association for Information Systems": ["1536-9323"],
    "European Journal of Information Systems": ["0960-085X", "1476-9344"],
    "Information Systems Journal": ["1350-1917", "1365-2575"],
}
SPRINGER = {"Business & Information Systems Engineering", "Information Systems Frontiers", "Electronic Markets"}
SHORT = {
    "Business & Information Systems Engineering": "BISE",
    "Information Systems Frontiers": "ISF",
    "Electronic Markets": "EM",
    "Information & Management": "I&M",
    "Decision Support Systems": "DSS",
    "MIS Quarterly": "MISQ",
    "Information Systems Research": "ISR",
    "Journal of Management Information Systems": "JMIS",
    "Journal of the Association for Information Systems": "JAIS",
    "European Journal of Information Systems": "EJIS",
    "Information Systems Journal": "ISJ",
}
# Term filter of crossref_counts.py (2026-10-05), unchanged.
TERMS = re.compile(r"language model|\bLLMs?\b|generative AI|generative artificial intelligence|ChatGPT|GPT-?[34]", re.I)
TAG = re.compile(r"<[^>]+>")

PLANNED_ACL = [  # volume id, role in the plan
    ("2023.emnlp-industry", "optional 2023-2024 anchor (plan 4.1)"),
    ("2024.naacl-industry", "optional 2023-2024 anchor (plan 4.1)"),
    ("2024.emnlp-industry", "named volume (idea card)"),
    ("2025.naacl-industry", "named volume (idea card)"),
    ("2025.acl-industry", "named volume (idea card)"),
    ("2025.emnlp-industry", "named volume (idea card)"),
    ("2026.acl-industry", "frame addition (plan 4.1)"),
]
PROBE_ACL = ["2026.naacl-industry", "2026.emnlp-industry", "2023.acl-industry", "2024.acl-industry",
             "2025.coling-industry", "2026.eacl-industry"]


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


class Fetcher:
    def __init__(self, raw_dir, delay):
        self.raw_dir = raw_dir
        self.delay = delay
        self.manifest = []
        os.makedirs(raw_dir, exist_ok=True)

    def get(self, url, fname, accept_404=False):
        """GET with up to 4 attempts; caches the body under raw_dir/fname. Returns (status, bytes)."""
        last = None
        for attempt in range(4):
            time.sleep(self.delay)
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA})
                with urllib.request.urlopen(req, timeout=120) as r:
                    body = r.read()
                    status = r.status
                break
            except urllib.error.HTTPError as e:
                if e.code == 404 and accept_404:
                    body, status = b"", 404
                    break
                last = e
                wait = 30 if e.code == 429 else 3 * (attempt + 1)
                print(f"  HTTP {e.code} on {url}; retry in {wait}s", file=sys.stderr)
                time.sleep(wait)
            except Exception as e:  # network error
                last = e
                print(f"  error {e!r} on {url}; retry", file=sys.stderr)
                time.sleep(3 * (attempt + 1))
        else:
            raise RuntimeError(f"failed after 4 attempts: {url}: {last!r}")
        path = os.path.join(self.raw_dir, fname)
        with open(path, "wb") as f:
            f.write(body)
        self.manifest.append({"url": url, "file": fname, "status": status, "bytes": len(body),
                              "sha256": sha256_bytes(body),
                              "fetched_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")})
        return status, body


def date_of(it, key):
    parts = (it.get(key) or {}).get("date-parts") or [[None]]
    p = parts[0]
    if not p or p[0] is None:
        return ""
    return "-".join(f"{x:02d}" if i else str(x) for i, x in enumerate(p))


def clean(s):
    return re.sub(r"\s+", " ", html.unescape(TAG.sub("", s or ""))).strip()


def crossref_leg(fetcher, from_date, until_date, tag):
    """Return {journal: {doi: item}} for one query configuration."""
    out = {}
    sel = ("DOI,title,abstract,container-title,issued,published,published-online,published-print,"
           "license,type,created,deposited")
    for name, issns in JOURNALS.items():
        items = {}
        for issn in issns:
            filt = f"issn:{issn},from-pub-date:{from_date},type:journal-article"
            if until_date:
                filt += f",until-pub-date:{until_date}"
            cursor, page = "*", 0
            while True:
                url = ("https://api.crossref.org/works?filter=%s&rows=1000&select=%s&cursor=%s"
                       % (filt, sel, urllib.parse.quote(cursor)))
                _, body = fetcher.get(url, f"crossref_{tag}_{issn}_p{page}.json")
                d = json.loads(body)
                its = d["message"]["items"]
                for it in its:
                    items[it["DOI"].lower()] = it
                cursor = d["message"].get("next-cursor")
                page += 1
                if not its or not cursor:
                    break
        out[name] = items
        print(f"  [{tag}] {SHORT[name]}: {len(items)} records", file=sys.stderr)
    return out


def row_for(name, it):
    title_raw = " ".join(it.get("title") or [])
    abs_raw = it.get("abstract") or ""
    title = clean(title_raw)
    abstract = clean(abs_raw)
    lic = it.get("license") or []
    cc_urls = sorted({l.get("URL", "") for l in lic if "creativecommons" in (l.get("URL") or "")})
    return {
        "doi": it["DOI"].lower(),
        "journal": SHORT[name],
        "journal_full": name,
        "springer_oa_journal": int(name in SPRINGER),
        "year_issued": date_of(it, "issued")[:4],
        "issued": date_of(it, "issued"),
        "published": date_of(it, "published"),
        "published_online": date_of(it, "published-online"),
        "published_print": date_of(it, "published-print"),
        "created": (it.get("created") or {}).get("date-time", "")[:10],
        "deposited": (it.get("deposited") or {}).get("date-time", "")[:10],
        "type": it.get("type", ""),
        "title": title,
        "has_crossref_abstract": int(bool(abs_raw)),
        "term_hit_title": int(bool(TERMS.search(title))),
        "term_hit_title_abstract": int(bool(TERMS.search(title + " " + abstract))),
        "term_hit_title_abstract_raw": int(bool(TERMS.search(title_raw + " " + abs_raw))),
        "cc_licensed": int(bool(cc_urls)),
        "cc_license_urls": " ".join(cc_urls),
        "license_content_versions": " ".join(sorted({l.get("content-version", "") for l in lic})),
    }


def parse_acl_volume(h, vol):
    """Parse paper entries from an ACL Anthology volume page."""
    papers = []
    pat = re.compile(r'<strong><a class=align-middle href=/(%s\.(\d+))/>(.*?)</a></strong>(.*?)</span></div>'
                     % re.escape(vol), re.S)
    for m in pat.finditer(h):
        aid, num, title_html, rest = m.group(1), int(m.group(2)), m.group(3), m.group(4)
        authors = [clean(a) for a in re.findall(r'<a href=/people/[^>]*>(.*?)</a>', rest)]
        am = re.search(r'id=abstract-%s><div class="card-body p-3 small">(.*?)</div>'
                       % re.escape(aid.replace(".", "--")), h, re.S)
        papers.append({"anthology_id": aid, "paper_number": num, "title": clean(title_html),
                       "n_authors": len(authors), "first_author": authors[0] if authors else "",
                       "has_abstract_on_page": int(bool(am)),
                       "pdf_url": f"https://aclanthology.org/{aid}.pdf"})
    seen, uniq = set(), []
    for p in papers:
        if p["anthology_id"] not in seen:
            seen.add(p["anthology_id"])
            uniq.append(p)
    return uniq


def write_csv(path, rows, fields):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--raw-dir", required=True, help="new directory for raw responses (outside the repo)")
    ap.add_argument("--from-date", default="2023-01-01")
    ap.add_argument("--freeze-date", default="2026-10-19")
    ap.add_argument("--baseline-json", required=True, help="crossref_counts.json of 2026-10-05")
    ap.add_argument("--compare-unbounded", action="store_true")
    ap.add_argument("--delay", type=float, default=1.0)
    a = ap.parse_args()
    os.makedirs(a.out_dir, exist_ok=True)
    t0 = time.time()
    started = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    F = Fetcher(a.raw_dir, a.delay)

    # ---- Crossref, frozen leg -------------------------------------------------
    print("Crossref frozen leg", file=sys.stderr)
    frozen = crossref_leg(F, a.from_date, a.freeze_date, "frozen")
    rows = []
    for name, items in frozen.items():
        for it in items.values():
            rows.append(row_for(name, it))
    rows.sort(key=lambda r: (r["journal"], r["doi"]))
    fields = list(rows[0].keys())
    write_csv(os.path.join(a.out_dir, "is_journal_articles.csv"), rows, fields)
    springer_hits = [r for r in rows if r["springer_oa_journal"] and r["term_hit_title_abstract"]]
    write_csv(os.path.join(a.out_dir, "springer_term_hits.csv"), springer_hits, fields)
    springer_oa = [r for r in springer_hits if r["cc_licensed"]]
    write_csv(os.path.join(a.out_dir, "springer_oa_term_hits.csv"), springer_oa, fields)

    base = json.load(open(a.baseline_json, encoding="utf-8"))
    per_j = []
    for name in JOURNALS:
        R = [r for r in rows if r["journal_full"] == name]
        hits = [r for r in R if r["term_hit_title_abstract"]]
        b = base.get(name, {})
        byyear = {}
        for r in hits:
            byyear[r["year_issued"]] = byyear.get(r["year_issued"], 0) + 1
        per_j.append({
            "journal": SHORT[name], "springer_oa_journal": int(name in SPRINGER),
            "articles": len(R), "articles_2026-10-05": b.get("total_articles_2023plus", ""),
            "with_crossref_abstract": sum(r["has_crossref_abstract"] for r in R),
            "with_crossref_abstract_2026-10-05": b.get("with_crossref_abstract", ""),
            "title_hits": sum(r["term_hit_title"] for r in R),
            "title_hits_2026-10-05": b.get("title_hits", ""),
            "title_abstract_hits": len(hits),
            "title_abstract_hits_raw_unstripped": sum(r["term_hit_title_abstract_raw"] for r in R),
            "title_abstract_hits_2026-10-05": b.get("title_or_abstract_hits", ""),
            "cc_licensed_articles": sum(r["cc_licensed"] for r in R),
            "cc_licensed_articles_2026-10-05": b.get("cc_license_all", ""),
            "cc_licensed_hits": sum(r["cc_licensed"] for r in hits),
            "cc_licensed_hits_2026-10-05": b.get("cc_license_hits", ""),
            "hits_by_year": json.dumps(dict(sorted(byyear.items()))),
            "hits_by_year_2026-10-05": json.dumps(dict(sorted(b.get("ta_hits_by_year", {}).items()))),
            "articles_created_after_2026-10-05": sum(1 for r in R if r["created"] > "2026-10-05"),
            "hits_created_after_2026-10-05": sum(1 for r in hits if r["created"] > "2026-10-05"),
        })
    write_csv(os.path.join(a.out_dir, "frame_counts_is_journals.csv"), per_j, list(per_j[0].keys()))

    # ---- Crossref, unbounded leg (replicates the 2026-10-05 query) --------------
    decomposition = None
    if a.compare_unbounded:
        print("Crossref unbounded leg (2026-10-05 query form)", file=sys.stderr)
        unb = crossref_leg(F, a.from_date, None, "unbounded")
        dec = []
        for name in JOURNALS:
            fz = set(frozen[name])
            ub = set(unb[name])
            only_ub = sorted(ub - fz)
            only_fz = sorted(fz - ub)
            ub_rows = [row_for(name, unb[name][d]) for d in only_ub]
            dec.append({"journal": SHORT[name], "frozen": len(fz), "unbounded": len(ub),
                        "only_in_unbounded": len(only_ub), "only_in_frozen": len(only_fz),
                        "only_in_unbounded_term_hits": sum(r["term_hit_title_abstract"] for r in ub_rows),
                        "only_in_unbounded_pub_dates": " ".join(sorted({r["published"] for r in ub_rows}))[:300]})
        write_csv(os.path.join(a.out_dir, "frame_decomposition_unbounded_vs_frozen.csv"), dec, list(dec[0].keys()))
        decomposition = dec

    # ---- ACL Anthology ----------------------------------------------------------
    print("ACL Anthology volumes", file=sys.stderr)
    acl_rows, acl_counts = [], []
    for vol, role in PLANNED_ACL:
        st, body = F.get(f"https://aclanthology.org/volumes/{vol}/", f"acl_{vol}.html")
        h = body.decode("utf-8", "replace")
        papers = parse_acl_volume(h, vol)
        front = [p for p in papers if p["paper_number"] == 0]
        papers = [p for p in papers if p["paper_number"] != 0]
        st2, bib = F.get(f"https://aclanthology.org/volumes/{vol}.bib", f"acl_{vol}.bib")
        bib_n = len(re.findall(rb"@inproceedings\{", bib))
        overview = [p for p in papers if re.search(r"industry track.*overview|overview of the .*industry", p["title"], re.I)]
        year = vol[:4]
        for p in papers:
            p.update({"volume": vol, "year": year, "venue": vol.split(".")[1].replace("-industry", "").upper()})
            acl_rows.append(p)
        acl_counts.append({"volume": vol, "role": role, "http": st, "papers_parsed_excl_front_matter": len(papers),
                           "front_matter_entries": len(front), "bib_inproceedings": bib_n,
                           "track_overview_papers": len(overview),
                           "with_abstract_on_page": sum(p["has_abstract_on_page"] for p in papers)})
    acl_fields = ["anthology_id", "volume", "venue", "year", "paper_number", "title", "n_authors",
                  "first_author", "has_abstract_on_page", "pdf_url"]
    write_csv(os.path.join(a.out_dir, "acl_industry_papers.csv"), acl_rows, acl_fields)
    write_csv(os.path.join(a.out_dir, "frame_counts_acl_industry.csv"), acl_counts, list(acl_counts[0].keys()))

    probes = []
    for vol in PROBE_ACL:
        st, body = F.get(f"https://aclanthology.org/volumes/{vol}/", f"acl_probe_{vol}.html", accept_404=True)
        n = len([p for p in parse_acl_volume(body.decode("utf-8", "replace"), vol) if p["paper_number"] != 0]) if st == 200 else 0
        probes.append({"volume": vol, "http": st, "papers_parsed_excl_front_matter": n,
                       "in_planned_frame": 0})
    write_csv(os.path.join(a.out_dir, "acl_volume_probes_not_in_frame.csv"), probes, list(probes[0].keys()))

    # ---- Summary -------------------------------------------------------------------
    sp = [r for r in per_j if r["springer_oa_journal"]]
    summary = {
        "sampling_date_frozen": a.freeze_date,
        "crossref_filter": f"issn:<ISSN>,from-pub-date:{a.from_date},until-pub-date:{a.freeze_date},type:journal-article",
        "term_regex": TERMS.pattern,
        "term_fields": "title + Crossref abstract, markup tags stripped (raw unstripped count also kept)",
        "cc_rule": "any Crossref license URL containing 'creativecommons'",
        "run_started_utc": started,
        "wall_clock_seconds": round(time.time() - t0, 1),
        "user_agent": UA,
        "python": sys.version.split()[0],
        "is_journals": {
            "journals": len(JOURNALS),
            "articles_total": len(rows),
            "articles_total_2026-10-05": sum(b.get("total_articles_2023plus", 0) for b in base.values()),
            "title_abstract_hits_total": sum(r["term_hit_title_abstract"] for r in rows),
        },
        "springer_stratum": {
            "journals": sorted(SHORT[n] for n in SPRINGER),
            "articles": sum(r["articles"] for r in sp),
            "term_hits": len(springer_hits),
            "term_hits_2026-10-05": sum(base[n]["title_or_abstract_hits"] for n in SPRINGER),
            "term_hits_raw_unstripped": sum(r["title_abstract_hits_raw_unstripped"] for r in sp),
            "cc_licensed_term_hits": len(springer_oa),
            "cc_licensed_term_hits_2026-10-05": sum(base[n]["cc_license_hits"] for n in SPRINGER),
            "term_hits_by_journal": {r["journal"]: r["title_abstract_hits"] for r in sp},
            "cc_term_hits_by_journal": {r["journal"]: r["cc_licensed_hits"] for r in sp},
        },
        "acl_industry": {
            "volumes": [c["volume"] for c in acl_counts],
            "papers_total": len(acl_rows),
            "papers_by_volume": {c["volume"]: c["papers_parsed_excl_front_matter"] for c in acl_counts},
            "bib_inproceedings_by_volume": {c["volume"]: c["bib_inproceedings"] for c in acl_counts},
            "acl2026_2026-10-05": 154,
            "probed_not_in_frame": {p["volume"]: p["http"] for p in probes},
        },
        "decomposition_available": bool(decomposition),
        "raw_dir": a.raw_dir,
        "raw_files": len(F.manifest),
    }
    with open(os.path.join(a.out_dir, "frame_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=1, ensure_ascii=False)
    with open(os.path.join(a.raw_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(F.manifest, f, indent=1)
    # small manifest of the HTML/bib files in the results (Crossref pages are many and large)
    write_csv(os.path.join(a.out_dir, "raw_manifest.csv"), F.manifest, ["url", "file", "status", "bytes", "sha256", "fetched_utc"])
    print(json.dumps(summary, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
