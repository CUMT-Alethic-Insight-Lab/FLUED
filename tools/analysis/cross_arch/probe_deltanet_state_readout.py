"""E122 配套表示侧仪器 · DeltaNet 线性状态闭式读出探针（3.3 环第二把尺子）。

目的：第一把尺子（probe_e122_deltanet_book.py，必要性账）答行为侧「用没用」
（冒烟正对比 +0.262 nat，500 窗 contrast 0.281 nat CI 不含 0）；本仪器答表示
侧配套问题——**远端内容是否以线性可读的形式住在递归状态 S_t 里**。若可读 +
行为在用 = 标准架构不盲（盲是我们字节级体制特有）；若不可读但行为在用 = 读出
是非线性/注意式的，两把尺子并读结论更微妙。两种结局都是资产。

状态抽取方案（fla 0.5.2，前提已读码验证）：
- fla 层不暴露中间状态：layers/delta_net.py 的 DeltaNet.forward 只经
  chunk_delta_rule 拿 final_state（q_len>64 走 chunk 模式，attn_mode=chunk）。
- 本仪器 **monkeypatch `fla.layers.delta_net.chunk_delta_rule`**（层模块全局
  名，delta_net.py 顶部 import、forward 内调用点；仅进程内改绑定，**不改库
  文件**）：原函数照常执行（模型行为零改动），旁路留存每层 (k, v, beta)
  （pre-l2norm；核内 l2 在 ops/delta_rule/chunk.py:170-172 施加）。
- chunk 边界态独立重算：`delta_rule_chunk_boundary_states`（naive.py
  delta_rule_chunkwise 状态更新同式的 fp32 移植）；语义 S[c] = chunk c 前的
  状态 = 已消费 token < c*chunk_size。首窗逐层与模型自身 final_state（wrapper
  以 output_final_state=True 重调原函数取回）对拍，相对误差超阈 RuntimeError
  响亮停机（前提哨兵）。
- granular 粒度 = chunk 边界（64 token）：这是模型递归的真实保存粒度，chunk 内
  部细粒度走 chunk 内注意力不经 S。

探针设计：
- 样本位：E122 同款选择链（**import 复用** cross_segment_occurrences /
  select_tail_positions / find_first / tokenize_window / load_model_and_tokenizer，
  不复制；不做稀有表过滤——手术要稀有防撞，探针要密度）选中的跨段重复续尾位
  t → chunk 边界 c = t // chunk_size；每边界认领一个 designated 源（t 最小，
  平局 gram 字典序，确定性）。窗口定义与必要性账逐字同构（顺序字节窗 4096B、
  utf-8 replace、BOS、截 2048、seg=256、n=3、tail=3）→ 同卷对拍成立。
- 目标 token 六探针/层：近程 = 边界前第 1/2/3 token（肯定在状态里，阳性对照）
  ；远程 = designated 源 gram（最早出现处）第 0/1/2 token（源必须整体在边界
  前 s+n ≤ b，否则该边界远程目标作废并诚实计数）。
- ridge 探针（线性核、对偶解，λ 可配）：S_t flatten（16 头×128×128 = 262144
  维，bf16 存、fp32 算）→ **训练窗**统计逐维标准化 → 预测目标 token 的输入
  嵌入（fp32）。多 λ 敏感性（--extra-ridge-lambdas）共享同一前向/状态缓存/
  Gram/测试核，只重解对偶系——主口径 = --ridge-lambda。
- 对照 = 打乱配对：同窗内置换目标（目标边缘分布不变、状态→目标配对破坏）重训
  同款探针；real/ctrl 两探针在同一测试配对上评估，差 = uplift（训练期配对信息
  的贡献，不是评估端技巧）。附加特异性读数：real 探针 × 测试端置换配对。
- 指标：cos(ŷ, E[target]) 与嵌入空间最近邻 top-1 acc（候选 = 测试劈分全部目标
  token，chance = 1/K 落盘）；uplift = real − ctrl；窗级符号翻转置换检验 p 值
  （单侧，方向 = uplift > 0，含 +1/(n+1) 保守约定）。
- 口径：窗级 train/test 对半劈（种子洗牌，全层同劈——跨层可比）；层分层全 24
  层逐层报 + early/mid/deep 组汇总；距离分层（近程 lag 探针 / 远程探针按源
  距离 near/mid/remote 桶在测试端分层报数）。

判词（描述性，冒烟级留白）：深部层远程 uplift>0 且 p<0.05 → 「线性可读」；
全否 → 「未见线性可读（读出或是非线性/注意式）」；其余 → 证据不足。两向都
与必要性账（行为侧）并读，不单独定案。

Usage:
  python tools/analysis/cross_arch/probe_deltanet_state_readout.py \
      --model-path /root/autodl-tmp/models/delta_net-1.3B-100B \
      --corpus /root/autodl-tmp/corpus/corpus_v3.txt \
      --n-windows 40 --device cuda \
      --out-dir /root/autodl-tmp/outputs/deltanet_state_readout_smoke_20260911
  CPU 冒烟: --device cpu --n-windows 1（无 fla 环境跑不了模型，核心逻辑走单测）
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import time
from pathlib import Path

import torch

try:  # repo 根可导入（pytest / python -m）
    from tools.analysis.cross_arch import probe_e122_deltanet_book as e122
except ImportError:  # 脚本直跑（sys.path[0] = 脚本目录）
    import probe_e122_deltanet_book as e122

NEAR_LAGS = (1, 2, 3)


# ---------------------------------------------------------------------------
# 样本构造（纯 python，单测覆盖）
# ---------------------------------------------------------------------------


def build_window_samples(ids: list[int], sel: dict[int, tuple[tuple, int]],
                         n: int, chunk_size: int, near_lags=NEAR_LAGS,
                         remote_js=(0, 1, 2)) -> tuple[list[dict], int]:
    """E122 选择链产物 sel（续尾位 -> (gram, 重复出现位)）→ 探针样本。

    每选中续尾位 t 映射 chunk 边界 c = t // chunk_size；每边界认领 designated
    （t 最小；同位唯一 gram，无需平局）。近程目标 = 边界前第 lag token；
    远程目标 = designated gram 源（最早出现处）第 j token——源必须整体在边界
    前（s + n ≤ b），否则该边界远程目标作废并计数（近程不受影响）。
    返回 (samples, n_remote_skipped)。"""
    designated: dict[int, int] = {}
    for t in sorted(sel):
        c = t // chunk_size
        cur = designated.get(c)
        if cur is None or t < cur:
            designated[c] = t
    samples, skipped = [], 0
    for c in sorted(designated):
        t = designated[c]
        g, p = sel[t]
        b = c * chunk_size
        if b - max(near_lags) < 0:
            continue
        s = e122.find_first(ids, g)
        remote: list[tuple[int, int, int, int]] = []
        if s >= 0 and s + n <= b:
            remote = [(j, s + j, ids[s + j], b - (s + j)) for j in remote_js]
        else:
            skipped += 1
        samples.append({
            "chunk": c, "boundary": b, "tail_pos": t, "gram": list(g),
            "repeat_pos": p, "source_pos": s,
            "near": {lag: (b - lag, ids[b - lag]) for lag in near_lags},
            "remote": remote,  # (j, token_pos, token_id, distance)
        })
    return samples, skipped


def distance_bucket(dist: int, near_cut: int, remote_cut: int) -> str:
    if dist < near_cut:
        return "near"
    if dist >= remote_cut:
        return "remote"
    return "mid"


def split_windows(window_ids: list[int], train_frac: float,
                  seed: int) -> tuple[list[int], list[int]]:
    """窗级 train/test 对半劈（种子洗牌；全层同劈，跨层可比）。"""
    ws = sorted(window_ids)
    rng = random.Random(seed)
    rng.shuffle(ws)
    k = int(len(ws) * train_frac)
    return sorted(ws[:k]), sorted(ws[k:])


# ---------------------------------------------------------------------------
# fp32 chunk 边界态（纯 torch，单测对拍逐 token 朴素递推）
# ---------------------------------------------------------------------------


def delta_rule_chunk_boundary_states(k: torch.Tensor, v: torch.Tensor,
                                     beta: torch.Tensor,
                                     chunk_size: int = 64) -> torch.Tensor:
    """DeltaNet chunk 边界态（fp32）。k [T,H,K]（应已 l2 归一）、v [T,H,V]、
    beta [T,H] → states [NS+1,H,K,V]：states[i] = chunk i 前的状态（已消费
    token < i*chunk_size），states[NS] = 终态。状态更新与
    fla/ops/delta_rule/naive.py delta_rule_chunkwise 同式：块内 WY 表示
    u = (I−tri(βKKᵀ))^{-1}(βV)、w 同 roles 于 βK，S ← S + Kᵀ(u − wS)；
    T 非整 chunk 零填充（β=0 → 无更新，终态不变）。"""
    k = k.transpose(0, 1).float()
    v = v.transpose(0, 1).float()
    beta = beta.transpose(0, 1).float()
    h, t_len, kd = k.shape
    vd = v.shape[-1]
    ns = (t_len + chunk_size - 1) // chunk_size
    pad = ns * chunk_size - t_len
    if pad:
        k = torch.cat([k, k.new_zeros(h, pad, kd)], 1)
        v = torch.cat([v, v.new_zeros(h, pad, vd)], 1)
        beta = torch.cat([beta, beta.new_zeros(h, pad)], 1)
    vb = v * beta.unsqueeze(-1)
    kb = k * beta.unsqueeze(-1)
    kch_raw = k.view(h, ns, chunk_size, kd)
    kch = kb.view(h, ns, chunk_size, kd)
    vch = vb.view(h, ns, chunk_size, vd)
    # (I − tri(βKKᵀ))^{-1} 的 Neumann 前代迭代（含对角，naive.delta_rule_chunkwise 同款：
    # 第一操作数 βK、第二操作数裸 K）
    mask = torch.triu(torch.ones(chunk_size, chunk_size, dtype=torch.bool,
                                 device=k.device), 0)
    attn = -(kch @ kch_raw.transpose(-1, -2)).masked_fill(mask, 0)
    for i in range(1, chunk_size):
        attn[..., i, :i] = attn[..., i, :i] + (
            attn[..., i, :, None] * attn[..., :, :i]).sum(-2)
    attn = attn + torch.eye(chunk_size, dtype=torch.float, device=k.device)
    u_c = attn @ vch
    w_c = attn @ kch
    s = k.new_zeros(h, kd, vd)
    states = [s]
    for c in range(ns):
        u_i = u_c[:, c] - w_c[:, c] @ s
        s = s + kch_raw[:, c].transpose(-1, -2) @ u_i
        states.append(s)
    return torch.stack(states)


# ---------------------------------------------------------------------------
# 探针核心（torch，CPU/GPU 通吃，单测覆盖）
# ---------------------------------------------------------------------------


def standardize_fit(x: torch.Tensor, eps: float = 1e-5):
    mean = x.mean(0)
    std = x.std(0).clamp_min(eps)
    return mean, std


def ridge_fit(x: torch.Tensor, y: torch.Tensor, lam: float) -> dict:
    """线性核对偶 ridge：ŷ = k(x)ᵀα + ȳ，K = XXᵀ/D + λI。x 已标准化、
    y 内部中心化。（单测/单 λ 便捷路径；生产多 λ 走 ridge_gram + ridge_solve）"""
    y_mean = y.mean(0)
    d = x.shape[1]
    gram = x @ x.T / d
    alpha = torch.linalg.solve(
        gram + lam * torch.eye(x.shape[0], dtype=x.dtype, device=x.device),
        y - y_mean)
    return {"alpha": alpha, "x_train": x, "d": d, "y_mean": y_mean}


def ridge_gram(x: torch.Tensor) -> torch.Tensor:
    """对偶 Gram 矩阵 K = XXᵀ/D（标准化后的训练特征；λ 无关，一次算全复用）。"""
    return x @ x.T / x.shape[1]


def ridge_solve(gram: torch.Tensor, y: torch.Tensor, lam: float) -> dict:
    """给定预计算 Gram 的对偶 ridge 求解（y 内部中心化）。"""
    y_mean = y.mean(0)
    alpha = torch.linalg.solve(
        gram + lam * torch.eye(gram.shape[0], dtype=gram.dtype,
                               device=gram.device),
        y - y_mean)
    return {"alpha": alpha, "y_mean": y_mean}


def ridge_predict(probe: dict, x: torch.Tensor) -> torch.Tensor:
    return ((x @ probe["x_train"].T) / probe["d"]) @ probe["alpha"] + probe["y_mean"]


def cos_rows(pred: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
    pn = pred / pred.norm(dim=-1, keepdim=True).clamp_min(1e-8)
    tn = target / target.norm(dim=-1, keepdim=True).clamp_min(1e-8)
    return (pn * tn).sum(-1)


def nn_top1_correct(pred: torch.Tensor, cand_emb: torch.Tensor,
                    target_row: torch.Tensor) -> torch.Tensor:
    """嵌入空间最近邻 top-1：候选 = cand_emb 行；target_row 为真值行号。"""
    d2 = (pred.pow(2).sum(-1, keepdim=True) - 2 * pred @ cand_emb.T
          + cand_emb.pow(2).sum(-1)[None, :])
    return d2.argmin(-1) == target_row


def signflip_p(diff: list[float], n_perm: int, seed: int) -> dict | None:
    """窗级符号翻转置换检验（单侧，方向 = diff 均值 > 0）。
    p = (1 + #{置换均值 ≥ 观测}) / (n_perm + 1)（含保守 +1 约定）。"""
    x = torch.tensor([d for d in diff if d is not None], dtype=torch.float64)
    if x.numel() == 0:
        return None
    obs = x.mean().item()
    g = torch.Generator().manual_seed(seed)
    signs = torch.where(torch.rand(n_perm, x.numel(), generator=g) < 0.5,
                        -1.0, 1.0)
    means = (signs * x[None, :]).mean(-1)
    p = (1 + int((means >= obs - 1e-12).sum().item())) / (n_perm + 1)
    return {"obs": obs, "p": p, "n_windows": int(x.numel()),
            "n_perm": n_perm, "seed": seed}


def _permute_ids_within_windows(ids_per_win: list[list[int]],
                                rng: random.Random) -> list[list[int]]:
    out = []
    for ids in ids_per_win:
        idx = list(range(len(ids)))
        rng.shuffle(idx)
        out.append([ids[i] for i in idx])
    return out


def probe_one(x_by_win: dict[int, torch.Tensor],
              tids_by_win: dict[int, list[int]],
              dist_by_win: dict[int, list[int]],
              train_win: list[int], test_win: list[int],
              emb: torch.Tensor, lam: float, ctrl_seed: int, p_seed: int,
              n_perm: int, near_cut: int, remote_cut: int,
              by_distance: bool, extra_lambdas: tuple = ()) -> dict:
    """单探针全流程：real/ctrl（打乱配对重训）双探针 → 同一测试配对上
    cos/acc → uplift + 窗级符号翻转 p + 距离桶分层。

    λ 敏感性：Gram 与测试核矩阵 k(x,x_train) 均 λ 无关，一次算全后每个
    λ 只多做两次 N×N 解与两次核×α GEMM（前向一次、多 λ 复用）。主口径
    = lam（顶层字段），extra_lambdas 只进 lambda_sensitivity 块；ctrl
    配对与置换符号序列跨 λ 固定（同 ctrl_seed/p_seed，λ 间可比）。"""
    d = next(iter(x_by_win.values())).shape[1]
    xtr = torch.cat([x_by_win[w] for w in train_win], 0)
    tids_tr = [t for w in train_win for t in tids_by_win[w]]
    mean, std = standardize_fit(xtr)
    xtr.sub_(mean).div_(std)  # 就地标准化（cat 副本，安全）
    gram = ridge_gram(xtr)
    ytr = emb[torch.tensor(tids_tr, device=emb.device)]
    ctrl_rng = random.Random(ctrl_seed)
    ids_tr_ctrl = _permute_ids_within_windows(
        [tids_by_win[w] for w in train_win], ctrl_rng)
    tids_tr_ctrl = [t for ids in ids_tr_ctrl for t in ids]
    ytr_ctrl = emb[torch.tensor(tids_tr_ctrl, device=emb.device)]

    # 测试核矩阵（λ 无关）一次算全；行切分与测试窗对齐
    k_test, win_slices = [], []
    c0 = 0
    for w in test_win:
        xg = (x_by_win[w] - mean) / std
        k_test.append(xg @ xtr.T / d)
        win_slices.append((w, c0, c0 + xg.shape[0]))
        c0 += xg.shape[0]
    k_test = torch.cat(k_test, 0) if k_test else None
    del xtr
    shuffled_by_win = {w: _permute_ids_within_windows([tids_by_win[w]],
                                                      ctrl_rng)[0]
                       for w in test_win}

    test_tids = [t for w in test_win for t in tids_by_win[w]]
    cand_ids = sorted(set(test_tids))
    cand_emb = emb[torch.tensor(cand_ids, device=emb.device)] if cand_ids else None
    row_of = {tid: i for i, tid in enumerate(cand_ids)}

    def _run_lambda(lam_v: float) -> dict:
        pr_p = ridge_solve(gram, ytr, lam_v)
        pc_p = ridge_solve(gram, ytr_ctrl, lam_v)
        pred_r = k_test @ pr_p["alpha"] + pr_p["y_mean"] if k_test is not None else None
        pred_c = k_test @ pc_p["alpha"] + pc_p["y_mean"] if k_test is not None else None
        per_win, per_sample, shuffled_cos = [], [], []
        for w, i0, i1 in win_slices:
            tids = tids_by_win[w]
            yg = emb[torch.tensor(tids, device=emb.device)]
            rows = torch.tensor([row_of[t] for t in tids], device=emb.device)
            pr, pc = pred_r[i0:i1], pred_c[i0:i1]
            cos_r, cos_c = cos_rows(pr, yg), cos_rows(pc, yg)
            acc_r = nn_top1_correct(pr, cand_emb, rows).float()
            acc_c = nn_top1_correct(pc, cand_emb, rows).float()
            # 特异性：real 探针 × 测试端窗内置换配对
            shuffled_cos.extend(cos_rows(pr, emb[torch.tensor(
                shuffled_by_win[w], device=emb.device)]).tolist())
            per_win.append({
                "window": w, "n": len(tids),
                "cos_real": cos_r.mean().item(), "cos_ctrl": cos_c.mean().item(),
                "acc_real": acc_r.mean().item(), "acc_ctrl": acc_c.mean().item(),
            })
            per_sample.extend({"window": w, "dist": int(dd),
                               "cos_real": float(a2), "cos_ctrl": float(b2),
                               "acc_real": float(c2), "acc_ctrl": float(e2)}
                              for a2, b2, c2, e2, dd in zip(
                                  cos_r.tolist(), cos_c.tolist(),
                                  acc_r.tolist(), acc_c.tolist(),
                                  dist_by_win[w]))

        def _agg(key_r, key_c):
            real = [pw[key_r] for pw in per_win]
            ctrl = [pw[key_c] for pw in per_win]
            sf = signflip_p([r - c for r, c in zip(real, ctrl)], n_perm, p_seed)
            ns = sum(pw["n"] for pw in per_win)
            mr = sum(r * pw["n"] for r, pw in zip(real, per_win)) / ns if ns else None
            mc = sum(c * pw["n"] for c, pw in zip(ctrl, per_win)) / ns if ns else None
            return mr, mc, sf

        cos_r, cos_c, cos_sf = _agg("cos_real", "cos_ctrl")
        acc_r, acc_c, acc_sf = _agg("acc_real", "acc_ctrl")
        return {"cos": {"real": cos_r, "ctrl": cos_c,
                        "uplift": (cos_r - cos_c) if (cos_r is not None and cos_c is not None) else None,
                        "perm": cos_sf},
                "acc": {"real": acc_r, "ctrl": acc_c,
                        "uplift": (acc_r - acc_c) if (acc_r is not None and acc_c is not None) else None,
                        "perm": acc_sf},
                "per_win": per_win, "per_sample": per_sample,
                "shuffled_cos": shuffled_cos}

    primary = _run_lambda(lam)
    res = {
        "train_n": int(gram.shape[0]), "test_n": len(test_tids),
        "n_candidates": len(cand_ids), "chance": (1.0 / len(cand_ids)) if cand_ids else None,
        "cos": primary["cos"], "acc": primary["acc"],
        "cos_real_shuffled_test": (sum(primary["shuffled_cos"]) / len(primary["shuffled_cos"]))
        if primary["shuffled_cos"] else None,
        "per_window": primary["per_win"],
    }
    if by_distance:
        buckets: dict[str, list[dict]] = {}
        for ps in primary["per_sample"]:
            buckets.setdefault(distance_bucket(ps["dist"], near_cut, remote_cut),
                               []).append(ps)
        res["by_distance"] = {
            b: {"n": len(rows),
                "cos_real": sum(r["cos_real"] for r in rows) / len(rows),
                "cos_ctrl": sum(r["cos_ctrl"] for r in rows) / len(rows),
                "acc_real": sum(r["acc_real"] for r in rows) / len(rows),
                "acc_ctrl": sum(r["acc_ctrl"] for r in rows) / len(rows)}
            for b, rows in sorted(buckets.items())
        }
    sens = {str(lam): {"cos": primary["cos"], "acc": primary["acc"]}}
    for lam_v in extra_lambdas:
        blk = _run_lambda(lam_v)
        sens[str(lam_v)] = {"cos": blk["cos"], "acc": blk["acc"]}
    res["lambda_sensitivity"] = sens
    return res


def run_layer_probes(x_by_win: dict[int, torch.Tensor],
                     samples_by_win: dict[int, list[dict]],
                     train_win: list[int], test_win: list[int],
                     emb: torch.Tensor, lam: float, seed: int, layer: int,
                     near_lags=(1, 2, 3), n_remote_js: int = 3,
                     near_cut: int = 32, remote_cut: int = 192,
                     n_perm: int = 4096, extra_lambdas: tuple = ()) -> dict:
    """一层全部探针（近程 lag × 远程 j）。x_by_win: {w: [n_w, D] fp32}。"""
    out: dict[str, dict] = {}
    for probe_i, lag in enumerate(near_lags):
        xw = {w: x_by_win[w] for w in x_by_win}
        tids = {w: [s["near"][lag][1] for s in samples_by_win[w]]
                for w in x_by_win}
        dists = {w: [lag] * len(tids[w]) for w in x_by_win}
        out[f"near_lag{lag}"] = probe_one(
            xw, tids, dists, train_win, test_win, emb, lam,
            ctrl_seed=seed + 500 * layer + probe_i,
            p_seed=seed + 1000 * layer + probe_i, n_perm=n_perm,
            near_cut=near_cut, remote_cut=remote_cut, by_distance=False,
            extra_lambdas=extra_lambdas)
    valid = {w: x_by_win[w] for w in x_by_win
             if any(s["remote"] for s in samples_by_win[w])}
    for j in range(n_remote_js):
        xw, tids, dists = {}, {}, {}
        for w in valid:
            # 行对齐：x 行必须与 remote 样本子集逐行对应（部分窗：同一窗内
            # 既有合法远程边界、又有源越界作废边界——500 窗实跑暴露的错位）
            keep = [i for i, s in enumerate(samples_by_win[w]) if s["remote"]]
            xw[w] = x_by_win[w][keep]
            ss = [s for s in samples_by_win[w] if s["remote"]]
            tids[w] = [s["remote"][j][2] for s in ss]
            dists[w] = [s["remote"][j][3] for s in ss]
        tr = [w for w in train_win if w in xw]
        te = [w for w in test_win if w in xw]
        if not tr or not te:
            out[f"remote_j{j}"] = {"train_n": 0, "test_n": 0, "n_candidates": 0,
                                   "chance": None, "cos": {"real": None, "ctrl": None,
                                                           "uplift": None, "perm": None},
                                   "acc": {"real": None, "ctrl": None,
                                           "uplift": None, "perm": None},
                                   "cos_real_shuffled_test": None, "per_window": [],
                                   "by_distance": {}, "lambda_sensitivity": {}}
            continue
        out[f"remote_j{j}"] = probe_one(
            xw, tids, dists, tr, te, emb, lam,
            ctrl_seed=seed + 500 * layer + len(near_lags) + j,
            p_seed=seed + 1000 * layer + len(near_lags) + j, n_perm=n_perm,
            near_cut=near_cut, remote_cut=remote_cut, by_distance=True,
            extra_lambdas=extra_lambdas)
    return out


# ---------------------------------------------------------------------------
# 状态捕获（fla 相关；仅远端执行。monkeypatch 仅进程内，不改库文件）
# ---------------------------------------------------------------------------


class ChunkDeltaRuleCapture:
    """monkeypatch `fla.layers.delta_net.chunk_delta_rule`（层模块全局名）：
    原函数照常执行（模型行为零改动），旁路留存每层 (k, v, beta)（pre-l2norm，
    detach）。verify_next=True 时该次 forward 的每层额外以 output_final_state=
    True 重调原函数取模型自身终态，供边界态对拍（前提哨兵）。"""

    def __init__(self):
        self.records: list[dict] = []
        self.verify_next = False
        self._mod = None
        self._orig = None

    def __enter__(self):
        import fla.layers.delta_net as dn_mod
        self._mod = dn_mod
        self._orig = dn_mod.chunk_delta_rule
        cap = self

        def wrapper(q, k, v, beta, scale=None, initial_state=None,
                    output_final_state=False, use_qk_l2norm_in_kernel=False,
                    **kw):
            rec = {"k": k.detach(), "v": v.detach(), "beta": beta.detach(),
                   "l2": use_qk_l2norm_in_kernel}
            if cap.verify_next:
                _o, ht = cap._orig(
                    q=q, k=k, v=v, beta=beta, scale=scale,
                    initial_state=initial_state, output_final_state=True,
                    use_qk_l2norm_in_kernel=use_qk_l2norm_in_kernel, **kw)
                rec["kernel_final_state"] = ht.detach().float()
            cap.records.append(rec)
            return cap._orig(q=q, k=k, v=v, beta=beta, scale=scale,
                             initial_state=initial_state,
                             output_final_state=output_final_state,
                             use_qk_l2norm_in_kernel=use_qk_l2norm_in_kernel,
                             **kw)

        dn_mod.chunk_delta_rule = wrapper
        return self

    def __exit__(self, *exc):
        self._mod.chunk_delta_rule = self._orig
        return False


def extract_layer_boundary_states(records: list[dict], chunk_size: int,
                                  tol_rel: float) -> tuple[list[torch.Tensor],
                                                           list[dict]]:
    """capture.records → 每层边界态 [NS+1,H,K,V]（fp32）；带 kernel_final_state
    的层与模型自身终态对拍（相对 Frobenius 误差），超阈 RuntimeError 响亮。"""
    from fla.modules.l2norm import l2norm_fwd
    outs, verr = [], []
    for i, rec in enumerate(records):
        k = rec["k"]
        if rec["l2"]:
            k = l2norm_fwd(k)[0]
        assert k.shape[0] == 1, f"batch>1 不在本仪器口径内（B={k.shape[0]}）"
        states = delta_rule_chunk_boundary_states(k.squeeze(0), rec["v"].squeeze(0),
                                                  rec["beta"].squeeze(0),
                                                  chunk_size)
        if "kernel_final_state" in rec:
            kern = rec["kernel_final_state"][0]
            rel = ((states[-1] - kern).norm() / kern.norm().clamp_min(1e-8)).item()
            verr.append({"layer": i, "rel_err": rel})
            if rel > tol_rel:
                raise RuntimeError(
                    f"状态抽取对拍失败：layer {i} fp32 边界态 vs 模型核终态 "
                    f"相对误差 {rel:.4g} > {tol_rel}（前提不成立，响亮停机）")
        outs.append(states)
    return outs, verr


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_int_list(text: str) -> list[int] | None:
    if text.strip().lower() == "all":
        return None
    vals = [int(x) for x in text.split(",") if x.strip()]
    if not vals:
        raise SystemExit("--probe-layers 解析失败")
    return vals


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--model-path", default="/root/autodl-tmp/models/delta_net-1.3B-100B")
    p.add_argument("--corpus", default="/root/autodl-tmp/corpus/corpus_v3.txt")
    p.add_argument("--n-windows", type=int, default=40)
    p.add_argument("--start-window", type=int, default=0)
    p.add_argument("--window-bytes", type=int, default=4096)
    p.add_argument("--max-tokens", type=int, default=2048)
    p.add_argument("--segment-tokens", type=int, default=256)
    p.add_argument("--ngram-len", type=int, default=3, choices=[2, 3, 4])
    p.add_argument("--tail", type=int, default=3)
    p.add_argument("--chunk-size", type=int, default=64, choices=[16, 32, 64])
    p.add_argument("--near-lags", default="1,2,3")
    p.add_argument("--ridge-lambda", type=float, default=1.0,
                   help="主口径 λ")
    p.add_argument("--extra-ridge-lambdas", default="",
                   help="逗号分隔附加 λ（敏感性分析；主口径不变，状态/核一次算全复用）")
    p.add_argument("--train-frac", type=float, default=0.5)
    p.add_argument("--near-dist", type=int, default=32)
    p.add_argument("--remote-dist", type=int, default=192)
    p.add_argument("--n-perm", type=int, default=4096)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--probe-layers", default="all",
                   help="'all' 或逗号层号（0 起）——默认全层；500 窗正式跑可子集省内存")
    p.add_argument("--max-boundaries-per-window", type=int, default=24)
    p.add_argument("--layers-per-pass", type=int, default=0,
                   help="分 pass 缓存层数（0=全层单 pass；大窗数下防 cgroup 内存顶穿，"
                        "每 pass 重跑前向，选择链零随机故各 pass 样本逐字一致）")
    p.add_argument("--verify-tol-rel", type=float, default=0.05)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--out-dir",
                   default=f"outputs/deltanet_state_readout_smoke_{time.strftime('%Y%m%d')}")
    args = p.parse_args()

    if not (0 < args.train_frac < 1):
        raise SystemExit("--train-frac ∈ (0,1)")
    if args.near_dist >= args.remote_dist:
        raise SystemExit("--near-dist须小于--remote-dist")
    near_lags = tuple(int(x) for x in args.near_lags.split(",") if x.strip())
    extra_lambdas = tuple(float(x) for x in args.extra_ridge_lambdas.split(",")
                          if x.strip())
    if any(lv <= 0 for lv in extra_lambdas) or args.ridge_lambda <= 0:
        raise SystemExit("λ 必须 > 0")

    device = torch.device(
        "cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda"
        else "cpu")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    corpus = Path(args.corpus)
    if not corpus.exists():
        raise SystemExit(f"corpus 不存在: {corpus}")

    model, tok, fingerprint = e122.load_model_and_tokenizer(args.model_path, device)
    n_layers = int(model.config.num_hidden_layers)
    probe_layers = parse_int_list(args.probe_layers) or list(range(n_layers))
    if any(l < 0 or l >= n_layers for l in probe_layers):
        raise SystemExit(f"--probe-layers 越界（模型 {n_layers} 层）")
    emb = model.get_input_embeddings().weight.detach().float()
    head_k = int(model.config.head_k_dim) if hasattr(model.config, "head_k_dim") \
        else (int(model.config.hidden_size) * int(model.config.expand_k)) // int(model.config.num_heads)
    state_dim = int(model.config.num_heads) * head_k * head_k  # K=V（expand 1.0 对角方阵）
    print(f"[dsr] model={Path(args.model_path).name} device={device.type} "
          f"layers={n_layers} probe={probe_layers} state_dim={state_dim}", flush=True)

    # 窗循环（同卷定义，与 e122 必要账逐字同构）。大窗数下全层状态缓存会顶穿
    # 容器 cgroup 内存限额（本机 memory.high=106GB：500 窗 × 24 层 ≈ 106GB），
    # 故支持分 pass：每 pass 只缓存 pass_layers 的状态、跑完该 pass 探针即释放，
    # 前向每 pass 重跑（选择链零随机 → 各 pass 样本逐字一致，同卷不破坏）。
    layers_per_pass = args.layers_per_pass or len(probe_layers)
    passes = [probe_layers[i:i + layers_per_pass]
              for i in range(0, len(probe_layers), layers_per_pass)]
    samples_by_win: dict[int, list[dict]] = {}
    win_tokens: dict[int, int] = {}
    tally = {"n_windows_attempted": 0, "n_windows_used": 0, "n_windows_empty": 0,
             "n_windows_truncated": 0, "n_windows_forward_fails": 0}
    totals = {"n_samples": 0, "n_remote_skipped": 0, "n_boundaries_capped": 0,
              "n_selected_tails": 0}
    max_byte_touched = 0
    layer_results: dict[int, dict] = {}
    split_cache: tuple[list[int], list[int]] | None = None
    capture = ChunkDeltaRuleCapture()
    print(f"[dsr] passes={[p[0] for p in passes]} layers_per_pass={layers_per_pass}",
          flush=True)

    with corpus.open("rb") as f, capture:
        for pi, pass_layers in enumerate(passes):
            store: dict[int, list[torch.Tensor]] = {l: [] for l in pass_layers}
            pass_used = 0
            f.seek(0)
            for wi in range(args.n_windows):
                w_abs = args.start_window + wi
                f.seek(w_abs * args.window_bytes)
                raw = f.read(args.window_bytes)
                if len(raw) < args.window_bytes:
                    print(f"[dsr] 语料前缀尽（窗 {w_abs}），停", flush=True)
                    break
                max_byte_touched = max(max_byte_touched, (w_abs + 1) * args.window_bytes)
                ids, full_len = e122.tokenize_window(
                    tok, raw.decode("utf-8", errors="replace"), args.max_tokens)
                if full_len > args.max_tokens:
                    tally["n_windows_truncated"] += 1
                tally["n_windows_attempted"] += 1
                tk = len(ids)
                if tk < max(2 * args.chunk_size, args.segment_tokens + args.ngram_len + args.tail):
                    tally["n_windows_empty"] += 1
                    continue
                occ = e122.cross_segment_occurrences(ids, args.ngram_len,
                                                     args.segment_tokens)
                rare = set(occ)  # 探针要密度：全体跨段 gram，无稀有表过滤（与必要账的差异，报告口径）
                sel, _ov = e122.select_tail_positions(occ, rare, args.ngram_len,
                                                      args.tail, tk)
                if not sel:
                    tally["n_windows_empty"] += 1
                    continue
                totals["n_selected_tails"] += len(sel)
                samples, skipped = build_window_samples(
                    ids, sel, args.ngram_len, args.chunk_size, near_lags=near_lags,
                    remote_js=tuple(range(args.ngram_len)))
                totals["n_remote_skipped"] += skipped
                if len(samples) > args.max_boundaries_per_window:
                    totals["n_boundaries_capped"] += len(samples) - args.max_boundaries_per_window
                    samples = samples[:args.max_boundaries_per_window]
                if not samples:
                    tally["n_windows_empty"] += 1
                    continue

                capture.records = []
                capture.verify_next = pass_used == 0  # 每 pass 首窗逐层对拍（前提哨兵）
                try:
                    with torch.no_grad():
                        model(torch.tensor([ids], dtype=torch.long, device=device))
                    states_all, verr = extract_layer_boundary_states(
                        capture.records, args.chunk_size, args.verify_tol_rel)
                except RuntimeError as e:
                    if "对拍失败" in str(e):
                        raise  # 前提哨兵响亮，不静默
                    tally["n_windows_forward_fails"] += 1
                    print(f"[dsr] win {w_abs} 前向失败（跳过）：{e}", flush=True)
                    continue
                idx = torch.tensor([s["chunk"] for s in samples], device=device)
                for l in pass_layers:
                    rows = states_all[l][idx].reshape(len(samples), -1)
                    store[l].append(rows.to(torch.bfloat16).cpu())
                if pi == 0:
                    samples_by_win[w_abs] = samples
                    win_tokens[w_abs] = tk
                pass_used += 1
                if pi == 0:
                    totals["n_samples"] += len(samples)
                print(f"[dsr] p{pi} win {w_abs:5d} tk={tk} bounds={len(samples)} "
                      f"remote_skip={skipped} verif_max="
                      f"{max((v['rel_err'] for v in verr), default=None)} "
                      f"({time.time() - t0:.0f}s)", flush=True)

            # 本 pass 探针（pass 0 完成后定劈分，全层同劈跨 pass 复用）
            if not samples_by_win:
                raise SystemExit("零有效窗（选择链颗粒或语料问题），响亮拒绝")
            if split_cache is None:
                window_ids = sorted(samples_by_win)
                split_cache = split_windows(window_ids, args.train_frac, args.seed)
                print(f"[dsr] 窗劈分 train={len(split_cache[0])} "
                      f"test={len(split_cache[1])}；探针逐层…", flush=True)
            train_win, test_win = split_cache
            for l in pass_layers:
                x_by_win = {w: store[l][i].float().to(emb.device)
                            for i, w in enumerate(sorted(samples_by_win))}
                layer_results[l] = run_layer_probes(
                    x_by_win, samples_by_win, train_win, test_win, emb,
                    args.ridge_lambda, args.seed, l, near_lags=near_lags,
                    n_remote_js=args.ngram_len, near_cut=args.near_dist,
                    remote_cut=args.remote_dist, n_perm=args.n_perm,
                    extra_lambdas=extra_lambdas)
                store[l] = []  # 逐层释放
                r = layer_results[l]
                print(f"[dsr] layer {l:2d} "
                      f"near1 cos {r['near_lag1']['cos']['uplift']:+.4f} "
                      f"(p={r['near_lag1']['cos']['perm']['p'] if r['near_lag1']['cos']['perm'] else None}) "
                      f"remote_j0 cos {r['remote_j0']['cos']['uplift']:+.4f} "
                      f"(p={r['remote_j0']['cos']['perm']['p'] if r['remote_j0']['cos']['perm'] else None})",
                      flush=True)
            del store
            if pi == 0:
                tally["n_windows_used"] = pass_used
                summary_tally = dict(tally)
                summary_totals = dict(totals)
            print(f"[dsr] pass {pi}（层 {pass_layers[0]}-{pass_layers[-1]}）完成 "
                  f"({time.time() - t0:.0f}s)", flush=True)

    # 同卷锚：计分窗字节前缀 SHA256（dd 顺序写语料下，读过前缀已定终）
    prefix_sha = None
    if max_byte_touched:
        h = hashlib.sha256()
        with corpus.open("rb") as f:
            remain = max_byte_touched
            while remain:
                chunk = f.read(min(1 << 20, remain))
                if not chunk:
                    break
                h.update(chunk)
                remain -= len(chunk)
        prefix_sha = h.hexdigest()

    # 层组汇总（early/mid/deep 三分）+ 判词
    groups = {"early": [l for l in probe_layers if l < n_layers / 3],
              "mid": [l for l in probe_layers if n_layers / 3 <= l < 2 * n_layers / 3],
              "deep": [l for l in probe_layers if l >= 2 * n_layers / 3]}
    group_summary = {}
    for gname, ls in groups.items():
        if not ls:
            continue
        ups = [layer_results[l]["remote_j0"]["cos"]["uplift"] for l in ls
               if layer_results[l]["remote_j0"]["cos"]["uplift"] is not None]
        ps = [layer_results[l]["remote_j0"]["cos"]["perm"]["p"] for l in ls
              if layer_results[l]["remote_j0"]["cos"]["perm"]]
        near_ups = [layer_results[l]["near_lag1"]["cos"]["uplift"] for l in ls
                    if layer_results[l]["near_lag1"]["cos"]["uplift"] is not None]
        group_summary[gname] = {
            "layers": ls,
            "remote_j0_cos_uplift_mean": (sum(ups) / len(ups)) if ups else None,
            "remote_j0_min_p": min(ps) if ps else None,
            "n_layers_remote_p_lt_0.05": sum(1 for x in ps if x < 0.05),
            "near_lag1_cos_uplift_mean": (sum(near_ups) / len(near_ups)) if near_ups else None,
        }
    # λ 敏感性表（主口径 + 附加 λ，每 λ 一行；Gram/测试核已共享复用）
    lam_table: dict[str, dict] = {}
    for lv in [args.ridge_lambda] + list(extra_lambdas):
        key = str(lv)
        row: dict[str, dict] = {}
        for gname, ls in groups.items():
            if not ls:
                continue
            for pname in ("remote_j0", "near_lag1"):
                ups, ps = [], []
                for l in ls:
                    sens = layer_results[l][pname].get("lambda_sensitivity", {})
                    blk = sens.get(key)
                    if not blk:
                        continue
                    if blk["cos"]["uplift"] is not None:
                        ups.append(blk["cos"]["uplift"])
                    if blk["cos"]["perm"]:
                        ps.append(blk["cos"]["perm"]["p"])
                row[f"{gname}_{pname}"] = {
                    "cos_uplift_mean": (sum(ups) / len(ups)) if ups else None,
                    "min_p": min(ps) if ps else None,
                    "n_layers_p_lt_0.05": sum(1 for x in ps if x < 0.05),
                }
        lam_table[key] = row

    deep = group_summary.get("deep", {})
    deep_up, deep_p = deep.get("remote_j0_cos_uplift_mean"), deep.get("remote_j0_min_p")
    if deep_up is None:
        verdict = "无读数"
    elif deep_up > 0 and deep_p is not None and deep_p < 0.05:
        verdict = ("深部层远程内容线性可读（remote uplift>0 且 p<0.05）——状态写入可线性读出；"
                   "与必要性账行为侧正对比并读 = 标准架构不盲（冒烟级，判词留白待 500 窗）")
    elif deep_up <= 0 or (deep_p is not None and deep_p >= 0.05):
        verdict = ("深部层远程内容未见线性可读——行为在用 + 表示不可读 → 读出或是非线性/注意式"
                   "（冒烟级，判词留白待 500 窗）")
    else:
        verdict = "证据不足（冒烟级，判词留白）"

    summary = {
        "probe": "E122 配套表示侧 · DeltaNet 线性状态闭式读出探针（第二把尺子）",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "model_fingerprint": fingerprint,
        "hardware_note": "体制判词一律「同机同 env 内成立」（AGENTS 坑 11 纪律）",
        "companion_run": "行为侧第一把尺子 = tools/analysis/cross_arch/probe_e122_deltanet_book.py"
                         "（500 窗 contrast 0.281 nat CI[0.227,0.336] 不含 0，2026-09-11）",
        "corpus": {
            "path": str(corpus),
            "window_bytes": args.window_bytes,
            "start_window": args.start_window,
            "scored_prefix_bytes": max_byte_touched,
            "scored_prefix_sha256": prefix_sha,
            "corpus_size_at_run": os.path.getsize(corpus),
        },
        "window_definition": {
            "window": "corpus[w*4096 : (w+1)*4096] 顺序字节窗（与必要性账逐字同构）",
            "decode": "utf-8 errors=replace",
            "tokenize": "tokenizer 默认 special tokens（Mistral 系加 BOS）",
            "truncation": f"ids[:{args.max_tokens}]",
            "segment": f"token 段 = {args.segment_tokens}，跨段 = 出现段严格晚于最早出现段",
            "note": "同卷纪律：窗定义+前缀 SHA256 落此；与必要性账同窗同位选择链对拍成立",
        },
        "state_capture": {
            "method": "进程内 monkeypatch fla.layers.delta_net.chunk_delta_rule（层模块全局名）"
                      "旁路捕获 (k,v,beta) pre-l2norm；chunk 边界态独立 fp32 重算"
                      "（naive.delta_rule_chunkwise 同式）；不改库文件",
            "granularity": f"chunk 边界（{args.chunk_size} token）；S[c] = 已消费 token < c*{args.chunk_size}",
            "state_dim_per_token": state_dim,
            "verification": "首有效窗逐层：fp32 边界态终态 vs 模型核 final_state（output_final_state=True 重调），"
                            f"相对误差阈 {args.verify_tol_rel}，超阈响亮停机",
            "dtype_note": "捕获 bf16、边界态 fp32 重算（比核内 bf16 更精；对拍误差即两者差）",
        },
        "probe_design": {
            "samples": "E122 选择链选中跨段重复续尾位 t → chunk 边界 c=t//64；每边界认领 designated 源（t 最小）",
            "targets": f"近程 = 边界前第 {list(near_lags)} token（阳性对照）；远程 = designated 源 gram 第 "
                       f"0..{args.ngram_len - 1} token（源须整体在边界前 s+n≤b，否则作废计数）",
            "features": f"S_t flatten {state_dim} 维（bf16 存 fp32 算）→ 训练窗逐维标准化",
            "ridge": f"线性核对偶 ridge，λ={args.ridge_lambda}，目标 = token 输入嵌入（fp32）",
            "control": "打乱配对 = 同窗内置换目标重训同款探针；real/ctrl 同测试配对评估；uplift = real − ctrl",
            "metrics": "cos(ŷ, E[target]) + 嵌入空间最近邻 top-1 acc（候选=测试劈分目标集）；"
                       "窗级符号翻转置换检验 p（单侧 uplift>0）",
            "splits": f"窗级 train/test {args.train_frac:.0%}/{1 - args.train_frac:.0%}（种子洗牌，全层同劈）",
            "selection_diff_vs_necessity": "无稀有表过滤（探针要密度；必要账要稀有防撞）——同窗同扫描函数，选择集更大",
        },
        "params": {
            "n_windows": args.n_windows, "ngram_len": args.ngram_len, "tail": args.tail,
            "segment_tokens": args.segment_tokens, "chunk_size": args.chunk_size,
            "near_lags": list(near_lags), "remote_js": list(range(args.ngram_len)),
            "ridge_lambda": args.ridge_lambda, "train_frac": args.train_frac,
            "extra_ridge_lambdas": list(extra_lambdas),
            "near_dist_cut": args.near_dist, "remote_dist_cut": args.remote_dist,
            "n_perm": args.n_perm, "seed": args.seed,
            "probe_layers": probe_layers,
            "max_boundaries_per_window": args.max_boundaries_per_window,
        },
        "windows": summary_tally,
        "samples": summary_totals,
        "split": {"train_windows": train_win, "test_windows": test_win},
        "layer_groups": group_summary,
        "lambda_sensitivity": {"primary_lambda": args.ridge_lambda,
                               "note": "主口径=--ridge-lambda；附加 λ 共享同一状态缓存/Gram/测试核与前向，仅重解对偶系",
                               "table": lam_table},
        "verdict": verdict,
        "timing_sec": round(time.time() - t0, 1),
    }
    (out_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    with (out_dir / "probes.jsonl").open("w", encoding="utf-8") as fp:
        for l in probe_layers:
            for name, res in layer_results[l].items():
                fp.write(json.dumps({"layer": l, "probe": name, **res},
                                    ensure_ascii=False) + "\n")
    with (out_dir / "samples.jsonl").open("w", encoding="utf-8") as fp:
        for w in window_ids:
            fp.write(json.dumps({
                "window_id": w, "byte_offset": w * args.window_bytes,
                "n_tokens": win_tokens[w], "samples": samples_by_win[w],
            }, ensure_ascii=False) + "\n")
    print(json.dumps({"verdict": verdict, "layer_groups": group_summary},
                     ensure_ascii=False, indent=2), flush=True)
    print(f"[dsr] summary -> {out_dir / 'summary.json'}\n"
          f"[dsr] probes -> {out_dir / 'probes.jsonl'}\n"
          f"[dsr] samples -> {out_dir / 'samples.jsonl'}", flush=True)


if __name__ == "__main__":
    main()
