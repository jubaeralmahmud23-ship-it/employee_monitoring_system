"""Step 03: automated-account detector, calibrated on BPI 2019's publisher-labelled batch users,
then applied to BPI 2017.

Usage:
    python -I 03_detector.py <bpic2017.parquet> <bpic2019.parquet> <results_dir> <derived_dir>

Pre-specified features (written before the labels were examined):
  f_offhours        share of events with local clock time in [20:00, 06:00) or on Sat/Sun,
                    ignoring events stamped exactly 00:00:00 local (date-only artefacts)
  f_multicase_burst share of events in a (resource, clock-minute) bucket touching >= 5 distinct cases
  z_volume          robust z of log10(event count) across accounts (median, 1.4826*MAD)
Pre-specified rules:
  R1 f_offhours >= 0.25 ; R2 f_multicase_burst >= 0.5 ; R3 z_volume >= 3.5 ; R_any = R1 or R2 or R3
Comparator: logistic regression on the three features plus log10 count, class-balanced,
stratified 5-fold CV repeated 20 times (seed 20261015).

Results (aggregate) go to results/; the per-account flag list goes to derived_dir only.
After the calibration showed low per-account precision for R_any, the BPI 2017 primary exclusion
was set to User_1 only (recorded as a deviation in README.md); R_any and LR flag sets are sensitivities.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import idea05lib as L  # noqa: E402


def features(base):
    b = base[base["res"] != L.NOUSER].copy()
    loc = pd.to_datetime(b["loc"])
    midnight = (loc.dt.hour == 0) & (loc.dt.minute == 0) & (loc.dt.second == 0)
    off = ((loc.dt.hour >= 20) | (loc.dt.hour < 6) | (loc.dt.dayofweek >= 5)) & ~midnight
    b["off"] = off.to_numpy()
    b["valid_clock"] = (~midnight).to_numpy()
    b["minute"] = (b["ts"] // 60).astype(np.int64)
    bucket = b.groupby(["res", "minute"])["case"].nunique().rename("ncase")
    b = b.join(bucket, on=["res", "minute"])
    b["burst"] = b["ncase"] >= 5
    g = b.groupby("res")
    f = pd.DataFrame({
        "n_events": g.size(),
        "f_offhours": g["off"].sum() / g["valid_clock"].sum().clip(lower=1),
        "f_multicase_burst": g["burst"].mean(),
    })
    lv = np.log10(f["n_events"])
    mad = 1.4826 * np.median(np.abs(lv - np.median(lv)))
    f["z_volume"] = (lv - np.median(lv)) / (mad if mad > 0 else 1.0)
    f["R1"] = f["f_offhours"] >= 0.25
    f["R2"] = f["f_multicase_burst"] >= 0.5
    f["R3"] = f["z_volume"] >= 3.5
    f["R_any"] = f["R1"] | f["R2"] | f["R3"]
    return f


def prf(y, p, w=None):
    w = np.ones(len(y)) if w is None else np.asarray(w, float)
    tp = float((w * (y & p)).sum()); fp = float((w * (~y & p)).sum()); fn = float((w * (y & ~p)).sum())
    tn = float((w * (~y & ~p)).sum())
    prec = tp / (tp + fp) if tp + fp > 0 else float("nan")
    rec = tp / (tp + fn) if tp + fn > 0 else float("nan")
    f1 = 2 * prec * rec / (prec + rec) if prec == prec and rec == rec and prec + rec > 0 else float("nan")
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn, "precision": prec, "recall": rec, "f1": f1}


def main():
    p17, p19, outdir, derived = sys.argv[1:5]
    os.makedirs(derived, exist_ok=True)
    b19, _ = L.load_log(p19, "bpic2019")
    f19 = features(b19)
    f19["label_batch"] = f19.index.str.startswith("batch_")
    rows = []
    for subset, mask in (("all accounts", np.ones(len(f19), bool)), (f"accounts with >= {L.N_MIN_EVENTS} events", f19["n_events"].to_numpy() >= L.N_MIN_EVENTS)):
        s = f19[mask]
        y = s["label_batch"].to_numpy()
        for rule in ["R1", "R2", "R3", "R_any"]:
            p = s[rule].to_numpy()
            for wname, w in (("per account", None), ("event-weighted", s["n_events"].to_numpy())):
                rows.append({"log": "bpic2019", "subset": subset, "n_accounts": int(len(s)), "n_batch": int(y.sum()),
                             "rule": rule, "weighting": wname, **prf(y, p, w)})
    # learned comparator
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import RepeatedStratifiedKFold
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    X = np.column_stack([np.log10(f19["n_events"]), f19["f_offhours"], f19["f_multicase_burst"], f19["z_volume"]])
    y = f19["label_batch"].to_numpy()
    cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=20, random_state=L.SEED)
    precs, recs = [], []
    for tr, te in cv.split(X, y):
        m = make_pipeline(StandardScaler(), LogisticRegression(class_weight="balanced", max_iter=1000))
        m.fit(X[tr], y[tr])
        p = m.predict(X[te]).astype(bool)
        r = prf(y[te], p)
        precs.append(r["precision"]); recs.append(r["recall"])
    rows.append({"log": "bpic2019", "subset": "all accounts", "n_accounts": int(len(y)), "n_batch": int(y.sum()),
                 "rule": "logistic regression (5-fold CV x20, mean over folds)", "weighting": "per account",
                 "precision": float(np.nanmean(precs)), "recall": float(np.nanmean(recs))})
    final = make_pipeline(StandardScaler(), LogisticRegression(class_weight="balanced", max_iter=1000)).fit(X, y)
    # calibration curve for the off-hours feature alone (added after the pre-specified rules were evaluated)
    sweep = []
    for thr in [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 0.60]:
        p = (f19["f_offhours"] >= thr).to_numpy()
        for wname, w in (("per account", None), ("event-weighted", f19["n_events"].to_numpy())):
            sweep.append({"threshold_f_offhours": thr, "weighting": wname, **prf(y, p, w)})
    pd.DataFrame(sweep).to_csv(os.path.join(outdir, "detector_offhours_threshold_sweep_bpic2019.csv"), index=False)

    # feature distributions by label (aggregate)
    dist = f19.groupby("label_batch")[["n_events", "f_offhours", "f_multicase_burst", "z_volume"]].describe().T
    dist.columns = ["human" if not c else "batch" for c in dist.columns]

    # apply to BPI 2017
    b17, _ = L.load_log(p17, "bpic2017")
    f17 = features(b17)
    X17 = np.column_stack([np.log10(f17["n_events"]), f17["f_offhours"], f17["f_multicase_burst"], f17["z_volume"]])
    f17["LR"] = final.predict(X17).astype(bool)
    flagged = {r: sorted(f17.index[f17[r]].tolist()) for r in ["R1", "R2", "R3", "R_any", "LR"]}
    apply_summary = {r: {"n_flagged": len(v), "events_of_flagged": int(f17.loc[v, "n_events"].sum()),
                         "share_of_events": float(f17.loc[v, "n_events"].sum() / f17["n_events"].sum()),
                         "User_1_flagged": "User_1" in v, "other_accounts_flagged": int(len([x for x in v if x != "User_1"]))}
                     for r, v in flagged.items()}
    u1 = f17.loc["User_1", ["n_events", "f_offhours", "f_multicase_burst", "z_volume"]].to_dict()
    others = f17.drop(index="User_1")[["f_offhours", "f_multicase_burst", "z_volume"]].describe().to_dict()

    pd.DataFrame(rows).to_csv(os.path.join(outdir, "detector_calibration_bpic2019.csv"), index=False)
    dist.to_csv(os.path.join(outdir, "detector_feature_distributions_bpic2019.csv"))
    summary = {
        "features_and_rules": __doc__,
        "bpic2019_accounts": int(len(f19)), "bpic2019_batch_accounts": int(y.sum()),
        "bpic2017_application": apply_summary,
        "bpic2017_User_1_features": {k: float(v) for k, v in u1.items()},
        "bpic2017_other_accounts_feature_summary": {k: {kk: float(vv) for kk, vv in v.items()} for k, v in others.items()},
        "primary_exclusion_rule_bpic2017": ("User_1 only. Deviation: R_any was pre-specified as the BPI 2017 exclusion rule, "
                                            "but its per-account precision on BPI 2019's labelled split was low, so the plan's "
                                            "named system account (User_1) is the primary exclusion and the R_any set is a sensitivity."),
        "primary_exclusion_rule_bpic2019": "publisher label (batch_*)",
    }
    with open(os.path.join(outdir, "detector_summary.json"), "w") as fh:
        json.dump(summary, fh, indent=1)
    # per-account outputs stay in the untracked derived directory
    f19.to_csv(os.path.join(derived, "detector_features_bpic2019.csv"))
    f17.to_csv(os.path.join(derived, "detector_features_bpic2017.csv"))
    excl = {
        "bpic2017": {"primary": ["User_1"], "none": [], "detector_R_any": flagged["R_any"], "detector_LR": flagged["LR"]},
        "bpic2019": {"primary": sorted(f19.index[f19["label_batch"]].tolist()), "none": [],
                     "labelled_or_detected": sorted(set(f19.index[f19["label_batch"]]) | set(f19.index[f19["R_any"]]))},
    }
    with open(os.path.join(derived, "exclusions.json"), "w") as fh:
        json.dump(excl, fh, indent=1)
    print(pd.DataFrame(rows).to_string())
    print(json.dumps({k: v for k, v in summary.items() if k != "features_and_rules"}, indent=1))
    print("exclusion set sizes:", {lg: {k: len(v) for k, v in d.items()} for lg, d in excl.items()})


if __name__ == "__main__":
    main()
