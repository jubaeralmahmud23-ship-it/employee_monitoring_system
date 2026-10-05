# Research records

Persistent, auditable records for the research collaboration (CS / AI / business information systems).

| Path | Purpose |
|---|---|
| `00_PROJECT_LOG.md` | Stage-by-stage log: completed work, evidence, uncertainties, decisions, next actions. Start here. |
| `RESUME.md` | What a new session needs to continue without repeating work (state table, open tasks, how to continue). |
| `01_literature/<area>.md` | One file per literature area (eight areas): search log, inclusion/exclusion criteria, evidence table, synthesis, candidate gaps, datasets, limitations, API verification, citation audit. |
| `01_literature/digest.json` | Machine-readable digest of the eight areas (gaps, contradictions, key papers, datasets). |
| `01_literature/verification_pass_2026-10-05.md` | Identifier-based verification of every evidence-table row (DOI via Crossref, arXiv id via the arXiv API) with the flags that need a human check. |
| `02_candidate_ideas_merged.json` | The eight merged candidate idea cards (Stage 3). |
| `02_candidate_ideas.md` | Stage 3-4 synthesis: comparison table, full idea cards with prior art and blockers, recommendations, decisions for the author, dropped ideas. |
| `03_challenge/<idea>__novelty.md` | Adversarial prior-art search per idea (search log, comparison table, verdict, search limits, reference verification). |
| `03_challenge/<idea>__feasibility.md` | Data, compute (CPU-only container and local GPU machine), approval and claim-support assessment per idea. |
| `04_journals/venue_landscape.md` | Stage 5: 18 journals and conferences with scope, fees, no-fee routes, rankings seen, fit matrix for ideas 1-8, requirements of top IS journals, open questions. |
| `05_critique_2026-10-05.md` | Completeness and integrity critique over all records (files read, issues fixed, issues left open, verdict). |
| `tools/verify_refs.py` | Title-based check of references against Crossref, OpenAlex, arXiv and Semantic Scholar. |
| `tools/verify_evidence_tables.py` | Identifier-based check of evidence-table rows (DOI and arXiv id) with year, venue and status flags. |
| `tools/workflow_*.js`, `tools/*_args.json` | The multi-agent workflow scripts that produced Stages 1-4 on 2026-10-03 (kept for provenance; paths inside refer to the earlier cloud container). |

Conventions:

- Every claim about a paper records its access depth (full-text, abstract, or metadata/snippet). Stage 0 ran with search-snippet access only; from the network widening on 2026-10-03 onward, records reach abstract depth broadly and full-text depth for open-access papers, and DOIs are verified against Crossref and arXiv. Publisher sites that refuse automated fetches (ACM DL, ScienceDirect, IEEE Xplore, Wiley, INFORMS, Taylor & Francis, SSRN) are covered through Crossref metadata and search snippets only.
- Nothing here is described as a systematic review. No screening counts or flow diagrams are reported.
- No experiment is reported as run unless its code, inputs, logs and outputs are in this repository. Timing benchmarks quoted in feasibility files (for example a 1.3 s Part 1 run for idea 4) are scratch measurements made during assessment, not study results.
- Dates in file names and headings are the dates the work was performed.
