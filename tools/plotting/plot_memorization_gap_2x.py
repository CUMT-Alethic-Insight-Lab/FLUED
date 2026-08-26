"""
plot_memorization_gap_2x.py — Memorization-gap curve for the scale-2x arm,
overlaid with its induction trajectory on a shared training-progress axis.

gap(step) = eval_completion_loss (held-out, eval-only pass on the milestone
checkpoint) minus same-window train completion_loss (train_log rows within
+/-60 steps of the milestone).

Sources:
  eval : outputs/memorization_gap_2x_20260827/eval_step_*.json
         (train_v36_s1.py --eval-only on checkpoints/v37ks_a_im_v373_scale2x_20k_ctx4096_20260826;
          20K point reproduces the run's own summary.json eval_completion_loss 3.0678278 exactly)
  train: checkpoints/v37ks_a_im_v373_scale2x_20k_ctx4096_20260826/train_log.jsonl
  induction: outputs/induction_scale2x_sweep/m*/induction_score.json (+latest=20K)

Usage: py -3.14 tools/plotting/plot_memorization_gap_2x.py
Outputs: outputs/memorization_gap_2x_20260827/memorization_gap_2x.png
         outputs/memorization_gap_2x_20260827/memorization_gap_data.json
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
C_GAP = "#f38ba8"     # red   — memorization gap
C_IND = "#fab387"     # peach — induction ratio
C_TRAIN = "#89dceb"   # cyan  — train loss
C_EVAL = "#cba6f7"    # mauve — eval loss

OUT_DIR = Path("outputs/memorization_gap_2x_20260827")
RUN_DIR = Path("checkpoints/v37ks_a_im_v373_scale2x_20k_ctx4096_20260826")
SWEEP_DIR = Path("outputs/induction_scale2x_sweep")
BUDGET = 20000
MILESTONES = [3000, 6000, 9000, 12000, 15000, 18000, 20000]
TRAIN_WINDOW = 60  # +/- steps around the milestone for the same-window train loss


def load_eval(step):
    f = OUT_DIR / f"eval_step_{step:06d}.json"
    txt = f.read_text(encoding="utf-8")
    return json.loads(txt[txt.find("{"):])


def load_train_completion():
    rows = [json.loads(l) for l in open(RUN_DIR / "train_log.jsonl", encoding="utf-8")]
    out = {}
    for m in MILESTONES:
        near = [r["completion_loss"] for r in rows if abs(r["step"] - m) <= TRAIN_WINDOW]
        out[m] = sum(near) / len(near)
    return out


def load_induction():
    pts = []
    for sub in sorted(SWEEP_DIR.iterdir()):
        f = sub / "induction_score.json"
        if not f.exists():
            continue
        d = json.loads(f.read_text(encoding="utf-8"))
        t = d["summary"]["trained"]
        step = 20000 if sub.name == "latest" else int(sub.name.lstrip("m"))
        pts.append({"step": step, "ratio": t["max"] / t["baseline"],
                    "n_heads_gt_2x": t["n_heads_gt_2x"]})
    pts.sort(key=lambda p: p["step"])
    return pts


def main():
    train_cl = load_train_completion()
    induction = load_induction()

    points = []
    for m in MILESTONES:
        ev = load_eval(m)
        points.append({
            "step": m,
            "progress": m / BUDGET,
            "eval_completion_loss": ev["eval_completion_loss"],
            "train_completion_loss_window": train_cl[m],
            "gap": ev["eval_completion_loss"] - train_cl[m],
            "eval_direct_loss": ev["eval_direct_loss"],
        })

    # anchor self-check: 20K eval must reproduce the run's own summary.json
    summary = json.loads((RUN_DIR / "summary.json").read_text(encoding="utf-8"))
    anchor_ok = abs(points[-1]["eval_completion_loss"] - summary["eval_completion_loss"]) < 1e-6
    print(f"[memgap] 20K anchor check vs run summary.json: "
          f"{points[-1]['eval_completion_loss']:.7f} vs {summary['eval_completion_loss']:.7f} "
          f"-> {'OK' if anchor_ok else 'MISMATCH'}")

    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    xs = [p["progress"] for p in points]
    gaps = [p["gap"] for p in points]
    ax.bar(xs, gaps, width=0.045, color=C_GAP, alpha=0.35)
    ax.plot(xs, gaps, color=C_GAP, marker="o", ms=5, lw=1.8,
            label="memorization gap = eval - train completion_loss")
    for p in points:
        ax.annotate(f"{p['gap']:+.3f}", xy=(p["progress"], p["gap"]),
                    xytext=(0, 7), textcoords="offset points", ha="center",
                    color=C_GAP, fontsize=7.5)
    ax.set_ylabel("completion-loss gap (eval - train)", color=C_GAP)
    ax.tick_params(axis="y", colors=C_GAP, labelsize=8)
    ax.set_ylim(0.0, max(gaps) * 1.35)

    ax2 = ax.twinx()
    ix = [p["step"] / BUDGET for p in induction]
    iy = [p["ratio"] for p in induction]
    ax2.plot(ix, iy, color=C_IND, marker="s", ms=5, lw=1.6,
             label="induction score max/baseline")
    ax2.axhline(2.0, color=SUBTLE, lw=0.8, ls=":")
    ax2.text(0.99, 2.02, "2x break-line", color=SUBTLE, fontsize=7,
             ha="right", va="bottom")
    pk = induction[0]
    ax2.annotate(f"induction peak {pk['ratio']:.2f}x @ 3K ({pk['n_heads_gt_2x']} heads >2x)",
                 xy=(pk["step"] / BUDGET, pk["ratio"]), xytext=(0.24, 2.12),
                 color=C_IND, fontsize=8,
                 arrowprops=dict(arrowstyle="->", color=C_IND, lw=0.8))
    ax2.annotate("decay @ 6K",
                 xy=(induction[1]["step"] / BUDGET, induction[1]["ratio"]),
                 xytext=(0.34, 1.45), color=SUBTLE, fontsize=8,
                 arrowprops=dict(arrowstyle="->", color=SUBTLE, lw=0.8))
    ax2.set_ylabel("induction score (max / baseline)", color=C_IND)
    ax2.tick_params(axis="y", colors=C_IND, labelsize=8)
    ax2.set_ylim(1.0, 2.35)
    for spine in ax2.spines.values():
        spine.set_color(GRID)

    ax.set_xlabel("training progress (step / 20000)", color=TEXT)
    ax.set_xlim(0.0, 1.05)
    ax.grid(color=GRID, linewidth=0.6, alpha=0.8)
    ax.tick_params(axis="x", colors=TEXT, labelsize=8)
    for spine in ax.spines.values():
        spine.set_color(GRID)
    ax.set_title("Scale-2x arm: memorization gap vs induction transient (E110, 20K@4096B)",
                 color=TEXT, fontsize=10, loc="left")
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, fontsize=8, facecolor=BG, edgecolor=GRID,
              labelcolor=TEXT, loc="upper center")
    fig.tight_layout()
    png = OUT_DIR / "memorization_gap_2x.png"
    fig.savefig(png, dpi=200, facecolor=BG)
    print(f"[memgap] wrote {png}")

    payload = {
        "figure": "memorization gap (held-out eval minus same-window train completion loss) "
                  "vs induction trajectory, scale-2x arm",
        "created_by": "tools/plotting/plot_memorization_gap_2x.py",
        "run": str(RUN_DIR),
        "budget_steps": BUDGET,
        "train_window": f"+/-{TRAIN_WINDOW} steps",
        "anchor_check_20k_vs_run_summary": {
            "eval_completion_loss": points[-1]["eval_completion_loss"],
            "run_summary_eval_completion_loss": summary["eval_completion_loss"],
            "match": anchor_ok,
        },
        "points": points,
        "induction": induction,
    }
    (OUT_DIR / "memorization_gap_data.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[memgap] wrote {OUT_DIR / 'memorization_gap_data.json'}")


if __name__ == "__main__":
    main()
