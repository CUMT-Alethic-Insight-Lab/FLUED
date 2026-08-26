"""任务书 FLUED_V3_7_LR_SCALE_2X2_20260826_CN (2026-08-26 冻结) 点火前检查测试:

- _window_burstiness 12-gram 覆盖率合成判例 (全唯一 -> 0; 半窗重复 -> 1.0;
  四分之一窗重复 -> 0.5; 短窗 -> 0);
- RNG 重放保真 (仪表命根子): replay_offsets 前 5 窗与
  StreamingReconstructionDataset 真实迭代逐比特一致 (含行首吸附 /
  UTF-8 边界微调 / 短读 continue 三段逻辑);
- 训练日志接线: main 循环 log row 含 data_burstiness 键, 且走
  _batch_data_burstiness 同一代码路径 (有效前缀口径).
"""

import mmap
import random
import re

import torch

from flued.data import BYTE_OFFSET, PAD_ID, StreamingReconstructionDataset
from tools.analysis.v3_6.measure_stream_burstiness import replay_offsets
from tools.train.v3_6 import train_v36_s1
from tools.train.v3_6.train_v36_s1 import _batch_data_burstiness, _window_burstiness

GRAM = 12


def _unique_gram_bytes(n: int, seed: int = 1234) -> bytes:
    """n 字节伪随机序列, 前置断言全部 12-gram 唯一 (固定 seed -> 确定性)."""
    w = random.Random(seed).randbytes(n)
    grams = [w[i : i + GRAM] for i in range(n - GRAM + 1)]
    assert len(set(grams)) == len(grams), "precondition: all 12-grams unique"
    return w


def test_window_burstiness_all_unique_zero():
    assert _window_burstiness(_unique_gram_bytes(4096)) == 0.0


def test_window_burstiness_short_window_zero():
    assert _window_burstiness(b"") == 0.0
    assert _window_burstiness(b"hello world") == 0.0  # 11 < 12
    assert _window_burstiness(b"hello world!") >= 0.0  # 恰 12B 不崩


def test_window_burstiness_half_duplicated_full_coverage():
    # 前半 A (2048B, gram 全唯一) 重复两次 -> A 区每个 12-gram 出现 >=2 次,
    # 首尾两副本的覆盖区间并集 = 全窗 -> 1.0
    a = _unique_gram_bytes(2048, seed=7)
    w = a + a
    assert _window_burstiness(w) == 1.0


def test_window_burstiness_quarter_duplicated():
    # A+A+X, |A|=1024 (gram 全唯一), |X|=2048 唯一 -> 重复 gram 覆盖
    # [0,2048) = 半个窗 -> 0.5; 前置断言 X 与接缝 gram 不引入额外重复
    a = _unique_gram_bytes(1024, seed=11)
    x = _unique_gram_bytes(2048, seed=13)
    w = a + a + x
    grams = [w[i : i + GRAM] for i in range(len(w) - GRAM + 1)]
    from collections import Counter

    dup = {g for g, c in Counter(grams).items() if c >= 2}
    # 前置: 重复 gram 只允许来自 A 内部 (位置 < 1024-GRAM+1 的 gram)
    a_grams = {a[i : i + GRAM] for i in range(len(a) - GRAM + 1)}
    assert dup <= a_grams, "precondition: no accidental repeats outside A"
    assert _window_burstiness(w) == 0.5


def test_replay_offsets_match_streaming_dataset(tmp_path):
    # 语料含多行 + CJK 多字节 (触发 UTF-8 微调) + 足够长度
    rng = random.Random(20260826)
    lines = []
    for i in range(400):
        lines.append(f"第{i}行: 边界压缩回路催生 τ={rng.random():.6f} " + "x" * rng.randint(0, 40))
    corpus = "\n".join(lines).encode("utf-8")
    fpath = tmp_path / "corpus.txt"
    fpath.write_bytes(corpus)

    seq_len = 64
    n = 5
    ds = StreamingReconstructionDataset(str(fpath), seq_len=seq_len, samples_per_worker=n, seed=42)
    real = []
    for src, _tgt in ds:
        real.append(bytes((src - BYTE_OFFSET).to(torch.uint8).numpy().tobytes()))
    assert len(real) == n

    offsets = replay_offsets(str(fpath), seq_len, n, seed=42, samples_per_worker=n)
    assert len(offsets) == n
    with open(fpath, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        for k, st in enumerate(offsets):
            assert bytes(mm[st : st + seq_len]) == real[k], f"window {k} mismatch"


def test_batch_data_burstiness_valid_prefix_only():
    # row0: 全唯一有效前缀 + PAD 尾 -> 0.0; row1: 半窗重复 + PAD 尾 -> 1.0
    a = _unique_gram_bytes(512, seed=17)
    b = _unique_gram_bytes(256, seed=19)
    row0 = torch.cat([torch.tensor([x + BYTE_OFFSET for x in a]), torch.zeros(64, dtype=torch.long)])
    row1 = torch.cat([torch.tensor([x + BYTE_OFFSET for x in (b + b)]), torch.zeros(64, dtype=torch.long)])
    batch = torch.stack([row0, row1])
    assert _batch_data_burstiness(batch) == 0.5
    # 全 PAD 行不崩
    assert _batch_data_burstiness(torch.zeros(1, 32, dtype=torch.long)) == 0.0


def test_train_log_row_wires_data_burstiness():
    # 接线守卫: main 循环 log row 必须经 _batch_data_burstiness 落
    # data_burstiness 键 (无条件常开, 任务书 §1)
    src = (train_v36_s1.__file__ and open(train_v36_s1.__file__, encoding="utf-8").read())
    assert '"data_burstiness": _batch_data_burstiness(batch[0])' in src
    assert re.search(r"if step % args\.log_every == 0 or step == 1:[\s\S]{0,1200}?data_burstiness", src)
