# Stage 4 synthesis: deep novelty checks and pilots for ideas 6, 5 and 4

**Date:** 2026-10-19. **Written by:** the lead-analyst agent (Claude), from the six Stage 4 agent reports in this directory. **No new experiment, search or download was run for this synthesis.** It reads the per-idea files, re-checks their stopping-rule numbers against the result files, and draws the recommendations.

**Status: EXPLORATORY. Nothing in this directory is a confirmatory result.**
- The three pilots were each run once, unregistered, with operational definitions fixed during the run. Each pilot README lists these choices as deviations.
- The idea-6 pilot was coded by one machine coder (Claude). The design requires two human coders, and no human has checked these codes.
- Stopping rules are applied exactly as written in `research/02_candidate_ideas.md` section 4. No rule or threshold was changed. Where a rule needed a reading, the pre-specified reading is primary and the others are labelled.
- Every number below cites the file it comes from. Paths are relative to `research/06_stage4/` unless they start with `research/`.

**Environment (verified 2026-10-19).** This was the cloud container, not the author's Windows PC used on 2026-10-05.
- Hardware: 4 vCPU (Intel Xeon @ 2.10 GHz, per `idea05/results/wall_clock.json`), 15 GB RAM, about 30 GB free disk, no GPU. No paid LLM APIs and no API keys.
- Software: Python 3.11.15 venv at `$SCRATCH/venv` with pm4py 2.7.23.8, pandas 3.0.6, numpy 2.4.6, scipy 1.17.1, scikit-learn 1.9.1, statsmodels 0.15.0 and pyarrow 26.0.0; pdftotext 24.02.0; curl 8.5.0. Versions are as reported in the pilot READMEs.
- Sites that answered: arXiv, Crossref, 4TU, ACL Anthology, Springer open access, Hugging Face, Zenodo, OSF, GitHub (the two ACLU repositories only).
- Sites that refused or limited access:
  - OpenAlex refused every list query all day: the anonymous daily budget for the shared IP was exhausted.
  - Semantic Scholar answered most citation-list calls, but keyword search and several legs returned HTTP 429.
  - dblp returned a bot-check page.
  - The AIS eLibrary search endpoint returned 403, and its PDFs sit behind Cloudflare and a subscription.
  - The ACM, Elsevier, Wiley, INFORMS, Taylor & Francis, APA, SAGE, OUP, SSRN and RAND sites refused or were not fetched.
- `$SCRATCH` = `/tmp/claude-0/-home-user-employee-monitoring-system/c64eab22-9c10-592c-b92e-5ac629c5be82/scratchpad`. Raw data and row-level derived files are kept there, outside the repository.

**Commits.** The pilot agents state that they made no commit, and this synthesis made none.
- A background loop started earlier in the session (`$SCRATCH/autosave.sh`, every 180 s) commits `research/` and pushes to `origin/claude/peaceful-cori-ny59q5`.
- The pushed history therefore contains intermediate versions of the Stage 4 files. These include idea-4 outputs from before a de-duplication bug fix (`idea04` agent report).
- The final files are authoritative. HEAD was `d5507c7` at 06:59:51 UTC, when the input checksums for this synthesis were recorded.

### At a glance

| Idea | Pilot clause of the stopping rule | Literature clause | Rule outcome | Deep novelty verdict | Recommendation |
|---|---|---|---|---|---|
| 6. Error-bar audit of LLM evaluations in IS and industry-track venues | Criterion 2 holds under the primary readings: 2a 15% < 30%, 2b 14 < 25 | Not triggered | **Triggered** (criterion 3 undetermined) | partially-covered; narrower than on 2026-10-05 and nearer "largely-covered" on design | **Pivot**: stop the JAIS-targeted audit. The rule's own fallback is a CAIS methods essay. |
| 5. Robustness of log-derived worker rankings | Not triggered: median tau 0.033 and 0.041 against > 0.9 | Not triggered | **Not triggered** | partially-covered; a design precedent exists in physician cost profiling | **Revise**, then Stage 6 as the recommended primary |
| 4. Sampling uncertainty in NYC LL 144 impact ratios | Not triggered: C1 no; C2 59.8% against > about 80% | Not triggered | **Not triggered** | partially-covered; the pooling lever is now shown on real data (Bommasani et al., FAccT 2026) | **Revise**; recommended backup |

---

## 2. Results per idea

### 2.1 Idea 6: "Would the Claim Survive an Error Bar?" (audit of statistical and judge-validation practice)

Sources:
- `idea06/README.md` (pilot)
- `idea06/novelty_deep_check.md` (literature)
- `idea06/results/pilot/stopping_rule.json`
- `idea06/results/pilot/screening_summary.csv`
- `idea06/results/pilot/pilot_timing.csv`
- `idea06/codebook_v0.md`

**What ran.**
- **Sampling frame.** The frame was frozen on 2026-10-19 by `code/build_frame.py`, which ran for 183.2 s (`results/frame/frame_summary.json`). It contains:
  - 3,543 articles from 11 IS journals, 2023-01-01 to 2026-10-19;
  - 84 Springer term hits, 65 of them CC-licensed. These 65 form the Springer-OA stratum, unchanged since 2026-10-05;
  - 777 ACL industry-track papers in seven volumes.

  The IS total was 3,583 on 2026-10-05. `results/frame/frame_decomposition_unbounded_vs_frozen.csv` reconciles the two counts: 29 new records, minus 69 Elsevier records whose issue dates fall after 2026-10-19.
- **Inclusion screening.** The 65 Springer-OA papers were screened at abstract level by one machine-assisted coder: 14 include, 7 borderline, 44 exclude.
- **Pilot coding.** A seeded draw (seed 20261015) took 10 Springer-OA papers and 10 ACL papers.
  - The papers were coded against `codebook_v0.md` using keyword-in-context and targeted reading. This took 726 s of machine time, a mean of 23.8 s per Springer paper and 48.8 s per ACL paper.
  - 10 of the 20 papers passed inclusion: 1 Springer and 9 ACL.
- **Survival calculator.** A standard-library survival calculator implements four models: M1 binomial, M2 paired and clustered bounds, M3 run-to-run band, M4 Beta-Binomial. It agrees with statsmodels to within 1.1e-16 and with a numpy Monte Carlo to within 0.38 pp (`results/pilot/calc_validation.csv`). It was run on 5 rule-based headline claims and 5 alternative cells.
- **Deep novelty check** (05:32-06:00 UTC). It covered:
  - 12 documents (10 at full-text depth, read in the sections cited);
  - Semantic Scholar forward chasing of Bean et al. (145 citing works), Miller (172), Bowyer et al. (27) and Groß (7);
  - a crawl of 4,564 AIS proceedings titles (ICIS 2023-2025, ECIS 2023-2026, AMCIS 2024-2026, PACIS 2024-2025), with 44 flagged titles and 7 abstracts read;
  - a Crossref enumeration of 8,490 records from 17 IS journals and HICSS;
  - 20 WebSearch and 16 arXiv API searches; 82 queries and legs in total (`novelty_deep_check.md` §8).

**Stopping rule** (`02_candidate_ideas.md` §4.1): *"stop (or demote to a CAIS methods essay) if any of the following holds after the pilot and the eLibrary search: a published IS-venue audit of statistical or judge-validation practice in LLM papers is found; fewer than 30% of pilot papers permit RQ2 (no n or no accuracies) and the Springer-OA stratum after inclusion screening is below 25 empirical papers; or no second coder has been secured within four weeks and no AIS eLibrary access is obtainable"*.

| Criterion | Threshold | Value | Outcome |
|---|---|---|---|
| 1. Published IS-venue audit of statistical or judge-validation practice in LLM papers | any found | None in 4,564 AIS proceedings titles, 8,490 Crossref records, 20 WebSearch and 16 arXiv searches, or the Semantic Scholar forward legs. The closest IS item, Ahmed and Husna Tamanna (AMCIS 2025), was readable at abstract level only and is descriptive there. | **Not triggered**, within search limits (`novelty_deep_check.md` §6) |
| 2a. Share of pilot papers that permit RQ2 | < 30% | **15% (3/20)**, strict reading, pre-specified primary. 25% (5/20) under the intermediate reading, which is post hoc. 35% (7/20) under the loose reading, the pre-specified secondary. | Holds under the primary reading; fails under the secondary |
| 2b. Springer-OA stratum after inclusion screening | < 25 empirical papers | **14** (primary); 13 to 21 under the other readings | Holds under every reading |
| 2. Both 2a and 2b | both | Both hold under the primary readings | **Holds** |
| 3. No second coder within four weeks **and** no AIS eLibrary access | both | No second coder is secured (author decision); the four weeks have not elapsed; no eLibrary access (search 403, PDFs behind Cloudflare and a subscription) | **Undetermined** |
| **Rule (any of 1 to 3)** | any | Criterion 2 holds | **Triggered** |

The rule is applied "after the pilot and the eLibrary search". The eLibrary keyword search itself returned HTTP 403, so that step was met only by a substitute: a browse-page crawl of 4,564 titles plus Crossref (`idea06/novelty_deep_check.md` §3a). Criterion 2 does not depend on that search.

**Other pilot findings** (exploratory, small n; `idea06/README.md` §4-5).
- **The Springer half drives 2a.** 9 of the 10 drawn Springer papers fail inclusion, so 0 of 10 permit RQ2. The ACL papers give 3, 5 and 7 of 10 under the three readings. Among the 10 included papers the strict share is 3 of 10. This is supplementary only, because the rule's denominator is all pilot papers.
- **Survival.** Of the 5 rule-based headline claims, 1 survives M1, the M2 paired upper bound and M4; it has n = 100,400. None survives the 15-point run-to-run band (M3). This shows that the pipeline works; it is not an estimate of the survival rate.
- **Reporting practice.** Among the 10 included papers, 1 reports any uncertainty (coded Y). 2 use an LLM judge, and neither validates it against humans.
- **Inconsistencies.** Coding surfaced reporting inconsistencies in three ACL papers (A03, A04, A09). These are unconfirmed with their authors.

**Deep novelty outcome: partially-covered.** The label is unchanged, but the uncovered space is smaller than on 2026-10-05 (`novelty_deep_check.md` §5).

New close prior art:
- **Pathade, Pawar, Patil** (arXiv 2609.25173, Sep 2026). They code variance, repeated runs, decoding and judge-human agreement together across 259 agentic-security papers. 58.0% of a hand-coded sample of 50 report neither variance nor repeated runs, and 29.7% of the papers that use a judge check it against humans.
- **Singh** (arXiv 2608.15046). A preregistered evidential-sufficiency audit of 17 published LLM equivalence claims.
- **The DKFZ "Claims Reloaded" estimator.** It already converts reported n and accuracies into a probability that a claim is false, which overlaps the planned calculator.

Corrections to earlier readings:
- Yang et al.'s "under 8%" uses all 3,334 NLG papers as its denominator. Among papers that use a judge, 37.4% validate it against humans, so H2 is not "close to settled".
- Bean et al.'s 16.0% counts "uncertainty estimates or statistical tests".
- Siddiq et al.'s venue question is about venue policies, not reporting.

IS venues already publish statistical-practice audits of non-LLM papers: the ISR 2026 p-hacking audit (DOI 10.1287/isre.2024.1365) and CAIS 2025 DERP (DOI 10.17705/1cais.05706). The paper therefore cannot be framed as a first IS reporting audit.

Within these searches, what remains uncovered is the combination applied to IS and industry-track papers:
- per-claim re-analysis on each paper's own n;
- judge validation coded together with its protocol fields;
- the comparison of IS against industry tracks and across years.

**Literature stop condition: not triggered.** Limits on that decision:
- The AIS full-text search and PDFs are blocked, so only titles and 7 abstracts were screened.
- The AMCIS 2025 paper was read at abstract level only.
- OpenAlex forward legs for all six seeds are not done.
- Semantic Scholar forward legs for Christodoulou et al. and "Awes, Laws, and Flaws" are not done.

**Deviations.** Full lists are in `idea06/README.md` §6 and `novelty_deep_check.md` §8.
- All seven ACL volumes were used for the draw.
- An upper date bound froze the frame.
- Markup was stripped before term matching.
- The 11 codebook entries were reconciled to 14 fields.
- The intermediate RQ2 reading and the table-cell rule for headline claims were added post hoc.
- Both M3 and M4 were run, and the "15%" band was read as percentage points.
- Screening was done at abstract level.
- The Springer frame was not reconciled against OpenAlex.
- The AIS keyword search was replaced by a browse-page crawl plus Crossref.
- dblp was replaced as a source.
- AMCIS and PACIS were added.

**Blockers.**
- Criterion 3 depends on the author: a second coder and AIS eLibrary access.
- No human has verified any pilot code, so no kappa exists.
- AIS full texts cannot be reached from the container.

**Recommendation: pivot.** The rule fired on its pilot criterion under the pre-specified primary readings. Its stated consequence is "stop (or demote to a CAIS methods essay)". Three further facts point the same way:
1. **The IS stratum is small.** The stratum the paper exists to study holds 14 empirical open-access papers (13 to 21 under other readings). Without AIS eLibrary access to restore ICIS/ECIS, that is too few for a JAIS or BISE paper about IS practice.
2. **The deep check narrowed the design-combination claim** (Pathade et al.; Singh; the DKFZ estimator).
3. **The human resources it needs are not in place.**

The outcome does depend on one reading: under the pre-specified secondary reading of "permit RQ2" the rule does not fire on criterion 2. Also, 2a is driven by drawing the pilot from unscreened term hits. Re-drawing from screened papers would change the rule's input. It must be recorded as a post hoc amendment, and it does not undo today's outcome under the rule as written.

I recommend that the author not keep idea 6 as a primary or backup candidate. If the author wants to keep this line of work, the rule's fallback is a CAIS methods essay. That essay would still need a human second coder.

### 2.2 Idea 5: robustness of log-derived worker rankings

Sources:
- `idea05/README.md` (pilot)
- `idea05/novelty_deep_check.md` (literature)
- `idea05/results/stopping_rule.csv`
- `idea05/results/bpic20{17,19}_tau_summary.json`
- `idea05/results/bpic20{17,19}_placebo_summary.json`
- `idea05/results/bpic20{17,19}_variance_decomposition.csv`
- `idea05/results/wall_clock.json`

**What ran.**
- **Data.** Two logs were converted to Parquet:
  - BPI 2017 (4TU General Terms of Use; sha256 `183c5e51…6f8249`, md5 equal to 4TU's).
  - BPI 2019 (CC BY 4.0; 728,558,522 bytes downloaded in 22.4 s; sha256 `af63bc68…6baae7`, md5 equal to 4TU's).
- **Resource fields** (`results/resource_fields.json`).
  - BPI 2017 has 149 `User_<n>` values, not 150: the card counted the XES default `UNKNOWN`. User_1 has 148,404 events (12.34%).
  - BPI 2019 has 607 human `user_*` accounts and 20 labelled `batch_*` accounts. The value `NONE` appears on 398,770 events. 327 out-of-period events were dropped.
- **Factorial.** The full 405-cell factorial (metric 5 x attribution 3 x window 3 x idle gap 3 x case-mix 3) collapses to 117 distinct score vectors. It ranked 140 workers on BPI 2017 and 307 on BPI 2019 at N_min = 100. Around it ran:
  - 500 case-bootstrap replicates;
  - 20 placebo label shuffles;
  - system-account sensitivity analyses;
  - an automated-account detector calibrated on BPI 2019's labels.
- **Run time.** The whole pipeline took about 21 min on the shared 4 vCPU. The bootstrap took 148.5 s (BPI 2017) and 513.6 s (BPI 2019); the placebo 98.1 s and 166.1 s. A re-run at B = 20 reproduced every deterministic output byte for byte.
- **Deep novelty check** (06:01 to about 07:00 UTC). It covered:
  - 14 documents (10 at full-text depth), including the 4TU General Terms of Use;
  - a Crossref enumeration of 1,360 ICPM, BPM, CAiSE and Process Science papers from 2022-2026, with 139 titles read by hand, 209 abstracts screened and 17 abstracts read;
  - 38 BPI Challenge 2017 and 2019 reports (1,019 pages), screened;
  - 86 ICIS future-of-work titles, read;
  - Semantic Scholar forward chasing of Pika et al. 2017 (62 citing works), Saisana et al. (911), Adams et al. (162), Nakatumba and van der Aalst (121) and Pika et al. 2014 (37);
  - Crossref backward chasing of Martin and Beerepoot (99 references);
  - 27 WebSearch and 8 arXiv queries.

**Stopping rule** (`02_candidate_ideas.md` §4.2): *"stop the confirmatory framing (and reduce the idea to a reassurance note or merge it into another paper) if, after excluding labelled or detected system accounts and resources below the pre-registered minimum-event threshold, the median Kendall tau across defensible configurations exceeds 0.9 on both BPI 2017 and BPI 2019 and bottom-quintile reclassification under case-mix adjustment is below 10% on both; also stop if the proceedings sweep finds a rank-stability study of resource measures on public logs"*.

No preregistration exists yet, so the "pre-registered minimum-event threshold" was read as N_min = 100, fixed in code before any tau was computed. The excluded system accounts are User_1 (BPI 2017) and the 20 labelled batch accounts (BPI 2019), because the detector failed (`idea05/README.md` §6, deviations 3 and 6).

| Criterion | Threshold | Value (95% case-bootstrap percentile interval) | Outcome |
|---|---|---|---|
| 1a. Median tau, BPI 2017 (117 distinct configurations; primary) | > 0.9 | **0.033** [0.017, 0.050]; 405-cell version 0.038 | Not met |
| 1a. Median tau, BPI 2019 | > 0.9 | **0.041** [0.032, 0.047]; 405-cell version 0.038 | Not met |
| 1b. Bottom-quintile reclassification under case mix, BPI 2017 (share of bottom quintile; primary) | < 10% | **17.9%** [17.4%, 25.0%]. Alternative reading (share of all workers): 7.1% | Not met (primary); met (alternative) |
| 1b. Same, BPI 2019 | < 10% | **27.3%** [24.6%, 29.0%]. Alternative reading: 9.4% | Not met (primary); met (alternative) |
| Empirical clause: 1a and 1b on both logs | all four | 1a fails on both logs under every reading and every sensitivity computed. The highest median tau in any variant is 0.051 (BPI 2017) and 0.069 (BPI 2019). 0 of 500 bootstrap replicates exceed 0.9. | **Not triggered** |
| 2. Proceedings sweep finds a rank-stability study of resource measures on public logs | any found | None among 1,360 papers, 38 BPI Challenge reports, 86 ICIS future-of-work titles and about 1,300 forward citations | **Not triggered** (`novelty_deep_check.md` §6) |
| **Rule (either clause)** | | | **Not triggered** |

The pilot README marks clause 2 and the 4TU terms as open. The novelty check, written after it, assessed both.

**Other pilot findings** (exploratory; `idea05/README.md` §5).
- **The rule's quantity is a weak estimand.**
  - The all-pairs median is dominated by pairs with different metrics, whose median tau is about 0 (-0.0004 and 0.0005).
  - On both logs it lies inside the placebo range: placebo mean 0.052 [0.032, 0.078] and 0.047 [0.033, 0.060].
  - Within one metric, the median tau is 0.488 (BPI 2017) and 0.503 (BPI 2019). Both are above all 20 placebo values: 0.338-0.394 and 0.405-0.423.
- **Variance decomposition.** Pooled shares of the variance in workers' rank percentiles across the 405 cells, computed on 112 and 136 complete-case workers:

  | Factor | BPI 2017 | BPI 2019 |
  |---|---|---|
  | Metric | 0.538 | 0.567 |
  | Attribution | 0.044 | 0.043 |
  | Window | 0.014 | 0.005 |
  | Idle gap | 0.002 | 0.001 |
  | Case-mix | 0.009 | 0.041 |
  | Interactions | 0.394 | 0.343 |
- **Attribution alone yields near-independent rankings of completed-case counts.** Last touch versus first touch gives tau 0.021 [-0.003, 0.026] on BPI 2017 and 0.185 on BPI 2019.
- **Case-mix confounding.** On BPI 2017, workers' mean expected case effort correlates with unadjusted rework at Spearman -0.768. After activity adjustment the correlation is -0.252.
- **The system account reshapes human rankings.** With User_1 in the BPI 2017 attribution pool, it holds 64.8% of completed cases under first touch. Including it changes the human ranking on completed cases attributed by last touch to tau 0.663 against the ranking without it.
- **The pre-specified automated-account detector failed.** On BPI 2019's labels its per-account precision is 0.087 (recall 0.85). A cross-validated logistic regression reaches 0.140.
- **H3** (shorter windows are less stable) gives mixed readings across three views.

**Deep novelty outcome: partially-covered.** The label is unchanged; the claim is narrower (`novelty_deep_check.md` §5).
- **Physician cost profiling already has the design for individual professionals:**
  - Thomas and Ward 2006 cross 3 attribution rules with 6 outlier treatments.
  - Mehrotra et al. 2010 vary 12 attribution rules; 17-61% of physicians change cost category.
  - Timbie et al. 2013 vary the adjustment; 1.1% of physicians move more than 2 percentiles. This is a counter-example for H2.
  - Kaye et al. 2019 vary the time window.
- **HR auditing.** Rhea et al. 2022 (DMKD) already provide a stability-audit framework and library for algorithmic HR tools.
- **Inside process mining:**
  - Braakman et al. 2025 found weak convergence between log-derived worker measures and survey scales.
  - Klijn et al. 2024 and Leribaux et al. 2025 measure actor-behaviour performance on loan-process and BPIC 2017/2019 logs. Leribaux et al. treat User 1 as an actor.
  - The BPI Challenge reports rank or flag individual users from single definitions, without stability checks. This is motivating evidence.
- **Claimable contribution.** No study found in the searches treats the scoring configuration of event-log worker measures as a crossed factorial with rank-agreement, reclassification and variance-decomposition statistics and an open audit artefact. The contribution is a transfer of physician-profiling misclassification analysis and composite-indicator sensitivity analysis to process mining, plus that artefact.

**Literature stop condition: not triggered.** Residual risk:
- 85% of the 1,360 sweep papers were screened at title level only.
- The ICPM 2025 workshop volume is not in Crossref.
- OpenAlex legs and the Semantic Scholar keyword search are not done.
- dblp was unavailable.

**Deviations.** Full lists are in `idea05/README.md` §6 and `novelty_deep_check.md` §8.
- **Definitions.** Metric, completion, attribution scope, window, idle-gap and case-mix definitions were all written during the run.
- **Defensible cells and threshold.** All 405 cells were treated as defensible. N_min = 100 was chosen in this run, before any tau was computed.
- **Analysis set.** It was switched to pairwise-complete after a test run had already shown the complete-case BPI 2017 medians.
- **Tie rule.** It was switched to inclusive ties after 107 of 307 BPI 2019 users were found tied at zero.
- **BPI 2017 exclusion.** It became User_1 only, after the pre-specified detector failed.
- **Additional runs.** The factorial, bootstrap and placebo were also run on BPI 2019.
- **Interval caveat.** The bootstrap intervals are conditional on fixed case-mix fits, and the percentile intervals are biased toward lower agreement.
- **Novelty check.** dblp was replaced by Crossref enumeration. Some early calls in the novelty session sent a personal contact e-mail (deviation 7; see section 6).

**Blockers.**
- **4TU General Terms of Use**, now read in full by the novelty check:
  - remixing is allowed only for non-commercial purposes (Art. 4b);
  - publications must be reported to 4TU (Art. 3);
  - datasets with personal data are limited to scientific research under the VSNU code (Art. 7).

  Per-pseudonym BPI 2017 rankings stay out of the repository until a data-handling rule is written.
- There is no fit-for-purpose automated-account detector.
- The AI Act timing argument rests on a snippet-only report of a postponement to December 2027, which is unverified.

**Recommendation: revise, then proceed to Stage 6.** The rule is not triggered on either clause, so by the plan's own test the confirmatory framing continues. The pilot shows four things to fix first:
- the rule's quantity cannot carry the paper: it sits at placebo level and mainly shows that the five metrics measure different things;
- the detector must be replaced;
- the novelty claim must be restated as a transfer from physician profiling;
- BPI 2017 and BPI 2019 have now been analysed, so confirmatory claims must rest on further logs.

The revisions are listed in section 5.

### 2.3 Idea 4: sampling uncertainty, exclusion rules and pooling in NYC LL 144 impact ratios

Sources:
- `idea04/README.md` (pilot)
- `idea04/novelty_deep_check.md` (literature)
- `idea04/results/run_metadata.json`
- `idea04/results/interval_summary_variants.csv`
- `idea04/results/interval_by_group_size.csv`
- `idea04/results/aclu_code_inference_check.csv`

**What ran.**
- **Corpus.** The ACLU "Auditing the Audits" repository was cloned at commit `cef7c273…`. `audits_full.csv` has 4,507 rows x 46 columns, covering 116 audits in 44 reports (sha256 `69fd290f…bbf85e`). Two further sources were used:
  - the ACLU tracker, at commit `5fca36bb…`;
  - the OSF extraction (449 rows), for a cross-check.

  The UGESP text (29 CFR 1607.4, XML) was also read.
- **Criterion 1 check.** All three ACLU code files were read line by line, with a keyword scan alongside.
- **Pipeline.** The steps were:
  - exclude HackerRank;
  - keep one rate definition per audit;
  - de-duplicate tables by identical counts (49 of 332 tables dropped);
  - apply a consistency filter;
  - recompute the comparator among groups holding at least 2% of known applicants.

  This left 1,157 usable ratios: 854 employer-posted and 303 vendor-posted.
- **Statistics.** Four interval methods were computed:
  - Katz, fixed as primary before any result was computed;
  - Clopper-Pearson with a Bonferroni split;
  - a stratified bootstrap with 2,000 resamples;
  - a Jeffreys posterior with 20,000 draws.

  Alongside them: the UGESP four-fifths flag, a two-proportion z test and Fisher's exact test.
- **Data-scope coding.** Employer-posted audits were coded post hoc from report text (`code/data_scope_coding.csv`).
- **Run time.** The pilot took 31.4 s and run.sh 55 s. An independent re-run reproduced all 25 CSVs byte for byte.
- **Deep novelty check.** It covered:
  - 18 documents (9 at full-text depth);
  - the FAccT 2026 (325 papers), AIES 2026 (265) and FAccT 2025 (217) tables of contents;
  - Semantic Scholar forward chasing of Gerchick et al. (16 citing works), Wright et al. (50), Roth et al. (58) and Collins and Morris (44), plus D-hacking (16), Ferrara et al. (2), Morris and Lobsenz (0) and Switzer et al. (0); the Lam et al. leg was not done (`idea04/results/novelty_chase_log.csv`);
  - 26 WebSearch, 8 arXiv and 9 Crossref queries.

**Stopping rule** (`02_candidate_ideas.md` §4.3):
- *"stop Part 1 if the ACLU code already computes sampling intervals or if, after de-duplication, more than about 80% of employer-level ratios have 95% intervals excluding 0.8"*;
- *"stop the whole idea if an I-O or FAccT paper is found that simulates the LL 144 exclusion and pooling levers on the published corpus"*.

| Criterion | Threshold | Value | Outcome |
|---|---|---|---|
| Part 1, C1. ACLU code already computes sampling intervals | any | **No.** The code computes only deterministic missing-data bounds (`helpers.R` lines 37-129) and point-estimate shares (`paper_results.Rmd` lines 159-196 and 475-486). The keyword scan found 0 genuine hits. | **Not triggered** |
| Part 1, C2. Employer-level ratios after de-duplication whose 95% interval excludes 0.8 | > about 80% | **59.8% (511 of 854)**: set E1 (employer-posted), Katz, pre-specified. Other methods on E1: 45.0%, 58.8% and 58.9%. Post hoc E5 (employer's own data): 55.2%. Range across employer-level variants and methods: 42.8% to 83.3%. Only S6 exceeds 80%: the 108 ratios whose counts are recorded as integers, with 3 of 4 methods. | **Not triggered**. S6 is a data-quality subset, not the rule's population. |
| Whole idea. An I-O or FAccT paper simulates the LL 144 exclusion and pooling levers on the published corpus | any found | None. Bommasani et al. (FAccT 2026) cover pooling only, empirically, on proprietary data. Gerchick et al. run no simulation. The I-O simulations pre-date LL 144. | **Not triggered** (`novelty_deep_check.md` §6) |
| **Rule** | | | **Not triggered** |

**Other pilot findings** (`idea04/README.md` §5).
- **Pooled tables.** The auditors' own report text shows that 662 of the 854 employer-posted ratios come from multi-employer pooled tables. A binomial interval is not a valid uncertainty model for these. DCI states that the aggregated ratios "cannot be computed directly from the aggregated selection rates".
- **Group size.** Among audits of employers' own data (E5, post hoc), informativeness is bimodal by the size of the smaller group:

  | Smaller group | Ratios | Share excluding 0.8 |
  |---|---|---|
  | Fewer than 100 applicants | 64 | 4.7% |
  | 1,000-4,999 | 48 | 91.7% |
  | 5,000 or more | 34 | 100% |
- **Reconstructed counts.** Of 3,144 rows with a selected count, 552 hold integers. Of the 2,592 non-integer rows, 2,588 equal N x the reported rate, so most counts were reconstructed from rounded rates.
- **Comparator.** Recomputing the comparator flips 99 four-fifths classifications in E1, 89 of them to below 0.8. The share of ratios below 0.8 rises from 14.0% to 23.2%.
- **Excluded populations.** For race tables, the median unknown share is 8.1% in employer-own-data audits, against 19.6% in vendor-posted audits (74.0% when pooled). The 2% rule removes at most 4.6% of known applicants in any kept table.
- **OSF cross-check.** Impact ratios agree in 20 of 20 sampled rows. The ACLU N was found in the employer PDF text for 15 of 15 checkable rows.

**Deep novelty outcome: partially-covered.** The label is unchanged; the claim is narrower (`novelty_deep_check.md` §5).
- **Bommasani et al.** (FAccT 2026, DOI 10.1145/3805689.3812400) analyse 4.2 million pymetrics applications.
  - Vendor-pooled impact ratios are all above 0.8, yet per-position tests find adverse impact in 10.62% of positions for Black applicants and 5.32% for Asian applicants.
  - The paper also criticises DCWP's pooling example.
  - The idea's pooling arm can therefore only quantify this mechanism on the published corpus; it cannot claim to discover it.
- **Settled I-O practice.** Impact-ratio CIs, Mantel-Haenszel and Breslow-Day aggregation, and the origin of the 2% rule are established I-O practice (TAC report 2010). Ferrara et al. 2025 cover the disparate-impact ratio. Jacobs et al. 2013 show that significance-based rules make pool size dominate.
- **Existing reanalysis.** A vendor blog (Noon Research, 2026-10-16) published a point-estimate reanalysis of the same ACLU file, so a "first reanalysis" claim is ruled out.
- **Still unrecorded within the searches:**
  - sampling intervals, posteriors and UGESP tests attached to the published ratios;
  - the applicant shares removed by the 2% rule;
  - a combined simulation of the five LL 144 levers, calibrated to the corpus;
  - a measured manipulation range on real reports.

**Literature stop condition: not triggered.** Residual risk:
- OpenAlex forward lists are not done for any seed.
- Semantic Scholar forward citers of Lam et al. are not done.
- Morris and Lobsenz have 38 Crossref citers, but Semantic Scholar returned 0.
- SIOP programmes and I-O journal tables of contents were not enumerated.

**Deviations.** Full lists are in `idea04/README.md` §7 and `novelty_deep_check.md` §8.
- **De-duplication.** It was operationalised by identical counts; the literal plan key is reported as sensitivity S2 (60.1%).
- **"Employer-level".** It was pre-specified as employer-posted (E1). The post hoc E4, E5 and M sets were added after reading the reports.
- **Interval methods.** Katz is asymptotic; Clopper-Pearson-Bonferroni is the exact option.
- **2-SD rule.** The 2-SD test was implemented as a pooled z test, because the UGESP text read does not define a 2-SD rule.
- **Additional analyses.** Several analyses not in the plan were added.
- **OpenAlex legs.** The remaining legs were skipped after the budget message.

**Blockers.**
- **Licence.** The licence of `audits_full.csv` is ambiguous: neither repository has a LICENSE file, and both READMEs say only that "The tracker in this repository is licensed under CC BY-NC 4.0". The licence email to analytics_inquiry@aclu.org has not been sent; it is an author action.
- **Unread reports.** The JetBlue and Citizens reports could not be read, and Cigna's tables are images.
- **Scope.** Parts 2 and 3 were not run.
- **Venue fit.** FAccT is a conference, with an APC of USD 250 for ACM members or USD 350 for non-members, or a non-archival option. JRC's APC terms are not shown.

**Recommendation: revise; recommended backup.** The rule did not trigger, so Part 1 continues. The pilot changes the headline, though:
- the population for the sampling-uncertainty claim should be audits of employers' own data;
- the group-size bimodality becomes the main result;
- most employer-posted ratios come from multi-employer pools that cannot carry a sampling interval at all.

Part 2 must add the aggregation lever and the reconstruction of counts from rounded rates. Its venues (FAccT and JRC, with an IS secondary route at JAIS, ISF or I&M) do not meet the top-journal goal directly. That is why idea 4 is the backup, not the primary.

---

## 3. Recommended primary and backup (a recommendation for the author to confirm, not a decision)

**Primary: idea 5, revised.** The reasons, each tied to the record:
1. **Its rule passed.** Its stopping rule was assessed on both clauses and was not triggered. Idea 6's rule fired.
2. **It meets every stated constraint.**
   - No participants and no LLM.
   - No fee at its primary venue (BISE's subscription route).
   - Public data with known terms: BPI 2019 is CC BY 4.0, and the BPI 2017 4TU terms have been read.
   - Compute is measured in minutes: about 21 min for two logs on 4 vCPU (`idea05/results/wall_clock.json`).
3. **The pilot found structure beyond "the metrics are unstable":**
   - a dominant metric factor (54-57% of rank-percentile variance);
   - near-independent rankings under different attribution rules;
   - case-mix confounding of the rework and deadline metrics;
   - a system account that reshapes human rankings;
   - a placebo design that separates within-metric signal from shuffled labels.

   These are the answers that the 2026-10-05 synthesis needed to the "obviously unstable" objection.
4. **Venue fit** (`research/04_journals/venue_landscape.md` (a), (c)).
   - BISE and the process-mining cluster are primary cells.
   - MISQ, ISR, JMIS, EJIS and ISJ are secondary cells that need a theory thread.
   - ISF's "Unethical Labour Practices" collection (deadline 2027-02-15) is a further no-fee route.

**Limit on the top-journal goal.** For idea 5 that goal is met only through a secondary cell. The realistic first target is BISE (Group 2). A Group 1 submission needs the theory argument to carry the paper. That argument is that reliability is a precondition for using scores even as screening instruments; it draws on Goldstein and Spiegelhalter, on Rhea et al., and on the deployer-oversight hook, whose AI Act timing has still to be verified. Of the Group 1 venues, EJIS's "exploitation of new data" wording is the most measurement-friendly; ISJ requires theory.

**Backup: idea 4, revised.**
- It is the quickest complete paper: the pilot takes 31.4 s and is deterministic. Its rule was not triggered, and it has a substantive reframed headline.
- Its venues are CS (FAccT, JRC) and its corpus licence is unresolved.
- It shares no resource with idea 5, so it can also run in parallel as a secondary paper. That should wait for the ACLU licence answer.

**Idea 6** is not recommended as primary or backup, because its rule was triggered (section 2.1).

The 2026-10-05 reserves (idea 3, idea 8 Part B) were not re-assessed in Stage 4.

---

## 4. What the author must decide now

Items kept from `research/02_candidate_ideas.md` section 5, with the original numbers in brackets, updated by the pilots:

1. **[7] Which idea goes forward.**
   - Confirm idea 5 as primary and idea 4 as backup, or choose otherwise.
   - Decide what happens to idea 6 under its triggered rule. The options are:
     - stop;
     - demote it to a CAIS methods essay;
     - amend the pilot input with a documented change, such as re-drawing from screened Springer papers. Such an amendment is post hoc and does not reverse today's outcome.
2. **[1, 2] Discipline and tier.** Confirm "IS first" for idea 5, with BISE as the realistic first venue and Group 1 only as a stretch that needs a theory thread. Idea 4 would then be the CS paper (FAccT or JRC).
3. **[4] APC.**
   - Idea 4 at FAccT: USD 250 for ACM members or USD 350 for non-members, or the non-archival option.
   - Idea 5 at Process Science: GBP 1,340 / USD 1,890 / EUR 1,590 plus VAT. This applies only to a process-cluster version.
   - JRC's APC is not shown.

   "No APC" routes idea 5 to BISE or ISF and idea 4 to FAccT's non-archival option.
4. **[8] Preregistration and AIS membership.**
   - An OSF preregistration for idea 5 before the full run (section 5.2).
   - AIS membership matters only if idea 6 is kept or a JAIS or CAIS submission is planned. It avoids the USD 75 non-member fee and is the route to eLibrary PDFs.
5. **[3] Second coder.**
   - Not needed for idea 5.
   - Needed for any form of idea 6.
   - Recommended for idea 4's data-scope coding: the idea-4 pilot proposes two independent coders for the confirmatory version, and 7 of its 20 report groups rest on inference.

**Dropped from section 5:**
- [5] multi-day local compute: ideas 4 and 5 need minutes to hours (section 5.3);
- [6] a Python 3.12 or WSL2 GPU environment: no recommended idea needs a GPU.

Both matter again only if idea 8 or ideas 1-3 are revived.

**New author actions raised by Stage 4:**

6. **Headline estimand for idea 5.** Within-metric agreement and the one-factor contrasts as primary, with the rule's all-pairs median still reported as stated. This research-direction call is needed before preregistration.
7. **Licence email for idea 4** to analytics_inquiry@aclu.org. No row-level derived data are published until it is answered.
8. **Data-handling rule for idea 5** under the 4TU terms: aggregates and re-hashed identifiers only, and publications reported to 4TU under Art. 3.
9. **Personal e-mail address in committed files** (section 6, item N1). Decide whether to scrub it from two scripts and two logs, and whether to rewrite the pushed history. A rewrite needs a force push, which is the author's call.
10. **API keys.** Decide whether to obtain free OpenAlex and Semantic Scholar API keys. Each key needs an e-mail address, and therefore the author's consent. The keys would complete the citation legs recorded as "not done" in all three novelty checks.

---

## 5. Stage 6 next actions for the recommended primary (idea 5)

Human-time figures below are labelled by their basis. The pilot measured machine time only.

### 5.1 Protocol work (before preregistration)

- **P1. Data-handling rule.** Write it under 4TU Art. 3, 4b and 7:
  - release distributions and configuration-level aggregates only;
  - re-hash identifiers;
  - report publications to 4TU;
  - apply the same rule to BPI 2019 for consistency, as the pilot did.
- **P2. Further logs.** Confirm the resource fields and download the further logs:
  - BPI 2013 incidents, 2015 (five municipalities) and 2018 (the stress case);
  - after checking whether the field holds persons or roles: 2012, 2014, 2020 (five sub-logs), Helpdesk and RTF.

  That is up to about 16 further logs or sub-logs. Each needs an `idea05lib.LOGCFG` entry with a log-specific completion rule, deadline and rework definition where the log supports one.
- **P3. Replace the automated-account detector.**
  - Use activity-mix and inter-event-regularity features.
  - Report per-account and event-weighted precision.
  - Validate on BPI 2019's labels and on BPI 2018.
  - Fix an acceptance criterion in advance. If no detector meets it, exclude only publisher-labelled or plan-named accounts and report the detector-flagged sets as sensitivities.
- **P4. Add what the novelty checks require:**
  - per-worker split-half reliability and rank intervals (Goldstein and Spiegelhalter);
  - Gu-Koenker selection as a comparator to raw bottom quintiles;
  - a workload covariate with its own pre-registered window (Nakatumba and van der Aalst);
  - four-fifths-style ratios across discovered roles;
  - per-replicate case-mix refits with basic or BCa intervals;
  - at least one more null, such as event-level or within-slot shuffles.
- **P5. Verify before citing.** These items are snippet-only:
  - the AI Act "Digital Omnibus" postponement;
  - Shahian et al. 2010;
  - Atteberry and Mangan 2020.

  The physician-profiling numbers used as comparators were read at abstract level and must be labelled so.

### 5.2 Preregistration content (OSF)

- **Framing.** A configuration-factorial reliability audit of event-log worker scores. Physician-profiling designs are the explicit template: Thomas and Ward 2006; Mehrotra et al. 2010; Timbie et al. 2013; Kaye et al. 2019.
- **Logs.**
  - BPI 2017 and BPI 2019 are declared pilot and calibration logs whose results are already known. Confirmatory statements rest on the further logs from P2.
  - State the inclusion criteria for a log: a person-level resource field and a minimum number of ranked workers.
- **Estimands and hypotheses.**
  - *Primary:* within-metric median tau, and the one-factor contrasts (attribution, window, idle gap, case mix), each against the placebo distribution.
  - *Reported as stated:* the section 4.2 all-pairs median tau.
  - *Reclassification:* both readings, the bottom-quintile share and all workers.
  - *Variance decomposition:* per factor.
  - *H2* stays open, because of the Timbie et al. counter-example.
  - *H3:* name which of the three window views is primary.
- **Fixed analysis choices:**
  - the metric definitions in `idea05/README.md` §4, plus log-specific deadline and rework rules;
  - N_min = 100, with 1, 20 and 500 as sensitivities;
  - inclusive ties;
  - the pairwise-complete analysis set, with complete-case as a sensitivity;
  - the exclusion rule from P3;
  - B = 500 with per-replicate refits;
  - the touch-unit placebo plus the added null;
  - the seed family 20261015.
- **Comparators.** External reference points, labelled with their access depth:
  - Mehrotra et al.: 17-61% reclassified across attribution rules;
  - Timbie et al.: 1.1% of physicians moved more than 2 percentiles;
  - Kaye et al.: 13-39% persistence of top-quartile spenders.
- **Interpretation rule.** Goldstein and Spiegelhalter: rankings are "screening instruments, but not definitive judgements".
- **Data handling and deviation policy.** Use P1 for data handling. Report every deviation with its timing relative to seeing results, as the pilots did.

### 5.3 Full run: compute estimates traced to the pilot timings

Source for all measured values: `idea05/results/wall_clock.json`. The arithmetic is in section 7.

| Item | Measured in the pilot (4 vCPU, shared with another pilot) | Extrapolation for Stage 6 | Assumption |
|---|---|---|---|
| Download | BPI 2019: 728,558,522 bytes in 22.4 s | Negligible per log | 4TU answers |
| Per log at pilot settings: conversion + factorial + B = 500 bootstrap + 20 placebos | BPI 2017: 371.2 s (6.2 min). BPI 2019: 851.5 s (14.2 min). Both logs: 1,222.7 s (20.4 min). | 16 further logs: about 1.7-3.8 h | Each log is no larger than BPI 2019; time scales linearly |
| Per-replicate case-mix refits, upper bound (the whole factorial step re-run in each replicate on 4 processes) | Factorial step: 34.8 s (BPI 2017) and 43.8 s (BPI 2019) | Adds about 73-91 min per log, giving about 1.3-1.8 h per log in total, or about 21-28 h for 16 logs on 4 vCPU | Upper bound: only the fits need repeating |
| Logs larger than BPI 2019 (BPI 2018 is the named stress case) | Not timed | Unknown | Time it in P2 before scheduling |
| Feasibility estimate of 2026-10-05 for the author's 20-core PC | n/a | 4-10 h wall-clock, 50-120 CPU-h | Not re-tested |

Disk: about 30 GB free in the container. BPI 2019 alone is 728.6 MB raw.

### 5.4 Effort and calendar

| Step | Compute (traceable) | Researcher time | Basis |
|---|---|---|---|
| P1 data-handling rule | none | about 0.5 day | judgement; no record measures it |
| P2 log checks and downloads | step 02 took about 10 s for both pilot logs; conversion took 90-128 s per log | 1-2 days | judgement |
| P3 detector | step 03 took about 10 s | 2-3 days | judgement |
| P4 additions | enters the full run (5.3) | 1-2 weeks | judgement |
| Preregistration | none | plan week 3 | `02_candidate_ideas.md` §4.2 calendar |
| Full run, variance decomposition, rank intervals | 1.7-3.8 h at pilot settings; up to about 21-28 h with refits (4 vCPU) | plan weeks 4-5 | §4.2 calendar |
| Audit-artefact packaging and manuscript (BISE; alternatives ISF collection, BPM Management track) | none | plan weeks 6-8 | §4.2 calendar |

- **Calendar.** The plan's weeks 3-8 (six part-time weeks) remain. Add about 2-3 weeks for P2-P4, which the plan did not foresee (judgement). The pilot covered the plan's weeks 1-2 in one day of agent time, which says nothing about human time.
- **Deadline.** The ISF collection deadline of 2027-02-15 is 17 weeks after 2026-10-19.

---

## 6. Integrity items

### 6.1 Items carried from `research/05_critique_2026-10-05.md` (section 4 and the lead's follow-up)

| # | Item (2026-10-05) | Status after Stage 4 | Evidence |
|---|---|---|---|
| 1 | Idea-6 frame counts rested on uncommitted scripts | **Resolved** | The 2026-10-05 follow-up committed the scripts to `research/tools/assessment_2026-10-05/idea06/`. Stage 4 then rebuilt the frame with the committed `idea06/code/build_frame.py`, froze it at 2026-10-19, cached 96 raw responses with sha256 (`idea06/results/frame/raw_manifest.csv`) and decomposed 3,583 to 3,543. Residual: +2 ISR records cannot be attributed, because no DOI list was kept on 2026-10-05. |
| 2 | Idea-2 reference verification never finished | Open | Outside the Stage 4 scope; idea 2 is deprioritised |
| 3 | Idea-3 reference-verification output never pasted | Open | Same |
| 4 | Absolute `/home/user/...` paths in 2026-10-03 files | Open (historical by design) | Stage 4 files also use absolute container paths (`$SCRATCH`, `/home/user/...`). These refer to this container only. |
| 5 | Kelemen 2022 labelled "unverified" in the idea-5 feasibility file | **Resolved in substance** | `idea05/novelty_deep_check.md` §1 read the full text: CEE eDem/eGov Days 2019, pp. 497-504; the DOI was registered in 2022. The feasibility file's label was not edited, because the task scope forbids it. |
| 6 | Idea-7 feasibility and novelty statements differ | Open | Idea 7 was not in Stage 4 |
| 7 | Digest gap numbering depends on convention | Open (cosmetic) | n/a |
| 8 | Nine citation items in `01_literature/verification_pass_2026-10-05.md` | Open | None was re-examined in Stage 4. The OpenAlex and Semantic Scholar limits persisted: the OpenAlex daily budget was exhausted all session. |
| 9 | Venue facts resting on third-party snippets (MISQ, ISR, I&M, IP&M, Patterns, NMI) | Open | No venue page was re-fetched |
| 10 | I-O papers known from metadata only (Roth et al. 2006, Collins and Morris 2008, Switzer et al. 2016) | **Partly resolved** | Roth et al. and Collins and Morris were upgraded to abstract depth; Roth et al. also via a third-party course outline. Switzer et al. remain metadata only. None shows signs of varying a 2%-type exclusion or pooling. Pre-2023 papers cannot meet the "published corpus" part of the idea-4 stop condition (`idea04/novelty_deep_check.md` §6). The full texts are still unread. |
| 11 | Sync state of the Windows working copy `E:\research 2` unverified | Open | This session ran in the cloud container on `claude/peaceful-cori-ny59q5` (HEAD `d5507c7` at 06:59:51 UTC). The Windows copy was not examined. |
| 12 | Provenance note about `digest.json` | Open (cosmetic) | n/a |
| F1 | Idea-4 micro-benchmark script lost (follow-up) | **Superseded** | The Stage 4 idea-4 pilot is committed (`idea04/code/ll144_pilot.py`, `run.sh`) and deterministic. The 2026-10-05 scratch figures remain uncitable. |
| F2 | Crossref contact address replaced with a placeholder (follow-up) | **Regressed in Stage 4** | See N1 below |

### 6.2 New integrity items raised during Stage 4

- **N1. The repository owner's personal e-mail address was sent to third-party APIs and committed.**
  - What happened:
    - `idea06/code/chase_citations.py` puts the address in the User-Agent of its OpenAlex and Semantic Scholar calls and in OpenAlex `mailto` parameters.
    - `idea06/code/crossref_is_sweep.py` puts it in the User-Agent and `mailto` of its Crossref calls.
    - 12 rows of `idea06/results/novelty/chase_log.csv` and 21 rows of `idea06/results/novelty/crossref_log.csv` record it.
    - The autosave loop committed and pushed these files.
  - Why it matters:
    - It reverses the 2026-10-05 placeholder fix.
    - It contradicts `idea06/novelty_deep_check.md` §2, which says no API key was requested so as not to send the address to a third party.
  - The idea-5 novelty session also sent the address in early calls and then removed it from its scripts. It discloses this in deviation 7. A search of `research/` found no committed idea-5 file containing the address.
  - Not fixed here, because this task allows edits to three files only. The author decides on scrubbing and any history rewrite (section 4, item 9).
- **N2. Intermediate commits.** The autosave loop pushed intermediate states of every Stage 4 directory, including idea-4 outputs from before a de-duplication bug fix. The final files and each idea's README are authoritative; the history should not be cited.
- **N3. Machine coding for idea 6.** The idea-6 pilot was coded by Claude, so an LLM coded an audit of LLM evaluation practice. That is the circularity the feasibility file warns against. The codes are not study data.
- **N4. Analysis choices made after seeing results.** All are disclosed in each README:
  - idea 5: the pairwise-complete set (after complete-case medians were seen); the inclusive tie rule; the User_1-only exclusion (after the detector failed);
  - idea 6: the intermediate RQ2 reading and the table-cell rule;
  - idea 4: the E4, E5 and M scope sets.

  The preregistrations must fix these choices. For idea 5, BPI 2017 and 2019 can no longer serve as untouched confirmatory data.
- **N5. Terms and licences.**
  - Idea 4: the licence of `audits_full.csv` is ambiguous, so only aggregates are in the repository and row-level files stay in `$SCRATCH/data/idea04/derived_private/`.
  - Idea 5: BPI 2017's 4TU terms bind publication (Art. 3) and remixing (Art. 4b); per-pseudonym files stay in `$SCRATCH/data/idea05/derived/`.
- **N6. Snippet-only and secondary items.** Items quoted in the novelty files must be verified before any citation:
  - the AI Act postponement;
  - Shahian et al. 2010;
  - Atteberry and Mangan 2020;
  - the Kwon 2014 and May 2012 theses;
  - Ko et al. 2025, Chen et al. 2026, Balloccu et al. 2024 and Briggs et al. 2025, known only through arXiv 2605.04135;
  - Roth et al. 2006's design, known from a third-party outline.
- **N7. Pilot READMEs not updated after the novelty checks.** `idea05/README.md` still lists the 4TU terms and the literature clause as open, and `idea06/README.md` still lists criterion 1 as undetermined. The novelty checks, written later, closed these points. This synthesis reconciles them. *Critic pass:* a dated note pointing to the novelty checks was added near the top of `idea05/README.md` and after section 1 of `idea06/README.md`; the original pilot text was kept (section 8).
- **N8. Index file.** `research/README.md` had no row for `06_stage4/`. This synthesis did not edit it, because its task allowed edits only to this file, `00_PROJECT_LOG.md` and `RESUME.md`. *Critic pass:* the row was added (section 8).

---

## 7. Reproducibility of this synthesis

**Inputs read in full.**
- The three idea READMEs and three `novelty_deep_check.md` files in this directory.
- `research/02_candidate_ideas.md` sections 1-5, including the idea 4-6 cards.
- `research/00_PROJECT_LOG.md`, entry of 2026-10-05.
- `research/RESUME.md`.
- `research/05_critique_2026-10-05.md`.
- `research/04_journals/venue_landscape.md`: header, (a) fit matrix, (b) cost routes, (c) requirements and (d) open questions.

**Result files checked against the README numbers:**
- `idea05/results/stopping_rule.csv`, `wall_clock.json`, `bpic20{17,19}_tau_summary.json`, `bpic20{17,19}_placebo_summary.json`, `bpic20{17,19}_variance_decomposition.csv`;
- `idea06/results/pilot/stopping_rule.json`, `pilot_timing.csv`, `screening_summary.csv`;
- `idea04/results/run_metadata.json`.

**sha256 of the inputs as read** (2026-10-19T06:59:51Z):

| File | sha256 |
|---|---|
| `idea06/README.md` | `f813f2f95b8640a88d12cb5dab21ea0decb6015ad06e60af6ff44cd369670e5a` |
| `idea06/novelty_deep_check.md` | `bf1694c42ff31e9a2771f03ac7074605858e58468c35562b3b3bb90ac7b7d67e` |
| `idea05/README.md` | `53d76559d34d365ded77c19712dc5f5864a1fd88850bf23c3e492044fa3b5e20` |
| `idea05/novelty_deep_check.md` | `e86c39c0424d6b675a8cb5ac0d095f8deb81ec83251d5d759809270dd81be4d7` |
| `idea04/README.md` | `afb71497575df97b2ab8c8a66c728b752e629cd6ae9b1c2bd66f42fc99a9a5a0` |
| `idea04/novelty_deep_check.md` | `4149a7bae04a12f388ee4595028ddc8942235d5145a470baad349f6d984dbccb` |
| `idea05/results/stopping_rule.csv` | `d5434f23b8058420db5ce7a1276324d7e1e7d9cf6edfca23bf6adf794a508975` |
| `idea05/results/wall_clock.json` | `f966e4668cefe9e66e0abdd028409e1a49ec852bb307a2a39faecac3303c46d7` |
| `idea06/results/pilot/stopping_rule.json` | `60d561a5ad4ce859e3fbea701b4a700a2414da618620c6b4ce00351952af7a00` |
| `idea06/results/pilot/pilot_timing.csv` | `fd687a7f68da3f3b31b0eab6ee87aa4961a847b346e6543a8e4ba268f5803998` |
| `idea04/results/run_metadata.json` | `58ade0ee40033459b61c473bdc1f5f84746d50a15f27eb8b1534d9546794be6f` |
| `research/02_candidate_ideas.md` | `62cc003b899a062999e7e1552b953897a3b47716e83f72dd94cb56f527378ee0` |
| `research/05_critique_2026-10-05.md` | `b90a5038b11cd5877176a730d4563a2ae350283ace03d3a886b276fb1c41df88` |
| `research/04_journals/venue_landscape.md` | `53823dbe4b84478091a421dd3e51ef511e22121095ea179d0fb5dcc41715e59c` |

**Commands.**
- Only read-only commands were used: `cat`, `sed`, `grep`, `sha256sum`, `git log`, `git status` and `ps`.
- The JSON result files were printed with the system `python3` for reading only. No value was computed with it; this deviates from the instruction to use the venv for analysis, but no analysis was done that way.
- The effort arithmetic in section 5 was done with the venv interpreter: `$SCRATCH/venv/bin/python -I -c ...`. It sums the `wall_clock.json` step times:
  - 89.8 + 34.8 + 148.5 + 98.1 = 371.2 s
  - 128.0 + 43.8 + 513.6 + 166.1 = 851.5 s
  - 16 x 371.2 s = 1.65 h; 16 x 851.5 s = 3.78 h
  - refit upper bound: 500 x 34.8 / 4 = 4,350 s and 500 x 43.8 / 4 = 5,475 s per log; added to the pilot-settings times above, this gives 78.7 and 105.4 min per log in total and 21.0 to 28.1 h for 16 logs.

  It also checks the idea-6 per-paper means: 23.8 s and 48.8 s, 726 s in total.

**Other details.**
- **Seeds:** none; no random numbers were drawn.
- **Software:** Python 3.11.15 (venv).
- **Wall-clock:** the input checksums were recorded at 06:59:51 UTC. The three output files (this README, the `00_PROJECT_LOG.md` entry and the `RESUME.md` update) were complete by 07:09:05 UTC.

**Deviations from the task.**
- `research/README.md` was not updated (see N8).
- `idea06/codebook_v0.md` and the per-idea result CSVs other than those listed above were not re-read. Their numbers are cited through the idea READMEs that report them.

---

## 8. Integrity critic pass (2026-10-19, after the synthesis)

A separate critic pass read every Markdown, JSON, code and `run.sh` file under `06_stage4/`, plus the CSV headers. It also read the Stage 4 entry of `00_PROJECT_LOG.md` and the 2026-10-19 section of `RESUME.md`. It checked the README and log numbers against the result files. **No result file, code file or `run.sh` was changed**, so the code checksums in the pilot READMEs and in `idea06/results/run_metadata.json` still match. The sha256 table in section 7 records the files as the synthesis read them, before the edits below.

**Edits (wording and consistency only):**
- **This file.**
  - "45 flagged titles" became 44. `idea06/results/novelty/aisel_flagged_titles.csv` holds 44 rows: 34 flag A, 8 flag B and 2 with both.
  - The idea-5 rule is now quoted verbatim, with the reading of "pre-registered minimum-event threshold".
  - A note on the idea-6 eLibrary precondition was added.
  - The idea-4 Semantic Scholar legs are completed from `idea04/results/novelty_chase_log.csv`.
  - The section 7 refit arithmetic was reworded.
  - N7 and N8 were updated.
- **`idea05/README.md`.**
  - The rule labelled "as written" was a paraphrase; it is now quoted verbatim.
  - A dated note points to the novelty check.
  - The pseudonym statement now mentions the three BPI 2019 batch-account labels in `bpic2019_sensitivity.csv`.
  - The results file count was corrected from 49 to 50.
- **`idea06/README.md`.** A dated note gives the rule state after the novelty check.
- **`idea04/README.md`.**
  - A pointer was added to the literature-condition outcome.
  - `run.sh` regenerates the pilot files but not the three `novelty_*` files.
- **`idea06/novelty_deep_check.md`.**
  - 45 flagged titles became 44.
  - "Only as the first one for LLM-evaluation papers" was replaced by a claim bounded by the searches.
  - Only 12 of the 16 arXiv searches are in `arxiv_api_queries.csv`; the note says where the other four are.
  - 2606.07936 was relabelled as abstract depth in the deviation list and the table heading.
- **`idea05/novelty_deep_check.md`.** "The first configuration-factorial reliability audit" was replaced by a claim bounded by the searches.
- **`00_PROJECT_LOG.md`.** Idea-4 Semantic Scholar forward chasing covered eight seeds, not four, with the Lam et al. leg not done. A pointer to this section was added.
- **`RESUME.md`** and **`research/README.md`.** The `06_stage4/` index row was added.

**Spot re-runs (outputs in `$SCRATCH/critic_check/`, outside the repository).** Each was run with the venv interpreter, `-I` and working directory `/`.
- Idea 4: `ll144_pilot.py`. The 25 CSVs are byte-identical to `idea04/results/` (35 s).
- Idea 6: the offline steps of `run.sh` (draw, calculator self-test, validation, claims, `analyze_pilot.py`). The 11 derived files are byte-identical to `idea06/results/pilot/` (3.6 s).
- Idea 5: `02_resource_fields.py` and `04_factorial.py` for BPI 2017. The 15 outputs are byte-identical to `idea05/results/`.

  The bootstrap, the placebo and BPI 2019 were not re-run.

**Still open:**
- **N1.** The e-mail address remains in two idea-6 scripts and two idea-6 logs. Scrubbing them would alter the run record and result logs, so it stays the author's decision.
- **Run headers.** The `idea04/code/run.sh` header comment still says it reproduces every file in `results/`. It was left unedited to keep its recorded sha256.
- **Novelty runners.** The idea-6 and idea-4 novelty scripts have no runner script. Idea 4 gives their command lines in a table (`idea04/novelty_deep_check.md` §8); idea 6 names the scripts but gives no command lines (`idea06/novelty_deep_check.md` §8).
- **Unverifiable log.** The idea-4 `run.sh` time of 55 s comes from `$SCRATCH/idea04_run.log`, which is outside the repository.
