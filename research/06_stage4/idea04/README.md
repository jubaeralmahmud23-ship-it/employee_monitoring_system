# Stage 4 pilot, idea 4: sampling uncertainty of NYC Local Law 144 impact ratios

**Status: EXPLORATORY PILOT, run 2026-10-19 in the cloud container (4 vCPU, 15 GB RAM, Python 3.11).** Not preregistered, not peer reviewed. All numbers below come from files produced in this run (paths given) or from documents read in this run (paths or URLs given). Part 2 (simulation) and Part 3 (reporting designs, manipulation range) of the idea were **not run**. The literature stop condition of section 4.3 is handled by another agent and is not assessed here.

Plan followed: `research/02_candidate_ideas.md`, Idea 4 card (section 2) and section 4.3; context from `research/03_challenge/04-published-but-uninformative-sampling-uncertainty__feasibility.md` and `__novelty.md` (all read in this run).

## 1. Stopping rule, criterion by criterion

Rule as written in `02_candidate_ideas.md` section 4.3: *"stop Part 1 if the ACLU code already computes sampling intervals or if, after de-duplication, more than about 80% of employer-level ratios have 95% intervals excluding 0.8"*. The rule and threshold were not altered.

| Criterion | What was computed | Value | Threshold | Outcome |
|---|---|---|---|---|
| C1. ACLU code already computes sampling intervals | Manual reading of all three code files plus a keyword scan (`results/aclu_code_inference_check.csv`) | **No.** The code computes deterministic missing-data bounds and point-estimate shares only; no interval, standard error, simulation, random number generation or significance test (details in section 3) | any | **Not triggered** |
| C2. Share of employer-level ratios, after de-duplication, whose 95% interval excludes 0.8 | Pre-specified primary: set E1 (employer-posted audits), Katz log-ratio 95% interval (`results/run_metadata.json`, `results/stopping_rule_criterion2_all_variants.csv`) | **59.8%** (511 of 854 ratios) | > about 80% | **Not triggered** |
| C2, other interval methods on E1 | Clopper-Pearson with Bonferroni split / stratified bootstrap / Jeffreys posterior | 45.0% / 58.8% / 58.9% | > about 80% | Not triggered |
| C2, post-hoc evidence-based reading of "employer-level" (E5: audits whose report states that the employer's own applicant data were used; section 5.6) | Katz | **55.2%** (95 of 172) | > about 80% | Not triggered |
| C2, all employer-level variants x all four methods (E1-E5, S1-S6) | range | 42.8% to 83.3% | > about 80% | Only S6 (the 108 employer-posted ratios whose counts are integers as recorded) exceeds 80% with Katz (83.3%), bootstrap (82.4%) and Jeffreys (81.5%); not with Clopper-Pearson (77.8%) |

**Part 1 outcome: not stopped.** Neither criterion is triggered under the pre-specified operationalisation, nor under the post-hoc evidence-based one. The single subset above 80% (S6) is a robustness subset defined by a data-quality attribute, not the rule's population. The vendor-posted audits (not part of the rule) are precise: 89.1% of their ratios have Katz intervals excluding 0.8 (`results/interval_summary_variants.csv`, set V).

What the pilot adds to the decision (not part of the rule): the employer-level share sits near 55-60% because the corpus is bimodal. Among employer-own-data ratios (E5), 4.7% of comparisons where the smaller group has fewer than 100 applicants exclude 0.8. The figure is 91.7% at 1,000-4,999 and 100% at 5,000 or more (`results/interval_by_group_size.csv`). Three of the seven employer-own-data employers (Burlington's two role-specific audits, Hartford, Wells Fargo) have no ratio whose interval excludes 0.8, while Morgan Stanley, NYU Langone and Bloomberg are mostly precise (`results/interval_E5_by_auditor_and_employer.csv`).

## 2. Inputs, provenance, checksums, licence terms as read

| Input | Location (git-ignored, outside the repository) | Provenance | sha256 |
|---|---|---|---|
| ACLU "Auditing the Audits" repository (Gerchick et al., FAccT 2025) | `$SCRATCH/data/idea04/auditing-the-audits-facct-2025/` | Clone of github.com/aclu-national/auditing-the-audits-facct-2025, commit `cef7c27398dc73852f06f20120500d361abbd37e` (2025-05-09) | `audits/audits_full.csv`: `69fd290fb0be9523254027e3508722e70501f8501a9a3d92f47f7ffd31bbf85e` (2,320,698 bytes); `README.md`: `6c93611a...d755d0`; `data_schema.md`: `cd49a08d...0327d4`; code file hashes in `results/aclu_code_inference_check.csv` |
| ACLU tracker | `$SCRATCH/data/idea04/tracking-ll144-bias-audits/` | Clone of github.com/aclu-national/tracking-ll144-bias-audits, commit `5fca36bbd3dd289e62cd965b3ff2789424573bbf` (2026-09-23) | `all_bias_audits.csv`: `1e9932c6f94ddfee68ca8bdf155dbb46ef53de3a829f0a8285b6aeb34bd54b07` |
| OSF osf.io/upfdk extraction (Wright et al., FAccT 2024), cached 2026-10-03 | copied to `$SCRATCH/data/idea04/osf/`; zip extracted to `osf/extracted/` only | `impact.csv` = OSF `2024-01-16-bias-audit-impact-scores.csv` (449 rows); `employer_docs.zip` = OSF `Employer Documents.zip` (80 PDFs, 36 PNGs, 22 `__MACOSX` metadata files, 21 employer folders) | `impact.csv`: `b54629ca7f0c14053720ebb69d5b28317dec6cb8c7d1137418e603ef9508b846`; zip: `99c49bd851ee0f7bfe2320c5cf627174c986a832c0d6de3926377a5a504d0d26`; the six PDFs used are hashed in `results/run_metadata.json` |
| UGESP 29 CFR 1607.4 (CFR 2023 edition) | `$SCRATCH/data/idea04/ugesp/CFR-2023-title29-vol4-sec1607-4.xml` | https://www.govinfo.gov/content/pkg/CFR-2023-title29-vol4/xml/CFR-2023-title29-vol4-sec1607-4.xml (fetched 2026-10-19; the eCFR API answered HTTP 406) | `247712a121932ed761042994147966429c0e7fc2071a084db3701e07c28e5d07` |
| DCI/HireVue reports fetched to classify data scope | `$SCRATCH/data/idea04/dci_reports/` | Original links listed in the ACLU tracker README: Burlington `AI audit for EC.pdf`, `NYC Audit AA.pdf`, `NYC Audit Intern.pdf` (dn9tckvz2rpxv.cloudfront.net), `Burlington DCI Audit Results (002).pdf` (seo.nlx.org), Citizens summary page (jobs.citizensbank.com, HTTP 200), JetBlue page (HTTP 404) | EC `704c0a30...`, AA `b3922da0...`, Intern `4bc0e0bb...`, 2024 `e150a250...`, Citizens HTML `aee11241...`, JetBlue 404 page `01f68c9e...` |

**Licence terms as read.** Neither ACLU repository contains a LICENSE file (`git ls-files` lists none). Both READMEs end with the same sentence: *"The tracker in this repository is licensed under CC BY-NC 4.0"* (FAccT repository `README.md` line 50; tracker `README.md` line 118). In the FAccT repository the sentence refers to "the tracker", which that repository does not contain. Whether CC BY-NC 4.0 covers `audits_full.csv` is therefore **ambiguous**. The OSF project is CC BY 4.0 (per the feasibility file, read in this run; not re-checked against the OSF API today).

**Author action flagged (not done by this agent):** the plan's licence email to the ACLU analytics contact (analytics_inquiry@aclu.org, given in both READMEs) asking whether `audits_full.csv` may be reused and whether derived tables may be published under CC BY-NC 4.0 or another licence. Until then this pilot redistributes no raw data. `results/` holds aggregated statistics only. Row-level derived files (per-ratio intervals, the 20-row cross-check detail, per-table excluded shares) are in `$SCRATCH/data/idea04/derived_private/` and are not in the repository.

`$SCRATCH` = `/tmp/claude-0/-home-user-employee-monitoring-system/c64eab22-9c10-592c-b92e-5ac629c5be82/scratchpad`.

## 3. Criterion 1: what the ACLU code computes (manual reading, with line references)

Files read in full: `code/helpers.R` (184 lines by `wc -l`), `code/paper_results.Rmd` (853), `code/extraction_template.Rmd` (169).

- `helpers.R` lines 13-34 (`extract_tables_from_audit`): PDF table extraction with tabulizer/tabulapdf.
- `helpers.R` lines 37-129 (`calc_audit_bounds`): **deterministic missing-data bounds**.
  - Lines 110-118: worst-case bounds that assign all `n_miss` unknown applicants to the row's group, all selected or all not selected.
  - Lines 120-123: bounds that allocate unknowns in proportion to the observed demographic shares.
  - Both are divided by `comparator_result` (line 101-106: the reported maximum rate, or a flagged comparator). No sampling distribution is involved.
- `helpers.R` lines 131-185: string utilities (`case_regex`, `glue_here`, `source_rmd`).
- `paper_results.Rmd` lines 47-141: counts of reports, audits, vendors, auditors and data types.
  - Lines 159-196: replaces missing impact ratios by `impact_calc` and computes the shares of audits and results with a point ratio below 0.8 or above 1.
  - Lines 198-285: comparator and group tabulations.
  - Lines 320-409: metadata and demographic missingness.
  - Lines 411-438: keeps one rate definition per audit ("Selection, top"; "Selection" for Dover).
  - Lines 475-486: `mean(impact_ratio_lower_bound < 0.8)` under the two missing-data assumptions (the paper's 70% and 28% figures, per the novelty file).
  - Lines 493-850: plots of those bounds.
- `extraction_template.Rmd`: per-audit extraction template only.
- Keyword scan (`code/check_aclu_code.py`; families: binomial/Clopper-Pearson/Wilson/Jeffreys, prop.test/chi-square/Fisher/z-test, bootstrap/resampling, rbinom/rnorm/runif/set.seed/simulation, qnorm/pnorm/qbeta, standard error/sd/var, confint/interval, p-value/significance, Bayes/posterior/prior): **one hit in total**, `paper_results.Rmd` line 2, the word "Replication" in the document title (false positive). Zero hits in `helpers.R` and `extraction_template.Rmd`.

Conclusion: the ACLU code attaches missing-data bounds, not sampling intervals. It runs no simulation and no significance test. Criterion 1 is not triggered.

## 4. Methods (as run)

All code is in `code/`, run by `code/run.sh` with the venv interpreter in isolated mode (`python -I`), from the code directory, with data paths as arguments.

1. **Corpus profile.** `audits_full.csv` has **4,507 rows and 46 columns**, covering 116 audits (`audit_id`) in 44 audit reports (`audit_report_id`). Column names with non-missing counts, unique counts and numeric ranges are in `results/aclu_columns_profile.csv`. The schema columns are documented in `data_schema.md`; the file also carries the ACLU team's derived columns (`result_calc`, `impact_calc`, `comparator_group`, `n_miss`, and the bound columns `impact_ratio_lower_bound` etc.).
2. **Exclusions following Gerchick et al.'s code.**
   - HackerRank rows are dropped, because "selection" is a negative outcome there (`paper_results.Rmd` lines 160-161).
   - One rate definition is kept per audit: "Selection, top" where both tier thresholds exist, and "Selection" for Dover (lines 162-163, 411-438). All rate definitions are kept in sensitivity sets S5 and S7.
3. **Result tables and de-duplication.**
   - A table is audit x rate definition x protected characteristic (sex, race/ethnicity, intersectional).
   - *Primary rule:* a table is a duplicate when an earlier table (sorted by table id) has identical counts, i.e. the same set of (group, N, selected count) over known groups with N > 0, and at least two such groups.
   - This operationalises the plan's key (auditor, tool, data window): identical counts confirm that two tables come from the same data, whereas the key alone is ambiguous (see deviations).
   - *Sensitivity S2:* the literal key (auditor, vendor, tool, known start and end date, rate definition, characteristic), keeping the first table per key regardless of counts.
   - *Sensitivity S1:* no de-duplication.
4. **Consistency filter.** For each known group with N > 0 and a selected count n, the absolute difference |n/N - reported rate| is compared with a tolerance.
   - Tolerance = 0.5 x 10^-d (+1e-9), where d is the number of decimals of the reported rate. d is floored at the table's modal decimals (this restores dropped trailing zeros) and capped at 6.
   - Rows within 2 x tolerance pass only in the lenient variant S3. Rows with n > N fail.
   - Rows with N and n but no reported rate are kept, flagged "rate not reported".
5. **Comparator recomputation and the 2% rule.**
   - Within each table, the comparator is the highest-rate group among usable groups holding at least 2% of the known applicants with reported N, following the LL 144 definition "most selected category" and rule 5-301(d) as quoted in the feasibility file. Ties go to the larger N.
   - Each other usable group of 2% or more gives one ratio. The comparator itself (ratio 1 by construction) is not counted.
   - Ratios for sub-2% groups against the same comparator form sensitivity S4.
   - Selected counts are rounded to integers for all binomial methods.
6. **Intervals and tests for every usable ratio** (`compute_stats` in `code/ll144_pilot.py`):
   - (a) **Katz log-ratio** 95%: log(RR) +/- 1.96 x sqrt(1/n_g - 1/N_g + 1/n_c - 1/N_c); 0.5 is added to every cell when a selected count is 0. *Designated primary for the stopping rule before any result was computed* (constant `PRIMARY_METHOD`).
   - (b) **Clopper-Pearson-Bonferroni**: exact 97.5% Clopper-Pearson intervals for each rate, combined as [L_g/U_c, U_g/L_c]. This is the "exact" option: simultaneous coverage of at least 95% by construction, conservative.
   - (c) **Stratified bootstrap**: binomial resampling of each group at its observed rate, which is equivalent to resampling applicants within the two groups. Comparator group held fixed; **seed 20261015, 2,000 resamples**; percentile interval (inverted-CDF quantiles). Resamples with 0/0 are dropped (79 of about 5.3 million, `results/run_metadata.json`).
   - (d) **Jeffreys posterior**: independent Beta(0.5, 0.5) priors on both rates, 20,000 Monte Carlo draws per ratio (seed [20261015, 1]). Gives an equal-tailed 95% credible interval, P(ratio < 0.8) and P(ratio < 1).
   - (e) **UGESP four-fifths flag** (point ratio < 0.8; 29 CFR 1607.4(D), read in this run).
   - (f) **"Two standard deviations" test**: pooled two-proportion z, |z| > 1.96. The UGESP text read in this run speaks of differences "significant in both statistical and practical terms" and does not itself define a two-standard-deviation rule; the 2-SD operationalisation is a convention, implemented as stated.
   - (g) **Fisher's exact test** (two-sided, scipy).
   - An interval "excludes" t when lower > t or upper < t, for t = 0.8 and t = 1.0.
7. **Scope sets.**
   - *Pre-specified:* E1 employer-posted (deploying entity is not the tool vendor; one alias, Staya Inc. = Dover, from the tracker README), E2 = E1 with historical data, E3 = E2 minus tables posted verbatim by two or more entities, V vendor-posted, ALL.
   - *Post hoc* (section 5.6): E4 = E1 minus multi-employer pooled audits; E5 = audits whose report states (or, for Morgan Stanley 2024, implies) the employer's own applicant data, plus Cigna (not verifiable); E5b = E5 without Cigna; M = multi-employer pooled.
   - The per-audit coding, with a quote and source for each decision, is `code/data_scope_coding.csv`; its application is `results/data_scope_coding_applied.csv`.
8. **Excluded populations**, per kept table (primary rate definition):
   - unknown share = N_unknown / (N_known + N_unknown), where the Missing/Unknown row carries a count (the ACLU schema uses 0 for "none or test data" and NA for "not specified");
   - sub-2% share = applicants in known groups below 2% of the known total, divided by the known total;
   - total excluded share = (N_unknown + N_sub-2%) / (N_known + N_unknown).
9. **OSF cross-check.**
   - *Pool:* the six employers present in both corpora under the same deploying entity (Bloomberg, BNP Paribas, Cigna, Morgan Stanley, NBCUniversal, Pfizer), fixed before sampling. 134 OSF rows, each with exactly one ACLU match (2023, sex or race table, same group; Pfizer also matched by assessment name).
   - *Sample:* 20 rows (pandas `sample`, seed 20261015).
   - *Comparison:* reported impact ratios at the common precision (the OSF CSV has no counts), plus a search for the ACLU N in the `pdftotext -layout` text of the employer PDF in the OSF zip. A row is "not checkable" when N is 0 or the PDF text layer has fewer than 1,000 characters.
10. **Validation** (`code/validate_methods.py`, `results/method_validation.csv`):
    - Katz bounds equal `scipy.stats.contingency.relative_risk(...).confidence_interval` (max abs difference 0 to 2e-15 on five count pairs).
    - Clopper-Pearson-Bonferroni lower bounds equal ratios of `scipy.stats.binomtest(...).proportion_ci(method='exact')` bounds (max 1.9e-13).
    - Monte Carlo coverage at a true ratio of exactly 0.8 (5 settings, N_g from 10 to 5,000, 1,000 replicates each, data seed 20261016): Katz 0.945-0.956, Clopper-Pearson-Bonferroni 0.996-1.000, bootstrap 0.914-0.957 (under-covers at N_g = 10), Jeffreys 0.937-0.957.
    - One ratio was also checked by hand against the pipeline output (agreement to 6 decimals).

## 5. Results

### 5.1 Pipeline counts (`results/pipeline_funnel.csv`)

| Step | Count |
|---|---|
| Rows / audits / reports | 4,507 / 116 / 44 |
| Rows after excluding HackerRank | 4,406 |
| Result tables, all rate definitions | 527 |
| Tables after HackerRank exclusion, primary rate definition | 332 |
| Dropped as identical-count duplicates (of which also share the plan key) | 49 (35) |
| Kept | 283 |
| Tables the literal plan key would drop instead | 87 |
| Known-group rows in kept tables / with N reported / N > 0 / with selected count | 2,142 / 2,104 / 1,803 / 1,780 |
| Passing the strict consistency filter (incl. 5 with no reported rate) / failing | 1,765 / 15 |
| **Usable ratios, all scopes** (2% or more, non-comparator) | **1,157** (in 277 tables, 96 audits, 39 reports) |
| **Usable employer-posted ratios (E1)** / vendor-posted | **854** / 303 |
| Employer-posted sub-2% ratios (S4 only) | 208 |

De-duplication by auditor and vendor (`results/dedup_summary.csv`):
- 45 of 201 DCI/HireVue tables, 3 ZoomInfo tables (identical counts to Bryq's 2023 vendor audit by Holistic AI) and 1 Alidoro/Landed table are identical-count duplicates.
- 72 DCI/HireVue tables carry counts that appear verbatim in reports of two or more deploying entities.
- The literal plan key would instead drop 84 DCI/HireVue tables and 3 Hartford/Wells Fargo-group tables, some with different counts.

### 5.2 Main shares (`results/interval_summary_variants.csv`)

Share of ratios whose 95% interval excludes 0.8 (Katz / Clopper-Pearson-Bonferroni / bootstrap / Jeffreys), share excluding 1.0 (Katz), share with a point ratio below 0.8, and median N of the focal group.

| Set | Ratios (reports) | Median N_g | Excl. 0.8: Katz / CP-B / boot / Jeffreys | Excl. 1.0 (Katz) | Point < 0.8 | Katz upper < 0.8 |
|---|---|---|---|---|---|---|
| **E1 employer-posted (primary)** | 854 (19) | 2,565.5 | **0.598** / 0.450 / 0.588 / 0.589 | 0.660 | 0.232 | 0.078 |
| E2 E1 historical | 821 (17) | 2,699 | 0.591 / 0.441 / 0.582 / 0.583 | 0.680 | 0.240 | 0.082 |
| E3 E2 not shared | 710 (17) | 2,578 | 0.592 / 0.437 / 0.582 / 0.582 | 0.669 | 0.237 | 0.080 |
| E4 post hoc | 192 (9) | 2,500 | 0.599 / 0.562 / 0.594 / 0.589 | 0.531 | 0.188 | 0.000 |
| **E5 employer own data, post hoc** | 172 (8) | 1,905 | **0.552** / 0.512 / 0.547 / 0.541 | 0.593 | 0.209 | 0.000 |
| E5b E5 without Cigna | 159 (7) | 2,574 | 0.560 / 0.541 / 0.566 / 0.560 | 0.604 | 0.220 | 0.000 |
| M multi-employer pooled, post hoc | 662 (11) | 2,725.5 | 0.598 / 0.417 / 0.586 / 0.589 | 0.698 | 0.245 | 0.101 |
| V vendor-posted | 303 (20) | 54,879 | 0.891 / 0.838 / 0.894 / 0.891 | 0.693 | 0.046 | 0.013 |
| ALL de-duplicated | 1,157 (39) | 3,795 | 0.675 / 0.551 / 0.668 / 0.668 | 0.669 | 0.183 | 0.061 |
| S1 E1 without de-duplication | 1,034 (19) | 2,712 | 0.623 / 0.479 / 0.616 / 0.617 | 0.667 | 0.221 | 0.075 |
| S2 E1 literal plan key | 675 (17) | 2,500 | 0.601 / 0.462 / 0.594 / 0.596 | 0.665 | 0.240 | 0.083 |
| S3 E1 lenient consistency | 856 (19) | 2,578 | 0.599 / 0.451 / 0.589 / 0.590 | 0.661 | 0.231 | 0.078 |
| S4 E1 with sub-2% groups | 1,062 (19) | 1,570.5 | 0.589 / 0.428 / 0.576 / 0.565 | 0.587 | 0.234 | 0.077 |
| S5 E1 all rate definitions | 1,426 (19) | 2,591 | 0.703 / 0.578 / 0.695 / 0.698 | 0.656 | 0.148 | 0.048 |
| S6 E1 integer counts only | 108 (6) | 4,491 | 0.833 / 0.778 / 0.824 / 0.815 | 0.639 | 0.028 | 0.000 |

Cluster-weighted Katz shares, where each report or each audit counts once (same file):
- E1: 0.679 report-weighted, 0.611 audit-weighted.
- E5: 0.531 report-weighted, 0.550 audit-weighted.
- ALL: 0.771 report-weighted, 0.679 audit-weighted.

The four interval methods agree closely except Clopper-Pearson-Bonferroni, which is conservative by construction (section 4, item 10).

### 5.3 By auditor, vendor, metric, characteristic, group size

From `results/interval_by_auditor.csv`, `interval_by_vendor.csv`, `interval_by_metric.csv`, `interval_by_char_group.csv`, `interval_by_group_size.csv` and `interval_E5_by_auditor_and_employer.csv`; Katz share excluding 0.8.

- **By auditor, E1:**
  - DCI Consulting Group: 671 ratios (78.6% of E1), 9 reports, median N_g 2,010, share 0.525.
  - Ambrose Consulting 0.864 (59 ratios); BABL AI 1.000 (11); BLDS 1.000 (26); Conductor AI 1.000 (34); Holistic AI 0.704 (27); Resolution Economics 0.923 (13); Unknown auditor (Cigna) 0.462 (13).
  - In ALL, Varun Ganesan (Dover) has 0.000 (12 ratios, median N_g 95; point ratio < 0.8 for 0.750).
- **By vendor, ALL:**
  - HireVue 0.554 (635 ratios); "Unknown" vendor (Cigna, Hartford, Wells Fargo) 0.122 (49 ratios, median N_g 49); Dover 0.000 (12).
  - ADP, Eightfold, Landed, Paradox, Phenom, Pymetrics and SmartRecruiters 1.000.
- **By rate definition, E1:** Scoring 0.908 (87); Selection 0.678 (118); "Selection, top" 0.558 (584); "Selection, top and middle" 0.400 (65).
- **By characteristic:**
  - E1: sex 0.866 (67), race/ethnicity 0.650 (277), intersectional 0.535 (510).
  - ALL: 0.889, 0.721 and 0.623.
- **By the smaller of N_g and N_c:**

  | Smaller N | E1 ratios | E1 excl. 0.8 | E5 ratios | E5 excl. 0.8 | E5 median Katz width |
  |---|---|---|---|---|---|
  | < 100 | 102 | 0.088 | 64 | 0.047 | 0.675 |
  | 100-499 | 167 | 0.341 | 15 | 0.467 | 0.162 |
  | 500-999 | 147 | 0.524 | 11 | 0.636 | 0.113 |
  | 1,000-4,999 | 267 | 0.768 | 48 | 0.917 | 0.051 |
  | 5,000-49,999 | 131 | 0.947 | 32 | 1.000 | 0.035 |
  | >= 50,000 | 40 | 0.975 | 2 | 1.000 | 0.019 |

- **E5 by employer:**

  | Employer (audits) | Ratios | Median N_g | Excl. 0.8 | Point ratio < 0.8 |
  |---|---|---|---|---|
  | Bloomberg | 13 | 645 | 0.923 | - |
  | Burlington (allocation analyst and intern audits only) | 25 | 108 | 0.000 | 0.760 |
  | Cigna | 13 | 167 | 0.462 | - |
  | Hartford | 22 | 10.5 | 0.000 | 0.409 |
  | Morgan Stanley | 26 | 26,491.5 | 1.000 | - |
  | NYU Langone | 59 | 10,458 | 0.864 | - |
  | Wells Fargo | 14 | 82.5 | 0.000 | 0.500 |

### 5.4 UGESP-style classification and posteriors

`results/ugesp_crosstab.csv`; Fisher p < 0.05 in 163 of 168 and 394 of 396 of the E1 "significant" cells.

| Set | Four-fifths flag and 2-SD significant | Four-fifths flag only | 2-SD significant only | Neither |
|---|---|---|---|---|
| E1 | 168 (19.7%) | 30 (3.5%) | 396 (46.4%) | 260 (30.4%) |
| E5 | 11 (6.4%) | 25 (14.5%) | 93 (54.1%) | 43 (25.0%) |
| V | 5 (1.7%) | 9 (3.0%) | 206 (68.0%) | 83 (27.4%) |

Jeffreys posterior P(ratio < 0.8) (`results/posterior_bands.csv`):

| Set | < 0.05 | 0.05-0.95 | > 0.95 |
|---|---|---|---|
| E1 | 55.3% | 36.1% | 8.7% |
| E5 | 57.6% | 42.4% | 0% |

### 5.5 Data quality: consistency, derived counts, comparators

**Counts are mostly derived** (`results/consistency_summary.csv`; known groups with N > 0, all rate definitions, HackerRank excluded):
- Of 3,144 rows with a selected count, only **552 (17.6%) hold integer counts**.
- 2,592 hold non-integer counts, of which 2,588 equal N x reported rate to within 1e-6, i.e. they were derived from a rounded rate.
- The consistency filter is therefore informative only for the integer rows. 13 of those fail, plus 3 derived rows; 5 pass only under the lenient tolerance.
- By auditor, DCI has 139 integer and 2,104 derived counts; BABL AI has 2 and 113.

**Reporting precision** (`results/extra_rounding_vs_sampling.csv`, an addition to the plan): for ratios with derived counts, the interval implied by rounding the published rates is narrower than the Katz interval in most cases.
- E1: wider than Katz for 60 of 746 ratios; median width 0.043 vs 0.142.
- ALL: 142 of 950.
- E5: 0 of 85.

**Comparator recomputation** (`results/comparator_check.csv`):
- In E1, 205 of 206 tables report a ratio of 1. The recomputed highest-rate comparator is one of the reported comparators in 142.
- 73 tables (all DCI) report ratios above 1.
- 281 of 853 ratios differ from the reported ratio by more than 0.05, and 99 change their four-fifths classification: 89 fall below 0.8 only after recomputation, 10 the reverse. The share of ratios below 0.8 rises from 14.0% (reported) to 23.2% (recomputed).
- E5: 5 flips (all to below 0.8), 18.1% to 21.1%.
- The DCI/HireVue reports explain why: "the aggregated impact ratios reported in the tables cannot be computed directly from the aggregated selection rates appearing in the tables" (Pfizer report in the OSF zip, read in this run).

### 5.6 Data scope of employer-posted audits (post hoc finding)

Reading the reports (text layers via `pdftotext`) showed that "employer-posted" does not mean "employer's own data" (coding with quotes: `code/data_scope_coding.csv`):
- **Multi-employer data, stated in the report:**
  - DCI/HireVue as posted by Pfizer 2023, Burlington 2023 (7 audits) and Burlington 2024: "historical data from multiple employers using the same automated employment decision tool (AEDT) are used as the basis of the audit".
  - NBCUniversal/SmartRecruiters: "gathered from multiple employers provided by the AEDT vendor".
  - BNP Paribas/Pymetrics: "employers with a NYC presence".
  - Sheppard Mullin/Suited 2023: "across all of the law firms using the Suited platform".
- **Multi-employer, inferred:**
  - JetBlue 2023/2024 and Citizens 2023/2024: reports not read. JetBlue's URL answered 404; the Citizens page is a summary. Their tables are verbatim identical to other employers' tables, with the same DCI data windows.
  - Sheppard Mullin 2024.
- **Employer's own data, stated:**
  - Bloomberg; Morgan Stanley 2023 ("Morgan Stanley supplied BLDS with applicant records").
  - NYU Langone ("Obtained 3 years of applicant data from NYU Langone").
  - Hartford and Wells Fargo (DCI: "New York City applicants").
  - Burlington's 2023 allocation-analyst and intern audits (single-employer template).
- **Employer's own data, inferred:** Morgan Stanley 2024.
- **Not verifiable:** Cigna (tables are images).
- **Vendor test data:** Alidoro (Landed).

Of E1's 854 ratios, 662 come from multi-employer pooled tables (set M). For these the auditor states that per-implementation analyses were aggregated. Binomial intervals on the aggregated counts are therefore **not a valid uncertainty model** for them, and M's shares are descriptive only.

### 5.7 Excluded populations (`results/excluded_population_by_data_scope.csv`, `_by_scope.csv`, `_by_auditor.csv`)

Medians are over tables that report an unknown count; "pooled" sums applicants over tables, where an applicant assessed by several tools counts once per tool.

**Employer-own-data audits** (13 tables per characteristic):

| Characteristic | Unknown count reported | Median unknown share (IQR) | Max | Sub-2% groups | Total excluded, median (max) |
|---|---|---|---|---|---|
| Race/ethnicity | 8 | 8.1% (5.4-9.6%) | 12.2% | in 12 tables; median 0.5% of known applicants, max 1.5% | - |
| Intersectional | 7 | 8.2% | 12.6% | in 13 tables; median 1.9%, max 3.2% | 9.5% (13.6%) |
| Sex | 8 | 4.4% | 9.25% | - | - |

**Multi-employer pooled:**
- Race/ethnicity: 52 of 55 tables report unknowns; median 3.5%, max 19.2%, pooled 5.3%.
- Intersectional: max 32.1%.

**Vendor-posted** (many do not report unknowns):
- Race/ethnicity: 10 of 25 tables; median 19.6% (IQR 5.1-50.9%), max 81.2%, pooled 74.0%.
- Sex: 9 of 24 tables; median 27.5%, max 71.0%.
- The intersectional maximum of 87.5% is Dover's. Its recorded unknown count of 4,853 equals the largest N in that audit and may be a total rather than an unknown count (flagged, not altered).

The 2% exclusion removes little: the largest sub-2% share of known applicants in any kept table is 4.6% (vendor-posted, intersectional).

**Sampling vs missing-data uncertainty** (`results/extra_missing_bounds_vs_sampling.csv`, using the ACLU file's precomputed bound columns):
- E1: Gerchick et al.'s worst-case missing-data bounds are wider than the Katz interval for 598 of 760 ratios; the proportional-allocation bounds for 302 of 731.
- E5: 47 of 92 and 19 of 63.
- In employer-own data, the sampling interval is therefore as wide as, or wider than, the proportional missing-data bound in most cases (median widths: Katz 0.535, proportional 0.091, worst case 0.530).

### 5.8 Cross-check against the OSF extraction (`results/osf_crosscheck_summary.csv`)

- 20 sampled rows: 12 Pfizer, 2 each Bloomberg, BNP Paribas and NBCUniversal, 1 each Cigna and Morgan Stanley.
- **Impact ratios agree in 20 of 20** (16 numeric values equal at the common precision, 4 both not reported).
- **The ACLU N was found verbatim in the employer PDF text for 15 of 15 checkable rows.** The other 5 were not checkable: 4 Pfizer rows with N = 0, and the Cigna PDF, whose tables are images.
- The OSF CSV has no counts, so the selected counts could not be cross-checked against it.

## 6. Reproducibility

- **Command:** `bash research/06_stage4/idea04/code/run.sh`. It stages the OSF files if absent, runs the code scan, the pilot and the validation, and rewrites everything in `results/`.
- **Software:** Python 3.11.15, numpy 2.4.6, pandas 3.0.6, scipy 1.17.1 (venv `$SCRATCH/venv`); pdftotext 24.02.0 (poppler); Linux 6.18.44 x86_64 (`results/run_metadata.json`). No package was installed for this pilot. The pilot uses only the standard library, numpy, scipy, pandas and the `pdftotext` binary.
- **Seeds:** bootstrap 20261015 (`np.random.default_rng(20261015)`, ratios processed in sorted order); Jeffreys posterior `default_rng([20261015, 1])`; OSF sample `random_state=20261015`; validation data 20261016.
- **Determinism:** a second independent run of the pilot into a scratch directory reproduced all 25 CSV outputs byte for byte.
- **Timings:** pilot 33.5 s in total, of which 25.4 s is the interval computation for 2,661 ratios (union over all variants). `run.sh` wall-clock 55 s including validation (about 21 s). Run at 2026-10-19 05:07 UTC.
- **Code checksums (sha256):**
  - `ll144_pilot.py`: `2fc5e8ae73d5d785cc013d9f538df54edb8c1094c4cb40eb2bdfb780e064e5d3`
  - `check_aclu_code.py`: `f945fb8c...e064e5d3`
  - `validate_methods.py`: `ae8a9861...18c1363`
  - `data_scope_coding.csv`: `cd439e79...0fd2207`
  - `run.sh`: `b8d3c539...18c1363` (as of the final run; recompute with `sha256sum code/*`)
- **Input checksums:** section 2.

## 7. Deviations from the written plan

1. **De-duplication operationalised.** The plan's key (auditor, tool, data window) was applied at table level and confirmed by identical counts.
   - The key alone cannot be applied to tables with unknown windows (only 4,004 of 4,507 rows have dates).
   - It merges same-window tables whose counts differ: 87 tables would be dropped by the literal key versus 49 by the confirmed rule.
   - It misses identical tables recorded with different windows: 14 of the 49 duplicates.
   - The literal key is reported as sensitivity S2 (60.1%, Katz).
2. **"Employer-level" operationalised as employer-posted (E1) before any result was computed.** After the first run, reading the reports showed most employer-posted DCI/HireVue, NBCUniversal, BNP Paribas and Sheppard Mullin audits use multi-employer data.
   - Post-hoc sets E4, E5, E5b and M were added and are labelled POSTHOC in every output.
   - E1 remains the reported primary. The C2 outcome is the same under both readings.
   - This required fetching four DCI PDFs and two employer web pages from links in the ACLU tracker; these downloads were not in the plan.
3. **"Exact interval":** Katz is asymptotic, not exact; Clopper-Pearson-Bonferroni is the exact-coverage option. Both are reported, Katz is primary for C2.
4. **"UGESP two-SD test":** the UGESP text read here does not define a two-SD rule. It is implemented as the conventional pooled z with |z| > 1.96 and reported alongside the four-fifths flag and Fisher's exact test.
5. **Exclusions taken from Gerchick et al.'s code:** HackerRank dropped; one rate definition per audit. Both are reversible in S5/S7.
6. **Comparator recomputed among groups of 2% or more**, which differs from the reported comparator in many DCI tables (section 5.5). Ratios against a reported pooled comparator cannot be recomputed from the published table.
7. **Additions not in the plan:**
   - rounding-precision bounds;
   - comparison with the ACLU missing-data bounds;
   - group-size bins and cluster-weighted shares;
   - method validation and coverage simulation;
   - per-audit data-scope coding.
8. **OSF cross-check compares impact ratios, not counts** (the OSF CSV has none). N was checked against PDF text instead.
9. **Not done:**
   - Part 2 and Part 3;
   - the 2025-2026 extension: the tracker has 15 dated 2025-2026 entries (13 WardenAI, 1 BABL AI, 1 FairNow) and 30 undated "TKTK" entries (`all_bias_audits.csv`), none retrieved;
   - reading the JetBlue and Citizens DCI reports (404 / summary page; Perma.cc blocks scripts);
   - the licence email (author action);
   - the literature stop condition (other agent).

## 8. Limitations

- **Exploratory and descriptive.** The corpus is the set of audits published by November 2024 and collected by the ACLU team. It is self-selected and covers 2023-2024 only. Nothing here estimates any tool's or employer's true disparity. A wide interval says the sample is small, not that hiring was fair or unfair.
- **Counts are mostly reconstructed.** 82% of selected counts are N x a rounded published rate. Binomial methods treat them as exact counts after rounding to integers. The reporting-precision analysis shows this matters for large-N vendor audits, not for small employer audits.
- **Pooled multi-employer tables:** the binomial model is not valid for aggregated per-implementation analyses (auditor's own statement). Set M and much of E1 are affected.
- **Data-dependent comparator:** the comparator is the maximum of several noisy rates (winner's curse), so the intervals condition on its identity. A procedure-level bootstrap that re-selects the comparator was not run.
- **Scoring-rate (median split) tools:** these induce dependence between groups; the independent-binomial model is approximate.
- **Correlated, unadjusted ratios:** intersectional, race and sex ratios from the same table are correlated and are counted as separate ratios with no multiplicity adjustment.
- **Single coder:** data-scope coding was done by one coder (this agent) from text-layer searches. Seven of the twenty coded report groups rest on inference, and one (Cigna) is unverifiable.
- **Dover's** intersectional unknown count looks like a total.
- **No novelty claim is made here** beyond what `03_challenge/04-...__novelty.md` already states; no new literature search was run by this agent.

## 9. Next steps

1. **Author:** send the licence question to analytics_inquiry@aclu.org before any further use or publication of derived tables.
2. **Preregister for the confirmatory version:**
   - the data-scope coding rule, with two independent coders and agreement reported;
   - E5-type "employer's own data" as the population for the sampling-uncertainty headline;
   - Katz as primary with Clopper-Pearson as sensitivity;
   - group-size bins as the main presentational device.
3. **Reframe the headline.** The pilot suggests the informative distinction is not "published ratios are uninformative" but "employer-level ratios split into precise large-employer audits and uninformative small-employer audits, while most employer-posted audits are multi-employer pools whose published numbers cannot carry a sampling interval at all".
4. **Retrieve the JetBlue and Citizens DCI reports and the 2025-2026 tracker entries in a browser.**
5. **Extend Part 2's simulation design:** it should include the multi-employer aggregation lever and the reconstruction of counts from rounded rates, both observed here.

## 10. Files

- **`code/`**
  - `run.sh`: entry point.
  - `ll144_pilot.py`: pipeline.
  - `check_aclu_code.py`: criterion 1 scan.
  - `validate_methods.py`: interval validation.
  - `data_scope_coding.csv`: manual coding, with quotes and sources.
- **`results/`** (aggregated only):
  - Corpus and pipeline: `aclu_columns_profile.csv`, `pipeline_funnel.csv`, `dedup_summary.csv`, `consistency_summary.csv`, `comparator_check.csv`, `data_scope_coding_applied.csv`.
  - Interval summaries: `interval_summary_variants.csv`, `interval_by_{auditor,vendor,metric,char_group,data_type,year,group_size,data_scope}.csv`, `interval_E5_by_auditor_and_employer.csv`.
  - Tests and posteriors: `ugesp_crosstab.csv`, `posterior_bands.csv`.
  - Excluded populations: `excluded_population_by_{scope,auditor,data_scope}.csv`.
  - Extras: `extra_rounding_vs_sampling.csv`, `extra_missing_bounds_vs_sampling.csv`.
  - Checks and stopping rule: `osf_crosscheck_summary.csv`, `aclu_code_inference_check.csv`, `method_validation.csv`, `stopping_rule_criterion2_all_variants.csv`.
  - Run record: `run_metadata.json` (versions, seeds, checksums, timings, stopping-rule summary).
