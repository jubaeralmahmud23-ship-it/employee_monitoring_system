#!/usr/bin/env bash
# Reproduce the idea-05 Stage 4 pilot from the data directory.
#
# Usage:
#   PY=/path/to/venv/bin/python bash run.sh <data_dir> [n_jobs] [bootstrap_B] [placebo_shuffles]
#
# <data_dir> must contain (download commands and checksums below):
#   bpic2017/bpic2017.xes.gz            4TU DOI 10.4121/uuid:5f3067df-f10b-45da-b98b-86ae4c7a310b
#   bpic2019/BPI_Challenge_2019.xes     4TU DOI 10.4121/uuid:d06aff4b-79f0-45e6-8ec8-e19730c248f1
# Derived per-resource files go to <data_dir>/derived (untracked); aggregate results to ../results
# (or to $RESULTS_DIR if set).
# Every interpreter call runs with -I from / (never from the data directory).
set -euo pipefail
DATA=$(cd "${1:?usage: run.sh <data_dir> [n_jobs] [B] [shuffles]}" && pwd)
JOBS=${2:-4}
B=${3:-500}
SH=${4:-20}
PY=${PY:-python3}
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
RES=${RESULTS_DIR:-$(cd "$HERE/.." && pwd)/results}   # override with RESULTS_DIR for test runs
DER=$DATA/derived
mkdir -p "$RES" "$DER"
cd /

# --- optional download (uncomment if the raw files are absent) ---
# curl -L --retry 3 --retry-delay 10 -o "$DATA/bpic2017/bpic2017.xes.gz" \
#   "https://data.4tu.nl/file/34c3f44b-3101-4ea9-8281-e38905c68b8d/f3aec4f7-d52c-4217-82f4-57d719a8298c"
# curl -L --retry 3 --retry-delay 10 -o "$DATA/bpic2019/BPI_Challenge_2019.xes" \
#   "https://data.4tu.nl/file/35ed7122-966a-484e-a0e1-749b64e3366d/864493d1-3a58-47f6-ad6f-27f95f995828"

echo "checking sha256 of raw logs"
echo "183c5e5189282779c811c78c33ff936351b3dd201165d612211fc220936f8249  $DATA/bpic2017/bpic2017.xes.gz" | sha256sum -c -
echo "af63bc687fc4152f2123b05c3af7772b37ef3fce2d3f67f812666c9e356baae7  $DATA/bpic2019/BPI_Challenge_2019.xes" | sha256sum -c -

t() { echo "[$(date -u +%FT%TZ)] $*"; }

t "01 convert XES -> Parquet (pm4py.read_xes)"
[ -f "$DATA/bpic2017/bpic2017.parquet" ] || "$PY" -I "$HERE/01_convert_to_parquet.py" "$DATA/bpic2017/bpic2017.xes.gz" "$DATA/bpic2017/bpic2017.parquet" "$RES/provenance_bpic2017_parquet.json"
[ -f "$DATA/bpic2019/bpic2019.parquet" ] || "$PY" -I "$HERE/01_convert_to_parquet.py" "$DATA/bpic2019/BPI_Challenge_2019.xes" "$DATA/bpic2019/bpic2019.parquet" "$RES/provenance_bpic2019_parquet.json"

t "02 resource fields"
"$PY" -I "$HERE/02_resource_fields.py" "$DATA/bpic2017/bpic2017.parquet" "$DATA/bpic2019/bpic2019.parquet" "$RES"

t "03 automated-account detector (calibrate on BPI 2019, apply to BPI 2017)"
"$PY" -I "$HERE/03_detector.py" "$DATA/bpic2017/bpic2017.parquet" "$DATA/bpic2019/bpic2019.parquet" "$RES" "$DER"

for LOG in bpic2017 bpic2019; do
  t "04 factorial point estimates: $LOG"
  "$PY" -I "$HERE/04_factorial.py" "$LOG" "$DATA/$LOG/$LOG.parquet" "$DER/exclusions.json" "$RES" "$DER"
done
for LOG in bpic2017 bpic2019; do
  t "05 case bootstrap ($B replicates): $LOG"
  "$PY" -I "$HERE/05_bootstrap.py" "$LOG" "$DATA/$LOG/$LOG.parquet" "$DER/exclusions.json" "$RES" "$B" "$JOBS"
done
for LOG in bpic2017 bpic2019; do
  t "06 placebo shuffles ($SH): $LOG"
  "$PY" -I "$HERE/06_placebo.py" "$LOG" "$DATA/$LOG/$LOG.parquet" "$DER/exclusions.json" "$RES" "$SH" "$JOBS"
done

t "07 stopping rule, summary, figures"
"$PY" -I "$HERE/07_report.py" "$RES" "$DER"
t "done"
