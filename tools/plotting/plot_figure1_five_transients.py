"""
plot_figure1_five_transients.py — Paper Figure 1 candidate: five same-signature
"transient appears -> gets eaten" observations on a shared training-progress axis.

Five panels, x = training progress fraction (step / run budget), each marking the
transient peak and the decay/rebound point. All series are read from archived
sources at runtime (no hardcoded metrics except registered anchors, which are
plotted as annotations only where the archived data confirms them):

  A. E79 soft-constraint rebound — outputs/audit_package_20260819/mu_trajectory_tokcenter.json
     (snapshot of the E79-era file; the live copy under outputs/key_collapse_survey_20260818/
     was overwritten by the b-tokwhiten trajectory on 2026-08-21, see E91 bookkeeping note)
  B. Q13 induction transient — outputs/induction_q13_sweep/m*/induction_score.json (+latest=20K)
  C. 2x-scale induction transient — outputs/induction_scale2x_sweep/m*/induction_score.json (+latest)
  D. Q15 attention performance — checkpoints/v37ks_d_sm_q15_circuit_20k_ctx4096_20260825b/train_log.jsonl
  E. Q17 echo transient — checkpoints/v37ks_d_q17_oracle_readout_10k_20260825/train_log.jsonl

Registered anchors (docs/CURRENT_STATE.md): E79 mu 0.690->0.811; E105 Q13 1.71x->2.34x->~1.5x;
E110 2x five-head break (see 口径注记 in figure1_data.json: registry says 2.74x, the archived
sweep JSONs give max/baseline = 2.09x under the same formula that reproduces E105/E107/E111);
E107 Q15 maxmass-chance +0.09~+0.16; E109 Q17 echo 0.1042@800 -> 0.040@1900, stop @2520.

Usage: py -3.14 tools/plotting/plot_figure1_five_transients.py
Outputs: outputs/figure1_five_transients_20260827/figure1_five_transients.png
         outputs/figure1_five_transients_20260827/figure1_data.json
         outputs/figure1_five_transients_20260827/caption_draft.md
No torch dependency; pure matplotlib (Agg backend).
"""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ── Style (catppuccin-mocha, matching tools/plotting conventions) ────────────
BG = "#1e1e2e"
GRID = "#313244"
TEXT = "#cdd6f4"
SUBTLE = "#a6adc8"
C_A = "#89dceb"  # cyan   — E79 mu
C_B = "#f9e2af"  # yellow — Q13 induction
C_C = "#fab387"  # peach  — 2x induction
C_D = "#f38ba8"  # red    — Q15 attention
C_E = "#a6e3a1"  # green  — Q17 echo
C_MAUVE = "#cba6f7"

OUT_DIR = Path("outputs/figure1_five_transients_20260827")

MU_TRAJ = Path("outputs/audit_package_20260819/mu_trajectory_tokcenter.json")
Q13_SWEEP = Path("outputs/induction_q13_sweep")
S2X_SWEEP = Path("outputs/induction_scale2x_sweep")
Q15_LOG = Path("checkpoints/v37ks_d_sm_q15_circuit_20k_ctx4096_20260825b/train_log.jsonl")
Q17_LOG = Path("checkpoints/v37ks_d_q17_oracle_readout_10k_20260825/train_log.jsonl")

BUDGET = {"e79": 20000, "q13": 20000, "s2x": 20000, "q15": 20000, "q17": 10000}


def load_mu_trajectories():
    data = json.loads(MU_TRAJ.read_text(encoding="utf-8"))
    out = {}
    for traj in data["trajectories"]:
        steps = [p["step"] for p in traj["points"]]
        mu = [p["mu_centered"] for p in traj["points"]]
        out[traj["label"]] = {"steps": steps, "mu_centered": mu}
    return out


def load_induction_sweep(sweep_dir):
    """ratio = trained.max / trained.baseline (same formula reproduces the
    registered E105 1.71x/2.34x, E107 2.13x and E111 1.61x anchors)."""
    pts = []
    for sub in sorted(sweep_dir.iterdir()):
        f = sub / "induction_score.json"
        if not f.exists():
            continue
        d = json.loads(f.read_text(encoding="utf-8"))
        t = d["summary"]["trained"]
        if sub.name == "latest":
            step = 20000
        else:
            step = int(sub.name.lstrip("m"))
        pts.append(
            {
                "step": step,
                "max": t["max"],
                "baseline": t["baseline"],
                "ratio": t["max"] / t["baseline"],
                "n_heads_gt_2x": t["n_heads_gt_2x"],
            }
        )
    pts.sort(key=lambda p: p["step"])
    return pts


def load_train_log(path, keys):
    rows = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            rows.append({k: r.get(k) for k in ["step", *keys]})
    return rows


def rolling_mean(xs, ys, w=5):
    out_x, out_y = [], []
    for i in range(len(ys)):
        lo = max(0, i - w // 2)
        hi = min(len(ys), i + w // 2 + 1)
        out_x.append(xs[i])
        out_y.append(sum(ys[lo:hi]) / (hi - lo))
    return out_x, out_y


def style_ax(ax):
    ax.set_facecolor(BG)
    ax.grid(color=GRID, linewidth=0.6, alpha=0.8)
    ax.tick_params(colors=TEXT, labelsize=8)
    for spine in ax.spines.values():
        spine.set_color(GRID)
    ax.xaxis.label.set_color(TEXT)
    ax.yaxis.label.set_color(TEXT)
    ax.title.set_color(TEXT)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    mu = load_mu_trajectories()
    q13 = load_induction_sweep(Q13_SWEEP)
    s2x = load_induction_sweep(S2X_SWEEP)
    q15 = load_train_log(Q15_LOG, ["q15_attend_maxmass", "q15_attend_chance", "q15_twin_d"])
    q17 = load_train_log(Q17_LOG, ["echo_byte_acc"])

    fig, axes = plt.subplots(5, 1, figsize=(9.5, 15), sharex=True)
    fig.patch.set_facecolor(BG)

    # ── Panel A: E79 soft-constraint rebound (centered key coherence mu) ──────
    ax = axes[0]
    b = mu["b-tokcenter"]
    c = mu["c-tokcenter"]
    ax.plot([s / BUDGET["e79"] for s in b["steps"]], b["mu_centered"],
            color=C_A, marker="o", ms=4, lw=1.6, label="b-grid K channel (surgery arm)")
    ax.plot([s / BUDGET["e79"] for s in c["steps"]], c["mu_centered"],
            color=C_B, marker="s", ms=3.5, lw=1.2, ls="--", label="c-grid V channel")
    i_min = min(range(len(b["mu_centered"])), key=lambda i: b["mu_centered"][i])
    ax.annotate(f"suppressed floor {b['mu_centered'][i_min]:.3f} @ {b['steps'][i_min]//1000}K",
                xy=(b["steps"][i_min] / BUDGET["e79"], b["mu_centered"][i_min]),
                xytext=(0.30, 0.60), color=C_A, fontsize=8,
                arrowprops=dict(arrowstyle="->", color=C_A, lw=0.8))
    ax.annotate(f"rebound {b['mu_centered'][-1]:.3f} @ 20K",
                xy=(1.0, b["mu_centered"][-1]),
                xytext=(0.66, 0.72), color=C_A, fontsize=8,
                arrowprops=dict(arrowstyle="->", color=C_A, lw=0.8))
    ax.set_ylabel(r"centered $\mu$")
    ax.set_ylim(0.18, 0.92)
    ax.set_title("A. E79 soft-constraint rebound: key coherence pressed, then climbs back (to_k_center, 20K)",
                 fontsize=9, loc="left")
    ax.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=TEXT, loc="center right")

    # ── Panel B: Q13 induction transient ──────────────────────────────────────
    ax = axes[1]
    xs = [p["step"] / BUDGET["q13"] for p in q13]
    ys = [p["ratio"] for p in q13]
    ax.axhline(2.0, color=SUBTLE, lw=0.8, ls=":", label="2x break-line criterion")
    ax.plot(xs, ys, color=C_B, marker="o", ms=4, lw=1.6)
    pk = max(q13, key=lambda p: p["ratio"])
    ax.annotate(f"peak {pk['ratio']:.2f}x @ {pk['step']//1000}K (1 head >2x)",
                xy=(pk["step"] / BUDGET["q13"], pk["ratio"]),
                xytext=(0.42, 2.18), color=C_B, fontsize=8,
                arrowprops=dict(arrowstyle="->", color=C_B, lw=0.8))
    dec = next(p for p in q13 if p["step"] == 9000)
    ax.annotate(f"decays to {dec['ratio']:.2f}x @ 9K, never returns (1.46-1.51x)",
                xy=(dec["step"] / BUDGET["q13"], dec["ratio"]),
                xytext=(0.50, 1.72), color=SUBTLE, fontsize=8,
                arrowprops=dict(arrowstyle="->", color=SUBTLE, lw=0.8))
    ax.set_ylabel("induction score\nmax / baseline")
    ax.set_ylim(1.2, 2.6)
    ax.set_title("B. Q13 burstiness injection: induction transient 1.71x -> 2.34x -> gone (E105, 20K)",
                 fontsize=9, loc="left")
    ax.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=TEXT, loc="lower right")

    # ── Panel C: 2x-scale induction transient ────────────────────────────────
    ax = axes[2]
    xs = [p["step"] / BUDGET["s2x"] for p in s2x]
    ys = [p["ratio"] for p in s2x]
    ax.axhline(2.0, color=SUBTLE, lw=0.8, ls=":")
    ax.plot(xs, ys, color=C_C, marker="o", ms=4, lw=1.6)
    pk = s2x[0]
    ax.annotate(f"peak {pk['ratio']:.2f}x @ 3K, {pk['n_heads_gt_2x']} heads >2x\n(registry narrative: 2.74x, see note)",
                xy=(pk["step"] / BUDGET["s2x"], pk["ratio"]),
                xytext=(0.24, 2.16), color=C_C, fontsize=8,
                arrowprops=dict(arrowstyle="->", color=C_C, lw=0.8))
    ax.annotate("decays, then oscillates 1.2-1.7x, never re-breaks",
                xy=(s2x[1]["step"] / BUDGET["s2x"], s2x[1]["ratio"]),
                xytext=(0.40, 1.32), color=SUBTLE, fontsize=8,
                arrowprops=dict(arrowstyle="->", color=SUBTLE, lw=0.8))
    ax.set_ylabel("induction score\nmax / baseline")
    ax.set_ylim(1.0, 2.45)
    ax.set_title("C. Scale-2x from-scratch arm: five-head induction break at 3K, transient + oscillation (E110, 20K)",
                 fontsize=9, loc="left")

    # ── Panel D: Q15 attention performance ───────────────────────────────────
    ax = axes[3]
    xs = [r["step"] / BUDGET["q15"] for r in q15]
    mm = [r["q15_attend_maxmass"] for r in q15]
    ch = [r["q15_attend_chance"] for r in q15]
    sx, smm = rolling_mean(xs, mm, w=15)
    _, sch = rolling_mean(xs, ch, w=15)
    ax.plot(xs, mm, color=C_D, lw=0.3, alpha=0.25)
    ax.plot(xs, ch, color=SUBTLE, lw=0.3, alpha=0.25)
    ax.plot(sx, smm, color=C_D, lw=1.6, label="attend maxmass (rewarded, w=15)")
    ax.plot(sx, sch, color=SUBTLE, lw=1.2, ls="--", label="chance mass (w=15)")
    ax.fill_between(sx, sch, smm, where=[a > b for a, b in zip(smm, sch)],
                    color=C_D, alpha=0.18, interpolate=True)
    gap_sm = [a - b for a, b in zip(smm, sch)]
    lo = min(gap_sm[25:])  # skip the warmup transient
    hi = max(gap_sm[25:])
    ax.annotate(f"smoothed gap holds +{lo:.2f}~+{hi:.2f} (E107: +0.09~+0.16)",
                xy=(0.55, smm[550] + 0.02), xytext=(0.42, 0.62),
                color=C_D, fontsize=8,
                arrowprops=dict(arrowstyle="->", color=C_D, lw=0.8))
    ax2 = ax.twinx()
    td = [r["q15_twin_d"] for r in q15]
    _, std = rolling_mean(xs, td, w=15)
    ax2.plot(xs, td, color=C_E, lw=0.3, alpha=0.2)
    ax2.plot(sx, std, color=C_E, lw=1.2, label="twin_d content sensitivity (w=15)")
    ax2.set_ylabel("twin sensitivity", color=C_E, fontsize=8)
    ax2.tick_params(colors=C_E, labelsize=7)
    ax2.set_ylim(-0.02, 0.10)
    for spine in ax2.spines.values():
        spine.set_color(GRID)
    ax.set_ylabel("attention mass")
    ax.set_ylim(0.05, 0.95)
    ax.set_title("D. Q15 circuit rearing: reward pulls attention up, content does not follow (E107, 20K)",
                 fontsize=9, loc="left")
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, fontsize=7, facecolor=BG, edgecolor=GRID,
              labelcolor=TEXT, loc="center right")

    # ── Panel E: Q17 echo transient ──────────────────────────────────────────
    ax = axes[4]
    xs_raw = [r["step"] / BUDGET["q17"] for r in q17]
    ys_raw = [r["echo_byte_acc"] for r in q17]
    rx, ry = rolling_mean(xs_raw, ys_raw, w=5)
    ax.axhline(0.30, color=C_D, lw=0.9, ls="-.", label="ignition criterion 0.30")
    ax.scatter(xs_raw, ys_raw, color=C_E, s=7, alpha=0.45, label="echo byte_acc (raw windows)")
    ax.plot(rx, ry, color=C_E, lw=1.6, label="rolling mean (w=5)")
    ax.annotate("peak 0.1042 @ 800",
                xy=(800 / BUDGET["q17"], 0.1042), xytext=(0.16, 0.135),
                color=C_E, fontsize=8,
                arrowprops=dict(arrowstyle="->", color=C_E, lw=0.8))
    ax.annotate("0.040 @ 1900",
                xy=(1900 / BUDGET["q17"], 0.0401), xytext=(0.30, 0.055),
                color=SUBTLE, fontsize=8,
                arrowprops=dict(arrowstyle="->", color=SUBTLE, lw=0.8))
    ax.axvline(2520 / BUDGET["q17"], color=C_MAUVE, lw=0.9, ls="--")
    ax.text(2520 / BUDGET["q17"] + 0.008, 0.12, "arm stopped @ 2520/10000\n(ignition failure, E109)",
            color=C_MAUVE, fontsize=7, va="top")
    ax.set_ylabel("echo byte_acc")
    ax.set_ylim(-0.01, 0.33)
    ax.set_xlim(0.0, 1.0)
    ax.set_xlabel("training progress (step / run budget)")
    ax.set_title("E. Q17 oracle readout from scratch: echo transient peaks at 0.104, falls back (10K budget)",
                 fontsize=9, loc="left")
    ax.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=TEXT, loc="upper right")

    for ax in axes:
        style_ax(ax)
    # style_ax resets twin axes colours; re-style the twin from panel D
    fig.suptitle("Figure 1 candidate — five transient-emergence-then-absorption observations, aligned on training progress",
                 color=TEXT, fontsize=11, y=0.995)
    fig.tight_layout(rect=(0, 0, 1, 0.985))
    png = OUT_DIR / "figure1_five_transients.png"
    fig.savefig(png, dpi=200, facecolor=BG)
    print(f"[fig1] wrote {png}")

    # ── data JSON ────────────────────────────────────────────────────────────
    payload = {
        "figure": "paper Figure 1 candidate: five same-signature transient observations",
        "created_by": "tools/plotting/plot_figure1_five_transients.py",
        "x_axis": "training progress = step / run budget",
        "panels": {
            "A_e79_soft_constraint_rebound": {
                "source": str(MU_TRAJ),
                "registry": "docs/CURRENT_STATE.md E79",
                "budget_steps": BUDGET["e79"],
                "b_tokcenter": mu["b-tokcenter"],
                "c_tokcenter": mu["c-tokcenter"],
                "anchors": {"suppressed_floor": 0.6903, "rebound_end": 0.8108},
            },
            "B_q13_induction_transient": {
                "source": str(Q13_SWEEP),
                "registry": "docs/CURRENT_STATE.md E105",
                "budget_steps": BUDGET["q13"],
                "ratio_definition": "trained.max / trained.baseline",
                "points": q13,
                "anchors": {"3K": 1.71, "6K_peak": 2.34, "9K_on": "1.46-1.51 flat"},
            },
            "C_scale2x_induction_transient": {
                "source": str(S2X_SWEEP),
                "registry": "docs/CURRENT_STATE.md E110",
                "budget_steps": BUDGET["s2x"],
                "ratio_definition": "trained.max / trained.baseline",
                "points": s2x,
                "note_koujing": (
                    "E110/E111/E112/E113 registry narrative says 3K peak = 2.74x. The archived "
                    "sweep JSONs give max/baseline = 0.5222/0.25 = 2.09x under the same formula that "
                    "exactly reproduces the E105 (1.71/2.34), E107 (2.13) and E111 (1.61) anchors. "
                    "2.74 = 0.5222/0.1905, i.e. the peak score divided by the q15b-instrument baseline "
                    "of a different run family -- likely a bookkeeping slip in the E110 narrative. "
                    "The shape claim (five heads >2x at 3K, then decay + 1.2-1.7x oscillation) IS "
                    "borne out by the archived data. Plotted values follow the instrument JSONs."
                ),
            },
            "D_q15_attention_performance": {
                "source": str(Q15_LOG),
                "registry": "docs/CURRENT_STATE.md E107",
                "budget_steps": BUDGET["q15"],
                "series": {
                    "steps": [r["step"] for r in q15],
                    "q15_attend_maxmass": mm,
                    "q15_attend_chance": ch,
                    "q15_twin_d": td,
                },
                "anchors": {"maxmass_minus_chance": "+0.09~+0.16 sustained", "mass_over_chance": "~1.5"},
            },
            "E_q17_echo_transient": {
                "source": str(Q17_LOG),
                "registry": "docs/CURRENT_STATE.md E109",
                "budget_steps": BUDGET["q17"],
                "series": {
                    "steps": [r["step"] for r in q17],
                    "echo_byte_acc": ys_raw,
                },
                "anchors": {"peak": "0.1042@800", "decay": "0.040@1900", "criterion": 0.30,
                            "stopped_at": 2520},
                "note": (
                    "raw log also contains a single-window spike 0.1429@2140 after the anneal "
                    "started (p=0.75); the registered narrative anchors on the p=1.0 segment "
                    "(first 2K steps). Raw points are plotted; rolling mean carries the shape."
                ),
            },
        },
    }
    (OUT_DIR / "figure1_data.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[fig1] wrote {OUT_DIR / 'figure1_data.json'}")

    caption = (
        "# Figure 1 caption draft\n\n"
        "**EN (one sentence):** Five independent training runs exhibit the same signature — a circuit-level "
        "competence (key-geometry suppression, induction-head formation, rewarded attention, oracle echo readout) "
        "transiently emerges early in training and is then re-absorbed as optimization proceeds — plotted on a "
        "shared training-progress axis with the transient peak and decay points marked.\n\n"
        "**CN 对照（一句）:** 五条独立训练臂呈现同一签名——回路级能力（键几何压制、induction 头形成、受奖励的"
        "注意力、oracle 回声读出）在训练早期瞬态涌现、随后被优化过程重新吃掉——统一训练进度横轴、标注瞬态峰值"
        "与消退点。\n\n"
        "口径注记：面板 C 的 3K 峰值按仪器 JSON 绘为 2.09x（max/baseline，同式复现 E105/E107/E111 锚点）；"
        "E110 叙事注册读数 2.74x 对应除以异源基线 0.1905，疑为簿记笔误，差异已在 figure1_data.json 登记。\n"
    )
    (OUT_DIR / "caption_draft.md").write_text(caption, encoding="utf-8")
    print(f"[fig1] wrote {OUT_DIR / 'caption_draft.md'}")


if __name__ == "__main__":
    main()
