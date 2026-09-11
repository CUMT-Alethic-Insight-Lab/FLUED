# E124 软训硬评缝量化仪器（零训练对拍，红队总审 2026-09-11 裁定收官件）。
#
# 缝的定义：E124 训练全程软门（rt_hard=False：logsigmoid 温度门 + 可学
# α-entmax 命中分布），判读全在硬门（rt_hard=True：名次<k 掩码 + entmax 精确
# 零）——top-k 解码必须 top-k 训练的文献判例对口，缝的大小必须量化进判读注记。
#
# 口径：同一 checkpoint、同一批评估窗（eval 流 + seed 1042 掩码口径，与训练器
# evaluate() 同构，复用 probe_oracle_write_verdict 的 build_eval_windows /
# build_masks / load_model），逐窗各跑一次软门与硬门前向（同预算、同 byte_mask、
# 同切点），收集：
#   - 输出 logits 差：L∞（valid 位最大绝对差）与 KL(P_hard‖P_soft)（valid 位均值）
#   - 遮蔽位目标 byte acc 差（direct/backbone 两腿，masked_slot 口径，hard − soft）
#   - 门差：block-1 门后分布 TV 距离与 KL、软支持集 vs 硬命中集对称差、命中数
# 零训练：no_grad + eval + 参数冻结，纯仪器。hard 臂即训练器 eval 部署姿态
# （progress=1.0 终点预算，温度对硬模式无作用仍按任务书 §6 钉 temp）。
#
# 用法：
#   python tools/analysis/v3_6/probe_e124_soft_hard_gate.py \
#       --run-dir checkpoints/_smoke_e124_comb_500 --windows 4
# 输出：<out-dir>/summary.json + stdout 摘要。
import argparse
import json
import sys
import time
from pathlib import Path

import torch
import torch.nn.functional as F

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from flued.data import MASK_ID, PAD_ID  # noqa: E402
from tools.analysis.v3_6.probe_oracle_write_verdict import (  # noqa: E402
    build_eval_windows,
    build_masks,
    load_model,
)
from tools.train.v3_3.train_v33 import make_targets  # noqa: E402
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402


def masked_byte_acc(logits: torch.Tensor, targets: torch.Tensor, slot: torch.Tensor):
    """遮蔽位目标 byte acc（masked_slot 口径；空集返回 None，不造假分数）。"""
    if not bool(slot.any()):
        return None
    pred = logits.argmax(dim=-1)[slot]
    gold = targets[slot]
    return float((pred == gold).float().mean().item())


def seam_metrics(
    logits_soft: torch.Tensor,
    logits_hard: torch.Tensor,
    domain: torch.Tensor,
    attn_soft: torch.Tensor,
    attn_hard: torch.Tensor,
    hit_hard: torch.Tensor | None,
) -> dict:
    """软/硬门单窗差分（纯函数，仪器与单测共用）。

    logits_*: (..., V) 输出 logits（字节级 (B,T,V) 或 chunk 网格 (B,C,S,V) 皆可）；
    domain: logits 前导维的 bool 有效位掩码（PAD/无效位不计入差分域）。
    attn_*: (B, H, n, n) block-1 门后分布（need_attn=True 捕获口）。
    hit_hard: (B, H, n, n) bool 硬门命中集（软门侧无离散命中集，恒 None 时
    以 attn_hard>0 代支持集口径）。
    返回全 float 标量 dict（JSON 可落盘；两端同键）。"""
    ls = logits_soft.float()
    lh = logits_hard.float()
    v3 = domain.unsqueeze(-1)
    diff = (lh - ls).abs().masked_fill(~v3, 0.0)
    linf = float(diff.max().item())
    logp_s = F.log_softmax(ls, dim=-1)
    logp_h = F.log_softmax(lh, dim=-1)
    p_h = logp_h.exp()
    kl = (p_h * (logp_h - logp_s)).masked_fill(~v3, 0.0).sum(dim=-1).mean()
    # 门后分布差：TV + KL(P_hard‖P_soft)（对角护栏 padded 行两侧同为近似独热，
    # 计入无妨——与门语义无关的常量底）
    tv_q = 0.5 * (attn_hard - attn_soft).abs().sum(dim=-1)  # (B, H, n)
    eps = 1e-12
    kl_q = (
        attn_hard * (attn_hard.clamp_min(eps).log() - attn_soft.clamp_min(eps).log())
    ).sum(dim=-1)
    sup_s = attn_soft > 0
    sup_h = hit_hard if hit_hard is not None else (attn_hard > 0)
    sym = (sup_s ^ sup_h).sum(dim=-1).float()
    return {
        "logit_linf": linf,
        "logit_kl": float(kl.item()),
        "gate_tv": float(tv_q.mean().item()),
        "gate_tv_max": float(tv_q.max().item()),
        "gate_kl": float(kl_q.mean().item()),
        "soft_support": float(sup_s.sum(dim=-1).float().mean().item()),
        "hard_hit": float(sup_h.sum(dim=-1).float().mean().item()),
        "support_symdiff": float(sym.mean().item()),
    }


def _masked_acc_block(out: dict, targets, masked_slot) -> dict:
    return {
        "backbone": masked_byte_acc(out["logits_backbone"], targets, masked_slot),
        "direct": masked_byte_acc(out["logits_direct"], targets, masked_slot),
    }


def aggregate(rows: list[dict]) -> dict:
    keys = [
        "logit_linf", "logit_kl", "gate_tv", "gate_tv_max", "gate_kl",
        "soft_support", "hard_hit", "support_symdiff",
        "backbone_acc_diff", "direct_acc_diff",
    ]
    out: dict = {}
    for k in keys:
        vals = [r[k] for r in rows if r.get(k) is not None]
        if not vals:
            continue
        vals_t = torch.tensor(vals)
        out[k] = {
            "mean": float(vals_t.mean()),
            "median": float(vals_t.median()),
            "max": float(vals_t.max()),
            "min": float(vals_t.min()),
        }
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="E124 软训硬评缝量化仪器（零训练）")
    ap.add_argument("--run-dir", default="checkpoints/_smoke_e124_comb_500")
    ap.add_argument("--ckpt", default="", help="显式 ckpt 文件（默认 <run-dir>/latest.pt）")
    ap.add_argument("--windows", type=int, default=4, help="评估窗数")
    ap.add_argument("--temp", type=float, default=0.05, help="软门温度 τ（默认 = temp_end）")
    ap.add_argument("--k", type=int, default=-1, help="绝对预算覆写（<0 = 按 progress 终点表）")
    ap.add_argument("--progress", type=float, default=1.0, help="退火进度（默认 1.0 = eval 终点预算）")
    ap.add_argument("--out-dir", default="outputs/_e124_soft_hard_seam_20260911")
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = ap.parse_args()

    device = torch.device(args.device)
    run_dir = Path(args.run_dir)
    ckpt_path = Path(args.ckpt) if args.ckpt else run_dir / "latest.pt"
    model, ns, step = load_model(run_dir, device)
    if args.ckpt:  # 显式 ckpt 覆盖 latest（load_model 默认吃 latest.pt）
        payload = torch.load(ckpt_path, map_location=device, weights_only=False)
        model.load_state_dict(payload["model"], strict=True)
        step = int(payload.get("step", 0))
    bb = getattr(model, "backbone", None)
    if bb is None or not getattr(bb, "e124_gate", False):
        raise SystemExit(f"{ckpt_path}: 非 E124 臂（backbone.e124_gate 关）——缝仪器只对 e124 ckpt 有定义")

    ns.data_manifest = ""
    windows = build_eval_windows(ns, args.windows)
    masks = build_masks(windows, ns)
    alpha = float(bb.e124_alpha_value().detach())
    knobs_hard = {"rt_hard": True, "rt_progress": float(args.progress)}
    knobs_soft = {"rt_hard": False, "rt_progress": float(args.progress), "rt_temp": float(args.temp)}
    if args.k > 0:
        for kn in (knobs_hard, knobs_soft):
            kn["rt_budget"] = int(args.k)

    rows = []
    grid_mismatch = 0
    t0 = time.time()
    for i, (batch, mbatch) in enumerate(zip(windows, masks)):
        for j in range(batch.size(0)):
            ids = batch[j]
            cut = int(ids.ne(PAD_ID).sum())
            clean = ids[:cut].unsqueeze(0).to(device)
            byte_mask = mbatch[j][:cut].unsqueeze(0).to(device).bool()
            source = clean.masked_fill(byte_mask, MASK_ID)
            outs = {}
            attns = {}
            hits = {}
            for arm, kn in (("soft", knobs_soft), ("hard", knobs_hard)):
                bb.e124_rt_hard = kn["rt_hard"]
                bb.e124_rt_progress = kn["rt_progress"]
                bb.e124_rt_temp = kn.get("rt_temp", float(getattr(ns, "e124_gate_temp_end", 0.05)))
                if "rt_budget" in kn:
                    bb.e124_rt_budget = kn["rt_budget"]
                else:
                    bb.e124_rt_budget = None
                with torch.no_grad(), torch.autocast(
                    "cuda", dtype=torch.bfloat16, enabled=bool(ns.amp) and device.type == "cuda"
                ):
                    outs[arm] = s1.s1_forward(
                        model, source, ns, clean=clean, byte_mask=byte_mask, need_attn=True
                    )
                # 捕获槽位逐臂即取（下一次 forward 会覆盖 bb 寄存口）
                attns[arm] = bb.last_block1_attn
                hits[arm] = bb.last_e124_hit
            attn_soft, attn_hard = attns["soft"], attns["hard"]
            hit_hard = hits["hard"]
            budget = float(bb.last_e124_k) if bb.last_e124_k is not None else float("nan")
            n_real = int(outs["hard"]["chunks"].chunk_mask[0].sum())
            if budget >= n_real:
                # bypass 窗：命中集寄存槽不更新（stale 槽位卫生）——门差口径只对
                # 激活窗有定义
                hit_hard = None

            ch_s = outs["soft"]["chunks"]
            ch_h = outs["hard"]["chunks"]
            grid_ok = bool((ch_s.chunk_ids == ch_h.chunk_ids).all()) and \
                int(ch_s.chunk_mask[0].sum()) == int(ch_h.chunk_mask[0].sum())
            if not grid_ok:
                grid_mismatch += 1
            targets, slot_mask, masked_slot = make_targets(
                clean, byte_mask, ch_h.chunk_ids, ch_h.offsets, ns.max_chunks, ns.max_span
            )
            m = seam_metrics(
                outs["soft"]["logits_backbone"], outs["hard"]["logits_backbone"],
                slot_mask, attn_soft, attn_hard, hit_hard,
            )
            acc_s = _masked_acc_block(outs["soft"], targets, masked_slot)
            acc_h = _masked_acc_block(outs["hard"], targets, masked_slot)
            m["backbone_acc_diff"] = (
                None if acc_h["backbone"] is None or acc_s["backbone"] is None
                else acc_h["backbone"] - acc_s["backbone"]
            )
            m["direct_acc_diff"] = (
                None if acc_h["direct"] is None or acc_s["direct"] is None
                else acc_h["direct"] - acc_s["direct"]
            )
            rows.append({
                "window": i,
                "n_bytes": cut,
                "n_real": n_real,
                "budget": budget,
                "gate_active": bool(budget < n_real),
                "grid_stable": grid_ok,
                **m,
                "masked_acc_soft": acc_s,
                "masked_acc_hard": acc_h,
            })

    n_direct = len({r["window"] for r in rows})
    summary = {
        "instrument": "probe_e124_soft_hard_gate",
        "ckpt": str(ckpt_path),
        "step": step,
        "device": str(device),
        "windows": n_direct,
        "eval_mask_seed": int(getattr(ns, "eval_mask_seed", -1)),
        "soft_knobs": {**knobs_soft, "temp": float(args.temp)},
        "hard_knobs": knobs_hard,
        "alpha": alpha,
        "grid_mismatch_windows": grid_mismatch,
        "gate_active_windows": sum(1 for r in rows if r["gate_active"]),
        "timing_sec": round(time.time() - t0, 1),
        "aggregate": aggregate(rows),
        "per_window": rows,
    }
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "summary.json"
    out_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary["aggregate"], ensure_ascii=False, indent=2), flush=True)
    print(f"[e124-seam] ckpt={ckpt_path} step={step} windows={n_direct} "
          f"gate_active={summary['gate_active_windows']}/{n_direct} "
          f"grid_mismatch={grid_mismatch} alpha={alpha:.4f} -> {out_path}", flush=True)


if __name__ == "__main__":
    main()
