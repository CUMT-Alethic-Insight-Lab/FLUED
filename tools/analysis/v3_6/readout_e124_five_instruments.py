# E124 收官五仪表雏形（零训练 eval-only 探针，2026-09-13）。
#
# 任务书：docs/versions/v3.7/FLUED_V3_7_E124_HARD_BUDGET_GATE_20260909_CN.md §4
# 判读表（v1 修订 2026-09-12：五仪表同批收官判读）。脚手架沿用
# probe_e124_soft_hard_gate.py（load_model / build_eval_windows / build_masks，
# 与训练器 evaluate() 同构：eval 流 + mask seed 1042 + 硬门部署姿态）。
#
# 五仪表（全部读数原样落盘，字段名中性，无判词）：
#   rd        仪表①  预算扫描 RD 曲线：预算档 × {整体 backbone_acc, 遮蔽位 byte acc,
#                 实际命中数（解析 min(k, 因果候选数)）}
#   scramble  仪表②  K 侧行置乱 Δ 逐档：正常 vs 只置换 K/index 行前向，遮蔽位
#                 byte acc 的 intact−scrambled Δ（逐窗 + bootstrap 95% CI）
#   posprior  仪表③  位置先验探针：终点预算 k 硬门命中集 vs 纯位置预测器
#                 （因果方向最近 min(k,候选数) 行）的逐窗重合率 + 命中位置熵 +
#                 首近因档直方图
#   traj      仪表④  遮蔽位读出精度轨迹（train_log.jsonl 训练步行字段）+
#                 summary.json 收官 eval 锚 + 盲猜地板（窗内众数字节 / 1/256）
#   ablation  仪表⑤  定向消融双跑：store 行全剔除 vs 只剔遮蔽位所在 chunk 的
#                 store 行，遮蔽位/非遮蔽位 acc 双分解 Δ（store_block=None
#                 逐位对拍先行，不过不许跑）
#
# 同卷纪律：所有仪表所有列用同一批窗（eval 流 + seed 1042 掩码；列间
# 窗/掩码决定性由 load 侧 seed 钉死，非门列同窗用于 ④ 地板）。
# 断点可续：<out-root>/<instrument>/<run_name>/summary.json 存在即跳过
# （--overwrite 强制重跑；items.jsonl 先写、summary.json 后写 = 完成标记）。
#
# 用法（例）：
#   python tools/analysis/v3_6/readout_e124_five_instruments.py rd \
#       --runs checkpoints/v37ks_a_e124_comb_10k_ctx4096_20260910 --windows 16
#   python tools/analysis/v3_6/readout_e124_five_instruments.py all --device cuda
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from argparse import Namespace
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from flued.data import MASK_ID, PAD_ID  # noqa: E402
from tools.analysis.v3_6.probe_e124_soft_hard_gate import masked_byte_acc  # noqa: E402
from tools.analysis.v3_6.probe_oracle_write_verdict import (  # noqa: E402
    build_eval_windows,
    build_masks,
    load_model,
)
from tools.train.v3_3.train_v33 import make_targets  # noqa: E402
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402

DEFAULT_RUNS = [
    "checkpoints/v37ks_a_e124_comb_10k_ctx4096_20260910",
    "checkpoints/v37ks_a_e124_gate_10k_ctx4096_20260910",
    "checkpoints/v37ks_a_e124_demand_10k_ctx4096_20260910",
    "checkpoints/v37ks_a_e124_cont_10k_ctx4096_20260910",
]
DEFAULT_BUDGETS = [1, 2, 3, 4, 6, 9, 13, 20, 30, 50, 86, 130, 173]  # 9 = 退火终点必含
DEFAULT_SCRAMBLE_BUDGETS = [1, 2, 4, 9, 173]
DEFAULT_K = 9
SCRAMBLE_SEED_BASE = 20260913  # 逐窗置换种子 = base + window_idx（可复现）
BOOT_SEED = 20260913


# ---------------------------------------------------------------------------
# 纯函数（仪器与单测共用）
# ---------------------------------------------------------------------------


def k_scramble_perm(n_real: int, seed: int) -> list[int]:
    """K 侧置乱置换（仪表②）：range(n_real) 的随机置换，种子决定论。"""
    if n_real < 2:
        return list(range(n_real))
    g = torch.Generator()
    g.manual_seed(int(seed))
    return torch.randperm(n_real, generator=g).tolist()


def bootstrap_ci_mean(values: list[float], n_boot: int = 10000, seed: int = BOOT_SEED,
                      level: float = 0.95) -> dict:
    """逐窗 Δ 均值的 bootstrap 百分位 CI（重采样决定论）。空集返回空 dict。"""
    vals = [v for v in values if v is not None]
    if not vals:
        return {}
    t = torch.tensor(vals, dtype=torch.float64)
    n = t.numel()
    g = torch.Generator()
    g.manual_seed(int(seed))
    idx = torch.randint(0, n, (int(n_boot), n), generator=g)
    means = t[idx].mean(dim=1)
    lo_q = (1.0 - level) / 2.0 * 100.0
    hi_q = (1.0 + level) / 2.0 * 100.0
    return {
        "mean": float(t.mean()),
        "ci_lo": float(torch.quantile(means, lo_q / 100.0)),
        "ci_hi": float(torch.quantile(means, hi_q / 100.0)),
        "n": int(n),
        "n_boot": int(n_boot),
        "level": float(level),
    }


def analytic_hits(chunk_mask_row: torch.Tensor, k: int) -> tuple[list[int], float]:
    """窗实际命中数（仪表①口径：逐查询 min(k, 因果候选数)，因果含对角 →
    候选数 = chunk_mask 前缀和）。返回（逐真实查询命中数, 窗均值）。"""
    cum = torch.cumsum(chunk_mask_row.to(torch.long), dim=0)
    hits = torch.where(chunk_mask_row, cum.clamp_max(int(k)), torch.zeros_like(cum))
    per_query = hits[chunk_mask_row].tolist()
    mean = float(sum(per_query) / len(per_query)) if per_query else 0.0
    return per_query, mean


def _entropy_bits(counts: list[int]) -> float:
    total = sum(counts)
    if total <= 0:
        return 0.0
    h = 0.0
    for c in counts:
        if c > 0:
            p = c / total
            h -= p * math.log2(p)
    return h


def position_prior_metrics(hit: torch.Tensor, chunk_mask: torch.Tensor, k: int) -> dict:
    """仪表③ 纯函数：硬门命中集 vs 纯位置预测器的逐窗统计。

    hit: (1, H, n, n) bool（bb.last_e124_hit，门激活前提）；
    chunk_mask: (1, n) bool 真实块。
    预测器（head 无关）：真实查询 i 命中因果方向（j ≤ i 的真实行）上最近的
    m_i = min(k, cum_i) 行。重合率 = |pred ∩ actual| / |pred|（actual 命中数
    构造上 = m_i，precision == recall）。"""
    cm = chunk_mask[0]
    n = int(cm.numel())
    real_idx = torch.nonzero(cm, as_tuple=False).flatten().tolist()
    cum = torch.cumsum(cm.to(torch.long), dim=0)
    H = int(hit.shape[1])
    overlap_sum = 0.0
    overlap_n = 0
    exact = 0
    lag_counts: dict[int, int] = {}
    abspos_counts: dict[int, int] = {}
    first_lag_counts: dict[int, int] = {}
    for i in real_idx:
        m = min(int(k), int(cum[i]))
        # 最近 m 个真实行（含 i 本行）：real 列表里 cum[i]-m 起的连续段
        r = int(cum[i])
        pred = set(real_idx[r - m:r])
        for h in range(H):
            actual_rows = torch.nonzero(hit[0, h, i, :], as_tuple=False).flatten().tolist()
            a = set(actual_rows)
            inter = len(pred & a)
            overlap_sum += inter / m if m > 0 else 0.0
            overlap_n += 1
            exact += int(pred == a)
            for j in a:
                lag_counts[i - j] = lag_counts.get(i - j, 0) + 1
                abspos_counts[j] = abspos_counts.get(j, 0) + 1
            if a:
                fl = i - max(a)  # 首近因档 = 到最近命中行的距离
                first_lag_counts[fl] = first_lag_counts.get(fl, 0) + 1
    first_lags = [i - max(torch.nonzero(hit[0, h, i, :], as_tuple=False).flatten().tolist())
                  for i in real_idx for h in range(H)
                  if bool(hit[0, h, i, :].any())]
    return {
        "n_real": len(real_idx),
        "k": int(k),
        "hit_rate": overlap_sum / overlap_n if overlap_n else None,
        "query_head_exact_rate": exact / overlap_n if overlap_n else None,
        "hit_lag_entropy_bits": _entropy_bits(list(lag_counts.values())),
        "hit_abspos_entropy_bits": _entropy_bits(list(abspos_counts.values())),
        "lag_hist": _hist_to_lists(lag_counts),
        "abspos_hist": _hist_to_lists(abspos_counts),
        "first_lag_hist": _hist_to_lists(first_lag_counts),
        "mean_first_lag": (sum(first_lags) / len(first_lags)) if first_lags else None,
        "n_query_head_obs": overlap_n,
    }


def _hist_to_lists(counts: dict[int, int]) -> dict:
    keys = sorted(counts)
    return {"values": [float(v) for v in keys], "counts": [int(counts[v]) for v in keys]}


def majority_floor_bytes(clean_row: torch.Tensor, byte_mask_row: torch.Tensor) -> dict:
    """盲猜地板纯函数（仪表④）：一窗内「众数字节」两口径（全窗 / 仅可见位）
    + 1/256 均匀。输入 1-D byte id 张量与同形遮蔽 bool。"""
    flat = clean_row.flatten()
    vis = flat[~byte_mask_row.flatten()]
    maj_all = int(torch.bincount(flat, minlength=256).argmax())
    maj_vis = int(torch.bincount(vis, minlength=256).argmax()) if vis.numel() else maj_all
    return {"maj_byte_all": maj_all, "maj_byte_visible": maj_vis, "acc_uniform": 1.0 / 256.0}


def acc_split(logits: torch.Tensor, targets: torch.Tensor,
              slot: torch.Tensor, masked_slot: torch.Tensor) -> dict:
    """遮蔽位 / 非遮蔽位（valid ∩ ~masked）双分解 byte acc（空集 None）。"""
    unmasked = slot & ~masked_slot
    return {
        "masked": masked_byte_acc(logits, targets, masked_slot),
        "unmasked": masked_byte_acc(logits, targets, unmasked),
    }


# ---------------------------------------------------------------------------
# 公共装载/前向
# ---------------------------------------------------------------------------


def hardware_fingerprint(device: torch.device) -> dict:
    fp = {
        "torch_version": torch.__version__,
        "device": str(device),
        "gpu_name": None,
        "cuda_version": torch.version.cuda,
    }
    if device.type == "cuda":
        fp["gpu_name"] = torch.cuda.get_device_name(device.index or 0)
    return fp


def set_hard_posture(bb, ns, budget: int | None) -> None:
    """eval 部署姿态：硬门 + 终点进度 + temp_end；budget 覆写（None=按进度表）。"""
    bb.e124_rt_hard = True
    bb.e124_rt_progress = 1.0
    bb.e124_rt_temp = float(getattr(ns, "e124_gate_temp_end", 0.05))
    bb.e124_rt_budget = (int(budget) if budget is not None else None)


def load_run(run_dir: Path, device: torch.device):
    model, ns, step = load_model(run_dir, device)
    bb = getattr(model, "backbone", None)
    gated = bool(getattr(bb, "e124_gate", False)) if bb is not None else False
    return model, ns, step, bb, gated


def iter_windows(ns, n_windows: int, device: torch.device):
    """与 probe_e124_soft_hard_gate 完全同构的窗流：eval 流 + seed1042 掩码。"""
    ns.data_manifest = ""
    windows = build_eval_windows(ns, n_windows)
    masks = build_masks(windows, ns)
    for i, (batch, mbatch) in enumerate(zip(windows, masks)):
        for j in range(batch.size(0)):
            ids = batch[j]
            cut = int(ids.ne(PAD_ID).sum())
            clean = ids[:cut].unsqueeze(0).to(device)
            byte_mask = mbatch[j][:cut].unsqueeze(0).to(device).bool()
            source = clean.masked_fill(byte_mask, MASK_ID)
            yield i * batch.size(0) + j, clean, byte_mask, source


def forward_once(model, ns, source, clean, byte_mask, device: torch.device,
                 need_attn: bool = False, store_block=None, k_perm=None):
    """单窗前向 + 目标网格（与训练器 evaluate 的 step_model 同构）。"""
    out = s1.s1_forward(
        model, source, ns, clean=clean, byte_mask=byte_mask,
        store_block_override=store_block, need_attn=need_attn,
        k_row_perm_override=k_perm,
    )
    ch = out["chunks"]
    targets, slot_mask, masked_slot = make_targets(
        clean, byte_mask, ch.chunk_ids, ch.offsets, ns.max_chunks, ns.max_span
    )
    return out, ch, targets, slot_mask, masked_slot


def write_outputs(out_dir: Path, summary: dict, items: list[dict]) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    items_path = out_dir / "items.jsonl"
    with items_path.open("w", encoding="utf-8") as f:
        for r in items:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    out_path = out_dir / "summary.json"  # 完成标记最后落盘（断点续跑判据）
    out_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_path


def skip_summary(out_dir: Path, reason: str, args, instrument: str, run_name: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    summary = {
        "instrument": instrument,
        "run": run_name,
        "status": "skipped",
        "reason": reason,
        "hardware": hardware_fingerprint(torch.device("cpu")),
        "windows": args.windows,
    }
    return write_outputs(out_dir, summary, [])


def prepare_run(run: str, instrument: str, args):
    """收官守卫 + 输出目录。返回 (run_dir, run_name, out_dir) 或 None（跳过）。"""
    run_dir = Path(run)
    run_name = run_dir.name
    out_dir = Path(args.out_root) / instrument / run_name
    if (out_dir / "summary.json").exists() and not args.overwrite:
        print(f"[{instrument}] {run_name}: summary.json 已在，跳过（--overwrite 重跑）", flush=True)
        return None
    if not (run_dir / "summary.json").exists():
        print(f"[{instrument}] {run_name}: 无 summary.json（未收官）——记 skip", flush=True)
        skip_summary(out_dir, "run not finished (run_dir/summary.json absent)", args, instrument, run_name)
        return None
    return run_dir, run_name, out_dir


# ---------------------------------------------------------------------------
# 仪表① RD 曲线
# ---------------------------------------------------------------------------


def run_rd(runs: list[str], args) -> None:
    budgets = [int(b) for b in args.budgets]
    for run in runs:
        prepared = prepare_run(run, "rd", args)
        if prepared is None:
            continue
        run_dir, run_name, out_dir = prepared
        device = torch.device(args.device)
        model, ns, step, bb, gated = load_run(run_dir, device)
        items: list[dict] = []
        if not gated:
            skip_summary(out_dir, "backbone.e124_gate=False (非门列): 预算覆写无效应", args, "rd", run_name)
            continue
        alpha = float(bb.e124_alpha_value().detach())
        t0 = time.time()
        for k in budgets:
            set_hard_posture(bb, ns, budget=k)
            for w, clean, byte_mask, source in iter_windows(ns, args.windows, device):
                with torch.no_grad(), torch.autocast(
                    "cuda", dtype=torch.bfloat16, enabled=bool(ns.amp) and device.type == "cuda"
                ):
                    out, ch, targets, slot, masked_slot = forward_once(
                        model, ns, source, clean, byte_mask, device)
                n_real = int(ch.chunk_mask[0].sum())
                _per_q, hits_mean = analytic_hits(ch.chunk_mask[0], k)
                items.append({
                    "run": run_name, "budget": k, "window": w,
                    "n_bytes": int(clean.numel()), "n_real": n_real,
                    "gate_active": bool(k < n_real),
                    "k_effective": None if bb.last_e124_k is None else float(bb.last_e124_k),
                    "mean_actual_hits": hits_mean,
                    "backbone_acc": masked_byte_acc(out["logits_backbone"], targets, slot),
                    "backbone_masked_acc": masked_byte_acc(out["logits_backbone"], targets, masked_slot),
                })
        summary = {
            "instrument": "rd", "run": run_name, "ckpt_step": step, "status": "ok",
            "budgets": budgets, "windows": args.windows,
            "eval_mask_seed": int(getattr(ns, "eval_mask_seed", -1)),
            "window_seed": int(getattr(ns, "seed", -1)) + 9999,
            "alpha": alpha, "hardware": hardware_fingerprint(device),
            "timing_sec": round(time.time() - t0, 1),
            "aggregate": _agg_rd(items, budgets),
        }
        path = write_outputs(out_dir, summary, items)
        print(f"[rd] {run_name}: {len(items)} 行 -> {path}", flush=True)


def _agg_rd(items: list[dict], budgets: list[int]) -> dict:
    agg = {}
    for k in budgets:
        rows = [r for r in items if r["budget"] == k]
        accs = [r["backbone_acc"] for r in rows if r["backbone_acc"] is not None]
        maccs = [r["backbone_masked_acc"] for r in rows if r["backbone_masked_acc"] is not None]
        hits = [r["mean_actual_hits"] for r in rows]
        agg[str(k)] = {
            "n_windows": len(rows),
            "gate_active_windows": sum(1 for r in rows if r["gate_active"]),
            "backbone_acc_mean": sum(accs) / len(accs) if accs else None,
            "backbone_masked_acc_mean": sum(maccs) / len(maccs) if maccs else None,
            "mean_actual_hits_mean": sum(hits) / len(hits) if hits else None,
        }
    return agg


# ---------------------------------------------------------------------------
# 仪表② K 侧置乱 Δ 逐档
# ---------------------------------------------------------------------------


def run_scramble(runs: list[str], args) -> None:
    budgets = [int(b) for b in args.scramble_budgets]
    for run in runs:
        prepared = prepare_run(run, "scramble", args)
        if prepared is None:
            continue
        run_dir, run_name, out_dir = prepared
        device = torch.device(args.device)
        model, ns, step, bb, gated = load_run(run_dir, device)
        if not gated:
            skip_summary(out_dir, "backbone.e124_gate=False (非门列): 置乱 Δ 无门内语义", args, "scramble", run_name)
            continue
        alpha = float(bb.e124_alpha_value().detach())
        t0 = time.time()
        items: list[dict] = []
        for k in budgets:
            set_hard_posture(bb, ns, budget=k)
            for w, clean, byte_mask, source in iter_windows(ns, args.windows, device):
                with torch.no_grad(), torch.autocast(
                    "cuda", dtype=torch.bfloat16, enabled=bool(ns.amp) and device.type == "cuda"
                ):
                    out_i, ch, targets, slot, masked_slot = forward_once(
                        model, ns, source, clean, byte_mask, device)
                    n_real = int(ch.chunk_mask[0].sum())
                    perm = k_scramble_perm(n_real, SCRAMBLE_SEED_BASE + w)
                    n_fixed = sum(1 for a, b in enumerate(perm) if a == b)
                    out_s, ch_s, t_s, slot_s, ms_s = forward_once(
                        model, ns, source, clean, byte_mask, device, k_perm=[perm])
                grid_ok = bool((ch.chunk_ids == ch_s.chunk_ids).all())
                acc_i = masked_byte_acc(out_i["logits_backbone"], targets, masked_slot)
                acc_s = masked_byte_acc(out_s["logits_backbone"], t_s, ms_s)
                ov_i = masked_byte_acc(out_i["logits_backbone"], targets, slot)
                ov_s = masked_byte_acc(out_s["logits_backbone"], t_s, slot_s)
                items.append({
                    "run": run_name, "budget": k, "window": w,
                    "n_bytes": int(clean.numel()), "n_real": n_real,
                    "gate_active": bool(k < n_real), "grid_stable": grid_ok,
                    "perm_fixed_points": n_fixed,
                    "backbone_masked_acc_intact": acc_i,
                    "backbone_masked_acc_scrambled": acc_s,
                    "delta_masked": (None if acc_i is None or acc_s is None else acc_i - acc_s),
                    "backbone_acc_intact": ov_i,
                    "backbone_acc_scrambled": ov_s,
                    "delta_overall": (None if ov_i is None or ov_s is None else ov_i - ov_s),
                })
        summary = {
            "instrument": "scramble", "run": run_name, "ckpt_step": step, "status": "ok",
            "budgets": budgets, "windows": args.windows,
            "scramble_seed_base": SCRAMBLE_SEED_BASE,
            "eval_mask_seed": int(getattr(ns, "eval_mask_seed", -1)),
            "window_seed": int(getattr(ns, "seed", -1)) + 9999,
            "alpha": alpha, "hardware": hardware_fingerprint(device),
            "timing_sec": round(time.time() - t0, 1),
            "aggregate": _agg_scramble(items, budgets),
        }
        path = write_outputs(out_dir, summary, items)
        print(f"[scramble] {run_name}: {len(items)} 行 -> {path}", flush=True)


def _agg_scramble(items: list[dict], budgets: list[int]) -> dict:
    agg = {}
    for k in budgets:
        rows = [r for r in items if r["budget"] == k]
        dm = bootstrap_ci_mean([r["delta_masked"] for r in rows])
        do = bootstrap_ci_mean([r["delta_overall"] for r in rows])
        agg[str(k)] = {
            "n_windows": len(rows),
            "gate_active_windows": sum(1 for r in rows if r["gate_active"]),
            "grid_stable_windows": sum(1 for r in rows if r["grid_stable"]),
            "perm_fixed_points_mean": (sum(r["perm_fixed_points"] for r in rows) / len(rows)) if rows else None,
            "delta_masked": dm,
            "delta_overall": do,
        }
    return agg


# ---------------------------------------------------------------------------
# 仪表③ 位置先验探针
# ---------------------------------------------------------------------------


def run_posprior(runs: list[str], args) -> None:
    k = int(args.k)
    for run in runs:
        prepared = prepare_run(run, "posprior", args)
        if prepared is None:
            continue
        run_dir, run_name, out_dir = prepared
        device = torch.device(args.device)
        model, ns, step, bb, gated = load_run(run_dir, device)
        if not gated:
            skip_summary(out_dir, "backbone.e124_gate=False (非门列): 无命中集寄存", args, "posprior", run_name)
            continue
        alpha = float(bb.e124_alpha_value().detach())
        set_hard_posture(bb, ns, budget=k)
        t0 = time.time()
        items: list[dict] = []
        for w, clean, byte_mask, source in iter_windows(ns, args.windows, device):
            with torch.no_grad(), torch.autocast(
                "cuda", dtype=torch.bfloat16, enabled=bool(ns.amp) and device.type == "cuda"
            ):
                out, ch, _t, _s, _m = forward_once(
                    model, ns, source, clean, byte_mask, device, need_attn=True)
            n_real = int(ch.chunk_mask[0].sum())
            gate_active = bool(k < n_real)
            hit = bb.last_e124_hit  # bypass 窗寄存槽不更新（stale 槽位卫生）→ 只统计激活窗
            row = {"run": run_name, "window": w, "n_bytes": int(clean.numel()),
                   "n_real": n_real, "gate_active": gate_active,
                   "k_effective": None if bb.last_e124_k is None else float(bb.last_e124_k)}
            if gate_active and hit is not None:
                row.update(position_prior_metrics(hit, ch.chunk_mask, k))
            else:
                row["skip_reason"] = "bypass window (stale hit slot)" if gate_active else "gate bypass"
            items.append(row)
        ok_rows = [r for r in items if r.get("hit_rate") is not None]
        pooled_fl: dict[float, int] = {}
        for r in ok_rows:
            for v, c in zip(r["first_lag_hist"]["values"], r["first_lag_hist"]["counts"]):
                pooled_fl[v] = pooled_fl.get(v, 0) + c
        summary = {
            "instrument": "posprior", "run": run_name, "ckpt_step": step, "status": "ok",
            "k": k, "windows": args.windows,
            "gate_active_windows": len(ok_rows),
            "eval_mask_seed": int(getattr(ns, "eval_mask_seed", -1)),
            "window_seed": int(getattr(ns, "seed", -1)) + 9999,
            "alpha": alpha, "hardware": hardware_fingerprint(device),
            "timing_sec": round(time.time() - t0, 1),
            "aggregate": {
                "hit_rate": bootstrap_ci_mean([r["hit_rate"] for r in ok_rows]),
                "query_head_exact_rate": bootstrap_ci_mean([r["query_head_exact_rate"] for r in ok_rows]),
                "hit_lag_entropy_bits": bootstrap_ci_mean([r["hit_lag_entropy_bits"] for r in ok_rows]),
                "hit_abspos_entropy_bits": bootstrap_ci_mean([r["hit_abspos_entropy_bits"] for r in ok_rows]),
                "mean_first_lag": bootstrap_ci_mean([r["mean_first_lag"] for r in ok_rows]),
                "pooled_first_lag_hist": _hist_to_lists(pooled_fl),
            },
        }
        path = write_outputs(out_dir, summary, items)
        print(f"[posprior] {run_name}: gate_active={len(ok_rows)}/{len(items)} -> {path}", flush=True)


# ---------------------------------------------------------------------------
# 仪表④ 遮蔽位读出精度轨迹（零 GPU）
# ---------------------------------------------------------------------------


TRAJ_FIELDS = ["backbone_masked_acc", "backbone_unmasked_acc", "direct_acc", "backbone_acc"]


def run_traj(runs: list[str], args) -> None:
    for run in runs:
        prepared = prepare_run(run, "traj", args)
        if prepared is None:
            continue
        run_dir, run_name, out_dir = prepared
        items: list[dict] = []
        log_path = run_dir / "train_log.jsonl"
        with log_path.open(encoding="utf-8") as f:
            for line in f:
                row = json.loads(line)
                item = {"step": int(row["step"])}
                for fld in TRAJ_FIELDS:
                    item[fld] = row.get(fld)
                items.append(item)
        col_summary = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
        eval_anchor = {k: col_summary.get(k) for k in (
            "eval_backbone_masked_acc", "eval_backbone_unmasked_acc", "eval_backbone_acc",
            "eval_direct_acc", "eval_backbone_ppl", "eval_direct_ppl",
            "eval_e124_alpha", "eval_e124_k", "eval_chunks_per_sample")}
        floors, floor_meta = _traj_floors(run_dir, args)
        last = items[-1] if items else {}
        summary = {
            "instrument": "traj", "run": run_name, "status": "ok",
            "log_note": "train_log.jsonl 无 eval 行（eval 仅收官一次进 summary.json，"
                        "train_v36_s1.py:5232）；轨迹字段为训练步行口径（训练流+训练姿态），"
                        "收官锚为 summary.json 顶层 eval_* 字段（eval 流+硬门部署姿态）",
            "n_log_rows": len(items),
            "log_first": items[0] if items else None,
            "log_last": last,
            "log_max_masked": max((r["backbone_masked_acc"] for r in items
                                   if r.get("backbone_masked_acc") is not None), default=None),
            "eval_anchor": eval_anchor,
            "floors": floors,
            "floor_meta": floor_meta,
            "final_gap": {
                "eval_backbone_masked_acc_minus_floor_majority_all":
                    (None if eval_anchor["eval_backbone_masked_acc"] is None
                     or floors.get("acc_majority_all_mean") is None
                     else eval_anchor["eval_backbone_masked_acc"] - floors["acc_majority_all_mean"]),
                "eval_backbone_masked_acc_minus_floor_majority_visible":
                    (None if eval_anchor["eval_backbone_masked_acc"] is None
                     or floors.get("acc_majority_visible_mean") is None
                     else eval_anchor["eval_backbone_masked_acc"] - floors["acc_majority_visible_mean"]),
                "eval_backbone_masked_acc_minus_uniform":
                    (None if eval_anchor["eval_backbone_masked_acc"] is None
                     else eval_anchor["eval_backbone_masked_acc"] - 1.0 / 256.0),
            },
            "hardware": hardware_fingerprint(torch.device("cpu")),
        }
        path = write_outputs(out_dir, summary, items)
        print(f"[traj] {run_name}: {len(items)} 行 -> {path}", flush=True)


def _traj_floors(run_dir: Path, args) -> tuple[dict, dict]:
    """盲猜地板：同批 eval 窗（eval 流 + seed1042）的遮蔽位 byte 空间计算
    （列无关；chunk 网格截断位差忽略——众数字节地板不依赖列）。"""
    cfg = json.loads((run_dir / "resolved_config.json").read_text(encoding="utf-8"))
    cfg["data_manifest"] = ""
    ns = Namespace(**cfg)
    if s1._BPE_TOKENIZER is None and getattr(ns, "mask_mode", "mixed") == "mixed" and ns.mask_prob > 0:
        s1._load_bpe_tokenizer(ns.bpe_tokenizer_path)
    accs_all, accs_vis, n_masked_total = [], [], 0
    for _w, clean, byte_mask, _source in iter_windows(ns, args.windows, torch.device("cpu")):
        target_bytes = clean[byte_mask]
        if target_bytes.numel() == 0:
            continue
        n_masked_total += int(target_bytes.numel())
        floor = majority_floor_bytes(clean, byte_mask)
        accs_all.append(float((target_bytes == floor["maj_byte_all"]).float().mean()))
        accs_vis.append(float((target_bytes == floor["maj_byte_visible"]).float().mean()))
    floors = {
        "acc_majority_all_mean": sum(accs_all) / len(accs_all) if accs_all else None,
        "acc_majority_visible_mean": sum(accs_vis) / len(accs_vis) if accs_vis else None,
        "acc_uniform": 1.0 / 256.0,
        "n_windows": len(accs_all),
        "n_masked_bytes": n_masked_total,
    }
    meta = {"definition": "byte 空间众数字节地板：全窗口径=窗内全部非 PAD 字节取众数；"
                          "可见位口径=窗内未遮蔽字节取众数；预测遮蔽位目标字节",
            "eval_mask_seed": int(getattr(ns, "eval_mask_seed", -1))}
    return floors, meta


# ---------------------------------------------------------------------------
# 仪表⑤ 定向消融双跑
# ---------------------------------------------------------------------------


def run_ablation(runs: list[str], args) -> None:
    k = int(args.k)
    for run in runs:
        prepared = prepare_run(run, "ablation", args)
        if prepared is None:
            continue
        run_dir, run_name, out_dir = prepared
        device = torch.device(args.device)
        model, ns, step, bb, gated = load_run(run_dir, device)
        if not gated:
            skip_summary(out_dir, "backbone.e124_gate=False (非门列): store 剔除探针口径不适用", args, "ablation", run_name)
            continue
        alpha = float(bb.e124_alpha_value().detach())
        set_hard_posture(bb, ns, budget=k)
        # 先行对拍：store_block_override=None 显式传参 vs 不传参，逐位一致才准跑
        parity = _ablation_parity(model, ns, args, device)
        if not parity["ok"]:
            parity["conclusion"] = "FAIL — store_block=None 前向与旧路径不逐位一致，消融双跑中止"
            write_outputs(out_dir, {"instrument": "ablation", "run": run_name, "status": "aborted",
                                    "reason": "store_block None-parity 对拍失败", "parity": parity,
                                    "hardware": hardware_fingerprint(device)}, [])
            print(f"[ablation] {run_name}: PARITY FAIL -> {out_dir}", flush=True)
            continue
        t0 = time.time()
        items: list[dict] = []
        for w, clean, byte_mask, source in iter_windows(ns, args.windows, device):
            with torch.no_grad(), torch.autocast(
                "cuda", dtype=torch.bfloat16, enabled=bool(ns.amp) and device.type == "cuda"
            ):
                out_b, ch, targets, slot, masked_slot = forward_once(
                    model, ns, source, clean, byte_mask, device)
                n_real = int(ch.chunk_mask[0].sum())
                n = int(ch.chunk_mask.shape[1])
                masked_chunks = masked_slot.any(dim=-1)  # (1, n) 遮蔽位→chunk 归属
                sb_global = torch.ones(1, n, n, dtype=torch.bool, device=device)
                sb_dir = masked_chunks.unsqueeze(1).expand(1, n, n).contiguous()
                out_g, ch_g, t_g, s_g, ms_g = forward_once(
                    model, ns, source, clean, byte_mask, device, store_block=sb_global)
                out_d, ch_d, t_d, s_d, ms_d = forward_once(
                    model, ns, source, clean, byte_mask, device, store_block=sb_dir)
            row = {
                "run": run_name, "window": w, "n_bytes": int(clean.numel()), "n_real": n_real,
                "gate_active": bool(k < n_real),
                "n_masked_chunks": int(masked_chunks.sum()),
                "grid_stable": bool((ch.chunk_ids == ch_g.chunk_ids).all()
                                    and (ch.chunk_ids == ch_d.chunk_ids).all()),
                "k_effective": None if bb.last_e124_k is None else float(bb.last_e124_k),
            }
            for tag, (o, t, s, m) in {
                "intact": (out_b, targets, slot, masked_slot),
                "global": (out_g, t_g, s_g, ms_g),
                "directional": (out_d, t_d, s_d, ms_d),
            }.items():
                bs = acc_split(o["logits_backbone"], t, s, m)
                ds = acc_split(o["logits_direct"], t, s, m)
                row[f"backbone_{tag}"] = bs
                row[f"direct_{tag}"] = ds
            for arm in ("global", "directional"):
                for leg in ("backbone", "direct"):
                    for part in ("masked", "unmasked"):
                        a, b = row[f"{leg}_intact"][part], row[f"{leg}_{arm}"][part]
                        row[f"delta_{leg}_{part}_{arm}"] = (
                            None if a is None or b is None else a - b)
            items.append(row)
        summary = {
            "instrument": "ablation", "run": run_name, "ckpt_step": step, "status": "ok",
            "k": k, "windows": args.windows,
            "parity": parity,
            "eval_mask_seed": int(getattr(ns, "eval_mask_seed", -1)),
            "window_seed": int(getattr(ns, "seed", -1)) + 9999,
            "alpha": alpha, "hardware": hardware_fingerprint(device),
            "timing_sec": round(time.time() - t0, 1),
            "aggregate": _agg_ablation(items),
        }
        path = write_outputs(out_dir, summary, items)
        print(f"[ablation] {run_name}: {len(items)} 行 -> {path}", flush=True)


def _ablation_parity(model, ns, args, device) -> dict:
    """store_block=None 显式传参 vs 不传参旧路径：逐位一致（冒烟 ckpt 2 窗起）。
    逐位 = logits L∞ == 0.0 精确零（对拍条款，任务书 ⑤ 先行对拍）。"""
    n_parity = int(args.parity_windows)
    rows = []
    ok = True
    for w, clean, byte_mask, source in iter_windows(ns, n_parity, device):
        with torch.no_grad(), torch.autocast(
            "cuda", dtype=torch.bfloat16, enabled=bool(ns.amp) and device.type == "cuda"
        ):
            out_a = s1.s1_forward(model, source, ns, clean=clean, byte_mask=byte_mask)
            out_b = s1.s1_forward(model, source, ns, clean=clean, byte_mask=byte_mask,
                                  store_block_override=None)
        linf_bb = float((out_a["logits_backbone"].float() - out_b["logits_backbone"].float())
                        .abs().max())
        linf_dir = float((out_a["logits_direct"].float() - out_b["logits_direct"].float())
                         .abs().max())
        rows.append({"window": w, "linf_backbone": linf_bb, "linf_direct": linf_dir})
        ok = ok and linf_bb == 0.0 and linf_dir == 0.0
    return {"ok": ok, "windows": n_parity, "rows": rows,
            "criterion": "logits L∞ == 0.0 (bitwise)"}


def _agg_ablation(items: list[dict]) -> dict:
    agg = {}
    for arm in ("global", "directional"):
        for leg in ("backbone", "direct"):
            for part in ("masked", "unmasked"):
                key = f"delta_{leg}_{part}_{arm}"
                vals = [r[key] for r in items if r.get(key) is not None]
                agg[key] = bootstrap_ci_mean(vals)
    for arm in ("intact", "global", "directional"):
        for leg in ("backbone", "direct"):
            for part in ("masked", "unmasked"):
                vals = [r[f"{leg}_{arm}"][part] for r in items
                        if r[f"{leg}_{arm}"][part] is not None]
                agg[f"{leg}_{arm}_{part}_mean"] = sum(vals) / len(vals) if vals else None
    agg["grid_stable_windows"] = sum(1 for r in items if r["grid_stable"])
    agg["n_windows"] = len(items)
    return agg


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    ap = argparse.ArgumentParser(description="E124 收官五仪表雏形（零训练 eval-only）")
    ap.add_argument("instrument", choices=["rd", "scramble", "posprior", "traj", "ablation", "all"])
    ap.add_argument("--runs", nargs="*", default=DEFAULT_RUNS)
    ap.add_argument("--windows", type=int, default=16)
    ap.add_argument("--budgets", type=str, default=",".join(str(b) for b in DEFAULT_BUDGETS))
    ap.add_argument("--scramble-budgets", type=str,
                    default=",".join(str(b) for b in DEFAULT_SCRAMBLE_BUDGETS))
    ap.add_argument("--k", type=int, default=DEFAULT_K, help="终点预算（仪表③⑤，默认 9）")
    ap.add_argument("--parity-windows", type=int, default=2, help="⑤ 先行对拍窗数")
    ap.add_argument("--out-root", default="outputs/e124_readout_20260913")
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    ap.add_argument("--overwrite", action="store_true")
    args = ap.parse_args()
    args.budgets = [b for b in args.budgets.split(",") if b]
    args.scramble_budgets = [b for b in args.scramble_budgets.split(",") if b]

    suite = {
        "rd": run_rd, "scramble": run_scramble, "posprior": run_posprior,
        "traj": run_traj, "ablation": run_ablation,
    }
    todo = list(suite) if args.instrument == "all" else [args.instrument]
    # 仪表④零 GPU 先行（其余按 ①②③⑤ 序）
    todo.sort(key=lambda x: ["traj", "rd", "scramble", "posprior", "ablation"].index(x))
    for instr in todo:
        suite[instr](args.runs, args)
    print("[e124-readout] done", flush=True)


if __name__ == "__main__":
    main()
