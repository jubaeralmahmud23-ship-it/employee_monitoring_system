# Claim survival under the uncertainty models (exploratory)

Generated from `claim_survival.csv` (`code/uncertainty_calc.py`, seed 20261015, 20,000 Beta draws). A claim survives when the model's 95% interval for the difference excludes 0. M2 paired: 'all' = survives at the unpaired SE (upper bound if item-level errors are not negatively correlated), 'some' = only at smaller SEs, 'none' = not even at the minimal-discordance SE.

| Claim | Paper | Role | Metric | A vs B (%) | diff (pp) | n (source) | M1 Wald | M1 Newcombe | M2 paired | M2 cluster ICC 0.1 / 0.3 | M3 band (|diff| > 15 pp) | M3 sd 3.75 pp | M4 Beta |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C01 | A02 | H1 (rule claim) | AIME2024 accuracy | 16.7 vs 6.7 | 10.0 | 30 (derived (benchmark size; not stated in paper)) | no [-6.07, 26.07] | no | none | NA / NA | no | no | no [-7.23, 26.74] |
| C02 | A02 | alternative cell | MATH-500 accuracy | 70.0 vs 62.6 | 7.4 | 500 (paper (§4.1 p.4)) | yes [1.56, 13.24] | yes | all | NA / NA | no | no | yes [1.54, 13.18] |
| C03 | A03 | H1 (rule claim) | HIT@5 (shipbuilding) | 96.0 vs 95.9 | 0.1 | 2932 (paper (§4.1 p.4)) | no [-0.91, 1.11] | no | none | NA / NA | no | no | no [-0.92, 1.12] |
| C04 | A03 | alternative cell | HIT@5 (shipbuilding) | 96.0 vs 87.7 | 8.3 | 2932 (paper (§4.1 p.4)) | yes [6.92, 9.68] | yes | all | NA / NA | no | no | yes [6.93, 9.72] |
| C05 | A04 | H1 (rule claim) | macro success rate VestaBench-VH | 47.0 vs 42.0 | 5.0 | 100 (paper (p.1-2; App. B.2 p.9)) | no [-8.76, 18.76] | no | some | NA / NA | no | no | no [-8.67, 18.30] |
| C06 | A07 | alternative cell | share of conversations with >=1 excellent response | 66.67 vs 43.33 | 23.34 | 30 (paper (§5 p.4)) | no [-1.13, 47.81] | no | some | NA / NA | yes | no | no [-2.43, 44.81] |
| C07 | A08 | alternative cell (Small variant assumed) | page-level accuracy DocSplit-Mono-Seq | 84.18 vs 82.39 | 1.79 | 6655 (assumed (500 packets x 13.31 pages; variant not stated)) | yes [0.52, 3.06] | yes | all | no / no | no | no | yes [0.53, 3.06] |
| C08 | A08 | alternative cell (Large variant assumed) | page-level accuracy DocSplit-Mono-Seq | 84.18 vs 82.39 | 1.79 | 5599 (assumed (102 packets x 54.89 pages; variant not stated)) | yes [0.41, 3.17] | yes | all | no / no | no | no | yes [0.40, 3.17] |
| C09 | A09 | H1 (rule claim) | AIME-2025 exact-match accuracy | 53.3 vs 40.0 | 13.3 | 30 (derived (benchmark size; not stated in paper)) | no [-11.72, 38.32] | no | some | NA / NA | no | no | no [-11.75, 35.93] |
| C10 | A10 | H1 (rule claim) | OCR-VQA test accuracy | 74.0 vs 71.5 | 2.5 | 100400 (paper (Table 7 p.11; 100.4K rounded)) | yes [2.11, 2.89] | yes | all | yes / yes | no | no | yes [2.11, 2.90] |

Rule-based headline claims (H1) run: 5; surviving M1 Wald: 1; M2 paired 'all': 1; M3 band: 0; M3 sd: 0; M4 Beta: 1.
