# Research Project Log

Persistent record for the research collaboration. Every stage appends an entry with: what was completed, what evidence was found, what remains uncertain, the proceed/revise/pivot/stop decision, and the next action.

Dates are the actual dates work was performed in this environment.

---

## Stage 0 — Environment, constraints, and open questions (2026-10-03)

### What was completed

- Verified the repository `jubaeralmahmud23-ship-it/employee_monitoring_system` is empty on GitHub (no commits, no branches). The working branch `claude/peaceful-cori-ny59q5` is created locally with these records as its first content.
- Probed which research tools and hosts are actually usable from this cloud session (see table below).
- Set up the records structure under `research/`.

### Environment facts (verified by direct probes on 2026-10-03)

| Capability | Status | Evidence |
|---|---|---|
| Web search (titles, URLs, snippets) | Available | WebSearch tool returned scholarly results (SciTePress, arXiv listings) |
| Fetching full text from arXiv, publishers, DOI resolver | **Blocked** | Egress proxy answered 403 to CONNECT for arxiv.org, export.arxiv.org, doi.org, sciencedirect.com, link.springer.com, dl.acm.org, ieeexplore.ieee.org, onlinelibrary.wiley.com, aisel.aisnet.org, openreview.net, aclanthology.org, and others |
| Bibliographic APIs (Crossref, OpenAlex, Semantic Scholar, DBLP) | **Blocked** | 403 to CONNECT for api.crossref.org, api.openalex.org, api.semanticscholar.org, dblp.org |
| Dataset hosts: Hugging Face, Zenodo, Kaggle, 4TU.ResearchData, UCI, OpenML, PhysioNet, Figshare, Mendeley Data | **Blocked** | 403 to CONNECT for each |
| Model downloads: Hugging Face Hub, Ollama registry, PyTorch download server | **Blocked** | 403 to CONNECT |
| GitHub (github.com, api.github.com, raw.githubusercontent.com, release assets) | Reachable | HTTP 200/301/400/404 responses (host reachable). GitHub access for this session is scoped to the user's repository; other public repositories must be added explicitly before being read |
| PyPI (pypi.org, files.pythonhosted.org) | Reachable | `pip download pm4py` succeeded |
| Google Cloud Storage (storage.googleapis.com) | Reachable at host level | HTTP 400 at root; individual public buckets untested |
| Paid LLM APIs | **Not available** | No API key present in the environment; none will be assumed |
| Compute | CPU only | 4 vCPUs, 15 GB RAM, ~30 GB writable disk, Python 3.11 |

Consequences for the project:

1. Literature review depth is limited to **metadata and search snippets**. No paper can be examined in full text from this session. All evidence tables must say so. Bibliographic details cannot be verified against Crossref or publisher pages; they can only be cross-checked across independent search results. This is a disclosed limitation, not a hidden one.
2. **No neural language model or embedding model can be run here** unless it is distributed via PyPI or GitHub releases (for example spaCy models). Any study whose method depends on running an LLM, or on calling an LLM API, is currently blocked. Studies using classical ML, statistics, process mining (pm4py), information retrieval with lexical methods, or re-analysis of released experimental outputs hosted on GitHub are feasible now.
3. Data must come from GitHub (added explicitly to the session) or PyPI, or the network policy must be widened. The owner can change *Network access* in the environment settings (cloud environment menu in the session title bar, then Edit): either a broader access level, or Custom with the hosts above added under Allowed domains. Steps: https://code.claude.com/docs/en/cloud-environments#network-access

### Open questions for the author (answers materially change feasibility)

1. **Network policy.** Are you willing to widen the environment's network access to include arxiv.org, doi.org, api.crossref.org, api.openalex.org, api.semanticscholar.org, huggingface.co and zenodo.org? Without this, full-text review, DOI verification, and any LLM/embedding experiment are impossible from this session.
2. **Research interest signal.** The repository is named `employee_monitoring_system`. Is AI-enabled employee monitoring / algorithmic management a topic you want to pursue (a strong business information systems topic with governance and privacy dimensions), or is the repository name unrelated to this project?
3. **Background and target.** What is your academic level and purpose (undergraduate thesis, Master's, PhD, independent researcher), and is there a preferred journal, publisher, discipline (CS vs. IS), or deadline? This drives journal selection and the kind of contribution reviewers will expect.
4. **Skills and resources beyond this session.** Do you have a local machine with a GPU, institutional access to full-text databases, any LLM API credits, or organizational data or participants you are permitted to use? If yes, parts of the study can run on your side with code prepared here.
5. **Budget constraints.** Is there any budget for publication fees (APCs) or API usage, or must the project be zero-cost end to end? This rules journals and methods in or out early.

Work continues under the default assumptions (zero budget, CPU only, public data reachable now or via a policy change) until answers arrive.


### Addendum (2026-10-03): verified offline tooling

A scratch virtual environment (outside the repository) installed and loaded, from PyPI and GitHub releases only:

| Package | Version | Note |
|---|---|---|
| pm4py | 2.7.23.8 | Process mining; AGPL-3.0 with commercial option (academic use fine) |
| scikit-learn | 1.9.1 | Classical ML |
| statsmodels | 0.15.0 | Statistics |
| spaCy + en_core_web_sm | 3.8.16 | Model downloaded from GitHub releases, so spaCy pipelines are usable without Hugging Face |

Additional hosts probed and **blocked** on 2026-10-03: SEC EDGAR (sec.gov), data.gov, EUR-Lex, World Bank API, OECD, archive.org, Common Crawl, Wikimedia dumps, FRED, ECB data portal, Bangladesh open-data portals, OpenStreetMap APIs. Any public-data study must therefore use data mirrored on GitHub or shipped in PyPI packages until the network policy is widened.

Git push to GitHub was refused on 2026-10-03 (the Claude GitHub App lacks write access to this repository). Commits are held locally until access is granted.


### Author answers received (2026-10-03)

1. **Network policy:** author agrees to widen network access. Not yet in effect as of this entry (arxiv.org, doi.org, api.crossref.org, api.openalex.org, api.semanticscholar.org, huggingface.co, zenodo.org still denied on re-probe). Full-text review, DOI verification and any model-based experiment remain blocked until the change is applied.
2. **Repository name:** unrelated to the project. AI-enabled employee monitoring is not a preferred topic; the human-AI / algorithmic-management area stays in the landscape only on its own merits.
3. **Goal:** publication in a top journal. No preferred discipline, journal or deadline stated. Implication: the contribution must be substantive by top-tier standards; a model-on-dataset study will not meet that bar.
4. **External resources:** none. No GPU, no institutional full-text access, no LLM API credits, no organizational data, no participants.
5. **Budget:** article processing charges only if the manuscript is very strong; otherwise a no-cost route. Note for later journal selection: most top IS and CS journals charge nothing on the standard subscription route; open access is optional, and choosing the no-fee route does not remove the paper from indexing or citation databases.

Working assumptions updated accordingly: zero cost, CPU only, public data via GitHub/PyPI now and via widened network access later; studies must be designed so that the main claim does not depend on paid APIs.


### Network policy widened (2026-10-03, re-verified)

| Capability | Status now | Evidence |
|---|---|---|
| arXiv (abstracts, HTML/PDF full text, export API) | Reachable | HTTP 200; API returned metadata for 2005.11401 |
| Crossref API, DOI resolver | Reachable | API returned the ACM Computing Surveys record for 10.1145/3571730 |
| OpenAlex API | Reachable but rate-limited | HTTP 429 on first calls |
| Semantic Scholar API and site, DBLP, OpenReview, ACL Anthology, NeurIPS/PMLR proceedings, Springer, AIS eLibrary | Reachable | HTTP 200/301/303 |
| Hugging Face models and datasets | Reachable, downloads work | 91 MB model file downloaded in 2.7 s via huggingface_hub; dataset metadata readable |
| Zenodo API, 4TU.ResearchData, UCI, OpenML, data.gov, EUR-Lex, archive.org, Wikimedia dumps, OSF, Figshare, PhysioNet, FRED | Reachable | HTTP 200 (Zenodo API query returned hit counts) |
| ACM DL, ScienceDirect, IEEE Xplore, Wiley, INFORMS, Taylor & Francis, MISQ site, SSRN, SEC EDGAR | Refuse automated fetches (HTTP 403/418 from the site itself) | Metadata for these venues comes from Crossref, Semantic Scholar and search snippets |
| Kaggle | Pages load; downloads need an account token | Not available |
| Paid LLM APIs, GPU | Still unavailable | Unchanged |

Consequences: literature records can now reach abstract depth broadly and full-text depth for open-access papers; DOIs and venues can be verified with `research/tools/verify_refs.py` (self-test passed against Crossref and arXiv); embedding models and small open LLMs can be run on CPU, so model-based pilots are possible at small scale. The first sweep was stopped after one area because its instructions still assumed the closed network; it was relaunched with updated instructions and the completed area is being redone at abstract depth.

GitHub push remains refused (Claude GitHub App not connected to the repository).


### Scope note (2026-10-03)

The author briefly considered broadening the landscape to software tools and packages and to other AI subfields such as computer vision, then withdrew the request. Scope remains the eight areas listed for Stage 1-2; a broadening can be added as a ninth sweep later if a candidate idea calls for it.


### Sweep interruption and resume (2026-10-03, 11:19-11:26 UTC)

The Stage 1-4 sweep completed all eight landscape scouts, eight citation audits, four ideation lenses and the merge (21 agent results). The first pair of challenge agents (novelty and feasibility for idea 1) was then stopped by an interrupt from the client at 11:19:50 UTC before writing any file; the run ended. The run was resumed from its journal cache at about 11:26 UTC: cached results are reused unchanged and only the challenge, synthesis and critique stages execute. No records from the completed stages were altered by the interruption.


### Hand-off snapshot (2026-10-03, ~12:40 UTC)

Author's usage allowance was about to end. Actions taken so that nothing is lost:

- All records committed on `claude/peaceful-cori-ny59q5` (15 commits at snapshot time). GitHub push refused both via git and via the GitHub connector (403 "Resource not accessible by integration"): the Claude GitHub App is not installed on the repository.
- A git bundle of the branch, a tarball of `research/`, and `RESUME.md` were sent to the author in the chat as the off-container backup.
- A background loop in the container commits any new files under `research/` every three minutes and will push automatically if GitHub access is granted while the session is alive.
- Stage 3-4 continuation workflow still running: novelty and feasibility checks complete for ideas 1-3 (six files in `03_challenge/`); ideas 4-8 and the synthesis and critique stages pending. `RESUME.md` says how to finish them.


### GitHub push working (2026-10-03, 12:41 UTC)

The author granted the Claude GitHub App access. `git push` succeeded; the remote branch `claude/peaceful-cori-ny59q5` matches the local HEAD exactly (verified by SHA and a 24-file tree listing through the GitHub API). From this point the repository on GitHub is the durable copy; the bundle and tarball sent earlier are a redundant backup. The background autosave loop now also pushes after each commit.

### Decision

**Proceed** to the preliminary literature landscape using web search, with every record marked as snippet-level evidence, and in parallel generate and adversarially challenge candidate ideas. No project selection yet.

### Next action

Run the Stage 1-2 landscape sweep across eight areas (see `research/01_literature/`), then a preliminary Stage 3-4 ideation and challenge round (see `research/02_candidate_ideas.md`).

---

## Stage 3-5 completion on the author's local machine (2026-10-05)

### Environment change (verified by direct probes on 2026-10-05)

This session ran on the author's local Windows 11 PC, not the earlier cloud container. The repository was cloned from GitHub (branch `claude/peaceful-cori-ny59q5`, 20 commits at start) into `E:\research 2`.

| Capability | Status now | Evidence |
|---|---|---|
| Compute | Intel i7-14700KF (20 cores / 28 threads), 31.9 GB RAM, NVIDIA GeForce RTX 5070 Ti with 16 GB VRAM, 626 GB free on drive E:, Python 3.14.4, Node 24 | PowerShell CIM queries and `nvidia-smi` |
| GitHub push | Works (`gh` authenticated as the repository owner) | `git push --dry-run` succeeded; later pushes succeeded |
| arXiv, export.arxiv.org API, Crossref API, OpenAlex API, Hugging Face API, Zenodo API, dblp API, OSF API, AIS eLibrary, ACL Anthology, Springer (abstracts), FAccT site | Reachable (HTTP 200/303) | curl probes |
| Semantic Scholar API | HTTP 429 on every call all day (shared rate budget) | curl probes and all agent reports |
| export.arxiv.org | Answered 429 for long stretches while eleven agents queried it in parallel; recovered afterwards | second verification run succeeded |
| doi.org | 403 to curl (use `api.crossref.org/works/<DOI>` instead) | curl probe |
| dblp HTML, OpenReview API | Bot-check page / 403 | agent reports |
| ACM DL, ScienceDirect, IEEE Xplore, Wiley, INFORMS, Taylor & Francis, MISQ site, SSRN, nyc.gov DCWP pages | Refuse automated fetches (unchanged) | curl probes and agent reports |
| Paid LLM APIs, participants, institutional library access | Still unavailable | unchanged author constraints |

Consequence: the "no GPU" assumption behind the 2026-10-03 feasibility checks for ideas 1-3 no longer holds. The checks for ideas 4-8 therefore assess two scenarios, A (the old 4-vCPU, 15 GB, no-GPU container, kept for comparability) and B (this machine). Ideas 1-3 have not been re-assessed under scenario B; their files say what GPU class would unblock them.

### What was completed

- **Stage 4 challenge round finished.** Novelty and feasibility checks written for ideas 4-8 (ten files in `03_challenge/`, 36-72 KB each, same structure as the files for ideas 1-3). Each novelty check ran 42-61 queries across WebSearch, the arXiv API, Crossref, dblp and (when it answered) Semantic Scholar, read 11-32 abstracts and one to four full texts, and ends with a reference-verification table. Verdicts: all five novelty checks "partially-covered" (idea 7 "close to largely-covered"; idea 8 Part A "leaning largely-covered on the construct"); feasibility "feasible-now" for ideas 4, 5 and 7; "feasible-now" for the restricted design of idea 6 (Springer open-access IS journals plus ACL industry tracks) while the as-written ICIS/ECIS stratum "needs-external-resources" (AIS eLibrary access and a second coder); idea 8 "feasible-but-slow-on-cpu" under scenario A and "feasible-now" under scenario B with the joint paper split into companions.
- **Material corrections to the idea cards surfaced by the checks** (the Stage 3 JSON is left as the historical record; the corrections are stated in `02_candidate_ideas.md`): Gerchick et al. (FAccT 2025) already attach missing-data uncertainty bounds to published LL 144 ratios and released a 116-audit dataset with per-group counts on GitHub, and two SSRN papers report LL 144 hiring outcomes (idea 4); Pika et al. 2017 contains no stability analysis, but the construct of idea 5 is a transfer of provider-profiling reliability, value-added stability and composite-indicator sensitivity methods (idea 5); Christodoulou et al. 2025 already perform a claim-survival re-analysis in medical imaging and Yang et al. 2026 find judge validation in under 8% of NLG papers (idea 6); Kadasi et al. (ICWSM 2025) already compared card-reported scores with re-evaluation of 500 models and Evaluation Cards (2026) computes cross-party divergence at scale (idea 7); Marie and Fujita 2025, Soualhi 2026 and Thomas 2026 already study low-bit quantization on 1.7-4B models across scripts (idea 8).
- **Stage 4 synthesis written**: `02_candidate_ideas.md` (about 100 KB) with the comparison table, eight idea cards carrying prior art, blockers and resolved/open undermining checks, recommendations, Stage 4 plans with stopping rules, author decisions, dropped ideas, provenance and an appendix of card-versus-check inconsistencies.
- **Stage 5 venue landscape written**: `04_journals/venue_landscape.md` (18 venues; the AIS Senior Scholars' list of premier journals confirmed from the official announcement; ICORE 2026 conference ranks; fit matrix for ideas 1-8; cost routes; what top IS journals require; seven open questions; 93-row search log). No-fee routes seen: JMIS, JAIS and CAIS (USD 75 without an AIS-member author), BISE and ISF (Springer subscription route), TMLR, Elsevier journals (subscription alternative), EJIS (green self-archiving).
- **Full citation verification pass over the eight literature files**: a new identifier-based tool (`tools/verify_evidence_tables.py`) resolved every DOI and arXiv id in the evidence tables (298 rows, 267 with an identifier, 55 flagged); a reconciliation pass checked all 55 flagged rows and the 31 rows without identifiers, made 20 minimal citation edits (published versions added for rows labelled preprint, OpenReview and Semantic Scholar sources added for ICLR/ICML rows that rested on arXiv ids, DOIs and author lists completed, one wrong Crossref suggestion explicitly rejected), judged 38 flags benign, and left 9 items for a human. Report and decision table: `01_literature/verification_pass_2026-10-05.md`.
- `README.md` index updated; a completeness and integrity critique over all records is recorded in `05_critique_2026-10-05.md`.

### What remains uncertain

- Semantic Scholar was unusable all day, dblp was behind a bot check and the WebSearch budget ran out in every novelty check, so each check names the specific sweeps it could not run (ICPM/BPM proceedings for idea 5; a direct AIS eLibrary search for idea 6; FAccT 2025-2026 coverage beyond Crossref title filtering for idea 7; Indonesian and Swahili quantized-LLM evaluations for idea 8).
- No idea reached "likely-novel-within-search-limits"; every retained idea is a field transfer, protocol increment or rule-specific extension and must be positioned as such.
- The local software stack for GPU work (Python 3.14 with CUDA-enabled torch, a Blackwell-capable llama.cpp build) was not verified.

### Decision

**Proceed** to Stage 4 deep checks and pilots on the three recommended candidates: idea 6 (error-bar audit of LLM evaluations in IS and industry-track venues; IS-framed primary for the top-journal goal, JAIS/BISE/CAIS fit), idea 5 (robustness of log-derived worker rankings; IS-framed co-primary that can start today, BISE fit) and idea 4 (sampling uncertainty and exclusion rules in LL 144 impact ratios; quickest complete paper, FAccT fit with an IS secondary route). Ideas 7 and 8 (joint) and 1-3 are deprioritized for the reasons in `02_candidate_ideas.md` section 6; idea 3 and idea 8 Part B are reserves. No primary project is selected: that choice belongs to the author (see section 5 of the synthesis).

### Next action

The author answers the decision items in `02_candidate_ideas.md` section 5 (CS versus IS framing; preference among ideas 6, 5 and 4; willingness to recruit a second coder and to obtain AIS eLibrary access; APC tolerance for FAccT or JRC; multi-day local compute; a Python 3.12 or WSL2 environment for GPU work). Then Stage 4 deep checks follow the per-idea plans in section 4 of the synthesis (named full texts to read first, backward and forward citation chasing once Semantic Scholar answers, the first pilot with its stopping rule), after which Stage 6 (protocol and preregistration) begins for the selected primary.

---

## Stage 4 deep checks and pilots (2026-10-19)

**Environment.** This session ran in the cloud container, not the author's Windows PC:
- 4 vCPU, 15 GB RAM, about 30 GB free disk, no GPU;
- Python 3.11.15 venv in the session scratchpad: pm4py 2.7.23.8, pandas 3.0.6, numpy 2.4.6, scipy 1.17.1, scikit-learn 1.9.1, statsmodels 0.15.0;
- no paid APIs and no API keys.

OpenAlex refused every list query all day because the anonymous daily budget for the shared IP was exhausted. Semantic Scholar returned HTTP 429 on keyword search and some legs. dblp showed a bot wall. The AIS eLibrary search returned 403 and its PDFs sit behind Cloudflare and a subscription. Publisher sites still refuse.

Commits: a background autosave loop (`autosave.sh` in the scratchpad, every 180 s) committed and pushed `research/` throughout. No agent ran `git commit` itself.

### What was completed

- **Idea 6.** The sampling frame was frozen and an exploratory pilot run (`research/06_stage4/idea06/`):
  - frame: 3,543 articles from 11 IS journals, a Springer-OA stratum of 65, and 777 ACL industry-track papers;
  - inclusion screening of the 65 Springer-OA papers;
  - a seeded 20-paper pilot, coded by a machine coder (Claude) against `codebook_v0.md`;
  - a validated survival calculator run on 10 claims.

  The deep novelty check:
  - read 12 documents, 10 at full-text depth;
  - crawled 4,564 AIS proceedings titles;
  - enumerated 8,490 Crossref records from 17 IS journals and HICSS;
  - ran Semantic Scholar forward chasing of four seeds.
- **Idea 5.** An exploratory pilot on BPI 2017 and BPI 2019 (`research/06_stage4/idea05/`):
  - the full 405-cell factorial (117 distinct score vectors);
  - 500 case-bootstrap replicates and 20 placebo shuffles;
  - system-account sensitivity;
  - an automated-account detector calibrated on BPI 2019's labels.

  The deep novelty check:
  - read 14 documents, 10 at full-text depth, including the 4TU General Terms of Use;
  - enumerated 1,360 ICPM, BPM, CAiSE and Process Science papers from 2022-2026 via Crossref (dblp was blocked);
  - screened 38 BPI Challenge reports and read 86 ICIS future-of-work titles;
  - ran Semantic Scholar forward chasing of five seeds and Crossref backward chasing of one.
- **Idea 4.** An exploratory Part 1 pilot on the ACLU `audits_full.csv` (`research/06_stage4/idea04/`):
  - de-duplication, consistency filter and comparator recomputation;
  - four interval methods on 1,157 usable ratios;
  - UGESP-style classification;
  - excluded-population shares;
  - a 20-row OSF cross-check;
  - post hoc data-scope coding from report text.

  The deep novelty check:
  - read 18 documents, 9 at full-text depth;
  - screened the FAccT 2026, AIES 2026 and FAccT 2025 tables of contents (807 papers);
  - ran Semantic Scholar forward chasing of eight seeds (the Lam et al. leg was not done).

  Parts 2 and 3 were not run.
- **Synthesis:** `research/06_stage4/README.md`. It covers the stopping-rule tables, the recommendations, the author decisions, the Stage 6 plan for the recommended primary and the integrity items.

### What evidence was found

All pilots are exploratory and nothing is confirmatory. Stopping rules were applied exactly as written in `02_candidate_ideas.md` section 4.

- **Idea 6. Rule triggered.**
  - Criterion 2 holds under the pre-specified primary readings:
    - 3 of 20 pilot papers (15%) permit RQ2, against a threshold below 30%;
    - the Springer-OA stratum has 14 empirical papers after screening, against a threshold below 25.
  - The literature criterion is not triggered: no IS-venue audit of statistical or judge-validation practice in LLM papers was found.
  - Criterion 3 (second coder and AIS access) is undetermined.
  - The outcome depends on the reading: under the pre-specified secondary reading, 2a is 35%.
  - 9 of the 10 drawn Springer papers failed inclusion.
  - Novelty is still partially-covered, but narrower than before:
    - Pathade et al. (arXiv 2609.25173) code uncertainty, repeated runs, decoding and judge-human agreement together;
    - Singh (arXiv 2608.15046) audits the evidential sufficiency of 17 LLM claims;
    - the DKFZ "Claims Reloaded" estimator overlaps the planned calculator;
    - Yang et al.'s judge-validation comparator is 37.4% among judge papers, not "under 8%".
- **Idea 5. Rule not triggered.**
  - The median Kendall tau across configurations is 0.033 on BPI 2017 [0.017, 0.050] and 0.041 on BPI 2019 [0.032, 0.047], against a stop threshold above 0.9.
  - Bottom-quintile reclassification under case-mix adjustment is 17.9% and 27.3%, against a stop threshold below 10%. Under the all-workers reading it is 7.1% and 9.4%.
  - The proceedings sweep found no rank-stability study of resource measures on public logs.
  - The all-pairs median is at placebo level. Within-metric agreement (0.488 and 0.503) exceeds all 20 placebo values.
  - The metric factor carries 54% and 57% of rank-percentile variance.
  - Attribution alone gives near-independent rankings: tau 0.021 on BPI 2017.
  - The pre-specified detector failed: per-account precision 0.087.
  - Novelty is still partially-covered, with a design precedent in physician cost profiling: Thomas and Ward 2006; Mehrotra et al. 2010; Timbie et al. 2013; Kaye et al. 2019. Rhea et al. 2022 offer a stability-audit framework for HR tools.
- **Idea 4. Rule not triggered.**
  - The ACLU code computes only deterministic missing-data bounds.
  - 59.8% of the 854 employer-posted ratios have a Katz interval excluding 0.8, against a stop threshold above about 80%.
  - No I-O or FAccT paper simulates the LL 144 levers on the published corpus.
  - 662 of the 854 employer-posted ratios come from multi-employer pooled tables, where binomial intervals are not valid.
  - In employer-own-data audits, informativeness is bimodal by group size: 4.7% of ratios exclude 0.8 below 100 applicants, and 91.7% do at 1,000-4,999.
  - 82% of selected counts are reconstructed from rounded rates.
  - Novelty is still partially-covered:
    - Bommasani et al. (FAccT 2026) show on real data that pooling masks position-level adverse impact;
    - the reporting designs are long-standing I-O practice (TAC 2010);
    - a vendor blog published a point-estimate reanalysis of the same file on 2026-10-16.

### What remains uncertain

- **Idea 6.**
  - The pilot was machine-coded with no human verification, so no kappa exists.
  - The rule outcome depends on the reading of "permit RQ2" and on drawing from unscreened term hits.
  - AIS full texts and the AMCIS 2025 full text are unread.
- **Idea 5.**
  - Which estimand should headline the paper.
  - Whether the results hold on other logs. BPI 2017 and 2019 are now pilot data.
  - A working automated-account detector.
  - Literature residual risk: 85% of the sweep was screened at title level only.
  - The AI Act timing (snippet only).
- **Idea 4.**
  - The licence of `audits_full.csv`.
  - Whether any confirmatory population other than employer-own data can carry intervals.
  - Parts 2 and 3 are unrun.
  - The JetBlue and Citizens reports are unread.
- **All ideas.**
  - OpenAlex forward legs are not done for any seed; several Semantic Scholar legs are not done.
  - Publisher full texts (APA, Wiley, Taylor & Francis, SSRN) are unread.
  - Several items are known from snippets only.
- **Integrity.**
  - The repository owner's personal e-mail address was sent to Crossref, OpenAlex and Semantic Scholar by two idea-6 novelty scripts. It is recorded in two committed logs, which reverses the 2026-10-05 placeholder fix.
  - The autosave loop pushed intermediate file versions.

  See `research/06_stage4/README.md` section 6.

  An integrity critic pass later on 2026-10-19 made small wording and consistency edits to the Stage 4 files. It changed no result file and no code. Its edits and checks are listed in `research/06_stage4/README.md` section 8.

### Decision

These are recommendations, pending the author's confirmation; no primary project is selected without the author.

- **Idea 5: revise**, then proceed to Stage 6 as the recommended primary. Its rule was not triggered on either clause, it needs no participants or fees, and the pilot found structure beyond "metrics are unstable".
- **Idea 4: revise.** It is the recommended backup or parallel secondary paper, after the ACLU licence answer.
- **Idea 6: pivot.** Its rule was triggered; under the rule this means stop the JAIS-targeted audit, or demote it to a CAIS methods essay. It is not recommended as primary or backup.

### Next action

1. The author answers the decisions in `research/06_stage4/README.md` section 4:
   - confirm the primary and backup and decide idea 6's disposition;
   - discipline and tier, APC and preregistration;
   - send the ACLU licence email;
   - the idea-5 estimand and data-handling rule;
   - the e-mail scrub and history decision;
   - API keys.
2. Stage 6 for idea 5 follows section 5 of that file:
   - protocol work P1-P5;
   - the OSF preregistration;
   - the full run on about 16 further logs.

   Compute extrapolated from the pilot timings is about 1.7-3.8 h at pilot settings, or up to about 21-28 h with per-replicate refits, on 4 vCPU.

---
