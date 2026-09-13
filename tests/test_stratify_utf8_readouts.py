"""UTF-8 位置分解审计仪器单测（stratify_utf8_readouts.py, 2026-09-13 用户
审计单 1 的分析件; 消费三件探针 --dump-* 落盘的同源 npz）。

Covers: (1) 目标 id → 位置类分类的边界字节（0x7F/0x80/0xBF/0xC0 + PAD/
MASK_ID）; (2) 类内 Top-1 地板 = 边际最大份额; (3) stratify_records 合成流
端到端精确对表（n/份额/acc/地板/超地板/混合合成一致性 composition_check/
窗均值/折均值/pad 缺席上报）; (4) 网格 npz 装载（as-encoded 主口径含 mask
echo 槽 + true_view 真字节路径的 fallback 键名）; (5) E73 折均值路径。
纯 numpy 合成数据, 不碰语料不碰模型。
"""

from __future__ import annotations

import numpy as np
import pytest

from tools.analysis.v3_6.stratify_utf8_readouts import (
    ALL_CLASSES,
    _grid_npz,
    classify_id,
    class_floor,
    stratify_e73,
    stratify_records,
)


# --- 1. 分类边界 ---------------------------------------------------------------


def test_classify_id_boundaries():
    assert classify_id(0) == "pad"
    assert classify_id(1) == "ascii"  # 0x00
    assert classify_id(65) == "ascii"  # 'A'
    assert classify_id(128) == "ascii"  # 0x7F
    assert classify_id(129) == "cont"  # 0x80
    assert classify_id(192) == "cont"  # 0xBF
    assert classify_id(193) == "lead"  # 0xC0
    assert classify_id(230) == "lead"  # 0xE5 中文高频首字节
    assert classify_id(256) == "lead"  # 0xFF
    assert classify_id(257) == "mask"  # MASK_ID


# --- 2. 类内 Top-1 地板 ---------------------------------------------------------


def test_class_floor_majority_share():
    targets = np.array([5, 5, 9, 200])
    sel = np.ones(4, dtype=bool)
    fl = class_floor(targets, sel)
    assert fl["n"] == 4
    assert fl["floor_id"] == 5
    assert fl["floor"] == pytest.approx(0.5)
    assert fl["floor_byte"] == 4
    # 空类
    empty = class_floor(targets, np.zeros(4, dtype=bool))
    assert empty["n"] == 0 and empty["floor"] is None


# --- 3. stratify_records 合成流端到端 -------------------------------------------


def _synth():
    # id: 5=ascii, 150=cont, 200=lead, 257=mask; 每类 2 槽
    targets = np.array([5, 200, 150, 257, 5, 200, 150, 257])
    preds = np.array([5, 200, 150, 257, 5, 9, 150, 7])
    sel = np.ones(8, dtype=bool)
    return preds, targets, sel


def test_stratify_records_exact():
    preds, targets, sel = _synth()
    out = stratify_records(preds, targets, sel, label="t")
    cl = out["classes"]
    assert out["n_slots"] == 8
    assert out["mixed_acc_pooled"] == pytest.approx(0.75)
    assert not out["pad_present"]
    # ascii: 全对; 地板=1.0（类内唯一 id）→ 超地板 0
    assert cl["ascii"]["acc"] == pytest.approx(1.0)
    assert cl["ascii"]["floor"] == pytest.approx(1.0)
    assert cl["ascii"]["over_floor"] == pytest.approx(0.0)
    assert cl["ascii"]["share"] == pytest.approx(0.25)
    # lead: 一对一错; 类内 id 恒 200 → 地板 1.0 → 超地板 −0.5
    assert cl["lead"]["acc"] == pytest.approx(0.5)
    assert cl["lead"]["over_floor"] == pytest.approx(-0.5)
    # mask echo 槽: 目标恒 257 → 地板 1.0
    assert cl["mask"]["floor"] == pytest.approx(1.0)
    # 混合合成一致性: mixed acc == Σ share×acc（槽池化精确合成）
    cc = out["composition_check"]
    assert cc["abs_diff_vs_pooled"] < 1e-12
    assert out["byte_share"] == {"ascii": 0.25, "lead": 0.25, "cont": 0.25}


def test_stratify_records_windows_and_folds():
    preds, targets, sel = _synth()
    rc = np.array([4, 4])  # 每窗 4 槽
    folds = np.array([0, 0, 0, 0, 1, 1, 1, 1])
    out = stratify_records(preds, targets, sel, row_counts=rc, folds=folds, label="t")
    cl = out["classes"]
    # 窗均值: lead 类 w0=[200→hit], w1=[200 vs 9→miss] → 0.5; ascii 两窗全对 → 1.0
    assert cl["lead"]["acc_win_mean"] == pytest.approx(0.5)
    assert cl["ascii"]["acc_win_mean"] == pytest.approx(1.0)
    assert cl["lead"]["win_count_nonempty"] == 2
    # 折均值: lead fold0=1.0, fold1=0.0 → 0.5（与池化同值于此例）
    assert cl["lead"]["acc_fold_mean"] == pytest.approx(0.5)


def test_stratify_records_sel_and_pad():
    preds, targets, sel = _synth()
    sel = sel.copy()
    sel[:4] = False  # 只计后半 4 槽
    targets = targets.copy()
    targets[4] = 0  # 原 ascii 槽改 PAD 目标 → pad 类上报, ascii 类清空
    out = stratify_records(preds, targets, sel, label="t")
    assert out["n_slots"] == 4
    assert out["pad_present"]
    assert out["classes"]["pad"]["n"] == 1
    assert out["classes"]["ascii"]["n"] == 0
    # 计分槽: pad(5vs0 miss) + lead(9vs200 miss) + cont(150 hit) + mask(7vs257 miss)
    assert out["mixed_acc_pooled"] == pytest.approx(0.25)


# --- 4. 网格 npz 装载（as-encoded 主口径 + true_view fallback）------------------


def _write_grid_npz(tmp_path, name, extra_key):
    # (1, 2 窗行, 4 槽); 第 4 槽 = as-encoded MASK echo 位（真字节=200）
    targets_enc = np.array([[5, 200, 150, 257], [5, 200, 150, 257]], dtype=np.int16)
    targets_true = np.array([[5, 200, 150, 200], [5, 200, 150, 200]], dtype=np.int16)
    preds = np.array([[5, 200, 150, 257], [5, 9, 150, 7]], dtype=np.int16)
    sel = np.ones((2, 4), dtype=np.uint8)
    masked = np.array([[0, 0, 0, 1], [0, 0, 0, 1]], dtype=np.uint8)
    p = tmp_path / name
    np.savez_compressed(
        p,
        mhat_preds=preds.reshape(1, 2, 4),
        mhat_targets_enc=targets_enc.reshape(1, 2, 4),
        **{extra_key: targets_true.reshape(1, 2, 4)},
        mhat_slot_mask=sel.reshape(1, 2, 4),
        mhat_masked_true=masked.reshape(1, 2, 4),
        mhat_row_counts=np.array([1, 1]),
    )
    return str(p)


def test_grid_npz_as_encoded_and_true_view(tmp_path):
    # as-encoded 主口径: 含 echo 槽, 池化 = 6/8 = 0.75
    p_enc = _write_grid_npz(tmp_path, "enc.npz", "mhat_targets_true")
    out = _grid_npz(p_enc, "mhat", "t")
    assert out["n_slots"] == 8
    assert out["classes"]["mask"]["n"] == 2
    assert out["mixed_acc_pooled"] == pytest.approx(0.75)
    # 全列 Top-1 地板: 四个 id 各出现 2 次, unique 首序取 id=5 → 0.25
    assert out["mixed_floor"] == pytest.approx(0.25)
    # true_view: masked 位按真字节 200 计分 → 5/8 = 0.625, mask 类清空
    out_t = _grid_npz(p_enc, "mhat", "t", true_view=True)
    tv = out_t["true_byte_view"]
    assert tv["n_slots"] == 8
    assert tv["mixed_acc_pooled"] == pytest.approx(0.625)
    assert tv["classes"]["mask"]["n"] == 0
    assert tv["byte_share"]["lead"] == pytest.approx(4 / 8)

    # Q19 键名 fallback（targets_clean）
    p_q19 = _write_grid_npz(tmp_path, "q19.npz", "mhat_targets_clean")
    out_q = _grid_npz(p_q19, "mhat", "t", true_view=True)
    assert out_q["true_byte_view"]["mixed_acc_pooled"] == pytest.approx(0.625)

    # 旧格式 npz 无真字节副块 → true_byte_view 如实为 None
    p_old = tmp_path / "old.npz"
    np.savez_compressed(
        p_old,
        mhat_preds=np.zeros((1, 1, 4), dtype=np.int16),
        mhat_targets_enc=np.full((1, 1, 4), 5, dtype=np.int16),
        mhat_slot_mask=np.ones((1, 1, 4), dtype=np.uint8),
        mhat_row_counts=np.array([1]),
    )
    out_old = _grid_npz(str(p_old), "mhat", "t", true_view=True)
    assert out_old["true_byte_view"] is None


def test_grid_npz_absent(tmp_path):
    out = _grid_npz(str(tmp_path / "missing.npz"), "mhat", "t")
    assert out["items_absent"] is True


# --- 5. E73 折均值路径 -----------------------------------------------------------


def test_stratify_e73_folds(tmp_path):
    # 两折各 2 样本, fold0 全对 / fold1 lead 错 → 折均值 lead 0.5
    preds = np.array([5, 5, 200, 9], dtype=np.int16)
    targets = np.array([5, 5, 200, 200], dtype=np.int16)
    sel = np.ones(4, dtype=np.uint8)
    fold = np.array([0, 1, 0, 1], dtype=np.uint8)
    p = tmp_path / "probe.npz"
    np.savez_compressed(
        p,
        v_s0_preds=preds,
        v_s0_targets=targets,
        v_s0_sel=sel,
        v_s0_fold=fold,
    )
    out = stratify_e73(str(p), "v", "0")
    cl = out["classes"]
    assert out["n_slots"] == 4
    assert cl["ascii"]["acc_fold_mean"] == pytest.approx(1.0)
    assert cl["lead"]["acc_fold_mean"] == pytest.approx(0.5)
    assert out["classes"]["lead"]["over_floor"] == pytest.approx(-0.5)


def test_stratify_e73_absent(tmp_path):
    out = stratify_e73(str(tmp_path / "missing.npz"))
    assert out["items_absent"] is True


def test_all_classes_registered():
    assert set(ALL_CLASSES) == {"ascii", "lead", "cont", "mask", "pad"}
