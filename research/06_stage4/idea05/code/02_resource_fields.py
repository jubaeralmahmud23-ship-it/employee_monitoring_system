"""Step 02: confirm what the resource field holds in each log and report counts.

Usage:
    python -I 02_resource_fields.py <bpic2017.parquet> <bpic2019.parquet> <results_dir>

Writes results/resource_fields.json and results/resource_fields.csv (aggregate counts only;
no per-pseudonym rows).
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import idea05lib as L  # noqa: E402


def classify(name, logname):
    if name == L.NOUSER:
        return "no user recorded (NONE/empty)"
    if logname == "bpic2019":
        if name.startswith("batch_"):
            return "batch user (publisher label: automated)"
        if name.startswith("user_"):
            return "normal user (publisher label: human)"
        return "other"
    if re.fullmatch(r"User_\d+", name):
        return "User_<n> pseudonym (no publisher label)"
    return "other"


def main():
    p17, p19, outdir = sys.argv[1:4]
    rows, out = [], {}
    for logname, path in (("bpic2017", p17), ("bpic2019", p19)):
        raw = pd.read_parquet(path)
        cols = L.LOGCFG[logname]["cols"]
        base, info = L.load_log(path, logname)
        vc = base["res"].value_counts()
        kinds = pd.Series({r: classify(r, logname) for r in vc.index})
        agg = pd.DataFrame({"n_events": vc, "kind": kinds}).groupby("kind").agg(
            accounts=("n_events", "size"), events=("n_events", "sum"),
            accounts_ge_100_events=("n_events", lambda s: int((s >= L.N_MIN_EVENTS).sum())),
            median_events_per_account=("n_events", "median"), max_events_per_account=("n_events", "max"))
        for k, r in agg.iterrows():
            rows.append({"log": logname, "kind": k, **{c: (float(v) if isinstance(v, (float, np.floating)) else int(v)) for c, v in r.items()}})
        lcv = raw[cols["lc"]].value_counts().to_dict() if cols["lc"] else {"(no lifecycle attribute)": int(len(raw))}
        out[logname] = {
            "events_in_parquet": int(len(raw)),
            "events_after_period_filter": int(len(base)),
            "period_filter": info,
            "cases": int(base["case"].nunique()),
            "distinct_resource_values_raw": int(raw[cols["res"]].nunique(dropna=False)),
            "distinct_resource_values_after_filter": int(len(vc)),
            "resource_attribute_columns": [c for c in raw.columns if c in ("org:resource", "User", "org:role", "org:group")],
            "lifecycle_values": {str(k): int(v) for k, v in lcv.items()},
            "timestamp_min_utc": str(raw[cols["ts"]].min()), "timestamp_max_utc": str(raw[cols["ts"]].max()),
            "share_timestamps_with_nonzero_seconds": float((raw[cols["ts"]].dt.second != 0).mean()),
            "top_account_share_of_events": float(vc.iloc[0] / vc.sum()),
            "top_account_is": classify(vc.index[0], logname),
        }
        if logname == "bpic2017":
            out[logname]["User_1_events"] = int(vc.get("User_1", 0))
            out[logname]["User_1_share_of_events"] = float(vc.get("User_1", 0) / vc.sum())
            u1 = base[base["res"] == "User_1"]["act"].value_counts().head(8)
            out[logname]["User_1_top_activities"] = {k: int(v) for k, v in u1.items()}
        if logname == "bpic2019":
            out[logname]["User_column_equals_org_resource_share"] = float(
                (raw["User"].astype(str) == raw["org:resource"].astype(str)).mean()) if "User" in raw.columns else None
    pd.DataFrame(rows).to_csv(os.path.join(outdir, "resource_fields.csv"), index=False)
    with open(os.path.join(outdir, "resource_fields.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(pd.DataFrame(rows).to_string())
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
