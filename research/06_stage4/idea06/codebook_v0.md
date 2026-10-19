# Codebook v0 (draft, as applied in the 2026-10-19 pilot)

**Status.** Draft for the exploratory pilot. Not preregistered. Written on 2026-10-19 before the first pilot paper was coded. The items are not new. They are transcribed from the feasibility file `research/03_challenge/06-would-the-claim-survive-an-error-bar-auditing-st__feasibility.md`, section 2, which cites the idea record (`research/02_candidate_ideas_merged.json`, `ideas[5].design`). Decision rules marked **[FEAS]** are quoted or closely paraphrased from that file. Rules marked **[PILOT]** were added for this pilot and need the author's approval before preregistration.

## 0. Source text (verbatim)

Feasibility file, section 2: *"The codebook in the idea record (n items; runs/seeds; decoding stated; model name with version or access date; prompts released; SE/CI/significance test; LLM judge used; human validation of judge; agreement metric and chance correction; contamination discussed; code/data availability) is a set of binary or short-categorical items ..."*

Headline-claim rule (idea record, `design`, which the feasibility file adopts): *"the first quantitative comparison in the abstract, else the first in the results; the author-labelled main claim is coded as well."* Feasibility file, section 2: *"Fix in advance: code the metric, the two compared quantities, n, and whether n refers to items, cases or users."*

Inclusion criterion (idea record, `design`): *"the paper reports a quantitative evaluation of an LLM-based model, prompt, pipeline or agent on at least one dataset."*

## 0a. Reconciling "11 entries" with "14 items"

The verbatim list has **11 semicolon-separated entries** (numbered 1-11 below). The feasibility file's labour table and plan section 4.1 speak of **"14 items plus headline claim"**. No 14-item list is written anywhere in the records. Three entries join two separate reporting acts with "/" or "and": runs/seeds, agreement metric and chance correction, and code/data. **[PILOT]** Splitting those three gives exactly 14 coded fields: 1, 2a, 2b, 3, 4, 5, 6, 7, 8, 9a, 9b, 10, 11a, 11b.

"SE/CI/significance test" is **not** split. It lists alternative forms of one reporting act ("any uncertainty", RQ1 of the idea record), and the form used is recorded as the value. This reconciliation is the pilot coder's reading and is listed as a deviation in the README.

## 1. Values and locations

Every item takes one of these values:

| Value | Meaning |
|---|---|
| `Y` | Reported |
| `N` | Not reported |
| `P` | Partly reported (the item's definition says what counts as partial) |
| `NA` | Not applicable (e.g. judge items when no LLM judge is used; every item when the paper fails inclusion) |

Each value carries a **location**:
- `p.<k>` is the PDF page index, counted from 1 by the form-feed count of `pdftotext -layout` output. This index differs from the printed journal page numbers in Springer PDFs.
- `§<section>` is the section heading as printed.
- `N`/`NA` values carry the places searched, e.g. "searched: §4, App. A, keyword scan".

## 2. Items

**Inclusion (I0).** Does the paper meet the inclusion criterion above?
- **[PILOT]** "LLM-based" covers decoder LLMs, vision-language models and pretrained transformer language models used as the evaluated system, including fine-tuned encoder models such as BERT. Encoder-only cases are flagged.
- Values:
  - `Y`.
  - `N` with a reason: editorial, conceptual, review, qualitative, survey of attitudes, or no quantitative evaluation of an LLM system.
  - `B-H`: borderline. A human-subject experiment where the LLM is a treatment and the outcome is human performance or behaviour.
  - `B-T`: borderline. The evaluated generative model is not a language model (e.g. a GAN, or a tabular synthetic-data generator).
- If I0 is not `Y`, items 1-11b are `NA` and the paper cannot permit RQ2 under the primary reading.

1. **n items.** Is the size of the evaluation set used for the reported results stated?
   - **[FEAS]** Record whether n refers to items, cases or users.
   - `Y`: a number of test items per evaluated condition is stated or directly derivable, e.g. a table of split sizes.
   - `P`: only the total dataset size is given and the test split is unclear, or n is given for some evaluations but not the headline one.
2. **runs/seeds.** Split into two fields:
   - **2a. Repeated runs.**
     - `Y`: more than one run, sample or seed per reported configuration, with the number stated, or a spread such as SD or min-max over runs.
     - `P`: repetition mentioned without a number or spread.
   - **2b. Seeds.** `Y`: a random seed, or a fixed set of seeds, is stated for training or generation.
3. **Decoding stated.**
   - `Y`: the decoding settings of the evaluated generative model(s) are stated: temperature, or greedy/sampling with parameters, or max tokens with a sampling choice.
   - `P`: stated for some models or stages only.
   - `NA` if no generative decoding is involved, e.g. encoder classifiers.
4. **Model name with version or access date.** **[FEAS]**
   - `gpt-4` alone counts as no version. `gpt-4-0613`, or a name plus an access date, counts as a version.
   - **[PILOT]** For open-weight models, a Hugging Face identifier with size and variant (e.g. `Llama-3.1-8B-Instruct`) counts as `Y`. A bare family name ("Llama", "Qwen") counts as `N`.
   - `P`: versioned for some models and not for others.
5. **Prompts released.**
   - `Y`: the full prompt text (or templates) is in the paper, appendix or a linked repository.
   - `P`: excerpts or a description only.
   - `NA` if no prompting is involved (pure fine-tuned classifiers with no prompt).
6. **SE/CI/significance test (any uncertainty).**
   - `Y`: any standard error, confidence or credible interval, error bar, SD over runs, or significance test is reported for an evaluation result. Record which kind (SE, CI, SD, test).
   - `P`: reported for a secondary analysis only, not the main evaluation.
7. **LLM judge used.** Is an LLM used to score or label outputs of the evaluated system (LLM-as-a-judge, LLM-based evaluation metric, LLM annotator for the evaluation)?
8. **Human validation of judge.** `NA` if item 7 = `N`.
   - `Y`: the judge's outputs are compared with human judgements on some sample, with the number stated.
   - `P`: a human check is mentioned without numbers.
9. **Agreement metric and chance correction.** Split into two fields:
   - **9a. Agreement metric reported.** `Y`: any agreement statistic between the judge and humans (raw % agreement, correlation, kappa, alpha). `NA` if item 7 = `N`.
   - **9b. Chance-corrected.** `Y`: the statistic is chance-corrected (Cohen's or Fleiss' kappa, Krippendorff's alpha, Gwet's AC1). `NA` if item 7 = `N`.
   - **[PILOT]** Agreement among human annotators that does not involve the judge is noted in the comment but does not count for 9a/9b.
10. **Contamination discussed.**
    - `Y`: the paper discusses whether evaluation data could be in the evaluated model's training data, or takes a step against it (held-out, post-cutoff or private data).
    - `P`: private or new data are used, but contamination is not discussed as such.
11. **Code/data availability.** Split into two fields:
    - **11a. Code.** `Y`: a working link to code, or a statement that code is released.
      - `P`: "available on request" or "will be released".
    - **11b. Data.** `Y`: the evaluation data are public (a named public benchmark, or a released set).
      - `P`: partly public, or available on request.

## 3. Headline claim (H)

- **H1. Rule-based headline claim.** **[FEAS]** The first quantitative comparison in the abstract, else the first in the results. Record:
  - the sentence (quoted, at most 40 words) and its location;
  - the metric;
  - the two compared quantities (system A vs system B, with values);
  - n, and whether n is items, cases or users;
  - the comparison structure (H5).
  - **[PILOT]** A "quantitative comparison" needs two numbers, or one number plus an explicit numeric gain, for two named conditions. A single score with no comparator is not a comparison; the rule then moves to the next candidate in the abstract, then to the results.
- **H2. Author-labelled main claim.** The claim the authors state as their main result, if different from H1, with the same fields.
- **H3. n extractable.**
  - `Y`: n for the headline comparison can be read or derived from the paper.
  - `P`: only the total dataset size or an ambiguous split is given.
- **H4. Accuracies extractable.**
  - `Y`: both compared values are proportions of countable items (accuracy, success rate, exact match, pass rate, or recall/precision with a known denominator), and both are reported.
  - `P`: both values are reported but the metric is not a simple proportion (F1, BLEU/ROUGE, mean ratings, AUC).
- **H5. Structure.** **[FEAS]** Record any cluster structure (items grouped by document, user or task) that the paper reports, with cluster sizes if given.
  - **[PILOT]** Two systems scored on the same items count as `paired (same items)`.
- **RQ2 permitted.**
  - **[PILOT]** Primary (strict): I0 = `Y`, H3 = `Y` and H4 = `Y`.
  - Secondary (loose): I0 = `Y`, H3 in {`Y`, `P`} and H4 in {`Y`, `P`}.
  - The stopping rule's parenthesis, "(no n or no accuracies)", is read strictly for the primary outcome.

## 4. Uncertainty models applied to H1 when RQ2 is permitted

Implemented in `code/uncertainty_calc.py` (standard library only).

- **M1. Binomial interval at the reported n.**
  - Naive unpaired (Wald) SE of the difference of two proportions. The claim survives if |Δ| > 1.96·SE.
  - Newcombe's hybrid-score interval is computed as a check.
- **M2. Structure adjustment, where the paper reports a structure.**
  - Paired (same items): the paired SE is bounded below by assuming minimal discordance, sqrt((|Δ| - Δ²)/n), and above by maximal discordance, sqrt((min(p1+p2, 2-p1-p2) - Δ²)/n). The claim is reported as surviving under all, some or none of the admissible pairings.
  - Clustered with reported cluster size m: Miller-style design effect sqrt(1 + (m - 1)·ICC) with ICC in {0, 0.1, 0.3}.
  - `NA` if no structure is reported.
- **M3. Run-to-run variance (Atil et al. 15% band).**
  - Primary: worst case. Each arm's single-run accuracy can lie anywhere in a 15-percentage-point band, so a single-run claim survives only if |Δ| > 15 pp.
  - Sensitivity: σ_run = 15/4 = 3.75 pp per arm, treating the band as ±2σ, added in quadrature to the M1 SE.
  - If the paper reports a run SD, that SD replaces σ_run.
- **M4. Beta-Binomial (Bowyer et al. regime; the idea card's model (c)).** Independent Beta(1 + k, 1 + n - k) posteriors, 20,000 Monte Carlo draws, seed 20261015. The claim survives if the 95% credible interval of the difference excludes 0.

## 5. Not in v0 (candidates for v1)

These are recommended in the records but are not part of the feasibility file's list:
- judge protocol fields: scale, abstention handling, pooling (novelty file, after Rao and Callison-Burch);
- alignment of item definitions with "Awes, Laws, and Flaws" (arXiv 2408.15409) and the 2605.21404 scoring schema (feasibility file, section 2);
- a "paired variance identifiable" flag (feasibility file, section 2).
