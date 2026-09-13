"""UTF-8 位置分解审计仪器（2026-09-13 用户审计单 1, 零训练 retroactive）:
四个读出数（62% 写入 / 0.33 岭回归 / 0.4572 管线 / 0.6045 训练读出件）按
目标字节在 UTF-8 码点中的位置三层分解（ASCII 单字节 / 首字节 lead /
续字节 continuation）, 逐类按位置自锚盲猜地板, 报**超地板值 = acc − 地板**,
不裸报 acc。背景: 中文 UTF-8 三字节首字节取值高度集中 → 混合口径的地板
本身高; 若 0.33 主要由首字节贡献, 「内容活在状态里」降级为「状态知道
语种/字类」（判决链环②重审输入）。

消费三件评测仪器的审计落盘 npz（重跑零口径改动只加落盘字段, 与聚合数
同源同一次前向/同一次拟合产出, 见各自 --dump-* 旗标）:
  probe_oracle_write_verdict --dump-probe-bytes   → byte_probe_records.npz (E73 A6, 62%)
  probe_closed_form_readout   --dump-stage3-bytes → stage3_byte_records.npz (Q19 段3, 0.33)
  probe_decoder_denoise_eval  --dump-bytes        → items_bytes.npz (E118 m̂ 0.4572 /
                                                    E119 q20_k 三种子 0.6045)

分类口径（目标 id, PAD-offset 编码: PAD=0, 字节 b→id b+1, MASK_ID=257）:
  ascii  id 1..128    字节 0x00–0x7F（单字节码点）
  cont   id 129..192  字节 0x80–0xBF（UTF-8 续字节）
  lead   id 193..256  字节 0xC0–0xFF（UTF-8 首字节）
  mask   id 257       as-encoded echo 槽（非字节目标; 目标恒定 → 地板恒 1,
                     超地板恒 0 —— echo 槽零内容证据, 单列不混入字节层）
  pad    id 0         合法计分槽应缺席; 出现即上报（口径事故）

地板口径（成文）: 逐类 Top-1 地板 = 该类计分槽内目标 id 边际分布最大份额
（常数预测器在该类的准确率上限）; 全列地板 = 全部计分槽上同口径（Q19 D3
纯先验预测器同族）。超地板 = 类 acc − 类地板。主口径 = 槽池化（与混合数
精确合成: 混合 acc = Σ_c 份额_c × 类 acc_c, 一致性检查随 JSON 落盘）;
E73 A6 另报折均值口径（原仪器 acc = 两折均值, 主口径沿用）。

Usage:
  python tools/analysis/v3_6/stratify_utf8_readouts.py \
    --e73-npz  outputs/utf8_strat_four_20260913/raw/e73_a6/byte_probe_records.npz \
    --q19-npz  outputs/utf8_strat_four_20260913/raw/q19/stage3_byte_records.npz \
    --e118-npz outputs/utf8_strat_four_20260913/raw/e118/items_bytes.npz \
    --q20-s42-npz outputs/utf8_strat_four_20260913/raw/q20_s42/items_bytes.npz \
    --q20-s1-npz  outputs/utf8_strat_four_20260913/raw/q20_s1/items_bytes.npz \
    --q20-s2-npz  outputs/utf8_strat_four_20260913/raw/q20_s2/items_bytes.npz \
    --out-json outputs/utf8_strat_four_20260913/stratified_four_numbers.json
任何输入缺席 → 对应数在 JSON 里标 "items_absent": true, 不补凑。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

PAD_ID, MASK_ID = 0, 257
BYTE_CLASSES = ("ascii", "lead", "cont")
NONBYTE_CLASSES = ("mask", "pad")
ALL_CLASSES = BYTE_CLASSES + NONBYTE_CLASSES


def classify_id(tid: int) -> str:
    """目标 id → 位置类（PAD-offset: 字节 = id−1）。"""
    if tid == PAD_ID:
        return "pad"
    if tid == MASK_ID:
        return "mask"
    b = tid - 1
    if b < 0x80:
        return "ascii"
    if b < 0xC0:
        return "cont"
    return "lead"


def class_floor(targets: np.ndarray, sel: np.ndarray) -> dict:
    """类内 Top-1 地板: sel 计分槽内该类目标 id 边际分布最大份额。
    Returns {floor, floor_id, floor_byte, floor_count, n}。空类全 None。"""
    ids = targets[sel]
    if ids.size == 0:
        return {"floor": None, "floor_id": None, "floor_byte": None, "floor_count": 0, "n": 0}
    vals, cnts = np.unique(ids, return_counts=True)
    i = int(np.argmax(cnts))
    fid = int(vals[i])
    return {
        "floor": float(cnts[i] / ids.size),
        "floor_id": fid,
        "floor_byte": fid - 1 if fid not in (PAD_ID,) else None,
        "floor_count": int(cnts[i]),
        "n": int(ids.size),
    }


def global_floor(targets: np.ndarray, sel: np.ndarray) -> dict:
    """全列（混合口径）Top-1 地板, class_floor 同式不加类掩码。"""
    return class_floor(targets, sel)


def stratify_records(
    preds: np.ndarray,
    targets: np.ndarray,
    sel: np.ndarray,
    row_counts: np.ndarray | None = None,
    folds: np.ndarray | None = None,
    label: str = "",
) -> dict:
    """一组逐样本/逐槽记录的三层分解。主口径 = 槽池化; row_counts 给定时
    附窗均值参考; folds 给定时附折均值参考（E73 原仪器 acc = 两折均值）。
    Returns {label, mixed:{...}, classes:{类:{n,share,acc,acc_win,acc_fold,floor,
    over_floor,floor_id,floor_byte}}, pad_present, composition_check}"""
    sel = sel.astype(bool)
    p, t = preds.reshape(-1)[sel.reshape(-1)], targets.reshape(-1)[sel.reshape(-1)]
    hits = (p == t).astype(np.float64)
    n_total = int(t.size)
    acc_pooled = float(hits.mean()) if n_total else None
    t_cls = np.array([classify_id(int(x)) for x in t]) if n_total else np.zeros(0, dtype="U6")

    classes: dict = {}
    acc_mix_recon = 0.0
    for c in ALL_CLASSES:
        csel = t_cls == c
        n_c = int(csel.sum())
        row = {"n": n_c, "share": (n_c / n_total) if n_total else None}
        if n_c:
            acc_c = float(hits[csel].mean())
            fl = class_floor(t, csel)
            row["acc"] = acc_c
            row["floor"] = fl["floor"]
            row["over_floor"] = acc_c - fl["floor"]
            row["floor_id"] = fl["floor_id"]
            row["floor_byte"] = fl["floor_byte"]
            acc_mix_recon += row["share"] * acc_c
            if row_counts is not None:
                # 窗均值参考: 逐窗类 acc, 空窗跳过（计窗数随报）
                rc = list(map(int, row_counts))
                offs = np.concatenate([[0], np.cumsum(rc)])
                per_win = []
                for wi in range(len(rc)):
                    w = slice(offs[wi], offs[wi + 1])
                    cw = csel[w]
                    if cw.any():
                        per_win.append(float(hits[w][cw].mean()))
                row["acc_win_mean"] = float(np.mean(per_win)) if per_win else None
                row["win_count_nonempty"] = len(per_win)
            if folds is not None:
                per_fold = []
                for fi in (0, 1):
                    cf = csel & (folds == fi)
                    if cf.any():
                        per_fold.append(float(hits[cf].mean()))
                row["acc_fold_mean"] = float(np.mean(per_fold)) if per_fold else None
                row["fold_count_nonempty"] = len(per_fold)
        else:
            row.update({"acc": None, "floor": None, "over_floor": None,
                        "floor_id": None, "floor_byte": None})
        classes[c] = row

    gf = global_floor(t, np.ones(t.shape, dtype=bool)) if n_total else {"floor": None, "floor_id": None}
    out = {
        "label": label,
        "n_slots": n_total,
        "mixed_acc_pooled": acc_pooled,
        "mixed_floor": gf["floor"],
        "mixed_floor_id": gf["floor_id"],
        "mixed_over_floor": (acc_pooled - gf["floor"]) if (acc_pooled is not None and gf["floor"] is not None) else None,
        "byte_share": {c: classes[c]["share"] for c in BYTE_CLASSES},
        "classes": classes,
        "pad_present": classes["pad"]["n"] > 0,
    }
    if n_total:
        out["composition_check"] = {
            "mixed_acc_reconstructed_from_classes": acc_mix_recon,
            "abs_diff_vs_pooled": abs(acc_mix_recon - acc_pooled) if acc_pooled is not None else None,
        }
    return out


# ---------------------------------------------------------------------------
# 三件仪器 npz 装载 → stratify_records 输入
# ---------------------------------------------------------------------------


def stratify_e73(npz_path: str, source: str = "v", slot: str = "0") -> dict | None:
    """E73 A6 逐样本记录（byte_probe_records.npz）: 折均值主口径。
    记录已按槽内 valid 样本选出（preds/targets/fold 同长）, sel 恒全真。"""
    if not Path(npz_path).exists():
        return {"items_absent": True, "label": f"e73_a6_{source}_s{slot}", "path": npz_path}
    z = np.load(npz_path)
    preds = z[f"{source}_s{slot}_preds"].astype(np.int64)
    return stratify_records(
        preds,
        z[f"{source}_s{slot}_targets"].astype(np.int64),
        np.ones(preds.shape, dtype=bool),
        folds=z[f"{source}_s{slot}_fold"],
        label=f"e73_a6_from_{source}_slot{slot}",
    )


def _grid_npz(npz_path: str, col: str, label: str, true_view: bool = False) -> dict | None:
    """decode 网格逐字节记录（items_bytes.npz / stage3_byte_records.npz 同构）。
    主口径恒 = as-encoded（targets_enc, 含 mask echo 槽 —— 与册上混合数同
    分母, 复现门对表用）; true_view=True 时附 true_byte_view 副块（masked
    位按真字节计分, 剔 mask/pad 后的纯字节层）。"""
    if not Path(npz_path).exists():
        return {"items_absent": True, "label": label, "path": npz_path}
    z = np.load(npz_path)
    preds = z[f"{col}_preds"].astype(np.int64)
    sel = z[f"{col}_slot_mask"]
    rc = z[f"{col}_row_counts"]
    out = stratify_records(preds, z[f"{col}_targets_enc"].astype(np.int64), sel, row_counts=rc, label=label)
    if true_view:
        tkey = f"{col}_targets_true" if f"{col}_targets_true" in z.files else f"{col}_targets_clean"
        if tkey not in z.files:
            out["true_byte_view"] = None  # 旧格式 npz 无真字节副块, 如实缺省
            return out
        t_true = z[tkey].astype(np.int64)
        sel_true = sel.astype(bool) & (t_true != MASK_ID) & (t_true != PAD_ID)
        out_true = stratify_records(
            preds, t_true, sel_true, row_counts=rc, label=label + "__true_bytes"
        )
        out["true_byte_view"] = {
            "n_slots": out_true["n_slots"],
            "mixed_acc_pooled": out_true["mixed_acc_pooled"],
            "mixed_floor": out_true["mixed_floor"],
            "mixed_over_floor": out_true["mixed_over_floor"],
            "byte_share": out_true["byte_share"],
            "classes": out_true["classes"],
        }
    return out


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--e73-npz", default=None, help="E73 A6 byte_probe_records.npz（62%% 写入）")
    ap.add_argument("--q19-npz", default=None, help="Q19 stage3_byte_records.npz（0.33 岭回归）")
    ap.add_argument("--e118-npz", default=None, help="E118 items_bytes.npz（0.4572 管线）")
    ap.add_argument("--q20-s42-npz", default=None, help="E119 s42 items_bytes.npz（0.6045 种子之一）")
    ap.add_argument("--q20-s1-npz", default=None)
    ap.add_argument("--q20-s2-npz", default=None)
    ap.add_argument("--e73-slot", default="0", help="E73 A6 主槽位（headline 62%% = slot0）")
    ap.add_argument("--out-json", default=None, help="汇总 JSON 路径（缺省只打印）")
    args = ap.parse_args()

    report: dict = {
        "audit": "UTF-8 位置分解（2026-09-13 用户审计单 1）",
        "convention": {
            "classes": {"ascii": "字节 0x00-0x7F", "lead": "字节 0xC0-0xFF (UTF-8 首字节)",
                        "cont": "字节 0x80-0xBF (UTF-8 续字节)", "mask": "MASK_ID echo 槽(非字节)",
                        "pad": "PAD(应缺席)"},
            "floor": "逐类 Top-1 地板 = 类内目标 id 边际最大份额（常数预测上限）; 报超地板 = acc − 地板",
            "primary_acc": "槽池化（与混合数精确合成）; acc_win_mean/acc_fold_mean 为参考",
        },
        "numbers": {},
    }
    nums = report["numbers"]

    # 1) 62% 写入: E73 A6 from-v slot0（headline）+ slots 1-3 + from-m 上限对照
    if args.e73_npz:
        nums["write_62pct_e73a6"] = {
            "headline": stratify_e73(args.e73_npz, "v", args.e73_slot),
            "aux_slots": {f"v_s{s}": stratify_e73(args.e73_npz, "v", str(s)) for s in (1, 2, 3)},
            "ceiling_from_m": {f"m_s{s}": stratify_e73(args.e73_npz, "m", str(s)) for s in (0, 1, 2, 3)},
        }

    # 2) 0.33 岭回归: Q19 段3 oracle（headline 0.3293）+ natural（0.3150）+ shuffled 地板列
    if args.q19_npz:
        nums["ridge_033_q19"] = {
            "headline_oracle": _grid_npz(args.q19_npz, "oracle", "q19_stage3_oracle", true_view=True),
            "natural": _grid_npz(args.q19_npz, "natural", "q19_stage3_natural", true_view=True),
            "shuffled_floor_col": _grid_npz(args.q19_npz, "shuffled", "q19_stage3_shuffled"),
        }

    # 3) 0.4572 管线: E118 m̂ 列（headline）+ clean/scrambled 控制
    if args.e118_npz:
        nums["pipeline_04572_e118"] = {
            "headline_mhat": _grid_npz(args.e118_npz, "mhat", "e118_mhat", true_view=True),
            "clean_ref": _grid_npz(args.e118_npz, "clean", "e118_clean"),
            "scrambled_floor_col": _grid_npz(args.e118_npz, "scrambled", "e118_scrambled"),
        }

    # 4) 0.6045 训练读出件: E119 q20_k 三种子各自分解 + 种子均值行
    q20_seeds = {}
    for tag, arg in (("s42", args.q20_s42_npz), ("s1", args.q20_s1_npz), ("s2", args.q20_s2_npz)):
        if arg:
            q20_seeds[tag] = _grid_npz(arg, "q20_k", f"q20_k_{tag}", true_view=True)
    if q20_seeds:
        present = [v for v in q20_seeds.values() if not v.get("items_absent")]
        seed_mean = {}
        for c in ALL_CLASSES:
            accs = [v["classes"][c]["acc"] for v in present if v["classes"][c].get("acc") is not None]
            floors = [v["classes"][c]["floor"] for v in present if v["classes"][c].get("floor") is not None]
            overs = [v["classes"][c]["over_floor"] for v in present if v["classes"][c].get("over_floor") is not None]
            shares = [v["classes"][c]["share"] for v in present if v["classes"][c].get("share") is not None]
            seed_mean[c] = {
                "acc_seed_mean": float(np.mean(accs)) if accs else None,
                "floor_seed_mean": float(np.mean(floors)) if floors else None,
                "over_floor_seed_mean": float(np.mean(overs)) if overs else None,
                "share_seed_mean": float(np.mean(shares)) if shares else None,
                "n_seeds": len(accs),
            }
        nums["trained_readout_06045_e119"] = {
            "per_seed": q20_seeds,
            "seed_mean_classes": seed_mean,
            "seeds_present": list(q20_seeds.keys()),
        }

    # 控制台摘要（headline 行）
    def line(cls_row):
        if cls_row.get("acc") is None:
            return "n=0"
        return (f"n={cls_row['n']} acc={cls_row['acc']:.4f} floor={cls_row['floor']:.4f} "
                f"over={cls_row['over_floor']:+.4f} share={cls_row['share']:.3f}")

    print("== UTF-8 位置分解（报超地板, 不裸报 acc 为主读出）==")
    for key, block in nums.items():
        head = block.get("headline") or block.get("headline_oracle") or block.get("headline_mhat")
        seeds = block.get("per_seed") if "trained_readout" in key else None
        if head is not None and not head.get("items_absent"):
            print(f"\n[{key}] mixed acc={head['mixed_acc_pooled']:.4f} "
                  f"floor={head['mixed_floor']:.4f} over={head['mixed_over_floor']:+.4f} n={head['n_slots']}")
            for c in ALL_CLASSES:
                print(f"  {c:6s} {line(head['classes'][c])}")
        elif seeds:
            print(f"\n[{key}] 三种子均值（{block['seeds_present']}）:")
            for c in BYTE_CLASSES + ("mask",):
                m = block["seed_mean_classes"][c]
                if m["acc_seed_mean"] is not None:
                    print(f"  {c:6s} acc={m['acc_seed_mean']:.4f} floor={m['floor_seed_mean']:.4f} "
                          f"over={m['over_floor_seed_mean']:+.4f} share={m['share_seed_mean']:.3f}")
        else:
            absent = head.get("path") if head is not None else "?"
            print(f"\n[{key}] items 缺席, 需重跑（{absent}）——如实登记, 不补凑")

    if args.out_json:
        Path(args.out_json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out_json).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nJSON -> {args.out_json}")


if __name__ == "__main__":
    main()
