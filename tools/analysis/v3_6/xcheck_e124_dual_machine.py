"""E124 双机一致性抽查对拍（用户裁定 2026-09-11，坑 9「硬件迁移」维度条款）：

选择器推理换机（5080 烧门②基座/量必要性账 → 4090 量产 mask log）前，同一批
窗（≥50）双机各跑一遍选择器，对拍四件：
  1. candidates 逐位一致（SHA256 确定性抽样，纯标准库，必须 100%）；
  2. hard_cut 逐位一致（整数路径，必须 100%）；
  3. masked_chunks 集合一致率——目标 50/50；容差：不一致窗 ≤1/50 且差异块
     落在阈值边界（|info−τ|/τ < 5%）或 top-3 剂量边界（第 3/4 名 info 差 <5%）；
  4. info_scores max|Δ| 浮点漂移量级呈报（不作判据，登记用）。

判据 1/2 任一不破即硬 FAIL（确定性底座断了）；判据 3 超容差 FAIL。

用法：
  python tools/analysis/v3_6/xcheck_e124_dual_machine.py \
      --a outputs/_e124_xcheck_local_50.jsonl --b outputs/_e124_xcheck_remote_50.jsonl \
      --threshold 0.02 --max-blocks 3
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _load(path: Path) -> dict[int, dict]:
    log: dict[int, dict] = {}
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rec = json.loads(line)
                log[int(rec["window_id"])] = rec
    return log


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--a", required=True, help="本地半边 JSONL")
    p.add_argument("--b", required=True, help="远端半边 JSONL")
    p.add_argument("--threshold", type=float, default=0.02)
    p.add_argument("--max-blocks", type=int, default=3)
    args = p.parse_args()

    A, B = _load(Path(args.a)), _load(Path(args.b))
    common = sorted(set(A) & set(B))
    if not common:
        print("FAIL: 两份日志无公共 window_id"); return 1
    if sorted(A) != sorted(B):
        print(f"WARN: 窗集不齐（A={len(A)} B={len(B)} 公共={len(common)}），仅对拍公共窗")

    n_cand_bad = n_cut_bad = 0
    mask_mismatch: list[dict] = []
    max_info_delta = 0.0
    for wi in common:
        ra, rb = A[wi], B[wi]
        if ra.get("candidates") != rb.get("candidates"):
            n_cand_bad += 1
        if ra.get("hard_cut") != rb.get("hard_cut"):
            n_cut_bad += 1
        ma, mb = set(ra["masked_chunks"]), set(rb["masked_chunks"])
        sa, sb = ra["info_scores"], rb["info_scores"]
        for c in set(sa) & set(sb):
            max_info_delta = max(max_info_delta, abs(sa[c] - sb[c]))
        if ma != mb:
            # 容差核验：差异块是否全在阈值边界或 top-N 剂量边界
            detail = {"window_id": wi, "only_a": sorted(ma - mb),
                      "only_b": sorted(mb - ma), "borderline": True}
            for side, extra, s_self in (("a", ma - mb, sa), ("b", mb - ma, sb)):
                for c in extra:
                    v = s_self[str(c)]
                    near_tau = abs(v - args.threshold) / args.threshold < 0.05
                    if not near_tau:
                        detail["borderline"] = False
                    detail.setdefault("edge_info", {})[f"{side}:{c}"] = v
            mask_mismatch.append(detail)

    n = len(common)
    print(json.dumps({
        "n_windows": n,
        "candidates_mismatch": n_cand_bad,
        "hard_cut_mismatch": n_cut_bad,
        "masked_set_mismatch": len(mask_mismatch),
        "masked_set_mismatch_nonborderline": sum(1 for m in mask_mismatch
                                                 if not m["borderline"]),
        "info_max_abs_delta": round(max_info_delta, 6),
        "hw_a": A[common[0]].get("hw", "?"),
        "hw_b": B[common[0]].get("hw", "?"),
    }, ensure_ascii=False, indent=1))
    for m in mask_mismatch[:5]:
        print("  mismatch:", json.dumps(m, ensure_ascii=False))

    ok = (n_cand_bad == 0 and n_cut_bad == 0
          and len(mask_mismatch) <= max(1, n // 50)
          and all(m["borderline"] for m in mask_mismatch))
    print("VERDICT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
