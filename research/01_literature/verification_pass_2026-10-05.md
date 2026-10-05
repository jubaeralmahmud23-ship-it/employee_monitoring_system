# Identifier-based verification of evidence tables (2026-10-05)

Method: see `research/tools/verify_evidence_tables.py`. Flags are prompts for a human check, not verdicts: a `year-near` flag usually means a preprint and its published version differ by one year; `venue-not-in-citation` means no informative word of the Crossref container title appears in the Citation cell (abbreviations such as QJE or ISR trigger it); `labelled-preprint-but-DOI-is-published-version` and `arxiv-lists-published-version` mean the row should name the published version.


## research/01_literature/agents-bpm-process-mining.md

Rows: 41 · rows with a DOI or arXiv id: 38 · rows with flags: 9 · rows without identifier: 3

| line | citation (start) | API findings | flags |
|---|---|---|---|
| 59 | Grohs, Abb, Elsayed and Rehse, 2023, BPM 2023 Workshops (NLP4BPM; LNBIP, Crossref year 2024), peer-reviewed workshop | DOI 10.1007/978-3-031-50974-2_34: 2024 · Lecture Notes in Business Information Processing · book-chapter · "Large Language Models Can Accomplish Business Process Management Tasks"<br>arXiv 2307.09923: first v 2023-07-19 · jref "" · doi - · "Large Language Models can accomplish Business Process Management Tasks" | year-near(2023 vs 2024) |
| 61 | Kourani, Berti, Schuster and van der Aalst, 2026 (online 2025), Software and Systems Modeling, peer-reviewed | DOI 10.1007/s10270-025-01318-w: 2025 · Software and Systems Modeling · journal-article · "Evaluating large language models on business process modeling: framework, benchmark, and s"<br>arXiv 2412.00023: first v 2024-11-17 · jref "" · doi - · "Evaluating Large Language Models on Business Process Modeling: Framework, Benchmark, and S" | year-near(2026 vs 2025) |
| 70 | Drouin, Gasse, Caccia, Laradji, Del Verme, Marty et al. (12 authors), 2024, ICML 2024 (per Semantic Scholar venue and the PyPI README; Cross | arXiv 2403.07718: first v 2024-03-12 · jref "" · doi - · "WorkArena: How Capable Are Web Agents at Solving Common Knowledge Work Tasks?" | peer-reviewed-label-rests-on-arxiv-only |
| 71 | Huang, Prabhakar, Thorat, Agarwal, Choubey, Mao et al. (9 authors), 2025 (arXiv v1, May 2025; no journal reference on arXiv), Transactions o | arXiv 2505.18878: first v 2025-05-24 · jref "" · doi - · "CRMArena-Pro: Holistic Assessment of LLM Agents Across Diverse Business Scenarios and Inte" | peer-reviewed-label-rests-on-arxiv-only |
| 78 | Dumas, Milani and Chapela-Campa, "Agentic Business Process Management Systems", BPM 2025 Workshops (AI4BPM keynote paper), LNBIP, DOI 10.100 | DOI 10.1007/978-3-032-13426-4_1: 2026 · Lecture Notes in Business Information Processing · book-chapter · "Agentic Business Process Management Systems"<br>arXiv 2601.18833: first v 2026-01-25 · jref "" · doi - · "Agentic Business Process Management Systems" | year-near(2025 vs 2026) |
| 81 | Berti, Kourani, Hafke, Li and Schuster, "Evaluating Large Language Models in Process Mining: Capabilities, Benchmarks, and Evaluation Strate | DOI 10.1007/978-3-031-61007-3_2: 2024 · Lecture Notes in Business Information Processing · book-chapter · "Evaluating Large Language Models in Process Mining: Capabilities, Benchmarks, and Evaluati"<br>arXiv 2403.06749: first v 2024-03-11 · jref "" · doi 10.1007/978-3-031-61007-3_2 · "Evaluating Large Language Models in Process Mining: Capabilities, Benchmarks, and Evaluati" | venue-not-in-citation |
| 82 | Kourani, Berti, Schuster and van der Aalst, "Process Modeling with Large Language Models", BPMDS 2024, DOI 10.1007/978-3-031-61007-3_18; arX | DOI 10.1007/978-3-031-61007-3_18: 2024 · Lecture Notes in Business Information Processing · book-chapter · "Process Modeling with Large Language Models"<br>arXiv 2403.07541: first v 2024-03-12 · jref "" · doi 10.1007/978-3-031-61007-3_18 · "Process Modeling With Large Language Models" | venue-not-in-citation |
| 88 | Padella, Frazzetto, Navarin and de Leoni, "Enhancing Predictive Process Monitoring on Small-Scale Event Logs Using LLMs", BPM 2025 Forum, DO | DOI 10.1007/978-3-032-02929-4_16: 2025 · Lecture Notes in Business Information Processing · book-chapter · "Enhancing Predictive Process Monitoring on Small-Scale Event Logs Using LLMs" | venue-not-in-citation |
| 96 | Barbieri, Stroeh, Madeira and van der Aalst, "An LLM-Based Q&A Natural Language Interface to Process Mining", ICPM 2024 Workshops, DOI 10.10 | DOI 10.1007/978-3-031-82225-4_1: 2025 · Lecture Notes in Business Information Processing · book-chapter · "An LLM-Based Q&amp;A Natural Language Interface to Process Mining" | venue-not-in-citation, year-near(2024 vs 2025) |

Rows whose identifiers resolved with no flags (line numbers): 57, 58, 60, 62, 63, 64, 65, 66, 67, 68, 69, 72, 79, 80, 83, 84, 85, 86, 87, 89, 90, 91, 92, 93, 94, 95, 97, 100, 101

Rows without a DOI or arXiv id (check by title with verify_refs.py):

- line 76: Item
- line 98: Laerum and Nüttgens, "Financial Process Mining In The Age Of Large Language Models", ECIS 2026 Proceedings paper 4 (entmodel)
- line 99: Göldi and Rietsche, "Making Sense of Large Language Model-Based AI Agents", ICIS 2024 Proceedings paper 16 (aiinbus)

## research/01_literature/decision-support-analytics.md

Rows: 32 · rows with a DOI or arXiv id: 26 · rows with flags: 5 · rows without identifier: 6

| line | citation (start) | API findings | flags |
|---|---|---|---|
| 66 | Lei et al. (16 authors), 2025, ICLR 2025 (Oral; OpenReview XmProj9cPs, venue "ICLR 2025 Oral"; DBLP conf/iclr/LeiCYCSSSGHYZX025), peer-revie | arXiv 2411.07763: first v 2024-11-12 · jref "" · doi - · "Spider 2.0: Evaluating Language Models on Real-World Enterprise Text-to-SQL Workflows" | peer-reviewed-label-rests-on-arxiv-only |
| 69 | Liu et al. (10 authors), 2025, IEEE TKDE (DOI 10.1109/TKDE.2025.3592032; arXiv v7 updated 2026-08-25), peer-reviewed | DOI 10.1109/TKDE.2025.3592032: 2025 · IEEE Transactions on Knowledge and Data Engineering · journal-article · "A Survey of Text-to-SQL in the Era of LLMs: Where Are We, and Where Are We Going?"<br>arXiv 2408.05109: first v 2024-08-09 · jref "TKDE July 2025" · doi 10.1109/TKDE.2025.3592032 · "A Survey of Text-to-SQL in the Era of LLMs: Where are we, and where are we going?" | venue-not-in-citation |
| 79 | Sahu et al. (14 authors), 2025, ICLR 2025 Poster (InsightBench; per the arXiv comment and OpenReview ZGqd0cbBvm, venue "ICLR 2025 Poster"; C | arXiv 2407.06423: first v 2024-07-08 · jref "" · doi - · "InsightBench: Evaluating Business Analytics Agents Through Multi-Step Insight Generation" | peer-reviewed-label-rests-on-arxiv-only |
| 86 | Luo, Li, Fan, Chai, Tang, "Natural Language to SQL: State of the Art and Open Problems", PVLDB 2025, DOI 10.14778/3750601.3750696 | DOI 10.14778/3750601.3750696: 2025 · Proceedings of the VLDB Endowment · journal-article · "Natural Language to SQL: State of the Art and Open Problems" | venue-not-in-citation |
| 94 | "The Dawn of Natural Language to SQL" predecessor "Natural language to SQL" (Kim et al.?), PVLDB 2020, DOI 10.14778/3401960.3401970 | DOI 10.14778/3401960.3401970: 2020 · Proceedings of the VLDB Endowment · journal-article · "Natural language to SQL" | venue-not-in-citation |

Rows whose identifiers resolved with no flags (line numbers): 65, 67, 68, 70, 71, 72, 73, 74, 75, 76, 77, 78, 80, 87, 88, 89, 96, 97, 98, 99, 100

Rows without a DOI or arXiv id (check by title with verify_refs.py):

- line 84: Item
- line 90: Parra-Moyano, Reinmoeller and Schmedders, "Research: Executives Who Used Gen AI Made Worse Predictions", Harvard Business Review digital art
- line 91: "Revisiting LLMs as Zero-Shot Time Series Forecasters: Small Noise Can Break Large Models", ACL 2025 short (aclanthology 2025.acl-short.71)
- line 92: "Calibrating LLMs for Text-to-SQL Parsing by Leveraging Sub-clause Frequencies", EMNLP 2025 (2025.emnlp-main.859)
- line 93: "Text-to-SQL Benchmarks are Broken: An In-Depth Analysis of Annotation Errors", CIDR 2026
- line 95: MMQA: multi-table, multi-hop QA benchmark, ICLR 2025 (OpenReview qResKYUOTf)

## research/01_literature/efficiency-privacy-low-resource.md

Rows: 16 · rows with a DOI or arXiv id: 14 · rows with flags: 0 · rows without identifier: 2


Rows whose identifiers resolved with no flags (line numbers): 58, 59, 60, 61, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73

Rows without a DOI or arXiv id (check by title with verify_refs.py):

- line 62: Kasigit, Akhlaghpour, Karanasios 2025, ACIS 2025 (Australasian Conference on Information Systems), peer-reviewed conference
- line 63: Mohammed, Kutar, Albakri 2025, UKAIS 2025 (UK Academy for Information Systems), peer-reviewed conference

## research/01_literature/evaluation-validity-safety.md

Rows: 34 · rows with a DOI or arXiv id: 30 · rows with flags: 12 · rows without identifier: 4

| line | citation (start) | API findings | flags |
|---|---|---|---|
| 60 | Liu, Jia, Geng, Jia, Gong, 2024, USENIX Security 2024, peer-reviewed | arXiv 2310.12815: first v 2023-10-19 · jref "" · doi - · "Formalizing and Benchmarking Prompt Injection Attacks and Defenses" | peer-reviewed-label-rests-on-arxiv-only |
| 63 | Ye, Wang, Huang, Chen et al., 2025 (arXiv 2024), ICLR 2025, peer-reviewed | arXiv 2410.02736: first v 2024-10-03 · jref "" · doi - · "Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge" | peer-reviewed-label-rests-on-arxiv-only |
| 64 | Li, Sun, Huang, Zhong et al. (author list corrected in the 2026-10-03 citation audit from the arXiv API: Dawei Li, Renliang Sun, Yue Huang,  | DOI 10.18653/v1/2025.findings-emnlp.510: 2025 · Findings of the Association for Computational Linguistics: EMNLP 2025 · proceedings-article · "Assistant-Guided Mitigation of Teacher Preference Bias in LLM-as-a-Judge"<br>arXiv 2502.01534: first v 2025-02-03 · jref "" · doi - · "Preference Leakage: A Contamination Problem in LLM-as-a-judge" | venue-not-in-citation, year-near(2026 vs 2025) |
| 65 | Tan, Zhuang, Montgomery, Tang et al., 2025 (arXiv 2024), ICLR 2025, peer-reviewed | arXiv 2410.12784: first v 2024-10-16 · jref "" · doi - · "JudgeBench: A Benchmark for Evaluating LLM-based Judges" | peer-reviewed-label-rests-on-arxiv-only |
| 67 | Dominguez-Olmedo, Dorner, Hardt, 2025 (arXiv 2024), ICLR 2025, peer-reviewed | arXiv 2407.07890: first v 2024-07-10 · jref "" · doi - · "Training on the Test Task Confounds Evaluation and Emergence" | peer-reviewed-label-rests-on-arxiv-only |
| 69 | Sharma, Tong, Korbak, Duvenaud et al., 2024 (arXiv 2023), ICLR 2024, peer-reviewed | arXiv 2310.13548: first v 2023-10-20 · jref "" · doi - · "Towards Understanding Sycophancy in Language Models" | peer-reviewed-label-rests-on-arxiv-only |
| 74 | Atil, Aykent, Chittams, Fu et al. (13 authors on arXiv v5, 2025-04-02; arXiv v1, 2024-08-06, listed six: Atil, Chittams, Fu, Ture, Xu, Baldw | DOI 10.18653/v1/2025.eval4nlp-1.12: 2025 · Proceedings of the 5th Workshop on Evaluation and Comparison of NLP Systems · proceedings-article · "Non-Determinism of “Deterministic” LLM System Settings in Hosted Environments"<br>arXiv 2408.04667: first v 2024-08-06 · jref "" · doi - · "Non-Determinism of "Deterministic" LLM Settings" | labelled-preprint-but-DOI-is-published-version |
| 84 | Bowyer, Aitchison, Ivanova, "Position: Don't Use the CLT in LLM Evals With Fewer Than a Few Hundred Datapoints", ICML 2025 position paper (c | arXiv 2503.01747: first v 2025-03-03 · jref "" · doi - · "Position: Don't Use the CLT in LLM Evals With Fewer Than a Few Hundred Datapoints" | peer-reviewed-label-rests-on-arxiv-only |
| 90 | Xu et al., "Benchmark Data Contamination of Large Language Models: A Survey", 2024, arXiv 2406.04244, preprint (Crossref offered a CONDA 202 | DOI 10.18653/v1/2024.conda-1.3: 2024 · Proceedings of the 1st Workshop on Data Contamination (CONDA) · proceedings-article · "A Taxonomy for Data Contamination in Large Language Models"<br>arXiv 2406.04244: first v 2024-06-06 · jref "" · doi - · "Benchmark Data Contamination of Large Language Models: A Survey" | labelled-preprint-but-DOI-is-published-version |
| 92 | Wataoka et al., "Self-Preference Bias in LLM-as-a-Judge", 2024, arXiv 2410.21819, preprint (Crossref offered DOI 10.18653/v1/2025.findings-e | DOI 10.18653/v1/2025.findings-emnlp.510: 2025 · Findings of the Association for Computational Linguistics: EMNLP 2025 · proceedings-article · "Assistant-Guided Mitigation of Teacher Preference Bias in LLM-as-a-Judge"<br>arXiv 2410.21819: first v 2024-10-29 · jref "" · doi - · "Self-Preference Bias in LLM-as-a-Judge" | labelled-preprint-but-DOI-is-published-version, venue-not-in-citation, year-near(2024 vs 2025) |
| 94 | Gu et al., "A Survey on LLM-as-a-Judge", arXiv 2411.15594 (2024); journal version in The Innovation, 2026, DOI 10.1016/j.xinn.2025.101253 (C | DOI 10.1016/j.xinn.2025.101253: 2026 · The Innovation · journal-article · "A survey on LLM-as-a-judge"<br>arXiv 2411.15594: first v 2024-11-23 · jref "" · doi - · "A Survey on LLM-as-a-Judge" | year-mismatch(2024 vs 2026) |
| 96 | Springer "From benchmarks to deployment: a comprehensive review of agentic AI evaluation" (Artificial Intelligence Review, DOI in URL 10.100 | DOI 10.1007/s10462-026-11571-0: 2026 · Artificial Intelligence Review · journal-article · "From benchmarks to deployment: a comprehensive review of agentic AI evaluation"<br>DOI 10.1145/3711896.3736570: 2025 · Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.2 · proceedings-article · "Evaluation and Benchmarking of LLM Agents: A Survey" | venue-not-in-citation |

Rows whose identifiers resolved with no flags (line numbers): 59, 61, 62, 66, 68, 70, 71, 72, 73, 80, 81, 83, 85, 88, 89, 91, 93, 95

Rows without a DOI or arXiv id (check by title with verify_refs.py):

- line 78: Record
- line 82: Huidrom and Belz, "Using LLM Judgements for Sanity Checking Results and Reproducibility of Human Evaluations in NLP", 2025, GEM workshop at 
- line 86: White et al., "LiveBench: A Challenging, Contamination-Limited LLM Benchmark", ICLR 2025 (per Semantic Scholar and the OpenReview PDF header
- line 87: Zhang et al., "Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents", ICLR 2025 (per Semantic S

## research/01_literature/genai-organizations.md

Rows: 31 · rows with a DOI or arXiv id: 26 · rows with flags: 13 · rows without identifier: 5

| line | citation (start) | API findings | flags |
|---|---|---|---|
| 60 | Dell'Acqua, McFowland, Mollick, Lifshitz(-Assaf), Kellogg, Rajendran, Krayer, Candelon (and Lakhani on the SSRN version), 2023/2026, "Naviga | DOI 10.1287/orsc.2025.21838: 2026 · Organization Science · journal-article · "Navigating the Jagged Technological Frontier: Field Experimental Evidence of the Effects o"<br>DOI 10.2139/ssrn.4573321: 2023 · Elsevier BV · posted-content · "Navigating the Jagged Technological Frontier: Field Experimental Evidence of the Effects o" | year-mismatch(2023 vs 2026) |
| 62 | Bick, Blandin and Deming, 2024/2026, "The Rapid Adoption of Generative AI", NBER w32966 (Sept 2024, DOI 10.3386/w32966; revised Feb 2025 per | DOI 10.1287/mnsc.2025.02523: 2026 · Management Science · journal-article · "The Rapid Adoption of Generative AI"<br>DOI 10.20955/wp.2024.027: 2024 · Federal Reserve Bank of St. Louis · report · "The Rapid Adoption of Generative AI" | year-mismatch(2024 vs 2026) |
| 68 | Riemer, Peter, Schwabe, Chatterjee, Adam and Davison, 2026, "Generative AI Is Neither Just Another IT Artefact nor a Colleague: Methodologic | DOI 10.1111/isj.70027: 2025 · Information Systems Journal · journal-article · "Generative
                    <scp>AI</scp>
                    Is Neither Just Another
 " | year-near(2026 vs 2025) |
| 72 | Sebastian, 2026, "Digital shadow AI risk theory (DART): A framework for managing data disclosure and privacy risks of AI tools at work", Tec | DOI 10.1016/j.techfore.2026.124697: 2026 · Technological Forecasting and Social Change · journal-article · "Digital shadow AI risk theory (DART): A framework for managing data disclosure and privacy"<br>DOI 10.2139/ssrn.5038258: 2025 · Elsevier BV · posted-content · "Digital Shadow Risk Theory (DSRT): Assessing Organizational Risks of AI in the Workplace" | year-near(2026 vs 2025) |
| 79 | Cui, Demirer, Jaffe, Musolff, Peng and Salz, "The Effects of Generative AI on High-Skilled Work: Evidence from Three Field Experiments with  | DOI 10.1257/rct.14530: 2024 · AEA Randomized Controlled Trials · dataset · "The Effects of Generative AI on High Skilled Work: Evidence from Three Field Experiments
w"<br>DOI 10.1287/mnsc.2025.00535: 2026 · Management Science · journal-article · "The Effects of Generative AI on High-Skilled Work: Evidence from Three Field Experiments w" | venue-not-in-citation |
| 80 | Dell'Acqua, Ayoubi, Lifshitz, Sadun, Mollick, Mollick, Han and Goldman, "The Cybernetic Teammate: A Field Experiment on Generative AI and Te | DOI 10.1287/orsc.2025.20702: 2026 · Organization Science · journal-article · "The Cybernetic Teammate: A Field Experiment on Generative AI and Teamwork"<br>DOI 10.2139/ssrn.5207588: 2025 · Elsevier BV · posted-content · "The Cybernetic Teammate: A Field Experiment on Generative AI Reshaping Teamwork and Expert" | venue-not-in-citation |
| 81 | Mayer, Baygi and Buwalda, "Generation AI: Job Crafting by Entry-Level Professionals in the Age of Generative AI" | DOI 10.1007/s12599-025-00959-x: 2025 · Business &amp; Information Systems Engineering · journal-article · "Generation AI: Job Crafting by Entry-Level Professionals in the Age of Generative AI" | venue-not-in-citation |
| 82 | Wagman, Dearing and Chetty, "Generative AI Uses and Risks for Knowledge Workers in a Science Organization" | DOI 10.1145/3706598.3713827: 2025 · Proceedings of the 2025 CHI Conference on Human Factors in Computing Systems · proceedings-article · "Generative AI Uses and Risks for Knowledge Workers in a Science Organization"<br>arXiv 2501.16577: first v 2025-01-27 · jref "" · doi - · "Generative AI Uses and Risks for Knowledge Workers in a Science Organization" | venue-not-in-citation |
| 83 | Hai, Long, Honora, Japutra and Guo, "The dark side of employee-generative AI collaboration in the workplace: An investigation on work aliena | DOI 10.1016/j.ijinfomgt.2025.102905: 2025 · International Journal of Information Management · journal-article · "The dark side of employee-generative AI collaboration in the workplace: An investigation o" | venue-not-in-citation |
| 84 | Messer and Leischnig, "Copilot in the wings: When do employees reveal the use of AI?" | DOI 10.1016/j.chbr.2026.101315: 2026 · Computers in Human Behavior Reports · journal-article · "Copilot in the wings: When do employees reveal the use of AI?" | venue-not-in-citation |
| 85 | Feuerriegel, Hartmann, Janiesch and Zschech, "Generative AI" | DOI 10.1007/s12599-023-00834-7: 2023 · Business &amp; Information Systems Engineering · journal-article · "Generative AI"<br>arXiv 2309.07930: first v 2023-09-13 · jref "" · doi 10.1007/s12599-023-00834-7 · "Generative AI" | venue-not-in-citation |
| 87 | Brachman, El-Ashry, Dugan and Geyer, "Current and Future Use of Large Language Models for Knowledge Work" | DOI 10.1145/3757403: 2025 · Proceedings of the ACM on Human-Computer Interaction · journal-article · "Current and Future Use of Large Language Models for Knowledge Work"<br>arXiv 2503.16774: first v 2025-03-21 · jref "" · doi - · "Current and Future Use of Large Language Models for Knowledge Work" | venue-not-in-citation |
| 92 | Kim and Kim, "Understanding the Role of Trust, Perceived Risk, and Habit in Organization Members' Generative AI Use" | DOI 10.1177/21582440251410620: 2026 · Sage Open · journal-article · "Understanding the Role of Trust, Perceived Risk, and Habit in Organization Members' Genera" | venue-not-in-citation |

Rows whose identifiers resolved with no flags (line numbers): 58, 59, 61, 63, 64, 65, 66, 67, 69, 73, 86, 90, 91

Rows without a DOI or arXiv id (check by title with verify_refs.py):

- line 70: Cohen and Zalmanson, 2025, "Why Generative AI Isn't Formalized (Yet): Socio-Technical Barriers to Top Down Organizational Implementation", I
- line 71: Tronnier, Pomrehn and Navakumaran, 2025, "Motivated or Overwhelmed? A Qualitative Study on Technostress in Generative Artificial Intelligenc
- line 77: Item
- line 88: Ulfsnes, Mikalsen and Barbala, "From generation to application: Exploring knowledge workers' relations with GenAI"
- line 89: "Generative AI in the Wild: An Exploratory Case Study of Knowledge Workers" (authors not extracted)

## research/01_literature/governance-xai-fairness-compliance.md

Rows: 48 · rows with a DOI or arXiv id: 46 · rows with flags: 7 · rows without identifier: 2

| line | citation (start) | API findings | flags |
|---|---|---|---|
| 66 | Costanza-Chock, Raji and Buolamwini 2022 (author list of the ACM proceedings record per Crossref; the arXiv 2310.02521 version lists Costanz | DOI 10.1145/3531146.3533213: 2022 · 2022 ACM Conference on Fairness Accountability and Transparency · proceedings-article · "Who Audits the Auditors? Recommendations from a field scan of the algorithmic auditing eco"<br>arXiv 2310.02521: first v 2023-10-04 · jref "" · doi 10.1145/3531146.3533213 · "Who Audits the Auditors? Recommendations from a field scan of the algorithmic auditing eco" | venue-not-in-citation |
| 68 | Papagiannidis, Enholm, Dremel, Mikalef and Krogstie 2023, "Toward AI Governance: Identifying Best Practices and Potential Barriers and Outco | DOI 10.1007/s10796-022-10251-y: 2022 · Information Systems Frontiers · journal-article · "Toward AI Governance: Identifying Best Practices and Potential Barriers and Outcomes" | year-near(2023 vs 2022) |
| 69 | Dolata, Feuerriegel and Schwabe 2022, "A sociotechnical view of algorithmic fairness", Information Systems Journal 32(4) 754-818, peer-revie | DOI 10.1111/isj.12370: 2021 · Information Systems Journal · journal-article · "A sociotechnical view of algorithmic fairness" | year-near(2022 vs 2021) |
| 74 | Kalff and Simbeck 2025, "Explained, yet misunderstood: How AI Literacy shapes HR Managers' interpretation of User Interfaces in Recruiting R | DOI 10.48550/arXiv.2509.06475: Crossref error HTTP Error 404: Not Found<br>arXiv 2509.06475: first v 2025-09-08 · jref "CEUR-WS: 28-Sep-2025" · doi - · "Explained, yet misunderstood: How AI Literacy shapes HR Managers' interpretation of User I" | doi-unresolved |
| 76 | Wagner, Song, Borg, Engström and Lysek 2026, "AI Act high-risk AI compliance challenge and industry impact: A multiple case study", Informat | DOI 10.1016/j.infsof.2026.108067: 2026 · Information and Software Technology · journal-article · "AI Act high-risk AI compliance challenge and industry impact: A multiple case study"<br>DOI 10.2139/ssrn.5221279: 2025 · Elsevier BV · posted-content · "Ai Act High-Risk Ai Compliance Challenge and Industry Impact: A Multiple Case Study" | year-near(2026 vs 2025) |
| 91 | Heger, Passi, Dhanorkar, Kahn, Wang et al. 2025, "Towards a Responsible AI Organizational Maturity Model", PACM HCI 9(7); DOI 10.1145/375751 | DOI 10.1145/3757514: 2025 · Proceedings of the ACM on Human-Computer Interaction · journal-article · "Towards a Responsible AI Organizational Maturity Model" | venue-not-in-citation |
| 105 | Langer, Lazar and Baum 2025, "On the Complexities of Testing for Compliance with Human Oversight Requirements in AI Regulation", arXiv 2504. | DOI 10.1007/978-3-032-07132-3_11: 2025 · Lecture Notes in Computer Science · book-chapter · "On the Complexities of Testing for Compliance with Human Oversight Requirements in AI Regu"<br>arXiv 2504.03300: first v 2025-04-04 · jref "" · doi - · "On the Complexities of Testing for Compliance with Human Oversight Requirements in AI Regu" | venue-not-in-citation |

Rows whose identifiers resolved with no flags (line numbers): 63, 64, 65, 67, 70, 71, 72, 73, 75, 77, 78, 84, 85, 86, 87, 88, 89, 90, 92, 93, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 106, 107, 108, 109, 110, 111, 112, 113, 114

Rows without a DOI or arXiv id (check by title with verify_refs.py):

- line 82: Citation
- line 94: Kempton, Parmiggiani and Vassilakopoulou 2023, "Accountability in Managing Artificial Intelligence: State of the Art and a way forward for I

## research/01_literature/human-ai-algorithmic-management.md

Rows: 45 · rows with a DOI or arXiv id: 37 · rows with flags: 0 · rows without identifier: 8


Rows whose identifiers resolved with no flags (line numbers): 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 73, 74, 75, 81, 82, 83, 84, 85, 86, 87, 88, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108

Rows without a DOI or arXiv id (check by title with verify_refs.py):

- line 71: Chan, Kyung, Yoon and Kim, 2023, ICIS 2023 Proceedings, peer-reviewed conference
- line 72: Schauer, Schikowski and Schnurr, 2025, ECIS 2025 Proceedings, peer-reviewed conference (preliminary findings)
- line 79: Citation
- line 89: Amoah and Mehta, 2025, ICIS 2025 Proceedings, research in progress
- line 90: Heimbach, Ruthsatz and Mueller, 2025, ICIS 2025 Proceedings, peer-reviewed conference (pre-registered pilot)
- line 91: Moritz and Schmidt, 2024, ECIS 2024 Proceedings, research in progress
- line 92: Klöpper and Messer, 2024, ECIS 2024 Proceedings, peer-reviewed conference
- line 93: Abramova and Voronin, 2025, ECIS 2025 Proceedings, peer-reviewed conference

## research/01_literature/rag-knowledge-management.md

Rows: 51 · rows with a DOI or arXiv id: 50 · rows with flags: 9 · rows without identifier: 1

| line | citation (start) | API findings | flags |
|---|---|---|---|
| 67 | Lewis et al., 2020, NeurIPS 33, peer-reviewed | arXiv 2005.11401: first v 2020-05-22 · jref "" · doi - · "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" | peer-reviewed-label-rests-on-arxiv-only |
| 68 | Barnett, Kurniawan, Thudumu, Brannelly & Abdelrazek, 2024, CAIN 2024 (IEEE/ACM), DOI 10.1145/3644815.3644945, peer-reviewed | DOI 10.1145/3644815.3644945: 2024 · Proceedings of the IEEE/ACM 3rd International Conference on AI Engineering - Software Engineering for AI · proceedings-article · "Seven Failure Points When Engineering a Retrieval Augmented Generation System"<br>arXiv 2401.05856: first v 2024-01-11 · jref "" · doi - · "Seven Failure Points When Engineering a Retrieval Augmented Generation System" | venue-not-in-citation |
| 77 | Brehme, Dornauer, Ströhle, Ehrhart & Breu, 2025, KDIR 2025 (SciTePress), DOI 10.5220/0013739500004000, peer-reviewed | DOI 10.5220/0013739500004000: 2025 · Proceedings of the 17th International Joint Conference on Knowledge Discovery, Knowledge Engineering and Knowledge Management · proceedings-article · "Retrieval-Augmented Generation in Industry: An Interview Study on Use Cases, Requirements,"<br>DOI 10.5281/zenodo.16778599: Crossref error HTTP Error 404: Not Found<br>arXiv 2508.14066: first v 2025-08-11 · jref "" · doi 10.5220/0013739500004000 · "Retrieval-Augmented Generation in Industry: An Interview Study on Use Cases, Requirements," | doi-unresolved, venue-not-in-citation |
| 78 | Mueller, Holstein, Bause, Satzger & Kuehl (KIT), 2025, ICIS 2025 Proceedings (AISeL icis2025/da_bus/da_bus/9; arXiv 2510.00552v1), peer-revi | arXiv 2510.00552: first v 2025-10-01 · jref "" · doi - · "Data Quality Challenges in Retrieval-Augmented Generation" | peer-reviewed-label-rests-on-arxiv-only |
| 88 | Liu, Lin, Hewitt, Paranjape, Bevilacqua, Petroni & Liang, 2024 (S2 year 2023), TACL, DOI 10.1162/tacl_a_00638 | DOI 10.1162/tacl_a_00638: 2024 · Transactions of the Association for Computational Linguistics · journal-article · "Lost in the Middle: How Language Models Use Long Contexts"<br>arXiv 2307.03172: first v 2023-07-06 · jref "" · doi - · "Lost in the Middle: How Language Models Use Long Contexts" | venue-not-in-citation |
| 90 | Zhao et al., 2026, ACM TOSEM, DOI 10.1145/3802824 (arXiv 2411.19463, 2024) | DOI 10.1145/3802824: 2026 · ACM Transactions on Software Engineering and Methodology · journal-article · "Understanding the Fundamental Design Decisions of Retrieval-Augmented Generation Systems"<br>arXiv 2411.19463: first v 2024-11-29 · jref "ACM Transactions on Software Engineering and Methodology (TO" · doi 10.1145/3802824 · "Understanding the Fundamental Design Decisions of Retrieval-Augmented Generation Systems" | venue-not-in-citation |
| 93 | Karakurt & Akbulut, 2025 (Crossref issued date; volume 16 suggests 2026), Applied Sciences, DOI 10.3390/app16010368 (preprint 10.20944/prepr | DOI 10.20944/preprints202512.0359.v1: 2025 · MDPI AG · posted-content · "Retrieval Augmented Generation (RAG) and Large Language Models (LLMs) for Enterprise Knowl"<br>DOI 10.3390/app16010368: 2025 · Applied Sciences · journal-article · "Retrieval-Augmented Generation (RAG) and Large Language Models (LLMs) for Enterprise Knowl" | labelled-preprint-but-DOI-is-published-version |
| 120 | Reproducibility preprints: "A Reproducibility Study of Metacognitive Retrieval-Augmented Generation" (arXiv 2604.19899) and "On The Reproduc | arXiv 2509.18869: first v 2025-09-23 · jref "" · doi - · "On The Reproducibility Limitations of RAG Systems"<br>arXiv 2604.19899: first v 2026-04-21 · jref "" · doi 10.1145/3805712.3808551 · "A Reproducibility Study of Metacognitive Retrieval-Augmented Generation" | arxiv-lists-published-version |
| 121 | Surveys (pointers only): Gao et al. 2023 (arXiv 2312.10997, 4,194 citations per S2); Fan et al. KDD 2024 (DOI 10.1145/3637528.3671470); Gan  | DOI 10.1145/3637528.3671470: 2024 · Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining · proceedings-article · "A Survey on RAG Meeting LLMs: Towards Retrieval-Augmented Large Language Models"<br>arXiv 2312.10997: first v 2023-12-18 · jref "" · doi - · "Retrieval-Augmented Generation for Large Language Models: A Survey"<br>arXiv 2405.07437: first v 2024-05-13 · jref "" · doi 10.1007/978-981-96-1024-2_8 · "Evaluation of Retrieval-Augmented Generation: A Survey" | year-near(2023 vs 2024) |

Rows whose identifiers resolved with no flags (line numbers): 69, 70, 71, 72, 73, 74, 75, 76, 79, 80, 81, 82, 89, 91, 92, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119

Rows without a DOI or arXiv id (check by title with verify_refs.py):

- line 86: Citation (as visible)

## Totals

Rows 298 · checked by identifier 267 · flagged 55 · without identifier 31


## Reconciliation (2026-10-05)

Summary. All 55 flagged rows and all 31 identifier-less rows listed above were re-examined (86 rows). Twenty rows were edited, all in place and only in their Citation cell: 17 of the flagged rows and 3 of the identifier-less rows. Of the 55 flags, 38 were benign (the year difference or the published version was already explained in the cell, the Crossref container title was only an abbreviation or the series name of the venue the cell already names, the venue sat in the adjacent column of a supplementary table, or the "unresolved" DOI is a DataCite DOI that resolves at doi.org). Of the 31 identifier-less rows, 7 are the header rows of the supplementary tables (the script lists them because it treats every table line after the evidence-table heading as a row) and 24 are real rows, of which 2 gained a DOI (both exact Crossref title matches with matching year), 1 gained a note about a related record, and 21 remain without an identifier, 16 of them AIS eLibrary ICIS/ECIS/ACIS/UKAIS papers, which carry no DOI. No row was deleted, no findings text was changed, and no file other than the eight area files and this file was modified. The five most consequential corrections: (1) evaluation-validity-safety.md line 74, Atil et al. "Non-Determinism" is now recorded as published at Eval4NLP 2025 (Crossref author list of 13 identical to arXiv v5), status changed from preprint to peer-reviewed workshop paper; (2) evaluation-validity-safety.md line 90, the Crossref DOI offered for the Xu et al. contamination survey is explicitly rejected (it is Palavalli, Bertsch and Gormley's taxonomy paper); (3) rag-knowledge-management.md line 120, the metacognitive-RAG reproducibility study is now recorded as a SIGIR '26 paper (DOI 10.1145/3805712.3808551); (4) the four ICLR/ICML venue claims in evaluation-validity-safety.md (lines 63, 67, 69, 84) now cite OpenReview and Semantic Scholar/DBLP keys instead of resting on the arXiv id or the authors' own comment; (5) decision-support-analytics.md lines 91 and 92 gained DOIs and author lists for the ACL 2025 and EMNLP 2025 papers, and line 94 resolves "(Kim et al.?)" to Kim, So, Han and Lee from the Crossref record.

Procedure notes. Line numbers are those of the report above (before this pass); every edit was in-line, so no line shifted. dblp could not be queried: dblp.org/search/publ/api returned a bot-check interstitial ("Making sure you're not a bot!") for every request, which was not bypassed; for the four peer-reviewed-on-arXiv-only rows with no stated source, the OpenReview API (api2.openreview.net/notes/search) and the Semantic Scholar graph API were used instead, both of which this file's status key already accepts as venue sources. verify_refs.py ran once over all 24 real identifier-less titles (titles for the ten AIS eLibrary rows that had none in the cell were taken from the bepress_citation_title meta tag of their AIS eLibrary pages); Crossref answered for all 24, OpenAlex and Semantic Scholar returned HTTP 429 for all 24 after the script's four retries, so those two legs are recorded as "not re-checked (429)" and were not re-run.

### Rows handled

| file | line (original) | flag(s) | decision | edit made |
|---|---|---|---|---|
| agents-bpm-process-mining.md | 59 | year-near (2023 vs 2024) | already explained ("Crossref year 2024" in cell) | no |
| agents-bpm-process-mining.md | 61 | year-near (2026 vs 2025) | already explained ("online 2025" in cell) | no |
| agents-bpm-process-mining.md | 70 | peer-reviewed-label-rests-on-arxiv-only | venue source stated (Semantic Scholar venue, PyPI README) | no |
| agents-bpm-process-mining.md | 71 | peer-reviewed-label-rests-on-arxiv-only | venue source stated (OpenReview EPlpe3Fx1x "Accepted by TMLR"; Semantic Scholar) | no |
| agents-bpm-process-mining.md | 78 | year-near (2025 vs 2026) | not explained; Crossref: book-chapter, LNBIP, issued 2026, online 2026-04-01 | yes: "BPM 2025 Workshops (AI4BPM keynote paper), LNBIP (volume dated 2026 by Crossref, published online 2026-04-01), DOI 10.1007/978-3-032-13426-4_1" |
| agents-bpm-process-mining.md | 81 | venue-not-in-citation | event named, series (LNBIP) absent; appended | yes: "BPMDS/EMMSAD 2024 (LNBIP), DOI 10.1007/978-3-031-61007-3_2" |
| agents-bpm-process-mining.md | 82 | venue-not-in-citation | event named, series absent; appended | yes: "BPMDS 2024 (LNBIP), DOI 10.1007/978-3-031-61007-3_18" |
| agents-bpm-process-mining.md | 88 | venue-not-in-citation | event named, series absent; appended | yes: "BPM 2025 Forum (LNBIP), DOI 10.1007/978-3-032-02929-4_16" |
| agents-bpm-process-mining.md | 96 | venue-not-in-citation, year-near (2024 vs 2025) | series absent and year not explained; Crossref issued 2025, online 2025-03-28 | yes: "ICPM 2024 Workshops (LNBIP, volume dated 2025 by Crossref, published online 2025-03-28), DOI 10.1007/978-3-031-82225-4_1" |
| decision-support-analytics.md | 66 | peer-reviewed-label-rests-on-arxiv-only | venue source stated (OpenReview XmProj9cPs, DBLP key) | no |
| decision-support-analytics.md | 69 | venue-not-in-citation | "IEEE TKDE" is the abbreviation of the Crossref container (IEEE Transactions on Knowledge and Data Engineering); same venue | no |
| decision-support-analytics.md | 79 | peer-reviewed-label-rests-on-arxiv-only | venue source stated (OpenReview ZGqd0cbBvm, arXiv comment) | no |
| decision-support-analytics.md | 86 | venue-not-in-citation | "PVLDB" is the abbreviation of Proceedings of the VLDB Endowment; same venue | no |
| decision-support-analytics.md | 94 | venue-not-in-citation | "PVLDB" abbreviation, same venue; the cell's "(Kim et al.?)" resolved from the Crossref author list (Hyeonji Kim, Byeong-Hoon So, Wook-Shin Han, Hongrae Lee) | yes: "(Kim, So, Han and Lee, authors per the Crossref record read 2026-10-05)" replaces "(Kim et al.?)" |
| evaluation-validity-safety.md | 60 | peer-reviewed-label-rests-on-arxiv-only | venue page in the Link cell (usenix.org/conference/usenixsecurity24/presentation/liu-yupei) | no |
| evaluation-validity-safety.md | 63 | peer-reviewed-label-rests-on-arxiv-only | no source stated; Crossref bibliographic: no match; dblp: bot-check page (not queried); OpenReview 3GTtZFiajM venue "ICLR 2025 Poster"; Semantic Scholar venue ICLR, DBLP conf/iclr/YeWHCZMGG0CC025 | yes: "ICLR 2025 (OpenReview 3GTtZFiajM, venue "ICLR 2025 Poster"; Semantic Scholar venue ICLR, DBLP key conf/iclr/YeWHCZMGG0CC025), peer-reviewed" |
| evaluation-validity-safety.md | 64 | venue-not-in-citation, year-near (2026 vs 2025) | already explained: the cell states the Crossref DOI resolves to a different paper and is rejected; the flags come from that rejected DOI | no |
| evaluation-validity-safety.md | 65 | peer-reviewed-label-rests-on-arxiv-only | OpenReview forum G0dksFayVq in the Link cell | no |
| evaluation-validity-safety.md | 67 | peer-reviewed-label-rests-on-arxiv-only | no source stated; Crossref bibliographic: no match; OpenReview jOmk0uS1hl venue "ICLR 2025 Oral"; Semantic Scholar venue ICLR | yes: "ICLR 2025 (OpenReview jOmk0uS1hl, venue "ICLR 2025 Oral"; Semantic Scholar venue ICLR), peer-reviewed" |
| evaluation-validity-safety.md | 69 | peer-reviewed-label-rests-on-arxiv-only | no source stated; Crossref bibliographic: no match; OpenReview tvhaxkMKAn venue "ICLR 2024 poster"; Semantic Scholar DBLP conf/iclr/SharmaTKDABDHJK24 | yes: "ICLR 2024 (OpenReview tvhaxkMKAn, venue "ICLR 2024 poster"; Semantic Scholar venue ICLR, DBLP key conf/iclr/SharmaTKDABDHJK24), peer-reviewed" |
| evaluation-validity-safety.md | 74 | labelled-preprint-but-DOI-is-published-version | Crossref 10.18653/v1/2025.eval4nlp-1.12: proceedings-article, "Non-Determinism of “Deterministic” LLM System Settings in Hosted Environments", Proceedings of the 5th Workshop on Evaluation and Comparison of NLP Systems, 2025; 13 authors identical in order to the arXiv v5 list in the cell (Atıl, Aykent, Chittams, Fu, ... Baldwin), so the published version is confirmed; status changed to peer-reviewed workshop paper | yes: "2024, arXiv; published as "Non-Determinism of “Deterministic” LLM System Settings in Hosted Environments", Proceedings of the 5th Workshop on Evaluation and Comparison of NLP Systems (Eval4NLP 2025, Association for Computational Linguistics), 2025, DOI 10.18653/v1/2025.eval4nlp-1.12 (Crossref type proceedings-article; the Crossref author list of 13 matches arXiv v5 ...; confirmed 2026-10-05 ...), peer-reviewed workshop paper" |
| evaluation-validity-safety.md | 84 | peer-reviewed-label-rests-on-arxiv-only | only the arXiv comment was cited (not independent); Crossref bibliographic: no match; OpenReview YhZ2PY2nZa venue "ICML 2025 Position Paper Track spotlightposter"; Semantic Scholar venue ICML, DBLP conf/icml/BowyerAI25 | yes: "ICML 2025 position paper (comment on arXiv 2503.01747; OpenReview YhZ2PY2nZa, venue "ICML 2025 Position Paper Track spotlightposter"; Semantic Scholar venue ICML, DBLP key conf/icml/BowyerAI25), peer-reviewed" |
| evaluation-validity-safety.md | 90 | labelled-preprint-but-DOI-is-published-version | Crossref 10.18653/v1/2024.conda-1.3 is "A Taxonomy for Data Contamination in Large Language Models" by Palavalli, Bertsch and Gormley: a different paper; the cell's "possible published version, unconfirmed" replaced by an explicit rejection; status stays preprint | yes: "... checked 2026-10-05: that DOI resolves to "A Taxonomy for Data Contamination in Large Language Models" by Palavalli, Bertsch and Gormley, a different paper, so it is rejected and the survey remains arXiv-only)" |
| evaluation-validity-safety.md | 92 | labelled-preprint-but-DOI-is-published-version, venue-not-in-citation, year-near (2024 vs 2025) | already explained: the cell already rejects DOI 10.18653/v1/2025.findings-emnlp.510 as a different paper (confirmed again by the Crossref title in the report) | no |
| evaluation-validity-safety.md | 94 | year-mismatch (2024 vs 2026) | already explained (arXiv 2024; journal version The Innovation 2026) | no |
| evaluation-validity-safety.md | 96 | venue-not-in-citation | cell lists three search-result titles; Crossref for 10.1145/3711896.3736570 gives KDD '25 proceedings (Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.2, 2025; Mohammadi, Li, Lo, Yip); venue appended; Artificial Intelligence Review already named | yes: "(10.1145/3711896.3736570; Crossref 2026-10-05: Mohammadi, Li, Lo and Yip, Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.2, KDD '25, 2025)" |
| genai-organizations.md | 60 | year-mismatch (2023 vs 2026) | already explained (SSRN 2023; Organization Science 2026) | no |
| genai-organizations.md | 62 | year-mismatch (2024 vs 2026) | already explained (NBER 2024; Management Science 2026) | no |
| genai-organizations.md | 68 | year-near (2026 vs 2025) | already explained ("Crossref date 2025-12-25") | no |
| genai-organizations.md | 72 | year-near (2026 vs 2025) | already explained (SSRN 2025 named with its year) | no |
| genai-organizations.md | 79 | venue-not-in-citation | supplementary table: the venue (Management Science) is in the adjacent "Venue and status" column, which the script does not read | no |
| genai-organizations.md | 80 | venue-not-in-citation | venue (Organization Science) in adjacent column | no |
| genai-organizations.md | 81 | venue-not-in-citation | venue (BISE) in adjacent column | no |
| genai-organizations.md | 82 | venue-not-in-citation | venue (CHI '25) in adjacent column | no |
| genai-organizations.md | 83 | venue-not-in-citation | venue (IJIM) in adjacent column | no |
| genai-organizations.md | 84 | venue-not-in-citation | venue (Computers in Human Behavior Reports) in adjacent column | no |
| genai-organizations.md | 85 | venue-not-in-citation | venue (BISE) in adjacent column | no |
| genai-organizations.md | 87 | venue-not-in-citation | venue (Proc. ACM HCI) in adjacent column | no |
| genai-organizations.md | 92 | venue-not-in-citation | venue (Sage Open) in adjacent column | no |
| governance-xai-fairness-compliance.md | 66 | venue-not-in-citation | "FAccT '22 (ACM)" is the standard abbreviation of the Crossref container "2022 ACM Conference on Fairness Accountability and Transparency"; same venue | no |
| governance-xai-fairness-compliance.md | 68 | year-near (2023 vs 2022) | already explained ("Crossref issued 2022") | no |
| governance-xai-fairness-compliance.md | 69 | year-near (2022 vs 2021) | not explained; Crossref: issued and published-online 2021-10-07, published-print 2022-07 | yes: "Information Systems Journal 32(4) 754-818 (print issue July 2022; Crossref issued and online-first date 2021-10-07), peer-reviewed" |
| governance-xai-fairness-compliance.md | 74 | doi-unresolved | 10.48550/arXiv.2509.06475 is a DataCite (arXiv) DOI, so Crossref 404 is expected; doi.org resolves it (HTTP 200 to arxiv.org/abs/2509.06475; DataCite: Preprint, arXiv, 2025); the cell already says "no Crossref DOI" | no |
| governance-xai-fairness-compliance.md | 76 | year-near (2026 vs 2025) | already explained (SSRN preprint 2025 named) | no |
| governance-xai-fairness-compliance.md | 91 | venue-not-in-citation | "PACM HCI" is the abbreviation of Proceedings of the ACM on Human-Computer Interaction; same venue | no |
| governance-xai-fairness-compliance.md | 105 | venue-not-in-citation | event (AISoLA 2025) named, series absent; Crossref container Lecture Notes in Computer Science appended | yes: "(AISoLA 2025 per the Semantic Scholar chase, Lecture Notes in Computer Science per Crossref, DOI 10.1007/978-3-032-07132-3_11)" |
| rag-knowledge-management.md | 67 | peer-reviewed-label-rests-on-arxiv-only | venue page in the Link cell (papers.nips.cc 2020 abstract page) | no |
| rag-knowledge-management.md | 68 | venue-not-in-citation | "CAIN 2024 (IEEE/ACM)" is the abbreviation of the Crossref container (Proceedings of the IEEE/ACM 3rd International Conference on AI Engineering - Software Engineering for AI); same venue | no |
| rag-knowledge-management.md | 77 | doi-unresolved, venue-not-in-citation | 10.5281/zenodo.16778599 is a DataCite DOI (replication package, Dataset, Zenodo 2025); doi.org resolves it (HTTP 200), Crossref 404 expected; "KDIR 2025" is the sub-conference of the Crossref container "Proceedings of the 17th International Joint Conference on Knowledge Discovery, Knowledge Engineering and Knowledge Management" (IC3K), same event | no |
| rag-knowledge-management.md | 78 | peer-reviewed-label-rests-on-arxiv-only | venue source stated (AISeL icis2025/da_bus/da_bus/9 in Citation and Link cells) | no |
| rag-knowledge-management.md | 88 | venue-not-in-citation | "TACL" abbreviation of Transactions of the Association for Computational Linguistics; same venue | no |
| rag-knowledge-management.md | 90 | venue-not-in-citation | "ACM TOSEM" abbreviation of ACM Transactions on Software Engineering and Methodology; same venue | no |
| rag-knowledge-management.md | 93 | labelled-preprint-but-DOI-is-published-version | the cell already names the published version (Applied Sciences, 10.3390/app16010368); the word "preprint" labels the companion MDPI preprint DOI | no |
| rag-knowledge-management.md | 120 | arxiv-lists-published-version | arXiv 2604.19899 lists DOI 10.1145/3805712.3808551; Crossref: proceedings-article, "A Reproducibility Study of Metacognitive Retrieval-Augmented Generation", Proceedings of the 49th International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR '26), 2026, Iturra Bocaz and Galuščáková; lead-in "Reproducibility preprints" changed because only the second item is still a preprint | yes: "Reproducibility studies: "A Reproducibility Study of Metacognitive Retrieval-Augmented Generation" (arXiv 2604.19899; published as Iturra Bocaz and Galuščáková, SIGIR '26, Proceedings of the 49th International ACM SIGIR Conference on Research and Development in Information Retrieval, 2026, DOI 10.1145/3805712.3808551, per the arXiv record and Crossref, peer-reviewed) and the preprint "On The Reproducibility Limitations of RAG Systems" (arXiv 2509.18869)" |
| rag-knowledge-management.md | 121 | year-near (2023 vs 2024) | benign: the cell lists four surveys with their own years (Gao 2023 arXiv vs Fan KDD 2024); while there, the arXiv record for 2405.07437 (Yu et al.) lists a published DOI, which Crossref gives as book-chapter in Communications in Computer and Information Science, 2025; added as a pointer | yes: "Yu et al. 2024 evaluation survey (arXiv 2405.07437; the arXiv record lists a published version, DOI 10.1007/978-981-96-1024-2_8, Communications in Computer and Information Science, Springer Nature Singapore, 2025, per Crossref)" |
| agents-bpm-process-mining.md | 76 | no identifier | header row of the supplementary table ("\| Item \| Status \| What was visible \| Access depth \|"), listed by the script because it treats every table line after the evidence-table heading as a row; not a broken row, nothing to fix | no |
| agents-bpm-process-mining.md | 98 | no identifier | Laerum and Nüttgens, ECIS 2026 (AIS eLibrary); Crossref best match 0.661 (an LNCS 2025 chapter, rejected); OpenAlex and S2 not re-checked (429); AIS eLibrary ECIS papers carry no DOI: no identifier found | no |
| agents-bpm-process-mining.md | 99 | no identifier | Göldi and Rietsche, ICIS 2024 (AIS eLibrary); Crossref best match 0.729 (an IJCTT 2024 article, rejected); OpenAlex and S2 429; no identifier found (AIS eLibrary) | no |
| decision-support-analytics.md | 84 | no identifier | header row of the supplementary table ("Item"); artefact, not a row | no |
| decision-support-analytics.md | 90 | no identifier | HBR digital article; Crossref best match 0.39 (rejected); OpenAlex and S2 429; practitioner article, no identifier found | no |
| decision-support-analytics.md | 91 | no identifier | Crossref title match 1.0: 10.18653/v1/2025.acl-short.71, ACL 2025 Volume 2: Short Papers, proceedings-article, 2025 (year matches); authors Park, Lee, Lee, Gwak, Choo added from the record | yes: "Park, Lee, Lee, Gwak and Choo (authors per Crossref), "Revisiting LLMs as Zero-Shot Time Series Forecasters: Small Noise Can Break Large Models", ACL 2025 short (aclanthology 2025.acl-short.71), DOI 10.18653/v1/2025.acl-short.71 (Crossref title match 1.0, 2026-10-05)" |
| decision-support-analytics.md | 92 | no identifier | Crossref title match 1.0: 10.18653/v1/2025.emnlp-main.859, Proceedings of EMNLP 2025, proceedings-article, 2025 (year matches); authors Liu, Wang, Preotiuc-Pietro, Chandarana, Gupta added | yes: "Liu, Wang, Preotiuc-Pietro, Chandarana and Gupta (authors per Crossref), "Calibrating LLMs for Text-to-SQL Parsing by Leveraging Sub-clause Frequencies", EMNLP 2025 (2025.emnlp-main.859), DOI 10.18653/v1/2025.emnlp-main.859 (Crossref title match 1.0, 2026-10-05)" |
| decision-support-analytics.md | 93 | no identifier | CIDR 2026 paper; Crossref best match 0.403 is the PVLDB companion paper 10.14778/3796195.3796206, already in the main table (line 67); CIDR publishes without DOIs; no identifier found | no |
| decision-support-analytics.md | 95 | no identifier | the cell gives a description ("MMQA: multi-table, multi-hop QA benchmark"), not the paper title; Crossref best match 0.675 is a monograph (rejected); OpenAlex and S2 429; no identifier found; the OpenReview id qResKYUOTf in the cell is the only pointer | no |
| efficiency-privacy-low-resource.md | 62 | no identifier | title taken from the AIS eLibrary page ("AI Adoption by SMEs in Developing Countries: Challenges, Applications, and Benefits"); Crossref best match 0.558 (rejected); OpenAlex and S2 429; ACIS 2025 on AIS eLibrary, no DOI: no identifier found | no |
| efficiency-privacy-low-resource.md | 63 | no identifier | title from the AIS eLibrary page ("Bridging the AI Divide: Barriers and Challenges to AI Adoption for Nigerian SMEs"); Crossref best match 0.431 (rejected); OpenAlex and S2 429; UKAIS 2025 on AIS eLibrary, no DOI: no identifier found | no |
| evaluation-validity-safety.md | 78 | no identifier | header row of the "Additional records" table ("Record"); artefact, not a row | no |
| evaluation-validity-safety.md | 82 | no identifier | Huidrom and Belz, GEM workshop at ACL 2025; Crossref best match 0.521 (an LREC 2024 paper, rejected); OpenAlex and S2 429; arXiv no entry; no identifier found (the ACL Anthology GEM 2025 volume would be the place to look for a 10.18653 DOI) | no |
| evaluation-validity-safety.md | 86 | no identifier | White et al., LiveBench, ICLR 2025; Crossref best match 0.434 (rejected); arXiv exact match 2406.19314 (score 1.0, no journal-ref or DOI); OpenAlex and S2 429; no DOI found; the arXiv id could be added by hand but the row already states its ICLR source | no |
| evaluation-validity-safety.md | 87 | no identifier | Zhang et al., ASB, ICLR 2025; Crossref best match 0.464 is again the different NeurIPS 2025 paper the cell already rejects; arXiv exact match 2410.02644 (score 1.0, no DOI); OpenAlex and S2 429; no DOI found | no |
| genai-organizations.md | 70 | no identifier | Cohen and Zalmanson, ICIS 2025 (AIS eLibrary); Crossref best match 0.495 (rejected); OpenAlex and S2 429; no identifier found (AIS eLibrary) | no |
| genai-organizations.md | 71 | no identifier | Tronnier, Pomrehn and Navakumaran, ICIS 2025 (AIS eLibrary); Crossref best match 0.528 (rejected); OpenAlex and S2 429; no identifier found (AIS eLibrary) | no |
| genai-organizations.md | 77 | no identifier | header row of the supplementary table ("Item"); artefact, not a row | no |
| genai-organizations.md | 88 | no identifier | Ulfsnes, Mikalsen and Barbala, ICIS 2024 (AIS eLibrary); Crossref best match 0.495 (rejected); OpenAlex and S2 429; no identifier found (AIS eLibrary) | no |
| genai-organizations.md | 89 | no identifier | "Generative AI in the Wild", ECIS 2024 (AIS eLibrary); Crossref best match 0.553 (an IJPR 2025 article, rejected); OpenAlex and S2 429; no identifier found (AIS eLibrary); authors still not extracted | no |
| governance-xai-fairness-compliance.md | 82 | no identifier | header row of the supplementary table ("Citation"); artefact, not a row | no |
| governance-xai-fairness-compliance.md | 94 | no identifier | Kempton, Parmiggiani and Vassilakopoulou, ECIS 2023 (AIS eLibrary); Crossref best match 0.623 (a Bled 2021 proceedings paper, rejected); OpenAlex and S2 429; no identifier found (AIS eLibrary) | no |
| human-ai-algorithmic-management.md | 71 | no identifier | title from the AIS eLibrary page ("Algorithm as Boss or Coworker? Randomized Field Experiment on Algorithmic Control and Collaboration in Gig Platform"); Crossref best match 0.53 (rejected); OpenAlex and S2 429; ICIS 2023, no DOI: no identifier found | no |
| human-ai-algorithmic-management.md | 72 | no identifier | title from AIS eLibrary ("Algorithmic Management with Human Oversight: An Experimental Analysis"); Crossref best match 0.423 (rejected); OpenAlex and S2 429; ECIS 2025, no DOI: no identifier found | no |
| human-ai-algorithmic-management.md | 79 | no identifier | header row of the supplementary table ("Citation"); artefact, not a row | no |
| human-ai-algorithmic-management.md | 89 | no identifier | title from AIS eLibrary ("Fear, Transparency, and Psychological Needs: Shaping Behavioral Intent in AI Workplace Surveillance"); Crossref best match 0.449 (rejected); OpenAlex and S2 429; ICIS 2025, no DOI: no identifier found | no |
| human-ai-algorithmic-management.md | 90 | no identifier | title from AIS eLibrary ("The Effects of Judge's AI Literacy and Bias Blind Spot on the Utilization of Biased Algorithmic Advice"); Crossref best match 0.383 (rejected); OpenAlex and S2 429; ICIS 2025, no DOI: no identifier found | no |
| human-ai-algorithmic-management.md | 91 | no identifier | title from AIS eLibrary ("Trust in Algorithmic Management: The Role of Justice and Prior Discrimination Experience"); Crossref match 0.944 to 10.5465/amproc.2024.14136abstract, Academy of Management Proceedings 2024, by the same authors (Moritz, Schmidt) but titled "... The Role of Task Type and Prior Discrimination Experience": a related AOM abstract, not the ECIS paper, so not attached as the paper's DOI; noted in the cell instead | yes: "Moritz and Schmidt, 2024, ECIS 2024 Proceedings, research in progress (no DOI, AIS eLibrary; a Crossref title search on 2026-10-05 surfaced a related Academy of Management Proceedings 2024 abstract by the same authors, "Trust in Algorithmic Management: The Role of Task Type and Prior Discrimination Experience", DOI 10.5465/amproc.2024.14136abstract, which is not the ECIS paper)" |
| human-ai-algorithmic-management.md | 92 | no identifier | title from AIS eLibrary ("Hiding Behind Algorithms: People Analytics and Perceived Fairness Violation in Managerial Decisions"); Crossref best match 0.653 (a Journal of Business Analytics 2025 article, rejected at this score; possibly a later journal version, not verified); OpenAlex and S2 429; ECIS 2024, no DOI: no identifier found | no |
| human-ai-algorithmic-management.md | 93 | no identifier | title from AIS eLibrary ("Synthesizing the Ambivalent Effects of Algorithmic Management on Workers' Well-Being"); Crossref best match 0.571 (rejected); OpenAlex and S2 429; ECIS 2025, no DOI: no identifier found | no |
| rag-knowledge-management.md | 86 | no identifier | header row of the pointer table ("Citation (as visible)"); artefact, not a row | no |

### Edits per file

| file | flagged rows | flagged rows edited | identifier-less rows (real / header artefacts) | identifier-less rows edited | total edits |
|---|---|---|---|---|---|
| agents-bpm-process-mining.md | 9 | 5 | 2 / 1 | 0 | 5 |
| decision-support-analytics.md | 5 | 1 | 5 / 1 | 2 | 3 |
| efficiency-privacy-low-resource.md | 0 | 0 | 2 / 0 | 0 | 0 |
| evaluation-validity-safety.md | 12 | 7 | 3 / 1 | 0 | 7 |
| genai-organizations.md | 13 | 0 | 4 / 1 | 0 | 0 |
| governance-xai-fairness-compliance.md | 7 | 2 | 1 / 1 | 0 | 2 |
| human-ai-algorithmic-management.md | 0 | 0 | 7 / 1 | 1 | 1 |
| rag-knowledge-management.md | 9 | 2 | 0 / 1 | 0 | 2 |
| total | 55 | 17 | 24 / 7 | 3 | 20 |

### Rows that still need a human decision

- evaluation-validity-safety.md line 74 (Atil et al.): the Citation cell now says peer-reviewed workshop paper, but the Limitations cell still reads "preprint; venue field empty in Semantic Scholar" (findings text, not touched). Decide whether to update it and whether to read the Eval4NLP version, whose title differs ("... LLM System Settings in Hosted Environments").
- rag-knowledge-management.md line 120: the SIGIR '26 version of the metacognitive-RAG reproducibility study was not read; the row's content still comes from snippets.
- human-ai-algorithmic-management.md line 91 (Moritz and Schmidt): a same-author Academy of Management Proceedings 2024 abstract with a different subtitle exists (DOI 10.5465/amproc.2024.14136abstract). Decide whether to cite the AOM version alongside or instead of the ECIS research-in-progress paper.
- human-ai-algorithmic-management.md line 92 (Klöpper and Messer): Crossref's best match (0.653) is a Journal of Business Analytics 2025 article, DOI 10.1080/2573234x.2025.2482645; it may be a later journal version of the ECIS 2024 paper but the score is below threshold and it was not opened.
- decision-support-analytics.md line 95 (MMQA): the cell has a description rather than the paper title; the real title must be taken from OpenReview qResKYUOTf before a title search can work.
- evaluation-validity-safety.md lines 86 and 87 (LiveBench, ASB): arXiv exact matches (2406.19314, 2410.02644) exist but were not added because the rows rest on ICLR 2025 sources and the task was to find DOIs; add the arXiv ids if the Link convention of this file wants them.
- evaluation-validity-safety.md line 82 (Huidrom and Belz): the ACL Anthology GEM 2025 volume was not checked for a 10.18653 DOI.
- genai-organizations.md line 89: authors of "Generative AI in the Wild" are still not extracted.
- All 24 identifier-less titles: OpenAlex and Semantic Scholar legs returned 429 and were not re-run; a later re-run may add OpenAlex ids or S2 venue confirmations.
- Tool note (not a citation decision): verify_evidence_tables.py reads only the first cell as the Citation, so in the supplementary tables of genai-organizations.md (Item | Venue and status | ...) every row with a DOI triggers venue-not-in-citation; and it lists the header row of each supplementary table as an identifier-less row. Both are script behaviours, not record errors.

### API calls used

- Crossref REST API, `GET https://api.crossref.org/works/{doi}` (User-Agent research-records-verify/0.2): 12 DOIs (9 for Task A confirmation of authors, container, type and dates; 3 for Task B candidate confirmation).
- Crossref REST API, `GET https://api.crossref.org/works?query.bibliographic=<title>&rows=3`: 4 titles (Task A, peer-reviewed-on-arXiv-only rows); no match for any.
- Crossref REST API, `GET https://api.crossref.org/works?query.title=<title>&rows=3` via verify_refs.py: 24 titles (Task B).
- OpenAlex `GET https://api.openalex.org/works?search=<title>` via verify_refs.py: 24 titles, all HTTP 429 after retries.
- Semantic Scholar `GET https://api.semanticscholar.org/graph/v1/paper/search?query=<title>` via verify_refs.py: 24 titles, all HTTP 429 after retries.
- Semantic Scholar `GET https://api.semanticscholar.org/graph/v1/paper/arXiv:{id}?fields=title,venue,publicationVenue,year,externalIds,publicationTypes`: 4 arXiv ids (Task A), all HTTP 200.
- arXiv export API `GET https://export.arxiv.org/api/query?search_query=ti:"<title>"` via verify_refs.py: 24 titles.
- OpenReview API v2 `GET https://api2.openreview.net/notes/search?term=<title>&content=title&group=all&source=forum`: 4 titles (Task A).
- dblp `GET https://dblp.org/search/publ/api?q=<title>&format=json`: 4 attempts, all answered with a bot-check HTML page; not bypassed, recorded as unavailable.
- doi.org `HEAD https://doi.org/{doi}` and DataCite `GET https://api.datacite.org/dois/{doi}`: 2 DOIs (10.48550/arXiv.2509.06475, 10.5281/zenodo.16778599), both resolve.
- AIS eLibrary HTML pages (`GET`, bepress_citation_title meta tag): 9 pages, to obtain titles for identifier-less rows.
