#!/usr/bin/env python3
"""Verify the evidence tables of the literature area files by identifier.

For every row of a "## Evidence table" in the given markdown files, the script
pulls DOIs (10.xxxx/...) and arXiv identifiers from the Citation and Link cells,
resolves each DOI through the Crossref API and each arXiv id through the arXiv
export API, and compares what the APIs return with what the row states:

  * year  - the first 4-digit year in the Citation cell versus the Crossref
            issued year or the arXiv first-published year (a one-year gap is
            reported as "near" because preprints and journal versions differ);
  * venue - whether the Crossref container-title (or the arXiv journal-ref)
            shares at least one informative token with the Citation cell;
  * status - whether a row labelled "preprint" has a DOI whose Crossref type is
            journal-article or proceedings-article (a published version may
            supersede the preprint), and whether a row labelled peer-reviewed
            has only an arXiv identifier and no DOI.

Rows with neither identifier are listed separately so that they can be checked
by title with verify_refs.py. Only the standard library is used. Requests are
polite: Crossref calls are spaced, arXiv ids are batched into one request per
file, and 429/5xx answers trigger exponential backoff.

Usage:
    python verify_evidence_tables.py area1.md [area2.md ...] > report.md
"""
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date

UA = "research-records-verify/0.2 (academic use; contact via repository owner)"
TIMEOUT = 30
DOI_RE = re.compile(r"10\.\d{4,9}/[^\s|)\]>\"',;]+")
ARXIV_RE = re.compile(r"(?:arxiv\.org/(?:abs|pdf|html)/|arXiv[: ]\s*)(\d{4}\.\d{4,5})(?:v\d+)?", re.I)
YEAR_RE = re.compile(r"\b(19[89]\d|20[0-3]\d)\b")
STOP = {"the", "of", "and", "on", "in", "for", "a", "an", "to", "journal", "proceedings", "conference",
        "international", "acm", "ieee", "annual", "workshop", "volume", "papers", "transactions", "arxiv",
        "preprint", "peer-reviewed", "peer", "reviewed", "crossref", "doi", "pp", "vol", "no", "by"}


def _get(url, retries=4, delay=2.0):
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


def crossref_doi(doi):
    try:
        m = json.loads(_get("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="")))["message"]
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)[:80]}
    issued = (m.get("issued", {}).get("date-parts") or [[None]])[0][0]
    return {"title": (m.get("title") or [""])[0], "venue": (m.get("container-title") or [""])[0],
            "year": issued, "type": m.get("type"), "publisher": m.get("publisher")}


def arxiv_batch(ids):
    out = {}
    if not ids:
        return out
    for i in range(0, len(ids), 40):
        chunk = ids[i:i + 40]
        q = urllib.parse.urlencode({"id_list": ",".join(chunk), "max_results": len(chunk)})
        try:
            root = ET.fromstring(_get("https://export.arxiv.org/api/query?" + q, retries=5, delay=15.0))
        except Exception as e:  # noqa: BLE001
            for a in chunk:
                out[a] = {"error": str(e)[:80]}
            continue
        ns = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}
        for e in root.findall("a:entry", ns):
            ident = e.findtext("a:id", default="", namespaces=ns)
            mm = re.search(r"(\d{4}\.\d{4,5})", ident)
            if not mm:
                continue
            out[mm.group(1)] = {"title": " ".join((e.findtext("a:title", default="", namespaces=ns) or "").split()),
                                "published": (e.findtext("a:published", default="", namespaces=ns) or "")[:10],
                                "journal_ref": e.findtext("x:journal_ref", default="", namespaces=ns) or "",
                                "doi": e.findtext("x:doi", default="", namespaces=ns) or ""}
        time.sleep(3)
    return out


def tokens(s):
    return {t for t in re.findall(r"[a-z][a-z&-]{2,}", (s or "").lower()) if t not in STOP}


ALIASES = {"neurips": "neural information processing systems", "nips": "neural information processing systems",
           "iclr": "learning representations", "icml": "machine learning", "emnlp": "empirical methods",
           "naacl": "north american chapter", "acl": "association for computational linguistics",
           "chi": "human factors in computing", "cscw": "computer-supported cooperative work",
           "facct": "fairness, accountability, and transparency", "aies": "ai, ethics, and society",
           "kdd": "knowledge discovery", "sigir": "information retrieval", "www": "web conference",
           "lnbip": "business information processing", "lncs": "computer science", "cacm": "communications of the acm",
           "pnas": "national academy of sciences", "misq": "mis quarterly", "isr": "information systems research",
           "jmis": "management information systems", "ejis": "european journal of information systems",
           "isj": "information systems journal", "jais": "association for information systems",
           "dss": "decision support systems", "qje": "quarterly journal of economics", "tois": "information systems",
           "tmis": "management information systems", "bise": "business & information systems engineering",
           "tmlr": "transactions on machine learning research", "hicss": "hawaii international conference",
           "icis": "international conference on information systems", "ecis": "european conference on information systems",
           "bpm": "business process management", "caise": "advanced information systems engineering",
           "icpm": "process mining", "aaai": "artificial intelligence", "ijcai": "artificial intelligence",
           "usenix": "usenix", "ccs": "computer and communications security", "coling": "computational linguistics",
           "lrec": "language resources", "ecir": "information retrieval", "cikm": "information and knowledge management",
           "vldb": "very large data bases", "sigmod": "management of data", "jbe": "business ethics"}


def venue_matches(venue, citation):
    """True if the Crossref/arXiv venue is recognisably named in the citation cell."""
    v = (venue or "").lower()
    if not v:
        return True
    if tokens(venue) & tokens(citation):
        return True
    words = [w for w in re.findall(r"[a-z][a-z&-]*", v) if w not in STOP]
    acronym = "".join(w[0] for w in words)
    for tok in re.findall(r"[A-Za-z&]{2,8}", citation):
        t = tok.lower()
        if len(t) >= 3 and t == acronym:
            return True
        if t in ALIASES and ALIASES[t] in v:
            return True
        # initials in order over the venue words (handles ACL, LNBIP, QJE, TMIS)
        if len(t) >= 3 and tok.isupper():
            i = 0
            for w in words:
                if i < len(t) and w.startswith(t[i]):
                    i += 1
            if i == len(t):
                return True
    return False


def evidence_rows(path):
    rows, inside, header_seen = [], False, False
    for n, line in enumerate(open(path, encoding="utf-8"), 1):
        if line.startswith("## "):
            inside = line.strip().lower().startswith("## evidence table")
            header_seen = False
            continue
        if not inside or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not header_seen:
            header_seen = True  # header row
            continue
        if set(cells[0]) <= set("-: "):
            continue  # separator
        if len(cells) < 2:
            continue
        rows.append((n, cells[0], cells[1]))
    return rows


def check_file(path):
    rows = evidence_rows(path)
    results, no_id = [], []
    arxiv_ids = []
    parsed = []
    for n, cit, link in rows:
        blob = cit + " " + link
        dois = sorted({d.rstrip(".") for d in DOI_RE.findall(blob)})
        arx = sorted({a for a in ARXIV_RE.findall(blob)})
        year = YEAR_RE.search(cit)
        low = cit.lower()
        if "peer-reviewed" in low or "peer reviewed" in low:
            status = "peer-reviewed"
        elif "preprint" in low or "working paper" in low:
            status = "preprint"
        else:
            status = "other"
        parsed.append((n, cit, link, dois, arx, int(year.group(1)) if year else None, status))
        arxiv_ids.extend(arx)
    arx_meta = arxiv_batch(sorted(set(arxiv_ids)))
    for n, cit, link, dois, arx, year, status in parsed:
        if not dois and not arx:
            no_id.append((n, cit[:140]))
            continue
        findings, flags = [], []
        for d in dois[:2]:
            m = crossref_doi(d)
            time.sleep(0.7)
            if "error" in m:
                findings.append(f"DOI {d}: Crossref error {m['error']}")
                flags.append("doi-unresolved")
                continue
            findings.append(f"DOI {d}: {m['year']} · {m['venue'] or m['publisher']} · {m['type']} · \"{(m['title'] or '')[:90]}\"")
            if year and m["year"]:
                if abs(year - m["year"]) > 1:
                    flags.append(f"year-mismatch({year} vs {m['year']})")
                elif year != m["year"]:
                    flags.append(f"year-near({year} vs {m['year']})")
            if m["venue"] and not venue_matches(m["venue"], cit):
                flags.append("venue-not-in-citation")
            if status == "preprint" and m["type"] in ("journal-article", "proceedings-article") and not d.lower().startswith("10.48550"):
                flags.append("labelled-preprint-but-DOI-is-published-version")
        for a in arx[:2]:
            m = arx_meta.get(a)
            if not m or "error" in m:
                findings.append(f"arXiv {a}: not returned by API")
                flags.append("arxiv-unresolved")
                continue
            findings.append(f"arXiv {a}: first v {m['published']} · jref \"{m['journal_ref'][:60]}\" · doi {m['doi'] or '-'} · \"{m['title'][:90]}\"")
            py = int(m["published"][:4]) if m["published"][:4].isdigit() else None
            if not dois and year and py and abs(year - py) > 1:
                flags.append(f"year-vs-arxiv({year} vs {py})")
            if status == "peer-reviewed" and not dois and not m["journal_ref"] and not m["doi"]:
                flags.append("peer-reviewed-label-rests-on-arxiv-only")
            if status == "preprint" and (m["doi"] or m["journal_ref"]):
                flags.append("arxiv-lists-published-version")
        results.append((n, cit[:140], findings, sorted(set(flags))))
    return rows, results, no_id


def main():
    files = sys.argv[1:]
    if not files:
        sys.exit("give one or more markdown files")
    print(f"# Identifier-based verification of evidence tables ({date.today().isoformat()})\n")
    print("Method: see `research/tools/verify_evidence_tables.py`. Flags are prompts for a human check, not verdicts: "
          "a `year-near` flag usually means a preprint and its published version differ by one year; "
          "`venue-not-in-citation` means no informative word of the Crossref container title appears in the Citation cell "
          "(abbreviations such as QJE or ISR trigger it); `labelled-preprint-but-DOI-is-published-version` and "
          "`arxiv-lists-published-version` mean the row should name the published version.\n")
    grand = {"rows": 0, "checked": 0, "flagged": 0, "no_id": 0}
    for f in files:
        rows, results, no_id = check_file(f)
        flagged = [r for r in results if r[3]]
        grand["rows"] += len(rows); grand["checked"] += len(results); grand["flagged"] += len(flagged); grand["no_id"] += len(no_id)
        print(f"\n## {f}\n")
        print(f"Rows: {len(rows)} · rows with a DOI or arXiv id: {len(results)} · rows with flags: {len(flagged)} · rows without identifier: {len(no_id)}\n")
        if flagged:
            print("| line | citation (start) | API findings | flags |\n|---|---|---|---|")
            for n, cit, findings, flags in flagged:
                print(f"| {n} | {cit.replace('|', '/')} | {'<br>'.join(x.replace('|', '/') for x in findings)} | {', '.join(flags)} |")
        clean = [r for r in results if not r[3]]
        if clean:
            print(f"\nRows whose identifiers resolved with no flags (line numbers): {', '.join(str(r[0]) for r in clean)}")
        if no_id:
            print("\nRows without a DOI or arXiv id (check by title with verify_refs.py):\n")
            for n, cit in no_id:
                print(f"- line {n}: {cit.replace('|', '/')}")
    print(f"\n## Totals\n\nRows {grand['rows']} · checked by identifier {grand['checked']} · flagged {grand['flagged']} · without identifier {grand['no_id']}")


if __name__ == "__main__":
    main()
