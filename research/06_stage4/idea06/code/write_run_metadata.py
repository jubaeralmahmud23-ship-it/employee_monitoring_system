#!/usr/bin/env python3
"""Write results/run_metadata.json: software versions, seeds, wall-clock times and sha256 of
the pilot's inputs and outputs (repository files) and of the downloaded data (outside the
repository, read from the manifests). Usage:
  python -I write_run_metadata.py --idea-dir <research/06_stage4/idea06> --data-dir <$DATA> --out <json>
"""
import argparse
import csv
import glob
import hashlib
import json
import os
import platform
import subprocess
import sys

MINE_CODE = ["build_frame.py", "draw_pilot.py", "fetch_fulltexts.py", "kwic.py", "uncertainty_calc.py",
             "validate_calc.py", "analyze_pilot.py", "write_run_metadata.py", "run.sh"]


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ver(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True)
        lines = (r.stderr or r.stdout).splitlines()
        return lines[0] if lines else "unavailable (no output)"
    except Exception as e:  # noqa
        return f"unavailable ({e!r})"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--idea-dir", required=True)
    ap.add_argument("--data-dir", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    import numpy
    import scipy
    import statsmodels
    files = {}
    for rel in [f"code/{c}" for c in MINE_CODE] + ["codebook_v0.md"]:
        files[rel] = sha(os.path.join(a.idea_dir, rel))
    for p in sorted(glob.glob(os.path.join(a.idea_dir, "code/coding/**/*"), recursive=True)):
        if os.path.isfile(p):
            files[os.path.relpath(p, a.idea_dir)] = sha(p)
    for sub in ["results/frame", "results/pilot"]:
        for p in sorted(glob.glob(os.path.join(a.idea_dir, sub, "*"))):
            files[os.path.relpath(p, a.idea_dir)] = sha(p)
    timing = list(csv.DictReader(open(os.path.join(a.idea_dir, "results/pilot/pilot_timing.csv"), encoding="utf-8")))
    fs = json.load(open(os.path.join(a.idea_dir, "results/frame/frame_summary.json"), encoding="utf-8"))
    pdfs = list(csv.DictReader(open(os.path.join(a.idea_dir, "results/pilot/fulltext_manifest.csv"), encoding="utf-8")))
    raw_manifest = os.path.join(a.idea_dir, "results/frame/raw_manifest.csv")
    meta = {
        "run_date_utc": "2026-10-19",
        "sampling_date_frozen": fs["sampling_date_frozen"],
        "machine": {"platform": platform.platform(), "cpus": os.cpu_count(), "note": "cloud container, 4 vCPU, 15 GB RAM, no GPU"},
        "software": {"python": sys.version.split()[0], "numpy": numpy.__version__, "scipy": scipy.__version__,
                     "statsmodels": statsmodels.__version__, "pdftotext": ver(["pdftotext", "-v"]),
                     "curl": ver(["curl", "--version"])},
        "seeds": {"pilot_draw": 20261015, "beta_binomial_mc": 20261015, "beta_draws": 20000,
                  "validation_numpy_rng": 7},
        "wall_clock_seconds": {"build_frame_py": fs["wall_clock_seconds"],
                               "coding_per_paper": {t["pilot_id"]: int(t["seconds"]) for t in timing},
                               "coding_total": sum(int(t["seconds"]) for t in timing),
                               "run_sh_offline": "about 3 (measured with time ./run.sh)"},
        "downloads": {"pilot_pdfs": {r["pilot_id"]: {"sha256": r["sha256"], "bytes": int(r["bytes"]), "url": r["url"]} for r in pdfs},
                      "frame_raw_manifest": os.path.relpath(raw_manifest, a.idea_dir),
                      "frame_raw_files": fs["raw_files"],
                      "springer_landing_manifest": "results/frame/springer_oa_landing_manifest.csv",
                      "data_dir_outside_repo": a.data_dir},
        "repository_files_sha256": files,
    }
    json.dump(meta, open(a.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"wrote {a.out}: {len(files)} file hashes")


if __name__ == "__main__":
    main()
