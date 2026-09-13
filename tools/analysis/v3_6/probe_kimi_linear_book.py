"""E122 必要性账 · Kimi-Linear-48B-A3B 跨架构复证仪器（kimi122 臂·行为侧）。

目的（审稿防御件）：把 E122 簇级同体半分对照设计移植到社区标准 SOTA 线性注意
力混合架构 Kimi-Linear-48B-A3B-Base（KDA 20 层 + MLA 7 层，token 级 tiktoken
tokenizer），在工业级非自造架构上复证「线性状态通道写入内容但解码端近乎读不
出」（读者类墙），与 DeltaNet 臂（tools/analysis/cross_arch/probe_e122_deltanet_book.py，
冒烟 +0.262 nat / 500 窗 contrast 0.281 nat CI 不含 0）互为独立复证。

移植设计（与 DeltaNet 臂的四条施工注记同构，差异如实记录）：
1. 遮蔽形态：同为**输入侧**手术——span 替换为同 token 数的诱饵 token 序列。
   粒度 = tiktoken token（非字节）；gram = token 级 n-gram（n=2-3）。打包基
   v = 163840（Kimi 词表），n=3 打包 int ≈ 4.4e15，python int 无虞。
2. 诱饵合格域条款（第一天就在）：与 e122 红队条款逐字同构（家族一切出现区间
   ∪ 源 span ∪ 计分位皆不可压；诱饵内容含拼接缝不得产生任何被测家族成员；
   违例 RuntimeError 响亮）——全部**原样复用** e122 的 plan_window_surgery，
   不复制不分叉。
3. 同卷纪律：窗从语料顺序抽取，纯文本按字节切 window_bytes(4096)B 窗，
   utf-8(errors='replace') 解码后 tokenize，截 max_tokens。**Kimi 差异**：
   TikTokenTokenizer ``__call__`` 不前置 BOS（未覆写
   build_inputs_with_special_tokens）——窗 = 裸 token 序列，落 summary。
4. 判读口径：主判读量 = mean ΔNLL(处理) − mean ΔNLL(对照)，逐位 fp32、无
   autocast；窗级 bootstrap 95% CI（2000 次）；强响应尾 1 nat；判序 CI 在先
   ——bootstrap_contrast 原样复用 e122；**verdict 用本臂本地版 _verdict_kimi**
   （2026-09-13 文案勘误：旧版直接复用 DeltaNet 臂 verdict，串中硬编码
   「DeltaNet 跨架构复证」张冠李戴；且混合架构 CI 含 0 的语义≠「复证未过」，
   须带逃逸口全限定——用户判词二）。

结构差（跨架构并表用）：
- MoE 架构（256 experts top-8）：推理路径确定（eval 模式无 dropout/路由随机），
  冻结前向确定性成立，手术双臂同前向路径，对照结构不受影响。
- MLA 全注意力层并存：必要性账只动输入，KDA/MLA 两类层同时接收同一手术窗，
  测的是「模型整体读不读」——与 DeltaNet 臂「纯线性架构」的差异，跨架构并表
  时如实标注（读出侧仪器才单独隔离 KDA 状态通道）。
- 硬件指纹（AGENTS 坑 11/12 纪律）：summary 记 GPU/torch/fla/transformers/
  attn_backend/dtype，体制判词一律「同机同 env 内成立」。

Usage:
  python tools/analysis/v3_6/probe_kimi_linear_book.py \
      --model-path /root/autodl-tmp/models/Kimi-Linear-48B-A3B-Base \
      --corpus /root/autodl-tmp/corpus/corpus_v3.txt \
      --n-windows 40 --device cuda \
      --out-dir /root/autodl-tmp/outputs/kimi_linear_book_<date>
  CPU 冒烟（需小模型替身或权重就位后的真机）: --device cpu --n-windows 2
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import time
from pathlib import Path

import torch

try:  # repo 根可导入（pytest / python -m）
    from tools.analysis.cross_arch import probe_e122_deltanet_book as e122
    from tools.analysis.v3_6 import probe_kimi_linear_load as kload
except ImportError:  # 脚本直跑（sys.path[0] = 脚本目录）
    import sys as _sys
    from pathlib import Path as _P

    _sys.path.insert(0, str(_P(__file__).resolve().parents[1] / "cross_arch"))
    _sys.path.insert(0, str(_P(__file__).resolve().parent))
    import probe_e122_deltanet_book as e122
    import probe_kimi_linear_load as kload


def _verdict_kimi(mean_sel, contrast: dict) -> str:
    """本臂 verdict（判序 CI 在先，与 e122 同构）——措辞锚=Kimi-Linear 混合架构整模
    必要性账。CI 含 0 在本臂的语义不是「复证未过」：3:1 KDA:MLA 混合下整模测量混
    读者（逃逸口条款），贴零只排除「此任务此剂量下整模远程依赖 ≳CI 半宽量级」，
    通道级结论归 surgery/readout 两臂（2026-09-13 用户判词二）。"""
    if mean_sel is None or contrast["point"] is None:
        return "无读数"
    if not contrast["ci_excludes_zero"]:
        return ("整模远程依赖贴零（CI 含 0）——限于本任务/剂量/窗流，排除 ≳CI 半宽量级的"
                "整模远程依赖；混合架构注意力层在场，本账不隔离 KDA 通道（逃逸口）")
    if contrast["point"] < 0:
        return "反常（对照>处理——仪器 bug 或选择口径错，停，转口径审计）"
    if mean_sel >= e122.STRONG_LINE_NAT:
        return "整模远程依赖实存（强）——剂量打在黑板上"
    return "整模远程依赖实存（弱）——剂量部分在板"

STRONG_LINE_NAT = e122.STRONG_LINE_NAT


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--model-path",
                   default="/root/autodl-tmp/models/Kimi-Linear-48B-A3B-Base")
    p.add_argument("--corpus", default="/root/autodl-tmp/corpus/corpus_v3.txt")
    p.add_argument("--n-windows", type=int, default=40)
    p.add_argument("--start-window", type=int, default=0)
    p.add_argument("--window-bytes", type=int, default=4096)
    p.add_argument("--max-tokens", type=int, default=2048,
                   help="窗 token 截断上限；须为 64 的倍数（fla chunk 约束）")
    p.add_argument("--segment-tokens", type=int, default=256)
    p.add_argument("--ngram-len", type=int, default=3, choices=[2, 3, 4])
    p.add_argument("--tail", type=int, default=3)
    p.add_argument("--rare-quantile", type=float, default=0.2)
    p.add_argument("--pool-quantile", type=float, default=0.1)
    p.add_argument("--table-windows", type=int, default=2048)
    p.add_argument("--strong-line", type=float, default=STRONG_LINE_NAT)
    p.add_argument("--bootstrap", type=int, default=2000)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--max-draws", type=int, default=64)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--max-memory", default="",
                   help="双卡显存约束，如 0:70GiB,1:70GiB（device_map=auto 聚合）")
    p.add_argument("--out-dir",
                   default=f"outputs/kimi_linear_book_{time.strftime('%Y%m%d')}")
    args = p.parse_args()

    if args.tail < 1 or args.segment_tokens < 1 or args.max_tokens < 64:
        raise SystemExit("--tail/--segment-tokens ≥1 且 --max-tokens ≥64")
    if args.max_tokens % 64:
        raise SystemExit("--max-tokens 须为 64 的倍数（fla chunk_kda 约束）")
    if not (0 < args.rare_quantile <= 1 and 0 < args.pool_quantile <= 1):
        raise SystemExit("--rare-quantile/--pool-quantile ∈ (0, 1]")

    device = torch.device(
        "cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda"
        else "cpu"
    )
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    corpus = Path(args.corpus)
    if not corpus.exists():
        raise SystemExit(f"corpus 不存在: {corpus}")

    max_memory = None
    if args.max_memory:
        max_memory = {
            (int(k) if k.isdigit() else k): v
            for k, v in (
                kv.split(":", 1) for kv in args.max_memory.split(",") if kv)}
    model, tok, fingerprint = kload.load_model_and_tokenizer(
        args.model_path, device, max_memory=max_memory)
    v = fingerprint["vocab_size"]
    print(f"[kbook] model={Path(args.model_path).name} device={device.type} "
          f"V={v} kda_layers={len(fingerprint['kda_layers_0based'])} "
          f"backend={fingerprint['attn_backend']} fp={fingerprint['gpus']}",
          flush=True)

    need_windows = max(args.table_windows, args.start_window + args.n_windows)
    table, table_scanned = e122.build_rare_table(
        tok, corpus, need_windows, args.window_bytes,
        args.ngram_len, v, args.max_tokens)
    pool = e122.build_replacement_pool(table, args.ngram_len, v, args.pool_quantile)
    if not pool:
        raise SystemExit("替换池为空（表过小或 --pool-quantile 过小），响亮拒绝")
    print(f"[kbook] 稀有表 {len(table)} gram（扫 {table_scanned} 窗），池 {len(pool)}",
          flush=True)

    scan = args  # run_window 所需字段（ngram_len/tail/segment_tokens/…）CLI 全带

    def forward(model_, ids):
        return e122.real_forward_nll(model_, ids, device)

    rng = random.Random(args.seed)
    items_path = out_dir / "items.jsonl"
    audit_path = out_dir / "audit.jsonl"
    window_sums: list[dict] = []
    tally = {"n_windows_attempted": 0, "n_windows_used": 0, "n_windows_empty": 0,
             "n_windows_truncated": 0}
    totals: dict[str, int] = {}
    max_byte_touched = 0
    sel_distances: list[int] = []
    decoy_gaps: list[int] = []

    with corpus.open("rb") as f:
        for wi in range(args.n_windows):
            w_abs = args.start_window + wi
            f.seek(w_abs * args.window_bytes)
            raw = f.read(args.window_bytes)
            if len(raw) < args.window_bytes:
                print(f"[kbook] 语料前缀尽（窗 {w_abs} 不足 {args.window_bytes}B），停",
                      flush=True)
                break
            max_byte_touched = max(max_byte_touched, (w_abs + 1) * args.window_bytes)
            ids, full_len = kload.tokenize_window(
                tok, raw.decode("utf-8", errors="replace"), args.max_tokens)
            if full_len > args.max_tokens:
                tally["n_windows_truncated"] += 1
            rec = e122.run_window(model, ids, scan, rng, table, pool, v, w_abs,
                                  forward_fn=forward)
            tally["n_windows_attempted"] += 1
            for k, val in rec["counts"].items():
                totals[k] = totals.get(k, 0) + val
            if rec["status"] == "ok" and rec["sums"]["n_sel"] > 0:
                tally["n_windows_used"] += 1
                window_sums.append(rec["sums"])
                sel_distances.extend(
                    it["source_repeat_distance"] for it in rec["items"]
                    if it["role"] == "selected" and it["source_repeat_distance"] is not None
                )
                decoy_gaps.extend(
                    d["gap_to_nearest_family_span"] for d in rec["audit"]["decoy_landings"]
                )
                audit_rec = {
                    "byte_offset": w_abs * args.window_bytes,
                    "n_bytes": args.window_bytes,
                    "n_tokens": len(ids), "n_tokens_full": full_len,
                    "truncated": full_len > args.max_tokens,
                    "segment_tokens": args.segment_tokens,
                    **rec["audit"],
                }
                with audit_path.open("a", encoding="utf-8") as fa:
                    fa.write(json.dumps(audit_rec, ensure_ascii=False) + "\n")
                with items_path.open("a", encoding="utf-8") as fi:
                    for item in rec["items"]:
                        fi.write(json.dumps(item, ensure_ascii=False) + "\n")
            else:
                tally["n_windows_empty"] += 1
            s = rec["sums"]
            print(f"[kbook] win {w_abs:5d} {rec['status']:5s} sel={s['n_sel']:3d} "
                  f"ctl={s['n_ctl']:3d} strong={s['n_strong']:3d} "
                  f"decoy={rec['counts']['n_decoys']:2d} ({time.time() - t0:.0f}s)",
                  flush=True)

    # 同卷锚：计分窗字节前缀 SHA256（dd 顺序写语料下，读过的前缀字节已定终）
    prefix_sha = None
    if max_byte_touched:
        h = hashlib.sha256()
        with corpus.open("rb") as f:
            remain = max_byte_touched
            while remain:
                chunk = f.read(min(1 << 20, remain))
                if not chunk:
                    break
                h.update(chunk)
                remain -= len(chunk)
        prefix_sha = h.hexdigest()

    n_sel = sum(w["n_sel"] for w in window_sums)
    n_ctl = sum(w["n_ctl"] for w in window_sums)
    mean_sel = sum(w["sel_d_b1"] for w in window_sums) / n_sel if n_sel else None
    mean_ctl = sum(w["ctl_d_b1"] for w in window_sums) / n_ctl if n_ctl else None
    boot = e122.bootstrap_contrast(window_sums, args.bootstrap, args.seed + 1)
    n_strong = sum(w["n_strong"] for w in window_sums)

    summary = {
        "probe": "E122 必要性账 · Kimi-Linear-48B 跨架构复证（输入侧遮蔽 + 簇级同体半分对照）",
        "arm": "kimi122",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "model_fingerprint": fingerprint,
        "companion_runs": "DeltaNet 臂 = tools/analysis/cross_arch/probe_e122_deltanet_book.py"
                          "（500 窗 contrast 0.281 nat CI 不含 0，2026-09-11）",
        "corpus": {
            "path": str(corpus),
            "window_bytes": args.window_bytes,
            "start_window": args.start_window,
            "scored_prefix_bytes": max_byte_touched,
            "scored_prefix_sha256": prefix_sha,
            "corpus_size_at_run": os.path.getsize(corpus),
        },
        "window_definition": {
            "window": "corpus[w*4096 : (w+1)*4096] 顺序字节窗（纯文本）",
            "decode": "utf-8 errors=replace",
            "tokenize": "TikTokenTokenizer __call__ 默认行为；Kimi 无 BOS 前置"
                        "（build_inputs_with_special_tokens 未覆写，同卷事实）",
            "truncation": f"ids[:{args.max_tokens}]",
            "segment": f"token 段 = {args.segment_tokens} tokens，跨段 = 出现段严格晚于最早出现段",
            "note": "同卷纪律：窗定义+前缀 SHA256 落此；跨模型只比方向不比绝对值",
        },
        "params": {
            "n_windows": args.n_windows, "ngram_len": args.ngram_len, "tail": args.tail,
            "segment_tokens": args.segment_tokens, "rare_quantile": args.rare_quantile,
            "pool_quantile": args.pool_quantile, "seed": args.seed,
            "strong_line_nat": args.strong_line, "max_draws": args.max_draws,
            "bootstrap": args.bootstrap, "table_windows_requested": args.table_windows,
            "table_windows_scanned": table_scanned,
        },
        "rare_table": {"n_grams": len(table), "pool_size": len(pool)},
        "windows": tally,
        "selected": {"n": n_sel, "mean_delta_b1": mean_sel},
        "control": {"n": n_ctl, "mean_delta_b1": mean_ctl},
        "contrast_b1": {
            **boot,
            "mean": (mean_sel - mean_ctl) if (mean_sel is not None and mean_ctl is not None) else None,
        },
        "strong_tail": {
            "n_strong": n_strong,
            "rate_of_selected": (n_strong / n_sel) if n_sel else None,
            "per_window_mean": (n_strong / len(window_sums)) if window_sums else 0.0,
        },
        "source_repeat_distance": {
            "n": len(sel_distances),
            "min": min(sel_distances) if sel_distances else None,
            "median": (sorted(sel_distances)[len(sel_distances) // 2] if sel_distances else None),
            "max": max(sel_distances) if sel_distances else None,
        },
        "red_team_audit": {
            "clause": "诱饵落点 ∩ 家族一切出现区间 = ∅ 且 ∩ 源 span = ∅ 且 ∩ 计分位 = ∅"
                      "（压线重叠才违规；相邻 gap=0 不违规只进距离字段）；"
                      "诱饵内容（含拼接缝）不含任何被测家族成员；非零违例即 RuntimeError",
            "n_decoys_total": totals.get("n_decoys", 0),
            "min_decoy_gap_to_family_span": min(decoy_gaps) if decoy_gaps else None,
            "n_overlap_violations": 0,
            "n_control_no_decoy": totals.get("n_control_no_decoy", 0),
            "n_treatment_clusters_skipped": totals.get("n_treatment_clusters_skipped", 0),
        },
        "exclusions": {
            "offtable_hit_grams": totals.get("offtable_grams", 0),
            "selection_overlap": totals.get("n_selection_overlap", 0),
        },
        "verdict": _verdict_kimi(mean_sel, boot),
        "arch_note": "Kimi-Linear = KDA(20) + MLA(7) 混合；必要性账动输入、双臂同前向，"
                     "测「模型整体读不读」；KDA 状态通道单独隔离见 "
                     "probe_kimi_linear_state_surgery.py / probe_kimi_linear_state_readout.py",
        "timing_sec": round(time.time() - t0, 1),
    }
    (out_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"verdict": summary["verdict"],
                      "contrast": summary["contrast_b1"]},
                     ensure_ascii=False, indent=2), flush=True)
    print(f"[kbook] items -> {items_path}\n[kbook] audit -> {audit_path}", flush=True)


if __name__ == "__main__":
    main()
