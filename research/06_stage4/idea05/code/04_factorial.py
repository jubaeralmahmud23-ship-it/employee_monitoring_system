"""Step 04: full 405-cell factorial (117 distinct score vectors) on one log: point estimates.

Usage:
    python -I 04_factorial.py <log> <log.parquet> <exclusions.json> <results_dir> <derived_dir>

Outputs (results_dir, aggregate only, prefixed by log name):
  config_space.csv / config_distinct.csv          configuration space (written once)
  <log>_config_summary.csv                        per distinct configuration: score distribution, agreement with baseline
  <log>_tau_summary.json                          stopping-rule quantities and tau distribution summaries
  <log>_tau_hist.csv                              tau histogram (distinct pairs and 405-cell pairs)
  <log>_tau_by_factor.csv                         median tau for pairs differing in exactly one factor, within-metric etc.
  <log>_casemix_reclass.csv                       bottom-quintile reclassification for all none-vs-adjusted pairs
  <log>_primary_contrasts_point.csv               point estimates for the primary contrasts
  <log>_variance_decomposition.csv                main-effect shares of rank-percentile variance over the 405 cells
  <log>_window_stability.csv                      H3: stability by window length (three views)
  <log>_case_difficulty.csv                       Spearman between assigned case difficulty and raw scores
  <log>_sensitivity.csv                           exclusion sets, minimum-event threshold, complete-case set
  <log>_system_account_attribution.json           share of cases/events captured by excluded accounts when included
The per-resource score matrix is saved to derived_dir only (pseudonymous per-worker rankings are not released).
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import idea05lib as L  # noqa: E402

FACTORS = ["metric", "attr", "win", "gap", "adj"]


def run(base, log, distinct, cmpairs, excluded, n_min=L.N_MIN_EVENTS, complete_case=False, keep_slots=False):
    P = L.prepare(base, log, excluded)
    if keep_slots:
        S, slots = L.compute_scores(P, distinct, keep_slots=True)
    else:
        S, slots = L.compute_scores(P, distinct), None
    A = L.analysis_set(P, S, n_min, complete_case)
    T = L.tau_b_matrix(S[:, A])
    tsum = L.summarize_tau(T, distinct)
    pairs, rsum = L.summarize_reclass(S[:, A], cmpairs)
    return {"P": P, "S": S, "A": A, "T": T, "tsum": tsum, "pairs": pairs, "rsum": rsum, "slots": slots}


def pair_table(T, distinct):
    k = len(distinct)
    iu, ju = np.triu_indices(k, 1)
    d = distinct.reset_index(drop=True)
    df = pd.DataFrame({"i": iu, "j": ju, "tau": T[iu, ju]})
    parts = np.array([k.split("|") for k in d["key"]], dtype=object)   # inapplicable levels are "-"
    for fi, f in enumerate(FACTORS):
        a = parts[:, fi]
        df[f"diff_{f}"] = a[iu] != a[ju]
    df["n_diff"] = df[[f"diff_{f}" for f in FACTORS]].sum(axis=1)
    df["same_metric"] = ~df["diff_metric"]
    df["weight405"] = d["multiplicity"].to_numpy()[iu] * d["multiplicity"].to_numpy()[ju]
    return df


def variance_decomposition(S, A_cc, cells, distinct):
    sub = S[:, A_cc]
    n = sub.shape[1]
    ranks = np.argsort(np.argsort(sub, axis=1, kind="stable"), axis=1, kind="stable")
    pct = (ranks + 0.5) / n                       # percentile rank per config
    V = pct[cells["cfg"].to_numpy()]              # 405 x n
    grand = V.mean(axis=0)
    sst = ((V - grand) ** 2).sum(axis=0)
    rows = []
    shares = {}
    for f in FACTORS:
        lev = cells[f].astype(str).to_numpy()
        ss = np.zeros(n)
        for l in np.unique(lev):
            m = lev == l
            ss += m.sum() * (V[m].mean(axis=0) - grand) ** 2
        shares[f] = ss
    resid = sst - sum(shares.values())
    for f, ss in list(shares.items()) + [("interactions", resid)]:
        ok = sst > 0
        rows.append({"factor": f, "mean_share_per_worker": float(np.mean(ss[ok] / sst[ok])),
                     "median_share_per_worker": float(np.median(ss[ok] / sst[ok])),
                     "pooled_share": float(ss.sum() / sst.sum())})
    out = pd.DataFrame(rows)
    out["n_workers"] = int(n)
    out["mean_sd_of_rank_percentile_across_405_cells"] = float(np.mean(np.sqrt(sst / len(cells))))
    return out


def window_stability(res, distinct, min_res=20):
    S, A, slots = res["S"], res["A"], res["slots"]
    rows = []
    T = res["T"]
    for w in L.WINS:
        ids = distinct.index[distinct["win"] == w].to_numpy()
        sub = T[np.ix_(ids, ids)]
        iu = np.triu_indices(len(ids), 1)
        whole = float(np.nanmedian(sub[iu]))
        # per-slot (dashboard view) cross-configuration tau
        nS = next(iter(slots[int(i)] for i in ids)).shape[1]
        per_slot_medians, n_slots_used = [], 0
        stacked = np.stack([L.ORIENT[distinct.loc[i, "metric"]] * slots[int(i)][A] for i in ids])  # cfg x nA x nS
        for s in range(nS):
            M = stacked[:, :, s]
            if np.isfinite(M).any(axis=0).sum() < min_res:
                continue
            Ts = L.tau_b_matrix(M)
            per_slot_medians.append(np.nanmedian(Ts[iu]))
            n_slots_used += 1
        # temporal stability: Spearman between consecutive slots, per config
        temporal = []
        for ci in range(len(ids)):
            M = stacked[ci]
            vals = []
            for s in range(nS - 1):
                a, b = M[:, s], M[:, s + 1]
                m = np.isfinite(a) & np.isfinite(b)
                if m.sum() >= 10:
                    vals.append(pd.Series(a[m]).corr(pd.Series(b[m]), method="spearman"))
            if vals:
                temporal.append(np.nanmedian(vals))
        rows.append({"window": w, "n_slots": int(nS), "n_configs": int(len(ids)),
                     "median_cross_config_tau_whole_log_ranking": whole,
                     "median_over_slots_of_median_cross_config_tau_per_slot": float(np.nanmedian(per_slot_medians)) if per_slot_medians else np.nan,
                     "slots_used_per_slot_view": int(n_slots_used),
                     "median_over_configs_of_adjacent_slot_spearman": float(np.nanmedian(temporal)) if temporal else np.nan})
    return pd.DataFrame(rows)


def main():
    log, path, exfile, outdir, derived = sys.argv[1:6]
    t0 = time.time()
    os.makedirs(outdir, exist_ok=True)
    os.makedirs(derived, exist_ok=True)
    excl = json.load(open(exfile))[log]
    base, info = L.load_log(path, log)
    cells, distinct = L.build_space()
    cells.to_csv(os.path.join(outdir, "config_space.csv"), index=False)
    distinct.to_csv(os.path.join(outdir, "config_distinct.csv"), index=False)
    cmpairs = L.casemix_pairs(distinct)
    key2cfg = dict(zip(distinct["key"], distinct["cfg"]))

    res = run(base, log, distinct, cmpairs, excl["primary"], keep_slots=True)
    P, S, A, T = res["P"], res["S"], res["A"], res["T"]
    np.savez_compressed(os.path.join(derived, f"{log}_scores_primary.npz"), S=S, A=A, res_names=P["res_names"].astype(str))

    # 1. per-config summary
    base_cfg = key2cfg[L.BASELINE]
    rows = []
    for _, r in distinct.iterrows():
        x = S[int(r["cfg"]), A]
        fin = np.isfinite(x)
        ra, _ = L.reclass_rate(S[base_cfg, A], x)
        sp = pd.Series(S[base_cfg, A]).corr(pd.Series(x), method="spearman")
        bset, bsize = L.bottom_set(x)
        rows.append({**r.to_dict(), "n_ranked": int(fin.sum()), "n_undefined": int((~fin).sum()),
                     "bottom_quintile_k": int(np.floor(0.2 * fin.sum() + 0.5)), "bottom_set_size_inclusive_ties": int(bsize),
                     "oriented_score_mean": float(np.nanmean(x)), "oriented_score_sd": float(np.nanstd(x)),
                     "oriented_score_median": float(np.nanmedian(x)),
                     "oriented_score_p25": float(np.nanpercentile(x, 25)), "oriented_score_p75": float(np.nanpercentile(x, 75)),
                     "tau_with_baseline": float(T[base_cfg, int(r["cfg"])]), "spearman_with_baseline": float(sp),
                     "bottom_quintile_share_leaving_vs_baseline": float(ra)})
    pd.DataFrame(rows).to_csv(os.path.join(outdir, f"{log}_config_summary.csv"), index=False)

    # 2. tau summaries
    pt = pair_table(T, distinct)
    within = pt[pt["same_metric"]]
    tsum = dict(res["tsum"])
    tsum.update({
        "log": log, "excluded_accounts": len(excl["primary"]), "n_min_events": L.N_MIN_EVENTS,
        "n_analysis_set": int(len(A)), "n_eligible_resources": int(P["eligible"].sum()),
        "median_tau_within_metric_distinct": float(np.nanmedian(within["tau"])),
        "median_tau_within_metric_405cells": L.weighted_median(
            np.r_[within["tau"].to_numpy(), np.ones(len(distinct))],
            np.r_[within["weight405"].to_numpy(), distinct["multiplicity"].to_numpy() * (distinct["multiplicity"].to_numpy() - 1) / 2.0]),
        "median_tau_by_metric_within": {m: float(np.nanmedian(within.loc[distinct.loc[within["i"], "metric"].to_numpy() == m, "tau"])) for m in L.METRICS},
        "median_tau_cross_metric_distinct": float(np.nanmedian(pt.loc[~pt["same_metric"], "tau"])),
        "reclassification": res["rsum"],
        "T_days_deadline": P["T_days"], "completed_cases": int(P["completed"].sum()), "cases": int(P["nC"]),
        "processing_time_mode": P["apt"]["mode"],
        "casemix_covariates": P["Xcase_names"][:60],
    })
    with open(os.path.join(outdir, f"{log}_tau_summary.json"), "w") as fh:
        json.dump(tsum, fh, indent=1, default=float)
    bins = np.round(np.arange(-1.0, 1.0001, 0.05), 2)
    h1, _ = np.histogram(pt["tau"].dropna(), bins=bins)
    h2, _ = np.histogram(pt["tau"].dropna(), bins=bins, weights=pt.loc[pt["tau"].notna(), "weight405"])
    h3, _ = np.histogram(within["tau"].dropna(), bins=bins)
    pd.DataFrame({"bin_lo": bins[:-1], "bin_hi": bins[1:], "distinct_pairs": h1, "cell405_pairs_excluding_identical": h2,
                  "within_metric_distinct_pairs": h3}).to_csv(os.path.join(outdir, f"{log}_tau_hist.csv"), index=False)
    frows = []
    for f in FACTORS:
        m = (pt["n_diff"] == 1) & pt[f"diff_{f}"]
        frows.append({"pairs": f"differ only in {f}", "n_pairs": int(m.sum()), "median_tau": float(np.nanmedian(pt.loc[m, "tau"])) if m.any() else np.nan,
                      "mean_tau": float(np.nanmean(pt.loc[m, "tau"])) if m.any() else np.nan,
                      "min_tau": float(np.nanmin(pt.loc[m, "tau"])) if m.any() else np.nan})
    for lab, m in (("same metric, any other difference", pt["same_metric"]), ("different metric", ~pt["same_metric"]), ("all distinct pairs", pt["tau"].notna())):
        frows.append({"pairs": lab, "n_pairs": int(m.sum()), "median_tau": float(np.nanmedian(pt.loc[m, "tau"])),
                      "mean_tau": float(np.nanmean(pt.loc[m, "tau"])), "min_tau": float(np.nanmin(pt.loc[m, "tau"]))})
    for m1 in L.METRICS:
        for m2 in L.METRICS:
            if m1 >= m2:
                continue
            a = distinct.loc[pt["i"], "metric"].to_numpy()
            b = distinct.loc[pt["j"], "metric"].to_numpy()
            mm = ((a == m1) & (b == m2)) | ((a == m2) & (b == m1))
            frows.append({"pairs": f"metric pair {m1}-{m2}", "n_pairs": int(mm.sum()), "median_tau": float(np.nanmedian(pt.loc[mm, "tau"])),
                          "mean_tau": float(np.nanmean(pt.loc[mm, "tau"])), "min_tau": float(np.nanmin(pt.loc[mm, "tau"]))})
    pd.DataFrame(frows).to_csv(os.path.join(outdir, f"{log}_tau_by_factor.csv"), index=False)

    # 3. case-mix reclassification
    res["pairs"].to_csv(os.path.join(outdir, f"{log}_casemix_reclass.csv"), index=False)

    # 4. primary contrasts (point)
    prow = []
    for name, ka, kb, fam in L.primary_contrasts():
        a, b = key2cfg[ka], key2cfg[kb]
        r1, r2 = L.reclass_rate(S[a, A], S[b, A])
        m = np.isfinite(S[a, A]) & np.isfinite(S[b, A])
        prow.append({"contrast": name, "family": fam, "config_a": ka, "config_b": kb, "n_pairwise": int(m.sum()),
                     "tau": float(T[a, b]), "spearman": float(pd.Series(S[a, A][m]).corr(pd.Series(S[b, A][m]), method="spearman")),
                     "reclass_bottom": r1, "status_change_all": r2})
    pd.DataFrame(prow).to_csv(os.path.join(outdir, f"{log}_primary_contrasts_point.csv"), index=False)

    # 5. variance decomposition on the complete-case subset
    A_cc = L.analysis_set(P, S, complete_case=True)
    variance_decomposition(S, A_cc, cells, distinct).to_csv(os.path.join(outdir, f"{log}_variance_decomposition.csv"), index=False)

    # 6. H3 window stability
    window_stability(res, distinct).to_csv(os.path.join(outdir, f"{log}_window_stability.csv"), index=False)

    # 7. case difficulty vs raw scores (last-touch, month, gap 60)
    cu = P["cases"]["last"]
    diff = np.bincount(cu["res"], weights=cu["e"]["regression"][:, 0], minlength=P["nR"]) / np.maximum(np.bincount(cu["res"], minlength=P["nR"]), 1)
    diff[np.bincount(cu["res"], minlength=P["nR"]) == 0] = np.nan
    crow = []
    for m in L.METRICS:
        for adj in L.ADJS:
            k = L.distinct_key(m, "last", "month", 60, adj)
            x = S[key2cfg[k], A]
            d = diff[A]
            ok = np.isfinite(x) & np.isfinite(d)
            crow.append({"config": k, "n": int(ok.sum()),
                         "spearman_oriented_score_vs_mean_expected_case_effort": float(pd.Series(x[ok]).corr(pd.Series(d[ok]), method="spearman"))})
    pd.DataFrame(crow).to_csv(os.path.join(outdir, f"{log}_case_difficulty.csv"), index=False)

    # 8. sensitivity runs
    srows = []

    def srow(label, r):
        t, q = r["tsum"], r["rsum"]
        pt2 = pair_table(r["T"], distinct)
        srows.append({"variant": label, "n_ranked": int(len(r["A"])),
                      "median_tau_distinct": t["median_tau_distinct"], "median_tau_405cells": t["median_tau_405cells"],
                      "median_tau_within_metric_distinct": float(np.nanmedian(pt2.loc[pt2["same_metric"], "tau"])),
                      "median_reclass_bottom_distinct": q["median_reclass_bottom_distinct"],
                      "median_reclass_bottom_405": q["median_reclass_bottom_405"],
                      "median_status_change_all_distinct": q["median_status_change_all_distinct"],
                      "baseline_vs_regression_reclass_bottom": float(r["pairs"].set_index(["key_a", "key_b"]).loc[(L.BASELINE, L.BASELINE.rsplit("|", 1)[0] + "|regression"), "reclass_bottom"])})

    srow(f"primary (exclusion={excl['primary'][:3]}{'...' if len(excl['primary']) > 3 else ''} n={len(excl['primary'])}; n_min={L.N_MIN_EVENTS}; pairwise-complete)", res)
    rcc = dict(res)
    rcc["A"] = A_cc
    rcc["T"] = L.tau_b_matrix(S[:, A_cc])
    rcc["tsum"] = L.summarize_tau(rcc["T"], distinct)
    rcc["pairs"], rcc["rsum"] = L.summarize_reclass(S[:, A_cc], cmpairs)
    srow("complete-case set (defined in all 117 configurations)", rcc)
    rti = {"A": A, "T": T, "tsum": res["tsum"]}
    rti["pairs"], rti["rsum"] = L.summarize_reclass(S[:, A], cmpairs, ties="index")
    srow("tie rule for quintiles: exactly k, ties broken by index (instead of inclusive)", rti)
    for nm in [1, 20, 500]:
        A2 = L.analysis_set(P, S, nm)
        r2 = {"A": A2, "T": L.tau_b_matrix(S[:, A2])}
        r2["tsum"] = L.summarize_tau(r2["T"], distinct)
        r2["pairs"], r2["rsum"] = L.summarize_reclass(S[:, A2], cmpairs)
        srow(f"n_min={nm} events", r2)
    sysattr = {}
    for label, ex in excl.items():
        if label == "primary":
            continue
        r3 = run(base, log, distinct, cmpairs, ex)
        srow(f"exclusion set '{label}' (n={len(ex)})", r3)
        if label == "none":
            P3 = r3["P"]
            sys_names = set(excl["primary"])
            sys_idx = np.flatnonzero(np.isin(P3["res_names"], list(sys_names)))
            sysattr = {"system_accounts": sorted(sys_names) if len(sys_names) <= 3 else f"{len(sys_names)} labelled accounts",
                       "share_of_events": float(P3["n_events_res"][sys_idx].sum() / P3["n_events"]),
                       "share_of_completed_cases_attributed": {
                           rule: float(np.isin(P3["cases"][rule]["res"], sys_idx).mean()) for rule in L.ATTRS},
                       "system_accounts_ranked_when_included": int(np.isin(r3["A"], sys_idx).sum())}
            # where do included system accounts land in the baseline ranking (aggregate: quintile index 1=bottom..5=top)
            qpos = {}
            for k in [L.BASELINE, L.distinct_key("EPH", "last", "month", 60, "none"), L.distinct_key("APT", "last", "month", 60, "none")]:
                x = r3["S"][key2cfg[k], r3["A"]]
                ranks = pd.Series(x).rank(pct=True).to_numpy()
                pos = [int(np.ceil(ranks[list(r3["A"]).index(i)] * 5)) for i in sys_idx if i in set(r3["A"]) and np.isfinite(ranks[list(r3["A"]).index(i)])]
                qpos[k] = pos if len(pos) <= 3 else {"n": len(pos), "share_in_top_quintile": float(np.mean(np.array(pos) == 5))}
            sysattr["quintile_of_system_accounts_when_included_(1=bottom,5=top)"] = qpos
            sysattr["contrast_primary_vs_included"] = {
                "median_tau_distinct": [res["tsum"]["median_tau_distinct"], r3["tsum"]["median_tau_distinct"]],
                "median_reclass_bottom_distinct": [res["rsum"]["median_reclass_bottom_distinct"], r3["rsum"]["median_reclass_bottom_distinct"]]}
            # agreement of the baseline ranking of human workers with and without system accounts in the attribution pool
            common = np.intersect1d(A, r3["A"])
            common = common[~np.isin(common, sys_idx)]
            names_p = P["res_names"][common]
            idx3 = {n: i for i, n in enumerate(P3["res_names"])}
            c3 = np.array([idx3[n] for n in names_p])
            taus = {}
            for k in [L.BASELINE, L.distinct_key("CCA", "first", "month", 60, "none"), L.distinct_key("CCA", "majority", "month", 60, "none"),
                      L.distinct_key("RWK", "first", "month", 60, "none"), L.distinct_key("DLA", "first", "month", 60, "none")]:
                xa, xb = S[key2cfg[k], common], r3["S"][key2cfg[k], c3]
                ok = np.isfinite(xa) & np.isfinite(xb)
                taus[k] = {"n": int(ok.sum()), "tau_same_config_system_excluded_vs_included": float(L.tau_b_matrix(np.vstack([xa[ok], xb[ok]]))[0, 1]),
                           "reclass_bottom": L.reclass_rate(xa, xb)[0]}
            sysattr["human_ranking_agreement_system_excluded_vs_included"] = taus
    pd.DataFrame(srows).to_csv(os.path.join(outdir, f"{log}_sensitivity.csv"), index=False)
    with open(os.path.join(outdir, f"{log}_system_account_attribution.json"), "w") as fh:
        json.dump(sysattr, fh, indent=1, default=float)
    print(json.dumps({k: v for k, v in tsum.items() if k not in ("casemix_covariates",)}, indent=1, default=float))
    print(pd.DataFrame(srows).to_string())
    print(json.dumps(sysattr, indent=1, default=float))
    print("seconds", round(time.time() - t0, 1))


if __name__ == "__main__":
    main()
