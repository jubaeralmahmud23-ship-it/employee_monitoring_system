#!/usr/bin/env bash
# Stage 4 pilot, idea 6 (error-bar audit of LLM evaluations). Exploratory.
#
# Default (FETCH=0): reproduces every derived file under ../results/pilot/ from the frozen
# frame snapshot in ../results/frame/ and the coder's inputs in ./coding/ (no network).
#
# FETCH=1 additionally (network needed):
#   1. re-enumerates the frame from Crossref and the ACL Anthology (build_frame.py). The
#      Crossref query carries until-pub-date = the frozen sampling date, but Crossref
#      metadata keep changing (late deposits, added abstracts), so a re-run can differ
#      from the 2026-10-19 snapshot. It overwrites ../results/frame/.
#   2. re-downloads the 20 pilot PDFs and 65 Springer landing pages (fetch_fulltexts.py)
#      into $DATA (git-ignored, outside the repository; cached files are reused).
#
# Downloads are untrusted data: they are only read by the scripts, which take paths as
# arguments; the interpreter never runs with the data directory as working directory.
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

SCRATCH="${SCRATCH:-/tmp/claude-0/-home-user-employee-monitoring-system/c64eab22-9c10-592c-b92e-5ac629c5be82/scratchpad}"
PY="${PY:-$SCRATCH/venv/bin/python}"
DATA="${DATA:-$SCRATCH/data/idea06}"
FETCH="${FETCH:-0}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_RESEARCH="$(cd "$HERE/../../.." && pwd)"
FRAME="$HERE/../results/frame"
PILOT="$HERE/../results/pilot"
mkdir -p "$FRAME" "$PILOT"
cd "$HERE"
START=$(date +%s)

if [ "$FETCH" = "1" ]; then
  RAW="$DATA/frame_raw_$(date -u +%Y%m%dT%H%M%SZ)"
  "$PY" -I "$HERE/build_frame.py" --out-dir "$FRAME" --raw-dir "$RAW" \
    --freeze-date 2026-10-19 --from-date 2023-01-01 \
    --baseline-json "$REPO_RESEARCH/tools/assessment_2026-10-05/idea06/crossref_counts.json" \
    --compare-unbounded
fi

# Seeded draw of the 20 pilot papers (seed 20261015) from the frozen frame.
"$PY" -I "$HERE/draw_pilot.py" --springer-oa "$FRAME/springer_oa_term_hits.csv" \
  --acl "$FRAME/acl_industry_papers.csv" --seed 20261015 --out "$PILOT/pilot_sample.csv"

if [ "$FETCH" = "1" ]; then
  "$PY" -I "$HERE/fetch_fulltexts.py" --pilot-csv "$PILOT/pilot_sample.csv" \
    --springer-oa-csv "$FRAME/springer_oa_term_hits.csv" \
    --papers-root "$DATA/papers" --landing-root "$DATA/springer_landing" \
    --manifest-out "$PILOT/fulltext_manifest.csv" \
    --abstracts-out "$DATA/springer_oa_abstracts.csv" \
    --landing-manifest-out "$FRAME/springer_oa_landing_manifest.csv"
fi

# Calculator: self-test, validation against statsmodels/numpy, then the pilot claims.
"$PY" -I "$HERE/uncertainty_calc.py" --selftest
"$PY" -I -B "$HERE/validate_calc.py" --calc "$HERE/uncertainty_calc.py" --out "$PILOT/calc_validation.csv"
"$PY" -I "$HERE/uncertainty_calc.py" --claims "$HERE/coding/pilot_claims.csv" \
  --out "$PILOT/claim_survival.csv" --seed 20261015 --draws 20000 --band-pp 15

# Compile coded table, timing, item prevalence, screening counts and the stopping rule.
"$PY" -I "$HERE/analyze_pilot.py" --coding-dir "$HERE/coding/papers" \
  --sample "$PILOT/pilot_sample.csv" --timing "$HERE/coding/coding_times.log" \
  --screening "$HERE/coding/springer_oa_screening.csv" \
  --survival "$PILOT/claim_survival.csv" --frame-summary "$FRAME/frame_summary.json" \
  --out-dir "$PILOT" > /dev/null


# Reproducibility metadata (versions, seeds, timings, sha256 of inputs and outputs).
"$PY" -I "$HERE/write_run_metadata.py" --idea-dir "$HERE/.." --data-dir "$DATA" --out "$HERE/../results/run_metadata.json"

echo "wall-clock seconds: $(( $(date +%s) - START ))"
