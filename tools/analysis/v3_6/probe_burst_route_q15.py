"""Q15 收官评测探针（任务书 §6 主终点 + 路由消融，2026-08-25，零训练纯评测）。

probe_burst_route.py（Q13/Q14 路由探针，原文一字不动保留历史可比性）的
Q15 变体。每条 eval 样本构造 burst 文档（训练侧 _splice_burst 同构造器：
现采 32-64B 语料段 ×R=3 随机位置插入，第 R 次出现末 2-4 字遮蔽），六臂
同窗同 mask 同计分，**所有臂带压缩区剔除**（任务书 §7.2：剔除是任务定义，
train/eval 同开——经 s1_forward 的 burst_metas_q15 传入，_burst_store_block
按 meta 在 _slm_forward 内自动构建）：

  intact        ：原样（答案 = 第 R 次遮蔽段尾的可读性）；
  src_scrambled ：Δ 主终点的置乱臂（§6）——occurrences 1..R−1 的段尾 tb
                  字节做 head-tail swap 篡改，直接复用训练侧
                  ``s1._burst_twin_bytes``（与 L_couple 孪生同一扰动，口径
                  一致是设计有意）；
  kstate_zero   ：d 格 K 通道状态读出行置零（k_rows/k_store）；
  vstate_zero   ：d 格 V 通道状态读出行置零（v_rows/v_store；口径注记:
                  v_rows 同时是 direct 的解码侧条件行, 本表只计 backbone
                  echo 槽位, direct 侧变化不进读数）；
  bothstate_zero：双通道同清（状态侧对照列）；
  early_masked  ：前 R−1 次出现全部遮蔽（窗内复制路由切断，原语义保留）。

通道存在性按 model.config.k_row_source/v_row_source == "state" 分别判定；
非 state 通道的臂记 N/A（None）不参评（d 格双臂皆 on）。

主终点（§6）：逐条目 Δ_i = byte_acc(intact) − byte_acc(src_scrambled)，
n=48 逐条目全量记录再聚合，报 mean ± 95% CI（正态近似 1.96·sd/√n）。
审计列：``swap_identity``（段首 tb 字节 == 段尾 tb 字节时篡改为恒等——
该条目置乱臂与完好臂逐字节同文，从 Δ 聚合剔除并单列计数）与
``copy_visible``（窗内副本存在，沿用原探针：前 R−1 次出现全部落在 chunk
网格内即可见——构造器 force-unmask 保证）。路由消融各臂的 intact 相对跌
幅只作机制叙事对照列（§6：供机制叙事，判词归判读矩阵四格会合后落）。

Usage:
  python tools/analysis/v3_6/probe_burst_route_q15.py --device cuda --ckpt <Q15_run_dir>
  CPU 冒烟: py -3.14 -X utf8 tools/analysis/v3_6/probe_burst_route_q15.py --device cpu --ckpt <tiny_ckpt> --max-items 2
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

from flued.data import MASK_ID, PAD_ID  # noqa: E402
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402
from tools.analysis.v3_6.probe_oracle_write_verdict import (  # noqa: E402
    build_eval_windows,
    load_model,
)

DEFAULT_CKPT = "checkpoints/v37ks_d_sm_q15_rearing_20k_ctx4096_20260825"  # Q15 训练收官后的正式跑数对象（占位）
OUT_DIR = "outputs/q15_delta_20260825"
SPLICE_SEED = 20260825  # Q15 变体独立种子流 (与 Q13/Q14 探针 20260822 串不混)
ARMS = ("intact", "src_scrambled", "kstate_zero", "vstate_zero", "bothstate_zero", "early_masked")
STATE_ARMS = {"kstate_zero": ("k",), "vstate_zero": ("v",), "bothstate_zero": ("k", "v")}


def _patch_state_zero(model, channels=("k",)):
    """Q15 d 格拆分 (任务书 §6): 按通道把 backbone 输入的状态读出行置零 --
    channels 含 "k" 清 k_rows(+k_store), 含 "v" 清 v_rows(+v_store);
    memory/index 行不动. 实例级包裹 ``_slm_store_rows``; 返回 restore()
    (删实例属性即还原类方法)."""
    orig = model._slm_store_rows
    zk, zv = "k" in channels, "v" in channels

    def wrapped(chunks, with_views=False):
        rows = list(orig(chunks, with_views=with_views))
        if zk:
            rows[0] = torch.zeros_like(rows[0])  # k_rows: K 通道状态读出行
            if with_views and rows[5] is not None:
                rows[5] = torch.zeros_like(rows[5])  # k_store (readout_views>1)
        if zv:
            rows[1] = torch.zeros_like(rows[1])  # v_rows: V 通道状态读出行
            if with_views and rows[6] is not None:
                rows[6] = torch.zeros_like(rows[6])  # v_store
        return tuple(rows)

    model._slm_store_rows = wrapped

    def restore():
        del model._slm_store_rows

    return restore


def _swap_identity(raw: bytes, meta: dict) -> bool:
    """审计列 (任务书 §6): head-tail swap 篡改为恒等当且仅当孪生与原文逐字节
    相同 (段首 tb 字节 == 各被篡改段尾 tb 字节). True 条目从 Δ 聚合剔除并
    单列计数."""
    return s1._burst_twin_bytes(raw, meta) == raw


def _delta_aggregate(items: list) -> dict:
    """主终点聚合 (§6): 逐条目 Δ_i = byte_acc(intact) − byte_acc(src_scrambled);
    swap_identity 条目剔除单列; mean ± 95% CI (正态近似 1.96·sd/√n, n>1 时
    sd 为样本标准差)."""
    excluded = sum(1 for r in items if r["swap_identity"])
    deltas = [
        r["intact"]["byte_acc"] - r["src_scrambled"]["byte_acc"]
        for r in items
        if not r["swap_identity"] and r.get("intact") and r.get("src_scrambled")
    ]
    n = len(deltas)
    mean = sum(deltas) / n if n else 0.0
    sd = (sum((d - mean) ** 2 for d in deltas) / (n - 1)) ** 0.5 if n > 1 else 0.0
    ci = 1.96 * sd / (n ** 0.5) if n else 0.0
    return {
        "n": n,
        "mean": round(mean, 4),
        "ci95": round(ci, 4),
        "n_swap_identity_excluded": excluded,
        "ci_excludes_zero": bool(n) and (mean - ci > 0 or mean + ci < 0),
    }


@torch.no_grad()
def run_arm(model, ids_orig: torch.Tensor, meta: dict, arm: str, device, mask_seed: int, ns, kstate_ok: bool, vstate_ok: bool, excise: bool = True):
    """One arm over one burst window: forward (压缩区剔除经 burst_metas_q15
    同开; excise=False = 无剔除形态, 规模轴 canonical 臂收官用——该口径对象
    无剔除训练史, 剔除会结构性压死直通格的内容路径), score the masked-tail
    slots (byte_acc + exact, cloze 同 schema).
    宽度纪律 (实跑事故修订): 入口先把拼接行剥到有效前缀 -- 批宽来自批内最长
    行, row 0 带 PAD 尾时 mask 与 scrambled 臂的 twin 行 (剥尾字节重建) 宽度
    会错位; 剥尾后 mask 锚在 intact 形态的有效内容上 (make_mixed_mask 内部
    本就按行剥 PAD 再抽签, 剥不剥 draw 流逐比特相同), 六臂共享 1042+wi
    种子的同一 mask; src_scrambled 是等长字节替换, mask 直接适用."""
    ids_orig = ids_orig[ids_orig.ne(PAD_ID)]  # 剥 PAD 尾: 宽度 = 有效内容
    ids_arm = ids_orig
    if arm == "src_scrambled":
        raw = bytes(int(x) - 1 for x in ids_orig.tolist())
        twin = s1._burst_twin_bytes(raw, meta)
        ids_arm = torch.tensor([b + 1 for b in twin], dtype=ids_orig.dtype)
    ids_b = ids_arm.unsqueeze(0).to(device)
    byte_mask = s1.make_mixed_mask(
        ids_orig.unsqueeze(0).cpu(), 0.05, char_frac=0.4, char_span_max=3,
        tokenizer=s1._BPE_TOKENIZER, generator=torch.Generator().manual_seed(mask_seed),
    ).to(device)
    byte_mask = s1._burst_mask_overrides(byte_mask, [meta])
    if arm == "early_masked":
        for lo, hi in meta["occurrences"][:-1]:
            byte_mask[0, lo:hi] = True  # 窗内复制路由切断 (盖过 force-unmask)
    source = ids_b.masked_fill(byte_mask, MASK_ID)
    restore = None
    if arm in STATE_ARMS:
        channels = STATE_ARMS[arm]
        if ("k" in channels and not kstate_ok) or ("v" in channels and not vstate_ok):
            return None  # 非 state 通道: 此臂 N/A
        restore = _patch_state_zero(model, channels)
    try:
        out = s1.s1_forward(model, source, ns, burst_metas_q15=[meta] if excise else None)  # 剔除同开 (§7.2) / 无剔除形态
    finally:
        if restore is not None:
            restore()
    chunks = out["chunks"]
    slot, active = s1._cloze_slot_grid(
        [meta], chunks.chunk_ids, chunks.offsets, model.config.max_chunks, model.config.max_span
    )
    if not bool(active[0]):
        return None  # 遮蔽段尾被挤出网格: 条目不激活
    targets, _sm, _m2 = s1.make_targets(
        ids_b, torch.zeros_like(byte_mask), chunks.chunk_ids, chunks.offsets,
        model.config.max_chunks, model.config.max_span,
    )
    pred = out["logits_backbone"].argmax(dim=-1)
    echo = slot[0]
    hits = pred[0][echo] == targets[0][echo]
    byte_acc = float(hits.float().mean()) if int(echo.sum()) else 0.0
    exact = bool(hits.all()) and int(echo.sum()) > 0
    # 审计列: 预测时刻窗内可见副本是否存在 = 前 R-1 次出现全部落在 chunk
    # 网格内 (intact 臂里它们被 force-unmask, 网格可达即可见)
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
    p.add_argument("--ckpt", default=DEFAULT_CKPT, help="Q15 run dir (resolved_config.json + latest.pt)")
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--max-items", type=int, default=48)
    p.add_argument("--out-dir", default=OUT_DIR)
    p.add_argument("--no-excision", action="store_true",
                   help="无剔除形态 (规模轴 canonical 臂收官口径: 对象无剔除训练史, 剔除会结构性压死直通格内容路径)")
    args = p.parse_args()
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    model, ns, step = load_model(Path(args.ckpt), device)
    if s1._BPE_TOKENIZER is None:
        s1._load_bpe_tokenizer(ns.bpe_tokenizer_path)
    kstate_ok = getattr(model.config, "k_row_source", "memory") == "state"
    vstate_ok = getattr(model.config, "v_row_source", "memory") == "state"
    sampler = s1.CorpusSampler(ns.data_path)  # 现采随机段 (防背: 与训练同纪律)
    windows = build_eval_windows(ns, args.max_items * 2)  # oversample: inactive rows skipped
    print(
        f"[q15-delta] model={Path(args.ckpt).name} step={step} device={device.type} "
        f"k_row_source={model.config.k_row_source} v_row_source={model.config.v_row_source} "
        f"state_arms=(k:{'on' if kstate_ok else 'N/A'},v:{'on' if vstate_ok else 'N/A'}) "
        f"({time.time() - t0:.0f}s)",
        flush=True,
    )

    gen = torch.Generator().manual_seed(SPLICE_SEED)
    items = []
    items_path = out_dir / "items.jsonl"
    items_fp = items_path.open("w", encoding="utf-8")
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
        raw = bytes(int(x) - 1 for x in ids.tolist() if int(x) != PAD_ID)
        rec = {
            "window": wi,
            "answer": m["answer_b"].decode("utf-8", errors="replace"),
            "seg_offset": m["seg_offset"],
            "seg_len": m["seg_len"],
            "occurrences": [list(o) for o in m["occurrences"]],
            "echo_span": list(m["echo_span"]),
            "tail_chars": m["tail_chars"],
            "swap_identity": _swap_identity(raw, m),  # 审计列: 恒等篡改条目
        }
        skip = False
        for arm in ARMS:
            r = run_arm(model, ids, m, arm, device, 1042 + wi, ns, kstate_ok, vstate_ok, excise=not args.no_excision)
            if arm not in STATE_ARMS and r is None:
                skip = True  # echo off-grid: item inactive (state 臂 N/A 不算)
                break
            rec[arm] = r
        if skip:
            continue
        rec["copy_visible"] = rec["intact"]["copy_visible"]
        rec["delta"] = round(rec["intact"]["byte_acc"] - rec["src_scrambled"]["byte_acc"], 4)
        items.append(rec)
        items_fp.write(json.dumps(rec, ensure_ascii=False) + "\n")
        items_fp.flush()
        if len(items) % 8 == 0:
            print(f"[q15-delta] items {len(items)}/{args.max_items} ({time.time() - t0:.0f}s)", flush=True)
    items_fp.close()

    n = len(items)

    def agg(rows, arm, key):
        vals = [r[arm][key] for r in rows if r.get(arm) is not None]
        return round(sum(vals) / len(vals), 4) if vals else None

    acc = {arm: agg(items, arm, "byte_acc") for arm in ARMS}
    exact = {arm: agg(items, arm, "exact") for arm in ARMS}
    delta = _delta_aggregate(items)
    # 分列聚合: 按窗内副本存在标记 (机制叙事对照)
    by_copy = {}
    for flag in (True, False):
        rows = [r for r in items if r["copy_visible"] == flag]
        by_copy[str(flag)] = {"n": len(rows), **{arm: agg(rows, arm, "byte_acc") for arm in ARMS}}

    # 描述性结论 (不落判词: 判读矩阵四格需 mass/d 列会合后由主会话裁定)
    if not n:
        verdict = "n=0: 无激活条目, 不落读数。"
    elif delta["ci_excludes_zero"] and delta["mean"] > 0:
        verdict = (f"Δ = {delta['mean']:.4f} ± {delta['ci95']:.4f}（95% CI 不含 0, n={delta['n']}，"
                   f"恒等篡改剔除 {delta['n_swap_identity_excluded']} 条）——主终点 Δ 张开；"
                   "判读矩阵落格（格一/格四）待注意力 mass 与孪生 d 列会合。")
    else:
        verdict = (f"Δ = {delta['mean']:.4f} ± {delta['ci95']:.4f}（CI 含 0 或 n=0, n={delta['n']}，"
                   f"恒等篡改剔除 {delta['n_swap_identity_excluded']} 条）——主终点 Δ 未张开。")

    report = {
        "probe": "Q15 收官评测探针（§6 主终点逐条目 Δ + d 格路由消融六臂）",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "checkpoint": {"run": Path(args.ckpt).name, "step": step},
        "params": {"n_items": n, "splice_seed": SPLICE_SEED,
                   "k_row_source": model.config.k_row_source,
                   "v_row_source": model.config.v_row_source},
        "arms": {"intact": "原样（剔除同开）", "src_scrambled": "置乱臂 (head-tail swap, Δ 减数)",
                 "kstate_zero": "K 通道状态读出行置零", "vstate_zero": "V 通道状态读出行置零",
                 "bothstate_zero": "双通道同清 (对照)", "early_masked": "前 R-1 次出现遮蔽 (窗内复制切断)"},
        "byte_acc": acc, "exact": exact,
        "delta": delta,
        "by_copy_visible": by_copy,
        "verdict": verdict,
        "items_path": str(items_path),
        "timing_sec": round(time.time() - t0, 1),
    }
    out_path = out_dir / "summary.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    def fmt(v):
        return "N/A" if v is None else f"{v:.4f}"

    lines = [
        "Q15 收官评测探针（§6 主终点逐条目 Δ，六臂全带压缩区剔除）",
        f"日期 {report['created']}  设备 {device.type}  n={n}  checkpoint={Path(args.ckpt).name} (step {step})",
        "",
        "byte_acc：" + " | ".join(f"{arm} {fmt(acc[arm])}" for arm in ARMS),
        "exact   ：" + " | ".join(f"{arm} {fmt(exact[arm])}" for arm in ARMS),
        "",
        f"主终点 Δ = intact − src_scrambled: {delta['mean']:.4f} ± {delta['ci95']:.4f} "
        f"(95% CI, n={delta['n']}, swap_identity 剔除 {delta['n_swap_identity_excluded']} 条)",
        f"分列 (窗内副本存在): 有 n={by_copy['True']['n']} intact={fmt(by_copy['True']['intact'])} | "
        f"无 n={by_copy['False']['n']} intact={fmt(by_copy['False']['intact'])}",
        "",
        f"读数：{verdict}",
        "",
        f"汇总: {out_path}  逐条目: {items_path}",
    ]
    (out_dir / "SUMMARY.txt").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
