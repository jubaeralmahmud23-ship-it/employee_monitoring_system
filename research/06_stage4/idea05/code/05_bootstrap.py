"""Step 05: case bootstrap of the primary contrasts and of the stopping-rule statistics.

Usage:
    python -I 05_bootstrap.py <log> <log.parquet> <exclusions.json> <results_dir> <B> <n_jobs>

Each replicate resamples cases with replacement (multinomial case weights, seed 20261015 via
numpy SeedSequence.spawn), re-aggregates every one of the 117 distinct configurations and
recomputes Kendall tau-b and bottom-quintile reclassification.  Per-unit quantities that depend
on the whole timeline (active-time credits, expected values of the case-mix models, case
completion and attribution) are held at their full-sample values: intervals are conditional on
the fitted case-mix models and on the attribution of each case.

Outputs: <log>_bootstrap_contrasts.csv, <log>_bootstrap_stopping.json, <log>_bootstrap_replicates.csv
"""
import json
import multiprocessing as mp
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import idea05lib as L  # noqa: E402

G = {}


def stats_for(S, A, distinct, cmpairs, contrasts, key2cfg, within_mask_iu):
    T = L.tau_b_matrix(S[:, A])
    ts = L.summarize_tau(T, distinct)
    _, rs = L.summarize_reclass(S[:, A], cmpairs)
    k = T.shape[0]
    iu, ju = np.triu_indices(k, 1)
    out = {"median_tau_distinct": ts["median_tau_distinct"], "median_tau_405cells": ts["median_tau_405cells"],
           "median_tau_within_metric_distinct": float(np.nanmedian(T[iu, ju][within_mask_iu])),
           "median_reclass_bottom_distinct": rs["median_reclass_bottom_distinct"],
           "median_reclass_bottom_405": rs["median_reclass_bottom_405"],
           "median_status_change_all_distinct": rs["median_status_change_all_distinct"]}
    for name, ka, kb, _ in contrasts:
        a, b = key2cfg[ka], key2cfg[kb]
        out[f"tau::{name}"] = float(T[a, b])
        out[f"reclass::{name}"] = L.reclass_rate(S[a, A], S[b, A])[0]
    return out


def one(seed_state):
    P, distinct, A = G["P"], G["distinct"], G["A"]
    rng = np.random.default_rng(seed_state)
    nC = P["nC"]
    w = np.bincount(rng.integers(0, nC, nC), minlength=nC).astype(float)
    S = L.compute_scores(P, distinct, w_case=w)
    return stats_for(S, A, distinct, G["cmpairs"], G["contrasts"], G["key2cfg"], G["within"])


def main():
    log, path, exfile, outdir, B, n_jobs = sys.argv[1:7]
    B, n_jobs = int(B), int(n_jobs)
    t0 = time.time()
    excl = json.load(open(exfile))[log]["primary"]
    base, _ = L.load_log(path, log)
    cells, distinct = L.build_space()
    P = L.prepare(base, log, excl)
    S0 = L.compute_scores(P, distinct)
    A = L.analysis_set(P, S0)
    key2cfg = dict(zip(distinct["key"], distinct["cfg"]))
    met = distinct["metric"].to_numpy()
    iu, ju = np.triu_indices(len(distinct), 1)
    G.update({"P": P, "distinct": distinct, "A": A, "cmpairs": L.casemix_pairs(distinct),
              "contrasts": L.primary_contrasts(), "key2cfg": key2cfg, "within": met[iu] == met[ju]})
    point = stats_for(S0, A, distinct, G["cmpairs"], G["contrasts"], key2cfg, G["within"])
    seeds = np.random.SeedSequence(L.SEED).spawn(B)
    t1 = time.time()
    ctx = mp.get_context("fork")
    with ctx.Pool(n_jobs) as pool:
        reps = pool.map(one, seeds, chunksize=max(1, B // (4 * n_jobs)))
    t_boot = time.time() - t1
    R = pd.DataFrame(reps)
    R.to_csv(os.path.join(outdir, f"{log}_bootstrap_replicates.csv"), index_label="replicate")
    rows = []
    for name, ka, kb, fam in G["contrasts"]:
        for stat in ("tau", "reclass"):
            v = R[f"{stat}::{name}"].to_numpy(dtype=float)
            rows.append({"contrast": name, "family": fam, "statistic": "kendall_tau_b" if stat == "tau" else "bottom_quintile_reclassification",
                         "point": point[f"{stat}::{name}"], "boot_mean": float(np.nanmean(v)), "boot_sd": float(np.nanstd(v, ddof=1)),
                         "ci95_lo": float(np.nanpercentile(v, 2.5)), "ci95_hi": float(np.nanpercentile(v, 97.5)),
                         "n_valid_replicates": int(np.isfinite(v).sum())})
    pd.DataFrame(rows).to_csv(os.path.join(outdir, f"{log}_bootstrap_contrasts.csv"), index=False)
    summ = {"log": log, "replicates": B, "seed": L.SEED, "n_jobs": n_jobs, "n_analysis_set": int(len(A)),
            "seconds_bootstrap": round(t_boot, 1), "seconds_total": round(time.time() - t0, 1),
            "resampling_unit": "case (multinomial weights)", "held_fixed": "active-time credits, case-mix model fits, case completion and attribution"}
    for k in ["median_tau_distinct", "median_tau_405cells", "median_tau_within_metric_distinct", "median_reclass_bottom_distinct",
              "median_reclass_bottom_405", "median_status_change_all_distinct"]:
        v = R[k].to_numpy(dtype=float)
        summ[k] = {"point": point[k], "ci95_lo": float(np.nanpercentile(v, 2.5)), "ci95_hi": float(np.nanpercentile(v, 97.5)),
                   "boot_mean": float(np.nanmean(v))}
    summ["share_replicates_median_tau_distinct_gt_0.9"] = float(np.mean(R["median_tau_distinct"] > 0.9))
    summ["share_replicates_median_reclass_bottom_distinct_lt_0.10"] = float(np.mean(R["median_reclass_bottom_distinct"] < 0.10))
    with open(os.path.join(outdir, f"{log}_bootstrap_stopping.json"), "w") as fh:
        json.dump(summ, fh, indent=1)
    print(json.dumps(summ, indent=1))


if __name__ == "__main__":
    main()
