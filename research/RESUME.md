# Resume instructions for the next session

Written 2026-10-03 because the author's usage allowance was about to end. Everything below is what a new session needs to continue without repeating work.

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
- No GPU, no API credits, no institutional access, no organizational data, no participants.
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
