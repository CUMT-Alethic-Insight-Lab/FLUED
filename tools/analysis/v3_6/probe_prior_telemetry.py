"""2x 臂盲猜先验逐里程碑遥测（用户裁定优先项 2026-08-28，喂图 1 先验
遥测定稿，"先验溶剂"假说的直接遥测——盲猜先验随训练爬升 = 先验在溶解
检索需求）。

测量定义（与 E103/Q14 同族）：裸猜协议——burst 段单独成文档（无前次
出现、无上下文），末 2-4 字符（非边界字符，Q13/Q14 同规）遮蔽，逐字节
acc；直接调用 train_v36_s1._burst_prior_guess_acc（fp32 eval，尾部不在
chunk 网格上的段记 None、单列不计均值）。

段集：固定种子（20260828）从 CorpusSampler（corpus_v3，32-64B 现采，
Q13 管束同分布同验收纪律）抽 48 段，**全里程碑共享同一批**——逐里程碑
变化只来自模型，不来自段集。

模型加载口径同 probe_oracle_write_verdict.load_model：run dir 的
resolved_config.json 建模 + 逐 milestone ckpt 的 model 权重 + 硬冻结
eval；milestone ckpt 只含 model 权重（~370MB），latest.pt 含优化器态
（~1.1GB），统一 map_location="cpu" 载入后上卡（与 16GB 卡上在跑训练
共存纪律）。

产出（--out-dir，默认 outputs/prior_telemetry_2x_20260828/）：
  segments.json            段集（offset/len/tail_bytes/tail_chars + 十六进制段字节）
  step_XXXXXX.json × 7     逐里程碑：均值±95%CI + 逐段条目（None 单列）
  series.json              汇总序列（供外部绘图/引用）
  prior_telemetry_curve.png 逐里程碑均值曲线（CI 误差棒 + E103 两点参照虚线）

形态如实落盘（爬升/走平/下降/震荡都记）——这是溶剂假说的判读材料，
本探针不落判词。

Usage:
  python tools/analysis/v3_6/probe_prior_telemetry.py --device cuda
  CPU 冒烟: python tools/analysis/v3_6/probe_prior_telemetry.py --device cpu --n-segments 4 --steps step_003000.pt
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from argparse import Namespace
from pathlib import Path

# torch / 训练栈重依赖懒导入（_deps()）: --plot-only 模式（从 series.json 重绘
# PNG）只需要 matplotlib，可用无 torch 的解释器跑（本地 soulvlm 环境无
# matplotlib、py -3.14 无 torch，绘图与探针分解释器执行）。

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

torch = None
s1 = None
build_model = None


def _deps():
    global torch, s1, build_model
    if torch is None:
        import torch as _torch

        import tools.train.v3_6.train_v36_s1 as _s1
        from tools.train.v3_6.train_v36 import build_model as _bm

        torch, s1, build_model = _torch, _s1, _bm
    return torch, s1, build_model

DEFAULT_RUN = "checkpoints/v37ks_a_im_v373_scale2x_20k_ctx4096_20260826"
DEFAULT_OUT = "outputs/prior_telemetry_2x_20260828"
SEG_SEED = 20260828
N_SEGMENTS = 48
MILESTONES = [
    "step_003000.pt",
    "step_006000.pt",
    "step_009000.pt",
    "step_012000.pt",
    "step_015000.pt",
    "step_018000.pt",
    "latest.pt",
]
# E103 参照（Q12 臂跨臂两点读数，判读对照用，非判词）
E103_REFS = (0.105, 0.131)


def draw_segments(data_path: str, n_segments: int, seed: int) -> list[dict]:
    """固定种子现采段集：Q13/Q14 管束同分布同验收纪律（32-64B UTF-8
    snapped 段；末 k 字符 k∈[2,4] 每段抽、全部非边界字符、不吃掉整段；
    N=8 重抽上限沿 CorpusSampler.draw 的机械断言）。全里程碑共享。"""
    sampler = s1.CorpusSampler(data_path)
    gen = torch.Generator().manual_seed(seed)
    segments: list[dict] = []
    while len(segments) < n_segments:
        got = sampler.draw(gen)  # 8 连撞已登记段时机械断言（48 段语料尺度下不会发生）
        if got is None:
            continue
        cand, key = got
        k = int(
            torch.randint(
                s1._BURST_TAIL_MIN_CHARS, s1._BURST_TAIL_MAX_CHARS + 1, (1,), generator=gen
            )
        )
        text = cand.decode("utf-8")  # sampler guarantees decodable
        if len(text) < k + 2:  # 遮蔽尾不能吃掉整段
            continue
        tail = text[-k:]
        if any(ch in s1._BOUNDARY_CHARS for ch in tail):
            continue
        tail_b = sum(len(ch.encode("utf-8")) for ch in tail)
        segments.append(
            {
                "seg_offset": key[0],
                "seg_len": key[1],
                "seg_bytes_hex": cand.hex(),
                "tail_chars": k,
                "tail_bytes": tail_b,
                "text": text,
            }
        )
    return segments


def load_model_at(run_dir: Path, ckpt_name: str, device: torch.device):
    """probe_oracle_write_verdict.load_model 同口径，唯 ckpt 文件名参数化；
    payload 落 CPU（latest.pt 含优化器态 ~1.1GB，共存纪律）再上卡。"""
    cfg = json.loads((run_dir / "resolved_config.json").read_text(encoding="utf-8"))
    cfg["data_manifest"] = ""
    if device.type != "cuda":
        cfg["kda_impl"] = "torch"  # fla kernels are GPU-only
    ns = Namespace(**cfg)
    if getattr(ns, "backbone_mode", "") != "slm":
        raise ValueError(f"{run_dir.name}: backbone_mode={ns.backbone_mode!r} != 'slm'")
    model = build_model(ns)
    payload = torch.load(run_dir / ckpt_name, map_location="cpu", weights_only=False)
    model.load_state_dict(payload["model"], strict=True)
    model = model.to(device)
    for p in model.parameters():  # hard-freeze
        p.requires_grad_(False)
    model.eval()
    return model, ns, int(payload.get("step", 0))


def _mean_ci(vals: list[float]) -> tuple[float, float, float]:
    n = len(vals)
    if not n:
        return 0.0, 0.0, 0.0
    mean = sum(vals) / n
    sd = (sum((v - mean) ** 2 for v in vals) / (n - 1)) ** 0.5 if n > 1 else 0.0
    return mean, sd, 1.96 * sd / (n**0.5)


def probe_milestone(model, segments: list[dict]) -> dict:
    """裸猜协议逐段测量（直接调 s1._burst_prior_guess_acc）：段单独成
    文档、末 tail_bytes 遮蔽、逐字节 acc；None（尾部 off-grid）单列。"""
    items = []
    for i, ent in enumerate(segments):
        seg = bytes.fromhex(ent["seg_bytes_hex"])
        acc = s1._burst_prior_guess_acc(model, seg, ent["tail_bytes"])
        items.append(
            {
                "idx": i,
                "seg_offset": ent["seg_offset"],
                "seg_len": ent["seg_len"],
                "tail_bytes": ent["tail_bytes"],
                "tail_chars": ent["tail_chars"],
                "acc": None if acc is None else round(acc, 6),
            }
        )
    vals = [it["acc"] for it in items if it["acc"] is not None]
    mean, sd, ci = _mean_ci(vals)
    return {
        "n_segments": len(items),
        "n_valid": len(vals),
        "n_offgrid": len(items) - len(vals),
        "acc_mean": round(mean, 6),
        "acc_sd": round(sd, 6),
        "ci95": round(ci, 6),
        "items": items,
    }


def plot_series(series: list[dict], out_png: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    xs = [r["step"] for r in series]
    ys = [r["acc_mean"] for r in series]
    es = [r["ci95"] for r in series]
    fig, ax = plt.subplots(figsize=(8, 4.8), dpi=140)
    ax.errorbar(xs, ys, yerr=es, marker="o", capsize=3, linewidth=1.6,
                color="#1f5fa8", ecolor="#7aa6d0", label="2x arm prior acc (mean ± 95% CI)")
    for ref in E103_REFS:
        ax.axhline(ref, color="#b0653a", linestyle="--", linewidth=1.0, alpha=0.8)
        ax.text(xs[-1], ref, f" E103 ref {ref:.3f}", va="bottom" if ref == max(E103_REFS) else "top",
                fontsize=8, color="#b0653a")
    for x, y in zip(xs, ys):
        ax.annotate(f"{y:.3f}", (x, y), textcoords="offset points", xytext=(0, 7),
                    ha="center", fontsize=7.5, color="#1f5fa8")
    ax.set_xlabel("training step")
    ax.set_ylabel("bare-guess prior acc (masked tail, per-byte)")
    ax.set_title("2x arm prior telemetry — blind-guess prior vs milestone (n=48 shared segments)")
    ax.grid(alpha=0.3)
    ax.legend(loc="best", fontsize=8)
    fig.tight_layout()
    fig.savefig(out_png)
    plt.close(fig)


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    p = argparse.ArgumentParser()
    p.add_argument("--run-dir", default=DEFAULT_RUN)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--n-segments", type=int, default=N_SEGMENTS)
    p.add_argument("--seed", type=int, default=SEG_SEED)
    p.add_argument("--steps", nargs="*", default=MILESTONES)
    p.add_argument("--out-dir", default=DEFAULT_OUT)
    p.add_argument(
        "--plot-only",
        action="store_true",
        help="只从 out-dir/series.json 重绘 PNG（无需 torch，供无 torch 解释器用）",
    )
    args = p.parse_args()
    out_dir = Path(args.out_dir)

    if args.plot_only:
        payload = json.loads((out_dir / "series.json").read_text(encoding="utf-8"))
        plot_series(payload["series"], out_dir / "prior_telemetry_curve.png")
        print(f"[prior-telemetry] re-plotted -> {out_dir / 'prior_telemetry_curve.png'}", flush=True)
        return

    _deps()
    device = torch.device(
        "cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu"
    )
    run_dir = Path(args.run_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    # 段集：固定种子现采，全里程碑共享（从 run dir 的 resolved_config 读 data_path）
    cfg = json.loads((run_dir / "resolved_config.json").read_text(encoding="utf-8"))
    segments = draw_segments(cfg["data_path"], args.n_segments, args.seed)
    (out_dir / "segments.json").write_text(
        json.dumps(
            {"seed": args.seed, "data_path": cfg["data_path"], "n": len(segments), "segments": segments},
            ensure_ascii=False, indent=2,
        ),
        encoding="utf-8",
    )
    print(f"[prior-telemetry] segments: {len(segments)} drawn (seed {args.seed}) ({time.time() - t0:.0f}s)", flush=True)

    series = []
    for ckpt_name in args.steps:
        model, ns, step = load_model_at(run_dir, ckpt_name, device)
        row = probe_milestone(model, segments)
        row["checkpoint"] = ckpt_name
        row["step"] = step
        series.append(row)
        (out_dir / f"step_{step:06d}.json").write_text(
            json.dumps(row, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(
            f"[prior-telemetry] {ckpt_name} (step {step}): acc_mean={row['acc_mean']:.4f} "
            f"±{row['ci95']:.4f} (n_valid={row['n_valid']}, offgrid={row['n_offgrid']}) ({time.time() - t0:.0f}s)",
            flush=True,
        )
        del model
        if device.type == "cuda":
            torch.cuda.empty_cache()

    payload = {
        "probe": "2x 臂盲猜先验逐里程碑遥测（E103/Q14 同族裸猜协议）",
        "run_dir": str(run_dir),
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "n_segments": len(segments),
        "seed": args.seed,
        "e103_refs": E103_REFS,
        "series": [{k: r[k] for k in ("checkpoint", "step", "acc_mean", "acc_sd", "ci95", "n_valid", "n_offgrid")} for r in series],
    }
    (out_dir / "series.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        plot_series(series, out_dir / "prior_telemetry_curve.png")
    except ModuleNotFoundError:
        print(
            "[prior-telemetry] 本环境无 matplotlib，PNG 未出——用带 matplotlib 的解释器重绘： "
            f"py -3.14 -X utf8 tools/analysis/v3_6/probe_prior_telemetry.py --plot-only --out-dir {out_dir}",
            flush=True,
        )
    print(f"[prior-telemetry] done -> {out_dir} ({time.time() - t0:.0f}s)", flush=True)


if __name__ == "__main__":
    main()
