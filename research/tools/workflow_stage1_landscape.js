export const meta = {
  name: 'research-landscape-stage1',
  description: 'Literature landscape sweep across 8 areas with citation audit, four-lens idea generation, adversarial novelty and feasibility challenge, and synthesis',
  phases: [
    { title: 'Landscape', detail: 'one web-search agent per research area; writes evidence table + search log' },
    { title: 'Audit', detail: 'independent citation existence check per area file' },
    { title: 'Ideate', detail: 'four lenses propose candidate ideas, then merge to 6-8' },
    { title: 'Challenge', detail: 'adversarial novelty search and feasibility check per idea' },
    { title: 'Synthesize', detail: 'comparative evaluation, recommendations, completeness critique' },
  ],
}

const ROOT = '/home/user/employee_monitoring_system/research'
const LIT = ROOT + '/01_literature'
const CHAL = ROOT + '/03_challenge'
const TODAY = '2026-10-03'

const ENV = [
  'ENVIRONMENT FACTS (verified ' + TODAY + ', after the author widened the network policy):',
  '- Tools: WebSearch (load with ToolSearch "select:WebSearch" if absent; supports allowed_domains and mode "standard"/"extended"), WebFetch (load with "select:WebFetch"), Bash with curl and python3.',
  '- Reachable and useful: arxiv.org (abstract pages /abs/ID, HTML full text at /html/ID for recent papers, PDFs), export.arxiv.org API, api.crossref.org (DOI metadata), api.semanticscholar.org/graph/v1 (paper search, references, citations; no key; back off on 429), api.openalex.org (rate-limited, use sparingly), doi.org, aisel.aisnet.org (AIS eLibrary: IS journals and ICIS/ECIS/HICSS proceedings, abstracts readable), openreview.net, aclanthology.org, proceedings.neurips.cc, proceedings.mlr.press, link.springer.com (abstracts), dblp.org, semanticscholar.org, huggingface.co (models and datasets; a 91 MB model downloaded in 3 s), zenodo.org (API works), data.4tu.nl (BPI Challenge event logs), archive.ics.uci.edu, openml.org, data.gov, eur-lex.europa.eu, archive.org, dumps.wikimedia.org, osf.io, figshare.com, physionet.org, fred.stlouisfed.org, github.com.',
  '- Refuse plain fetches because of bot protection (use WebSearch snippets plus Crossref or Semantic Scholar metadata instead; do not retry repeatedly): dl.acm.org, sciencedirect.com, ieeexplore.ieee.org, onlinelibrary.wiley.com, pubsonline.informs.org, tandfonline.com, misq.umn.edu, papers.ssrn.com, sec.gov. Kaggle pages load but downloads need an account token we do not have. Do not clone or read any GitHub repository other than the working repository; GitHub-hosted data is confirmed via WebSearch only and must be added to the session before use.',
  '- Access-depth rules: mark a paper "full-text" only if you actually read its full text (arXiv HTML or PDF, or an open-access page); "abstract" if you read the abstract on arXiv, the AIS eLibrary, Springer, Crossref, or Semantic Scholar; otherwise "metadata/snippet". Never claim more than you read.',
  '- Reference verification: /home/user/employee_monitoring_system/research/tools/verify_refs.py (python3, standard library only) checks a file of titles, one per line, against Crossref, OpenAlex and arXiv and prints a markdown table with similarity scores. Scores below 0.85 need manual review; NeurIPS and ICLR papers are often absent from Crossref, so use the arXiv column for those. OpenAlex may answer 429; that is not an error in your work. Write temporary files under /tmp/claude-0/-home-user-employee-monitoring-system/c64eab22-9c10-592c-b92e-5ac629c5be82/scratchpad/.',
  '- Compute for later experiments: 4 CPU cores, 15 GB RAM, about 30 GB disk, Python 3.11, PyPI, Hugging Face downloads. No GPU, no paid LLM APIs, no API keys, no research participants, no institutional database access. Embedding models and small open generative models (roughly 1-4B parameters, quantized) run on CPU, slowly; large-scale LLM experiments are not feasible here.',
  'HONESTY RULES: Only list papers that appeared in results you actually received (search results, API responses, or fetched pages). Copy titles exactly as shown. Write "not shown" for metadata you could not see rather than guessing. Include a DOI only if Crossref, arXiv metadata, the publisher page, or a search result literally showed it. Never invent screening counts, never call the review systematic, never write "the first" or "no prior work" claims. Distinguish peer-reviewed venues from preprints and note when a preprint has a published version.',
].join('\n')

const AREAS = [
  { key: 'genai-organizations', title: 'Generative AI and LLM adoption, use, value and risk in organizations (IS perspective)',
    scope: 'Empirical and conceptual IS research on how organizations adopt and use generative AI: productivity effects, trust, delegation, appropriation, shadow AI, governance of use, affordances, worker experience. Include field experiments and surveys, and critiques.',
    venues: 'MIS Quarterly, Information Systems Research, Journal of MIS, EJIS, JAIS, Information & Management, BISE (Business & Information Systems Engineering), Decision Support Systems, IJIM, Computers in Human Behavior, ICIS/ECIS/HICSS proceedings, plus NBER/SSRN economics working papers on GenAI productivity.' },
  { key: 'rag-knowledge-management', title: 'Retrieval-augmented generation and enterprise knowledge management',
    scope: 'RAG architectures and evaluation for enterprise document QA and knowledge management: benchmarks, evaluation frameworks, failure modes, industry studies, cost and reliability, hybrid lexical/dense retrieval, long-context vs RAG, graph RAG, domain adaptation. Note which benchmarks/datasets are hosted on GitHub versus blocked hosts.',
    venues: 'ACL/EMNLP/NAACL, NeurIPS/ICLR/ICML, SIGIR/CIKM/ECIR, KDD, arXiv, Information Processing & Management, ACM TOIS, Expert Systems with Applications, Journal of Knowledge Management, IEEE Access (lower weight).' },
  { key: 'agents-bpm-process-mining', title: 'LLM agents for enterprise workflows, business process management, intelligent automation and process mining',
    scope: 'Agentic BPM, LLMs for process modeling and process mining tasks, predictive process monitoring, RPA + LLM, tool-using agents in enterprise workflows, reliability and evaluation of agents, agent benchmarks in business settings. Record which event logs and benchmarks exist and where they are hosted (4TU is blocked; GitHub is reachable).',
    venues: 'BPM conference and forum, ICPM, CAiSE, Information Systems (Elsevier), Decision Support Systems, BISE, Process Science, Software and Systems Modeling, arXiv, NeurIPS/ICLR agent benchmarks.' },
  { key: 'decision-support-analytics', title: 'LLM-based decision support and business analytics',
    scope: 'Text-to-SQL and natural-language BI assistants, LLMs over tabular and time-series business data, LLM forecasting claims and critiques, explainable analytics, decision quality and overreliance, human decision-making with AI advice. Record benchmark hosting.',
    venues: 'Decision Support Systems, European Journal of Operational Research, International Journal of Forecasting, VLDB/SIGMOD, ACL/EMNLP, KDD, Management Science, Information Systems Research, arXiv.' },
  { key: 'human-ai-algorithmic-management', title: 'Human-AI collaboration, algorithmic management and AI-enabled workplace/employee monitoring',
    scope: 'Algorithmic management, electronic performance monitoring and AI-based employee monitoring (productivity scoring, surveillance, bossware), worker trust, privacy, fairness, resistance, regulation (EU AI Act, GDPR), human-AI teaming and complementarity, AI advice-taking. Include critical and ethical perspectives and empirical measurement studies. This area is included because the author repository is named employee_monitoring_system.',
    venues: 'MIS Quarterly, ISR, JMIS, Information Systems Journal, Organization Science, Academy of Management Annals, CHI/CSCW, FAccT, Computers in Human Behavior, New Technology Work and Employment, Journal of Business Ethics, ICIS/ECIS.' },
  { key: 'governance-xai-fairness-compliance', title: 'Explainability, fairness, reliability, AI governance, auditing and regulatory compliance in enterprise AI',
    scope: 'AI governance frameworks in organizations, EU AI Act compliance operationalization, AI auditing and assurance, model cards and documentation practice, XAI in business use, fairness in HR/credit/operations decisions, accountability, responsible AI implementation gaps between principles and practice.',
    venues: 'FAccT, AIES, MIS Quarterly, JAIS, Information Systems Frontiers, Government Information Quarterly, Computer Law & Security Review, AI & Society, Business Horizons, Technological Forecasting and Social Change, arXiv.' },
  { key: 'evaluation-validity-safety', title: 'AI evaluation methodology and safety: LLM-as-judge validity, benchmark contamination, reproducibility, sycophancy and agent security',
    scope: 'Validity and bias of LLM-as-judge, meta-evaluation, benchmark contamination and data leakage, reproducibility of LLM research (version drift, nondeterminism), statistical practice in LLM evaluation, sycophancy and deception evals, prompt injection and security of tool-using agents, safety evaluation feasible at small scale. Record which human-judgment datasets or released model outputs are on GitHub.',
    venues: 'NeurIPS (Datasets and Benchmarks), ICLR, ACL/EMNLP, TMLR, Nature Machine Intelligence, Patterns, arXiv, USENIX Security, IEEE S&P, CCS.' },
  { key: 'efficiency-privacy-low-resource', title: 'Efficient and private AI for resource-constrained organizations and underserved languages',
    scope: 'Small and local models for SMEs and public-sector organizations, on-premise deployment, CPU inference, privacy-preserving LLM use, cost-performance trade-offs, low-resource language business NLP (e.g., Bangla, Swahili, Indonesian), AI adoption in developing economies, digital divide in GenAI, frugal AI.',
    venues: 'Information Technology for Development, Electronic Journal of Information Systems in Developing Countries, Information Systems Frontiers, ACL/EMNLP low-resource tracks, LREC-COLING, arXiv, Telematics and Informatics, Technology in Society.' },
]

const PAPER = { type: 'object', required: ['title', 'authors_short', 'year', 'venue', 'url', 'status', 'access_depth', 'finding', 'relevance'],
  properties: { title: { type: 'string' }, authors_short: { type: 'string' }, year: { type: 'string' }, venue: { type: 'string' }, url: { type: 'string' }, doi: { type: 'string' },
    status: { type: 'string', enum: ['peer-reviewed', 'preprint', 'other', 'unknown'] }, access_depth: { type: 'string', enum: ['full-text', 'abstract', 'metadata/snippet'] },
    finding: { type: 'string' }, relevance: { type: 'string' } } }
const DATASET = { type: 'object', required: ['name', 'host', 'url', 'reachable_now', 'license_note'],
  properties: { name: { type: 'string' }, host: { type: 'string' }, url: { type: 'string' }, reachable_now: { type: 'boolean' }, license_note: { type: 'string' }, what: { type: 'string' } } }
const LANDSCAPE_SCHEMA = { type: 'object', required: ['area', 'file', 'papers', 'gaps', 'contradictions', 'datasets', 'search_log_count', 'access_note'],
  properties: { area: { type: 'string' }, file: { type: 'string' }, papers: { type: 'array', items: PAPER }, gaps: { type: 'array', items: { type: 'string' } },
    contradictions: { type: 'array', items: { type: 'string' } }, datasets: { type: 'array', items: DATASET }, search_log_count: { type: 'integer' }, access_note: { type: 'string' } } }
const AUDIT_SCHEMA = { type: 'object', required: ['checked', 'confirmed', 'unconfirmed', 'notes'],
  properties: { checked: { type: 'integer' }, confirmed: { type: 'integer' },
    unconfirmed: { type: 'array', items: { type: 'object', required: ['title', 'issue'], properties: { title: { type: 'string' }, issue: { type: 'string' } } } }, notes: { type: 'string' } } }
const IDEA = { type: 'object', required: ['working_title', 'problem_rq', 'why_matters', 'contribution', 'closest_studies', 'difference', 'design', 'data_resources', 'risks', 'journal_audience', 'undermining_evidence', 'lens', 'runs_without_llm'],
  properties: { working_title: { type: 'string' }, problem_rq: { type: 'string' }, why_matters: { type: 'string' }, contribution: { type: 'string' },
    closest_studies: { type: 'array', items: { type: 'string' } }, difference: { type: 'string' }, design: { type: 'string' }, data_resources: { type: 'string' },
    risks: { type: 'string' }, journal_audience: { type: 'string' }, undermining_evidence: { type: 'string' }, lens: { type: 'string' }, runs_without_llm: { type: 'boolean' } } }
const IDEAS_SCHEMA = { type: 'object', required: ['ideas'], properties: { ideas: { type: 'array', items: IDEA }, notes: { type: 'string' } } }
const NOVELTY_SCHEMA = { type: 'object', required: ['idea_title', 'file', 'prior_art', 'verdict', 'differences', 'search_limits', 'query_count'],
  properties: { idea_title: { type: 'string' }, file: { type: 'string' },
    prior_art: { type: 'array', items: { type: 'object', required: ['title', 'url', 'year', 'how_close'], properties: { title: { type: 'string' }, url: { type: 'string' }, year: { type: 'string' }, how_close: { type: 'string' } } } },
    verdict: { type: 'string', enum: ['likely-novel-within-search-limits', 'partially-covered', 'largely-covered'] }, differences: { type: 'string' }, search_limits: { type: 'string' }, query_count: { type: 'integer' } } }
const FEAS_SCHEMA = { type: 'object', required: ['idea_title', 'file', 'data_options', 'compute_ok_cpu', 'needs_llm_or_embeddings', 'needs_participants', 'needs_approval', 'claim_supportable', 'blockers', 'verdict', 'notes'],
  properties: { idea_title: { type: 'string' }, file: { type: 'string' },
    data_options: { type: 'array', items: { type: 'object', required: ['name', 'url', 'host', 'reachable_now', 'license'], properties: { name: { type: 'string' }, url: { type: 'string' }, host: { type: 'string' }, reachable_now: { type: 'boolean' }, license: { type: 'string' } } } },
    compute_ok_cpu: { type: 'boolean' }, needs_llm_or_embeddings: { type: 'boolean' }, needs_participants: { type: 'boolean' }, needs_approval: { type: 'boolean' }, claim_supportable: { type: 'boolean' },
    blockers: { type: 'array', items: { type: 'string' } }, verdict: { type: 'string', enum: ['feasible-now', 'feasible-but-slow-on-cpu', 'needs-external-resources', 'infeasible'] }, notes: { type: 'string' } } }
const SYNTH_SCHEMA = { type: 'object', required: ['file', 'recommended', 'summary', 'overall_decision'],
  properties: { file: { type: 'string' }, recommended: { type: 'array', items: { type: 'string' } }, summary: { type: 'string' }, overall_decision: { type: 'string', enum: ['proceed', 'revise', 'pivot', 'stop'] } } }
const CRITIC_SCHEMA = { type: 'object', required: ['issues_fixed', 'issues_open', 'verdict'],
  properties: { issues_fixed: { type: 'array', items: { type: 'string' } }, issues_open: { type: 'array', items: { type: 'string' } }, verdict: { type: 'string' } } }

const landscapePrompt = (a) => [
  'You are one of eight literature scouts for a research project in computer science / AI / business information systems. Today is ' + TODAY + '.',
  ENV,
  'YOUR AREA: ' + a.title,
  'SCOPE: ' + a.scope,
  'VENUES TO TARGET: ' + a.venues,
  'TASK: Run at least 14 distinct WebSearch queries covering (1) foundational work, (2) recent 2025-2026 work (use mode "extended" for at least 3 recent queries), (3) surveys and literature reviews, (4) IS-journal venues named above (use allowed_domains such as ["aisel.aisnet.org"], ["pubsonline.informs.org"], ["sciencedirect.com"], ["link.springer.com"], ["onlinelibrary.wiley.com"], ["dl.acm.org"]), (5) CS venues (allowed_domains ["arxiv.org"], ["openreview.net"], ["aclanthology.org"], ["proceedings.neurips.cc"]), (6) critiques, negative results and replication failures, (7) datasets, benchmarks and public data for this area and where they are hosted, (8) backward and forward citation chasing for the 3 most central papers through the Semantic Scholar API (references and citations endpoints) or arXiv listings.',
  'Record 10 to 16 papers that matter most for finding research gaps. Prefer peer-reviewed venues; include preprints when central and label them. For every recorded paper try to read its abstract (arXiv abs page, AIS eLibrary, Springer, or the Semantic Scholar API with fields=title,abstract,venue,year,externalIds) so that most rows reach "abstract" depth; for the 3 most central papers read the full text when it is open access (arXiv HTML or PDF) and mark them "full-text". Record the depth you actually reached per row.',
  'Before writing the file, put the exact titles one per line in a scratch text file and run: python3 /home/user/employee_monitoring_system/research/tools/verify_refs.py <that file>. Use its table to correct year, venue, DOI and status in your evidence table; keep rows the APIs could not match but say so.',
  'Then WRITE a markdown file at ' + LIT + '/' + a.key + '.md (create the directory if needed) with these sections, in this order:',
  '1. "# Area: ' + a.title + '" with the date and a statement of the access depth actually achieved (how many rows are full-text, abstract, metadata/snippet).',
  '2. "## Search log" as a table with columns: # | date | tool/domain filter | exact query | mode | useful results (count) | note.',
  '3. "## Inclusion and exclusion criteria" (what you kept and dropped, honestly, e.g. vendor blogs excluded).',
  '4. "## Evidence table" as a markdown table with columns: Citation (authors short, year, venue, status) | Link | Research question / context | Method and theory | Data / participants / setting | Baselines and measures | Main findings (as visible) | Limitations (as visible or inferred, say which) | Relevance to gaps | Access depth.',
  '5. "## Synthesis" with subsections Agreements, Contradictions or tensions, Methodological weaknesses, Unresolved questions. Synthesize across papers; do not summarize one by one.',
  '6. "## Candidate research gaps" (3-6 bullets, each stating what evidence suggests the gap exists and what would disprove it).',
  '7. "## Datasets, benchmarks and public data" as a table: name | what it contains | host | URL | reachable from this session now (GitHub, PyPI, Hugging Face, Zenodo, 4TU, UCI, OpenML, data.gov: yes; Kaggle: needs a token; publisher supplements behind bot protection: no) | license note.',
  '8. "## API verification (Crossref / OpenAlex / arXiv)" containing the verify_refs.py output table and the corrections you made because of it.',
  '9. "## Limitations of this scan" (access depth per row, search engine and API coverage, limits of citation chasing, sites that refused fetches, date).',
  'Return the structured summary (schema enforced). In "papers", "finding" is one or two sentences of what the result actually showed as visible in snippets; "relevance" says which gap it informs. "search_log_count" is the number of queries you actually ran. "file" is the absolute path you wrote.',
].join('\n\n')

const auditPrompt = (a, res) => [
  'You are an independent citation auditor. Today is ' + TODAY + '.',
  ENV,
  'Read the file ' + res.file + ' (area: ' + a.title + '). It was written by another agent from web-search snippets.',
  'First check that the file has an "API verification" section and that its corrections were applied to the evidence table; if the section is missing, run the verify_refs.py tool on the table titles yourself and add it. Then pick 5 papers from the evidence table: the 3 that the Synthesis and Candidate gaps sections rely on most, plus the 2nd and the second-to-last rows. For each, confirm independently (Crossref API by DOI or title, the arXiv abs page via WebFetch, the AIS eLibrary page, the Semantic Scholar API, or a WebSearch with the exact title in double quotes): (a) a paper with this title exists, (b) authors/year/venue in the table match, (c) whether it is peer-reviewed or a preprint, (d) whether a published version supersedes a preprint listed, (e) whether the stated access depth is plausible given what the file shows (an "abstract" row should contain abstract-level detail).',
  'Also scan the whole file for: claims of "first" or "no prior work"; the word "systematic" used to describe this scan; screening counts; DOIs that do not appear in any search result; datasets marked reachable although hosted on sites that refuse fetches or need credentials (Kaggle, SSRN, publisher supplements). Fix wording problems directly in the file with minimal edits (do not delete evidence rows).',
  'Append a section "## Citation audit (' + TODAY + ')" to the end of the file listing each checked paper, the query used, and the outcome (confirmed / partially confirmed with corrections made / not found). Correct any confirmed metadata errors in the evidence table in place and note the correction in the audit section.',
  'Return the structured result. "unconfirmed" lists papers you could not confirm or had to correct, with the issue.',
].join('\n\n')

const LENSES = [
  { key: 'cs-technical', name: 'Computer-science technical or empirical contribution', brief: 'Favor contributions that are a new method, a new measurement or evaluation methodology, a reproducible empirical finding about systems or models, or a well-designed negative result. Must be testable on CPU with public data. Be concrete about baselines.' },
  { key: 'bis-organizational', name: 'Business information systems contribution', brief: 'Favor contributions about organizations and information systems: an organizational problem, identified stakeholders, and a contribution to IS knowledge (design science artifact with evaluation, empirical study on public organizational traces such as event logs, public filings, job postings, app reviews, policy documents, open government data, or secondary data re-analysis). Use theory only when it explains a mechanism. Applying a model to a business dataset is not enough.' },
  { key: 'governance-evaluation', name: 'AI governance, safety and evaluation validity', brief: 'Favor contributions about whether we can trust how AI is evaluated, audited or governed: validity of LLM-as-judge, reproducibility and statistical practice in published evaluations, benchmark contamination, compliance operationalization, documentation practice, auditability. Re-analysis of released results and documents is in scope and feasible on CPU.' },
  { key: 'frugal-low-resource', name: 'Resource-constrained organizations, efficiency and underserved languages', brief: 'Favor contributions relevant to SMEs, public bodies or developing-economy contexts: CPU-only or small-model methods, cost-performance trade-offs, low-resource language business text (e.g., Bangla), lexical versus neural retrieval under constraints, and the adoption gap. State clearly which parts need the network policy widened.' },
]

const lensPrompt = (L, digest) => [
  'You are generating candidate research ideas for an original, credible research project in CS / AI / business information systems. Today is ' + TODAY + '.',
  ENV,
  'LENS: ' + L.name + '. ' + L.brief,
  'LANDSCAPE DIGEST (from eight literature scouts; snippet-level evidence; files under ' + LIT + ' hold the full tables and you may Read them):',
  digest,
  'Propose exactly 3 distinct ideas through your lens. For each idea fill every field: working_title; problem_rq (precise problem and research question); why_matters; contribution (technical / theoretical / empirical / systems, or IS contribution with organizational problem and stakeholders); closest_studies (3-5 titles from the digest or files, exact titles); difference (what would differ from those studies); design (plausible research design with baselines, measures, unit of analysis, confirmatory vs exploratory parts); data_resources (name concrete datasets or public sources and where they are hosted; GitHub, PyPI, Hugging Face, Zenodo, 4TU, UCI, OpenML and data.gov are reachable now, Kaggle is not without a token); risks (validity and execution); journal_audience; undermining_evidence (what finding or prior paper would kill the idea); lens; runs_without_llm (true if the core study can be executed with no LLM or embedding model at all; note that embedding models and small open LLMs can run on CPU here, paid APIs and GPUs cannot be used).',
  'Reject ideas that merely rename an existing method, combine fashionable techniques without a reason, test another model on another dataset without new insight, chase small benchmark gains, or claim a gap because one paper suggested future work. Prefer ideas that can produce a defensible contribution even if the main hypothesis fails.',
  'At least one of your three ideas must be executable now with runs_without_llm = true. Do not write files. Return structured output only.',
].join('\n\n')

const mergePrompt = (ideas, digest) => [
  'You consolidate candidate research ideas. Today is ' + TODAY + '.',
  ENV,
  'Below are ' + ideas.length + ' raw ideas produced through four lenses. Merge duplicates and near-duplicates, drop ideas that fail the substance test (renaming, fashionable combination, model-on-dataset without insight, small benchmark gain, gap-from-one-future-work-sentence), and return 6 to 8 distinct, strongest ideas, keeping every field complete and recording in "lens" which lenses they came from (e.g. "merged: cs-technical + governance-evaluation"). Keep the set diverse: at least two ideas with runs_without_llm = true, at least one business-information-systems idea with a clear organizational problem, at least one evaluation-validity or governance idea.',
  'RAW IDEAS JSON:',
  JSON.stringify(ideas, null, 1),
  'LANDSCAPE DIGEST for context:',
  digest,
  'Do not write files. Return structured output only.',
].join('\n\n')

const slugOf = (t, i) => String(i + 1).padStart(2, '0') + '-' + String(t || 'idea').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 48)

const noveltyPrompt = (idea, slug) => [
  'You are a skeptical reviewer whose job is to REFUTE the novelty of a proposed research idea. Today is ' + TODAY + '.',
  ENV,
  'IDEA JSON:',
  JSON.stringify(idea, null, 1),
  'Run at least 12 targeted queries, mixing WebSearch, the Semantic Scholar API (curl "https://api.semanticscholar.org/graph/v1/paper/search?query=...&limit=10&fields=title,year,venue,externalIds,citationCount"; back off on 429) and the arXiv API (export.arxiv.org/api/query?search_query=all:...), looking for: the same underlying idea under different terminology; closely related work in adjacent disciplines (IS, OR/management science, HCI, software engineering, economics); recent 2025-2026 preprints and conference papers (use mode "extended" for at least 3 queries, and allowed_domains ["arxiv.org"] for at least 2); existing tools, products or open-source systems that already provide the claimed capability; studies that contradict the proposed motivation. Try at least 3 phrasings that do not reuse the idea\'s own keywords. Read the abstracts of the 3-5 closest works (arXiv abs pages, AIS eLibrary, Semantic Scholar) before judging overlap, and say in the comparison table which abstracts you read.',
  'Default to "partially-covered" when uncertain. Use "largely-covered" if a paper or tool already does substantially what is proposed. Use "likely-novel-within-search-limits" only if nothing close surfaced after all queries, and state the limits.',
  'WRITE a markdown file at ' + CHAL + '/' + slug + '__novelty.md (create the directory if needed) containing: the idea title; a search log table (# | query | filters/mode | useful hits); a prior-art comparison table (work | year | venue/status | link | what it does | overlap with the idea | what the idea would still add); the verdict with reasoning; search limits. Return structured output; "file" is the absolute path written; "query_count" is the number of queries actually run.',
].join('\n\n')

const feasPrompt = (idea, slug) => [
  'You are a feasibility assessor for a research idea under tight constraints. Today is ' + TODAY + '.',
  ENV,
  'IDEA JSON:',
  JSON.stringify(idea, null, 1),
  'Assess, using WebSearch where needed (at least 6 queries; use allowed_domains ["github.com"] to locate GitHub-hosted datasets and code): (1) does suitable data actually exist: name, URL, host, license, approximate size, and whether it is reachable now. Confirm existence with an API call where possible (Hugging Face: curl https://huggingface.co/api/datasets/<id>; Zenodo: https://zenodo.org/api/records?q=...; 4TU, UCI, OpenML pages via WebFetch). For GitHub-hosted data confirm via WebSearch only and note that the repository must be added to the session before use. Kaggle needs an account token we do not have; (2) are labels and measurements adequate for the intended claim; (3) can the experiments run on 4 CPU cores and 15 GB RAM in reasonable time; (4) does the core method need an LLM or embedding model; embedding models and small open generative models (roughly 1-4B parameters, quantized) from Hugging Face run on CPU here, slowly, while paid APIs and GPUs are unavailable; is there a credible small-model or non-neural variant, and how many model calls would the design need; (5) are baselines reproducible from public code; (6) are participants, consent, or institutional approval required; (7) is the intended claim supportable with the design (e.g. no causal claims from observational data).',
  'Do NOT download datasets or model weights and do not clone repositories; existence and metadata checks only. Do not install packages.',
  'WRITE a markdown file at ' + CHAL + '/' + slug + '__feasibility.md containing: idea title; data options table (name | what | host | URL | reachable now | license | size | adequacy for the claim | how existence was confirmed); compute and dependency assessment including estimated CPU hours for the pilot and the full study; approvals and ethics; what the design can and cannot claim; blockers; verdict with reasoning; the minimum change in resources that would unblock it. Return structured output; "file" is the absolute path written.',
].join('\n\n')

const synthPrompt = (chal, digest) => [
  'You are the lead analyst synthesizing the preliminary idea round for a research project in CS / AI / business information systems. Today is ' + TODAY + '.',
  ENV,
  'INPUT: ' + chal.length + ' candidate ideas, each with an adversarial novelty check and a feasibility check (JSON below). Full per-idea reports are under ' + CHAL + ' and literature files under ' + LIT + '; Read them where the JSON is not enough.',
  JSON.stringify(chal, null, 1),
  'LANDSCAPE DIGEST:',
  digest,
  'WRITE ' + ROOT + '/02_candidate_ideas.md with: (1) a header stating the date, that this is a PRELIMINARY Stage 3-4 round based on abstract-level literature access with API-verified metadata where available, and that scores are decision aids, not evidence of publishability; (2) a comparison table across all ideas with qualitative ratings High/Medium/Low for novelty (within search limits), significance, methodological strength, feasibility now on CPU, feasibility with external resources (GPU or API credits), reproducibility, top-journal fit (the author targets a top journal; say which tier each idea could realistically reach and why), plus the novelty verdict and feasibility verdict from the checks, and one-line rationale per rating cell group; (3) a full idea card per idea with all eleven fields, the closest prior art found by the novelty check and exactly where the idea differs, the data options and blockers from the feasibility check, and the evidence that would undermine it; (4) a recommendation of the strongest 2 or 3 candidates for deeper Stage 4 investigation, with explicit reasons and the main risk of each; (5) for each recommended idea, a concrete plan to test novelty further (which databases to query once network access allows, backward/forward citation chasing on which papers) and feasibility (which datasets to add, which pilot to run first, what result would stop the idea); (6) what the author must decide (discipline CS vs IS, journal tier versus feasibility trade-off, willingness to run slow CPU experiments over weeks) before a primary project is selected; (7) a list of ideas dropped or deprioritized and why.',
  'Be conservative: if a novelty check says largely-covered, do not recommend that idea unless you can articulate a sharp, defensible difference. Do not recommend anything that is infeasible under every plausible resource scenario. Return structured output; "overall_decision" is proceed/revise/pivot/stop for the project as a whole.',
].join('\n\n')

const criticPrompt = () => [
  'You are a completeness and integrity critic for a research records directory. Today is ' + TODAY + '.',
  ENV,
  'Read every markdown file under ' + ROOT + ' (use Glob and Read). Check for: (a) claims not traceable to a search result (DOIs, author lists, venues, numbers); (b) any area file missing its search log, inclusion/exclusion criteria, synthesis, gaps, datasets, or limitations section; (c) use of "systematic", "first", "novel" without qualification, or invented screening counts; (d) datasets marked reachable although hosted on sites that refuse fetches or need credentials (Kaggle, SSRN, publisher supplements), or GitHub repositories implied to be readable without being added to the session; access-depth labels that overstate what was read; (e) inconsistencies between the comparison table ratings in 02_candidate_ideas.md and the per-idea challenge files; (f) ideas recommended despite a "largely-covered" novelty verdict or an "infeasible" feasibility verdict without an explicit justification; (g) any statement that reads as a completed experiment, result, or verified finding when none was run.',
  'Fix small wording and consistency problems directly with minimal edits. Do not delete evidence. List everything you fixed and everything that remains open and needs a human or a later stage. Return structured output.',
].join('\n\n')

phase('Landscape')
const land = await pipeline(AREAS,
  (a) => agent(landscapePrompt(a), { label: 'landscape:' + a.key, phase: 'Landscape', schema: LANDSCAPE_SCHEMA }),
  (res, a) => res && res.file ? agent(auditPrompt(a, res), { label: 'audit:' + a.key, phase: 'Audit', schema: AUDIT_SCHEMA }).then(aud => ({ area: a, landscape: res, audit: aud })) : null,
)
const done = land.filter(Boolean)
log('Landscape complete for ' + done.length + '/' + AREAS.length + ' areas' + (done.length < AREAS.length ? '; dropped: ' + AREAS.filter((a, i) => !land[i]).map(a => a.key).join(', ') : ''))

const digest = done.map(d => ({
  area: d.landscape.area, file: d.landscape.file, gaps: d.landscape.gaps, contradictions: d.landscape.contradictions,
  key_papers: d.landscape.papers.slice(0, 9).map(p => ({ title: p.title, authors: p.authors_short, year: p.year, venue: p.venue, status: p.status, finding: String(p.finding || '').slice(0, 260), url: p.url })),
  datasets: d.landscape.datasets, audit: d.audit ? { checked: d.audit.checked, confirmed: d.audit.confirmed, issues: d.audit.unconfirmed } : null,
}))
const digestStr = JSON.stringify(digest, null, 1)

phase('Ideate')
const lensResults = await parallel(LENSES.map(L => () => agent(lensPrompt(L, digestStr), { label: 'ideate:' + L.key, phase: 'Ideate', schema: IDEAS_SCHEMA })))
const rawIdeas = lensResults.filter(Boolean).flatMap(r => r.ideas || [])
log('Ideation produced ' + rawIdeas.length + ' raw ideas from ' + lensResults.filter(Boolean).length + ' lenses')
const merged = await agent(mergePrompt(rawIdeas, digestStr), { label: 'merge-ideas', phase: 'Ideate', schema: IDEAS_SCHEMA })
const ideas = ((merged && merged.ideas) || []).slice(0, 8)
log('Merged to ' + ideas.length + ' candidate ideas')

phase('Challenge')
const challenged = await pipeline(ideas,
  (idea, _o, i) => {
    const slug = slugOf(idea.working_title, i)
    return parallel([
      () => agent(noveltyPrompt(idea, slug), { label: 'novelty:' + slug, phase: 'Challenge', schema: NOVELTY_SCHEMA }),
      () => agent(feasPrompt(idea, slug), { label: 'feasibility:' + slug, phase: 'Challenge', schema: FEAS_SCHEMA }),
    ]).then(([nov, feas]) => ({ slug, idea, novelty: nov, feasibility: feas }))
  },
)
const chal = challenged.filter(Boolean)
log('Challenge complete for ' + chal.length + '/' + ideas.length + ' ideas')

phase('Synthesize')
const synth = await agent(synthPrompt(chal, digestStr), { label: 'synthesis', phase: 'Synthesize', schema: SYNTH_SCHEMA })
const critic = await agent(criticPrompt(), { label: 'completeness-critic', phase: 'Synthesize', schema: CRITIC_SCHEMA })

return {
  areas: done.map(d => ({ key: d.area.key, file: d.landscape.file, papers: d.landscape.papers.length, searches: d.landscape.search_log_count, gaps: d.landscape.gaps, audit: d.audit })),
  ideas: chal.map(c => ({ slug: c.slug, title: c.idea.working_title, runs_without_llm: c.idea.runs_without_llm, novelty: c.novelty && c.novelty.verdict, feasibility: c.feasibility && c.feasibility.verdict, blockers: c.feasibility && c.feasibility.blockers, prior_art_count: c.novelty && c.novelty.prior_art ? c.novelty.prior_art.length : null })),
  synthesis: synth,
  critic,
}