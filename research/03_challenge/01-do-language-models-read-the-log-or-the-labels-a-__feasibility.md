# Feasibility assessment — idea 01

**Idea title:** Do Language Models Read the Log or the Labels? A Label-Intervention Protocol for Semantics-Aware Next-Activity Prediction at Varying Training Sizes

**Assessed:** 2026-10-03. Source record: `research/02_candidate_ideas_merged.json`, `ideas[0]` (lens: cs-technical; `runs_without_llm: false`).

**Method of this assessment:** 9 WebSearch queries (4 restricted to github.com), 4TU.ResearchData v2 API calls, doi.org redirect checks, Hugging Face model API calls, arXiv export API, two arXiv HTML full texts pulled with curl (Weytjens and Weber 2606.15868; Padella, de Leoni and Dumas 2601.11468), PyPI JSON checks, and one run of `research/tools/verify_refs.py`. Semantic Scholar and OpenAlex answered HTTP 429 on every call today; Crossref and arXiv answered. WebFetch is blocked by the egress proxy for arxiv.org, data.4tu.nl and dev.to; curl to arxiv.org and data.4tu.nl works. No dataset, model weight or repository was downloaded; no package was installed.

---

## 1. Data options

| Name | What | Host | URL | Reachable now | License | Size | Adequacy for the claim | How existence was confirmed |
|---|---|---|---|---|---|---|---|---|
| BPI Challenge 2012 | Loan-application event log (XES) | 4TU.ResearchData | https://doi.org/10.4121/uuid:3926db30-f712-4394-aebc-75976070e91f (article 12689204) | Yes (doi.org 302 to data.4tu.nl; v2 API 200) | 4TU General Terms of Use | `BPI_Challenge_2012.xes.gz` 3,342,406 bytes; after Weytjens–Weber preprocessing 9,487 cases, 37 classes, 173,498 prefixes | Fine for label-agnostic baselines, anonymised arm and learning curves; labels are partly Dutch (e.g. `W_Nabellen incomplete dossiers`, quoted by Padella et al.), so the idea correctly assigns it to the non-semantic arms. Used by both Weytjens–Weber and Padella et al., so it is the one log that directly bridges the two results. | doi.org HEAD + 4TU v2 API (title, DOI, licence, file list) |
| BPI Challenge 2017 | Loan-application log (XES) | 4TU.ResearchData | https://doi.org/10.4121/uuid:5f3067df-f10b-45da-b98b-86ae4c7a310b (article 12696884) | Yes | 4TU General Terms of Use | `BPI Challenge 2017.xes.gz` 29,658,747 bytes; 29,306 cases, 63 classes, 1,100,691 prefixes after preprocessing (W–W Table 2) | Same as BPI12 (partly Dutch labels). The 1.1 M prefixes make it the main compute driver for embedding and LSTM arms; test subsampling for the LLM arm is already planned. One of only two logs where W–W found LLMs beating argmax, so it is a useful stress case. | doi.org + 4TU v2 API |
| Sepsis Cases – Event Log | Hospital sepsis pathway log (XES) | 4TU.ResearchData | https://doi.org/10.4121/uuid:915d2bfb-7e84-49ad-a286-dc35f063a460 (article 12707639) | Yes | 4TU General Terms of Use | `Sepsis Cases - Event Log.xes.gz` 202,508 bytes; "about 1000 cases with in total 15,000 events ... 16 different activities" (4TU description) | Small log: only two of the seven training sizes (50–500) are reachable before "full"; good for the data-scarce end of the curves. Label language not read here (the idea record says English). Timestamps randomised by the publisher but intra-trace gaps preserved, so temporal splitting is only approximately meaningful. | doi.org + 4TU v2 API (description read) |
| Road Traffic Fine Management Process | Italian municipality fines log (XES) | 4TU.ResearchData | https://doi.org/10.4121/uuid:270fd440-1057-4fb9-89a9-b699b47990f5 (article 12683249) | Yes | 4TU General Terms of Use | `Road_Traffic_Fine_Management_Process.xes.gz` 3,454,978 bytes; case count not shown in the 4TU description | Short traces and few activities (per the idea record; not verified here) make it an easy target where argmax will be strong; useful as a ceiling case but weak for detecting semantic gain. Not used by Weytjens–Weber, so no published reference numbers under their split. | doi.org + 4TU v2 API |
| BPI Challenge 2020: Prepaid Travel Costs | Travel-expense sub-log (XES) | 4TU.ResearchData | https://doi.org/10.4121/uuid:5d2fe5e1-f91f-4a3b-ad9b-9e4126870165 (article 12696722) | Yes | CC BY-NC 4.0 | `PrepaidTravelCost.xes.gz` 370,047 bytes; 1,791 cases, 30 classes, 15,730 prefixes after preprocessing (W–W Table 2) | English declaration-workflow labels (per idea record), so it carries the semantic arms. Small, so the 1000/2500 training sizes collapse into "full". | 4TU collection 5065541 article list + v2 API |
| BPI Challenge 2020: Travel Permit Data | Travel-permit sub-log (XES) | 4TU.ResearchData | https://doi.org/10.4121/uuid:ea03d361-a7cd-4f5e-83d8-5fbdf0362550 (article 12718178) | Yes | CC BY-NC 4.0 | `PermitLog.xes.gz` 1,938,192 bytes; "7,065 cases, 86,581 events" (4TU); 6,847 cases, 52 classes, 83,620 prefixes after preprocessing (W–W) | As above; the richest of the BPI20 sub-logs (52 classes) and the best candidate for the conflict-set construction because its labels encode a stage order (submit, approve, pay). | 4TU v2 API (description read) |
| BPI Challenge 2020: Request For Payment | Request-for-payment sub-log (XES) | 4TU.ResearchData | https://doi.org/10.4121/uuid:895b26fb-6f25-46eb-9e48-0dca26fcd030 (article 12706886) | Yes | CC BY-NC 4.0 | `RequestForPayment.xes.gz` 696,896 bytes; "6,886 cases, 36,796 events" (4TU); 5,701 cases, 18 classes, 30,153 prefixes after preprocessing (W–W) | As above. Only 245 unique prefixes and a 57.6 % top-5 prefix share (W–W Table 2), so argmax will be near ceiling; semantic effects will be hard to see here. | 4TU v2 API |
| BPI Challenge 2020 collection (also Domestic and International Declarations) | Parent collection | 4TU.ResearchData | https://doi.org/10.4121/uuid:52fb97d4-4588-43c9-9d04-3604d4613b51 (collection 5065541) | Yes | CC BY-NC 4.0 (sub-logs) | 5 sub-logs | Two further English-label logs (12692543, 12687374) are available as replication logs if needed. | 4TU collection API |
| "Bac" (Bank Account Closure) log used by Padella et al. | CSV event log in IBM demo repository (`Datasets_usecases`) | GitHub (IBM/processmining) | https://github.com/IBM/processmining | Repository exists (WebSearch); not fetched; must be added to the session before use | Not shown | 25,843 training traces per Padella et al. Table 1; file size not shown | Would allow a direct link to Padella's hashing result, but it is a vendor demo log with no documented provenance; optional. | WebSearch (github.com) and the arXiv HTML footnote of 2601.11468 |
| Padella et al. "Hospital" log | Private emergency-department log | Not public | — | No | — | 30,394 training traces (Table 1) | Not usable; the idea record already says so. | arXiv HTML of 2601.11468 |
| Weytjens–Weber split and code | Leakage-free temporal split scripts and the "David vs. Goliath" notebooks | GitHub | https://github.com/hansweytjens/predictive-process-monitoring-benchmarks ; https://github.com/hansweytjens/DavidGoliath | Repositories exist (WebSearch; the second is cited in the paper as `github.com/hansweytjens/DavidGoliath`, "last updated June 12, 2026" per the search snippet); must be added to the session before use | Not shown | Not shown | Needed to reproduce the 20 % test / 10 % validation split "according to Weytjens et al. [26]" that the idea wants to match. | WebSearch (github.com) + arXiv HTML |
| Rebmann et al. benchmark/code | `a-rebmann/llms4pm` evaluation scripts for semantics-aware tasks | GitHub | https://github.com/a-rebmann/llms4pm | Exists (WebSearch); must be added to the session before use | Not shown | Not shown | Useful only as a reference implementation of label-text serialisation; its tasks are not next-activity prediction. | WebSearch (github.com) |
| PGTNet code | Baseline used by Padella et al. (remaining-time) | GitHub | https://github.com/keyvan-amiri/PGTNet | Exists (WebSearch) | Not shown | Not shown | Not needed: PGTNet is a remaining-time model; the idea's baselines are argmax, Markov and LSTM. | WebSearch (github.com) |
| Padella et al. code | `Pado123/gui_xrecs_presc_analytics` (footnote 7 of 2601.11468) | GitHub | https://github.com/Pado123/gui_xrecs_presc_analytics | Seen only as a footnote in the arXiv HTML; not confirmed via WebSearch | Not shown | Not shown | Their pipeline calls Gemini 2.5 Flash Thinking through Google's API, so it cannot be rerun here; only the hashing logic is reusable. | arXiv HTML footnote |

### Models (Hugging Face API, all `gated: False`, `private: False`, checked 2026-10-03)

| Model id | Licence tag | Role in design | GGUF availability |
|---|---|---|---|
| Qwen/Qwen2.5-1.5B-Instruct | apache-2.0 | few-shot + LoRA arm | Qwen/Qwen2.5-1.5B-Instruct-GGUF (q2_k … fp16 files listed) |
| Qwen/Qwen2.5-3B-Instruct | other (Qwen research licence) | few-shot arm | Qwen/Qwen2.5-3B-Instruct-GGUF (q2_k … fp16) |
| Qwen/Qwen3-1.7B | apache-2.0 | few-shot arm | Qwen/Qwen3-1.7B-GGUF (only `Qwen3-1.7B-Q8_0.gguf` in the official repo) |
| Qwen/Qwen3-4B | apache-2.0 | few-shot arm | Qwen/Qwen3-4B-GGUF (Q4_K_M, Q5_0, Q5_K_M, Q6_K, Q8_0) |
| HuggingFaceTB/SmolLM2-1.7B-Instruct | apache-2.0 | few-shot arm | HuggingFaceTB/SmolLM2-1.7B-Instruct-GGUF and bartowski/… exist (API search) |
| microsoft/Phi-3.5-mini-instruct | mit | few-shot arm | no GGUF in the Microsoft repo; MaziyarPanahi/ and bartowski/Phi-3.5-mini-instruct-GGUF exist (API search; third-party conversions) |
| Qwen/Qwen2.5-0.5B-Instruct | apache-2.0 | fallback for the LoRA arm (not in the idea record) | not checked |
| sentence-transformers/all-MiniLM-L6-v2 | apache-2.0 | embedding classifier arm | n/a |
| BAAI/bge-small-en-v1.5 | mit | embedding classifier arm | n/a |

Per-file sizes were not returned by the API call used; typical Q4_K_M files for 1.5–4 B models are roughly 1–2.5 GB each (estimate, not read).

### Licence notes
- The four older logs carry the "4TU General Terms of Use" (licence id 98 in the 4TU licence list). The terms page itself could not be rendered (JavaScript page); the DOI must be cited. These logs are routinely used in published academic work, including Weytjens–Weber and Padella et al.
- BPI20 sub-logs are CC BY-NC 4.0: non-commercial academic use with attribution is permitted; derived label-rewritten versions may be redistributed under the same terms.
- Qwen2.5-3B-Instruct is under the Qwen research licence ("other"); the other generative models are Apache-2.0 or MIT. No model is gated.

---

## 2. Labels and measurements (adequacy for the intended claim)

- **Next-activity labels** come directly from the logs; no annotation is needed. Weytjens–Weber append an "EOS" token per case and concatenate activity with lifecycle transition where present; matching that choice is required for comparability and is cheap.
- **Label-condition arms** (original, anonymised codes, synonym paraphrase, meaning-conflicting permutation, reversed stage names) are deterministic rewrites of the activity vocabulary (18–63 labels per log). They can be produced by hand or with a small model and frozen before any run; the anonymised arm is exactly Padella et al.'s "semantic hashing" ("we encode all process-related strings, such as trace variable and activity names, into hashed representations"), so the comparison is like-for-like.
- **Conflict-set construction** needs an operational definition of the "label-implied" next activity that does not use the predictor under test. The defensible choice is: under permutation π, the label-implied successor of text t is the original-log majority successor of the activity that originally carried text t, remapped through π. This is computable from the log alone and avoids human raters. It should be preregistered.
- **Measurement precision is the real limit.** With 500 test prefixes per (log, condition) in the LLM arm, a single accuracy estimate has a 95 % half-width of about ±4.4 points at 50 % accuracy; the manipulation-check tolerance of 0.5 points (H1) and the "not distinguishable from zero at n ≥ 1000" claim (H2) cannot be established from 500 unpaired prefixes. Because every condition is evaluated on the *same* prefixes, the analysis must be paired (per-prefix differences, McNemar-type or paired bootstrap, trace-clustered), and H2 must be an equivalence test (TOST) with a preregistered margin of a few points, not a non-significant difference. The classical and embedding arms use full test sets (tens of thousands to 220 k prefixes), where 0.5-point tolerances are measurable.
- **Partly Dutch labels** in BPI12/BPI17 are a known limitation; the idea already routes the semantic hypotheses through the English logs (Sepsis, RTF, BPI20). Note that Padella et al.'s BPI12 hashing effect was obtained on exactly these mixed-language labels with a proprietary model, so the "English-only semantic arm" choice makes the reconciliation with Padella indirect.
- **Calibration (ECE)** is available for argmax, Markov, LSTM and the embedding classifiers; for generative LLM arms it exists only if next-token log-probabilities over candidate labels are scored (llama.cpp returns logits), which multiplies cost; treat as exploratory.

---

## 3. Compute and dependency assessment

**Environment today:** 4 CPU cores, 15 GB RAM, 29 GB free disk, Python 3.11.15, gcc 13.3 and cmake 3.28 present. None of pm4py, numpy, scikit-learn, torch, sentence-transformers, transformers, peft or llama-cpp-python is installed; PyPI pages for all of them answered (pm4py 2.7.23.8, llama-cpp-python 0.3.36, sentence-transformers 6.1.0, torch 2.14.1, peft 0.21.2, scikit-learn 1.9.1). llama-cpp-python compiles from source on install (toolchain available). Hugging Face downloads work (a 91 MB model in 3 s per the environment note).

**CPU inference speed references (WebSearch snippets, not measured here):** Qwen2.5-3B on an Intel i7-6700, CPU only, current llama.cpp: 35.1 tokens/s prompt processing, 12.0 tokens/s generation; Qwen2 3B Q4_K_M with 4 threads: pp512 67.3 t/s, tg128 22.7 t/s. I assume 30–60 t/s prefill for 3–4 B Q4 models and roughly double for 1.5–1.7 B on this machine.

**Per-prompt cost.** A text-serialised few-shot prompt with ~10 demonstration prefixes is roughly 1,500–4,000 tokens (BPI17 prefixes average ~38 events; BPI20 RFP ~5). Without cache reuse that is 30–120 s per prompt on a 3–4 B model. With the demonstration block fixed per (log, size, condition, model) and its KV state cached (llama.cpp prompt cache / state save), only the query prefix (100–400 tokens) plus ≤ 8 generated tokens are processed: ~3–12 s per prompt. The design must use cache reuse; the estimates below assume it. Qwen3 "thinking" must be disabled or generation length explodes.

**Design as written:** 7 logs × 7 sizes × 5 conditions × 6 LLMs × 500 prefixes = 735,000 prompts ≈ 1,400 CPU-hours even with cache reuse (≈ 60 days wall-clock on 4 cores), or several thousand hours without. **Not feasible as written.**

**Trimmed LLM arm (recommended):** 4 English logs × 3 sizes (50, 250, 1000/full) × 3 conditions (original, anonymised, conflicting) × 2 models (Qwen2.5-1.5B, Qwen3-4B) × 300 prefixes = 21,600 prompts ≈ 50 CPU-hours; add paraphrase and reversed conditions for one model (+14,400 prompts, ≈ 30 h). Four further models could be run on one log and one size as a robustness table (≈ 10 h). **LLM arm ≈ 90–100 CPU-hours, ~36,000–40,000 model calls.**

**Embedding arm:** embeddings depend on the label condition but not on training size, so each prefix text is encoded 5 × 2 (conditions × models) times. Total prefixes across the seven logs after W–W preprocessing are roughly 1.9–2.4 M (BPI17 alone 1.1 M; RTF count not shown). At a few hundred sequences/s for a 22 M-parameter MiniLM on 4 cores (estimate), encoding is ~20–40 CPU-hours; kNN/logistic fits over 7 sizes × 5 seeds are minutes each. Subsampling BPI17 and RTF test sets to ~50 k prefixes halves this.

**LSTM arm:** 7 logs × 7 sizes × 5 seeds × 2 conditions (the manipulation check needs only two) = 490 small runs; minutes each for n ≤ 2,500, 1–2 h each at full size for BPI17. ≈ 40–80 CPU-hours; reduce to 3 seeds at full size if needed.

**Argmax and Markov:** seconds per run; negligible.

**LoRA arm (the bottleneck):** fine-tuning a 1.5 B model on CPU is ~6 × 1.5e9 FLOPs per token; at n = 100 traces (≈ 500–1,800 prefix examples × ~200 tokens) one epoch is ~1e14–2e15 FLOPs ≈ 1–20 h at a realistic 30–100 GFLOP/s, and n = 500 is five times that. Memory fits (bf16 base 3 GB + LoRA states). Realistic scope: Qwen2.5-1.5B at n ∈ {50, 100} on two logs, 3 epochs, 1 seed (≈ 60–120 CPU-hours), or Qwen2.5-0.5B at n ≤ 500 for a third of that. Treat LoRA as exploratory, not confirmatory.

**Totals.**
- *Pilot* (2 logs: BPI20 Travel Permit and Sepsis; sizes 50/250/full; conditions original/anonymised/conflicting; argmax, Markov, LSTM, MiniLM-kNN, Qwen2.5-1.5B few-shot on 200 prefixes): **≈ 15–25 CPU-hours**, 2–3 days wall-clock including setup and prompt-cache engineering.
- *Full study, trimmed as above:* LLM 90–100 h + embeddings 20–40 h + LSTM 40–80 h + LoRA (restricted) 60–120 h ≈ **250–350 CPU-hours ≈ 3–5 weeks wall-clock on 4 cores**, runs sequentially because llama.cpp uses all cores for one prompt.
- Disk: ~8–12 GB of GGUF and safetensors plus ~2 GB of torch/CPU wheels and <0.3 GB of logs; within the 29 GB free.
- RAM: largest resident is Qwen3-4B Q4 (~3 GB) plus KV cache; LoRA on 1.5 B in bf16 with batch 4 stays under 10 GB.

**Does the core method need an LLM or embedding model?** Yes for the research question (it asks about language models), but the *protocol* (label interventions + argmax/Markov/LSTM manipulation checks + learning curves) runs with no neural model at all, and the semantics-aware arm can be carried credibly by the 22 M-parameter sentence-embedding classifiers alone. That non-generative variant is the cheapest version of the study and answers RQ1 and RQ2 for embedding-based predictors; the generative-LLM arm adds generality but is the only expensive part. Paid APIs and GPUs are not needed for the trimmed design.

---

## 4. Approvals and ethics

- All logs are public, de-identified research datasets published by their owners on 4TU.ResearchData (the Sepsis log additionally has randomised timestamps). No human participants, no survey, no interviews, no institutional data access. **No IRB/ethics approval is required.**
- Licence compliance: cite each DOI; BPI20 sub-logs are CC BY-NC 4.0 (non-commercial, attribution); 4TU General Terms for the rest. Rewritten-label derivatives should be released with the same terms and a changelog.
- Model licences permit research use (Apache-2.0, MIT, Qwen research licence for the 3 B model).
- No sensitive content is generated; LLM outputs are activity names.

---

## 5. What the design can and cannot claim

**Can claim (internally valid):**
- For each tested predictor, the causal effect of activity-label *text* on its next-activity predictions, because the label condition is an experimenter-controlled intervention on the model's input with everything else held fixed (same prefixes, same split, same seed). "Semantic dependence" and "evidence fidelity" are therefore interventional quantities, not observational correlations.
- Learning curves of trivial, classical and semantics-aware predictors on the same seven public logs under the Weytjens–Weber split, with paired, trace-clustered intervals.
- A replication of the Weytjens–Weber argmax-parity finding on BPI12/BPI17/BPI20 (same logs, same split) and a conceptual replication of Padella et al.'s hashing effect with open models, which is the reconciliation the idea promises.

**Cannot claim (or must be scoped):**
- Anything about proprietary or frontier models (Gemini 2.5 Flash, GPT-class). If 1.5–4 B models show no semantic dependence, that does not show that Padella et al.'s effect is absent at larger scale; the paper must say "for open models up to 4 B on CPU".
- "No semantic gain" as a point null: H2 must be an equivalence claim with a preregistered margin, and only in the arms with enough paired prefixes to support it (classical and embedding arms; LLM arms with ≤ 500 prefixes can support margins of ~4–5 points, not 0.5).
- Generalisation beyond the seven logs or beyond next-activity prediction (Padella's KPIs were total time and activity occurrence).
- Fidelity rates are conditional on a selected conflict set; always report the conflict-set size and base rate, and the fidelity of argmax (which is 100 % by construction) as the reference.
- If small models sit at chance in every condition, the LLM arm is uninformative and the paper reverts to an embedding-classifier study plus argmax replication; the idea record already names this.

---

## 6. Blockers

1. **LLM arm as written exceeds the CPU budget by an order of magnitude** (≈ 735,000 prompts). Must be trimmed to ~36,000–40,000 prompts with KV-cache reuse, 2 primary models and 3 primary conditions; this is a design change, not a resource acquisition.
2. **LoRA fine-tuning on CPU** is feasible only for the 1.5 B (or 0.5 B) model at n ≤ 100–250 on one or two logs; it cannot be a confirmatory arm across sizes.
3. **Statistical precision** for H1/H2 in the LLM arms at 500 prefixes is insufficient for the preregistered 0.5-point tolerance; hypotheses need paired tests and realistic equivalence margins before preregistration.
4. **Three GitHub repositories must be added to the session** before use (hansweytjens/predictive-process-monitoring-benchmarks and hansweytjens/DavidGoliath for the split and baselines; IBM/processmining only if the Bac log is wanted). Padella et al.'s pipeline depends on the Gemini API and cannot be rerun.
5. **Undermining-evidence check still open:** Fertig et al. (arXiv 2607.27797) and van Straten et al. (arXiv 2608.28236) were read at abstract level only; their full texts (reachable via curl on arxiv.org/html) should be read before preregistration to confirm neither already reports label-intervention controls with trivial baselines across training sizes.
6. Minor: no packages are installed yet; llama-cpp-python needs a source build (toolchain present); Qwen3 thinking mode must be disabled; third-party GGUF conversions for Phi-3.5-mini and SmolLM2 are community uploads, not vendor files.

None of these is a hard blocker; items 1–3 are design corrections, 4–6 are setup steps.

---

## 7. Verdict

**feasible-but-slow-on-cpu.**

Reasoning: every dataset exists, is reachable today, is licensed for academic use and needs no approval; every model is ungated with GGUF builds; the split procedure and argmax baseline are reproducible from public code (Weytjens–Weber cite `github.com/hansweytjens/DavidGoliath` and the benchmark-split repository); the measurement protocol is an input intervention that supports causal statements about predictor behaviour. The only resource problem is the generative-LLM arm, whose factorial as written (6 models × 5 conditions × 7 sizes × 7 logs × 500 prefixes) is ~1,400 CPU-hours with caching; cut to the primary contrasts it is ~100 CPU-hours, and the whole trimmed study is ~250–350 CPU-hours (3–5 weeks on this machine). The embedding-classifier variant of the semantics-aware arm is cheap and is a credible non-generative version of the study. The LoRA arm should be exploratory.

**Reference check (verify_refs.py, Crossref/arXiv columns; OpenAlex and Semantic Scholar returned 429):**
- "David vs. Goliath in Next Activity Prediction: Argmax vs. LSTM, Transformer, and LLM" — Crossref 10.1007/978-3-032-37877-4_19, LNBIP 2026 (BPM Forum chapter, peer-reviewed); arXiv 2606.15868 (full text read via curl).
- "Exploring LLM Features in Predictive Process Monitoring for Small-Scale Event-Logs" — arXiv 2601.11468 (preprint, full text read); Crossref's best match (score 0.747, 10.1007/978-3-032-02929-4_16, LNBIP 2025) is below threshold and is most likely the earlier BPM Forum paper "Enhancing Predictive Process Monitoring on Small-Scale Event Logs Using LLMs" that the preprint says it extends; the preprint itself has no published version shown.
- "Knowledge-Driven Hallucination in Large Language Models: An Empirical Study on Process Modeling" — arXiv 2509.15336v2 and TechRxiv 10.36227/techrxiv.175695580.03540927/v1 (preprints; no peer-reviewed version shown).
- "On the potential of large language models to solve semantics-aware process mining tasks" — Crossref 10.1007/s44311-025-00019-3, Process Science 2025 (peer-reviewed journal); arXiv 2504.21074.
- "Revisiting Predictive Process Monitoring in the Age of Foundation Models: A Comparative Study of Sequence, Tabular, and LLM Approaches" — arXiv 2607.27797 (preprint; the ECML PKDD 2026 workshop venue stated in the idea record was not verified here; the Crossref match at 0.426 is a different paper).

---

## 8. Minimum change in resources that would unblock the full design

A single mid-range GPU (24 GB class) for roughly 30–50 GPU-hours would run the entire as-written LLM factorial (735,000 cached prompts at >50 prompts/s batched) and LoRA for all six models at all seven training sizes, removing blockers 1 and 2 entirely. Short of that, no new resource is needed: the trimmed design above runs on the present machine in 3–5 weeks, and raising the LLM-arm test subsample from 300 to ~1,000 prefixes (to support a 2–3-point equivalence margin) would add about 100 CPU-hours.
