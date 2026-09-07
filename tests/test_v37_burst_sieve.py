"""v3.7 Q14 需求侧先验筛注入臂 (修订案 2026-08-23 冻结; spec:
docs/versions/v3_7/FLUED_V3_7_Q14_PRIOR_SIEVED_DEMAND_20260823_CN.md).

Q13 构造一字不改, 新增三项: (1) 先验筛 -- 候选段构造期过裸猜测量 (参考模型
固定在开工 checkpoint, 段单独成文档测段尾遮蔽 byte_acc, <0.05 才录用, 重抽
N=8 沿用, 耗尽不激活, 全程不重筛); (2) 产出率入册 -- burst_sieve_reject_rate
/ burst_yield 随行, 产出率 <70% 打报警行 (不静默放宽); (3) 臂中点复测钩 --
max_steps//2 用当前模型对滚动 ledger (最近 <=2000 个已用段) 重测裸猜率,
均值漂移 >0.02 登记先验侵蚀 (print + out_dir/prior_erosion_midpoint.json).

Covers: (1) 旗标默认关 = 逐比特不变 + 零占位; (2) 裸猜测量函数本身 (tiny
模型出 [0,1] 浮点/None); (3) 筛子拒收 (恒可猜 -> N=8 耗尽不激活, reject
统计全中) 与录用 (恒不可猜 -> 激活, 基准入 ledger); (4) 产出率指标
(reject 全开时 yield=0; 筛关时 yield=1) 与报警行; (5) ledger 滚动登记
(maxlen 2000); (6) 中点复测文件落盘 + 先验侵蚀登记行; (7) 响亮报错
(筛挂空任务/非 slm/互斥沿用); (8) parser 默认.
"""

from __future__ import annotations

import json

import pytest
import torch

from flued.v36 import FLUEDV36
from tests.test_v37_burst_task import _sampler
from tests.test_v37_retrieval_task import TEXT1, TEXT2, _clean
from tests.test_v37_slm import _s1_args, tiny_config
from tools.train.v3_6 import train_v36_s1 as s1


@pytest.fixture()
def corpus_file(tmp_path):
    p = tmp_path / "corpus.txt"
    p.write_bytes("天地玄黄宇宙洪荒日月盈昃辰宿列张律吕调阳云腾致雨露结为霜".encode("utf-8") * 40)
    return p


@pytest.fixture()
def sieve_off_model():
    """构造期筛用假参考模型占位 (真测量由 monkeypatch 脚本化)."""
    torch.manual_seed(0)
    return FLUEDV36(tiny_config())


# --- 1. 旗标默认关 = 逐比特不变 + 零占位 -------------------------------------------


def test_sieve_off_is_bitwise_identical(corpus_file):
    clean = _clean([TEXT1, TEXT2], 384)
    out0, metas0 = s1._splice_burst(clean, 1.0, torch.Generator().manual_seed(7), _sampler(corpus_file))
    stats = {"drawn": 0, "spliced": 0, "sieve_measured": 0, "sieve_rejected": 0}
    out1, metas1 = s1._splice_burst(
        clean, 1.0, torch.Generator().manual_seed(7), _sampler(corpus_file),
        sieve_model=None, stats=stats,
    )
    assert torch.equal(out0, out1)
    assert metas0 == metas1  # 筛关时 stats 袋不改变任何行为
    assert stats == {"drawn": 2, "spliced": 2, "sieve_measured": 0, "sieve_rejected": 0}


def test_off_metrics_carry_zeroed_q14_keys():
    torch.manual_seed(0)
    model = FLUEDV36(tiny_config())
    batch = (torch.randint(1, 257, (2, 48)),)
    loss, m = s1.step_model(model, batch, _s1_args(burst_prob=0.0), torch.device("cpu"), train=False)
    assert torch.isfinite(loss)
    for key in ("burst_sieve_reject_rate", "burst_yield"):
        assert key in m and m[key].item() == 0.0


def test_parser_default_sieve_off():
    from tools.train.v3_6.train_v36 import build_parser

    s1_parser = build_parser()
    s1._add_s1_args(s1_parser)
    args = s1_parser.parse_args([])
    assert args.burst_prior_sieve is False  # 默认关 = Q13 形态


# --- 2. 裸猜测量函数 ---------------------------------------------------------------


def test_prior_guess_acc_plumbing():
    """段单独成文档 (无前次出现无上下文), 段尾遮蔽, fp32 eval -> [0,1] 浮点."""
    torch.manual_seed(0)
    model = FLUEDV36(tiny_config(max_chunks=64, max_span=32, bytes_per_chunk=16, max_positions=64))
    seg = "天地玄黄宇宙洪荒日月盈昃辰宿列张".encode("utf-8")  # 48B
    acc = s1._burst_prior_guess_acc(model, seg, 9)  # 末 3 字 = 9B
    assert acc is not None and 0.0 <= acc <= 1.0
    # 模式保持纪律: 测量内部 eval, 进出同模 (参考模型恒 eval / 中点钩当前模型 train)
    assert model.training
    model.eval()
    s1._burst_prior_guess_acc(model, seg, 9)
    assert not model.training
    # 段尾落不上网格的小网格模型 -> None (调用侧按拒收处理)
    torch.manual_seed(0)
    tiny_grid = FLUEDV36(tiny_config())  # 4 chunks x 8 slots = 32B 网格
    assert s1._burst_prior_guess_acc(tiny_grid, seg, 9) is None


# --- 3. 筛子拒收/录用 (脚本化裸猜率) -------------------------------------------------


def test_sieve_rejects_guessable_segments(corpus_file, sieve_off_model, monkeypatch):
    """候选段恒可猜 (裸猜 0.5 >= 0.05) -> 全部拒收 -> N=8 耗尽 -> 不激活,
    行逐字节不变; reject 统计 8/8."""
    monkeypatch.setattr(s1, "_burst_prior_guess_acc", lambda *a, **k: 0.5)
    clean = _clean([TEXT1], 384)
    stats = {"drawn": 0, "spliced": 0, "sieve_measured": 0, "sieve_rejected": 0}
    out, metas = s1._splice_burst(
        clean, 1.0, torch.Generator().manual_seed(7), _sampler(corpus_file),
        sieve_model=sieve_off_model, stats=stats,
    )
    assert metas == [None]
    assert torch.equal(out, clean)
    assert stats["drawn"] == 1 and stats["spliced"] == 0
    assert stats["sieve_measured"] == s1._RETRIEVAL_MAX_RETRY
    assert stats["sieve_rejected"] == s1._RETRIEVAL_MAX_RETRY


def test_sieve_accepts_unguessable_and_records_baseline(corpus_file, sieve_off_model, monkeypatch):
    """候选段恒不可猜 (裸猜 0.01 < 0.05) -> 录用激活, 筛时基准入 ledger."""
    monkeypatch.setattr(s1, "_burst_prior_guess_acc", lambda *a, **k: 0.01)
    clean = _clean([TEXT1, TEXT2], 384)
    smp = _sampler(corpus_file)
    stats = {"drawn": 0, "spliced": 0, "sieve_measured": 0, "sieve_rejected": 0}
    out, metas = s1._splice_burst(
        clean, 1.0, torch.Generator().manual_seed(7), smp,
        sieve_model=sieve_off_model, stats=stats,
    )
    assert all(m is not None for m in metas)
    assert stats == {"drawn": 2, "spliced": 2, "sieve_measured": 2, "sieve_rejected": 0}
    assert len(smp.ledger) == 2
    for ent in smp.ledger:
        assert ent["prior_baseline"] == 0.01
        assert 2 <= ent["tail_bytes"] <= 12
        assert len(ent["seg"]) >= 16


def test_sieve_threshold_boundary(corpus_file, sieve_off_model, monkeypatch):
    """阈值边界: 恰好 0.05 不录用 (<0.05 才录用)."""
    monkeypatch.setattr(s1, "_burst_prior_guess_acc", lambda *a, **k: 0.05)
    clean = _clean([TEXT1], 384)
    out, metas = s1._splice_burst(
        clean, 1.0, torch.Generator().manual_seed(7), _sampler(corpus_file),
        sieve_model=sieve_off_model, stats={"drawn": 0, "spliced": 0, "sieve_measured": 0, "sieve_rejected": 0},
    )
    assert metas == [None]
    assert torch.equal(out, clean)


# --- 4. 产出率指标与报警行 ------------------------------------------------------------


def test_yield_metrics_full_reject_and_free_pass(corpus_file, monkeypatch):
    torch.manual_seed(0)
    cfg = tiny_config(max_chunks=64, max_span=32, bytes_per_chunk=16, max_positions=64)
    batch = (_clean([TEXT1, TEXT2], 384),)
    # 全拒收: yield=0, reject_rate=1, burst_count=0
    monkeypatch.setattr(s1, "_burst_prior_guess_acc", lambda *a, **k: 0.5)
    model = FLUEDV36(cfg)
    args = _s1_args(burst_prob=1.0, burst_prior_sieve=True, mask_prob=0.1, max_chunks=64, max_span=32)
    s1._BURST_SAMPLER = _sampler(corpus_file)
    s1._BURST_SIEVE_MODEL = sieve_off = FLUEDV36(cfg)
    s1._BURST_GENERATOR.manual_seed(42 + s1._BURST_SEED_OFFSET)
    try:
        loss, m = s1.step_model(model, batch, args, torch.device("cpu"), train=False)
    finally:
        s1._BURST_SAMPLER = None
        s1._BURST_SIEVE_MODEL = None
    assert torch.isfinite(loss)
    assert m["burst_yield"].item() == 0.0
    assert m["burst_sieve_reject_rate"].item() == 1.0
    assert m["burst_count"].item() == 0.0
    # 筛关: 同一批全激活 -> yield=1, reject_rate=0
    model2 = FLUEDV36(cfg)
    args2 = _s1_args(burst_prob=1.0, burst_prior_sieve=False, mask_prob=0.1, max_chunks=64, max_span=32)
    s1._BURST_SAMPLER = _sampler(corpus_file)
    s1._BURST_GENERATOR.manual_seed(42 + s1._BURST_SEED_OFFSET)
    try:
        _, m2 = s1.step_model(model2, batch, args2, torch.device("cpu"), train=False)
    finally:
        s1._BURST_SAMPLER = None
    assert m2["burst_yield"].item() == 1.0
    assert m2["burst_sieve_reject_rate"].item() == 0.0


def test_yield_alarm_line(capsys):
    s1._burst_yield_alarm(100, 0.55)
    out = capsys.readouterr().out
    assert "WARN" in out and "0.55" in out and "不静默放宽" in out
    s1._burst_yield_alarm(100, 0.70)  # 线上不报警
    s1._burst_yield_alarm(100, 0.95)
    assert capsys.readouterr().out == ""


# --- 5. ledger 滚动登记 -----------------------------------------------------------------


def test_ledger_rolling_maxlen(corpus_file):
    smp = _sampler(corpus_file)
    for i in range(2005):
        smp.note_used(f"seg{i}".encode(), 6, 0.01)
    assert len(smp.ledger) == 2000  # 滚动 <=2000
    assert smp.ledger[0]["seg"] == b"seg5"  # 最老 5 条已滚出
    # 筛关条目 baseline=None: 不参与中点对比
    smp2 = _sampler(corpus_file)
    smp2.note_used(b"x" * 40, 6, None)
    assert smp2.ledger[-1]["prior_baseline"] is None


# --- 6. 中点复测钩 ---------------------------------------------------------------------


def test_midpoint_check_writes_json_and_erosion_line(corpus_file, tmp_path, monkeypatch, capsys):
    torch.manual_seed(0)
    model = FLUEDV36(tiny_config())
    smp = _sampler(corpus_file)
    smp.note_used("天地玄黄宇宙洪荒日月盈昃辰宿列张".encode(), 9, 0.01)
    smp.note_used("律吕调阳云腾致雨露结为霜天地玄黄".encode(), 6, 0.02)
    smp.note_used(b"z" * 40, 6, None)  # 无基准条目被跳过
    s1._BURST_SAMPLER = smp
    # 当前模型裸猜率漂移 +0.05 -> 均值漂移 >0.02 -> 先验侵蚀登记行
    monkeypatch.setattr(s1, "_burst_prior_guess_acc", lambda m, seg, tb: {9: 0.06, 6: 0.07}[tb])
    args = _s1_args(max_steps=20)
    try:
        s1._burst_prior_midpoint_check(model, args, torch.device("cpu"), tmp_path)
    finally:
        s1._BURST_SAMPLER = None
    out = capsys.readouterr().out
    assert "先验侵蚀" in out and "WARN" in out
    payload = json.loads((tmp_path / "prior_erosion_midpoint.json").read_text(encoding="utf-8"))
    assert payload["n_segments"] == 2
    assert payload["step"] == 10
    assert payload["prior_erosion"] is True
    assert payload["drift_mean"] == pytest.approx(0.05)
    for item in payload["items"]:
        assert set(item) == {"seg_len", "tail_bytes", "prior_at_init", "prior_at_midpoint", "drift"}
        assert item["drift"] == pytest.approx(item["prior_at_midpoint"] - item["prior_at_init"], abs=1e-5)


def test_midpoint_check_no_erosion(corpus_file, tmp_path, monkeypatch, capsys):
    torch.manual_seed(0)
    model = FLUEDV36(tiny_config())
    smp = _sampler(corpus_file)
    smp.note_used("天地玄黄宇宙洪荒日月盈昃辰宿列张".encode(), 9, 0.01)
    s1._BURST_SAMPLER = smp
    monkeypatch.setattr(s1, "_burst_prior_guess_acc", lambda m, seg, tb: 0.02)  # 漂移 0.01 < 0.02
    args = _s1_args(max_steps=20)
    try:
        s1._burst_prior_midpoint_check(model, args, torch.device("cpu"), tmp_path)
    finally:
        s1._BURST_SAMPLER = None
    out = capsys.readouterr().out
    assert "无先验侵蚀" in out and "WARN" not in out
    payload = json.loads((tmp_path / "prior_erosion_midpoint.json").read_text(encoding="utf-8"))
    assert payload["prior_erosion"] is False


# --- 7. 响亮报错 ------------------------------------------------------------------------


def test_sieve_requires_burst_and_slm():
    base = _s1_args()  # 筛开但 burst 关
    base.burst_prior_sieve = True
    with pytest.raises(SystemExit, match="burst-prob"):
        s1._check_burst_args(base)
    base = _s1_args(burst_prob=0.5, burst_prior_sieve=True, cloze_prob=0.3)
    base.backbone_mode = "slm"
    with pytest.raises(SystemExit, match="mutually exclusive"):
        s1._check_burst_args(base)
    base = _s1_args(burst_prob=0.5, burst_prior_sieve=True, retrieval_prob=0.3)
    base.backbone_mode = "slm"
    with pytest.raises(SystemExit, match="mutually exclusive"):
        s1._check_burst_args(base)
    base = _s1_args(burst_prob=0.5, burst_prior_sieve=True)
    base.backbone_mode = "xattn"
    with pytest.raises(SystemExit, match="slm"):
        s1._check_burst_args(base)
    ok = _s1_args(burst_prob=0.5, burst_prior_sieve=True)
    ok.backbone_mode = "slm"
    s1._check_burst_args(ok)
