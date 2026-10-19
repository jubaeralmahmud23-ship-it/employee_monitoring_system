#!/usr/bin/env python3
"""Download and screen the BPI Challenge 2017 and 2019 report submissions for per-resource
rankings and any stability / sensitivity analysis of them (plan section 4.2, 'Databases').

Usage:
  python -I bpic_reports.py <bpic2017_page.html> <bpic2019_page.html> <download_root> <results_dir>

The listing pages were saved beforehand (ais.win.tue.nl/bpi/2017/challenge.html and
icpmconference.org/2019/bpi-challenge/). Each PDF goes into its own directory under
<download_root>/<year>_<name>/ and is converted with `pdftotext -layout`; nothing in the
downloads is executed. For each report the script counts regex matches (case-insensitive):
  RES   resource-level vocabulary: resource(s), employee(s), user(s), worker(s), staff,
        originator(s), clerk(s), User_<n>, "per resource", "per user"
  RANK  ranking vocabulary: rank, ranking, top <n>, most/least productive, best/worst
        performing, productivity, efficient/efficiency
  STAB  stability vocabulary: stabil, sensitiv, robust, Kendall, Spearman, reliab, bootstrap
  JOINT lines that contain both a RES and a RANK term
Writes <results_dir>/bpic_reports_screen.csv (year, file, url, http, bytes, sha256, pages,
RES, RANK, STAB, JOINT) and <download_root>/bpic_joint_lines.txt (every JOINT line and every
STAB line with page numbers) for manual reading. Standard library + pdftotext.
"""
import csv
import hashlib
import os
import re
import subprocess
import sys
import time
import urllib.parse

UA = "idea05-novelty-check/1.0 (academic use; contact via repository owner)"
RES = re.compile(r"(\bresources?\b|\bemployees?\b|\busers?\b|\bworkers?\b|\bstaff\b|\boriginators?\b|\bclerks?\b|"
                 r"user_\d+|per resource|per user|per employee)", re.I)
RANK = re.compile(r"(\brank|\btop[- ]?\d+|most productive|least productive|best[- ]performing|worst[- ]performing|"
                  r"productiv|efficien)", re.I)
STAB = re.compile(r"(stabil|sensitiv|robust|kendall|spearman|reliab|bootstrap)", re.I)


def links(page, base, pattern):
    html = open(page, encoding="utf-8", errors="replace").read()
    out = []
    for h in re.findall(r'href="([^"]+\.pdf)"', html):
        u = urllib.parse.urljoin(base, h).replace("http://", "https://")  # plain http fails via the proxy
        if re.search(pattern, u) and u not in out:
            out.append(u)
    return out


def main():
    p17, p19, root, res = sys.argv[1:5]
    os.makedirs(res, exist_ok=True)
    targets = [("2017", u) for u in links(p17, "https://ais.win.tue.nl/bpi/2017/challenge.html", r"bpi2017_")]
    targets += [("2019", u) for u in links(p19, "https://icpmconference.org/2019/bpi-challenge/", r"BPI-Challenge")]
    rows, joint_out = [], []
    for year, url in targets:
        name = url.rsplit("/", 1)[-1]
        d = os.path.join(root, f"{year}_{name[:-4]}")
        os.makedirs(d, exist_ok=True)
        pdf = os.path.join(d, "report.pdf")
        p = subprocess.run(["curl", "-sS", "-L", "--max-time", "180", "-A", UA, "-o", pdf, "-w", "%{http_code}", url],
                           capture_output=True, text=True)
        time.sleep(2)
        code = p.stdout.strip()
        size = os.path.getsize(pdf) if os.path.exists(pdf) else 0
        sha, pages, nres, nrank, nstab, njoint = "", "", "", "", "", ""
        if code == "200" and size and open(pdf, "rb").read(4) == b"%PDF":
            sha = hashlib.sha256(open(pdf, "rb").read()).hexdigest()
            txt = os.path.join(d, "text.txt")
            subprocess.run(["pdftotext", "-layout", pdf, txt], check=False, capture_output=True)
            t = open(txt, encoding="utf-8", errors="replace").read()
            pages = t.count("\f") + 1
            nres, nrank, nstab = len(RES.findall(t)), len(RANK.findall(t)), len(STAB.findall(t))
            njoint = 0
            for pg, ptxt in enumerate(t.split("\f"), 1):
                for line in ptxt.split("\n"):
                    j = RES.search(line) and RANK.search(line)
                    s = STAB.search(line)
                    if j:
                        njoint += 1
                    if j or s:
                        joint_out.append(f"{year}\t{name}\tp{pg}\t{'J' if j else ''}{'S' if s else ''}\t{' '.join(line.split())[:200]}")
        rows.append([year, name, url, code, size, sha, pages, nres, nrank, nstab, njoint])
        print(year, name, code, size, pages, nres, nrank, nstab, njoint, flush=True)
    with open(os.path.join(res, "bpic_reports_screen.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["year", "file", "url", "http", "bytes", "sha256", "pages", "RES", "RANK", "STAB", "JOINT"])
        w.writerows(rows)
    with open(os.path.join(root, "bpic_joint_lines.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(joint_out))


if __name__ == "__main__":
    main()
