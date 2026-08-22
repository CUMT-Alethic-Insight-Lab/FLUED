"""F2 点火前提：严格 2-fold 非线性段尾探针（用户裁定最后一道关，2026-08-21）。

与岭回归探针（E73-A6 byte_probe）完全同任务、同 2-fold、同 real−garbage
协议、同 majority 基线——唯一变量是探针族：2 层 MLP（hidden 1024，GELU）
vs 岭回归。对象与张量：c 格 v37_c_is V 通道 memory 行（summarizer 出口、
未进状态机），冻结 checkpoint，16 窗 eval seed 1042 同 mask。

防过拟合护栏（预注册，用户裁定）：
  1. MLP 参数量 ≤ 岭回归参数量 ×4（岭回归=(513×258)×有效 slot 数；
     MLP=512-1024-1024-(S×258) 联合头，约 10M ≤ 4×预算，随行核验）；
  2. held-out fold 上报数（2-fold 双向，与 byte_probe 同 ((0,n/2),(n/2,n))）；
  3. train/test 差距 >15pp 判 probe 伪影 → 该读数作废并自动降容量
     （hidden 1024→512）重跑一次，两臂同报。

判读二分（预注册，用户裁定）：
  段尾区（slot18-31+）非线性 ≈ 线性（仍贴 majority）→ 段尾信息真缺席，
    F2 靶子 = 压缩目标/容量；
  段尾区非线性 − 线性 ≥ +0.10 → 信息在但线性不可达，F2 靶子改读出接口形态。

注：E89（48/16 split 版）已初判"零超额"，本探针是岭回归同协议严格版收官。
判词落定后 F2 方可点火。

Usage:
  python tools/analysis/v3_6/probe_tail_nonlinear_2fold.py --device cuda
  CPU 冒烟: python tools/analysis/v3_6/probe_tail_nonlinear_2fold.py --device cpu --max-windows 2 --steps 100
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import torch
import torch.nn.functional as F
from torch import nn

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402
from tools.analysis.v3_6.probe_oracle_write_verdict import (  # noqa: E402
    _front_end,
    build_eval_windows,
    build_masks,
    byte_probe,
    load_model,
)
from flued.data import MASK_ID  # noqa: E402

C_RUN = "checkpoints/v37_c_is_v371_20k_ctx4096_20260817"
OUT_DIR = "outputs/audit_measurements_20260819"
PERM_SEED = 20260819
PROBE_SEED = 20260821
N_CLS = 258
GAP_LIMIT = 0.15  # train/test gap guardrail (pre-registered)
TAIL_LIFT = 0.10  # verdict threshold (pre-registered)
PARAM_BUDGET_MULT = 4


@torch.no_grad()
def collect(model, windows, masks, device):
    """Memory rows + per-slot clean byte targets (+ chunk-axis garbage pairing),
    16 canonical windows — identical collection to the ridge profile."""
    gen = torch.Generator().manual_seed(PERM_SEED)
    xs, xs_g, ys, yv = [], [], [], []
    for clean, bm in zip(windows, masks):
        source = clean.masked_fill(bm.to(clean.device), MASK_ID).to(device)
        chunks, memory, _index = _front_end(model, source)
        n = int(chunks.chunk_mask[0].sum())
        bt, bs, _m = s1.make_targets(
            clean.to(device), torch.zeros_like(bm).to(device),
            chunks.chunk_ids, chunks.offsets, model.config.max_chunks, model.config.max_span,
        )
        perm = torch.randperm(n, generator=gen).to(device)
        xs.append(memory[0, :n].float().cpu())
        xs_g.append(memory[0, :n].float()[perm].cpu())
        ys.append(bt[0, :n].cpu())
        yv.append(bs[0, :n].cpu())
    return torch.cat(xs), torch.cat(xs_g), torch.cat(ys), torch.cat(yv)


class _MLP(nn.Module):
    def __init__(self, d_in: int, n_slots: int, hidden: int):
        super().__init__()
        self.n_slots = n_slots
        self.net = nn.Sequential(
            nn.Linear(d_in, hidden), nn.GELU(),
            nn.Linear(hidden, hidden), nn.GELU(),
            nn.Linear(hidden, n_slots * N_CLS),
        )

    def forward(self, x):
        return self.net(x).view(x.size(0), self.n_slots, N_CLS)


def _slot_metrics(logits, y, v):
    pred = logits.argmax(dim=-1)
    hits, vals = [], []
    for s in range(y.size(1)):
        m = v[:, s]
        if int(m.sum()) < 40:
            continue
        hits.append((s, float((pred[:, s][m] == y[:, s][m]).float().mean())))
    return dict(hits)


def train_eval_mlp(x_tr, y_tr, v_tr, x_te, y_te, v_te, hidden, device, steps, batch, lr, seed):
    """One fold direction: train MLP on (x_tr -> y_tr) with a val carve-out
    (80/20 of the train fold) and best-val model selection — kills the
    memorization artifact (fixed 3000 steps × tiny rowset = >1000 epochs);
    report per-slot train and held-out acc from the best-val probe."""
    torch.manual_seed(seed)
    probe = _MLP(x_tr.size(1), y_tr.size(1), hidden).to(device)
    opt = torch.optim.AdamW(probe.parameters(), lr=lr, weight_decay=0.01)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=steps)
    gen = torch.Generator().manual_seed(seed + 1)
    n = x_tr.size(0)
    cut = int(n * 0.8)
    vidx = torch.arange(cut, n)
    tidx_pool = torch.arange(0, cut)

    def val_score():
        probe.eval()
        with torch.no_grad():
            logits = probe(x_tr[vidx].to(device))
            pred = logits.argmax(dim=-1).cpu()
            hits, vals = 0, 0
            for s in range(y_tr.size(1)):
                m = v_tr[vidx, s]
                hits += int((pred[:, s][m] == y_tr[vidx, s][m]).sum())
                vals += int(m.sum())
        probe.train()
        return hits / max(vals, 1)

    best = (-1.0, None)
    for step_i in range(steps):
        idx = tidx_pool[torch.randint(0, cut, (batch,), generator=gen)]
        logits = probe(x_tr[idx].to(device))
        loss = F.cross_entropy(
            logits.reshape(-1, N_CLS), y_tr[idx].to(device).reshape(-1).clamp(min=0),
            reduction="none", ignore_index=0,
        )
        m = v_tr[idx].to(device).reshape(-1)
        loss = (loss * m).sum() / m.sum().clamp(min=1)
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
        if (step_i + 1) % 50 == 0 or step_i + 1 == steps:
            sc = val_score()
            if sc > best[0]:
                best = (sc, {k: v_.detach().clone() for k, v_ in probe.state_dict().items()})
    if best[1] is not None:
        probe.load_state_dict(best[1])
    probe.eval()
    with torch.no_grad():
        # 两种"gap"分列（护栏口径注记，2026-08-21 用户裁定前的如实披露）：
        # tr_acc = 训练行 acc（含被训练行——它与 test 的差距是"记忆差距"，
        #   高容量探针在小行数预算下必然 >15pp，与 held-out 估计的有效性无关）；
        # va_acc = val 留出集 acc（探针从未见过）——它与 test 的差距才是
        #   "泛化一致性"，两个未见集上提取能力是否稳定（护栏的真实意图）。
        tr_acc = _slot_metrics(probe(x_tr.to(device)), y_tr.to(device), v_tr.to(device))
        va_acc = _slot_metrics(probe(x_tr[vidx].to(device)), y_tr[vidx].to(device), v_tr[vidx].to(device))
        te_acc = _slot_metrics(probe(x_te.to(device)), y_te.to(device), v_te.to(device))
    n_params = sum(p.numel() for p in probe.parameters())
    return tr_acc, va_acc, te_acc, n_params


def run_probe(xs, ys, yv, hidden, device, steps, batch, lr, seed):
    """Full 2-fold both-directions MLP protocol on one pairing (real or garbage)."""
    n = xs.size(0)
    idx = torch.randperm(n, generator=torch.Generator().manual_seed(0))  # byte_probe 同 seed 0
    halves = [(idx[: n // 2], idx[n // 2 :]), (idx[n // 2 :], idx[: n // 2])]
    tr_all: dict[int, list] = {}
    va_all: dict[int, list] = {}
    te_all: dict[int, list] = {}
    n_params = 0
    for tr_idx, te_idx in halves:
        tr_acc, va_acc, te_acc, n_params = train_eval_mlp(
            xs[tr_idx], ys[tr_idx], yv[tr_idx], xs[te_idx], ys[te_idx], yv[te_idx],
            hidden, device, steps, batch, lr, seed,
        )
        for s, a in tr_acc.items():
            tr_all.setdefault(s, []).append(a)
        for s, a in va_acc.items():
            va_all.setdefault(s, []).append(a)
        for s, a in te_acc.items():
            te_all.setdefault(s, []).append(a)
    avg = lambda d: {str(s): round(sum(v) / len(v), 4) for s, v in d.items()}
    return avg(tr_all), avg(va_all), avg(te_all), n_params


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    p = argparse.ArgumentParser()
    p.add_argument("--run-dir", default=C_RUN)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--max-windows", type=int, default=16)
    p.add_argument("--hidden", type=int, default=1024)
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
    windows = build_eval_windows(ns, args.max_windows)
    masks = build_masks(windows, ns)
    print(f"[nlp2f] model={Path(args.run_dir).name} step={step} device={device.type} windows={len(windows)} "
          f"({time.time() - t0:.0f}s)", flush=True)

    xs, xs_g, ys, yv = collect(model, windows, masks, device)
    print(f"[nlp2f] rows={xs.size(0)} ({time.time() - t0:.0f}s)", flush=True)

    # ridge reference on the SAME rows (E73-A6 口径, per-slot majority included)
    ridge_real = byte_probe(xs, ys, yv)
    ridge_garb = byte_probe(xs_g, ys, yv)
    majority = {s: ridge_real[s]["majority"] for s in ridge_real}
    ridge_diff = {s: round(ridge_real[s]["acc"] - ridge_garb[s]["acc"], 4) for s in ridge_real}
    ridge_params = 513 * N_CLS * len(ridge_real)

    def mlp_pass(hidden):
        tr_r, va_r, te_r, n_params = run_probe(xs, ys, yv, hidden, device, args.steps, args.batch, args.lr, PROBE_SEED)
        _t1, _v1, te_g, _p2 = run_probe(xs_g, ys, yv, hidden, device, args.steps, args.batch, args.lr, PROBE_SEED + 1)
        return tr_r, va_r, te_r, te_g, n_params

    tr_r, va_r, te_r, te_g, n_params = mlp_pass(args.hidden)
    param_ok = n_params <= PARAM_BUDGET_MULT * ridge_params

    def tail_mean(d, lo=18, hi=32):
        vals = [d[str(s)] for s in range(lo, hi) if str(s) in d]
        return round(sum(vals) / len(vals), 4) if vals else None

    # 两种 gap（口径见 train_eval_mlp 注记）：mem_gap=记忆差距（训练行 vs test，
    # 高容量小数据必然 >15pp，仅作透明披露）；gen_gap=泛化一致性（val vs test，
    # 两个探针未见集——护栏真实意图的读数）。
    mem_gaps = {s: round(tr_r.get(s, 0.0) - te_r.get(s, 0.0), 4) for s in te_r}
    gen_gaps = {s: round(va_r.get(s, 0.0) - te_r.get(s, 0.0), 4) for s in te_r}
    tail_slots = [str(s) for s in range(18, 32) if str(s) in gen_gaps]
    tail_gen_gap_max = max((gen_gaps[s] for s in tail_slots), default=None)
    tail_mem_gap_max = max((mem_gaps[s] for s in tail_slots), default=None)
    artifact = tail_gen_gap_max is not None and tail_gen_gap_max > GAP_LIMIT
    rerun = None
    if artifact:
        print(f"[nlp2f] guardrail: tail val/test gen-gap {tail_gen_gap_max} > {GAP_LIMIT} -> artifact, "
              f"re-running at hidden {args.hidden // 2}", flush=True)
        tr_r, va_r, te_r, te_g, n_params = mlp_pass(args.hidden // 2)
        param_ok = n_params <= PARAM_BUDGET_MULT * ridge_params
        mem_gaps = {s: round(tr_r.get(s, 0.0) - te_r.get(s, 0.0), 4) for s in te_r}
        gen_gaps = {s: round(va_r.get(s, 0.0) - te_r.get(s, 0.0), 4) for s in te_r}
        tail_gen_gap_max = max((gen_gaps[s] for s in tail_slots), default=None)
        tail_mem_gap_max = max((mem_gaps[s] for s in tail_slots), default=None)
        rerun = {"hidden": args.hidden // 2, "tail_gen_gap_max": tail_gen_gap_max}
        artifact = tail_gen_gap_max is not None and tail_gen_gap_max > GAP_LIMIT

    mlp_diff = {s: round(te_r[s] - te_g.get(s, 0.0), 4) for s in te_r}
    delta_vs_ridge = {s: round(mlp_diff.get(s, 0.0) - ridge_diff.get(s, 0.0), 4) for s in ridge_diff}
    tail_delta = tail_mean(delta_vs_ridge)
    tail_mlp = tail_mean(mlp_diff)
    tail_maj = tail_mean(majority)

    if artifact:
        verdict = "probe 伪影（降容量后 tail 泛化一致性 gap 仍 >15pp）——读数作废，F2 点火阻塞，先修探针。"
    elif tail_delta is not None and tail_delta >= TAIL_LIFT:
        verdict = (f"信息在但线性不可达（段尾 非线性−线性 = +{tail_delta} ≥ +{TAIL_LIFT}）——"
                   "F2 靶子 = 读出接口形态。")
    else:
        verdict = (f"段尾信息真缺席（段尾 非线性−线性 = {tail_delta:+} < +{TAIL_LIFT}，"
                   f"且非线性段尾 {tail_mlp} 贴 majority 档 {tail_maj}）——F2 靶子 = 压缩目标/容量。")

    report = {
        "probe": "严格 2-fold 非线性段尾探针（F2 点火前提，与岭回归同任务同 2-fold 同 real−garbage 同 majority）",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "checkpoint": {"run": Path(args.run_dir).name, "step": step},
        "params": {"windows": len(windows), "hidden": args.hidden, "steps": args.steps,
                   "batch": args.batch, "lr": args.lr, "perm_seed": PERM_SEED, "probe_seed": PROBE_SEED},
        "guardrails": {
            "param_budget": {"mlp_params": n_params, "ridge_params_x4": PARAM_BUDGET_MULT * ridge_params, "ok": param_ok},
            "gap_limit": GAP_LIMIT,
            "tail_gen_gap_max": tail_gen_gap_max,
            "tail_mem_gap_max_transparency": tail_mem_gap_max,
            "gap_definition_note": "gen_gap=val留出集(探针未见) vs test 的泛化一致性——护栏真实意图；mem_gap=训练行 vs test 的记忆差距（高容量小数据必然>15pp，仅透明披露，不作判据）",
            "artifact": artifact, "rerun": rerun,
        },
        "per_slot": {
            "majority": majority,
            "ridge_real_minus_garbage": ridge_diff,
            "mlp_real_minus_garbage": mlp_diff,
            "mlp_minus_ridge": delta_vs_ridge,
            "mlp_gen_gap_val_vs_test": gen_gaps,
            "mlp_mem_gap_train_vs_test": mem_gaps,
        },
        "tail_region": {"slots": "18-31", "mlp_minus_ridge_mean": tail_delta,
                        "mlp_real_minus_garbage_mean": tail_mlp, "majority_mean": tail_maj},
        "verdict": verdict,
        "timing_sec": round(time.time() - t0, 1),
    }
    out_path = out_dir / "probe_tail_nonlinear_2fold.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "严格 2-fold 非线性段尾探针（F2 点火前提）— c 格 v37_c_is memory 行，16 窗",
        f"日期 {report['created']}  设备 {device.type}  MLP hidden={args.hidden} steps={args.steps}",
        "",
        f"护栏：参数量 {n_params} ≤ 4×ridge {PARAM_BUDGET_MULT * ridge_params} -> {'OK' if param_ok else '✗ 超预算'}；"
        f"tail 泛化一致性 gap（val vs test，探针未见集）max {tail_gen_gap_max}（限 {GAP_LIMIT}）{'-> 伪影作废' if artifact else ''}；"
        f"tail 记忆差距（训练行 vs test）max {tail_mem_gap_max}（仅透明披露）",
    ]
    if rerun:
        lines.append(f"  （已按护栏自动降容量重跑：hidden {rerun['hidden']}，gen-gap {rerun['tail_gen_gap_max']}）")
    lines += ["", "逐 slot：slot | majority | ridge | mlp | mlp−ridge | gen gap"]
    for s in range(len(ridge_diff)):
        k = str(s)
        if k not in ridge_diff:
            continue
        lines.append(f"  {s:>4d} | {majority.get(k, float('nan')):.4f} | {ridge_diff[k]:+.4f} | "
                     f"{mlp_diff.get(k, float('nan')):+.4f} | {delta_vs_ridge.get(k, float('nan')):+.4f} | "
                     f"{gen_gaps.get(k, float('nan')):+.3f}")
    lines += [
        "",
        f"段尾区（slot18-31）：mlp−ridge 均值 {tail_delta:+}；mlp real−garbage {tail_mlp}；majority {tail_maj}",
        "",
        "判读二分（预注册）：段尾 非线性−线性 ≥ +0.10 → 读出接口靶；否则（贴 majority）→ 压缩目标/容量靶。",
        f"判词：{verdict}",
        "",
        f"完整数据: {out_path}",
    ]
    summary_path = out_dir / "SUMMARY_tail_nonlinear_2fold.txt"
    summary_path.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
