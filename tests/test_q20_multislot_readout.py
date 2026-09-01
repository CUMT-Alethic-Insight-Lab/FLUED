"""Q20 多槽读出臂单测（E119; 任务书冻结 v1 2026-08-29:
docs/versions/v3.7/FLUED_V3_7_Q20_MULTISLOT_READOUT_20260829_CN.md; 训练器旋钮在
tools/train/v3_6/train_v36_s1.py 的 --multislot-readout-* 旗标族, 模型件在
flued/v36/model.py 的 MultiSlotReadout/CGRidgeReadout）。

Covers: (1) 关闭态逐比特对照（旗标关 = 无新件/无新键, direct 腿手工复算逐位
一致; 旗标开但 eval(train=False) 与关态逐位一致）; (2) 旋钮接通 = 只进 direct
腿（train 态旗标开: direct logits 变, backbone 腿与 predict 锚 v_rows 逐位未
动）; (3) 冻结白名单（仅 multislot_readout.* 可训, tied byte_lookup 不误伤不
误放, CG 臂只 2 键）; (4) 温启动装载（loud-fail 缺件/缺键/形不符; 成功路径 =
槽0 ridge 主方向 + 其余槽逐头正交 + 投影槽0块部署桥/余块置零/偏置截距; CG 臂
只装段2 投影且不需要主方向件）; (5) CG 迭代件（T=8 逼闭式解的代数对照 +
梯度穿迭代件流通 + 形状）; (6) 探针五列（q20_k 列确定性与同链性, q20_e68
归因列接线, 旗标关 = 四列旧行为回归, 自检门锚切换）; (7) 主方向生成器代数
（ridge_readout_directions 键空间形 == Gram 形闭式, principal_direction 主
方向恢复）。
Tiny 随机初始化 b 格 (k=state, v=memory) CPU 模型, boundary_mode="uniform"
保持分块确定; 只测接线与代数, 不测训练行为。
"""

from __future__ import annotations

import json
from types import SimpleNamespace

import numpy as np
import pytest
import torch
import torch.nn.functional as F

from flued.v36 import FLUEDV36
from flued.v36.model import CGRidgeReadout, MultiSlotReadout, Q20_CG_LAM, _kda_scan_post_states
import tools.train.v3_6.train_v36_s1 as s1
from tools.analysis.v3_6 import probe_decoder_denoise_eval as probe
from tools.analysis.v3_6 import probe_q20_ridge_direction as q20gen
from tools.analysis.v3_6.probe_oracle_write_verdict import _front_end, trained_states
from tests.test_v37_oracle_probe import _tiny_c_config

DEVICE = torch.device("cpu")
H, HK, HV, D_MEM = 2, 16, 32, 96  # tiny b 格 kda 头/键宽/值宽/decoder 入口宽


def _tiny_b_config(**overrides):
    # b 格 (k=state, v=memory): write_head_k/state_machine_k/decoder_in_mem 在岗
    return _tiny_c_config(k_row_source="state", v_row_source="memory", **overrides)


def _model(seed: int = 0, **overrides) -> FLUEDV36:
    torch.manual_seed(seed)
    return FLUEDV36(_tiny_b_config(**overrides)).eval()


def _q20_model(seed: int = 0, k: str = "4") -> FLUEDV36:
    return _model(seed, multislot_readout=True, multislot_readout_k=k)


def _ids(seed: int = 1, t: int = 96):
    g = torch.Generator().manual_seed(seed)
    return torch.randint(1, 257, (1, t), generator=g)


def _q20_args(**overrides):
    args = SimpleNamespace(multislot_readout=True)
    for k, v in overrides.items():
        setattr(args, k, v)
    return args


def _toy_fuzz_dir(tmp_path, with_ridge: bool = True, ridge_shape=(H, HK)):
    """玩具温启动产物目录: fuzz_stats.json (grade_map light→opt) +
    bridge_light.npz (W/scale/lam, λ=1.0) + resid_chol_light.npz (L/rho/lam)
    (+ q20_ridge_dir.npz 主方向件)。"""
    tmp_path.mkdir(parents=True, exist_ok=True)
    g = torch.Generator().manual_seed(5)
    W = torch.randn(H * HV + 1, D_MEM, generator=g) * 0.02
    scale = 1.7
    (tmp_path / "fuzz_stats.json").write_text(
        json.dumps({"grade_map": {"light": "opt"}}), encoding="utf-8"
    )
    np.savez(tmp_path / "bridge_light.npz", W=W.numpy(), scale=np.float64(scale), lam=np.float64(1.0))
    np.savez(
        tmp_path / "resid_chol_light.npz",
        L=(torch.eye(D_MEM) * 0.1).numpy(), rho=np.float64(0.8), lam=np.float64(1.0),
    )
    if with_ridge:
        q_ridge = torch.randn(*ridge_shape, generator=g)
        np.savez(
            tmp_path / "q20_ridge_dir.npz",
            q_ridge=q_ridge.numpy(), lam_unmix=np.float64(0.01),
            n_dirs=np.int64(64), mean_norm=np.float64(0.5),
        )
    return W, scale


def _toy_gates(n: int = 6, seed: int = 3, requires_grad: bool = False):
    g = torch.Generator().manual_seed(seed)
    kk = torch.randn(1, n, H, HK, generator=g, requires_grad=requires_grad)
    return kk, {
        "k": F.normalize(kk, dim=-1),
        "v": torch.randn(1, n, H, HV, generator=g),
        "beta": torch.rand(1, n, H, generator=g) * 0.5 + 0.25,
        "alpha": torch.full((1, 1, H, HK), 0.9),
    }


# --- 1. 关闭态逐比特对照 -------------------------------------------------------


def test_off_no_module_no_keys_bit_identical():
    model = _model()
    assert not hasattr(model, "multislot_readout")
    assert not any(k.startswith("multislot_readout.") for k in model.state_dict())
    out = s1._slm_forward(model, _ids(), SimpleNamespace(), train=True)
    assert out["q20_engaged"] == 0.0
    # direct 腿 = decoder_in_mem(v_rows)+pos→decoder 手工复算, 逐位一致
    n = out["chunks"].chunk_mask.size(1)
    pos = model.chunk_pos.weight.unsqueeze(0)[:, :n]
    ref = model.decoder(model.decoder_in_mem(out["v_rows"]) + pos, out["chunks"].token_mask)
    assert torch.equal(ref, out["logits_direct"])


def test_flag_on_eval_bit_identical_to_off():
    """旗标开但 eval (train=False): 读出件不进前向, 与关态逐位一致 (同种子
    共享权重逐位相等——新件在 __init__ 末尾创建, 不消耗上游 RNG)。"""
    off, on = _model(), _q20_model()
    assert torch.equal(off.decoder_in_mem.weight, on.decoder_in_mem.weight)
    assert torch.equal(off.chunk_pos.weight, on.chunk_pos.weight)
    ids = _ids()
    out_off = s1._slm_forward(off, ids, SimpleNamespace(), train=False)
    out_on = s1._slm_forward(on, ids, _q20_args(), train=False)
    assert out_on["q20_engaged"] == 0.0
    assert torch.equal(out_off["logits_direct"], out_on["logits_direct"])
    assert torch.equal(out_off["logits_backbone"], out_on["logits_backbone"])


def test_parser_defaults_off():
    from tools.train.v3_6.train_v36 import build_parser

    parser = build_parser()
    s1._add_s1_args(parser)
    args = parser.parse_args([])
    assert args.multislot_readout is False
    assert args.multislot_readout_k == "4"
    assert args.multislot_readout_fuzz_id == "outputs/decoder_denoise_fuzz_id_20260829"


def test_config_guards():
    # 非 b 格/非 kda 响亮报错 (结构性 N/A 不静默)
    with pytest.raises(ValueError, match="multislot_readout requires"):
        FLUEDV36(_tiny_c_config(multislot_readout=True))  # c 格: k=index
    with pytest.raises(ValueError, match="recurrence='kda' only"):
        _model(multislot_readout=True, recurrence="gdn2")
    with pytest.raises(ValueError, match="multislot_readout_k"):
        _model(multislot_readout=True, multislot_readout_k="3")
    # 老 ckpt strict-load 干净: 关态模型键集 == 历史键集 (无新件)
    off = _model()
    off.load_state_dict(off.state_dict(), strict=True)


# --- 2. 旋钮接通 = 只进 direct 腿 -----------------------------------------------


def test_knob_engages_direct_leg_only():
    off, on = _model(), _q20_model()
    ids = _ids()
    out_off = s1._slm_forward(off, ids, SimpleNamespace())
    out_on = s1._slm_forward(on, ids, _q20_args(), train=True)
    assert out_on["q20_engaged"] == 1.0
    # predict 锚 (v_rows) 与 backbone 腿逐位未动
    assert torch.equal(out_off["v_rows"], out_on["v_rows"])
    assert torch.equal(out_off["logits_backbone"], out_on["logits_backbone"])
    # direct 腿确实换了读出行
    assert not torch.equal(out_off["logits_direct"], out_on["logits_direct"])


def test_step_model_trains_only_readout_piece():
    model = _q20_model()
    s1._multislot_readout_freeze(model)
    base = dict(
        mask_prob=0.0, mask_span_min=1, mask_span_max=8, mask_mode="byte_span",
        max_chunks=32, max_span=16, task1_loss_weight=1.0, task2_loss_weight=1.0,
        predict_weight=1.0, predict_mode="latent", amp=False,
        multislot_readout=True,
    )
    loss, metrics = s1.step_model(model, (_ids(),), SimpleNamespace(**base), DEVICE, train=True)
    assert torch.isfinite(loss)
    assert float(metrics["q20_engaged"]) == 1.0
    loss.backward()
    saw_grad = False
    for name, p in model.named_parameters():
        if name.startswith("multislot_readout."):
            assert p.grad is not None and torch.isfinite(p.grad).all() and p.grad.abs().sum() > 0, name
            saw_grad = True
        else:
            assert p.grad is None or p.grad.abs().sum() == 0, name
    assert saw_grad


# --- 3. 冻结白名单 ---------------------------------------------------------------


def test_freeze_whitelist_k_arm():
    model = _q20_model(k="4")
    n_train, n_frozen = s1._multislot_readout_freeze(model)
    assert n_train == 3  # slot_query + proj.weight + proj.bias
    assert n_frozen > 0
    assert model.multislot_readout.slot_query.requires_grad is True
    assert model.multislot_readout.proj.weight.requires_grad is True
    # 端口/decoder/写入侧/前端全冻 (本臂连 decoder 也冻——与去噪臂反向)
    assert model.decoder_in_mem.weight.requires_grad is False
    assert model.chunk_pos.weight.requires_grad is False
    assert model.decoder.slot.requires_grad is False
    for mod in (model.backbone, model.summarizer, model.write_head_k, model.state_machine_k, model.decoder):
        assert all(not p.requires_grad for p in mod.parameters())
    # tied 字节表: 同一参数对象, 不命中白名单, 留在冻结侧 (不误伤不误放)
    assert model.decoder.byte_lookup is model.byte_lookup
    assert model.byte_lookup.embedding.weight.requires_grad is False


def test_freeze_whitelist_cg_arm():
    model = _q20_model(k="cg")
    assert isinstance(model.multislot_readout, CGRidgeReadout)
    n_train, _ = s1._multislot_readout_freeze(model)
    assert n_train == 2  # CG 臂无槽查询: 仅段2 投影 weight+bias
    assert model.multislot_readout.proj.weight.requires_grad is True


# --- 4. 温启动装载 ---------------------------------------------------------------


def test_warm_start_loud_fail(tmp_path):
    model = _q20_model(k="4")
    with pytest.raises((SystemExit, FileNotFoundError)):  # 目录缺席
        s1._multislot_readout_warm_start(model, str(tmp_path / "missing"))
    _toy_fuzz_dir(tmp_path, with_ridge=False)
    with pytest.raises(SystemExit, match="ridge 段 1 主方向缺席"):  # k 槽臂缺主方向件
        s1._multislot_readout_warm_start(model, str(tmp_path))
    # 主方向形状不符
    bad = tmp_path / "badshape"
    _toy_fuzz_dir(bad, with_ridge=True, ridge_shape=(H, HK + 1))
    with pytest.raises(SystemExit, match="q_ridge 形状不符"):
        s1._multislot_readout_warm_start(_q20_model(k="4"), str(bad))
    # 部署桥形状不符
    badw = tmp_path / "badw"
    _toy_fuzz_dir(badw)
    z = np.load(badw / "bridge_light.npz")
    np.savez(badw / "bridge_light.npz", W=np.zeros((H * HV, D_MEM + 1), dtype=np.float32),
             scale=z["scale"], lam=z["lam"])
    with pytest.raises(SystemExit, match="部署桥形状不符"):
        s1._multislot_readout_warm_start(_q20_model(k="4"), str(badw))


def test_warm_start_k_arm_contents(tmp_path):
    W, scale = _toy_fuzz_dir(tmp_path)
    model = _q20_model(k="4")
    note = s1._multislot_readout_warm_start(model, str(tmp_path))
    assert "k=4" in note
    q_ridge = torch.from_numpy(np.load(tmp_path / "q20_ridge_dir.npz")["q_ridge"])
    ms = model.multislot_readout
    assert torch.equal(ms.slot_query[0], q_ridge)  # 槽 0 = ridge 段 1 主方向
    # 其余槽与已有槽逐头正交 (含槽 0)
    with torch.no_grad():
        for j in range(1, ms.k):
            for jj in range(j):
                num = (ms.slot_query[j] * F.normalize(ms.slot_query[jj], dim=-1)).sum(-1).abs()
                assert float(num.max()) < 1e-5, (j, jj, num)
    # 投影: 槽 0 块 = 部署桥 (折叠 scale), 其余槽块置零, 偏置 = 截距行
    w = ms.proj.weight.view(D_MEM, ms.k, H * HV)
    assert torch.allclose(w[:, 0], (W[:-1] / scale).T, atol=1e-6)
    assert torch.equal(w[:, 1:], torch.zeros_like(w[:, 1:]))
    assert torch.allclose(ms.proj.bias, W[-1], atol=1e-6)


def test_warm_start_cg_arm_needs_no_ridge_dir(tmp_path):
    W, scale = _toy_fuzz_dir(tmp_path, with_ridge=False)  # CG 臂不读主方向件
    model = _q20_model(k="cg")
    note = s1._multislot_readout_warm_start(model, str(tmp_path))
    assert "cg" in note
    assert torch.allclose(model.multislot_readout.proj.weight, (W[:-1] / scale).T, atol=1e-6)
    assert torch.allclose(model.multislot_readout.proj.bias, W[-1], atol=1e-6)


def test_k1_slot_query_shape():
    model = _q20_model(k="1")
    assert isinstance(model.multislot_readout, MultiSlotReadout)
    assert model.multislot_readout.slot_query.shape == (1, H, HK)
    assert model.multislot_readout.proj.weight.shape == (D_MEM, H * HV)
    model8 = _q20_model(k="8")
    assert model8.multislot_readout.proj.weight.shape == (D_MEM, 8 * H * HV)


# --- 5. CG 迭代件: 闭式对照 + 梯度流通 + 形状 -------------------------------------


def test_cg_converges_to_closed_form():
    model = _q20_model(k="cg")
    cg = model.multislot_readout
    kk, gates = _toy_gates(n=6)
    mask = torch.ones(1, 6, dtype=torch.bool)
    out = cg(gates, mask)
    assert out.shape == (1, 6, D_MEM)
    # 闭式参照: 同基板状态轨迹 (substrate 与生产 _forward_torch 同律) +
    # 逐段解 (K_iᵀK_i+λI)c_i=k_i (float64) → v̂ → 同投影
    states = _kda_scan_post_states(gates, mask).double()
    kf = gates["k"].double()[0]  # (n, H, hk)
    vh_ref = torch.zeros(1, 6, H, HV, dtype=torch.float64)
    for i in range(6):
        for h in range(H):
            K = kf[: i + 1, h]
            A = K.T @ K + Q20_CG_LAM * torch.eye(HK, dtype=torch.float64)
            c = torch.linalg.solve(A, K[i])
            vh_ref[0, i, h] = c @ states[0, i, h]
    out_ref = cg.proj(vh_ref.reshape(1, 6, H * HV).float())
    rel = (out - out_ref).norm() / out_ref.norm().clamp_min(1e-12)
    assert float(rel.detach()) < 1e-3, f"CG T=8 相对残差 {float(rel.detach()):.2e}"


def test_cg_gradient_flows_through_iterations():
    model = _q20_model(k="cg")
    cg = model.multislot_readout
    kk, gates = _toy_gates(n=5, requires_grad=True)  # 写入键叶子带梯度
    out = cg(gates, torch.ones(1, 5, dtype=torch.bool))
    out.square().mean().backward()
    assert cg.proj.weight.grad is not None and cg.proj.weight.grad.abs().sum() > 0
    # 梯度穿 T=8 步 CG 迭代件落到写入键 (段 1 结构可微的直接证据)
    assert kk.grad is not None and torch.isfinite(kk.grad).all() and kk.grad.abs().sum() > 0


def test_k_arm_forward_shape_and_state_substrate():
    model = _q20_model(k="4")
    kk, gates = _toy_gates(n=6)
    mask = torch.ones(1, 6, dtype=torch.bool)
    out = model.multislot_readout(gates, mask)
    assert out.shape == (1, 6, D_MEM) and out.dtype == torch.float32
    # post-state 基板与探针参考递推 (trained_states) 逐点一致
    ref = trained_states(None, gates, 6)
    assert torch.allclose(_kda_scan_post_states(gates, mask), ref, atol=1e-6)


# --- 6. 探针五列 -------------------------------------------------------------------


def _toy_fuzz():
    g = torch.Generator().manual_seed(5)
    return {
        "W": torch.randn(H * HV + 1, D_MEM, generator=g) * 0.02,
        "scale": 1.0,
        "chol": torch.eye(D_MEM) * 0.1,
        "rho": 0.8,
        "lam": 1.0,
        "tag": "opt",
    }


def test_probe_column_rows_q20_deterministic_and_shared_chain():
    model = _q20_model(k="4")
    chunks, memory, index = _front_end(model, _ids())
    real = chunks.chunk_mask
    n_real = int(real[0].sum())
    m = memory[0, :n_real].float()
    fuzz = _toy_fuzz()
    cols = probe.column_rows(
        model, m, index, real, fuzz,
        torch.Generator().manual_seed(11), torch.Generator().manual_seed(13),
    )
    assert set(cols) == {"clean", "q20_k", "noise_s0.5", "noise_s1", "noise_s2", "mhat", "scrambled"}
    assert list(cols)[1] == "q20_k"  # 主判据列紧跟 clean
    assert cols["q20_k"].shape == (n_real, D_MEM)
    # 确定性: 重跑逐位一致 (列生产零随机流——噪声/置乱抽签不碰 q20_k)
    cols2 = probe.column_rows(
        model, m, index, real, fuzz,
        torch.Generator().manual_seed(11), torch.Generator().manual_seed(13),
    )
    assert torch.equal(cols["q20_k"], cols2["q20_k"])
    # 同链性: == 训练器 _multislot_readout_rows 直算 (串联测零域移)
    ref = s1._multislot_readout_rows(model, index, real)[0, :n_real]
    assert torch.equal(cols["q20_k"], ref)


def test_probe_column_rows_legacy_regression():
    """旗标关 (模型无读出件) = 四列旧行为逐位不变。"""
    model = _model()
    chunks, memory, index = _front_end(model, _ids())
    real = chunks.chunk_mask
    n_real = int(real[0].sum())
    m = memory[0, :n_real].float()
    cols = probe.column_rows(
        model, m, index, real, _toy_fuzz(),
        torch.Generator().manual_seed(11), torch.Generator().manual_seed(13),
    )
    assert set(cols) == {"clean", "noise_s0.5", "noise_s1", "noise_s2", "mhat", "scrambled"}


def test_probe_eval_window_q20_e68_donor_column():
    model, donor = _q20_model(k="4"), _model()
    ids = _ids()
    ns = SimpleNamespace(max_chunks=32, max_span=16)
    zeros = torch.zeros_like(ids, dtype=torch.bool)
    rec = probe.eval_window_columns(
        model, ns, ids, zeros, DEVICE, _toy_fuzz(),
        torch.Generator().manual_seed(11), torch.Generator().manual_seed(13),
        donor=donor,
    )
    assert "q20_k" in rec and "q20_e68" in rec
    assert rec["q20_k"]["n_slots"] == rec["q20_e68"]["n_slots"]
    # 不带 donor = q20_k 在、归因列缺席; legacy 模型 = 两列都缺席
    rec2 = probe.eval_window_columns(
        model, ns, ids, zeros, DEVICE, _toy_fuzz(),
        torch.Generator().manual_seed(11), torch.Generator().manual_seed(13),
    )
    assert "q20_k" in rec2 and "q20_e68" not in rec2
    rec3 = probe.eval_window_columns(
        donor, ns, ids, zeros, DEVICE, _toy_fuzz(),
        torch.Generator().manual_seed(11), torch.Generator().manual_seed(13),
    )
    assert "q20_k" not in rec3 and "q20_e68" not in rec3


def test_probe_self_check_anchor_switch():
    # 旧行为 (默认锚 = E68 水位 0.7917)
    assert probe.self_check_failures(0.7917, 0.05) == []
    assert probe.self_check_failures(0.8323, 0.05)  # E118 水位在旧锚下误报
    # Q20 形态: clean ∈ 0.8323±2pp (E118 锚) 且 scrambled ≤0.10
    assert probe.self_check_failures(0.8323, 0.05, clean_ref=probe.CLEAN_REF_Q20) == []
    assert probe.self_check_failures(0.8123, 0.10, clean_ref=probe.CLEAN_REF_Q20) == []  # 边界贴线过
    assert probe.self_check_failures(0.7917, 0.05, clean_ref=probe.CLEAN_REF_Q20)  # 旧水位在新锚下 = 回落 4pp loud
    assert probe.self_check_failures(0.8323, 0.11, clean_ref=probe.CLEAN_REF_Q20)  # 漏地板


# --- 7. 主方向生成器代数 -----------------------------------------------------------


def test_ridge_direction_keyspace_equals_gram_form():
    _kk, gates = _toy_gates(n=6)
    n_real, lam = 6, 0.01
    dirs = q20gen.ridge_readout_directions(gates, n_real, lam)  # (H, n, hk) 键空间形
    k = gates["k"].float()[0]  # (n, H, hk)
    for h in range(H):
        K = k[:, h]
        for i in (0, 3, 5):
            Ki = K[: i + 1]
            A = Ki @ Ki.T + lam * torch.eye(i + 1)
            c_gram = Ki.T @ torch.linalg.solve(A, F.one_hot(torch.tensor(i), i + 1).float())
            assert torch.allclose(dirs[h, i], c_gram, atol=1e-5), (h, i)


def test_principal_direction_recovers_cloud_axis():
    g = torch.Generator().manual_seed(7)
    axis = F.normalize(torch.randn(HK, generator=g), dim=0)
    amps = torch.rand(40, generator=g) + 0.5
    cloud = amps.unsqueeze(-1) * axis  # 全在云轴上 (异号参半)
    cloud[::2] = -cloud[::2]
    dirs = [cloud.unsqueeze(0).expand(H, -1, -1).contiguous().permute(0, 1, 2)]  # (H, n, hk)
    q, st = q20gen.principal_direction(dirs)
    cos = F.cosine_similarity(q[0], axis, dim=0).abs()
    assert float(cos) > 0.999
    assert st["mean_norm"] > 0
