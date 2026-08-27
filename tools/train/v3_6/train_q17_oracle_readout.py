"""Q17 oracle 状态读出训练臂（任务书 2026-08-25 冻结:
docs/versions/v3_7/FLUED_V3_7_Q17_ORACLE_READOUT_20260825_CN.md —— §1/§2 是
施工合同, 逐条照做）。

存在性证明 / 锁 v2 判死实验: 基座 = Q15 正臂收官 ckpt（d 格）, 编码器/写头/
KDA 递推全冻 no-grad; 从零重初始化（固定种子, 与 __init__ 同分布 = 新建
同种子模型取链权重）并只训读出链: readout_query×2 + realign×2（修订 v1
补列, 读出投影本体, 同一足迹从零）+ backbone 全部（含 align_k/align_v）
+ decoder_in/decoder_in_mem + decoder。逐窗: 冻结前端的 gates（index/memory
经 write_head）→
同一 fp32 参考循环同时产出自然态 S_nat（KDA 递推, probe_oracle_write_verdict
trained_states 同款数学）与 oracle 态 S_or = Σ_{j≤i} k_j v_jᵀ（无衰减无
delta, oracle_states 同款）→ α 缩放（条件 2: α = median_i‖S_nat,i‖_F /
median_i‖S_or,i‖_F 逐窗逐通道, α 落日志）→ 退火档位 p 抽签（专用
generator 固定顺序, 同一窗双通道同取）→ 可训练 readout_query 读出（镜像
KDAStateMachine 读出数学）→ K~/V~ 行 → backbone（压缩区剔除
s1._burst_store_block 照常）→ decoder → echo CE（唯一损失; codec 不参训）。

任务管束 = Q15 同款: burst R=3 + 末 2-4 CJK 字符遮蔽 + 先验筛保留（参考模型
= 基座 ckpt 第二次独立加载, 固定, GPU 驻留 -- E101 教训）+ 产出率入册
（Q14 纪律: <70% 报警）。退火课程（预注册档位, 禁止中途改）: p ∈ {1.0,
0.75, 0.5, 0.25, 0.0} 每档 2K 共 10K; LR 1e-3 + warmup 100 + cosine→0;
batch=1, 窗规格继承基座 resolved_config。里程碑每 2K（档位切换点）
step_*.pt; latest.pt 带 optimizer（resume 纪律照旧）。收官: run dir
（resolved_config.json 照抄基座 + latest.pt 全模型 state_dict +
train_log.jsonl + summary.json）必须能被 probe_burst_route_q15 --ckpt 直接
加载; codec 双指标收官 eval 测读作参照列（s1.evaluate 同形态, 自然路径）。

口径注记（入册）: 自然态用 fp32 torch 参考递推（E73 同款口径）, 与基座训练
时的 fla kernel 数值有已知口径差（E-a 注记）——读出链反正从零重训, Q17
内部一致性不受影响; decoder_in/decoder_in_mem 重初始化后无对应损失（codec
不参训）, 收官 eval 的 direct 列预期近随机, 参照列的有效部分是 completion。

Usage:
  python tools/train/v3_6/train_q17_oracle_readout.py --device cuda \
      --ckpt checkpoints/v37ks_d_sm_q15_circuit_20k_ctx4096_20260825b \
      --out-dir checkpoints/v37ks_d_q17_oracle_readout_10k_20260825
  CPU 冒烟: py -3.14 -X utf8 tools/train/v3_6/train_q17_oracle_readout.py \
      --device cpu --max-steps 3 --seq-len 512 --max-eval-batches 1 \
      --ckpt checkpoints/v37ks_d_sm_q15_circuit_20k_ctx4096_20260825b \
      --out-dir checkpoints/_smoke_q17_cpu
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from argparse import Namespace
from pathlib import Path

import torch
import torch.nn.functional as F

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from flued.data import MASK_ID, PAD_ID  # noqa: E402
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402
from tools.train.v3_6.train_v36 import build_model  # noqa: E402

# 退火课程 (任务书 §1 预注册档位, 禁止中途改): p 每档 2K 步共 10K
_Q17_TIERS = (1.0, 0.75, 0.5, 0.25, 0.0)
_Q17_TIER_STEPS = 2000
# 退火抽签专用 generator (任务书 §4: 抽签流全部可复现): 独立种子偏移, 与
# burst/掩码流不混; 每窗一抽, 固定顺序.
_Q17_GENERATOR = torch.Generator()
_Q17_SEED_OFFSET = 101_033
# 读出链范围 (任务书 §1): 这些模块固定种子重初始化 + 训练; 其余全冻.
_Q17_CHAIN_MODULES = ("backbone", "decoder", "decoder_in", "decoder_in_mem")
_Q17_CHAIN_SMS = ("state_machine", "state_machine_k")  # 重训 readout_query + realign (修订 v1)


# 步级看门狗 (Q18 挂死急诊单 2026-08-27: 双机训练链反复挂死/病态变慢——单步
# 墙钟超阈值即作废该窗, 保证活性; Q17/Q18 两主循环共用本段, 计数入 log schema)
_WATCHDOG_STEP_SEC = 300.0


def _watchdog_call(fn, *args, threshold: float = _WATCHDOG_STEP_SEC, clock=None):
    """步级看门狗包装 (Q18 挂死急诊单 2026-08-27): 计 fn(*args) 墙钟。
    Returns (loss, metrics, elapsed, overrun); overrun=True 时调用侧按
    "echo 离网" 同款处理——步进照走不参训 (loss 未 backward 无梯度残留),
    计 watchdog_step_skip 入 log 行, 不中断训练。"""
    clock = clock or time.time
    t0 = clock()
    loss, metrics = fn(*args)
    elapsed = clock() - t0
    return loss, metrics, elapsed, elapsed > threshold


def _q17_anneal_p(step: int, tier_steps: int = _Q17_TIER_STEPS) -> float:
    """退火档位表 (任务书 §1): step // 2000 索引 {1.0, 0.75, 0.5, 0.25, 0.0},
    超界钳到末档."""
    return _Q17_TIERS[min(step // tier_steps, len(_Q17_TIERS) - 1)]


def _q17_states_dual(gates: dict, chunk_mask: torch.Tensor):
    """逐 chunk 自然态 S_nat 与 oracle 态 S_or, 同一 fp32 参考递推
    (probe_oracle_write_verdict trained_states / oracle_states 同款数学;
    padded chunk = 恒等步, 不入累计). Returns (S_nat, S_or), 各 (B, C, H,
    hk, hv) float32.

    向量化 (Q18 挂死急诊单 2026-08-27: 双机训练链在本函数反复挂死——主线程
    100% CPU 空转 + GPU 忙 + 日志 30-50min 不动, faulthandler SIGABRT 取证;
    根因候选 = 逐 chunk ~12 个小 kernel 的 launch 风暴触发驱动级病态;
    KDAStateMachine._forward_torch/fla 只暴露逐 chunk 读出 q·S_i 不暴露状态
    本体, 无单源可复用, 故保留递推但合并 kernel):
    oracle 态 = keep 遮罩后 k⊗v 的纯 cumsum (一行; padded 已清零 = 零贡献 =
    态不变, 与原循环同数学); natural 态 KDA delta 递推有顺序依赖不能 cumsum,
    每 chunk 合并为 5 个大 kernel (decay 乘 / kTs einsum / 减 / delta 写
    einsum / 加), erase+write 合并为单 einsum —— S + b·k⊗(v−kᵀS) 与原
    "−b·k⊗kTs 再 +b·k⊗v" 三步代数等价。数值与原循环 1e-5 内一致
    (tests/test_q17_oracle_readout.py::test_states_dual_vectorized_matches_legacy_loop
    以原循环为参照守卫; 既有 1e-6 手算断言不受影响)。"""
    keep = chunk_mask.float()
    keep4 = keep.unsqueeze(-1).unsqueeze(-1)  # (B, C, 1, 1) for k/v (B, C, H, d)
    k = gates["k"].float() * keep4
    v = gates["v"].float() * keep4
    beta = gates["beta"].float() * keep.unsqueeze(-1)  # (B, C, H) <- (B, C, 1)
    bsz, chunks, heads, hk = k.shape
    hv = v.size(-1)
    a = gates["alpha"][0].float().unsqueeze(-1)  # (1, H, hk, 1) per-channel decay
    # padded chunk = 恒等步 (model.py _forward_torch 同款): alpha_eff=1, beta=0
    a_eff = 1.0 - keep.view(-1, chunks, 1, 1, 1) + keep.view(-1, chunks, 1, 1, 1) * a
    # oracle 态: 无衰减无 delta 的纯累计叠加 = 遮罩后外积的 cumsum (单行)
    S_or = torch.einsum("bchk,bchv->bchkv", k, v).cumsum(dim=1)
    # 自然态: KDA 递推 (衰减 + delta 擦除/写入合并)
    S_nat = k.new_zeros(bsz, heads, hk, hv, dtype=torch.float32)
    outs_nat = []
    for i in range(chunks):
        ki, vi, bi = k[:, i], v[:, i], beta[:, i]
        S_nat = a_eff[:, i] * S_nat
        kTs = torch.einsum("bhk,bhkv->bhv", ki, S_nat)
        S_nat = S_nat + torch.einsum("bh,bhk,bhv->bhkv", bi, ki, vi - kTs)
        outs_nat.append(S_nat)
    return torch.stack(outs_nat, dim=1), S_or


def _q17_alpha_scale(S_nat: torch.Tensor, S_or: torch.Tensor, chunk_mask: torch.Tensor):
    """范数尺度匹配 (任务书 §1 条件 2, 冻结公式): α = median_i‖S_nat,i‖_F /
    median_i‖S_or,i‖_F 逐窗逐通道 (只统计有效 chunk); S_or 乘 α 后进出链.
    Returns (S_or_scaled, alpha (B,))."""
    norms_nat = S_nat.norm(dim=(-2, -1))  # (B, C)
    norms_or = S_or.norm(dim=(-2, -1))
    alpha = []
    for b in range(S_nat.size(0)):
        m = chunk_mask[b]
        nn = norms_nat[b][m].median()
        no = norms_or[b][m].median().clamp(min=1e-12)
        alpha.append(nn / no)
    alpha = torch.stack(alpha)
    return S_or * alpha.view(-1, 1, 1, 1, 1), alpha


def _q17_readout(sm, S: torch.Tensor) -> torch.Tensor:
    """可训练读出 (镜像 KDAStateMachine 的读出数学, 单源复用): read =
    einsum(readout_query, S) → reshape → realign. S 无梯度 (状态不经梯度);
    readout_query 与 realign 都在链上带梯度 (任务书 §1 修订 v1: realign 是
    读出投影本体, 同一足迹从零). Returns package (B, C, nq, d_pack)."""
    q = sm.readout_query.float()
    read = torch.einsum("qhk,bchkv->bcqhv", q, S.float())
    read = read.reshape(S.size(0), S.size(1), q.size(0), -1)
    w_dtype = next(sm.realign.parameters()).dtype
    return sm.realign(read.to(w_dtype))


def _q17_reinit_readout_chain(model, ns, seed: int) -> None:
    """固定种子重初始化读出链 (任务书 §1 修订 v1): 与 __init__ 同分布 -- 新建
    同种子模型取其链权重 (可复现; 全局 RNG 先存后还). 范围: backbone 全部
    (含 align_k/align_v), decoder_in, decoder_in_mem, decoder, 双状态机的
    readout_query 与 realign (读出投影本体, model.py:613; 修订 v1 补列 --
    条件 1 的单变量对照要求同一足迹从零, 留它冻结等于链里留一段共适应史);
    按格裁剪缺席模块 (d 格无 decoder_in_mem, a/b 格无 state_machine_k --
    跳过了了之, 链范围以存在者为准). 其余全部保持基座值. 调用侧负责先冻结
    再解冻.

    tied-embedding 护栏 (实跑核实): decoder.byte_lookup 与模型级 byte_lookup
    是同一参数 (model.py:2086 共享构造) -- 任务书冻结面 "byte/encoder 全部
    不动" 覆盖它: 链拷贝后把 byte_lookup 状态回写基座值 (经共享参数同时还原
    decoder 侧视图)."""
    byte_state = {k: v.clone() for k, v in model.byte_lookup.state_dict().items()}
    rng = torch.get_rng_state()
    torch.manual_seed(seed)
    fresh = build_model(ns)  # CPU, 与 __init__ 同分布
    torch.set_rng_state(rng)
    for name in _Q17_CHAIN_MODULES:
        if hasattr(model, name):
            getattr(model, name).load_state_dict(getattr(fresh, name).state_dict())
    for name in _Q17_CHAIN_SMS:
        if hasattr(model, name):
            sm = getattr(model, name)
            sm_fresh = getattr(fresh, name)
            sm.readout_query.data.copy_(sm_fresh.readout_query.data)
            sm.realign.load_state_dict(sm_fresh.realign.state_dict())  # 修订 v1
    model.byte_lookup.load_state_dict(byte_state)  # tied 护栏: 回写基座值
    del fresh


def _q17_load_models(run_dir: Path, device: torch.device, kda_impl_override: str = ""):
    """基座加载 (任务书 §1): Q15 收官 ckpt 全模型构建 + latest.pt strict;
    先验筛参考模型 = 同一 ckpt 第二次独立加载 (固定, GPU 驻留 -- E101 教训).
    Returns (model, sieve_model, ns, step); 两者全部参数 requires_grad False
    (model 的读出链由调用侧重初始化后解冻). kda_impl_override: 2026-08-27 挂死
    急诊单——远端 4090 (triton 3.8/torch 2.15/sm_89) 上 fla chunk_kda 死锁,
    传 "torch" 强制参考实现 (口径注记: 与 fla 有已知数值差, 跨机种子读数按
    机器分档注册)."""
    cfg = json.loads((run_dir / "resolved_config.json").read_text(encoding="utf-8"))
    cfg["data_manifest"] = ""
    if device.type != "cuda" or kda_impl_override:
        cfg["kda_impl"] = kda_impl_override or "torch"  # fla kernels are GPU-only
    ns = Namespace(**cfg)
    payload = torch.load(run_dir / "latest.pt", map_location=device, weights_only=False)
    model = build_model(ns).to(device)
    model.load_state_dict(payload["model"], strict=True)
    sieve = build_model(ns).to(device)
    sieve.load_state_dict(payload["model"], strict=True)
    for m in (model, sieve):
        for p_ in m.parameters():
            p_.requires_grad_(False)
        m.eval()
    return model, sieve, ns, int(payload.get("step", 0))


def _q17_unfreeze_chain(model) -> list:
    """解冻读出链, 返回可训练参数列表 (optimizer 只含这些; 按格裁剪缺席
    模块, 与 _q17_reinit_readout_chain 同规则; realign 在链上 -- 修订 v1)."""
    trainable = []
    for name in _Q17_CHAIN_MODULES:
        if hasattr(model, name):
            for p_ in getattr(model, name).parameters():
                p_.requires_grad_(True)
                trainable.append(p_)
    for name in _Q17_CHAIN_SMS:
        if hasattr(model, name):
            sm = getattr(model, name)
            for p_ in [sm.readout_query, *sm.realign.parameters()]:
                p_.requires_grad_(True)
                trainable.append(p_)
    return trainable


@torch.no_grad()
def _q17_encode_and_states(model, source: torch.Tensor):
    """冻结前端 (no-grad): masked source → chunks → memory/index → 双通道
    gates → 双通道 (S_nat, S_or) + α 缩放. Returns dict."""
    byte_states, confidence, valid, _ = model._encode(source)
    hard_cut, utf8_cont, _ = model._cuts(source, confidence, valid)
    chunks = model.chunk_builder(byte_states, valid, hard_cut, confidence)
    chunks = model.bridge(chunks, byte_states, confidence, valid, utf8_cont)
    memory, index = model.summarizer.forward_with_index(chunks.span_embeddings, chunks.token_mask)
    gates_k = model.write_head_k(index)  # K 通道: index gates (d 格)
    gates_v = model.write_head(memory)  # V 通道: memory gates
    sn_k, so_k = _q17_states_dual(gates_k, chunks.chunk_mask)
    sn_v, so_v = _q17_states_dual(gates_v, chunks.chunk_mask)

    def _med_norm(S):
        n = S.norm(dim=(-2, -1))  # (B, C)
        return torch.stack([n[b][chunks.chunk_mask[b]].median() for b in range(S.size(0))])

    # oracle/自然分列的 state_norm 用缩放前的原始范数 (缩放后两者按构造
    # 中位相等, 无信息量); α 列单独示缩放系数
    snorm_k_or_raw, snorm_v_or_raw = _med_norm(so_k), _med_norm(so_v)
    snorm_k_nat, snorm_v_nat = _med_norm(sn_k), _med_norm(sn_v)
    so_k, alpha_k = _q17_alpha_scale(sn_k, so_k, chunks.chunk_mask)
    so_v, alpha_v = _q17_alpha_scale(sn_v, so_v, chunks.chunk_mask)

    return {
        "chunks": chunks,
        "sn_k": sn_k, "so_k": so_k, "sn_v": sn_v, "so_v": so_v,
        "alpha_k": alpha_k, "alpha_v": alpha_v,
        "snorm_k_nat": snorm_k_nat, "snorm_k_or": snorm_k_or_raw,
        "snorm_v_nat": snorm_v_nat, "snorm_v_or": snorm_v_or_raw,
    }


def _q17_stream_channel(sm, gates: dict, chunk_mask: torch.Tensor, used_t: torch.Tensor):
    """流式单通道读出 (内存压力根治单 2026-08-27: 主会话十次周期堆栈转储
    定罪——"楔死"实为内存压力下的减速爬行; 旧训练路径 (_q17_encode_and_states
    + _q17_readout) 把全窗逐 chunk 状态矩阵 S_i (各 (B,H,hk,hv) fp32) 累积入
    列表再 torch.stack, C≈64-700 时单步瞬态 ~0.7-1.5GB×2 通道, 16GB 卡被打进
    分配器爬行态; s1 生产训练器 fla chunk kernel 不物化全窗状态故从不犯)。

    本函数结构消灭该瞬态: 递推循环只驻留当前 S_nat/S_or (O(1) 驻留, no_grad),
    逐 chunk 收集四族范数标量列 (metrics) 并立即用可训练 readout_query 算
    读出行 (梯度只经 query/realign; S_i 无梯度, python 侧即用即弃——注意
    autograd 为 query 的反向仍会暂存选中族 S_i (每窗每通道 ~256MB 级, 较旧
    路径 GB 级列表+stack 复制降 5-6 倍; 进一步的 O(1) 化需分块 checkpoint,
    留作后手)。收集 reads (B,C,nq,H*hv) ≈2MB/窗而非状态本体。

    等价性注记: α 范数匹配施加于读出行 (读出对状态线性, 先读后缩放与旧
    "先缩放 S 后读"数值等价; realign 首层 LayerNorm 对正标量行缩放不变,
    双保险); realign 在窗口级一次调用 (LayerNorm 无跨行耦合, 逐行 = 逐 chunk
    等价); padded chunk 恒等步语义与原循环同 (keep 遮罩原样); batch=1 冻结
    路径只读选中族, B>1 读双族再 where (语义同旧 where)。parity 由
    tests/test_q17_oracle_readout.py::test_stream_channel_package_parity
    守卫 (1e-5, 生产域 gates)。Returns dict: reads (B,C,nq,H*hv) 带梯度 /
    alpha (B,) / snorm_nat / snorm_or (B,) 中位范数列 (口径同旧 _med_norm:
    缩放前原始范数, 有效 chunk×head 全集中位)。"""
    keep = chunk_mask.float()
    keep4 = keep.unsqueeze(-1).unsqueeze(-1)  # (B, C, 1, 1) for k/v (B, C, H, d)
    k = gates["k"].float() * keep4
    v = gates["v"].float() * keep4
    beta = gates["beta"].float() * keep.unsqueeze(-1)  # (B, C, H)
    bsz, chunks, heads, hk = k.shape
    hv = v.size(-1)
    a = gates["alpha"][0].float().unsqueeze(-1)  # (1, H, hk, 1) per-channel decay
    # padded chunk = 恒等步 (model.py _forward_torch 同款): alpha_eff=1, beta=0
    a_eff = 1.0 - keep.view(-1, chunks, 1, 1, 1) + keep.view(-1, chunks, 1, 1, 1) * a
    q = sm.readout_query.float()  # 链上参数: 读出在 no_grad 外, 梯度经 query
    single = bsz == 1  # batch=1 冻结 (任务书): 抽签逐窗单值, 只读选中族
    sel = bool(used_t[0]) if single else None
    S_nat = k.new_zeros(bsz, heads, hk, hv, dtype=torch.float32)
    S_or = torch.zeros_like(S_nat)
    norms_nat, norms_or, reads_nat, reads_or = [], [], [], []
    for i in range(chunks):
        ki, vi, bi = k[:, i], v[:, i], beta[:, i]  # 视图, 无 kernel
        with torch.no_grad():
            # 自然态: KDA 递推 (衰减 + delta 擦除/写入合并, 向量化单同款)
            S_nat = a_eff[:, i] * S_nat
            kTs = torch.einsum("bhk,bhkv->bhv", ki, S_nat)
            S_nat = S_nat + torch.einsum("bh,bhk,bhv->bhkv", bi, ki, vi - kTs)
            # oracle 态: 无衰减无 delta 的纯累计叠加
            S_or = S_or + ki.unsqueeze(-1) * vi.unsqueeze(-2)
            norms_nat.append(S_nat.norm(dim=(-2, -1)))  # (B, H)
            norms_or.append(S_or.norm(dim=(-2, -1)))
        if sel is None or sel:
            reads_or.append(torch.einsum("qhk,bhkv->bqhv", q, S_or).reshape(bsz, q.size(0), -1))
        if sel is None or not sel:
            reads_nat.append(torch.einsum("qhk,bhkv->bqhv", q, S_nat).reshape(bsz, q.size(0), -1))
    nn = torch.stack(norms_nat, dim=1)  # (B, C, H)
    no_ = torch.stack(norms_or, dim=1)
    med_nat = torch.stack([nn[b][chunk_mask[b]].median() for b in range(bsz)])
    med_or = torch.stack([no_[b][chunk_mask[b]].median() for b in range(bsz)])
    alpha = med_nat / med_or.clamp(min=1e-12)  # 冻结公式 (_q17_alpha_scale 同款)
    if sel is None:
        rn = torch.stack(reads_nat, dim=1)  # (B, C, nq, H*hv)
        ro = torch.stack(reads_or, dim=1) * alpha.view(-1, 1, 1, 1)
        reads = torch.where(used_t.view(-1, 1, 1, 1), ro, rn)
    else:
        reads = torch.stack(reads_or if sel else reads_nat, dim=1)
        if sel:
            reads = reads * alpha.view(-1, 1, 1, 1)
    return {"reads": reads, "alpha": alpha, "snorm_nat": med_nat, "snorm_or": med_or}


def _q17_stream_encode(model, source: torch.Tensor, p: float, gen: torch.Generator):
    """流式训练步编码 (内存压力根治单 2026-08-27): 冻结前端与旧
    _q17_encode_and_states 逐行同 (no-grad); 退火抽签提前到读出前 (专用
    generator 每窗仍恰一抽/行, 抽签流与旧顺序逐比特一致); 双通道走
    _q17_stream_channel; realign 窗口级一次。Returns dict: chunks / used_t /
    package_k / package_v (带梯度, (B,C,nq,d_pack)) / alpha_k / alpha_v /
    snorm_{k,v}_{nat,or} (各 (B,) 中位范数列, 口径同旧)。"""
    with torch.no_grad():
        byte_states, confidence, valid, _ = model._encode(source)
        hard_cut, utf8_cont, _ = model._cuts(source, confidence, valid)
        chunks = model.chunk_builder(byte_states, valid, hard_cut, confidence)
        chunks = model.bridge(chunks, byte_states, confidence, valid, utf8_cont)
        memory, index = model.summarizer.forward_with_index(chunks.span_embeddings, chunks.token_mask)
        gates_k = model.write_head_k(index)  # K 通道: index gates (d 格)
        gates_v = model.write_head(memory)  # V 通道: memory gates
    # 退火抽签 (任务书 §1: 逐窗, 同一窗双通道同取; 专用 generator 固定顺序)
    used_t = torch.tensor(
        [float(torch.rand((), generator=gen)) < p for _ in range(source.size(0))],
        dtype=torch.bool, device=source.device,
    )
    out = {"chunks": chunks, "used_t": used_t}
    for tag, sm, gates in (("k", model.state_machine_k, gates_k), ("v", model.state_machine, gates_v)):
        r = _q17_stream_channel(sm, gates, chunks.chunk_mask, used_t)
        w_dtype = next(sm.realign.parameters()).dtype
        out[f"package_{tag}"] = sm.realign(r["reads"].to(w_dtype))  # LN 无跨行耦合: 逐行=逐 chunk 等价
        out[f"alpha_{tag}"] = r["alpha"]
        out[f"snorm_{tag}_nat"] = r["snorm_nat"]
        out[f"snorm_{tag}_or"] = r["snorm_or"]
    return out


def _q17_step(model, clean: torch.Tensor, ns, device, p: float, gen: torch.Generator):
    """One training step (batch=1 窗规格继承基座): burst splice (筛子) →
    冻结前端 + 流式双通道读出 (内存压力根治单 2026-08-27, 见
    _q17_stream_encode; 梯度只经读出链) → echo CE. Returns
    (loss_or_None, metrics dict)."""
    stats = {"drawn": 0, "spliced": 0, "sieve_measured": 0, "sieve_rejected": 0}
    clean, metas = s1._splice_burst(
        clean, float(getattr(ns, "burst_prob", 1.0)), s1._BURST_GENERATOR, s1._BURST_SAMPLER,
        s1._BURST_REPEAT_FROZEN, s1._BURST_TAIL_MAX_CHARS,
        sieve_model=s1._BURST_SIEVE_MODEL,  # 先验筛保留 (任务书 §1; 参考模型固定)
        stats=stats,
    )
    clean = clean.to(device)
    valid = clean.ne(PAD_ID)
    if getattr(ns, "mask_mode", "mixed") == "mixed":
        byte_mask = s1.make_mixed_mask(
            clean.cpu(), ns.mask_prob, char_frac=getattr(ns, "mask_char_frac", 0.4),
            char_span_max=getattr(ns, "mask_char_span_max", 3),
            tokenizer=s1._BPE_TOKENIZER, generator=s1._MASK_GENERATOR,
        ).to(device)
    else:
        byte_mask = s1.make_byte_mask(valid, ns.mask_prob, ns.mask_span_min, ns.mask_span_max)
    byte_mask = s1._burst_mask_overrides(byte_mask, metas)
    source = clean.masked_fill(byte_mask, MASK_ID)
    enc = _q17_stream_encode(model, source, p, gen)
    chunks = enc["chunks"]
    used_t = enc["used_t"]
    # 读出链 (带梯度): readout_query → realign → K~/V~ 行 → backbone → decoder
    package_k = enc["package_k"]
    package_v = enc["package_v"]
    k_rows = package_k.mean(dim=2)  # (B, C, d_pack)
    v_rows = package_v.mean(dim=2)
    n_chunks = chunks.chunk_mask.size(1)
    pos = model.chunk_pos.weight.unsqueeze(0)[:, :n_chunks]
    # 压缩区剔除照常 (Q15 同管束): occurrences 1..R-1 的 store 行档 a 剔除
    block = s1._burst_store_block(metas, chunks)
    backbone_out = model.backbone(k_rows, v_rows, chunks.chunk_mask, pos, store_block=block)
    logits = model.decoder(backbone_out + pos, chunks.token_mask)
    slot, active = s1._cloze_slot_grid(
        metas, chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
    )
    if not bool(active.any()):
        return None, {
            "echo_byte_acc": 0.0, "echo_exact": 0.0,
            "echo_count": 0.0, "burst_yield": stats["spliced"] / stats["drawn"] if stats["drawn"] else 1.0,
            "sieve_reject_rate": stats["sieve_rejected"] / stats["sieve_measured"] if stats["sieve_measured"] else 0.0,
            "p": p, "oracle_frac": float(used_t.float().mean()),
            "alpha_k": float(enc["alpha_k"].mean()), "alpha_v": float(enc["alpha_v"].mean()),
            "snorm_k_nat": float(enc["snorm_k_nat"].mean()), "snorm_k_or": float(enc["snorm_k_or"].mean()),
            "snorm_v_nat": float(enc["snorm_v_nat"].mean()), "snorm_v_or": float(enc["snorm_v_or"].mean()),
        }
    targets, _sm, _m2 = s1.make_targets(
        clean, torch.zeros_like(byte_mask), chunks.chunk_ids, chunks.offsets,
        ns.max_chunks, ns.max_span,
    )
    loss = s1._ce(logits, targets, slot)  # 唯一损失: echo CE (codec 不参训)
    pred = logits.argmax(dim=-1)
    hit = pred.eq(targets) & slot
    byte_acc = hit.float().sum() / slot.float().sum().clamp(min=1.0)
    exact_per = (hit | ~slot).flatten(1).all(dim=1) & active
    return loss, {
        "echo_byte_acc": float(byte_acc),  # 点火判据读数 (§3: p=1.0 段 >0.30)
        "echo_exact": float(exact_per.float().sum() / active.float().sum().clamp(min=1.0)),
        "echo_count": float(active.float().mean()),
        "burst_yield": stats["spliced"] / stats["drawn"] if stats["drawn"] else 1.0,
        "sieve_reject_rate": stats["sieve_rejected"] / stats["sieve_measured"] if stats["sieve_measured"] else 0.0,
        "p": p, "oracle_frac": float(used_t.float().mean()),
        "alpha_k": float(enc["alpha_k"].mean()), "alpha_v": float(enc["alpha_v"].mean()),
        "snorm_k_nat": float(enc["snorm_k_nat"].mean()), "snorm_k_or": float(enc["snorm_k_or"].mean()),
        "snorm_v_nat": float(enc["snorm_v_nat"].mean()), "snorm_v_or": float(enc["snorm_v_or"].mean()),
    }


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--ckpt", default="checkpoints/v37ks_d_sm_q15_circuit_20k_ctx4096_20260825b",
                   help="Q15 正臂收官 ckpt (基座, run dir)")
    p.add_argument("--run-id", default="v37ks_d_q17_oracle_readout_10k_20260825")
    p.add_argument("--out-dir", default="checkpoints/v37ks_d_q17_oracle_readout_10k_20260825")
    p.add_argument("--data-path", default="", help="默认继承基座 resolved_config 的 data_path")
    p.add_argument("--max-steps", type=int, default=10_000)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--resume", action=argparse.BooleanOptionalAction, default=True)
    p.add_argument("--log-every", type=int, default=20)
    p.add_argument("--max-eval-batches", type=int, default=16)
    p.add_argument("--seq-len", type=int, default=0, help="0 = 继承基座 resolved_config (窗规格)")
    p.add_argument("--seed", type=int, default=0, help="0 = 继承基座 seed")
    return p


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    args = build_parser().parse_args()
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    t0 = time.time()

    model, sieve_model, ns, base_step = _q17_load_models(Path(args.ckpt), device)
    if args.data_path:
        ns.data_path = args.data_path
    if args.seq_len:
        ns.seq_len = args.seq_len
        ns.stride = args.seq_len
    seed = args.seed or ns.seed
    # batch=1 (任务书 §1 冻结); 窗规格继承基座 resolved_config
    if ns.batch_size != 1:
        print(f"[q17] batch_size 覆写 {ns.batch_size} -> 1 (任务书 §1 冻结)", flush=True)
        ns.batch_size = 1
    _q17_reinit_readout_chain(model, ns, seed)  # 固定种子, 与 __init__ 同分布
    trainable = _q17_unfreeze_chain(model)
    model.train()  # 读出链训练态; 前端参数仍全冻 (no-grad 前向)
    # LR 1e-3 + warmup 100 + cosine→0 (任务书 §1 冻结配方; 状态不经梯度,
    # 无 E103 风险面) -- 覆盖基座 resolved_config 的 2e-4
    ns.lr = 1e-3
    print(
        f"[q17] 基座={Path(args.ckpt).name} step={base_step} | 读出链重初始化 "
        f"(seed={seed}), 可训练参数 {sum(p_.numel() for p_ in trainable)} "
        f"({time.time() - t0:.0f}s)",
        flush=True,
    )

    if s1._BPE_TOKENIZER is None and getattr(ns, "mask_mode", "mixed") == "mixed":
        s1._load_bpe_tokenizer(ns.bpe_tokenizer_path)
    s1._MASK_GENERATOR.manual_seed(seed)
    s1._BURST_GENERATOR.manual_seed(seed + s1._BURST_SEED_OFFSET)
    s1._BURST_SAMPLER = s1.CorpusSampler(ns.data_path)
    s1._BURST_SIEVE_MODEL = sieve_model  # 先验筛参考模型: 基座固定, GPU 驻留
    _Q17_GENERATOR.manual_seed(seed + _Q17_SEED_OFFSET)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    # 收官兼容 (条件 3): resolved_config 照抄基座 (探针从此建模)
    (out_dir / "resolved_config.json").write_text(
        json.dumps(vars(ns), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    opt = s1.build_optimizer(ns, iter(trainable))
    sched = s1._cosine_with_warmup(opt, 100, args.max_steps)  # warmup 100 + cosine→0 (冻结配方)
    train_loader, _eval_loader = s1.make_dataloaders(ns)

    start_step = 0
    latest = out_dir / "latest.pt"
    if args.resume and latest.exists():
        payload = torch.load(latest, map_location=device, weights_only=False)
        model.load_state_dict(payload["model"])  # resume 纪律照旧 (覆盖重初始化的链)
        opt.load_state_dict(payload["optimizer"])
        start_step = int(payload.get("step", 0))
        if start_step > 0:
            sched.step(start_step)
        print(f"[q17] resumed from step {start_step}", flush=True)

    log_path = out_dir / "train_log.jsonl"
    nan_skips = 0
    watchdog_skips = 0  # 步级看门狗计数 (Q18 挂死急诊单; 入 log schema)
    step = start_step
    pending: dict[str, float] = {}
    pending_n = 0
    pending_loss = 0.0
    while step < args.max_steps:
        for batch in train_loader:
            if step >= args.max_steps:
                break
            p = _q17_anneal_p(step)
            loss, metrics, step_sec, overrun = _watchdog_call(
                _q17_step, model, batch[0], ns, device, p, _Q17_GENERATOR
            )
            if loss is None or overrun:
                if overrun and loss is not None:
                    watchdog_skips += 1  # 该窗作废: 步进照走不参训, 不中断训练
                    print(
                        f"[q17] 看门狗: step {step} 单步 {step_sec:.0f}s > {_WATCHDOG_STEP_SEC:.0f}s, "
                        f"该窗作废不参训 (累计 {watchdog_skips})",
                        flush=True,
                    )
                step += 1  # echo 离网/看门狗: 步进照走 (课程按步), 不参训
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
                }
                s1._append_jsonl(log_path, row)
                pending = {}
                pending_n = 0
                pending_loss = 0.0
                s1._burst_yield_alarm(step, row.get("burst_yield", 1.0))  # Q14 纪律沿用
                print(
                    f"[q17] step {step} p={row['p']} loss={row['loss']:.4f} "
                    f"echo_acc={row.get('echo_byte_acc', 0.0):.4f} "
                    f"α_k={row.get('alpha_k', 0.0):.4f} α_v={row.get('alpha_v', 0.0):.4f}",
                    flush=True,
                )
            if step % 500 == 0:
                torch.save(
                    {"step": step, "model": model.state_dict(), "optimizer": opt.state_dict(),
                     "args": vars(args)},
                    latest,
                )
            if step % _Q17_TIER_STEPS == 0:
                # 里程碑每 2K (档位切换点), 不带 optimizer
                torch.save(
                    {"step": step, "model": model.state_dict(), "args": vars(args)},
                    out_dir / f"step_{step:06d}.pt",
                )

    torch.save(
        {"step": step, "model": model.state_dict(), "optimizer": opt.state_dict(), "args": vars(args)},
        latest,
    )

    # 收官 eval (条件 3 参照列): codec 双指标, s1.evaluate 同形态 (自然路径,
    # p=0 后的生产形态); Q15 管束 (burst/筛/剔除) 随 ns 口径同开.
    eval_stats = {}
    if args.max_eval_batches > 0:
        ns.max_eval_batches = args.max_eval_batches  # CLI 覆写 (冒烟 1 批)
        eval_stats = s1.evaluate(model, _eval_loader, ns, device)
    summary = {
        "run_id": args.run_id,
        "steps": step,
        "params": sum(p_.numel() for p_ in model.parameters()),
        "elapsed_sec": time.time() - t0,
        "steps_per_sec": step / max(time.time() - t0, 1e-9),
        "nan_skips": nan_skips,
        "watchdog_step_skip": watchdog_skips,
        "args": vars(args),
        "base_ckpt": str(args.ckpt),
        "base_step": base_step,
        **eval_stats,
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
