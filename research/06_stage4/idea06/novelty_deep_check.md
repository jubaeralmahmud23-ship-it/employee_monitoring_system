# Idea 6, Stage 4 deep novelty check: "Would the Claim Survive an Error Bar?"

**Date:** 2026-10-19 (session 05:32-06:00 UTC). **Environment:** cloud container (4 vCPU, 15 GB RAM, no GPU), not the author's Windows PC used on 2026-10-05. **Plan followed:** `research/02_candidate_ideas.md` section 4.1, "Novelty tests". **Earlier check:** `research/03_challenge/06-would-the-claim-survive-an-error-bar-auditing-st__novelty.md` (2026-10-05).

**Scope.** This file covers only the novelty part of the Stage 4 plan: reading the named full texts, citation chasing, the sweeps the earlier check could not run, and the literature criterion of the stopping rule. The pilot criteria of the stopping rule (share of pilot papers that permit RQ2, size of the Springer-OA stratum, second coder and AIS access) are not assessed here.

**Outcome in brief.**
- Verdict: **partially-covered** (unchanged in category, but the uncovered space is smaller than on 2026-10-05; see Section 5).
- Literature stop condition: **not-triggered**. No published IS-venue audit of statistical or judge-validation practice in LLM papers was found (Section 6). One AMCIS 2025 paper could only be read at abstract level and should be checked in full before preregistration.
- The full texts correct three readings in the earlier check:
  - Yang et al.'s "fewer than 8%" uses all 3,334 NLG papers as the denominator. Among papers that use an LLM judge the figure is 37.4%, so H2 is not "close to settled" (Section 1).
  - Siddiq et al.'s "venue" research question analyses venue policies, not reporting by venue.
  - Bean et al.'s 16.0% counts "uncertainty estimates or statistical tests", not statistical testing alone.
- New prior art narrows two of the claimed increments:
  - A September 2026 audit of 259 agentic-security papers already codes variance, repeated runs, decoding and judge-human agreement together, and adds a power analysis (arXiv 2609.25173).
  - DKFZ's public "Claims Reloaded" estimator already turns reported test-set size and accuracies into a probability of false claims, which overlaps the planned calculator.

All derived files are in `research/06_stage4/idea06/results/novelty/`. The scripts are in `research/06_stage4/idea06/code/`: `chase_citations.py`, `aisel_crawl.py`, `crossref_is_sweep.py`, `screen_titles.py` and `arxiv_parse.py`. Raw downloads are in the scratchpad (`.../scratchpad/data/idea06_novelty/`) and are not committed.

---

## 1. Full texts read

Access depth:
- **full-text**: the arXiv PDF was downloaded, converted with `pdftotext -layout`, and read in the sections cited.
- **full-text (sections)**: the PDF was downloaded, and the abstract, introduction and the named sections were read.
- **abstract**: the abstract only.
- **metadata/snippet**: Crossref record and/or WebSearch snippet only.

Page numbers are PDF page indices of the arXiv versions whose sha256 values are listed in `results/novelty/fulltext_manifest.csv`.

| Title | Source URL | Access depth | What changed relative to the 2026-10-05 reading |
|---|---|---|---|
| Christodoulou et al., "False Promises in Medical Imaging AI? Assessing Validity of Outperformance Claims" (v2, 6 Aug 2025) | https://arxiv.org/abs/2505.04720 | full-text (main text, Methods, SI section A) | **Confirms, and makes it more specific.** The cohort is one venue: MICCAI 2023, 126 classification and 221 segmentation papers, 347 in total (p. 2, p. 9). The false-claim analysis covers only 43 classification and 131 segmentation papers that report a separate test set, at least two methods' Accuracy or DSC, and n (p. 9). The model is **paired**: a Dirichlet over discordant cells, using an externally estimated "model congruence" (median 0.67; sensitivity at the 25th and 75th percentiles) (pp. 9-11). That is the paired-variance problem the feasibility file called "unidentifiable", here handled by imputation plus sensitivity. Statistical testing: 13% of classification and 10% of segmentation papers (p. 3). CIs: 12% and 1% (SI A, p. 13). Paper-level data are withheld for reputational reasons (p. 11); code is public. **New:** the authors' "Claims Reloaded" web estimator has a "For reviewers" mode that "evaluates outperformance claims using summary statistics from reported results" for Accuracy and DSC (claims-reloaded.dkfz.de/calculate-false-claims, fetched with curl on 2026-10-19). No mention of language models or NLP anywhere in the text (keyword check). |
| Bean et al., "Measuring what Matters: Construct Validity in Large Language Model Benchmarks" (NeurIPS 2025 D&B) | https://arxiv.org/abs/2511.04703 | full-text (sections 3-6, appendices B-C) | **Confirms 17.1% and 3.1%; corrects the definition behind 16.0%; confirms that no venue breakdown is reported, with one qualification.** Corpus: 46,114 articles (ICML/ICLR/NeurIPS 2018-2024; ACL/NAACL/EMNLP 2020-2024), then 2,189 keyword hits, 522 after GPT-4o-mini screening, and 445 included (p. 3). The unit is papers that *introduce* a benchmark, not all empirical LLM evaluations. The Results section says "16.0% used uncertainty estimates **or** statistical tests to compare the results" (p. 5). Section 5.6 rephrases this as "conducted any statistical testing" (p. 8), so as a comparator it matches the idea's "any uncertainty" item, not a significance-test item. LLM-as-a-judge is used at least partially by 17.1% and exclusively by 3.1% (p. 5). It is coded only as a metric type; whether the judge was validated is not coded. Reliability: 46 papers double-reviewed, mean Brennan-Prediger kappa .524 (p. 3), mean percent agreement 68.1% (p. 28), which is a useful benchmark for the idea's own kappa. No result is broken down by venue or track (venue appears only in the corpus definition; limitations on p. 10). **Qualification:** the codebook has an `authorship` field (Academia 230, Mix 186, Industry 33, Other 4; p. 25), and the coded dataset is on GitHub (p. 19). An industry-versus-academia contrast is therefore computable from their release, although they do not report one. |
| Yang et al., "What Are We Measuring in NLG? A Meta-Analysis of Evaluation Trends 2020-2025" (v3, 13 Oct 2026) | https://arxiv.org/abs/2601.07648 | full-text (sections 1-6, appendix prompts) | **Corrects the earlier reading of H2.** "Under 8%" is 254 papers out of all 3,334 NLG papers. Of the 679 papers that use an LLM judge, 37.4% validate it against humans; of the 433 papers that use both a judge and human evaluation, 58.7% do (p. 7). The figure caption gives "16% of papers in 2025" (p. 1). The earlier statement that H2 (fewer than 25% of *judge* papers report *chance-corrected* agreement) is "close to settled" therefore rested on the wrong denominator. The right comparator is 37.4% for any validation. The share using a chance-corrected statistic is not reported in the main text, although the extraction prompt records the metric type (Appendix E). Scope: **main-conference** papers of ACL, EMNLP, NAACL and INLG only (p. 2), which confirms that industry tracks are not covered. A venue regression on the presence of human evaluation finds no venue effect among ACL/EMNLP/NAACL/INLG (Table 2, p. 8). Extraction was done by LLM (three-model majority), with 88.9% agreement with humans on validation presence (p. 5). |
| de Wynter, "Awes, Laws, and Flaws From Today's LLM Research" (v3; Findings of ACL 2025, DOI 10.18653/v1/2025.findings-acl.664, confirmed via Crossref) | https://arxiv.org/abs/2408.15409 | full-text (sections 1-9, appendices B-D) | **Confirms, with scope made precise.** The corpus is the most-cited papers citing GPT-3 or GPT-4 (Google Scholar top 1,000 each; Scopus top 2,000 for GPT-3; up to 10 June 2024), full texts taken from arXiv, giving 2,054 LLM-centred papers (pp. 3-4). Labels come from GPT-4o (gpt4-o-2024-05-13), checked against 100 hand labels per criterion (mean 91.91 ± 1.22%; p. 4). The criteria include statistical significance tests, declared model versions, declared call parameters, accounting for stochasticity, and evaluator type (Table 1, p. 4). "Only a quarter" of SOTA-claiming papers include statistical tests (p. 4). Validation of LLM evaluators is **not** coded, only their use. Venue stratification is explicitly left to future work (section 9.3, p. 9). Fields other than NLP are in the corpus but not separated, and there is no IS or business breakdown. |
| Siddiq, Islam-Gomes, Sekerak, Santos, "Large Language Models for Software Engineering: A Reproducibility Crisis" (v1, 29 Nov 2025) | https://arxiv.org/abs/2512.00651 | full-text (sections 1-4; 112 pp, appendices skimmed by keyword) | **Corrects the earlier reading.** RQ4 ("how do SE research venues ensure ... reproducible") analyses venues' calls for papers, artefact tracks and badges (section 3.6, pp. 12-13). It is not a paper-level comparison of reporting across venues; the earlier file called it a "venue-stratified reporting audit". Sample: 394 papers from Hou et al.'s SLR plus the ICSE 2025 (102), FSE 2025 (67) and ASE 2024 (77) technical tracks (pp. 6-7). The "Model" smell includes undisclosed inference parameters such as temperature, top-k and top-p (p. 10). There is no smell category for statistical uncertainty, repeated runs or validation of judges (keyword check). The EMSE publication stated on the abs page remains unverified: a Crossref title query on 2026-10-19 returned no match. |
| Rao and Callison-Burch, retitled in v2 (31 Jul 2026) "Agreement Measurement for Rubric-based LLM Judges: What to Report and Why" | https://arxiv.org/abs/2606.00093 | full-text (sections 1-4, 8) | **Confirms the snippet and qualifies it.** The 24-paper scan is coded by judged output scale: 11 graded or continuous, 7 pairwise, 3 binary, 2 ensembles, 1 mixed (p. 2). It is "descriptive and non-exhaustive ... not a systematic review", single-coded with no inter-coder reliability (p. 2). The 0.551-to-0.899 accuracy swing, with kappa crossing zero, is confirmed (p. 1). The paper shows that, for binary verdicts, Pearson, Spearman, Kendall's tau-b, phi and MCC are the same statistic (abstract). The idea's judge codes should therefore record the statistic **and** the protocol (scale, abstention handling, pooling), as the earlier file recommended. |
| Naser Moghadasi and Ghaderi, "What Twelve LLM Agent Benchmark Papers Disclose About Themselves: A Pilot Audit and an Open Scoring Schema" (v1, 20 May 2026) | https://arxiv.org/abs/2605.21404 | full-text | **Confirms it as a format template; it overlaps little in content.** Five fields (benchmark identity, harness, inference settings, cost, failure breakdown), each scored {0, 0.5, 1} with N/A collapsed out of the denominator, a one-sentence justification per field (pp. 1-4), single auditor in one pass (pp. 1, 4). Means: 0.38 for agent benchmarks, 0.66 for static benchmarks, 0.47 overall (Table III, p. 6). Released as a JSON Schema, a CODEBOOK.md and a CSV (github.com/mahdinaser/reprobe-audit; p. 8). It has no uncertainty field and no judge-validation field. |
| Riemer, Peter, Schwabe, Chatterjee, Adam, Davison, "Generative AI Is Neither Just Another IT Artefact nor a Colleague: Methodological Guidance for IS Scholarship" | https://doi.org/10.1111/isj.70027 (Crossref: https://api.crossref.org/works/10.1111/isj.70027) | metadata/snippet | **Not readable here (Wiley refuses automated fetches).** Crossref gives ISJ 36(2):161-165, issued 2025-12-25. The licence entries are Wiley VoR and TDM terms, **not** CC, so the earlier note that most ISJ title hits are CC does not apply to this item. No abstract is deposited. Of the 24 deposited references, none is an audit of LLM-paper practice; they include ISR 2001 (10.1287/isre.12.2.121.9700), MISQ 2021, two BISE items and HICSS 2025. Still an editorial with guidance, not an audit (as on 2026-10-05). |

Additional full texts read in this run (not named in the plan; read because they surfaced as close prior art):

| Title | Source URL | Access depth | Why it matters |
|---|---|---|---|
| Pathade, Pawar, Patil, "Attack Success Rate Is Not a Number: On Measurement Validity in Agentic AI Security Evaluation" (v1, 21 Sep 2026) | https://arxiv.org/abs/2609.25173 | full-text (all 7 pp.) | Full-text meta-analysis of 259 arXiv agentic-security papers (1,168 records, 911 unique, 550 screened, 535 full texts; Fig. 1, p. 3) with validated regex detectors. Headline figures (Table II, p. 4): **58.0% (Wilson 44.2-70.6) of a hand-coded random sample of 50 report neither a variance estimate nor repeated runs** (65.3% by automated coding); 30.9% disclose decoding; at least 24.7% use an LLM judge, of which **29.7% report any human-agreement check**. Analytical part: minimum detectable difference of 18.2 percentage points at m = 100, and about 21% ranking inversion for a 5-point true gap (p. 5). Adds a 10-item checklist (p. 5). Single coder; arXiv-only; no venue stratification; no per-paper claim re-analysis (pp. 6-7). It states that statistical practice "has been examined for language-model capabilities ... but not, to our knowledge, for agentic security" (p. 2). |
| Singh, "Certifying Compressed Language Models: An Audit and a Statistical Toolkit" (v1, 15 Aug 2026) | https://arxiv.org/abs/2608.15046 | full-text (sections) | A **preregistered audit of 17 published equivalence claims** (method papers, model cards, vendor documents; 16 eligible): none states a numerical margin, none releases task-matched per-item outputs, and 5 report too little to assess (abstract, p. 1). It explicitly computes certification "from disagreement observed under compression, not from independent-binomial variance". Its stated "constructive-audit genre" lineage is Dodge et al. 2019 and Marie et al. 2021 (Appendix A.3, p. 41). |
| Gringras and Salahshoor, "Frontier Lag: A Bibliometric Audit of Capability Misrepresentation in Academic AI Evaluation" (v4) | https://arxiv.org/abs/2605.04135 | full-text (sections) | A preregistered (OSF 10.17605/OSF.IO/7XM3D) OpenAlex audit of applied-domain LLM evaluations: 112,303 keyword matches, 18,574 admissible records. **Five domains: medicine, coding, law, education, scientific reasoning, plus "other"** (p. 10). An evaluation date is stated in 18.4% of full texts. Its related work (pp. 6-7) names further domain audits: Ko et al. 2025 (159 medical LLM papers with MI-CLEAR-LLM; stochasticity reported in 15.1%), Chen et al. 2026 (4,609 medical LLM evaluation articles), Balloccu et al. 2024 (255 ChatGPT studies) and Briggs et al. 2025 (2,674 political-science articles). These four are known here only through this paper. |
| "Illusions of the Gold Standard: A Large-scale Analysis of Human Evaluation Protocols for Long-form Text Generation" (ACL 2026 Main per arXiv comment) | https://arxiv.org/abs/2606.07936 | abstract (PDF keyword-checked) | 284 *CL papers (2023-2025) reviewed by hand plus about 1.8k by LLM-assisted analysis against 20 reportable human-evaluation criteria, including inter-annotator agreement. This is the human-evaluation side of the idea's "judge validation" component, in main-track NLP. |

---

## 2. Citation-chasing log

The tools are those the plan names. Each leg was tried at most three times, with 30, 45 and then 60 s back-off on HTTP 429 and at least 3.5 s between calls (`code/chase_citations.py`; per-call log in `results/novelty/chase_log.csv`; all returned works in `results/novelty/chase_works.csv`).

**OpenAlex.** The work lookups succeeded for all six seeds. Every `filter=cites:` call then returned HTTP 429. A manual check showed the body "$0 remaining; resets at midnight UTC", with retryAfter 65,945 s: the anonymous daily budget was exhausted. OpenAlex offered a free API key on request. No key was requested, because that would mean sending the user's e-mail address to a third party without the user's consent. All OpenAlex forward legs are therefore **not done**. For the two arXiv-only seeds, the OpenAlex records carry no `referenced_works`, so OpenAlex backward chasing returns nothing for them.

| Seed paper | Direction | Tool | Status | New relevant works found |
|---|---|---|---|---|
| Christodoulou et al. 2505.04720 | backward | Full-text reference list (22 main + 3 SI refs, pp. 11-12, 22) | done | Meta-research lineage only: Kapoor and Narayanan 2023 (*Patterns*, leakage), Varoquaux 2018 (*NeuroImage*, small-sample error bars), Ioannidis 2005, Christodoulou et al. MICCAI 2024 ("Confidence intervals uncovered"). No LLM or NLP meta-research is cited. |
| Christodoulou et al. | backward | Semantic Scholar /references | done (25 refs; 2 attempts) | Same as the full-text list. |
| Christodoulou et al. | backward | OpenAlex referenced_works | done, empty (0 deposited for the arXiv record) | none |
| Christodoulou et al. | forward | Semantic Scholar /citations | **not done** (429 on 3 attempts) | - |
| Christodoulou et al. | forward | OpenAlex cited_by | **not done** (429, daily budget) | - |
| Christodoulou et al. | forward | WebSearch (2 queries, #12 and #19) and DKFZ project page | done (proxy) | No application of the probability-of-false-claims method to LLM evaluation found. DKFZ "Claims Reloaded" estimator (tool). Oh 2605.17273 is now an ICML 2026 poster (icml.cc snippet). |
| Bean et al. 2511.04703 | forward | Semantic Scholar /citations | done (145 citing works; 3 attempts) | 2605.30315 (Resolution Diagnostics, ICML 2026 workshop); 2604.27405 (item-level reliable change); 2609.19182 (map of 14,767 benchmark papers); 2609.08812 (convergent/discriminant validity of 56 benchmarks); 2606.05029 (validity threats); 2603.18294 (health benchmark composition); 2608.19269 (claim replay in Inspect Evals); 2609.19866 and 2606.28574 (reproducibility is not construct validity, for LLM coding); 2601.10926 (model selection for social science). **None is a venue-stratified or IS audit of statistical or judge practice.** |
| Bean et al. | forward | OpenAlex cited_by | **not done** (429) | - |
| Bean et al. | backward | Crossref `reference` for 10.52202/085713-0590 | done, empty (reference-count 0 deposited) | - |
| Groß 2020/2021 (10.1007/978-3-030-55958-8_1) | forward | Semantic Scholar /citations | done (7 citing works) | Groß's own follow-ups (2109.10839 "Why Most Results of Socio-Technical Security User Studies Are False"; 2010.02117 extended version); a CHI 2025 meta-study of effect sizes; SoK on sample-size estimation (SOUPS 2023). **No LLM or venue-stratified follow-up.** |
| Groß 2020/2021 | forward | OpenAlex cited_by | **not done** (429) | - |
| Groß 2020/2021 | backward | Crossref `reference` | available (18 refs deposited; not needed for the plan's forward leg) | - |
| "Awes, Laws, and Flaws" 2408.15409 | backward | Semantic Scholar /references | done (55 refs; 2 attempts) | **Pang et al., "Understanding the LLM-ification of CHI"** (2501.12557, CHI 2025; venue-specific review of 153 LLM papers at CHI): an HCI analogue of the IS field transfer. Also "Get in Researchers; We're Measuring Reproducibility" (CCS 2023), Burnell et al. *Science* 2023, Gehrmann et al. JAIR 2023, Bouthillier et al. 2021, and the 32,111-model-card study (NMI 2024). |
| "Awes, Laws, and Flaws" | backward | Crossref `reference` for 10.18653/v1/2025.findings-acl.664 | done, empty (0 deposited) | - |
| "Awes, Laws, and Flaws" | forward | Semantic Scholar /citations | **not done** (429 on 3 attempts) | - |
| "Awes, Laws, and Flaws" | forward | OpenAlex cited_by | **not done** (429) | - |
| "Awes, Laws, and Flaws" | forward | WebSearch #18 and arXiv API author query (au:"Adrian de Wynter", 30 entries) | done (proxy) | No follow-up audit by the author or others found. |
| Miller 2411.00640 | forward | Semantic Scholar /citations | done (172 citing works; 2 attempts) | **2609.25173** (agentic-security audit, read in full); **2609.28177** (item-based audit of 394 adjacent-rank Open LLM Leaderboard claims, 391 without statistical support); 2606.00920 (pooled-binomial interval about 2x off; 12 of 15 adjacent pairs unresolved); 2604.11581 (naive SEs 40-60% smaller than total-error SEs); 2609.35815 (evalstats: statistics over LLM-judge scores); 2602.07150, 2509.24086, 2512.21326, 2608.22331 (run-to-run noise studies). None is IS. |
| Miller | forward | OpenAlex cited_by | **not done** (429) | - |
| Bowyer et al. 2503.01747 | forward | Semantic Scholar /citations | done (27 citing works; 2 attempts) | 2609.28177; 2606.00920; 2608.16894 (audit of the NeurIPS/ICML 2025 position tracks); "How Many Samples Do We Need? A Toolkit for Power-Aware Evaluation Design" (no arXiv id in record). None is IS. |
| Bowyer et al. | forward | OpenAlex cited_by | **not done** (429) | - |
| Singh 2608.15046 (new item) | backward | Full-text Appendix A.3 | done | Gringras and Salahshoor 2605.04135 (read, see Section 1); Thomas, Gligoric, Shah 2606.27687 (preregistering LLM analyses; abstract). |

The plan asked for Semantic Scholar "with a free API key" for forward citations of Miller, Bowyer and Christodoulou. No key was available. Miller and Bowyer succeeded without one; Christodoulou did not.

---

## 3. Sweeps the earlier check named as not done

### 3a. AIS eLibrary (JAIS, CAIS, MISQ, ICIS, ECIS 2023-2026; plan terms: reporting, reproducibility, error bars, inter-rater, large language model)

- **Direct search endpoint:** `https://aisel.aisnet.org/do/search/?q=...` answered **HTTP 403** to curl with a browser User-Agent (1 attempt). WebFetch could not resolve `aisel.aisnet.org` in this container. Full-text PDFs (`/cgi/viewcontent.cgi`) answered 403 behind a Cloudflare JavaScript challenge (3 attempts on 2 papers). The keyword search the plan asks for therefore still could not be run as a search.
- **Substitute 1, a crawl of public browse pages** (`code/aisel_crawl.py`; 1.5 s between requests; 308 track and landing pages, all HTTP 200; ECIS 2023 via its `ecis2023_rp` and `ecis2023_rip` listings, 14 more pages). This yielded **4,564 paper titles**: ICIS 2023 385, ICIS 2024 439, ICIS 2025 519; ECIS 2023 302, ECIS 2024 345, ECIS 2025 245, ECIS 2026 383; and, beyond the plan, AMCIS 2024 406, AMCIS 2025 618, AMCIS 2026 418, PACIS 2024 242, PACIS 2025 262 (`results/novelty/aisel_titles_2023_2026.csv`). ICIS 2026 has not taken place yet (December 2026). The crawl skipped panels, PDWs and TREO listings.
- **Title screen** (`code/screen_titles.py`; `results/novelty/aisel_screen_counts.csv`): 454 titles carry an LLM term. 36 combine an LLM term with a methods or evaluation term (flag A), and 10 combine a strict methods term with a review or audit term (flag B). All 45 flagged titles were read (`results/novelty/aisel_flagged_titles.csv`), as were every title in the methods tracks (ICIS 2025 "IS Research Methods", ICIS 2023-2024 and PACIS 2025 "Advances in Theory/Methods", ECIS 2024 "Innovative Research Methods", ECIS 2026 "Data Science and IS Research", AMCIS SIG-OSRA 2024-2026).
- **Abstracts read** (AIS eLibrary article pages, 7 papers): AMCIS 2025 Ahmed and Husna Tamanna, "Generative AI for Methodological Contributions in IS Research" (analyses "recently published articles in leading information systems journals" for how GenAI "influenced research methods"; it gives no sign of coding statistical reporting or judge validation; full text blocked); AMCIS 2026 "Beyond Agreement: Structural Alignment in Hybrid Human-LLM Evaluation Systems" (single study, 71 explanations); AMCIS 2026 "Collective Sensemaking ... Evaluation Practices Under Uncertainty" (team sensemaking, not research practice); AMCIS 2026 "Scale or Validity? Measuring Competitive Moves with Validated LLM Coding" (applied measurement study); AMCIS 2026 "Structural Biases in LLM-as-a-Judge Systems" (8,000 pairwise judgments, Fleiss' kappa 0.357; an evaluation, not an audit); ICIS 2024 "Integrating LLMs and Psychometrics: Global Construct Validity" (no abstract on the page); PACIS 2024 "Evaluation Framework for LLM-based Conversational Agents" (DSR framework). **None is an audit of published LLM-evaluation practice.**
- **Substitute 2, JAIS, CAIS and MISQ through Crossref**, which also covers 14 more IS journals and HICSS (`code/crossref_is_sweep.py`). Every record 2023-01-01 to 2026-12-31 by ISSN or DOI prefix gives **8,490 records**:

  | Source | Records | With deposited abstract |
  |---|---|---|
  | MISQ | 289 | 260 |
  | ISR | 558 | |
  | JMIS | 173 | |
  | JAIS | 106 | 99 |
  | ISJ | 275 | |
  | EJIS | 155 | |
  | JIT | 104 | |
  | JSIS | 134 | |
  | CAIS | 374 | 337 |
  | BISE | 233 | |
  | ISF | 450 | |
  | Electronic Markets | 317 | |
  | DSS | 581 | 0 |
  | I&M | 504 | |
  | ACM TMIS | 105 | |
  | IJIM | 397 | |
  | MISQE | 67 | |
  | HICSS (prefix 10.24251) | 3,668 | 0 (titles only) |

  Abstract counts are shown only for the plan's three journals and for the sources with no deposited abstracts; the rest are not reproduced in this table. Results:
  - 83 records combine an LLM term with a methods term (`results/novelty/is_flagged.csv`), and 6 have the methods term in the title (`is_flagged_strict.csv`).
  - All 83, plus 107 LLM titles containing research or evaluation words, were read.
  - **No audit of LLM-evaluation practice.** The IS-venue items closest to the idea are statistical-practice or reporting audits that are **not** about LLM papers: ISR 2026 "p-Hacking and Publication Bias in Design-Based Causal Studies in IS" (558 articles, 7,516 tests, seven IS journals, 2000-2023, with an IS-calibrated local false discovery rate); CAIS 2025 "The Digital Experiment Reporting Protocol (DERP)" (a CONSORT-derived checklist applied to digital experiments in ISR and MISQ: "only 43% of the papers providing sufficient detail on core items"); CAIS 2026 "How OPEN Are We?" (policies of 19 IS venues); CAIS 2023 "HARKing and P-Hacking" (survey and recommendations).
  - LLM-specific IS items are editorials or guidance: ISJ 10.1111/isj.70027; ISR 2023 and 2025 editorials; JIT 2025 "Next-generation IS research methods ... generative AI as the elephant in the room"; IJIM 2024 "Augmenting research methods with foundation models and generative AI"; ACM TMIS 2025 TAISR framework; ISJ 2026 integrity editorials.
- **HICSS-57 (2024), found by WebSearch #2 and #14:** Koenigstorfer, Haberl, Kowald, Ross-Hellauer, Thalmann, "Black Box or Open Science? Assessing Reproducibility-Related Documentation in AI Research" (DOI 10.24251/hicss.2024.081 per Crossref). A documentation framework applied to 51 AI papers (snippet). This is an IS-venue reproducibility audit of **AI** papers, not of LLM evaluations or statistical or judge practice. ScholarSpace answered with a browser challenge, so it is metadata/snippet only. HICSS also has a minitrack, "Open Science Practices in IS Research".
- **WebSearch, aisel-restricted** (#1-4, #17): the domain filter leaked in #4 (arXiv only). No audit was found. ECIS 2025 "Are LLMs Good Management Consultants?" is an applied paper using an LLM judge with "strong alignment with human raters" (no statistic visible in the snippet), and is a plausible audit subject.

### 3b. dblp titles for ICIS/ECIS/HICSS methods tracks

**Not done.** `dblp.org`, `dblp.uni-trier.de` and `dblp.dagstuhl.de` all returned an Anubis "Making sure you're not a bot!" page (HTTP 202) to curl. WebFetch could not resolve `dblp.org`. As substitutes, the ICIS/ECIS titles come from the AIS crawl above, and HICSS 2023-2026 titles (3,668) come from Crossref.

### 3c. Other sweeps run

- **arXiv API** (`results/novelty/arxiv_api_queries.csv`): 16 searches, including meta-research plus LLM, audits of published LLM claims, judge-validation surveys, reporting-practice terms, "information systems" with LLM and rigor, claim survival, repeated-run meta-analyses, industry tracks, and business/management reporting audits. There were also 7 id-list lookups for 33 candidate abstracts.
- **WebSearch:** 20 calls (`results/novelty/websearch_log.csv`).
- **Crossref title queries:** 7, for venue status and DOIs.

---

## 4. New prior-art comparison

Works not in the 2026-10-05 table, or whose reading changed. Ordered by closeness to the idea.

| Work | Year | Venue or status | Link | What it does | Overlap with idea 6 | What the idea still adds |
|---|---|---|---|---|---|---|
| Pathade, Pawar, Patil, "Attack Success Rate Is Not a Number" | 2026 | arXiv preprint (cs.CR, Sep 2026) | https://arxiv.org/abs/2609.25173 | Codes 259 agentic-security papers for variance or CI, repeated runs, decoding disclosure, LLM-judge use and human-agreement checks; hand-coded subsample with Wilson CI; power and ranking-inversion analysis; 10-item checklist | **High on design.** Same RQ1 items (uncertainty, runs, decoding, judge validation) coded together, plus an n-based resolvability argument (the RQ2 logic, analytically rather than per paper). It refutes the earlier statement that no study "codes judge validation ... alongside statistical practice" | IS venues and industry tracks; per-claim re-analysis on each paper's own n; two coders with kappa (theirs is single-coder); venue and year comparison |
| Singh, "Certifying Compressed Language Models: An Audit and a Statistical Toolkit" | 2026 | arXiv preprint (Aug 2026) | https://arxiv.org/abs/2608.15046 | Preregistered audit of 17 published LLM-compression equivalence claims for evidential sufficiency; paired equivalence tests; certification tables | **High on RQ2 framing** ("we audit evidential sufficiency, not truth"; claims checked against what the reported evidence could support). It argues that independent-binomial variance is the wrong model for close pairs | Superiority claims in applied IS and industry LLM papers; field-level survival rate; reporting-prevalence pairing |
| Christodoulou et al. "Claims Reloaded" estimator (DKFZ) | 2025-2026 | Public web tool accompanying arXiv 2505.04720 | https://claims-reloaded.dkfz.de/calculate-false-claims | "For reviewers" mode: probability of false outperformance claim from reported test-set size and performance (Accuracy, DSC), paired via model congruence | **Overlaps the "standard-library survival calculator" deliverable.** | ICC or clustered and Beta-Binomial arms; a command-line or library form; application to LLM claims. The calculator is no longer a distinct contribution |
| Gringras and Salahshoor, "Frontier Lag" | 2026 | arXiv preprint (v4), preregistered | https://arxiv.org/abs/2605.04135 | OpenAlex audit of 18,574 applied-domain LLM evaluation records: models versus frontier, evaluation-date disclosure, configuration disclosure | Domain-stratified reporting audit of LLM evaluations (model, date, decoding) across five applied fields | Business/IS is not among its five domains; statistical uncertainty, judge validation and claim survival are not coded |
| Ko et al. (as reported in 2605.04135) | 2025 | Journal article (not verified here) | via https://arxiv.org/abs/2605.04135 (pp. 6-7) | MI-CLEAR-LLM audit of 159 medical LLM papers in top-decile journals: model version 96.9%, query date 50.9%, stochasticity 15.1% | Field-specific checklist audit of LLM-study reporting (medicine) | Field (IS), uncertainty and claim survival, judge validation. *Not read; secondary* |
| "Illusions of the Gold Standard: A Large-scale Analysis of Human Evaluation Protocols for Long-form Text Generation" | 2026 | ACL 2026 Main (arXiv comment) | https://arxiv.org/abs/2606.07936 | 284 + about 1.8k *CL papers coded against 20 human-evaluation reporting criteria, including inter-annotator agreement | Judge and human-evaluation validation reporting in NLP main tracks | Industry tracks; IS; statistical uncertainty; claim survival |
| Ahmed and Husna Tamanna, "Generative AI for Methodological Contributions in Information Systems Research" | 2025 | AMCIS 2025 (SIG-OSRA) | https://aisel.aisnet.org/amcis2025/sig_osra/sig_osra/29/ | Per its abstract, analyses recent articles in leading IS journals for how GenAI has influenced research methods | **Only IS-venue review of IS papers using GenAI found.** On its abstract it is descriptive (uses), not an audit of statistical or judge-validation practice | Almost everything in RQ1-RQ3. *Abstract only; full text behind Cloudflare and subscription* |
| Koenigstorfer et al., "Black Box or Open Science? Assessing Reproducibility-Related Documentation in AI Research" | 2024 | HICSS-57, DOI 10.24251/hicss.2024.081 | https://aisel.aisnet.org/hicss-57/cl/open_science_practices/3 | Documentation framework applied to 51 AI papers | IS-venue reproducibility audit of AI papers (not LLM-specific; no statistical items per snippet) | LLM evaluations; statistics; judge validation; claim survival. *Snippet only* |
| "p-Hacking and Publication Bias in Design-Based Causal Studies in Information Systems" | 2026 | Information Systems Research, DOI 10.1287/isre.2024.1365 | https://doi.org/10.1287/isre.2024.1365 | Caliper-style audit of 7,516 tests in 558 articles from seven IS journals; IS-calibrated local false discovery rate | **IS-venue statistical-practice audit with a re-analysis tool**, but of causal-inference papers, not LLM evaluations | The LLM-evaluation frame. It is also a precedent showing ISR publishes this genre. *Crossref abstract* |
| "The Digital Experiment Reporting Protocol (DERP)" | 2025 | CAIS 57, DOI 10.17705/1cais.05706 | https://doi.org/10.17705/1cais.05706 | CONSORT-derived checklist applied to digital experiments in ISR and MISQ: 43% give sufficient detail on core items | IS-venue reporting-prevalence audit plus a checklist (the RQ1 design, for experiments) | LLM evaluations; uncertainty and claim survival; judge validation. *Crossref abstract* |
| Pang et al., "Understanding the LLM-ification of CHI" | 2025 | CHI 2025 (arXiv comment: conditionally accepted) | https://arxiv.org/abs/2501.12557 | Systematic review of 153 CHI papers 2020-24 that engage with LLMs: roles, contributions, acknowledged validity and reproducibility concerns | Venue-specific review of LLM papers in an applied computing field: the HCI analogue of "do this for IS" | Statistical and judge coding; claim re-analysis; IS frame. *Abstract* |
| "How Sensitive Are LLM Leaderboard Claims to Hidden Model Selection?" | 2026 | arXiv preprint | https://arxiv.org/abs/2609.28177 | Item-based audit of 394 adjacent-rank Open LLM Leaderboard claims: 391 lack statistical support | Claim-survival audit, on leaderboards | Papers rather than leaderboards; IS and industry; reporting coding. *Abstract* |
| "Resolution Diagnostics for Paired LLM Evaluation" | 2026 | ICML 2026 Workshop on Hypothesis Testing (arXiv comment) | https://arxiv.org/abs/2605.30315 | Paired resolution ratio q = N/N*: 11 of 40 Open LLM Leaderboard v1 pairs and 4 of 9 MMLU-Pro top-10 pairs unresolved; the unpaired Cohen-h shortcut is off by about 2x | Retrospective resolvability of published comparisons (RQ2 logic) | Literature of papers; IS. It also implies the idea's three unpaired models need a paired arm. *Abstract* |
| "How Much Can Repeated Running Buy? A Measured Variance Ceiling for LLM Code Evaluation" | 2026 | NeurIPS 2026 workshop (arXiv comment) | https://arxiv.org/abs/2606.00920 | The pooled-binomial interval is about 2x too narrow for generalisation and 2x too wide for the fixed set; 12 of 15 adjacent pairs unresolved under clustered intervals | Directly bears on the naive-binomial arm of RQ2 | One benchmark, not a literature. *Abstract* |
| "Hidden Measurement Error in LLM Pipelines Distorts Annotation, Evaluation, and Benchmarking" | 2026 | arXiv preprint | https://arxiv.org/abs/2604.11581 | Naive SEs 40-60% smaller than total-evaluation-error SEs (judge, temperature, prompt) | Supports the "procedure" fragility component and the upper-bound reading of survival | Literature audit. *Abstract* |
| J Clin Epidemiol cross-sectional study of LLMs for systematic reviews | 2026 | *Journal of Clinical Epidemiology* (per PubMed and HKBU listing) | https://pubmed.ncbi.nlm.nih.gov/42309363/ | 229 studies and 440 tasks appraised with adapted CHART and QUADAS-2 for reporting transparency and safeguards | Reporting audit of LLM-evaluation papers in one applied field (evidence synthesis) | IS; statistics and claim survival. *Snippet only* |
| BMC Medical Research Methodology scoping review of LLM use and methodological reporting in qualitative research | 2026 | BMC Med Res Methodol, DOI 10.1186/s12874-026-02913-1 | https://link.springer.com/article/10.1186/s12874-026-02913-1 | Reporting of LLM technical parameters (e.g. temperature) "highly inconsistent" | Reporting-prevalence audit of LLM-using studies (qualitative research) | IS; quantitative evaluation claims. *Snippet only* |
| Oh, "Position: State-of-the-Art Claims Require State-of-the-Art Evidence" (status update) | 2026 | **ICML 2026 poster** (icml.cc snippet; was "arXiv only") | https://arxiv.org/abs/2605.17273 | As in the earlier table | As before | As before |

Also seen at abstract level, lower overlap:
- 2604.25923, scoping review of 22 evaluation concerns.
- 2609.19182, map of 14,767 benchmark papers.
- 2609.24516, LLJ Cards.
- 2508.18076, Chehbouni et al., "Neither Valid nor Reliable?"
- 2507.04491, Lin, *Behavior Research Methods* 2026.
- 2606.27687, preregistering for the next LLM.
- 2610.16051, an audit of ML speed claims in topology optimisation.
- 2606.16974, documentation in 56,800 AI-conference papers.
- 2604.27405, 2602.07150, 2509.24086, 2512.21326 and 2608.22331, run-to-run noise studies.
- IS-venue LLM applications: MISQ 2026 RATER; ISR 2026 "From Lexicons to LLMs"; Electronic Markets 2026 "LLM-as-a-Judge for mental support: a meta-evaluation"; AMCIS 2026 "Structural Biases in LLM-as-a-Judge Systems".

---

## 5. Updated verdict: partially-covered

**What the deep check adds to the earlier reasoning:**

1. **The field gap stands within these searches.** The following checked sources contain no audit of statistical or judge-validation practice in LLM-evaluation papers published in IS journals or IS conferences, and no audit of ACL/EMNLP/NAACL industry tracks:
   - 4,564 AIS proceedings titles for 2023-2026;
   - 8,490 Crossref records for 17 IS journals plus HICSS;
   - 20 WebSearch queries and 16 arXiv API searches;
   - Semantic Scholar forward chasing of Bean et al. (145 citers), Miller (172), Bowyer et al. (27) and Groß (7).

   Yang et al. confirm that they cover main tracks only. Bean et al. and "Awes, Laws, and Flaws" report no venue breakdown, and the latter defers it to future work.
2. **The design-combination claim has narrowed further.**
   - Pathade et al. (2609.25173) code uncertainty, repeated runs, decoding and judge-human agreement together, with a Wilson-CI hand-coded sample and a power analysis. Each element of RQ1 now has an LLM-specific precedent from September 2026.
   - Singh (2608.15046) and 2609.28177 run claim-level evidential-sufficiency audits of published LLM claims.
   - Christodoulou et al.'s method is paired and already packaged as a reviewer-facing tool.
   - What remains distinct is the **combination applied to IS and industry-track papers**: per-claim re-analysis on each paper's own reported n, judge validation coded with protocol fields, and an IS versus industry versus year comparison.
3. **Two earlier undermining items weaken, and two strengthen.**
   - Weaker: the H2 objection, because 37.4% (not under 8%) is the right comparator for judge papers and chance-corrected agreement is not reported by Yang et al. Also weaker: the Siddiq et al. venue overlap, because their venue question is about policies.
   - Stronger: the calculator overlap with the DKFZ estimator, and the RQ1 design overlap with 2609.25173.
   - Further, IS venues already publish statistical-practice audits (ISR 2026 p-hacking; CAIS 2025 DERP). The paper cannot be framed as the first IS reporting or statistics audit, only as the first one for LLM-evaluation papers. This helps venue fit (ISR, CAIS) and removes the "methodological novelty to IS" angle.
4. **Why not "largely-covered":** the unit of analysis (IS and industry-track LLM evaluations) and the IS-versus-industry comparison over 2023-2026 are uncovered by anything found. The field-transfer contribution is the one the plan relies on. **Why not "likely novel":** every component construct is published in a neighbouring field. The verdict stays **partially-covered**, nearer to "largely-covered" on design than it was on 2026-10-05.

**Consequences for the plan** (recommendations, not results):
- Add a paired arm (congruence-based, as in Christodoulou et al., or the paired resolution in 2605.30315) to the three unpaired uncertainty models. Report the naive-binomial arm as a known-biased reference, since 2606.00920 and 2608.15046 both argue that independent-binomial variance is mis-specified for close pairs.
- Drop the survival calculator from the contribution list, or position it as an extension of the DKFZ estimator.
- Replace the H2 comparator "under 8%" with Yang et al.'s 37.4% (judge papers with any human validation) and Pathade et al.'s 29.7%.
- Use Bean et al.'s 16.0% for the "any uncertainty or test" item; report the comparators with their different units.
- Cite 2609.25173, 2608.15046, 2605.04135 and the ISR 2026 and CAIS 2025 audits as the immediate antecedents.

---

## 6. Literature stop condition

Rule (`02_candidate_ideas.md` section 4.1, first clause of the stopping rule, applied exactly as written): *stop (or demote to a CAIS methods essay) if ... a published IS-venue audit of statistical or judge-validation practice in LLM papers is found.*

**Decision: not-triggered.**

Evidence:
- **AIS proceedings:** none of the 454 LLM-titled papers in 4,564 AIS proceedings titles (ICIS 2023-2025, ECIS 2023-2026, AMCIS 2024-2026, PACIS 2024-2025) is such an audit. All 45 flagged titles were read, and 7 abstracts.
- **Crossref, IS journals and HICSS:** none of 8,490 records is such an audit. The 83 flagged records and 107 LLM research-practice titles were read.
- **WebSearch:** five aisel-targeted queries and five IS-journal-targeted queries found none.
- **Not LLM papers:** the IS-venue audits that were found concern causal-inference studies (ISR 2026), digital experiments (CAIS 2025), AI-paper documentation (HICSS-57) or venue policies (CAIS 2026).
- **AMCIS 2025 (Ahmed and Husna Tamanna):** the one IS-venue review of IS papers that use GenAI is descriptive on its abstract. It does not meet the condition on the evidence available, but its full text could not be read.

Limits on this decision:
- (i) The AIS full-text search endpoint and the PDFs are still blocked, so matching inside abstracts and full texts of ICIS/ECIS/AMCIS papers was not possible (titles only, plus 7 abstracts).
- (ii) HICSS has titles only in Crossref.
- (iii) ICIS 2026 is unpublished; AMCIS 2023, PACIS 2023 and ICIS/ECIS panel and TREO listings were not crawled.
- (iv) Publisher full texts for ISR, MISQ, JMIS, ISJ, EJIS, JIT, JSIS, DSS and I&M were not searched, only their Crossref titles and deposited abstracts.

Before preregistration: obtain the AMCIS 2025 full text and re-run an AIS eLibrary keyword search from a browser.

---

## 7. Search limits

- **OpenAlex:** the anonymous daily budget was exhausted on the first cited-by call (429, retryAfter 65,945 s). No OpenAlex forward leg was done. No API key was requested, because that would mean sending the user's e-mail address to a third party.
- **Semantic Scholar** (no key): forward citations of Christodoulou et al. and of "Awes, Laws, and Flaws" failed (429 on 3 attempts each). WebSearch and arXiv API proxies found no follow-ups, but proxy searches are not citation indexes, so citing works may be missing.
- **dblp:** blocked by a bot check on all hosts. ICIS/ECIS titles came from the AIS crawl and HICSS titles from Crossref.
- **AIS eLibrary:** the search endpoint answered 403 and the PDFs sit behind Cloudflare and a subscription. Title-level coverage only, plus 7 abstracts. The crawl skipped panels, PDWs and TREOs. AMCIS and PACIS were added beyond the plan.
- **Publisher sites** (Wiley, INFORMS, Elsevier, Taylor & Francis, ACM) were not fetched. ISR, CAIS and other items are cited from Crossref-deposited abstracts or WebSearch snippets and marked as such. Ko et al. 2025, Chen et al. 2026, Balloccu et al. 2024 and Briggs et al. 2025 are known only through 2605.04135's related work.
- **WebFetch** could not resolve `dblp.org`, `aisel.aisnet.org` or `claims-reloaded.dkfz.de` in this container. curl reached the last two.
- **Keyword screening of titles** can miss audits whose titles name neither LLMs nor methods terms. Abstract screening was possible only where Crossref holds abstracts: none for DSS, I&M, JMIS, JSIS, EJIS, IJIM or HICSS.
- **Coverage gaps:** English only. No Scopus, Web of Science or Google Scholar. Semantic Scholar /citations returned at most 1,000 rows per seed; all seeds were below that (maximum 172).
- **Reading depth:** full texts were read in the sections cited, not cover to cover for the long items (2512.00651: 112 pp; 2608.15046: 109 pp; 2605.04135: 52 pp).

---

## 8. Reproducibility

- **Software:** Python 3.11.15 (scratchpad venv; all scripts use the standard library only, run with `-I`); pdftotext 24.02.0 (poppler); curl 8.5.0. No random numbers were drawn, so there are no seeds.
- **Scripts:** `code/chase_citations.py` (run 05:36-05:50 UTC, 868.0 s elapsed); `code/aisel_crawl.py` (308 fetches, all HTTP 200); `code/crossref_is_sweep.py` (21 cursor pages); `code/screen_titles.py`; `code/arxiv_parse.py`. Small ad-hoc curl calls (ECIS 2023 listing pages, abstract pages, Crossref DOI and title lookups, the DKFZ pages) were run inline and are described in Sections 1-3.
- **Inputs and checksums:**
  - The full-text PDFs are listed with sha256, page count and size in `results/novelty/fulltext_manifest.csv` (11 files).
  - Large intermediates that are not committed: `is_records.csv` (8,490 Crossref records with abstracts, 4.97 MB, sha256 `304e3030a79b40a378e1d90794514c1dc9296c977cf247e01ffa822b0dbcc3fc`) and the crawler's `aisel_titles.csv` (sha256 `36a9c4d8a16b13fc1299eb04b8f6cef10b663397e26c4f6a2d642be614a8fe7d`; the committed `aisel_titles_2023_2026.csv` adds the 302 ECIS 2023 titles).
- **Outputs** (`results/novelty/`):
  - `chase_summary.csv`, `chase_log.csv`, `chase_works.csv`;
  - `aisel_titles_2023_2026.csv`, `aisel_screen_counts.csv`, `aisel_flagged_titles.csv`, `aisel_fetch_log.csv`;
  - `is_source_counts.csv`, `is_flagged.csv`, `is_flagged_strict.csv`, `crossref_log.csv`;
  - `arxiv_api_queries.csv`, `websearch_log.csv`, `fulltext_manifest.csv`.

  The last line of `aisel_screen_counts.csv` is a "total" row.
- **Query counts:**
  - WebSearch: 20.
  - arXiv API: 16 searches and 7 id lookups; the author query was issued twice because the first syntax returned 0.
  - Crossref: 21 sweep pages, 7 DOI lookups and 8 title queries.
  - OpenAlex: 6 lookups OK and 19 calls answered 429.
  - Semantic Scholar: 8 legs, 6 done.
  - AIS: 1 search attempt (403), 322 listing pages, 14 article-page fetches and 3 PDF attempts (403).
  - dblp: 3 curl attempts and 1 WebFetch attempt.
  - WebFetch: 3 attempts, all DNS failures.
- **Deviations from the written plan:**
  1. The AIS eLibrary keyword search was replaced by a browse-page crawl plus Crossref, because the search endpoint returned 403.
  2. The dblp sweep was replaced by the AIS crawl (ICIS/ECIS) and Crossref (HICSS) because of the bot wall.
  3. The Semantic Scholar key was unavailable, and the OpenAlex daily budget was exhausted. The affected forward legs are recorded as not done, with WebSearch and arXiv API proxies.
  4. AMCIS 2024-2026 and PACIS 2024-2025 were added to the plan's ICIS/ECIS list.
  5. Four full texts not named in the plan were read (2609.25173, 2608.15046, 2605.04135, 2606.07936).
  6. The ISJ editorial is metadata-only (Wiley).
  7. Only the literature criterion of the stopping rule is decided here; the pilot criteria belong to the pilot report.
