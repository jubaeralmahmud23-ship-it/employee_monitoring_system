#!/usr/bin/env bash
# Stage 4 pilot, idea 4 (NYC LL 144 impact ratios). Exploratory.
# Reproduces every file in ../results/ from the inputs named below.
#
# Inputs (git-ignored, outside the repository; see ../README.md for provenance and sha256):
#   $DATA/auditing-the-audits-facct-2025/   ACLU repository clone (commit cef7c273...)
#   $DATA/osf/impact.csv, $DATA/osf/employer_docs.zip   OSF osf.io/upfdk extraction of 2026-10-03
# Row-level derived files are written to $DATA/derived_private/ (never to the repository).
set -euo pipefail

SCRATCH="${SCRATCH:-/tmp/claude-0/-home-user-employee-monitoring-system/c64eab22-9c10-592c-b92e-5ac629c5be82/scratchpad}"
PY="${PY:-$SCRATCH/venv/bin/python}"
DATA="${DATA:-$SCRATCH/data/idea04}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="$HERE/../results"
PRIV="$DATA/derived_private"
mkdir -p "$OUT" "$PRIV"

# Stage the OSF files in their own directory (copy from the 2026-10-03 cache if absent).
if [ ! -f "$DATA/osf/impact.csv" ]; then
  mkdir -p "$DATA/osf"
  cp "$SCRATCH/ideas/employer_docs.zip" "$SCRATCH/ideas/impact.csv" "$DATA/osf/"
fi
if [ ! -d "$DATA/osf/extracted/Employer Documents" ]; then
  mkdir -p "$DATA/osf/extracted"
  unzip -q -o "$DATA/osf/employer_docs.zip" -d "$DATA/osf/extracted"
fi

# Never run the interpreter with the data directory as working directory.
cd "$HERE"
START=$(date +%s)

# Stopping-rule criterion 1: keyword scan of the ACLU code (manual reading is in the README).
"$PY" -I "$HERE/check_aclu_code.py" \
  --code-dir "$DATA/auditing-the-audits-facct-2025/code" \
  --out "$OUT/aclu_code_inference_check.csv"

# Pilot: profile, de-duplicate, filter, intervals, tabulations, excluded shares, OSF check, stop rule.
"$PY" -I "$HERE/ll144_pilot.py" \
  --aclu-csv "$DATA/auditing-the-audits-facct-2025/audits/audits_full.csv" \
  --osf-csv "$DATA/osf/impact.csv" \
  --osf-pdf-dir "$DATA/osf/extracted/Employer Documents" \
  --out-dir "$OUT" \
  --private-dir "$PRIV"

echo "wall-clock seconds: $(( $(date +%s) - START ))"
