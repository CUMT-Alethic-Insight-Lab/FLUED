"""v3.7 Q12 示例密集型招募臂 (修订案 v3, 2026-08-22 冻结; spec:
docs/versions/v3.7/FLUED_V3_7_RECRUITMENT_ARM_NATURAL_RETRIEVAL_20260821_CN.md
修订案 v3 + 附录 A1/A2/A3).

每条训练样本 = --retrieval-examples (2–4) 条完整示例 (答案可见) + 1 条查询
(答案遮蔽). 示例与查询内容独立 (来源段 span/内容两两不同), 角色随机化 (one
role draw per attempt), 遮蔽位置随机化 (uniform candidate). 反捷径条款
(Q12.2) 逐样本机械断言: 查询答案字符串不得出现在任何示例中 (字节级子串),
示例来源段 ≠ 查询来源段; 违反重抽 N=8, 仍违反样本不激活. 窗口预算 (A2②):
来源段与查询段永不截断, 溢出按最早示例先丢 (retrieval_drop_rate), 查询段
被挤到 chunk 网格外 = 构造缺陷 (retrieval_defect), 占用比入日志
(retrieval_budget_ratio). 默认 --retrieval-examples 0 = 无示例形态逐比特不变.

Covers: (1) flag off = bitwise-identical legacy splice + parser default;
(2) structure invariants (示例数/格式/答案可见/查询在尾); (3) 反捷径条款
(many-seed property + 注入恒冲突窗口必须不激活); (4) 预算规则 (溢出丢最早
示例 + 丢弃率 + 查询永不截断 + 窗沿缺陷弃用计数); (5) mask overrides
(示例答案可见, 查询 echo 全遮, 查询来源答案词 force-unmask); (6) store_block
只剔查询来源 chunk, 示例 store 行不动; (7) e2e 有限 loss + 全部新指标;
(8) 确定性; (9) 响亮报错 (examples 取值/无任务).
"""

from __future__ import annotations

import pytest
import torch

from flued.data import BYTE_OFFSET, MASK_ID, PAD_ID
from flued.v36 import FLUEDV36
from tests.test_v37_retrieval_task import TEXT1, TEXT2, _clean, _fake_chunks, _row_bytes
from tests.test_v37_slm import _s1_args, tiny_config
from tools.train.v3_6 import train_v36_s1 as s1

CAP = 64 * 32  # e2e 网格字节容量 (A2② 窗 = max_chunks * max_span)


def _n_valid(row: torch.Tensor) -> int:
    return int(row.ne(PAD_ID).sum())


def _example_block(row: bytes, n_orig: int, ex_metas: list, i: int) -> bytes:
    """Example block i spans from the previous block's end to its echo end."""
    start = n_orig if i == 0 else ex_metas[i - 1]["echo_span"][1]
    return row[start : ex_metas[i]["echo_span"][1]]


# --- 1. flag off = bitwise-identical legacy path ------------------------------


def test_examples_zero_is_bitwise_identical():
    clean = _clean([TEXT1, TEXT2], 384)
    out0, metas0 = s1._splice_retrieval(clean, 1.0, torch.Generator().manual_seed(7))
    out1, metas1 = s1._splice_retrieval(clean, 1.0, torch.Generator().manual_seed(7), "cjk", 0, CAP)
    assert torch.equal(out0, out1)
    assert metas0 == metas1
    for m in metas1:
        assert m is None or "examples" not in m  # legacy meta shape untouched


def test_parser_default_examples_zero():
    from tools.train.v3_6.train_v36 import build_parser

    s1_parser = build_parser()
    s1._add_s1_args(s1_parser)
    args = s1_parser.parse_args([])
    assert args.retrieval_examples == 0  # default off = 无示例形态


def test_off_metrics_carry_zeroed_q12_keys():
    torch.manual_seed(0)
    model = FLUEDV36(tiny_config())
    batch = (torch.randint(1, 257, (2, 48)),)
    loss, m = s1.step_model(
        model, batch, _s1_args(retrieval_prob=0.0, retrieval_examples=0), torch.device("cpu"), train=False
    )
    assert torch.isfinite(loss)
    for key in ("retrieval_budget_ratio", "retrieval_examples", "retrieval_drop_rate", "retrieval_defect"):
        assert key in m and m[key].item() == 0.0


# --- 2. structure invariants ----------------------------------------------------


def test_examples_structure_invariants():
    clean = _clean([TEXT1, TEXT2], 384)
    out, metas = s1._splice_retrieval(clean, 1.0, torch.Generator().manual_seed(7), "cjk", 3, 10**6)
    pre = "\n前文'".encode("utf-8")
    post = "'空格处是什么？".encode("utf-8")
    prompt = "\n答案是：".encode("utf-8")
    for b, m in enumerate(metas):
        assert m is not None
        row = _row_bytes(out[b])
        n_orig = _n_valid(clean[b])
        assert m["n_examples"] == 3 and m["n_dropped"] == 0
        assert len(m["examples"]) == 3
        assert m["budget_ratio"] == pytest.approx(len(row) / 10**6)
        # layout: examples first (contiguous), query LAST -- nothing is ever
        # inserted after the query block
        assert row.count(pre) == 4  # 3 examples + 1 query
        assert m["query_start"] == m["examples"][-1]["echo_span"][1]
        elo, ehi = m["echo_span"]
        assert elo < ehi == len(row)  # query echo at the very tail
        assert row[elo:ehi] == m["answer_b"]
        assert row[elo - len(prompt) : elo] == prompt
        qtail = row[m["query_start"] :]
        assert qtail.count(pre) == 1 and qtail.count(b"___") == 1
        # every block matches the frozen format reconstructed from meta spans
        slo, shi = m["source_span"]
        alo, ahi = m["source_answer_span"]
        assert row[slo:shi] and row[alo:ahi] == m["answer_b"]
        assert qtail == s1._retrieval_qa_block(
            row[slo:shi], alo - slo, ahi - slo, m["answer_b"]
        )
        ex_spans = []
        for i, ex in enumerate(m["examples"]):
            blk = _example_block(row, n_orig, m["examples"], i)
            xlo, xhi = ex["echo_span"]
            assert blk.endswith(prompt + ex["answer_b"])  # 示例答案可见
            assert row[xlo:xhi] == ex["answer_b"]
            xs, xe = ex["source_span"]
            assert row[ex["source_answer_span"][0] : ex["source_answer_span"][1]] == ex["answer_b"]
            assert blk == s1._retrieval_qa_block(
                row[xs:xe],
                ex["source_answer_span"][0] - xs,
                ex["source_answer_span"][1] - xs,
                ex["answer_b"],
            )
            assert blk.count(b"___") == 1
            ex_spans.append((xs, xe))
            # 反捷径条款 (Q12.2): 查询答案不得出现在任何示例中 (字节级子串)
            assert m["answer_b"] not in blk
            # 示例来源段 ≠ 查询来源段 (span AND content)
            assert (xs, xe) != (slo, shi)
            assert row[xs:xe] != row[slo:shi]
        assert len(set(ex_spans)) == len(ex_spans)


def test_examples_role_randomization_query_not_always_first():
    """角色随机化: over seeds the query is not always the first-drawn item --
    observable via the query source span varying among the drawn spans."""
    clean = _clean([TEXT1], 384)
    seen = set()
    for seed in range(12):
        _, metas = s1._splice_retrieval(clean, 1.0, torch.Generator().manual_seed(seed), "cjk", 2, 10**6)
        m = metas[0]
        if m is None:
            continue
        order = tuple(ex["source_span"] for ex in m["examples"])
        seen.add(order)
    assert len(seen) > 1  # draws/roles actually vary


# --- 3. 反捷径条款: many-seed property + 注入冲突 --------------------------------


def test_anti_shortcut_property_many_seeds():
    clean = _clean([TEXT1, TEXT2], 384)
    pre = "\n前文'".encode("utf-8")
    for seed in range(16):
        out, metas = s1._splice_retrieval(clean, 1.0, torch.Generator().manual_seed(seed), "cjk", 4, 10**6)
        for b, m in enumerate(metas):
            if m is None:
                continue
            row = _row_bytes(out[b])
            n_orig = _n_valid(clean[b])
            qs, qe = m["source_span"]
            for i, ex in enumerate(m["examples"]):
                blk = _example_block(row, n_orig, m["examples"], i)
                assert m["answer_b"] not in blk  # 查询答案不出现在示例中
                assert ex["source_span"] != (qs, qe)
                xs, xe = ex["source_span"]
                assert row[xs:xe] != row[qs:qe]


def test_anti_shortcut_conflict_window_never_activates():
    """注入恒冲突样本: 全 '天' 窗口 -- 任何 2–4 字答案都是 '天' 的重复, 必然
    出现在任何示例块的残留 '天' 串里 (每块至少留 14 个连续 '天'), 反捷径条款
    逐 attempt 违反 -> 重抽 N=8 仍违反 -> 样本不激活, 行逐字节不变."""
    raw = "天".encode("utf-8") * 200
    clean = _clean([raw], 200)
    for seed in range(4):
        out, metas = s1._splice_retrieval(clean, 1.0, torch.Generator().manual_seed(seed), "cjk", 2, 10**6)
        assert metas == [None]
        assert torch.equal(out, clean)


# --- 4. 窗口预算 (A2②) -----------------------------------------------------------


def _block_lens(row: bytes, n_orig: int, m: dict) -> tuple[list[int], int]:
    """Per-example block lengths and the query block length of a spliced row."""
    lens = []
    start = n_orig
    for ex in m["examples"]:
        end = ex["echo_span"][1]
        lens.append(end - start)
        start = end
    return lens, len(row) - m["query_start"]


def test_budget_drops_earliest_examples_first():
    clean = _clean([TEXT1], 384)
    n_orig = _n_valid(clean[0])
    seed = 13
    out_full, metas_full = s1._splice_retrieval(
        clean, 1.0, torch.Generator().manual_seed(seed), "cjk", 3, 10**6
    )
    m_full = metas_full[0]
    assert m_full["n_examples"] == 3
    row_full = _row_bytes(out_full[0])
    ex_lens, q_len = _block_lens(row_full, n_orig, m_full)

    # capacity fits exactly the LAST two examples + query: earliest dropped
    cap2 = n_orig + ex_lens[1] + ex_lens[2] + q_len
    out2, metas2 = s1._splice_retrieval(clean, 1.0, torch.Generator().manual_seed(seed), "cjk", 3, cap2)
    m2 = metas2[0]
    assert m2["n_examples"] == 2 and m2["n_dropped"] == 1
    # the drop consumes no RNG: same seed -> same draws -> the retained
    # examples are exactly the full run's last two, query identical
    assert [ex["answer_b"] for ex in m2["examples"]] == [ex["answer_b"] for ex in m_full["examples"][1:]]
    assert [ex["source_span"] for ex in m2["examples"]] == [ex["source_span"] for ex in m_full["examples"][1:]]
    assert m2["answer_b"] == m_full["answer_b"]
    assert m2["source_span"] == m_full["source_span"]
    row2 = _row_bytes(out2[0])
    assert m2["budget_ratio"] == pytest.approx(len(row2) / cap2)
    assert len(row2) <= cap2

    # capacity fits the query only: all examples dropped, query NEVER truncated
    cap0 = n_orig + q_len
    out0, metas0 = s1._splice_retrieval(clean, 1.0, torch.Generator().manual_seed(seed), "cjk", 3, cap0)
    m0 = metas0[0]
    assert m0["n_examples"] == 0 and m0["n_dropped"] == 3
    assert m0["examples"] == []
    row0 = _row_bytes(out0[0])
    elo, ehi = m0["echo_span"]
    assert ehi == len(row0) and row0[elo:ehi] == m_full["answer_b"]  # 查询段完整
    assert m0["query_start"] == n_orig

    # capacity below even the query: source/query still untruncated; the
    # over-budget sample is spliced and left to the grid-edge defect count
    outx, metasx = s1._splice_retrieval(clean, 1.0, torch.Generator().manual_seed(seed), "cjk", 3, 64)
    mx = metasx[0]
    assert mx["n_dropped"] == 3 and mx["budget_ratio"] > 1.0
    rowx = _row_bytes(outx[0])
    assert rowx[mx["echo_span"][0] : mx["echo_span"][1]] == m_full["answer_b"]


def test_budget_metrics_flow_to_step_model():
    """溢出丢弃率与占用比入指标: tiny grid capacity forces drops; means are
    taken over spliced samples only."""
    torch.manual_seed(0)
    cfg = tiny_config(max_chunks=64, max_span=32, bytes_per_chunk=16, max_positions=64)
    model = FLUEDV36(cfg)
    args = _s1_args(
        retrieval_prob=1.0, retrieval_weight=1.0, retrieval_block_prob=0.0,
        retrieval_examples=4, mask_prob=0.1, max_chunks=64, max_span=32,
    )
    batch = (_clean([TEXT1, TEXT2], 384),)
    s1._RETRIEVAL_GENERATOR.manual_seed(42 + s1._RETRIEVAL_SEED_OFFSET)
    loss, metrics = s1.step_model(model, batch, args, torch.device("cpu"), train=False)
    assert torch.isfinite(loss)
    # grid capacity 64*32=2048B: window 384 + 4 examples + query fits, no drops
    assert metrics["retrieval_examples"].item() == 4.0
    assert metrics["retrieval_drop_rate"].item() == 0.0
    assert 0.0 < metrics["retrieval_budget_ratio"].item() < 1.0
    assert metrics["retrieval_count"].item() == 1.0
    assert metrics["retrieval_defect"].item() == 0.0


def test_query_pushed_off_grid_is_defect_and_discarded():
    """查询段因果可见性断言: 网格容量装不下查询段 -> echo 落不上网格 ->
    样本弃用 (retrieval_count=0) 且构造缺陷计数 retrieval_defect=1."""
    torch.manual_seed(0)
    cfg = tiny_config()  # 4 chunks x 8 slots = 32B grid: the tail never packs
    model = FLUEDV36(cfg)
    args = _s1_args(
        retrieval_prob=1.0, retrieval_weight=1.0, retrieval_examples=2, mask_prob=0.1,
    )
    batch = (_clean([TEXT1, TEXT2], 384),)
    s1._RETRIEVAL_GENERATOR.manual_seed(42 + s1._RETRIEVAL_SEED_OFFSET)
    loss, metrics = s1.step_model(model, batch, args, torch.device("cpu"), train=False)
    assert torch.isfinite(loss)
    assert metrics["retrieval_count"].item() == 0.0  # 样本弃用
    assert metrics["retrieval_defect"].item() == 1.0  # 构造缺陷计数
    assert metrics["retrieval_loss"].item() == 0.0  # no active echo slots


# --- 5. mask overrides: 示例答案可见 / 查询 echo 全遮 -----------------------------


def test_mask_overrides_examples_visible_query_masked():
    clean = _clean([TEXT1], 384)
    out, metas = s1._splice_retrieval(clean, 1.0, torch.Generator().manual_seed(3), "cjk", 3, 10**6)
    m = metas[0]
    byte_mask = torch.ones_like(out, dtype=torch.bool)  # the regular mask hides EVERYTHING
    after = s1._retrieval_mask_overrides(byte_mask.clone(), metas)
    elo, ehi = m["echo_span"]
    assert after[0, elo:ehi].all()  # 查询 echo 全遮
    alo, ahi = m["source_answer_span"]
    assert not after[0, alo:ahi].any()  # 查询来源段答案词 force-unmask
    for ex in m["examples"]:
        xlo, xhi = ex["echo_span"]
        assert not after[0, xlo:xhi].any()  # 示例答案可见 (不遮)
        # 示例其余部分 (含来源段答案词) 保持常规掩码 -- 这里常规掩码是全 True
        xs, xe = ex["source_answer_span"]
        assert after[0, xs:xe].all()
    # and the encoded source really shows MASK_ID at the query echo only
    source = out.masked_fill(after, MASK_ID)
    assert (source[0, elo:ehi] == MASK_ID).all()
    for ex in m["examples"]:
        xlo, xhi = ex["echo_span"]
        assert (source[0, xlo:xhi] != MASK_ID).all()


# --- 6. store_block: 只剔查询来源 chunk, 示例 store 行不动 ------------------------


def test_store_block_excises_query_source_only():
    chunk_ids = torch.tensor([[0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3]])
    chunks = _fake_chunks(chunk_ids, 4)
    metas = [
        {
            "source_span": (6, 9),  # 查询来源段 -> chunk 2
            "query_start": 9,
            "echo_span": (10, 12),
            "examples": [  # 示例来源段 -> chunks 0/1: store 行不得剔除
                {"source_span": (0, 3), "source_answer_span": (0, 2), "echo_span": (9, 10), "answer_b": b"ab"},
                {"source_span": (3, 6), "source_answer_span": (3, 5), "echo_span": (9, 10), "answer_b": b"cd"},
            ],
        }
    ]
    block, rate = s1._retrieval_store_block(metas, chunks, 1.0, torch.Generator().manual_seed(1))
    assert rate == 1.0
    expect = torch.zeros(1, 4, 4, dtype=torch.bool)
    expect[0, 3:, 2] = True  # >= 问句首 chunk (3) 的 query 剔除查询来源 chunk 2
    assert torch.equal(block, expect)
    assert not block[:, :, 0].any() and not block[:, :, 1].any()  # 示例脚手架必须可读


# --- 7. e2e: finite loss + 指标 + 梯度 -------------------------------------------


def test_step_model_examples_finite_and_metrics():
    torch.manual_seed(0)
    cfg = tiny_config(max_chunks=64, max_span=32, bytes_per_chunk=16, max_positions=64)
    model = FLUEDV36(cfg)
    args = _s1_args(
        retrieval_prob=1.0, retrieval_weight=1.0, retrieval_block_prob=1.0,
        retrieval_examples=3, mask_prob=0.1, max_chunks=64, max_span=32,
    )
    batch = (_clean([TEXT1, TEXT2], 384),)
    s1._RETRIEVAL_GENERATOR.manual_seed(42 + s1._RETRIEVAL_SEED_OFFSET)
    loss, metrics = s1.step_model(model, batch, args, torch.device("cpu"), train=True)
    assert torch.isfinite(loss)
    for key in (
        "retrieval_loss", "retrieval_byte_acc", "retrieval_exact", "retrieval_count",
        "retrieval_block_rate", "retrieval_budget_ratio", "retrieval_examples",
        "retrieval_drop_rate", "retrieval_defect",
    ):
        assert key in metrics, key
        assert torch.isfinite(metrics[key]), key
    assert metrics["retrieval_count"].item() == 1.0
    assert metrics["retrieval_block_rate"].item() == 1.0
    assert metrics["retrieval_examples"].item() == 3.0
    assert 0.0 < metrics["retrieval_budget_ratio"].item() < 1.0
    assert metrics["retrieval_loss"].item() > 0.0
    loss.backward()
    assert model.backbone.align_k.weight.grad is not None
    assert model.backbone.align_k.weight.grad.abs().sum() > 0


# --- 8. determinism -----------------------------------------------------------------


def test_examples_splice_deterministic_same_seed():
    clean = _clean([TEXT1, TEXT2], 384)
    out1, metas1 = s1._splice_retrieval(clean, 1.0, torch.Generator().manual_seed(7), "cjk", 3, 10**6)
    out2, metas2 = s1._splice_retrieval(clean, 1.0, torch.Generator().manual_seed(7), "cjk", 3, 10**6)
    assert torch.equal(out1, out2)
    assert metas1 == metas2
    out3, metas3 = s1._splice_retrieval(clean, 1.0, torch.Generator().manual_seed(8), "cjk", 3, 10**6)
    assert not torch.equal(out1, out3) or metas1 != metas3  # non-vacuous


# --- 9. 响亮报错 ---------------------------------------------------------------------


def test_check_retrieval_args_examples_loud():
    base = _s1_args(retrieval_prob=0.5)
    base.backbone_mode = "slm"
    base.retrieval_examples = 1
    with pytest.raises(SystemExit, match="retrieval-examples"):
        s1._check_retrieval_args(base)
    base.retrieval_examples = 5
    with pytest.raises(SystemExit, match="retrieval-examples"):
        s1._check_retrieval_args(base)
    base = _s1_args()  # examples>0 without a live retrieval task
    base.retrieval_examples = 2
    with pytest.raises(SystemExit, match="retrieval-prob"):
        s1._check_retrieval_args(base)
    ok = _s1_args(retrieval_prob=0.5, retrieval_examples=4, retrieval_block_prob=1.0)
    ok.backbone_mode = "slm"
    s1._check_retrieval_args(ok)
    ok0 = _s1_args(retrieval_prob=0.5, retrieval_examples=0)
    ok0.backbone_mode = "slm"
    s1._check_retrieval_args(ok0)
