"""R3 丙臂判决仪器启动器：probe_e122_deltanet_book 之上注入变长铺瓦装载与逐窗计划。

纪律（任务书 §3.6/点火令）：**仪器零口径改动**——本体文件
``tools/analysis/cross_arch/probe_e122_deltanet_book.py`` 一字节不改（施工回执
附 sha256），本启动器只替换其两个模块级函数（甲臂启动器同范式，仅装载路径 +
每窗计划注入，窗/选择链/手术/bootstrap/种子全走仪器本体）：

- ``load_model_and_tokenizer``：checkpoint config 带 ``r3_vtile.enabled``（丙臂）
  → attach 变长铺瓦 patch（r3_spec.attach_vtile）+ 键集全等校验 strict 重载
  （r3_spec.verify_vtile_reload，丙零新增参数→键集=基座全等）+ S0'' 段界器就位；
  无该字段（R2 母列/对照底物）→ 原装载路径原样返回。
- ``run_window``：进窗前按 window_id 从语料直读窗字节 → S0'' 切点 → token 计划
  （r3_spec.vtile_plan_for_window），设计划后委托原 run_window，finally 清计划
  （a 基线与 b1 手术臂共用同一计划：等长 gram 替换保持 T 与位置，计划按位置
  索引在两臂间精确迁移）。逐窗 S0'' 切点统计落 ``<out-dir>/vtile_window_stats
  .jsonl``（门②直测复核 ≈172.7 的存档副产物）。

S0'' 权重解析：环境变量 ``R3_VTILE_S0_CKPT`` 优先，缺省读
``configs/canonical_v37.json`` 的 init_checkpoint（任务书 §2.3 口径）；缺席响亮。

Usage（形态与母列收盘逐字同构，仅换启动器与 checkpoint）:
  python tools/baselines/deltanet_r2/probe_r3_vtile_book.py \
      --model-path outputs/r3_transplant_vtile_20260914/main20k_vtile/latest \
      --corpus /workspace/corpus/corpus_v3.txt \
      --n-windows 500 --start-window 0 --seed 424242 --device cuda \
      --out-dir outputs/r3_transplant_vtile_20260914/verdict_b0
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import tools.analysis.cross_arch.probe_e122_deltanet_book as e122  # noqa: E402
import tools.baselines.deltanet_r2.r2_spec as r2spec  # noqa: E402
import tools.baselines.deltanet_r2.r3_spec as r3  # noqa: E402

_orig_run_window = e122.run_window

_HOLDER: dict = {"segmentor": None, "tok": None, "device": None,
                 "plan_cache": {}, "stats_path": None}


def _resolve_s0_checkpoint() -> str:
    p = os.environ.get("R3_VTILE_S0_CKPT")
    if not p:
        root = Path(__file__).resolve().parents[3]
        cfg = json.loads((root / "configs" / "canonical_v37.json").read_text(
            encoding="utf-8"))
        p = cfg["init_checkpoint"]
    if not Path(p).exists():
        raise RuntimeError(f"[r3-vtile] S0'' 段界器权重缺席：{p}——停报")
    return p


def _load_with_r3_vtile(model_path, device):
    # 本地 5080 env 无 accelerate：装载走 r3_spec 本地等价装载器（device_map →
    # .to，单卡放置等价；shim/规范化/fingerprint 全保留），丙字段照常接通
    model, tok, fp = r3.load_model_and_tokenizer_local(model_path, device)
    if r3.config_has_vtile(model.config):
        s0 = _resolve_s0_checkpoint()
        report = r3.attach_and_reload_vtile(model, model_path, s0,
                                            device=str(device))
        segmentor = report.pop("segmentor")
        fp["r3_vtile"] = report
        _HOLDER["segmentor"] = segmentor
        _HOLDER["tok"] = tok
        _HOLDER["device"] = str(device)
        print(f"[r3-vtile] 变长铺瓦已接通（键集全等 {report['n_keys']} 键，参数锚 "
              f"{r2spec.EXPECTED_PARAM_COUNT:,} 零新增）+ S0'' 段界器就位（{s0}）",
              flush=True)
    else:
        print("[r3-vtile] checkpoint 无 r3_vtile 字段——按原路径装载"
              "（母列/对照底物）", flush=True)
    return model, tok, fp


def _plan_for(scan, window_id: int, ids: list[int]) -> list[int]:
    key = (str(scan.corpus), int(scan.window_bytes), int(window_id), len(ids))
    hit = _HOLDER["plan_cache"].get(key)
    if hit is not None:
        return hit
    with Path(scan.corpus).open("rb") as f:
        f.seek(int(scan.window_bytes) * int(window_id))
        raw = f.read(int(scan.window_bytes))
    if len(raw) != int(scan.window_bytes):
        raise RuntimeError(f"[r3-vtile] 窗 {window_id} 不足整窗（{len(raw)}B）——停报")
    plan, stats = r3.vtile_plan_for_window(
        _HOLDER["segmentor"], _HOLDER["tok"], raw, t_total=len(ids),
        device=_HOLDER["device"])
    if _HOLDER["stats_path"] is not None:
        with open(_HOLDER["stats_path"], "a", encoding="utf-8") as fa:
            fa.write(json.dumps({"window_id": window_id, **stats}) + "\n")
    _HOLDER["plan_cache"][key] = plan
    return plan


def _run_window_with_vtile(model, ids, scan, rng, table, pool, v, window_id,
                           **kw):
    if _HOLDER["segmentor"] is None:
        return _orig_run_window(model, ids, scan, rng, table, pool, v,
                                window_id, **kw)
    if _HOLDER["stats_path"] is None:
        out_dir = Path(getattr(scan, "out_dir", "."))
        out_dir.mkdir(parents=True, exist_ok=True)
        _HOLDER["stats_path"] = str(out_dir / "vtile_window_stats.jsonl")
    plan = _plan_for(scan, window_id, ids)
    r3.set_vtile_plan(plan)
    try:
        return _orig_run_window(model, ids, scan, rng, table, pool, v,
                                window_id, **kw)
    finally:
        r3.clear_vtile_plan()


e122.load_model_and_tokenizer = _load_with_r3_vtile
e122.run_window = _run_window_with_vtile

if __name__ == "__main__":
    raise SystemExit(e122.main())
