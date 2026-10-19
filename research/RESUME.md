# Resume instructions for the next session

Written 2026-10-03 because the author's usage allowance was about to end. Everything below is what a new session needs to continue without repeating work. **The 2026-10-03 text is kept as written; the "Update 2026-10-05" section near the end states the current state and supersedes the state table, the "No GPU" line and the "Known blockers" section where they differ.** **The "Update 2026-10-19" section at the very end is the latest state. It supersedes both earlier sections where they differ.**

## State at hand-off

| Stage | Status | Where |
|---|---|---|
| 0 Environment and author answers | Done | `00_PROJECT_LOG.md` |
| 1-2 Literature landscape, 8 areas, audited | Done | `01_literature/*.md`, machine-readable digest in `01_literature/digest.json` |
| 3 Candidate ideas (4 lenses, merged to 8) | Done | `02_candidate_ideas_merged.json` |
| 4 Adversarial novelty + feasibility checks per idea | **In progress / possibly incomplete** | `03_challenge/<idea>__novelty.md` and `__feasibility.md`; whichever files exist were completed |
| 4 Synthesis (`02_candidate_ideas.md`) and completeness critique | Not done unless the file exists | `02_candidate_ideas.md` |
| 5 Journal landscape | Not started | planned `04_journals/` |
| 6+ Protocol, execution, manuscript | Not started | |

## Author decisions already recorded

- Network policy widened (arXiv, Crossref, OpenAlex, Semantic Scholar, Hugging Face, Zenodo, 4TU reachable). Re-probe in a new session; the policy belongs to the environment, not the session.
- Repository name is unrelated to the topic. No topic preference.
- Goal: a top journal. Discipline (CS vs IS) still open.
- No GPU, no API credits, no institutional access, no organizational data, no participants. (The "no GPU" part was superseded on 2026-10-05: the author's local PC has an RTX 5070 Ti with 16 GB VRAM; see the update below. The other constraints are unchanged.)
- APC only if the manuscript is very strong; otherwise the no-fee route.

## Known blockers

- **GitHub push works since 12:41 UTC on 2026-10-03** (access granted by the author). The remote branch `claude/peaceful-cori-ny59q5` is the durable copy. A git bundle and tarball sent in the chat before that are a redundant backup; if ever needed, restore with `git clone -b claude/peaceful-cori-ny59q5 research-records.bundle employee_monitoring_system`.
- Workflow journals live outside the repository and do not survive the session; the scripts that reproduce the stages are saved in `tools/`.

## How to continue

1. Start the new session on branch `claude/peaceful-cori-ny59q5` of the GitHub repository; it holds all records. Confirm `research/03_challenge/` contents against the table above.
2. Re-probe network access (`curl -sI https://arxiv.org/`), run `python3 research/tools/verify_refs.py --self-test`.
3. List `03_challenge/`. For each of the 8 ideas in `02_candidate_ideas_merged.json`, an idea is done when both `NN-...__novelty.md` and `NN-...__feasibility.md` exist. Re-run only the missing ones: edit `tools/workflow_stage34_continuation_args.json` to keep only the missing titles (keep their original order so slugs stay stable, or accept new numbering), then run the Workflow tool with `scriptPath` = `tools/workflow_stage34_continuation.js` and the JSON as `args`. The script reads ideas by index into the merged JSON, so if you subset the titles you must also pass matching indices; simplest is to re-run all eight if usage allows.
4. When all 16 files exist, run the synthesis and critic stages (the last part of the continuation script), or ask the session to write `02_candidate_ideas.md` from the challenge files directly.
5. Then: author picks 1-2 primary candidates; Stage 4 deep novelty check (backward and forward citation chasing on the closest prior art), Stage 5 journal landscape, Stage 6 protocol.

## Open task list at hand-off

- Stage 3-4 challenge and synthesis (in progress).
- Full citation verification pass over all records with `tools/verify_refs.py`, reconciling year/venue/DOI mismatches.
- Stage 5 journal landscape for 3-5 top IS and CS venues from official pages.
- Push to GitHub once access is granted.

## Update 2026-10-05 (current state; supersedes the sections above where they differ)

Environment: this session ran on the author's local Windows 11 PC (Intel i7-14700KF, 20 cores / 28 threads, 31.9 GB RAM, NVIDIA RTX 5070 Ti 16 GB, 626 GB free, Python 3.14 with 3.12 also installed), not the 2026-10-03 cloud container. The working copy is `E:\research 2` (contains a `.git` directory; branch and sync state with `claude/peaceful-cori-ny59q5` should be re-checked with `git status` at the start of the next session). Details and probes: `00_PROJECT_LOG.md`, entry "Stage 3-5 completion on the author's local machine (2026-10-05)".

State at hand-off (2026-10-05):

| Stage | Status | Where |
|---|---|---|
| 4 Adversarial novelty + feasibility checks, ideas 1-8 | Done (ideas 1-3 on 2026-10-03 under the no-GPU container; ideas 4-8 on 2026-10-05 under scenarios A and B) | `03_challenge/` (16 files) |
| 4 Synthesis and critique | Done | `02_candidate_ideas.md`; `05_critique_2026-10-05.md` |
| 5 Journal landscape | Done (18 venues) | `04_journals/venue_landscape.md` |
| Citation verification | Done (identifier-based pass over all eight area files; 9 items left for a human) | `01_literature/verification_pass_2026-10-05.md` |
| 6+ Protocol, execution, manuscript | Not started; waits on the author's decisions in `02_candidate_ideas.md` section 5 | |

Current blockers and limits (2026-10-05):

- Semantic Scholar API: HTTP 429 on every call all day; dblp: bot-check page; OpenReview API: 403; doi.org: 403 to curl (use `api.crossref.org/works/<DOI>`); export.arxiv.org rate-limits under parallel load. A free Semantic Scholar API key would remove the first limit.
- Publisher sites still refuse automated fetches (ACM DL, ScienceDirect, IEEE Xplore, Wiley, INFORMS, Taylor & Francis, MISQ site, SSRN, nyc.gov, perma.cc); AIS eLibrary PDFs sit behind a subscription login (abstracts are readable); Kaggle downloads need an account token. These items are read through Crossref, arXiv and snippets only.
- The WebSearch budget (200 calls per session) ran out in every 2026-10-05 novelty check; the sweeps each check could not run are named in its "Search limits" section.
- GPU software stack unverified: the local torch is a CPU build; a CUDA (cu130) wheel for Python 3.14 exists but Blackwell (sm_120) operation is untested; CMake, MSVC and nvcc are absent; vLLM is not Windows-native. Ideas 1-3 have not been re-assessed under the GPU scenario.
- Unchanged author constraints: no paid LLM APIs, no participants, no institutional library access, no organizational data; APC only if the manuscript is very strong.
- GitHub push works (see the project log, 2026-10-03 12:41 UTC and 2026-10-05 entries); the earlier "push refused" statements in this file and in the log are historical.

How to continue (2026-10-05): the author answers the decision items in `02_candidate_ideas.md` section 5; then the Stage 4 deep-check plans in section 4 (ideas 6, 5 and 4) run, starting with the named full texts and the pilots with their stopping rules; the nine human-check items in `verification_pass_2026-10-05.md` ("Rows that still need a human decision") and the open items in `05_critique_2026-10-05.md` should be cleared in the same session.

## Update 2026-10-19 (latest state; supersedes the sections above where they differ)

### Environment of this session

This session ran in the cloud container, not on the author's Windows PC:
- 4 vCPU (Intel Xeon @ 2.10 GHz), 15 GB RAM, about 30 GB free disk, no GPU;
- Python 3.11.15 venv at `/tmp/claude-0/-home-user-employee-monitoring-system/c64eab22-9c10-592c-b92e-5ac629c5be82/scratchpad/venv`, holding pm4py 2.7.23.8, pandas 3.0.6, numpy 2.4.6, scipy 1.17.1, scikit-learn 1.9.1, statsmodels 0.15.0 and pyarrow 26.0.0;
- pdftotext 24.02.0 and curl 8.5.0;
- no paid APIs and no API keys.

Some things do not survive the container:
- Raw data and row-level derived files are in the scratchpad (`data/idea04`, `data/idea05`, `data/idea06`, and the `*_novelty` directories). They are outside the repository and are lost when the container ends.
- A background autosave loop (`autosave.sh` in the scratchpad) commits and pushes `research/` every 180 s. It also stops with the container.

Repository state: branch `claude/peaceful-cori-ny59q5`, HEAD `d5507c7` at 06:59:51 UTC.

### State table (2026-10-19)

| Stage | Status | Where |
|---|---|---|
| 4 Deep novelty checks and pilots, ideas 6, 5 and 4 | **Done 2026-10-19. Exploratory only, not confirmatory.** Stopping-rule outcomes: idea 6 **triggered** (pilot criterion 2; criterion 3 undetermined); ideas 5 and 4 **not triggered** on any clause. All three novelty verdicts stay "partially-covered", each narrower than before. | `06_stage4/README.md` (synthesis); `06_stage4/idea0{4,5,6}/README.md` (pilots) and `novelty_deep_check.md` (literature); `00_PROJECT_LOG.md` entry "Stage 4 deep checks and pilots (2026-10-19)" |
| 6 Protocol, preregistration, full run | **Not started.** The recommended primary is idea 5 (revised), with idea 4 (revised) as backup and idea 6 as pivot. This is a recommendation; it waits on the author's confirmation and the decisions in `06_stage4/README.md` section 4. | Plan: `06_stage4/README.md` section 5 |

### Blockers and limits (2026-10-19)

- **OpenAlex.** List queries returned HTTP 429 all day, because the anonymous daily budget for the shared IP was exhausted. Semantic Scholar keyword search and some citation legs also returned 429. Free API keys would help, but each needs an e-mail address and therefore the author's consent.
- **Blocked sites.**
  - dblp shows a bot wall on all hosts.
  - The AIS eLibrary search endpoint returns 403, and its PDFs are behind Cloudflare and a subscription.
  - The ACM, Elsevier, Wiley, INFORMS, Taylor & Francis, APA, SAGE, OUP, SSRN and RAND sites refuse automated fetches.
- **Idea 4 licence.** The licence of the ACLU `audits_full.csv` is ambiguous. The author's email to analytics_inquiry@aclu.org has not been sent. Until it is answered, only aggregates may be published.
- **Idea 5 data terms.** The 4TU terms for BPI 2017 allow non-commercial remixing only (Art. 4b) and require publications to be reported to 4TU (Art. 3). Per-pseudonym rankings stay out of the repository until a data-handling rule is written. The pre-specified automated-account detector failed (precision 0.087).
- **Idea 6 coding.** There is no second coder and no AIS eLibrary access. The pilot codes come from a machine coder and are unverified.
- **E-mail exposure.** The repository owner's personal e-mail address is embedded in `06_stage4/idea06/code/chase_citations.py` and `crossref_is_sweep.py` and appears in two committed logs under `06_stage4/idea06/results/novelty/`. These files have already been pushed. Scrubbing them, and possibly rewriting history, is the author's call.

### How to continue

1. **Start on the right branch.** Use branch `claude/peaceful-cori-ny59q5` and run `git status`. In a new container the autosave loop is not running, so commit by hand or restart it deliberately.
2. **Read the Stage 4 synthesis.** Read `06_stage4/README.md`, sections 3 to 6. The author answers section 4 there:
   - primary and backup, and what happens to idea 6;
   - discipline and tier, APC and preregistration;
   - the ACLU licence email;
   - the idea-5 estimand and data-handling rule;
   - the e-mail scrub;
   - API keys.
3. **Re-create the environment if the pilots must be re-run.**
   - Create a Python venv with the versions above.
   - Download BPI 2017 (4TU DOI 10.4121/uuid:5f3067df-f10b-45da-b98b-86ae4c7a310b) and BPI 2019 (4TU article 12715853), and check them against the sha256 values in `06_stage4/idea05/README.md` §2.
   - Clone the two ACLU repositories at the commits in `06_stage4/idea04/README.md` §2.
4. **Re-run the pilots** with these entry points:

   | Idea | Command | Runtime |
   |---|---|---|
   | 5 | `PY=<venv>/bin/python bash research/06_stage4/idea05/code/run.sh <data_dir> 4 500 20` | about 21 min on 4 vCPU |
   | 4 | `bash research/06_stage4/idea04/code/run.sh` | about 55 s |
   | 6 | `bash research/06_stage4/idea06/code/run.sh` | about 3 s offline; `FETCH=1` re-queries the network |

5. **Stage 6 for the confirmed primary.** If idea 5 is confirmed, follow `06_stage4/README.md` section 5:
   - protocol work P1-P5: data-handling rule, further logs, new detector, reliability and rank intervals, Gu-Koenker comparator, workload covariate, per-replicate refits, an extra null;
   - an OSF preregistration that treats BPI 2017 and 2019 as pilot logs;
   - the full run on about 16 further logs.
6. **Integrity debt.** The open items are listed in `06_stage4/README.md` section 6. They include the nine human-check citation items of 2026-10-05, the idea-2 and idea-3 reference verifications, the snippet-only items, and the missing `06_stage4/` row in `research/README.md`.
