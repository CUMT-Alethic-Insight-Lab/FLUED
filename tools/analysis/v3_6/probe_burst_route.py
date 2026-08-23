"""Q13 路由归因仪表（判读矩阵第四格配套，prereg §7，2026-08-22，零训练纯评测）。

判读矩阵格四的前置裁决（禁止跳层：路由未归因前第四格不许落判词）：
每条 eval 样本构造 burst 文档（训练侧 _splice_burst 同构造器：现采 32-64B
语料段 ×R=3 随机位置插入，第 R 次出现末 2-4 字遮蔽），四臂同窗同 mask
同计分：

  intact      ：原样（答案 = 第 R 次遮蔽段尾的可读性）；
  state_zero  ：状态读出行置零——实例级包裹 ``_slm_store_rows``，把 backbone
                输入的 k_rows（b 格 = K 通道状态读出行 package_k.mean(dim=2)，
                fork 2 多视图时连同 k_store）置零；memory/index 行不动。
                口径注记：只在 k_row_source=="state"（b/d 格）有意义；a/c 格
                k_rows 是 index 行（非状态读出），该臂记 N/A 不参评；
  early_masked：前 R−1 次出现全部遮蔽（窗内复制路由切断，盖过构造器的
                force-unmask 覆写）；
  both_zero   ：双臂同切（对照列）。

判读（§7 冻结）：state_zero 答案死而 early_masked 活 → 路由在状态通道；
反之 → 窗内复制；两都死 → 混合/不明；两臂分报互不代报。"答案死"可操作化：
臂 byte_acc 相对 intact 跌 ≥0.10（沿用有效性门边际家族，仪表内部口径，
不进任何判据文本）。逐条目审计列：预测时刻是否存在窗内可见副本（metas
的 occurrences[:-1] 是否全部落在 chunk 网格内且在 intact 臂可见——构造
器 force-unmask 保证可见性，故审计 = 网格可达性）；聚合按该标记分列。

Usage:
  python tools/analysis/v3_6/probe_burst_route.py --device cuda --run-dir <Q13_run_dir>
  CPU 冒烟: py -3.14 -X utf8 tools/analysis/v3_6/probe_burst_route.py --device cpu --run-dir <tiny_ckpt> --max-items 2
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import torch

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from flued.data import MASK_ID  # noqa: E402
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402
from tools.analysis.v3_6.probe_oracle_write_verdict import (  # noqa: E402
    build_eval_windows,
    load_model,
)

DEFAULT_RUN = "checkpoints/v37ks_b_sm_burst_20k_20260822"  # Q13 训练收官后的正式跑数对象（占位）
OUT_DIR = "outputs/burst_route_20260822"
SPLICE_SEED = 20260822
DEAD_MARGIN = 0.10  # "答案死" 可操作化边际（intact − 臂 ≥ 此值记死；仪表内部口径）


def _patch_state_zero(model):
    """state_zero 臂: instance-level wrap of ``_slm_store_rows`` zeroing the
    K-channel state readout rows (k_rows, and k_store when fork 2 multi-view
    rows exist) handed to the backbone; V 行与 memory/index 不动. Returns a
    restore() callable (deleting the instance attr un-shadows the class
    method)."""
    orig = model._slm_store_rows  # bound method

    def wrapped(chunks, with_views=False):
        rows = list(orig(chunks, with_views=with_views))
        rows[0] = torch.zeros_like(rows[0])  # k_rows: b 格 K 通道状态读出行
        if with_views and rows[5] is not None:
            rows[5] = torch.zeros_like(rows[5])  # k_store (readout_views>1)
        return tuple(rows)

    model._slm_store_rows = wrapped

    def restore():
        del model._slm_store_rows

    return restore


@torch.no_grad()
def run_arm(model, ids, meta, arm: str, device, mask_seed: int, state_zero_ok: bool):
    """One arm over one burst window: forward, score the masked-tail slots
    (byte_acc + exact, same completion logits / same normalization as the
    retrieval echo scoring). arm in {intact, state_zero, early_masked,
    both_zero}; mask_seed is per-window and SHARED by all four arms."""
    ids = ids.unsqueeze(0).to(device)
    byte_mask = s1.make_mixed_mask(
        ids.cpu(), 0.05, char_frac=0.4, char_span_max=3,
        tokenizer=s1._BPE_TOKENIZER, generator=torch.Generator().manual_seed(mask_seed),
    ).to(device)
    byte_mask = s1._burst_mask_overrides(byte_mask, [meta])
    if arm in ("early_masked", "both_zero"):
        for lo, hi in meta["occurrences"][:-1]:
            byte_mask[0, lo:hi] = True  # 窗内复制路由切断 (盖过 force-unmask)
    source = ids.masked_fill(byte_mask, MASK_ID)
    restore = None
    if arm in ("state_zero", "both_zero"):
        if not state_zero_ok:
            return None  # a/c 格: k_rows 非状态读出行, 此臂 N/A
        restore = _patch_state_zero(model)
    try:
        out = model(source)
    finally:
        if restore is not None:
            restore()
    chunks = out.chunks
    slot, active = s1._cloze_slot_grid(
        [meta], chunks.chunk_ids, chunks.offsets, model.config.max_chunks, model.config.max_span
    )
    if not bool(active[0]):
        return None  # 遮蔽段尾被挤出网格: 条目不激活
    targets, _sm, _m2 = s1.make_targets(
        ids, torch.zeros_like(byte_mask), chunks.chunk_ids, chunks.offsets,
        model.config.max_chunks, model.config.max_span,
    )
    pred = out.logits_backbone.argmax(dim=-1)
    echo = slot[0]
    hits = pred[0][echo] == targets[0][echo]
    byte_acc = float(hits.float().mean()) if int(echo.sum()) else 0.0
    exact = bool(hits.all()) and int(echo.sum()) > 0
    # 审计列 (§7.2): 预测时刻窗内可见副本是否存在 = 前 R-1 次出现全部落在
    # chunk 网格内 (intact 臂里它们被 force-unmask, 网格可达即可见)
    copy_visible = True
    for lo, hi in meta["occurrences"][:-1]:
        j = chunks.chunk_ids[0, lo:hi]
        if not bool(j.ge(0).all()):
            copy_visible = False
            break
    return {"byte_acc": byte_acc, "exact": exact, "n_echo": int(echo.sum()), "copy_visible": copy_visible}


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    p = argparse.ArgumentParser()
    p.add_argument("--run-dir", default=DEFAULT_RUN)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--max-items", type=int, default=48)
    p.add_argument("--out-dir", default=OUT_DIR)
    args = p.parse_args()
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    model, ns, step = load_model(Path(args.run_dir), device)
    if s1._BPE_TOKENIZER is None:
        s1._load_bpe_tokenizer(ns.bpe_tokenizer_path)
    state_zero_ok = getattr(model.config, "k_row_source", "memory") == "state"
    sampler = s1.CorpusSampler(ns.data_path)  # 现采随机段 (防背: 与训练同纪律)
    windows = build_eval_windows(ns, args.max_items * 2)  # oversample: inactive rows skipped
    print(
        f"[route] model={Path(args.run_dir).name} step={step} device={device.type} "
        f"k_row_source={model.config.k_row_source} state_zero_arm={'on' if state_zero_ok else 'N/A'} "
        f"({time.time() - t0:.0f}s)",
        flush=True,
    )

    gen = torch.Generator().manual_seed(SPLICE_SEED)
    items = []
    for wi, clean in enumerate(windows):
        if len(items) >= args.max_items:
            break
        spliced, metas = s1._splice_burst(
            clean, 1.0, gen, sampler,
            s1._BURST_REPEAT_FROZEN, s1._BURST_TAIL_MAX_CHARS,
        )
        m = metas[0]
        if m is None:
            continue
        ids = spliced[0]
        rec = {
            "window": wi,
            "answer": m["answer_b"].decode("utf-8", errors="replace"),
            "seg_offset": m["seg_offset"],
            "seg_len": m["seg_len"],
            "occurrences": [list(o) for o in m["occurrences"]],
            "echo_span": list(m["echo_span"]),
            "tail_chars": m["tail_chars"],
        }
        skip = False
        for arm in ("intact", "state_zero", "early_masked", "both_zero"):
            r = run_arm(model, ids, m, arm, device, 1042 + wi, state_zero_ok)
            if arm != "state_zero" and r is None:
                skip = True  # echo off-grid: item inactive (state_zero N/A 不算)
                break
            rec[arm] = r
        if skip:
            continue
        rec["copy_visible"] = rec["intact"]["copy_visible"]
        items.append(rec)
        if len(items) % 8 == 0:
            print(f"[route] items {len(items)}/{args.max_items} ({time.time() - t0:.0f}s)", flush=True)

    n = len(items)

    def agg(rows, arm, key):
        vals = [r[arm][key] for r in rows if r.get(arm) is not None]
        return round(sum(vals) / len(vals), 4) if vals else None

    arms = ("intact", "state_zero", "early_masked", "both_zero")
    acc = {arm: agg(items, arm, "byte_acc") for arm in arms}
    exact = {arm: agg(items, arm, "exact") for arm in arms}
    # 分列聚合 (§7.2): 按窗内副本存在标记
    by_copy = {}
    for flag in (True, False):
        rows = [r for r in items if r["copy_visible"] == flag]
        by_copy[str(flag)] = {
            "n": len(rows),
            **{arm: agg(rows, arm, "byte_acc") for arm in arms},
        }

    # 判读 (§7 冻结矩阵, 两臂分报互不代报): 死 = intact − 臂 ≥ DEAD_MARGIN
    verdict = "n=0: 无激活条目, 不落判词。"
    if n and acc["intact"] is not None:
        base = acc["intact"]
        state_dead = acc["state_zero"] is not None and (base - acc["state_zero"]) >= DEAD_MARGIN
        early_dead = acc["early_masked"] is not None and (base - acc["early_masked"]) >= DEAD_MARGIN
        if acc["state_zero"] is None:
            verdict = (
                f"state_zero 臂 N/A (k_row_source={model.config.k_row_source}, 非 b/d 格): "
                f"early_masked {'死' if early_dead else '活'} (intact {base:.4f} -> "
                f"{acc['early_masked']:.4f})。状态通道侧需在 b/d 格 checkpoint 上复测, 本表不落路由判词。"
            )
        elif state_dead and not early_dead:
            verdict = (f"路由在状态通道: state_zero 答案死 ({base:.4f} -> {acc['state_zero']:.4f}), "
                       f"early_masked 活 ({acc['early_masked']:.4f})。第四格第一层归因完成——路由挂状态通道。")
        elif early_dead and not state_dead:
            verdict = (f"路由在窗内复制: early_masked 答案死 ({base:.4f} -> {acc['early_masked']:.4f}), "
                       f"state_zero 活 ({acc['state_zero']:.4f})。第四格判词候选: 分配跟随需求沿最便宜通道兑现。")
        elif state_dead and early_dead:
            verdict = (f"混合/不明: 双臂皆死 (state_zero {acc['state_zero']:.4f}, "
                       f"early_masked {acc['early_masked']:.4f}, intact {base:.4f})。如实登记, 不代报。")
        else:
            verdict = (f"两臂皆不死 (state_zero {acc['state_zero']:.4f}, early_masked "
                       f"{acc['early_masked']:.4f}, intact {base:.4f}): 答案不靠任一单路由 "
                       f"(先验可猜/冗余双路由), 如实登记, 不代报。")

    report = {
        "probe": "Q13 路由归因仪表（判读矩阵第四格配套, prereg §7）",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "checkpoint": {"run": Path(args.run_dir).name, "step": step},
        "params": {"n_items": n, "splice_seed": SPLICE_SEED, "dead_margin": DEAD_MARGIN,
                   "k_row_source": model.config.k_row_source},
        "arms": {"intact": "原样", "state_zero": "状态读出行置零 (k_rows/k_store)",
                 "early_masked": "前 R-1 次出现遮蔽 (窗内复制切断)", "both_zero": "双臂同切 (对照)"},
        "byte_acc": acc, "exact": exact,
        "by_copy_visible": by_copy,
        "verdict": verdict,
        "items": items,
        "timing_sec": round(time.time() - t0, 1),
    }
    out_path = out_dir / "burst_route.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    def fmt(v):
        return "N/A" if v is None else f"{v:.4f}"

    lines = [
        "Q13 路由归因仪表（判读矩阵第四格配套）",
        f"日期 {report['created']}  设备 {device.type}  n={n}  checkpoint={Path(args.run_dir).name} (step {step})",
        "",
        f"byte_acc：intact {fmt(acc['intact'])} | state_zero {fmt(acc['state_zero'])} | "
        f"early_masked {fmt(acc['early_masked'])} | both_zero {fmt(acc['both_zero'])}",
        f"exact   ：intact {fmt(exact['intact'])} | state_zero {fmt(exact['state_zero'])} | "
        f"early_masked {fmt(exact['early_masked'])} | both_zero {fmt(exact['both_zero'])}",
        "",
        f"分列 (窗内副本存在): 有 n={by_copy['True']['n']} intact={fmt(by_copy['True']['intact'])} | "
        f"无 n={by_copy['False']['n']} intact={fmt(by_copy['False']['intact'])}",
        "",
        f"判词：{verdict}",
        "",
        f"完整数据: {out_path}",
    ]
    (out_dir / "SUMMARY.txt").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
