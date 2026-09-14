"""R3 丙臂（S0'' 段界器 × c1 变长铺瓦）施工件单测。

任务书：docs/versions/v3.7/FLUED_V3_7_R3_DELTANET_TRANSPLANT_DRAFT_20260914_CN.md
（冻结 v1.0 §2.3/§3）。三件必备测试（施工规格）：
① flag-off 逐位/逐键不变（默认关 = 与 R2 母列逐位不变；丙零新增参数）；
② 白名单 loud-fail（丙白名单=空集：checkpoint 键集必须与基座全等，坑 8）；
③ 铺瓦恒等数学语义（同一输入原生 BT=64 vs 变长铺瓦输出容差内一致 + 状态
接力链契约 + byte→token 映射规约确定性）。

mock 替身复刻 fla 0.5.2 ``chunk_delta_rule`` 的签名/返回合同（(q,k,v,β) 全
kwarg、(o, final_state) 二元返回、initial_state/output_final_state 接力），
零依赖可测；fla 门控用例在装 fla 的环境上运行（本臂施工靶机 = 本地 5080，
fla 0.5.2 × CUDA 全量在此执行）。
"""

from __future__ import annotations

import json

import pytest
import torch

import tools.baselines.deltanet_r2.r2_spec as r2spec
import tools.baselines.deltanet_r2.r3_spec as r3

try:
    import fla  # noqa: F401
    _HAS_FLA = True
except ImportError:
    _HAS_FLA = False

_HAS_FLA_CUDA = _HAS_FLA and torch.cuda.is_available()


@pytest.fixture(autouse=True)
def _vtile_state_reset():
    """用例间状态卫生：patch/计划不留场（attach 用例泄漏会污染后续用例）。"""
    yield
    r3.clear_vtile_plan()
    if r3._VTILE["patched"]:
        r3.detach_vtile()


# ---------------------------------------------------------------------------
# ③a byte→char 增量解码边界（纯函数）
# ---------------------------------------------------------------------------


def test_byte_char_boundaries_ascii():
    raw = b"abc"
    b = r3.byte_char_boundaries(raw)
    assert b == [0, 1, 2, 3]  # ASCII：1 byte = 1 char


def test_byte_char_boundaries_multibyte_cjk():
    raw = "中a文".encode("utf-8")  # 3B + 1B + 3B = 7B
    b = r3.byte_char_boundaries(raw)
    assert b == [0, 0, 0, 1, 2, 2, 2, 3]  # 增量解码：lead 字节不产出，闭合才计
    assert b[3] == 1 and b[4] == 2 and b[7] == 3


def test_byte_char_boundaries_invalid_replacement():
    # 违例窗：逐前缀慢路径——每个位置与 len(decode(raw[:b])) 精确相等（规约本体）
    raw = b"a\xe4\xb8bX\xffend"
    b = r3.byte_char_boundaries(raw)
    assert b == [len(raw[:i].decode("utf-8", errors="replace"))
                 for i in range(len(raw) + 1)]
    # 切点合格位（非续字节起点）的映射字符位抽查：'X' 前切点 =
    # decode(b"a\xe4\xb8b") = a+U+FFFD+b = 3 chars（截断子串已被 'b' 证闭）
    x_pos = raw.index(b"X")
    assert b[x_pos] == 3


def test_byte_char_boundaries_prefix_semantics_clean_path():
    # 净 utf-8 窗：切点合格位（非续字节处）与前缀解码语义逐位一致
    raw = ("_hello " * 8 + "你好世界" * 4).encode("utf-8")
    b = r3.byte_char_boundaries(raw)
    for i in range(len(raw) + 1):
        if i == len(raw) or not (128 <= raw[i] <= 191):  # 切点合格位
            assert b[i] == len(raw[:i].decode("utf-8", errors="replace")), i


def test_byte_char_boundaries_truncated_tail():
    raw = "中".encode("utf-8")[:2]  # 截断的多字节序列
    b = r3.byte_char_boundaries(raw)
    assert b[-1] == 1  # flush 后补替换字符（不消耗字节）


# ---------------------------------------------------------------------------
# ③b byte 切点 → token 计划映射规约（纯函数）
# ---------------------------------------------------------------------------


def _offsets_from_lens(lens):
    out, s = [], 0
    for l in lens:
        out.append((s, s + l))
        s += l
    return out


def test_token_plan_identity_mapping():
    # 每 token 覆盖 1 char：byte 切点=token 边界（恒等映射；byte 0=窗起点标记跳过）
    offsets = _offsets_from_lens([1] * 10)
    char_before = list(range(11))
    plan, st = r3.token_plan_from_byte_cuts([0, 3, 7], char_before, offsets, 10)
    assert plan == [3, 4, 3]  # 边界 3、7（byte 0 为窗起点标记，跳过）
    assert st["n_cuts_byte"] == 3 and st["n_segments"] == 3


def test_token_plan_round_right_snap():
    # token1 覆盖 char [0,4)：切在 char 2/3 处均 snap 到 token 边界 2
    # （round-right：跨切点的 token1 归左段，右段永不含切点前字节）
    offsets = [(0, 0), (0, 4), (4, 8), (8, 10)]
    char_before = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    plan, st = r3.token_plan_from_byte_cuts([2], char_before, offsets, 4)
    assert plan == [2, 2]  # 边界 = 2（token2 起 = start ≥ c=2）
    plan2, _ = r3.token_plan_from_byte_cuts([3], char_before, offsets, 4)
    assert plan2 == [2, 2]  # 同一 token 内切点 → 同一边界（dedupe 语义）


def test_token_plan_dedupe_and_windowstart_drop():
    offsets = _offsets_from_lens([1] * 8)
    char_before = list(range(9))
    # byte 0（窗起点标记）跳过；byte 1 两处 → 同一边界 1 去重
    plan, st = r3.token_plan_from_byte_cuts([0, 1, 1], char_before, offsets, 8)
    assert plan == [1, 7]
    assert st["n_segments"] == 2 and st["n_cuts_byte"] == 3


def test_token_plan_truncation_drops_tail_bounds():
    offsets = _offsets_from_lens([1] * 10)
    char_before = list(range(11))
    plan, _ = r3.token_plan_from_byte_cuts([3, 9], char_before, offsets, 5)
    assert plan == [3, 2]  # 边界 9 ≥ t_total 丢弃


def test_token_plan_loudfail_bad_cut():
    offsets = _offsets_from_lens([1] * 4)
    with pytest.raises(RuntimeError, match="出界"):
        r3.token_plan_from_byte_cuts([9], list(range(5)), offsets, 4)


# ---------------------------------------------------------------------------
# ③c vtile_apply 核契约（fake orig 替身）
# ---------------------------------------------------------------------------


class _FakeOrig:
    """chunk_delta_rule 合同替身：o = 切片 q 原样返回；final_state = 该段 T 的
    fp32 标量张量；记录 initial_state 接力链。"""

    def __init__(self):
        self.calls: list[dict] = []

    def __call__(self, q, k, v, beta, **kw):
        self.calls.append({"t": q.shape[1],
                           "h_in": None if kw.get("initial_state") is None
                           else float(kw["initial_state"]),
                           "ofs": kw.get("output_final_state")})
        h = torch.tensor(float(q.shape[1]), dtype=torch.float32)
        return q, h


def _qkvb(t_total=6):
    shape = (1, t_total, 2, 4)
    q = torch.randn(shape, dtype=torch.bfloat16)
    return q, q.clone(), q.clone(), torch.rand(1, t_total, 2, dtype=torch.bfloat16)


def test_vtile_apply_passthrough_none_plan():
    fake = _FakeOrig()
    q, k, v, beta = _qkvb()
    o, ht = r3.vtile_apply(fake, None, q, k, v, beta, output_final_state=True)
    assert len(fake.calls) == 1
    assert torch.equal(o, q) and float(ht) == 6.0  # 原样直通（逐位）


def test_vtile_apply_carry_chain_and_slices():
    fake = _FakeOrig()
    q, k, v, beta = _qkvb(6)
    o, ht = r3.vtile_apply(fake, [2, 3, 1], q, k, v, beta,
                           output_final_state=True)
    assert [c["t"] for c in fake.calls] == [2, 3, 1]  # 段长即切片
    assert fake.calls[0]["h_in"] is None  # 首段无初态
    assert fake.calls[1]["h_in"] == 2.0   # 接力自段 1 末态
    assert fake.calls[2]["h_in"] == 3.0   # 接力自段 2 末态
    assert float(ht) == 1.0               # 函数级末态 = 末段末态
    assert o.shape == q.shape and torch.equal(o, q)


def test_vtile_apply_handoff_casts_to_q_dtype():
    fake = _FakeOrig()  # hi 恒 fp32 → handoff 必须 cast 回 q.dtype（bf16）
    seen = []

    def spy(q, k, v, beta, **kw):
        seen.append(kw["initial_state"].dtype if kw.get("initial_state") is not None
                    else None)
        return q, torch.tensor(1.0, dtype=torch.float32)

    q, k, v, beta = _qkvb(4)
    r3.vtile_apply(spy, [2, 2], q, k, v, beta)
    assert seen == [None, torch.bfloat16]  # 接力态与 q 同 dtype


def test_vtile_apply_loudfail_sum_mismatch():
    fake = _FakeOrig()
    q, k, v, beta = _qkvb(6)
    with pytest.raises(RuntimeError, match="计划与输入不齐"):
        r3.vtile_apply(fake, [2, 3], q, k, v, beta)
    with pytest.raises(RuntimeError, match="非法计划|计划与输入不齐"):
        r3.vtile_apply(fake, [], q, k, v, beta)


def test_vtile_apply_loudfail_cuseqlens():
    fake = _FakeOrig()
    q, k, v, beta = _qkvb(6)
    with pytest.raises(RuntimeError, match="cu_seqlens"):
        r3.vtile_apply(fake, [6], q, k, v, beta, cu_seqlens=torch.tensor([0, 6]))


def test_vtile_apply_output_final_state_false_returns_none():
    fake = _FakeOrig()
    q, k, v, beta = _qkvb(6)
    o, ht = r3.vtile_apply(fake, [6], q, k, v, beta)  # 默认 output_final_state 缺省
    assert ht is None  # 层内 use_cache=False 路径契约：不外泄末态


# ---------------------------------------------------------------------------
# 计划上下文（模块级单例）
# ---------------------------------------------------------------------------


def test_set_plan_requires_attach():
    assert r3._VTILE["patched"] is False
    with pytest.raises(RuntimeError, match="未挂接"):
        r3.set_vtile_plan([4, 4])


def test_set_plan_validation():
    r3._VTILE["patched"] = True  # 白盒：仅测校验逻辑，finally 复原
    try:
        with pytest.raises(RuntimeError, match="非法计划"):
            r3.set_vtile_plan([4, 0])
        with pytest.raises(RuntimeError, match="非法计划"):
            r3.set_vtile_plan([4.0])
        r3.set_vtile_plan([4, 4])
        assert r3._VTILE["plan"] == [4, 4]
        r3.set_vtile_plan(None)
        assert r3._VTILE["plan"] is None
    finally:
        r3._VTILE["patched"] = False
        r3._VTILE["plan"] = None


# ---------------------------------------------------------------------------
# ① flag-off 逐位/逐键不变 + ② 白名单（空集）loud-fail（fla 门控）
# ---------------------------------------------------------------------------


def _build_model():
    from fla.models.delta_net import DeltaNetConfig, DeltaNetForCausalLM
    return DeltaNetForCausalLM(DeltaNetConfig(**r2spec.R2_CONFIG))


def _same_seed_build(vtile: bool):
    torch.manual_seed(r2spec.TRAIN_SEED)
    m = _build_model()
    report = r3.attach_vtile(m, vtile)
    if vtile:
        r3.stamp_vtile_config(m.config)
    return m, report


@pytest.mark.skipif(not _HAS_FLA, reason="fla 未安装（跳过）")
def test_param_anchor_vtile_zero_new_params():
    assert r2spec.EXPECTED_PARAM_COUNT == 48_152_896
    m0 = _build_model()
    n0 = sum(p.numel() for p in m0.parameters())
    m1, rep = _same_seed_build(vtile=True)
    n1 = sum(p.numel() for p in m1.parameters())
    assert rep["patched"] is True and rep["n_params_added"] == 0
    assert n1 == n0 == 48_152_896  # 丙零新增参数（与甲/乙的本质差异）
    assert list(m1.state_dict()) == list(m0.state_dict())  # 键集逐键不变


@pytest.mark.skipif(not _HAS_FLA_CUDA, reason="fla triton 核需 CUDA（本地 5080 跑）")
def test_flag_off_forward_bitwise_vs_pure_fla():
    torch.manual_seed(r2spec.TRAIN_SEED)
    a = _build_model().cuda()
    torch.manual_seed(r2spec.TRAIN_SEED)
    b = _build_model().cuda()
    rep = r3.attach_vtile(b, False)  # 旗标关：no-op 分支
    assert rep == {"patched": False, "n_params_added": 0}
    x = torch.randint(3, 32000, (1, 96), device="cuda")
    with torch.no_grad(), torch.autocast("cuda", dtype=torch.bfloat16):
        assert torch.equal(a(input_ids=x).logits, b(input_ids=x).logits)  # 逐位不变


@pytest.mark.skipif(not _HAS_FLA_CUDA, reason="fla triton 核需 CUDA（本地 5080 跑）")
def test_passthrough_plan_none_bitwise_after_attach():
    torch.manual_seed(r2spec.TRAIN_SEED)
    a = _build_model().cuda()
    torch.manual_seed(r2spec.TRAIN_SEED)
    b = _build_model().cuda()
    r3.attach_vtile(b, True)
    x = torch.randint(3, 32000, (1, 96), device="cuda")
    with torch.no_grad(), torch.autocast("cuda", dtype=torch.bfloat16):
        la = a(input_ids=x).logits  # 未挂接
        lb = b(input_ids=x).logits  # 挂接 + 无计划 → 直通
    assert torch.equal(la, lb)  # 直通洁净性（对拍门逐位档同款）


@pytest.mark.skipif(not _HAS_FLA_CUDA, reason="fla triton 核需 CUDA（本地 5080 跑）")
def test_vtile_forward_tolerant_vs_native_and_grads_flow():
    """③ 铺瓦恒等（模型级）：同一输入，变长计划 vs 原生，logits 容差内一致
    （bf16 结合序量级）；梯度链贯通（finite）。"""
    torch.manual_seed(r2spec.TRAIN_SEED)
    m, _ = _same_seed_build(vtile=True)
    m = m.cuda().train()
    x = torch.randint(3, 32000, (1, 96), device="cuda")
    with torch.no_grad(), torch.autocast("cuda", dtype=torch.bfloat16):
        native = m(input_ids=x).logits
    plan = [11, 7, 13, 5, 9, 3, 16, 8, 2, 22]  # sum=96
    assert sum(plan) == 96
    r3.set_vtile_plan(plan)
    try:
        with torch.autocast("cuda", dtype=torch.bfloat16):
            out = m(input_ids=x).logits
        # 容差实测定标（2026-09-14，本机 5080）：T=96/10 段 max|Δ|=0.117/
        # mean 0.012；in-family 对照 = fla 自身 BT64→BT32 粒度差（T=640/
        # 53 段均）max 0.203 / mean 0.0225，vtile 同量级（1.26×）——偏差=
        # 纯 fp 结合序，非实现误差。取实测 2× 余量。
        d = (out.float() - native.float()).abs()
        assert d.mean().item() <= 0.03
        assert d.max().item() <= 0.25
        assert not torch.equal(out, native)  # 铺瓦确实生效（非直通）
    finally:
        r3.clear_vtile_plan()
    r3.set_vtile_plan(plan)
    try:
        with torch.autocast("cuda", dtype=torch.bfloat16):
            loss = m(input_ids=x).logits.float().square().mean()
        loss.backward()
    finally:
        r3.clear_vtile_plan()
    grads = [p.grad for p in m.parameters() if p.grad is not None]
    assert grads and all(torch.isfinite(g).all() for g in grads)


@pytest.mark.skipif(not _HAS_FLA_CUDA, reason="fla triton 核需 CUDA（本地 5080 跑）")
def test_uniform64_plan_close_to_native():
    """均匀 64 段计划 vs 原生 = handoff cast 单一机制（对拍门校准档的同款量）：
    容差须显著紧于任意变长计划（无边界重排，仅接力 cast）。"""
    torch.manual_seed(r2spec.TRAIN_SEED)
    m, _ = _same_seed_build(vtile=True)
    m = m.cuda()
    x = torch.randint(3, 32000, (1, 128), device="cuda")
    with torch.no_grad(), torch.autocast("cuda", dtype=torch.bfloat16):
        native = m(input_ids=x).logits
        r3.set_vtile_plan([64, 64])
        try:
            uni = m(input_ids=x).logits
        finally:
            r3.clear_vtile_plan()
    assert torch.allclose(uni.float(), native.float(), atol=0.02, rtol=0.02)


@pytest.mark.skipif(not _HAS_FLA, reason="fla 未安装（跳过）")
def test_double_attach_loudfail():
    m, _ = _same_seed_build(vtile=True)
    with pytest.raises(RuntimeError, match="重复挂接"):
        r3.attach_vtile(m, True)
    r3.clear_vtile_plan()
    r3.detach_vtile()
    assert r3._VTILE["patched"] is False


@pytest.mark.skipif(not _HAS_FLA, reason="fla 未安装（跳过）")
def test_flag_off_after_attach_with_patch_loudfail():
    m, _ = _same_seed_build(vtile=True)
    with pytest.raises(RuntimeError, match="patch 仍在"):
        r3.attach_vtile(m, False)
    r3.clear_vtile_plan()
    r3.detach_vtile()


def test_attach_no_fla_loudfail():
    if _HAS_FLA:
        pytest.skip("fla 在场（本用例只测缺 fla 路径）")
    torch.manual_seed(0)

    class _Cfg:
        attn_mode = "chunk"

    class _M:
        config = _Cfg()

    with pytest.raises(ImportError):
        r3.attach_vtile(_M(), True)


def test_config_stamp_roundtrip():
    class _Cfg:
        pass

    cfg = _Cfg()
    assert not r3.config_has_vtile(cfg)
    r3.stamp_vtile_config(cfg)
    assert r3.config_has_vtile(cfg)
    assert cfg.r3_vtile["enabled"] is True
    assert cfg.r3_vtile["n_params_added"] == 0
    assert json.loads(json.dumps(cfg.r3_vtile))["chunk_size"] == 64  # json 可落盘
    del cfg.r3_vtile
    assert not r3.config_has_vtile(cfg)


@pytest.mark.skipif(not _HAS_FLA, reason="fla 未安装（跳过）")
def test_verify_vtile_reload_keys_equal_and_bitexact(tmp_path):
    """坑 8 全链（丙特化）：零新增参数 → 键集=基座全等；save → from_pretrained
    → verify_vtile_reload 逐位复原。"""
    from transformers import AutoModelForCausalLM
    r2spec.normalize_tied_weights_keys()
    m, _ = _same_seed_build(vtile=True)
    with torch.no_grad():
        m.state_dict()["model.embeddings.weight"].fill_(0.01)
    d = tmp_path / "vtile_ckpt"
    m.save_pretrained(d)
    cfg = json.loads((d / "config.json").read_text(encoding="utf-8"))
    assert cfg["r3_vtile"]["enabled"] is True

    loaded = AutoModelForCausalLM.from_pretrained(d)
    assert r3.config_has_vtile(loaded.config)
    rep = r3.verify_vtile_reload(loaded, d)
    assert rep["n_params_added"] == 0
    assert rep["expected_param_count"] == 48_152_896
    src_sd, got_sd = m.state_dict(), loaded.state_dict()
    assert set(src_sd) == set(got_sd)
    for k in src_sd:
        assert torch.equal(src_sd[k], got_sd[k]), k  # 逐位复原


@pytest.mark.skipif(not _HAS_FLA, reason="fla 未安装（跳过）")
def test_verify_vtile_reload_loudfail_extra_key(tmp_path):
    """丙白名单=空集：文件多出任何键 = loud fail（坑 8：静默过滤=不点火）。"""
    from safetensors.torch import save_file
    m, _ = _same_seed_build(vtile=True)
    sd = dict(m.state_dict())
    sd["model.layers.0.attn.junk_gate"] = torch.zeros(2)
    d = tmp_path / "ckpt"
    d.mkdir()
    save_file({k: v.contiguous() for k, v in sd.items()},
              str(d / "model.safetensors"))
    with pytest.raises(RuntimeError, match="不全等"):
        r3.verify_vtile_reload(m, d)
