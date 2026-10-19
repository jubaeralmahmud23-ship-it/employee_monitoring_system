#!/usr/bin/env python3
"""arXiv API searches for the idea 5 deep novelty check (forward-chasing substitute and
topic sweep). Usage: python -I arxiv_queries.py <raw_dir> <results_dir>
Each query: export.arxiv.org/api/query, sortBy=submittedDate desc, max_results=50; pacing 4 s;
up to 3 attempts with 30/45/60 s waits on 429/503. Writes <results_dir>/arxiv_queries.csv
(query_id, query, http, n_returned, total_results) and <results_dir>/arxiv_hits.csv
(query_id, arxiv_id, published, title). Raw Atom XML stays in raw_dir. Standard library only.
"""
import csv
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

UA = "idea05-novelty-check/1.0 (academic use; contact via repository owner)"
NS = {"a": "http://www.w3.org/2005/Atom", "os": "http://a9.com/-/spec/opensearch/1.1/"}
QUERIES = [
    ("A1", 'all:"event log" AND (all:resource OR all:employee OR all:worker) AND (all:ranking OR all:stability OR all:sensitivity OR all:reliability)'),
    ("A2", 'all:"process mining" AND (all:employee OR all:worker OR all:workforce OR all:"human resource") AND (all:performance OR all:productivity)'),
    ("A3", 'all:"multiverse analysis" AND (all:ranking OR all:performance OR all:workers OR all:employees)'),
    ("A4", '(all:"productivity score" OR all:"productivity metric" OR all:"productivity metrics") AND (all:employee OR all:worker OR all:developer)'),
    ("A5", '(all:"rank stability" OR all:"ranking stability" OR all:"rank reversal") AND (all:performance OR all:productivity OR all:indicator)'),
    ("A6", '(all:"algorithmic management" OR all:"workplace surveillance" OR all:"employee monitoring") AND (all:metric OR all:measurement OR all:validity OR all:score)'),
    ("A7", '(all:"developer productivity" OR all:"engineer productivity") AND (all:ranking OR all:robustness OR all:sensitivity OR all:disagree)'),
    ("A8", '(all:"value-added" OR all:"provider profiling" OR all:"league table") AND (all:ranking OR all:reliability) AND (all:workers OR all:employees OR all:teachers OR all:physicians)'),
]


def get(url):
    for i in range(3):
        time.sleep(4)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            code = e.code
        except Exception as e:
            code = "ERR:" + type(e).__name__
        if i < 2:
            time.sleep([30, 45, 60][i])
    return code, None


def main():
    raw, res = sys.argv[1], sys.argv[2]
    os.makedirs(raw, exist_ok=True)
    qrows, hrows = [], []
    for qid, q in QUERIES:
        url = ("https://export.arxiv.org/api/query?search_query=" + urllib.parse.quote(q)
               + "&sortBy=submittedDate&sortOrder=descending&max_results=50")
        code, body = get(url)
        if body is None:
            qrows.append([qid, q, code, 0, ""])
            continue
        open(os.path.join(raw, f"arxiv_{qid}.xml"), "w", encoding="utf-8").write(body)
        root = ET.fromstring(body)
        total = root.findtext("os:totalResults", default="", namespaces=NS)
        n = 0
        for e in root.findall("a:entry", NS):
            aid = (e.findtext("a:id", default="", namespaces=NS) or "").rsplit("/", 1)[-1]
            title = re.sub(r"\s+", " ", e.findtext("a:title", default="", namespaces=NS) or "").strip()
            pub = (e.findtext("a:published", default="", namespaces=NS) or "")[:10]
            hrows.append([qid, aid, pub, title])
            n += 1
        qrows.append([qid, q, code, n, total])
        print(qid, code, n, total, flush=True)
    with open(os.path.join(res, "arxiv_queries.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["query_id", "query", "http", "n_returned", "total_results"])
        w.writerows(qrows)
    with open(os.path.join(res, "arxiv_hits.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["query_id", "arxiv_id", "published", "title"])
        w.writerows(hrows)


if __name__ == "__main__":
    main()
