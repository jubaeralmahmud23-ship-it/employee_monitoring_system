# Resume instructions for the next session

Written 2026-10-03 because the author's usage allowance was about to end. Everything below is what a new session needs to continue without repeating work. **The 2026-10-03 text is kept as written; the "Update 2026-10-05" section near the end states the current state and supersedes the state table, the "No GPU" line and the "Known blockers" section where they differ.**

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
