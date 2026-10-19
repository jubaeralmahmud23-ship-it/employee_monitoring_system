"""Step 06: placebo shuffles of resource labels (null distribution).

Usage:
    python -I 06_placebo.py <log> <log.parquet> <exclusions.json> <results_dir> <n_shuffles> <n_jobs>

Shuffle design (defined for this pilot): a "touch unit" is all events of one eligible resource in
one case.  Within strata defined by the activity of the touch unit's first event, the resource
labels of touch units are permuted at random.  Each resource keeps its number of touch units per
stratum (volume and role mix are preserved) while the link between a worker and particular cases,
timings and outcomes is broken.  Excluded (system / no-user) events are not shuffled.  The full
pipeline (gaps, work segments, attribution, case-mix fits, 117 configurations, analysis set) is
re-run on every shuffled log.  Seeds: numpy SeedSequence([20261015, 6]).spawn(n_shuffles).

Outputs: <log>_placebo.csv (one row per shuffle), <log>_placebo_summary.json
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


def summarize(P, S, distinct, cmpairs, key2cfg):
    A = L.analysis_set(P, S)
    T = L.tau_b_matrix(S[:, A])
    ts = L.summarize_tau(T, distinct)
    _, rs = L.summarize_reclass(S[:, A], cmpairs)
    met = distinct["metric"].to_numpy()
    iu, ju = np.triu_indices(len(distinct), 1)
    out = {"n_analysis_set": int(len(A)), "median_tau_distinct": ts["median_tau_distinct"],
           "median_tau_405cells": ts["median_tau_405cells"],
           "median_tau_within_metric_distinct": float(np.nanmedian(T[iu, ju][met[iu] == met[ju]])),
           "median_tau_cross_metric_distinct": float(np.nanmedian(T[iu, ju][met[iu] != met[ju]])),
           "median_reclass_bottom_distinct": rs["median_reclass_bottom_distinct"],
           "median_reclass_bottom_405": rs["median_reclass_bottom_405"],
           "median_status_change_all_distinct": rs["median_status_change_all_distinct"]}
    for name, ka, kb, _ in L.primary_contrasts():
        a, b = key2cfg[ka], key2cfg[kb]
        out[f"tau::{name}"] = float(T[a, b])
        out[f"reclass::{name}"] = L.reclass_rate(S[a, A], S[b, A])[0]
    return out


def one(seed_state):
    base, log, excl = G["base"], G["log"], G["excl"]
    rng = np.random.default_rng(seed_state)
    unit_code, unit_strat, unit_res, ev_unit = G["unit_code"], G["unit_strat"], G["unit_res"], G["ev_unit"]
    new_res = unit_res.copy()
    for s in np.unique(unit_strat):
        idx = np.flatnonzero(unit_strat == s)
        new_res[idx] = unit_res[idx][rng.permutation(len(idx))]
    b2 = base.copy()
    res = b2["res"].to_numpy(dtype=object).copy()
    m = ev_unit >= 0
    res[m] = new_res[ev_unit[m]]
    b2["res"] = res
    P = L.prepare(b2, log, excl)
    S = L.compute_scores(P, G["distinct"])
    return summarize(P, S, G["distinct"], G["cmpairs"], G["key2cfg"])


def main():
    log, path, exfile, outdir, n_sh, n_jobs = sys.argv[1:7]
    n_sh, n_jobs = int(n_sh), int(n_jobs)
    t0 = time.time()
    excl = json.load(open(exfile))[log]["primary"]
    base, _ = L.load_log(path, log)
    cells, distinct = L.build_space()
    key2cfg = dict(zip(distinct["key"], distinct["cfg"]))
    cmpairs = L.casemix_pairs(distinct)
    # observed
    P0 = L.prepare(base, log, excl)
    S0 = L.compute_scores(P0, distinct)
    obs = summarize(P0, S0, distinct, cmpairs, key2cfg)
    # touch units among eligible events
    elig = ~base["res"].isin(list(excl) + [L.NOUSER]).to_numpy()
    b = base.loc[elig, ["case", "res", "act", "ts", "eorder"]].copy()
    b["row"] = np.flatnonzero(elig)
    b = b.sort_values(["case", "ts", "eorder"], kind="stable")
    key = b["case"].astype(str) + "\x1f" + b["res"].astype(str)
    codes, uniq = pd.factorize(key, sort=False)
    first = pd.Series(np.arange(len(b))).groupby(codes).first().to_numpy()
    unit_strat = pd.factorize(b["act"].to_numpy()[first])[0]
    unit_res = b["res"].to_numpy(dtype=object)[first]
    ev_unit = np.full(len(base), -1, dtype=np.int64)
    ev_unit[b["row"].to_numpy()] = codes
    G.update({"base": base, "log": log, "excl": excl, "distinct": distinct, "cmpairs": cmpairs, "key2cfg": key2cfg,
              "unit_code": codes, "unit_strat": unit_strat, "unit_res": unit_res, "ev_unit": ev_unit})
    seeds = np.random.SeedSequence([L.SEED, 6]).spawn(n_sh)
    t1 = time.time()
    with mp.get_context("fork").Pool(n_jobs) as pool:
        reps = pool.map(one, seeds, chunksize=1)
    R = pd.DataFrame(reps)
    R.to_csv(os.path.join(outdir, f"{log}_placebo.csv"), index_label="shuffle")
    summ = {"log": log, "n_shuffles": n_sh, "seed": [L.SEED, 6], "touch_units": int(len(unit_res)),
            "strata": int(len(np.unique(unit_strat))), "seconds_placebo": round(time.time() - t1, 1),
            "seconds_total": round(time.time() - t0, 1), "observed": obs, "placebo": {}}
    for k in R.columns:
        v = R[k].to_numpy(dtype=float)
        summ["placebo"][k] = {"mean": float(np.nanmean(v)), "min": float(np.nanmin(v)), "max": float(np.nanmax(v)),
                              "p05": float(np.nanpercentile(v, 5)), "p95": float(np.nanpercentile(v, 95)),
                              "share_placebo_ge_observed": float(np.mean(v >= obs[k]))}
    with open(os.path.join(outdir, f"{log}_placebo_summary.json"), "w") as fh:
        json.dump(summ, fh, indent=1)
    keys = ["n_analysis_set", "median_tau_distinct", "median_tau_405cells", "median_tau_within_metric_distinct",
            "median_tau_cross_metric_distinct", "median_reclass_bottom_distinct", "median_status_change_all_distinct"]
    print(json.dumps({"observed": {k: obs[k] for k in keys}, "placebo": {k: summ["placebo"][k] for k in keys},
                      "seconds": summ["seconds_total"]}, indent=1))


if __name__ == "__main__":
    main()
