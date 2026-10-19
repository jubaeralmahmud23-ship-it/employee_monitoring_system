#!/usr/bin/env python3
"""Stage 4 pilot for idea 4: sampling uncertainty of NYC Local Law 144 impact ratios.

EXPLORATORY PILOT. Reads the ACLU 'Auditing the Audits' corpus (Gerchick et al., FAccT 2025,
audits/audits_full.csv) and:
  1. profiles its columns and rows;
  2. groups rows into result tables (audit x rate definition x protected characteristic);
  3. de-duplicates tables (plan key auditor/tool/data window, confirmed by identical counts;
     the literal key without confirmation is a sensitivity variant);
  4. applies a consistency filter |n/N - reported rate| <= rounding tolerance;
  5. recomputes the comparator (highest-rate group among groups with >= 2% of known applicants);
  6. for every usable impact ratio computes four 95% intervals (Katz log-ratio; Clopper-Pearson
     with Bonferroni split; stratified bootstrap, seed 20261015, 2000 resamples; Jeffreys-prior
     posterior), the posterior P(ratio < 0.8), the UGESP four-fifths flag, a pooled two-proportion
     z ("two standard deviations") test and Fisher's exact test;
  7. tabulates shares of ratios whose intervals exclude 0.8 and 1.0 by scope, auditor, vendor,
     metric and characteristic;
  8. computes excluded-population shares (unknown demographics; groups under 2%);
  9. cross-checks 20 rows against the OSF (Wright et al.) extraction and the employer PDFs;
 10. evaluates the Part 1 stopping rule of research/02_candidate_ideas.md section 4.3.

Only aggregated tables are written to --out-dir (inside the repository). Row-level derived data
(per-ratio intervals; the 20-row cross-check detail) are written to --private-dir, which must be
outside the repository: the ACLU repository README carries a CC BY-NC 4.0 notice, and the plan
does not redistribute the raw data.

Usage:
  python -I ll144_pilot.py --aclu-csv <csv> --osf-csv <csv> --osf-pdf-dir <dir> \
      --out-dir <dir> --private-dir <dir>
"""
import argparse
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import time

import numpy as np
import pandas as pd
import scipy
from scipy import stats

SEED = 20261015          # bootstrap seed fixed by the task; also used for the OSF sample
N_BOOT = 2000            # bootstrap resamples fixed by the task
N_POST = 20000           # Monte Carlo draws per ratio for the Jeffreys posterior
Z975 = float(stats.norm.ppf(0.975))
THRESH = 0.8             # four-fifths convention
SHARE_MIN = 0.02         # LL 144 rule 5-301(d): categories under 2% may be excluded
STOP_SHARE = 0.80        # stopping rule threshold ("more than about 80%")
KNOWN_SEX = ("Female", "Male")
MISSING = "Missing/Unknown"
# Deploying entities that are the tool vendor under another name. Source: ACLU tracker README
# row "Dover | Dover | Varun Ganesan | 6/23/23" (deploying entity Dover); ACLU audit_id
# staya_inc_dover_varun_ganesan_2023_audit_1 lists the deploying entity as "Staya, Inc.".
VENDOR_ALIASES = {("staya, inc.", "dover")}
METHODS = {
    "katz": ("katz_lo", "katz_hi"),
    "cp_bonf": ("cp_lo", "cp_hi"),
    "boot": ("boot_lo", "boot_hi"),
    "jeffreys": ("jef_lo", "jef_hi"),
}
PRIMARY_METHOD = "katz"  # fixed in code before the first run; see README


# ----------------------------------------------------------------------------- helpers
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def to_num(s):
    s = s.astype(str).str.strip()
    return pd.to_numeric(s.where(~s.isin(["", "NA", "NaN", "nan"])), errors="coerce")


def n_decimals(s):
    s = str(s).strip()
    if s in ("", "NA", "NaN", "nan"):
        return -1
    if "e" in s.lower():
        return 7
    return len(s.split(".")[1]) if "." in s else 0


def write_csv(df, path):
    df.to_csv(path, index=False, float_format="%.6g")


class Timer:
    def __init__(self):
        self.t0 = time.perf_counter()
        self.last = self.t0
        self.marks = {}

    def mark(self, name):
        now = time.perf_counter()
        self.marks[name] = round(now - self.last, 3)
        self.last = now

    def total(self):
        return round(time.perf_counter() - self.t0, 3)


# ----------------------------------------------------------------------------- load + profile
def load_aclu(path):
    raw = pd.read_csv(path, dtype=str, keep_default_na=False)
    df = raw.copy()
    df["row_id"] = np.arange(len(df))
    df["N"] = to_num(df["number_of_applications"])
    df["n"] = to_num(df["n_selected_or_n_above_median"])
    df["r"] = to_num(df["result"])
    df["ir"] = to_num(df["impact_ratio"])
    for c in ["impact_ratio_lower_bound", "impact_ratio_upper_bound",
              "impact_ratio_lower_bound2", "impact_ratio_upper_bound2"]:
        df[c + "_num"] = to_num(df[c])
    df["r_dec"] = df["result"].map(n_decimals)
    pcg = df["protected_char_group"]
    df["is_missing"] = (df["race_ethnicity"] == MISSING) | (df["sex"] == MISSING)
    known_sex = (pcg == "sex") & (df["race_ethnicity"] == "Total") & df["sex"].isin(KNOWN_SEX)
    known_race = (pcg == "race/ethnicity") & (df["sex"] == "Total") & ~df["race_ethnicity"].isin(["Total", MISSING])
    known_int = (pcg == "intersectional") & df["sex"].isin(KNOWN_SEX) & ~df["race_ethnicity"].isin(["Total", MISSING])
    df["known"] = (known_sex | known_race | known_int) & ~df["is_missing"]
    df["group"] = np.where(pcg == "sex", df["sex"],
                           np.where(pcg == "race/ethnicity", df["race_ethnicity"],
                                    df["race_ethnicity"] + " x " + df["sex"]))
    df["tbl"] = df["audit_id"] + " | " + df["selection_or_scoring_rate"] + " | " + pcg
    return raw, df


def profile_columns(raw):
    out = []
    for c in raw.columns:
        s = raw[c].astype(str).str.strip()
        present = ~s.isin(["", "NA", "NaN", "nan"])
        num = pd.to_numeric(s.where(present), errors="coerce")
        is_num = present.sum() > 0 and num.notna().sum() == present.sum()
        out.append({
            "column": c,
            "non_missing": int(present.sum()),
            "missing_or_NA": int((~present).sum()),
            "n_unique_non_missing": int(s[present].nunique()),
            "numeric": bool(is_num),
            "min": float(num.min()) if is_num else None,
            "max": float(num.max()) if is_num else None,
        })
    return pd.DataFrame(out)


# ----------------------------------------------------------------------------- tables
def primary_rate(rates):
    s = set(rates)
    if {"Selection, top", "Selection, top and middle"} <= s:
        return "Selection, top"          # as Gerchick et al., paper_results.Rmd lines 413-437
    if {"Selection", "Scoring"} <= s:
        return "Selection"               # Dover; as paper_results.Rmd lines 162-163, 414
    if len(s) == 1:
        return next(iter(s))
    raise ValueError(f"unexpected rate set {s}")


def build_tables(df):
    meta_cols = ["audit_id", "audit_report_id", "deploying_entity", "auditor", "tool_vendor",
                 "tool_id", "selection_or_scoring_rate", "protected_char_group", "data_type",
                 "audit_data_start_date", "audit_data_end_date", "year_of_audit_result", "position"]
    T = df.groupby("tbl", sort=True)[meta_cols].first().reset_index()
    prate = df.groupby("audit_id")["selection_or_scoring_rate"].agg(lambda s: primary_rate(s.unique()))
    T["primary_rate"] = T["audit_id"].map(prate)
    T["is_primary_rate"] = T["selection_or_scoring_rate"] == T["primary_rate"]
    T["hackerrank_excluded"] = T["deploying_entity"].str.lower() == "hackerrank"  # Rmd lines 160-161
    T["vendor_posted"] = [
        (d.strip().lower() == v.strip().lower()) or ((d.strip().lower(), v.strip().lower()) in VENDOR_ALIASES)
        for d, v in zip(T["deploying_entity"], T["tool_vendor"])
    ]
    T["vendor_norm"] = T["tool_vendor"].map(
        lambda v: {"adp": "ADP", "bryq": "Bryq", "covey": "Covey", "dover": "Dover", "hackerrank": "HackerRank",
                   "hiredscore": "HiredScore", "phenom": "Phenom", "sense": "Sense", "vervoe": "Vervoe"}.get(v, v))

    # per-table aggregates
    K = df[df["known"]]
    agg = K.groupby("tbl").agg(
        n_known_rows=("row_id", "size"),
        N_known_total=("N", lambda s: s.sum(min_count=1)),
        n_known_N_reported=("N", lambda s: int(s.notna().sum())),
    )
    M = df[df["is_missing"]]
    magg = M.groupby("tbl").agg(n_missing_rows=("row_id", "size"),
                                N_unknown=("N", lambda s: s.sum(min_count=1)))
    T = T.merge(agg, left_on="tbl", right_index=True, how="left").merge(
        magg, left_on="tbl", right_index=True, how="left")
    T["n_missing_rows"] = T["n_missing_rows"].fillna(0).astype(int)

    # content signature over known groups with N > 0 (group, N, n)
    sigs = {}
    for tbl, g in K.groupby("tbl", sort=True):
        k = g[g["N"] > 0].sort_values("group")
        if len(k) < 2:
            sigs[tbl] = None
            continue
        parts = [f"{a}:{b:.0f}:{'' if pd.isna(c) else f'{c:.2f}'}" for a, b, c in zip(k["group"], k["N"], k["n"])]
        s = g["selection_or_scoring_rate"].iloc[0] + "#" + g["protected_char_group"].iloc[0] + "#" + "|".join(parts)
        sigs[tbl] = hashlib.md5(s.encode()).hexdigest()
    T["signature"] = T["tbl"].map(sigs)

    # window known?
    def known_date(x):
        x = str(x).strip()
        return x not in ("", "NA", "Unknown", "unknown", "nan")
    T["window_known"] = T["audit_data_start_date"].map(known_date) & T["audit_data_end_date"].map(known_date)
    T["plan_key"] = (T["auditor"] + "|" + T["tool_vendor"].str.lower() + "|" + T["tool_id"].str.lower() + "|"
                     + T["audit_data_start_date"] + "|" + T["audit_data_end_date"] + "|"
                     + T["selection_or_scoring_rate"] + "|" + T["protected_char_group"])

    # primary de-dup: identical counts (content signature); keep first table in sorted tbl order
    T = T.sort_values("tbl").reset_index(drop=True)
    first_by_sig = {}
    dup_of = []
    for tbl, sig in zip(T["tbl"], T["signature"]):
        if not isinstance(sig, str):   # pandas stores a missing signature as NaN
            dup_of.append(None)
        elif sig in first_by_sig:
            dup_of.append(first_by_sig[sig])
        else:
            first_by_sig[sig] = tbl
            dup_of.append(None)
    T["dup_primary_of"] = dup_of
    T["dup_primary"] = T["dup_primary_of"].notna()
    # which primary duplicates share the plan key (auditor, tool, known window)?
    key_of = dict(zip(T["tbl"], T["plan_key"]))
    wk_of = dict(zip(T["tbl"], T["window_known"]))
    T["dup_primary_same_plan_key"] = [
        isinstance(d, str) and wk and wk_of[d] and key_of[d] == k
        for d, k, wk in zip(T["dup_primary_of"], T["plan_key"], T["window_known"])
    ]
    # literal plan rule: one table per (auditor, tool, known window, rate def, characteristic)
    first_by_key = {}
    lit = []
    for tbl, k, wk in zip(T["tbl"], T["plan_key"], T["window_known"]):
        if not wk:
            lit.append(None)
        elif k in first_by_key:
            lit.append(first_by_key[k])
        else:
            first_by_key[k] = tbl
            lit.append(None)
    T["dup_literal_of"] = lit
    T["dup_literal"] = T["dup_literal_of"].notna()
    # shared across employers: same signature posted by >= 2 distinct deploying entities
    ents = T.dropna(subset=["signature"]).groupby("signature")["deploying_entity"].nunique()
    T["shared_across_entities"] = T["signature"].map(ents).fillna(1) >= 2
    return T


# ----------------------------------------------------------------------------- consistency
def consistency(df):
    """Row-level consistency status for known groups."""
    df = df.copy()
    # effective decimals of the reported rate: row decimals, floored at the table mode
    # (handles dropped trailing zeros), capped at 6 (longer strings are computed values)
    mode = {}
    for tbl, g in df[df["known"]].groupby("tbl"):
        d = g["r_dec"][(g["r_dec"] >= 1) & (g["r_dec"] <= 6)]
        mode[tbl] = int(d.mode().max()) if len(d) else 2
    tm = df["tbl"].map(mode).fillna(2).astype(int)
    d_eff = np.minimum(np.maximum(df["r_dec"].clip(lower=0), tm), 6)
    df["d_eff"] = d_eff
    df["tol"] = 0.5 * 10.0 ** (-d_eff) + 1e-9
    df["n_is_int"] = df["n"].notna() & ((df["n"] - df["n"].round()).abs() < 1e-6)
    diff = (df["n"] / df["N"] - df["r"]).abs()
    df["cons_absdiff"] = diff
    status = np.full(len(df), "not_known_group", dtype=object)
    k = df["known"].to_numpy()
    N = df["N"].to_numpy()
    n = df["n"].to_numpy()
    r = df["r"].to_numpy()
    tol = df["tol"].to_numpy()
    dd = diff.to_numpy()
    for i in np.where(k)[0]:
        if np.isnan(N[i]):
            status[i] = "N_not_reported"
        elif N[i] == 0:
            status[i] = "zero_N"
        elif np.isnan(n[i]):
            status[i] = "n_not_reported"
        elif n[i] > N[i] + 1e-6 or n[i] < 0:
            status[i] = "fail"
        elif np.isnan(r[i]):
            status[i] = "rate_not_reported"
        elif dd[i] <= tol[i]:
            status[i] = "pass"
        elif dd[i] <= 2 * tol[i]:
            status[i] = "pass_lenient_only"
        else:
            status[i] = "fail"
    df["cons_status"] = status
    df["n_int"] = df["n"].round()
    return df


# ----------------------------------------------------------------------------- ratios
def build_ratios(df, lenient):
    """One ratio per eligible non-comparator group; comparator = highest-rate group among
    groups with share >= 2% of the known applicants with reported N in the table."""
    ok = {"pass", "rate_not_reported"} | ({"pass_lenient_only"} if lenient else set())
    K = df[df["known"]]
    out = []
    for tbl, g in K.groupby("tbl", sort=True):
        Ntot = g["N"].sum(min_count=1)
        if not (Ntot > 0):
            continue
        g = g.assign(share=g["N"] / Ntot)
        usable = g[g["cons_status"].isin(ok) & (g["N"] > 0)]
        big = usable[usable["share"] >= SHARE_MIN]
        if len(big) < 2:
            continue
        big = big.assign(rate=big["n_int"] / big["N"]).sort_values(
            ["rate", "N", "group"], ascending=[False, False, True])
        comp = big.iloc[0]
        if comp["n_int"] <= 0:
            continue
        others = pd.concat([big.iloc[1:], usable[usable["share"] < SHARE_MIN].assign(
            rate=lambda x: x["n_int"] / x["N"])])
        for _, row in others.iterrows():
            out.append({
                "tbl": tbl, "row_id": int(row["row_id"]), "comp_row_id": int(comp["row_id"]),
                "group": row["group"], "comp_group": comp["group"],
                "ng": float(row["n_int"]), "Ng": float(row["N"]), "nc": float(comp["n_int"]), "Nc": float(comp["N"]),
                "share": float(row["share"]), "comp_share": float(comp["share"]),
                "is_small": bool(row["share"] < SHARE_MIN),
                "ir_reported": row["ir"], "ir_comp_reported": comp["ir"],
                "r_g": row["r"], "r_c": comp["r"], "d_g": int(row["d_eff"]), "d_c": int(comp["d_eff"]),
                "counts_reported_int": bool(row["n_is_int"] and comp["n_is_int"]),
                "status_g": row["cons_status"], "status_c": comp["cons_status"],
            })
    R = pd.DataFrame(out)
    R["lenient_build"] = lenient
    return R


def cp_bounds(n, N, alpha):
    """Clopper-Pearson two-sided (1 - alpha) interval, vectorised."""
    n = np.asarray(n, float)
    N = np.asarray(N, float)
    a_lo = np.where(n == 0, 1.0, n)
    lo = np.where(n == 0, 0.0, stats.beta.ppf(alpha / 2, a_lo, N - n + 1))
    b_hi = np.where(n == N, 1.0, N - n)
    hi = np.where(n == N, 1.0, stats.beta.ppf(1 - alpha / 2, n + 1, b_hi))
    return lo, hi


def compute_stats(R):
    R = R.sort_values(["tbl", "row_id", "comp_row_id"]).reset_index(drop=True)
    ng, Ng, nc, Nc = (R[c].to_numpy(float) for c in ("ng", "Ng", "nc", "Nc"))
    pg, pc = ng / Ng, nc / Nc
    with np.errstate(divide="ignore", invalid="ignore"):
        R["ir_point"] = pg / pc
        # Katz log-ratio interval; 0.5 added to each 2x2 cell when a selected count is zero
        zero = (ng == 0) | (nc == 0)
        a = np.where(zero, ng + 0.5, ng)
        A = np.where(zero, Ng + 1.0, Ng)
        c = np.where(zero, nc + 0.5, nc)
        C = np.where(zero, Nc + 1.0, Nc)
        lr = np.log((a / A) / (c / C))
        se = np.sqrt(np.maximum(1 / a - 1 / A + 1 / c - 1 / C, 0))
        R["katz_lo"] = np.exp(lr - Z975 * se)
        R["katz_hi"] = np.exp(lr + Z975 * se)
        # Clopper-Pearson 97.5% for each rate (Bonferroni), ratio of bounds: coverage >= 95%
        lg, ug = cp_bounds(ng, Ng, 0.025)
        lc, uc = cp_bounds(nc, Nc, 0.025)
        R["cp_lo"] = lg / uc
        R["cp_hi"] = np.where(lc > 0, ug / np.where(lc > 0, lc, 1.0), np.inf)
    # stratified bootstrap within the two groups, comparator fixed, percentile (inverted CDF)
    rng = np.random.default_rng(SEED)
    blo = np.empty(len(R))
    bhi = np.empty(len(R))
    n_degen = 0
    for s in range(0, len(R), 500):
        e = min(s + 500, len(R))
        gs = rng.binomial(Ng[s:e, None].astype(np.int64), pg[s:e, None], size=(e - s, N_BOOT))
        cs = rng.binomial(Nc[s:e, None].astype(np.int64), pc[s:e, None], size=(e - s, N_BOOT))
        with np.errstate(divide="ignore", invalid="ignore"):
            rat = (gs / Ng[s:e, None]) / (cs / Nc[s:e, None])
        n_degen += int(np.isnan(rat).sum())
        blo[s:e] = np.nanquantile(rat, 0.025, axis=1, method="inverted_cdf")
        bhi[s:e] = np.nanquantile(rat, 0.975, axis=1, method="inverted_cdf")
    R["boot_lo"], R["boot_hi"] = blo, bhi
    # Jeffreys Beta(0.5, 0.5) priors, independent; Monte Carlo posterior of the ratio
    rng2 = np.random.default_rng([SEED, 1])
    jlo = np.empty(len(R))
    jhi = np.empty(len(R))
    p08 = np.empty(len(R))
    p10 = np.empty(len(R))
    for s in range(0, len(R), 100):
        e = min(s + 100, len(R))
        bg = rng2.beta(ng[s:e, None] + 0.5, Ng[s:e, None] - ng[s:e, None] + 0.5, size=(e - s, N_POST))
        bc = rng2.beta(nc[s:e, None] + 0.5, Nc[s:e, None] - nc[s:e, None] + 0.5, size=(e - s, N_POST))
        rat = bg / bc
        jlo[s:e] = np.quantile(rat, 0.025, axis=1)
        jhi[s:e] = np.quantile(rat, 0.975, axis=1)
        p08[s:e] = (rat < THRESH).mean(axis=1)
        p10[s:e] = (rat < 1.0).mean(axis=1)
    R["jef_lo"], R["jef_hi"], R["p_below08"], R["p_below1"] = jlo, jhi, p08, p10
    # UGESP four-fifths flag, pooled two-proportion z ("two standard deviations"), Fisher exact
    pp = (ng + nc) / (Ng + Nc)
    with np.errstate(divide="ignore", invalid="ignore"):
        z = (pg - pc) / np.sqrt(pp * (1 - pp) * (1 / Ng + 1 / Nc))
    R["z"] = z
    R["four_fifths_flag"] = R["ir_point"] < THRESH
    R["two_sd_signif"] = np.abs(z) > 1.96
    fp = []
    for a_, A_, c_, C_ in zip(ng, Ng, nc, Nc):
        fp.append(stats.fisher_exact([[int(a_), int(A_ - a_)], [int(c_), int(C_ - c_)]])[1])
    R["fisher_p"] = fp
    # reporting-precision (rounding) bounds from the reported rates, where rates are reported
    hg = 0.5 * 10.0 ** (-R["d_g"].to_numpy(float))
    hc = 0.5 * 10.0 ** (-R["d_c"].to_numpy(float))
    rg = R["r_g"].to_numpy(float)
    rc = R["r_c"].to_numpy(float)
    with np.errstate(divide="ignore", invalid="ignore"):
        R["round_lo"] = np.maximum(rg - hg, 0) / (rc + hc)
        R["round_hi"] = (rg + hg) / np.maximum(rc - hc, 1e-12)
    return R, n_degen


# ----------------------------------------------------------------------------- summaries
def excl(lo, hi, t):
    return (lo > t) | (hi < t)


def summarise(R, by, label=None):
    rows = []
    groups = [((), R)] if not by else list(R.groupby(by, sort=True, dropna=False))
    for key, g in groups:
        if len(g) == 0:
            continue
        d = {}
        if label is not None:
            d["set"] = label
        if by:
            key = key if isinstance(key, tuple) else (key,)
            for b, k in zip(by, key):
                d[b] = k
        d["n_ratios"] = len(g)
        d["n_tables"] = g["tbl"].nunique()
        d["n_audits"] = g["audit_id"].nunique()
        d["n_reports"] = g["audit_report_id"].nunique()
        d["Ng_p10"] = g["Ng"].quantile(0.1)
        d["Ng_median"] = g["Ng"].median()
        d["Ng_p90"] = g["Ng"].quantile(0.9)
        d["share_point_ir_below_0.8"] = (g["ir_point"] < THRESH).mean()
        for m, (lo, hi) in METHODS.items():
            d[f"share_excl_0.8_{m}"] = excl(g[lo], g[hi], THRESH).mean()
        for m, (lo, hi) in METHODS.items():
            d[f"share_excl_1.0_{m}"] = excl(g[lo], g[hi], 1.0).mean()
        d["share_katz_entirely_below_0.8"] = (g["katz_hi"] < THRESH).mean()
        d["share_katz_entirely_above_0.8"] = (g["katz_lo"] > THRESH).mean()
        d["share_two_sd_signif"] = g["two_sd_signif"].mean()
        d["share_fisher_p_lt_0.05"] = (g["fisher_p"] < 0.05).mean()
        d["share_post_P_below_0.8_gt_0.95"] = (g["p_below08"] > 0.95).mean()
        d["share_post_P_below_0.8_lt_0.05"] = (g["p_below08"] < 0.05).mean()
        d["share_post_P_below_0.8_indeterminate"] = ((g["p_below08"] >= 0.05) & (g["p_below08"] <= 0.95)).mean()
        d["median_katz_width"] = (g["katz_hi"] - g["katz_lo"]).median()
        rows.append(d)
    return pd.DataFrame(rows)


def excluded_population(df, T):
    """Per-table excluded populations; returns per-table frame (private) and summaries."""
    K = df[df["known"]]
    rows = []
    for _, t in T.iterrows():
        g = K[K["tbl"] == t["tbl"]]
        Nk = g["N"].sum(min_count=1)
        if not (Nk > 0):
            continue
        share = g["N"] / Nk
        small = g[(g["N"] > 0) & (share < SHARE_MIN)]
        Nu = t["N_unknown"]
        if t["n_missing_rows"] == 0:
            ustat = "no_unknown_row"
        elif pd.isna(Nu):
            ustat = "unknown_count_not_reported"
        elif Nu == 0:
            ustat = "reported_zero"
        else:
            ustat = "reported_positive"
        rows.append({
            "tbl": t["tbl"], "auditor": t["auditor"], "vendor": t["vendor_norm"], "scope": t["scope"],
            "char_group": t["protected_char_group"], "data_type": t["data_type"],
            "N_known": Nk, "N_unknown": Nu, "unknown_status": ustat,
            "unknown_share": (Nu / (Nk + Nu)) if (pd.notna(Nu)) else np.nan,
            "N_sub2": small["N"].sum(), "n_groups_sub2": len(small),
            "sub2_share_of_known": small["N"].sum() / Nk,
            "excluded_total_share": ((Nu + small["N"].sum()) / (Nk + Nu)) if pd.notna(Nu) else np.nan,
            "n_groups_N_but_no_count": int(((g["N"] > 0) & g["n"].isna()).sum()),
        })
    P = pd.DataFrame(rows)

    def summ(x, by):
        out = []
        for key, g in (x.groupby(by, sort=True) if by else [((), x)]):
            d = {}
            key = key if isinstance(key, tuple) else (key,)
            for b, k in zip(by, key):
                d[b] = k
            u = g[g["unknown_status"].isin(["reported_zero", "reported_positive"])]
            d["n_tables"] = len(g)
            d["n_tables_unknown_count_reported"] = len(u)
            d["n_tables_unknown_positive"] = int((g["unknown_status"] == "reported_positive").sum())
            d["unknown_share_median"] = u["unknown_share"].median()
            d["unknown_share_q1"] = u["unknown_share"].quantile(0.25)
            d["unknown_share_q3"] = u["unknown_share"].quantile(0.75)
            d["unknown_share_max"] = u["unknown_share"].max()
            d["unknown_share_pooled"] = u["N_unknown"].sum() / (u["N_known"].sum() + u["N_unknown"].sum()) if len(u) else np.nan
            d["n_tables_with_sub2_groups"] = int((g["n_groups_sub2"] > 0).sum())
            d["sub2_share_median"] = g["sub2_share_of_known"].median()
            d["sub2_share_max"] = g["sub2_share_of_known"].max()
            d["sub2_share_pooled"] = g["N_sub2"].sum() / g["N_known"].sum()
            d["excluded_total_share_median"] = u["excluded_total_share"].median()
            d["excluded_total_share_max"] = u["excluded_total_share"].max()
            d["applicants_known_sum"] = g["N_known"].sum()
            d["applicants_unknown_sum"] = u["N_unknown"].sum()
            d["applicants_sub2_sum"] = g["N_sub2"].sum()
            d["n_groups_N_but_no_count"] = int(g["n_groups_N_but_no_count"].sum())
            out.append(d)
        return pd.DataFrame(out)

    return P, summ(P, ["char_group", "scope"]), summ(P, ["char_group", "auditor"])


# ----------------------------------------------------------------------------- OSF cross-check
OSF_DIRECT = {  # OSF CompanyName -> (ACLU deploying_entity, PDF relative path in the OSF zip)
    "Bloomberg": ("Bloomberg", "Bloomberg/20230703-BLP-Bias-Audit-for-AEDT.pdf"),
    "BNP Paribas": ("BNP Paribas", "BNP Paribas/Harver Soft Skills Platform Public Summary.pdf"),
    "Cigna": ("Cigna", "Cigna/nyc-aedt-bias-audit-2023.pdf"),
    "Morgan Stanley": ("Morgan Stanley", "Morgan Stanley/MORGAN-STANLEY-BIAS-AUDIT-REPORT-07052023brs.pdf"),
    "NBCUniversal": ("NBCUniversal", "NBC/nbc audit.pdf"),
    "Pfizer": ("Pfizer", "Pfizer/HireVue_2023_Bias_Report_14AUG2023.pdf"),
}
PFIZER_TOOL = [  # OSF AuditingFor keyword -> ACLU tool_id
    ("Adaptability", "adaptability"), ("Communication", "communication"), ("Dependability", "dependability"),
    ("Agreeableness", "agreeableness"), ("Conscientiousness", "conscientiousness"), ("Openness", "openness"),
    ("Relationship Building", "relationship-building"), ("Safety", "safety-compliance"),
    ("Think", "think-digitspan-shapedance-and-or-numerosity"), ("Willingness to Learn", "willingness-to-learn"),
]


def norm_group(s):
    s = str(s).strip().lower()
    s = s.replace("native american or alaska native", "american indian or alaska native")
    s = s.replace("native hawaiian or pacific islander", "native hawaiian or other pacific islander")
    return s


def pdf_text(path):
    try:
        return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True,
                              timeout=120).stdout
    except Exception:
        return ""


def osf_crosscheck(df, osf_csv, pdf_dir):
    o = pd.read_csv(osf_csv, dtype=str, keep_default_na=False)
    o["osf_row"] = np.arange(len(o))
    o["ir_osf"] = to_num(o["ImpactRatio"])
    o["ir_osf_dec"] = o["ImpactRatio"].map(n_decimals)
    A = df[(df["year_of_audit_result"] == "2023") & df["known"] & df["protected_char_group"].isin(["sex", "race/ethnicity"])].copy()
    A["gnorm"] = A["group"].map(norm_group)
    A["ir_dec"] = A["impact_ratio"].map(n_decimals)
    pool = []
    for _, row in o[o["CompanyName"].isin(OSF_DIRECT)].iterrows():
        ent, _pdf = OSF_DIRECT[row["CompanyName"]]
        cg = "sex" if row["Category"] == "Sex" else "race/ethnicity"
        m = A[(A["deploying_entity"] == ent) & (A["protected_char_group"] == cg) & (A["gnorm"] == norm_group(row["Type"]))]
        if ent == "Pfizer":
            tool = next((t for kw, t in PFIZER_TOOL if kw.lower() in row["AuditingFor"].lower()), None)
            m = m[m["tool_id"] == tool]
        pool.append({"osf_row": row["osf_row"], "n_match": len(m),
                     "aclu_row_id": int(m["row_id"].iloc[0]) if len(m) == 1 else -1})
    P = pd.DataFrame(pool)
    n_pool_total = len(P)
    P1 = P[P["n_match"] == 1]
    sample = P1.sample(n=min(20, len(P1)), random_state=SEED).sort_values("osf_row")
    texts = {}
    det = []
    for _, s in sample.iterrows():
        orow = o.iloc[int(s["osf_row"])]
        arow = df.iloc[int(s["aclu_row_id"])]
        ent, pdfrel = OSF_DIRECT[orow["CompanyName"]]
        a, b = arow["ir"], orow["ir_osf"]
        if pd.isna(a) and pd.isna(b):
            agree_exact, agree_01, kind = True, True, "both_NA"
        elif pd.isna(a) or pd.isna(b):
            agree_exact, agree_01, kind = False, False, "NA_in_one"
        else:
            dmin = max(min(n_decimals(arow["impact_ratio"]), int(orow["ir_osf_dec"])), 0)
            agree_exact = abs(round(a, dmin) - round(b, dmin)) < 1e-9
            agree_01 = abs(a - b) <= 0.01 + 1e-9
            kind = "numeric"
        if pdfrel not in texts:
            texts[pdfrel] = pdf_text(os.path.join(pdf_dir, pdfrel))
        txt = texts[pdfrel]
        N = arow["N"]
        found = None
        if pd.notna(N) and txt:
            Ni = int(N)
            pats = {f"{Ni:,}", str(Ni)}
            found = any(re.search(r"(?<![\d,.])" + re.escape(p) + r"(?![\d,])", txt) for p in pats)
        det.append({
            "osf_row": int(s["osf_row"]), "aclu_row_id": int(s["aclu_row_id"]), "company": orow["CompanyName"],
            "category": orow["Category"], "group": orow["Type"], "osf_auditing_for": orow["AuditingFor"],
            "aclu_audit_id": arow["audit_id"], "aclu_rate_def": arow["selection_or_scoring_rate"],
            "ir_aclu": a, "ir_osf": b, "match_kind": kind, "agree_exact_at_common_precision": agree_exact,
            "agree_within_0.01": agree_01, "aclu_N": N, "aclu_N_found_in_pdf_text": found,
            "pdf_text_chars": len(txt),
        })
    D = pd.DataFrame(det)
    summ = []
    for comp, g in [("ALL", D)] + list(D.groupby("company")):
        summ.append({
            "company": comp, "n_sampled": len(g),
            "n_agree_exact": int(g["agree_exact_at_common_precision"].sum()),
            "n_agree_within_0.01": int(g["agree_within_0.01"].sum()),
            "n_both_NA": int((g["match_kind"] == "both_NA").sum()),
            "n_NA_in_one_only": int((g["match_kind"] == "NA_in_one").sum()),
            "n_N_checked_in_pdf": int(g["aclu_N_found_in_pdf_text"].notna().sum()),
            "n_N_found_in_pdf": int((g["aclu_N_found_in_pdf_text"] == True).sum()),  # noqa: E712
        })
    S = pd.DataFrame(summ)
    pool_info = {
        "osf_rows_total": int(len(o)),
        "osf_rows_direct_employers": n_pool_total,
        "osf_rows_with_exactly_one_aclu_match": int(len(P1)),
        "osf_rows_with_no_match": int((P["n_match"] == 0).sum()),
        "osf_rows_with_multiple_matches": int((P["n_match"] > 1).sum()),
        "sample_size": int(len(sample)),
        "sample_seed": SEED,
        "pdf_sha256": {k: sha256(os.path.join(pdf_dir, k)) for k in sorted(texts)},
    }
    return D, S, pool_info


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aclu-csv", required=True)
    ap.add_argument("--osf-csv", required=True)
    ap.add_argument("--osf-pdf-dir", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--private-dir", required=True)
    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)
    os.makedirs(args.private_dir, exist_ok=True)
    out = lambda name: os.path.join(args.out_dir, name)        # noqa: E731
    priv = lambda name: os.path.join(args.private_dir, name)   # noqa: E731
    tm = Timer()

    # 1. load and profile
    raw, df = load_aclu(args.aclu_csv)
    prof = profile_columns(raw)
    write_csv(prof, out("aclu_columns_profile.csv"))
    tm.mark("load_profile")

    # 2-3. tables and de-duplication
    T = build_tables(df)
    T["scope"] = np.where(T["vendor_posted"], "vendor-posted", "employer-posted")
    # 4. consistency
    df = consistency(df)
    tm.mark("tables_dedup_consistency")

    # 5-6. ratios and statistics (union of strict and lenient builds, one statistics pass)
    Rs = build_ratios(df, lenient=False)
    Rl = build_ratios(df, lenient=True)
    key = ["tbl", "row_id", "comp_row_id"]
    Rl_only = Rl.merge(Rs[key], on=key, how="left", indicator=True)
    Rl_only = Rl_only[Rl_only["_merge"] == "left_only"].drop(columns="_merge")
    Ru = pd.concat([Rs.assign(in_strict=True), Rl_only.assign(in_strict=False)], ignore_index=True)
    lenient_keys = set(map(tuple, Rl[key].to_numpy()))
    Ru["in_lenient"] = [tuple(x) in lenient_keys for x in Ru[key].to_numpy()]
    Ru, n_degen = compute_stats(Ru)
    tcols = ["tbl", "audit_id", "audit_report_id", "deploying_entity", "auditor", "tool_vendor", "vendor_norm",
             "tool_id", "selection_or_scoring_rate", "protected_char_group", "data_type", "year_of_audit_result",
             "is_primary_rate", "hackerrank_excluded", "vendor_posted", "scope", "dup_primary", "dup_literal",
             "shared_across_entities"]
    Ru = Ru.merge(T[tcols], on="tbl", how="left")
    Ru["metric"] = np.where(Ru["selection_or_scoring_rate"] == "Scoring", "scoring rate", "selection rate")
    tm.mark("ratios_statistics")

    # analysis sets
    base = (~Ru["hackerrank_excluded"]) & Ru["is_primary_rate"]
    strict = Ru["in_strict"]
    big = ~Ru["is_small"]
    dedup = ~Ru["dup_primary"]
    emp = Ru["scope"] == "employer-posted"
    sets = {
        "E1_employer_posted_PRIMARY": base & strict & big & dedup & emp,
        "E2_employer_posted_historical": base & strict & big & dedup & emp & (Ru["data_type"] == "historical"),
        "E3_employer_posted_historical_not_shared": base & strict & big & dedup & emp & (Ru["data_type"] == "historical") & ~Ru["shared_across_entities"],
        "V_vendor_posted": base & strict & big & dedup & ~emp,
        "ALL_dedup": base & strict & big & dedup,
        "S1_employer_no_dedup": base & strict & big & emp,
        "S2_employer_literal_plan_key_dedup": base & strict & big & emp & ~Ru["dup_literal"],
        "S3_employer_lenient_consistency": base & Ru["in_lenient"] & big & dedup & emp,
        "S4_employer_incl_sub2pct_groups": base & strict & dedup & emp,
        "S5_employer_all_rate_definitions": (~Ru["hackerrank_excluded"]) & strict & big & dedup & emp,
        "S6_employer_counts_reported_as_integers": base & strict & big & dedup & emp & Ru["counts_reported_int"],
        "S7_ALL_dedup_all_rate_definitions": (~Ru["hackerrank_excluded"]) & strict & big & dedup,
    }
    variants = pd.concat([summarise(Ru[m], [], label=k) for k, m in sets.items()], ignore_index=True)
    write_csv(variants, out("interval_summary_variants.csv"))
    E1 = Ru[sets["E1_employer_posted_PRIMARY"]]
    AL = Ru[sets["ALL_dedup"]]
    for by, name in [(["auditor"], "auditor"), (["vendor_norm"], "vendor"), (["selection_or_scoring_rate"], "metric"),
                     (["protected_char_group"], "char_group"), (["data_type"], "data_type"),
                     (["year_of_audit_result"], "year")]:
        t = pd.concat([summarise(E1, by, "E1_employer_posted_PRIMARY"), summarise(AL, by, "ALL_dedup")],
                      ignore_index=True)
        write_csv(t, out(f"interval_by_{name}.csv"))
    # UGESP cross-tabulation
    ug = []
    for k in ["E1_employer_posted_PRIMARY", "V_vendor_posted", "ALL_dedup"]:
        g = Ru[sets[k]]
        for ff in (True, False):
            for sd in (True, False):
                m = (g["four_fifths_flag"] == ff) & (g["two_sd_signif"] == sd)
                ug.append({"set": k, "four_fifths_ratio_below_0.8": ff, "two_sd_significant": sd,
                           "n_ratios": int(m.sum()), "share": m.mean() if len(g) else np.nan,
                           "of_which_fisher_p_lt_0.05": int((m & (g["fisher_p"] < 0.05)).sum())})
    write_csv(pd.DataFrame(ug), out("ugesp_crosstab.csv"))
    # posterior probability bands
    pb = []
    for k in ["E1_employer_posted_PRIMARY", "V_vendor_posted", "ALL_dedup"]:
        g = Ru[sets[k]]
        bins = [-0.001, 0.05, 0.5, 0.95, 1.0]
        lab = ["P<0.05", "0.05-0.5", "0.5-0.95", ">0.95"]
        cnt = pd.cut(g["p_below08"], bins=bins, labels=lab).value_counts().reindex(lab)
        for l_, c_ in cnt.items():
            pb.append({"set": k, "posterior_P_ratio_below_0.8": l_, "n_ratios": int(c_), "share": c_ / len(g)})
    write_csv(pd.DataFrame(pb), out("posterior_bands.csv"))
    tm.mark("tabulations")

    # pipeline funnel (primary path)
    Tp = T[~T["hackerrank_excluded"] & T["is_primary_rate"]]
    kept_tbls = set(Tp.loc[~Tp["dup_primary"], "tbl"])
    Kp = df[df["known"] & df["tbl"].isin(kept_tbls)]
    funnel = [
        ("rows in audits_full.csv", len(df)),
        ("audits (audit_id)", df["audit_id"].nunique()),
        ("audit reports (audit_report_id)", df["audit_report_id"].nunique()),
        ("rows after excluding HackerRank (negative outcome, as Gerchick et al.)", int((df["deploying_entity"].str.lower() != "hackerrank").sum())),
        ("result tables (audit x rate definition x characteristic), all", len(T)),
        ("tables after HackerRank exclusion, primary rate definition", len(Tp)),
        ("tables dropped as duplicates (identical counts)", int(Tp["dup_primary"].sum())),
        ("  of which share auditor, tool and known data window (plan key)", int(Tp["dup_primary_same_plan_key"].sum())),
        ("tables kept after de-duplication", len(kept_tbls)),
        ("tables the literal plan key would drop instead", int(Tp["dup_literal"].sum())),
        ("known-group rows in kept tables", len(Kp)),
        ("  with N reported", int(Kp["N"].notna().sum())),
        ("  with N > 0", int((Kp["N"] > 0).sum())),
        ("  with N > 0 and selected count reported", int(((Kp["N"] > 0) & Kp["n"].notna()).sum())),
        ("  passing the consistency filter (strict) or rate not reported", int(Kp["cons_status"].isin(["pass", "rate_not_reported"]).sum())),
        ("  failing the consistency filter (strict)", int(Kp["cons_status"].isin(["fail", "pass_lenient_only"]).sum())),
        ("usable ratios (>= 2% groups, non-comparator), all scopes", int(sets["ALL_dedup"].sum())),
        ("usable ratios, employer-posted (E1, primary)", int(sets["E1_employer_posted_PRIMARY"].sum())),
        ("usable ratios, vendor-posted", int(sets["V_vendor_posted"].sum())),
        ("sub-2% group ratios (employer-posted), excluded from primary", int((sets["S4_employer_incl_sub2pct_groups"] & Ru["is_small"]).sum())),
    ]
    write_csv(pd.DataFrame(funnel, columns=["step", "count"]), out("pipeline_funnel.csv"))

    # de-duplication summary
    dd = Tp.groupby(["auditor", "vendor_norm"]).agg(
        tables=("tbl", "size"), dup_identical_counts=("dup_primary", "sum"),
        dup_identical_same_plan_key=("dup_primary_same_plan_key", "sum"),
        literal_plan_key_would_drop=("dup_literal", "sum"),
        shared_across_entities=("shared_across_entities", "sum"),
        window_known=("window_known", "sum")).reset_index()
    write_csv(dd, out("dedup_summary.csv"))

    # consistency summary (all known rows with N > 0, HackerRank excluded, all rate definitions)
    C = df[df["known"] & (df["N"] > 0) & (df["deploying_entity"].str.lower() != "hackerrank")]
    cs = []
    for aud, g in [("ALL", C)] + list(C.groupby("auditor")):
        h = g[g["n"].notna()]
        cs.append({"auditor": aud, "rows_N_gt_0": len(g), "rows_with_selected_count": len(h),
                   "count_integer_as_reported": int(h["n_is_int"].sum()),
                   "count_non_integer_derived": int((~h["n_is_int"]).sum()),
                   "pass": int((g["cons_status"] == "pass").sum()),
                   "pass_lenient_only": int((g["cons_status"] == "pass_lenient_only").sum()),
                   "fail": int((g["cons_status"] == "fail").sum()),
                   "rate_not_reported": int((g["cons_status"] == "rate_not_reported").sum()),
                   "fail_among_integer_counts": int(((g["cons_status"] == "fail") & g["n_is_int"]).sum()),
                   "pass_among_integer_counts": int(((g["cons_status"] == "pass") & g["n_is_int"]).sum())})
    write_csv(pd.DataFrame(cs), out("consistency_summary.csv"))

    # comparator recomputation check (kept tables, primary rate definition, all scopes)
    AR = Ru[base & strict & dedup & big]
    comp = []
    for aud, g in [("ALL", AR)] + list(AR.groupby("auditor")):
        tabs = g.groupby("tbl").first()
        rep_comp_match = []
        for tbl, t in tabs.iterrows():
            rows_t = df[(df["tbl"] == tbl) & df["known"]]
            rep_ones = rows_t[(rows_t["ir"] - 1.0).abs() < 1e-9]
            if len(rep_ones) == 0:
                rep_comp_match.append(np.nan)
            else:
                rep_comp_match.append(float(t["comp_group"] in set(rep_ones["group"])))
        rcm = pd.Series(rep_comp_match, dtype=float)
        has_ir = g[g["ir_reported"].notna()]
        dlt = (has_ir["ir_point"] - has_ir["ir_reported"]).abs()
        ext = df[df["tbl"].isin(set(g["tbl"])) & df["known"] & (df["ir"] > 1.0 + 1e-9)]["tbl"].nunique()
        comp.append({
            "auditor": aud, "tables": len(tabs), "tables_with_reported_ir_equal_1": int(rcm.notna().sum()),
            "recomputed_comparator_is_a_reported_comparator": int((rcm == 1).sum()),
            "tables_with_any_reported_ir_above_1": int(ext),
            "ratios": len(g), "ratios_with_reported_ir": len(has_ir),
            "abs_diff_le_0.005": int((dlt <= 0.005 + 1e-9).sum()), "abs_diff_le_0.01": int((dlt <= 0.01 + 1e-9).sum()),
            "abs_diff_le_0.05": int((dlt <= 0.05 + 1e-9).sum()), "abs_diff_gt_0.05": int((dlt > 0.05 + 1e-9).sum()),
            "four_fifths_classification_flips": int(((has_ir["ir_point"] < THRESH) != (has_ir["ir_reported"] < THRESH)).sum()),
            "reported_ir_missing_for_usable_ratio": int(g["ir_reported"].isna().sum()),
        })
    write_csv(pd.DataFrame(comp), out("comparator_check.csv"))
    tm.mark("funnel_dedup_consistency_comparator")

    # excluded populations (kept tables, primary rate definition)
    Tk = Tp[~Tp["dup_primary"]]
    Pex, ex_scope, ex_aud = excluded_population(df, Tk)
    write_csv(ex_scope, out("excluded_population_by_scope.csv"))
    write_csv(ex_aud, out("excluded_population_by_auditor.csv"))
    tm.mark("excluded_population")

    # extras: reporting precision (rounding) and Gerchick et al. missing-data bounds vs sampling
    ex = []
    for k in ["E1_employer_posted_PRIMARY", "ALL_dedup"]:
        g = Ru[sets[k]]
        der = g[~g["counts_reported_int"] & g["r_g"].notna() & g["r_c"].notna()]
        ex.append({"set": k, "ratios": len(g), "ratios_with_derived_counts_and_reported_rates": len(der),
                   "rounding_bounds_contain_0.8": int(((der["round_lo"] <= THRESH) & (der["round_hi"] >= THRESH)).sum()),
                   "katz_contains_0.8": int(((der["katz_lo"] <= THRESH) & (der["katz_hi"] >= THRESH)).sum()),
                   "rounding_width_gt_katz_width": int(((der["round_hi"] - der["round_lo"]) > (der["katz_hi"] - der["katz_lo"])).sum()),
                   "median_rounding_width": (der["round_hi"] - der["round_lo"]).median(),
                   "median_katz_width": (der["katz_hi"] - der["katz_lo"]).median()})
    write_csv(pd.DataFrame(ex), out("extra_rounding_vs_sampling.csv"))
    mb = []
    lbm = df.set_index("row_id")
    for k in ["E1_employer_posted_PRIMARY", "ALL_dedup"]:
        g = Ru[sets[k]].copy()
        g["mlo"] = g["row_id"].map(lbm["impact_ratio_lower_bound_num"])
        g["mhi"] = g["row_id"].map(lbm["impact_ratio_upper_bound_num"])
        g["mlo2"] = g["row_id"].map(lbm["impact_ratio_lower_bound2_num"])
        g["mhi2"] = g["row_id"].map(lbm["impact_ratio_upper_bound2_num"])
        h = g[g["mlo"].notna() & g["mhi"].notna()]
        h2 = g[g["mlo2"].notna() & g["mhi2"].notna()]
        kw = h["katz_hi"] - h["katz_lo"]
        kw2 = h2["katz_hi"] - h2["katz_lo"]
        mb.append({"set": k, "ratios": len(g), "ratios_with_gerchick_worst_case_bounds": len(h),
                   "worst_case_width_gt_katz_width": int(((h["mhi"] - h["mlo"]) > kw).sum()),
                   "worst_case_bounds_contain_0.8": int(((h["mlo"] <= THRESH) & (h["mhi"] >= THRESH)).sum()),
                   "katz_contains_0.8_same_rows": int(((h["katz_lo"] <= THRESH) & (h["katz_hi"] >= THRESH)).sum()),
                   "ratios_with_gerchick_proportional_bounds": len(h2),
                   "proportional_width_gt_katz_width": int(((h2["mhi2"] - h2["mlo2"]) > kw2).sum()),
                   "median_worst_case_width": (h["mhi"] - h["mlo"]).median(),
                   "median_proportional_width": (h2["mhi2"] - h2["mlo2"]).median(),
                   "median_katz_width_same_rows": kw.median()})
    write_csv(pd.DataFrame(mb), out("extra_missing_bounds_vs_sampling.csv"))
    tm.mark("extras")

    # OSF cross-check
    D, S, pool_info = osf_crosscheck(df, args.osf_csv, args.osf_pdf_dir)
    write_csv(S, out("osf_crosscheck_summary.csv"))
    write_csv(D, priv("osf_crosscheck_detail_PRIVATE.csv"))
    tm.mark("osf_crosscheck")

    # stopping rule
    stop_rows = []
    for k in sets:
        g = Ru[sets[k]]
        for m, (lo, hi) in METHODS.items():
            v = excl(g[lo], g[hi], THRESH).mean() if len(g) else np.nan
            stop_rows.append({"set": k, "method": m, "n_ratios": len(g), "share_excl_0.8": v,
                              "threshold": STOP_SHARE, "exceeds_threshold": bool(v > STOP_SHARE)})
    stop_tab = pd.DataFrame(stop_rows)
    write_csv(stop_tab, out("stopping_rule_criterion2_all_variants.csv"))
    prim = stop_tab[(stop_tab["set"] == "E1_employer_posted_PRIMARY") & (stop_tab["method"] == PRIMARY_METHOD)].iloc[0]
    e1_all = stop_tab[stop_tab["set"] == "E1_employer_posted_PRIMARY"]
    stop = {
        "rule_text": ("stop Part 1 if the ACLU code already computes sampling intervals or if, after de-duplication, "
                      "more than about 80% of employer-level ratios have 95% intervals excluding 0.8"),
        "criterion_1_aclu_code_computes_sampling_intervals": "see aclu_code_inference_check.csv and README (manual reading)",
        "criterion_2_primary": {"set": "E1_employer_posted_PRIMARY", "method": PRIMARY_METHOD,
                                "n_ratios": int(prim["n_ratios"]), "share_excl_0.8": float(prim["share_excl_0.8"]),
                                "threshold": STOP_SHARE, "triggered": bool(prim["exceeds_threshold"])},
        "criterion_2_E1_other_methods": {r["method"]: float(r["share_excl_0.8"]) for _, r in e1_all.iterrows()},
        "criterion_2_range_over_all_variants_and_methods": [float(stop_tab["share_excl_0.8"].min()),
                                                            float(stop_tab["share_excl_0.8"].max())],
        "criterion_2_variants_exceeding_threshold": stop_tab.loc[stop_tab["exceeds_threshold"], ["set", "method"]].values.tolist(),
    }

    meta = {
        "run_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "python": sys.version.split()[0], "platform": platform.platform(),
        "numpy": np.__version__, "pandas": pd.__version__, "scipy": scipy.__version__,
        "pdftotext": subprocess.run(["pdftotext", "-v"], capture_output=True, text=True).stderr.splitlines()[0]
        if subprocess.run(["which", "pdftotext"], capture_output=True).returncode == 0 else None,
        "seeds": {"bootstrap": SEED, "jeffreys_posterior": [SEED, 1], "osf_sample": SEED},
        "n_boot": N_BOOT, "n_posterior_draws": N_POST, "primary_method": PRIMARY_METHOD,
        "bootstrap_nan_resamples_total": n_degen,
        "inputs": {"aclu_csv": {"path": args.aclu_csv, "sha256": sha256(args.aclu_csv), "bytes": os.path.getsize(args.aclu_csv),
                                "rows": int(len(df)), "columns": int(raw.shape[1])},
                   "osf_csv": {"path": args.osf_csv, "sha256": sha256(args.osf_csv), "bytes": os.path.getsize(args.osf_csv)}},
        "osf_crosscheck_pool": pool_info,
        "ratios_union_computed": int(len(Ru)),
        "timings_seconds": tm.marks,
        "stopping_rule": stop,
    }
    tm.mark("stopping_rule_meta")
    meta["timings_seconds"] = tm.marks
    meta["total_seconds"] = tm.total()
    with open(out("run_metadata.json"), "w") as f:
        json.dump(meta, f, indent=2, default=str)
    # row-level outputs stay private
    Ru.to_csv(priv("ratios_all_PRIVATE.csv"), index=False)
    T.to_csv(priv("tables_PRIVATE.csv"), index=False)
    Pex.to_csv(priv("excluded_population_per_table_PRIVATE.csv"), index=False)
    print(json.dumps({"stopping_rule": stop, "total_seconds": meta["total_seconds"]}, indent=2, default=str))


if __name__ == "__main__":
    main()
