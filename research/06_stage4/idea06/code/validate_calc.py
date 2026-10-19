#!/usr/bin/env python3
"""Validate uncertainty_calc.py against independent implementations (statsmodels, numpy).

Checks, on a grid of (k_a, n_a, k_b, n_b):
  - Wilson intervals vs statsmodels.stats.proportion.proportion_confint(method='wilson');
  - Newcombe hybrid-score difference intervals vs
    statsmodels.stats.proportion.confint_proportions_2indep(method='newcomb');
  - Beta-Binomial Monte Carlo interval (20,000 draws, stdlib) vs a 1,000,000-draw numpy
    Monte Carlo with a different seed (agreement within 0.5 percentage points).
Writes a CSV with the maximum absolute differences.
"""
import argparse
import csv
import importlib.util
import random

import numpy as np
import statsmodels
from statsmodels.stats.proportion import confint_proportions_2indep, proportion_confint


def load(path):
    spec = importlib.util.spec_from_file_location("uc", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calc", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    uc = load(a.calc)
    grid = [(5, 30, 2, 30), (16, 30, 12, 30), (47, 100, 42, 100), (350, 500, 313, 500),
            (2815, 2932, 2812, 2932), (20, 30, 13, 30), (56, 70, 48, 80), (0, 10, 3, 10)]
    rows = []
    max_w = max_n = max_b = 0.0
    for ka, na, kb, nb in grid:
        lo, hi = uc.wilson(ka, na)
        slo, shi = proportion_confint(ka, na, alpha=0.05, method="wilson")
        dw = max(abs(lo - slo), abs(hi - shi))
        nlo, nhi = uc.newcombe_diff(ka, na, kb, nb)
        snlo, snhi = confint_proportions_2indep(ka, na, kb, nb, method="newcomb", compare="diff", alpha=0.05)
        dn = max(abs(nlo - snlo), abs(nhi - snhi))
        blo, bhi, _ = uc.beta_binomial(ka, na, kb, nb, 20000, random.Random(20261015))
        g = np.random.default_rng(7)
        diff = g.beta(1 + ka, 1 + na - ka, 1_000_000) - g.beta(1 + kb, 1 + nb - kb, 1_000_000)
        rlo, rhi = np.quantile(diff, [0.025, 0.975])
        db = max(abs(blo - rlo), abs(bhi - rhi))
        max_w, max_n, max_b = max(max_w, dw), max(max_n, dn), max(max_b, db)
        rows.append({"case": f"{ka}/{na} vs {kb}/{nb}", "wilson_absdiff": f"{dw:.2e}",
                     "newcombe_absdiff": f"{dn:.2e}", "beta_mc_absdiff_pp": f"{100*db:.3f}",
                     "calc_newcombe": f"[{nlo:.4f}, {nhi:.4f}]",
                     "statsmodels_newcombe": f"[{snlo:.4f}, {snhi:.4f}]"})
    rows.append({"case": "MAX", "wilson_absdiff": f"{max_w:.2e}", "newcombe_absdiff": f"{max_n:.2e}",
                 "beta_mc_absdiff_pp": f"{100*max_b:.3f}",
                 "calc_newcombe": "", "statsmodels_newcombe": f"statsmodels {statsmodels.__version__}"})
    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    ok = max_w < 1e-9 and max_n < 1e-9 and max_b < 0.005
    print(f"max |Wilson diff| {max_w:.2e}; max |Newcombe diff| {max_n:.2e}; max |Beta MC diff| {100*max_b:.3f} pp ->",
          "PASS" if ok else "FAIL")


if __name__ == "__main__":
    main()
