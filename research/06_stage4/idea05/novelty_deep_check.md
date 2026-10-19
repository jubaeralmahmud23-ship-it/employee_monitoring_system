# Idea 5, Stage 4 deep novelty check: "Productivity Scores from Workflow Traces"

**Date:** 2026-10-19 (session 06:01 to about 07:00 UTC). **Environment:** cloud container (4 vCPU, 15 GB RAM, no GPU). This is not the author's Windows PC used on 2026-10-05. **Plan followed:** `research/02_candidate_ideas.md` section 4.2, "Novelty tests". **Earlier check:** `research/03_challenge/05-productivity-scores-from-workflow-traces-how-rob__novelty.md` (2026-10-05, verdict "partially-covered") and its `__feasibility.md`.

**Scope.** This file covers only the novelty part of the Stage 4 plan:
- reading the named full texts;
- citation chasing;
- the sweeps the earlier check could not run;
- the literature clause of the stopping rule.

The pilot clauses of the stopping rule (median Kendall tau and bottom-quintile reclassification on BPI 2017 and BPI 2019) are reported separately in `README.md` and are not assessed here.

**Outcome in brief**

- **Verdict: partially-covered.** The category is unchanged, but the uncovered space is smaller than on 2026-10-05 (Section 5). Inside process mining, no study was found that tests how stable worker or resource rankings are across measurement choices. Outside process mining, the closest design already exists: physician cost profiling has crossed measurement choices for individual professionals since 2006.
  - Thomas and Ward 2006: 3 attribution rules x 6 outlier rules.
  - Mehrotra et al. 2010: 12 attribution rules, with 17-61% of physicians changing cost category.
  - Timbie et al. 2013: rankings with and without socioeconomic adjustment.
  - Kaye et al. 2019: year-to-year stability of the top spending quartile.
- **Literature stop condition: not triggered** (Section 6). The sweep and the other searches found no rank-stability study of resource performance measures on public event logs. The sweep enumerated 1,360 papers from ICPM, BPM, CAiSE and Process Science (2022-2026). The other searches covered 38 BPI Challenge 2017/2019 reports, 86 ICIS future-of-work papers, about 1,300 forward citations and 99 backward references. Residual risk is listed in Section 7.
- **What the full texts change.** They confirm the earlier readings of Adams et al., Gu and Koenker, Nakatumba and van der Aalst, and Goldstein and Spiegelhalter, and correct details:
  - Adams et al. use a lowest-25% tier, not quintiles.
  - Larger samples raise reliability only modestly: doubling episodes moved one physician's reliability from 0.61 to 0.76 and misclassification from 17% to 15%.
  - Nakatumba's workload measure has its own free window parameters.
  - Kelemen is a CEE eDem/eGov Days 2019 paper (DOI registered 2022) that reviews 9 papers and never discusses validity.
- **New prior art that changes the framing.** These works are closer to parts of the idea than anything in the earlier table:
  - **Stability audit of algorithmic HR tools:** Rhea et al. 2022, with an open-source audit library.
  - **Convergent validity of log-derived worker variables:** Braakman et al. 2025 found no strong correlations with validated survey measures.
  - **Actor-behaviour performance measures on BPIC 2017 and 2019:** Klijn et al. 2024; Leribaux et al. 2025. Leribaux et al. treat "User 1", the system account named on the idea card, as an actor.
  - **Per-user rankings in the BPI Challenge 2017 reports:** the reports rank individual users and draw judgements from the rankings without any stability check. Jeong et al. flag users for investigation; Rodrigues et al. call low-activity resources "adding low value".

All derived files are in `research/06_stage4/idea05/results/novelty/`. Scripts are in `research/06_stage4/idea05/code/novelty/`, with the command order in `run_novelty.sh`. Raw downloads are in `/tmp/claude-0/-home-user-employee-monitoring-system/c64eab22-9c10-592c-b92e-5ac629c5be82/scratchpad/data/idea05_novelty/`, which is not committed.

---

## 1. Full texts read

Access depth:
- **full-text**: the document was downloaded and converted (`pdftotext -layout` for PDFs, `html2text.py` for HTML), then read in the sections cited.
- **abstract**: only the abstract, or a summary page, was read.
- **metadata/snippet**: only the Crossref record and/or a WebSearch snippet was seen.

Page numbers are PDF page indices of the copy read. Checksums are in `results/novelty/fulltext_manifest.csv` and `fulltext_manifest_extra.csv`.

| Title | Source URL | Access depth | What changed relative to the 2026-10-05 reading |
|---|---|---|---|
| Adams, Mehrotra, Thomas, McGlynn, "Physician Cost Profiling — Reliability and Risk of Misclassification", NEJM 2010 (author manuscript) | https://pmc.ncbi.nlm.nih.gov/articles/PMC2878194/ | full-text (HTML) | **Confirms** 59% of physicians below reliability 0.70 and 22% misclassified (Abstract, Results). **Corrects** the tier: physicians in the lowest 25% are labelled "lower cost" (Methods, "Analysis of misclassification"), not a quintile. **Adds:** (a) reliability is a signal-to-noise ratio from a two-level hierarchical model (Methods, "Analysis of reliability"); (b) the sensitivity analyses cover Winsorizing, actual reimbursements, plan-specific profiles, two alternative episode-assignment rules (both lowered reliability) and a minimum of 30 episodes (higher median reliability in 18 of 28 specialties, but 8,689 vs 12,789 physicians profiled); (c) two alternative profiling applications gave higher misclassification (Results, "Sensitivity analyses"); (d) 43% of physicians labelled lower cost were not, across 26 of 28 specialties (Table 5 note). **Qualifies** the earlier claim "reliability rises with observation count": even at about 100 episodes reliability "varies widely" (Results, Figure 1), and doubling the episodes of an average family physician raised reliability only from 0.61 to 0.76, with misclassification falling from 17% to 15% (Discussion). The reference list points to Mehrotra et al.'s attribution-rule study, followed up in Section 4. The supplementary appendix returned a reCAPTCHA page and was not read. |
| Adams et al., "Physician Cost Profiling–Reliability and Risk of Misclassification: Detailed Methodology and Sensitivity Analyses", RAND Health Quarterly 2012 (10.7249/rhq-02-01-03) | https://pmc.ncbi.nlm.nih.gov/articles/PMC4945285/ | abstract (PMC summary page) | The PMC record is a short summary of RAND TR-799-DOL. It confirms that the method computes reliability and misclassification "from data typically available to health plans", including cut points at percentiles and statistical testing. The full report (rand.org TR799 page and PDF) answered HTTP 403 twice, so the detailed sensitivity tables were **not** read. |
| Saisana, Saltelli, Tarantola, "Uncertainty and Sensitivity Analysis Techniques as Tools for the Quality Assessment of Composite Indicators", JRSS A 2005 | https://doi.org/10.1111/j.1467-985x.2005.00350.x (academic.oup.com answered 403) | abstract (Crossref; 22 references deposited) | **Confirms** the abstract: uncertainty and sensitivity analysis are used to assess "the reliability of countries' rankings", applied to the UN Technology Achievement Index. No open copy was found in two WebSearch queries, so the variance-decomposition details were not read. |
| Papay, "Different Tests, Different Answers", AERJ 2011 | https://doi.org/10.3102/0002831210362589 (journals.sagepub.com answered 403) | abstract (Crossref; 38 references deposited) | **Confirms** rank correlations of 0.15-0.58 across three reading tests. **Adds** from the abstract: content, scaling and student sample do not explain the instability; "test timing and measurement error" do. A WebSearch snippet names a replication, Atteberry and Mangan 2020 (Educational Researcher, 10.3102/0013189x20922993); its snippet reports correlations of .13-.15 that persist across value-added specifications (snippet only). |
| Gu and Koenker, "Invidious Comparisons: Ranking and Selection as Compound Decisions" (arXiv 2012.12550v3, Sept 2021; published Econometrica 2023) | https://arxiv.org/pdf/2012.12550 | full-text | **Confirms** the earlier reading. **Adds:** (a) when measurement error is comparable to the spread of latent ability, even oracle selection rules may not beat "about even odds" that a selected unit is truly above the threshold (Section 1, p. 3; restated p. 9); (b) a teacher value-added simulation that targets selection from the **left tail**, "those teachers whose jobs are endangered" (Section 7.2, p. 30), which is the analogue of the idea's bottom quintile; (c) the dialysis-centre application (Section 8, p. 31). Read from the arXiv version, not the Econometrica text. |
| Nakatumba and van der Aalst, "Analyzing Resource Behavior Using Process Mining", BPM 2009 Workshops (LNBIP 2010) | https://www.vdaalst.com/publications/p585.pdf | full-text (author copy) | **Confirms** the per-resource regression of processing speed on workload. **Corrects/adds:** (a) the workload measure has its own free parameters: reference and load event sets and a time window `hback`/`hforw` of 1-24 hours (Definition 3, p. 7), and "multiple definitions of the workload are possible" (p. 6); (b) the case study uses a private Dutch municipality log (2,076 cases, 67,271 events, 109 resources, 11 activities; p. 9) with a 23-hour window; (c) R² per resource ranges from 0.05 to 0.71 (Table 2, p. 9) and reaches 0.99 for a resource-activity pair (Table 3, pp. 10-11); (d) there is no ranking, comparison or stability analysis. **Implication:** a workload covariate brings its own configuration factor (the window) into the factorial. |
| Goldstein and Spiegelhalter, "League Tables and Their Limitations", JRSS A 1996 (University of Bristol preprint, 32 pp., without the published discussion) | https://www.bristol.ac.uk/media-library/sites/cmm/migrated/documents/limitations-of-league-tables.pdf | full-text (preprint) | **Confirms** interval estimates for ranks (Section 3.2, p. 10) and adjustment for intake (Section 3.3, p. 11). **Adds:** "individual clinicians" are listed as units of comparison (p. 7), and the authors' conclusion is to use rankings "as screening instruments, but not as definitive judgements" (p. 16). That conclusion is the position the idea's oversight framing takes for workers. |
| Martin and Beerepoot, "Unveiling Use Cases for Human Resource Mining", BISE 2024 (vol. 67, pp. 531-550, 2025) | https://link.springer.com/article/10.1007/s12599-024-00894-3 | abstract + Crossref reference list (99 entries) | The Springer page shows "a preview of subscription content", so the full text was not read. The abstract is unchanged. The 99 deposited references were used for backward chasing (Section 2). None is a stability, sensitivity or validity study of resource measures. |
| Kelemen, "Measuring human resources performance using process mining" (DOI 10.24989/ocg.v335.41) | https://ejournals.facultas.at/index.php/ocgcp/article/download/2098/1753 | full-text (PDF; its font maps glyphs to ASCII minus 29, repaired with `decode_shifted_font.py`) | **Resolves the "unverified" flag** in the plan. The running header reads "CEE e\|Dem and e\|Gov Days 2019", pp. 497-504; Crossref's 2022 is the DOI registration year. It is a Google-Scholar-only review: search in December 2018, 254 → 151 → 22 → 9 papers (Section 2). It treats event-log measures as "objective information about employees' performance" (Abstract) and never discusses reliability, validity or robustness. Its stated future work is to combine Pika et al.'s DEA with a Balanced Scorecard (p. 504). |
| 4TU.ResearchData, "General terms of use" (August 2016; 4TU article 12721292) | https://data.4tu.nl/file/b39084ec-9338-4441-a8fd-fa9a022d4f0c/f4d8ddff-fad6-46ac-8546-83306408e827 (md5 matches the 4TU-supplied value) | full-text | **New for the feasibility side.** Data may be remixed only for non-commercial purposes (Art. 4b). Users must send 4TU the bibliographic details of every publication based on the data (Art. 3). Datasets with personal data may be used only for historical, statistical or scientific research under the VSNU code of conduct (Art. 7). This bears on releasing per-pseudonym ranking tables for BPI 2017 (4TU terms), but not BPI 2019 (CC BY 4.0). |
| Leribaux, Oyamada, De Smedt, Bozorgi, Polyvyanyy, De Weerdt, "Linking Actor Behavior to Process Performance over Time" (BPM 2025 Workshops, LNBIP 2026, 10.1007/978-3-032-13426-4_20) | https://arxiv.org/pdf/2507.23037 | full-text (arXiv v1) | **New.** Uses BPIC 2011, **2017 and 2019**. It builds daily time series of actor behaviours (continuation, interruption, handovers) and tests Granger causality on throughput time (Section 5, pp. 7-10). It names "User 1's handovers" as a top influence (p. 9). The idea card calls User_1 a system account with 148,404 events. The limitations (p. 11) note that behaviour classification depends on timestamp precision and task definitions and "can lead to misclassifications", but this is not tested. There is no per-actor ranking and no stability analysis. |
| Jeong, Lim, Bae, "BPIC 2017: Business process mining – A Loan process application" (BPIC 2017 student report) | https://ais.win.tue.nl/bpi/2017/bpi2017_paper_20.pdf | full-text (resource section pp. 21-24; whole report keyword-screened) | **New evidence for the idea's motivation.** Section 8 ranks the "top 4 resources" per workflow activity by mean execution time (Tables 14-16, pp. 23-24). Some ranked users have very few executions (one with 2). The report singles out users ("the company needs to investigate how he handled it fast", p. 23) and notes that mean execution time "tends to be lower as the execution number of resources is increased" (p. 23). There is no stability, interval or sensitivity analysis. |
| Rodrigues et al., "Stairway to value: mining a loan application process" (BPIC 2017 academic winner) | https://ais.win.tue.nl/bpi/2017/bpi2017_winner_academic.pdf | full-text (Section 4.6, pp. 13-15; whole report keyword-screened) | **New.** Labels 24 low-activity resources as "adding low value to the process" (p. 14). A footnote adds that some of them "seem to have left the company" and that others first appear late in the log (p. 14): a window and exposure problem raised but not handled. |
| Porter et al., "Balancing Efficiency and Risk in Procure to Pay" (BPIC 2019 non-student submission 8) | https://icpmconference.org/2019/wp-content/uploads/sites/6/2019/07/BPI-Challenge-Submission-8.pdf | full-text (pp. 22-25; whole report keyword-screened) | **New.** Restricts the analysis to the 112 of 627 resources with more than 3,000 compliance-related events and flags "three problematic users" by ID (p. 23). These are individual compliance flags derived from the log, with no robustness check. |

---

## 2. Citation-chasing log

Logs: `results/novelty/chase_log.csv` (every HTTP call), `chase_summary.csv` (one row per leg), `chase_works.csv` (every work returned, titles only) and `chase_screen.csv` (screen flags).

**Pacing.** Calls were at least 3.5 s apart. On HTTP 429 the script waited 30, 45 and 60 s, with at most 3 attempts per call.

**OpenAlex.** Single-work lookups (`works/doi:...`) answered 200. Every list query (`filter=cites:` or `filter=openalex:`) answered HTTP 429 "Insufficient budget ... free daily budget shared by everyone on your network's IP address ... resets at midnight UTC" (retry-after 63,964 s). After the first leg the script recorded later OpenAlex list legs as "not done" without retrying.

**Semantic Scholar** citation lists answered 200.

**Screen** (`screen_chase.py`): a work is a hit when its title or abstract contains worker or process-mining vocabulary (or an individual-professional analogue), plus a stability/ranking term, plus a performance term. All hits were read by hand.

| Seed | Direction | Tool | Status | Works returned | Hits / new relevant works found |
|---|---|---|---|---|---|
| Pika et al. 2017, TMIS (10.1145/3041218) | forward | OpenAlex | **not done**: HTTP 429, daily budget exhausted (OpenAlex cited_by_count = 66) | 0 | n/a |
| Pika et al. 2017 | forward | Semantic Scholar `/citations` | done | 62 records (33 with an S2 abstract) | 0 screen hits. Abstracts for 3 more works were read from landing pages: Martin and Beerepoot 2024; Rubensson, Pufahl, Mendling, EDOC 2024 Workshops; Aysolmaz, Nemeth, Iren, ECIS 2021 (3 duplicate S2 records). **38 of 62 records read at abstract level, 24 at title level.** No stability or sensitivity study. Nearest new works: Aysolmaz et al. 2021 (team benchmarking with process mining + DEA on a loan process, validated by interviews, no robustness reported in the abstract); Hoogmoed et al. 2025 (SoSyM, visual resource analytics with metrics for allocation, performance, workload and utilisation, user evaluation only); Yang et al. 2021 (BPM, group work profiles on five Dutch municipality logs); Rubensson et al. 2025 (SLR framework for resource analysis). Title-only records include "Holograph: A Tool for Assessing the Impact of Resource Assignment on Business Process Performance" (2018) and "Monitoring Employee Well-Being with Process Mining" (2024). |
| Martin and Beerepoot 2024, BISE (10.1007/s12599-024-00894-3) | backward | OpenAlex | **not done**: the lookup returned 79 referenced_works ids, but resolving them needs list calls (HTTP 429, budget) | 0 | n/a |
| Martin and Beerepoot 2024 | backward | Semantic Scholar `/references` | **not done**: `data: null`, "fields have been elided by the publisher" | 0 | n/a |
| Martin and Beerepoot 2024 | backward | Crossref `reference` list | done | 99 references | 0 screen hits; all 99 titles read. The SLR corpus cannot be separated from other references without the full text. Relevant entries: Caldeira et al., ICPM 2019 (software teams' efficiency from IDE logs); Swennen et al. 2016 (resource-behaviour metrics); Beerepoot et al., ICPM 2023 (active window tracking); Tang and Matzner, ICIS 2020 (humanistic value of process mining for work conditions); Wang et al. 2017 (process performance integrating time and resources). None measures stability or validity. |
| Saisana et al. 2005, JRSS A | forward | OpenAlex | **not done** (HTTP 429, budget; cited_by_count = 957) | 0 | n/a |
| Saisana et al. 2005 | forward | Semantic Scholar | done | 911 (390 with abstract) | 9 hits, 1 relevant: **Bas, Tarantola, Carot, Conchado 2016** (Social Indicators Research), a teaching-activity composite indicator for individual academic staff with sensitivity analysis. The other 8 concern countries, dams, firms or food security. 2 further titles mention workers (a tourism-awareness index; sales per employee); neither ranks individuals. |
| Adams et al. 2010, NEJM | forward | OpenAlex | **not done** (HTTP 429, budget; cited_by_count = 165) | 0 | n/a |
| Adams et al. 2010 | forward | Semantic Scholar | done | 162 (84 with abstract) | 23 hits, all in health care. Relevant (abstracts read): **Timbie, Hussey, Adams, Ruder, Mehrotra 2013** (Medical Care; after socioeconomic adjustment "only 1.1% of physicians changed relative cost rankings >2 percentiles"); **Kaye et al. 2019** (Urology; only 39%, 16% and 13% of top-quartile spenders stayed top-quartile the next year); **Adams and Paddock 2016** (HSR; tier misclassification 4.5-25.7% across three scoring systems); 2014 Statistics in Medicine (claims-based identification of poor performers "extremely sensitive to algorithm specificity"); Med Care 2013 variance-components profiling (title only). **None concerns non-clinical workers or event logs.** |
| Nakatumba and van der Aalst 2010 | forward | OpenAlex | **not done** (HTTP 429, budget; cited_by_count = 110) | 0 | n/a |
| Nakatumba and van der Aalst 2010 | forward | Semantic Scholar | done | 121 (42 with abstract) | 2 hits, both off-topic (concept-drift explanation; customer paths). 42 titles with resource/workload vocabulary were read. None is a stability study. Title-only: "Extracting accurate performance indicators from execution logs using process models" (2015) and "Investigating the Impact of Collaborative Patterns on Business Process Performance" (PACIS 2016). |
| Pika et al. 2014, CAiSE (extra leg, not in the plan) | forward | OpenAlex / Semantic Scholar | OpenAlex not done (429); S2 done | 37 (13 with abstract) | 0 hits |
| Topic sweep in lieu of OpenAlex `search` | n/a | arXiv API, 8 queries (`arxiv_queries.csv`, `arxiv_hits.csv`) | done (all HTTP 200) | 170 entries | No rank-stability study of worker measures. Adjacent: "One Model Many Scores" (multiverse for fairness metrics, 2023). |
| Topic sweep | n/a | Semantic Scholar `/paper/search`, 3 queries | **not done**: HTTP 429 on all 9 attempts | 0 | n/a |

Plan legs completed:
- **Pika forward:** done at abstract level for 38 of 62 records; 24 title-only.
- **Martin and Beerepoot backward:** done via Crossref only.
- **Saisana, Adams and Nakatumba forward:** done via Semantic Scholar only.

Every OpenAlex list leg is **not done** today.

---

## 3. Sweeps the earlier check named as not done

### 3a. ICPM, BPM, CAiSE and Process Science, 2022-2026

**Method** (`proceedings_sweep.py`). dblp (dblp.org and dblp.uni-trier.de) answered every request with an Anubis "Making sure you're not a bot!" page (HTTP 202). The plan's database could therefore not be used, and the venues were enumerated from Crossref instead:

| Venue group | Volumes enumerated (Crossref book records found 2026-10-19) | Papers |
|---|---|---|
| BPM main (LNCS) | BPM 2022, 2023, 2024, 2025, 2026 | 163 |
| BPM Forum (LNBIP) | 2022-2026 | 104 |
| BPM Workshops (LNBIP) | 2021 (published 2022) to 2025 | 176 |
| BPM Blockchain/RPA/CEE/Educators/Responsible BPM fora | 2022-2026 | 133 |
| CAiSE main (LNCS) | 2022-2026 (2025 and 2026 in two parts) | 186 |
| CAiSE Workshops | 2022-2026 | 123 |
| CAiSE Forum ("Intelligent Information Systems") | 2022-2026 | 121 |
| ICPM Workshops (LNBIP) | ICPM 2021-2024 workshops (published 2022-2025) | 165 |
| ICPM main (IEEE) | 2022 4th to 2025 7th (exact container-title match) | 130 |
| Process Science (Springer journal, ISSN 2948-2178) | all issues | 59 |
| **Total** | 46 enumeration units (`sweep_volumes.csv`) | **1,360** (`sweep_papers.csv`) |

Coverage gaps:
- The ICPM 2025 workshop volume was not in Crossref on 2026-10-19, so it is not covered.
- ICPM 2026 had no accepted-papers page (`icpmconference.org/2026/` answered 404).
- Abstracts came from Crossref for 176 papers and from Semantic Scholar's batch endpoint for 33. The S2 batch answered 200 once, then 429 six times, and OpenAlex enrichment was refused (budget). So **209 of 1,360 papers (15%) were screened at abstract level; the rest at title level.**

**Screening.**
- An automatic flag marked titles or abstracts with actor vocabulary plus a measure or robustness term: 41 papers at stage A, 9 at stage B, 9 on titles alone.
- All 139 titles containing actor or robustness vocabulary (resource, actor, employee, worker, human, workforce, staff, team, user, work, workload, fairness, robust, sensitiv, stabil, reliab, rank) were then read by hand.
- 17 of them were selected for abstract reading (`read_list_dois.txt`; abstracts from Crossref, Springer landing pages or Semantic Scholar via `fetch_abstracts.py`).

**Result.** No paper tests the stability, sensitivity or reliability of resource or worker performance rankings. The titles that contain stability or robustness terms concern other objects:
- process-discovery conditioning and stability (CAiSE 2026);
- stabilising DFG layouts (BPM 2025);
- stability of outcome predictions (ICPM 2023);
- adversarial robustness of predictive monitoring (ICPM 2022, 2023);
- process robustness by simulation (BPM Forum 2026);
- ranking event-log realisations (ICPM 2024 workshops).

The closest works:

| Work | Venue | Reading |
|---|---|---|
| Klijn, Tentina, Fahland, Mannhardt, "Decomposing Process Performance based on Actor Behavior" | ICPM 2024 | Splits waiting time into actor-behaviour components on a loan application process. It argues that average waiting times are "potentially misleading", which is a measure-definition point, at process level, without rankings. |
| Leribaux et al., "Linking Actor Behavior to Process Performance over Time" | BPM 2025 Workshops | Full text read (Section 1). |
| Braakman, Zuijderwijk, Beerepoot et al., "Mining for Well-Being" | BPM 2024 Workshops | Compares process-mining scores of work characteristics with validated survey measures and finds **"no strong correlations ... between corresponding survey variables and process mining variables"**. This is a convergent-validity test of log-derived worker measures: a different question from configuration stability, but the closest validity study found in the venues. |
| Leyer, ter Hofstede, Syed, "Detecting Weasels at Work" | BPM Forum 2023 | Event-log patterns for detecting undesirable employee behaviour, validated by a stakeholder survey. Shows that the community designs worker-surveillance patterns; no robustness analysis. |
| Revoredo, Bala, Santoro, "FairPM: A Taxonomy of Bias and Interventions in Process Mining" | BPM Forum 2025 | Bias taxonomy; no measurement study. |
| Beerepoot et al., "A Window of Opportunity: Active Window Tracking for Mining Work Practices" | ICPM 2023 | Brings monitoring-style telemetry into process mining. This narrows the proxy gap the feasibility file names, but measures nothing about ranking stability. |
| Rubensson, Pufahl, Mendling, "A Conceptual Framework for Resource Analysis in Process Mining" | EDOC 2024 Workshops | SLR. Finds resource-analysis methods "data-driven, developed to solve a specific business problem", with no mention of validity or stability. |

### 3b. BPI Challenge 2017 and 2019 report submissions

**Method** (`bpic_reports.py`). The 2017 listing page (`ais.win.tue.nl/bpi/2017/challenge.html`) and the 2019 listing page (`icpmconference.org/2019/bpi-challenge/`) were saved. All linked reports were downloaded: **23 for 2017 and 15 for 2019, all HTTP 200, 1,019 pages in total** (`bpic_reports_screen.csv`, with sha256 per report). Each report was keyword-screened for resource vocabulary, ranking vocabulary and stability vocabulary. Every line combining a resource term with a ranking term, and every stability-term line, was read.

**Result.**
- Six reports have resource-plus-ranking lines; nine contain a stability term. **No stability term refers to resource or worker rankings.** The terms concern robust medians, "reliable KPI", robust process mining and XmR charts.
- The resource sections of the most resource-heavy reports were read (Section 1 table). They show that challenge participants routinely rank or flag individual users on BPI 2017 and 2019 from single, unvalidated definitions:
  - Jeong et al.: mean execution time per activity, ranked users with as few as 2 executions;
  - Rodrigues et al.: "adding low value";
  - Porter et al.: "problematic users".
- Other reports cluster resources into roles (BPIC 2017 papers 27, 35 and 38; BPIC 2019 submission 8). None tests whether such judgements survive another metric, window or attribution rule.

This supports the idea's motivation and does not pre-empt it. Limit: text-based screening misses rankings that appear only in figures (several reports are figure-heavy).

### 3c. ICIS "IS and the Future of Work" tracks

**Method** (`icis_fow_tracks.py`). Public AIS eLibrary browse pages, track slugs read from the proceedings landing pages:

| Year | Track | Papers |
|---|---|---|
| 2022 | `is_futureofwork` | 17 |
| 2023 | `techandfow` | 20 |
| 2024 | `digtech_fow` | 25 |
| 2025 | `is_transformwork` | 24 |

ICIS 2026 (December 2026) had no proceedings online.

**Result.** **86 titles; 19 matched the title screen; all 86 were read** (`icis_fow_titles.csv`). The track studies algorithmic control and management through perceptions, taxonomies and field experiments, for example:
- "A Taxonomy of Algorithmic Control Systems" (2023);
- "Algorithm as Boss or Coworker?" (2023 field experiment);
- "Fear, Transparency, and Psychological Needs ... AI Workplace Surveillance" (2025);
- "From Digital Cage to Digital Compass" (2025);
- "The Shock Absorbers of Algorithmic Management" (2025).

**No paper audits the measurement properties of log-derived worker scores.** This matches the earlier check's statement that the algorithmic-management literature measures monitoring by self-report. Only titles were screened here, so a paper whose title hides such an audit would be missed.

### 3d. Other sweeps run

**27 WebSearch queries** (Section 8 lists them). Beyond the full-text location queries, the topics were:
- process-mining rank stability;
- DEA employee rankings;
- people analytics and telemetry;
- call-centre agents;
- warehouse pick rates;
- validity of algorithmic-management scores;
- teacher value-added multiverse;
- developer-productivity rankings;
- idle-time thresholds in occupational-health measurement;
- hospital-wide mortality methods;
- EU AI Act guidance;
- bossware accuracy;
- workforce analytics;
- analyst variability.

**New relevant works found:** Rhea et al. 2022; Oliveira et al. 2020; Shahian et al. 2010; Aysolmaz et al. 2021; the occupational-health idle-cutoff report; the AI Act timing note (all in Section 4).

**Practitioner-only results** (no peer-reviewed study of ranking stability surfaced): call-centre agents, warehouse pickers, bossware accuracy.

---

## 4. New prior-art comparison

These works are **not** in the 2026-10-05 table. Earlier entries (Pika et al. 2017, Adams et al. 2010, Papay 2011, Saisana et al. 2005, Steegen et al. 2016, Silberzahn et al. 2018, Qafari and van der Aalst 2019, Gu and Koenker 2023 and the rest) stand, with the full-text corrections of Section 1.

| Work | Year | Venue / status | Link | What it does | Overlap with the idea | What the idea still adds | Access depth |
|---|---|---|---|---|---|---|---|
| Thomas and Ward, "Economic Profiling of Physician Specialists: Use of Outlier Treatment and Episode Attribution Rules" | 2006 | Inquiry 43(3), 10.5034/inquiryjrnl_43.3.271 | https://doi.org/10.5034/inquiryjrnl_43.3.271 | 18 simulations per specialty crossing 3 episode-attribution rules with 6 outlier methods, scoring the sensitivity and specificity of classifying cost-efficient physicians; "no consistent combination ... was found to be superior for identifying cost-inefficient physicians" | **The closest design precedent:** a crossed factorial over measurement choices (attribution x outlier treatment) for individual professionals' scores, evaluated by classification accuracy | Event logs and non-clinical workers; process-mining factors (metric, window, idle gap, case-mix); rank agreement and variance decomposition across the full configuration space; public data; open audit artefact | abstract (Crossref) |
| Mehrotra, Adams, Thomas, McGlynn, "The Effect of Different Attribution Rules on Individual Physician Cost Profiles" | 2010 | Annals of Internal Medicine, 10.7326/0003-4819-152-10-201005180-00005 | https://doi.org/10.7326/0003-4819-152-10-201005180-00005 | 12 attribution rules applied to the same claims; 20-69% of episodes attributable; versus the default rule, "17 to 61% of physicians would be assigned a different category" | Exactly the idea's **attribution factor** and its reclassification statistic, for physicians | The other four factors, their interactions, and transfer to workflow logs | abstract (Semantic Scholar) |
| Timbie, Hussey, Adams, Ruder, Mehrotra, "Impact of Socioeconomic Adjustment on Physicians' Relative Cost of Care" | 2013 | Medical Care, 10.1097/mlr.0b013e31828d1251 | https://doi.org/10.1097/mlr.0b013e31828d1251 | Rankings with and without socioeconomic adjustment on top of case-mix adjustment; "only 1.1% of physicians changed relative cost rankings >2 percentiles"; case mix explained "nearly 70%" of the variation in average episode cost | The **case-mix/adjustment factor** with a ranking-change statistic, and a **counter-example**: one added adjustment barely moved rankings | Whether case-mix adjustment matters for worker rankings in event logs (H2) is an open empirical question, not a foregone one | abstract (Semantic Scholar) |
| Kaye, Ye, Li, Herrel, Dupree, Ellimoottil, Miller, "The Stability of Physician-Specific Episode Costs for Urologic Cancer Surgery" | 2019 (online 2018) | Urology, 10.1016/j.urology.2018.04.051 | https://doi.org/10.1016/j.urology.2018.04.051 | Year-to-year persistence of top-quartile spenders: 39%, 16% and 13% by procedure; weak or no year-to-year correlation | The **window/time factor** (H3) for individual professionals | Window length as a factor crossed with the others; event logs | abstract (Semantic Scholar) |
| Adams and Paddock, "Misclassification Risk of Tier-Based Physician Quality Performance Systems" | 2016 | Health Services Research, 10.1111/1475-6773.12561 | https://doi.org/10.1111/1475-6773.12561 | Beta-binomial reliabilities for 23,085 physicians; misclassification 8.6-25.7%, 6.4-22.8% and 4.5-21.7% under three scoring systems | Tier-misclassification statistic across scoring systems | As above | abstract (Crossref) |
| Shahian, Wolf, Iezzoni, Kirle, Normand, "Variability in the Measurement of Hospital-wide Mortality Rates" | 2010 | NEJM, 10.1056/nejmsa1006396 | https://doi.org/10.1056/nejmsa1006396 | Four vendors' methods on the same 2.5 M discharges; inclusion 28-95%; 12 of 28 hospitals flagged high by one method were low by another (per snippet) | "Same data, different methods, discordant classification" at institution level, with a policy audience | Individual workers; configuration factorial; logs | metadata/snippet |
| Bas, Tarantola, Carot, Conchado, "Sensitivity Analysis: A Necessary Ingredient for Measuring the Quality of a Teaching Activity Index" | 2016 | Social Indicators Research, 10.1007/s11205-016-1297-2 | https://doi.org/10.1007/s11205-016-1297-2 | Composite indicator of **individual academic staff's** teaching activity at a Spanish university, with sensitivity analysis of effective versus intended weights | Saisana-style sensitivity analysis applied to individual employees' scores | Event-log measures; rank stability across non-weighting choices (window, idle gap, attribution) | abstract (Springer page) |
| Rhea, Markey, D'Arinzo, Schellmann, Sloane, Squires, "An external stability audit framework to test the validity of personality prediction in AI hiring" | 2022 | Data Mining and Knowledge Discovery, 10.1007/s10618-022-00861-0; arXiv 2201.09151 | https://arxiv.org/abs/2201.09151 | Socio-technical framework and open-source library for **external stability audits** of algorithmic HR tools (Humantic AI, Crystal), on the premise that "reliability is a necessary, but not a sufficient, condition for validity" | The idea's **audit-artefact framing** (open tool, stability as a precondition for validity, high-stakes HR) already exists for hiring | Performance evaluation rather than hiring; deployer-side configuration choices rather than input perturbations of a vendor black box; event logs | abstract (arXiv) |
| Oliveira, Fernandes, Steinmacher, Cristo, Conte, Garcia, "Code and commit metrics of developer productivity: a study on team leaders perceptions" | 2020 | Empirical Software Engineering, 10.1007/s10664-020-09820-z | https://doi.org/10.1007/s10664-020-09820-z | Eight leaders ranked their developers; Kendall-type correlations of leader rankings with code-based and commit-based metric rankings | Metric choice changes how individual workers rank against a criterion, in software engineering | No configuration factorial; the idea has no criterion and studies internal agreement across configurations | abstract (Springer page) |
| Braakman, Zuijderwijk, Beerepoot, Lugtigheid, Martens, Peeters, "Mining for Well-Being: The Potential of Process Mining for Evaluating Employee Well-Being" | 2025 | BPM 2024 Workshops, LNBIP, 10.1007/978-3-031-78666-2_14 | https://doi.org/10.1007/978-3-031-78666-2_14 | Process-mining scores of work characteristics (workload, autonomy and others) compared with validated survey scales; "no strong correlations" between corresponding variables | **Validity of log-derived worker measures**, inside the BPM community | Rank stability across configurations; performance scores rather than well-being; variance decomposition | abstract (Springer page) |
| Klijn, Tentina, Fahland, Mannhardt, "Decomposing Process Performance based on Actor Behavior" | 2024 | ICPM 2024, 10.1109/icpm63005.2024.10680657 | https://doi.org/10.1109/icpm63005.2024.10680657 | Decomposes waiting time by actor behaviour (continuation, interruption, handover) with event knowledge graphs; evaluated on a loan application process | Shows that a single performance measure can mislead and that actor behaviour should be separated, on a log of the BPI 2017 type | Worker rankings, configuration factorial, stability statistics | abstract (Semantic Scholar) |
| Leribaux, Oyamada, De Smedt, Bozorgi, Polyvyanyy, De Weerdt, "Linking Actor Behavior to Process Performance over Time" | 2026 (arXiv 2025) | BPM 2025 Workshops, LNBIP, 10.1007/978-3-032-13426-4_20 | https://arxiv.org/abs/2507.23037 | Granger causality from daily actor-behaviour series to throughput time on BPIC 2011, 2017 and 2019 | Same public logs (BPI 2017 and 2019); names misclassification risk from timestamp and task definitions without testing it; treats User 1 as an actor | Testing those definitional choices; per-worker rankings; system-account handling | full-text (arXiv) |
| Leyer, ter Hofstede, Syed, "Detecting Weasels at Work" | 2023 | BPM Forum 2023, LNBIP, 10.1007/978-3-031-41623-1_20 | https://doi.org/10.1007/978-3-031-41623-1_20 | Event-log patterns for undesirable employee behaviour, validated by a stakeholder survey | Individual-level evaluative use of logs in the BPM community | Measurement robustness of such patterns | abstract (Springer page) |
| Aysolmaz, Nemeth, Iren, "A method for objective performance benchmarking of teams with process mining and DEA" | 2021 | ECIS 2021 Research Papers 144 | https://aisel.aisnet.org/ecis2021_rp/144 | Design-science method benchmarking **teams** with process mining + DEA + SNA on a real-life loan management process, validated by interviews; claims an "objective and transparent mechanism" | IS-venue precedent for log-based performance benchmarking of work units | Individuals; robustness of the benchmark to metric and configuration choice (the PDF answered 403, so whether the full text has a DEA sensitivity analysis is **not known**) | abstract (AISeL) |
| Jeong, Lim, Bae; Rodrigues et al.; Porter et al. (BPIC 2017 and 2019 reports) | 2017, 2019 | BPI Challenge reports (not peer-reviewed) | see Section 1 | Per-user rankings and flags from single definitions on the idea's two pilot logs | **Motivating evidence**: the practice the idea audits, on the same data | Everything the audit measures | full-text (sections) |
| Caldeira, Brito e Abreu, Reis, Cardoso, "Assessing Software Development Teams' Efficiency using Process Mining" | 2019 | ICPM 2019, 10.1109/icpm.2019.00020 | https://doi.org/10.1109/icpm.2019.00020 | Process models discovered from IDE event logs of teams compared on efficiency against expert-assessed quality | Log-based efficiency comparison of work units, with a quality criterion | Individuals; configuration robustness | abstract (Semantic Scholar) |
| Occupational-health measurement of computer use from keyboard/mouse logs (CDC-linked progress report; NTU 2007 VDTlog thesis) | n/a | grey literature | https://stacks.cdc.gov/view/cdc/218598/cdc_218598_DS1.pdf | Per snippet: activity-duration cutoffs of 28-60 s gave unbiased estimates of computer-use duration; most software uses a 30 s cutoff; validated against video | The **idle-gap factor** has been calibrated against observation for duration measurement | Effect of the cutoff on worker rankings | metadata/snippet |
| AI Act timing (law-firm commentary on the "Digital Omnibus") | 2026 | McCann FitzGerald note, via WebSearch | https://www.mccannfitzgerald.com/knowledge/data-privacy-and-cyber-risk/employment-spotlight-eu-ai-act-draft-guidelines-on-high-risk-ai-classification | Per snippet: political agreement postpones Annex III high-risk obligations (including employment) from 2 August 2026 to 2 December 2027; draft Commission classification guidelines | Changes the idea's policy hook from "already applicable" to "applicable from late 2027 if enacted" | n/a (framing) | metadata/snippet; **to verify** against the Official Journal before use |

---

## 5. Updated verdict: partially-covered

**Why not "likely-novel".** The 2026-10-05 check had already shown that the construct and statistics exist under other names. The full texts and the chasing now show that the **design** exists too, for one class of workers:

1. **Measurement-choice designs for individual professionals' scores exist in physician profiling.**
   - Crossed rules: Thomas and Ward 2006 cross attribution rules with outlier treatments.
   - One factor at a time: Mehrotra et al. 2010 vary attribution (17-61% reclassified); Timbie et al. 2013 vary adjustment (1.1% moved more than 2 percentiles); Kaye et al. 2019 vary time (13-39% persistence of top-quartile spenders).
   - Two of the idea's five factors (attribution and adjustment) and its window hypothesis therefore have direct, published analogues with the same statistics.
2. **The audit-artefact framing exists for algorithmic HR.** Rhea et al. 2022 published a stability-audit framework with an open-source library and the reliability-before-validity argument.
3. **Inside process mining, validity questions about log-derived worker measures have started.** Braakman et al. 2025 found weak convergence with survey measures. Klijn et al. 2024 and Leribaux et al. 2025 show that single performance measures mislead and that actor-behaviour definitions matter, on the idea's own logs.

**Why not "largely-covered".** After the sweeps in Section 3, **no study was found that:**
- treats the scoring configuration of log-derived **worker** performance measures as a crossed factorial on **public event logs**, with factors specific to process mining (metric x attribution x window x idle gap x case-mix);
- reports rank agreement, quintile reclassification and a variance decomposition over those factors;
- handles automated accounts as a validity threat, calibrated on BPI 2019's labelled split;
- releases a pm4py audit protocol;
- ties the result to deployer oversight of worker-evaluation systems.

The physician studies do not use event logs, do not vary metric definitions, idle thresholds or window jointly with attribution, and do not decompose ranking variance across factors. The process-mining studies do not rank workers or test stability. The BPI Challenge reports show the unaudited practice on the same data.

**How the claimable contribution should now be stated.** Not "the first study of rank instability in worker scores", which is refuted by the physician literature. Instead: "the first configuration-factorial reliability audit of event-log worker scores, transferring physician-profiling misclassification analysis and composite-indicator sensitivity analysis to process mining, with an open audit artefact". This is the same category as before (application-level transfer plus engineering artefact), with more antecedents to cite.

**Changes to the recommendations of 2026-10-05.**
- **Cite directly:** Thomas and Ward 2006; Mehrotra et al. 2010; Timbie et al. 2013; Kaye et al. 2019; Adams and Paddock 2016; Shahian et al. 2010; Rhea et al. 2022; Bas et al. 2016; Braakman et al. 2025; Klijn et al. 2024; Leribaux et al. 2025. Use the physician factorials as the explicit design template and comparator. For example, the attribution factor's reclassification can be set against the 17-61% range.
- **Treat H2 as open.** Timbie et al. found that an extra adjustment barely moved rankings.
- **Pre-register the window for any workload covariate.** Nakatumba's workload measure has its own window parameters.
- **Use Gu and Koenker's left-tail results** to justify comparing raw bottom-quintile selection with precision-aware selection. Their oracle "even odds" bound shows that bottom-quintile flags can be unreliable even under ideal estimation.
- **Use the BPI Challenge reports as motivating cases** (users ranked from 2 executions; "adding low value"; "problematic users"). Report only aggregates, given the 4TU terms (Art. 3, 4b, 7) for BPI 2017.
- **Re-time the AI Act argument** if the Digital Omnibus postponement to December 2027 is confirmed.

The verdict defaults to partially-covered and is not a borderline call. The new evidence moves the idea toward "transfer" but does not find the specific study.

---

## 6. Literature stop condition

**Rule as written** (section 4.2): "also stop if the proceedings sweep finds a rank-stability study of resource measures on public logs."

**Decision: not triggered.**

**Evidence:**
- **Proceedings sweep.** 1,360 papers enumerated from 41 Springer volumes (BPM, BPM Forum, BPM Workshops, BPM fora, CAiSE, CAiSE Workshops, CAiSE Forum, ICPM Workshops 2022-2026), ICPM 2022-2025 (IEEE) and Process Science. 139 titles read by hand, 209 abstracts screened automatically, 17 selected abstracts read. No rank-stability, sensitivity or reliability study of resource measures. The nearest are Klijn et al. 2024, Leribaux et al. 2025 and Braakman et al. 2025, none of which ranks resources or tests stability.
- **BPI Challenge 2017 and 2019 reports** (38 reports, 1,019 pages). Per-resource rankings exist, but no stability analysis.
- **Forward chasing** of Pika et al. 2017 (62), Pika et al. 2014 (37) and Nakatumba and van der Aalst 2010 (121) on public logs, and of Adams et al. 2010 (162) and Saisana et al. 2005 (911) outside them. The rank-stability studies found (physician profiling) use claims data, not public event logs.
- **arXiv API** (8 queries) and **WebSearch** (27 queries): nothing that meets the condition.

**Why not "undetermined".** The sweep was run on the venues the plan names, and every title containing stability, robustness, ranking or reliability vocabulary was read. The residual risk is a paper whose title has no such terms and whose abstract was not available. Section 7 lists the gaps: abstract coverage of 15%, the ICPM 2025 workshop volume, and dblp/OpenAlex unavailability. If one of those later surfaces such a study, the rule must be re-applied as written.

---

## 7. Search limits

- **dblp.** The Anubis bot check answered every call on two hosts, so the plan's dblp sweep was replaced by Crossref enumeration by ISBN and ISSN. Crossref may miss chapters deposited without the volume ISBN, and the ICPM 2025 workshop volume was not in Crossref.
- **OpenAlex.** List queries were refused for the whole session: daily budget for the shared IP exhausted, retry-after about 17.8 h. Only single-work lookups worked. All OpenAlex forward and backward legs are "not done". A free API key was offered by the error message but was not requested, because that would create an account on the user's behalf.
- **Semantic Scholar.** No API key. Citation lists worked. Keyword search failed with 429 on all 9 attempts. The batch abstract endpoint answered once and then 429. The Martin and Beerepoot reference list is elided by the publisher.
- **Abstract coverage.** Only 209 of 1,360 sweep papers (15%) were screened at abstract level, plus 29 targeted abstract fetches. For Pika et al.'s 62 citing records, 38 were read at abstract level and 24 at title level.
- **Paywalled full texts.** Saisana et al. (OUP 403) and Papay (SAGE 403) were read at abstract level only. The RAND TR-799 methodology (rand.org 403) was read as a PMC summary only, and the NEJM supplementary appendix (reCAPTCHA) was not read. Martin and Beerepoot (Springer, subscription) and Oliveira et al. (Springer, subscription) were read at abstract level; Aysolmaz et al. (AISeL PDF 403) at abstract level.
- **Older version.** Gu and Koenker was read in its arXiv v3 (2021), not the published Econometrica version. Goldstein and Spiegelhalter was read from a preprint without the published discussion.
- **BPI Challenge reports.** Screened by extracted text only. Rankings shown only in figures would be missed; reports of other BPI Challenge years were not screened.
- **ICIS.** Future-of-work tracks screened by title only; other ICIS tracks, ECIS and other AIS venues were not swept. AIS eLibrary full-text search refuses automated clients.
- **Not swept.** Google Scholar, Scopus and Web of Science were not used; only English-language sources were covered.
- **Snippet-only items.** Shahian et al. 2010, Atteberry and Mangan 2020, the occupational-health idle-cutoff report and the AI Act timing note are known from WebSearch snippets only. Every number quoted from them is the snippet's, and each must be verified before citation.

---

## 8. Reproducibility

**Software.**
- Python 3.11.15 (venv at `/tmp/claude-0/-home-user-employee-monitoring-system/c64eab22-9c10-592c-b92e-5ac629c5be82/scratchpad/venv/bin/python`, run with `-I`); the scripts use only the standard library.
- pdftotext 24.02.0; curl 8.5.0.
- No random numbers are used, so there are no seeds.

**Scripts** (all under `research/06_stage4/idea05/code/novelty/`; order in `run_novelty.sh`):

| Script | Purpose |
|---|---|
| `fetch_fulltexts.py` | Full texts named by the plan, plus Crossref records |
| `html2text.py` | HTML to text |
| `decode_shifted_font.py` | Repairs the Kelemen PDF text |
| `kwic.py` | Page-referenced keyword search |
| `chase_citations.py`, `screen_chase.py` | Citation chasing and screening |
| `proceedings_sweep.py`, `fetch_abstracts.py` | Venue sweep and abstract fetching |
| `bpic_reports.py` | BPI Challenge report download and screen |
| `icis_fow_tracks.py` | ICIS future-of-work track listings |
| `arxiv_queries.py` | arXiv API topic queries |

**Outputs** (`research/06_stage4/idea05/results/novelty/`):
- `fulltext_manifest.csv`, `fulltext_manifest_extra.csv` (sha256 of every full text read);
- `crossref_records.csv`;
- `chase_log.csv`, `chase_summary.csv`, `chase_works.csv`, `chase_screen.csv`;
- `sweep_volumes.csv`, `sweep_papers.csv`, `sweep_log.csv`, `read_list_dois.txt`;
- `bpic_reports_screen.csv` (sha256 per report);
- `icis_fow_titles.csv`;
- `arxiv_queries.csv`, `arxiv_hits.csv`.

Abstract texts are kept only in the scratchpad (`abstracts.jsonl` files), not in the repository.

**Selected checksums (sha256):**

| Document | sha256 |
|---|---|
| Adams et al. NEJM, PMC HTML | `10cd80e793515d6a458632357de5d64a71c8ea3c423572e9ec4e43cfad70f3c3` |
| Gu and Koenker, arXiv PDF | `5099b9f389535d35dc52e15f0a93a60fbf95bee86fd890abff919aa6164ee302` |
| Nakatumba and van der Aalst, author copy | `9359182b962dff036147321ab33a5f5af2f68badd20fb80f222d982dcba58654` |
| Goldstein and Spiegelhalter, preprint | `3afdd705a25039b6385ae1208aa4854af81cd5cd44ddc171c8973039e3f54265` |
| Kelemen | `5c049de3d7b047ad00fbb94962832f360cd2dd341fcce718210cea81c1692f43` |
| 4TU terms PDF | `e4dc9caf93f5d19cc5b7d1d48a15f363e5f59eb8a54f1aabafed2e79f4a26f04` (md5 `5a37f1aea024a6339971a69994e094d5`, as supplied by 4TU) |
| Leribaux et al., arXiv PDF | `edde0c035d4dd31b07241c66e3a5db641a7ead3566b02b82f0a14a3c5e2e1b51` |

**Wall-clock (UTC, 2026-10-19):**

| Step | Time |
|---|---|
| Session | 06:01-07:00 |
| Full-text fetch | 06:04-06:05 (53 s) |
| Citation chasing, second run | 06:13-06:15 (111 s) |
| Crossref-only enumeration | 06:13-06:20 |
| Full sweep with enrichment | 06:21-06:29 |
| BPIC reports | about 06:27-06:30 |
| ICIS crawl | about 06:31 (under 1 min) |
| arXiv queries | about 06:36 (under 1 min) |

**Query and call counts:**

| Source | Count | Notes |
|---|---|---|
| WebSearch | 27 | Locating full texts: 8. Topic sweeps: 19. |
| arXiv API | 8 queries | All 200 |
| Semantic Scholar keyword search | 3 queries | 9 attempts, all 429 |
| Semantic Scholar citation-list legs | 6 | 5 done, 1 elided |
| Semantic Scholar per-DOI and batch calls | about 17 | |
| dblp | 3 probes | All bot check |
| Crossref enumeration | 46 units | `sweep_log.csv`: 46 Crossref calls answered 200 after 4 retries on 429 |
| Crossref exploratory and title queries | about 33 | Not logged by a script; reconstructed from this session's commands |
| Crossref per-DOI records | 48 | |
| OpenAlex single-work lookups | 15 | 200 |
| OpenAlex list calls | 2 attempts | 429; later legs skipped |
| BPI Challenge PDFs | 38 | Plus 3 listing pages |
| AIS eLibrary | 4 track pages | Plus 4 proceedings landing pages |
| WebFetch | 0 | |

**Deviations from the written plan and from this session's own procedure:**

1. **dblp replaced by Crossref** enumeration (bot wall). Semantic Scholar "with key" was not possible (no key).
2. **OpenAlex list legs not done** (daily budget). Forward chasing used Semantic Scholar only; backward chasing used Crossref only.
3. **Extra leg** not in the plan: Pika et al. 2014 forward.
4. **The first chase run crashed** on Semantic Scholar's `data: null` for the publisher-elided reference list of Martin and Beerepoot. The script was fixed to record "not done (elided)" and re-run. The first run's raw output is kept as `chase_attempt1_crashed/` in the scratchpad, and its partial results were discarded.
5. **The BPIC 2019 downloads first failed** because the listing links use plain `http://`, which the proxy refuses. The script was changed to `https://` and re-run.
6. **The first Adams et al. PMC fetch returned a reCAPTCHA page.** The retry with the project user agent succeeded. `fulltext_manifest.csv` still lists the failed first fetch; `fulltext_manifest_extra.csv` records the retry.
7. **Contact email removed from requests.** Early calls in this session sent a personal contact email in Crossref/OpenAlex `mailto` parameters and the User-Agent: the first full-text fetch, OpenAlex/Semantic Scholar probes, Crossref facet queries and the first chase run. This copied the convention of the sibling idea-6 scripts. It was then removed from all scripts, which now follow the repository's own convention in `research/tools/verify_refs.py` ("contact via repository owner").
8. **One stray arXiv `id_list` lookup** (2511.21011, unrelated to the topic) was sent by mistake while reading Rhea et al.'s abstract. Its result was ignored.
9. **Pilot criteria not assessed here.** The pilot clauses of the stopping rule are assessed in `README.md`.
