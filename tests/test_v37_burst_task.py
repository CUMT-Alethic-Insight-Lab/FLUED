"""v3.7 Q13 突发性注入臂 (burstiness injection, prereg 2026-08-22 冻结;
spec: docs/versions/v3.7/FLUED_V3_7_Q13_BURSTINESS_INJECTION_20260822_CN.md).

数据层注入: 每训练窗现采一个 32-64B 语料随机段 (CorpusSampler 随机文件偏移,
防背护栏: (偏移,长度) 进程级登记, 同 epoch 重复采中重抽 N=8 后响亮报错,
严禁固定段库), 在窗内 R=3 个随机位置逐字重复插入; 第 R 次出现的末 2-4 个
非边界字符 force-mask, 前 R-1 次 force-unmask. 不加新损失项 (注入只改数据
分布); 指标 burst_tail_byte_acc/burst_tail_exact/burst_count/burst_tail_chars,
off 时零占位.

Covers: (1) off = 逐比特不变 + 零 RNG 消耗 + 零占位; (2) CorpusSampler 现采/
登记/重抽/响亮报错; (3) splice 确定性与结构不变量 (R=3 出现/位置随机化/
段尾遮蔽/加宽); (4) 遮蔽纪律 (段尾遮, 早次出现可见); (5) 防背断言与冻结值
越界报错; (6) 三方互斥与非 slm 响亮报错; (7) e2e 指标 + 无新损失项; (8)
parser 默认.
"""

from __future__ import annotations

import pytest
import torch

from flued.data import BYTE_OFFSET, MASK_ID, PAD_ID
from flued.v36 import FLUEDV36
from tests.test_v37_retrieval_task import TEXT1, TEXT2, _clean, _row_bytes
from tests.test_v37_slm import _s1_args, tiny_config
from tools.train.v3_6 import train_v36_s1 as s1


@pytest.fixture()
def corpus_file(tmp_path):
    """中文为主的临时语料 (足够大, 段抽取不撞车)."""
    p = tmp_path / "corpus.txt"
    p.write_bytes("天地玄黄宇宙洪荒日月盈昃辰宿列张律吕调阳云腾致雨露结为霜".encode("utf-8") * 40)
    return p


def _sampler(path) -> s1.CorpusSampler:
    return s1.CorpusSampler(str(path))


# --- 1. off = 逐比特不变 ---------------------------------------------------------


def test_burst_off_is_bitwise_identical():
    torch.manual_seed(0)
    model = FLUEDV36(tiny_config())
    batch = (torch.randint(1, 257, (2, 48)),)
    device = torch.device("cpu")
    gen_state_before = s1._BURST_GENERATOR.get_state()
    torch.manual_seed(123)
    loss1, m1 = s1.step_model(model, batch, _s1_args(burst_prob=0.0), device, train=False)
    torch.manual_seed(123)
    loss2, m2 = s1.step_model(model, batch, _s1_args(burst_prob=0.0), device, train=False)
    assert torch.equal(loss1, loss2)
    assert torch.equal(s1._BURST_GENERATOR.get_state(), gen_state_before)  # zero RNG consumption
    for key in ("burst_tail_byte_acc", "burst_tail_exact", "burst_count", "burst_tail_chars"):
        assert key in m1 and m1[key].item() == 0.0
    # the off-path loss is exactly the three-task sum (no new loss term)
    expect = m1["direct_loss"] * 1.0 + m1["completion_loss"] * 1.0 + m1["predict_loss"] * 1.0
    assert torch.equal(loss1, expect)
    for key in m1:
        if key.startswith("burst_"):
            continue
        assert torch.equal(m1[key], m2[key])


def test_parser_defaults_burst_off():
    from tools.train.v3_6.train_v36 import build_parser

    s1_parser = build_parser()
    s1._add_s1_args(s1_parser)
    args = s1_parser.parse_args([])
    assert args.burst_prob == 0.0  # default off = zero intrusion
    assert args.burst_repeat == 3
    assert args.burst_tail_max_chars == 4


# --- 2. CorpusSampler: 现采/登记/重抽/响亮报错 -----------------------------------


def test_corpus_sampler_draws_fresh_registered_segments(corpus_file):
    smp = _sampler(corpus_file)
    gen = torch.Generator().manual_seed(0)
    keys = []
    for _ in range(8):
        seg, key = smp.draw(gen)
        assert 16 <= len(seg) <= 64
        seg.decode("utf-8")  # 边界吸附后可解码
        keys.append(key)
    assert len(set(keys)) == len(keys)  # 登记簿: 无重复 (偏移, 长度)
    assert set(keys) == smp._seen


def _tiny_corpus(tmp_path):
    """40B 小语料 + seg_min=seg_max=32: 长度维固定, 偏移维 7 个 -> 键空间 7,
    防背重抽/耗尽两条路径都可确定性构造."""
    p = tmp_path / "tiny.txt"
    p.write_bytes("玄".encode("utf-8") * 13 + b"x")  # 40B
    return p


def _candidate_keys(smp: s1.CorpusSampler, seed: int, count: int) -> list[tuple[int, int]]:
    """Replay the draw stream's candidate keys (off, len) without touching the
    sampler (draw order: offset randint, then length randint, per attempt)."""
    probe = torch.Generator().manual_seed(seed)
    keys = []
    for _ in range(count):
        off = int(torch.randint(0, smp._size - smp._seg_max - 1, (1,), generator=probe))
        ln = int(torch.randint(smp._seg_min, smp._seg_max + 1, (1,), generator=probe))
        keys.append((off, ln))
    return keys


def test_corpus_sampler_collision_redraws(tmp_path):
    """同 epoch 重复采中同一段 -> 重抽: 预登记首个候选键, 抽中的必是候选流里
    的下一个未登记键."""
    smp = s1.CorpusSampler(str(_tiny_corpus(tmp_path)), seg_min=32, seg_max=32)
    cands = _candidate_keys(smp, seed=0, count=s1._RETRIEVAL_MAX_RETRY)
    smp._seen = {cands[0]}
    expected = next(k for k in cands if k != cands[0])
    seg, key = smp.draw(torch.Generator().manual_seed(0))
    assert key == expected and key != cands[0]  # 撞登记 -> 重抽到下一个键
    assert key in smp._seen
    seg.decode("utf-8")


def test_corpus_sampler_exhausted_retries_fail_loudly(tmp_path):
    """重抽上限 N=8 后响亮报错 (防背护栏机械断言)."""
    smp = s1.CorpusSampler(str(_tiny_corpus(tmp_path)), seg_min=32, seg_max=32)
    smp._seen = {(off, 32) for off in range(7)}  # 全部键已登记
    with pytest.raises(RuntimeError, match="防背护栏"):
        smp.draw(torch.Generator().manual_seed(0))


# --- 3. splice 确定性与结构不变量 ---------------------------------------------------


def test_splice_burst_structure_invariants(corpus_file):
    clean = _clean([TEXT1, TEXT2], 384)
    smp = _sampler(corpus_file)
    out, metas = s1._splice_burst(clean, 1.0, torch.Generator().manual_seed(7), smp)
    assert out.size(1) > clean.size(1)  # 插入式加宽
    for b, m in enumerate(metas):
        assert m is not None  # prob 1.0 selects every eligible row
        row = _row_bytes(out[b])
        n_orig = int(clean[b].ne(PAD_ID).sum())
        # R=3 次出现, 字节序递增, 内容逐字节相同 (逐字重复)
        occ = m["occurrences"]
        assert len(occ) == 3
        assert occ[0][0] < occ[1][0] < occ[2][0]
        segs = [row[lo:hi] for lo, hi in occ]
        assert segs[0] == segs[1] == segs[2]
        assert 16 <= len(segs[0]) <= 64
        # 段来自语料 (偏移, 长度) 登记处: 吸附后的段是登记读窗的子串
        with open(corpus_file, "rb") as fh:
            fh.seek(m["seg_offset"])
            read_back = fh.read(m["seg_len"] + 8)
        assert segs[0] in read_back
        # 遮蔽段尾 = 第 R 次出现的末 2-4 个非边界字符
        elo, ehi = m["echo_span"]
        assert (elo, ehi) == (occ[-1][1] - len(m["answer_b"]), occ[-1][1])
        assert row[elo:ehi] == m["answer_b"]
        ans = m["answer_b"].decode("utf-8")
        assert len(ans) == m["tail_chars"] and 2 <= m["tail_chars"] <= 4
        assert not any(ch in s1._BOUNDARY_CHARS for ch in ans)
        # 原窗字节保持: 去掉三段插入后是原文
        stripped = row[: occ[0][0]] + row[occ[0][1] : occ[1][0]] + row[occ[1][1] : occ[2][0]] + row[occ[2][1] :]
        assert stripped == _row_bytes(clean[b])


def test_splice_burst_positions_randomized(corpus_file):
    """位置随机化 (不固定窗首/窗尾): 跨种子出现位置确实变化."""
    clean = _clean([TEXT1], 384)
    seen = set()
    for seed in range(8):
        smp = _sampler(corpus_file)
        _, metas = s1._splice_burst(clean, 1.0, torch.Generator().manual_seed(seed), smp)
        m = metas[0]
        assert m is not None
        seen.add(tuple(m["occurrences"]))
    assert len(seen) > 1


def test_splice_burst_deterministic_same_seed(corpus_file):
    clean = _clean([TEXT1, TEXT2], 384)
    out1, metas1 = s1._splice_burst(clean, 1.0, torch.Generator().manual_seed(7), _sampler(corpus_file))
    out2, metas2 = s1._splice_burst(clean, 1.0, torch.Generator().manual_seed(7), _sampler(corpus_file))
    assert torch.equal(out1, out2)
    assert metas1 == metas2
    out3, metas3 = s1._splice_burst(clean, 1.0, torch.Generator().manual_seed(8), _sampler(corpus_file))
    assert not torch.equal(out1, out3) or metas1 != metas3  # non-vacuous


def test_splice_burst_prob_zero_and_short_window(corpus_file):
    clean = _clean([TEXT1, TEXT2], 200)
    out, metas = s1._splice_burst(clean, 0.0, torch.Generator().manual_seed(11), _sampler(corpus_file))
    assert torch.equal(out, clean)
    assert metas == [None, None]
    short = _clean([b"hi burst"], 16)  # n < 32: 不合格
    out2, metas2 = s1._splice_burst(short, 1.0, torch.Generator().manual_seed(11), _sampler(corpus_file))
    assert torch.equal(out2, short)
    assert metas2 == [None]


# --- 4. 遮蔽纪律 ---------------------------------------------------------------------


def test_burst_mask_overrides_tail_masked_early_visible(corpus_file):
    clean = _clean([TEXT1], 384)
    out, metas = s1._splice_burst(clean, 1.0, torch.Generator().manual_seed(3), _sampler(corpus_file))
    m = metas[0]
    byte_mask = torch.ones_like(out, dtype=torch.bool)  # 常规掩码全遮
    after = s1._burst_mask_overrides(byte_mask.clone(), metas)
    elo, ehi = m["echo_span"]
    assert after[0, elo:ehi].all()  # 第 R 次段尾 force-mask
    for lo, hi in m["occurrences"][:-1]:
        assert not after[0, lo:hi].any()  # 前 R-1 次 force-unmask (突发性本体)
    keep = torch.ones_like(after)
    keep[0, elo:ehi] = False
    for lo, hi in m["occurrences"][:-1]:
        keep[0, lo:hi] = False
    assert torch.equal(after & keep, byte_mask & keep)  # 其余字节不动
    source = out.masked_fill(after, MASK_ID)
    assert (source[0, elo:ehi] == MASK_ID).all()
    for lo, hi in m["occurrences"][:-1]:
        assert (source[0, lo:hi] != MASK_ID).all()


# --- 5/6. 响亮报错: 冻结值越界 / 三方互斥 / 非 slm -----------------------------------


def test_check_burst_args_frozen_values_loud():
    base = _s1_args(burst_prob=0.5)
    base.backbone_mode = "slm"
    base.burst_repeat = 2
    with pytest.raises(SystemExit, match="burst-repeat"):
        s1._check_burst_args(base)
    base.burst_repeat = 4
    with pytest.raises(SystemExit, match="burst-repeat"):
        s1._check_burst_args(base)
    base = _s1_args(burst_prob=0.5)
    base.backbone_mode = "slm"
    base.burst_tail_max_chars = 5
    with pytest.raises(SystemExit, match="burst-tail-max-chars"):
        s1._check_burst_args(base)
    base.burst_tail_max_chars = 1
    with pytest.raises(SystemExit, match="burst-tail-max-chars"):
        s1._check_burst_args(base)
    # 冻结值校验在 off 时同样生效 (越界即响亮报错)
    off = _s1_args()
    off.burst_repeat = 7
    with pytest.raises(SystemExit, match="burst-repeat"):
        s1._check_burst_args(off)
    s1._check_burst_args(_s1_args())  # canonical off path passes silently


def test_check_burst_args_mutex_and_slm():
    base = _s1_args(burst_prob=0.5, cloze_prob=0.3)
    base.backbone_mode = "slm"
    with pytest.raises(SystemExit, match="mutually exclusive"):
        s1._check_burst_args(base)
    base = _s1_args(burst_prob=0.5, retrieval_prob=0.3)
    base.backbone_mode = "slm"
    with pytest.raises(SystemExit, match="mutually exclusive"):
        s1._check_burst_args(base)
    base = _s1_args(burst_prob=0.5)
    base.backbone_mode = "xattn"
    with pytest.raises(SystemExit, match="slm"):
        s1._check_burst_args(base)
    ok = _s1_args(burst_prob=0.5)
    ok.backbone_mode = "slm"
    s1._check_burst_args(ok)


def test_step_model_burst_rejects_mutex_and_xattn(corpus_file):
    torch.manual_seed(0)
    batch = (_clean([TEXT1, TEXT2], 384),)
    s1._BURST_SAMPLER = _sampler(corpus_file)
    try:
        model = FLUEDV36(tiny_config(backbone_mode="xattn", k_row_source="memory", v_row_source="memory"))
        with pytest.raises(ValueError, match="burst"):
            s1.step_model(model, batch, _s1_args(burst_prob=0.3), torch.device("cpu"), train=False)
        model = FLUEDV36(tiny_config())
        args = _s1_args(burst_prob=0.3, retrieval_prob=0.3)
        with pytest.raises(ValueError, match="mutually exclusive"):
            s1.step_model(model, batch, args, torch.device("cpu"), train=False)
    finally:
        s1._BURST_SAMPLER = None  # restore module state


def test_step_model_burst_requires_sampler():
    torch.manual_seed(0)
    model = FLUEDV36(tiny_config())
    batch = (torch.randint(1, 257, (2, 48)),)
    s1._BURST_SAMPLER = None
    with pytest.raises(ValueError, match="CorpusSampler"):
        s1.step_model(model, batch, _s1_args(burst_prob=0.3), torch.device("cpu"), train=False)


# --- 7. e2e: 指标 + 无新损失项 --------------------------------------------------------


def test_step_model_burst_e2e_metrics_and_no_new_loss(corpus_file):
    torch.manual_seed(0)
    cfg = tiny_config(max_chunks=64, max_span=32, bytes_per_chunk=16, max_positions=64)
    model = FLUEDV36(cfg)
    args = _s1_args(burst_prob=1.0, mask_prob=0.1, max_chunks=64, max_span=32)
    batch = (_clean([TEXT1, TEXT2], 384),)
    s1._BURST_SAMPLER = _sampler(corpus_file)
    s1._BURST_GENERATOR.manual_seed(42 + s1._BURST_SEED_OFFSET)
    try:
        loss, metrics = s1.step_model(model, batch, args, torch.device("cpu"), train=True)
    finally:
        s1._BURST_SAMPLER = None
    assert torch.isfinite(loss)
    for key in ("burst_tail_byte_acc", "burst_tail_exact", "burst_count", "burst_tail_chars"):
        assert key in metrics, key
        assert torch.isfinite(metrics[key]), key
    assert metrics["burst_count"].item() == 1.0  # prob 1.0 + 容量足够: 全激活
    assert 0.0 <= metrics["burst_tail_byte_acc"].item() <= 1.0
    assert 2.0 <= metrics["burst_tail_chars"].item() <= 4.0
    # 不加新损失项: loss 恰好是三任务加权和 (cloze/retrieval 零占位不影响)
    expect = (
        metrics["direct_loss"] * 1.0
        + metrics["completion_loss"] * 1.0
        + metrics["predict_loss"] * 1.0
    )
    assert torch.equal(loss.detach(), expect)
    loss.backward()
    assert model.backbone.align_k.weight.grad is not None
    assert model.backbone.align_k.weight.grad.abs().sum() > 0


def test_step_model_burst_deterministic_eval_seed(corpus_file):
    """eval 同源固定种子: 两次 evaluate 式传递 (各自新 sampler + 同种子)
     splice 与指标逐比特一致."""
    torch.manual_seed(0)
    cfg = tiny_config(max_chunks=64, max_span=32, bytes_per_chunk=16, max_positions=64)
    model = FLUEDV36(cfg)
    args = _s1_args(burst_prob=1.0, mask_prob=0.1, max_chunks=64, max_span=32)
    batch = (_clean([TEXT1, TEXT2], 384),)
    rows = []
    for _ in range(2):
        s1._BURST_SAMPLER = _sampler(corpus_file)
        torch.manual_seed(args.eval_mask_seed)
        s1._MASK_GENERATOR.manual_seed(args.eval_mask_seed)
        s1._BURST_GENERATOR.manual_seed(args.eval_mask_seed + s1._BURST_SEED_OFFSET)
        loss, metrics = s1.step_model(model, batch, args, torch.device("cpu"), train=False)
        rows.append((loss, dict(metrics)))
    s1._BURST_SAMPLER = None
    assert torch.equal(rows[0][0], rows[1][0])
    for key in rows[0][1]:
        assert torch.equal(rows[0][1][key], rows[1][1][key]), key
