"""Q18 v2 读出墙裁定臂（任务书 2026-08-27 冻结:
docs/versions/v3.7/FLUED_V3_7_Q18_V2_READOUT_WALL_20260827_CN.md —— §1 双臂/
§2 判读表/§3 施工注记是合同）。实现形态 = Q17 训练器
(tools/train/v3_6/train_q17_oracle_readout.py) 的双臂扩展, Q17 原文件零改动。

A 臂（预算终审）: Q17 形态原样复刻延长——同一从零读出链（Q17 修订 v1 足迹:
readout_query×2+realign×2+align_k/align_v+backbone+decoder_in+decoder, Q15 d
格基座冻结面不变）, oracle 态全程（退火课程关闭, p 恒 1.0——审的是"读人造
健康态"本身的可学习性）, 40K 步 + warmup 200 + cosine→0（E103 承重墙条款）,
LR 1e-3（同任务同链, 终审变量是预算不是配方）, 种子参数化（42/1/2）。收官
schema 同 Q17（run dir 可被 probe_burst_route_q15 --ckpt 直接加载; codec 双
指标参照列; train_log 全 trajectory 供 trailing 斜率 CI）。

A′ 臂（闭式温启动, 双列）: 链模块不从零——Q19 闭式三段件的等价权重挂载。
outputs/q19_closed_form_20260827/ 未落盘权重（只有 json/txt 台账）, 开工时按
Q19 同协议（同 eval 窗流 seed+9999 / eval_mask_seed 1042 / 同 λ）重拟合,
闭式确定性。映射规格（§3.2 "分解/挂载方式由施工核实后注释入册", 残差全部
落盘 warmstart_report.json）:
  段1（S→v̂）→ readout_query（双状态机双通道）: ridge_unmix 是位置依赖算子
    （有效查询 q_i = K_iᵀ(K_iK_iᵀ+λI)⁻¹e_i 随窗随 chunk 变）, 无法逐位挂进
    固定 readout_query——施工核实后的挂载 = 逐头定点查询的闭式 ridge 回归
    q_h = (Σ_i S_i,h S_i,hᵀ + λ̂I)⁻¹ Σ_i S_i,h v̂_i,h（λ̂ = λ·mean(diag) 相对
    预条件, Q19 D5 教训: 固定 λ 对 α≈0.003 缩比的 oracle 特征变相过正则）。
  段2（v̂→m̂）→ realign 复合线性层: realign 内 LayerNorm 数据依赖不可折叠
    进固定线性, 段2 在 LN 后特征 z 上重拟合（全局单折固定权重——温启动要
    的是一组权重不是 held-out 预测, Q19 的分窗 2-fold 形式随之替换, 申报）。
    v 通道: 桥目标 = donor 格真实 memory 行（Q19 D6 同口径）, 挂 realign
    第一 Linear 前 d_mem 行（其余置零）; k 通道 Q19 段2 无对应物, 全宽
    ridge z→package 直挂（申报）。realign 第二 Linear 闭式 ridge 收尾:
    SiLU(L1(z)) → package_target, package_target = 基座生产 v_rows/k_rows
    （read_trained 同态——停放文档第 3 条"状态→package 回归再挂载"）。
  decoder_in_mem 等价位置: d 格基座无 decoder_in_mem——沿用 Q19 D1 donor
    端口方案（b 格 v371 冻结组件）, 灌 d 格 decoder_in（1536→384, direct
    口输入投影）: composite ridge packagê → donor.decoder_in_mem(m_donor)。
    donor 端口权重经此复合入链, 不新增模块——收官 state_dict 与基座同构,
    probe strict 加载不破。decoder 保持基座值（任务书原文）。echo CE 不经
    direct 口——该挂载只影响收官 eval 的 direct 参照列。
  backbone/align_k/align_v 保持基座值（申报: 任务书只明说 decoder; 从零
    backbone 使零变化律物理不可达——echo 路径 decoder(backbone_out+pos)
    必过 backbone）。A′ 的单变量声明 = 温启动 vs 从零（从零足迹由 A 臂承担）。
零变化律自检（任务书 §1 预注册; 考场口径修订 Q18-D7, 实测证据见
DECLARED_DEVIATIONS）: 温启动后首步 eval——Q19 同款 fine 细格（全槽
as-encoded, 无 burst 拼接, eval_mask_seed 1042, 列自己的态）backbone 腿
均值必须 >0.15（从零链同格贴盲猜先验 ~0.07; echo 格参照 ~0.00-0.04）,
不过响亮退出——初始化没接通, 臂作废重查不许判负。direct 腿读数随录入册。
RNG 隔离: 检查后训练流重 seed, 自检不消耗训练流。
微调 20K/列（微调非从零——与 A 的 40K 不直接比步数, 比"摸到天花板没有",
审稿 parity 注记入册）: oracle 列 p≡1.0 / natural 列 p≡0.0; LR 1e-3 +
warmup 200 + cosine→0。收官 schema 同 Q17——natural 列收官 run dir 即
probe_burst_route_q15 兼容 Δ 考场的加载对象（Q17 条件 3 兼容条款沿用）。
种子 42 单种子先行（A′ 方向性实测, 种子加固等方向成立后再补）。

B 参照列（任务书 §1 "从零链读明文 memory 行"）未施工: 施工清单未列且 d 格
维度不通（memory 行 512 ≠ 链 v_rows 1536, 无冻结消费口）——待主会话钉规格。

Usage:
  A 臂: python tools/train/v3_6/train_q18_readout_wall.py --q18-arm A \
      --seed 42 --device cuda
  A′ 臂: python tools/train/v3_6/train_q18_readout_wall.py --q18-arm Aprime \
      --q18-warmstart oracle --device cuda   （或 natural）
  CPU 冒烟: py -3.14 -X utf8 tools/train/v3_6/train_q18_readout_wall.py \
      --q18-arm Aprime --q18-warmstart natural --device cpu --max-steps 3 \
      --seq-len 512 --max-eval-batches 1 --q18-calib-windows 2 \
      --q18-zc-windows 4 --out-dir checkpoints/_smoke_q18_cpu
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import torch
import torch.nn as nn
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
    load_model,
    read_trained,
    ridge_unmix,
)
from tools.analysis.v3_6.probe_closed_form_readout import row_cos  # noqa: E402
from tools.train.v3_6 import train_q17_oracle_readout as q17  # noqa: E402

BASE_RUN = "checkpoints/v37ks_d_sm_q15_circuit_20k_ctx4096_20260825b"
DONOR_RUN = "checkpoints/v37ks_b_sm_v371_20k_ctx4096_20260817"  # A′ 段3/donor 端口 (Q19 D1)

# 退火抽签流独立种子偏移 (与 Q17 的 101_033 不混; 任务书 §4: 抽签流全部可复现)
_Q18_SEED_OFFSET = 101_077
_Q18_GENERATOR = torch.Generator()
_Q18_ZC_SEED = 202_608_27  # 零变化律自检专用流
_Q18_ZC_THRESHOLD = 0.15  # 任务书 §1 预注册: 温启动首步必须显著高于从零 (~0.00-0.04)
_Q18_MILESTONE_STEPS = 2000  # 里程碑 cadence 沿用 Q17 (每 2K)

DECLARED_DEVIATIONS = [
    "Q18-D1: 段1 ridge_unmix 是位置依赖算子 (q_i = K_iᵀ(K_iK_iᵀ+λI)⁻¹e_i 随窗随 chunk 变), 不可逐位挂进固定 "
    "readout_query——施工核实挂载 = 逐头闭式 ridge 回归 q_h = argmin Σ_i‖qᵀS_i,h−v̂_i,h‖² (相对 λ 预条件), "
    "映射残差落盘 warmstart_report.json。",
    "Q18-D2: realign 内 LayerNorm 数据依赖不可折叠进固定线性——段2 在 LN 后特征 z 上全局单折重拟合 (温启动要 "
    "固定权重, Q19 分窗 2-fold held-out 形式随之替换); λ 用相对预条件 (D5 教训)。",
    "Q18-D3: package 落点 = 基座生产 v_rows/k_rows (read_trained 同态; 停放文档第 3 条 '状态→package 回归再挂载'); "
    "v 通道 realign L1 前 d_mem 行挂段2 桥 (目标 = donor 真实 memory 行, Q19 D6 同口径), k 通道 Q19 段2 无对应物 "
    "改全宽 ridge z→package 直挂; L2 闭式 ridge 收尾吸收 SiLU 非线性。",
    "Q18-D4: d 格无 decoder_in_mem——等价位置 = d 格 decoder_in (1536→384, direct 口输入投影), 灌 composite ridge "
    "packagê→donor.decoder_in_mem(m_donor); donor 端口权重经复合入链, 不新增模块 (收官 state_dict 与基座同构, "
    "probe strict 加载不破); decoder 保持基座值 (任务书原文)。echo CE 不经 direct 口——该挂载只影响收官 eval "
    "direct 参照列。",
    "Q18-D5: backbone/align_k/align_v 保持基座值 (任务书只明说 decoder 保持基座值; 从零 backbone 使零变化律物理 "
    "不可达——echo 路径 decoder(backbone_out+pos) 必过 backbone)。A′ 的单变量声明 = 温启动 vs 从零 (A 臂承担 "
    "从零足迹)。",
    "Q18-D6: B 参照列 (任务书 §1 '从零链读明文 memory 行') 未施工——施工清单未列且 d 格维度不通 (memory 行 512 "
    "≠ 链 v_rows 1536, 无冻结消费口)——待主会话钉规格。",
    "Q18-D7: 零变化律考场口径修订 (实测驱动, 证据入册): 预注册文本的 echo byte_acc 考场 (burst 尾遮蔽槽, "
    "backbone 腿) 对本检查不可分辨——基座生产链自身同点读数 0.0 (seq512 冒烟窗, 每窗仅 3-6 高熵 CJK 尾字节槽) "
    "/ 官方收官 eval_burst_tail_byte_acc 0.0608 (seq4096) 皆低于 0.15 阈值, 从零/温启动/生产链三者无区分度。"
    "自检考场移至 Q19 同款 fine 细格 (全槽 as-encoded, 无 burst 拼接, eval_mask_seed 1042): 从零链≈盲猜先验 "
    "~0.07, 基座生产 0.53(natural)/0.17(oracle), Q19 闭式 0.31-0.33, 三者分离。判官腿 = backbone 腿 (echo CE "
    "训练/判读同路), direct 腿读数随录入册。阈值 0.15 不变。",
]


# ---------------------------------------------------------------------------
# 课程 (任务书 §1: A 臂退火关闭 p 恒 1.0; A′ 按列固定)
# ---------------------------------------------------------------------------


def _q18_course_p(arm: str, warmstart: str | None, step: int) -> float:
    """Q18 课程表: A 臂 oracle 全程 p≡1.0 (退火课程关闭——审的是"读人造健康
    态"本身的可学习性); A′ 臂 oracle 列 p≡1.0 / natural 列 p≡0.0。与步数无关
    (课程断言对此: 任意 step 恒定)。"""
    del step
    if arm == "A":
        return 1.0
    if arm == "Aprime":
        return 1.0 if warmstart == "oracle" else 0.0
    raise ValueError(f"unknown q18 arm {arm!r}")


# ---------------------------------------------------------------------------
# 闭式 ridge (fp64 累计/求解, 相对 λ 预条件 — Q19 D5 教训; 纯函数, 测试同用)
# ---------------------------------------------------------------------------


def _ridge_solve(X: torch.Tensor, Y: torch.Tensor, lam: float) -> torch.Tensor:
    """闭式 ridge 带截距: W = argmin ‖[X,1]W − Y‖² + λ̂‖W‖², λ̂ = lam·mean(diag(G))
    相对预条件 (固定 λ 对 α≈0.003 缩比的 oracle 特征变相过正则, D5)。X (n,d)
    Y (n,e) → W (d+1,e) fp32。fp64 求解, 确定性。"""
    X = X.double().cpu()
    Y = Y.double().cpu()
    n = X.size(0)
    X1 = torch.cat([X, torch.ones(n, 1, dtype=torch.float64)], dim=1)
    G = X1.T @ X1
    # 相对预条件 (Q19 D5): λ̂ 锚在特征块均值对角线上 (截距列 diag=n 不计入——
    # 否则特征缩比被截距稀释, 相对性名存实亡)
    lam_eff = lam * torch.diagonal(G)[: X.size(1)].mean().clamp(min=1e-20)
    W = torch.linalg.solve(G + lam_eff * torch.eye(G.size(0), dtype=torch.float64), X1.T @ Y)
    return W.float()


def _q18_apply_linear(X: torch.Tensor, W: torch.Tensor) -> torch.Tensor:
    """[X,1] @ W — _ridge_solve 产物的应用侧 (截距行在末行)。"""
    X1 = torch.cat([X.float(), torch.ones(X.size(0), 1)], dim=1)
    return X1 @ W


def _q18_solve_stage1_grams(A: torch.Tensor, B: torch.Tensor, lam: float) -> torch.Tensor:
    """段1 Gram 求解: A (H,hk,hk) = Σ_i S_iS_iᵀ, B (H,hk) = Σ_i S_i v̂_i (fp64)
    → q (H,hk) fp32。λ̂ = lam·mean(diag) 逐头相对预条件。"""
    out = []
    for h in range(A.size(0)):
        Ah, Bh = A[h].double().cpu(), B[h].double().cpu()
        lam_eff = lam * torch.diagonal(Ah).mean().clamp(min=1e-20)
        out.append(torch.linalg.solve(Ah + lam_eff * torch.eye(Ah.size(0), dtype=torch.float64), Bh))
    return torch.stack(out).float()


def _q18_fit_stage1_queries(S: torch.Tensor, v_hat: torch.Tensor, lam: float) -> torch.Tensor:
    """段1 定点查询闭合形式 (映射规格 Q18-D1): ridge_unmix 的位置依赖算子不可
    逐位挂进固定 readout_query——逐头 ridge 回归 q_h = argmin_q Σ_i
    ‖qᵀS_i,h − v̂_i,h‖²。S (n,H,hk,hv), v_hat (n,H*hv) → q (H,hk) fp32。"""
    n, H, hk, hv = S.shape
    assert v_hat.shape == (n, H * hv), f"v_hat shape {tuple(v_hat.shape)} != {(n, H * hv)}"
    Sd = S.double()
    vhd = v_hat.double().view(n, H, hv)
    A = torch.einsum("nhkv,nhjv->hkj", Sd, Sd)
    B = torch.einsum("nhkv,nhv->hk", Sd, vhd)
    return _q18_solve_stage1_grams(A, B, lam)


# ---------------------------------------------------------------------------
# 挂载 (任务书 §3.2, 分解/挂载方式施工核实后注释入册 — 见模块 docstring)
# ---------------------------------------------------------------------------


@torch.no_grad()
def _q18_mount_stage1(sm, q: torch.Tensor) -> None:
    """段1 查询 → readout_query。映射规格假定 nq=1 (Q15 d 格 resolved_config
    readout_queries=1), 超规格响亮退出。"""
    if sm.readout_query.size(0) != 1:
        raise ValueError(
            f"readout_queries={sm.readout_query.size(0)} != 1 — Q18 映射规格假定 nq=1, 需主会话钉多查询分解"
        )
    sm.readout_query.data[0].copy_(q.to(sm.readout_query.dtype))


@torch.no_grad()
def _q18_mount_realign(sm, W_bridge: torch.Tensor, W_out: torch.Tensor) -> None:
    """段2 桥 + 收尾 → realign 复合线性层 (Q18-D2/D3)。realign = LayerNorm →
    L1(d_in→d_pack) → SiLU → L2(d_pack→d_pack): L1 前 d_bridge 行 = W_bridge
    (v 通道: 段2 v̂→m̂ 闭式桥; k 通道: 全宽 z→package 直挂), 其余置零; L2 =
    W_out (SiLU 后特征 → package_target 闭式收尾)。LN 保持基座值。"""
    ln, l1, _silu, l2 = sm.realign
    d_in, d_total, d_out = l1.in_features, l1.out_features, l2.out_features
    d_bridge = W_bridge.size(1)
    assert W_bridge.shape == (d_in + 1, d_bridge), f"W_bridge {tuple(W_bridge.shape)} != {(d_in + 1, d_bridge)}"
    assert d_bridge <= d_total
    assert W_out.shape == (d_total + 1, d_out), f"W_out {tuple(W_out.shape)} != {(d_total + 1, d_out)}"
    l1.weight.data.zero_()
    l1.bias.data.zero_()
    l1.weight.data[:d_bridge] = W_bridge[:d_in].T.to(l1.weight.dtype)
    l1.bias.data[:d_bridge] = W_bridge[d_in].to(l1.bias.dtype)
    l2.weight.data.copy_(W_out[:d_total].T.to(l2.weight.dtype))
    l2.bias.data.copy_(W_out[d_total].to(l2.bias.dtype))


def _q18_chain_features(z: torch.Tensor, W_bridge: torch.Tensor, d_total: int) -> torch.Tensor:
    """挂载后 realign L1→SiLU 的闭式等价特征: pre[:, :d_bridge] = [z,1]@W_bridge,
    其余 0 → SiLU。与 _q18_mount_realign 的前向逐位对应 (测试同用)。"""
    d_bridge = W_bridge.size(1)
    pre = z.new_zeros(z.size(0), d_total)
    pre[:, :d_bridge] = _q18_apply_linear(z, W_bridge)
    return F.silu(pre)


# ---------------------------------------------------------------------------
# 零变化律自检 (任务书 §1 预注册)
# ---------------------------------------------------------------------------


def _q18_zero_change_verdict(accs: list[float], threshold: float = _Q18_ZC_THRESHOLD) -> float:
    """零变化律判读: 温启动首步 eval 均值必须 > threshold (从零链同格参照:
    echo 格 ~0.00-0.04 / 细格贴盲猜先验 ~0.07), 不过响亮退出——初始化没接通,
    臂作废重查不许判负。空窗同样响亮退出 (无法验证 ≠ 通过)。"""
    if not accs:
        raise RuntimeError("Q18 零变化律自检失败: 0 窗可读——无法验证温启动接通, 臂作废重查")
    mean = sum(accs) / len(accs)
    if not (mean > threshold):
        raise RuntimeError(
            f"Q18 零变化律自检失败: 温启动首步 acc={mean:.4f} <= {threshold} "
            f"(n={len(accs)})——初始化没接通 (从零链同格贴先验), 臂作废重查不许判负"
        )
    return mean


@torch.no_grad()
def _q18_zero_change_check(model, ns, device, p: float, n_windows: int, threshold: float):
    """温启动后首步 eval (任务书 §1 预注册零变化律; 考场口径修订 Q18-D7):
    Q19 同款 fine 细格 (全槽 as-encoded, 无 burst 拼接, eval_mask_seed 1042,
    D2 考场) 双腿读数。预注册文本的 echo byte_acc 考场 (burst 尾遮蔽槽,
    backbone 腿) 实测对本检查不可分辨——基座生产链自身同点读数 0.0
    (seq512 冒烟窗 3-6 槽) / 收官 0.0608 (seq4096) 皆低于 0.15 阈值,
    从零/温启动/生产链三者无区分度; 细格上三者分离 (从零≈先验 0.07,
    基座生产 0.53(natural)/0.17(oracle), Q19 闭式 0.31-0.33)。判官腿 =
    backbone 腿 (echo CE 训练/判读同路), direct 腿读数随录入册。
    列自己的态: p>=0.5 -> oracle 态 (α 缩放), 否则自然态。RNG: 只动
    s1._MASK_GENERATOR (build_masks 重 seed 1042), 调用侧检查后重 seed 训练流。
    Returns (mean_backbone, {"backbone": [...], "direct": [...]})。"""
    windows = build_eval_windows(ns, n_windows)
    masks = build_masks(windows, ns)
    was_training = model.training
    model.eval()
    accs: dict[str, list[float]] = {"backbone": [], "direct": []}
    try:
        for clean, byte_mask in zip(windows, masks):
            source = clean.masked_fill(byte_mask, MASK_ID).to(device)
            enc = q17._q17_encode_and_states(model, source)
            chunks = enc["chunks"]
            use_oracle = p >= 0.5
            S_k = enc["so_k"] if use_oracle else enc["sn_k"]
            S_v = enc["so_v"] if use_oracle else enc["sn_v"]
            k_rows = q17._q17_readout(model.state_machine_k, S_k).mean(dim=2)
            v_rows = q17._q17_readout(model.state_machine, S_v).mean(dim=2)
            n_chunks = chunks.chunk_mask.size(1)
            pos = model.chunk_pos.weight.unsqueeze(0)[:, :n_chunks]
            logits = {
                "backbone": model.decoder(
                    model.backbone(k_rows, v_rows, chunks.chunk_mask, pos, store_block=None) + pos,
                    chunks.token_mask,
                ),
                "direct": model.decoder(model.decoder_in(v_rows) + pos, chunks.token_mask),
            }
            zeros = torch.zeros_like(byte_mask)
            targets, slot, _m = s1.make_targets(
                source.cpu(), zeros.cpu(), chunks.chunk_ids.cpu(), chunks.offsets.cpu(),
                ns.max_chunks, ns.max_span,
            )
            for leg, lg in logits.items():
                n = lg.size(1)
                accs[leg].append(float(s1._acc_tensor(lg.argmax(dim=-1).cpu(), targets[:, :n], slot[:, :n])))
    finally:
        if was_training:
            model.train()
    return _q18_zero_change_verdict(accs["backbone"], threshold), accs


# ---------------------------------------------------------------------------
# A′ 闭式温启动 (两遍标定, Q19 同协议窗, 闭式确定性; 残差全部落盘)
# ---------------------------------------------------------------------------


@torch.no_grad()
def _q18_warmstart(model, donor, ns, device, column: str, n_windows: int, lam_unmix: float, lam_stage2: float,
                   xstate_target: bool = False) -> dict:
    """Q19 闭式三段件等价权重挂载 (任务书 §3.2; 权重未落盘, 按 Q19 同协议
    重拟合——闭式确定性)。pass1: 逐窗前端×2 + 双态 + 选列态 + ridge_unmix,
    累计段1 Gram (fp64) + 缓存 v̂/package_target (read_trained 同态, 挂载前
    基座读出)/m_donor; solve+挂载段1。pass2: 重算态 (前端确定性) → 挂载后
    段1 链输出 u → LN 后特征 z 缓存。之后全部从缓存行闭式求解: 段2 桥 →
    realign L1, SiLU 特征 → package 收尾 → realign L2, decoder_in 复合
    (v 通道)。Returns 映射报告 dict。

    xstate_target (候选偏差, 默认关 = 同态忠实): oracle 列的 package_target
    改取自然态生产行 read_trained(sm, S_nat)——特征仍来自 oracle 态, 即
    "oracle 态 → 生产格式"的翻译挂载; 同态挂载的考场读数被"基座读 oracle 态"
    自身上限钳住 (冒烟实测 0.127, 低于 0.15 门), 翻译挂载不受该上限约束。
    natural 列两形态逐位相同 (S_sel = S_nat)。"""
    windows = build_eval_windows(ns, n_windows)
    masks = build_masks(windows, ns)  # side-effect 重置 s1._MASK_GENERATOR — 调用侧标定后重 seed 训练流
    channels = (("v", "state_machine"), ("k", "state_machine_k"))
    d_mem = donor.decoder_in_mem.in_features
    grams: dict[str, dict] = {ch: {"A": None, "B": None} for ch, _ in channels}
    cache: dict[str, dict] = {ch: {"vh": [], "pkg": [], "u": [], "z": [], "cos": []} for ch, _ in channels}
    m_donor_by_win: list[torch.Tensor] = []

    def _window_states(wi, clean, byte_mask):
        source = clean.masked_fill(byte_mask, MASK_ID).to(device)
        chunks, memory, index = _front_end(model, source)
        n_real = int(chunks.chunk_mask[0].sum())
        out = {}
        for ch, _sm_name in channels:
            gates = model.write_head(memory) if ch == "v" else model.write_head_k(index)
            S_nat, S_or = q17._q17_states_dual(gates, chunks.chunk_mask)
            if column == "oracle":
                S_full, _alpha = q17._q17_alpha_scale(S_nat, S_or, chunks.chunk_mask)
            else:
                S_full = S_nat
            out[ch] = (gates, S_full[0, :n_real], S_nat[0, :n_real])  # (n,H,hk,hv) ×2
        return source, chunks, n_real, out

    # pass 1: 段1 Gram + 缓存 (package_target 必须挂载前取 — read_trained 用基座读出权重)
    for wi, (clean, byte_mask) in enumerate(zip(windows, masks)):
        source, chunks, n_real, states = _window_states(wi, clean, byte_mask)
        _dc, d_memory, _di = _front_end(donor, source)
        if not torch.equal(chunks.token_mask, _dc.token_mask):
            raise ValueError(f"window {wi}: base/donor token_mask 不一致——D1 前端同源假设破裂, loud fail")
        m_donor_by_win.append(d_memory[0, :n_real].float().cpu())
        for ch, sm_name in channels:
            gates, S, S_nat = states[ch]
            sm = getattr(model, sm_name)
            vh, cos = ridge_unmix(gates, S.unsqueeze(0), lam_unmix)
            S_pkg = S_nat if xstate_target else S  # 翻译挂载候选: oracle 态特征 → 自然态生产行
            pkg = read_trained(sm, S_pkg.unsqueeze(0))[0].float()  # (n, d_pack) 基座生产行
            vh = vh[0].float()  # (n, H*hv)
            cache[ch]["vh"].append(vh.cpu())
            cache[ch]["pkg"].append(pkg.cpu())
            cache[ch]["cos"].append(cos)
            n_c, H_c, _hk_c, hv_c = S.shape
            Sd = S.double()
            vhd = vh.to(S.device).double().view(n_c, H_c, hv_c)
            A = torch.einsum("nhkv,nhjv->hkj", Sd, Sd)
            B = torch.einsum("nhkv,nhv->hk", Sd, vhd)
            grams[ch]["A"] = A if grams[ch]["A"] is None else grams[ch]["A"] + A
            grams[ch]["B"] = B if grams[ch]["B"] is None else grams[ch]["B"] + B
        print(f"[q18] 标定 pass1 window {wi} n_real={n_real}", flush=True)

    # solve + 挂载段1 (双通道)
    for ch, sm_name in channels:
        q = _q18_solve_stage1_grams(grams[ch]["A"], grams[ch]["B"], lam_unmix)
        _q18_mount_stage1(getattr(model, sm_name), q)

    # pass 2: 重算态 (前端确定性) → 挂载后链输出 u → LN 后 z
    for wi, (clean, byte_mask) in enumerate(zip(windows, masks)):
        _source, _chunks, n_real, states = _window_states(wi, clean, byte_mask)
        for ch, sm_name in channels:
            _gates, S, _snat = states[ch]
            sm = getattr(model, sm_name)
            q = sm.readout_query.detach().float()[0]  # nq=1 (挂载时断言)
            u = torch.einsum("hk,nhkv->nhv", q, S).reshape(n_real, -1)  # (n, H*hv)
            ln = sm.realign[0]
            z = ln(u.to(next(ln.parameters()).dtype))  # LN 基座值, eval 确定性
            cache[ch]["u"].append(u.float().cpu())
            cache[ch]["z"].append(z.float().cpu())
        print(f"[q18] 标定 pass2 window {wi}", flush=True)

    # 闭式求解段2 桥 + realign 收尾 + decoder_in 复合, 残差落盘
    m_all = torch.cat(m_donor_by_win)
    report = {"column": column, "windows": len(windows), "lam_unmix": lam_unmix, "lam_stage2": lam_stage2,
              "xstate_target": xstate_target, "d_mem": d_mem, "channels": {}}
    pkg_mounted_v = None
    for ch, sm_name in channels:
        sm = getattr(model, sm_name)
        z_all = torch.cat(cache[ch]["z"])
        vh_all = torch.cat(cache[ch]["vh"])
        pkg_all = torch.cat(cache[ch]["pkg"])
        u_all = torch.cat(cache[ch]["u"])
        if ch == "v":
            W_bridge = _ridge_solve(z_all, m_all, lam_stage2)  # 段2: v̂→m̂ (donor 真实 memory 行, Q19 D6)
            bridge_target = m_all
        else:
            W_bridge = _ridge_solve(z_all, pkg_all, lam_stage2)  # k 通道 Q19 段2 无对应物 (Q18-D3)
            bridge_target = pkg_all
        bridge_cos = row_cos(_q18_apply_linear(z_all, W_bridge), bridge_target)
        phi = _q18_chain_features(z_all, W_bridge, sm.realign[1].out_features)
        W_out = _ridge_solve(phi, pkg_all, lam_stage2)
        pkg_mounted = _q18_apply_linear(phi, W_out)
        _q18_mount_realign(sm, W_bridge, W_out)
        rel_l2 = float((pkg_mounted - pkg_all).norm() / pkg_all.norm().clamp(min=1e-12))
        report["channels"][ch] = {
            "cos_unmix": round(sum(cache[ch]["cos"]) / len(cache[ch]["cos"]), 4),  # Q19 段1 自带 cos(v̂,v)
            "stage1_cos_mounted_vs_vhat": round(row_cos(u_all, vh_all), 4),
            "bridge_cos": round(bridge_cos, 4),
            "package_cos": round(row_cos(pkg_mounted, pkg_all), 4),
            "package_rel_l2": round(rel_l2, 4),
        }
        if ch == "v":
            pkg_mounted_v = pkg_mounted
        print(
            f"[q18] 通道 {ch}: cos_unmix={report['channels'][ch]['cos_unmix']} "
            f"段1挂载 cos={report['channels'][ch]['stage1_cos_mounted_vs_vhat']} "
            f"桥 cos={report['channels'][ch]['bridge_cos']} "
            f"package cos={report['channels'][ch]['package_cos']} rel_l2={report['channels'][ch]['package_rel_l2']}",
            flush=True,
        )

    # decoder_in_mem 等价位置 (Q18-D4): composite ridge packagê → donor 端口输出
    if not isinstance(model.decoder_in, nn.Linear):
        raise ValueError("d 格 decoder_in 预期为 Linear (d_pack≠d_backbone)——decoder_in_mem 等价位置缺席, loud fail")
    target_di = donor.decoder_in_mem(m_all.to(device)).float().cpu()  # (N, d_backbone)
    W_di = _ridge_solve(pkg_mounted_v, target_di, lam_stage2)
    model.decoder_in.weight.data.copy_(W_di[: model.decoder_in.in_features].T.to(model.decoder_in.weight.dtype))
    model.decoder_in.bias.data.copy_(W_di[model.decoder_in.in_features].to(model.decoder_in.bias.dtype))
    report["decoder_in_cos"] = round(row_cos(_q18_apply_linear(pkg_mounted_v, W_di), target_di), 4)
    report["declared_deviations"] = DECLARED_DEVIATIONS
    print(f"[q18] decoder_in 复合 cos={report['decoder_in_cos']}", flush=True)
    return report


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--q18-arm", required=True, choices=["A", "Aprime"], help="A=预算终审 (从零 40K); Aprime=闭式温启动双列 (20K)")
    p.add_argument("--q18-warmstart", default="oracle", choices=["oracle", "natural"], help="A′ 列: oracle 态 / natural 态 (生产判词)")
    p.add_argument("--ckpt", default=BASE_RUN, help="Q15 正臂收官 ckpt (基座, run dir)")
    p.add_argument("--donor-ckpt", default=DONOR_RUN, help="A′ donor 端口 (b 格 v371, Q19 D1 方案)")
    p.add_argument("--run-id", default="")
    p.add_argument("--out-dir", default="")
    p.add_argument("--data-path", default="", help="默认继承基座 resolved_config 的 data_path")
    p.add_argument("--max-steps", type=int, default=0, help="0 = 臂默认 (A: 40K, A′: 20K)")
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--resume", action=argparse.BooleanOptionalAction, default=True)
    p.add_argument("--log-every", type=int, default=20)
    p.add_argument("--max-eval-batches", type=int, default=16)
    p.add_argument("--seq-len", type=int, default=0, help="0 = 继承基座 resolved_config (窗规格)")
    p.add_argument("--seed", type=int, default=0, help="0 = 继承基座 seed (42); A 臂 42/1/2")
    p.add_argument("--warmup-steps", type=int, default=200, help="任务书 §1: warmup 200 + cosine→0")
    p.add_argument("--q18-calib-windows", type=int, default=16, help="A′ 标定窗数 (16 = Q19 协议)")
    p.add_argument("--q18-zc-windows", type=int, default=8, help="零变化律自检窗数")
    p.add_argument("--q18-zc-threshold", type=float, default=_Q18_ZC_THRESHOLD)
    p.add_argument("--lam-unmix", type=float, default=1e-2, help="段1 ridge 解混 λ (Q19 同档)")
    p.add_argument("--lam-stage2", type=float, default=1.0, help="段2/收尾 ridge λ (相对预条件后, Q19 同档)")
    p.add_argument("--kda-impl", default="", choices=["", "torch", "fla"], help="2026-08-27 挂死急诊单: 远端 4090 fla chunk_kda 死锁 -> 远端链传 torch")
    p.add_argument("--q18-no-sieve", action="store_true", help="2026-08-27 楔死急诊单 B-2: 关先验筛 (Q17/Q18 训练器每步筛子前向与基座前向交错疑致 CUDA 楔死; A 臂终审读数不依赖筛子——先验地板已在册 0.03-0.05, 口径注记入册)")
    p.add_argument("--q18-xstate-target", action="store_true",
                   help="候选偏差 (默认关): oracle 列 package_target 取自然态生产行 (翻译挂载), 见 _q18_warmstart docstring")
    return p


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    args = build_parser().parse_args()
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    t0 = time.time()

    model, sieve_model, ns, base_step = q17._q17_load_models(Path(args.ckpt), device, kda_impl_override=args.kda_impl)
    if args.data_path:
        ns.data_path = args.data_path
    if args.seq_len:
        ns.seq_len = args.seq_len
        ns.stride = args.seq_len
    seed = args.seed or ns.seed
    max_steps = args.max_steps or (40_000 if args.q18_arm == "A" else 20_000)
    run_id = args.run_id or (
        f"v37ks_d_q18a_readout_wall_{max_steps // 1000}k_s{seed}_20260827"
        if args.q18_arm == "A"
        else f"v37ks_d_q18ap_{args.q18_warmstart}_{max_steps // 1000}k_s{seed}_20260827"
    )
    out_dir = Path(args.out_dir or f"checkpoints/{run_id}")
    out_dir.mkdir(parents=True, exist_ok=True)
    if ns.batch_size != 1:
        print(f"[q18] batch_size 覆写 {ns.batch_size} -> 1 (Q17 同款冻结)", flush=True)
        ns.batch_size = 1
    # LR 1e-3 (任务书 §1: 同任务同链, 终审变量是预算不是配方) — 覆盖基座 2e-4
    ns.lr = 1e-3
    (out_dir / "resolved_config.json").write_text(
        json.dumps(vars(ns), ensure_ascii=False, indent=2), encoding="utf-8"
    )

    if s1._BPE_TOKENIZER is None and getattr(ns, "mask_mode", "mixed") == "mixed":
        s1._load_bpe_tokenizer(ns.bpe_tokenizer_path)

    latest = out_dir / "latest.pt"
    resuming = bool(args.resume and latest.exists())

    # 链初始化: A = 固定种子从零 (Q17 修订 v1 足迹); A′ = 闭式温启动挂载
    warm_report = None
    if not resuming:
        if args.q18_arm == "A":
            q17._q17_reinit_readout_chain(model, ns, seed)
        else:
            donor, dns, donor_step = load_model(Path(args.donor_ckpt), device)
            # D1 接口断言 (Q19 同款, loud): donor 必须有 decoder_in_mem 且 v=memory
            if getattr(dns, "v_row_source", "") != "memory" or not hasattr(donor, "decoder_in_mem"):
                raise ValueError(f"{args.donor_ckpt}: donor 缺 decoder_in_mem (v_row_source={getattr(dns, 'v_row_source', None)!r})")
            if getattr(ns, "v_row_source", "") != "state":
                raise ValueError(f"{args.ckpt}: 预期 d 格 v_row_source='state', got {ns.v_row_source!r}")
            for k in ("max_chunks", "max_span"):
                if getattr(ns, k) != getattr(dns, k):
                    raise ValueError(f"base/donor {k} 不一致: {getattr(ns, k)} vs {getattr(dns, k)}")
            print(f"[q18] donor={Path(args.donor_ckpt).name} step={donor_step} ({time.time() - t0:.0f}s)", flush=True)
            warm_report = _q18_warmstart(
                model, donor, ns, device, args.q18_warmstart, args.q18_calib_windows, args.lam_unmix, args.lam_stage2,
                xstate_target=args.q18_xstate_target,
            )
            (out_dir / "warmstart_report.json").write_text(
                json.dumps(warm_report, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            del donor  # 标定完即释放 (16GB 显存纪律)
            if device.type == "cuda":
                torch.cuda.empty_cache()

    trainable = q17._q17_unfreeze_chain(model)
    n_train = sum(p_.numel() for p_ in trainable)
    print(
        f"[q18] arm={args.q18_arm} 基座={Path(args.ckpt).name} step={base_step} | "
        f"{'温启动 ' + args.q18_warmstart if args.q18_arm == 'Aprime' else f'从零重初始化'} "
        f"(seed={seed}), 可训练参数 {n_train} ({time.time() - t0:.0f}s)",
        flush=True,
    )

    # 抽签流 (任务书 §4 可复现): mask/burst 流与 Q17 同 discipline, 退火抽签流
    # 用 Q18 独立偏移; 先验筛参考模型 = 基座第二次独立加载 (固定, GPU 驻留, E101)
    def _seed_streams() -> None:
        s1._MASK_GENERATOR.manual_seed(seed)
        s1._BURST_GENERATOR.manual_seed(seed + s1._BURST_SEED_OFFSET)
        s1._BURST_SAMPLER = s1.CorpusSampler(ns.data_path)
        _Q18_GENERATOR.manual_seed(seed + _Q18_SEED_OFFSET)

    s1._BURST_SIEVE_MODEL = None if args.q18_no_sieve else sieve_model  # 楔死急诊单 B-2: --q18-no-sieve 时筛子卸载
    _seed_streams()

    # 零变化律自检 (A′, 任务书 §1 预注册; 考场口径修订 Q18-D7): 温启动后首步
    # fine 细格 acc (判官 = backbone 腿) 必须 >0.15, 不过响亮退出
    p_col = _q18_course_p(args.q18_arm, args.q18_warmstart, 0)
    if args.q18_arm == "Aprime" and not resuming:
        zc_mean, zc_accs = _q18_zero_change_check(
            model, ns, device, p_col, args.q18_zc_windows, args.q18_zc_threshold
        )
        warm_report["zero_change"] = {
            "threshold": args.q18_zc_threshold,
            "windows": args.q18_zc_windows,
            "metric": "fine 细格全槽 as-encoded acc, 判官=backbone 腿 (Q18-D7)",
            "backbone_accs": [round(a, 4) for a in zc_accs["backbone"]],
            "direct_accs": [round(a, 4) for a in zc_accs["direct"]],
            "mean": round(zc_mean, 4),
        }
        (out_dir / "warmstart_report.json").write_text(
            json.dumps(warm_report, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(
            f"[q18] 零变化律自检通过: 首步细格 acc(backbone)={zc_mean:.4f} > {args.q18_zc_threshold} "
            f"| direct 腿 {[round(a, 3) for a in zc_accs['direct']]}",
            flush=True,
        )
        _seed_streams()  # 检查后重 seed 训练流 (RNG 隔离声明落到实处)

    model.train()  # 读出链训练态; 前端参数仍全冻 (no-grad 前向)
    opt = s1.build_optimizer(ns, iter(trainable))
    sched = s1._cosine_with_warmup(opt, args.warmup_steps, max_steps)  # warmup 200 + cosine→0 (任务书 §1)
    train_loader, _eval_loader = s1.make_dataloaders(ns)

    start_step = 0
    if resuming:
        payload = torch.load(latest, map_location=device, weights_only=False)
        model.load_state_dict(payload["model"])  # resume 纪律照旧 (覆盖温启动/重初始化的链)
        opt.load_state_dict(payload["optimizer"])
        start_step = int(payload.get("step", 0))
        if start_step > 0:
            sched.step(start_step)
        print(f"[q18] resumed from step {start_step}", flush=True)

    log_path = out_dir / "train_log.jsonl"
    nan_skips = 0
    watchdog_skips = 0  # 步级看门狗计数 (挂死急诊单 2026-08-27; 入 log schema)
    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats()  # 显存峰值探针 (内存根治单): 只量训练循环段
    step = start_step
    pending: dict[str, float] = {}
    pending_n = 0
    pending_loss = 0.0
    while step < max_steps:
        for batch in train_loader:
            if step >= max_steps:
                break
            p = _q18_course_p(args.q18_arm, args.q18_warmstart, step)  # 课程断言: 恒定
            loss, metrics, step_sec, overrun = q17._watchdog_call(
                q17._q17_step, model, batch[0], ns, device, p, _Q18_GENERATOR
            )
            if loss is None or overrun:
                if overrun and loss is not None:
                    watchdog_skips += 1  # 该窗作废: 步进照走不参训, 不中断训练
                    print(
                        f"[q18] 看门狗: step {step} 单步 {step_sec:.0f}s > {q17._WATCHDOG_STEP_SEC:.0f}s, "
                        f"该窗作废不参训 (累计 {watchdog_skips})",
                        flush=True,
                    )
                step += 1  # echo 离网/看门狗: 步进照走, 不参训 (Q17 同款)
                sched.step()
                continue
            if not bool(torch.isfinite(loss)):
                nan_skips += 1
                opt.zero_grad(set_to_none=True)
                step += 1
                sched.step()
                continue
            opt.zero_grad(set_to_none=True)
            loss.backward()
            grad = torch.nn.utils.clip_grad_norm_(trainable, ns.grad_clip)
            opt.step()
            sched.step()
            step += 1
            pending_loss += float(loss)
            for k, v in metrics.items():
                pending[k] = pending.get(k, 0.0) + v
            pending_n += 1
            if step % args.log_every == 0 or step == 1:
                row = {
                    "step": step,
                    "lr": float(opt.param_groups[0]["lr"]),
                    "grad": float(grad.item()),
                    "steps_per_sec": step / max(time.time() - t0, 1e-9),
                    "nan_skips": nan_skips,
                    "watchdog_step_skip": watchdog_skips,
                    "loss": pending_loss / max(pending_n, 1),
                    **{k: v / max(pending_n, 1) for k, v in pending.items()},
                    "q18_arm": args.q18_arm,
                    "q18_seed": seed,
                }
                if args.q18_arm == "Aprime":
                    row["q18_warmstart"] = args.q18_warmstart
                s1._append_jsonl(log_path, row)
                pending = {}
                pending_n = 0
                pending_loss = 0.0
                s1._burst_yield_alarm(step, row.get("burst_yield", 1.0))  # Q14 纪律沿用
                print(
                    f"[q18] step {step} p={row['p']} loss={row['loss']:.4f} "
                    f"echo_acc={row.get('echo_byte_acc', 0.0):.4f} "
                    f"α_k={row.get('alpha_k', 0.0):.4f} α_v={row.get('alpha_v', 0.0):.4f}",
                    flush=True,
                )
            if step % 500 == 0:
                # 楔死急诊单 B-3 (2026-08-27): 分配器碎片累积假说的对照修复——
                # 周期 empty_cache (二分复现 L1/L2 实测 0.3-0.5MB/步缓爬,
                # 历史楔点 5780-6380 ~ 外推 2-3GB 增量入爬行阈); 证据充分前按
                # "候选修复"注册, 40K 不楔为治愈终证.
                torch.cuda.empty_cache()
                torch.save(
                    {"step": step, "model": model.state_dict(), "optimizer": opt.state_dict(),
                     "args": vars(args)},
                    latest,
                )
            if step % _Q18_MILESTONE_STEPS == 0:
                torch.save(
                    {"step": step, "model": model.state_dict(), "args": vars(args)},
                    out_dir / f"step_{step:06d}.pt",
                )

    torch.save(
        {"step": step, "model": model.state_dict(), "optimizer": opt.state_dict(), "args": vars(args)},
        latest,
    )

    # 收官 eval (Q17 条件 3 参照列): codec 双指标, s1.evaluate 同形态; Q15 管束
    # 随 ns 口径同开。收官 run dir (resolved_config 照抄基座 + latest.pt 全模型
    # state_dict + train_log.jsonl + summary.json) 可被 probe_burst_route_q15
    # --ckpt 直接加载——natural 列收官即 Δ 考场的加载对象。
    eval_stats = {}
    if args.max_eval_batches > 0:
        ns.max_eval_batches = args.max_eval_batches  # CLI 覆写 (冒烟 1 批)
        eval_stats = s1.evaluate(model, _eval_loader, ns, device)
    summary = {
        "run_id": run_id,
        "steps": step,
        "params": sum(p_.numel() for p_ in model.parameters()),
        "elapsed_sec": time.time() - t0,
        "steps_per_sec": step / max(time.time() - t0, 1e-9),
        "nan_skips": nan_skips,
        "watchdog_step_skip": watchdog_skips,
        "cuda_max_mem_gb": round(torch.cuda.max_memory_allocated() / 1e9, 3) if device.type == "cuda" else None,
        "args": vars(args),
        "q18_arm": args.q18_arm,
        "q18_seed": seed,
        "base_ckpt": str(args.ckpt),
        "base_step": base_step,
        **eval_stats,
    }
    if args.q18_arm == "Aprime":
        summary["q18_warmstart"] = args.q18_warmstart
        summary["warmstart_report"] = warm_report
        summary["declared_deviations"] = DECLARED_DEVIATIONS
    (out_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
