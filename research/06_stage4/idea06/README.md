# Stage 4 pilot, idea 6: sampling frame and pilot coding for the error-bar audit

**Status: EXPLORATORY PILOT, run 2026-10-19 in the cloud container (4 vCPU, 15 GB RAM, Python 3.11.15).** Not preregistered, not peer reviewed.

**Who coded the pilot.** The coding was done by one machine-assisted coder: this agent, Claude. It scanned each paper with a keyword-in-context script and read the evaluation sections the scan pointed to. Papers were not read in full. **No human checked these codes.** This is not the human double coding the study design requires (two coders, kappa), and the codes should not be used as data for the study.

**Where the numbers come from.** Every number below comes from a file produced in this run (path given) or from a document read in this run (URL given).

**Scope of this pilot.**
- It covers the pilot criteria of the stopping rule in `research/02_candidate_ideas.md` section 4.1.
- The literature criterion is assessed by another agent. That agent's files are not part of this pilot: `results/novelty/` and `code/aisel_crawl.py`, `arxiv_parse.py`, `chase_citations.py`, `crossref_is_sweep.py`, `screen_titles.py`.
- An auto-save process committed intermediate versions of this directory during the run. This agent made no commit.

Plan followed: `research/02_candidate_ideas.md` (Idea 6 card; section 4.1). Also read in this run:
- `research/03_challenge/06-would-the-claim-survive-an-error-bar-auditing-st__feasibility.md` (frame, codebook, labour estimates);
- `__novelty.md`, first part only;
- `research/tools/assessment_2026-10-05/idea06/` (README, `crossref_counts.py`, its JSON outputs);
- `research/05_critique_2026-10-05.md` section 4.

## 1. Stopping rule, criterion by criterion

The rule as written in section 4.1 is quoted below. It was not altered and its thresholds were not changed:

> *"stop (or demote to a CAIS methods essay) if any of the following holds after the pilot and the eLibrary search: a published IS-venue audit of statistical or judge-validation practice in LLM papers is found; fewer than 30% of pilot papers permit RQ2 (no n or no accuracies) and the Springer-OA stratum after inclusion screening is below 25 empirical papers; or no second coder has been secured within four weeks and no AIS eLibrary access is obtainable"*

Sources for the table: `results/pilot/stopping_rule.json` and `results/pilot/stopping_rule.md`.

| Criterion | Reading | Value | Threshold | Holds? |
|---|---|---|---|---|
| 2a. Pilot papers permitting RQ2 | **Primary (pre-specified in `codebook_v0.md` before coding):** inclusion = Y, n stated in the paper, and both compared values are proportions | **3 of 20 = 15%** | < 30% | **yes** |
| 2a | Post hoc: n may come from the benchmark's standard size (AIME = 30) | 5 of 20 = 25% | < 30% | yes |
| 2a | Secondary (pre-specified): partial n, or non-proportion metrics (F1, mean ratings, composite scores), accepted | 7 of 20 = 35% | < 30% | **no** |
| 2b. Springer-OA stratum after inclusion screening | **Primary:** papers coded I (include) | **14** | < 25 | **yes** |
| 2b | Sensitivity: I plus borderline (B-T, B-H) | 21 | < 25 | yes |
| 2b | Sensitivity: I excluding encoder-only | 13 | < 25 | yes |
| **2 (2a AND 2b)** | Primary readings | 15% and 14 | both | **holds** |
| 1. Published IS-venue audit found | n/a | n/a | n/a | **undetermined**: the literature check (including the AIS eLibrary search) is run by another agent |
| 3. No second coder within four weeks and no AIS eLibrary access | n/a | n/a | n/a | **undetermined**: securing a second coder is the author's decision, the four-week window has not elapsed, and no eLibrary access was attempted in this run |

**Outcome.** Criterion 2 holds under the pre-specified primary readings, so the rule (which stops on *any* criterion) is **triggered by the pilot criterion**. Criteria 1 and 3 are undetermined. Read the result with three facts in view:

- **It depends on the reading of "permit RQ2".**
  - Under the pre-specified secondary reading, 2a fails (35%), so criterion 2 does not hold.
  - Criterion 2b holds under every inclusion reading: 13, 14 or 21 papers, all below 25.
- **2a is driven by the Springer half of the sample.**
  - The plan draws the IS pilot papers from the *unscreened* term-hit stratum. 9 of the 10 drawn Springer papers do not pass inclusion. Seven are excluded: two conceptual articles, a survey, a bibliometric study, two qualitative studies and a GNN case study. Two are borderline: a synthetic tabular-data study and a human-subject experiment.
  - Hence 0 of 10 Springer papers permit RQ2, against 3, 5 and 7 of 10 ACL industry papers under the three readings.
  - Among the 10 pilot papers that pass inclusion, the strict share is 3 of 10 = 30%. This is supplementary only; the rule's denominator is "pilot papers".
- **The pilot is exploratory and machine-coded.** A human second coder could move individual codes. 2a sits close to the threshold: 15-35% across readings against 30%.

The decision to stop, demote to a CAIS methods essay, or change the frame belongs to the author.

**Note added in the critic pass (2026-10-19).** Criterion 1 was assessed after this pilot, in `novelty_deep_check.md` §6, and is not triggered within the searches run there. The AIS eLibrary keyword search returned HTTP 403 and was replaced by a browse-page crawl plus Crossref. The rule's state is therefore: triggered by criterion 2, criterion 1 not triggered, criterion 3 undetermined (synthesis: `../README.md` §2.1). The table above records the state at the end of this pilot run.

## 2. Sampling frame (frozen 2026-10-19)

Script: `code/build_frame.py`. It uses the standard library, a polite User-Agent, and no e-mail address (none was provided). It ran from 2026-10-19T05:21:22Z for 183.2 s (`results/frame/frame_summary.json`).

**How the IS journals were queried.**
- Crossref `works` with filter `issn:<ISSN>,from-pub-date:2023-01-01,until-pub-date:2026-10-19,type:journal-article`.
- The same 11 journals and ISSNs as `crossref_counts.py` of 2026-10-05.
- The same term regular expression on title and title+abstract: `language model|\bLLMs?\b|generative AI|generative artificial intelligence|ChatGPT|GPT-?[34]`.
- Markup tags are stripped before matching; the raw count is kept too.
- The Creative-Commons licence URL and the content version are recorded per record.

**How the ACL industry volumes were read.** The volume pages were parsed and front matter (paper 0) excluded. Each volume's `.bib` was fetched as a cross-check, and the counts agree for all seven volumes. The 96 raw responses are cached outside the repository, with sha256 in `results/frame/raw_manifest.csv`.

| Stratum | Count on 2026-10-19 | 2026-10-05 count | File |
|---|---|---|---|
| IS journal articles, 11 journals, 2023-01-01 to 2026-10-19 | **3,543** | 3,583 | `results/frame/is_journal_articles.csv`, `frame_counts_is_journals.csv` |
| Springer term hits (BISE 24, ISF 42, EM 18) | **84** | 83 | `results/frame/springer_term_hits.csv` |
| Springer term hits with a CC licence (BISE 23, ISF 26, EM 16): the Springer-OA stratum | **65** | 65 | `results/frame/springer_oa_term_hits.csv` |
| ACL industry: EMNLP 2023 (77), NAACL 2024 (43), EMNLP 2024 (121), NAACL 2025 (80), ACL 2025 (109), EMNLP 2025 (193), ACL 2026 (154) | **777** | 777 (503 + 154 + 77 + 43) | `results/frame/acl_industry_papers.csv`, `frame_counts_acl_industry.csv` |

More detail on the Springer-OA stratum and the ACL industry stratum:
- Licences in the Springer-OA stratum: 63 CC BY 4.0 and 2 CC BY-NC-ND 4.0.
- Publication years of the Springer-OA stratum: 2023: 5, 2024: 1, 2025: 21, 2026: 38.
- Publication years of the 777 ACL industry papers: 2023: 77, 2024: 164, 2025: 382, 2026: 154.
- ACL 2025 and ACL 2026 each contain one track-overview paper, kept in the frame.

**Why the counts differ from 2026-10-05.** The source is `results/frame/frame_decomposition_unbounded_vs_frozen.csv`, plus a count of creation dates in the cached raw responses.

- **IS total, 3,583 to 3,543 (net -40).** A second leg repeated the 2026-10-05 query form, with no upper date bound, and returned 3,612 records.
  - **Freezing removes 69 records.** They are Elsevier records whose Crossref `published` date lies after 2026-10-19 (2026-11 to 2027-01, i.e. future issue dates): I&M 41 and DSS 28. They include 5 I&M and 1 DSS term hits. That is why I&M falls from 12 to 7 hits and DSS from 25 to 24 under the frozen definition.
  - **New records add 29 (+29 net).** 27 records were registered after 2026-10-05: I&M 7, DSS 6, ISF 4, EM 3, ISJ 3, EJIS 2, BISE 1, ISR 1. The remaining +2 (both ISR) cannot be attributed, because the 2026-10-05 run kept counts but no DOI list.
  - 3,583 + 29 - 69 = 3,543.
- **Springer term hits, 83 to 84.** One new ISF article, 10.1007/s10796-026-10824-1, was registered on 2026-10-08 and is not CC-licensed. The Springer-OA stratum is therefore unchanged at 65.
- **ISJ term hits, 6 to 9.** This comes from tag stripping (`Generative <scp>AI</scp>`). The raw, unstripped count is 6. The 2026-10-05 recount (`crossref_recount_scp.json`) had already found 9. ISR rises from 34 to 35 with no new hit records. Records with an abstract rose from 507 to 510, which is consistent with an abstract deposited after 2026-10-05, but this cannot be checked per DOI.
- **ACL.** ACL 2026 has 154 papers, the same as on 2026-10-05, and all seven volumes match the 2026-10-05 `.bib` counts.

**Volumes probed but not in the planned frame** (`results/frame/acl_volume_probes_not_in_frame.csv`):

| Volume | Status | Papers |
|---|---|---|
| 2026.naacl-industry | HTTP 404 | n/a |
| 2026.emnlp-industry | HTTP 404 | n/a |
| 2024.acl-industry | HTTP 404 | n/a |
| 2023.acl-industry | exists | 76 |
| 2025.coling-industry | exists | 69 |
| 2026.eacl-industry | exists | 71 |

Adding the last three is an author decision; they were not added.

## 3. Inclusion screening of the Springer-OA stratum (65 papers)

Abstracts were taken from the Springer landing pages. 58 of 65 have one; the 7 without one are editorials, a catchword, a discussion, a profile and a correction. The fetch is recorded in `code/fetch_fulltexts.py`, with sha256 in `results/frame/springer_oa_landing_manifest.csv`; abstract texts are kept outside the repository.

The single machine-assisted coder screened each paper against the idea record's criterion: *"the paper reports a quantitative evaluation of an LLM-based model, prompt, pipeline or agent on at least one dataset"*. Four unclear abstracts were resolved by a full-text keyword check.
- Decisions with reasons: `code/coding/springer_oa_screening.csv`.
- Counts: `results/pilot/screening_summary.csv`.

| Journal | I (include) | B-T (non-language generative model) | B-H (human-subject experiment with LLM treatment) | E (exclude) | Total |
|---|---|---|---|---|---|
| BISE | 5 | 1 | 4 | 13 | 23 |
| EM | 2 | 1 | 0 | 13 | 16 |
| ISF | 7 | 1 | 0 | 18 | 26 |
| **All** | **14** | 3 | 4 | 44 | 65 |

- 1 of the 14 included papers evaluates encoder-only models only (BERT/RoBERTa).
- By year, the 14 included papers are 2024: 1, 2025: 2, 2026: 11.
- The feasibility file expected "maybe 8-15 of the 24" BISE hits, and 30-50 Springer papers in total, to be empirical. This screen found 14 strictly, or 21 with borderline cases, among the 65 OA hits.
- The 19 non-OA Springer hits were not screened.

## 4. Pilot sample and coding

**Draw.** `code/draw_pilot.py` uses `random.Random(20261015)`, sampling 10 papers from the 65 Springer-OA term hits sorted by DOI and then 10 from the 777 ACL industry papers sorted by Anthology ID. The sample is in `results/pilot/pilot_sample.csv` (sha256 `ba96536813b14761…`).

**Full texts.** `code/fetch_fulltexts.py` downloaded 20 PDFs into `$SCRATCH/data/idea06/papers/<ID>/`. Byte counts and sha256 are in `results/pilot/fulltext_manifest.csv`. Two access details:
- link.springer.com served a JavaScript "Client Challenge" page to python-urllib. It served the PDFs to curl, so the script uses curl.
- The ACL PDFs were fetched by the first, urllib-based version of the script. They are marked "cached" in the manifest; the hashes are unchanged across runs.

**Codebook.** `codebook_v0.md` sets out the items, numbered, as the feasibility file defines them.
- **The feasibility file's list has 11 entries; the plan says "14 items".** Splitting the three compound entries (runs/seeds, agreement metric and chance correction, code/data) gives 14 fields. This reconciliation is the coder's own and is listed as a deviation.
- Decision rules from the feasibility file are marked [FEAS]. Rules added for the pilot are marked [PILOT].

**Coding.**
- One JSON file per paper in `code/coding/papers/`, with value plus page/section location per item.
- Compiled into `results/pilot/pilot_coding.csv` (every location) and `results/pilot/pilot_coding.md` (readable).
- The helper `code/kwic.py` prints keyword-in-context lines with PDF page indices (pdftotext form-feed count). The coder decides every code; the helper decides nothing.

**Timing.** Source: `results/pilot/pilot_timing.csv` and `code/coding/coding_times.log`.
- Machine wall-clock per paper ranged from 8 to 62 s, 726 s in total. Mean per paper: 24 s for the 10 Springer papers (9 did not pass inclusion) and 49 s for the 10 ACL papers.
- These are machine timings of targeted reading, not estimates of human labour. The feasibility file's 30-45 min per paper for a trained human coder is not tested by this pilot.
- Page-reference corrections made during verification, after the timed windows, are not timed (A01, A05, S01).

**Inclusion and RQ2 extractability** (`results/pilot/pilot_coding.md`):

| | Springer-OA IS (10) | ACL industry (10) |
|---|---|---|
| Inclusion: Y | 1 (S09, encoder-only) | 9 (A02-A10) |
| Inclusion: N or borderline | 9 (N 7, B-T 1, B-H 1) | 1 (A01, systems-efficiency paper with no task dataset) |
| RQ2, strict / post hoc intermediate / loose | 0 / 0 / 0 | 3 / 5 / 7 |

Why RQ2 failed for the included papers:
- **n not stated** (A05).
- **Metric not a proportion:** F1 (A05), compute ratio and calibration errors (A06), mean expert rating (A07), composite packet score (A08), relative gains pooled over datasets (S09).
- **n only derivable from the benchmark's conventional size** (A02, A09: AIME, 30 problems, not stated in the paper).
- **Headline-claim rule picks a table cell.** For A02, A03 and A09 the headline claim had to be mapped to one of several table cells. The cell was chosen during coding: the first row pair in the first column, or the cell the text names. This is a post hoc rule, not in `codebook_v0.md`. Alternative cells were also run (section 5).

**Item prevalence among the 10 included pilot papers** (exploratory, n = 10; Wilson 95% CIs in `results/pilot/item_prevalence.csv`):

| Item | Y | P | N | NA |
|---|---|---|---|---|
| n stated | 6 | 3 | 1 | 0 |
| Repeated runs | 2 | 1 | 7 | 0 |
| Seeds | 0 | 1 | 9 | 0 |
| Decoding | 2 | 2 | 4 | 2 |
| Model version or date | 5 | 5 | 0 | 0 |
| Prompts | 4 | 3 | 2 | 1 |
| Any uncertainty (SE, CI, test) | 1 | 3 | 6 | 0 |
| Contamination | 1 | 4 | 5 | 0 |
| Code | 5 | 0 | 5 | 0 |
| Data | 5 | 3 | 2 | 0 |

- An LLM judge was used in 2 of the 10 papers (A03, A07). Neither validated it against humans, so both are N on items 8, 9a and 9b.
- The one Y on uncertainty is A07, and only for its production A/B test.

**Observations the coding surfaced.** These come from arithmetic on reported values in this run and were not confirmed with the authors.
- **A03:** the sentence "Our retrievers outperform all baseline models across all evaluation metrics" is contradicted by its own Table 1, which shows ties with ColQwen2.5-3B on MRR and nDCG.
- **A04:** four micro success rates equal k/133 to two decimals, although 135 goals are stated.
- **A09:** some values are not consistent with the standard benchmark sizes. For example, 69.7 is not k/30.
- **S04:** the confusion counts sum to the full dataset, not to the stated test split. S04 is out of scope (a GNN).

## 5. Uncertainty models on the extracted claims

**Calculator.** `code/uncertainty_calc.py` uses the standard library only. Its `--selftest` passes. `code/validate_calc.py` checks it against independent implementations:
- Wilson and Newcombe intervals agree with statsmodels 0.15.0 to within 1.1e-16.
- The Beta-Binomial Monte Carlo agrees with a 10^6-draw numpy run to within 0.38 percentage points (`results/pilot/calc_validation.csv`).
- The Newcombe reference values 0.0524 and 0.3339 for 56/70 vs 48/80 were recalled from memory, not re-read in this run. statsmodels reproduces them.

**Inputs.** The claims are in `code/coding/pilot_claims.csv`: 5 rule-based headline claims and 5 alternative cells. Results are in `results/pilot/claim_survival.csv` and `results/pilot/survival_summary.md`, with seed 20261015 and 20,000 Beta draws.

**The models.** A claim survives when the 95% interval of the difference excludes 0.
- **M1, binomial at the reported n.** The naive unpaired Wald interval, with the Newcombe interval as a check.
- **M2, structure where the paper reports one.**
  - Paired (same items): survival is bounded between the minimal-discordance SE and the unpaired SE, as the feasibility file proposes ("paired lower bound … unpaired upper bound"). The maximal-discordance SE is also reported.
  - Clustered: a Miller design effect with ICC in {0, 0.1, 0.3}, using the cluster size the paper reports.
- **M3, run-to-run variance.** Atil et al.'s abstract (arXiv 2408.04667, read via the arXiv API; sha256 of the response `be0436ff…`) says "accuracy variations up to 15% across naturally occurring runs".
  - **Primary, worst case:** a single-run claim survives only if |Δ| > 15 percentage points.
  - **Sensitivity:** σ_run = 3.75 pp per arm, added in quadrature to the M1 SE.
  - Reading "15%" as percentage points rather than as a relative change is the coder's interpretation.
- **M4, Beta-Binomial.** Bowyer et al.'s regime, the idea card's model (c), added because the task's third model differs from the card's.

| Claim | Paper | A vs B (%) | n (source) | M1 | M2 paired | M2 clustered, ICC 0.1 / 0.3 | M3 worst / σ | M4 |
|---|---|---|---|---|---|---|---|---|
| C01 (H1) | A02 | 16.7 vs 6.7 | 30 (benchmark size) | no | none | n/a | no / no | no |
| C02 (alt) | A02 | 70.0 vs 62.6 | 500 (paper) | yes | all | n/a | no / no | yes |
| C03 (H1) | A03 | 96.0 vs 95.9 | 2,932 (paper) | no | none | n/a | no / no | no |
| C04 (alt) | A03 | 96.0 vs 87.7 | 2,932 (paper) | yes | all | n/a | no / no | yes |
| C05 (H1) | A04 | 47.0 vs 42.0 | 100 (paper) | no | some | n/a | no / no | no |
| C06 (alt) | A07 | 66.67 vs 43.33 | 30 (paper) | no | some | n/a | yes / no | no |
| C07 (alt) | A08 | 84.18 vs 82.39 | 6,655 pages (Small variant assumed) | yes | all | no / no | no / no | yes |
| C08 (alt) | A08 | 84.18 vs 82.39 | 5,599 pages (Large variant assumed) | yes | all | no / no | no / no | yes |
| C09 (H1) | A09 | 53.3 vs 40.0 | 30 (benchmark size) | no | some | n/a | no / no | no |
| C10 (H1) | A10 | 74.0 vs 71.5 | 100,400 (paper) | yes | all | yes / yes | no / no | yes |

**The five rule-based headline claims.**
- 1 survives M1, M2 (paired upper bound) and M4: A10, at n = 100,400.
- None survives either version of M3. For the large-n claims, a 15-point run band dwarfs sampling error. This is the feasibility file's point that survival is an upper bound on robustness.

**The alternative cells.** They show how much the claim-selection rule matters. A03's sentence-level claim (vs the strongest baseline, Δ = 0.1 pp) fails every model. Its comparison with its own backbone (Δ = 8.3 pp) survives M1, M2 and M4.

These are five claims, so the numbers are a demonstration of the pipeline and not survival-rate estimates.

## 6. Deviations from the written plan and the task

1. **ACL frame volumes.** The task names "the ACL 2026 industry track plus EMNLP 2023 and NAACL 2024 industry tracks". The plan treats these as additions to the four volumes named in the idea card. All seven volumes (777 papers) were enumerated and the ACL pilot draw is from all seven. Drawing only from the three named volumes would give a different sample.
2. **Upper publication-date bound.** `until-pub-date:2026-10-19` is a definition the 2026-10-05 run did not have. It excludes 69 Elsevier records with future issue dates (section 2). Both counts are reported. Whether in-press Elsevier articles belong in the frame is an author decision; it does not affect the Springer or ACL strata.
3. **Tag stripping** before term matching. It changes ISJ only, from 6 to 9; the raw count is kept.
4. **Codebook.** The 11 listed entries were reconciled to 14 fields (`codebook_v0.md` §0a). The [PILOT] rules in the codebook were written before coding: what counts as "LLM-based", what counts as a quantitative comparison, the Hugging Face identifier rule for open-weight versions, and the strict and loose RQ2 readings. The choice of table cell when a headline claim maps to several cells (first row pair in the first column, or the cell the text names) was made during coding and is not in `codebook_v0.md`. It is a post hoc rule and a v1 item.
5. **"Permit RQ2" readings.** Strict (primary) and loose (secondary) were fixed in the codebook before coding. The intermediate reading (n from a benchmark's standard size) was added after coding and is labelled post hoc.
6. **Third uncertainty model.** The task names run-to-run variance (Atil et al.); the idea card's third model is the Beta-Binomial. Both were implemented, as M3 and M4. The "15% band" was read as 15 percentage points, with a worst-case primary and a variance sensitivity.
7. **Inclusion screening** was done at abstract level, with full-text keyword checks for 4 unclear cases. Full-text screening of all 65 papers was not done.
8. **The pilot was drawn from unscreened term hits,** as the task specifies. Inclusion was coded per paper (section 1 explains the effect on 2a).
9. **Alternative claim cells and assumed n.** Five alternative claim cells were run beyond the five rule-based claims. For A08, n is assumed under two variants because the paper does not state which variant Table 2 uses.
10. **Download tool and reconciliation.** Springer downloads used curl instead of python-urllib (section 4). The plan's reconciliation of the Springer frame with Springer's own search or OpenAlex "when rate limits allow" was not done in this run: neither OpenAlex nor Semantic Scholar was queried.
11. **Additional ACL volumes probed** (ACL 2023, COLING 2025, EACL 2026 industry) were reported but not added.

## 7. Limitations

- **The pilot was coded by a machine, single coder, without human verification.**
  - An LLM coding an audit of LLM evaluation practice is the circularity the feasibility file (section 3) warns against for the confirmatory pipeline.
  - No inter-coder agreement exists.
  - Reading was targeted (section scan plus keyword-in-context plus the evaluation sections), not complete. Items coded N ("not reported") may be false negatives where text was missed: appendices, footnotes, linked repositories (which were not opened).
- **Small numbers.** 20 pilot papers, 10 included, 5 headline claims. The prevalence CIs are wide (e.g. any uncertainty 1 of 10, Wilson 95% 0.02-0.40).
- **Headline-claim ambiguity is real.** In 3 of the 9 included ACL papers (A02, A03, A09) the headline claim had to be mapped to one of several table cells, and the choice of cell changes survival (A03). n for the headline claim was not fully extractable from the paper (H3 not Y) in 5 of the 10 included papers.
- **Screening and frame.** Screening was by one coder at abstract level. Crossref abstracts are absent for Elsevier and Taylor & Francis, so those counts are title-only. The Crossref snapshot will drift with late deposits; the frozen CSVs are the reference.
- **Timings are not human labour.** They do not test the 150-220 person-hour estimate.
- **The survival models need assumptions the papers do not supply.** These include the item-level correlation (paired bound), the ICC and cluster sizes, the meaning of Atil et al.'s 15%, and that table values are single runs. The paired upper bound assumes non-negative error correlation.

## 8. Next steps (for the author)

1. **Decide on criterion 2.**
   - Primary reading: triggered. Secondary reading: not triggered.
   - Decide whether the pilot should instead be drawn from *screened* Springer papers. That would change the rule's input, so it needs an explicit amendment, not a silent re-run.
2. **Recruit the second coder.**
   - Double-code these 20 papers by hand, using `codebook_v0.md` and these machine codes as a blind-later comparison, not as a gold standard.
   - Report kappa.
3. **Fix codebook v1:**
   - a table-cell rule for headline claims;
   - whether benchmark documentation may supply n;
   - how to treat non-proportion metrics (F1, ratings, composites) and systems-efficiency papers;
   - the judge protocol fields recommended in the novelty file.
4. **Full-text screening.** Screen the 21 I and borderline Springer papers in full. If the IS stratum must reach 25, add ICIS/ECIS (needs AIS eLibrary access) or the Elsevier journals (needs access).
5. **Merge with the literature criterion** from the parallel agent (`results/novelty/`) before any decision.

## 9. Reproducibility

- **Re-run.** `bash code/run.sh` reproduces every derived file from the frozen frame and the coder's inputs, with no network, in about 3 s. `FETCH=1 bash code/run.sh` re-queries Crossref and the ACL Anthology and re-downloads the papers. Crossref drift can change the frame; see the script header.
- **Seeds.**
  - 20261015: the pilot draw and the Beta-Binomial Monte Carlo (20,000 draws).
  - 7: the numpy validation run.
- **Software.**
  - Python 3.11.15, numpy 2.4.6, scipy 1.17.1, statsmodels 0.15.0 (validation only).
  - pdftotext 24.02.0, curl 8.5.0.
  - Linux 6.18.44.
- **Wall-clock times.**
  - Frame build: 183.2 s.
  - Coding: 726 s for 20 papers (`results/pilot/pilot_timing.csv`).
  - Offline `run.sh`: about 3 s.
- **Checksums.**
  - sha256 of every code, input and result file: `results/run_metadata.json`.
  - sha256 of the 20 PDFs: `results/pilot/fulltext_manifest.csv`.
  - sha256 of the 96 raw Crossref and ACL responses: `results/frame/raw_manifest.csv`.
  - sha256 of the 65 Springer landing pages: `results/frame/springer_oa_landing_manifest.csv`.
  - sha256 of the Atil et al. arXiv API response: `be0436ffe3007b82374a620fccc304d214b00e41a7a6a604d9c3147b559c4444`.
- **Downloads.** About 100 MB, outside the repository in `$SCRATCH/data/idea06/` (`frame_raw_20261019/`, `papers/`, `springer_landing/`, `refs/`, plus probe directories). `$SCRATCH` = `/tmp/claude-0/-home-user-employee-monitoring-system/c64eab22-9c10-592c-b92e-5ac629c5be82/scratchpad`.

## 10. Files written by this pilot

| Path | Content |
|---|---|
| `codebook_v0.md` | Draft codebook as applied (numbered items, [FEAS]/[PILOT] rules) |
| `code/build_frame.py` | Frame enumeration (Crossref and ACL Anthology), frozen date |
| `code/draw_pilot.py` | Seeded pilot draw |
| `code/fetch_fulltexts.py` | PDF and landing-page download (curl), pdftotext conversion, manifests |
| `code/kwic.py` | Keyword-in-context helper for the coder |
| `code/uncertainty_calc.py` | Standard-library survival calculator (M1-M4), `--selftest` |
| `code/validate_calc.py` | Validation against statsmodels and numpy |
| `code/analyze_pilot.py` | Compiles tables, prevalence, screening counts, stopping rule |
| `code/write_run_metadata.py` | Versions, seeds, timings, sha256 |
| `code/run.sh` | Runs the pipeline |
| `code/coding/papers/*.json` | Per-paper codes with locations (coder input) |
| `code/coding/pilot_claims.csv` | Claims passed to the calculator |
| `code/coding/springer_oa_screening.csv` | Inclusion screening decisions (65 papers) |
| `code/coding/coding_times.log` | Raw per-paper timing log |
| `results/frame/*` | Frozen frame CSVs, counts per stratum, `frame_summary.json`, decomposition, manifests |
| `results/pilot/*` | Sample, full-text manifest, coded table (CSV and MD), timing, item prevalence, screening summary, claim survival (CSV and MD), calculator validation, stopping rule (JSON and MD) |
| `results/run_metadata.json` | Reproducibility metadata |


## Redaction note (2026-10-19)

During the 2026-10-19 run the two citation scripts (`code/chase_citations.py`, `code/crossref_is_sweep.py`) hardcoded the repository owner's personal e-mail address as the API contact (User-Agent and `mailto=` parameter), and the request logs (`results/novelty/crossref_log.csv`, `results/novelty/chase_log.csv`) recorded it in 33 URLs. The address was never authorised for that use. It has been removed: the scripts now read an optional contact from the `MAILTO` environment variable (none by default), and the logged URLs show `mailto=REDACTED`. Request URLs, statuses and attempts are otherwise unchanged, so the logs remain a faithful record of what was queried. The sha256 values recorded earlier for these four files no longer match because of this redaction; no result file or count changed.
