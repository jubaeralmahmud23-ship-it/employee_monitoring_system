"""Citation chasing for the Stage 4 deep novelty check of idea 4 (NYC LL 144 impact ratios).

Backward and forward chasing through OpenAlex, Semantic Scholar and Crossref, with the pacing
rules of the Stage 4 brief: at least 3 s between calls to the same service, a 30-60 s back-off
after HTTP 429, at most 3 attempts per leg, then the leg is recorded as 'not done'.

Usage:
  python -I novelty_chase.py --raw-dir <dir for raw JSON> --log <csv> --hits <csv>

Raw API responses go to --raw-dir (outside the repository). The --log CSV records one row per leg
(seed, direction, tool, status, attempts, number of works returned). The --hits CSV lists every
returned work whose title matches the relevance keywords below (title, year, DOI, seed, leg).
No e-mail address or API key is sent.
"""
import argparse
import csv
import json
import os
import random
import re
import time
import urllib.parse

import requests

SEEDS = [
    # key, DOI (or None), arXiv id (or None), directions to chase
    ("gerchick2025", "10.1145/3715275.3732004", None, ["forward"]),
    ("wright2024", "10.1145/3630106.3658998", "2406.01399", ["forward"]),
    ("morris_lobsenz2000", "10.1111/j.1744-6570.2000.tb00195.x", None, ["forward", "backward"]),
    ("roth_bobko_switzer2006", "10.1037/0021-9010.91.3.507", None, ["forward", "backward"]),
    ("collins_morris2008", "10.1037/0021-9010.93.2.463", None, ["forward", "backward"]),
    ("switzer_roth_rosopa2016", "10.1080/08959285.2016.1154060", None, ["forward", "backward"]),
    ("lam2024", "10.1145/3630106.3658957", "2401.14908", ["forward"]),
    ("ferrara2025", "10.52202/085713-3272", "2506.10586", ["backward", "forward"]),
    ("black_dhacking2024", "10.1145/3630106.3658928", None, ["forward"]),
]

KEYWORDS = re.compile(
    r"local law 144|ll ?144|\bnyc\b|new york city|bias audit|audit|four[- ]fifths|4/5|80 ?%|adverse impact|"
    r"disparate impact|impact ratio|selection rate|sample size|small sample|confidence interval|"
    r"significance|power|uncertaint|hiring|employment|selection procedure|uniform guidelines|"
    r"aggregat|pool|simpson|mantel|intersectional|fairness test|hypothesis test|automated employment",
    re.I,
)

UA = {"User-Agent": "stage4-novelty-check/1.0 (research script; no contact)"}
_last_call = {}


def paced_get(service, url, params=None):
    """GET with >=3 s spacing per service; returns (status, json or None)."""
    gap = 3.2
    last = _last_call.get(service, 0.0)
    wait = gap - (time.time() - last)
    if wait > 0:
        time.sleep(wait)
    _last_call[service] = time.time()
    try:
        r = requests.get(url, params=params, headers=UA, timeout=60)
    except requests.RequestException as exc:  # network failure counts as an attempt
        return f"error:{type(exc).__name__}", None
    if r.status_code != 200:
        return str(r.status_code), None
    try:
        return "200", r.json()
    except ValueError:
        return "200-nonjson", None


def leg(service, fetch, raw_dir, name):
    """Run one leg with at most 3 attempts; back off 30-60 s on 429."""
    attempts = 0
    status = "not run"
    payload = None
    while attempts < 3:
        attempts += 1
        status, payload = fetch()
        if status == "200":
            break
        if status == "429":
            time.sleep(random.uniform(30, 60))
        else:
            time.sleep(5)
    if payload is not None:
        with open(os.path.join(raw_dir, f"{name}.json"), "w", encoding="utf-8") as fh:
            json.dump(payload, fh)
    return status, attempts, payload


def openalex_forward(doi, raw_dir, name):
    works = []
    statuses = []
    tot_attempts = 0
    # resolve the seed
    st, att, seed = leg("openalex", lambda: paced_get("openalex", f"https://api.openalex.org/works/doi:{doi}",
                                                         {"select": "id,display_name,cited_by_count,referenced_works,cited_by_api_url"}),
                        raw_dir, name + "_seed")
    tot_attempts += att
    statuses.append(st)
    if seed is None:
        return "not done (" + st + ")", tot_attempts, [], None
    wid = seed["id"].rsplit("/", 1)[-1]
    cursor = "*"
    page = 0
    while cursor:
        page += 1
        st, att, js = leg("openalex", lambda c=cursor: paced_get(
            "openalex", "https://api.openalex.org/works",
            {"filter": f"cites:{wid}", "per-page": "200", "cursor": c,
             "select": "id,doi,display_name,publication_year,type,primary_location"}),
            raw_dir, f"{name}_citedby_p{page}")
        tot_attempts += att
        statuses.append(st)
        if js is None:
            return f"partial ({st} on page {page})", tot_attempts, works, seed
        for w in js.get("results", []):
            venue = ((w.get("primary_location") or {}).get("source") or {}).get("display_name")
            works.append({"title": w.get("display_name"), "year": w.get("publication_year"),
                          "doi": w.get("doi"), "venue": venue, "id": w.get("id")})
        cursor = js.get("meta", {}).get("next_cursor")
        if not js.get("results"):
            break
    return "done", tot_attempts, works, seed


def openalex_backward(seed, raw_dir, name):
    refs = seed.get("referenced_works", []) if seed else []
    works = []
    tot = 0
    for i in range(0, len(refs), 50):
        chunk = "|".join(r.rsplit("/", 1)[-1] for r in refs[i:i + 50])
        st, att, js = leg("openalex", lambda c=chunk: paced_get(
            "openalex", "https://api.openalex.org/works",
            {"filter": f"openalex:{c}", "per-page": "50", "select": "id,doi,display_name,publication_year"}),
            raw_dir, f"{name}_refs_{i}")
        tot += att
        if js is None:
            return f"partial ({st})", tot, works
        for w in js.get("results", []):
            works.append({"title": w.get("display_name"), "year": w.get("publication_year"),
                          "doi": w.get("doi"), "venue": None, "id": w.get("id")})
    return ("done" if refs else "done (0 referenced_works deposited)"), tot, works


def s2_leg(pid, direction, raw_dir, name):
    endpoint = "citations" if direction == "forward" else "references"
    key = "citingPaper" if direction == "forward" else "citedPaper"
    st, att, js = leg("s2", lambda: paced_get(
        "s2", f"https://api.semanticscholar.org/graph/v1/paper/{pid}/{endpoint}",
        {"fields": "title,year,venue,externalIds", "limit": "1000"}), raw_dir, name)
    if js is None:
        return f"not done ({st} x{att})", att, []
    works = []
    for item in js.get("data", []):
        p = item.get(key) or {}
        ext = p.get("externalIds") or {}
        works.append({"title": p.get("title"), "year": p.get("year"), "doi": ext.get("DOI"),
                      "venue": p.get("venue"), "id": p.get("paperId")})
    return "done", att, works


def crossref_backward(doi, raw_dir, name):
    st, att, js = leg("crossref", lambda: paced_get("crossref", f"https://api.crossref.org/works/{urllib.parse.quote(doi)}"),
                      raw_dir, name)
    if js is None:
        return f"not done ({st} x{att})", att, []
    msg = js.get("message", {})
    works = []
    for ref in msg.get("reference", []) or []:
        title = ref.get("article-title") or ref.get("volume-title") or ref.get("unstructured") or ""
        works.append({"title": title, "year": ref.get("year"), "doi": ref.get("DOI"),
                      "venue": ref.get("journal-title"), "id": ref.get("key")})
    status = "done" if works else "done (no reference list deposited)"
    return status, att, works


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw-dir", required=True)
    ap.add_argument("--log", required=True)
    ap.add_argument("--hits", required=True)
    ap.add_argument("--only", default="", help="comma-separated seed keys to run (default all)")
    args = ap.parse_args()
    os.makedirs(args.raw_dir, exist_ok=True)
    random.seed(20261019)
    only = set(filter(None, args.only.split(",")))
    log_rows, hit_rows = [], []
    t0 = time.time()
    for key, doi, arx, dirs in SEEDS:
        if only and key not in only:
            continue
        seed_json = None
        # OpenAlex
        if doi and "forward" in dirs:
            st, att, works, seed_json = openalex_forward(doi, args.raw_dir, f"oa_{key}")
            log_rows.append([key, "forward", "OpenAlex", st, att, len(works)])
            for w in works:
                if w["title"] and KEYWORDS.search(w["title"]):
                    hit_rows.append([key, "forward", "OpenAlex", w["title"], w["year"], w["doi"], w["venue"]])
        if doi and "backward" in dirs:
            if seed_json is None:
                st0, att0, seed_json = leg("openalex", lambda: paced_get(
                    "openalex", f"https://api.openalex.org/works/doi:{doi}",
                    {"select": "id,display_name,cited_by_count,referenced_works"}), args.raw_dir, f"oa_{key}_seedb")
            if seed_json is None:
                log_rows.append([key, "backward", "OpenAlex", "not done (seed unresolved)", 3, 0])
            else:
                st, att, works = openalex_backward(seed_json, args.raw_dir, f"oa_{key}")
                log_rows.append([key, "backward", "OpenAlex", st, att, len(works)])
                for w in works:
                    if w["title"] and KEYWORDS.search(w["title"]):
                        hit_rows.append([key, "backward", "OpenAlex", w["title"], w["year"], w["doi"], w["venue"]])
        # Semantic Scholar
        pid = f"DOI:{doi}" if doi and not arx else (f"ARXIV:{arx}" if arx else f"DOI:{doi}")
        for d in dirs:
            st, att, works = s2_leg(pid, d, args.raw_dir, f"s2_{key}_{d}")
            log_rows.append([key, d, "SemanticScholar", st, att, len(works)])
            for w in works:
                if w["title"] and KEYWORDS.search(w["title"]):
                    hit_rows.append([key, d, "SemanticScholar", w["title"], w["year"], w["doi"], w["venue"]])
        # Crossref reference list (backward only)
        if doi and "backward" in dirs:
            st, att, works = crossref_backward(doi, args.raw_dir, f"cr_{key}")
            log_rows.append([key, "backward", "Crossref", st, att, len(works)])
            for w in works:
                if w["title"] and KEYWORDS.search(w["title"]):
                    hit_rows.append([key, "backward", "Crossref", w["title"][:300], w["year"], w["doi"], w["venue"]])
    with open(args.log, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh)
        wr.writerow(["seed", "direction", "tool", "status", "attempts", "n_works_returned"])
        wr.writerows(log_rows)
    with open(args.hits, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh)
        wr.writerow(["seed", "direction", "tool", "title", "year", "doi", "venue"])
        wr.writerows(hit_rows)
    print(f"legs={len(log_rows)} keyword_hits={len(hit_rows)} wall_clock_s={time.time() - t0:.0f}")


if __name__ == "__main__":
    main()
