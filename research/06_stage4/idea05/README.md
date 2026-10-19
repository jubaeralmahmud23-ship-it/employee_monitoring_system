# Idea 5, Stage 4 pilot: robustness of log-derived worker rankings (BPI 2017 and BPI 2019)

**Status: exploratory pilot, run 2026-10-19 in the cloud container (not the author's Windows PC).** Nothing here is preregistered. The aim was to apply the stopping rule of `research/02_candidate_ideas.md` section 4.2 and to show that the factorial, bootstrap, placebo and detector steps run end to end. It is not a confirmatory test of H1 to H3.

**Outcome in one paragraph.** The full 405-cell factorial reduces to 117 distinct score vectors. It ran on both logs: BPI 2017 with 140 ranked workers and BPI 2019 with 307. The median Kendall tau-b across all distinct configuration pairs is 0.033 on BPI 2017 and 0.041 on BPI 2019; the 95% case-bootstrap intervals are [0.017, 0.050] and [0.032, 0.047]. Bottom-quintile reclassification under case-mix adjustment has a median of 17.9% on BPI 2017 and 27.3% on BPI 2019. Both tau medians are far below the 0.9 needed to stop, so **the empirical clause of the section 4.2 stopping rule is not triggered**. That holds under every exclusion set, minimum-event threshold, tie rule and alternative reading computed here. The literature clause (proceedings sweep) was not assessed in this run.

Three qualifications matter more than the headline:
1. The all-pairs median is dominated by pairs with different metrics. On both logs it sits inside the placebo (label-shuffle) range, so on its own it says the five metrics measure unrelated things, not that worker scores are noise.
2. Within a metric, the median tau is 0.488 on BPI 2017 and 0.503 on BPI 2019. Both are above all 20 placebo values (0.338 to 0.394 and 0.405 to 0.423).
3. The metric factor carries 54% (BPI 2017) and 57% (BPI 2019) of the variance in workers' rank percentiles across the 405 cells.

Sources: `results/stopping_rule.csv`, `results/*_tau_summary.json`, `results/*_bootstrap_stopping.json`, `results/*_placebo_summary.json` and `results/*_variance_decomposition.csv`.

---

## 1. What was run

| Step | Script (`code/`) | Inputs | Outputs (`results/` unless noted) |
|---|---|---|---|
| 01 | `01_convert_to_parquet.py` | raw XES / XES.GZ | Parquet in the data directory; `provenance_<log>_parquet.json` |
| 02 | `02_resource_fields.py` | both Parquet files | `resource_fields.json`, `resource_fields.csv` |
| 03 | `03_detector.py` | both Parquet files | `detector_calibration_bpic2019.csv`, `detector_offhours_threshold_sweep_bpic2019.csv`, `detector_feature_distributions_bpic2019.csv`, `detector_summary.json`; per-account flags and `exclusions.json` go to `<data>/derived/` only |
| 04 | `04_factorial.py` | one log + `exclusions.json` | `config_space.csv` (405 cells), `config_distinct.csv` (117 distinct), `<log>_config_summary.csv`, `<log>_tau_summary.json`, `<log>_tau_hist.csv`, `<log>_tau_by_factor.csv`, `<log>_casemix_reclass.csv`, `<log>_primary_contrasts_point.csv`, `<log>_variance_decomposition.csv`, `<log>_window_stability.csv`, `<log>_case_difficulty.csv`, `<log>_sensitivity.csv`, `<log>_system_account_attribution.json`; the per-resource score matrix goes to `<data>/derived/` only |
| 05 | `05_bootstrap.py` | one log, B = 500, 4 processes | `<log>_bootstrap_contrasts.csv`, `<log>_bootstrap_stopping.json`, `<log>_bootstrap_replicates.csv` |
| 06 | `06_placebo.py` | one log, 20 shuffles, 4 processes | `<log>_placebo.csv`, `<log>_placebo_summary.json` |
| 07 | `07_report.py` | the results above | `stopping_rule.csv`, `stopping_rule.json`, `pilot_summary.json`, `bootstrap_intervals_percentile_vs_basic.csv`, `fig_tau_distribution.png`, `fig_primary_contrasts.png`, `fig_tau_matrix.png` |
| all | `run.sh` | data directory | everything above; `wall_clock.json` was assembled from the run logs |

`idea05lib.py` holds every definition: the configuration space, metrics, attribution, case-mix models, the scoring engine and the rank statistics. Reproduce with:

```
PY=<venv>/bin/python bash code/run.sh <data_dir> 4 500 20
```

Here `<data_dir>` holds `bpic2017/bpic2017.xes.gz` and `bpic2019/BPI_Challenge_2019.xes`. run.sh checks both sha256 values, runs every interpreter with `-I` from `/`, and skips step 01 when the Parquet files already exist.

**Reproduction check.** run.sh was run end to end with B = 20 and 2 shuffles into a scratch results directory, taking 3 min 13 s (`wall_clock.json`). Every deterministic output was byte-identical to the committed files: configuration space, resource fields, detector tables, config summaries, case-mix reclassification, sensitivity, variance decomposition, window stability and primary contrasts. The first 20 bootstrap replicates and the first 2 placebo shuffles matched the full runs exactly (maximum absolute difference 0.0), because seeds are spawned per replicate.

## 2. Data provenance and checksums

| Log | Source | Licence (4TU record) | Raw file | sha256 (raw) | md5 check | Parquet sha256 |
|---|---|---|---|---|---|---|
| BPI Challenge 2017 | 4TU DOI 10.4121/uuid:5f3067df-f10b-45da-b98b-86ae4c7a310b. File copied from `scratchpad/bpic2017.xes.gz`, downloaded 2026-10-03 | 4TU General Terms of Use (rights URL 10.4121/resource:terms_of_use; **terms PDF not read in this run**) | `BPI Challenge 2017.xes.gz`, 29,658,747 bytes | `183c5e5189282779c811c78c33ff936351b3dd201165d612211fc220936f8249` | `10b37a2f78e870d78406198403ff13d2`, equal to 4TU `supplied_md5` and `computed_md5` (`https://data.4tu.nl/v2/articles/12696884/files`) | `0037fe2dff00c692fe1ddec0e5ab5e49a55b7ed40e7477dec263c66cadf0bc05` |
| BPI Challenge 2019 | 4TU DOI 10.4121/uuid:d06aff4b-79f0-45e6-8ec8-e19730c248f1 (article 12715853). Downloaded 2026-10-19 04:39 UTC with curl `-L --retry 3`, first attempt, 22.4 s | CC BY 4.0 | `BPI_Challenge_2019.xes`, 728,558,522 bytes | `af63bc687fc4152f2123b05c3af7772b37ef3fce2d3f67f812666c9e356baae7` | `4eb909242351193a61e1c15b9c3cc814`, equal to 4TU `supplied_md5` | `861bc143deb8ff42e55b9de8b1ee1224be5aa8d76cf595cbb04c802465e247cc` |

Raw and Parquet files live under `/tmp/claude-0/-home-user-employee-monitoring-system/c64eab22-9c10-592c-b92e-5ac629c5be82/scratchpad/data/idea05/{bpic2017,bpic2019}/` and are git-ignored. Per-resource derived files (detector features, exclusion lists, score matrices) are in `.../data/idea05/derived/` and are deliberately not in the repository. `exclusions.json` has sha256 `b2156d6bea18b89a2a48bb094126dda752cf116699766c1b92f301f788601dad`.

## 3. What the resource field holds (`results/resource_fields.json`, `resource_fields.csv`)

- **BPI 2017.** One resource attribute, `org:resource`, with 149 distinct values, all of the form `User_<n>`. The publisher gives no label for person versus system. 141 accounts have at least 100 events.
  - `User_1` has 148,404 events (12.34%). Its top activities are W_Handle leads, A_Create Application, A_Submitted, W_Complete application, A_Concept, W_Call after offers, O_Cancelled and A_Cancelled, which is consistent with an automated or online-channel account.
  - **Correction to the idea card:** the card's "150 resources" counts the XES `<global scope="event">` default value `UNKNOWN`. A direct count of the raw XES gives 150 distinct value strings across 1,202,268 occurrences: 1,202,267 events plus the one global declaration.
  - The log has seven lifecycle values; 98.4% of timestamps have non-zero seconds.
- **BPI 2019.** `org:resource` and `User` are identical on 100% of events. There are 607 `user_*` accounts (publisher label: human), 307 of them with at least 100 events, holding 1,040,639 events. There are 20 `batch_*` accounts (publisher label: automated), 15 of them with at least 100 events, holding 156,187 events. The value `NONE`, meaning no user was recorded, covers 398,770 events.
  - The log has no lifecycle attribute, and timestamps have minute resolution (0% non-zero seconds).
  - 327 events fall outside 2018-01-01 to 2019-02-01 (local time) and were dropped. They include dates from 1948 to 2020.

## 4. Operational definitions (written for this pilot; see Deviations)

The plan names the factor levels but not their operationalisation. Every definition below was fixed in `idea05lib.py`.

- **Units.** A resource (pseudonymous account) within one log. All scores are oriented so that higher means better.
- **Metric (5 levels).**
  - *EPH, events per active hour:* the resource's events divided by its active time.
  - *CCA, completed cases attributed:* the count of completed cases attributed to the resource in a slot.
  - *APT, mean activity processing time* (lower is better). In BPI 2017 it is the summed duration of each resource's start/resume-to-suspend/complete/ate_abort work segments per (case, activity, instance, resource). There are 227,858 such units from 252,895 segments; 1,475 segments whose closing event had another resource were dropped. In BPI 2019, which has a single timestamp per event, it is the time from the previous event in the case to the event, attributed to the event's resource (1,343,862 units). That is waiting plus working time, not processing time.
  - *RWK, rework share* (lower is better): the share of attributed completed cases in which some activity label is completed more than once up to completion. This applies to 51.5% of BPI 2017 cases and 8.1% of BPI 2019 cases.
  - *DLA, deadline adherence:* the share of attributed completed cases closed within T days of their first event. T is the ceiling of the log's median case duration: 20 days for BPI 2017 and 72 days for BPI 2019. On-time shares are 51.8% and 50.1%.
- **Case completion.**
  - BPI 2017: the first A_Pending, A_Denied or A_Cancelled event. 31,411 of 31,509 cases are completed.
  - BPI 2019: the last event, if it is Clear Invoice or Delete Purchase Order Item, or Record Goods Receipt for consignment items. 202,584 of 251,734 cases are completed.
- **Attribution (3 levels; applies to CCA, RWK and DLA).** First, last or majority touch among eligible events up to completion; majority ties go to the earliest first touch. The case-mix stratum of a case is the activity of the attributed touch, or the majority resource's most frequent activity in the case.
- **Window (3 levels).** Week (Monday to Sunday), month or quarter, in local time (Europe/Amsterdam). The window is the time-slot length of Pika et al.'s indicator time series. The metric is computed per (resource, slot), and the resource's score is the mean over the slots in which it is defined. For CCA, those are the slots where the resource is active or has completions. BPI 2017 has 58, 14 and 5 slots; BPI 2019 has 55, 13 and 5.
- **Idle gap (3 levels: 15, 60, 240 min; applies to EPH).** Each event is credited with active time equal to min(gap to the resource's next event, g), with g for the resource's last event. Active time is the sum of these credits, the idle-timeout logic of monitoring tools.
- **Case-mix adjustment (3 levels).**
  - *none.*
  - *activity:* indirect standardisation against activity-stratum means. The stratum is activity|lifecycle for EPH, the activity for APT and the attributed activity for the case metrics.
  - *regression:* expected values from OLS on activity fixed effects plus case covariates. For BPI 2017 the covariates are LoanGoal, ApplicationType and log RequestedAmount. For BPI 2019 they are Item Category, Item Type, Document Type, Spend area, Company and log item value.
  - Adjusted scores are computed as follows. EPH is expected over observed active time. APT is observed over expected time. RWK and DLA use the mean of (observed minus expected). CCA counts cases weighted by expected effort, where effort is the events up to completion, scaled to mean 1 (a case-mix-index analogue).
  - The models are fitted on all units of eligible resources.
- **Configuration space.** The 405 cells form 117 distinct score vectors, because attribution does not change EPH or APT and the idle gap only changes EPH (`config_space.csv`, `config_distinct.csv`). Statistics are reported over both the 6,786 distinct pairs and the 81,810 cell pairs; in the cell version, identical cells count as tau = 1.
- **Exclusions and analysis set.**
  - Eligible accounts are those not excluded as system accounts and not "no user". BPI 2017 excludes `User_1` (see Deviations); BPI 2019 excludes the 20 labelled batch users.
  - The minimum-event threshold is N_min = 100 events, fixed in code before any tau was computed.
  - Statistics are pairwise-complete over eligible accounts with at least N_min events: 140 (BPI 2017) and 307 (BPI 2019).
- **Statistics.**
  - Kendall tau-b, pairwise-complete.
  - The bottom quintile is every worker whose score is at or below the k-th smallest score, with k = round(0.2 n), so tied workers stay together.
  - Reclassification is the share of the bottom quintile under configuration a that is not in the bottom quintile under b. An alternative, the share of all workers whose bottom-quintile status changes, is also reported.
- **Primary contrasts (20, defined here; `idea05lib.primary_contrasts`).** The dashboard baseline is CCA, last touch, month, no adjustment. The contrasts are:
  - one-factor-at-a-time changes of metric (4), attribution (2), window (2) and idle gap for EPH (2);
  - all 10 case-mix contrasts (5 metrics x activity/regression) at last touch and month.
- **Stopping-rule quantities.**
  - Median tau over all distinct configuration pairs (primary).
  - Median over the 78 distinct none-versus-adjusted pairs of the bottom-quintile reclassification rate (primary). The 405-cell weighted versions are also given.
- **Bootstrap.**
  - 500 case-resampling replicates using multinomial case weights, seeded with `SeedSequence(20261015).spawn(500)`.
  - Every configuration is re-aggregated in each replicate. Active-time credits, case-mix fits, completion and attribution are held at their full-sample values.
- **Placebo (20 shuffles).** A touch unit is all events of one eligible resource in one case: 196,339 units in BPI 2017 and 933,995 in BPI 2019. Resource labels are permuted across touch units within strata defined by the activity of the unit's first event (18 and 28 strata). This keeps each worker's volume and role mix but breaks the link to particular cases, times and outcomes. The whole pipeline is re-run per shuffle, seeded with `SeedSequence([20261015, 6]).spawn(20)`.
- **Automated-account detector (pre-specified before the labels were examined).** Features:
  - off-hours share: 20:00 to 06:00 or weekend, ignoring 00:00:00 date-only stamps;
  - multi-case burst share: events in a (resource, minute) bucket that touches at least 5 cases;
  - robust z-score of log10 event count.

  Rules: R1 is off-hours share of at least 0.25; R2 is burst share of at least 0.5; R3 is z of at least 3.5; R_any is any of the three. The comparator is a class-balanced logistic regression with 5-fold CV repeated 20 times.

## 5. Results

### 5.1 Stopping rule (section 4.2), criterion by criterion (`results/stopping_rule.csv`, `stopping_rule.json`)

Rule as written: stop the confirmatory framing if, after the named exclusions, the median Kendall tau across defensible configurations exceeds 0.9 on both BPI 2017 and BPI 2019 **and** bottom-quintile reclassification under case-mix adjustment is below 10% on both. Also stop if the proceedings sweep finds a rank-stability study of resource measures on public logs.

| Criterion | Log | Computed value | 95% case-bootstrap interval (percentile) | Threshold | Condition met? |
|---|---|---|---|---|---|
| 1a median tau across configurations (117 distinct; primary) | BPI 2017 | 0.033 | [0.017, 0.050] | > 0.9 | no |
| 1a same, over the 405-cell pairs | BPI 2017 | 0.038 | [0.024, 0.058] | > 0.9 | no |
| 1a median tau (primary) | BPI 2019 | 0.041 | [0.032, 0.047] | > 0.9 | no |
| 1a same, over the 405-cell pairs | BPI 2019 | 0.038 | [0.031, 0.047] | > 0.9 | no |
| 1b bottom-quintile reclassification under case-mix (share of bottom quintile; primary) | BPI 2017 | 17.9% | [17.4%, 25.0%] | < 10% | no |
| 1b alternative reading: share of all ranked workers whose bottom-quintile status changes | BPI 2017 | 7.1% | [7.0%, 10.0%] | < 10% | yes |
| 1b reclassification (primary) | BPI 2019 | 27.3% | [24.6%, 29.0%] | < 10% | no |
| 1b alternative reading (all workers) | BPI 2019 | 9.4% | [8.8%, 10.5%] | < 10% | yes |
| Empirical clause (1a and 1b on both logs) | both | 1a fails on both logs under every reading | 0 of 500 replicates had median tau > 0.9, on either log | all four conditions | **not met: not triggered** |
| 2 proceedings sweep finds a rank-stability study | n/a | **not assessed in this run** | n/a | n/a | not assessed |

Sensitivity of the stopping quantities (`results/<log>_sensitivity.csv`). The highest median tau in any variant is 0.051 (BPI 2017) and 0.069 (BPI 2019). The variants are: complete-case set; index tie rule; N_min of 1, 20 or 500; system accounts included; and exclusion of the detector-flagged sets of 25 and 19 accounts (BPI 2017) or 198 labelled-or-detected accounts (BPI 2019). The highest within-metric median tau in any variant is 0.505 and 0.581. The lowest median reclassification is 16.7% and 23.3%. No reading or variant computed here comes close to the 0.9 tau condition.

### 5.2 Rank agreement across configurations

| | BPI 2017 | BPI 2019 | Source |
|---|---|---|---|
| Workers ranked (eligible) | 140 (148) | 307 (607) | `<log>_tau_summary.json` |
| Median tau, all 6,786 distinct pairs | 0.033 | 0.041 | same |
| Median tau, same-metric pairs (1,440) | 0.488 | 0.503 | same |
| Median tau, different-metric pairs (5,346) | -0.0004 | 0.0005 | same |
| Within-metric medians: EPH / CCA / APT / RWK / DLA | 0.672 / 0.532 / 0.798 / 0.343 / 0.191 | 0.667 / 0.717 / 0.543 / 0.231 / 0.276 | same |
| Share of pairs with tau > 0.9 / tau < 0.7 | 1.2% / 94.9% | 1.7% / 94.2% | same |
| Median tau, pairs differing **only** in metric / attribution / window / idle gap / case-mix | -0.016 / 0.145 / 0.816 / 0.785 / 0.870 | 0.035 / 0.236 / 0.894 / 0.837 / 0.682 | `<log>_tau_by_factor.csv` |
| Variance of rank percentile across the 405 cells (pooled share): metric / attribution / window / idle gap / case-mix / interactions | 0.538 / 0.044 / 0.014 / 0.002 / 0.009 / 0.394 (112 complete-case workers) | 0.567 / 0.043 / 0.005 / 0.001 / 0.041 / 0.343 (136) | `<log>_variance_decomposition.csv` |

Metric choice and attribution rule are the dominant sources of instability. Window and idle gap matter much less. Case-mix adjustment matters a lot for some metrics: on BPI 2017, rework and deadline adherence have tau of 0.39 to 0.55 against their unadjusted versions. Attribution alone produces near-independent rankings of completed-case counts: last versus first touch has tau 0.021 [-0.003, 0.026] on BPI 2017 and 0.185 on BPI 2019 (`<log>_bootstrap_contrasts.csv`, `<log>_primary_contrasts_point.csv`). `fig_tau_distribution.png` and `fig_tau_matrix.png` show the structure: high-agreement blocks within a metric, near-zero agreement across metrics.

### 5.3 Case-mix adjustment and bottom-quintile reclassification (`<log>_casemix_reclass.csv`, `<log>_primary_contrasts_point.csv`, `<log>_case_difficulty.csv`)

- **Medians over the 78 distinct pairs.** 17.9% on BPI 2017 (mean 27.4%, maximum 92.6%) and 27.3% on BPI 2019. The bottom-quintile share rule pushes the BPI 2019 figure to 30.9% if ties are broken by index instead of kept together.
- **BPI 2017 dashboard baseline (CCA, last touch, month).** Case-mix adjustment hardly moves it: tau 0.920, reclassification 3.6% (activity) or 7.1% (regression). It moves deadline adherence strongly: tau 0.389, 66.7% of the bottom quintile reclassified.
- **Confounding by case mix.** On BPI 2017, the Spearman correlation between a worker's mean expected case effort and the unadjusted rework score is -0.768. For unadjusted deadline adherence it is 0.708. After activity adjustment these fall to -0.252 and -0.018.
- **Large tie groups in BPI 2019.** 107 of 307 users have zero last-touch completed cases (`results/bpic2019_config_summary.csv`, column `bottom_set_size_inclusive_ties`). Bottom-quintile membership for CCA is therefore mostly a tie group at zero, and CCA case-mix contrasts show 0% reclassification.

### 5.4 Placebo null (`<log>_placebo_summary.json`)

| Statistic | BPI 2017 observed | Placebo mean [min, max] (20) | BPI 2019 observed | Placebo mean [min, max] (20) |
|---|---|---|---|---|
| Median tau, all distinct pairs | 0.033 | 0.052 [0.032, 0.078] | 0.041 | 0.047 [0.033, 0.060] |
| Median tau, same-metric pairs | 0.488 | 0.362 [0.338, 0.394] | 0.503 | 0.415 [0.405, 0.423] |
| Median reclassification under case-mix | 17.9% | 29.6% [25.0%, 37.5%] | 27.3% | 34.0% [31.5%, 38.6%] |
| Median share of all workers changing status | 7.1% | 11.9% [10.0%, 15.3%] | 9.4% | 13.6% [12.7%, 15.5%] |

Reading:
- The all-pairs median is at placebo level. The placebo keeps each worker's volume and role mix, so this statistic cannot tell a stable worker signal apart from shuffled labels.
- Within-metric agreement exceeds every placebo value on both logs.
- Observed case-mix reclassification is lower than every placebo value, so worker identity makes bottom-quintile membership more stable than shuffled labels do.
- The placebo is a single, design-specific null. Other nulls (event-level shuffles, shuffles within time slots) were not run.

### 5.5 System-account sensitivity (`<log>_system_account_attribution.json`, `<log>_sensitivity.csv`)

- **BPI 2017, User_1 in the attribution pool.**
  - User_1 captures 64.8% of completed cases under first touch, 25.3% under last touch and 1.9% under majority touch.
  - When ranked, it sits in the top quintile for CCA (last touch) and EPH.
  - Human workers' rankings change with its inclusion, measured for the same configuration with User_1 excluded versus included: CCA last touch tau 0.663 with 32.1% of the bottom quintile reclassified; CCA first touch tau 0.684 (7.1%); CCA majority tau 0.987 (0%); RWK first touch tau 0.595 (27.3%); DLA first touch tau 0.494 (50.0%).
  - The stopping quantities barely move: median tau 0.041 versus 0.033, reclassification 17.9% versus 17.9%.
- **BPI 2019, batch users in the pool.**
  - Batch users hold 9.8% of events and capture 8.3% (first touch), 0.35% (last) and 8.1% (majority) of completed cases. 15 of them pass N_min.
  - Human ranking agreement, included versus excluded, is tau 0.87 to 0.94.
  - Median tau with batch users included is 0.046 (versus 0.041), and median reclassification 26.1% (versus 27.3%).

### 5.6 Automated-account detector calibrated on BPI 2019's labels (`detector_calibration_bpic2019.csv`, `detector_offhours_threshold_sweep_bpic2019.csv`, `detector_summary.json`)

| Rule (pre-specified) | All 627 accounts: precision / recall | 322 accounts with at least 100 events: precision / recall | Event-weighted precision / recall (all) |
|---|---|---|---|
| R1 off-hours share of at least 0.25 | 0.478 / 0.550 | 0.615 / 0.533 | 0.974 / 0.695 |
| R2 multi-case burst share of at least 0.5 | 0.067 / 0.600 | 0.075 / 0.733 | 0.091 / 0.460 |
| R3 volume z of at least 3.5 | no account flagged / 0.000 | no account flagged / 0.000 | no account flagged / 0.000 |
| **R_any (the pre-specified detector)** | **0.087 / 0.850** | **0.092 / 0.933** | 0.151 / 0.821 |
| Logistic regression, 5-fold CV x 20 (mean) | 0.140 / 0.723 | n/a | n/a |

The pre-specified detector is not fit for purpose at the account level.
- R2 fails because a BPI 2019 case is a purchase-order line item, so a human creating one order touches many cases in the same minute.
- R1 has high event-weighted precision: the humans it flags have few events.
- The threshold sweep (added after the pre-specified rules were evaluated) reaches at best a per-account precision of 0.714 with recall 0.50, at off-hours share of at least 0.5.
- Applied to BPI 2017, R_any flags 25 accounts holding 22.3% of events, among them User_1; the logistic model flags 19 (20.3%). User_1's features are off-hours 0.421, burst 0.218 (the highest; the other 148 accounts reach at most 0.142) and z 2.71.

### 5.7 Pilot readings for H1 to H3 (not confirmatory tests)

- **H1 (median tau < 0.7).** Consistent on both logs: 0.033 and 0.041 overall; 0.488 and 0.503 within a metric.
- **H2 (case-mix flips bottom-quintile membership for > 25%).** BPI 2017 gives 17.9% [17.4%, 25.0%]; BPI 2019 gives 27.3% [24.6%, 29.0%]. The intervals touch or straddle 25%. Under the all-workers reading the values are 7.1% and 9.4%.
- **H3 (shorter windows monotonically less stable)** gives mixed readings across three views (`<log>_window_stability.csv`).
  - Per-slot "dashboard" cross-configuration tau, week / month / quarter: BPI 2017 0.046 / 0.054 / 0.072 (monotone); BPI 2019 0.055 / 0.038 / 0.041 (not monotone).
  - Adjacent-slot Spearman: BPI 2017 0.528 / 0.695 / 0.592 (not monotone); BPI 2019 0.560 / 0.727 / 0.755 (monotone).
  - Whole-log cross-configuration tau by window: not monotone on either log.

### 5.8 Bootstrap interval caveat (`bootstrap_intervals_percentile_vs_basic.csv`)

Case resampling adds noise to every configuration's scores, which pulls rank agreement down. For the within-metric median tau, the point estimate lies above its percentile interval on both logs:
- BPI 2017: 0.488 against [0.438, 0.480]; the basic (reflected) interval is [0.495, 0.538].
- BPI 2019: 0.503 against [0.464, 0.493]; the basic interval is [0.513, 0.542].

In 6 of the 92 statistics in that file, the point estimate lies outside its percentile interval. Treat the percentile intervals in `fig_primary_contrasts.png` as conservative toward lower agreement. None of this affects the stopping decision.

## 6. Deviations from the written plan (section 4.2, idea card, feasibility file)

1. **Operational definitions written here.** The plan names the factor levels, but the metrics, completion rules, attribution scope, window semantics, idle-gap credit and case-mix models had to be defined (section 4). In particular:
   - Attribution applies to the three case-level metrics, not only to completed cases. The feasibility file assumed CCA only.
   - The window is the time-slot length, with per-slot means.
   - "Regression" adjustment includes activity fixed effects.
   - Deadline adherence uses a median-based target (20 and 72 days) because neither log has an SLA field.
2. **"Defensible configurations".** All 405 cells are treated as defensible. The primary statistic uses the 117 distinct score vectors; the 405-cell version is also reported. The within-metric median is a sensitivity reading, not the rule's quantity.
3. **Minimum-event threshold.** N_min = 100 events was chosen in this run because no preregistration exists. It was fixed in code before any tau was computed; 1, 20 and 500 are reported as sensitivities.
4. **Analysis set.** The primary analysis is pairwise-complete. A complete-case set (a defined score in all 117 configurations) loses 28 of 140 BPI 2017 workers and 171 of 307 BPI 2019 workers. The switch was made after the first test run, which had already shown the complete-case BPI 2017 medians (tau 0.031, reclassification 22.7%). Both versions are in `<log>_sensitivity.csv`.
5. **Tie rule for quintiles.** The first implementation broke ties by index. After 107 of 307 BPI 2019 users turned out to be tied at zero completed cases, the primary rule became "at or below the 20th-percentile score" (ties kept together). The index rule is reported: identical on BPI 2017; 30.9% instead of 27.3% median reclassification on BPI 2019.
6. **System-account exclusion for BPI 2017.** R_any was pre-specified as the BPI 2017 exclusion rule. Its per-account precision on BPI 2019's labels was 0.087, so the primary exclusion became the plan's named account, User_1. The R_any (25 accounts) and logistic (19 accounts) exclusion sets are sensitivities. The off-hours threshold sweep was added after the pre-specified rules were evaluated.
7. **BPI 2019 scope.** Section 4.2's pilot list mentions only detector calibration on BPI 2019. The factorial, bootstrap (500) and placebo (20) were also run on BPI 2019, because the stopping rule needs values from both logs; the plan's calendar foresees a pilot on both. BPI 2019 adaptations:
   - processing time is inter-event time;
   - the completion rule is log-specific;
   - 327 out-of-period events were dropped;
   - `NONE` is treated as no user.
8. **Bootstrap design.** Per-unit timeline quantities, case-mix fits and attribution are held fixed, so intervals are conditional on them. Replicates were not reduced, since the full run took 2.5 min (BPI 2017) and 8.6 min (BPI 2019).
9. **Placebo and primary contrasts** were defined in this run (sections 4 and 5.4); the plan does not specify them.
10. **Not done in this pilot.** These were recommended by the novelty file but are not in the pilot as written:
    - per-worker reliability and rank intervals;
    - a Gu-Koenker empirical-Bayes selection comparator;
    - a workload covariate (Nakatumba and van der Aalst);
    - four-fifths-style ratios across roles;
    - the ICPM/BPM proceedings sweep.
11. **Environment.** Cloud container (Python 3.11, 4 vCPU, 15 GB), not the author's Windows PC with Python 3.14. pm4py 2.7.23.8 matches the version named in the feasibility file. Another Stage 4 pilot process (idea04) shared the four vCPUs during steps 04 to 06, so wall-clock times are upper bounds.
12. **Card correction.** BPI 2017 has 149 resource values, not 150 (section 3).

## 7. Limitations

- **Exploratory pilot.** Definitions were fixed during the run (section 6), nothing is preregistered, and the H1 to H3 readings are descriptive.
- **Pseudonymous identifiers.** Accounts cannot be verified as individual persons:
  - User_1 is treated as a system account on behavioural and activity grounds only.
  - R1 flags 24 further BPI 2017 accounts with evening or weekend work, which may be shift workers or shared logins.
  - BPI 2019's batch labels come from the publisher.
- **No ground-truth productivity.** The pilot measures agreement between configurations and confounding by case mix, not validity.
- **Workflow logs, not monitoring telemetry.** Single-timestamp metrics in BPI 2019 measure event density and waiting time, not labour time.
- **Generic metric definitions.** Rework (any repeated activity) and the median-based deadline are generic choices. Alternative domain-specific definitions could change within-metric agreement.
- **Narrow null.** The placebo preserves volume and role mix. It is one null among several possible.
- **Simple case-mix models.** The models are linear and fitted once. The bootstrap does not propagate their uncertainty.
- **No release of derived per-resource rankings.** Per-pseudonym rankings and scores have not been released. They stay in the untracked `data/idea05/derived/` directory until the 4TU General Terms of Use (article 12721292, `General_terms_of_use.pdf`) have been read and a data-handling rule is written. Results contain only configuration-level aggregates. The only pseudonym named in `results/` is the system account User_1, which the idea card already named. BPI 2019 is CC BY 4.0, but the same rule is applied for consistency.
- **Novelty not reassessed.** No literature search was run in this pilot. Novelty claims stay as in `03_challenge/05-...__novelty.md` (verdict "partially-covered").

## 8. Reproducibility

- **Software** (venv at `.../scratchpad/venv`): Python 3.11.15 on Linux 6.18.44, pm4py 2.7.23.8, pandas 3.0.6, numpy 2.4.6, scipy 1.17.1, scikit-learn 1.9.1, matplotlib 3.11.2, pyarrow 26.0.0 (installed in this run), lxml 6.1.3. pm4py prints an AGPL banner and suggested the optional `r4pm` reader, which was not installed.
- **Seed** 20261015 (`idea05lib.SEED`). The bootstrap uses `SeedSequence(20261015).spawn(B)`, the placebo `SeedSequence([20261015, 6]).spawn(n)`, and the detector CV `random_state=20261015`.
- **Wall-clock** (`results/wall_clock.json`; 4 vCPU Intel Xeon @ 2.10 GHz, shared with another pilot):

  | Step | BPI 2017 | BPI 2019 |
  |---|---|---|
  | BPI 2019 download | n/a | 22.4 s |
  | Parquet conversion | 89.8 s | 128.0 s |
  | Factorial | 34.8 s | 43.8 s |
  | Bootstrap B = 500 (4 processes) | 148.5 s | 513.6 s |
  | Placebo, 20 shuffles (4 processes) | 98.1 s | 166.1 s |

  Steps 02 and 03 took about 10 s each. The full pipeline takes roughly 21 min, and the run.sh check at B = 20 took 3 min 13 s. The feasibility file's local-PC estimate for the BPI 2017 pilot was 20 to 40 minutes.
- **Results size.** 49 files, 1.6 MB.

## 9. Exact next steps

1. Read the 4TU `General_terms_of_use.pdf` (article 12721292). Then write the data-handling rule for per-pseudonym tables: re-hash identifiers and release distributions only. Do this before any per-resource table leaves the machine.
2. Run the literature clause of the stopping rule: the dblp and Semantic Scholar sweep of ICPM, BPM, CAiSE and Process Science 2022-2026, plus the BPI Challenge 2017 and 2019 report submissions, as listed in section 4.2. Only then can the full rule be declared not triggered.
3. Settle the headline estimand before the OSF preregistration. The all-pairs median tau is dominated by cross-metric pairs and sits at placebo level, so it is a weak test of the claim. Preregister these alongside the rule's quantity:
   - the within-metric median tau, which is above every placebo value;
   - the one-factor contrasts, especially attribution, which produced tau 0.02 to 0.30;
   - both readings of reclassification (bottom-quintile share and all workers).
4. Fix in the preregistration: N_min, the tie rule, the pairwise-complete analysis set, the exclusion rule, the metric definitions in section 4, and a log-specific deadline and rework definition where the log supports one.
5. Replace the automated-account detector. Account-level timing features fail on BPI 2019. Try activity-mix and inter-event-regularity features, report event-weighted precision, and validate on BPI 2019 and BPI 2018.
6. Add the elements the novelty file asks for: per-worker split-half reliability and rank intervals, Gu-Koenker selection as a comparator to raw quintiles, a workload covariate, and four-fifths-style ratios across discovered roles.
7. Improve the bootstrap: refit the case-mix models per replicate and report basic or BCa intervals for rank-agreement statistics.
8. Extend to the other logs with confirmed resource fields: BPI 2013 incidents, 2015 x5, 2018, and 2012, 2014, 2020 and Helpdesk after checking their resource fields. Use `run.sh` with a per-log entry in `idea05lib.LOGCFG`.
