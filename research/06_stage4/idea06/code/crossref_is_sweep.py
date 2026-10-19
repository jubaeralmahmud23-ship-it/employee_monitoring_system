"""Crossref sweep of IS journals and HICSS (2023-01-01 to 2026-12-31) for
meta-research on LLM evaluation practice.

Usage:
  python -I crossref_is_sweep.py <out_dir>

Enumerates every Crossref record per ISSN (and the HICSS DOI prefix 10.24251)
with cursor paging (rows=1000), keeps DOI, title, abstract, issued date,
container and type, and writes <out_dir>/is_records.csv. Then flags records
whose title or abstract contains an LLM term AND a methods/meta-research term
(lists in LLM_TERMS / META_TERMS) and writes <out_dir>/is_flagged.csv with the
matched terms, plus a stricter list <out_dir>/is_flagged_strict.csv where the
methods term is in the title. Pace: 1 s between calls; three attempts per page.
Standard library only.
"""
import csv
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

import os as _os
# Contact for the Crossref polite pool: set the MAILTO environment variable to your own address.
# It is deliberately not hardcoded (redacted 2026-10-19).
MAILTO = _os.environ.get("MAILTO", "")
UA = "idea06-novelty-check/1.0" + (" (mailto:%s)" % MAILTO if MAILTO else "")
SOURCES = [
    ("MIS Quarterly", "issn", "0276-7783"),
    ("Information Systems Research", "issn", "1047-7047"),
    ("Journal of Management Information Systems", "issn", "0742-1222"),
    ("Journal of the AIS", "issn", "1536-9323"),
    ("Information Systems Journal", "issn", "1350-1917"),
    ("European Journal of Information Systems", "issn", "0960-085X"),
    ("Journal of Information Technology", "issn", "0268-3962"),
    ("Journal of Strategic Information Systems", "issn", "0963-8687"),
    ("Communications of the AIS", "issn", "1529-3181"),
    ("Business & Information Systems Engineering", "issn", "2363-7005"),
    ("Information Systems Frontiers", "issn", "1387-3326"),
    ("Electronic Markets", "issn", "1019-6781"),
    ("Decision Support Systems", "issn", "0167-9236"),
    ("Information & Management", "issn", "0378-7206"),
    ("ACM Transactions on Management Information Systems", "issn", "2158-656X"),
    ("International Journal of Information Management", "issn", "0268-4012"),
    ("MIS Quarterly Executive", "issn", "1540-1960"),
    ("HICSS proceedings", "prefix", "10.24251"),
]
LLM_TERMS = ["large language model", "llm", "chatgpt", "gpt-", "gpt4", "gpt 4", "generative ai", "genai",
             "generative artificial intelligence", "language model", "foundation model", "ai-generated",
             "llm-as-a-judge", "ai judge", "machine-generated"]
META_TERMS = ["reporting", "reproducib", "replicab", "replication", "error bar", "confidence interval",
              "uncertainty", "statistical", "significance test", "inter-rater", "interrater", "intercoder",
              "inter-coder", "kappa", "krippendorff", "agreement", "validity", "validation", "rigor", "rigour",
              "methodolog", "guideline", "checklist", "meta-analysis", "meta-research", "metascience",
              "audit", "transparen", "research practice", "evaluation practice", "benchmark", "robustness",
              "best practice", "research method", "standards"]
STRONG = ["reporting", "reproducib", "replicab", "error bar", "inter-rater", "interrater", "intercoder",
          "inter-coder", "kappa", "krippendorff", "meta-research", "metascience", "methodolog", "guideline",
          "checklist", "rigor", "rigour", "audit", "research practice", "evaluation practice", "best practice",
          "research method", "confidence interval", "statistical"]
_last = [0.0]


def get(url, log):
    for attempt in range(1, 4):
        w = 1.0 - (time.time() - _last[0])
        if w > 0:
            time.sleep(w)
        _last[0] = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as r:
                body = r.read().decode("utf-8", "replace")
                log.append([url[:300], r.status, attempt])
                return json.loads(body)
        except urllib.error.HTTPError as e:
            log.append([url[:300], e.code, attempt])
            time.sleep(20 * attempt)
        except Exception as e:
            log.append([url[:300], "ERR:" + type(e).__name__, attempt])
            time.sleep(20 * attempt)
    return None


def clean(s):
    s = html.unescape(re.sub(r"<[^>]+>", " ", s or ""))
    return re.sub(r"\s+", " ", s).strip()


def has(text, terms):
    t = text.lower()
    out = []
    for term in terms:
        if term == "llm":
            if re.search(r"\bllms?\b", t):
                out.append(term)
        elif term in t:
            out.append(term)
    return out


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    log, recs = [], []
    counts = []
    for name, kind, ident in SOURCES:
        cursor = "*"
        n = 0
        while cursor:
            filt = f"{kind}:{ident},from-pub-date:2023-01-01,until-pub-date:2026-12-31"
            url = ("https://api.crossref.org/works?filter=" + urllib.parse.quote(filt, safe=":,")
                   + "&select=DOI,title,abstract,issued,container-title,type&rows=1000&cursor="
                   + urllib.parse.quote(cursor) + ("&mailto=" + urllib.parse.quote(MAILTO) if MAILTO else ""))
            d = get(url, log)
            if d is None:
                counts.append([name, ident, n, "incomplete"])
                break
            items = d["message"].get("items", [])
            for it in items:
                title = clean(" ".join(it.get("title") or []))
                ab = clean(it.get("abstract"))
                yr = ((it.get("issued") or {}).get("date-parts") or [[None]])[0][0]
                recs.append([name, it.get("DOI"), yr, it.get("type"), " ".join(it.get("container-title") or []), title, ab])
            n += len(items)
            if not items or len(items) < 1000:
                break
            cursor = d["message"].get("next-cursor")
        else:
            pass
        if not counts or counts[-1][0] != name:
            counts.append([name, ident, n, "complete"])
        print(name, n, flush=True)
    with open(os.path.join(out, "is_records.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source", "doi", "year", "type", "container", "title", "abstract"])
        w.writerows(recs)
    flagged, strict = [], []
    for r in recs:
        title, ab = r[5], r[6]
        l_t, l_a = has(title, LLM_TERMS), has(ab, LLM_TERMS)
        m_t, m_a = has(title, META_TERMS), has(ab, META_TERMS)
        s_t = has(title, STRONG)
        if (l_t or l_a) and (m_t or m_a):
            flagged.append(r[:6] + [";".join(sorted(set(l_t + l_a))), ";".join(sorted(set(m_t + m_a))), "yes" if ab else "no"])
        if (l_t or l_a) and s_t:
            strict.append(r[:6] + [";".join(sorted(set(l_t + l_a))), ";".join(s_t), ab[:600]])
    with open(os.path.join(out, "is_flagged.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source", "doi", "year", "type", "container", "title", "llm_terms", "meta_terms", "abstract_present"])
        w.writerows(flagged)
    with open(os.path.join(out, "is_flagged_strict.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source", "doi", "year", "type", "container", "title", "llm_terms", "strong_title_terms", "abstract_600"])
        w.writerows(strict)
    with open(os.path.join(out, "is_source_counts.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source", "id", "records", "status"])
        w.writerows(counts)
    with open(os.path.join(out, "crossref_log.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["url", "status", "attempt"])
        w.writerows(log)
    print("records", len(recs), "flagged", len(flagged), "strict", len(strict))


if __name__ == "__main__":
    main()
