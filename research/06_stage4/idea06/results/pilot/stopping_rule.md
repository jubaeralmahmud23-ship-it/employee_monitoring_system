# Stopping rule (section 4.1), criterion by criterion

Rule as written: *"stop (or demote to a CAIS methods essay) if any of the following holds after the pilot and the eLibrary search: a published IS-venue audit of statistical or judge-validation practice in LLM papers is found; fewer than 30% of pilot papers permit RQ2 (no n or no accuracies) and the Springer-OA stratum after inclusion screening is below 25 empirical papers; or no second coder has been secured within four weeks and no AIS eLibrary access is obtainable"*

| Criterion | Reading | Value | Threshold | Holds? |
|---|---|---|---|---|
| 2a share of pilot papers permitting RQ2 | RQ2_strict (primary, pre-specified) | 3/20 = 15% | < 30% | yes |
| 2a share of pilot papers permitting RQ2 | RQ2_intermediate (post hoc: n from standard benchmark size allowed) | 5/20 = 25% | < 30% | yes |
| 2a share of pilot papers permitting RQ2 | RQ2_loose (secondary, pre-specified) | 7/20 = 35% | < 30% | no |
| 2b Springer-OA stratum after inclusion screening | strict (I only) (primary) | 14 | < 25 | yes |
| 2b Springer-OA stratum after inclusion screening | I + borderline (B-T, B-H) (sensitivity) | 21 | < 25 | yes |
| 2b Springer-OA stratum after inclusion screening | I excluding encoder-only (sensitivity) | 13 | < 25 | yes |
| 2 (2a AND 2b) | primary readings | 2a 3/20, 2b 14 | both | **holds** |
| 1 published IS-venue audit found | - | undetermined | - | undetermined (another agent runs the literature check) |
| 3 no second coder in four weeks and no AIS eLibrary access | - | undetermined | - | undetermined (author decision; window not elapsed) |

RQ2 by stratum: {"Springer-OA IS": {"RQ2_strict": "0/10", "RQ2_intermediate": "0/10", "RQ2_loose": "0/10"}, "ACL industry": {"RQ2_strict": "3/10", "RQ2_intermediate": "5/10", "RQ2_loose": "7/10"}}; among included papers only (supplementary, not the rule's denominator): {"RQ2_strict": "3/10", "RQ2_intermediate": "5/10", "RQ2_loose": "7/10"}.
