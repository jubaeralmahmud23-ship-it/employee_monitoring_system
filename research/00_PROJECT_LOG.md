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

### Decision

**Proceed** to the preliminary literature landscape using web search, with every record marked as snippet-level evidence, and in parallel generate and adversarially challenge candidate ideas. No project selection yet.

### Next action

Run the Stage 1-2 landscape sweep across eight areas (see `research/01_literature/`), then a preliminary Stage 3-4 ideation and challenge round (see `research/02_candidate_ideas.md`).

---
