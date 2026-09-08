"""E123 前置门② 必要性账 v2（2026-09-07，冻结任务书 §3.2；零训练）。

测「内容信息量」而非「基座现状依赖」（外审攻击③修正）：候选 chunk 的内容
**完全缺席**（双遮蔽 = 注意力 block_mask + store 行替换，槽一口径）vs 基线，
下游目标位 NLL 之差 = 该区内容对目标的携带信息（互信息下界）。

  双遮蔽（槽一钉死）：字节流/位置/分段全不动——(1) 窗内注意力键侧视野抹除
  （attn_block_mask 线程，E123 遮蔽器件同码）；(2) 该 chunk 的 store 行与上游
  相邻行交换（内容错误、行存在性保留，E122 b2 纪律；donor 避开下游 c+1 防直
  接面污染）。目标位 = 下游第一个真实 chunk（c+1）的 valid 字节；读数面分开：
  logits_direct（编码器状态效应）与 logits_backbone（行替换效应），合计等权
  为主判读。口径与 E122 冻结 §4 同源：500 窗 seed42+9999 eval 流、窗级
  bootstrap 2000、逐位 NLL fp32 无 autocast、判读只在 CUDA 线、任务注入零。

  门判（两门一预算方程，质量侧）：合计对比 CI 不含 0 且 >0 = 这段内容值得读、
  需求可造（随机 chunk 候选池可用）；CI 含 0 = 无可测需求——先验/局部可推，
  该候选池淘汰、改语料/位点池（措辞纪律：一切输出表述为「相对于此基座与此
  探测手段，无可测需求」，永不表述「需求不存在」）。
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
import time
from argparse import Namespace
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from flued.data import MASK_ID, PAD_ID  # noqa: E402
from tools.analysis.v3_6.probe_e122_necessity_book import (  # noqa: E402
    assert_cell_keys,
    bootstrap_contrast,
    gather_nll,
    patch_store_rows_perm,
)
from tools.analysis.v3_6.probe_oracle_write_verdict import (  # noqa: E402
    build_eval_windows,
    build_masks,
    load_model,
)
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402

BASE_RUN = "checkpoints/v37ks_a_d1_w1_10k_ctx4096_20260904"
OUT_DIR = "outputs/e123_gate_necessity_v2_20260907"
N_BLOCKS = 4        # 每窗候选块数（臂剂量 1-4 上界同构）
SCORE_DIST = 8      # 下游计分距离（chunk 单位；回执二源-汇直方图支撑）
N_WINDOWS = 500
BOOTSTRAP = 2000
SEED = 42


def row_swap_perm(c: int, n_real: int) -> list[int]:
    """单块行交换：perm[c] ↔ perm[donor]，donor 取上游（c-1），c==0 时取 c+2
    （避开下游 c+1 防直接面污染）；n_real 太小则退回 c+1（无污染可用时）。"""
    perm = list(range(n_real))
    if n_real < 2:
        return perm
    if c - 1 >= 0:
        donor = c - 1
    elif c + 2 < n_real:
        donor = c + 2
    else:
        donor = c + 1
    perm[c], perm[donor] = donor, c
    return perm


def run_gate_window(model, ns, clean, byte_mask, rng, wi, n_blocks=N_BLOCKS,
                    b_mode: str = "both") -> dict:
    """一窗：基线 A（共享）+ 每候选块一个 B 前向。b_mode=both（注意力遮蔽+行
    交换，=槽一完全缺席）/ mask（只注意力遮蔽——内容经编码器通道的依赖）/
    swap（只行交换——内容经状态行身份通道的依赖；伪影拆分控制）。"""
    device = clean.device
    source_a = clean.masked_fill(byte_mask.bool(), MASK_ID)

    def fwd(mask=None, perm=None):
        restore = None
        if perm is not None:
            restore = patch_store_rows_perm(model, perm)
        try:
            return s1.s1_forward(model, source_a, ns, attn_block_mask=mask)
        finally:
            if restore is not None:
                restore()

    out_a = fwd()
    ca, oa = out_a["chunks"].chunk_ids, out_a["chunks"].offsets
    n_real = int(out_a["chunks"].chunk_mask[0].sum())
    if n_real < 3:
        return {"status": "empty", "items": [], "sums": None}

    # 候选块：均匀抽样 n_blocks 个真实 chunk（避开最后一个，保证下游存在）
    pool = [c for c in range(n_real - 1)]
    picks = rng.sample(pool, min(n_blocks, len(pool)))

    items = []
    for c in picks:
        # 下游目标位 = chunk c+1 .. c+D 的 valid 字节（v1.2 回执二需要源-汇
        # 距离直方图：单距离读数推不出 K_max 课程锚）
        tgt = [(t, int(ca[0, t]))
               for t in range(clean.size(1))
               if int(ca[0, t]) - c in range(1, SCORE_DIST + 1)
               and 0 <= int(oa[0, t]) < int(ns.max_span)
               and not bool(byte_mask[0, t])]
        if not tgt:
            continue
        tgt_ids = [int(clean[0, t]) for t, _c in tgt]
        mask_b = torch.zeros(1, 1, 1, clean.size(1), dtype=torch.bool, device=device)
        for t in range(clean.size(1)):
            if int(ca[0, t]) == c:
                mask_b[0, 0, 0, t] = True
        out_b = fwd(mask=mask_b, perm=row_swap_perm(c, n_real))
        cb, ob = out_b["chunks"].chunk_ids, out_b["chunks"].offsets
        # 双遮蔽下分段不漂移的卫检（block_mask 不喂 segmentor，切点必不变）
        if not bool((cb == ca).all()):
            raise RuntimeError(f"win{wi} chunk c={c}: 双遮蔽下分段漂移（卫检失败）——仪器 bug")
        na_d = gather_nll(out_a["logits_direct"], ca, oa, [t for t, _c in tgt], tgt_ids)
        nb_d = gather_nll(out_b["logits_direct"], cb, ob, [t for t, _c in tgt], tgt_ids)
        na_b = gather_nll(out_a["logits_backbone"], ca, oa, [t for t, _c in tgt], tgt_ids)
        nb_b = gather_nll(out_b["logits_backbone"], cb, ob, [t for t, _c in tgt], tgt_ids)
        # 块基线 surprisal（验证性代理）：块自身 valid 字节在基线前向的 mean NLL
        # ——若它与信息量强相关，选择器可退化为单前向 surprisal 扫描（省 4×）
        src_pos = [t for t in range(clean.size(1))
                   if int(ca[0, t]) == c
                   and 0 <= int(oa[0, t]) < int(ns.max_span)
                   and not bool(byte_mask[0, t])]
        src_ids = [int(clean[0, t]) for t in src_pos]
        surprisal = None
        if src_pos:
            na_src = gather_nll(out_a["logits_direct"], ca, oa, src_pos, src_ids)
            surprisal = sum(na_src) / len(na_src)
        for i, (t, sink_c) in enumerate(tgt):
            items.append({
                "window_id": wi,
                "chunk": c,
                "sink_chunk": sink_c,
                "distance": sink_c - c,
                "byte_pos": t,
                "block_baseline_surprisal": surprisal,  # 代理验证用
                "d_direct": nb_d[i] - na_d[i],
                "d_backbone": nb_b[i] - na_b[i],
                "d_total": 0.5 * (nb_d[i] - na_d[i]) + 0.5 * (nb_b[i] - na_b[i]),
            })
    sums = {"n": len(items)}
    if items:
        for k in ("d_direct", "d_backbone", "d_total"):
            sums[k] = sum(it[k] for it in items) / len(items)
    return {"status": "ok" if items else "empty", "items": items, "sums": sums}


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    p = argparse.ArgumentParser()
    p.add_argument("--ckpt", default=BASE_RUN)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--n-windows", type=int, default=N_WINDOWS)
    p.add_argument("--n-blocks", type=int, default=N_BLOCKS)
    p.add_argument("--bootstrap", type=int, default=BOOTSTRAP)
    p.add_argument("--data-path", default=None)
    p.add_argument("--out-dir", default=OUT_DIR)
    p.add_argument("--cell-relaxed", action="store_true", help="a 格档（坑 8 放宽）")
    args = p.parse_args()
    device = torch.device(
        "cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu"
    )
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    model, ns, step = load_model(Path(args.ckpt), device)
    assert_cell_keys(ns, model.config, strict=not args.cell_relaxed)
    ns.burst_prob = 0
    ns.cloze_prob = 0
    ns.retrieval_prob = 0
    if args.data_path:
        ns.data_path = args.data_path
    batch_size = max(int(ns.batch_size), 1)
    n_batches = math.ceil(args.n_windows / batch_size)
    windows = build_eval_windows(ns, n_batches)
    masks = build_masks(windows, ns)
    rng = random.Random(SEED)
    print(f"[e123-necessity] ckpt={Path(args.ckpt).name} step={step} device={device.type} "
          f"windows={args.n_windows} blocks={args.n_blocks}", flush=True)

    items_path = out_dir / "items.jsonl"
    window_sums = []
    wi = 0
    for batch, mbatch in zip(windows, masks):
        for j in range(batch.size(0)):
            if wi >= args.n_windows:
                break
            ids = batch[j]
            cut = int(ids.ne(PAD_ID).sum())
            clean_row = ids[:cut].unsqueeze(0).to(device)
            mask_row = mbatch[j][:cut].unsqueeze(0).to(device)
            rec = run_gate_window(model, ns, clean_row, mask_row, rng, wi, args.n_blocks)
            if rec["status"] == "ok":
                window_sums.append(rec["sums"])
                with items_path.open("a", encoding="utf-8") as f:
                    for it in rec["items"]:
                        f.write(json.dumps(it, ensure_ascii=False) + "\n")
            print(f"[e123-necessity] win {wi:4d} {rec['status']:5s} "
                  f"n={rec['sums']['n'] if rec['sums'] else 0:4d} ({time.time()-t0:.0f}s)",
                  flush=True)
            wi += 1
        if wi >= args.n_windows:
            break

    n_used = len(window_sums)
    if n_used == 0:
        raise SystemExit("零有效窗——查语料路径/基座口径")
    # 窗级 bootstrap（E122 §4 同源）：把窗 sums 投影成 E122 bootstrap 输入形
    boot_in = [
        {"n_sel": w["n"], "sel_d_b1": w["d_total"] * w["n"],
         "n_ctl": w["n"], "ctl_d_b1": 0.0}
        for w in window_sums
    ]
    boot = bootstrap_contrast(boot_in, args.bootstrap, SEED + 1)
    mean_direct = sum(w["d_direct"] for w in window_sums) / n_used
    mean_backbone = sum(w["d_backbone"] for w in window_sums) / n_used
    mean_total = sum(w["d_total"] for w in window_sums) / n_used
    n_pos = sum(w["n"] for w in window_sums)
    verdict = (
        "内容信息量显著 > 0——这段内容值得读，需求可造（随机 chunk 候选池可用，过门）"
        if boot["ci_excludes_zero"] and mean_total > 0 else
        "无可测需求（相对于此基座与此探测手段）——先验/局部可推，随机 chunk 候选池"
        "淘汰、改语料/位点池（两门一预算方程：门不及格改位点池不改剂量）"
    )
    summary = {
        "gate": "E123 前置门② 必要性账 v2",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "ckpt": {"run": Path(args.ckpt).name, "step": step},
        "device": device.type,
        "params": {"n_windows_requested": args.n_windows, "n_windows_used": n_used,
                   "n_blocks_per_window": args.n_blocks, "seed": SEED,
                   "bootstrap": args.bootstrap},
        "measure": "候选 chunk 双遮蔽（注意力 block_mask+行交换 donor=c-1/c+2）vs 基线；"
                   "下游 chunk c+1 valid 字节；两面读数 direct/backbone 等权合计",
        "results": {
            "n_positions": n_pos,
            "mean_d_direct": round(mean_direct, 5),
            "mean_d_backbone": round(mean_backbone, 5),
            "mean_d_total": round(mean_total, 5),
            "bootstrap": boot,
        },
        "verdict": verdict,
        "wording_discipline": "一切输出表述为「相对于此基座与此探测手段，无可测需求」，"
                             "永不表述为「需求不存在」",
        "timing_sec": round(time.time() - t0, 1),
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2),
                                          encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
