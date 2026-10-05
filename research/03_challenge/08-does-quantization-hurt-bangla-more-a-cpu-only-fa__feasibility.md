# Feasibility assessment — idea 08

**Idea title:** Does Quantization Hurt Bangla More? A CPU-Only Factorial of Precision, Model Size and Script for Generative and Retrieval Models, with a Cost-Matched Lexical-versus-Dense Frontier for Bengali, Swahili and Indonesian

**Assessed:** 2026-10-05. Source record: `research/02_candidate_ideas_merged.json`, `ideas[7]` (lens: merged efficiency-low-resource retrieval frontier + quantization factorial; `runs_without_llm: false`). Part A = generative factorial (RQ1, H1-H3), Part B = retrieval frontier (RQ2, H4-H6), RQ3 joins them.

**Method of this assessment:** 16 WebSearch queries; 46 Hugging Face API calls (`/api/datasets/<id>`, `/api/models/<id>?blobs=true`, `/api/models?search=`) for gated/private flags, licence tags, config lists and per-file sizes; 10 dataset/model cards read via `raw/main/README.md` (metadata only, no data files downloaded); arXiv abstract pages for 9 papers (the `export.arxiv.org` Atom API answered HTTP 200 but returned zero entries for every `ti:` and `id_list` query today, so `arxiv.org/abs` pages were used instead); Crossref for three DOIs (the TACL MIRACL DOI returned a non-JSON body); PyPI JSON for 12 packages; `download.pytorch.org` wheel indexes for cu126/cu128/cu130; `gh api` metadata for ggml-org/llama.cpp, abetlen/llama-cpp-python, EleutherAI/lm-evaluation-harness (task folder names only), castorini/pyserini and xhluca/bm25s; three WebFetch reads (NVIDIA Blackwell migration guide, a 4-core Xeon llama.cpp benchmark post, an OpenBenchmarking i7-14700K result); local probes of the author's machine (`nvidia-smi`, `java -version`, `python --version`, `importlib.util.find_spec`). No package was installed; no model weights or datasets were downloaded. Semantic Scholar and OpenAlex were not used (429 on earlier probes). Two compute scenarios are assessed throughout: **A** = 4 CPU cores, 15 GB RAM, ~30 GB disk, no GPU (the "CPU-only" baseline of ideas 1-3); **B** = the author's local PC measured today: Intel i7-14700KF (8 P + 12 E cores, 28 threads), 31.9 GB RAM, NVIDIA GeForce RTX 5070 Ti 16 GB (compute capability 12.0 per `nvidia-smi`, driver 591.59), 626 GB free disk, Windows 11, Python 3.14.4. Neither scenario has paid LLM APIs, native-speaker raters or institutional access.

---

## 1. Data options

All Hugging Face records below answered HTTP 200 on 2026-10-05 with `gated: False` and `private: False` unless stated. "Configs" lists only the four target languages.

| Name | What | Host | URL | Reachable now | Gated | License | Size / configs | Adequacy for the claim | How existence was confirmed |
|---|---|---|---|---|---|---|---|---|---|
| facebook/belebele | Parallel 4-way multiple-choice reading comprehension; 900 questions per variant on 488 FLORES-200 passages; 122 variants | Hugging Face | https://huggingface.co/datasets/facebook/belebele | Yes | No | cc-by-sa-4.0 | 122 configs incl. `ben_Beng` (3.24 MB jsonl), `ben_Latn` (0.88 MB, romanised Bengali), `swh_Latn` (0.86 MB), `ind_Latn` (0.88 MB), `eng_Latn` (0.84 MB) | The backbone of H1: fully parallel items, so language x precision is a within-item contrast. `ben_Latn` is a free script-only manipulation (same Bangla content, Latin script) that directly separates script from language for RQ1/RQ3 and is not in the idea record. 900 items give ~±2.6-point paired 95 % CIs per cell. Passages are translated FLORES news/wiki text, not organisational text. | HF API (configs, siblings with sizes); card read; Crossref 10.18653/v1/2024.acl-long.44 (ACL 2024) |
| CohereLabs/Global-MMLU | 42-language MMLU translation; 14,042 test + dev per language; "machine translations ... along with professional translations and crowd-sourced post-edits" | Hugging Face | https://huggingface.co/datasets/CohereLabs/Global-MMLU | Yes | No | apache-2.0 | configs `bn` (test parquet 6.2 MB), `sw` (3.9 MB), `id` (3.85 MB), `en` (3.9 MB); card marks bn/id "Mid", sw "Low" resource | Parallel items across languages (same MMLU questions). Translation provenance per language is mixed (which of bn/sw/id are fully human-translated is not shown in the card lines read). 14k items x 4 languages x 48 cells is far too many for CPU; must be subsampled (1,000 stratified items) or replaced by **CohereLabs/Global-MMLU-Lite** (apache-2.0, not gated, human-translated, 200 CS + 200 CA items; configs include `bn`, `sw`, `id`, `en`; confirmed via API today). | HF API; card read; arXiv 2412.03304 |
| indonlp/indonlu | IndoNLU benchmark; SmSA sentiment 11,000 / 1,260 / 500 (train/val/test), 3 classes | Hugging Face | https://huggingface.co/datasets/indonlp/indonlu | Yes | No | mit | 4 files only (`indonlu.py` loading script, `dataset_infos.json`); data pulled by the script from an external URL (not shown); no parquet | Native Indonesian reviews with linguist labels; 500 test items is small but adequate for a classification cell. Script-based dataset: recent `datasets` releases dropped script loading, so the raw files must be fetched manually via the script's URLs. Not parallel with the bn/sw sentiment sets. | HF API; card read (split table) |
| masakhane/masakhanews | News topic classification, 16 African languages; `swa` 1,658 / 237 / 476 | Hugging Face | https://huggingface.co/datasets/masakhane/masakhanews | Yes | No | afl-3.0 | configs `swa`, `eng`; `data/swa/{train,dev,test}.tsv` (6.2 / 0.86 / 1.76 MB) | Native Swahili news; 7-way topic, not sentiment, so the "classification" task differs in label space from SmSA and the Bangla set. 476 test items. English config allows a same-task control. | HF API (files, sizes); card read |
| csebuetnlp/xlsum | BBC article-summary pairs, 45 languages | Hugging Face | https://huggingface.co/datasets/csebuetnlp/xlsum | Yes | No | cc-by-nc-sa-4.0 | per-language tar.bz2 in repo: bengali 13.0 MB, swahili 7.0 MB, indonesian 41.1 MB, english 282 MB | Native text per language but **not parallel**; the design caps it at 200 items/language with chrF and ROUGE-L. Without raters, summarisation is exploratory only (Section 2). Non-commercial licence. | HF API (files); card read |
| csebuetnlp/squad_bn | Bengali extractive QA translated from SQuAD 2.0 and TyDi QA; train 127,771 / validation 2,502 / test 2,504 | Hugging Face | https://huggingface.co/datasets/csebuetnlp/squad_bn | Yes | No | cc-by-nc-sa-4.0 | `data/squad_bn.tar.bz2` 8.4 MB + `squad_bn.py` | Machine-translated with LaBSE filtering (card). bn-only, so it supports size x precision (H2) and fertility cost (H3) but not the language contrast; use 500 validation items. | HF API; card read |
| ragibhasan/coke_studio_bangla_sentiment | 57,592 YouTube comments on Coke Studio Bangla, 3-class sentiment | Hugging Face | https://huggingface.co/datasets/ragibhasan/coke_studio_bangla_sentiment | Yes | No | apache-2.0 | configs `default`, `curated`; parquet 13.0 / 7.3 MB; last modified 2026-10-03 | **Not adequate for confirmatory use:** card declares `annotations_creators: machine-generated`, fields `sentiment_model`, `p_negative/p_neutral/p_positive`, `needs_review`; 55.7 % of comments are Latin/Banglish script. Silver labels from a model would measure agreement with another model, not accuracy. Updated two days ago (unstable). | HF API; card read |
| TanjimKIT/Bangla_Sentiments_in_eLearning | Bangla and romanised-Bangla e-learning comments, sentiment | Hugging Face | https://huggingface.co/datasets/TanjimKIT/Bangla_Sentiments_in_eLearning | Yes | No | apache-2.0 | `Elearning_Bangla.csv` 0.56 MB, `Elearning_Romanize.csv` 0.54 MB, `Combine_Main.csv` 0.95 MB; 1K-10K rows | Cites Rahman et al. 2024 (IEEE Access). Annotation process, label set and class balance **not shown** in the card; small; domain-specific. Usable as the Bangla classification cell only after an audit of the CSV, and it offers a second script-only contrast (Bangla vs romanised rows). | HF API; card read |
| tabularisai/swahili-sentiment-dataset | Swahili sentiment, 10K-100K rows | Hugging Face | https://huggingface.co/datasets/tabularisai/swahili-sentiment-dataset | Yes | No | apache-2.0 | `swahili_data.csv` 39.1 MB; tags `synthetic`, `synthetic data` | **Synthetic:** card cites Gyamfi et al. 2026, "Synthetic Data Generation Pipeline for Low-Resource Swahili Sentiment Analysis: Multi-LLM Judging with Human Validation" (AfricaNLP workshop). LLM-written text with LLM-judged labels is not native Swahili usage; usable only as a labelled exploratory set, not for a native-text claim. MasakhaNEWS is the better Swahili classification cell. | HF API; card read |
| momahadi/bangladesh-legal-qa-dataset | 2,165 context-grounded legal QA records (1,211 bn, 954 en) + statutory corpus of 6 Acts + 3 schedules; direct-answer and IRAC SFT files | Hugging Face | https://huggingface.co/datasets/momahadi/bangladesh-legal-qa-dataset | Yes | No | cc-by-4.0 | configs `audit`, `direct_answer`, `irac`; 30 files, 41 MB total; `law-corpus/bangla/*.json`, `qa-splits/*_bangla.json` | Organisational-domain bilingual extension (bn/en only). Free-text answers need an EM/F1 or option-scoring protocol; the companion 400-item Bar Council MCQ set is a separate repo (`momahadi/bangladesh-bar-council-exam-dataset`, licence tag `other`, source-rights notice). Associated paper arXiv 2608.30327 (Mahadi et al.) is the one the idea cites for language drift. | HF API; card read; arXiv abs |
| miracl/miracl | MIRACL topics and qrels, 16 languages; dev queries bn 411, sw 482, id 960, en 799 (card table) | Hugging Face | https://huggingface.co/datasets/miracl/miracl | Yes | No | apache-2.0 | `miracl-v1.0-{bn,sw,id,en}/topics/*.tsv` and `qrels/*.tsv`; 3.5 MB for the four languages; train/dev/test-a/test-b topics, dev and train qrels | Native-speaker queries and judgements ("the topics are generated by native speakers ... who also label the relevance"); negatives also human-annotated. Dev judged counts: bn 4,206, sw 5,092, id 9,668, en 8,350. Exactly what H4-H6 need; test qrels are not public. | HF API (files, sizes); card read; arXiv 2210.09984 |
| miracl/miracl-corpus | MIRACL passage collections (Wikipedia 2019-02 dumps, WikiExtractor passages) | Hugging Face | https://huggingface.co/datasets/miracl/miracl-corpus | Yes | No | apache-2.0 | bn 297,265 passages (`docs-0.jsonl.gz` 59.7 MB); sw 131,924 (10.2 MB); id 1,446,315 (3 files, 169.6 MB); en 32,893,221 (66 files, 5.06 GB) | Confirms the idea's passage counts. The **English control at full scale is out of reach** under both scenarios (32.9 M passages); cap en at the Indonesian tier (1.45 M nested sample with judged passages fixed). Wikipedia, not invoices or circulars. | HF API with `?blobs=true`; card table |
| castorini/mr-tydi | Mr. TyDi queries/qrels, 11 languages | Hugging Face | https://huggingface.co/datasets/castorini/mr-tydi | Yes | No | apache-2.0 | `mrtydi-v1.1-{bengali,swahili,indonesian,english}/` dev/test/train jsonl.gz + `ir-format-data/` topics and qrels; 86 MB total | Replication set for H4/H6 (dev and test qrels public). Sparse judgements (TyDi-derived), so Recall@100 is noisier than on MIRACL. | HF API (files, sizes); card read |
| castorini/mr-tydi-corpus | Mr. TyDi passage collections | Hugging Face | https://huggingface.co/datasets/castorini/mr-tydi-corpus | Yes | No | apache-2.0 | bengali 60.8 MB, swahili 10.7 MB, indonesian 172.7 MB, english 5.07 GB (gz) | Same Wikipedia provenance; per-language passage counts not shown in the card (the paper abstract page did not list them). English again too large for full-tier dense indexing. | HF API with `?blobs=true` |
| RaiyanKhaan/AgriTrust-RAG | Bengali agricultural advisory test collection (1,000 queries, 2,882 knowledge nodes per arXiv 2608.14886) | Hugging Face (claimed) | https://huggingface.co/datasets/RaiyanKhaan/AgriTrust-RAG | **No** (HTTP 401 "Invalid username or password" = repo does not exist or is private); `/api/datasets?search=AgriTrust` returned 0 results | n/a | not shown | not shown | Optional colloquial-vs-formal query analysis cannot be planned on it; treat as unavailable unless the authors publish. | HF API (401) and search (0 hits); arXiv abs 2608.14886 read |

### Models (Hugging Face API, `?blobs=true`, checked 2026-10-05)

| Repo | Params (safetensors `total`) | Licence tag | Gated | Quant files present (exact names) | Size of key files |
|---|---|---|---|---|---|
| Qwen/Qwen3-1.7B | 2,031,739,904 | apache-2.0 | No | n/a (safetensors; local GGUF conversion) | 4.06 GB bf16 safetensors |
| Qwen/Qwen3-1.7B-GGUF (official) | — | apache-2.0 | No | **only `Qwen3-1.7B-Q8_0.gguf`** | 1.83 GB |
| unsloth/Qwen3-1.7B-GGUF | — | apache-2.0 | No | `Qwen3-1.7B-BF16.gguf`, `-Q8_0`, `-Q6_K`, `-Q5_K_M`, `-Q4_K_M`, `-Q3_K_M`, `-Q2_K` (+ Q4_0/Q4_1/Q*_K_S, IQ*, UD-* dynamic quants) | BF16 3.45 GB; Q8_0 1.83 GB; Q6_K 1.42 GB; Q4_K_M 1.11 GB; Q3_K_M 0.94 GB; Q2_K 0.78 GB |
| bartowski/Qwen_Qwen3-1.7B-GGUF | — | (none) | No | `Qwen_Qwen3-1.7B-{bf16,Q8_0,Q6_K,Q4_K_M,Q3_K_M,Q2_K,...}.gguf` (imatrix quants) | Q4_K_M 1.28 GB vs unsloth 1.11 GB: **different recipes** (embedding/output precision), so uploader must be held constant or quantise locally |
| Qwen/Qwen3-4B | 4,022,468,096 | apache-2.0 | No | n/a | 8.05 GB bf16 |
| Qwen/Qwen3-4B-GGUF (official) | — | apache-2.0 | No | `Qwen3-4B-Q4_K_M`, `-Q5_0`, `-Q5_K_M`, `-Q6_K`, `-Q8_0` (**no Q3_K_M, Q2_K, BF16**) | Q8_0 4.28 GB; Q6_K 3.31 GB; Q4_K_M 2.50 GB |
| unsloth/Qwen3-4B-GGUF | — | apache-2.0 | No | `Qwen3-4B-BF16`, `-Q8_0`, `-Q6_K`, `-Q4_K_M`, `-Q3_K_M`, `-Q2_K` (+ others) | BF16 8.05 GB; Q3_K_M 2.08 GB; Q2_K 1.67 GB |
| Qwen/Qwen2.5-1.5B-Instruct | 1,543,714,304 | apache-2.0 | No | n/a | 3.09 GB |
| Qwen/Qwen2.5-1.5B-Instruct-GGUF (official) | — | apache-2.0 | No | `qwen2.5-1.5b-instruct-{fp16,q8_0,q6_k,q5_k_m,q5_0,q4_k_m,q4_0,q3_k_m,q2_k}.gguf` — full ladder | fp16 3.56 GB; q8_0 1.89 GB; q6_k 1.46 GB; q4_k_m 1.12 GB; q3_k_m 0.92 GB; q2_k 0.75 GB |
| Qwen/Qwen2.5-3B-Instruct | 3,085,938,688 | other (`license_name: qwen-research`) | No | n/a | 6.17 GB |
| Qwen/Qwen2.5-3B-Instruct-GGUF (official) | — | other (qwen-research) | No | fp16 (2 shards), q8_0, q6_k, q5_k_m, q5_0, q4_k_m, q4_0, q3_k_m, q2_k — full ladder | fp16 6.80 GB; q8_0 3.62 GB; q4_k_m 2.10 GB; q3_k_m 1.72 GB; q2_k 1.38 GB |
| google/gemma-3-4b-it (original) | 4,300,079,472 | gemma | **manual** | n/a | 8.6 GB |
| unsloth/gemma-3-4b-it-GGUF | — | gemma | No | `gemma-3-4b-it-BF16`, `-Q8_0`, `-Q6_K`, `-Q5_K_M`, `-Q4_K_M`, `-Q3_K_M`, `-Q2_K` (+ Q*_K_S, IQ*, UD-*, `mmproj-*` vision files) | BF16 7.77 GB; Q8_0 4.13 GB; Q6_K 3.19 GB; Q4_K_M 2.49 GB; Q3_K_M 2.10 GB; Q2_K 1.73 GB. Pipeline tag `image-text-to-text`; text-only use needs no mmproj |
| meta-llama/Llama-3.2-3B-Instruct (original) | 3,212,749,824 | llama3.2 | **manual** | n/a | 6.4 GB |
| unsloth/Llama-3.2-3B-Instruct-GGUF | — | llama3.2 | No | `Llama-3.2-3B-Instruct-BF16`, `-F16`, `-Q8_0`, `-Q6_K`, `-Q5_K_M`, `-Q4_K_M`, `-Q3_K_M`, `-Q2_K` (+ others) | BF16 6.43 GB; Q8_0 3.42 GB; Q6_K 2.64 GB; Q4_K_M 2.02 GB; Q3_K_M 1.69 GB; Q2_K 1.36 GB |
| md-nishat-008/TigerLLM-1B-it | 999,885,952 | cc-by-4.0 | No | none in repo; third-party `mradermacher/TigerLLM-1B-it-GGUF` and `Shojoy06/tigerllm-1b-gguf` exist (API search; files not inspected) | `model.safetensors` 2.0 GB (bf16) plus an unexplained `adapter_model.safetensors` 26 MB; `config.json` architecture `Gemma3ForCausalLM` (a Gemma-3-1B derivative tagged cc-by-4.0, see licence notes). ACL 2025 short paper (Crossref 10.18653/v1/2025.acl-short.69) |
| sarvamai/sarvam-1 | 2,525,087,744 | **no licence tag**; `LICENSE.md` = "Sarvam AI Research License" (research-only; other uses need Sarvam's permission) | No | none in repo; third-party `bartowski/sarvam-1-GGUF`, `QuantFactory/sarvam-1-GGUF`, `MaziyarPanahi/sarvam-1-GGUF`, `DevQuasar-3/sarvamai.sarvam-1-GGUF` exist (API search) | 5.05 GB; card: "a text-completion model ... cannot be used directly as a chat or an instruction-following model" and supports bn but not sw/id — it fits only as a bn-fertility/base-model contrast, not as an instruction-tuned cell |
| CohereLabs/tiny-aya-base (avoided) | 3,349,227,520 | cc-by-nc-4.0 | **auto** | n/a | correctly excluded by the idea |

### Encoders (Hugging Face API, checked 2026-10-05; all `gated: False`)

| Repo | Params | Licence | ONNX / int8 already published | Size of int8 file |
|---|---|---|---|---|
| intfloat/multilingual-e5-small | 117,654,272 | mit | `onnx/model.onnx` (fp32, 470 MB), `onnx/model_O4.onnx` (235 MB), **`onnx/model_qint8_avx512_vnni.onnx`** (118 MB) in the official repo; `Xenova/multilingual-e5-small` adds `model_int8`, `model_uint8`, `model_quantized`, `model_fp16`, `model_q4`, `model_bnb4` | 118 MB |
| intfloat/multilingual-e5-base | 278,044,162 | mit | official `onnx/model.onnx` (1.11 GB), `model_O4.onnx` (555 MB), **`model_qint8_avx512_vnni.onnx`** (279 MB); `Xenova/multilingual-e5-base` adds int8/uint8/quantized/fp16/q4 | 279 MB |
| sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 | 117,654,272 | apache-2.0 | official `onnx/model.onnx`, `model_O1..O4`, **`model_qint8_avx512_vnni`, `model_qint8_avx512`, `model_quint8_avx2`, `model_qint8_arm64`** (118 MB each); `Xenova/paraphrase-multilingual-MiniLM-L12-v2` adds int8/uint8/quantized | 118 MB |
| BAAI/bge-m3 | not shown (568 M per the idea) | mit | official `onnx/model.onnx` + `model.onnx_data` 2.27 GB (fp32 only); `Xenova/bge-m3` (mit) has `model_int8.onnx` 568 MB, `model_quantized`, `model_uint8`, `model_fp16` 1.13 GB, `model_q4`, plus `sentence_transformers_*` variants; `gpustack/bge-m3-GGUF` (mit) has `bge-m3-{FP16,Q8_0,Q6_K,Q5_K_M,Q4_K_M,Q3_K,Q2_K}.gguf` for llama.cpp embedding | int8 568 MB |
| onnx-community/multilingual-e5-small, onnx-community/bge-m3, intfloat/multilingual-e5-small-onnx | — | — | **do not exist** (HTTP 401) | — |

So no local ONNX export or quantisation is needed; every encoder in the design has a published int8 graph. One ISA caveat: the official `qint8_avx512_vnni` graphs target AVX-512 VNNI kernels; the i7-14700KF (Raptor Lake) has AVX2 and AVX-VNNI but **no AVX-512**, and a 4-vCPU cloud slice's ISA is unknown. onnxruntime falls back to AVX2 kernels for these graphs (correct results, lower speed), but the cleaner choice is `model_quint8_avx2.onnx` (MiniLM) or the Xenova `model_int8`/`model_uint8` dynamic-quant graphs, used identically on both machines. The int8 variant must be fixed in the preregistration.

### Licence notes
- Datasets: Belebele cc-by-sa-4.0 (share-alike on derived item sets); Global-MMLU and all MIRACL/Mr. TyDi repos apache-2.0; IndoNLU mit; MasakhaNEWS afl-3.0 (Academic Free License, permissive); XL-Sum and squad_bn **cc-by-nc-sa-4.0** (non-commercial, share-alike: fine for the paper, but the released "SME selection aid" must not bundle those items or be sold); the three sentiment sets and legal QA are apache-2.0 / cc-by-4.0.
- Models: Qwen3 and Qwen2.5-1.5B apache-2.0; Qwen2.5-3B-Instruct under the Qwen Research licence (`other`); gemma-3-4b-it under the Gemma Terms of Use and Llama-3.2-3B-Instruct under the Llama 3.2 Community License, both reached through ungated unsloth GGUF mirrors (`gated: False`) while the originals are `gated: manual`. Both licences permit evaluation and research but attach use-policy and attribution/redistribution conditions to derived artefacts (locally re-quantised GGUF files must not be republished without the licence text and prefix "Llama" naming rules; Gemma derivatives must carry the Gemma terms).
- **Two licence inconsistencies to resolve before use:** TigerLLM-1B-it is a `Gemma3ForCausalLM` checkpoint tagged cc-by-4.0, which cannot override the upstream Gemma terms; and sarvam-1 has no licence tag but a research-only LICENSE.md whose full text was read only in its first lines (derivative/redistribution clauses not shown). Both models can be evaluated locally; released artefacts derived from them should be limited to result tables.

---

## 2. Labels and measurements (adequacy for the intended claim)

- **Parallel items exist where the confirmatory hypotheses need them.** Belebele (900 items, FLORES passages human-translated and questions curated by human annotators per the card and the ACL 2024 paper) and Global-MMLU (14k items; or the human-translated Global-MMLU-Lite 400 items) are the only tasks where bn, sw, id and en share items; H1 (language x precision in decoders) and the RQ3 comparison should be restricted to them. The `ben_Latn` Belebele config gives a within-language script manipulation that the merged record does not use and that strengthens the "script, not language" reading of H1 considerably: the same Bangla items in Bengali and Latin script, same model, same precision.
- **Non-parallel task cells (sentiment/topic, squad_bn, XL-Sum, legal QA) differ in items, domain, label space and provenance across languages**, so they cannot carry a language x precision interaction; they support task-type moderation (exploratory) and the size x precision (H2) and fertility-cost (H3) hypotheses within a language. SmSA is 3-class native reviews; MasakhaNEWS is 7-class news topic; the Bangla and Swahili sentiment candidates are, respectively, model-labelled YouTube comments (ragibhasan), a small e-learning set with undocumented annotation (TanjimKIT), and a **synthetic LLM-generated** set (tabularisai). A human-labelled sentiment set parallel across bn/sw/id was not among the checked resources. Recommendation: use MasakhaNEWS (sw, en) and SmSA (id) as native classification cells, audit TanjimKIT's Bangla CSV (and use its romanised split as a second script control), and drop the synthetic Swahili and the machine-labelled Bangla sets from confirmatory analysis.
- **Translated versus native.** Belebele, Global-MMLU and squad_bn are translated; XL-Sum, SmSA, MasakhaNEWS, legal QA and MIRACL are native. The confirmatory interaction tests therefore run on translated items, and the paper must say so; the native cells show whether the direction replicates on native text.
- **Scoring.** Multiple-choice tasks should be scored by option log-likelihood (lm-evaluation-harness `belebele_*` and `global_mmlu_full_*` tasks exist for `ben_Beng`, `swh_Latn`, `ind_Latn`, `eng_Latn` and `bn`, `sw`, `id`, `en`; task-folder names confirmed via GitHub API). This makes the "3 seeded greedy runs" redundant for quality on MC tasks (deterministic); the three repeats are needed only for latency and throughput. Generation tasks (squad_bn F1, XL-Sum chrF/ROUGE-L, legal QA) need greedy decoding with a token cap; Qwen3 thinking mode must be disabled. XL-Sum has no bn/id/en task in the harness (the only `xlsum` tasks found are under `afrobench/` and `spanish_bench/`), so a custom task YAML is needed.
- **Summarisation without raters is weak by the idea's own citation**: Marchisio et al. report "a 1.7% average drop in Japanese across automatic tasks corresponds to a 16.0% drop reported by human evaluators" (abstract, arXiv 2407.03211). With no native-speaker raters, XL-Sum chrF/ROUGE-L is exploratory; a cheap partial remedy is to add refusal/empty-output and language-drift (script-mismatch) rates, which are measurable without raters and which Mahadi et al. 2026 report as the dominant failure mode in small models.
- **Retrieval labels are strong.** MIRACL dev qrels are native-speaker judgements with human-annotated negatives (card); dev query counts bn 411, sw 482, id 960, en 799 match the idea record. Nested corpus tiers must keep every judged passage (positive and negative) in every tier, as Wang et al. do; unjudged passages retrieved at small tiers will be scored as non-relevant, which biases nDCG downward more at small tiers — report judged@10 alongside nDCG@10.
- **Encoder quantisation (H5)** is measured by re-encoding the corpus with the int8 graph and comparing per-query nDCG@10 against the fp32 graph on the same queries: a paired design over 2,652 dev queries with language as a between-query factor; interaction power is adequate for differences of roughly 2 nDCG points.
- **Fertility (H3)** is computable offline from the tokenisers (tokens per character and per item) and is hardware-independent; the cost term "CPU-seconds per item" is hardware-dependent and must be reported with the exact CPU, thread count and memory bandwidth.
- **Statistics.** statsmodels (0.15.0 cp314 wheels on PyPI; 0.14.6 installed locally) provides `MixedLM` for linear mixed models and only a Bayesian variational `BinomialBayesMixedGLM` for logistic mixed models; a frequentist GLMM with random intercepts for items and models, as preregistered, needs R `lme4`/`glmmTMB` (R not probed) or a reformulation (conditional logistic / GEE with item clustering; item-level paired bootstrap with Holm). Decide before preregistration.

---

## 3. Compute and dependency assessment

### 3.1 Toolchain status (verified today)

| Component | Scenario A (4-core container) | Scenario B (local PC, Python 3.14.4) |
|---|---|---|
| torch | PyPI 2.14.1 (requires >=3.10; cp310-cp314 Linux/Windows wheels) | Installed: **torch 2.12.0+cpu, no CUDA**. CUDA wheels for Python 3.14 on Windows exist: `torch-2.14.1+cu130-cp314-cp314-win_amd64.whl` (and cu128 up to 2.11.0) on download.pytorch.org. Blackwell (sm_120) needs a CUDA >= 12.8 build (NVIDIA migration guide: "a PyTorch build with CUDA 12.8 is required"); cu130 satisfies that in principle. **Not verified**: that the cu130 wheel's arch list includes sm_120 and runs on this card (needs the reinstall and a `torch.cuda.get_arch_list()` check). |
| onnxruntime | 1.30.0 cp311-cp314 wheels (requires >=3.11) | Installed 1.28.0 CPU with `CPUExecutionProvider`; `onnxruntime-gpu 1.30.0` has a cp314 win wheel; GPU EP not needed (int8 encoders must run on CPU anyway). |
| sentence-transformers | 6.1.0 (py3, >=3.10) | Installed 5.6.0. |
| llama-cpp-python | 0.3.36 on PyPI is **sdist only** (source build needs CMake and a C++ toolchain; present on the earlier container per the idea-01 assessment) | **CMake and MSVC `cl.exe` not on PATH** today, so the PyPI sdist will not build as-is. GitHub release assets for v0.3.36 include `llama_cpp_python-0.3.36-py3-none-win_amd64.whl` under the `-cu124`, `-cu125`, `-cu130`, `-cu132`, `-vulkan` and `-hip-radeon` tags (a plain CPU v0.3.36 release was not among the 8 most recent listed; not shown). `py3-none` wheels are interpreter-version-agnostic (ctypes), so 3.14 should load them, but this was not tested; whether the cu130 wheel was compiled with sm_120 is not shown. |
| llama.cpp binaries | build from source (toolchain present on the container) | Prebuilt `llama-b11405-bin-win-cuda-13.4-x64.zip` and `-cuda-12.4-x64.zip` plus CPU builds published today (b11405, MIT). CUDA 12.4 cannot target sm_120; the 13.4 build should (CUDA 13 supports compute capability 12.0) but the arch list is not shown; the NVIDIA guide's fallback is a source build with `CMAKE_CUDA_ARCHITECTURES=...;120`. **nvcc is not installed locally.** The CPU build is sufficient for everything that must be on CPU. |
| lm-evaluation-harness | `lm_eval` 0.4.13 (py3, >=3.10); gguf/llama-cpp backend supports `loglikelihood` and `generate_until` (WebSearch) | same; Python 3.14 compatibility not verified. |
| BM25 | `bm25s` 0.3.12 (pure Python, numpy; optional numba and PyStemmer); `rank_bm25` 0.2.2 (2022, slow) | same; not installed yet. Snowball/PyStemmer language coverage for Swahili and Bengali not verified. |
| pyserini (Anserini baselines) | 2.4.0 requires Python >=3.12 **and Java 21**; sdist only | **Local Java is Temurin 17.0.19**, so pyserini needs a JDK 21 install; Windows build caveats reported. Optional: only needed to reproduce the published MIRACL BM25 numbers with Lucene analyzers. |
| statsmodels / sentencepiece | 0.15.0 / 0.2.2 wheels incl. cp314 | installed 0.14.6 / not checked |

### 3.2 Part A (generative factorial)

**Cell count as written.** 8 models x 6 precisions (bf16 + Q8_0, Q6_K, Q4_K_M, Q3_K_M, Q2_K) = 48 model-precision cells, each evaluated on 4 languages x the task set. Because MC scoring is deterministic, the "3 runs" apply to timing only (100-item timing subsets x 3 repeats), which removes a factor of three from the quality budget.

**Token budget per model-precision cell** (reduced plan applied: Global-MMLU 1,000 stratified items or Lite; sentiment/topic 500 items; squad_bn 500 items, bn only; XL-Sum 200 items with 1,024-token input cap and 80-token output; legal QA 500 items, bn/en only). Prefill tokens assume Qwen-family fertility of 1.0 (en), 1.2 (id), 1.4 (sw) and ~3.0 (bn) tokens per English-token equivalent (Bangla fertility is the quantity H3 measures; the 3x figure is an assumption consistent with Mahfuz et al.'s "inefficient Bengali tokenization", not a measurement):

| Task | Items x langs | Prefill tokens | Generated tokens |
|---|---|---|---|
| Belebele | 900 x 4 | ~1.8 M | ~11 k (4 options x ~3 tokens, cached prefix) |
| Global-MMLU (1,000 subsample) | 1,000 x 4 | ~0.8 M | ~12 k |
| Classification (SmSA, MasakhaNEWS swa/eng, Bangla set) | 500 x 4 | ~0.27 M | ~6 k |
| squad_bn | 500 x 1 | ~0.3 M | ~10 k |
| XL-Sum | 200 x 4 | ~0.82 M | ~64 k |
| Legal QA | 500 x 2 | ~0.8 M | ~30 k |
| **Per cell** | | **~4.8 M** | **~0.13 M** |
| **48 cells** | | **~230 M** (quant 192 M, bf16 38 M) | **~6 M** (quant 5 M, bf16 1 M) |

If Global-MMLU is run in full (14,042 x 4 languages x 48 cells), prefill rises by ~540 M tokens and more than doubles everything below; the idea record does not cap it, and it must.

**Throughput anchors (published, not measured here).** (i) A reproducible CPU-only Qwen3-4B benchmark on the Hub (`b4ph/qwen3-4b-lowram-bench`, 16 threads, CPU model not shown, llama-bench pp512/tg128): F16/BF16 357.6 / 2.52 t/s; Q8_0 1,355.9 / 5.04; Q6_K 1,523.2 / 5.93; Q4_K_M 2,064.8 / 6.50; Q3_K_M 2,142.5 / 6.56. (ii) A 4-core Xeon E5-2696 v4 post (llama.cpp v3770): Llama 3.1 8B Q4_K_M 3.2 t/s, Q8_0 2.1 t/s; Qwen 2.5 7B Q4_K_M 3.8 t/s; "memory bandwidth and capacity" the limit. (iii) OpenBenchmarking on an i7-14700K: Llama-3.1-Tulu-3-8B Q8_0 text generation 70.0 t/s, but via the **Vulkan** backend (GPU), so not a CPU anchor. From (i)-(ii), generation is bandwidth-bound (a 4B Q4 model at ~2.5 GB per token-step), prefill is compute-bound and scales with cores.

**Assumed speeds** (averaged over the 1-4 B models; stated so they can be replaced by a 1-hour `llama-bench` calibration on each machine):

| | Scenario A, 4 cores | Scenario B, 20 cores (28 threads) CPU | Scenario B, RTX 5070 Ti (bf16 only) |
|---|---|---|---|
| Quant prefill | ~500 t/s | ~2,500 t/s | (not used) |
| Quant generation | ~8 t/s | ~30 t/s (DDR5 bandwidth not measured) | (not used) |
| bf16 prefill | ~110 t/s | ~500 t/s | >5,000 t/s |
| bf16 generation | ~3 t/s | ~10 t/s | ~60-100 t/s |

**Hour estimates, single quality pass over 48 cells, reduced plan:**

| Component | Scenario A | Scenario B all-CPU | Scenario B, bf16 on GPU |
|---|---|---|---|
| Quant prefill 192 M | 107 h | 21 h | 21 h (CPU) |
| Quant generation 5 M | 174 h | 46 h | 46 h (CPU) |
| bf16 prefill 38 M | 96 h | 21 h | ~2 h (GPU) |
| bf16 generation 1 M | 93 h | 28 h | ~3 h (GPU) |
| Timing repeats (3 x 100 items x 48 cells x 4 langs, 4 threads) | ~15 h | ~15 h (must stay at 4 threads) | ~15 h (CPU) |
| Local GGUF conversion + quantisation (Qwen x4, TigerLLM, sarvam-1; 5 quants each) | ~6 h | ~2 h | ~2 h |
| **Total** | **~490 CPU-hours ≈ 3 weeks wall-clock** (sequential; llama.cpp saturates the 4 cores) | **~135 h ≈ 5.5 days** | **~85 CPU-hours ≈ 3.5 days**, GPU jobs (~5 h) run concurrently |

Trimming the model set to the four models that span the size and family contrasts (Qwen3-1.7B, Qwen3-4B, gemma-3-4b-it, Llama-3.2-3B-Instruct; 24 cells) halves these: ~250 h (10 days) under A, ~45 CPU-hours (2 days) under B with GPU bf16. Add roughly one week of engineering under either scenario (prompt-cache configuration, custom XL-Sum/legal-QA tasks, timing harness).

**RAM/disk.** Scenario A: largest resident is a 4B bf16 GGUF (8.05 GB) plus KV cache, inside 15 GB; GGUF files for 8 models x 6 precisions total roughly 90 GB if kept simultaneously, far over the ~30 GB disk, so models must be converted, evaluated and deleted one at a time (download bandwidth then matters). Scenario B: 626 GB free; all files can stay resident.

**What must stay on CPU for the CPU-only claim.** All throughput, latency, CPU-seconds-per-item and peak-RAM measurements (4 threads, pinned to P-cores on the i7); and, preferably, the quantised-quality runs themselves, because the deployment claim is about llama.cpp CPU kernels and GGUF dequantisation differs slightly between the CPU and CUDA backends. Quant quality on 20 cores uses the same kernels as on 4 cores (logits identical up to thread-order rounding), so the i7 can run them at full width. **What can move to the GPU**: the bf16 reference (8 GB fits in 16 GB VRAM with room for a 4k KV cache, via llama.cpp CUDA or transformers bf16), with a one-cell CPU-vs-GPU bf16 agreement check (expected within ~0.3 accuracy points) reported in the appendix. Caveat on portability: an i7-14700KF P-core at 5.5 GHz with DDR5 is 2-3x faster per core than a cloud 4-vCPU slice, so absolute latency figures from Scenario B overstate what an SME's 4-core box gets; the fertility-adjusted *relative* cost (bn/en ratio at equal precision, H3) is hardware-independent and should be the headline cost quantity, with absolute numbers reported per machine.

### 3.3 Part B (retrieval frontier)

**Encoding set.** bn 297,265 + sw 131,924 + id 1,446,315 = 1,875,504 passages, plus an English control capped at 1.45 M nested passages (the full 32.9 M English corpus is 5.06 GB compressed and infeasible for dense indexing in both scenarios) = **3.32 M passages**. Nested tiers are subsets of one full encode, so each encoder-precision combination encodes the corpus once: e5-small fp32/int8, e5-base fp32/int8, MiniLM fp32/int8 = 6 full encodes; bge-m3 restricted by the reduction plan to the two smallest tiers (say 10k and 50k per language = 240k passages).

**Throughput anchors.** Bekko (arXiv 2607.25180, via WebSearch) reports multilingual-e5-small at 226 documents/s on an x86 CPU via OpenVINO (CPU not shown); a Core Ultra OpenVINO figure of 20.4 sentences/s was also reported; "INT8 quantization provides 2-4x speed improvements". For GPUs, a search snippet gave "2,000-5,000+ short sentences/sec at batch_size=64" for an RTX 5070 with sentence-transformers (model not stated). Passages (~200 tokens, max_seq 256) are longer than those sentences, so the assumptions below are discounted.

| | Scenario A, 4 cores | Scenario B, 20 cores CPU | Scenario B, RTX 5070 Ti fp16 |
|---|---|---|---|
| e5-small / MiniLM fp32 | ~50 passages/s | ~250/s | ~1,500/s |
| e5-small / MiniLM int8 | ~110/s | ~500/s | (CPU only, by design) |
| e5-base fp32 | ~18/s | ~90/s | ~600/s |
| e5-base int8 | ~40/s | ~180/s | (CPU only) |
| bge-m3 fp32/fp16 | ~5/s | ~25/s | ~200/s |

**Hour estimates:**

| Component | Scenario A | Scenario B (GPU for fp32/fp16, CPU for int8) |
|---|---|---|
| e5-small fp32 + MiniLM fp32 (2 x 3.32 M) | 37 h | 1.2 h GPU |
| e5-small int8 + MiniLM int8 | 17 h | 3.7 h CPU |
| e5-base fp32 | 51 h | 1.5 h GPU |
| e5-base int8 | 23 h | 5.1 h CPU |
| bge-m3, two smallest tiers (240 k) | 13 h | 0.3 h GPU (full 3.32 M would be ~4.6 h GPU, so the tier restriction can be lifted under B) |
| BM25 variants (whitespace, analyzer, char n-gram, SentencePiece subwords, RM3) with bm25s; SentencePiece training on id | ~5 h | ~2 h |
| nDCG/Recall evaluation: ~40 configs x 2,652 dev queries, brute-force inner product over up to 1.45 M x 768 fp32 (4.4 GB) | ~9 h | <1 h (GPU matmul) |
| Latency p50/p95, 3 repeats, full tier, ~7 dense + 5 lexical + hybrids, **4 threads on CPU** | ~6 h | ~6 h (4 threads) |
| Mr. TyDi replication (bn/sw/id dev+test; corpora of similar size to MIRACL's, counts not shown) | +50-70 % of the above | +1 day |
| **Total (MIRACL only)** | **~160 CPU-hours ≈ 7 days**, RAM fine (4.4 GB matrices), **disk tight**: fp32 embeddings for the six combinations are ~41 GB, so store fp16 (~20 GB) or process one language at a time and delete | **~8 h GPU + ~17 h CPU ≈ 1.5-2 days wall-clock**; disk trivial |

**What must stay on CPU in Part B.** The int8 ONNX encoders (the published int8 graphs are CPU-kernel quantisations; "int8 on GPU" would be a different model), and every latency/CPU-seconds/peak-RAM measurement (4 threads). The fp32 reference embeddings can be computed on the GPU in fp32 (numerically equivalent to CPU fp32 to ~1e-5 cosine) or fp16; the clean choice for H5 is GPU **fp32**, with one language re-encoded on CPU fp32 as an agreement check. BM25 indexing is CPU in both scenarios (bm25s is numpy-only). The nested-tier evaluation (nDCG, Recall) can use GPU brute-force search because it does not produce the cost measurements.

### 3.4 Totals and verdict on scale

- **Scenario A:** Part A ~490 CPU-hours (~3 weeks) or ~250 h with four models; Part B ~160 CPU-hours (~1 week); plus ~1.5 weeks engineering: **the joint design is 5-7 weeks of continuous 4-core time with the reduction plan, and infeasible without it** (full Global-MMLU, bge-m3 at all tiers and the full English corpus would add months). Disk (30 GB) forces streaming of GGUF files and embeddings.
- **Scenario B:** Part A ~85 CPU-hours with bf16 on the GPU (~3.5 days; ~2 days with four models), Part B ~2 days, engineering ~1 week: **the joint design is roughly 2-3 weeks wall-clock and is measured in days of compute, not weeks.** The GPU removes the two components the idea's own risk section calls out (bf16 4B inference "a few tokens per second" and bge-m3 on 1.4 M Indonesian passages "takes days"), while every cost measurement that the CPU-only claim depends on still runs on the CPU at 4 threads.
- **Scenario B unverified items** that could cost a day or two: installing a CUDA torch build for Python 3.14 (wheel exists; sm_120 behaviour untested), obtaining a Blackwell-capable llama.cpp CUDA binary (cuda-13.4 prebuilt likely; nvcc absent for a source build), llama-cpp-python wheel loading under 3.14 (or use the llama.cpp server with lm-eval's `local-completions`-style backend), and Java 21 for pyserini (optional).

### 3.5 Does the method need an LLM or embeddings?

Yes by construction. Part A's object of study is 1-4 B decoders (no LLM-as-judge anywhere; scoring is log-likelihood, EM/F1, chrF/ROUGE). Part B's dense arms need the 118-568 M encoders. The **non-neural variant** is the lexical half of Part B: tokenisation-aware BM25 (whitespace vs analyzer vs character n-grams vs SentencePiece subwords vs RM3) across nested corpus tiers for bn/sw/id/en, testing H4 and the lexical half of H6 with no neural model at all; that variant runs in a few CPU-hours under either scenario and is a publishable reproducibility-track result on its own (MIRACL's Anserini BM25 baselines are the comparison point). Paid APIs are not needed anywhere.

---

## 4. Approvals and ethics

- No human participants, surveys, interviews or private data: all datasets are public research releases (Wikipedia passages, translated benchmarks, BBC summaries, public legal statutes, public YouTube comments in the one machine-labelled set). **No IRB/ethics approval is required.** The absence of native-speaker raters is a validity limitation (Section 2), not an approval issue.
- Licence compliance: cite every dataset; keep cc-by-nc-sa items (XL-Sum, squad_bn) out of any redistributed artefact and out of commercial use; honour share-alike on Belebele-derived item files; the released configuration tables and result tables are unaffected.
- Model terms: Gemma and Llama 3.2 permit evaluation and research publication; derived GGUF files re-quantised locally should not be redistributed without the licence text and naming/attribution requirements; sarvam-1 (Sarvam AI Research License) and Qwen2.5-3B (Qwen Research) are research-only. TigerLLM-1B-it's cc-by-4.0 tag conflicts with its Gemma-3 architecture and should be queried with the authors or treated as Gemma-licensed.
- The YouTube-comment sentiment set contains author identifiers (`author_id`) and raw text; if used at all, drop identifiers and do not redistribute.
- Content risk is low: outputs are option letters, short answers and summaries of news; the legal QA domain is public statute, not case files.

---

## 5. What the design can and cannot claim

**Can claim (internally valid under both scenarios):**
- For each tested model, the causal effect of GGUF precision on quality for bn, sw, id and en on **identical items** (Belebele, Global-MMLU), with paired item-level intervals, and the script-only effect via `ben_Beng` vs `ben_Latn`; whether the language x precision interaction exists at 1-4 B under k-quantisation down to Q2_K — the cell that Marchisio et al. (8B-103B, GPU quantisers), Borgersen and Goodwin (one 70B model, en/no, GGUF; "all experiments ... yielded non-significant results"), Marie and Fujita (MT only, 55 languages, 1.7B-70B; "GGUF variants provide the most consistent performance, even at 2-bit") and Hossain et al. (7B-20B, 8-bit, Bangla NLU; "architecture and quantization method matters more than the bit width") leave open. All four abstracts were read today and confirm the gap as the idea states it.
- Fertility-adjusted relative cost per item (bn vs en) at each precision, hardware-independent, plus absolute CPU latency on a stated machine.
- A cost-annotated lexical-vs-dense frontier for bn/sw/id (and a capped en control) on human-judged MIRACL dev queries, with the int8-vs-fp32 encoder contrast and the corpus-tier crossover, replicating Wang et al.'s English scaling result (arXiv 2607.26497, "around 10 million corpus tokens, BM25 overtakes") in three non-English settings.
- The RQ3 comparison of standardised interaction estimates across decoders and encoders, as a descriptive joint result.

**Cannot claim (or must be scoped):**
- Anything about human-perceived quality of generation: automatic summarisation metrics understate harm by an order of magnitude in Marchisio et al.; XL-Sum and legal QA free-text results are exploratory.
- "Bangla organisational text": the confirmatory items are translated (Belebele, Global-MMLU) or Wikipedia (MIRACL); the native cells are reviews, news and statutes. No invoices, circulars or forms are in any resource.
- English at full corpus scale in Part B (capped at 1.45 M passages), and bge-m3 at full tiers under Scenario A.
- Equivalence of ungated GGUF mirrors with the gated originals for gemma and llama: the quant recipes of unsloth vs bartowski differ visibly in file size (Q4_K_M 1.11 vs 1.28 GB for Qwen3-1.7B), so cross-model comparisons must hold the recipe constant (local `llama-quantize` without imatrix for all ungated originals; unsloth plain `Q*_K_M` files for the two gated families, with the recipe difference stated).
- A null language x precision interaction as a point null: it must be an equivalence claim with a preregistered margin (about 2-3 points on Belebele per model, ~1.5 pooled).
- If bf16 small models sit near chance on Bangla Global-MMLU (plausible for 1.5-1.7 B models), the degradation headroom there vanishes; Belebele (passage-grounded) is the safer confirmatory task.
- The Saragih et al. ICADEIS 2026 paper named in the undermining-evidence field could not be located by WebSearch today (ICADEIS 2026 is scheduled for 12-13 November 2026); Indonesian cannot yet be ruled in or out of Part B on that basis.
- Scope: Part A and Part B each have the size of a full paper; the companion-paper split the idea anticipates is the realistic publication plan.

---

## 6. Blockers

1. **Compute under Scenario A exceeds a reasonable budget unless both the reduction plan and a model-set cut are applied**: ~650 CPU-hours (≈ 5-7 weeks of sequential 4-core time) for the joint design; ~400 h with four models. Disk (30 GB) cannot hold the GGUF ladder or the fp32 embeddings simultaneously. This is a design-reduction and scheduling problem, not an acquisition problem, and it disappears under Scenario B.
2. **Scenario B software stack is unverified for Python 3.14 + Blackwell**: local torch is CPU-only; a cu130 cp314 wheel exists but sm_120 operation is untested; no CMake/MSVC/nvcc on PATH (so llama-cpp-python must come from a prebuilt `py3-none-win_amd64` wheel or the llama.cpp server binaries); lm_eval under 3.14 untested. Expect 1-2 days of setup; a Python 3.12 virtual environment would remove most of the uncertainty.
3. **Sentiment cells**: the Swahili set is synthetic and the Bangla YouTube set is machine-labelled; both are unfit for confirmatory use. Use MasakhaNEWS and SmSA as native classification cells, audit TanjimKIT, and move sentiment to exploratory.
4. **Global-MMLU must be subsampled or replaced by Global-MMLU-Lite** (bn, sw, id, en configs confirmed); XL-Sum needs a custom harness task; the IndoNLU repo is script-based.
5. **Model-set hygiene**: Qwen3-1.7B official GGUF has only Q8_0 and Qwen3-4B official lacks Q3_K_M/Q2_K/BF16, so Qwen ladders must be quantised locally (planned); TigerLLM-1B-it licence conflict and stray adapter file; sarvam-1 is a base model that cannot follow instructions and supports bn only; the design should either drop sarvam-1 or use it solely for the fertility/base-model contrast.
6. **Statistics tooling**: no frequentist logistic GLMM in statsmodels; preregister either R `lme4` or a clustered/paired-bootstrap alternative.
7. **AgriTrust-RAG does not exist on the Hub** (401; search returns nothing); drop the colloquial-vs-formal analysis or source it elsewhere.
8. **pyserini** (optional Anserini reproduction) needs Java 21 (local JDK is 17) and Python >= 3.12.

None is a hard blocker under Scenario B; items 1 and the disk limit are hard constraints under Scenario A that force the companion-paper split and a four-model Part A.

---

## 7. Verdict

**Part A (generative factorial): feasible-but-slow-on-cpu under Scenario A; feasible-now under Scenario B.**
Every dataset is reachable, ungated and licensed for research; every decoder has an ungated GGUF ladder (official, unsloth or locally quantised); the harness has the Belebele and Global-MMLU tasks in all four languages; the measurement (option log-likelihood on parallel items) supports the preregistered interaction tests, and `ben_Latn` adds a free script-only control. The cost is the problem under Scenario A: ~490 CPU-hours for the 48-cell single pass with the reduction plan (3 weeks), ~250 h with four models. Under Scenario B the same pass is ~85 CPU-hours with bf16 on the RTX 5070 Ti (3.5 days), and all cost measurements still run on the CPU at 4 threads, which is the quantity the CPU-only claim needs.

**Part B (retrieval frontier): feasible-but-slow-on-cpu under Scenario A; feasible-now under Scenario B.**
MIRACL and Mr. TyDi topics, qrels and corpora are present with the stated passage counts; all four encoders have published int8 ONNX graphs (no local quantisation); bm25s gives a Java-free BM25 with custom tokenisation. Scenario A needs ~160 CPU-hours and careful disk management; Scenario B does the fp32/fp16 encodes in ~8 GPU-hours, the int8 encodes in ~9 CPU-hours and the 4-thread latency sweep in ~6 h, so the whole frontier is about two days, and the bge-m3 tier restriction can be lifted. The English control must be capped at 1.45 M passages in both scenarios.

**Joint paper (RQ3): feasible-but-slow-on-cpu under Scenario A (5-7 weeks of compute plus engineering, and only with the reduction plan and a four-model Part A); feasible-now under Scenario B (2-3 weeks wall-clock including setup), with the caveat that the merged scope is two papers' worth of results and should be written as the quantisation factorial plus a companion reproducibility-track retrieval paper citing shared hypotheses.** Claim support is adequate for the exact-match and human-judged-retrieval hypotheses (H1, H2, H3, H4, H5, H6) and inadequate for any human-perceived generation-quality statement, which the design already routes to exploratory status.

**Reference check (arXiv abstract pages read today; Crossref where a DOI was known):**
- "How Does Quantization Affect Multilingual LLMs?" — Marchisio, Dash, Chen, Aumiller, Üstün, Hooker; arXiv 2407.03211; Crossref 10.18653/v1/2024.findings-emnlp.935, Findings of EMNLP 2024 (peer-reviewed).
- "English K_Quantization of LLMs Does Not Disproportionately Diminish Multilingual Performance" — Borgersen and Goodwin; arXiv 2503.03592 (v1-v4; venue not shown).
- "The Uneven Impact of Post-Training Quantization in Machine Translation" — Marie and Fujita; arXiv 2508.20893 (2025-08-28; venue not shown).
- "Quantization Effects on Bangla Language Understanding in Large Language Models: A Systematic Evaluation" — Hossain, Shafin, Al Mumin; arXiv 2608.24615 (2026-08-25; preprint; models Qwen-2.5-7B, LLaMA-3.1-8B, GPT-OSS-20B; formats GPTQ-Int8, GPTQ-Q8, GGUF-W8A16; lm-evaluation-harness zero-shot).
- "Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages" — Zhang et al.; arXiv 2210.09984; the card links TACL doi 10.1162/tacl_a_00595 (Crossref returned a non-JSON body today; not re-verified).
- "Mr. TyDi: A Multi-lingual Benchmark for Dense Retrieval" — Zhang, Ma, Shi, Lin; arXiv 2108.08787 (2021).
- "BM25 Wins at Scale: A Scaling Study of Retrieval-Augmented Generation Paradigms" — Wang et al.; arXiv 2607.26497 (WebSearch; abstract snippet confirms the 28 nested tiers and the ~10 M-token crossover).
- "Where Does Retrieval Fail? Evaluating RAG Architectures for Agricultural Advisory" — Reza, Maria, Nimi; arXiv 2608.14886 (2026-08-14; abstract confirms 1,000 queries, 2,882 nodes, BM25 R@10 0.506 vs hybrid 0.539; dataset repo not on the Hub).
- "Do Small Models Use the Law You Give Them?" — Mahadi et al.; arXiv 2608.30327 (2026-08-31; the legal-QA dataset's associated paper).
- "The Belebele Benchmark" — Bandarkar et al.; arXiv 2308.16884; Crossref 10.18653/v1/2024.acl-long.44 (ACL 2024). "Global MMLU" — Singh et al.; arXiv 2412.03304. "TigerLLM" — Raihan and Zampieri; Crossref 10.18653/v1/2025.acl-short.69 (ACL 2025 short).
- Not located: "Are LLM-Based Retrievers Worth Their Cost?" (Abdallah et al.), "Calibrating Beyond English" (Chimoto et al.) and the Saragih et al. ICADEIS 2026 paper were not searched or not found today; the idea record's descriptions of them are unverified here.

---

## 8. Minimum change in resources that would unblock the full design

Under Scenario A the single change is **the machine the author already owns**: moving to Scenario B turns a 5-7-week sequential CPU plan into a 2-3-week one with days of compute, because the 16 GB GPU absorbs the bf16 references (~190 of the ~490 Part A CPU-hours) and all fp32/fp16 corpus encoding (~100 of the ~160 Part B CPU-hours), while the 20-core CPU runs the quantised cells and int8 encoders 4-5x faster and still provides a 4-thread configuration for the deployment-cost measurements. Nothing else needs to be bought. Under Scenario B the remaining unblockers are setup, not resources: a CUDA-enabled torch for Python 3.14 (or a Python 3.12 environment), a Blackwell-capable llama.cpp CUDA binary (prebuilt cuda-13.4 build, or CUDA Toolkit 12.8+ with CMake for a source build), and, optionally, JDK 21 for pyserini. The one resource that no hardware change supplies is **native-speaker raters** (two per language, ~200 summaries each, roughly 40 rater-hours in total); adding them is the only way to promote the summarisation and legal-QA cells from exploratory to confirmatory and to test the Marchisio et al. automatic-versus-human gap directly for Bangla.
