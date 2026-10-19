#!/usr/bin/env python3
"""Claim-survival calculator for idea 6 (standard library only).

Given a reported comparison of two proportions (accuracy-type metrics) at a reported n,
it asks whether the reported difference exceeds the interval implied by that n under:

  M1  binomial interval at the reported n
        - naive unpaired Wald SE of the difference (the idea card's "naive binomial SE");
        - Newcombe's hybrid score interval (method 10) as a check.
  M2  structure adjustment, only where the paper reports a structure
        - paired (same items): the paired SE is not identified from published tables, so it
          is bounded as the feasibility file proposes (paired lower bound ... unpaired upper
          bound): minimal discordance d = |delta| gives the smallest SE; the unpaired SE
          (zero item-level correlation) is the upper bound if the two systems' item-level
          errors are not negatively correlated. Survival is reported as 'all' (survives at
          the unpaired SE), 'some' (only at smaller SEs) or 'none'. The SE at maximal
          discordance d = min(pA+pB, 2-pA-pB) (negative correlation) is reported too.
        - clustered (cluster size m reported): Miller-style design effect
          sqrt(1 + (m-1)*ICC) applied to the unpaired SE, ICC in {0, 0.1, 0.3}.
  M3  run-to-run variance, Atil et al. "accuracy variations up to 15% across naturally
      occurring runs" (arXiv 2408.04667 abstract):
        - primary, worst case: a single-run accuracy may sit anywhere in a band of width
          15 percentage points, so a single-run difference survives only if |delta| > 15 pp;
        - sensitivity: sigma_run = 15/4 = 3.75 pp per arm (band read as +/- 2 sigma), added
          in quadrature to the M1 SE; a reported run SD replaces sigma_run.
  M4  Beta-Binomial (Bowyer et al. regime; the idea card's model (c)): independent
      Beta(1+k, 1+n-k) posteriors, Monte Carlo difference, 95% equal-tailed interval.

A claim "survives" a model when the model's 95% interval for the difference excludes 0
(equivalently |delta| > 1.96 SE for the normal-approximation models).

Usage:
  python -I uncertainty_calc.py --claims claims.csv --out survival.csv [--seed 20261015]
  python -I uncertainty_calc.py --selftest
"""
import argparse
import csv
import math
import random
import sys

Z = 1.959963984540054  # two-sided 95% normal quantile
ICCS = (0.0, 0.1, 0.3)


def wilson(k, n, z=Z):
    if n <= 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (centre - half, centre + half)


def wald_diff(pa, na, pb, nb):
    se = math.sqrt(pa * (1 - pa) / na + pb * (1 - pb) / nb)
    d = pa - pb
    return d, se, (d - Z * se, d + Z * se)


def newcombe_diff(ka, na, kb, nb):
    """Newcombe (1998) method 10: hybrid score interval for pA - pB (independent)."""
    pa, pb = ka / na, kb / nb
    l1, u1 = wilson(ka, na)
    l2, u2 = wilson(kb, nb)
    d = pa - pb
    lo = d - math.sqrt((pa - l1) ** 2 + (u2 - pb) ** 2)
    hi = d + math.sqrt((u1 - pa) ** 2 + (pb - l2) ** 2)
    return (lo, hi)


def paired_bounds(pa, pb, n):
    """Bounds on the SE of a paired difference of proportions on the same n items."""
    d = pa - pb
    dmin = abs(d)
    dmax = min(pa + pb, 2 - pa - pb)
    var_min = max(dmin - d * d, 0.0) / n
    var_max = max(dmax - d * d, 0.0) / n
    return math.sqrt(var_min), math.sqrt(var_max)


def beta_binomial(ka, na, kb, nb, draws, rng):
    diffs = []
    sup = 0
    for _ in range(draws):
        ta = rng.betavariate(1 + ka, 1 + na - ka)
        tb = rng.betavariate(1 + kb, 1 + nb - kb)
        diffs.append(ta - tb)
        sup += ta > tb
    diffs.sort()
    lo = diffs[int(0.025 * draws)]
    hi = diffs[min(int(0.975 * draws), draws - 1)]
    return lo, hi, sup / draws


def yn(b):
    return "yes" if b else "no"


def evaluate(row, draws, rng, band_pp=15.0):
    pa = float(row["p_a_pct"]) / 100.0
    pb = float(row["p_b_pct"]) / 100.0
    na = int(float(row["n_a"]))
    nb = int(float(row["n_b"]))
    ka = round(pa * na)
    kb = round(pb * nb)
    d, se, (lo, hi) = wald_diff(pa, na, pb, nb)
    out = dict(row)
    out.update({
        "k_a": ka, "k_b": kb,
        "diff_pp": round(100 * d, 3),
        "M1_wald_se_pp": round(100 * se, 3),
        "M1_wald_ci_pp": f"[{100*lo:.2f}, {100*hi:.2f}]",
        "M1_wald_survives": yn(abs(d) > Z * se),
    })
    nlo, nhi = newcombe_diff(ka, na, kb, nb)
    out["M1_newcombe_ci_pp"] = f"[{100*nlo:.2f}, {100*nhi:.2f}]"
    out["M1_newcombe_survives"] = yn(nlo > 0 or nhi < 0)
    out["M1_min_detectable_diff_pp"] = round(100 * Z * se, 2)

    structure = row.get("structure", "")
    if "paired" in structure:
        n = min(na, nb)
        se_min, se_max = paired_bounds(pa, pb, n)
        se_ind = math.sqrt(pa * (1 - pa) / n + pb * (1 - pb) / n)
        best = abs(d) > Z * se_min
        upper = abs(d) > Z * se_ind
        out["M2_paired_se_range_pp"] = f"[{100*se_min:.2f}, {100*se_ind:.2f}]"
        out["M2_paired_survival"] = "all" if upper else ("some" if best else "none")
        out["M2_paired_se_max_discordance_pp"] = round(100 * se_max, 3)
        out["M2_paired_survives_max_discordance"] = yn(abs(d) > Z * se_max)
    else:
        out["M2_paired_se_range_pp"] = "NA"
        out["M2_paired_survival"] = "NA (no paired structure reported)"
        out["M2_paired_se_max_discordance_pp"] = "NA"
        out["M2_paired_survives_max_discordance"] = "NA"
    m = row.get("cluster_m", "")
    if m not in ("", None):
        m = float(m)
        for icc in ICCS:
            deff = 1 + (m - 1) * icc
            sec = se * math.sqrt(deff)
            out[f"M2_cluster_icc{icc}_se_pp"] = round(100 * sec, 3)
            out[f"M2_cluster_icc{icc}_survives"] = yn(abs(d) > Z * sec)
    else:
        for icc in ICCS:
            out[f"M2_cluster_icc{icc}_se_pp"] = "NA"
            out[f"M2_cluster_icc{icc}_survives"] = "NA (no cluster structure reported)"

    runs = row.get("runs", "1") or "1"
    run_sd = row.get("run_sd_pp", "")
    if run_sd not in ("", None):
        sigma = float(run_sd) / 100.0
        k = max(int(float(runs)), 1)
        se_run = math.sqrt(se * se + 2 * sigma * sigma / k)
        out["M3_band_worst_survives"] = "NA (run SD reported)"
        out["M3_sd_total_se_pp"] = round(100 * se_run, 3)
        out["M3_sd_survives"] = yn(abs(d) > Z * se_run)
    else:
        sigma = band_pp / 4.0 / 100.0
        se_run = math.sqrt(se * se + 2 * sigma * sigma)
        out["M3_band_worst_survives"] = yn(abs(100 * d) > band_pp)
        out["M3_sd_total_se_pp"] = round(100 * se_run, 3)
        out["M3_sd_survives"] = yn(abs(d) > Z * se_run)

    blo, bhi, psup = beta_binomial(ka, na, kb, nb, draws, rng)
    out["M4_beta_cri_pp"] = f"[{100*blo:.2f}, {100*bhi:.2f}]"
    out["M4_p_a_greater"] = round(psup, 4)
    out["M4_beta_survives"] = yn(blo > 0 or bhi < 0)
    return out


def selftest():
    ok = True
    # Newcombe (1998), Statistics in Medicine 17:873-890, example 56/70 vs 48/80, method 10.
    # Reference values 0.0524 and 0.3339 are recalled, not re-read in this run; the
    # independent check is validate_calc.py (comparison with statsmodels).
    lo, hi = newcombe_diff(56, 70, 48, 80)
    ok &= abs(lo - 0.0524) < 5e-4 and abs(hi - 0.3339) < 5e-4
    print(f"Newcombe 56/70 vs 48/80: [{lo:.4f}, {hi:.4f}] (reference 0.0524, 0.3339, recalled)")
    # Wilson for 0/10 must have lower bound 0
    l, u = wilson(0, 10)
    ok &= abs(l) < 1e-12
    print(f"Wilson 0/10: [{l:.4f}, {u:.4f}]")
    # Paired bounds: with discordance at its minimum the SE equals sqrt(|d|(1-|d|)/n)
    smin, smax = paired_bounds(0.6, 0.5, 100)
    ok &= abs(smin - math.sqrt(0.1 * 0.9 / 100)) < 1e-12
    print(f"paired bounds 0.6 vs 0.5, n=100: [{smin:.4f}, {smax:.4f}]")
    print("SELFTEST", "PASS" if ok else "FAIL")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--claims")
    ap.add_argument("--out")
    ap.add_argument("--seed", type=int, default=20261015)
    ap.add_argument("--draws", type=int, default=20000)
    ap.add_argument("--band-pp", type=float, default=15.0)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(0 if selftest() else 1)
    rng = random.Random(a.seed)
    rows = list(csv.DictReader(open(a.claims, encoding="utf-8")))
    outs = [evaluate(r, a.draws, rng, a.band_pp) for r in rows]
    fields = list(outs[0].keys())
    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(outs)
    for o in outs:
        print(o["claim_id"], o["diff_pp"], "M1", o["M1_wald_survives"], "M2p", o["M2_paired_survival"],
              "M3", o["M3_band_worst_survives"], o["M3_sd_survives"], "M4", o["M4_beta_survives"])


if __name__ == "__main__":
    main()
