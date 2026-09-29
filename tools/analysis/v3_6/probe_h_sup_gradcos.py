"""H-sup 候选假设零训练测量臂：direct vs completion 两 codec 损失在写入侧的梯度余弦。

假设（候选，登记口径）：codec 保真梯度把写入侧锁死在毒性盆地——direct（decoder 从
raw V rows 还原 as-encoded 字节流，含 MASK 位）与 completion（decoder(backbone_out+pos)
还原干净文本）两股梯度在共享写入侧参数（encoder/summarizer/KDA 状态机写侧/
readout_query）上汇合（flued/v36/model.py `_forward_slm` 全程 attached 无 detach），
若两股梯度持续互相拉扯（负余弦），写入侧被锁死在「逐字节保真但抗消费」的形态。

测量对象：checkpoints/v37ks_d_sm_q15_circuit_20k_ctx4096_20260825b（d 格 Q15 收官
正臂）的 latest.pt + 同目录 resolved_config.json。坑 8 对偶纪律：模型实例化严格按
resolved_config（Namespace(**cfg) 直建，不经 parser 现行默认值），加载做全键全形
双向校验，不齐 loud fail，禁止静默跳过（audit_payload_full_key_shape）。

损失口径（逐位复用训练器机器，禁止重写实现）：s1_forward（autocast bf16 内 forward，
与 step_model 同调用形态）→ d 格（v_row_source=state）目标网格分形——direct 目标 =
make_cumulative_retention_targets(source, byte_mask, ...)（as-encoded，含 MASK_ID），
completion 目标 = _completion_target_grids(..., cumulative=True)（干净文本），CE 走
train_v36._ce 原函数。Q15 过程奖励三件套（L_attend/sg(g)/L_couple）是 train-only
附加件，本探针**只跑标准 direct/completion 两损失**（在 q15 训出的权重上测标准
codec 损失）；burst/cloze/retrieval 数据臂同关（prob=0）——测的是标准 codec 损失面
在基座权重点的梯度几何。skip_hard 是 legacy v0.4 线（flued/model.py）概念，v36 主线
无此旋钮，N/A。

梯度口径：照训练器实际精度路径——fp32 主权重、autocast bf16 前向（amp 照
resolved_config）、kda_impl 照基座（fla，CUDA）；每窗两次 torch.autograd.grad
（direct_loss / completion_loss，retain_graph=True），返回即 fp32 主权重梯度。
余弦在 float64 下计算（测量精度，不进图）。

窗流/掩码流 = evaluate() 纪律：StreamingReconstructionDataset(seed+9999) 顺序窗，
_MASK_GENERATOR 一次播种 eval_mask_seed 后逐窗顺序消费（build_eval_windows /
build_masks 原样复用 probe_oracle_write_verdict 的实现）。

参数组（前缀匹配，空组响亮报错）：
  ① summarizer          summarizer.* 全体（DiT 共享干 + qpool 查询 + 双头；判读组）
     summarizer_shared  summarizer.blocks.* + summarizer.pool_queries（双头共享段，诊断）
     summarizer_head_v  summarizer.ffn.*（memory/V 头，双路径；诊断）
     summarizer_head_k  summarizer.index_ffn.*（index/K 头，completion-only，direct N/A）
  ② kda_write_v         write_head.*（V 通道 KDA 写侧：trunk/to_k/to_v/to_beta/
                        alpha_logit = k/v 投影+门控；判读组）
     kda_write_k        write_head_k.*（K 通道写侧；completion-only，direct N/A）
  ③ readout_query_v     state_machine.readout_query（V 通道读出查询；判读组）
     readout_query_k    state_machine_k.readout_query（K 通道；completion-only）
  ④ encoder_blocks      encoder_blocks.*（对照；本臂训练时前端冻结——读数为开梯度
                        的反事实几何，非训练中真实流过的梯度，SUMMARY 注记）
  ⑤ decoder             decoder.*（两损失共享，次级读出）
  ⑥ byte_lookup         byte_lookup.*（tied 字节表，对照；冻结注记同④）
  ⑦ backbone            backbone.*（结构对照：direct 路径不经 backbone，期望
                        direct 零梯度 → N/A 行，验证图接线）

d 格拓扑注记：K 通道（write_head_k/state_machine_k/index_ffn）只喂 backbone store，
不经 direct 腿——这些组 direct 梯度结构性为零，报 N/A 不报错（allow_unused）。
判读三组（①②③）取双路径组：summarizer / kda_write_v / readout_query_v。
未测件（不在任务六组内）：state_machine{,_k}.realign、decoder_in、chunk_pos、
bridge、segmentor_*、chunk_builder（无参数）。

判读尺（预注册，不许事后挪）：
  - 写入侧三组 mean 余弦持续为负且 CI95 排零 = 拉扯实锤（H-sup 升级为已验证）；
  - 围绕零对称震荡、CI 含零 = 正交（容量够，拉扯不立，H-sup 证伪）；
  - 持续正余弦 = 两目标同向（H-sup 证伪且写入侧无辜加深）；
  - 对照组（④⑤⑥）读数用于排除「全模型处处拉扯」的平庸解释。

聚合输出：每组 cosine 的 mean / CI95（bootstrap 2000）/ 负余弦占比 / 两损失幅度
量级（损失值 + 各组梯度范数），逐窗明细（含逐层余弦）落 JSONL。

Usage:
  python tools/analysis/v3_6/probe_h_sup_gradcos.py --device cuda --n-windows 512
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from argparse import Namespace
from pathlib import Path

import numpy as np
import torch

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from flued.data import MASK_ID, PAD_ID  # noqa: E402
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402
from tools.train.v3_3.train_v33 import make_targets  # noqa: E402
from tools.train.v3_6.train_v36 import _ce, build_model  # noqa: E402
from tools.analysis.v3_6.probe_oracle_write_verdict import (  # noqa: E402
    build_eval_windows,
    build_masks,
)

# 参数组名 -> 前缀元组（named_parameters startswith 匹配；空组响亮报错）
GROUP_PREFIXES: dict[str, tuple[str, ...]] = {
    "summarizer": ("summarizer.",),
    "summarizer_shared": ("summarizer.blocks.", "summarizer.pool_queries"),
    "summarizer_head_v": ("summarizer.ffn.",),
    "summarizer_head_k": ("summarizer.index_ffn.",),
    "kda_write_v": ("write_head.",),
    "kda_write_k": ("write_head_k.",),
    "readout_query_v": ("state_machine.readout_query",),
    "readout_query_k": ("state_machine_k.readout_query",),
    "encoder_blocks": ("encoder_blocks.",),
    "decoder": ("decoder.",),
    "byte_lookup": ("byte_lookup.",),
    "backbone": ("backbone.",),
}

# 判读三组：双路径写入侧（K 通道组/direct-不经组只作诊断与结构对照，不进判读）
JUDGMENT_GROUPS: tuple[str, ...] = ("summarizer", "kda_write_v", "readout_query_v")

BOOT_SEED = 20260930  # bootstrap 抽签种子（落盘可复演）

GROUP_LEGEND = {
    "summarizer": "① summarizer 全体（双头+共享干；判读组）",
    "summarizer_shared": "summarizer 共享段（DiT blocks+qpool 查询；诊断）",
    "summarizer_head_v": "summarizer memory/V 头（双路径；诊断）",
    "summarizer_head_k": "summarizer index/K 头（completion-only，direct N/A）",
    "kda_write_v": "② V 通道 KDA 写侧 write_head（k/v 投影+门控；判读组）",
    "kda_write_k": "K 通道写侧 write_head_k（completion-only，direct N/A）",
    "readout_query_v": "③ V 通道 state_machine.readout_query（判读组）",
    "readout_query_k": "K 通道 state_machine_k.readout_query（completion-only，direct N/A）",
    "encoder_blocks": "④ encoder blocks（对照；训练时冻结，反事实几何）",
    "decoder": "⑤ decoder（两损失共享，次级读出）",
    "byte_lookup": "⑥ tied 字节表（对照；训练时冻结，反事实几何）",
    "backbone": "⑦ backbone（结构对照：direct 不经此，期望 N/A）",
}


# ---------------------------------------------------------------------------
# 基座装载（坑 8 对偶纪律：严格 resolved_config 实例化 + 全键全形双向校验）
# ---------------------------------------------------------------------------


def audit_payload_full_key_shape(model: torch.nn.Module, sd: dict, ckpt_dir: Path) -> None:
    """全键全形双向校验（去噪/Q20/E120 臂 loud-fail 先例同款）：模型侧一键
    缺失/形不符或 ckpt 侧一键冗余即 SystemExit，禁止静默跳过。"""
    cur = model.state_dict()
    bad = [k for k in cur if k not in sd or sd[k].shape != cur[k].shape]
    extra = [k for k in sd if k not in cur]
    if bad or extra:
        raise SystemExit(
            f"[h_sup] 基座全键全形校验失败: {len(bad)} 键缺失/形不符 + {len(extra)} 冗键 "
            f"(如 {(bad + extra)[:5]}) —— {ckpt_dir} 的 latest.pt 与 resolved_config 架构漂移, "
            "禁止静默跳过（坑 8 对偶纪律）"
        )


def load_base_model(ckpt_dir: Path, device: torch.device, kda_impl: str = ""):
    """严格按 resolved_config 实例化（Namespace 直建，不经 parser 现行默认值），
    strict 装载 + 全键全形双向校验。测量姿态：全参数 requires_grad_(True) ——
    本臂训练时前端（byte_lookup/encoder/segmentor）冻结，④⑥两组读数因此是
    开梯度的反事实几何（SUMMARY 注记）；写入侧各组训练中本就在链上。"""
    cfg = json.loads((ckpt_dir / "resolved_config.json").read_text(encoding="utf-8"))
    cfg["data_manifest"] = ""
    if device.type != "cuda":
        cfg["kda_impl"] = "torch"  # fla kernels GPU-only（非 CUDA 设备覆写, 主会话先例）
    elif kda_impl:
        cfg["kda_impl"] = kda_impl
    ns = Namespace(**cfg)
    # 探针姿态：标准 codec 两损失，任务数据臂全关（口径注记进 SUMMARY）
    ns.burst_prob = 0.0
    ns.q15_circuit_rearing = False
    ns.cloze_prob = 0.0
    ns.retrieval_prob = 0.0
    model = build_model(ns).to(device)
    payload = torch.load(ckpt_dir / "latest.pt", map_location=device, weights_only=False)
    audit_payload_full_key_shape(model, payload["model"], ckpt_dir)
    model.load_state_dict(payload["model"], strict=True)
    for p in model.parameters():
        p.requires_grad_(True)
    model._front_end_frozen_reset()  # C8 缓存失效——否则 _encode 按训练冻结面走 no_grad
    model.eval()
    return model, ns, int(payload.get("step", 0)), cfg


# ---------------------------------------------------------------------------
# 参数组 / 余弦 / 逐窗测量
# ---------------------------------------------------------------------------


def build_param_groups(model: torch.nn.Module) -> dict[str, list[tuple[str, torch.nn.Parameter]]]:
    named = list(model.named_parameters())
    groups: dict[str, list[tuple[str, torch.nn.Parameter]]] = {}
    for gname, prefixes in GROUP_PREFIXES.items():
        sel = [(n, p) for n, p in named if any(n.startswith(pre) for pre in prefixes)]
        if not sel:
            raise ValueError(
                f"参数组 {gname!r} 匹配为空（前缀 {prefixes}）——模型结构漂移或组名笔误，响亮报错"
            )
        groups[gname] = sel
    return groups


def _cos64(a: torch.Tensor | None, b: torch.Tensor | None) -> float | None:
    """float64 余弦；任一侧缺失或零范数 → None（N/A，不报错）。"""
    if a is None or b is None:
        return None
    x = a.detach().reshape(-1).to(torch.float64)
    y = b.detach().reshape(-1).to(torch.float64)
    nx, ny = float(x.norm()), float(y.norm())
    if nx == 0.0 or ny == 0.0:
        return None
    return float(torch.dot(x, y) / (x.norm() * y.norm()))


def window_losses(model, source: torch.Tensor, clean: torch.Tensor, byte_mask: torch.Tensor, ns, device):
    """step_model d 格 eval 姿态的两 codec 损失（逐位复用训练器机器）：
    s1_forward（autocast bf16, train=False）→ v_row_source 分形目标网格 → _ce。"""
    with torch.autocast("cuda", dtype=torch.bfloat16, enabled=bool(getattr(ns, "amp", False)) and device.type == "cuda"):
        out = s1.s1_forward(
            model, source, ns, clean=clean, byte_mask=byte_mask,
            retrieval_metas=None, burst_metas_q15=None, need_attn=False, train=False,
        )
    chunks = out["chunks"]
    slm_mode = getattr(model.config, "backbone_mode", "") == "slm"
    slm_coarse_v = slm_mode and getattr(model.config, "v_row_source", "memory") == "state"
    comp_cumulative = slm_coarse_v if slm_mode else getattr(ns, "cumulative_mask_retention", True)
    comp_targets, comp_slot_mask, _comp_masked, _trunc = s1._completion_target_grids(
        clean, byte_mask, chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span, comp_cumulative
    )
    if slm_coarse_v:
        encoded_targets, encoded_slot_mask, _m, _dtrunc = s1.make_cumulative_retention_targets(
            source, byte_mask, chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
        )
    else:
        encoded_targets, encoded_slot_mask, _ = make_targets(
            source, torch.zeros_like(byte_mask), chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
        )
    direct_loss = _ce(out["logits_direct"], encoded_targets, encoded_slot_mask)
    completion_loss = _ce(out["logits_backbone"], comp_targets, comp_slot_mask)
    return direct_loss, completion_loss


def measure_window(model, source: torch.Tensor, clean: torch.Tensor, byte_mask: torch.Tensor, ns, device,
                   groups: dict[str, list[tuple[str, torch.nn.Parameter]]]) -> dict:
    """一窗测量：两损失 + 每窗两次 autograd.grad + 逐组/逐层余弦与梯度范数。"""
    direct_loss, completion_loss = window_losses(model, source, clean, byte_mask, ns, device)
    union: list[tuple[str, torch.nn.Parameter]] = []
    seen: set[str] = set()
    for members in groups.values():
        for n, p in members:
            if n not in seen:
                seen.add(n)
                union.append((n, p))
    plist = [p for _, p in union]
    g_dir = torch.autograd.grad(direct_loss, plist, retain_graph=True, allow_unused=True)
    g_cmp = torch.autograd.grad(completion_loss, plist, retain_graph=False, allow_unused=True)
    gd = {n: t for (n, _), t in zip(union, g_dir)}
    gc = {n: t for (n, _), t in zip(union, g_cmp)}
    out_groups = {}
    for gname, members in groups.items():
        layer_cos: dict[str, float | None] = {}
        side_d: list[torch.Tensor] = []  # direct 侧有梯度的全部张量（范数口径）
        side_c: list[torch.Tensor] = []  # completion 侧同上
        flat_d: list[torch.Tensor] = []  # 双侧俱在的交集（余弦口径）
        flat_c: list[torch.Tensor] = []
        for n, _p in members:
            layer_cos[n] = _cos64(gd[n], gc[n])
            if gd[n] is not None:
                side_d.append(gd[n].detach().reshape(-1).to(torch.float64))
            if gc[n] is not None:
                side_c.append(gc[n].detach().reshape(-1).to(torch.float64))
            if gd[n] is not None and gc[n] is not None:
                flat_d.append(gd[n].detach().reshape(-1).to(torch.float64))
                flat_c.append(gc[n].detach().reshape(-1).to(torch.float64))
        cos_flat = None
        gn_d = float(torch.cat(side_d).norm()) if side_d else None
        gn_c = float(torch.cat(side_c).norm()) if side_c else None
        if flat_d:
            fd, fc = torch.cat(flat_d), torch.cat(flat_c)
            nd, nc = float(fd.norm()), float(fc.norm())
            if nd > 0.0 and nc > 0.0:
                cos_flat = float(torch.dot(fd, fc) / (fd.norm() * fc.norm()))
        out_groups[gname] = {
            "cos": cos_flat,
            "grad_norm_direct": gn_d,
            "grad_norm_completion": gn_c,
            "n_tensors": len(members),
            "n_with_direct_grad": len(side_d),
            "n_with_completion_grad": len(side_c),
            "n_with_both_grads": len(flat_d),
            "layer_cos": {k: (None if v is None else round(v, 6)) for k, v in layer_cos.items()},
        }
    return {
        "direct_loss": float(direct_loss.detach()),
        "completion_loss": float(completion_loss.detach()),
        "groups": out_groups,
    }


# ---------------------------------------------------------------------------
# 聚合 / 判读尺
# ---------------------------------------------------------------------------


def bootstrap_ci95(values: list[float], n_boot: int = 2000, seed: int = BOOT_SEED) -> tuple[float | None, float | None]:
    v = np.asarray(values, dtype=np.float64)
    if v.size == 0:
        return (None, None)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, v.size, size=(n_boot, v.size))
    means = v[idx].mean(axis=1)
    return (float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5)))


def _mean(xs: list[float]) -> float | None:
    return (sum(xs) / len(xs)) if xs else None


def aggregate_rows(rows: list[dict], n_boot: int = 2000, seed: int = BOOT_SEED) -> dict:
    """逐窗明细 -> 聚合（纯函数，判读尺的机械输入）。"""
    losses_d = [r["direct_loss"] for r in rows]
    losses_c = [r["completion_loss"] for r in rows]
    groups: dict[str, dict] = {}
    for g in GROUP_PREFIXES:
        cos_vals = [r["groups"][g]["cos"] for r in rows if r["groups"][g]["cos"] is not None]
        nd = [r["groups"][g]["grad_norm_direct"] for r in rows if r["groups"][g]["grad_norm_direct"] is not None]
        nc = [r["groups"][g]["grad_norm_completion"] for r in rows if r["groups"][g]["grad_norm_completion"] is not None]
        entry: dict = {
            "n": len(cos_vals),
            # 范数按侧独立聚合——结构性 N/A 组（direct 不经）也有 completion 侧读数
            "grad_norm_direct_mean": _mean(nd),
            "grad_norm_completion_mean": _mean(nc),
        }
        if cos_vals:
            lo, hi = bootstrap_ci95(cos_vals, n_boot, seed)
            entry.update(
                cos_mean=_mean(cos_vals),
                cos_ci95=[lo, hi],
                frac_negative=sum(1 for v in cos_vals if v < 0.0) / len(cos_vals),
                cos_min=min(cos_vals),
                cos_max=max(cos_vals),
            )
        groups[g] = entry
    return {
        "losses": {
            "direct_mean": _mean(losses_d),
            "direct_ci95": list(bootstrap_ci95(losses_d, n_boot, seed)),
            "completion_mean": _mean(losses_c),
            "completion_ci95": list(bootstrap_ci95(losses_c, n_boot, seed)),
        },
        "groups": groups,
    }


def _classify(mean: float, lo: float, hi: float) -> str:
    if mean < 0.0 and hi < 0.0:
        return "negative_solid"  # 负余弦且 CI 排零 = 拉扯实锤
    if mean > 0.0 and lo > 0.0:
        return "positive_solid"  # 正余弦且 CI 排零 = 同向
    return "ci_contains_zero"  # CI 含零 = 正交兼容


def verdict(group_stats: dict) -> dict:
    """判读尺（预注册，机械执行，不许事后挪）：
    - 判读三组全 negative_solid → H-sup 升级已验证；
    - 三组全 ci_contains_zero → 正交, H-sup 证伪；
    - 三组全 positive_solid → 同向, H-sup 证伪且写入侧无辜加深；
    - 其余组合 → 混合, 不升级, 逐组读数为准。"""
    per: dict[str, dict] = {}
    for g, a in group_stats.items():
        if a.get("n", 0) == 0 or a.get("cos_mean") is None:
            per[g] = {"class": "na", "note": "结构性零梯度（direct 路径不经此组），N/A 不报错"}
        else:
            per[g] = {
                "class": _classify(a["cos_mean"], a["cos_ci95"][0], a["cos_ci95"][1]),
                "cos_mean": a["cos_mean"],
                "cos_ci95": a["cos_ci95"],
                "frac_negative": a["frac_negative"],
            }
    classes = [per[g]["class"] for g in JUDGMENT_GROUPS]
    if all(c == "negative_solid" for c in classes):
        h_sup, conclusion = (
            "升级已验证",
            "写入侧三组（summarizer / kda_write_v / readout_query_v）mean 余弦持续为负且 "
            "CI95 排零——两 codec 目标在写入侧持续互相拉扯，H-sup 升级为已验证。",
        )
    elif all(c == "ci_contains_zero" for c in classes):
        h_sup, conclusion = (
            "证伪（正交）",
            "写入侧三组余弦围绕零震荡、CI95 含零——两目标近正交，容量够，拉扯不立，H-sup 证伪。",
        )
    elif all(c == "positive_solid" for c in classes):
        h_sup, conclusion = (
            "证伪（同向）",
            "写入侧三组持续正余弦——两目标同向，H-sup 证伪且写入侧无辜加深。",
        )
    else:
        h_sup, conclusion = (
            "混合（不升级）",
            "写入侧三组判读不一（负/零/正混合）——H-sup 不升级，逐组读数为准。",
        )
    return {
        "h_sup": h_sup,
        "conclusion": conclusion,
        "judgment_groups": list(JUDGMENT_GROUPS),
        "per_group": per,
    }


# ---------------------------------------------------------------------------
# 运行侧（corpus 校验 / 主循环 / 落盘）
# ---------------------------------------------------------------------------


def _sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def _round_row(row: dict) -> dict:
    out = dict(row)
    out["direct_loss"] = round(row["direct_loss"], 6)
    out["completion_loss"] = round(row["completion_loss"], 6)
    out["mask_rate"] = round(row["mask_rate"], 6)
    groups = {}
    for g, a in row["groups"].items():
        groups[g] = {
            "cos": None if a["cos"] is None else round(a["cos"], 6),
            "grad_norm_direct": None if a["grad_norm_direct"] is None else round(a["grad_norm_direct"], 8),
            "grad_norm_completion": None if a["grad_norm_completion"] is None else round(a["grad_norm_completion"], 8),
            "n_tensors": a["n_tensors"],
            "n_with_direct_grad": a["n_with_direct_grad"],
            "n_with_completion_grad": a["n_with_completion_grad"],
            "n_with_both_grads": a["n_with_both_grads"],
            "layer_cos": a["layer_cos"],
        }
    out["groups"] = groups
    return out


def render_summary(path: Path, meta: dict, agg: dict, verd: dict, rows: list[dict]) -> None:
    L = []
    L.append("# H-sup 梯度余弦测量臂 SUMMARY（零训练）")
    L.append("")
    L.append(f"- 生成时间：{meta['created']}")
    L.append(f"- 假设（候选）：codec 保真梯度把写入侧锁死在毒性盆地（direct vs completion 在写入侧持续负余弦拉扯）")
    L.append(f"- 基座：`{meta['ckpt_dir']}`（step={meta['base_step']}，d 格 Q15 收官正臂）")
    L.append(f"- 语料：`{meta['data_path']}`（sha256 前16={meta['corpus_sha256_16']}，在册值核对通过）")
    L.append(f"- 窗数：{len(rows)}（StreamingReconstructionDataset seed+9999 顺序窗，batch=1）")
    L.append("")
    L.append("## 口径注记")
    L.append("")
    L.append("- 损失：训练器机器逐位复用——`s1_forward`（autocast bf16，`train=False` eval 姿态）→ d 格"
             "（v_row_source=state）目标网格分形：direct 目标 = `make_cumulative_retention_targets(source, byte_mask)`"
             "（as-encoded 含 MASK_ID），completion 目标 = `_completion_target_grids(cumulative=True)`（干净文本），"
             "CE = `train_v36._ce` 原函数。")
    L.append("- **Q15 过程奖励三件套（L_attend / sg(g) / L_couple）是 train-only 附加件，本探针只跑标准 "
             "direct/completion 两损失**（在 q15 训出的权重上测标准 codec 损失）；burst/cloze/retrieval 数据臂同关"
             "（prob=0）。")
    L.append("- dtype：照训练器实际精度路径——fp32 主权重 + autocast bf16 前向 + `kda_impl` 照基座"
             f"（{meta['kda_impl']}）；梯度 = `torch.autograd.grad`（fp32 主权重口径），余弦 float64 计算。")
    L.append("- 掩码流 = `evaluate()` 纪律：`_MASK_GENERATOR` 一次播种 eval_mask_seed="
             f"{meta['eval_mask_seed']} 后逐窗顺序消费；mask_mode=mixed（40/60 char/BPE-word），mask_prob={meta['mask_prob']}。")
    L.append("- skip_hard 是 legacy v0.4 线（`flued/model.py`）概念，v36 主线无此旋钮，N/A。")
    L.append("- ④⑥ 两组（encoder_blocks / byte_lookup）在本臂训练时随前端冻结"
             "（freeze_prefixes=byte_lookup,encoder_blocks,segmentor_blocks,segmentor_head）——其读数是开梯度的"
             "**反事实几何**（若梯度可流，两目标在该点的方向关系），非训练中真实流过的梯度；作对照组用。")
    L.append("- 模型实例化严格按基座 resolved_config（Namespace 直建，不经 parser 现行默认值）；装载做全键"
             "全形双向校验（不齐 loud fail，坑 8 对偶纪律）。")
    L.append("- d 格拓扑：K 通道（write_head_k / state_machine_k / index_ffn）只喂 backbone store，不经 direct 腿"
             "——对应组 direct 梯度结构性为零，报 N/A 不报错。backbone 组同理（direct 不过 backbone）。")
    L.append("- 未测件（不在任务六组内）：state_machine{,_k}.realign、decoder_in、chunk_pos、bridge、segmentor_*。")
    L.append("")
    L.append("## 判读尺（预注册，不许事后挪）")
    L.append("")
    L.append("- 写入侧三组（① summarizer、② kda_write_v、③ readout_query_v）mean 余弦持续为负且 CI95 排零"
             " = 拉扯实锤（H-sup 升级为已验证）；")
    L.append("- 围绕零对称震荡、CI 含零 = 正交（容量够，拉扯不立，H-sup 证伪）；")
    L.append("- 持续正余弦 = 两目标同向（H-sup 证伪且写入侧无辜加深）；")
    L.append("- 对照组（④⑤⑥）读数用于排除「全模型处处拉扯」的平庸解释。")
    L.append("")
    L.append("## 结果")
    L.append("")
    L.append(f"- 两损失幅度：direct_loss mean = {agg['losses']['direct_mean']:.4f}"
             f"（CI95 [{agg['losses']['direct_ci95'][0]:.4f}, {agg['losses']['direct_ci95'][1]:.4f}]），"
             f"completion_loss mean = {agg['losses']['completion_mean']:.4f}"
             f"（CI95 [{agg['losses']['completion_ci95'][0]:.4f}, {agg['losses']['completion_ci95'][1]:.4f}]）")
    L.append("")
    L.append("| 组 | n | mean cos | CI95 | 负余弦占比 | ‖g_direct‖ | ‖g_completion‖ | 判读 |")
    L.append("|---|---|---|---|---|---|---|---|")
    for g in GROUP_PREFIXES:
        a = agg["groups"][g]
        v = verd["per_group"][g]
        if a.get("n", 0) == 0 or a.get("cos_mean") is None:
            nd = a.get("grad_norm_direct_mean")
            nc = a.get("grad_norm_completion_mean")
            nd_s = "—" if nd is None else f"{nd:.3e}"
            nc_s = "—" if nc is None else f"{nc:.3e}"
            L.append(f"| {g} | 0 | N/A | N/A | N/A | {nd_s} | {nc_s} | {v['class']}（{v.get('note','')}） |")
        else:
            L.append(
                f"| {g} | {a['n']} | {a['cos_mean']:+.4f} | [{a['cos_ci95'][0]:+.4f}, {a['cos_ci95'][1]:+.4f}] "
                f"| {a['frac_negative']:.3f} | {a['grad_norm_direct_mean']:.3e} | {a['grad_norm_completion_mean']:.3e} "
                f"| {v['class']} |"
            )
    L.append("")
    L.append("## 结论（判读尺对照）")
    L.append("")
    L.append(f"**{verd['h_sup']}**：{verd['conclusion']}")
    L.append("")
    path.write_text("\n".join(L), encoding="utf-8")


def main() -> None:
    p = argparse.ArgumentParser(description="H-sup: direct vs completion 梯度余弦（写入侧, 零训练）")
    p.add_argument("--ckpt-dir", default="checkpoints/v37ks_d_sm_q15_circuit_20k_ctx4096_20260825b")
    p.add_argument("--out-dir", default="outputs/h_sup_gradcos_20260930")
    p.add_argument("--n-windows", type=int, default=256, help="测量窗数（≥256；eval 流池 512）")
    p.add_argument("--min-windows", type=int, default=256, help="提前收官时的最少窗数，不足响亮失败")
    p.add_argument("--max-seconds", type=float, default=0.0, help=">0 时到点提前收官（仍聚合）")
    p.add_argument("--bootstrap", type=int, default=2000)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--kda-impl", default="", help="覆盖基座 kda_impl（默认照 resolved_config）")
    p.add_argument("--verify-corpus-sha256", default="ed4ab97810776ce7",
                   help="语料在册 sha256 前 16 位；空串跳过校验")
    p.add_argument("--progress-every", type=int, default=16)
    args = p.parse_args()

    device = torch.device(
        "cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu"
    )
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    ckpt_dir = Path(args.ckpt_dir)
    model, ns, base_step, _cfg = load_base_model(ckpt_dir, device, kda_impl=args.kda_impl)
    print(
        f"[h_sup] 基座 {ckpt_dir.name} step={base_step} 装载（全键全形校验通过）| "
        f"d 格 k={ns.k_row_source}/v={ns.v_row_source} kda_impl={ns.kda_impl} device={device.type}",
        flush=True,
    )
    if args.verify_corpus_sha256:
        digest = _sha256(ns.data_path)
        if not digest.startswith(args.verify_corpus_sha256):
            raise SystemExit(
                f"[h_sup] 语料 sha256 校验失败: {digest[:16]} != 在册 {args.verify_corpus_sha256} ({ns.data_path})"
            )
        print(f"[h_sup] 语料 {ns.data_path} sha256 前16={digest[:16]} 核对通过 ({time.time()-t0:.0f}s)", flush=True)
    if s1._BPE_TOKENIZER is None and getattr(ns, "mask_mode", "mixed") == "mixed" and ns.mask_prob > 0:
        s1._load_bpe_tokenizer(ns.bpe_tokenizer_path)

    windows = build_eval_windows(ns, args.n_windows)
    if len(windows) < args.n_windows:
        raise SystemExit(f"[h_sup] eval 流只产出 {len(windows)} 窗 < 请求 {args.n_windows}（池=512），响亮失败")
    masks = build_masks(windows, ns)
    groups = build_param_groups(model)
    n_union = len({n for members in groups.values() for n, _ in members})
    print(
        f"[h_sup] {len(windows)} 窗就绪；参数组 {len(groups)} 个 / 并集 {n_union} 张量 "
        f"({time.time()-t0:.0f}s)",
        flush=True,
    )

    rows: list[dict] = []
    jsonl_path = out_dir / "windows.jsonl"
    stopped_early = False
    with jsonl_path.open("w", encoding="utf-8") as jf:
        for wi, (clean_cpu, mask_cpu) in enumerate(zip(windows, masks)):
            clean = clean_cpu.to(device)
            byte_mask = mask_cpu.to(device)
            valid = clean_cpu.ne(PAD_ID)
            mask_rate = float(mask_cpu[valid].float().mean()) if bool(valid.any()) else 0.0
            source = clean.masked_fill(byte_mask, MASK_ID)
            meas = measure_window(model, source, clean, byte_mask, ns, device, groups)
            row = {"window": wi, "mask_rate": mask_rate, **meas}
            rows.append(row)
            jf.write(json.dumps(_round_row(row), ensure_ascii=False) + "\n")
            jf.flush()
            del clean, byte_mask, source, meas
            if (wi + 1) % args.progress_every == 0 or wi == 0:
                dt = time.time() - t0
                eta = dt / (wi + 1) * (args.n_windows - wi - 1)
                g = rows[-1]["groups"]
                sw = g["summarizer"]["cos"]
                print(
                    f"[h_sup] 窗 {wi+1}/{args.n_windows} | direct={row['direct_loss']:.3f} "
                    f"comp={row['completion_loss']:.3f} | summarizer cos={sw if sw is None else round(sw,4)} "
                    f"| 已用 {dt:.0f}s ETA {eta:.0f}s",
                    flush=True,
                )
            if (wi + 1) % 32 == 0 and device.type == "cuda":
                torch.cuda.empty_cache()
            if args.max_seconds > 0 and (time.time() - t0) > args.max_seconds:
                stopped_early = True
                print(f"[h_sup] 到点提前收官（{args.max_seconds}s），已测 {len(rows)} 窗", flush=True)
                break
    if len(rows) < args.min_windows:
        raise SystemExit(
            f"[h_sup] 仅测得 {len(rows)} 窗 < --min-windows {args.min_windows}，样本量不足，响亮失败"
        )

    agg = aggregate_rows(rows, n_boot=args.bootstrap, seed=BOOT_SEED)
    verd = verdict(agg["groups"])
    meta = {
        "probe": "H-sup direct-vs-completion 写入侧梯度余弦（零训练测量臂）",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "ckpt_dir": str(ckpt_dir),
        "base_step": base_step,
        "data_path": ns.data_path,
        "corpus_sha256_16": args.verify_corpus_sha256 or None,
        "n_windows": len(rows),
        "stopped_early": stopped_early,
        "eval_stream_seed": int(ns.seed) + 9999,
        "eval_mask_seed": int(ns.eval_mask_seed),
        "mask_mode": getattr(ns, "mask_mode", "mixed"),
        "mask_prob": float(ns.mask_prob),
        "kda_impl": ns.kda_impl,
        "amp": bool(getattr(ns, "amp", False)),
        "device": device.type,
        "dtype_path": "fp32 主权重 + autocast bf16 前向（训练器实际精度路径）; autograd.grad fp32; 余弦 float64",
        "posture": "标准 codec 两损失（Q15 三件套/burst/cloze/retrieval 全关），eval 姿态 train=False",
        "group_prefixes": GROUP_PREFIXES,
        "group_legend": GROUP_LEGEND,
        "judgment_groups": list(JUDGMENT_GROUPS),
        "bootstrap": args.bootstrap,
        "boot_seed": BOOT_SEED,
        "timing_sec": round(time.time() - t0, 1),
    }
    report = {**meta, "losses": agg["losses"], "groups": agg["groups"], "verdict": verd}
    agg_path = out_dir / "aggregate.json"
    agg_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    render_summary(out_dir / "SUMMARY.md", meta, agg, verd, rows)

    print(f"\n[h_sup] 判读尺结论: {verd['h_sup']} —— {verd['conclusion']}", flush=True)
    for g in JUDGMENT_GROUPS:
        a = agg["groups"][g]
        if a.get("cos_mean") is not None:
            print(
                f"[h_sup]   {g:18s} mean={a['cos_mean']:+.4f} CI95=[{a['cos_ci95'][0]:+.4f}, "
                f"{a['cos_ci95'][1]:+.4f}] neg%={a['frac_negative']:.3f}",
                flush=True,
            )
    print(f"[h_sup] 产物: {jsonl_path} / {agg_path} / {out_dir / 'SUMMARY.md'} ({time.time()-t0:.0f}s)", flush=True)


if __name__ == "__main__":
    main()
