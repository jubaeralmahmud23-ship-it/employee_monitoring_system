"""Step 07: stopping-rule table, pilot summary and figures from the result files.

Usage:
    python -I 07_report.py <results_dir> <derived_dir>

Reads only files written by steps 02-06.  Writes:
  stopping_rule.csv / stopping_rule.json   criterion-by-criterion evaluation of the section 4.2 rule
  pilot_summary.json                        key numbers with their source files
  fig_tau_distribution.png                  pairwise tau, within- vs cross-metric, both logs
  fig_primary_contrasts.png                 bootstrap intervals for the primary contrasts, both logs
  fig_tau_matrix.png                        117 x 117 tau matrices ordered by metric, both logs
  bootstrap_intervals_percentile_vs_basic.csv  percentile and basic (reflected) bootstrap intervals
The tau-matrix figure is drawn from the per-config score matrices in derived_dir
(aggregate over workers: configuration-by-configuration correlations only).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

import idea05lib as L  # noqa: E402

LOGS = ["bpic2017", "bpic2019"]
SERIES = {"bpic2017": "#2a78d6", "bpic2019": "#eb6834"}   # validated categorical slots 1-2 (light)
WITHIN, CROSS = "#2a78d6", "#eb6834"
INK, INK2, MUTED, GRID, AXIS, SURF = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7", "#fcfcfb"
LABEL = {"bpic2017": "BPI Challenge 2017", "bpic2019": "BPI Challenge 2019"}


def style(ax):
    ax.set_facecolor(SURF)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(AXIS)
    ax.tick_params(colors=MUTED, labelcolor=INK2, labelsize=8)
    ax.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)


def load(outdir, name):
    with open(os.path.join(outdir, name)) as fh:
        return json.load(fh)


def main():
    outdir, derived = sys.argv[1:3]
    plt.rcParams.update({"font.family": "sans-serif", "font.size": 9, "text.color": INK, "axes.labelcolor": INK2,
                         "figure.facecolor": SURF, "savefig.facecolor": SURF})
    tau = {lg: load(outdir, f"{lg}_tau_summary.json") for lg in LOGS}
    boot = {lg: load(outdir, f"{lg}_bootstrap_stopping.json") for lg in LOGS}
    plac = {lg: load(outdir, f"{lg}_placebo_summary.json") for lg in LOGS}
    sens = {lg: pd.read_csv(os.path.join(outdir, f"{lg}_sensitivity.csv")) for lg in LOGS}

    # ---------------- stopping rule ----------------
    rows = []
    for lg in LOGS:
        t, b = tau[lg], boot[lg]
        rows.append({"criterion": "1a median Kendall tau across defensible configurations > 0.9", "log": lg,
                     "statistic": "median tau-b over 6,786 distinct configuration pairs (primary)",
                     "value": t["median_tau_distinct"], "ci95_lo": b["median_tau_distinct"]["ci95_lo"],
                     "ci95_hi": b["median_tau_distinct"]["ci95_hi"], "threshold": "> 0.9",
                     "condition_met": bool(t["median_tau_distinct"] > 0.9)})
        rows.append({"criterion": "1a (alternative reading) same, over the 81,810 pairs of the 405 cells", "log": lg,
                     "statistic": "median tau-b, 405-cell pairs (identical cells count tau = 1)",
                     "value": t["median_tau_405cells"], "ci95_lo": b["median_tau_405cells"]["ci95_lo"],
                     "ci95_hi": b["median_tau_405cells"]["ci95_hi"], "threshold": "> 0.9",
                     "condition_met": bool(t["median_tau_405cells"] > 0.9)})
        rows.append({"criterion": "1b bottom-quintile reclassification under case-mix adjustment < 10%", "log": lg,
                     "statistic": "median over 78 distinct none-vs-adjusted pairs of the share of the unadjusted bottom quintile leaving it (primary)",
                     "value": t["reclassification"]["median_reclass_bottom_distinct"],
                     "ci95_lo": b["median_reclass_bottom_distinct"]["ci95_lo"], "ci95_hi": b["median_reclass_bottom_distinct"]["ci95_hi"],
                     "threshold": "< 0.10", "condition_met": bool(t["reclassification"]["median_reclass_bottom_distinct"] < 0.10)})
        rows.append({"criterion": "1b (alternative reading) share of ALL ranked workers whose bottom-quintile status changes", "log": lg,
                     "statistic": "median over 78 distinct pairs of |B_none symmetric-difference B_adj| / n",
                     "value": t["reclassification"]["median_status_change_all_distinct"],
                     "ci95_lo": b["median_status_change_all_distinct"]["ci95_lo"], "ci95_hi": b["median_status_change_all_distinct"]["ci95_hi"],
                     "threshold": "< 0.10", "condition_met": bool(t["reclassification"]["median_status_change_all_distinct"] < 0.10)})
    sr = pd.DataFrame(rows)
    prim = sr[~sr["criterion"].str.contains("alternative")]
    stop_primary = bool(prim["condition_met"].all())
    alt_tau = sr[sr["criterion"].str.contains("405 cells")]
    alt_rc = sr[sr["criterion"].str.contains("ALL ranked")]
    stop_any_reading = bool((sr[sr["criterion"].str.startswith("1a")].groupby("log")["condition_met"].any().all())
                            and (sr[sr["criterion"].str.startswith("1b")].groupby("log")["condition_met"].any().all()))
    sens_max_tau = {lg: float(sens[lg]["median_tau_distinct"].max()) for lg in LOGS}
    sens_max_tau_within = {lg: float(sens[lg]["median_tau_within_metric_distinct"].max()) for lg in LOGS}
    sens_min_rc = {lg: float(sens[lg]["median_reclass_bottom_distinct"].min()) for lg in LOGS}
    sr.to_csv(os.path.join(outdir, "stopping_rule.csv"), index=False)
    verdict = {
        "rule_text_section_4.2": ("stop the confirmatory framing ... if, after excluding labelled or detected system accounts and resources "
                                  "below the pre-registered minimum-event threshold, the median Kendall tau across defensible configurations "
                                  "exceeds 0.9 on both BPI 2017 and BPI 2019 and bottom-quintile reclassification under case-mix adjustment "
                                  "is below 10% on both; also stop if the proceedings sweep finds a rank-stability study of resource measures on public logs."),
        "empirical_clause_all_four_conditions_met_primary_reading": stop_primary,
        "empirical_clause_met_under_any_reading_shown": stop_any_reading,
        "sensitivity_max_median_tau_any_variant": sens_max_tau,
        "sensitivity_max_within_metric_median_tau_any_variant": sens_max_tau_within,
        "sensitivity_min_median_reclass_any_variant": sens_min_rc,
        "bootstrap_share_replicates_median_tau_gt_0.9": {lg: boot[lg]["share_replicates_median_tau_distinct_gt_0.9"] for lg in LOGS},
        "bootstrap_share_replicates_median_reclass_lt_0.10": {lg: boot[lg]["share_replicates_median_reclass_bottom_distinct_lt_0.10"] for lg in LOGS},
        "literature_clause": "not assessed in this pilot (the ICPM/BPM proceedings sweep was not part of this run)",
        "outcome_empirical_clause": "not triggered" if not stop_primary else "triggered",
    }
    with open(os.path.join(outdir, "stopping_rule.json"), "w") as fh:
        json.dump(verdict, fh, indent=1)

    # ---------------- pilot summary ----------------
    summ = {"seed": L.SEED, "n_min_events": L.N_MIN_EVENTS, "logs": {}}
    for lg in LOGS:
        t = tau[lg]
        summ["logs"][lg] = {
            "n_ranked": t["n_analysis_set"], "median_tau_distinct": t["median_tau_distinct"], "median_tau_405cells": t["median_tau_405cells"],
            "median_tau_within_metric": t["median_tau_within_metric_distinct"], "median_tau_cross_metric": t["median_tau_cross_metric_distinct"],
            "median_tau_by_metric_within": t["median_tau_by_metric_within"],
            "median_reclass_bottom": t["reclassification"]["median_reclass_bottom_distinct"],
            "median_status_change_all": t["reclassification"]["median_status_change_all_distinct"],
            "placebo_mean_median_tau": plac[lg]["placebo"]["median_tau_distinct"]["mean"],
            "placebo_range_median_tau": [plac[lg]["placebo"]["median_tau_distinct"]["min"], plac[lg]["placebo"]["median_tau_distinct"]["max"]],
            "placebo_mean_within_metric_tau": plac[lg]["placebo"]["median_tau_within_metric_distinct"]["mean"],
            "placebo_range_within_metric_tau": [plac[lg]["placebo"]["median_tau_within_metric_distinct"]["min"], plac[lg]["placebo"]["median_tau_within_metric_distinct"]["max"]],
            "placebo_mean_median_reclass": plac[lg]["placebo"]["median_reclass_bottom_distinct"]["mean"],
            "bootstrap_ci_median_tau": [boot[lg]["median_tau_distinct"]["ci95_lo"], boot[lg]["median_tau_distinct"]["ci95_hi"]],
            "bootstrap_ci_median_reclass": [boot[lg]["median_reclass_bottom_distinct"]["ci95_lo"], boot[lg]["median_reclass_bottom_distinct"]["ci95_hi"]],
            "sources": [f"{lg}_tau_summary.json", f"{lg}_bootstrap_stopping.json", f"{lg}_placebo_summary.json"],
        }
    with open(os.path.join(outdir, "pilot_summary.json"), "w") as fh:
        json.dump(summ, fh, indent=1)

    # ---------------- percentile vs basic bootstrap intervals ----------------
    brow = []
    for lg in LOGS:
        rep = pd.read_csv(os.path.join(outdir, f"{lg}_bootstrap_replicates.csv"))
        pts = {k: boot[lg][k]["point"] for k in ["median_tau_distinct", "median_tau_405cells", "median_tau_within_metric_distinct",
                                                 "median_reclass_bottom_distinct", "median_reclass_bottom_405", "median_status_change_all_distinct"]}
        bcx = pd.read_csv(os.path.join(outdir, f"{lg}_bootstrap_contrasts.csv"))
        for _, r in bcx.iterrows():
            pts[("tau::" if r["statistic"] == "kendall_tau_b" else "reclass::") + r["contrast"]] = r["point"]
        for k, pt in pts.items():
            v = rep[k].to_numpy(dtype=float)
            lo, hi = np.nanpercentile(v, 2.5), np.nanpercentile(v, 97.5)
            brow.append({"log": lg, "statistic": k, "point": pt, "boot_mean": float(np.nanmean(v)), "bias_boot_mean_minus_point": float(np.nanmean(v) - pt),
                         "percentile_lo": lo, "percentile_hi": hi, "basic_lo": 2 * pt - hi, "basic_hi": 2 * pt - lo,
                         "point_outside_percentile_interval": bool(pt < lo or pt > hi)})
    pd.DataFrame(brow).to_csv(os.path.join(outdir, "bootstrap_intervals_percentile_vs_basic.csv"), index=False)

    # ---------------- figure 1: tau distribution ----------------
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.6), sharey=False)
    for ax, lg in zip(axes, LOGS):
        style(ax)
        h = pd.read_csv(os.path.join(outdir, f"{lg}_tau_hist.csv"))
        x = np.r_[h["bin_lo"].to_numpy(), h["bin_hi"].iloc[-1]]
        cross = h["distinct_pairs"] - h["within_metric_distinct_pairs"]
        tot_w, tot_c = h["within_metric_distinct_pairs"].sum(), cross.sum()
        ax.stairs(cross / tot_c, x, color=CROSS, linewidth=2, label=f"different metric ({tot_c:,} pairs)")
        ax.stairs(h["within_metric_distinct_pairs"] / tot_w, x, color=WITHIN, linewidth=2, label=f"same metric ({tot_w:,} pairs)")
        for v, lab in ((0.9, "0.9 stop threshold"), (0.7, "0.7 (H1)")):
            ax.axvline(v, color=MUTED, linewidth=1, linestyle=(0, (3, 2)))
            ax.text(v - 0.02, ax.get_ylim()[1] * 0.97, lab, color=INK2, fontsize=7.5, ha="right", va="top", rotation=90)
        m = tau[lg]["median_tau_distinct"]
        ax.axvline(m, color=INK, linewidth=1)
        ax.set_xlim(-0.6, 1.02)
        ax.set_xlabel("Kendall tau-b between two configurations")
        ax.set_ylabel("share of pairs within group")
        ax.set_title(f"{LABEL[lg]} ({tau[lg]['n_analysis_set']} workers); black line: median {m:.2f}",
                     fontsize=9, color=INK, loc="left")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, [l.split(" (")[0] + " pairs" for l in labels], frameon=False, fontsize=8, loc="upper right",
               ncol=2, labelcolor=INK2, bbox_to_anchor=(0.99, 0.99))
    fig.suptitle("Pairwise rank agreement across the 117 distinct scoring configurations", fontsize=10.5, color=INK, x=0.01, ha="left")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(os.path.join(outdir, "fig_tau_distribution.png"), dpi=150)
    plt.close(fig)

    # ---------------- figure 2: primary contrasts ----------------
    bc = {lg: pd.read_csv(os.path.join(outdir, f"{lg}_bootstrap_contrasts.csv")) for lg in LOGS}
    names = [c[0] for c in L.primary_contrasts()]
    fig, axes = plt.subplots(1, 2, figsize=(10, 6.2), sharey=True)
    for ax, stat, xlab in zip(axes, ["kendall_tau_b", "bottom_quintile_reclassification"],
                              ["Kendall tau-b (95% case-bootstrap interval)", "share of bottom quintile reclassified (95% interval)"]):
        style(ax)
        ax.grid(True, axis="y", color=SURF)
        y = np.arange(len(names))[::-1]
        for off, lg in ((0.17, "bpic2017"), (-0.17, "bpic2019")):
            d = bc[lg][bc[lg]["statistic"] == stat].set_index("contrast").loc[names]
            ax.hlines(y + off, d["ci95_lo"], d["ci95_hi"], color=SERIES[lg], linewidth=2)
            ax.plot(d["point"], y + off, "o", color=SERIES[lg], markersize=5, markeredgecolor=SURF, markeredgewidth=1, label=LABEL[lg])
        thr = 0.9 if stat == "kendall_tau_b" else 0.10
        ax.axvline(thr, color=MUTED, linewidth=1, linestyle=(0, (3, 2)))
        ax.text(thr + (-0.01 if stat == "kendall_tau_b" else 0.01), len(names) - 0.3, f"stop threshold {thr:g}", color=INK2,
                fontsize=7.5, ha="right" if stat == "kendall_tau_b" else "left", va="bottom")
        ax.set_yticks(np.arange(len(names))[::-1])
        ax.set_yticklabels(names, fontsize=7.5)
        ax.set_xlabel(xlab)
        ax.set_ylim(-0.7, len(names) + 0.3)
    axes[0].set_xlim(-0.4, 1.05)
    axes[1].set_xlim(-0.02, 1.02)
    axes[0].legend(frameon=False, fontsize=8, loc="lower left", labelcolor=INK2)
    fig.suptitle("Primary contrasts against the dashboard baseline (completed cases, last touch, month, no adjustment)",
                 fontsize=10.5, color=INK, x=0.01, ha="left")
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, "fig_primary_contrasts.png"), dpi=150)
    plt.close(fig)

    # ---------------- figure 3: tau matrices ----------------
    cells, distinct = L.build_space()
    cmap = LinearSegmentedColormap.from_list("div", ["#e34948", "#f0efec", "#2a78d6"])
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.9))
    order = np.argsort(distinct["metric"].map({m: i for i, m in enumerate(L.METRICS)}).to_numpy() * 1000 + distinct["cfg"].to_numpy(), kind="stable")
    bounds = np.cumsum([int((distinct["metric"] == m).sum()) for m in L.METRICS])
    for ax, lg in zip(axes, LOGS):
        z = np.load(os.path.join(derived, f"{lg}_scores_primary.npz"), allow_pickle=True)
        T = L.tau_b_matrix(z["S"][:, z["A"]])[np.ix_(order, order)]
        im = ax.imshow(T, cmap=cmap, vmin=-1, vmax=1, interpolation="nearest")
        for bnd in bounds[:-1]:
            ax.axhline(bnd - 0.5, color=SURF, linewidth=2)
            ax.axvline(bnd - 0.5, color=SURF, linewidth=2)
        mids = np.r_[0, bounds[:-1]] + np.diff(np.r_[0, bounds]) / 2 - 0.5
        ax.set_xticks(mids)
        ax.set_xticklabels(L.METRICS, fontsize=8, color=INK2)
        ax.set_yticks(mids)
        ax.set_yticklabels(L.METRICS, fontsize=8, color=INK2)
        ax.tick_params(length=0)
        for s in ax.spines.values():
            s.set_visible(False)
        ax.set_title(LABEL[lg], fontsize=9.5, color=INK, loc="left")
    cb = fig.colorbar(im, ax=axes, fraction=0.025, pad=0.02)
    cb.set_label("Kendall tau-b", color=INK2)
    cb.ax.tick_params(labelsize=8, colors=MUTED, labelcolor=INK2)
    cb.outline.set_visible(False)
    fig.suptitle("Configuration-by-configuration rank agreement, blocks ordered by metric "
                 "(EPH events/active hour, CCA completed cases, APT processing time, RWK rework, DLA deadline)",
                 fontsize=9, color=INK, x=0.01, ha="left")
    fig.savefig(os.path.join(outdir, "fig_tau_matrix.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(sr.to_string())
    print(json.dumps(verdict, indent=1))


if __name__ == "__main__":
    main()
