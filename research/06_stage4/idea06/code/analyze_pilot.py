#!/usr/bin/env python3
"""Compile the idea-6 pilot: coded table, timing, item prevalence, screening counts,
claim survival summary and the stopping-rule table (section 4.1 of 02_candidate_ideas.md).

Inputs (all in the repository):
  --coding-dir   code/coding/papers/*.json  (one per pilot paper, written by the pilot coder)
  --sample       results/pilot/pilot_sample.csv (seeded draw)
  --timing       code/coding/coding_times.log (start/end epoch seconds per paper)
  --screening    code/coding/springer_oa_screening.csv (inclusion screening, 65 papers)
  --survival     results/pilot/claim_survival.csv (uncertainty_calc.py output)
  --frame-summary results/frame/frame_summary.json
Outputs to --out-dir: pilot_coding.csv, pilot_coding.md, pilot_timing.csv,
  item_prevalence.csv, screening_summary.csv, survival_summary.md, stopping_rule.json,
  stopping_rule.md
"""
import argparse
import csv
import glob
import json
import math
import os

ITEMS = [
    ("1_n_items", "1 n items"),
    ("2a_runs", "2a repeated runs"),
    ("2b_seeds", "2b seeds"),
    ("3_decoding", "3 decoding stated"),
    ("4_model_version", "4 model version/date"),
    ("5_prompts", "5 prompts released"),
    ("6_uncertainty", "6 SE/CI/test"),
    ("7_llm_judge", "7 LLM judge used"),
    ("8_judge_human_validation", "8 human validation of judge"),
    ("9a_agreement_metric", "9a agreement metric"),
    ("9b_chance_corrected", "9b chance-corrected"),
    ("10_contamination", "10 contamination discussed"),
    ("11a_code", "11a code available"),
    ("11b_data", "11b data available"),
]
THRESH_SHARE = 0.30   # stopping rule: "fewer than 30% of pilot papers permit RQ2"
THRESH_STRATUM = 25   # stopping rule: "Springer-OA stratum after inclusion screening is below 25"


def wilson(k, n, z=1.959963984540054):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (c - h, c + h)


def md_escape(s):
    return str(s).replace("|", "/").replace("\n", " ")


def main():
    ap = argparse.ArgumentParser()
    for k in ["coding-dir", "sample", "timing", "screening", "survival", "frame-summary", "out-dir"]:
        ap.add_argument("--" + k, required=True)
    a = ap.parse_args()
    os.makedirs(a.out_dir, exist_ok=True)

    sample = {r["pilot_id"]: r for r in csv.DictReader(open(a.sample, encoding="utf-8"))}
    codes = {}
    for p in sorted(glob.glob(os.path.join(a.coding_dir, "*.json"))):
        d = json.load(open(p, encoding="utf-8"))
        codes[d["pilot_id"]] = d
    assert set(codes) == set(sample), "every sampled paper must be coded"

    # timing
    t = {}
    for line in open(a.timing, encoding="utf-8"):
        pid, kind, epoch, iso = line.split()
        t.setdefault(pid, {})[kind] = (int(epoch), iso)
    timing_rows = []
    for pid in sample:
        s, e = t[pid]["start"], t[pid]["end"]
        timing_rows.append({"pilot_id": pid, "start_utc": s[1], "end_utc": e[1], "seconds": e[0] - s[0],
                            "I0": codes[pid]["I0"]["value"]})
    with open(os.path.join(a.out_dir, "pilot_timing.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(timing_rows[0].keys()))
        w.writeheader()
        w.writerows(timing_rows)

    # coded table
    rows = []
    for pid, s in sample.items():
        d = codes[pid]
        h = d["headline"]
        h1 = h["H1"]
        i0 = d["I0"]["value"]
        r = {"pilot_id": pid, "stratum": s["stratum"], "key": s["key"], "venue": s["venue"], "year": s["year"],
             "title": s["title"], "I0_inclusion": i0, "I0_reason": d["I0"]["reason"], "I0_loc": d["I0"]["loc"],
             "encoder_only": d.get("encoder_only"), "coded_for_information": d.get("coded_for_information", False)}
        items = d["items"]
        for key, label in ITEMS:
            if items == "NA_inclusion_failed":
                r[key] = "NA"
                r[key + "_loc"] = "inclusion failed"
            else:
                r[key] = items[key]["value"]
                r[key + "_loc"] = items[key].get("loc", "")
        r.update({"H1_sentence": h1["sentence"], "H1_loc": h1["loc"], "H1_metric": h1["metric"],
                  "H1_A": h1["A"], "H1_A_value": h1["A_value"], "H1_B": h1["B"], "H1_B_value": h1["B_value"],
                  "H1_n": h1["n"], "H1_n_unit": h1["n_unit"], "H1_structure": h1["structure"],
                  "H1_runs": h1["runs"], "H2_main_claim": h["H2"],
                  "H3_n_extractable": h["H3_n_extractable"], "H4_acc_extractable": h["H4_acc_extractable"]})
        n_numeric = str(h1["n"]).replace(",", "").isdigit()
        r["RQ2_strict"] = int(i0 == "Y" and h["H3_n_extractable"] == "Y" and h["H4_acc_extractable"] == "Y")
        r["RQ2_intermediate"] = int(i0 == "Y" and h["H4_acc_extractable"] == "Y" and
                                    (h["H3_n_extractable"] == "Y" or (h["H3_n_extractable"] == "P" and n_numeric)))
        r["RQ2_loose"] = int(i0 == "Y" and h["H3_n_extractable"] in ("Y", "P") and h["H4_acc_extractable"] in ("Y", "P"))
        r["seconds"] = next(x["seconds"] for x in timing_rows if x["pilot_id"] == pid)
        r["notes"] = d.get("notes", "")
        rows.append(r)
    fields = list(rows[0].keys())
    with open(os.path.join(a.out_dir, "pilot_coding.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    # item prevalence among included papers (I0 = Y)
    inc = [r for r in rows if r["I0_inclusion"] == "Y"]
    prev = []
    for key, label in ITEMS:
        vals = [r[key] for r in inc]
        app = [v for v in vals if v != "NA"]
        y = sum(v == "Y" for v in app)
        p = sum(v == "P" for v in app)
        lo, hi = wilson(y, len(app))
        prev.append({"item": label, "included_papers": len(inc), "applicable": len(app), "Y": y, "P": p,
                     "N": sum(v == "N" for v in app), "share_Y": f"{y/len(app):.2f}" if app else "NA",
                     "wilson95_Y": f"[{lo:.2f}, {hi:.2f}]" if app else "NA"})
    with open(os.path.join(a.out_dir, "item_prevalence.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(prev[0].keys()))
        w.writeheader()
        w.writerows(prev)

    # screening
    scr = list(csv.DictReader(open(a.screening, encoding="utf-8")))
    cnt = {}
    for r in scr:
        cnt[r["decision"]] = cnt.get(r["decision"], 0) + 1
    by_j = {}
    for r in scr:
        by_j.setdefault(r["journal"], {}).setdefault(r["decision"], 0)
        by_j[r["journal"]][r["decision"]] += 1
    srows = [{"journal": j, **{k: v.get(k, 0) for k in ["I", "B-T", "B-H", "E"]}, "total": sum(v.values())}
             for j, v in sorted(by_j.items())]
    srows.append({"journal": "ALL", **{k: cnt.get(k, 0) for k in ["I", "B-T", "B-H", "E"]}, "total": len(scr)})
    with open(os.path.join(a.out_dir, "screening_summary.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(srows[0].keys()))
        w.writeheader()
        w.writerows(srows)
    enc_only = sum(1 for r in scr if r["decision"] == "I" and r["encoder_only"] == "1")

    # survival
    surv = list(csv.DictReader(open(a.survival, encoding="utf-8")))

    # stopping rule
    n_pilot = len(rows)
    share = {k: sum(r[k] for r in rows) for k in ["RQ2_strict", "RQ2_intermediate", "RQ2_loose"]}
    strat = {"strict (I only)": cnt.get("I", 0),
             "I + borderline (B-T, B-H)": cnt.get("I", 0) + cnt.get("B-T", 0) + cnt.get("B-H", 0),
             "I excluding encoder-only": cnt.get("I", 0) - enc_only}
    crit_a = {k: (v / n_pilot) < THRESH_SHARE for k, v in share.items()}
    crit_b = {k: v < THRESH_STRATUM for k, v in strat.items()}
    by_stratum = {}
    for st in ["Springer-OA IS", "ACL industry"]:
        rr = [r for r in rows if r["stratum"] == st]
        by_stratum[st] = {k: f"{sum(r[k] for r in rr)}/{len(rr)}" for k in ["RQ2_strict", "RQ2_intermediate", "RQ2_loose"]}
    among_included = {k: f"{sum(r[k] for r in inc)}/{len(inc)}" for k in ["RQ2_strict", "RQ2_intermediate", "RQ2_loose"]}
    primary_trig = crit_a["RQ2_strict"] and crit_b["strict (I only)"]
    out = {
        "rule_text": ("stop (or demote to a CAIS methods essay) if any of the following holds after the pilot and the "
                      "eLibrary search: a published IS-venue audit of statistical or judge-validation practice in LLM "
                      "papers is found; fewer than 30% of pilot papers permit RQ2 (no n or no accuracies) and the "
                      "Springer-OA stratum after inclusion screening is below 25 empirical papers; or no second coder "
                      "has been secured within four weeks and no AIS eLibrary access is obtainable"),
        "source": "research/02_candidate_ideas.md section 4.1",
        "pilot_papers": n_pilot,
        "criterion_2a_share_permitting_RQ2": {k: {"count": v, "share": round(v / n_pilot, 3), "below_30pct": crit_a[k]}
                                              for k, v in share.items()},
        "criterion_2a_primary": "RQ2_strict (pre-specified in codebook_v0.md before coding); RQ2_loose is the pre-specified secondary; RQ2_intermediate was added after coding (post hoc)",
        "criterion_2a_by_stratum": by_stratum,
        "criterion_2a_among_included_papers_supplementary": among_included,
        "criterion_2b_springer_oa_after_screening": {k: {"count": v, "below_25": crit_b[k]} for k, v in strat.items()},
        "criterion_2b_primary": "strict (I only)",
        "criterion_2_pilot_outcome_primary": "holds" if primary_trig else "does not hold",
        "criterion_2_pilot_outcome_all_variants": {f"{ka} & {kb}": (crit_a[ka] and crit_b[kb]) for ka in crit_a for kb in crit_b},
        "criterion_1_literature": "undetermined (the literature check is run by another agent)",
        "criterion_3_second_coder_and_eLibrary": "undetermined (second coder is an author decision; the four-week window has not elapsed; eLibrary access not obtained in this run)",
        "overall": ("triggered by criterion 2 under the pre-specified primary reading; criteria 1 and 3 undetermined"
                    if primary_trig else "criterion 2 not triggered under the primary reading; criteria 1 and 3 undetermined"),
        "claims_run": len(surv),
    }
    json.dump(out, open(os.path.join(a.out_dir, "stopping_rule.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    # Markdown outputs
    L = ["# Pilot coded table (exploratory; machine-assisted single coder)", "",
         "Generated by `code/analyze_pilot.py` from `code/coding/papers/*.json`. Values: Y / P (partial) / N / NA. "
         "Locations are PDF page indices (pdftotext form-feed count) and sections; see `pilot_coding.csv` for every location.", "",
         "## Inclusion, headline claim and RQ2", "",
         "| ID | Venue, year | Title (truncated) | I0 | H1 metric | H1 values (A vs B) | n | H3 n | H4 acc | RQ2 strict / intermediate / loose | seconds |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        vals = f"{r['H1_A_value']} vs {r['H1_B_value']}" if r["H1_A_value"] else ""
        L.append(f"| {r['pilot_id']} | {r['venue']} {r['year']} | {md_escape(r['title'][:60])} | {r['I0_inclusion']} | "
                 f"{md_escape(r['H1_metric'][:50])} | {md_escape(vals)} | {md_escape(str(r['H1_n'])[:20])} | {r['H3_n_extractable']} | "
                 f"{r['H4_acc_extractable']} | {r['RQ2_strict']} / {r['RQ2_intermediate']} / {r['RQ2_loose']} | {r['seconds']} |")
    L += ["", "## Codebook items (papers passing or coded for information)", "",
          "| ID | " + " | ".join(lbl.split(" ")[0] for _, lbl in ITEMS) + " |",
          "|---|" + "---|" * len(ITEMS)]
    for r in rows:
        if r["I0_inclusion"] == "Y" or r["coded_for_information"]:
            L.append(f"| {r['pilot_id']}{' (info)' if r['coded_for_information'] else ''} | " + " | ".join(r[k] for k, _ in ITEMS) + " |")
    L += ["", "Item key: " + "; ".join(lbl for _, lbl in ITEMS) + ".", "",
          "## Reasons and notes", ""]
    for r in rows:
        L.append(f"- **{r['pilot_id']}** ({r['key']}). I0 = {r['I0_inclusion']}: {md_escape(r['I0_reason'])}."
                 + (f" Headline: \"{md_escape(r['H1_sentence'])}\" ({md_escape(r['H1_loc'])})." if r["H1_sentence"] else "")
                 + (f" Note: {md_escape(r['notes'])}" if r["notes"] else ""))
    open(os.path.join(a.out_dir, "pilot_coding.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")

    S = ["# Claim survival under the uncertainty models (exploratory)", "",
         "Generated from `claim_survival.csv` (`code/uncertainty_calc.py`, seed 20261015, 20,000 Beta draws). "
         "A claim survives when the model's 95% interval for the difference excludes 0. "
         "M2 paired: 'all' = survives at the unpaired SE (upper bound if item-level errors are not negatively correlated), "
         "'some' = only at smaller SEs, 'none' = not even at the minimal-discordance SE.", "",
         "| Claim | Paper | Role | Metric | A vs B (%) | diff (pp) | n (source) | M1 Wald | M1 Newcombe | M2 paired | M2 cluster ICC 0.1 / 0.3 | M3 band (|diff| > 15 pp) | M3 sd 3.75 pp | M4 Beta |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for s in surv:
        S.append(f"| {s['claim_id']} | {s['pilot_id']} | {s['role']} | {md_escape(s['metric'])} | {s['p_a_pct']} vs {s['p_b_pct']} | "
                 f"{s['diff_pp']} | {s['n_a']} ({md_escape(s['n_source'])}) | {s['M1_wald_survives']} {s['M1_wald_ci_pp']} | "
                 f"{s['M1_newcombe_survives']} | {s['M2_paired_survival']} | "
                 f"{s['M2_cluster_icc0.1_survives'].split(' ')[0]} / {s['M2_cluster_icc0.3_survives'].split(' ')[0]} | "
                 f"{s['M3_band_worst_survives']} | {s['M3_sd_survives']} | {s['M4_beta_survives']} {s['M4_beta_cri_pp']} |")
    h1 = [s for s in surv if s["role"].startswith("H1")]
    S += ["", f"Rule-based headline claims (H1) run: {len(h1)}; surviving M1 Wald: "
          f"{sum(s['M1_wald_survives']=='yes' for s in h1)}; M2 paired 'all': {sum(s['M2_paired_survival']=='all' for s in h1)}; "
          f"M3 band: {sum(s['M3_band_worst_survives']=='yes' for s in h1)}; M3 sd: {sum(s['M3_sd_survives']=='yes' for s in h1)}; "
          f"M4 Beta: {sum(s['M4_beta_survives']=='yes' for s in h1)}."]
    open(os.path.join(a.out_dir, "survival_summary.md"), "w", encoding="utf-8").write("\n".join(S) + "\n")

    T = ["# Stopping rule (section 4.1), criterion by criterion", "",
         f"Rule as written: *\"{out['rule_text']}\"*", "",
         "| Criterion | Reading | Value | Threshold | Holds? |", "|---|---|---|---|---|"]
    for k, v in out["criterion_2a_share_permitting_RQ2"].items():
        tag = {'RQ2_strict': ' (primary, pre-specified)', 'RQ2_loose': ' (secondary, pre-specified)', 'RQ2_intermediate': ' (post hoc: n from standard benchmark size allowed)'}[k]
        T.append(f"| 2a share of pilot papers permitting RQ2 | {k}{tag} | {v['count']}/{n_pilot} = {v['share']:.0%} | < 30% | {'yes' if v['below_30pct'] else 'no'} |")
    for k, v in out["criterion_2b_springer_oa_after_screening"].items():
        tag2 = {'strict (I only)': ' (primary)', 'I + borderline (B-T, B-H)': ' (sensitivity)', 'I excluding encoder-only': ' (sensitivity)'}[k]
        T.append(f"| 2b Springer-OA stratum after inclusion screening | {k}{tag2} | {v['count']} | < 25 | {'yes' if v['below_25'] else 'no'} |")
    T.append(f"| 2 (2a AND 2b) | primary readings | 2a {share['RQ2_strict']}/{n_pilot}, 2b {strat['strict (I only)']} | both | **{out['criterion_2_pilot_outcome_primary']}** |")
    T.append("| 1 published IS-venue audit found | - | undetermined | - | undetermined (another agent runs the literature check) |")
    T.append("| 3 no second coder in four weeks and no AIS eLibrary access | - | undetermined | - | undetermined (author decision; window not elapsed) |")
    T += ["", f"RQ2 by stratum: {json.dumps(by_stratum)}; among included papers only (supplementary, not the rule's denominator): {json.dumps(among_included)}."]
    open(os.path.join(a.out_dir, "stopping_rule.md"), "w", encoding="utf-8").write("\n".join(T) + "\n")
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
