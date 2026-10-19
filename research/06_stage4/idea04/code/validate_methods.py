#!/usr/bin/env python3
"""Validate the interval code of ll144_pilot.py (loaded by file path, so the code under test is
exactly the pilot's compute_stats).

Checks:
  1. Katz log-ratio bounds against scipy.stats.contingency.relative_risk(...).confidence_interval;
  2. Clopper-Pearson 97.5% bounds against scipy.stats.binomtest(...).proportion_ci(method='exact');
  3. Monte Carlo coverage of the four 95% intervals when the true impact ratio is exactly 0.8, at
     group sizes typical of the corpus (synthetic data; data-generation seed 20261016).

Usage: python -I validate_methods.py --pilot <path/to/ll144_pilot.py> --out <csv>
"""
import argparse
import importlib.util
import time

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats.contingency import relative_risk

GEN_SEED = 20261016
REPS = 1000


def load_pilot(path):
    spec = importlib.util.spec_from_file_location("ll144_pilot", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def frame(ng, Ng, nc, Nc):
    k = len(ng)
    return pd.DataFrame({
        "tbl": [f"t{i:06d}" for i in range(k)], "row_id": np.arange(k), "comp_row_id": np.arange(k),
        "ng": np.asarray(ng, float), "Ng": np.asarray(Ng, float), "nc": np.asarray(nc, float), "Nc": np.asarray(Nc, float),
        "r_g": np.nan, "r_c": np.nan, "d_g": 2, "d_c": 2,
    })


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    P = load_pilot(args.pilot)
    rows = []
    t0 = time.perf_counter()

    # 1-2. deterministic agreement checks on count pairs spanning the corpus range
    cases = [(542, 678, 3162, 3543), (12, 130, 7, 95), (3, 23, 37, 980), (25000, 60000, 31000, 61000), (5, 40, 30, 50)]
    R, _ = P.compute_stats(frame(*zip(*cases)))
    for i, (a, A, c, C) in enumerate(cases):
        ci = relative_risk(a, A, c, C).confidence_interval(0.95)
        rows.append({"check": "katz_vs_scipy_relative_risk", "setting": f"{a}/{A} vs {c}/{C}",
                     "value": max(abs(R.loc[i, "katz_lo"] - ci.low), abs(R.loc[i, "katz_hi"] - ci.high)),
                     "expected": "< 1e-9"})
        lg = stats.binomtest(a, A).proportion_ci(confidence_level=0.975, method="exact")
        uc = stats.binomtest(c, C).proportion_ci(confidence_level=0.975, method="exact")
        rows.append({"check": "cp_bonf_lower_vs_scipy_binomtest", "setting": f"{a}/{A} vs {c}/{C}",
                     "value": abs(R.loc[i, "cp_lo"] - lg.low / uc.high), "expected": "< 1e-9"})

    # 3. coverage at a true ratio of 0.8
    rng = np.random.default_rng(GEN_SEED)
    settings = [(10, 50, 0.30), (30, 150, 0.50), (100, 500, 0.30), (500, 2500, 0.50), (5000, 25000, 0.30)]
    for Ng, Nc, pc in settings:
        pg = 0.8 * pc
        ng = rng.binomial(Ng, pg, REPS)
        nc = rng.binomial(Nc, pc, REPS)
        keep = nc > 0
        R, _ = P.compute_stats(frame(ng[keep], np.full(keep.sum(), Ng), nc[keep], np.full(keep.sum(), Nc)))
        for m, (lo, hi) in P.METHODS.items():
            cover = ((R[lo] <= 0.8) & (R[hi] >= 0.8)).mean()
            rows.append({"check": f"coverage_true_ratio_0.8_{m}", "setting": f"Ng={Ng} Nc={Nc} p_c={pc} reps={int(keep.sum())}",
                         "value": cover, "expected": "about 0.95 (CP-Bonferroni >= 0.95)"})
        rows.append({"check": "share_point_ratio_ge_0.8_when_true_ratio_is_0.8", "setting": f"Ng={Ng} Nc={Nc} p_c={pc}",
                     "value": (R["ir_point"] >= 0.8).mean(), "expected": "descriptive"})
    out = pd.DataFrame(rows)
    out.to_csv(args.out, index=False, float_format="%.6g")
    print(out.to_string())
    print(f"seconds: {time.perf_counter() - t0:.1f}")


if __name__ == "__main__":
    main()
