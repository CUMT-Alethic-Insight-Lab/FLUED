"""E122 配套表示侧仪器 · Kimi-Linear KDA 线性状态闭式读出探针（kimi122 臂·第三把尺子）。

目的：必要性账（probe_kimi_linear_book.py）答行为侧「用没用」；本仪器答表示侧
配套问题——**远端内容是否以线性可读的形式住在 KDA 递归状态 S_t 里**。移植自
tools/analysis/cross_arch/probe_deltanet_state_readout.py（DeltaNet 臂），探针
核心（ridge 对偶解 / real-ctrl 对照 / 符号翻转置换 / 距离分层）**原样 import
复用，不复制不分叉**；换的只有状态捕获与层集合。

与 DeltaNet 臂的结构差（如实记录，跨架构并表用）：
1. 层集合 = 20 个 KDA 层（0 基 {0,1,2,4,5,6,8,9,10,12,13,14,16,17,18,20,21,22,
   24,25}），非全 27 层——MLA 层无递归状态，不在本仪器口径内。
2. 状态捕获 = monkeypatch modeling_kimi.chunk_kda（层模块全局名，进程内，不改
   库文件）：旁路留存每层 (k,v,g,beta) pre-L2 + 核 final_state；**fp32 边界态
   独立重算**（fla/ops/kda/naive.py naive_recurrent_kda 同式，K 维 fine-grained
   门控 + per-token L2），逐层与核 final_state 对拍（相对误差阈，超阈 RuntimeError
   响亮停机——前提哨兵，递推语义不符时绝无静默错状态）。
3. 状态形状 [H=32, K=128, V=128]（无 GVA），每边界 524288 维；DeltaNet 臂为
   16×128×128=262144 维。粒度同 = chunk 边界（64 token），模型递归的真实保存粒度。
4. 样本构造 / 窗定义 / 窗劈分 / λ 敏感性：与 DeltaNet 臂逐字同构（build_window_samples
   原样复用），同卷对拍成立；跨模型只比方向不比绝对值。

判词（描述性，冒烟级留白）：与 DeltaNet 臂同表——深部层远程 uplift>0 且 p<0.05
→ 「线性可读」；全否 → 「未见线性可读」；其余 → 证据不足。两向都与必要性账、
置零解离（probe_kimi_linear_state_surgery.py）并读，不单独定案。

Usage:
  python tools/analysis/v3_6/probe_kimi_linear_state_readout.py \
      --model-path /root/autodl-tmp/models/Kimi-Linear-48B-A3B-Base \
      --corpus /root/autodl-tmp/corpus/corpus_v3.txt \
      --n-windows 40 --device cuda \
      --out-dir /root/autodl-tmp/outputs/kimi_state_readout_<date>
  内存注：全 20 层单 pass ≈ 40 窗 × 20 层 × 33MB ≈ 27GB CPU RAM（1TB 机器无虞）；
  紧张时 --layers-per-pass 4 分 pass（前向重跑，选择链零随机，样本逐字一致）。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
from pathlib import Path

import torch

try:  # repo 根可导入（pytest / python -m）
    from tools.analysis.cross_arch import probe_deltanet_state_readout as dsr
    from tools.analysis.cross_arch import probe_e122_deltanet_book as e122
    from tools.analysis.v3_6 import probe_kimi_linear_load as kload
except ImportError:  # 脚本直跑（sys.path[0] = 脚本目录）
    import sys as _sys
    from pathlib import Path as _P

    _sys.path.insert(0, str(_P(__file__).resolve().parents[1] / "cross_arch"))
    _sys.path.insert(0, str(_P(__file__).resolve().parent))
    import probe_deltanet_state_readout as dsr
    import probe_e122_deltanet_book as e122
    import probe_kimi_linear_load as kload


def parse_int_list(text: str, kda_layers: list[int]) -> list[int]:
    """'kda'（全部 KDA 层）/ 'all'（全 27 层，报错——MLA 层无状态，显式拒绝）
    / 逗号层号。"""
    t = text.strip().lower()
    if t == "kda":
        return list(kda_layers)
    if t == "all":
        raise SystemExit("--probe-layers all 不支持：MLA 层无递归状态；用 'kda' 或显式层号")
    vals = [int(x) for x in text.split(",") if x.strip()]
    if not vals:
        raise SystemExit("--probe-layers 解析失败")
    return vals


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--model-path",
                   default="/root/autodl-tmp/models/Kimi-Linear-48B-A3B-Base")
    p.add_argument("--corpus", default="/root/autodl-tmp/corpus/corpus_v3.txt")
    p.add_argument("--n-windows", type=int, default=40)
    p.add_argument("--start-window", type=int, default=0)
    p.add_argument("--window-bytes", type=int, default=4096)
    p.add_argument("--max-tokens", type=int, default=2048,
                   help="须为 64 的倍数（fla chunk 约束）")
    p.add_argument("--segment-tokens", type=int, default=256)
    p.add_argument("--ngram-len", type=int, default=3, choices=[2, 3, 4])
    p.add_argument("--tail", type=int, default=3)
    p.add_argument("--chunk-size", type=int, default=64, choices=[16, 32, 64])
    p.add_argument("--near-lags", default="1,2,3")
    p.add_argument("--ridge-lambda", type=float, default=1.0)
    p.add_argument("--extra-ridge-lambdas", default="")
    p.add_argument("--train-frac", type=float, default=0.5)
    p.add_argument("--near-dist", type=int, default=32)
    p.add_argument("--remote-dist", type=int, default=192)
    p.add_argument("--n-perm", type=int, default=4096)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--probe-layers", default="kda",
                   help="'kda'（全部 20 KDA 层，默认）或逗号层号（0 基）")
    p.add_argument("--max-boundaries-per-window", type=int, default=24)
    p.add_argument("--layers-per-pass", type=int, default=0,
                   help="分 pass 缓存层数（0=全部单 pass；防 cgroup 内存顶穿，"
                        "每 pass 重跑前向，选择链零随机故各 pass 样本逐字一致）")
    p.add_argument("--verify-tol-rel", type=float, default=0.05)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--max-memory", default="",
                   help="双卡显存约束，如 0:70GiB,1:70GiB")
    p.add_argument("--out-dir",
                   default=f"outputs/kimi_state_readout_{time.strftime('%Y%m%d')}")
    args = p.parse_args()

    if not (0 < args.train_frac < 1):
        raise SystemExit("--train-frac ∈ (0,1)")
    if args.near_dist >= args.remote_dist:
        raise SystemExit("--near-dist 须小于 --remote-dist")
    if args.max_tokens % args.chunk_size:
        raise SystemExit("--max-tokens 须为 chunk-size 的倍数（fla chunk 约束）")
    near_lags = tuple(int(x) for x in args.near_lags.split(",") if x.strip())
    extra_lambdas = tuple(float(x) for x in args.extra_ridge_lambdas.split(",")
                          if x.strip())
    if any(lv <= 0 for lv in extra_lambdas) or args.ridge_lambda <= 0:
        raise SystemExit("λ 必须 > 0")

    device = torch.device(
        "cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda"
        else "cpu")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    corpus = Path(args.corpus)
    if not corpus.exists():
        raise SystemExit(f"corpus 不存在: {corpus}")

    max_memory = None
    if args.max_memory:
        max_memory = dict(
            kv.split(":", 1) for kv in args.max_memory.split(",") if kv)
    model, tok, fingerprint = kload.load_model_and_tokenizer(
        args.model_path, device, max_memory=max_memory)
    n_layers = int(model.config.num_hidden_layers)
    kda_layers = fingerprint["kda_layers_0based"]
    probe_layers = parse_int_list(args.probe_layers, kda_layers)
    if any(l < 0 or l >= n_layers for l in probe_layers):
        raise SystemExit(f"--probe-layers 越界（模型 {n_layers} 层）")
    if any(l not in kda_layers for l in probe_layers):
        raise SystemExit(f"--probe-layers 含非 KDA 层（无递归状态）: "
                         f"{[l for l in probe_layers if l not in kda_layers]}")
    emb = model.get_input_embeddings().weight.detach().float()
    state_dim = kload.STATE_DIM_PER_BOUNDARY
    print(f"[kread] model={Path(args.model_path).name} device={device.type} "
          f"layers={n_layers} kda={len(kda_layers)} probe={probe_layers} "
          f"state_dim={state_dim}", flush=True)

    layers_per_pass = args.layers_per_pass or len(probe_layers)
    passes = [probe_layers[i:i + layers_per_pass]
              for i in range(0, len(probe_layers), layers_per_pass)]
    samples_by_win: dict[int, list[dict]] = {}
    win_tokens: dict[int, int] = {}
    tally = {"n_windows_attempted": 0, "n_windows_used": 0, "n_windows_empty": 0,
             "n_windows_truncated": 0, "n_windows_forward_fails": 0}
    totals = {"n_samples": 0, "n_remote_skipped": 0, "n_boundaries_capped": 0,
              "n_selected_tails": 0}
    max_byte_touched = 0
    layer_results: dict[int, dict] = {}
    split_cache: tuple[list[int], list[int]] | None = None
    capture = kload.KdaChunkCapture().bind(model)
    verr_max_overall: float | None = None
    print(f"[kread] passes={[pp[0] for pp in passes]} layers_per_pass={layers_per_pass}",
          flush=True)

    with corpus.open("rb") as f, capture:
        for pi, pass_layers in enumerate(passes):
            store: dict[int, list[torch.Tensor]] = {l: [] for l in pass_layers}
            pass_used = 0
            for wi in range(args.n_windows):
                w_abs = args.start_window + wi
                f.seek(w_abs * args.window_bytes)
                raw = f.read(args.window_bytes)
                if len(raw) < args.window_bytes:
                    print(f"[kread] 语料前缀尽（窗 {w_abs}），停", flush=True)
                    break
                max_byte_touched = max(max_byte_touched, (w_abs + 1) * args.window_bytes)
                ids, full_len = kload.tokenize_window(
                    tok, raw.decode("utf-8", errors="replace"), args.max_tokens)
                if full_len > args.max_tokens:
                    tally["n_windows_truncated"] += 1
                tally["n_windows_attempted"] += 1
                tk = len(ids)
                if tk < max(2 * args.chunk_size,
                            args.segment_tokens + args.ngram_len + args.tail):
                    tally["n_windows_empty"] += 1
                    continue
                occ = e122.cross_segment_occurrences(ids, args.ngram_len,
                                                     args.segment_tokens)
                rare = set(occ)  # 探针要密度：全体跨段 gram（与必要账的差异，报告口径）
                sel, _ov = e122.select_tail_positions(occ, rare, args.ngram_len,
                                                      args.tail, tk)
                if not sel:
                    tally["n_windows_empty"] += 1
                    continue
                totals["n_selected_tails"] += len(sel)
                samples, skipped = dsr.build_window_samples(
                    ids, sel, args.ngram_len, args.chunk_size, near_lags=near_lags,
                    remote_js=tuple(range(args.ngram_len)))
                totals["n_remote_skipped"] += skipped
                if len(samples) > args.max_boundaries_per_window:
                    totals["n_boundaries_capped"] += len(samples) - args.max_boundaries_per_window
                    samples = samples[:args.max_boundaries_per_window]
                if not samples:
                    tally["n_windows_empty"] += 1
                    continue

                capture.records = []
                try:
                    with torch.no_grad():
                        model(torch.tensor([ids], dtype=torch.long, device=device))
                    states_all, verr = kload.extract_kda_boundary_states(
                        capture.records, args.chunk_size, args.verify_tol_rel)
                except RuntimeError as e:
                    if "对拍失败" in str(e):
                        raise  # 前提哨兵响亮，不静默
                    tally["n_windows_forward_fails"] += 1
                    print(f"[kread] win {w_abs} 前向失败（跳过）：{e}", flush=True)
                    continue
                if verr:
                    vm = max(v["rel_err"] for v in verr)
                    verr_max_overall = vm if verr_max_overall is None \
                        else max(verr_max_overall, vm)
                idx = torch.tensor([s["chunk"] for s in samples])
                for l in pass_layers:
                    rows = states_all[l][idx].reshape(len(samples), -1)
                    store[l].append(rows.to(torch.bfloat16).cpu())
                if pi == 0:
                    samples_by_win[w_abs] = samples
                    win_tokens[w_abs] = tk
                    totals["n_samples"] += len(samples)
                pass_used += 1
                print(f"[kread] p{pi} win {w_abs:5d} tk={tk} bounds={len(samples)} "
                      f"remote_skip={skipped} verif_max={vm if verr else None} "
                      f"({time.time() - t0:.0f}s)", flush=True)

            if not samples_by_win:
                raise SystemExit("零有效窗（选择链颗粒或语料问题），响亮拒绝")
            if split_cache is None:
                window_ids = sorted(samples_by_win)
                split_cache = dsr.split_windows(window_ids, args.train_frac, args.seed)
                print(f"[kread] 窗劈分 train={len(split_cache[0])} "
                      f"test={len(split_cache[1])}；探针逐层…", flush=True)
            train_win, test_win = split_cache
            for l in pass_layers:
                x_by_win = {w: store[l][i].float().to(emb.device)
                            for i, w in enumerate(sorted(samples_by_win))}
                layer_results[l] = dsr.run_layer_probes(
                    x_by_win, samples_by_win, train_win, test_win, emb,
                    args.ridge_lambda, args.seed, l, near_lags=near_lags,
                    n_remote_js=args.ngram_len, near_cut=args.near_dist,
                    remote_cut=args.remote_dist, n_perm=args.n_perm,
                    extra_lambdas=extra_lambdas)
                store[l] = []  # 逐层释放
                r = layer_results[l]
                print(f"[kread] layer {l:2d} "
                      f"near1 cos {r['near_lag1']['cos']['uplift']:+.4f} "
                      f"remote_j0 cos {r['remote_j0']['cos']['uplift']:+.4f}",
                      flush=True)
            del store
            if pi == 0:
                tally["n_windows_used"] = pass_used
                summary_tally = dict(tally)
                summary_totals = dict(totals)
            print(f"[kread] pass {pi}（层 {pass_layers[0]}-{pass_layers[-1]}）完成 "
                  f"({time.time() - t0:.0f}s)", flush=True)

    # 同卷锚：计分窗字节前缀 SHA256
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

    # 层组汇总（early/mid/deep 按模型深度三分）+ 判词（dsr 同表）
    groups = {"early": [l for l in probe_layers if l < n_layers / 3],
              "mid": [l for l in probe_layers if n_layers / 3 <= l < 2 * n_layers / 3],
              "deep": [l for l in probe_layers if l >= 2 * n_layers / 3]}
    group_summary = {}
    for gname, ls in groups.items():
        if not ls:
            continue
        ups = [layer_results[l]["remote_j0"]["cos"]["uplift"] for l in ls
               if layer_results[l]["remote_j0"]["cos"]["uplift"] is not None]
        ps = [layer_results[l]["remote_j0"]["cos"]["perm"]["p"] for l in ls
              if layer_results[l]["remote_j0"]["cos"]["perm"]]
        near_ups = [layer_results[l]["near_lag1"]["cos"]["uplift"] for l in ls
                    if layer_results[l]["near_lag1"]["cos"]["uplift"] is not None]
        group_summary[gname] = {
            "layers": ls,
            "remote_j0_cos_uplift_mean": (sum(ups) / len(ups)) if ups else None,
            "remote_j0_min_p": min(ps) if ps else None,
            "n_layers_remote_p_lt_0.05": sum(1 for x in ps if x < 0.05),
            "near_lag1_cos_uplift_mean": (sum(near_ups) / len(near_ups)) if near_ups else None,
        }

    deep = group_summary.get("deep", {})
    deep_up, deep_p = deep.get("remote_j0_cos_uplift_mean"), deep.get("remote_j0_min_p")
    if deep_up is None:
        verdict_txt = "无读数"
    elif deep_up > 0 and deep_p is not None and deep_p < 0.05:
        verdict_txt = ("深部 KDA 层远程内容线性可读（remote uplift>0 且 p<0.05）——状态写入可线性读出；"
                       "与必要性账/置零解离并读（冒烟级，判词留白待 500 窗）")
    elif deep_up <= 0 or (deep_p is not None and deep_p >= 0.05):
        verdict_txt = ("深部 KDA 层远程内容未见线性可读——读出或是非线性/注意式"
                       "（冒烟级，判词留白待 500 窗）")
    else:
        verdict_txt = "证据不足（冒烟级，判词留白）"

    summary = {
        "probe": "E122 配套表示侧 · Kimi-Linear KDA 线性状态闭式读出探针（第三把尺子）",
        "arm": "kimi122",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "model_fingerprint": fingerprint,
        "companion_runs": "行为侧 = probe_kimi_linear_book.py；置零解离 = "
                          "probe_kimi_linear_state_surgery.py；DeltaNet 臂 = "
                          "tools/analysis/cross_arch/probe_deltanet_state_readout.py",
        "corpus": {
            "path": str(corpus),
            "window_bytes": args.window_bytes,
            "start_window": args.start_window,
            "scored_prefix_bytes": max_byte_touched,
            "scored_prefix_sha256": prefix_sha,
            "corpus_size_at_run": os.path.getsize(corpus),
        },
        "window_definition": {
            "window": "corpus[w*4096 : (w+1)*4096] 顺序字节窗（与必要性账逐字同构）",
            "decode": "utf-8 errors=replace",
            "tokenize": "TikTokenTokenizer __call__ 默认（无 BOS 前置，同卷事实）",
            "truncation": f"ids[:{args.max_tokens}]",
            "segment": f"token 段 = {args.segment_tokens}，跨段 = 出现段严格晚于最早出现段",
            "note": "同卷纪律：窗定义+前缀 SHA256 落此；跨模型只比方向不比绝对值",
        },
        "state_capture": {
            "method": "进程内 monkeypatch modeling_kimi.chunk_kda（层模块全局名）旁路捕获 "
                      "(k,v,g,beta) pre-L2；fp32 边界态独立重算"
                      "（fla/ops/kda/naive.py naive_recurrent_kda 同式：K 维 fine-grained "
                      "门控 + per-token L2）；不改库文件",
            "granularity": f"chunk 边界（{args.chunk_size} token）；S[c] = 已消费 token < c*{args.chunk_size}",
            "state_shape_per_layer": [kload.KDA_HEADS, kload.KDA_HEAD_DIM, kload.KDA_HEAD_DIM],
            "state_dim_per_boundary": state_dim,
            "verification": "每窗逐层：fp32 边界态终态 vs 核 final_state，"
                            f"相对误差阈 {args.verify_tol_rel}，超阈响亮停机"
                            f"（本次实跑最大 rel_err = {verr_max_overall}）",
        },
        "probe_design": {
            "samples": "E122 选择链选中跨段重复续尾位 t → chunk 边界 c=t//64；每边界认领 designated 源",
            "targets": "近程 = 边界前第 lag token（阳性对照）；远程 = designated 源 gram 第 0..2 token",
            "features": f"S_t flatten {state_dim} 维（bf16 存 fp32 算）→ 训练窗逐维标准化",
            "ridge": f"线性核对偶 ridge，λ={args.ridge_lambda}，目标 = token 输入嵌入（fp32）",
            "control": "打乱配对 = 同窗内置换目标重训同款探针；uplift = real − ctrl",
            "metrics": "cos + 嵌入空间最近邻 top-1 acc；窗级符号翻转置换检验 p（单侧 uplift>0）",
            "splits": f"窗级 train/test {args.train_frac:.0%}/{1 - args.train_frac:.0%}（全层同劈）",
            "selection_diff_vs_necessity": "无稀有表过滤（探针要密度；必要账要稀有防撞）",
        },
        "params": {
            "n_windows": args.n_windows, "ngram_len": args.ngram_len, "tail": args.tail,
            "segment_tokens": args.segment_tokens, "chunk_size": args.chunk_size,
            "near_lags": list(near_lags), "remote_js": list(range(args.ngram_len)),
            "ridge_lambda": args.ridge_lambda, "train_frac": args.train_frac,
            "extra_ridge_lambdas": list(extra_lambdas),
            "near_dist_cut": args.near_dist, "remote_dist_cut": args.remote_dist,
            "n_perm": args.n_perm, "seed": args.seed,
            "probe_layers": probe_layers,
            "max_boundaries_per_window": args.max_boundaries_per_window,
        },
        "windows": summary_tally,
        "samples": summary_totals,
        "split": {"train_windows": split_cache[0], "test_windows": split_cache[1]},
        "layer_groups": group_summary,
        "verdict": verdict_txt,
        "timing_sec": round(time.time() - t0, 1),
    }
    (out_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    with (out_dir / "probes.jsonl").open("w", encoding="utf-8") as fp:
        for l in probe_layers:
            for name, res in layer_results[l].items():
                fp.write(json.dumps({"layer": l, "probe": name, **res},
                                    ensure_ascii=False) + "\n")
    with (out_dir / "samples.jsonl").open("w", encoding="utf-8") as fp:
        for w in sorted(samples_by_win):
            fp.write(json.dumps({
                "window_id": w, "byte_offset": w * args.window_bytes,
                "n_tokens": win_tokens[w], "samples": samples_by_win[w],
            }, ensure_ascii=False) + "\n")
    print(json.dumps({"verdict": verdict_txt, "layer_groups": group_summary},
                     ensure_ascii=False, indent=2), flush=True)
    print(f"[kread] summary -> {out_dir / 'summary.json'}\n"
          f"[kread] probes -> {out_dir / 'probes.jsonl'}\n"
          f"[kread] samples -> {out_dir / 'samples.jsonl'}", flush=True)


if __name__ == "__main__":
    main()
