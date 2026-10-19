# Stage 4 deep novelty check, idea 4: sampling uncertainty, exclusion rules and pooling in NYC Local Law 144 impact ratios

**Date:** 2026-10-19 (cloud container: 4 vCPU, 15 GB RAM, Python 3.11 venv; no API keys). **Stance:** adversarial. The job was to find prior work that removes the idea's novelty, and above all work that meets the literature stop condition in `research/02_candidate_ideas.md` section 4.3.

**Inputs read first (in this run):**
- `research/02_candidate_ideas.md`: the Idea 4 card and section 4.3.
- `research/03_challenge/04-published-but-uninformative-sampling-uncertainty__novelty.md`: the earlier check of 2026-10-05, with its comparison table, verdict and search limits.
- `research/03_challenge/04-published-but-uninformative-sampling-uncertainty__feasibility.md`.
- `research/06_stage4/idea04/README.md`: the pilot written by another agent. It is used here only for its reading of the ACLU code (stopping-rule criterion 1).

**Bottom line.**
- **Verdict:** **partially-covered**, the same as before. The coverage has shifted, though:
  - The headline of the *pooling* lever ("pooling across employers hides adverse impact") has now been shown on real applicant data in a FAccT 2026 paper (Bommasani et al.). It also has an I-O simulation lineage on aggregation tests.
  - The *reporting designs* (intervals, significance tests, practical significance) are practitioner consensus in I-O. The 2010 TAC report is the clearest example.
- **Still unrecorded after this check:**
  - sampling intervals, posteriors and UGESP tests attached to the published LL 144 ratios;
  - applicant shares removed by the 2% rule;
  - a combined simulation of the 2% exclusion, the unknown exclusion, the median split, intersectional splitting and pooling, calibrated to the published corpus;
  - a measured "manipulation range" on real reports.
- **Literature stop condition:** **not triggered**, within the searches listed in section 7.

Path conventions:
- `$ND` = `/tmp/claude-0/-home-user-employee-monitoring-system/c64eab22-9c10-592c-b92e-5ac629c5be82/scratchpad/data/idea04/novelty_deep`. This is untrusted downloaded material, outside the repository.
- Scripts are in `research/06_stage4/idea04/code/`.
- Small derived files are in `research/06_stage4/idea04/results/`.

---

## 1. Full texts and primary documents read

Access depth uses three levels:
- **full-text:** the whole PDF was obtained; the named sections were read and the rest was keyword-grepped.
- **abstract:** only the abstract was read, from Crossref, a publisher landing page, an arXiv listing or a mirror.
- **metadata/snippet:** only Crossref metadata, a reference list and/or WebSearch snippets were seen.

Page numbers are the printed page numbers unless "PDF p." is given.

| Title (plan item) | Source URL | Access depth | What the reading confirms, corrects or refutes relative to the 2026-10-05 check |
|---|---|---|---|
| Gerchick et al., "Auditing the Audits" (FAccT '25), re-read with the simulation design in hand | https://facctconference.org/static/docs/facct2025-206archivalpdfs/facct2025-final14-acmpaginated.pdf (sha256 `586a788f…a56af19c`) | full-text | **Confirms:** the per-ratio bounds are deterministic missing-data bounds, not sampling intervals. Eq. 1 puts all *x* unknown applicants into group *a* (Section 4.2.4, p. 35). The 70% worst-case and 28% proportional-allocation figures are confirmed (p. 35; Appendix A.4, p. 42). The appendix says that alternative assumptions about other groups' rates were explored, and all of them are deterministic. Section 5.2.3 (p. 37) recommends "uncertainty bounds ... that take into account missing data". In this PDF the grep counts are 0 for "confidence", "standard error", "sample size", "simulat", "bootstrap", "binomial" and "Fisher". "statistical" has 3 hits, none about sampling.<br>**Confirms (qualitative only):** pooling is treated qualitatively in Section 4.1.1 (p. 33): "it was often impossible to tell how much of that specific employer's actual data was used". The 2% exclusion is treated qualitatively in Section 4.2.2 (p. 34). Section 5.2.4 (pp. 37-38) asks for transparency on aggregation. Section 6 (p. 38) proposes only re-running the patterns on more audits. No simulation is proposed.<br>**New for chasing:** the paper cites "D-hacking" [24], Morris and Dunleavy's *Adverse Impact Analysis* book [91], and Raghavan and Kim **2024**, Geo. L. Tech. Rev. 8:93 [101]. The last corrects the earlier check, which gave the year as "not shown". |
| Lam et al., "A Framework for Assurance Audits of Algorithmic Systems" (FAccT '24) | https://arxiv.org/pdf/2401.14908 (v2; sha256 `249261a2…bf630a1d6`) | full-text | **Confirms**, with one correction of sub-criterion numbering against Table 2 (PDF p. 14). The uncertainty requirement is **Q.G.2** ("results of uncertainty analysis (e.g., standard error for the mean) or error propagation of impact ratios"). The 2% exclusion disclosure is **Q.G.4** (justification, sample size, rate). **Q.H.1** prescribes the two-sample binomial Z-test for n >= 30 and Fisher's exact test below 30. Section 4.2.1 (PDF p. 6) lists "impact ratio calculations, including of uncertainties (Q.G)". The paper proposes criteria. It applies none of them to published reports. |
| Watkins, McKenna, Chen, "The four-fifths rule is not disparate impact" (FAccT '24) | https://arxiv.org/pdf/2202.09519 (sha256 `3c4f6198…7e2869`) | full-text | **Confirms** the earlier abstract-level reading: the 4/5 rule is a rule of thumb that toolkits (AIF360, Aequitas) codify (section 3). Courts prefer significance testing "principally, the greater consistency of statistical significance" (PDF p. 3).<br>**New:** Appendix A quotes 29 CFR 1607.4(D) (PDF p. 9). Differences "based on small numbers and ... not statistically significant" may not be adverse impact. When numbers are "too small to be reliable", evidence over a longer period or "in similar circumstances elsewhere may be considered". UGESP itself therefore contemplates pooling over time and sites for small samples. The paper never mentions Local Law 144 (0 hits). |
| Ferrara et al., "Size-adaptive Hypothesis Testing for Fairness" (NeurIPS 2025) | https://arxiv.org/pdf/2506.10586 (sha256 `3c09d800…84047d7`) | full-text | **Corrects** the earlier check, which treated "ratio metric against 0.8 rather than parity difference" as a difference. The framework covers the **Disparate Impact ratio** as a special case of Theorem 2 (PDF p. 7, "the asymptotic behaviour of the Disparate Impact assessment"). It generalises Besse et al.'s asymptotic CIs for DI ratios (PDF p. 2). The Dirichlet-multinomial posterior is metric-agnostic. "four-fifths" appears only in reference titles. No LL 144 and no audit corpus.<br>**Backward chasing** (reference list, PDF pp. 10-12) adds Besse et al. 2018 (CIs for testing disparate impact) and Himmelreich et al. 2025 (intersectional hypothesis testing). |
| Hilliard, Gulley, Koshiyama, Kazim, "Bias audit laws" (IRLCT 2024) | https://research.gold.ac.uk/id/eprint/37547/ (OA PDF, sha256 `c0b674a8…0627e7`) | full-text | **Confirms** the earlier snippet-level reading: this is a legal/conceptual review. Section 5.1 (PDF p. 10) notes "a lack of reliability for small sample sizes" of the four-fifths rule, citing Morris and Lobsenz 2000. The 2% exclusion is mentioned only as a reporting item (Section 4.1.3). Grep counts are 0 for "simulat", "pool", "Fisher" and "z-test". No corpus statistics. |
| Morris and Lobsenz 2000, Personnel Psychology | https://api.crossref.org/works/10.1111/j.1744-6570.2000.tb00195.x | abstract (+ Crossref reference list, 39 items) | Abstract unchanged from the earlier reading. The reference list is the 1979-1997 antecedent literature: Greenberg 1979; Boardman 1979; Wing 1982 "Statistical hazards ... with small samples"; York 1995. None of it concerns exclusion rules or pooling. Wiley full text not fetched (publisher refuses). |
| Roth, Bobko, Switzer 2006, J. Applied Psychology | Abstract mirror https://academicnewsletter.sufe.edu.cn/info/372321 ; third-party course outline https://web.pdx.edu/~mccunee/quant_621/Outlines/Roth,%20Bobko,%20Switzer%202006.doc (sha256 `ad280c7d…ae217`) ; Crossref reference list (50 items) | abstract (+ third-party summary, not the paper) | **Upgrades** the earlier metadata/snippet reading to the abstract.<br>**Per the outline (not verified against the paper):** Study 1 varies applicant-pool size (200, 400, 2,000), minority proportion and selection ratio in two-hurdle systems with d = 0. False positives were 10-35% at N = 200 with 12% minorities. Follow-up tests were Fisher (N = 200, 400) and chi-square (N = 2,000), with "one-person"/"N of 1" rules. Study 2 uses meta-analytic d values.<br>Nothing in the abstract, the outline or the reference list indicates a 2%-type exclusion or cross-employer pooling factor. The backward list adds Morris 2001, "Sample size required for adverse impact analysis" (Applied HRM Research). |
| Collins and Morris 2008, J. Applied Psychology | https://academicnewsletter.sufe.edu.cn/info/371782 | abstract | **Upgrades** metadata to abstract. The study compares tests by Type I error and power at small n. Significance testing "of limited value because of low power". The Z-test performs reasonably except at extremely small n. **Fisher's exact test and Yates are not recommended** (too conservative, lower power).<br>**New tension:** Lam et al.'s Q.H.1 prescribes Fisher below n = 30. A reporting-design comparison should test that choice. |
| Switzer, Roth, Rosopa 2016, Human Performance | https://api.crossref.org/works/10.1080/08959285.2016.1154060 | metadata (+ Crossref reference list, 28 items) | Still metadata only. Semantic Scholar states the abstract is "elided by the publisher". Clemson profiles (WebSearch snippet) give a title variant, "Statistical power of various adverse impact indices", Human Performance 29(3), 159-171. The reference list covers the small-sample and power literature (Biddle and Morris 2011; Hauenstein et al. 2013; Morris 2001; Roth et al. 2006; Collins and Morris 2008). Whether it varies an exclusion or pooling factor **remains unverified**. |
| Aobdia, Ma, Zhang 2025, SSRN (motivation rewrite) | https://api.crossref.org/works/10.2139/ssrn.5703842 | abstract (SSRN not fetched) | **Confirms** the earlier abstract: difference-in-differences; about a two-percentage-point fall in the male share of hires; no effect on white hiring; longer time to fill. Authors per Crossref: Daniel Aobdia, Hao Ma, Sheryl Zhang.<br>**New detail:** the effects are stronger in firms with larger pre-audit gender imbalance and "higher AI intensity", and are concentrated in lower to mid-tier positions. Seminar listings (WebSearch snippets: RUC, SJTU, SSE 2026) add a performance outcome (analyst forecast accuracy); snippet level only. Jansen 2026 (SSRN 10.2139/ssrn.6465063) is re-read from Crossref: null effects; undergraduate honours thesis. |
| Bommasani, Bana, Creel, Jurafsky, Liang, "Algorithmic Monocultures in Hiring" (FAccT '26), **new** | https://arxiv.org/pdf/2605.27371 (sha256 `3605725f…0be81059fbe`); DOI 10.1145/3805689.3812400 | full-text | **New closest work on the pooling lever.**<br>Data: 4,197,168 applications by 3,372,132 applicants to 1,746 positions at 156 employers, all screened by one vendor (pymetrics) (p. 2).<br>Aggregate impact ratios are all above 0.8. Analysed per position (z-test, Benjamini-Hochberg, positions with >= 30 applicants who self-report race; Table 2 caption, PDF p. 6), 10.62% of positions adversely impact Black applicants (PDF pp. 2 and 7) and 5.32% Asian applicants (PDF p. 7). 62.35% of applicants do not self-report one of the four races studied (PDF p. 7).<br>Recommendation 1 (PDF p. 13) says that DCWP's LL 144 example of vendor data pooled across employers "blurs distinctions between positions and even employers".<br>Its "simulation" is about outcome homogenisation across models, not about LL 144 rule levers. It uses neither the published audit corpus nor the 2% exclusion. |
| Black, Gillis, Hall, "D-hacking" (FAccT '24), **new, from Gerchick's references** | https://facctconference.org/static/papers24/facct24-43.pdf (sha256 `6ad5db13…653918f4`) | full-text | Defines d-hacking as selecting models on favourable in-sample fairness metrics. It reviews robustness requirements in disparate-impact law (magnitude, "robustness in statistical significance", PDF p. 8). LL 144 is cited only as an example of municipal law (ref. [5]). No published-audit analysis and no simulation of LL 144 rules. It is a conceptual neighbour of the idea's "manipulation range" (Part 3). |
| Aamodt, Cohen, Dunleavy, *Technical Advisory Committee Report on Best Practices in Adverse Impact Analyses* (Center for Corporate Equality, Sept 2010), **new, from Courey and Oswald's references** | https://adverse-impact.com/wp-content/uploads/2015/02/TAC-Report-on-Adverse-Impact-Analyses-1.pdf (sha256 `209482b1…58665018`) | full-text (keyword-guided reading) | **New I-O practice record.** The data-aggregation section (pp. 47-50) gives Mantel-Haenszel and Breslow-Day guidance. On confidence intervals around the impact ratio (p. 46; PDF p. 57), "Ninety-one percent of the 35 survey respondents said that confidence intervals were somewhat or very useful", with focus-group disagreement about explaining them. On the 2% rule, the report states that "UGESP ... says that any group that does not make up at least 2% of the applicant pool should be excluded from the analysis" (pp. 74-75; PDF p. 86), citing UGESP Q&A 11/16.<br>The 2023 CFR text of 29 CFR 1607.4 was also read in this run (`$SCRATCH/data/idea04/ugesp/CFR-2023-title29-vol4-sec1607-4.xml`). It contains no 2% wording, so the threshold comes from the UGESP Q&A, not from section 1607.4. No simulation. |
| Noon Research (D. Witten), "NYC AI Hiring Bias Audits: What 116 Public Reports Show", published 2026-10-16, **new** | https://www.noon.ai/blog/articles/402-nyc-ai-hiring-bias-audit-results (HTML sha256 `4ac9516f…9bfd2e2e`) | full-text (whole page) | **New:** a vendor blog that re-analyses the ACLU `audits_full.csv` with **point estimates only**:<br>- 59 of 116 audits (50.9%) have at least one ratio below 0.80;<br>- the 3,025 numeric ratios have a median of 0.96, and 7.7% are below 0.80;<br>- a link-liveness check on 83 URLs;<br>- 10 Warden AI "assurance dashboards" from 2026 with stated sample sizes of 6,268 to 345,739.<br>Grep counts are 0 for "confidence", "interval", "significan", "sampling" and "uncertain". It is not peer reviewed, and it is marketing content. |
| Courey and Oswald 2025, J. Business and Psychology (OA), **new, from Semantic Scholar forward chasing** | https://link.springer.com/article/10.1007/s10869-025-10044-5 | abstract (the landing page holds the abstract and references, 2,821 words) | Interviews with 31 personnel-selection and legal experts on how adverse-impact measures are chosen and communicated. No LL 144 mention on the page. It led to the TAC 2010 report. |
| Jacobs, Murphy, Silva 2013, J. Business and Psychology, **new** | https://link.springer.com/article/10.1007/s10869-012-9268-3 | abstract | **New I-O Monte Carlo:** with significance tests, "the size of an organization or an applicant pool has more impact on determining adverse impact than the extent to which procedures actually discriminate". A direct antecedent for comparing reporting designs across vendor-level (large) and employer-level (small) audits. |
| Dunleavy, Morris, Howard 2015, "Measuring Adverse Impact in Employee Selection Decisions" (Springer chapter), **new** | https://link.springer.com/chapter/10.1007/978-3-319-11143-8_1 | abstract | A review of significance testing and practical-significance measures, ending with "a framework for conducting adverse impact analyses". It shows the reporting-design space is mapped in I-O. |
| Sariola, Button, Culotta, Mattei, "The Illusion of Fairness: Auditing Fairness Interventions in Algorithmic Hiring with Audit Studies" (AAAI 2026), **new** | https://ojs.aaai.org/index.php/AAAI/article/view/41267 | abstract | Uses audit-study data on age discrimination to evaluate resampling interventions. No LL 144 and no impact-ratio uncertainty. Not a competitor. |

Items the plan named that could not be read beyond what is stated:
- Roth et al. 2006, Collins and Morris 2008, Biddle and Morris 2011: APA, publisher refuses.
- Switzer et al. 2016: Taylor & Francis.
- Morris and Lobsenz 2000: Wiley.
- Aobdia et al.: SSRN.
- Two IIT theses (Kwon 2014; May 2012): repository.iit.edu reset the connection to curl and failed DNS in WebFetch.
- Two WebSearch queries for author copies of the I-O papers found none (section 3).

---

## 2. Citation-chasing log

**Tools.**
- Script `code/novelty_chase.py`; per-leg log in `results/novelty_chase_log.csv`.
- 132 title keyword hits in `results/novelty_chase_keyword_hits.csv`.
- Raw API responses are in `$ND/api_run1/` and `$ND/api_run2/` (not in the repository).
- Pacing: at least 3.2 s between calls to a service, a 30-60 s back-off on HTTP 429, at most 3 attempts per leg.

**Run history.**
- Run 1 (06:04:49-06:15:09 UTC) crashed on a Semantic Scholar reply with `data: null`.
- Run 2 (06:15:59-06:23:50 UTC, 470 s) used the patched script. It reused the raw replies that run 1 had received successfully.

**OpenAlex: daily budget exhausted.** OpenAlex answered every list query (the `cites:` filter and the `openalex:` filter) with HTTP 429 and this body: "Insufficient budget. This request has no API key, so it counts against the free daily budget shared by everyone on your network's IP address, and that budget is used up ($0 remaining; resets at midnight UTC)."
- Three single-work seed look-ups succeeded first (Gerchick, Wright, Morris and Lobsenz).
- After the budget message, later OpenAlex legs were not retried. This is allowed under the "at most 3 attempts" rule.

| Seed paper | Direction | Tool | Status | New relevant works found |
|---|---|---|---|---|
| Gerchick et al. 2025 | forward | OpenAlex | **not done**. Run 1: 3 attempts, 429. Run 2: 1 attempt, 429 with the daily-budget message | none |
| Gerchick et al. 2025 | forward | Semantic Scholar | done (16 citing works) | Escher, Banovic, Green (FAccT '26, audit-policy assumptions; low); Sharma and Molamohammadi 2026 (arXiv 2604.22679, supply-chain attribution; low-moderate); Verma et al. 2026 and Galdón-Clavell 2026 (already known); Black, Bogen, Koepke et al. "Fair Lending Model" (FAccT '26; interviews; low). **No citing work simulates LL 144 rules or attaches sampling intervals.** |
| Gerchick et al. 2025 | forward | WebSearch | done (1 query) | nothing beyond the above |
| Gerchick et al. 2025 | backward | full-text reference list | done (manual reading of refs 18, 24, 39, 42, 59, 61, 79, 81, 87, 88, 91, 101, 120, 123) | **Black, Gillis, Hall, "D-hacking" (FAccT '24)**; Morris and Dunleavy (eds.) 2016 book; Raghavan and Kim 2024 (year correction) |
| Wright et al. 2024 | forward | OpenAlex | **not done**. Run 1: 3 attempts, 429. Run 2: daily budget exhausted | none |
| Wright et al. 2024 | forward | Semantic Scholar | done (50 citing works) | **Bommasani et al. (FAccT '26)**; Lafargue et al. "Exposing the Illusion of Fairness" (arXiv 2507.20708, ECML-PKDD 2026 ADS per arXiv journal_ref); Lacmanovic and Skare 2025 (Review of Accounting and Finance, qualitative LL 144 comparison; low); Burgess and Cates 2026 (doctrinal; low). No interval or simulation study of LL 144 ratios. |
| Morris and Lobsenz 2000 | forward | OpenAlex | **not done**. Run 1: 3 attempts, 429. Run 2: budget exhausted | none |
| Morris and Lobsenz 2000 | forward | Semantic Scholar | done, but **0 citing works returned**, whereas Crossref `is-referenced-by-count` = 38. This is a coverage gap. | none |
| Morris and Lobsenz 2000 | forward | WebSearch | done (1 query; the author-copy query surfaced the same thesis) | **May 2012 IIT thesis** (small-sample-adjusted CI for the adverse-impact ratio; Monte Carlo); Biddle and Morris 2011 (mid-P Fisher) |
| Morris and Lobsenz 2000 | backward | Crossref | done (39 references) | antecedents only (Greenberg 1979; Boardman 1979; Wing 1982; York 1995) |
| Morris and Lobsenz 2000 | backward | OpenAlex / Semantic Scholar | **not done** (OpenAlex budget; Semantic Scholar returned `data: null`, list withheld) | none |
| Roth, Bobko, Switzer 2006 | forward | Semantic Scholar | done (58 citing works) | **Jacobs, Murphy, Silva 2013** ("Being big is worse than being bad", Monte Carlo); Courey and Oswald 2025; Alexander, Song, Hickman, Shin 2024 (IJSA, sourcing-algorithm Monte Carlo; adverse-impact ratio misses sourcing effects); "On the Consequences of Frequent Applicants in Adverse Impact Analyses" (IJSA 2008, title only); Miao and Gastwirth 2013 (LPR, title only). **None concerns LL 144.** |
| Roth, Bobko, Switzer 2006 | forward / backward | OpenAlex | **not done** (budget exhausted) | none |
| Roth, Bobko, Switzer 2006 | backward | Crossref | done (50 references) | Morris 2001, "Sample size required for adverse impact analysis"; Sackett and Roth 1996 (multistage Monte Carlo); Wing 1982 |
| Roth, Bobko, Switzer 2006 | backward | Semantic Scholar | done, `data: null` (withheld) | none |
| Collins and Morris 2008 | forward | Semantic Scholar | done (44 citing works) | Aigner, del Ángel, Wiles 2023 (Statistics and Public Policy; fair housing; title only); "Statistical Significance Standards for Basic Adverse Impact Analysis" (2010) and "A Consideration of Practical Significance in Adverse Impact Analysis" (2010) (titles only); Switzer et al. 2016. None on LL 144. |
| Collins and Morris 2008 | backward | Crossref / Semantic Scholar / OpenAlex | **not done**: Crossref has no deposited reference list, Semantic Scholar `data: null`, OpenAlex budget exhausted | none |
| Switzer, Roth, Rosopa 2016 | forward | Semantic Scholar | done, 0 citing works (Crossref count = 2) | none |
| Switzer, Roth, Rosopa 2016 | backward | Crossref | done (28 references) | small-sample/power literature only |
| Switzer, Roth, Rosopa 2016 | backward | Semantic Scholar | **not done** (429 on all 3 attempts) | none |
| Lam et al. 2024 | forward | Semantic Scholar | **not done** (429 on all 3 attempts) | none |
| Lam et al. 2024 | forward | OpenAlex | **not done** (budget exhausted) | none |
| Lam et al. 2024 | forward | WebSearch | done (1 query) | no application of Q.G/Q.H to published reports found. BABL AI's own page says the paper underlies its audit methodology (snippet). |
| Ferrara et al. 2025 | backward | full text and Semantic Scholar | done (46 references in the PDF; Semantic Scholar 49) | **Besse, del Barrio, Gordaliza, Loubes 2018, "Confidence Intervals for Testing Disparate Impact in Fair Learning"** (arXiv 1807.06362); Himmelreich et al. 2025 (PMLR 279); Barrainkua et al. AISTATS 2024 |
| Ferrara et al. 2025 | backward | Crossref | done, no reference list deposited | none |
| Ferrara et al. 2025 | forward | Semantic Scholar | done (2 citing works) | none relevant (hate-speech audit budget; text-to-image survey) |
| Black, Gillis, Hall 2024 (D-hacking) | forward | Semantic Scholar | done (16 citing works) | none on LL 144 rule levers |

**Hand correction to the log.**
- Four "seed unresolved" OpenAlex backward rows had a hard-coded attempt count of 3. They were corrected by hand to 0, because the legs were skipped after the budget message.
- The code was fixed afterwards (see section 8).
- "attempts = 0" on a "done" row means the raw reply was reused from run 1, where the leg took one attempt.

---

## 3. Sweeps named as not done in the earlier check, and other searches

**FAccT 2026 table of contents.**
- Source: the official accepted-papers CSV behind https://facctconference.org/2026/acceptedpapers.html, namely `facct2026-final.csv`: 325 papers with titles and abstracts; sha256 `96f70eda…87ae`; page "Updated Fri, 16 Oct 2026".
- Screened with `code/toc_scan.py` (keyword families: LL 144/NYC/bias audit; hiring; four-fifths/impact ratio; uncertainty; audit rules). A wider title list was also read by hand.
- **No accepted paper mentions Local Law 144 in its title or abstract.**
- Relevant papers:
  - Bommasani et al., "Algorithmic Monocultures in Hiring" (read in full; section 1);
  - Monnier et al., "Beyond Base Metric: ... Meta-Metrics in Intersectional Fairness" (aggregation choices for intersectional summaries; abstract);
  - He et al., MPC for post-market fairness monitoring in hiring (abstract; low);
  - Escher, Banovic, Green, "Algorithm Auditing Policies Rest on Flawed Assumptions..." (abstract; public-sector, low).
- CRAFT sessions and tutorials were not screened.

**AIES 2026 table of contents.**
- Source: AAAI OJS issues 743-746 (AIES-26 Main Tracks I-IV and Student Abstracts). 265 article pages, all with abstracts, fetched by `code/fetch_ojs_abstracts.py` (06:08-06:21 UTC; 0 pages missing; JSON sha256 `464c8902…c9f340`).
- **No abstract mentions Local Law 144, NYC or "LL144"** (0 of 265).
- Relevant papers (abstracts read):
  - Wilson et al., "Applications of Risk Science to AI Fairness Evaluation". A review of 22 fairness metrics used in hiring and employment evaluations: most "do not follow best practices to characterize the uncertainty". This supports the motivation and does not compete.
  - Godinot et al., "Manipulation-Proof Oblivious Audits" (an audit protocol against manipulation; low).
  - Cerrato et al., "An Agent-Based Simulation of Fairness Interventions in Hiring" (dynamic training feedback, not reporting rules; low).

**FAccT 2025 (added, not in the plan).** `facct2025-final.csv` holds 217 rows (sha256 `d539f74d…9e9f9b`). Only Gerchick et al. matches LL 144. Matches for all three venues are in `results/novelty_toc_scan_matches.csv`.

**Forward citations of Gerchick and Wright:** done through Semantic Scholar (16 and 50 works; section 2). OpenAlex was not available.

**ACLU repository code.**
- Another agent read the code (`research/06_stage4/idea04/README.md`, section 3). It reports deterministic missing-data bounds in `helpers.R` lines 110-123 and no interval, simulation or significance test (stopping-rule criterion C1 not triggered).
- Statements in the paper agree (section 1, row 1).
- The repository's `README.md` and `data_schema.md` (commit `cef7c273…`, read in this run) contain no statement about intervals, bounds or significance.

**Search log** (queries issued in this run):

| Channel | Queries | Notes |
|---|---|---|
| WebSearch | 26 (3 extended-mode) | I-O full texts and author copies (6); D-hacking (2); FAccT/AIES 2026 TOCs (2); LL 144 simulation/2%/pooling/reanalysis/I-O-journal coverage (5); I-O aggregation and intersectional (3); forward chasing of Morris-Lobsenz, Roth, Gerchick, Lam (4); EAAMO/CSLaw/workshops (2); Aobdia (1); multiverse/discretion (1) |
| arXiv API search | 8 | `all:"Local Law 144"` (7 hits, no new LL 144 statistics paper since 2026-10-05 except 2604.22679); `"bias audit" AND hiring` (11); `"four-fifths rule"` (3); `"impact ratio" AND audit` (6); `abs:"disparate impact" AND abs:"confidence interval"` (2); `"adverse impact" AND selection` (60, off-topic); `"automated employment decision"` (5); `ti:"D-hacking"` (0) |
| Crossref bibliographic | 9 (1 returned non-JSON) | I-O aggregation (Howard, Morris, Dunleavy 2017 found); LL 144 since 2024-06 (no new statistical paper; KC 2026 SSRN; Srivastava and Singh 2026 chapter) |
| Direct look-ups (not counted as queries) | 18 Crossref DOI records; 4 arXiv `id_list` calls; 2 manual Semantic Scholar calls (1 returned 200, 1 returned 429); 2 OpenAlex diagnostic calls (both 429); PDFs, HTML and other pages as listed in sections 1 and 8 | |

---

## 4. New prior-art comparison table

This table lists only works that are new relative to the 2026-10-05 check, or whose reading changed. The earlier table (`03_challenge/04-…__novelty.md`, section 2) still applies otherwise.

| Work | Year | Venue / status | Link | What it does | Overlap with the idea | What the idea still adds |
|---|---|---|---|---|---|---|
| Bommasani, Bana, Creel, Jurafsky, Liang, "Algorithmic Monocultures in Hiring" | 2026 | FAccT '26 (peer-reviewed), DOI 10.1145/3805689.3812400 | https://arxiv.org/abs/2605.27371 | Analyses 4.2 M applications to 1,746 positions at 156 employers from one vendor. Pooled impact ratios all exceed 0.8, but per-position z-tests with BH correction (>= 30 self-reported applicants) find adverse impact for Black applicants (10.62% of positions) and Asian applicants (5.32%). It criticises DCWP's cross-employer pooling example for LL 144. | **High on the pooling lever**: shows on real data that vendor-level pooling under LL 144 guidance masks position-level adverse impact. FAccT venue. Uses significance testing with a minimum-n rule. | It does not use the published LL 144 corpus. It does not simulate pooling, the 2% exclusion, the unknown exclusion or the median split as rule levers. It gives no false-pass/false-fail rates as functions of pool heterogeneity, and no intervals for published ratios. The idea's pooling arm must be framed as quantifying this mechanism, calibrated to the published corpus, not as discovering it. |
| Aamodt, Cohen, Dunleavy, TAC Report on Best Practices in Adverse Impact Analyses | 2010 | Center for Corporate Equality report (practitioner consensus of 70 experts; not peer-reviewed) | https://adverse-impact.com/wp-content/uploads/2015/02/TAC-Report-on-Adverse-Impact-Analyses-1.pdf | Best-practice survey. Aggregation via Mantel-Haenszel and Breslow-Day (pp. 47-50); CIs around the impact ratio rated useful by 91% of 35 respondents (p. 46); UGESP's 2% subgroup exclusion (pp. 74-75). | **Reporting designs and the 2% rule's provenance** are established I-O practice: intervals and multiple-event aggregation tests are not new proposals. | An evaluation of these designs on LL 144's published counts, and of what the 2% exclusion removes in applicants. |
| Kwon (adviser S. B. Morris), "Appropriateness of Aggregation in Adverse Impact Analysis: A Monte Carlo Simulation" | 2014 | IIT master's thesis (not peer-reviewed; full text restricted) | https://repository.iit.edu/islandora/object/islandora%3A7013 (not reachable from this container) | Per WebSearch snippets: a Monte Carlo of Breslow-Day and modified Breslow-Day homogeneity tests used to decide whether to aggregate samples. Both have weak power except with large per-sample n and many samples. | **The I-O simulation lineage for the pooling lever** (generic, pre-LL 144). | LL 144-specific pooling (unknown employer shares, vendor reports reused across employers), combined with the exclusions and calibrated to the published corpus. |
| Howard, Morris, Dunleavy, "Generalizability Versus Situational Specificity in Adverse Impact Analysis: Issues in Data Aggregation" | 2017 | Industrial and Organizational Psychology (commentary; peer-reviewed), DOI 10.1017/iop.2017.48 | https://api.crossref.org/works/10.1017/iop.2017.48 | Metadata only. Aggregation of adverse-impact data across units. | Pooling is a recognised I-O issue. | As above. |
| Jacobs, Murphy, Silva, "Unintended Consequences of EEO Enforcement Policies: Being Big is Worse than Being Bad" | 2013 (online 2012) | J. Business and Psychology, DOI 10.1007/s10869-012-9268-3 | https://link.springer.com/article/10.1007/s10869-012-9268-3 | Monte Carlo: significance-based adverse-impact rules make organisation and pool size matter more than the degree of discrimination. | **Moderate on Part 3**: any proposal to add significance tests to LL 144 reports inherits this size asymmetry (vendor-pooled audits will "fail" more easily than small employer audits). | It quantifies the asymmetry on the actual LL 144 size distribution (the pilot's bimodal employer/vendor corpus). |
| May, "Using Confidence Intervals with a Small Sample Size Adjustment to Assess Adverse Impact" | 2012 | IIT master's thesis (snippet only) | https://repository.iit.edu/islandora/object/islandora%3A8992 (not reachable) | Per snippets: a Monte Carlo showing that a 0.5 adjustment improves the Morris and Lobsenz CI over the unadjusted interval and Agresti-Caffo. | The interval method for Part 1 already has an I-O small-sample evaluation. | Applying intervals to the published ratios; a method choice informed by this. |
| Besse, del Barrio, Gordaliza, Loubes, "Confidence Intervals for Testing Disparate Impact in Fair Learning" | 2018 | arXiv preprint (later surveyed in The American Statistician 2022 per Ferrara's references) | https://arxiv.org/abs/1807.06362 | Asymptotic distribution and CIs for disparate-impact indices; argues for CIs instead of point values. | The ML-side antecedent of attaching intervals to DI ratios (alongside Morris and Lobsenz). | A regulatory corpus; LL 144 rules. |
| Ferrara et al. (re-read) | 2025 | NeurIPS 2025 | https://arxiv.org/abs/2506.10586 | The size-adaptive test covers the **DI ratio** as well as parity differences (PDF p. 7). | Raises the overlap on posterior or credible-interval reporting for ratios. | Application to published LL 144 counts; rule levers. |
| Noon Research (D. Witten), "NYC AI Hiring Bias Audits: What 116 Public Reports Show" | 2026-10-16 | Vendor blog (not peer-reviewed) | https://www.noon.ai/blog/articles/402-nyc-ai-hiring-bias-audit-results | Point-estimate reanalysis of the ACLU file (50.9% of audits have at least one ratio < 0.80; median ratio 0.96). Link-liveness check. 2026 Warden AI dashboards with sample sizes from 6,268 to 345,739. | **Low to moderate:** a descriptive reanalysis of the same corpus is now public, so "first reanalysis of the ACLU data" cannot be claimed. It confirms that 2026 vendor-level dashboards have large N. | All inferential content: intervals, posteriors, tests, excluded shares, simulation. |
| Ogbanufe, "Towards Using AI Bias Audits As Inputs For Red Teaming and Performance" | 2026 | ECIS 2026 (AIS eLibrary) | https://aisel.aisnet.org/ecis2026/resp_AI/resp_AI/9/ | Abstract: an analysis of LL 144 reports reveals "demographic missingness, from under 3% to over 50%"; institutional and stewardship-theory framing. | **Partial on RQ1's unknown-share component** (descriptive range). Already listed in the feasibility file; now in the novelty record. | Shares in applicants per audit and the 2%-rule exclusions; uncertainty; simulation. |
| Black, Gillis, Hall, "D-hacking" | 2024 | FAccT '24, DOI 10.1145/3630106.3658928 | https://facctconference.org/static/papers24/facct24-43.pdf | Selecting models on favourable in-sample fairness metrics produces non-generalisable fairness. Argues for robustness requirements in regulation. | Conceptual neighbour of Part 3's manipulation range. | A measured range of permitted LL 144 choices on real reports. |
| Lafargue, Laurindo Monteiro, Claeys, Risser, Loubes, "Exposing the Illusion of Fairness: Auditing Vulnerabilities to Distributional Manipulation Attacks" | 2025 (v3 2026) | ECML-PKDD 2026 Applied Data Science track (per arXiv journal_ref) | https://arxiv.org/abs/2507.20708 | The minimal distributional shift that makes a sample DI-compliant while looking representative; tests to detect it. | Theoretical manipulation of the DI ratio through the audit sample (Part 3). | LL 144's permitted discretionary choices (exclusions, metric, pooling, comparator) on real reports. |
| Godinot et al., "Manipulation-Proof Oblivious Audits Against Deceptive Model Providers" | 2026 | AIES 2026 | https://ojs.aaai.org/index.php/AIES/article/view/43209 | An audit protocol that raises the cost of hiding unfairness. | Low (manipulation in black-box audits). | As above. |
| Wilson et al., "Applications of Risk Science to AI Fairness Evaluation" | 2026 | AIES 2026 | https://ojs.aaai.org/index.php/AIES/article/view/43345 | Review of 22 fairness metrics in hiring and employment evaluations; most do not characterise uncertainty; proposes an "AI Risk Report Card". | Supports the motivation. A reporting-design proposal in the same space. | Evidence from LL 144 published reports. |
| Courey and Oswald | 2025 | J. Business and Psychology (OA), DOI 10.1007/s10869-025-10044-5 | https://link.springer.com/article/10.1007/s10869-025-10044-5 | 31 expert interviews on choosing and communicating adverse-impact measures. | Low (qualitative; no LL 144). | — |
| Dunleavy, Morris, Howard, "Measuring Adverse Impact in Employee Selection Decisions" | 2015 | Springer book chapter, DOI 10.1007/978-3-319-11143-8_1 | https://link.springer.com/chapter/10.1007/978-3-319-11143-8_1 | Review of significance and practical-significance analyses and a framework for adverse-impact analysis. | The reporting-design space is mapped in I-O. | — |
| Ramineni, Rahmani, Yilmaz, Barber, "Beyond Internal Data: Bounding and Estimating Fairness from Incomplete Data" | 2025 | arXiv preprint | https://arxiv.org/abs/2508.13040 | Bounds on fairness metrics when protected attributes sit in separate data sources. | Methodological cousin of Gerchick's missing-data bounds. | — |
| Sharma, Molamohammadi, "How Supply Chain Dependencies Complicate Bias Measurement and Accountability Attribution in AI Hiring Applications" | 2026 | arXiv preprint | https://arxiv.org/abs/2604.22679 | Literature and regulatory analysis of the vendor/deployer split, including LL 144. | Low to moderate (attribution side of pooling). | Quantification. |

---

## 5. Updated verdict: partially-covered (unchanged label, narrower claim)

Component by component. The idea's four claimable components come from the 2026-10-05 check, section 3.

1. **Sampling intervals, posteriors and the UGESP test on the published LL 144 ratios (Part 1). Still no record.** None of the following does this:
   - the Gerchick full text (deterministic missing-data bounds only, section 1);
   - the ACLU code (another agent's reading);
   - the new Noon Research reanalysis (point estimates only);
   - 325 FAccT 2026 and 265 AIES 2026 papers, or 16 + 50 Semantic Scholar citers of Gerchick and Wright;
   - the eight arXiv searches.

   The statistics are mature: Morris and Lobsenz 2000, May 2012, Besse et al. 2018, and Ferrara et al. 2025 (which covers the DI ratio). Practitioners have endorsed CIs since at least the 2010 TAC report. The contribution is an application. It is not a method.
2. **Excluded populations in applicants. Partly covered.** Gerchick et al. report how often data are missing (83% of audits). Ogbanufe (ECIS 2026) reports a missingness range from under 3% to over 50%. Nothing was found that reports the applicant shares removed by the **2% rule**, per audit, across the corpus. The TAC report and UGESP Q&A place that rule's origin in 1979 I-O practice.
3. **Rule-specific simulation (Part 2). Partly covered, more than before.**
   - **Pooling.** The qualitative result is now shown on real applicant data in a FAccT paper (Bommasani et al. 2026). It also has an I-O simulation lineage (Kwon 2014; the TAC report's aggregation guidance; Howard et al. 2017). The UGESP text quoted by Watkins et al. itself contemplates pooling small samples across time and sites.
   - **Small-N false positives:** Roth et al. 2006.
   - **Size effects of significance rules:** Jacobs et al. 2013.
   - **Median split:** Filippi et al. 2023.
   - **Intersectional small groups:** Ferrara et al. 2025, plus Bommasani's BH-corrected per-position tests.
   - **Not found:** a simulation that combines LL 144's levers, calibrated to the published corpus, and reports false-pass and false-fail rates. The levers are the 2% exclusion, the unknown exclusion, the median-split scoring rate, intersectional splitting and cross-employer pooling. The 2% exclusion has no simulation record at all in what was searched.
4. **Manipulation range on real reports (Part 3). Not found.** The theoretical neighbours have grown: D-hacking (FAccT 2024), Verma et al. 2026, Lafargue et al. (ECML-PKDD 2026) and Godinot et al. (AIES 2026). The reporting designs that Part 3 would compare are already specified:
   - Lam et al. Q.G.2 and Q.H.1;
   - the TAC 2010 CIs and practical-significance guidance;
   - Collins and Morris 2008, which advises *against* the Fisher test that Q.H.1 prescribes below n = 30.

   Part 3 is therefore an evaluation of existing designs on the real size distribution, including the Jacobs et al. size asymmetry. It cannot claim to propose those designs.

**Why not "largely-covered":** no work found does components 1, 2 (for the 2% rule), the combined calibrated simulation in 3, or 4 on the LL 144 corpus.

**Why not "likely-novel":**
- The pooling headline is now in a FAccT 2026 paper with stronger data than a simulation.
- Every statistical tool and reporting design is decades old in I-O.
- A public descriptive reanalysis of the same ACLU corpus appeared on 2026-10-16.

**Required positioning changes** (adding to those in the 2026-10-05 file):
- Cite Bommasani et al. as the empirical demonstration that pooling masks position-level adverse impact. Present the pooling arm as quantifying, on the published corpus, how much pooled LL 144 ratios can hide.
- Cite the TAC 2010 report and Jacobs et al. 2013 in the reporting-design comparison. Test Fisher against the Z-test and mid-P at LL 144 sizes, because Lam's Q.H.1 and Collins and Morris disagree.
- Cite Ferrara et al. for the ratio posterior. Cite May 2012 or Morris and Lobsenz for interval choice.
- Do not describe the corpus reanalysis as the first. Noon Research published point estimates; Gerchick et al. published missing-data bounds.

---

## 6. Literature stop condition

**Rule (section 4.3, unchanged):** "stop the whole idea if an I-O or FAccT paper is found that simulates the LL 144 exclusion and pooling levers on the published corpus."

**Decision: not-triggered.** Each closest candidate fails at least one part of the condition:

| Candidate | I-O or FAccT? | Simulates LL 144 exclusion **and** pooling levers? | On the published LL 144 corpus? |
|---|---|---|---|
| Bommasani et al. 2026 | FAccT, yes | Pooling only, analysed empirically (per position versus aggregate) on proprietary pymetrics data. It does not simulate rule levers. Its only exclusion is a 30-applicant floor for its own tests, not the 2% or unknown exclusion. | **No** |
| Gerchick et al. 2025 | FAccT, yes | No simulation. Deterministic missing-data bounds only (p. 35, A.4). Pooling and the 2% rule are discussed qualitatively. | Yes |
| Kwon 2014 thesis | I-O, yes | A simulation of aggregation (homogeneity) tests. No LL 144 exclusions. | No (pre-dates LL 144) |
| Roth, Bobko, Switzer 2006; Collins and Morris 2008; Jacobs et al. 2013; Switzer et al. 2016 | I-O, yes | Generic small-N or size simulations. Per the abstracts, the outline and the reference lists, they vary neither a 2%-type exclusion nor pooling. Switzer's full text is unread. | No (pre-date LL 144) |
| Noon Research 2026; Ogbanufe 2026 | Neither (vendor blog; ECIS) | No simulation | Yes / partially |

Every I-O paper published before July 2023 cannot meet the "published corpus" part of the condition, because LL 144 audits only exist from then. This holds even for the I-O full texts that could not be read.

**Residual risk** comes from LL 144-era work that the searches could not reach:
- the forward citers of Morris and Lobsenz (Semantic Scholar returned 0 against Crossref's 38);
- OpenAlex forward lists for every seed;
- Semantic Scholar forward citers of Lam et al.;
- SIOP 2025-2026 programmes and I-O journal tables of contents, which were not enumerated.

---

## 7. Search limits

- **OpenAlex:** list queries were refused all session (daily IP budget exhausted; quoted in section 2). No OpenAlex forward list and no OpenAlex reference resolution was obtained for any seed. Seed records for Gerchick, Wright and Morris and Lobsenz were retrieved; all other seeds were not.
- **Semantic Scholar:**
  - Lam et al. forward and Switzer et al. backward got 429 on all 3 attempts each (not done).
  - Reference lists were withheld (`data: null`) for Morris and Lobsenz, Roth et al. and Collins and Morris.
  - Morris and Lobsenz forward returned 0 citers, Switzer forward 0 (Crossref counts: 38 and 2).
  - Two manual Semantic Scholar calls made in this run (abstract look-ups) may have added to the 429s.
  - No API key was available, so the plan's "Semantic Scholar (with key)" could not be followed.
- **Crossref:** no reference list is deposited for Collins and Morris 2008 or for Ferrara et al.'s NeurIPS record. Abstracts are absent for Roth 2006, Collins and Morris 2008 and Switzer 2016. One bibliographic query returned non-JSON and was not repeated.
- **Publisher and host refusals:**
  - Not fetched, per the environment facts: APA, Wiley, Taylor & Francis, SSRN, ACM DL.
  - repository.iit.edu: connection reset to curl, DNS failure in WebFetch. The Kwon 2014 and May 2012 theses are known only from WebSearch snippets.
  - oit-portal-test2.newhaven.edu: refused by the egress proxy.
  - WebFetch failed DNS for pure.ul.ie, ojs.aaai.org, noon.ai and aisel.aisnet.org. All except pure.ul.ie were then fetched with curl. The University of Limerick item ("When and why do different indices lead to different conclusions a…") remains unidentified; Crossref found no match.
- **Proceedings sweeps:**
  - FAccT 2026: main-track accepted papers only (325). CRAFTs and tutorials were not screened.
  - AIES 2026: all four OJS issues (265 papers).
  - FAccT 2025 was added (217 rows).
  - The screens were keyword-based on titles and abstracts, with manual reading of flagged items and of wider title lists. A paper that discusses LL 144 only in its body would be missed. Full texts of these 807 papers were not grepped.
- **Not searched:** Google Scholar, Scopus, Web of Science, dblp. Also not searched: SIOP 2025/2026 programmes, and the 2023-2026 tables of contents of Personnel Psychology, J. Applied Psychology, IJSA, J. Business and Psychology and Human Performance (covered only through Semantic Scholar forward legs and Crossref queries). Law reviews were reached only through WebSearch snippets. Only English-language sources were used.
- **Partial readings:**
  - The Roth et al. 2006 study design is known from a third-party course outline, not from the paper.
  - The TAC report was read through keyword-guided passages, not cover to cover.
  - Gerchick et al. was re-read in the named sections plus a grep. Other sections were read on 2026-10-05.

---

## 8. Reproducibility

**Software.**
- Python 3.11.15 (venv `$SCRATCH/venv`), requests 2.34.2.
- pdftotext 24.02.0 (poppler).
- curl 8.5.0.
- System Python 3.11.15, used only for inline HTML/JSON parsing of downloaded files, with `-I`.

**Seeds.** `random.seed(20261019)` in `novelty_chase.py`. It sets only the 30-60 s back-off jitter. No stochastic analysis was run.

**Scripts** (all in `research/06_stage4/idea04/code/`):

| Script | Run as | Writes |
|---|---|---|
| `novelty_chase.py` | `venv/bin/python -I novelty_chase.py --raw-dir $ND/api_run2 --reuse-dir $ND/api_run1 --log ../results/novelty_chase_log.csv --hits ../results/novelty_chase_keyword_hits.csv` | `results/novelty_chase_log.csv`, `results/novelty_chase_keyword_hits.csv` |
| `toc_scan.py` | `venv/bin/python -I toc_scan.py --in <csv/json> ... --out <csv>` | per-venue scans, merged into `results/novelty_toc_scan_matches.csv` (25 matches) |
| `fetch_ojs_abstracts.py` | `venv/bin/python -I fetch_ojs_abstracts.py --in $ND/aies2026/aies2026_titles.json --out $ND/aies2026/aies2026_with_abstracts.json` | `$ND/aies2026/aies2026_with_abstracts.json` |

**Wall-clock (UTC, 2026-10-19).**

| Step | Start | End | Duration |
|---|---|---|---|
| First download (Gerchick PDF) | 06:02:05 | | |
| Chasing run 1 (crashed) | 06:04:49 | 06:15:09 | |
| Chasing run 2 | 06:15:59 | 06:23:50 | 470 s |
| AIES abstract fetch | 06:08:27 | 06:21:09 | |
| Whole check, before writing this file | | | about 25 minutes |

**Checksums (sha256, full values) of downloaded inputs** (all under `$ND/`):

| File | sha256 |
|---|---|
| gerchick/gerchick2025.pdf | `586a788f2df068d566f801f39ffe04bc635df26a0bd079d37c754878a56af19c` |
| lam/lam2401.14908.pdf | `249261a2881be7b6a2b789a9da0678c7e0bf0e001185ea35bdec5c9bf630a1d6` |
| watkins/watkins2202.09519.pdf | `3c4f6198d958873c4189f56d89917e5f7f255936ef2d88bed86dfac7467e2869` |
| ferrara/ferrara2506.10586.pdf | `3c09d800b088c6160bfdaf9b574261b3491a57b9e1e5552228dc1c69684047d7` |
| hilliard/hilliard2024.pdf | `c0b674a8adf7f22d6f86f2e873f7dca88e5720e9beb2006eea471d19f00627e7` |
| dhacking/facct24-43.pdf | `6ad5db13360325fb157bc986a1913fc1c7f81ad965ce0c1bff08a0fe653918f4` |
| bommasani/2605.27371.pdf | `3605725fb9401649d8f39fb3a4401629196de43eb0002d5d17d5d0be81059fbe` |
| tac2010/tac.pdf | `209482b1abb6d36cd30687182b4a7c47c7e6d366fd61e54416ae4c6058665018` |
| pdx_roth/roth2006_outline.doc | `ad280c7dad62ac76a7296553e6bdc032cab7e13e27d4f528afa29e6d489ae217` |
| facct2026/facct2026-final.csv | `96f70eda7e65686f3382dcac2f42548f70d5aa1a588b35b5f784abbabe9d87ae` |
| facct2025/facct2025-final.csv | `d539f74d468ccdcc4c48640fe96a423c9fecf7686cc31b8068897e41750e9f9b` |
| aies2026/aies2026_with_abstracts.json | `464c89021dfebdb5a6b665bfe2e6921c8fa5fa3d4879a0027c2d6cf777f9c340` |
| noon/402.html | `4ac9516ff4134e3429fbc03378a946a2f2546e273d55975901cc31db9bfd2e2e` |
| courey/page.html | `d280d6ca2da662e5e04e3d533edffa64f5ca882709acbfeecc3092cd855243c3` |
| sufe/372321.html (Roth abstract) | `bb890309bfb497b9cb1d9580861554ac540454dfb47486823cfb7679bc54f505` |
| sufe/371782.html (Collins and Morris abstract) | `4a937bef33e61e7de127dffd32fa8fdc42d3fff204ee9359e23bcf2d9b2ec61f` |
| sufe/371270.html (Biddle and Morris abstract) | `9fbf4b201a2420848256a3f5fe70cdf004d10775bd173783ba42acc5dc44889f` |

**Deviations from the written plan and from the brief.**

1. **OpenAlex legs.** After the daily-budget 429 message, the remaining OpenAlex legs were skipped with 0 attempts instead of 3. The brief says "at most 3", so this stays within it.
   - Run 1 used 3 attempts on four OpenAlex legs: Gerchick forward, Wright forward, Morris and Lobsenz forward, and Morris and Lobsenz backward through the list endpoint. The last is inferred from timestamps, because run 1's log was never written.
   - The backward OpenAlex code was then changed to single-work look-ups, which were also refused.
2. **Run 1 crashed** with a `TypeError` on a Semantic Scholar `data: null` reply. The script was patched (null handling, budget detection, `--reuse-dir`) and run again as run 2, reusing run 1's successful raw replies. No leg that had used 3 attempts was retried.
3. **Logging bug.** The log CSV contained a hard-coded attempt count of 3 for "seed unresolved" rows. Four rows were corrected by hand to 0 (they are marked in the CSV), and the code was fixed afterwards.
4. **Calls outside the script.** These were 2 Semantic Scholar paper look-ups (1 returned 200, 1 returned 429) and 2 OpenAlex diagnostic calls (both 429).
5. **FAccT 2025 added.** The FAccT 2025 table of contents was screened although the plan did not ask for it. Its first scan used the wrong column names (0 matches) and was rerun with `--title-col TITLE --abstract-col ABSTRACT`.
6. **"Author pages for the I-O papers"** was carried out as two WebSearch queries for author copies, plus the reachable mirrors (SUFE abstracts, the PDX outline). No author page holding a full text was found.
7. **Semantic Scholar without a key**, because none was available.
8. **No experiment was run.** This file is a literature check. Numbers about the LL 144 corpus that are quoted here come from the documents named, not from new analysis. The pilot's numbers are in `research/06_stage4/idea04/README.md` (another agent).
