"""KDA 状态置零手术 · 局部/长程解离仪器（kimi122 臂·第四把尺子）。

目的：把 E122 家族「写入内容但解码端读不出」问题推到手术级——**置零 KDA 递归
状态**（20 层线性注意力的跨 token 状态通道），分别测 suffix 局部位置与长程内容
位置的 ΔNLL，直接检验「KDA 状态是否特异性承载长程内容」：
- 置零伤长程（remote ΔNLL ≫ local ΔNLL，CI 分离）→ 状态承载长程、模型在用；
- 两边都不动 → 状态写而不读（读者类墙的手术级复证，与 DeltaNet 臂行为侧并读）；
- 伤局部不伤长程 → 反常（仪器 bug 或局部集污染，停）。

与 DeltaNet 臂的结构差（如实记录）：
- DeltaNet 臂无此臂（e122 b2 行手术在 DeltaNet 上无显式状态接口可置换）；Kimi
  的状态躺在 KimiDynamicCache.recurrent_states——**两段式前向**给了解剖刀：
  prefix 前向（use_cache=True）建缓存 → 快照 → 置零（手术臂）/ 不动（基线臂，
  快照恢复）→ 同一 suffix 前向两次，逐位 ΔNLL 双臂直接可比。
- MLA 全注意力层不手术：其 KV 缓存原样保留，prefix 内容仍经注意力可见——本仪器
  隔离的是「KDA 状态通道」的边际贡献，不是「全部长程通道」。claim 半径如实标注。
- conv 状态不置零（默认）：short conv 只携带 ≤kernel-1 近邻 token，非长程通道；
  --zero-conv-too 可选（读数时如实分层）。

选择链（纯 python，单测覆盖）：
- suffix = 窗 tokens[split:]；remote 计分位 = suffix 内 n-gram 出现，其最早出现
  源**整体在 prefix 内**（s+n ≤ split）且距离 p−s ≥ remote_cut——证据只存在于
  远端；local 计分位 = suffix 内 n-gram 出现，其前一次出现距本次起点 ≤ local_cut
  ——证据就在近旁。冲突位 local 优先（保守：remote 集不得含任何有近旁证据的位），
  重叠计数如实落账。
- ΔNLL = 术臂 − 基线臂，逐位 fp32（transformers 坑 2 对偶守卫：logits 先 .float()
  再 log_softmax）；主判读量 = mean ΔNLL(remote) − mean ΔNLL(local)，窗级
  bootstrap 95% CI（复用 e122.bootstrap_contrast），强响应尾 1 nat，判序 CI 在先。
- 硬件指纹（AGENTS 坑 11/12 纪律）：summary 记 GPU/torch/fla/transformers/
  attn_backend，体制判词一律「同机同 env 内成立」。

Usage:
  python tools/analysis/v3_6/probe_kimi_linear_state_surgery.py \
      --model-path /root/autodl-tmp/models/Kimi-Linear-48B-A3B-Base \
      --corpus /root/autodl-tmp/corpus/corpus_v3.txt \
      --n-windows 40 --device cuda \
      --out-dir /root/autodl-tmp/outputs/kimi_state_surgery_<date>
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
    from tools.analysis.cross_arch import probe_e122_deltanet_book as e122
    from tools.analysis.v3_6 import probe_kimi_linear_load as kload
except ImportError:  # 脚本直跑（sys.path[0] = 脚本目录）
    import sys as _sys
    from pathlib import Path as _P

    _sys.path.insert(0, str(_P(__file__).resolve().parents[1] / "cross_arch"))
    _sys.path.insert(0, str(_P(__file__).resolve().parent))
    import probe_e122_deltanet_book as e122
    import probe_kimi_linear_load as kload

STRONG_LINE_NAT = e122.STRONG_LINE_NAT


# ---------------------------------------------------------------------------
# 计分位选择链（纯 python，单测覆盖）
# ---------------------------------------------------------------------------


def gram_all_occurrences(ids: list[int], g: tuple[int, ...]) -> list[int]:
    """gram 在窗内的一切出现位（起点）。"""
    n = len(g)
    return [p for p in range(len(ids) - n + 1) if tuple(ids[p:p + n]) == g]


def select_dissociation_positions(ids: list[int], split: int, n: int, tail: int,
                                  remote_cut: int, local_cut: int
                                  ) -> tuple[dict[int, tuple[tuple, int]],
                                             dict[int, tuple[tuple, int]], dict]:
    """suffix（tokens[split:]）内的 remote/local 计分尾位。

    remote: 出现位 p ≥ split 且最早出现源 s = occurrences[0] 满足 s+n ≤ split
            （源整体在 prefix）且 p − s ≥ remote_cut。
    local:  出现位 p ≥ split 且存在前一次出现 q（q+n ≤ p）满足 p − (q+n) ≤
            local_cut（证据在近旁；取最近一个 q 判定）。
    冲突位 local 优先（保守口径：remote 集不含任何有近旁证据的位）；尾位重叠
    （两 gram 尾位相撞）先到先得、计数如实。返回 (remote_tails, local_tails,
    counts)，tails: 尾位 t → (gram, 出现位 p)。"""
    tk = len(ids)
    pos_by_gram: dict[tuple, list[int]] = {}
    for p in range(tk - n + 1):
        pos_by_gram.setdefault(tuple(ids[p:p + n]), []).append(p)
    counts = {"n_remote": 0, "n_local": 0, "n_overlap": 0,
              "n_local_wins_over_remote": 0}
    remote: dict[int, tuple[tuple, int]] = {}
    local: dict[int, tuple[tuple, int]] = {}
    for g in sorted(pos_by_gram):
        ps = pos_by_gram[g]
        s = ps[0]
        for p in ps:
            if p < split:
                continue
            # local 判据：最近一次前出现 q（q+n ≤ p）距本次起点 ≤ local_cut
            prevs = [q for q in ps if q + n <= p]
            is_local = bool(prevs) and (p - (max(prevs) + n) <= local_cut)
            is_remote = (s + n <= split) and (p - s >= remote_cut)
            if not (is_local or is_remote):
                continue
            for t in range(p + n, min(p + n + tail, tk)):
                if t in local:
                    counts["n_overlap"] += 1
                elif is_local:
                    if t in remote:  # 冲突 local 优先（保守口径）
                        counts["n_local_wins_over_remote"] += 1
                        del remote[t]
                    local[t] = (g, p)
                    counts["n_local"] += 1
                elif t in remote:
                    counts["n_overlap"] += 1
                else:
                    remote[t] = (g, p)
                    counts["n_remote"] += 1
    return remote, local, counts


def build_window_sums(nll_base: list[float | None],
                      nll_zero: list[float | None],
                      remote_tails: dict[int, tuple],
                      local_tails: dict[int, tuple],
                      split: int = 0) -> dict:
    """单窗 sums（e122.bootstrap_contrast 键位同构：remote→sel，local→ctl）。

    tails 的键是全窗绝对位 t；nll_base/nll_zero 是 suffix 局部坐标
    （长度 = tk − split，绝对位 t 对应 j = t − split）——索引统一换算。"""
    sums = {"n_sel": 0, "sel_d_b1": 0.0, "n_strong": 0,
            "n_ctl": 0, "ctl_d_b1": 0.0}
    for role, tails, k_n, k_d in (("remote", remote_tails, "n_sel", "sel_d_b1"),
                                  ("local", local_tails, "n_ctl", "ctl_d_b1")):
        for t in sorted(tails):
            j = t - split
            if j < 0 or j >= len(nll_base):
                continue
            nb, nz = nll_base[j], nll_zero[j]
            if nb is None or nz is None:
                continue
            d = nz - nb
            sums[k_n] += 1
            sums[k_d] += d
            if role == "remote" and d >= STRONG_LINE_NAT:
                sums["n_strong"] += 1
    return sums


def suffix_position_nll(prefix_last_logits: torch.Tensor,
                        suffix_logits: torch.Tensor,
                        suffix_ids: list[int]) -> list[float | None]:
    """suffix 逐位 NLL（fp32、detach；e122.token_nll 的两段式同构）。

    位置 j 的读数 = 预测 suffix_ids[j] 的 CE：j=0 用 prefix 末行 logits
    （两臂 prefix 前向相同，该位 ΔNLL 恒 0——置零不波及，物理如实）；j≥1 用
    suffix_logits[j-1]。返回长度 = len(suffix_ids)。"""
    rows = [prefix_last_logits.detach().float()] + [
        suffix_logits[0, j - 1].detach().float() for j in range(1, len(suffix_ids))]
    out: list[float | None] = []
    for j, row in enumerate(rows):
        logp = torch.log_softmax(row, dim=-1)
        out.append(-logp[suffix_ids[j]].item())
    return out


def run_dissociation_window(model, ids: list[int], split: int,
                            device: torch.device, zero_layers: list[int],
                            zero_conv: bool = False) -> dict:
    """单窗三前向：prefix 建缓存 → 置零手术 suffix（术臂）→ 快照恢复 suffix
    （基线臂）。返回 {nll_base, nll_zero, n_zeroed}；nll_* 为 suffix 局部坐标
    （长度 = tk − split，全窗绝对位 t 对应 j = t − split）。"""
    pre_ids = torch.tensor([ids[:split]], dtype=torch.long, device=device)
    suf_ids = torch.tensor([ids[split:]], dtype=torch.long, device=device)
    with torch.no_grad():
        out_pre = model(input_ids=pre_ids, use_cache=True)
        cache = out_pre.past_key_values
        snap = kload.snapshot_linear_cache(cache)
        n_zeroed = kload.zero_kda_recurrent_states(cache, zero_layers,
                                                   conv_too=zero_conv)
        out_z = model(input_ids=suf_ids, past_key_values=cache, use_cache=True)
        kload.restore_linear_cache(cache, snap)
        out_b = model(input_ids=suf_ids, past_key_values=cache, use_cache=True)
    suffix_ids = ids[split:]
    nll_base = suffix_position_nll(out_pre.logits[0, -1], out_b.logits, suffix_ids)
    nll_zero = suffix_position_nll(out_pre.logits[0, -1], out_z.logits, suffix_ids)
    return {"nll_base": nll_base, "nll_zero": nll_zero, "n_zeroed": n_zeroed}


def resolve_zero_layers(spec: str, kda_layers: list[int],
                        n_layers: int) -> list[int]:
    """kda（全部）/ early|mid|deep（模型深度三分与 KDA 层集之交）/ 逗号层号。"""
    t = spec.strip().lower()
    if t == "kda":
        return list(kda_layers)
    if t in ("early", "mid", "deep"):
        if t == "early":
            base = [l for l in range(n_layers) if l < n_layers / 3]
        elif t == "mid":
            base = [l for l in range(n_layers)
                    if n_layers / 3 <= l < 2 * n_layers / 3]
        else:
            base = [l for l in range(n_layers) if l >= 2 * n_layers / 3]
        return [l for l in kda_layers if l in base]
    vals = [int(x) for x in spec.split(",") if x.strip()]
    if not vals:
        raise SystemExit("--zero-layers 解析失败")
    return vals


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


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
    p.add_argument("--split-frac", type=float, default=0.6,
                   help="prefix 占窗 token 比例（suffix = 其余）")
    p.add_argument("--ngram-len", type=int, default=3, choices=[2, 3, 4])
    p.add_argument("--tail", type=int, default=3)
    p.add_argument("--remote-cut", type=int, default=192,
                   help="remote 计分位最小源距离（token）")
    p.add_argument("--local-cut", type=int, default=8,
                   help="local 计分位最大近邻出现距离（token）")
    p.add_argument("--zero-layers", default="kda",
                   help="'kda'（全部 20 层）/ early|mid|deep / 逗号层号（0 基）")
    p.add_argument("--zero-conv-too", action="store_true",
                   help="连同 short conv 状态置零（默认不动，读数分层如实）")
    p.add_argument("--strong-line", type=float, default=STRONG_LINE_NAT)
    p.add_argument("--bootstrap", type=int, default=2000)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--max-memory", default="",
                   help="双卡显存约束，如 0:70GiB,1:70GiB")
    p.add_argument("--out-dir",
                   default=f"outputs/kimi_state_surgery_{time.strftime('%Y%m%d')}")
    args = p.parse_args()

    if not (0.2 < args.split_frac < 0.9):
        raise SystemExit("--split-frac ∈ (0.2, 0.9)")
    if args.max_tokens % 64:
        raise SystemExit("--max-tokens 须为 64 的倍数（fla chunk_kda 约束）")
    if args.local_cut < 1 or args.remote_cut < 1:
        raise SystemExit("--remote-cut/--local-cut ≥ 1")

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
        max_memory = {
            (int(k) if k.isdigit() else k): v
            for k, v in (
                kv.split(":", 1) for kv in args.max_memory.split(",") if kv)}
    model, tok, fingerprint = kload.load_model_and_tokenizer(
        args.model_path, device, max_memory=max_memory)
    n_layers = int(model.config.num_hidden_layers)
    zero_layers = resolve_zero_layers(args.zero_layers,
                                      fingerprint["kda_layers_0based"], n_layers)
    if not zero_layers:
        raise SystemExit("--zero-layers 解析为空集，响亮拒绝")
    print(f"[ksurg] model={Path(args.model_path).name} device={device.type} "
          f"zero_layers={zero_layers} conv_too={args.zero_conv_too}",
          flush=True)

    items_path = out_dir / "items.jsonl"
    window_sums: list[dict] = []
    tally = {"n_windows_attempted": 0, "n_windows_used": 0, "n_windows_empty": 0}
    totals = {"n_remote": 0, "n_local": 0, "n_overlap": 0,
              "n_local_wins_over_remote": 0}
    max_byte_touched = 0

    with corpus.open("rb") as f:
        for wi in range(args.n_windows):
            w_abs = args.start_window + wi
            f.seek(w_abs * args.window_bytes)
            raw = f.read(args.window_bytes)
            if len(raw) < args.window_bytes:
                print(f"[ksurg] 语料前缀尽（窗 {w_abs}），停", flush=True)
                break
            max_byte_touched = max(max_byte_touched, (w_abs + 1) * args.window_bytes)
            ids, full_len = kload.tokenize_window(
                tok, raw.decode("utf-8", errors="replace"), args.max_tokens)
            tk = len(ids)
            split = int(tk * args.split_frac)
            if split < args.ngram_len + 1 or tk - split < args.ngram_len + args.tail:
                tally["n_windows_empty"] += 1
                continue
            remote, local, cnt = select_dissociation_positions(
                ids, split, args.ngram_len, args.tail,
                args.remote_cut, args.local_cut)
            tally["n_windows_attempted"] += 1
            for k, v in cnt.items():
                totals[k] = totals.get(k, 0) + v
            if not remote or not local:
                tally["n_windows_empty"] += 1
                continue
            rec = run_dissociation_window(model, ids, split, device,
                                          zero_layers, args.zero_conv_too)
            sums = build_window_sums(rec["nll_base"], rec["nll_zero"],
                                     remote, local, split=split)
            if sums["n_sel"] > 0 and sums["n_ctl"] > 0:
                tally["n_windows_used"] += 1
                window_sums.append(sums)
                with items_path.open("a", encoding="utf-8") as fi:
                    for role, tails in (("remote", remote), ("local", local)):
                        for t in sorted(tails):
                            g, pp = tails[t]
                            j = t - split  # nll_* 为 suffix 局部坐标
                            nb_t = rec["nll_base"][j] if 0 <= j < len(rec["nll_base"]) else None
                            nz_t = rec["nll_zero"][j] if 0 <= j < len(rec["nll_zero"]) else None
                            fi.write(json.dumps({
                                "window_id": w_abs, "role": role,
                                "token_pos": t, "gram": list(g), "repeat_pos": pp,
                                "NLL_base": nb_t,
                                "NLL_zero": nz_t,
                                "delta": (None if nb_t is None or nz_t is None
                                          else nz_t - nb_t),
                            }, ensure_ascii=False) + "\n")
            else:
                tally["n_windows_empty"] += 1
            print(f"[ksurg] win {w_abs:5d} remote={sums['n_sel']:3d} "
                  f"local={sums['n_ctl']:3d} strong={sums['n_strong']:3d} "
                  f"({time.time() - t0:.0f}s)", flush=True)

    # 同卷锚
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
    mean_remote = sum(w["sel_d_b1"] for w in window_sums) / n_sel if n_sel else None
    mean_local = sum(w["ctl_d_b1"] for w in window_sums) / n_ctl if n_ctl else None
    boot = e122.bootstrap_contrast(window_sums, args.bootstrap, args.seed + 1)
    n_strong = sum(w["n_strong"] for w in window_sums)

    if mean_remote is None or mean_local is None:
        verdict_txt = "无读数"
    elif not boot["ci_excludes_zero"]:
        verdict_txt = "解离未落——remote−local 对比 CI 含 0（剂量未落或状态不承载，转 500 窗/换层集）"
    elif boot["point"] <= 0:
        verdict_txt = "反常（置零伤局部 ≥ 伤长程——仪器 bug 或局部集污染，停，转口径审计）"
    else:
        verdict_txt = ("解离成立方向：置零 KDA 状态特异性伤长程读取"
                       + ("（强：强响应尾在板）" if mean_remote >= STRONG_LINE_NAT
                          else "（弱：部分在板）")
                       + "——与必要性账/读出探针并读")

    summary = {
        "probe": "KDA 状态置零手术 · 局部/长程解离（kimi122 臂·第四把尺子）",
        "arm": "kimi122",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "model_fingerprint": fingerprint,
        "claim_scope": "MLA KV 不手术——隔离的是 KDA 状态通道的边际贡献，非全部长程通道",
        "corpus": {
            "path": str(corpus),
            "window_bytes": args.window_bytes,
            "start_window": args.start_window,
            "scored_prefix_bytes": max_byte_touched,
            "scored_prefix_sha256": prefix_sha,
            "corpus_size_at_run": os.path.getsize(corpus),
        },
        "params": {
            "n_windows": args.n_windows, "split_frac": args.split_frac,
            "ngram_len": args.ngram_len, "tail": args.tail,
            "remote_cut": args.remote_cut, "local_cut": args.local_cut,
            "zero_layers": zero_layers, "zero_conv_too": args.zero_conv_too,
            "strong_line_nat": args.strong_line, "bootstrap": args.bootstrap,
            "seed": args.seed,
        },
        "windows": tally,
        "remote": {"n": n_sel, "mean_delta": mean_remote},
        "local": {"n": n_ctl, "mean_delta": mean_local},
        "contrast_remote_minus_local": {
            **boot,
            "mean": (mean_remote - mean_local) if (mean_remote is not None and mean_local is not None) else None,
        },
        "strong_tail": {
            "n_strong": n_strong,
            "rate_of_remote": (n_strong / n_sel) if n_sel else None,
        },
        "selection_audit": totals,
        "verdict": verdict_txt,
        "timing_sec": round(time.time() - t0, 1),
    }
    (out_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"verdict": verdict_txt,
                      "contrast": summary["contrast_remote_minus_local"]},
                     ensure_ascii=False, indent=2), flush=True)
    print(f"[ksurg] items -> {items_path}", flush=True)


if __name__ == "__main__":
    main()
