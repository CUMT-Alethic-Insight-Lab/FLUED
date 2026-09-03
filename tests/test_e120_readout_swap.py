"""E120 端到端点燃臂单测（任务书冻结 v1+修订 v2 2026-09-03:
docs/versions/v3.7/FLUED_V3_7_E120_END_TO_END_IGNITION_20260903_CN.md; 模型件在
flued/v36/model.py 的 E120WarmReadout, 训练器旋钮在 tools/train/v3_6/train_v36_s1.py
的 --e120-readout-swap/--e120-fit-dir, t=0 仪器在
tools/analysis/v3_6/probe_e120_t0_decodability.py）。

Covers: (1) 关闭态逐比特对照（旗标关 = 无新件/无新键, 老 ckpt strict-load 干净;
旗标开不动共享权重——新件在 __init__ 末尾创建不消耗上游 RNG）; (2) 配置守卫
（非 d 格/gdn2/readout_views>1 响亮报错）; (3) 旋钮接通 = v_rows 整行换源
（生产拼接点 _slm_store_rows 的 v_rows == 读出件直算, state_norm 诊断口径不变,
被替换的 package_v.mean 行不再进链）; (4) 读出件代数（torch 路径 = einsum 手工
复算, chunk_mask 遮罩语义）; (5) 温启动装载（loud-fail 缺目录/缺件/缺键/形不符;
成功路径 = slot_query<-ridge 主方向, proj<-部署桥折叠 scale+截距行）; (6) 甲列
冻结/乙列解冻语义（全冻含新件 trainable=0 / 全解冻 frozen=0, tied byte_lookup
无别名敞口）; (7) parser 默认关; (8) t=0 仪器判读线与解码代数。
Tiny 随机初始化 d 格 (k=state, v=state) CPU 模型 (kda_impl="torch"),
boundary_mode="uniform" 保持分块确定; 只测接线与代数, 不测训练行为。
"""

from __future__ import annotations

import json
from types import SimpleNamespace

import numpy as np
import pytest
import torch
import torch.nn.functional as F

from flued.v36 import FLUEDV36
from flued.v36.model import E120WarmReadout, _kda_scan_post_states
import tools.train.v3_6.train_v36_s1 as s1
from tools.analysis.v3_6 import probe_e120_t0_decodability as t0probe
from tests.test_v37_oracle_probe import _tiny_c_config

DEVICE = torch.device("cpu")
H, HK, HV, D_PACK = 2, 16, 32, 64  # tiny d 格 kda 头/键宽/值宽/生产行宽


def _tiny_d_config(**overrides):
    # d 格 (k=state, v=state): write_head/state_machine (V) + write_head_k/
    # state_machine_k (K) 双通道在岗
    return _tiny_c_config(k_row_source="state", v_row_source="state", **overrides)


def _model(seed: int = 0, **overrides) -> FLUEDV36:
    torch.manual_seed(seed)
    return FLUEDV36(_tiny_d_config(**overrides)).eval()


def _e120_model(seed: int = 0) -> FLUEDV36:
    return _model(seed, e120_readout_swap=True)


def _ids(seed: int = 1, t: int = 96):
    g = torch.Generator().manual_seed(seed)
    return torch.randint(1, 257, (1, t), generator=g)


def _toy_gates(n: int = 6, seed: int = 3, requires_grad: bool = False):
    g = torch.Generator().manual_seed(seed)
    kk = torch.randn(1, n, H, HK, generator=g, requires_grad=requires_grad)
    return kk, {
        "k": F.normalize(kk, dim=-1),
        "v": torch.randn(1, n, H, HV, generator=g),
        "beta": torch.rand(1, n, H, generator=g) * 0.5 + 0.25,
        "alpha": torch.full((1, 1, H, HK), 0.9),
    }


def _toy_fit_dir(tmp_path, with_bridge: bool = True, with_ridge: bool = True,
                 w_shape=(H * HV + 1, D_PACK), ridge_shape=(H, HK)):
    """玩具温启动产物目录: bridge_deploy.npz (W/scale/lam) + q_ridge_dir.npz
    (q_ridge)。Returns (W, scale, q_ridge|None)。"""
    tmp_path.mkdir(parents=True, exist_ok=True)
    g = torch.Generator().manual_seed(5)
    W = torch.randn(*w_shape, generator=g) * 0.02
    scale = 1.7
    q_ridge = None
    if with_bridge:
        np.savez(tmp_path / "bridge_deploy.npz", W=W.numpy(), scale=np.float64(scale),
                 lam=np.float64(10.0))
    if with_ridge:
        q_ridge = torch.randn(*ridge_shape, generator=g)
        np.savez(tmp_path / "q_ridge_dir.npz", q_ridge=q_ridge.numpy())
    return W, scale, q_ridge


# --- 1. 关闭态逐比特对照 -------------------------------------------------------


def test_off_no_module_no_keys_strict_load_clean():
    model = _model()
    assert not hasattr(model, "e120_readout")
    assert not any(k.startswith("e120_readout.") for k in model.state_dict())
    # 老 ckpt strict-load 干净: 关态键集 == 历史键集
    model.load_state_dict(model.state_dict(), strict=True)


def test_flag_on_shared_weights_bit_identical():
    """旗标开不扰动共享权重（新件在 __init__ 末尾创建, 不消耗上游 RNG）。"""
    off, on = _model(), _e120_model()
    assert torch.equal(off.byte_lookup.embedding.weight, on.byte_lookup.embedding.weight)
    assert torch.equal(off.decoder.slot, on.decoder.slot)
    assert torch.equal(off.state_machine.readout_query, on.state_machine.readout_query)
    assert torch.equal(off.write_head.to_v.weight, on.write_head.to_v.weight)


def test_config_guards():
    # 非 d 格响亮报错 (结构性 N/A 不静默): c 格 k=index / b 格 v=memory
    with pytest.raises(ValueError, match="e120_readout_swap requires"):
        FLUEDV36(_tiny_c_config(e120_readout_swap=True))
    with pytest.raises(ValueError, match="e120_readout_swap requires"):
        FLUEDV36(_tiny_c_config(k_row_source="state", v_row_source="memory",
                                e120_readout_swap=True))
    with pytest.raises(ValueError, match="recurrence='kda' only"):
        _model(e120_readout_swap=True, recurrence="gdn2")
    with pytest.raises(ValueError, match="readout_views"):
        _model(e120_readout_swap=True, readout_views=2)


def test_parser_defaults_off():
    from tools.train.v3_6.train_v36 import build_parser

    parser = build_parser()
    s1._add_s1_args(parser)
    args = parser.parse_args([])
    assert args.e120_readout_swap is False
    assert args.e120_fit_dir == "outputs/e120_warmstart_fit_20260903"


# --- 2. 旋钮接通 = v_rows 整行换源 -----------------------------------------------


def test_knob_swaps_v_rows_source():
    off, on = _model(), _e120_model()
    ids = _ids()
    out_off = s1._slm_forward(off, ids, SimpleNamespace())
    out_on = s1._slm_forward(on, ids, SimpleNamespace())
    # 生产拼接点 v_rows == 读出件直算 (同输入同网格)
    gates_v = on.write_head(out_on["memory"])
    ref = on.e120_readout(gates_v, out_on["chunks"].chunk_mask)
    assert torch.equal(out_on["v_rows"], ref)
    # 换源生效: 与被替换的 package_v.mean 旧产源不同
    assert not torch.equal(out_off["v_rows"], out_on["v_rows"])
    # state_norm 诊断口径不变 (被替换的生产读出照跑出链外)
    assert torch.equal(out_off["state_norm"], out_on["state_norm"])
    # K 通道 index 行与 logits 网格形状不动 (v_rows 换源不碰 K 侧)
    assert torch.equal(out_off["index"], out_on["index"])
    assert out_off["logits_direct"].shape == out_on["logits_direct"].shape


def test_readout_piece_gets_gradient_in_full_unfreeze():
    """乙列语义: 全模型解冻, 梯度落到新件 slot_query/proj 且穿过写入侧。"""
    model = _e120_model()
    n_train, n_frozen = s1._e120_unfreeze_all(model)
    assert n_frozen == 0 and n_train > 0
    base = dict(
        mask_prob=0.0, mask_span_min=1, mask_span_max=8, mask_mode="byte_span",
        max_chunks=32, max_span=16, task1_loss_weight=1.0, task2_loss_weight=1.0,
        predict_weight=1.0, predict_mode="latent", amp=False,
    )
    loss, _metrics = s1.step_model(model, (_ids(),), SimpleNamespace(**base), DEVICE, train=True)
    assert torch.isfinite(loss)
    loss.backward()
    for name in ("e120_readout.slot_query", "e120_readout.proj.weight", "e120_readout.proj.bias"):
        p = dict(model.named_parameters())[name]
        assert p.grad is not None and torch.isfinite(p.grad).all() and p.grad.abs().sum() > 0, name
    # 全解冻: 梯度穿新件落到写入侧 (乙列"主干会用"判据的梯度通路证据)
    assert model.write_head.to_v.weight.grad is not None
    assert model.write_head.to_v.weight.grad.abs().sum() > 0


# --- 3. 读出件代数 ---------------------------------------------------------------


def test_warm_readout_torch_algebra():
    rd = E120WarmReadout(_tiny_d_config()).eval()
    _kk, gates = _toy_gates(n=6)
    mask = torch.ones(1, 6, dtype=torch.bool)
    out = rd(gates, mask)
    assert out.shape == (1, 6, D_PACK) and out.dtype == torch.float32
    states = _kda_scan_post_states(gates, mask)
    ref = torch.einsum("qhk,bchkv->bcqhv", rd.slot_query.float(), states)
    ref = rd.proj(ref.reshape(1, 6, H * HV))
    assert torch.allclose(out, ref, atol=1e-6)


def test_warm_readout_chunk_mask_semantics():
    """padding chunk 不进状态递推: 尾部遮罩后前缀读出行逐位不变。"""
    rd = E120WarmReadout(_tiny_d_config()).eval()
    _kk, gates = _toy_gates(n=6)
    full = rd(gates, torch.ones(1, 6, dtype=torch.bool))
    mask = torch.tensor([[True, True, True, True, False, False]])
    masked = rd(gates, mask)
    assert torch.allclose(masked[:, :4], full[:, :4], atol=1e-6)


def test_warm_readout_gradient_flows_to_gates():
    rd = E120WarmReadout(_tiny_d_config()).eval()
    kk, gates = _toy_gates(n=5, requires_grad=True)
    out = rd(gates, torch.ones(1, 5, dtype=torch.bool))
    out.square().mean().backward()
    assert rd.slot_query.grad is not None and rd.slot_query.grad.abs().sum() > 0
    assert kk.grad is not None and torch.isfinite(kk.grad).all() and kk.grad.abs().sum() > 0


# --- 4. 温启动装载 ---------------------------------------------------------------


def test_warm_start_loud_fail(tmp_path):
    model = _e120_model()
    with pytest.raises(SystemExit, match="温启动产物目录缺席"):
        s1._e120_warm_start(model, str(tmp_path / "missing"))
    # 缺部署桥
    _toy_fit_dir(tmp_path / "nobridge", with_bridge=False)
    with pytest.raises(SystemExit, match="部署桥缺席"):
        s1._e120_warm_start(model, str(tmp_path / "nobridge"))
    # 部署桥缺键
    bad = tmp_path / "badkey"
    bad.mkdir(parents=True)
    np.savez(bad / "bridge_deploy.npz", W=np.zeros((H * HV + 1, D_PACK), dtype=np.float32))
    with pytest.raises(SystemExit, match="缺 scale 键"):
        s1._e120_warm_start(model, str(bad))
    # 部署桥形状不符
    badw = tmp_path / "badw"
    _toy_fit_dir(badw, w_shape=(H * HV, D_PACK + 1))
    with pytest.raises(SystemExit, match="部署桥形状不符"):
        s1._e120_warm_start(model, str(badw))
    # 缺 ridge 主方向件
    noridge = tmp_path / "noridge"
    _toy_fit_dir(noridge, with_ridge=False)
    with pytest.raises(SystemExit, match="ridge 段 1 主方向缺席"):
        s1._e120_warm_start(model, str(noridge))
    # 主方向形状不符
    badq = tmp_path / "badq"
    _toy_fit_dir(badq, ridge_shape=(H, HK + 1))
    with pytest.raises(SystemExit, match="q_ridge 形状不符"):
        s1._e120_warm_start(model, str(badq))


def test_warm_start_contents(tmp_path):
    W, scale, q_ridge = _toy_fit_dir(tmp_path)
    model = _e120_model()
    note = s1._e120_warm_start(model, str(tmp_path))
    assert "q_ridge" in note and "部署桥" in note
    rd = model.e120_readout
    assert torch.equal(rd.slot_query[0], q_ridge)  # 槽查询 = ridge 段 1 主方向
    assert torch.allclose(rd.proj.weight, (W[:-1] / scale).T, atol=1e-6)  # 折叠 scale
    assert torch.allclose(rd.proj.bias, W[-1], atol=1e-6)  # 截距行
    # 装载后前向 == apply_bridge 应用形 [v̂/scale, 1] @ W (部署语义闭环)
    _kk, gates = _toy_gates(n=4)
    mask = torch.ones(1, 4, dtype=torch.bool)
    states = _kda_scan_post_states(gates, mask)
    vh = torch.einsum("qhk,bchkv->bcqhv", rd.slot_query.float(), states).reshape(1, 4, H * HV)
    x1 = torch.cat([vh / scale, torch.ones(1, 4, 1)], dim=-1)
    assert torch.allclose(rd(gates, mask), x1 @ W, atol=1e-5)


# --- 5. 甲列冻结 / 乙列解冻语义 ----------------------------------------------------


def test_freeze_all_includes_new_piece():
    model = _e120_model()
    n_train, n_frozen = s1._e120_freeze_all(model)
    assert n_train == 0 and n_frozen > 0
    assert all(not p.requires_grad for p in model.parameters())
    assert model.e120_readout.slot_query.requires_grad is False
    # tied 字节表同一参数对象, named_parameters 去重后冻结是全集无别名敞口
    assert model.decoder.byte_lookup is model.byte_lookup


def test_unfreeze_all_includes_new_piece():
    model = _e120_model()
    s1._e120_freeze_all(model)
    n_train, n_frozen = s1._e120_unfreeze_all(model)
    assert n_frozen == 0
    assert all(p.requires_grad for p in model.parameters())
    assert model.e120_readout.proj.weight.requires_grad is True


# --- 6. t=0 仪器 --------------------------------------------------------------------


def test_t0_judgment_line():
    # 判读线 = 参照带基尺 −3pp (修订 v2 钉死: 0.6078 → 0.5778)
    assert t0probe.judgment_line(0.6078) == 0.5778


def test_t0_decode_acc_algebra():
    g = torch.Generator().manual_seed(9)
    rows = torch.randn(40, H * HV, generator=g)
    W = torch.randn(H * HV + 1, 258, generator=g) * 0.02
    ys = torch.randint(0, 258, (40,), generator=g)
    yv = torch.ones(40, dtype=torch.bool)
    acc = t0probe.decode_acc(rows, ys, yv, W)
    x1 = torch.cat([rows, torch.ones(40, 1)], dim=1)
    ref = float((x1 @ W).argmax(dim=-1).eq(ys).float().mean())
    assert acc == pytest.approx(ref)
    # 槽内无有效样本 = None; 特征宽不符 = 响亮报错
    assert t0probe.decode_acc(rows, ys, torch.zeros(40, dtype=torch.bool), W) is None
    with pytest.raises(SystemExit, match="特征宽不符"):
        t0probe.decode_acc(rows[:, :8], ys, yv, W)


def test_t0_load_deploy_probe_loud_fail(tmp_path):
    with pytest.raises(SystemExit, match="部署件缺席"):
        t0probe.load_deploy_probe(tmp_path)
    np.savez(tmp_path / "probe_t0.npz", probe_slots=np.array([0]), W_probe=np.zeros((1, 5, 258)))
    with pytest.raises(SystemExit, match="缺 W_probe_prod 键"):
        t0probe.load_deploy_probe(tmp_path)
