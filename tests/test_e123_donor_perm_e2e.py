"""E123 乱序列跨窗置换（donor_perm）端到端测试（红队补测 2026-09-11）。

既有 test_e123_gates.py 覆盖了置换表代数（零不动点/封闭性/确定性）与注入数学
（_e123_apply_injections 的 donor_row 直算形）；本测补**端到端**：真 mask log +
真数据流 donor 料化 + tiny a 格模型，断言乱序列（--e123-mode shuffled）的注入
源确实按置换表**跨窗**取材（不是本窗行），且：
  - 注入经 _slm_forward 真链路落进 direct 腿（e123_stats 计数 + logits 变化，
    且与本窗源注入逐位不同）；
  - 跑真训练步（step_model train=True + backward）：loss 有限、读出件收梯度、
    donor 行 detach 语义保持（no_grad 取料）；
  - control 列零触发：mask/inject 全 None，loss 与 e123 整体关闭逐位同值
    （「纯续训 + 仪表 = 地板参照」的端到端锚）。

数据流口径与训练器同构：donor 窗料化走 _e123_materialize_windows 本体
（StreamingReconstructionDataset, batch=1, 同种子重放），当前窗 = 同一回放流
wi=0（训练器里两者本就是同一条流）。boundary_mode=uniform 钉死分段确定性。
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import torch

from flued.v36 import FLUEDV36
import tools.train.v3_6.train_v36_s1 as s1
from tests.test_v37_slm import _s1_args, tiny_config

DEVICE = torch.device("cpu")


@pytest.fixture()
def _e123_state(monkeypatch):
    """模块级 E123 状态隔离：测试后全量复位（同 test_e123_gates 口径）。"""
    saved = (s1._E123_LOG, s1._E123_KMAX_SCHED, s1._E123_DONOR, s1._E123_DONOR_WINDOWS)
    yield
    (s1._E123_LOG, s1._E123_KMAX_SCHED, s1._E123_DONOR, s1._E123_DONOR_WINDOWS) = saved


def _corpus(tmp_path: Path, n_chars: int = 24000) -> str:
    """非周期合成语料（二次相位，杜绝 8B 块重合假前提）+ 换行供行首吸附。"""
    chars = []
    for k in range(n_chars):
        if k % 40 == 39:
            chars.append("\n")
        else:
            chars.append(chr(97 + (k * 7 + (k * k) // 5) % 26))
    p = tmp_path / "corpus.txt"
    p.write_text("".join(chars), encoding="utf-8")
    return str(p)


def _mask_log(tmp_path: Path, n_windows: int = 4) -> dict:
    """4 窗 mask log：wi 0-2 各一枚依赖对（src_chunk 0, 遮 [0,8), 依赖位
    [16,17)）；wi 3 无料（eligible 集封闭性旁观）。"""
    def entry(wi, pairs):
        return {"window_id": wi, "n_real": 32, "masked_chunks": [p["src_chunk"] for p in pairs],
                "info_scores": {}, "dependency_pairs": pairs}

    def pair():
        return {"src_chunk": 0, "src_byte_range": [0, 8], "distance": 1,
                "positions": [16, 17], "info": 0.1}

    entries = [entry(wi, [pair()] if wi < 3 else []) for wi in range(n_windows)]
    p = tmp_path / "mask_log.jsonl"
    p.write_text("".join(json.dumps(e) + "\n" for e in entries), encoding="utf-8")
    return str(p)


def _tiny_model() -> FLUEDV36:
    torch.manual_seed(0)
    return FLUEDV36(tiny_config(boundary_mode="uniform")).eval()


def _window_args(data_path: str, seq_len: int, **over):
    args = _s1_args()
    base = dict(
        data_path=data_path, seq_len=seq_len, amp=False, mask_prob=0.0,
        e123_mode="shuffled", e123_window_id=0, e123_step=500,
        e123_lambda_ramp=1, e123_cuts_pin=False, e123_mask_log="synthetic",
    )
    base.update(over)
    for k, v in base.items():
        setattr(args, k, v)
    return args


def _front_rows(model, window: torch.Tensor):
    """_e123_donor_metas 的部分前向复算口径（_encode→…→_slm_store_rows）。"""
    with torch.no_grad():
        bs, conf, val, _ = model._encode(window)
        hc, u8, _ = model._cuts(window, conf, val)
        dch = model.chunk_builder(bs, val, hc, conf)
        dch = model.bridge(dch, bs, conf, val, u8)
        _, v_rows, _, _, _, _, _ = model._slm_store_rows(dch, with_views=True)
    return dch, v_rows


def test_e123_donor_perm_end_to_end(_e123_state, tmp_path):
    data_path = _corpus(tmp_path)
    seq_len = 32  # uniform 切点 0/8/16/24 → 恰 4 真实块（tiny max_chunks=4）
    args = _window_args(data_path, seq_len)
    model = _tiny_model()

    s1._E123_LOG = s1._load_e123_mask_log(str(_mask_log(tmp_path)))
    s1._E123_KMAX_SCHED = s1._e123_parse_kmax("2:0")
    s1._E123_DONOR = s1._e123_build_donor_perm(s1._E123_LOG, seed=7)
    s1._E123_DONOR_WINDOWS = s1._e123_materialize_windows(args, 4)

    # 置换表前提：零不动点、封闭于 eligible 集
    perm = s1._E123_DONOR
    assert sorted(perm) == [0, 1, 2] and sorted(perm.values()) == [0, 1, 2]
    assert all(perm[w] != w for w in perm)

    clean = s1._E123_DONOR_WINDOWS[0].unsqueeze(0)  # 当前窗 = 同流 wi=0
    donor_win = s1._E123_DONOR_WINDOWS[perm[0]]
    assert clean.size(1) == seq_len and donor_win.numel() == seq_len
    assert not torch.equal(clean[0, :8], donor_win[:8])  # 前提非空：跨窗字节确不同

    plan, mask, inject, cuts = s1._e123_window_plan(model, clean, args, DEVICE)
    assert cuts is None  # cuts_pin 关 = 旧路径逐位不变
    assert mask is not None and mask.shape == (1, 1, 1, seq_len)
    assert bool(mask[0, 0, 0, :8].all()) and not bool(mask[0, 0, 0, 8:].any())
    assert plan["kmax"] == 2 and len(plan["kept"]) == 1
    meta = inject[0][0]
    assert meta["lam"] == 1.0  # ramp=1, step=500 → λ 满档
    assert meta["donor_row"] is not None and not meta["donor_row"].requires_grad

    # —— 核心断言：注入源 = 置换表指向的 donor 窗行（不是本窗行）——
    dch, d_vrows = _front_rows(model, donor_win.unsqueeze(0))
    c_d = int(dch.chunk_ids[0][min(meta["src_range"][0], donor_win.numel() - 1)])
    assert torch.equal(meta["donor_row"], d_vrows[0, c_d].detach())
    _ch_cur, v_cur = _front_rows(model, clean)
    c_src = int(_ch_cur.chunk_ids[0][meta["src_range"][0]])
    assert not torch.equal(d_vrows[0, c_d], v_cur[0, c_src])  # 跨窗 ≠ 本窗同位行

    # —— 注入经真链路落 direct 腿，且与本窗源注入逐位不同 ——
    byte_mask = torch.zeros_like(clean, dtype=torch.bool)
    out_donor = s1.s1_forward(model, clean, args, clean=clean, byte_mask=byte_mask,
                              e123_inject=inject)
    assert out_donor["e123_stats"] == {"pairs": 1, "positions": 2}
    out_ctrl = s1.s1_forward(model, clean, args, clean=clean, byte_mask=byte_mask,
                             e123_inject=None)
    assert out_ctrl["e123_stats"] is None
    assert not torch.equal(out_donor["logits_direct"], out_ctrl["logits_direct"])
    inject_sw = [[{**meta, "donor_row": None}]]  # 本窗源（combined 形态对照）
    out_sw = s1.s1_forward(model, clean, args, clean=clean, byte_mask=byte_mask,
                           e123_inject=inject_sw)
    assert not torch.equal(out_donor["logits_direct"], out_sw["logits_direct"])

    # —— 真训练步：loss 有限 + 读出件收梯度（第七性质经 dec_in 保持）——
    loss, _metrics = s1.step_model(model, (clean,), args, DEVICE, train=True)
    assert torch.isfinite(loss)
    loss.backward()
    g = model.decoder_in_mem.weight.grad
    assert g is not None and bool(torch.isfinite(g).all()) and float(g.abs().sum()) > 0


def test_e123_control_column_bitwise_equals_off(_e123_state, tmp_path):
    """control 列零触发端到端：mask/inject 全 None → loss 与 e123 整体关闭
    逐位同值（mask_prob=0 消掉掩码 RNG，前向确定性 → 可比逐位）。"""
    data_path = _corpus(tmp_path)
    seq_len = 32
    args_shuf = _window_args(data_path, seq_len)
    model = _tiny_model()
    s1._E123_LOG = s1._load_e123_mask_log(str(_mask_log(tmp_path)))
    s1._E123_KMAX_SCHED = s1._e123_parse_kmax("2:0")
    s1._E123_DONOR = s1._e123_build_donor_perm(s1._E123_LOG, seed=7)
    s1._E123_DONOR_WINDOWS = s1._e123_materialize_windows(args_shuf, 4)
    clean = s1._E123_DONOR_WINDOWS[0].unsqueeze(0)

    args_ctrl = _window_args(data_path, seq_len, e123_mode="control")
    plan, mask, inject, cuts = s1._e123_window_plan(model, clean, args_ctrl, DEVICE)
    assert mask is None and inject is None and cuts is None and plan["pairs"]

    loss_ctrl, m_ctrl = s1.step_model(model, (clean,), args_ctrl, DEVICE, train=True)
    args_off = _window_args(data_path, seq_len, e123_mask_log="")
    assert not s1._e123_enabled(args_off)
    loss_off, m_off = s1.step_model(model, (clean,), args_off, DEVICE, train=True)
    assert loss_ctrl.item() == loss_off.item()
    assert m_ctrl["direct_loss"] == m_off["direct_loss"]
    assert m_ctrl["completion_loss"] == m_off["completion_loss"]
