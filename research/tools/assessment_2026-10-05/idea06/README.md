# Assessment scripts for idea 6 (run 2026-10-05)

Scratch scripts used during the feasibility assessment in `research/03_challenge/06-would-the-claim-survive-an-error-bar-auditing-st__feasibility.md` to enumerate the sampling frame. Kept so the counts in that file can be reproduced; they are assessment tooling, not study code.

| File | What it does | Output kept |
|---|---|---|
| `crossref_counts.py` | Counts 2023+ research articles per IS journal (by ISSN) in Crossref and the subset with "language model" / LLM / generative AI / ChatGPT terms in title or abstract; reports Creative-Commons licence shares | `crossref_counts.json`, `crossref_recount_scp.json` (recount after stripping `<scp>` markup from Wiley abstracts) |
| `aisel_crawl.py` | Counts papers per ICIS/ECIS proceedings year on the AIS eLibrary track pages and the subset with LLM terms in titles | `aisel_counts.json` |

Crossref abstracts are missing for most Elsevier and Taylor & Francis records, so the term counts for those journals are title-only (see the feasibility file, section 1). The Crossref contact address was replaced with a placeholder before committing; set `MAILTO` to your own address to use the polite pool.
