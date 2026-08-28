"""v3.7 Q18 v2 读出墙裁定臂 — B 计划 s1 骨架移植 (2026-08-28).
宿主: tools/train/v3_6/train_v36_s1.py (--q18-arm/--q18-warmstart/
--q18-base-ckpt 旗标 + 主循环/损失层挂接); 机制本体在独立训练器模块
(train_q17_oracle_readout / train_q18_readout_wall), 本文件只测挂接层。

Covers: (1) 旗标响亮校验 (缺 base-ckpt / base 缺文件 / 非 d 格基座 /
Aprime 缺 donor / eval_only / cloze-retrieval 组合 → SystemExit); (2) 基
座配置回填 (IO 键剔除防写穿基座 run dir, data_manifest 强制空, 缺文件响
亮); (3) 链范围 (A 臂挂接后可训练参数 == Q17 修订 v1 足迹, 其余全冻,
tied byte_lookup 护栏, 种子 42/1 链权重不同 + 同种子可复现); (4) 温启动
零变化律 (A′ 路径温启动→自检串联, 自检失败响亮传播臂作废 + 映射报告已
落盘供 postmortem, 通过则 zero_change 块落盘 + 抽签流重 seed); (5) 抽签
流隔离 (q18 退火抽签流 == 独立种子参照, mask/burst 消耗不污染, 重 seed
复位); (6) legacy 零侵入 (q18_arm 缺省/空 = 关)。机制级 parity
(stream/双态/α) 由 tests/test_q17_oracle_readout.py 守卫, 不重测。"""

from __future__ import annotations

import json
from argparse import Namespace
from pathlib import Path

import pytest
import torch

import tools.train.v3_6.train_v36_s1 as s1
from tests.test_q17_oracle_readout import _tiny_d_run_dir
from tools.train.v3_6.train_v36 import build_model


def _q18_args(cfg, run_dir, **kw):
    """从 tiny fixture 的完整 config 派生 Q18 模式 args (默认 A 臂合法形态)。"""
    d = vars(cfg).copy()
    d.update(
        q18_arm="A",
        q18_warmstart="oracle",
        q18_base_ckpt=str(run_dir),
        q18_donor_ckpt=str(run_dir),  # 占位; A′ 测试再换/打补丁
        q18_steps=0,
        q18_calib_windows=2,
        q18_zc_windows=2,
        q18_zc_threshold=0.15,
        q18_no_sieve=False,
        lam_unmix=1e-2,
        lam_stage2=1.0,
        eval_only="",
        cloze_prob=0.0,
        retrieval_prob=0.0,
    )
    d.update(kw)
    return Namespace(**d)


# --- 1. 旗标响亮校验 ----------------------------------------------------------


def test_validate_requires_base_ckpt(tmp_path):
    run_dir, cfg = _tiny_d_run_dir(tmp_path)
    with pytest.raises(SystemExit):
        s1._q18_validate_args(_q18_args(cfg, run_dir, q18_base_ckpt=""))
    with pytest.raises(SystemExit):
        s1._q18_validate_args(_q18_args(cfg, run_dir, q18_base_ckpt=str(tmp_path / "ghost")))


def test_validate_requires_latest_pt(tmp_path):
    run_dir, cfg = _tiny_d_run_dir(tmp_path)
    (run_dir / "latest.pt").rename(run_dir / "latest.pt.bak")
    with pytest.raises(SystemExit):
        s1._q18_validate_args(_q18_args(cfg, run_dir))


def test_validate_requires_d_grid_base(tmp_path):
    run_dir, cfg = _tiny_d_run_dir(tmp_path)
    with pytest.raises(SystemExit):
        s1._q18_validate_args(_q18_args(cfg, run_dir, backbone_mode="xattn"))
    with pytest.raises(SystemExit):
        s1._q18_validate_args(_q18_args(cfg, run_dir, v_row_source="memory"))


def test_validate_aprime_requires_donor(tmp_path):
    run_dir, cfg = _tiny_d_run_dir(tmp_path)
    with pytest.raises(SystemExit):
        s1._q18_validate_args(
            _q18_args(cfg, run_dir, q18_arm="Aprime", q18_donor_ckpt=str(tmp_path / "ghost"))
        )


def test_validate_rejects_eval_only_and_cloze_retrieval(tmp_path):
    run_dir, cfg = _tiny_d_run_dir(tmp_path)
    with pytest.raises(SystemExit):
        s1._q18_validate_args(_q18_args(cfg, run_dir, eval_only="some.pt"))
    with pytest.raises(SystemExit):
        s1._q18_validate_args(_q18_args(cfg, run_dir, cloze_prob=0.3))
    with pytest.raises(SystemExit):
        s1._q18_validate_args(_q18_args(cfg, run_dir, retrieval_prob=0.3))
    # 合法形态通过 (A 与 Aprime 双臂)
    s1._q18_validate_args(_q18_args(cfg, run_dir))
    s1._q18_validate_args(_q18_args(cfg, run_dir, q18_arm="Aprime"))


# --- 2. 基座配置回填 (IO 键剔除) -----------------------------------------------


def test_base_config_defaults_excludes_io_keys(tmp_path):
    run_dir, _cfg = _tiny_d_run_dir(tmp_path)
    d = s1._q18_base_config_defaults(str(run_dir))
    for k in ("out_dir", "run_id", "init_checkpoint", "init_prefixes", "eval_only", "config"):
        assert k not in d, f"IO 键 {k} 未剔除——继承基座会把续跑写进基座 run dir"
    assert d["data_manifest"] == ""
    assert d["backbone_mode"] == "slm" and d["v_row_source"] == "state"
    with pytest.raises(SystemExit):
        s1._q18_base_config_defaults(str(tmp_path / "ghost"))


# --- 3. 链范围 (Q17 修订 v1 足迹) ----------------------------------------------


def _expected_chain_param_ids(model):
    """链参数的 object-id 集 (与 q17._q17_unfreeze_chain 遍历规则同构)。
    tied-embedding 注记 (机制如实保留): decoder.byte_lookup 与模型级
    byte_lookup 是同一参数对象 (model.py 共享构造), decoder.parameters()
    含它——独立训练器的可训练集因此也含 byte_lookup, 本移植一字不改。"""
    ids = set()
    for mod in ("backbone", "decoder", "decoder_in", "decoder_in_mem"):
        if hasattr(model, mod):
            ids |= {id(p) for p in getattr(model, mod).parameters()}
    for sm_name in ("state_machine", "state_machine_k"):
        if hasattr(model, sm_name):
            sm = getattr(model, sm_name)
            ids.add(id(sm.readout_query))
            ids |= {id(p) for p in sm.realign.parameters()}
    return ids


def _load_tiny_model(run_dir, cfg):
    model = build_model(cfg)
    payload = torch.load(run_dir / "latest.pt", map_location="cpu", weights_only=False)
    model.load_state_dict(payload["model"], strict=True)
    return model, payload


def test_chain_scope_after_setup(tmp_path):
    run_dir, cfg = _tiny_d_run_dir(tmp_path)
    model, payload = _load_tiny_model(run_dir, cfg)
    args = _q18_args(cfg, run_dir, seed=42)
    report = s1._q18_setup_chain(model, args, torch.device("cpu"), tmp_path / "out", resuming=False)
    assert report is None  # A 臂无温启动报告
    trainable_ids = {id(p) for p in model.parameters() if p.requires_grad}
    assert trainable_ids == _expected_chain_param_ids(model)
    # 链外全冻抽查 (前端/写头/状态机递推本体)
    for n, p in model.named_parameters():
        if n.startswith(("encoder", "segmentor", "summarizer", "write_head")):
            assert not p.requires_grad, n
    # tied-embedding 护栏: byte_lookup 值保持基座 (链重初始化不得污染——
    # 它经 decoder 在可训练集内是独立训练器的如实机制, 值护栏同样照移植)
    for k, v in model.byte_lookup.state_dict().items():
        assert torch.equal(v, payload["model"][f"byte_lookup.{k}"]), k
    # A 臂从零: readout_query 与基座不同 (重初始化确实发生)
    assert not torch.equal(
        model.state_machine.readout_query.data, payload["model"]["state_machine.readout_query"]
    )


def test_chain_reinit_seed_reproducible(tmp_path):
    run_dir, cfg = _tiny_d_run_dir(tmp_path)
    ws = []
    for sd in (42, 1, 42):
        model, _p = _load_tiny_model(run_dir, cfg)
        s1._q18_setup_chain(
            model, _q18_args(cfg, run_dir, seed=sd), torch.device("cpu"), tmp_path / "o", resuming=False
        )
        ws.append(model.state_machine.readout_query.data.clone())
    assert not torch.equal(ws[0], ws[1])  # seed 42 vs 1 链权重不同
    assert torch.equal(ws[0], ws[2])  # 同种子可复现


# --- 4. 温启动零变化律 (A′ 路径, 温启动/自检打桩——机制本体由 test_q18 守卫) -----


class _FakeDonor(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.decoder_in_mem = torch.nn.Linear(4, 4)


def _patch_aprime(monkeypatch, zc_outcome):
    q17m, q18m = s1._q18_deps()
    calls = {"warmstart": 0, "zc": 0}
    monkeypatch.setattr(
        q18m, "load_model",
        lambda *a, **k: (_FakeDonor(), Namespace(v_row_source="memory", max_chunks=8, max_span=16), 0),
    )

    def _fake_warmstart(*a, **k):
        calls["warmstart"] += 1
        return {"column": "oracle", "windows": 2}

    monkeypatch.setattr(q18m, "_q18_warmstart", _fake_warmstart)

    def _fake_zc(*a, **k):
        calls["zc"] += 1
        if isinstance(zc_outcome, Exception):
            raise zc_outcome
        return zc_outcome

    monkeypatch.setattr(q18m, "_q18_zero_change_check", _fake_zc)
    return calls


def test_aprime_zero_change_loud_abort(tmp_path, monkeypatch):
    """自检失败 (初始化没接通) → RuntimeError 响亮传播, 臂作废重查不许判负;
    映射报告已在自检前落盘 (postmortem 纪律)。"""
    run_dir, cfg = _tiny_d_run_dir(tmp_path)
    model, _p = _load_tiny_model(run_dir, cfg)
    calls = _patch_aprime(monkeypatch, RuntimeError("Q18 零变化律自检失败: 0 窗可读"))
    args = _q18_args(cfg, run_dir, q18_arm="Aprime")
    out = tmp_path / "out"
    out.mkdir()
    with pytest.raises(RuntimeError, match="零变化律自检失败"):
        s1._q18_setup_chain(model, args, torch.device("cpu"), out, resuming=False)
    assert calls["warmstart"] == 1 and calls["zc"] == 1
    assert (out / "warmstart_report.json").exists()  # 自检前落盘


def test_aprime_zero_change_pass_writes_report(tmp_path, monkeypatch):
    """自检通过 → zero_change 块落盘 + 链解冻 + 抽签流重 seed (RNG 隔离)。"""
    run_dir, cfg = _tiny_d_run_dir(tmp_path)
    model, _p = _load_tiny_model(run_dir, cfg)
    calls = _patch_aprime(monkeypatch, (0.31, {"backbone": [0.31, 0.30], "direct": [0.10, 0.11]}))
    args = _q18_args(cfg, run_dir, q18_arm="Aprime", seed=42)
    out = tmp_path / "out"
    out.mkdir()
    report = s1._q18_setup_chain(model, args, torch.device("cpu"), out, resuming=False)
    assert calls["warmstart"] == 1 and calls["zc"] == 1
    saved = json.loads((out / "warmstart_report.json").read_text(encoding="utf-8"))
    assert saved["zero_change"]["mean"] == 0.31
    assert saved["zero_change"]["backbone_accs"] == [0.31, 0.3]
    trainable_ids = {id(p) for p in model.parameters() if p.requires_grad}
    assert trainable_ids == _expected_chain_param_ids(model)
    # RNG 隔离: 自检后抽签流已重 seed——下一抽 == 新 seed 流首抽
    _q17m, q18m = s1._q18_deps()
    ref = torch.Generator().manual_seed(42 + q18m._Q18_SEED_OFFSET)
    assert float(torch.rand((), generator=q18m._Q18_GENERATOR)) == float(torch.rand((), generator=ref))


# --- 5. 抽签流隔离 --------------------------------------------------------------


def test_draw_stream_isolation():
    q17m, q18m = s1._q18_deps()
    args = Namespace(seed=42)
    s1._q18_seed_streams(args)
    ref = torch.Generator().manual_seed(42 + q18m._Q18_SEED_OFFSET)
    draws = [float(torch.rand((), generator=q18m._Q18_GENERATOR)) for _ in range(4)]
    assert draws == [float(torch.rand((), generator=ref)) for _ in range(4)]
    # mask/burst 流消耗不污染 q18 流
    s1._q18_seed_streams(args)
    for _ in range(8):
        torch.rand((), generator=s1._MASK_GENERATOR)
        torch.rand((), generator=s1._BURST_GENERATOR)
    assert [float(torch.rand((), generator=q18m._Q18_GENERATOR)) for _ in range(4)] == draws
    # 重 seed 复位 (温启动/自检后 RNG 隔离条款)
    s1._q18_seed_streams(args)
    assert [float(torch.rand((), generator=q18m._Q18_GENERATOR)) for _ in range(4)] == draws
    # 与 Q17 偏移不混 (101_033 vs 101_077)
    q17_ref = torch.Generator().manual_seed(42 + q17m._Q17_SEED_OFFSET)
    assert draws[0] != float(torch.rand((), generator=q17_ref))


# --- 6. legacy 零侵入 -------------------------------------------------------------


def test_legacy_path_zero_intrusion():
    assert not s1._q18_enabled(Namespace())  # 无属性 = 关
    assert not s1._q18_enabled(Namespace(q18_arm=""))
    assert s1._q18_enabled(Namespace(q18_arm="A"))
    assert s1._q18_enabled(Namespace(q18_arm="Aprime"))
