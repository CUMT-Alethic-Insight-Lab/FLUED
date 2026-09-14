"""R3 乙臂（summarizer 双头构造移植）施工件单测。

任务书：docs/versions/v3.7/FLUED_V3_7_R3_DELTANET_TRANSPLANT_DRAFT_20260914_CN.md
（冻结 v1.0 §2.2/§3）。施工规格必备测试：
① flag-off 逐位/逐键不变（默认关 = 与 R2 母列逐位不变）；
② summarizer 键白名单 loud-fail（坑 8：strict 加载、白名单外静默过滤=不点火）；
③ 双头数学语义（summarizer 输出常数化时逐位退化为可控形态 + 块内广播纯函数）。

mock 替身复刻 fla 0.5.1 ``fla/layers/delta_net.py`` 调用序（q/k/v 各 proj→conv1d
元组输出、β=b_proj(hidden_states) 原生、核替身逐位置乘积、o_norm→o_proj）；
summarizer 本体 = 原件 ``flued.v36.model.DiTChunkSummarizer`` 实类（320 维参数
化），零替身。fla 门控用例在装 fla 的环境上运行（远端 4090 施工靶机跑全量；
autocast bf16 / CUDA 门控 / ShortConvolution 元组解包三坑照甲例趟平形态）。
"""

from __future__ import annotations

import json

import pytest
import torch
from torch import nn

import tools.baselines.deltanet_r2.r2_spec as r2spec
import tools.baselines.deltanet_r2.r3_spec as r3

try:
    import fla  # noqa: F401
    _HAS_FLA = True
except ImportError:
    _HAS_FLA = False  # 本地单测环境无 fla：零依赖用例照跑，门控用例跳过（远端跑全量）


# ---------------------------------------------------------------------------
# mock 替身：fla DeltaNet 层调用序（conv1d 元组输出 → 核 → o_norm → o_proj）
# ---------------------------------------------------------------------------


class _Conv(nn.Module):
    """ShortConvolution 替身：恒返回 (x·s, None) 元组（fla 0.5.1 元组契约），
    可辨识变换 ×s 证明下游消费的是**替换后**的 conv 输出（hook 改写元组首元，
    层内解包拿到替换值）。"""

    def __init__(self, scale: float = 1.0):
        super().__init__()
        self.scale = scale

    def forward(self, x, **kw):
        return x * self.scale, None


class _Scale(nn.Module):
    """RMSNorm 替身（o_norm 位）：定点 ×s，闭式可手算。"""

    def __init__(self, s: float):
        super().__init__()
        self.s = s

    def forward(self, o):
        return o * self.s


class _Attn(nn.Module):
    """fla DeltaNet 层调用序替身：核 o = k ⊙ v（逐位置，k/v 广播后闭式可算）；
    q/β 走原生投影（β 与 v 无关，delta_net.py:251 同构）。"""

    def __init__(self, dim: int = r3.SUMM_D):
        super().__init__()
        self.q_proj = nn.Linear(dim, dim, bias=False)
        self.k_proj = nn.Linear(dim, dim, bias=False)
        self.v_proj = nn.Linear(dim, dim, bias=False)
        self.b_proj = nn.Linear(dim, dim, bias=False)
        self.q_conv1d = _Conv(3.0)
        self.k_conv1d = _Conv(5.0)
        self.v_conv1d = _Conv(7.0)
        self.o_norm = _Scale(2.0)
        self.o_proj = nn.Linear(dim, dim, bias=False)

    def forward(self, x):
        _q = self.q_conv1d(self.q_proj(x))[0]  # 原生（读侧不动）
        k = self.k_conv1d(self.k_proj(x))[0]  # 地址侧替换点（conv 输出）
        v = self.v_conv1d(self.v_proj(x))[0]  # 值侧替换点（conv 输出）
        o = k * v  # delta rule 核替身 :261-270
        o = self.o_norm(o)  # :286 对应
        return x + self.o_proj(o)


class _Block(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.attn = _Attn(dim)


class _MockModel(nn.Module):
    """embeddings（内层 model 属性，供 embed hook 挂接）→ 层栈 → head。"""

    def __init__(self, n_layers: int = 2, dim: int = r3.SUMM_D, vocab: int = 11):
        super().__init__()
        self.model = nn.Module()
        self.model.embeddings = nn.Embedding(vocab, dim)
        self.model.layers = nn.ModuleList([_Block(dim) for _ in range(n_layers)])
        self.head = nn.Linear(dim, 7)

    def forward(self, input_ids):
        h = self.model.embeddings(input_ids)
        for lyr in self.model.layers:
            h = lyr.attn(h)
        return self.head(h)


def _summ_params(model) -> dict[str, nn.Parameter]:
    return {k: p for k, p in model.named_parameters()
            if f".{r3.SUMM_ATTR}." in f".{k}"}


def _constantize_summ(model, c_m: float, c_k: float):
    """summarizer 输出常数化（测试③）：全件参数归零后置双头末层 bias →
    blocks 输出过 LN(零仿射)=0 → ffn(0)=bias ⇒ m_c ≡ c_m、k_c ≡ c_k（对任意
    输入；pool 对常数化的不敏感性由 LN 零仿射保证）。"""
    for p in _summ_params(model).values():
        p.detach().zero_()
    base = model.model
    base.r3_summ.ffn[3].bias.detach().fill_(c_m)
    base.r3_summ.index_ffn[3].bias.detach().fill_(c_k)


# ---------------------------------------------------------------------------
# 0. 参数锚与构造常量（纯算术 + 原件实例化互证）
# ---------------------------------------------------------------------------


def test_param_anchor_summ_constants():
    assert r2spec.EXPECTED_PARAM_COUNT == 48_152_896
    assert r3.SUMM_CHUNK_TOKENS == r2spec.NATIVE_CHUNK_TOKENS == 64
    assert (r3.SUMM_DIT_LAYERS, r3.SUMM_D, r3.SUMM_HEADS) == (2, 320, 5)
    assert (r3.SUMM_FFN_DIM, r3.SUMM_HIDDEN, r3.SUMM_D_MEM) == (768, 768, 320)
    assert r3.SUMM_NUM_PARAMS == 4_972_932  # 施工精算锚（≈+10.3%，回执 §0.4）
    assert r3.EXPECTED_PARAM_COUNT_SUMM == 48_152_896 + 4_972_932 == 53_125_828
    assert r3.expected_param_count_any(False, False) == 48_152_896
    assert r3.expected_param_count_any(True, False) == 48_152_920
    assert r3.expected_param_count_any(False, True) == 53_125_828


def test_summ_instantiation_matches_analytic_anchor():
    summ = r3.build_summarizer()
    n = sum(p.numel() for p in summ.parameters())
    assert n == r3.SUMM_NUM_PARAMS
    from flued.v36.model import DiTChunkSummarizer
    assert isinstance(summ, DiTChunkSummarizer)
    assert (summ.QPOOL_QUERIES, summ.QPOOL_ANCHOR_TEMP) == (4, 16.0)
    assert summ.pool_mode == "qpool"
    assert hasattr(summ, "index_ffn") and hasattr(summ, "ffn")  # 双头齐备


def test_broadcast_per_chunk_semantics():
    pc = torch.arange(2 * 3 * 4, dtype=torch.float32).reshape(2, 3, 4)
    ref = torch.zeros(2, 130, 4)  # T=130 → 3 块（64/64/2，尾块残块常态）
    out = r3.broadcast_per_chunk(pc, ref)
    for t in (0, 63, 64, 127, 128, 129):
        assert torch.equal(out[:, t], pc[:, t // 64])
    assert out.shape == ref.shape


def test_broadcast_per_chunk_shape_mismatch_loudfail():
    with pytest.raises(RuntimeError, match="形状不符"):
        r3.broadcast_per_chunk(torch.zeros(1, 2, 3), torch.zeros(1, 5, 4))


# ---------------------------------------------------------------------------
# ① flag-off 逐位/逐键不变
# ---------------------------------------------------------------------------


def test_flag_off_no_params_no_hooks_bitwise():
    torch.manual_seed(0)
    plain = _MockModel()
    torch.manual_seed(0)
    flagged = _MockModel()
    keys_before = list(flagged.state_dict())
    got = r3.attach_summ(flagged, False)
    assert got == []
    assert list(flagged.state_dict()) == keys_before  # 键集逐键不变
    assert not _summ_params(flagged)
    assert not hasattr(flagged.model, r3.SUMM_ATTR)
    ids = torch.randint(0, 11, (1, 7))
    with torch.no_grad():
        assert torch.equal(plain(ids), flagged(ids))  # 逐位不变
    with torch.no_grad():  # 二次调用仍逐位一致（无 hook 残留、无状态泄漏）
        assert torch.equal(plain(ids), flagged(ids))


def test_flag_off_after_attach_loudfail():
    m = _MockModel()
    r3.attach_summ(m, True)
    with pytest.raises(RuntimeError, match="残留"):
        r3.attach_summ(m, False)


def test_double_attach_loudfail():
    m = _MockModel()
    r3.attach_summ(m, True)
    with pytest.raises(RuntimeError, match="重复挂接"):
        r3.attach_summ(m, True)


def test_trainer_flags_mutually_exclusive(monkeypatch):
    import tools.baselines.deltanet_r2.train_deltanet_r3 as tr
    monkeypatch.setattr("sys.argv", [
        "train_deltanet_r3.py", "--corpus", "x", "--tokenizer-path", "y",
        "--out-dir", "z", "--echo", "--summ"])
    with pytest.raises(SystemExit, match="互斥"):
        tr.parse_args()


# ---------------------------------------------------------------------------
# ② 键白名单 loud-fail（坑 8）
# ---------------------------------------------------------------------------


def _write_sd(tmp_path, sd, name="model.safetensors"):
    from safetensors.torch import save_file
    save_file({k: v.contiguous() for k, v in sd.items()}, str(tmp_path / name))
    return tmp_path


def test_whitelist_check_missing_key_loudfail():
    with pytest.raises(RuntimeError, match="坑 8"):
        r3.check_key_whitelist(file_keys={"a"}, model_keys={"a", "b"},
                               echo_keys=set())


def test_whitelist_check_extra_key_loudfail():
    with pytest.raises(RuntimeError, match="白名单外多出键"):
        r3.check_key_whitelist(file_keys={"a", "junk"}, model_keys={"a"},
                               echo_keys=set())


def test_strict_reload_restores_summ_bitexact(tmp_path):
    torch.manual_seed(0)
    src = _MockModel(n_layers=1)
    keys = r3.attach_summ(src, True)
    assert len(keys) == len(_summ_params(src))
    assert sum(p.numel() for p in _summ_params(src).values()) == r3.SUMM_NUM_PARAMS
    with torch.no_grad():  # 模拟训练后漂移
        for p in _summ_params(src).values():
            p.add_(0.01)
    d = _write_sd(tmp_path, src.state_dict())

    torch.manual_seed(0)
    fresh = _MockModel(n_layers=1)  # 未挂接（strict_load_summ 内建 attach）
    rep = r3.strict_load_summ(fresh, d)
    assert rep["n_summ_keys"] == len(keys)
    for (k_a, v_a), (k_b, v_b) in zip(src.state_dict().items(),
                                      fresh.state_dict().items()):
        assert k_a == k_b and torch.equal(v_a, v_b), k_a  # 逐位一致
    assert set(_summ_params(fresh)) == set(keys)


def test_strict_reload_loudfail_missing_summ_key_in_file(tmp_path):
    torch.manual_seed(0)
    model = _MockModel(n_layers=1)
    r3.attach_summ(model, True)
    sd = dict(model.state_dict())
    victim_key = sorted(_summ_params(model))[0]
    sd.pop(victim_key)
    d = _write_sd(tmp_path, sd)
    torch.manual_seed(0)
    victim = _MockModel(n_layers=1)
    with pytest.raises(RuntimeError, match="不点火"):
        r3.strict_load_summ(victim, d)


def test_strict_reload_loudfail_junk_key_in_file(tmp_path):
    torch.manual_seed(0)
    model = _MockModel(n_layers=1)
    sd = dict(model.state_dict())
    sd["model.r3_summ.evil_proj.weight"] = torch.zeros(4)
    d = _write_sd(tmp_path, sd)
    torch.manual_seed(0)
    victim = _MockModel(n_layers=1)
    with pytest.raises(RuntimeError, match="不点火"):
        r3.strict_load_summ(victim, d)


def test_strict_reload_loudfail_no_summ_keys(tmp_path):
    torch.manual_seed(0)
    model = _MockModel(n_layers=1)  # 未挂接
    _write_sd(tmp_path, model.state_dict())
    with pytest.raises(RuntimeError, match="无 summarizer 键"):
        r3.strict_load_summ(model, tmp_path, attach=False)


def test_config_stamp_roundtrip():
    class _Cfg:
        pass

    cfg = _Cfg()
    assert not r3.config_has_summ(cfg)
    r3.stamp_summ_config(cfg)
    assert r3.config_has_summ(cfg)
    assert cfg.r3_summ["enabled"] is True
    assert cfg.r3_summ["num_params"] == r3.SUMM_NUM_PARAMS
    assert json.loads(json.dumps(cfg.r3_summ))["pool"] == "qpool"  # json 可落盘
    r3.unstamp_summ_config(cfg)
    assert not r3.config_has_summ(cfg)


# ---------------------------------------------------------------------------
# ③ 双头数学语义：常数化 → 逐位退化可控形态
# ---------------------------------------------------------------------------


def test_constantized_summ_closed_form_bitexact():
    """常数化 sum件：m_c≡c_m、k_c≡c_k ⇒ 每层 h ← h + 2·(c_k⊙c_m)（核替身
    o=k⊙v、o_norm ×2、o_proj=I），闭式逐位可算；同时探测 hook 消费的确实是
    替换后 conv 输出（conv 可辨识变换 ×5/×7 被替换丢弃）。"""
    torch.manual_seed(0)
    m = _MockModel(n_layers=2)
    with torch.no_grad():
        for lyr in m.model.layers:
            lyr.attn.o_proj.weight.copy_(torch.eye(r3.SUMM_D))
    r3.attach_summ(m, True)
    c_m, c_k = 0.25, -0.5
    _constantize_summ(m, c_m, c_k)

    captured = []
    for lyr in m.model.layers:  # 挂在替换 hook 之后（注册序=触发序）→ 见替换值
        lyr.attn.k_conv1d.register_forward_hook(
            lambda _mo, _i, out: captured.append(("k", out[0])) or out)
        lyr.attn.v_conv1d.register_forward_hook(
            lambda _mo, _i, out: captured.append(("v", out[0])) or out)

    ids = torch.randint(0, 11, (1, 130))  # 64+64+2：尾块残块常态
    with torch.no_grad():
        got = m(ids)
    # 闭式：h0=E(ids)；h_{l+1}=h_l + 2·(c_k·c_m)；logits=head(h2)
    h = m.model.embeddings(ids)
    delta = 2.0 * (c_k * c_m) * torch.ones_like(h)
    want = m.head(h + 2 * delta)
    assert torch.allclose(got, want, atol=1e-6)  # 逐位退化可控形态
    # 探测：每层 k/v 位置值 = 常数广播（t//64 同块恒等）
    ks = [x for tag, x in captured if tag == "k"]
    vs = [x for tag, x in captured if tag == "v"]
    assert len(ks) == len(vs) == 2
    for k, v in zip(ks, vs):
        assert k.shape == (1, 130, r3.SUMM_D) and v.shape == (1, 130, r3.SUMM_D)
        assert torch.equal(k[0, 0], k[0, 127]) and torch.equal(k[0, 0], k[0, 129])
        assert torch.allclose(k[0, 0], torch.full_like(k[0, 0], c_k), atol=1e-7)
        assert torch.allclose(v[0, 64], torch.full_like(v[0, 64], c_m), atol=1e-7)


def test_zero_summ_attn_contributes_zero_bitexact():
    """全零 summarizer：m_c=k_c=0 ⇒ 核替身 o=0 ⇒ 层恒等，模型=embeddings→head。"""
    torch.manual_seed(0)
    m = _MockModel(n_layers=2)
    r3.attach_summ(m, True)
    _constantize_summ(m, 0.0, 0.0)
    ids = torch.randint(0, 11, (1, 96))
    with torch.no_grad():
        assert torch.equal(m(ids), m.head(m.model.embeddings(ids)))  # 逐位


def test_gradient_flows_to_summ_params():
    torch.manual_seed(0)
    m = _MockModel(n_layers=1)
    r3.attach_summ(m, True)
    loss = m(torch.randint(0, 11, (1, 64))).square().sum()
    loss.backward()
    named = {k: p for k, p in m.named_parameters() if f".{r3.SUMM_ATTR}." in f".{k}"}
    assert all(p.grad is not None and torch.isfinite(p.grad).all()
               for p in named.values())
    assert any(p.grad.abs().sum() > 0 for p in named.values())  # 非零梯度
    assert named["model.r3_summ.pool_queries"].grad is not None  # qpool 在梯度链上


def test_embed_hook_order_violation_loudfail():
    """k/v hook 先于 embed hook 触发（不可能序）→ loud fail（hook 序契约）。"""
    torch.manual_seed(0)
    m = _MockModel(n_layers=1)
    r3.attach_summ(m, True)
    # 直接拨层（绕过 embeddings）模拟序违例
    with pytest.raises(RuntimeError, match="hook 序漂移"):
        m.model.layers[0].attn(torch.randn(1, 8, r3.SUMM_D))


# ---------------------------------------------------------------------------
# fla 门控用例（远端 4090 施工靶机执行全量；三坑照甲例：autocast bf16 /
# CUDA 门控 / ShortConvolution 元组解包）
# ---------------------------------------------------------------------------


def _build_model():
    from fla.models.delta_net import DeltaNetConfig, DeltaNetForCausalLM
    return DeltaNetForCausalLM(DeltaNetConfig(**r2spec.R2_CONFIG))


def _same_seed_build(summ: bool):
    torch.manual_seed(r2spec.TRAIN_SEED)
    m = _build_model()
    keys = r3.attach_summ(m, summ)
    if summ:  # 镜像训练器 build_model：元数据随 config 落盘
        r3.stamp_summ_config(m.config)
    return m, keys


_HAS_FLA_CUDA = _HAS_FLA and torch.cuda.is_available()


@pytest.mark.skipif(not _HAS_FLA, reason="fla 未安装（本地跳过，远端跑全量）")
def test_param_anchor_instantiation_summ_flag():
    m0, keys0 = _same_seed_build(summ=False)
    assert sum(p.numel() for p in m0.parameters()) == 48_152_896
    assert keys0 == []
    m1, keys1 = _same_seed_build(summ=True)
    assert sum(p.numel() for p in m1.parameters()) == r3.EXPECTED_PARAM_COUNT_SUMM
    assert len(keys1) == len(_summ_params(m1)) > 0
    assert all(k.startswith("model.r3_summ.") for k in keys1)


@pytest.mark.skipif(not _HAS_FLA, reason="fla 未安装（本地跳过，远端跑全量）")
def test_key_diff_two_instantiations_summ_on_identical():
    m1, _ = _same_seed_build(summ=True)
    m2, _ = _same_seed_build(summ=True)
    k1, k2 = list(m1.state_dict()), list(m2.state_dict())
    assert k1 == k2  # 键序列逐键一致
    assert all(m1.state_dict()[k].shape == m2.state_dict()[k].shape for k in k1)
    # summ-on 键集 == R2 母列键集 ∪ summarizer 白名单，无任何其他差异
    torch.manual_seed(r2spec.TRAIN_SEED)
    m0 = _build_model()
    assert set(k1) - set(m0.state_dict()) == set(_summ_params(m1))
    assert set(m0.state_dict()) - set(k1) == set()


@pytest.mark.skipif(not _HAS_FLA_CUDA,
                    reason="fla triton 核需 CUDA（本地跳过，远端 4090 跑全量）")
def test_flag_off_forward_bitwise_vs_pure_fla():
    torch.manual_seed(r2spec.TRAIN_SEED)
    a = _build_model().cuda()
    torch.manual_seed(r2spec.TRAIN_SEED)
    b = _build_model().cuda()
    r3.attach_summ(b, False)  # 旗标关：挂接函数走 no-op 分支
    assert torch.equal(a.state_dict()["model.embeddings.weight"],
                       b.state_dict()["model.embeddings.weight"])
    x = torch.randint(3, 32000, (1, 96), device="cuda")
    with torch.no_grad(), torch.autocast("cuda", dtype=torch.bfloat16):
        assert torch.equal(a(input_ids=x).logits, b(input_ids=x).logits)  # 逐位不变


@pytest.mark.skipif(not _HAS_FLA_CUDA,
                    reason="fla triton 核需 CUDA（本地跳过，远端 4090 跑全量）")
def test_summ_on_dual_head_semantics_on_fla():
    """真机双头语义：值侧 v_t=m_c 广播、地址侧 k_t=k_c 广播（fused_recurrent
    与 chunk 两核路径），块内位置逐位恒等，且块向量=独立复算 summarizer 输出。"""
    m, _ = _same_seed_build(summ=True)
    m = m.cuda().eval()
    summ = m.model.r3_summ
    captured = {}
    for li, lyr in enumerate(m.model.layers):  # 挂在替换 hook 之后 → 见替换值
        def _cap_k(_mo, _i, out, _li=li):
            captured.setdefault(("k", _li), out[0].detach())
            return out

        def _cap_v(_mo, _i, out, _li=li):
            captured.setdefault(("v", _li), out[0].detach())
            return out
        lyr.attn.k_conv1d.register_forward_hook(_cap_k)
        lyr.attn.v_conv1d.register_forward_hook(_cap_v)

    for t_len, core in ((48, "fused_recurrent(q_len<=64)"), (130, "chunk")):
        captured.clear()
        x = torch.randint(3, 32000, (1, t_len), device="cuda")
        with torch.no_grad(), torch.autocast("cuda", dtype=torch.bfloat16):
            m(input_ids=x, use_cache=False)  # 全窗前向（eval 态禁 fla 缓存路径）
        # 独立复算 summarizer（同输入同 autocast 同形状 → 同构造）
        with torch.no_grad(), torch.autocast("cuda", dtype=torch.bfloat16):
            h = m.model.embeddings(x)
            n_chunk = (t_len + 63) // 64
            pad = n_chunk * 64 - t_len
            hp = torch.nn.functional.pad(h, (0, 0, 0, pad)) if pad else h
            valid = torch.ones(1, n_chunk, 64, dtype=torch.bool, device="cuda")
            if pad:
                valid[:, -1, 64 - pad:] = False
            m_c, k_c = summ.forward_with_index(hp.view(1, n_chunk, 64, -1), valid)
        for li in range(24):
            k, v = captured[("k", li)], captured[("v", li)]
            assert k.shape == (1, t_len, 320) and v.shape == (1, t_len, 320)
            for c in range(n_chunk):  # 块内位置逐位恒等（广播=index_select 拷贝）
                lo, hi = c * 64, min((c + 1) * 64, t_len)
                assert torch.equal(k[0, lo:hi], k[0, lo:hi][0:1].expand(hi - lo, 320))
                assert torch.equal(v[0, lo:hi], v[0, lo:hi][0:1].expand(hi - lo, 320))
                assert torch.allclose(k[0, lo].float(), k_c[0, c].float(), atol=1e-2)
                assert torch.allclose(v[0, lo].float(), m_c[0, c].float(), atol=1e-2)


@pytest.mark.skipif(not _HAS_FLA_CUDA,
                    reason="fla triton 核需 CUDA（本地跳过，远端 4090 跑全量）")
def test_summ_on_differs_from_mother_and_grads_finite():
    a, _ = _same_seed_build(summ=False)
    a = a.cuda()
    b, _ = _same_seed_build(summ=True)
    b = b.cuda()
    b.train()
    x = torch.randint(3, 32000, (1, 96), device="cuda")
    with torch.autocast("cuda", dtype=torch.bfloat16):
        la = a(input_ids=x).logits.float().square().sum()
        lb = b(input_ids=x).logits
        assert not torch.equal(la.detach(), lb.detach())  # 移植件确实改变前向
        lb.float().square().sum().backward()
    grads = [p.grad for k, p in b.named_parameters()
             if f".{r3.SUMM_ATTR}." in f".{k}"]
    assert len(grads) > 0
    assert all(g is not None and torch.isfinite(g).all() for g in grads)
    assert any(g.abs().sum() > 0 for g in grads)  # summarizer 在梯度链上


@pytest.mark.skipif(not _HAS_FLA, reason="fla 未安装（本地跳过，远端跑全量）")
def test_save_roundtrip_strict_reload_summ_bitexact(tmp_path):
    """坑 8 全链：save 带 r3_summ 键 → from_pretrained 静默丢弃（事故形态复现）
    → attach+strict 白名单重载逐位复原 + config 字段往返。"""
    from transformers import AutoModelForCausalLM
    r2spec.normalize_tied_weights_keys()
    m, _ = _same_seed_build(summ=True)
    with torch.no_grad():  # 模拟训练后漂移
        for k, p in m.named_parameters():
            if f".{r3.SUMM_ATTR}." in f".{k}":
                p.add_(0.01)
    d = tmp_path / "summ_ckpt"
    m.save_pretrained(d)
    cfg = json.loads((d / "config.json").read_text(encoding="utf-8"))
    assert cfg["r3_summ"]["enabled"] is True  # 元数据随 config 落盘
    sd_file = r3.read_state_dict(d)
    n_summ_file = sum(1 for k in sd_file if k.startswith("model.r3_summ."))
    assert n_summ_file == len(_summ_params(m))

    loaded = AutoModelForCausalLM.from_pretrained(d)
    assert r3.config_has_summ(loaded.config)
    assert not any(f".{r3.SUMM_ATTR}." in f".{k}" for k in loaded.state_dict())

    rep = r3.attach_and_strict_reload_summ(loaded, d)
    assert rep["n_summ_keys"] == n_summ_file
    src_sd, got_sd = m.state_dict(), loaded.state_dict()
    assert set(src_sd) == set(got_sd)
    for k in src_sd:
        assert torch.equal(src_sd[k], got_sd[k].to(src_sd[k].dtype)), k  # 逐位复原
