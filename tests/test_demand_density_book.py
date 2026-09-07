"""甲形态密度账合成测试（口径钉死：跨 chunk 重复 + 稀有过滤 + 尾长计数）。"""
import random

from tools.analysis.v3_6.demand_density_book import (
    CHUNK, count_supervised_positions, collect_candidates)

GRAM = b"\x01\x02\x03\x04"


def _window_with_repeat() -> bytes:
    # 伪随机底（意外 4-gram 碰撞概率 ~3e-5），在 chunk 0 与 chunk 4 各植一次稀有 gram。
    w = bytearray(random.Random(7).randbytes(512))
    w[0:4] = GRAM        # chunk 0 首次
    w[64:68] = GRAM      # chunk 4 二次出现（跨 chunk）
    return bytes(w)


def test_cross_chunk_repeat_counts_tail():
    w = _window_with_repeat()
    # L=4, T=3：命中位置 = 二次出现处起的 3 个字节（68,69,70）
    n, grams = count_supervised_positions(w, 4, 3, {GRAM})
    assert n == 3
    assert grams == {GRAM}


def test_same_chunk_repeat_not_counted():
    w = bytearray(_window_with_repeat())
    w[64:68] = b"\xff\xfe\xfd\xfc"  # 抹掉跨 chunk 重复
    w[8:12] = GRAM                  # 同 chunk(0) 内重复——不算
    n, _ = count_supervised_positions(bytes(w), 4, 3, {GRAM})
    assert n == 0


def test_rarity_filter_excludes_unlisted_gram():
    w = _window_with_repeat()
    n, _ = count_supervised_positions(w, 4, 3, set())  # 稀有集为空 → 全滤掉
    assert n == 0
    n2, _ = count_supervised_positions(w, 4, 3, None)  # 不过滤（候选收集形态）
    assert n2 == 3


def test_collect_candidates_finds_repeat():
    cand = collect_candidates([_window_with_repeat()], 4)
    assert GRAM in cand


def test_chunk_constant():
    assert CHUNK == 16
