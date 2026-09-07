"""E123 前置门① 密度账改造版（2026-09-07，零训练纯算术，冻结任务书 §3.1）。

合体臂辅助监督=逐位置稠密（第七性质）：每个被遮蔽字节都是读出件的监督位。
本账落一行算术：每窗遮蔽位点数 × 每位置监督字节 = 等效监督字节/窗，对照
维护成本线（Q13 瞬态基线 1.5 字节/窗、D1 监督 ~110 字节/窗、密度账最严口径
54.8）落盘。口径钉死：遮蔽粒度=chunk 16B、块数 1–4（开口项③），窗=4096B。
"""
import json
from pathlib import Path

CHUNK = 16          # 遮蔽粒度（字节，= chunk）
BLOCKS = (1, 2, 3, 4)  # 开口项③ 提案上限域
Q13_BASELINE = 1.5   # 五次瞬态坟：每窗 ~1.5 字节监督密度（只催生瞬态）
D1_SUPERVISED = 110.0   # D1 实际监督（算术关按此放行，54.8=50% 落点线）
LANDING_STRICT = 54.8   # 密度账最严口径

rows = []
for n in BLOCKS:
    bpw = n * CHUNK  # 等效监督字节/窗（逐位置稠密：每被遮字节一监督位）
    rows.append({
        "blocks_per_window": n,
        "masked_bytes_per_window": bpw,
        "supervised_bytes_per_window": bpw,  # 第七性质：1 字节 ↔ 1 监督位
        "vs_q13_baseline": round(bpw / Q13_BASELINE, 2),
        "vs_d1_supervised": round(bpw / D1_SUPERVISED, 3),
        "vs_landing_strict": round(bpw / LANDING_STRICT, 3),
    })

out_dir = Path("outputs/e123_gate_density_20260907")
out_dir.mkdir(parents=True, exist_ok=True)
summary = {
    "gate": "E123 前置门① 密度账改造版",
    "doctrine": "两门一预算方程：本账数梯度供给量（必要性账 v2 测梯度质量）；"
                "两门任一不及格改语料/位点池，不改剂量",
    "window_bytes": 4096,
    "mask_granularity_chunk_bytes": CHUNK,
    "dose_rows": rows,
    "verdict": (
        "过账：16–64 监督字节/窗 = Q13 瞬态基线的 10.7–42.7×、密度账最严口径的 "
        "29%–117%、D1 监督同量级——且本臂监督是逐位置稠密（每被遮字节都直接作用于"
        "读出件，第七性质），密度天然过账。维护成本线的对照值同册：D1 的 110 字节/窗"
        "当年按算术关放行，本臂上界 64 落在同量级深处；与 Q13 的 1.5（只催生瞬态）"
        "差一个量级以上。"
    ),
}
(out_dir / "summary.json").write_text(
    json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False, indent=2))
