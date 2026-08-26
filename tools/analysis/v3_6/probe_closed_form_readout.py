"""Q19 闭式三段臂（容量墙重审，零训练）探针（任务书 2026-08-27 冻结:
docs/versions/v3.7/FLUED_V3_7_Q19_CLOSED_FORM_READOUT_20260827_CN.md —— 四输入列/
三段管线/三叉判读行/台账格式以它为准）。

管线（全闭式，无梯度无训练动力学；ridge 为闭式代数）：
  段1: 状态行 S_i --ridge 解混(E73 ridge_unmix 同款)--> v̂（写值估计）
  段2: v̂ --ridge 闭式回归(分窗 2-fold, 逐列 RMS 预条件)--> m̂（memory 行估计,
       目标 = 同窗 donor 格冻结模型的真实 memory 行, D6）
  段3: m̂ --冻结生产 decoder direct 口(decoder_in_mem(m̂)+pos→decoder, D1 借口)
       --> logits --> 逐槽 byte_acc（direct 细格, as-encoded 主口径 + clean 视图）

四输入列（每 eval 窗, seed 1042 同 E73/Q16 probe 口径）：
  oracle   : S_or = Σ_{j≤i} k_j v_jᵀ（无衰减无 delta, α 范数匹配沿用 Q17 §1
             条件 2 冻结公式, α 逐窗落盘）；
  natural  : S_nat = KDA 递推原样（_q17_states_dual fp32 参考, padded 恒等步）；
  shuffled : 自然态逐窗行置乱（地板列, 固定种子 generator）；
  cleartext: donor 格真实 memory 行直喂段3（段1/2 恒等, 正对照列, D6 后
             ≡ donor 自锚 = 段3 在岗验证）。

已申报口径偏差（施工审查发现, 任务书文本与名下基座的接口冲突 + 实跑口径校准,
全部显式登记不静默）：
  D1. 任务书 §1 段3 写作 decoder_in_mem(m̂)+pos→decoder（"已知消费 memory 行
      ~0.6–0.7"），但名下基座 v37ks_d_sm_q15_circuit_20k_ctx4096_20260825b
      是 d 格 (k_row_source=state, v_row_source=state)——resolved_config 与
      state_dict 双重核实：无 decoder_in_mem、无 aux_recon，生产 direct 口为
      decoder_in(d_pack=1536 行)。消费 memory 行(512) 的生产 direct 口只存在于
      v=memory 格（a/b）。处理：段3 借用同 ks 家族 b 格 checkpoint
      (v37ks_b_sm_v371_20k_ctx4096_20260817, E68 收官 direct_acc 0.7917) 的
      decoder_in_mem+chunk_pos+decoder 全冻组件。已验证两 ckpt 前端
      (byte_lookup/encoder/segmentor) 位级同源, 逐窗断言 token_mask 位级一致
      （不等则 loud fail）——chunk 划分对齐, 唯一域移 = summarizer memory 行空间。
  D2. 考场窗 = E73/Q16 probe 口径（StreamingReconstructionDataset seed+9999
      前 N 窗 + eval_mask_seed 1042 掩码, 无 burst 拼接）——与 Q15 收官 eval
      （burst_prob=0.5 管束）有已知口径差；基座生产 direct 自锚（read_trained
      →decoder_in, E73 A1 同款）同窗同格复现随行。
  D3. 地板先验：任务书 §2 的 ≈0.03–0.05 源自 echo/cloze 格先验；本考场为
      codec direct 细格, 地板参照 = 同格实测纯先验预测器（网格众数 id 常数
      预测, as-encoded 与 clean 两视图各一）。置乱列贴该实测先验 = 无泄漏；
      显著高于它 = 管线泄漏（判读降级, 同任务书 §2 辅助判读精神）。
  D4. direct 网格 = fine 本段格（row i 还原本段; E73 A0 锚同款 make_targets
      (source, 零掩码) 形态, masked 槽 target=MASK_ID）——因为段3 消费的是
      本段 memory 行估计（细粒度 V 家族, 与 0.79 水位同格）；clean 视图
      （targets 取 clean 字节）与 masked/unmasked 拆分随报。判读三叉的
      0.4/0.1 两线按 acc(as-encoded) 主读数定位, acc_clean 并列随行。
  D5. oracle 态 α 缩放（Q17 §1 条件 2 冻结公式）作用于段1 输入并逐窗落盘;
      段1 逐槽探针与段2 输入特征做逐列 RMS 预条件（标量由训练折/全列 pooled
      特征估计, 闭式无泄漏）——固定 λ 的 ridge 对 α≈0.003 缩比的 oracle 特征
      会变相过正则（λ 有效放大 ~1/α²）, 预条件使各列同尺公平竞争; 段1 cos
      本身尺度不变不受影响。
  D6. 段2 目标与明文列 = donor 格真实 memory 行（同窗同 chunk 划分,
      token_mask 位级一致逐窗断言）。动机（CPU 冒烟实测, 诊断行落盘）:
      基座 d 格 memory 行空间与 donor 正交（逐 chunk cos≈0.01）, 直喂 donor
      段3 贴地（base_mem_passthrough 诊断 ≈ 0.02 档 vs donor 自锚 0.76 档）
      ——任务书"它若低于 0.6 历史水位, 段 3 先查"的明文列纪律在此触发并
      定位到跨格域移; 但两空间内容线性可桥（ridge base→donor memory
      held-out cos ≈0.47, 同落盘）。D6 后明文列 ≡ donor 自锚, 即段3 在岗
      验证（生产水位复现）。
  D7. 基座官方收官 direct（册上 0.2189）属累积 as-encoded 粗格家族
      （coarse V, train_v36_s1.py:2180-2187）, 与本矩阵 fine 细格不同族——
      基座生产 direct 自锚双格同报（fine 格与矩阵同格可比; 累积格与收官
      口径对表, 残余差为 D2 窗口径差）。

判读行（§2 三叉 + 辅助判读）由纯函数 _describe_verdicts 产出描述行, 只描述
不落终判词（终判词归主会话）。

输出: outputs/q19_closed_form_20260827/closed_form_readout.json
      （四列 × 三段全矩阵 + 锚 + 诊断 + 逐窗）+ SUMMARY.txt。

Usage:
  python tools/analysis/v3_6/probe_closed_form_readout.py --device cuda
  CPU 冒烟: py -3.14 -X utf8 tools/analysis/v3_6/probe_closed_form_readout.py --device cpu --max-windows 2
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

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from flued.data import MASK_ID  # noqa: E402
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402
from tools.analysis.v3_6.probe_oracle_write_verdict import (  # noqa: E402
    _front_end,
    build_eval_windows,
    build_masks,
    byte_probe,
    decode_direct,
    load_model,
    read_trained,
    ridge_unmix,
)
from tools.analysis.v3_6.probe_breakpoint_stations import _ridge_2fold_hits  # noqa: E402
from tools.train.v3_6.train_q17_oracle_readout import (  # noqa: E402
    _q17_alpha_scale,
    _q17_states_dual,
)

BASE_RUN = "checkpoints/v37ks_d_sm_q15_circuit_20k_ctx4096_20260825b"
DONOR_RUN = "checkpoints/v37ks_b_sm_v371_20k_ctx4096_20260817"  # 段3 借口 (D1)
OUT_DIR = "outputs/q19_closed_form_20260827"
SHUF_SEED = 20260827  # 置乱列逐窗行置乱 generator 种子（固定顺序）
PROBE_SLOTS = 4  # 段1/段2 逐槽探针槽数（E73 A6 同款 0-3）
SLOT_BINS = 16  # 段3 逐槽 breakdown: 0..15 单槽 + 16+ 尾桶
COLUMNS = ("oracle", "natural", "shuffled", "cleartext")

DECLARED_DEVIATIONS = [
    "D1: 基座 d 格无 decoder_in_mem（v_row_source=state, resolved_config+state_dict 双核实）——"
    "段3 借 v37ks_b_sm_v371_20k_ctx4096_20260817 的 decoder_in_mem+chunk_pos+decoder 全冻组件;"
    "两 ckpt 前端位级同源, 逐窗断言 token_mask 位级一致; 域移仅限 summarizer memory 行空间（D6 定量）。",
    "D2: 考场窗 = E73/Q16 probe 口径（无 burst 拼接）, 与 Q15 收官 eval（burst 0.5 管束）有已知口径差;"
    "基座生产 direct 自锚（read_trained→decoder_in, E73 A1 同款）同窗同格复现随行。",
    "D3: 地板参照 = 同格实测纯先验预测器（众数 id 常数预测）; 任务书 0.03–0.05 为 echo 格先验, 不直接适用本格。",
    "D4: direct 网格 = fine 本段格（E73 A0 同款, masked 槽 target=MASK_ID）+ clean 视图; 0.4/0.1 两线按 acc 主读数定位。",
    "D7: 基座官方收官 direct（册上 0.2189）属累积 as-encoded 粗格家族（coarse V, train_v36_s1.py:2180-2187）,"
    "与本矩阵 fine 细格不同族——基座生产 direct 自锚双格同报（fine 格与矩阵同格可比; 累积格与收官口径对表,"
    "残余差为 D2 窗口径差: burst 0.5 管束 + fla/amp 前向 vs fp32-manual）。",
    "D5: oracle 态 α 缩放（Q17 条件 2 公式）作用于段1 并逐窗落盘; 段1 逐槽探针与段2 输入做逐列 RMS 预条件"
    "（标量来自训练折/ pooled 特征, 闭式无泄漏）——固定 λ 对 α 缩比特征会变相过正则, 预条件使各列同尺竞争。",
    "D6: 段2 目标与明文列 = donor 格真实 memory 行（同窗同 chunk 划分）; 动机实测: 基座 memory 行与 donor 空间"
    "正交（逐 chunk cos≈0.01）且直喂 donor 段3 贴地（base_mem_passthrough 诊断行）, 但内容线性可桥"
    "（ridge base→donor held-out cos 落盘）; D6 后明文列 ≡ donor 自锚 = 段3 在岗验证。",
]


# ---------------------------------------------------------------------------
# 段2: ridge 闭式拟合 v̂→m̂（分窗 2-fold + 逐列 RMS 预条件, 纯张量函数, 测试同用）
# ---------------------------------------------------------------------------


def _rms(x: torch.Tensor) -> torch.Tensor:
    return x.float().pow(2).mean().sqrt().clamp(min=1e-12)


def ridge_fit_predict(xs_by_win: list[torch.Tensor], ys_by_win: list[torch.Tensor], lam: float):
    """分窗 2-fold（偶/奇窗互换）闭式 ridge（带截距项 + RMS 预条件, D5）:
    特征除以训练折 RMS 标量（逐折估计, 无泄漏）, 目标不缩放。每窗的预测由
    对侧折拟合产出。Returns (preds_by_win, Ws)。全部 CPU fp32。
    窗数 <2 时退化为全量拟合（仅冒烟路径会走到, 申报于 docstring）。"""
    n = len(xs_by_win)
    preds: list[torch.Tensor | None] = [None] * n
    ws = []
    for fold in (0, 1):
        tr = [i for i in range(n) if i % 2 != fold]
        te = [i for i in range(n) if i % 2 == fold]
        if not te:
            continue
        if not tr:  # 单窗退化（冒烟）: 全量拟合, 仅非判读路径
            tr = list(range(n))
        X = torch.cat([xs_by_win[i].float().cpu() for i in tr])
        Y = torch.cat([ys_by_win[i].float().cpu() for i in tr])
        scale = _rms(X)
        X = torch.cat([X / scale, torch.ones(X.size(0), 1)], dim=1)
        W = torch.linalg.solve(X.T @ X + lam * torch.eye(X.size(1)), X.T @ Y)
        ws.append({"W": W, "scale": float(scale)})
        for i in te:
            xi = torch.cat([xs_by_win[i].float().cpu() / scale, torch.ones(xs_by_win[i].size(0), 1)], dim=1)
            preds[i] = xi @ W
    return preds, ws


def row_cos(pred: torch.Tensor, target: torch.Tensor) -> float:
    """逐行 cos 均值（fp32）。"""
    return float(F.cosine_similarity(pred.float(), target.float(), dim=-1).mean())


# ---------------------------------------------------------------------------
# 段3: 冻结生产 decoder direct 口 + 网格读数（纯张量函数, 测试同用）
# ---------------------------------------------------------------------------


@torch.no_grad()
def decode_rows_donor(donor, rows: torch.Tensor, token_mask: torch.Tensor) -> torch.Tensor:
    """段3（D1 借口）: decoder_in_mem(rows)+pos → decoder。rows (B, n, d_mem),
    token_mask 取基座 chunks（前端位级同源 + 逐窗断言, D1）。"""
    n = rows.size(1)
    pos = donor.chunk_pos.weight.unsqueeze(0)[:, :n]
    cond = donor.decoder_in_mem(rows) + pos
    return donor.decoder(cond, token_mask[:, :n])


def grid_metrics(logits, targets_enc, slot_mask, targets_clean, masked_slot, slot_bins: int = SLOT_BINS):
    """direct 细格读数: as-encoded 主口径（masked 槽 target=MASK_ID）+ clean
    视图（masked/unmasked 拆分）+ 逐槽（chunk 内 slot）breakdown（hit/cnt 可
    跨窗池化）。输入需同 device。"""
    n = logits.size(1)
    te, sm_, tc, ms = targets_enc[:, :n], slot_mask[:, :n], targets_clean[:, :n], masked_slot[:, :n]
    pred = logits.argmax(dim=-1)
    out = {
        "acc": float(s1._acc_tensor(pred, te, sm_)),
        "ce": float(s1._ce(logits, te, sm_)),
        "acc_clean": float(s1._acc_tensor(pred, tc, sm_)),
        "acc_clean_masked": float(s1._acc_tensor(pred, tc, sm_ & ms)),
        "acc_clean_unmasked": float(s1._acc_tensor(pred, tc, sm_ & ~ms)),
        "n_slots": int(sm_.sum()),
    }
    slots = torch.arange(logits.size(2), device=logits.device).view(1, 1, -1)
    hits_c, hits_e, cnts = [], [], []
    for s in range(slot_bins + 1):
        m = sm_ & (slots == s) if s < slot_bins else sm_ & (slots >= slot_bins)
        hits_c.append(int((pred.eq(tc) & m).sum()))
        hits_e.append(int((pred.eq(te) & m).sum()))
        cnts.append(int(m.sum()))
    out["per_slot_hits_clean"] = hits_c
    out["per_slot_hits_enc"] = hits_e
    out["per_slot_cnt"] = cnts
    return out


def merge_grid_metrics(rows: list[dict]) -> dict:
    """逐窗 grid_metrics 聚合: 标量 = 逐窗均值（E73 同族口径）; 逐槽 = hit/cnt
    池化。ppl = exp(mean ce)。"""
    agg = {
        "acc": round(sum(r["acc"] for r in rows) / len(rows), 4),
        "ce": round(sum(r["ce"] for r in rows) / len(rows), 4),
        "ppl": round(math.exp(min(sum(r["ce"] for r in rows) / len(rows), 20.0)), 3),
        "acc_clean": round(sum(r["acc_clean"] for r in rows) / len(rows), 4),
        "acc_clean_masked": round(sum(r["acc_clean_masked"] for r in rows) / len(rows), 4),
        "acc_clean_unmasked": round(sum(r["acc_clean_unmasked"] for r in rows) / len(rows), 4),
        "n_slots": sum(r["n_slots"] for r in rows),
    }
    cnt = [sum(r["per_slot_cnt"][i] for r in rows) for i in range(SLOT_BINS + 1)]
    agg["per_slot_clean"] = [
        round(sum(r["per_slot_hits_clean"][i] for r in rows) / c, 4) if c else None for i, c in enumerate(cnt)
    ]
    agg["per_slot_enc"] = [
        round(sum(r["per_slot_hits_enc"][i] for r in rows) / c, 4) if c else None for i, c in enumerate(cnt)
    ]
    agg["per_slot_cnt"] = cnt
    return agg


def prior_acc(targets: torch.Tensor, slot_mask: torch.Tensor):
    """纯先验预测器（D3 地板参照）: 网格众数 id 常数预测的 acc。Returns
    (acc, majority_id)。"""
    ids = targets[slot_mask].long().clamp(0, 257)
    maj = int(torch.bincount(ids, minlength=258).argmax())
    return float((ids == maj).float().mean()), maj


# ---------------------------------------------------------------------------
# 段1/段2 逐槽探针台账（E73 byte_probe / Q16 real−garbage 同族）
# ---------------------------------------------------------------------------


def stage1_probe(vhat_rows: torch.Tensor, ys: torch.Tensor, y_valid: torch.Tensor):
    """段1 后逐槽恢复率: one-vs-all ridge v̂→slot byte id（E73 byte_probe 同款,
    2-fold 样本分半, 报 acc vs majority）; 输入先做 pooled RMS 预条件（D5,
    探针只读方向内容, cos/方向尺度不变）。"""
    return byte_probe(vhat_rows / _rms(vhat_rows), ys, y_valid)


def stage2_probe(mhat_rows: torch.Tensor, ys: torch.Tensor, y_valid: torch.Tensor, lam: float = 1e-2):
    """段2 后逐槽 real−garbage 探针增量（Q16 _ridge_2fold_hits 同族: 偶奇折
    + 固定种子标签置换 garbage + majority 基线; 指标 = real−garbage）。"""
    out = {}
    for s in range(ys.size(1)):
        m = y_valid[:, s]
        n = int(m.sum())
        if n < 40:
            continue
        got = _ridge_2fold_hits(mhat_rows[m], ys[m][:, s], lam=lam)
        if got is None:
            continue
        hr, hg, hm = got
        r, g, mj = float(hr.float().mean()), float(hg.float().mean()), float(hm.float().mean())
        out[str(s)] = {
            "real": round(r, 4),
            "garbage": round(g, 4),
            "majority": round(mj, 4),
            "delta": round(r - g, 4),
            "n": n,
        }
    return out


# ---------------------------------------------------------------------------
# 判读行（纯函数, 只描述不落终判词 —— 终判词归主会话）
# ---------------------------------------------------------------------------


def _pos_line(acc: float) -> str:
    if acc >= 0.4:
        return f"{acc:.4f} ≥ 0.4 线"
    if acc <= 0.1:
        return f"{acc:.4f} 落 ~0.1 档（≤0.1）"
    return f"{acc:.4f} 落 0.1–0.4 之间"


def _describe_verdicts(matrix: dict, anchors: dict) -> list[str]:
    """§2 三叉 + 辅助判读的描述行（不落终判词）。matrix[col]['stage3'] 为
    merge_grid_metrics 聚合行。"""
    lines = ["判读行（描述性, 终判词归主会话; 0.4/0.1 两线按 acc 主读数, clean 视图随行）:"]
    or3, na3 = matrix["oracle"]["stage3"], matrix["natural"]["stage3"]
    sh3, cl3 = matrix["shuffled"]["stage3"], matrix["cleartext"]["stage3"]
    lines.append(
        f"  ① oracle 端到端相对 0.4/0.1 两线: acc {_pos_line(or3['acc'])}; "
        f"clean 视图 {_pos_line(or3['acc_clean'])}"
    )
    lines.append(
        f"  ② oracle vs 自然落差: acc {or3['acc']:.4f} vs {na3['acc']:.4f} "
        f"(Δ={or3['acc'] - na3['acc']:+.4f}); clean {or3['acc_clean']:.4f} vs {na3['acc_clean']:.4f}"
    )
    pr_e, pr_c = anchors["prior"]["acc_enc"], anchors["prior"]["acc_clean"]
    lines.append(
        f"  ③ 置乱地板列 vs 同格实测先验（D3）: acc {sh3['acc']:.4f} vs 先验 {pr_e:.4f} "
        f"(差 {sh3['acc'] - pr_e:+.4f}); clean {sh3['acc_clean']:.4f} vs 先验 {pr_c:.4f} "
        f"——任务书 0.03–0.05 为 echo 格先验, 本格以实测先验为准; 显著高于先验 = 管线泄漏"
    )
    lines.append(
        f"  ④ 明文列（D6 后 ≡ donor 自锚 = 段3 在岗验证）vs decoder_in_mem 历史水位: "
        f"acc {cl3['acc']:.4f} / clean {cl3['acc_clean']:.4f}（册上 E68 收官 0.7917; "
        f"任务书 0.6–0.7 历史水位属 decoder_in_mem 格）; 基座 memory 行直喂变体（域移读数）: "
        f"acc {anchors['base_mem_passthrough']['acc']:.4f} ——明文列在水位 = 段3 无虞; "
        f"直喂变体贴地 = 跨格域移实锤（D6 动机）"
    )
    return lines


# ---------------------------------------------------------------------------
# 逐窗采集（第一遍: 前端×2 + 态 + 段1 + 网格 + 锚 + 域移诊断）
# ---------------------------------------------------------------------------


@torch.no_grad()
def collect_window(base, donor, ns, clean, byte_mask, lam_unmix, device, wi):
    source = clean.masked_fill(byte_mask, MASK_ID)
    chunks, memory, _index = _front_end(base, source)
    n_real = int(chunks.chunk_mask[0].sum())
    gates = base.write_head(memory)  # V 通道 gates（d 格）
    sm = base.state_machine

    S_nat_full, S_or_full = _q17_states_dual(gates, chunks.chunk_mask)
    S_or_scaled, alpha = _q17_alpha_scale(S_nat_full, S_or_full, chunks.chunk_mask)
    S_nat = S_nat_full[:, :n_real]
    S_or = S_or_scaled[:, :n_real]
    gen = torch.Generator().manual_seed(SHUF_SEED + wi)
    perm = torch.randperm(n_real, generator=gen).to(device)
    S_shuf = S_nat[:, perm]

    vh_or, cos_or = ridge_unmix(gates, S_or, lam_unmix)
    vh_nat, cos_nat = ridge_unmix(gates, S_nat, lam_unmix)
    vh_shuf, cos_shuf = ridge_unmix(gates, S_shuf, lam_unmix)

    m_base = memory[:, :n_real].float()  # (1, n, 512) 基座真实 memory 行（域移诊断用）

    # donor 前端（D6: 段2 目标/明文列 = donor 格真实 memory 行）
    d_chunks, d_memory, _di = _front_end(donor, source)
    d_n = int(d_chunks.chunk_mask[0].sum())
    if not torch.equal(chunks.token_mask, d_chunks.token_mask):
        raise ValueError(f"window {wi}: base/donor token_mask 不一致——D1 前端同源假设破裂, loud fail")
    m_donor = d_memory[:, :d_n].float()

    # direct 网格（D4: fine 本段格, E73 A0 同款形态 + clean 视图）
    zeros = torch.zeros_like(byte_mask)
    targets_enc, slot_mask, _m = s1.make_targets(
        source, zeros, chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
    )
    targets_clean, _sm2, masked_slot = s1.make_targets(
        clean, byte_mask, chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
    )
    # 逐槽探针目标（E73 A6 同款: clean 字节, slots 0-3）
    base_targets, base_slot, _bm = s1.make_targets(
        clean, zeros, chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
    )
    ys = base_targets[0, :n_real, :PROBE_SLOTS].cpu()
    y_valid = base_slot[0, :n_real, :PROBE_SLOTS].cpu()

    # 锚甲: 基座生产 direct 复现（E73 A1 同款: trained 态+trained 读出→decoder_in）
    v_rows = read_trained(sm, S_nat)
    logits_base = decode_direct(base, v_rows, chunks)
    anchor_base = grid_metrics(logits_base, targets_enc, slot_mask, targets_clean, masked_slot)
    # 锚甲补格（D7）: 官方收官 direct 口径 = 累积 as-encoded 粗格（coarse V,
    # train_v36_s1.py:2180-2187）——同窗同前向补一记, 与册上 0.2189 对表
    cum_targets, cum_slot, _cm, _tr = s1.make_cumulative_retention_targets(
        source, byte_mask, chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
    )
    nb_ = logits_base.size(1)
    anchor_base_cum = {
        "acc": float(s1._acc_tensor(logits_base.argmax(dim=-1), cum_targets[:, :nb_], cum_slot[:, :nb_])),
        "ce": float(s1._ce(logits_base, cum_targets[:, :nb_], cum_slot[:, :nb_])),
    }

    # 域移诊断（D6 动机落盘）: 基座 memory 行直喂 donor 段3（贴地预期）
    logits_pass = decode_rows_donor(donor, m_base, chunks.token_mask)
    base_pass = grid_metrics(logits_pass, targets_enc, slot_mask, targets_clean, masked_slot)
    cos_bd = row_cos(m_base[0], m_donor[0])  # 逐 chunk 空间夹角（≈0 = 正交）

    rec = {
        "window": wi,
        "n_real": n_real,
        "alpha": float(alpha.mean()),
        "cos": {"oracle": round(cos_or, 4), "natural": round(cos_nat, 4), "shuffled": round(cos_shuf, 4)},
        "anchor_base": anchor_base,
        "anchor_base_cum": anchor_base_cum,
        "base_mem_passthrough": base_pass,
        "cos_base_donor_mem": round(cos_bd, 4),
        "vh": {
            "oracle": vh_or[0].float().cpu(),
            "natural": vh_nat[0].float().cpu(),
            "shuffled": vh_shuf[0].float().cpu(),
        },
        "m_donor": m_donor[0].cpu(),
        "m_base": m_base[0].cpu(),
        "token_mask": chunks.token_mask[:, :n_real].clone(),
        "targets_enc": targets_enc.cpu(),
        "slot_mask": slot_mask.cpu(),
        "targets_clean": targets_clean.cpu(),
        "masked_slot": masked_slot.cpu(),
        "ys": ys,
        "y_valid": y_valid,
        "xs_v": gates["v"][0, :n_real].float().reshape(n_real, -1).cpu(),  # A6 诊断
    }
    return rec


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    p = argparse.ArgumentParser()
    p.add_argument("--base-run-dir", default=BASE_RUN)
    p.add_argument("--donor-run-dir", default=DONOR_RUN)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--max-windows", type=int, default=16, help="eval 窗数（16 = 训练终评协议）")
    p.add_argument("--lam-unmix", type=float, default=1e-2, help="段1 ridge 解混 λ（E73 扫档中值固定）")
    p.add_argument("--lam-stage2", type=float, default=1.0, help="段2 ridge v̂→m̂ λ（RMS 预条件后, D5）")
    p.add_argument("--out-dir", default=OUT_DIR)
    args = p.parse_args()
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    base, ns, base_step = load_model(Path(args.base_run_dir), device)
    donor, dns, donor_step = load_model(Path(args.donor_run_dir), device)
    # D1 接口断言（loud, 不静默）: donor 必须有 decoder_in_mem 且 v=memory
    if getattr(dns, "v_row_source", "") != "memory" or not hasattr(donor, "decoder_in_mem"):
        raise ValueError(f"{args.donor_run_dir}: donor 缺 decoder_in_mem（v_row_source={getattr(dns, 'v_row_source', None)!r}）")
    if getattr(ns, "v_row_source", "") != "state":
        raise ValueError(f"{args.base_run_dir}: 预期 d 格 v_row_source='state', got {ns.v_row_source!r}")
    for k in ("max_chunks", "max_span"):
        if getattr(ns, k) != getattr(dns, k):
            raise ValueError(f"base/donor {k} 不一致: {getattr(ns, k)} vs {getattr(dns, k)}")
    print(f"[q19] base={Path(args.base_run_dir).name} step={base_step} | donor={Path(args.donor_run_dir).name} step={donor_step}", flush=True)

    windows = build_eval_windows(ns, args.max_windows)
    masks = build_masks(windows, ns)
    print(f"[q19] {len(windows)} eval 窗 + 掩码就位（{time.time() - t0:.0f}s）", flush=True)

    recs = []
    for wi, (clean, byte_mask) in enumerate(zip(windows, masks)):
        rec = collect_window(base, donor, ns, clean.to(device), byte_mask.to(device), args.lam_unmix, device, wi)
        recs.append(rec)
        print(
            f"[q19] window {wi} n_real={rec['n_real']} α={rec['alpha']:.4f} "
            f"cos or/nat/shuf={rec['cos']['oracle']:.3f}/{rec['cos']['natural']:.3f}/{rec['cos']['shuffled']:.3f} "
            f"锚: base_acc={rec['anchor_base']['acc']:.3f} pass={rec['base_mem_passthrough']['acc']:.3f} "
            f"cos(m_b,m_d)={rec['cos_base_donor_mem']:.3f}（{time.time() - t0:.0f}s）",
            flush=True,
        )

    n_win = len(recs)
    m_by_win = [r["m_donor"] for r in recs]  # D6: 段2 目标 = donor 格真实 memory 行

    # 段2: 逐列分窗 2-fold ridge v̂→m̂（闭式 + RMS 预条件, D5）; 明文列恒等
    # （m̂ = donor 真 memory 行, D6 后 ≡ donor 自锚）
    mhat: dict[str, list[torch.Tensor]] = {}
    cos_mhat: dict[str, float] = {}
    stage2_fits: dict[str, list] = {}
    for col in ("oracle", "natural", "shuffled"):
        preds, ws = ridge_fit_predict([r["vh"][col] for r in recs], m_by_win, args.lam_stage2)
        mhat[col] = preds
        stage2_fits[col] = [{"scale": w_["scale"]} for w_ in ws]
        cos_mhat[col] = round(
            sum(row_cos(preds[i], m_by_win[i]) for i in range(n_win)) / n_win, 4
        )
    mhat["cleartext"] = m_by_win
    cos_mhat["cleartext"] = 1.0

    # 域移诊断（D6 动机落盘）: ridge base→donor memory 行 held-out cos（同
    # 段2 分窗 2-fold 纪律）
    bridge_preds, _bw = ridge_fit_predict([r["m_base"] for r in recs], m_by_win, args.lam_stage2)
    bridge_cos = round(sum(row_cos(bridge_preds[i], m_by_win[i]) for i in range(n_win)) / n_win, 4)

    # 段1/段2 逐槽探针台账（全窗池化; 段2 探针只探 held-out 预测行——每窗皆 held-out）
    ys_all = torch.cat([r["ys"] for r in recs])
    yv_all = torch.cat([r["y_valid"] for r in recs])
    stage1_ledger, stage2_ledger = {}, {}
    for col in ("oracle", "natural", "shuffled"):
        xs = torch.cat([r["vh"][col] for r in recs])
        stage1_ledger[col] = {
            "cos": round(sum(r["cos"][col] for r in recs) / n_win, 4),
            "byte_probe": stage1_probe(xs, ys_all, yv_all),
        }
        stage2_ledger[col] = {
            "cos_mhat": cos_mhat[col],
            "probe": stage2_probe(torch.cat(mhat[col]), ys_all, yv_all),
        }
    stage1_ledger["cleartext"] = "identity（明文列直喂段3, 段1 不过）"
    stage2_ledger["cleartext"] = "identity（明文列直喂段3, 段2 不过）"

    # A6 同族诊断（列无关参照行）: 写真值 v / memory 行 → slot byte id
    diag_v = byte_probe(torch.cat([r["xs_v"] for r in recs]), ys_all, yv_all)
    diag_m_base = byte_probe(torch.cat([r["m_base"] for r in recs]), ys_all, yv_all)
    diag_m_donor = byte_probe(torch.cat(m_by_win), ys_all, yv_all)

    # 段3: 逐窗逐列冻结 donor direct 口 + 网格读数
    stage3_ledger: dict[str, list[dict]] = {c: [] for c in COLUMNS}
    for wi, rec in enumerate(recs):
        tm = rec["token_mask"]
        te, sm_ = rec["targets_enc"].to(device), rec["slot_mask"].to(device)
        tc, ms = rec["targets_clean"].to(device), rec["masked_slot"].to(device)
        for col in COLUMNS:
            rows = mhat[col][wi].unsqueeze(0).to(device)
            logits = decode_rows_donor(donor, rows, tm)
            stage3_ledger[col].append(grid_metrics(logits, te, sm_, tc, ms))
        print(f"[q19] 段3 window {wi} 完成（{time.time() - t0:.0f}s）", flush=True)

    matrix = {
        col: {
            "stage1": stage1_ledger[col],
            "stage2": stage2_ledger[col],
            "stage3": merge_grid_metrics(stage3_ledger[col]),
        }
        for col in COLUMNS
    }

    # 锚与先验
    anchors = {
        "base_direct_repro": merge_grid_metrics([r["anchor_base"] for r in recs]),
        "base_direct_repro_cumgrid": {
            "acc": round(sum(r["anchor_base_cum"]["acc"] for r in recs) / n_win, 4),
            "ce": round(sum(r["anchor_base_cum"]["ce"] for r in recs) / n_win, 4),
        },
        "base_mem_passthrough": merge_grid_metrics([r["base_mem_passthrough"] for r in recs]),
    }
    te_all = torch.cat([r["targets_enc"] for r in recs])
    tc_all = torch.cat([r["targets_clean"] for r in recs])
    sm_all = torch.cat([r["slot_mask"] for r in recs])
    pr_e, maj_e = prior_acc(te_all, sm_all)
    pr_c, maj_c = prior_acc(tc_all, sm_all)
    anchors["prior"] = {
        "acc_enc": round(pr_e, 4),
        "acc_clean": round(pr_c, 4),
        "majority_id_enc": maj_e,
        "majority_id_clean": maj_c,
    }

    verdict_lines = _describe_verdicts(matrix, anchors)

    report = {
        "probe": "Q19 闭式三段臂（容量墙重审, 零训练）",
        "spec": "docs/versions/v3.7/FLUED_V3_7_Q19_CLOSED_FORM_READOUT_20260827_CN.md",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "checkpoints": {
            "base": {"run": Path(args.base_run_dir).name, "step": base_step},
            "donor_stage3": {"run": Path(args.donor_run_dir).name, "step": donor_step},
        },
        "declared_deviations": DECLARED_DEVIATIONS,
        "params": {
            "windows": n_win,
            "lam_unmix": args.lam_unmix,
            "lam_stage2": args.lam_stage2,
            "eval_mask_seed": ns.eval_mask_seed,
            "shuffle_seed": SHUF_SEED,
            "probe_slots": PROBE_SLOTS,
            "slot_bins": SLOT_BINS,
            "stage2_fit_scales": stage2_fits,
        },
        "matrix": matrix,
        "anchors": anchors,
        "diagnostics": {
            "byte_probe_from_v": diag_v,
            "byte_probe_from_m_base": diag_m_base,
            "byte_probe_from_m_donor": diag_m_donor,
            "bridge_cos_base_to_donor_mem": bridge_cos,
            "cos_base_donor_mem_per_window": [r["cos_base_donor_mem"] for r in recs],
            "alpha_per_window": [round(r["alpha"], 6) for r in recs],
            "cos_per_window": [r["cos"] for r in recs],
        },
        "verdict_lines": verdict_lines,
        "per_window": [
            {
                "window": r["window"],
                "n_real": r["n_real"],
                "alpha": round(r["alpha"], 6),
                "cos": r["cos"],
                "anchor_base_acc": round(r["anchor_base"]["acc"], 4),
                "anchor_base_cumgrid_acc": round(r["anchor_base_cum"]["acc"], 4),
                "base_mem_passthrough_acc": round(r["base_mem_passthrough"]["acc"], 4),
                "stage3": {col: {k: v for k, v in stage3_ledger[col][wi].items() if not k.startswith("per_slot")} for col in COLUMNS},
            }
            for wi, r in enumerate(recs)
        ],
        "timing_sec": round(time.time() - t0, 1),
    }
    out_path = out_dir / "closed_form_readout.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    # SUMMARY: 四列 × 三段全矩阵 + 锚 + 判读行 + 申报
    lines = [
        "Q19 闭式三段臂（容量墙重审, 零训练）——四输入列 × 三段损耗台账全矩阵",
        f"日期 {report['created']}  设备 {device.type}  窗口 {n_win}  口径 fp32-manual",
        f"基座 {Path(args.base_run_dir).name} (step {base_step}) | 段3 借口 {Path(args.donor_run_dir).name} (step {donor_step})",
        f"λ_unmix={args.lam_unmix} λ_stage2={args.lam_stage2} | 网格: fine 本段 direct 格（D4, as-encoded 主口径 + clean 视图）",
        "",
        "已申报口径偏差（不静默）:",
        *[f"  {d}" for d in DECLARED_DEVIATIONS],
        "",
        "锚行与域移诊断（不在 4×3 矩阵内）:",
        f"  基座生产 direct 复现（E73 A1 同款, D2/D7 双格同报）: fine 格 acc={anchors['base_direct_repro']['acc']:.4f} "
        f"ppl={anchors['base_direct_repro']['ppl']} clean={anchors['base_direct_repro']['acc_clean']:.4f} | "
        f"累积粗格 acc={anchors['base_direct_repro_cumgrid']['acc']:.4f} ce={anchors['base_direct_repro_cumgrid']['ce']:.4f} "
        f"（册上收官 eval_direct_acc 0.2189 属累积粗格家族, 残余差 = D2 窗口径差）",
        f"  基座 memory 行直喂 donor 段3（D6 域移读数）: acc={anchors['base_mem_passthrough']['acc']:.4f} "
        f"clean={anchors['base_mem_passthrough']['acc_clean']:.4f}（贴地 = 跨格域移实锤）",
        f"  ridge 桥 base→donor memory 行 held-out cos={bridge_cos}（内容线性可桥）; "
        f"逐 chunk 空间 cos 均值={sum(r['cos_base_donor_mem'] for r in recs) / n_win:.4f}（≈0 = 空间正交）",
        f"  纯先验预测器（D3 地板参照）: acc_enc={anchors['prior']['acc_enc']:.4f} (众数 id {anchors['prior']['majority_id_enc']}) "
        f"acc_clean={anchors['prior']['acc_clean']:.4f} (众数 id {anchors['prior']['majority_id_clean']})",
        "",
        "四列 × 三段全矩阵:",
    ]
    for col in COLUMNS:
        mrow = matrix[col]
        lines.append(f"== 列: {col} ==")
        if col == "cleartext":
            lines.append("  段1: identity（直喂段3） | 段2: identity（直喂段3）")
        else:
            s1row, s2row = mrow["stage1"], mrow["stage2"]
            bp = " ".join(
                f"s{s}={v['acc']:.3f}/maj{v['majority']:.3f}" for s, v in sorted(s1row["byte_probe"].items(), key=lambda kv: int(kv[0]))
            )
            lines.append(f"  段1: cos(v̂,v)={s1row['cos']:.4f} | 逐槽恢复率(acc/majority): {bp}")
            pb = " ".join(
                f"s{s}=Δ{v['delta']:+.3f}(r{v['real']:.3f}/g{v['garbage']:.3f}/m{v['majority']:.3f})"
                for s, v in sorted(s2row["probe"].items(), key=lambda kv: int(kv[0]))
            )
            lines.append(f"  段2: cos(m̂,m)={s2row['cos_mhat']:.4f} | 逐槽 real−garbage: {pb}")
        s3row = mrow["stage3"]
        lines.append(
            f"  段3: acc={s3row['acc']:.4f} ppl={s3row['ppl']} | clean={s3row['acc_clean']:.4f} "
            f"(masked {s3row['acc_clean_masked']:.4f} / unmasked {s3row['acc_clean_unmasked']:.4f}) n_slots={s3row['n_slots']}"
        )
        pc = " ".join(f"s{i}={a}" for i, a in enumerate(s3row["per_slot_clean"]) if a is not None)
        lines.append(f"       逐槽 clean acc: {pc}")
    lines += [
        "",
        "诊断行（A6 同族, 列无关参照）:",
        f"  byte_probe from v（写值真值）: {json.dumps(diag_v, ensure_ascii=False)}",
        f"  byte_probe from m_base（基座 memory 行真值）: {json.dumps(diag_m_base, ensure_ascii=False)}",
        f"  byte_probe from m_donor（donor memory 行真值, 段3 面上限对照）: {json.dumps(diag_m_donor, ensure_ascii=False)}",
        f"  α（逐窗范数匹配系数）: {report['diagnostics']['alpha_per_window']}",
        "",
        *verdict_lines,
        "",
        f"完整数据: {out_path}",
    ]
    summary_path = out_dir / "SUMMARY.txt"
    summary_path.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
