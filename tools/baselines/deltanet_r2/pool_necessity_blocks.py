"""R2 收官必要性账多块池化（判决件聚合，仪器零口径改动）。

读 N 个块目录的 items.jsonl（probe_e122_deltanet_book 产物），按仪器自家
run_window 聚合语义重建逐窗 sums，再调用仪器自家 bootstrap_contrast 出
池化点估+CI。判读函数也用仪器自家 verdict（判序 CI 在先，同构 E122）。
每块独立 summary 的 contrast 一并汇报（块间稳健性）。

Usage:
  python tools/baselines/deltanet_r2/pool_necessity_blocks.py \
      --blocks dir1 dir2 ... --out pooled_summary.json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from tools.analysis.cross_arch import probe_e122_deltanet_book as e122


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--blocks", nargs="+", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()

    window_sums: list[dict] = []
    blocks_meta = []
    for b in args.blocks:
        items_path = Path(b) / "items.jsonl"
        summary_path = Path(b) / "summary.json"
        sums = defaultdict(lambda: {"n_sel": 0, "sel_d_b1": 0.0, "n_strong": 0,
                                    "n_ctl": 0, "ctl_d_b1": 0.0})
        n_items = 0
        with items_path.open(encoding="utf-8") as f:
            for line in f:
                it = json.loads(line)
                s = sums[it["window_id"]]
                if it["role"] == "selected":
                    s["n_sel"] += 1
                    s["sel_d_b1"] += it["delta_b1"]
                    s["n_strong"] += int(it["strong"])
                else:
                    s["n_ctl"] += 1
                    s["ctl_d_b1"] += it["delta_b1"]
                n_items += 1
        window_sums.extend(sums.values())
        d = json.load(open(summary_path, encoding="utf-8"))
        blocks_meta.append({
            "dir": b, "n_items": n_items, "n_windows": len(sums),
            "contrast_point": d["contrast_b1"]["point"],
            "ci95": [d["contrast_b1"]["ci95_lo"], d["contrast_b1"]["ci95_hi"]],
            "ci_excludes_zero": d["contrast_b1"]["ci_excludes_zero"],
            "mean_sel": d["selected"]["mean_delta_b1"],
            "verdict": d["verdict"],
        })
        print(f"[pool] {b}: windows={len(sums)} point={d['contrast_b1']['point']:+.4f} "
              f"CI=[{d['contrast_b1']['ci95_lo']:+.4f},{d['contrast_b1']['ci95_hi']:+.4f}]",
              flush=True)

    pooled = e122.bootstrap_contrast(window_sums, 2000, 424243)
    n_sel = sum(w["n_sel"] for w in window_sums)
    n_ctl = sum(w["n_ctl"] for w in window_sums)
    mean_sel = sum(w["sel_d_b1"] for w in window_sums) / n_sel
    mean_ctl = sum(w["ctl_d_b1"] for w in window_sums) / n_ctl
    out = {
        "probe": "R2 收官必要性账多块池化（bootstrap=仪器自家函数，种子 424243）",
        "blocks": blocks_meta,
        "pooled": {
            "n_windows": len(window_sums), "n_sel": n_sel, "n_ctl": n_ctl,
            "mean_sel": mean_sel, "mean_ctl": mean_ctl,
            "contrast_point": pooled["point"],
            "ci95": [pooled["ci95_lo"], pooled["ci95_hi"]],
            "ci_excludes_zero": pooled["ci_excludes_zero"],
            "n_boot_valid": pooled["n_boot_valid"], "seed": pooled["seed"],
            "verdict_instrument_own": e122.verdict(mean_sel, pooled),
            "positive_line_note": "预注册阳性线=CI 下界>0 且点估≥0.05 nat（§9.4 已裁定）；"
                                  "过线与否报数不判读，判读归主会话",
        },
    }
    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=2),
                              encoding="utf-8")
    print(json.dumps(out["pooled"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
