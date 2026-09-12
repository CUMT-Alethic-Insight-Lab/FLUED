"""门② 距离分档 CI 补算测试（协议同构钉死）。

核心断言：本脚本的每格 bootstrap 必须与门②仪器实际调用的
bootstrap_contrast（boot_in 投影形：sel_d_b1 = d̄_w·n_w，ctl≡0）在相同
seed 下逐位相等——点估、CI、n_boot_valid 三者全同构才算过。
"""
from __future__ import annotations

import json
import random

import pytest

import tools.analysis.v3_6.bucket_ci_gate2_necessity as bci
import tools.analysis.v3_6.probe_e122_necessity_book as e122


def _synth_items() -> list[dict]:
    """6 窗合成 items：距离覆盖 1/2/3..8，d_total 手工定值便于手算。"""
    rows = []
    for wi in range(6):
        rng = random.Random(100 + wi)
        for k in range(3):
            d = 1 + (k % 8)          # 距离 1..8 循环
            rows.append({
                "window_id": wi,
                "chunk": k,
                "sink_chunk": k + d,
                "distance": d,
                "byte_pos": rng.randrange(4096),
                "block_baseline_surprisal": 1.0,
                "d_direct": 0.5,
                "d_backbone": 0.5,
                "d_total": 0.01 * (wi + 1) + 0.001 * k + 0.0001 * d,
            })
    return rows


def _write_items(path, rows) -> None:
    path.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")


def _gate_boot_in(agg: dict, windows: list[int], bucket: str) -> list[dict]:
    """门②仪器 run_gate_window→main 的投影形（gate_e123_necessity_v2.py:236）：
    sel_d_b1 = d̄_w·n_w（窗均值回程，与门② sums["d_total"]/n 的构造逐位同）。"""
    out = []
    for wi in windows:
        n, s = agg.get((wi, bucket), (0, 0.0))
        out.append({"n_sel": n, "sel_d_b1": (s / n) * n if n else 0.0,
                    "n_ctl": n, "ctl_d_b1": 0.0})
    return out


def test_bucket_rule():
    assert bci.bucket_of(1) == "d1"
    assert bci.bucket_of(2) == "d2"
    for d in range(3, 9):
        assert bci.bucket_of(d) == "dge3"
    assert bci.bucket_of(0) is None
    assert bci.bucket_of(9) is None      # SCORE_DIST=8 域外


def test_cell_isomorphic_to_gate_bootstrap_contrast(tmp_path):
    """每格 vs 仪器 bootstrap_contrast：同 seed 下 point/CI/valid 逐位相等。"""
    rows = _synth_items()
    path = tmp_path / "items.jsonl"
    _write_items(path, rows)
    scan = bci.scan_items(path)
    windows = scan["windows"]
    for bucket in bci.BUCKETS:
        cell = bci.bucket_cell(scan["agg"], windows, bucket, n_boot=300, seed=43)
        boot = e122.bootstrap_contrast(
            _gate_boot_in(scan["agg"], windows, bucket), n_boot=300, seed=43)
        assert cell["point_pooled"] == pytest.approx(boot["point"], abs=0.0)
        assert cell["ci95_lo"] == pytest.approx(boot["ci95_lo"], abs=0.0)
        assert cell["ci95_hi"] == pytest.approx(boot["ci95_hi"], abs=0.0)
        assert cell["n_boot_valid"] == boot["n_boot_valid"]
        # 池化点估 = Σsum/Σn 手算复核
        n_tot = sum(scan["agg"].get((w, bucket), (0, 0.0))[0] for w in windows)
        s_tot = sum(scan["agg"].get((w, bucket), (0, 0.0))[1] for w in windows)
        assert cell["point_pooled"] == pytest.approx(s_tot / n_tot, abs=1e-15)
        assert cell["n"] == n_tot


def test_bootstrap_seed_determinism_and_sensitivity(tmp_path):
    path = tmp_path / "items.jsonl"
    _write_items(path, _synth_items())
    scan = bci.scan_items(path)
    a = bci.bucket_cell(scan["agg"], scan["windows"], "d2", n_boot=200, seed=43)
    b = bci.bucket_cell(scan["agg"], scan["windows"], "d2", n_boot=200, seed=43)
    c = bci.bucket_cell(scan["agg"], scan["windows"], "d2", n_boot=200, seed=44)
    assert (a["ci95_lo"], a["ci95_hi"]) == (b["ci95_lo"], b["ci95_hi"])
    assert (a["ci95_lo"], a["ci95_hi"]) != (c["ci95_lo"], c["ci95_hi"])


def test_invalid_resample_skipped_not_zero_filled(tmp_path):
    """仅 1/3 窗含该档 → 必有重采样全落空窗 → n_boot_valid < n_boot
    （与 bootstrap_contrast 的 None 跳过同，不得当 0 填充）。"""
    rows = [{"window_id": 0, "chunk": 0, "sink_chunk": 1, "distance": 1,
             "byte_pos": 0, "block_baseline_surprisal": 0.0,
             "d_direct": 0.1, "d_backbone": 0.1, "d_total": 0.1}]
    for wi in (1, 2):
        rows.append({"window_id": wi, "chunk": 0, "sink_chunk": 2,
                     "distance": 2, "byte_pos": 0,
                     "block_baseline_surprisal": 0.0,
                     "d_direct": 0.0, "d_backbone": 0.0, "d_total": 0.0})
    path = tmp_path / "items.jsonl"
    _write_items(path, rows)
    scan = bci.scan_items(path)
    cell = bci.bucket_cell(scan["agg"], scan["windows"], "d1", n_boot=400, seed=43)
    assert 0 < cell["n_boot_valid"] < 400
    gate = e122.bootstrap_contrast(
        _gate_boot_in(scan["agg"], scan["windows"], "d1"), n_boot=400, seed=43)
    assert cell["n_boot_valid"] == gate["n_boot_valid"]


def test_empty_bucket_none_not_crash(tmp_path):
    rows = _synth_items()
    for r in rows:
        r["distance"] = 1
        r["sink_chunk"] = r["chunk"] + 1
    path = tmp_path / "items.jsonl"
    _write_items(path, rows)
    scan = bci.scan_items(path)
    cell = bci.bucket_cell(scan["agg"], scan["windows"], "d2", n_boot=50, seed=43)
    assert cell["n"] == 0
    assert cell["point_pooled"] is None
    assert cell["ci95_lo"] is None and cell["ci95_hi"] is None


def test_window_mean_form_diverges_from_pooled(tmp_path):
    """窗均形态（无权平均窗均值）与池化形态在手造不等权数据上必然分叉。"""
    rows = [
        {"window_id": 0, "chunk": 0, "sink_chunk": 1, "distance": 1,
         "byte_pos": 0, "block_baseline_surprisal": 0.0,
         "d_direct": 1.0, "d_backbone": 1.0, "d_total": 1.0},
        {"window_id": 1, "chunk": 0, "sink_chunk": 1, "distance": 1,
         "byte_pos": 0, "block_baseline_surprisal": 0.0,
         "d_direct": 0.0, "d_backbone": 0.0, "d_total": 0.0},
        {"window_id": 1, "chunk": 1, "sink_chunk": 2, "distance": 1,
         "byte_pos": 1, "block_baseline_surprisal": 0.0,
         "d_direct": 0.0, "d_backbone": 0.0, "d_total": 0.0},
    ]
    path = tmp_path / "items.jsonl"
    _write_items(path, rows)
    scan = bci.scan_items(path)
    cell = bci.bucket_cell(scan["agg"], scan["windows"], "d1", n_boot=10, seed=43)
    assert cell["point_pooled"] == pytest.approx(1 / 3)
    assert cell["point_window_mean"] == pytest.approx(0.5)


def test_analyze_items_total_check_against_summary(tmp_path):
    """端到端：items + summary.json（用仪器自身代码算出 point/mean_d_total）
    → analyze_items 的 total_check 两个偏差都必须 ≈ 0。"""
    rows = _synth_items()
    path = tmp_path / "items.jsonl"
    _write_items(path, rows)
    # 用门②自身聚合路径造 summary 读数
    per_win: dict[int, dict] = {}
    for r in rows:
        w = per_win.setdefault(r["window_id"], {"n": 0, "d_total": 0.0})
        w["n"] += 1
        w["d_total"] += r["d_total"]
    window_sums = []
    for wi in sorted(per_win):
        w = per_win[wi]
        window_sums.append({"n": w["n"], "d_total": w["d_total"] / w["n"]})
    boot_in = [{"n_sel": w["n"], "sel_d_b1": w["d_total"] * w["n"],
                "n_ctl": w["n"], "ctl_d_b1": 0.0} for w in window_sums]
    boot = e122.bootstrap_contrast(boot_in, n_boot=1, seed=43)
    mean_d_total = sum(w["d_total"] for w in window_sums) / len(window_sums)
    (tmp_path / "summary.json").write_text(json.dumps(
        {"results": {"mean_d_total": mean_d_total, "bootstrap": boot}}),
        encoding="utf-8")

    run = bci.analyze_items("synth", path, n_boot=50, seed=43)
    chk = run["total_check"]
    assert chk["abs_diff_pooled_vs_summary_point"] < 1e-9
    assert chk["wmean_round5_vs_summary"] == pytest.approx(mean_d_total, abs=5e-6)
    assert run["n_positions"] == len(rows)
    assert run["unexpected_distances"] == {}
