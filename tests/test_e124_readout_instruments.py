"""E124 收官五仪表雏形单测（readout_e124_five_instruments，2026-09-13）。

配套仪器：tools/analysis/v3_6/readout_e124_five_instruments.py（零训练 eval-only
五仪表：RD 扫描 / K 侧置乱 Δ / 位置先验 / 读出轨迹+地板 / 定向消融）。

Covers：
  (1) K 侧置乱探针条件创建纪律：k_row_perm_override=None（默认）与 store_block_
      override=None（默认）时 _slm_forward 前向逐位不变；
  (2) 只置换 K 侧：置乱后 backbone logits 改变，v_rows / index（V 侧与下游
      返回行）逐位不变，网格稳定；非法置换（非置换序列）响亮报错；
  (3) 纯函数代数：k_scramble_perm（置换性/决定论）、bootstrap_ci_mean（常数
      收缩/区间夹住均值/决定论/空集）、position_prior_metrics（最近邻预测器
      重合率 1.0 锚 / 远端命中重合率 0 锚 / 首近因档）、majority_floor_bytes
      （众数字节两口径）、analytic_hits（min(k, 因果候选数) 前缀和口径）。

模型级夹具：tests.test_v37_slm.tiny_config（slm a 格），同 test_e124_gate /
test_e124_soft_hard_seam 口径；全 CPU。
"""

from __future__ import annotations

import pytest
import torch

from flued.v36 import FLUEDV36
from tools.analysis.v3_6.readout_e124_five_instruments import (
    analytic_hits,
    bootstrap_ci_mean,
    k_scramble_perm,
    majority_floor_bytes,
    position_prior_metrics,
)
import tools.train.v3_6.train_v36_s1 as s1
from tests.test_v37_slm import tiny_config


def _tiny_ids(seed: int = 1) -> torch.Tensor:
    g = torch.Generator().manual_seed(seed)
    return torch.randint(1, 257, (1, 96), generator=g)


def _tiny_model(**overrides):
    torch.manual_seed(0)
    model = FLUEDV36(tiny_config(e124_budget_gate=True, tau_cut=0.0, **overrides))
    model.eval()
    return model


# --- 1. 条件创建纪律：默认 None = 旧路径逐位不变 -----------------------------------


def test_probe_kwargs_default_none_bitwise():
    model = _tiny_model()
    ids = _tiny_ids()
    with torch.no_grad():
        base = s1.s1_forward(model, ids, None)
        kw_none = s1.s1_forward(model, ids, None, k_row_perm_override=None)
        sb_none = s1.s1_forward(model, ids, None, store_block_override=None)
    for key in ("logits_backbone", "logits_direct"):
        assert torch.equal(base[key], kw_none[key]), f"k_row_perm_override=None 改变了 {key}"
        assert torch.equal(base[key], sb_none[key]), f"store_block_override=None 改变了 {key}"


# --- 2. 只置换 K 侧：backbone 变、V 侧与返回行不变；非法置换响亮 -------------------


def test_k_row_perm_k_side_only():
    model = _tiny_model()
    bb = model.backbone
    bb.e124_rt_budget = 2  # 门激活（硬门），置乱经门内 top-k 打分生效
    bb.e124_rt_hard = True
    ids = _tiny_ids()
    with torch.no_grad():
        out_i = s1.s1_forward(model, ids, None)
        n_real = int(out_i["chunks"].chunk_mask[0].sum())
        perm = k_scramble_perm(int(n_real), seed=7)
        assert perm != list(range(int(n_real)))  # 前提：非恒等置换
        out_s = s1.s1_forward(model, ids, None, k_row_perm_override=[perm])
    assert not torch.equal(out_i["logits_backbone"], out_s["logits_backbone"])
    # K 侧置乱的边界：V 侧行与下游 decode 行逐位不变（v_rows/index 返回本体）
    assert torch.equal(out_i["v_rows"], out_s["v_rows"])
    assert torch.equal(out_i["index"], out_s["index"])
    # 网格稳定（置乱不动前端分段）
    assert torch.equal(out_i["chunks"].chunk_ids, out_s["chunks"].chunk_ids)


def test_k_row_perm_invalid_loud():
    model = _tiny_model()
    ids = _tiny_ids()
    with torch.no_grad():
        out = s1.s1_forward(model, ids, None)
    n_real = int(out["chunks"].chunk_mask[0].sum())
    bad = list(range(int(n_real) - 1))  # 长度不足 → 非置换
    with pytest.raises(ValueError, match="置换"):
        with torch.no_grad():
            s1.s1_forward(model, ids, None, k_row_perm_override=[bad])


# --- 3. 纯函数代数 ------------------------------------------------------------------


def test_k_scramble_perm_properties():
    n = 11
    p1 = k_scramble_perm(n, seed=20260913)
    p2 = k_scramble_perm(n, seed=20260913)
    p3 = k_scramble_perm(n, seed=1)
    assert sorted(p1) == list(range(n))  # 置换性
    assert p1 == p2                      # 决定论
    assert p1 != p3                      # 异种子异置换
    assert k_scramble_perm(1, seed=0) == [0] and k_scramble_perm(0, seed=0) == []


def test_bootstrap_ci_algebra():
    const = bootstrap_ci_mean([0.5] * 8)
    assert const["mean"] == pytest.approx(0.5)
    assert const["ci_lo"] == pytest.approx(0.5) and const["ci_hi"] == pytest.approx(0.5)
    wide = bootstrap_ci_mean([0.0, 1.0] * 10, n_boot=2000, seed=42)
    assert wide["ci_lo"] <= wide["mean"] <= wide["ci_hi"]
    assert bootstrap_ci_mean([0.0, 1.0] * 10, n_boot=2000, seed=42) == wide  # 决定论
    assert bootstrap_ci_mean([]) == {} and bootstrap_ci_mean([None, None]) == {}


def test_position_prior_predictor_algebra():
    n, k = 6, 2
    cm = torch.ones(1, n, dtype=torch.bool)
    hit = torch.zeros(1, 1, n, n, dtype=torch.bool)
    for i in range(n):  # 预测器本身：命中 = 因果方向最近 min(k, i+1) 行
        for j in range(max(0, i - k + 1), i + 1):
            hit[0, 0, i, j] = True
    m = position_prior_metrics(hit, cm, k)
    assert m["hit_rate"] == pytest.approx(1.0)      # 纯位置命中 → 重合率恰 1
    assert m["query_head_exact_rate"] == pytest.approx(1.0)
    assert m["mean_first_lag"] == pytest.approx(0.0)  # 每查询命中含自身 → 首近因档 0
    # lag 分布：i=0 贡献 {0}，i≥1 各贡献 {0,1} → 非退化熵 > 0
    assert m["hit_lag_entropy_bits"] > 0.0
    # 远端命中对照：每查询改命中 {0,1}（对 i≥2 与最近邻预测错位）
    hit_far = torch.zeros(1, 1, n, n, dtype=torch.bool)
    for i in range(n):
        for j in (0, 1):
            if j <= i:
                hit_far[0, 0, i, j] = True
    mf = position_prior_metrics(hit_far, cm, k)
    assert mf["hit_rate"] < 1.0
    # 手算：i=0 → 1/1；i=1 → 2/2；i=2 → 1/2；i=3..5 → 0；合计 2.5/6
    assert mf["hit_rate"] == pytest.approx(5 / 12)
    # 首近因档：i=0 命中 {0}→0；i≥1 命中 {0,1}，最近行 j=1 → lag=i-1
    # 均值 = (0+0+1+2+3+4)/6 = 5/3
    assert mf["mean_first_lag"] == pytest.approx(5 / 3)
    # 远端命中把 lag 摊开 → 熵高于纯位置情形
    assert mf["hit_lag_entropy_bits"] > m["hit_lag_entropy_bits"]


def test_majority_floor_bytes_algebra():
    clean = torch.tensor([5, 5, 5, 9])
    mask = torch.tensor([False, False, True, True])
    f = majority_floor_bytes(clean, mask)
    assert f["maj_byte_all"] == 5          # 全窗众数
    assert f["maj_byte_visible"] == 5      # 可见位 [5,5] 众数
    assert f["acc_uniform"] == pytest.approx(1.0 / 256.0)
    # 遮蔽位 gold = [5,9]：全窗众数 5 命中一半；可见位众数同为 5
    gold = clean[mask]
    assert float((gold == f["maj_byte_all"]).float().mean()) == pytest.approx(0.5)


def test_analytic_hits_algebra():
    cm = torch.tensor([True, False, True, True])
    per_q, mean = analytic_hits(cm, k=1)
    assert per_q == [1, 1, 1] and mean == pytest.approx(1.0)  # min(1, cum)=1
    per_q, mean = analytic_hits(cm, k=2)
    assert per_q == [1, 2, 2] and mean == pytest.approx(5 / 3)  # min(2,[1,2,3])
    per_q, mean = analytic_hits(cm, k=99)
    assert per_q == [1, 2, 3] and mean == pytest.approx(2.0)  # 全量 = 前缀和
