"""Step 01: convert an XES / XES.GZ event log to Parquet once, with pm4py.

Usage:
    python -I 01_convert_to_parquet.py <input.xes[.gz]> <output.parquet> <provenance.json>

Reads the log with pm4py.read_xes (pandas DataFrame in pm4py 2.7), writes it to
Parquet with pyarrow and records sha256 of input and output, row/column counts,
pm4py/pandas versions and wall-clock time in a small JSON provenance file.
"""
import hashlib
import json
import os
import sys
import time


def sha256(path, block=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(block)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def main():
    src, dst, prov = sys.argv[1], sys.argv[2], sys.argv[3]
    t0 = time.time()
    import pandas as pd
    import pm4py

    df = pm4py.read_xes(src)
    t_read = time.time() - t0
    # object columns with mixed types break pyarrow; coerce them to string
    for c in df.columns:
        if df[c].dtype == object:
            kinds = set(type(v).__name__ for v in df[c].dropna().head(20000))
            if len(kinds) > 1 or (kinds and kinds != {"str"}):
                df[c] = df[c].astype("string")
    df.to_parquet(dst, index=False)
    t_total = time.time() - t0
    info = {
        "input": os.path.abspath(src),
        "input_bytes": os.path.getsize(src),
        "input_sha256": sha256(src),
        "output": os.path.abspath(dst),
        "output_bytes": os.path.getsize(dst),
        "output_sha256": sha256(dst),
        "rows": int(len(df)),
        "columns": [str(c) for c in df.columns],
        "dtypes": {str(c): str(t) for c, t in df.dtypes.items()},
        "pm4py_version": pm4py.__version__,
        "pandas_version": pd.__version__,
        "seconds_read_xes": round(t_read, 1),
        "seconds_total": round(t_total, 1),
    }
    with open(prov, "w") as fh:
        json.dump(info, fh, indent=1)
    print(json.dumps({k: v for k, v in info.items() if k not in ("columns", "dtypes")}, indent=1))


if __name__ == "__main__":
    main()
