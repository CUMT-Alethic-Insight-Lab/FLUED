"""fork 3 前置非线性段尾探针（用户裁定 2026-08-20，probe-only 分钟级）。

段尾丢失已定位到 summarizer 压缩一级（E88/段尾定位包：memory 行头尾比
5.15× 在进状态机之前已成形），但 ridge 是线性下界——"丢"的严格含义只是
"线性不可解码"。本探针回答 fork 3 立项书第一段怎么写：

  在 memory 行（summarizer 出口、未进状态机，c 格 v37_c_is V 通道）上训一个
  小型非线性解码器重构逐 slot 字节，与同协议线性探针（0 隐藏层 softmax）
  同窗同 split 对照：
    段尾 nonlinear ≫ linear  → 信息在 memory 行里但线性形态拿不到
                               → fork 3 靶子 = 读出接口形态；
    段尾 nonlinear ≈ linear（都贴 garbage）→ 信息在 memory 行真缺席
                               → fork 3 靶子 = summarizer 编码目标/容量。

协议：checkpoint 硬冻结、只收 memory 行 + 逐 slot 干净字节目标（make_targets
同口径）；test split = eval 流前 16 窗（canonical 终评同窗，与 ridge 剖面
可对照），train split = 其后 48 窗；探针特征用 train split 均值/方差标准化。
garbage 纪律与段尾定位包同：per-window chunk 轴排列（种子 20260819，窗序
一致）打碎行↔内容配对。线性臂 = 同拓扑 0 隐藏层 softmax，与 MLP 臂同
优化器同步数同 batch——两臂唯一差别是隐藏层。

判词阈值（赛前冻结）：tail=slot16-31 均值 real−garbage Δacc；
  nonlinear_tail > linear_tail×2 且差值 > 0.05 → "信息在但线性拿不到"；
  nonlinear_tail − linear_tail < 0.02 且 nonlinear_tail < 0.05 → "信息真缺席"；
  中间 → 人工读表。

Usage:
  python tools/analysis/v3_6/probe_tail_nonlinear.py --device cuda
  CPU 冒烟: python tools/analysis/v3_6/probe_tail_nonlinear.py --device cpu --train-windows 4 --test-windows 2 --steps 50
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

import torch
import torch.nn.functional as F
from torch import nn

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from flued.data import MASK_ID  # noqa: E402
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402
from tools.analysis.v3_6.probe_oracle_write_verdict import (  # noqa: E402
    _front_end,
    build_eval_windows,
    build_masks,
    load_model,
)

C_RUN = "checkpoints/v37_c_is_v371_20k_ctx4096_20260817"
OUT_DIR = "outputs/audit_measurements_20260819"
PERM_SEED = 20260819  # same convention as the tail-loss localization package
N_CLS = 258  # PAD-offset byte ids (PAD=0, byte b -> b+1) + MASK(257, unused)
PROBE_SEED = 20260820


# ---------------------------------------------------------------------------
# row collection (c-grid V channel: summarizer memory rows, pre-state-machine)
# ---------------------------------------------------------------------------


@torch.no_grad()
def collect_rows(model, windows, masks, device):
    """Per real chunk: memory row (d_mem) + per-slot clean byte targets, plus
    the garbage pairing (per-window chunk-axis permutation, one randperm per
    window drawn in window order from PERM_SEED — same discipline as the
    localization package). Returns rows + per-window chunk counts (single
    pass)."""
    gen = torch.Generator().manual_seed(PERM_SEED)
    xs, xs_g, ys, yv, counts = [], [], [], [], []
    for clean, bm in zip(windows, masks):
        source = clean.masked_fill(bm.to(clean.device), MASK_ID).to(device)
        chunks, memory, _index = _front_end(model, source)
        n = int(chunks.chunk_mask[0].sum())
        counts.append(n)
        bt, bs, _m = s1.make_targets(
            clean.to(device), torch.zeros_like(bm).to(device),
            chunks.chunk_ids, chunks.offsets, model.config.max_chunks, model.config.max_span,
        )
        perm = torch.randperm(n, generator=gen).to(device)
        xs.append(memory[0, :n].float().cpu())
        xs_g.append(memory[0, :n].float()[perm].cpu())
        ys.append(bt[0, :n].cpu())
        yv.append(bs[0, :n].cpu())
    return torch.cat(xs), torch.cat(xs_g), torch.cat(ys), torch.cat(yv), counts


# ---------------------------------------------------------------------------
# probes: linear (0 hidden layers) vs MLP (2 hidden layers), same everything else
# ---------------------------------------------------------------------------


class _Probe(nn.Module):
    def __init__(self, d_in: int, n_slots: int, hidden_layers: int = 0, hidden: int = 1024):
        super().__init__()
        self.n_slots = n_slots
        layers: list[nn.Module] = []
        d = d_in
        for _ in range(hidden_layers):
            layers += [nn.Linear(d, hidden), nn.SiLU()]
            d = hidden
        layers.append(nn.Linear(d, n_slots * N_CLS))
        self.net = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x).view(x.size(0), self.n_slots, N_CLS)


def train_probe(x_tr, y_tr, v_tr, x_te, y_te, v_te, hidden_layers, device, steps, batch, lr, seed):
    torch.manual_seed(seed)
    n_slots = y_tr.size(1)
    probe = _Probe(x_tr.size(1), n_slots, hidden_layers).to(device)
    opt = torch.optim.AdamW(probe.parameters(), lr=lr, weight_decay=0.01)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=steps)
    n = x_tr.size(0)
    gen = torch.Generator().manual_seed(seed + 1)
    for step in range(steps):
        idx = torch.randint(0, n, (batch,), generator=gen)
        xb = x_tr[idx].to(device)
        logits = probe(xb)
        loss = F.cross_entropy(
            logits.reshape(-1, N_CLS),
            y_tr[idx].to(device).reshape(-1).clamp(min=0),
            reduction="none", ignore_index=0,
        )
        m = v_tr[idx].to(device).reshape(-1)
        loss = (loss * m).sum() / m.sum().clamp(min=1)
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
    probe.eval()
    with torch.no_grad():
        acc = []
        for i0 in range(0, x_te.size(0), 4096):
            logits = probe(x_te[i0:i0 + 4096].to(device))
            pred = logits.argmax(dim=-1).cpu()
            tgt = y_te[i0:i0 + 4096]
            val = v_te[i0:i0 + 4096]
            hit = (pred == tgt) & val
            acc.append((hit.sum(dim=0), val.sum(dim=0)))
        hits = torch.stack([a[0] for a in acc]).sum(dim=0)
        vals = torch.stack([a[1] for a in acc]).sum(dim=0)
    return {str(s): round(float(hits[s]) / max(float(vals[s]), 1.0), 4) for s in range(n_slots)}


def _shape(diff: dict[str, float], head=(0, 4), tail=(16, 32)):
    def mean(lo, hi):
        vals = [diff[str(s)] for s in range(lo, hi) if str(s) in diff]
        return round(sum(vals) / len(vals), 4) if vals else None
    h, t = mean(*head), mean(*tail)
    return {
        "head_mean": h, "tail_mean": t,
        "head_over_tail": round(h / t, 3) if h is not None and t and t > 1e-9 else None,
    }


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")  # GBK consoles cannot encode U+2212 (real−garbage)
    p = argparse.ArgumentParser()
    p.add_argument("--run-dir", default=C_RUN)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--test-windows", type=int, default=16, help="canonical eval stream head (anchor-comparable)")
    p.add_argument("--train-windows", type=int, default=48, help="windows AFTER the test split")
    p.add_argument("--steps", type=int, default=3000)
    p.add_argument("--batch", type=int, default=512)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--out-dir", default=OUT_DIR)
    args = p.parse_args()
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    model, ns, step = load_model(Path(args.run_dir), device)
    windows = build_eval_windows(ns, args.test_windows + args.train_windows)
    masks = build_masks(windows, ns)
    print(f"[nlp] model={Path(args.run_dir).name} step={step} device={device.type} "
          f"windows={len(windows)} ({time.time() - t0:.0f}s)", flush=True)

    xs, xs_g, ys, yv, counts = collect_rows(model, windows, masks, device)
    print(f"[nlp] rows={xs.size(0)} ({time.time() - t0:.0f}s); probes training...", flush=True)

    # test = FIRST test-windows (canonical eval head); train = the rest
    n_test = sum(counts[: args.test_windows])
    sl = {
        "tr": slice(n_test, None),
        "te": slice(0, n_test),
    }
    # standardize features on the train split (no label leakage)
    mu = xs[sl["tr"]].mean(dim=0, keepdim=True)
    sd = xs[sl["tr"]].std(dim=0, keepdim=True).clamp_min(1e-6)
    xs_n = (xs - mu) / sd
    xs_gn = (xs_g - mu) / sd

    results = {}
    for name, (xtr, xte) in {
        "linear_real": (xs_n[sl["tr"]], xs_n[sl["te"]]),
        "mlp_real": (xs_n[sl["tr"]], xs_n[sl["te"]]),
        "linear_garbage": (xs_gn[sl["tr"]], xs_gn[sl["te"]]),
        "mlp_garbage": (xs_gn[sl["tr"]], xs_gn[sl["te"]]),
    }.items():
        hl = 0 if name.startswith("linear") else 2
        results[name] = train_probe(
            xtr, ys[sl["tr"]], yv[sl["tr"]], xte, ys[sl["te"]], yv[sl["te"]],
            hl, device, args.steps, args.batch, args.lr, PROBE_SEED,
        )
        print(f"[nlp] {name} done ({time.time() - t0:.0f}s)", flush=True)

    diff = {
        "linear": {s: round(results["linear_real"][s] - results["linear_garbage"][s], 4) for s in results["linear_real"]},
        "mlp": {s: round(results["mlp_real"][s] - results["mlp_garbage"][s], 4) for s in results["mlp_real"]},
    }
    shapes = {"linear": _shape(diff["linear"]), "mlp": _shape(diff["mlp"])}

    lt, mt = shapes["linear"]["tail_mean"], shapes["mlp"]["tail_mean"]
    if mt is not None and lt is not None and mt > lt * 2 and (mt - lt) > 0.05:
        verdict = ("信息在但线性拿不到（nonlinear_tail 显著超 linear_tail）——fork 3 靶子 = 读出接口形态"
                   "（编码目标/容量无罪的强证据）。")
    elif mt is not None and lt is not None and (mt - lt) < 0.02 and mt < 0.05:
        verdict = ("信息真缺席（nonlinear 段尾同样贴 garbage）——fork 3 靶子 = summarizer 编码目标/容量"
                   "（段尾为什么没进 memory 行）。")
    else:
        verdict = "中间形态——人工读表定 fork 3 靶子。"

    report = {
        "probe": "fork 3 前置非线性段尾探针（memory 行，c 格 v37_c_is V 通道）",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "checkpoint": {"run": Path(args.run_dir).name, "step": step},
        "params": {
            "test_windows": args.test_windows, "train_windows": args.train_windows,
            "steps": args.steps, "batch": args.batch, "lr": args.lr,
            "perm_seed": PERM_SEED, "probe_seed": PROBE_SEED, "eval_mask_seed": ns.eval_mask_seed,
        },
        "protocol": "test=eval 流前 16 窗（canonical 同窗）；train=其后 48 窗；特征 train-split 标准化；"
        "linear=0 隐藏层 softmax 与 MLP(512-1024-1024) 同优化器同步数同 batch；"
        "garbage=per-window chunk 轴排列（种子 20260819）；指标=逐 slot acc real−garbage",
        "counts": {"test_rows": n_test, "train_rows": int(xs.size(0)) - n_test},
        "acc": results,
        "real_minus_garbage": diff,
        "shapes": shapes,
        "verdict": verdict,
        "timing_sec": round(time.time() - t0, 1),
    }
    out_path = out_dir / "probe_tail_nonlinear.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "fork 3 前置非线性段尾探针（memory 行=summarizer 出口，c 格 v37_c_is，未进状态机）",
        f"日期 {report['created']}  设备 {device.type}  test={args.test_windows}窗(canonical头) train={args.train_windows}窗",
        "",
        "逐 slot real−garbage Δacc（test split）：slot | linear | mlp",
    ]
    for s in range(min(32, len(diff["linear"]))):
        k = str(s)
        lines.append(f"  {s:>4d} | {diff['linear'].get(k, float('nan')):+.4f} | {diff['mlp'].get(k, float('nan')):+.4f}")
    lines += [
        "",
        f"形态：linear head {shapes['linear']['head_mean']} tail {shapes['linear']['tail_mean']} "
        f"比 {shapes['linear']['head_over_tail']}",
        f"      mlp    head {shapes['mlp']['head_mean']} tail {shapes['mlp']['tail_mean']} "
        f"比 {shapes['mlp']['head_over_tail']}",
        "",
        "判词阈值（赛前冻结）：nonlinear_tail > linear×2 且差 >0.05 → 读出接口靶；",
        "nonlinear−linear <0.02 且 nonlinear_tail<0.05 → summarizer 编码目标/容量靶；中间→人工。",
        f"判词：{verdict}",
        "",
        f"完整数据: {out_path}",
    ]
    summary_path = out_dir / "SUMMARY_tail_nonlinear.txt"
    summary_path.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
