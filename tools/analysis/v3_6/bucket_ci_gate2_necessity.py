"""门② 必要性账 距离分档 bootstrap CI（2026-09-12，用户裁定补算）。

对 gate_e123_necessity_v2.py 的 items.jsonl 按下游距离分档
（distance = sink_chunk − chunk ∈ [1..SCORE_DIST=8]：d1 / d2 / d≥3），
按仪器自举协议**同构**地对每档分别算点估 + 窗级 bootstrap CI95。
零训练、零前向，纯流式分析（items.jsonl 216MB 逐行读，不整载）。

协议同构（以 gate_e123_necessity_v2.py / probe_e122_necessity_book.py 代码为准）：
- 重采样单位 = 窗（window_id；= 仪器 window_sums 的粒度，非位点级）。
  窗宇宙 = items.jsonl 中出现的全部 window_id（= 仪器 status=="ok" 的窗）。
- 统计量 = Σ_w sum_{w,b} / Σ_w n_{w,b}（逐字节池化均值）——即门② 把窗 sums
  投影成 boot_in（sel_d_b1 = d̄_w·n_w，ctl≡0）后 bootstrap_contrast 的
  contrast 形态。
- 每格独立 random.Random(SEED+1=43)，n_boot=2000，重采样次序与
  bootstrap_contrast 一致（W 次 rng.randrange(W) / 抽样）；某次重采样该档
  计数为 0 → 记 None 跳过（与 bootstrap_contrast 的无效样本处理同）；CI95
  取 sorted boots 的 [int(0.025·len), int(0.975·len)−1] 索引（percentile）。
- 诚实注记：仪器 summary 的 mean_d_total 是「窗均值的无权平均」，与
  bootstrap point（池化）形态不同。本脚本两种点估都输出，headline 用
  池化形态（与 CI 同统计量），window_mean 形态仅作对照。
- 一致性自检：全档合计的池化点估须复现 items 同目录 summary.json 的
  bootstrap.point；合计窗均形态须复现 mean_d_total。偏差非零 → 响亮报错。
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.analysis.v3_6.probe_e122_necessity_book import bootstrap_contrast  # noqa: E402

DEFAULT_ITEMS = [
    "44M=outputs/e124_gate2_necessity_v2_20260910/items.jsonl",
    "150M=outputs/e124_gate2_necessity_scale3x_20260912/items.jsonl",
]
DEFAULT_OUT = "outputs/e124_gate2_necessity_bucket_ci_20260912.json"
N_BOOT = 2000
SEED = 43          # = 仪器 SEED(42) + 1，同 bootstrap_contrast 调用口径
SCORE_DIST = 8     # gate_e123_necessity_v2.SCORE_DIST，距离支撑 [1..8]
BUCKETS = ("d1", "d2", "dge3")
BUCKET_DEFS = {"d1": "distance == 1", "d2": "distance == 2",
               "dge3": "3 <= distance <= 8"}


def bucket_of(distance: int) -> str | None:
    """分档规则（与仪器 tgt 收集条件 `sink_c − c in range(1, SCORE_DIST+1)`
    同源）：1→d1，2→d2，3..8→dge3，域外 → None（上游不该出现，单独计数）。"""
    if distance == 1:
        return "d1"
    if distance == 2:
        return "d2"
    if 3 <= distance <= SCORE_DIST:
        return "dge3"
    return None


def scan_items(path: Path) -> dict:
    """流式扫 items.jsonl，聚出 (window_id, bucket) → (n, sum_d_total)。"""
    agg: dict[tuple[int, str], list] = {}
    windows: set[int] = set()
    unexpected = Counter()
    n_positions = 0
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            it = json.loads(line)
            n_positions += 1
            wi = int(it["window_id"])
            windows.add(wi)
            b = bucket_of(int(it["distance"]))
            if b is None:
                unexpected[int(it["distance"])] += 1
                continue
            cell = agg.get((wi, b))
            if cell is None:
                agg[(wi, b)] = [1, float(it["d_total"])]
            else:
                cell[0] += 1
                cell[1] += float(it["d_total"])
    return {"agg": agg, "windows": sorted(windows), "n_positions": n_positions,
            "unexpected_distances": dict(unexpected)}


def percentile_ci(boots: list[float], level: float = 0.95) -> tuple[float | None, float | None]:
    """与 bootstrap_contrast 相同的 percentile 取法（索引公式逐位同）。"""
    if not boots:
        return None, None
    s = sorted(boots)
    lo = s[max(0, int((1 - level) / 2 * len(s)))]
    hi = s[min(len(s) - 1, int((1 + level) / 2 * len(s)) - 1)]
    return lo, hi


def bucket_cell(agg: dict, windows: list[int], bucket: str,
                n_boot: int, seed: int) -> dict:
    """单档一格：池化点估 + 窗级 bootstrap CI（协议同 bootstrap_contrast）。

    统计量计算路径精确镜像门②投影：门② boot_in 的 sel_d_b1 = d̄_w·n_w
    （窗均值×n 回程），本处逐位同形——保证与仪器同码路径下 boots 逐位相等。"""
    rows = []
    for wi in windows:
        n, s = agg.get((wi, bucket), (0, 0.0))
        rows.append((n, (s / n) * n if n else 0.0))  # (n, sel_d_b1 回程形)
    W = len(windows)
    total_n = sum(r[0] for r in rows)
    total_sel = sum(r[1] for r in rows)
    point = total_sel / total_n if total_n else None
    nonempty = [r for r in rows if r[0]]
    point_wmean = (sum(s / n for n, s in nonempty) / len(nonempty)) if nonempty else None

    rng = random.Random(seed)
    boots = []
    for _ in range(n_boot):
        # 内建 sum()（3.12+ 对 float 为 Neumaier 补偿求和）+ 先建样本表再聚合
        # ——与 bootstrap_contrast 的 contrast() 逐字同形，boots 逐位相等。
        idx = [rng.randrange(W) for _ in range(W)]
        ns_ = sum(rows[j][0] for j in idx)
        nc_ = ns_
        if not ns_ or not nc_:
            continue
        sel = sum(rows[j][1] for j in idx)
        ctl = sum(0.0 for _ in idx)
        boots.append(sel / ns_ - ctl / nc_)
    lo, hi = percentile_ci(boots)
    return {
        "bucket": bucket,
        "definition": BUCKET_DEFS[bucket],
        "point_pooled": point,
        "point_window_mean": point_wmean,
        "ci95_lo": lo,
        "ci95_hi": hi,
        "ci_excludes_zero": bool(point is not None and lo is not None and (lo > 0 or hi < 0)),
        "n": total_n,
        "n_windows_nonempty": len(nonempty),
        "n_boot": n_boot,
        "n_boot_valid": len(boots),
        "seed": seed,
        "resample_unit": "window",
    }


def analyze_items(label: str, path: Path, n_boot: int, seed: int) -> dict:
    t0 = time.time()
    scan = scan_items(path)
    agg, windows = scan["agg"], scan["windows"]
    if not windows:
        raise SystemExit(f"{label}: items.jsonl 零窗——{path}")
    cells = {b: bucket_cell(agg, windows, b, n_boot, seed) for b in BUCKETS}

    # 一致性自检：全档合计复现 summary.json 的 bootstrap.point / mean_d_total
    total_n = sum(c["n"] for c in cells.values())
    total_sum = sum(c["n"] * c["point_pooled"] for c in cells.values() if c["point_pooled"] is not None)
    pooled_total = total_sum / total_n if total_n else None
    all_win = [(0, 0.0)] * len(windows)
    for (wi, _b), (n, s) in agg.items():
        i = windows.index(wi)
        all_win[i] = (all_win[i][0] + n, all_win[i][1] + s)
    wmean_total = (sum(s / n for n, s in all_win if n) / len(windows)) if windows else None

    summary_path = path.parent / "summary.json"
    check: dict = {"recomputed_pooled_total": pooled_total,
                   "recomputed_window_mean_total": wmean_total}
    if summary_path.exists():
        sj = json.loads(summary_path.read_text(encoding="utf-8"))
        boot = sj["results"]["bootstrap"]
        check["summary_bootstrap_point"] = boot["point"]
        check["summary_mean_d_total"] = sj["results"]["mean_d_total"]
        check["abs_diff_pooled_vs_summary_point"] = abs(pooled_total - boot["point"])
        check["wmean_round5_vs_summary"] = round(wmean_total, 5)
        # summary 的 bootstrap.point 未舍入 → 1e-9 容差；mean_d_total 是仪器
        # round(...,5) 后的值 → 重算值舍到 5 位须逐字相等（全精度对舍入值
        # 卡紧容差会假警报）。
        if check["abs_diff_pooled_vs_summary_point"] > 1e-9:
            raise SystemExit(f"{label}: 池化合计 {pooled_total} 与 summary bootstrap.point "
                             f"{boot['point']} 偏差 {check['abs_diff_pooled_vs_summary_point']} "
                             f"超容差 1e-9——重建逻辑与仪器不同构，响亮失败")
        if round(wmean_total, 5) != sj["results"]["mean_d_total"]:
            raise SystemExit(f"{label}: 窗均合计 round5={round(wmean_total, 5)} 与 summary "
                             f"mean_d_total {sj['results']['mean_d_total']} 不等——窗宇宙重建不一致")
    return {
        "label": label,
        "items_path": str(path),
        "n_positions": scan["n_positions"],
        "n_windows": len(windows),
        "unexpected_distances": scan["unexpected_distances"],
        "cells": cells,
        "total_check": check,
        "elapsed_sec": round(time.time() - t0, 1),
    }


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--items", action="append", default=None,
                   metavar="LABEL=PATH",
                   help="label=items.jsonl 路径，可重复；默认 44M/150M 两套")
    p.add_argument("--out", default=DEFAULT_OUT)
    p.add_argument("--bootstrap", type=int, default=N_BOOT)
    p.add_argument("--seed", type=int, default=SEED)
    args = p.parse_args()
    specs = args.items or DEFAULT_ITEMS
    runs = []
    for spec in specs:
        label, sep, path = spec.partition("=")
        if not sep:
            raise SystemExit(f"--items 需 LABEL=PATH 形态，收到：{spec}")
        runs.append(analyze_items(label, Path(path), args.bootstrap, args.seed))

    out = {
        "gate2_necessity_bucket_ci": True,
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "source_instrument": "tools/analysis/v3_6/gate_e123_necessity_v2.py",
        "protocol": {
            "resample_unit": "window（window_id；= 仪器 window_sums 粒度，非位点级）",
            "statistic": "Σ_w sum_d_total / Σ_w n（逐字节池化均值；门② ctl≡0，"
                         "= bootstrap_contrast 投影 boot_in 的 contrast 形态）",
            "n_boot": args.bootstrap,
            "seed": args.seed,
            "seed_note": "仪器 SEED=42，bootstrap 用 SEED+1=43（bootstrap_contrast 调用口径）",
            "ci": "percentile：sorted boots 的 [int(0.025·len), int(0.975·len)−1]",
            "invalid_resample": "该次重采样档计数为 0 → None 跳过（与 bootstrap_contrast 同）",
            "point_forms_note": "headline point_pooled 与 CI 同统计量形态；"
                                "point_window_mean（窗均值无权平均）仅对照——仪器 "
                                "summary 的 mean_d_total 属后一形态",
        },
        "bucket_definitions": BUCKET_DEFS,
        "runs": runs,
    }
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
