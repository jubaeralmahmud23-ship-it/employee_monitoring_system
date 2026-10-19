#!/usr/bin/env bash
# Idea 5, Stage 4 deep novelty check (2026-10-19): the commands as run, in order.
# Downloads go to the scratchpad (untrusted data, git-ignored); derived CSVs to results/novelty/.
# Scripts are run with the isolated venv interpreter (-I); no script is run from a data directory.
set -euo pipefail
PY=/tmp/claude-0/-home-user-employee-monitoring-system/c64eab22-9c10-592c-b92e-5ac629c5be82/scratchpad/venv/bin/python
D=/tmp/claude-0/-home-user-employee-monitoring-system/c64eab22-9c10-592c-b92e-5ac629c5be82/scratchpad/data/idea05_novelty
C=/home/user/employee_monitoring_system/research/06_stage4/idea05/code/novelty
R=/home/user/employee_monitoring_system/research/06_stage4/idea05/results/novelty
mkdir -p "$D" "$R"

# 1. Full texts named by the plan (open copies only) + Crossref records
mkdir -p "$D/fulltexts"
$PY -I $C/fetch_fulltexts.py "$D/fulltexts" "$R"
#    Adams et al. NEJM retry (first fetch returned a reCAPTCHA page), then HTML -> text:
#    curl -A "idea05-novelty-check/1.0 (academic use; contact via repository owner)" \
#         -o $D/fulltexts/adams2010_nejm_pmc_retry/source.html https://pmc.ncbi.nlm.nih.gov/articles/PMC2878194/
$PY -I $C/html2text.py "$D/fulltexts/adams2010_nejm_pmc_retry/source.html" "$D/fulltexts/adams2010_nejm_pmc_retry/text.txt"
$PY -I $C/decode_shifted_font.py "$D/fulltexts/kelemen2022_oa/text.txt" "$D/fulltexts/kelemen2022_oa/text_decoded.txt"
#    4TU terms: file listed by https://data.4tu.nl/v2/articles/12721292/files, fetched with curl, pdftotext -layout
#    arXiv 2507.23037 (Leribaux et al.): curl https://arxiv.org/pdf/2507.23037 ; pdftotext -layout
#    page-referenced keyword search in any pdftotext output:
#    $PY -I $C/kwic.py <text.txt> <regex>

# 2. Citation chasing (OpenAlex lists refused: daily budget exhausted; S2 and Crossref used)
mkdir -p "$D/chase"
$PY -I $C/chase_citations.py "$D/chase" "$R"
$PY -I $C/screen_chase.py "$D/chase/abstracts.jsonl" "$R"

# 3a. Proceedings sweep (ICPM, BPM, CAiSE, Process Science 2022-2026) via Crossref
mkdir -p "$D/sweep"
$PY -I $C/proceedings_sweep.py "$D/sweep" "$R"
$PY -I $C/fetch_abstracts.py "$R/read_list_dois.txt" "$D/abstracts/pages" "$D/abstracts/abstracts.jsonl"

# 3b. BPI Challenge 2017 and 2019 reports (listing pages saved first with curl:
#     https://ais.win.tue.nl/bpi/2017/challenge.html and https://icpmconference.org/2019/bpi-challenge/)
mkdir -p "$D/bpic_reports"
$PY -I $C/bpic_reports.py "$D/bpic_pages/38c1fc99.html" "$D/bpic_pages/c838fc9e.html" "$D/bpic_reports" "$R"

# 3c. ICIS future-of-work track listings 2022-2025 (AIS eLibrary browse pages)
mkdir -p "$D/aisel/tracks"
$PY -I $C/icis_fow_tracks.py "$D/aisel/tracks" "$R"

# 3d. arXiv API topic queries
mkdir -p "$D/arxiv"
$PY -I $C/arxiv_queries.py "$D/arxiv" "$R"
