"""R3 丙附带件 c3：评测侧对齐附属读数（任务书 §2.3 (c3)，§9.3 已采纳，零训练）。

模型不动、仪器跨段定义对齐 S0'' 切点——机制注记不判负正，不改主判决口径
（以免破同卷）。本启动器只替换仪器本体
``tools/analysis/cross_arch/probe_e122_deltanet_book.py`` 的三个模块级接缝
（本体一字节不改；丙启动器同范式）：

- ``load_model_and_tokenizer``：本地 5080 无 accelerate → r3_spec 本地等价
  装载器（device_map→.to 单卡放置等价，shim/规范化/fingerprint 全保留）；
  c3 不挂 vtile patch、不改任何权重（**模型不动**=母列 ckpt 原样）。fingerprint
  注入 ``r3_c3`` 字段随 summary 落盘（跨段定义对齐的口径戳记）。
- ``run_window``：进窗前按 window_id 从语料直读窗字节 → S0'' 切点 → token
  段长计划（r3_spec.vtile_plan_for_window，与丙臂 c1 同一切点管线）→ 展成
  位置→段号映射表存 holder，委托原 run_window，finally 清 holder（防跨窗
  泄漏）。逐窗 S0'' 切点统计落 ``<out-dir>/c3_window_stats.jsonl``。
- ``cross_segment_occurrences``：选择链的「跨段」判定从固定 256-token 网格
  （``p // seg_tokens``）换成 S0'' 段号映射（holder 当前窗映射表；缺席响亮
  停报——绝不静默回落原生网格 = 口径漂移）。**仅此选择语义对齐**；其余全
  走仪器本体（稀有表/池/簇半分/手术/计分位/bootstrap/种子零改动）。items
  审计字段 source_segment/repeat_segment 仍按原生 seg_tokens 网格记（描述
  字段不进计分；summary 注记此边界）。

读数性质（预注册）：S0'' 段均 ~11 token ≪ 原生 256-token 段，「跨段重复」
口径大幅放宽 → n_sel 与对比结构显著位移属预期形态；c3 不判负正、不与主判
决口径混排，只作机制注记素材归主会话。

Usage（形态与门③同构，仅换启动器）:
  python tools/baselines/deltanet_r2/probe_r3_c3_book.py \
      --model-path outputs/r2_mother_20k_local_20260914/mother20k_latest \
      --corpus P:/FLUED_corpus/corpus_v3/corpus_v3.txt \
      --n-windows 40 --start-window 0 --seed 424242 --device cuda \
      --out-dir outputs/r3_transplant_vtile_20260914/c3_s0align40w
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import tools.analysis.cross_arch.probe_e122_deltanet_book as e122  # noqa: E402
import tools.baselines.deltanet_r2.r3_spec as r3  # noqa: E402

_orig_run_window = e122.run_window
_orig_cross_segment_occurrences = e122.cross_segment_occurrences

_HOLDER: dict = {"segmentor": None, "tok": None, "device": None,
                 "seg_map": None, "stats_path": None}


def _resolve_s0_checkpoint() -> str:
    p = os.environ.get("R3_VTILE_S0_CKPT")
    if not p:
        root = Path(__file__).resolve().parents[3]
        cfg = json.loads((root / "configs" / "canonical_v37.json").read_text(
            encoding="utf-8"))
        p = cfg["init_checkpoint"]
    if not Path(p).exists():
        raise RuntimeError(f"[r3-c3] S0'' 段界器权重缺席：{p}——停报")
    return p


def _load_for_c3(model_path, device):
    model, tok, fp = r3.load_model_and_tokenizer_local(model_path, device)
    if r3.config_has_vtile(model.config):
        raise RuntimeError("[r3-c3] 底物带 r3_vtile 戳记——c3 口径=模型不动，"
                           "只对齐仪器跨段定义（应喂母列 ckpt）——停报")
    s0 = _resolve_s0_checkpoint()
    _HOLDER["segmentor"] = r3.load_s0_segmentor(s0, device=str(device))
    _HOLDER["tok"] = tok
    _HOLDER["device"] = str(device)
    fp["r3_c3"] = {
        "construction": "cross-segment definition aligned to S0'' cut points "
                        "(selection semantics only; model untouched, no vtile "
                        "patch, zero training)",
        "s0_checkpoint": s0,
        "s0_seq_len": r3.VTILE_S0_SEQ_LEN,
        "s0_max_chunks": r3.VTILE_S0_MAX_CHUNKS,
        "audit_fields_note": "items 的 source_segment/repeat_segment 仍按原生 "
                             "segment-tokens 网格记（描述字段，不进计分）",
        "reading_class": "附属读数（机制注记，不判负正，不改主判决口径）",
    }
    print(f"[r3-c3] 评测侧对齐已接通：S0'' 段界器就位（{s0}），模型零改动"
          "（母列原样，无 vtile patch）", flush=True)
    return model, tok, fp


def _cross_segment_occurrences_s0(ids: list[int], n: int, seg_tokens: int):
    """仪器选择链接缝的 S0'' 对齐版：段号 = holder 当前窗映射表（S0'' 切点），
    其余逻辑（最早出现段严格在前才算跨段重复）逐字镜像仪器本体。
    seg_tokens 形参保留签名兼容、不参与计算。holder 缺席 = 响亮停报。"""
    seg_map = _HOLDER["seg_map"]
    if seg_map is None or len(seg_map) != len(ids):
        raise RuntimeError("[r3-c3] 跨段判定缺 S0'' 段号映射（或长度不齐 "
                           f"{None if seg_map is None else len(seg_map)} != "
                           f"{len(ids)}）——静默回落原生网格即口径漂移，停报")
    first_seg: dict[tuple, int] = {}
    occ: dict[tuple, list[int]] = {}
    for p in range(0, len(ids) - n + 1):
        g = tuple(ids[p:p + n])
        c = seg_map[p]
        fc = first_seg.get(g)
        if fc is None:
            first_seg[g] = c
        elif fc < c:
            occ.setdefault(g, []).append(p)
    return occ


def _run_window_with_c3(model, ids, scan, rng, table, pool, v, window_id, **kw):
    if _HOLDER["stats_path"] is None:
        out_dir = Path(getattr(scan, "out_dir", "."))
        out_dir.mkdir(parents=True, exist_ok=True)
        _HOLDER["stats_path"] = str(out_dir / "c3_window_stats.jsonl")
    with Path(scan.corpus).open("rb") as f:
        f.seek(int(scan.window_bytes) * int(window_id))
        raw = f.read(int(scan.window_bytes))
    if len(raw) != int(scan.window_bytes):
        raise RuntimeError(f"[r3-c3] 窗 {window_id} 不足整窗（{len(raw)}B）——停报")
    plan, stats = r3.vtile_plan_for_window(
        _HOLDER["segmentor"], _HOLDER["tok"], raw, t_total=len(ids),
        device=_HOLDER["device"])
    with open(_HOLDER["stats_path"], "a", encoding="utf-8") as fa:
        fa.write(json.dumps({"window_id": window_id, **stats}) + "\n")
    _HOLDER["seg_map"] = [i for i, ln in enumerate(plan) for _ in range(ln)]
    try:
        return _orig_run_window(model, ids, scan, rng, table, pool, v,
                                window_id, **kw)
    finally:
        _HOLDER["seg_map"] = None


e122.load_model_and_tokenizer = _load_for_c3
e122.run_window = _run_window_with_c3
e122.cross_segment_occurrences = _cross_segment_occurrences_s0

if __name__ == "__main__":
    raise SystemExit(e122.main())
