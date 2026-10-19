"""Shared library for the idea-05 Stage 4 pilot (worker-ranking robustness).

Everything that defines the configuration space, the metric definitions, the
case-mix adjustment, attribution rules and the rank statistics lives here so
that every step script uses one implementation.  See ../README.md, section
"Operational definitions", for the prose version of each definition.

Scripts import this module by inserting their own directory into sys.path
(python -I does not add the script directory automatically).
"""
import math
import warnings

import numpy as np
import pandas as pd

SEED = 20261015
N_MIN_EVENTS = 100          # minimum events per resource for ranking (fixed before any tau was computed)
NOUSER = "__NOUSER__"

# ----------------------------------------------------------------------------
# Log-specific settings
# ----------------------------------------------------------------------------
LOGCFG = {
    "bpic2017": {
        "cols": {"case": "case:concept:name", "act": "concept:name", "lc": "lifecycle:transition",
                 "ts": "time:timestamp", "res": "org:resource"},
        "case_cat": ["case:LoanGoal", "case:ApplicationType"],
        "case_num": ["case:RequestedAmount"],
        "case_num_event": None,
        "tz": "Europe/Amsterdam",
        "period": ("2016-01-01", "2017-02-02"),
        "no_user_values": [""],
        # case completion = first terminal application decision
        "terminal": {"type": "first_of", "acts": ["A_Pending", "A_Denied", "A_Cancelled"]},
    },
    "bpic2019": {
        "cols": {"case": "case:concept:name", "act": "concept:name", "lc": None,
                 "ts": "time:timestamp", "res": "org:resource"},
        "case_cat": ["case:Item Category", "case:Item Type", "case:Document Type",
                     "case:Spend area text", "case:Company"],
        "case_num": [],
        "case_num_event": "Cumulative net worth (EUR)",   # first value in the case = item value
        "tz": "Europe/Amsterdam",
        "period": ("2018-01-01", "2019-02-01"),
        "no_user_values": ["NONE", ""],
        # case completion = last event, if it is a closing activity (consignment items close at goods receipt)
        "terminal": {"type": "last_if", "acts": ["Clear Invoice", "Delete Purchase Order Item"],
                     "consignment": ("case:Item Category", "Consignment", "Record Goods Receipt")},
    },
}

# ----------------------------------------------------------------------------
# Configuration space: metric x attribution x window x idle gap x case-mix = 405 cells
# ----------------------------------------------------------------------------
METRICS = ["EPH", "CCA", "APT", "RWK", "DLA"]
METRIC_LABEL = {"EPH": "events per active hour", "CCA": "completed cases attributed",
                "APT": "mean activity processing time", "RWK": "rework share",
                "DLA": "deadline adherence"}
ORIENT = {"EPH": 1.0, "CCA": 1.0, "APT": -1.0, "RWK": -1.0, "DLA": 1.0}   # higher oriented score = better
CASE_METRICS = {"CCA", "RWK", "DLA"}      # attribution rule applies
ATTRS = ["first", "last", "majority"]
WINS = ["week", "month", "quarter"]
GAPS = [15, 60, 240]                    # idle-gap threshold, minutes (applies to EPH only)
ADJS = ["none", "activity", "regression"]


def distinct_key(metric, attr, win, gap, adj):
    a = attr if metric in CASE_METRICS else "-"
    g = str(gap) if metric == "EPH" else "-"
    return f"{metric}|{a}|{win}|{g}|{adj}"


def build_space():
    """Return (cells DataFrame with 405 rows, distinct configs DataFrame)."""
    cells = []
    for m in METRICS:
        for a in ATTRS:
            for w in WINS:
                for g in GAPS:
                    for j in ADJS:
                        cells.append({"metric": m, "attr": a, "win": w, "gap": g, "adj": j,
                                      "key": distinct_key(m, a, w, g, j)})
    cells = pd.DataFrame(cells)
    keys = list(dict.fromkeys(cells["key"]))
    mult = cells["key"].value_counts()
    rows = []
    for i, k in enumerate(keys):
        m, a, w, g, j = k.split("|")
        rows.append({"cfg": i, "key": k, "metric": m, "attr": a, "win": w,
                     "gap": (int(g) if g != "-" else None), "adj": j, "multiplicity": int(mult[k])})
    distinct = pd.DataFrame(rows)
    cells["cfg"] = cells["key"].map(dict(zip(distinct["key"], distinct["cfg"])))
    return cells, distinct


BASELINE = distinct_key("CCA", "last", "month", 60, "none")


def primary_contrasts():
    """One-factor-at-a-time contrasts from the dashboard baseline plus every case-mix contrast
    at the baseline attribution/window/gap.  Returns list of (name, key_a, key_b, family)."""
    b = ("CCA", "last", "month", 60, "none")
    out = []
    for m in ["EPH", "APT", "RWK", "DLA"]:
        out.append((f"metric: CCA vs {m}", BASELINE, distinct_key(m, "last", "month", 60, "none"), "metric"))
    for a in ["first", "majority"]:
        out.append((f"attribution: last vs {a}", BASELINE, distinct_key("CCA", a, "month", 60, "none"), "attribution"))
    for w in ["week", "quarter"]:
        out.append((f"window: month vs {w}", BASELINE, distinct_key("CCA", "last", w, 60, "none"), "window"))
    for g in [15, 240]:
        out.append((f"idle gap (EPH): 60 vs {g} min", distinct_key("EPH", "last", "month", 60, "none"),
                    distinct_key("EPH", "last", "month", g, "none"), "idle_gap"))
    for m in METRICS:
        for j in ["activity", "regression"]:
            out.append((f"case-mix ({m}): none vs {j}", distinct_key(m, "last", "month", 60, "none"),
                        distinct_key(m, "last", "month", 60, j), "case_mix"))
    return out


def casemix_pairs(distinct):
    """All distinct (none, adjusted) pairs: same metric/attr/win/gap, adj none vs activity|regression.
    Returns DataFrame with cfg_a, cfg_b, weight (= number of 405-space pairs represented)."""
    d = distinct.set_index("key")
    rows = []
    for k, r in d.iterrows():
        if r["adj"] != "none":
            continue
        for j in ["activity", "regression"]:
            k2 = k.rsplit("|", 1)[0] + "|" + j
            rows.append({"key_a": k, "key_b": k2, "cfg_a": int(r["cfg"]), "cfg_b": int(d.loc[k2, "cfg"]),
                         "metric": r["metric"], "adj_b": j, "weight": int(r["multiplicity"])})
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------
# Loading
# ----------------------------------------------------------------------------
def load_log(path, logname):
    """Load the Parquet export of a log into a canonical event table.

    Columns: case, act, lc, res, ts (UTC seconds), loc (naive local time), eorder,
    cc_* (case categorical attributes as str), cn_* (case numeric, log1p)."""
    c = LOGCFG[logname]
    cols = c["cols"]
    use = [v for v in cols.values() if v] + c["case_cat"] + c["case_num"]
    if c["case_num_event"]:
        use.append(c["case_num_event"])
    df = pd.read_parquet(path, columns=use)
    out = pd.DataFrame({
        "case": df[cols["case"]].astype(str).to_numpy(),
        "act": df[cols["act"]].astype(str).to_numpy(),
    })
    out["lc"] = df[cols["lc"]].astype(str).str.lower().to_numpy() if cols["lc"] else "complete"
    res = df[cols["res"]]
    resv = res.astype(str).to_numpy(dtype=object)
    bad = res.isna().to_numpy() | np.isin(resv, c["no_user_values"]) | (resv == "nan")
    resv[bad] = NOUSER
    out["res"] = resv
    ts = df[cols["ts"]]
    out["ts"] = (ts - pd.Timestamp("1970-01-01", tz="UTC")).dt.total_seconds().to_numpy()
    out["loc"] = ts.dt.tz_convert(c["tz"]).dt.tz_localize(None).to_numpy()
    out["eorder"] = np.arange(len(df))
    for i, a in enumerate(c["case_cat"]):
        out[f"cc_{i}"] = df[a].astype(str).fillna("NA").to_numpy()
    for i, a in enumerate(c["case_num"]):
        out[f"cn_{i}"] = np.log1p(df[a].astype(float).clip(lower=0).fillna(0).to_numpy())
    if c["case_num_event"]:
        out["cn_ev"] = df[c["case_num_event"]].astype(float).to_numpy()
    lo, hi = pd.Timestamp(c["period"][0]), pd.Timestamp(c["period"][1])
    keep = (out["loc"] >= lo) & (out["loc"] < hi)
    info = {"events_read": int(len(out)), "events_outside_period_dropped": int((~keep).sum()),
            "period_local": list(c["period"])}
    out = out[keep].reset_index(drop=True)
    if c["case_num_event"]:
        # case value = first recorded value of the event attribute in the case
        first = out.sort_values(["case", "ts", "eorder"]).groupby("case")["cn_ev"].first()
        out["cn_ev"] = np.log1p(out["case"].map(first).clip(lower=0).fillna(0).to_numpy())
    return out, info


# ----------------------------------------------------------------------------
# Preparation of all metric units
# ----------------------------------------------------------------------------
def _factorize(x, sort=True):
    codes, uniques = pd.factorize(pd.Series(x), sort=sort)
    return codes.astype(np.int64), np.asarray(uniques)


def _first_per_group(g):
    """g sorted; return index of first element of each run and the group values."""
    idx = np.flatnonzero(np.r_[True, g[1:] != g[:-1]])
    return idx


def prepare(base, logname, excluded=()):
    """Build every unit table needed by the scoring engine.

    base: canonical event table (load_log); excluded: resource names treated as
    ineligible (system/batch accounts) for attribution and ranking."""
    c = LOGCFG[logname]
    df = base.sort_values(["case", "ts", "eorder"], kind="stable").reset_index(drop=True)
    n = len(df)
    case_ev, case_names = _factorize(df["case"].to_numpy())
    nC = len(case_names)
    res_ev, res_names = _factorize(df["res"].to_numpy())
    nR = len(res_names)
    excl = np.isin(res_names, list(excluded)) | (res_names == NOUSER)
    eligible = ~excl
    act_ev, act_names = _factorize(df["act"].to_numpy())
    lc = df["lc"].to_numpy(dtype=object)
    strat_ev, strat_names = _factorize((df["act"] + "|" + df["lc"]).to_numpy())
    ts = df["ts"].to_numpy(dtype=float)
    loc = pd.Series(df["loc"])
    slots = {}
    for w, f in (("week", "W-SUN"), ("month", "M"), ("quarter", "Q")):
        codes, names = _factorize(loc.dt.to_period(f).astype(str).to_numpy())
        slots[w] = (codes, len(names), names)

    # --- per-resource event gaps (for active time) ---
    order = np.lexsort((df["eorder"].to_numpy(), ts, res_ev))
    ts_o, r_o = ts[order], res_ev[order]
    gap = np.full(n, np.inf)
    same = r_o[1:] == r_o[:-1]
    d = ts_o[1:] - ts_o[:-1]
    gap[:-1] = np.where(same, d, np.inf)
    gap_next = np.empty(n)
    gap_next[order] = gap

    # --- case table ---
    first_idx = _first_per_group(case_ev)
    last_idx = np.r_[first_idx[1:] - 1, n - 1]
    start_ts = ts[first_idx]
    t = c["terminal"]
    comp_ev = np.full(nC, -1, dtype=np.int64)
    if t["type"] == "first_of":
        m = np.isin(df["act"].to_numpy(), t["acts"])
        idx = np.flatnonzero(m)
        cs = case_ev[idx]
        fi = _first_per_group(cs)
        comp_ev[cs[fi]] = idx[fi]
    else:
        la = df["act"].to_numpy()[last_idx]
        ok = np.isin(la, t["acts"])
        col, val, act2 = t["consignment"]
        ci = LOGCFG[logname]["case_cat"].index(col)
        cat = df[f"cc_{ci}"].to_numpy()[last_idx]
        ok |= (cat == val) & (la == act2)
        comp_ev[ok] = last_idx[ok]
    completed = comp_ev >= 0
    comp_ts = np.where(completed, ts[np.maximum(comp_ev, 0)], np.nan)
    upto = completed[case_ev] & (ts <= np.nan_to_num(comp_ts, nan=-np.inf)[case_ev])
    effort = np.bincount(case_ev, weights=upto.astype(float), minlength=nC)
    # rework: an activity label completed more than once in the case (up to completion)
    cm = upto & (lc == "complete")
    key = case_ev[cm] * len(act_names) + act_ev[cm]
    uk, cnt = np.unique(key, return_counts=True)
    rework = np.zeros(nC, dtype=bool)
    rework[(uk[cnt > 1] // len(act_names)).astype(np.int64)] = True
    dur_days = (comp_ts - start_ts) / 86400.0
    T_days = float(math.ceil(np.nanmedian(dur_days[completed])))
    ontime = dur_days <= T_days

    # case covariate design (reference level = most frequent level dropped)
    xs, xnames = [], []
    for i, a in enumerate(c["case_cat"]):
        v = df[f"cc_{i}"].to_numpy()[first_idx]
        vc = pd.Series(v).value_counts()
        for lev in vc.index[1:]:
            xs.append((v == lev).astype(float))
            xnames.append(f"{a}={lev}")
    numcols = [col for col in df.columns if col.startswith("cn_")]
    for col in numcols:
        v = df[col].to_numpy()[first_idx].astype(float)
        sd = v.std() if v.std() > 0 else 1.0
        xs.append((v - v.mean()) / sd)
        xnames.append(col)
    Xcase = np.column_stack(xs) if xs else np.zeros((nC, 0))

    # --- attribution ---
    elig_ev = upto & eligible[res_ev]
    sub = np.flatnonzero(elig_ev)
    cs = case_ev[sub]
    att = {}
    if len(sub):
        fi = _first_per_group(cs)
        li = np.r_[fi[1:] - 1, len(sub) - 1]
        for rule, pos in (("first", fi), ("last", li)):
            r = np.full(nC, -1, dtype=np.int64)
            a = np.full(nC, -1, dtype=np.int64)
            r[cs[pos]] = res_ev[sub[pos]]
            a[cs[pos]] = act_ev[sub[pos]]
            att[rule] = (r, a)
        # majority: most events in the case; ties -> earliest first touch
        k = cs * nR + res_ev[sub]
        uk, firstpos, cnt = np.unique(k, return_index=True, return_counts=True)
        ucase = uk // nR
        o = np.lexsort((firstpos, -cnt, ucase))
        sel = o[_first_per_group(ucase[o])]
        r = np.full(nC, -1, dtype=np.int64)
        r[ucase[sel]] = uk[sel] % nR
        # attributed activity: the majority resource's most frequent activity in the case (ties -> earliest)
        mres = r[cs]
        mm = res_ev[sub] == mres
        s2 = sub[mm]
        k2 = case_ev[s2] * len(act_names) + act_ev[s2]
        uk2, fp2, cnt2 = np.unique(k2, return_index=True, return_counts=True)
        uc2 = uk2 // len(act_names)
        o2 = np.lexsort((fp2, -cnt2, uc2))
        sel2 = o2[_first_per_group(uc2[o2])]
        a = np.full(nC, -1, dtype=np.int64)
        a[uc2[sel2]] = uk2[sel2] % len(act_names)
        att["majority"] = (r, a)
    else:
        for rule in ATTRS:
            att[rule] = (np.full(nC, -1, dtype=np.int64), np.full(nC, -1, dtype=np.int64))

    # --- processing-time units ---
    has_start = set(df.loc[lc == "start", "act"].unique())
    if has_start:
        m = np.isin(df["act"].to_numpy(), list(has_start)) & np.isin(lc, ["start", "resume", "suspend", "complete", "ate_abort"])
        w = df.loc[m, ["act", "lc", "res", "ts", "eorder"]].copy()
        w["case_i"] = case_ev[m]
        w["act_i"] = act_ev[m]
        w["res_i"] = res_ev[m]
        w["ev"] = np.flatnonzero(m)
        w = w.sort_values(["case_i", "act_i", "ts", "eorder"], kind="stable")
        grp = (w["case_i"].to_numpy() * len(act_names) + w["act_i"].to_numpy())
        newg = np.r_[True, grp[1:] != grp[:-1]]
        lcw = w["lc"].to_numpy(dtype=object)
        inst = np.cumsum(lcw == "start")  # global counter is fine: unique per group because groups are contiguous
        nxt_same = np.r_[~newg[1:], False]
        nlc = np.concatenate([lcw[1:], np.array(["END"], dtype=object)])
        nres = np.r_[w["res_i"].to_numpy()[1:], -1]
        nts = np.r_[w["ts"].to_numpy()[1:], np.nan]
        nev = np.r_[w["ev"].to_numpy()[1:], -1]
        seg = (np.isin(lcw, ["start", "resume"]) & nxt_same & np.isin(nlc, ["suspend", "complete", "ate_abort"])
               & (nres == w["res_i"].to_numpy()))
        segdf = pd.DataFrame({"case_i": w["case_i"].to_numpy()[seg], "act_i": w["act_i"].to_numpy()[seg],
                              "inst": inst[seg], "res_i": w["res_i"].to_numpy()[seg],
                              "dur": (nts - w["ts"].to_numpy())[seg], "end_ev": nev[seg]})
        u = segdf.groupby(["case_i", "act_i", "inst", "res_i"], sort=False).agg(dur=("dur", "sum"), end_ev=("end_ev", "max")).reset_index()
        apt = {"case": u["case_i"].to_numpy(), "res": u["res_i"].to_numpy(), "strat": u["act_i"].to_numpy(),
               "y": u["dur"].to_numpy(dtype=float), "ev": u["end_ev"].to_numpy(), "mode": "start-complete work segments",
               "segments": int(seg.sum()), "segments_dropped_resource_change": int((np.isin(lcw, ["start", "resume"]) & nxt_same & np.isin(nlc, ["suspend", "complete", "ate_abort"]) & (nres != w["res_i"].to_numpy())).sum())}
    else:
        prev_same = np.r_[False, case_ev[1:] == case_ev[:-1]]
        idx = np.flatnonzero(prev_same)
        apt = {"case": case_ev[idx], "res": res_ev[idx], "strat": act_ev[idx],
               "y": ts[idx] - ts[idx - 1], "ev": idx, "mode": "inter-event time within case (single-timestamp log)",
               "segments": int(len(idx)), "segments_dropped_resource_change": 0}

    n_events_res = np.bincount(res_ev, minlength=nR)
    P = {
        "logname": logname, "n_events": n, "nC": nC, "nR": nR, "res_names": res_names, "act_names": act_names,
        "eligible": eligible, "n_events_res": n_events_res,
        "case_ev": case_ev, "res_ev": res_ev, "strat_ev": strat_ev, "gap_next": gap_next,
        "slots": slots, "completed": completed, "comp_ev": comp_ev, "effort": effort,
        "rework": rework, "ontime": ontime, "T_days": T_days, "dur_days": dur_days,
        "Xcase": Xcase, "Xcase_names": xnames, "att": att, "apt": apt,
    }
    _fit_expectations(P)
    return P


# ----------------------------------------------------------------------------
# Case-mix expectations
# ----------------------------------------------------------------------------
def _expected(y, strat, case_idx, Xcase, fit):
    """Activity-stratified means and regression (activity FE + case covariates) fitted values."""
    y2 = y.reshape(len(y), -1).astype(float)
    k = y2.shape[1]
    nS = int(strat.max()) + 1 if len(strat) else 1
    fidx = np.flatnonzero(fit)
    cnt = np.bincount(strat[fidx], minlength=nS).astype(float)
    gm = y2[fidx].mean(axis=0)
    ms = np.empty((nS, k))
    for j in range(k):
        s = np.bincount(strat[fidx], weights=y2[fidx, j], minlength=nS)
        ms[:, j] = np.where(cnt > 0, s / np.maximum(cnt, 1), gm[j])
    e_strat = ms[strat]
    p = nS + Xcase.shape[1]
    XtX = np.zeros((p, p))
    Xty = np.zeros((p, k))

    def build(ix):
        X = np.zeros((len(ix), p))
        X[np.arange(len(ix)), strat[ix]] = 1.0
        if Xcase.shape[1]:
            X[:, nS:] = Xcase[case_idx[ix]]
        return X

    for s0 in range(0, len(fidx), 200000):
        ix = fidx[s0:s0 + 200000]
        X = build(ix)
        XtX += X.T @ X
        Xty += X.T @ y2[ix]
    beta = np.linalg.solve(XtX + 1e-8 * np.eye(p), Xty)
    e_reg = np.empty_like(y2)
    allix = np.arange(len(y2))
    for s0 in range(0, len(allix), 200000):
        ix = allix[s0:s0 + 200000]
        e_reg[ix] = build(ix) @ beta
    if k == 1:
        return e_strat[:, 0], e_reg[:, 0]
    return e_strat, e_reg


def _fit_expectations(P):
    elig = P["eligible"]
    # EPH: active-time credit per event for each gap
    a = np.column_stack([np.minimum(P["gap_next"], g * 60.0) for g in GAPS])
    a[~np.isfinite(a)] = 0  # never happens: inf gaps are capped by min()
    P["eph_a"] = a
    fit = elig[P["res_ev"]]
    es, er = _expected(a, P["strat_ev"], P["case_ev"], P["Xcase"], fit)
    P["eph_e"] = {"activity": es, "regression": er}
    # APT
    u = P["apt"]
    fit = elig[u["res"]]
    es, er = _expected(u["y"], u["strat"], u["case"], P["Xcase"], fit)
    u["e"] = {"activity": np.maximum(es, 1e-9), "regression": np.maximum(er, 1e-9)}
    # case-level units per attribution rule
    P["cases"] = {}
    for rule in ATTRS:
        r, aact = P["att"][rule]
        cidx = np.flatnonzero((r >= 0) & P["completed"])
        y = np.column_stack([P["effort"][cidx], P["rework"][cidx].astype(float), P["ontime"][cidx].astype(float)])
        es, er = _expected(y, aact[cidx], cidx, P["Xcase"], np.ones(len(cidx), dtype=bool))
        P["cases"][rule] = {"case": cidx, "res": r[cidx], "strat": aact[cidx], "y": y,
                            "e": {"activity": es, "regression": er}}


# ----------------------------------------------------------------------------
# Scoring engine
# ----------------------------------------------------------------------------
def _slot_values(key, num, den, nR, nS, count_scope=None):
    N = np.bincount(key, weights=num, minlength=nR * nS).reshape(nR, nS)
    if count_scope is not None:
        scope = count_scope | (N > 0)
        return np.where(scope, N, np.nan)
    D = np.bincount(key, weights=den, minlength=nR * nS).reshape(nR, nS)
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(D > 0, N / D, np.nan)


def _nanmean_rows(V):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        return np.nanmean(V, axis=1)


def compute_scores(P, distinct, w_case=None, keep_slots=False):
    """Oriented resource scores (higher = better) for every distinct configuration.

    w_case: optional case weights (bootstrap).  Returns array (n_cfg, nR) and, if
    keep_slots, a dict cfg -> per-slot value matrix (nR, nS) (unoriented)."""
    nR = P["nR"]
    w_ev = np.ones(P["n_events"]) if w_case is None else w_case[P["case_ev"]]
    u = P["apt"]
    w_apt = np.ones(len(u["y"])) if w_case is None else w_case[u["case"]]
    out = np.full((len(distinct), nR), np.nan)
    slots_out = {} if keep_slots else None
    for win in WINS:
        sl, nS, _ = P["slots"][win]
        key_ev = P["res_ev"] * nS + sl
        active = np.bincount(key_ev, weights=w_ev, minlength=nR * nS).reshape(nR, nS) > 0
        key_apt = u["res"] * nS + sl[u["ev"]]
        ckeys = {}
        for rule in ATTRS:
            cu = P["cases"][rule]
            ckeys[rule] = (cu["res"] * nS + sl[P["comp_ev"][cu["case"]]],
                           np.ones(len(cu["case"])) if w_case is None else w_case[cu["case"]])
        for _, row in distinct[distinct["win"] == win].iterrows():
            m, adj = row["metric"], row["adj"]
            if m == "EPH":
                gi = GAPS.index(int(row["gap"]))
                a = P["eph_a"][:, gi]
                num = w_ev * (3600.0 if adj == "none" else P["eph_e"][adj][:, gi])
                V = _slot_values(key_ev, num, w_ev * a, nR, nS)
            elif m == "APT":
                if adj == "none":
                    V = _slot_values(key_apt, w_apt * u["y"] / 3600.0, w_apt, nR, nS)
                else:
                    V = _slot_values(key_apt, w_apt * u["y"], w_apt * u["e"][adj], nR, nS)
            else:
                cu = P["cases"][row["attr"]]
                key, wc = ckeys[row["attr"]]
                if m == "CCA":
                    if adj == "none":
                        num = wc
                    else:
                        e = cu["e"][adj][:, 0]
                        num = wc * e / e.mean()
                    V = _slot_values(key, num, None, nR, nS, count_scope=active)
                else:
                    j = 1 if m == "RWK" else 2
                    y = cu["y"][:, j]
                    yy = y if adj == "none" else y - cu["e"][adj][:, j]
                    V = _slot_values(key, wc * yy, wc, nR, nS)
            out[int(row["cfg"])] = ORIENT[m] * _nanmean_rows(V)
            if keep_slots:
                slots_out[int(row["cfg"])] = V
    return (out, slots_out) if keep_slots else out


def analysis_set(P, scores, n_min=N_MIN_EVENTS, complete_case=False):
    """Primary: eligible (not system/no-user) resources with >= n_min events; statistics are then
    pairwise-complete.  complete_case=True additionally requires a defined score in every configuration."""
    ok = P["eligible"] & (P["n_events_res"] >= n_min)
    if complete_case:
        ok &= np.all(np.isfinite(scores), axis=0)
    return np.flatnonzero(ok)


# ----------------------------------------------------------------------------
# Rank statistics
# ----------------------------------------------------------------------------
def tau_b_matrix(S):
    """Kendall tau-b between all rows of S (configs x units), pairwise-complete on NaN."""
    k, n = S.shape
    iu, ju = np.triu_indices(n, 1)
    valid = np.isfinite(S)
    D = np.sign(np.nan_to_num(S[:, iu]) - np.nan_to_num(S[:, ju]))
    M = (valid[:, iu] & valid[:, ju]).astype(np.float64)
    D = D * M
    num = D @ D.T
    A = np.abs(D)
    den = np.sqrt((A @ M.T) * (M @ A.T))
    with np.errstate(divide="ignore", invalid="ignore"):
        T = num / den
    return T


def spearman_matrix(S):
    df = pd.DataFrame(S.T)
    return df.corr(method="spearman").to_numpy()


def bottom_set(x, frac=0.2):
    idx = np.flatnonzero(np.isfinite(x))
    k = int(math.floor(frac * len(idx) + 0.5))
    o = idx[np.lexsort((idx, x[idx]))]
    return set(o[:k].tolist()), k


def reclass_rate(xa, xb, frac=0.2):
    """Share of the bottom quintile under a that is not in the bottom quintile under b
    (computed on units defined under both)."""
    m = np.isfinite(xa) & np.isfinite(xb)
    xa2 = np.where(m, xa, np.nan)
    xb2 = np.where(m, xb, np.nan)
    A, k = bottom_set(xa2, frac)
    B, _ = bottom_set(xb2, frac)
    if k == 0:
        return np.nan, np.nan
    moved = len(A - B)
    return moved / k, 2 * moved / int(m.sum())   # (share of bottom quintile, share of all workers changing status)


def weighted_median(values, weights):
    v = np.asarray(values, float)
    w = np.asarray(weights, float)
    m = np.isfinite(v)
    v, w = v[m], w[m]
    o = np.argsort(v)
    v, w = v[o], w[o]
    c = np.cumsum(w)
    half = c[-1] / 2.0
    i = np.searchsorted(c, half)
    if np.isclose(c[i], half) and i + 1 < len(v):
        return float((v[i] + v[i + 1]) / 2)
    return float(v[i])


def summarize_tau(T, distinct):
    """Median tau over distinct pairs and over the 405-cell pairs (identical cells count tau=1)."""
    k = T.shape[0]
    iu, ju = np.triu_indices(k, 1)
    vals = T[iu, ju]
    mult = distinct["multiplicity"].to_numpy()
    w = mult[iu] * mult[ju]
    vals405 = np.r_[vals, np.ones(k)]
    w405 = np.r_[w, mult * (mult - 1) / 2.0]
    return {
        "n_distinct_configs": int(k), "n_distinct_pairs": int(len(vals)),
        "median_tau_distinct": float(np.nanmedian(vals)), "mean_tau_distinct": float(np.nanmean(vals)),
        "p10_tau_distinct": float(np.nanpercentile(vals, 10)), "p90_tau_distinct": float(np.nanpercentile(vals, 90)),
        "min_tau_distinct": float(np.nanmin(vals)), "max_tau_distinct": float(np.nanmax(vals)),
        "share_pairs_tau_gt_0.9": float(np.nanmean(vals > 0.9)), "share_pairs_tau_lt_0.7": float(np.nanmean(vals < 0.7)),
        "median_tau_405cells": weighted_median(vals405, w405),
        "n_405cell_pairs": int(round(w405.sum())),
    }


def summarize_reclass(scores_sub, pairs):
    r1, r2 = [], []
    for _, p in pairs.iterrows():
        a, b = reclass_rate(scores_sub[p["cfg_a"]], scores_sub[p["cfg_b"]])
        r1.append(a)
        r2.append(b)
    pairs = pairs.copy()
    pairs["reclass_bottom"] = r1
    pairs["status_change_all"] = r2
    return pairs, {
        "n_distinct_casemix_pairs": int(len(pairs)),
        "median_reclass_bottom_distinct": float(np.nanmedian(r1)),
        "mean_reclass_bottom_distinct": float(np.nanmean(r1)),
        "median_reclass_bottom_405": weighted_median(r1, pairs["weight"]),
        "median_status_change_all_distinct": float(np.nanmedian(r2)),
        "median_status_change_all_405": weighted_median(r2, pairs["weight"]),
        "max_reclass_bottom_distinct": float(np.nanmax(r1)),
        "min_reclass_bottom_distinct": float(np.nanmin(r1)),
    }
