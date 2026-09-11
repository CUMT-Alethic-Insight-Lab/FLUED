"""E124 旗标互斥校验 CLI 回归网（坑 8 家族护栏，红队补测 2026-09-11）。

train_v36_s1.main() 的 e124 响亮校验段（tools/train/v3_6/train_v36_s1.py
`--e124-budget-gate` 块：slm 限定 / a 格限定 / batch=1 / k_block_eval 互斥 /
历史臂互斥循环 / --init-checkpoint 必带 / 退火窗 (0,1]）此前零测试覆盖。本网
参数化枚举各互斥组合，经**子进程真 CLI** 点火（校验段全部位于数据装载与基座
审计之前，秒级退出），断言：exit≠0（SystemExit）∧ stderr 非空 ∧ stderr 含预期
护栏指纹。指纹逐项对应真实校验位置，含三枚**被前置护栏遮蔽**的组合（见下
「代码事实」）。

代码事实（2026-09-11 施工核实，入档防误判）：
  e124 mutex 循环里的 Q18 / Q15 主开关 / Q20 多槽读出 / E120 读出替换四个臂名
  经 CLI **不可达**——四臂各自的响亮校验在 e124 段之前先 exit（Q18 需要
  q18-base-ckpt；Q15 主开关要 d 格；Q20 要 b 格；E120 要 d 格），而格别约束与
  e124 的 a 格前提结构性不相容。故这四枚按真实可达枚举为「前置护栏指纹」，
  e124 循环内的互斥拒绝对其余七臂（k_block_eval/denoise/burst/retrieval/
  cloze/D1/q15-attn-diag/decoder-markov）全部可达且逐枚钉死。

对照锚（control）：裸 e124 合法姿态 + 假基座 → **不**含 e124 互斥指纹地死在
下游（基座审计 torch.load），证明基线姿态不被互斥网误拒（false-reject 护栏）。
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[1]
TRAINER = REPO / "tools" / "train" / "v3_6" / "train_v36_s1.py"

# 裸 e124 合法姿态（a 格 + batch 1 + 假基座占位 + 退火窗合法）：
# 校验段只看旗标值不读基座文件（审计在校验段之后），dummy 即可过闸。
BASE = [
    "--e124-budget-gate",
    "--backbone-mode", "slm",
    "--k-row-source", "index",
    "--v-row-source", "memory",
    "--batch-size", "1",
    "--init-checkpoint", "dummy",
    "--e124-gate-anneal-frac", "0.4",
]


def _run_cli(extra: list[str], base: list[str] | None = None) -> subprocess.CompletedProcess:
    cmd = [sys.executable, "-X", "utf8", str(TRAINER), *(base or BASE), *extra]
    return subprocess.run(
        cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=str(REPO), timeout=180,
        env={**os.environ, "PYTHONUTF8": "1"},
    )


def _cloze_bank(tmp_path: Path) -> str:
    # tools/data/mine_cloze_bank.py 契约：passage 96-192B / answer 28-36B /
    # query = passage 把 answer 换成恰一个 ___
    answer = "a" * 28
    passage = "p" * 34 + answer + "q" * 34  # 96B
    query = "p" * 34 + "___" + "q" * 34
    p = tmp_path / "cloze_bank.jsonl"
    p.write_text(json.dumps(
        {"id": 0, "passage": passage, "answer": answer, "query": query, "answer_bytes": 28},
    ) + "\n", encoding="utf-8")
    return str(p)


def _d1_rare_table(tmp_path: Path) -> str:
    # build_d1_rare_table.py 主形态：(N, L) uint8 grams + int64 counts
    p = tmp_path / "rare_table.npz"
    np.savez(p, grams=np.array([[1, 2, 3, 4], [5, 6, 7, 8]], dtype=np.uint8),
             counts=np.array([5, 7], dtype=np.int64))
    return str(p)


@pytest.mark.parametrize(
    "extra,expect",
    [
        pytest.param(["--k-block-eval"], "不组合 --k-block-eval",
                     id="k_block_eval"),
        pytest.param(["--k-row-source", "state"], "requires slm a 格", id="grid_k_state"),
        pytest.param(["--v-row-source", "state"], "requires slm a 格", id="grid_v_state"),
        pytest.param(["--batch-size", "2"], "requires batch_size=1", id="batch2"),
        pytest.param(["--e124-gate-anneal-frac", "1.5"], "须在 (0, 1]", id="anneal_frac_gt1"),
        pytest.param(["--e124-gate-anneal-frac", "0.0"], "须在 (0, 1]", id="anneal_frac_zero"),
        pytest.param(["--decoder-denoise", "--decoder-denoise-fuzz-id", "dummy"],
                     "不组合 decoder 去噪", id="mutex_denoise"),
        pytest.param(["--burst-prob", "0.5"], "不组合 burst", id="mutex_burst"),
        pytest.param(["--retrieval-prob", "0.5"], "不组合 retrieval", id="mutex_retrieval"),
        pytest.param(["--q15-attn-diag", "--burst-prob", "0.5"],
                     "不组合 q15-attn-diag", id="mutex_q15_attn_diag"),
        pytest.param(["--decoder-markov", "2"], "不组合 decoder-markov", id="mutex_decoder_markov"),
        pytest.param(["--e120-readout-swap"], "--e120-readout-swap requires",
                     id="mutex_e120_shadowed_by_d_grid_guard"),
        pytest.param(["--multislot-readout"], "--multislot-readout requires",
                     id="mutex_q20_shadowed_by_b_grid_guard"),
        pytest.param(["--q18-arm", "A"], "--q18-arm 需要 --q18-base-ckpt",
                     id="mutex_q18_shadowed_by_q18_guard"),
    ],
)
def test_e124_mutex_combos_exit_loud(extra: list[str], expect: str):
    r = _run_cli(extra)
    assert r.returncode != 0, f"应 SystemExit，实得 exit=0\nstdout={r.stdout[-800:]}"
    assert r.stderr.strip(), "stderr 应非空（响亮拒绝）"
    assert expect in r.stderr, f"护栏指纹 {expect!r} 缺席\nstderr={r.stderr[-800:]}"


def test_e124_mutex_cloze_combos_exit_loud(tmp_path):
    r = _run_cli(["--cloze-prob", "0.5", "--cloze-bank", _cloze_bank(tmp_path)])
    assert r.returncode != 0 and r.stderr.strip()
    assert "不组合 cloze" in r.stderr, r.stderr[-800:]


def test_e124_mutex_d1_combos_exit_loud(tmp_path):
    r = _run_cli(["--d1-tail-rewire", "--d1-rare-table", _d1_rare_table(tmp_path)])
    assert r.returncode != 0 and r.stderr.strip()
    assert "不组合 D1" in r.stderr, r.stderr[-800:]


def test_e124_baseline_posture_not_false_rejected():
    """对照锚：裸 e124 姿态过互斥网，死在下游基座审计（假基座 torch.load 失败）
    ——互斥网无误拒（护栏只拦真互斥组合，不拦合法基线）。"""
    r = _run_cli([])
    assert r.returncode != 0 and r.stderr.strip()
    assert "不组合" not in r.stderr, f"基线姿态被互斥网误拒:\n{r.stderr[-800:]}"
