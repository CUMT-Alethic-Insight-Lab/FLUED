"""Induction 分数仪器（双时间点版，A3 归因章的前置测量，2026-08-22，零训练）。

A3 暂扣的两个候选归因：(a) 形式理解上限 vs (b) 基础复制回路从未形成。本仪器
测 (b) 的前体：SLM backbone 注意力头的 prefix-matching（induction）行为——
**窗内**复制回路在不在。

构造（Olsson 族 chunk 级适配）：k 个随机字节段 S_1..S_k（各 ~16B 均匀随机）
排成 S_1..S_k S_1..S_k 双拷贝窗；induction 头应当在第二拷贝 S_i 的 chunk 上
把注意力投给**第一拷贝 S_{i+1}** 的 chunk（前缀匹配的"下一个"）。逐 block
逐 head 报 induction score（query→target 注意力质量）+ 均匀基线 1/n。

判读矩阵（预注册，三层）：
  分数显著超均匀基线 → 窗内复制回路在，四代失败归因"回路到状态通道没有路由"；
  分数贴基线 → 窗内复制回路都没长出来，解法=数据注突发性（Q13 系）；
  反向不成立：窗内回路在 ≠ 状态通道能承载复制——仪器只确认/排除前体。

双时间点（K3 复核强化项）：
  init = 同种子新建模型 + 底座前端（backbone 随机初始化；run 未存 step-0
         快照，如实标注）；
  trained = 被测 checkpoint（默认 Q12 40K）。
  两点对照：底座有/现在没有 → 回路曾形成被我们的训练砍掉（装饰律新例）；
  底座就没有 → 从未形成；都有 → 纯路由问题。

机制注记（K3 写入）：induction 头是注意力的窗内复制回路；我们的检索任务要求
**过窗**经 KDA 状态的复制——两者不是同一机制，仪器只测前体。

Usage:
  python tools/analysis/v3_6/probe_induction_score.py --device cuda
  CPU 冒烟: py -3.14 -X utf8 tools/analysis/v3_6/probe_induction_score.py --device cpu --n-docs 2
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from argparse import Namespace
from pathlib import Path

import torch
import torch.nn.functional as F

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.train.v3_6.train_v36 import build_model  # noqa: E402

TRAINED_RUN = "checkpoints/v37ks_b_sm_retrieval_cjk_ex3_A_20k_ctx4096_20260822"  # Q12 40K
OUT_DIR = "outputs/induction_score_20260822"
SEG_LEN = 16
N_SEGS = 8
DOC_SEED = 20260822

_ATTN_CAPTURE = []


def _sdpa_capture(q, k, v, attn_mask=None, **kw):
    """SDPA replacement that captures attention weights (math kernel form)."""
    scale = q.size(-1) ** 0.5
    attn = (q @ k.transpose(-2, -1)) / scale
    if attn_mask is not None:
        if attn_mask.dtype == torch.bool:
            attn = attn.masked_fill(~attn_mask, float("-inf"))
        else:
            attn = attn + attn_mask
    attn = attn.softmax(dim=-1)
    _ATTN_CAPTURE.append(attn.detach())
    return attn @ v


def _build_doc(gen: torch.Generator, seg_len: int = SEG_LEN, n_segs: int = N_SEGS):
    """k random segments x2 copies: query byte = start of 2nd copy of S_j,
    target byte = start of 1st copy of S_{j+1} (chunk-level induction pairs)."""
    segs = [bytes(int(torch.randint(1, 256, (1,), generator=gen)) for _ in range(seg_len)) for _ in range(n_segs)]
    doc = b"".join(segs) * 2
    off = [0]
    for s in segs:
        off.append(off[-1] + len(s))
    total1 = off[-1]
    # seg j (0-based) occupies [off[j], off[j+1]) in copy 1, [total1+off[j], ...) in copy 2
    pairs = []
    for j in range(n_segs - 1):
        # at the 2nd copy of seg j, the "next after the 1st occurrence" is seg j+1 (copy 1)
        query_byte = total1 + off[j]
        target_byte = off[j + 1]
        pairs.append((query_byte, target_byte))
    ids = torch.tensor([b + 1 for b in doc], dtype=torch.long)
    return ids, pairs


@torch.no_grad()
def induction_scores(model, ids, pairs, device):
    """Front-end unpatched, then the SLM backbone forward under SDPA capture;
    per (block, head) induction score."""
    global _ATTN_CAPTURE
    source = ids.unsqueeze(0).to(device)
    byte_states, confidence, valid, _ = model._encode(source)
    hard_cut, utf8_cont, _ = model._cuts(source, confidence, valid)
    chunks = model.chunk_builder(byte_states, valid, hard_cut, confidence)
    chunks = model.bridge(chunks, byte_states, confidence, valid, utf8_cont)
    k_rows, v_rows, _sn, _memory, _index = model._slm_store_rows(chunks)
    n = chunks.chunk_mask.size(1)
    pos = model.chunk_pos.weight.unsqueeze(0)[:, :n]
    _ATTN_CAPTURE = []
    orig = F.scaled_dot_product_attention
    F.scaled_dot_product_attention = _sdpa_capture
    try:
        model.backbone(k_rows, v_rows, chunks.chunk_mask, pos)
    finally:
        F.scaled_dot_product_attention = orig
    cid = chunks.chunk_ids[0]  # (T,) byte -> chunk id

    def chunk_of(byte_pos):
        j = int(cid[byte_pos])
        return j if j >= 0 else None

    results = {}
    bb = model.backbone
    names = ["block1_cross"] + [f"self{i}" for i in range(len(bb.self_blocks))]
    for bi, attn in enumerate(_ATTN_CAPTURE):
        name = names[bi] if bi < len(names) else f"block{bi}"
        a = attn[0].float()  # (H, n_q, n_kv)
        for h in range(a.size(0)):
            scores = []
            for qb, tb in pairs:
                qc, tc = chunk_of(qb), chunk_of(tb)
                if qc is None or tc is None or qc >= a.size(1) or tc >= a.size(2):
                    continue
                scores.append(float(a[h, qc, tc]))
            if scores:
                results[f"{name}/h{h}"] = round(sum(scores) / len(scores), 4)
    n_chunks = int(chunks.chunk_mask[0].sum())
    return results, n_chunks


def load_trained(run_dir: str, device):
    import json as _json
    import tools.train.v3_6.train_v36_s1 as s1
    cfg = _json.loads((Path(run_dir) / "resolved_config.json").read_text(encoding="utf-8"))
    cfg["data_manifest"] = ""
    if device.type != "cuda":
        cfg["kda_impl"] = "torch"
    ns = Namespace(**cfg)
    if s1._BPE_TOKENIZER is None and getattr(ns, "mask_mode", "mixed") == "mixed" and ns.mask_prob > 0:
        s1._load_bpe_tokenizer(ns.bpe_tokenizer_path)
    model = build_model(ns).to(device)
    payload = torch.load(Path(run_dir) / "latest.pt", map_location=device, weights_only=False)
    model.load_state_dict(payload["model"], strict=True)
    model.eval()
    for p in model.parameters():
        p.requires_grad_(False)
    return model, ns


def load_init(device, ns):
    """Same-seed fresh model + 底座前端（init_checkpoint 前缀）；backbone 随机
    初始化（run 未存 step-0 快照——如实标注的近似 init 点）。"""
    import tools.train.v3_6.train_v36_s1 as s1
    torch.manual_seed(ns.seed)
    model = build_model(ns).to(device)
    payload = torch.load(ns.init_checkpoint, map_location=device, weights_only=False)
    current = model.state_dict()
    compat = {k: v for k, v in payload["model"].items() if k in current and current[k].shape == v.shape}
    prefixes = [p.strip() for p in ns.freeze_prefixes.split(",") if p.strip()]
    compat = {k: v for k, v in compat.items() if any(k.startswith(p) for p in prefixes)}
    model.load_state_dict(compat, strict=False)
    model.eval()
    for p in model.parameters():
        p.requires_grad_(False)
    return model


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    p = argparse.ArgumentParser()
    p.add_argument("--run-dir", default=TRAINED_RUN)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--n-docs", type=int, default=16)
    p.add_argument("--seg-len", type=int, default=SEG_LEN)
    p.add_argument("--n-segs", type=int, default=N_SEGS)
    p.add_argument("--out-dir", default=OUT_DIR)
    args = p.parse_args()
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    model_tr, ns = load_trained(args.run_dir, device)
    model_init = load_init(device, ns)
    print(f"[ind] models loaded (trained={Path(args.run_dir).name} + init点) ({time.time() - t0:.0f}s)", flush=True)

    import tools.train.v3_6.train_v36_s1 as s1  # noqa
    import flued.v36.model as M
    orig_sdpa = F.scaled_dot_product_attention

    per_tp = {}
    for tp, model in (("init", model_init), ("trained", model_tr)):
        all_scores: dict[str, list] = {}
        n_chunks_l = []
        for d in range(args.n_docs):
            gen = torch.Generator().manual_seed(DOC_SEED + d)
            ids, pairs = _build_doc(gen, args.seg_len, args.n_segs)
            scores, n_chunks = induction_scores(model, ids, pairs, device)
            n_chunks_l.append(n_chunks)
            for k, v in scores.items():
                all_scores.setdefault(k, []).append(v)
        mean_scores = {k: round(sum(v) / len(v), 4) for k, v in all_scores.items()}
        per_tp[tp] = {
            "scores": mean_scores,
            "uniform_baseline": round(1.0 / (sum(n_chunks_l) / len(n_chunks_l)), 4),
            "n_chunks_mean": round(sum(n_chunks_l) / len(n_chunks_l), 1),
        }
        top = sorted(mean_scores.items(), key=lambda kv: -kv[1])[:3]
        print(f"[ind] {tp}: baseline={per_tp[tp]['uniform_baseline']} top3={top} ({time.time() - t0:.0f}s)", flush=True)

    def summarize(tp):
        s = per_tp[tp]["scores"]
        base = per_tp[tp]["uniform_baseline"]
        if not s:
            return {"max": None, "mean": None, "baseline": base}
        return {"max": max(s.values()), "mean": round(sum(s.values()) / len(s), 4), "baseline": base,
                "n_heads_gt_2x": sum(1 for v in s.values() if v > 2 * base)}

    si, st = summarize("init"), summarize("trained")
    # 判读（预注册三层矩阵）
    if st["n_heads_gt_2x"] > 0:
        verdict = ("窗内复制回路在（trained 有 head 显著超 2× 基线）——四代失败归因向\"回路到状态通道没有路由\"倾斜；"
                   "注意反向不成立：窗内回路在 ≠ 状态通道能承载复制。")
    else:
        verdict = ("窗内复制回路贴基线（无 head 显著超 2× 基线）——基础复制回路未形成，"
                   "四代失败不冤；解法=数据注突发性（Q13 系）；A3 归因章向\"回路缺席\"倾斜。")
    report = {
        "probe": "induction 分数仪器（双时间点版，A3 归因章前置）",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "checkpoint": {"trained": Path(args.run_dir).name,
                       "init": "同种子新建+底座前端（backbone 随机初始化，run 未存 step-0 快照）"},
        "params": {"n_docs": args.n_docs, "seg_len": SEG_LEN, "n_segs": N_SEGS, "doc_seed": DOC_SEED},
        "summary": {"init": si, "trained": st},
        "per_head": per_tp,
        "verdict": verdict,
        "timing_sec": round(time.time() - t0, 1),
    }
    out_path = out_dir / "induction_score.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "induction 分数仪器（双时间点版）— A3 归因章前置测量",
        f"日期 {report['created']}  设备 {device.type}  docs={args.n_docs}（{N_SEGS}段×{SEG_LEN}B×双拷贝）",
        "",
        f"均匀基线 1/n_chunks: init {si['baseline']} / trained {st['baseline']}",
        f"init    : max {si['max']} mean {si['mean']} >2×基线 head 数 {si['n_heads_gt_2x']}",
        f"trained : max {st['max']} mean {st['mean']} >2×基线 head 数 {st['n_heads_gt_2x']}",
        "",
        "逐 head 明细（trained top5）：",
    ]
    top5 = sorted(per_tp["trained"]["scores"].items(), key=lambda kv: -kv[1])[:5]
    for k, v in top5:
        lines.append(f"  {k}: {v}")
    lines += ["", "判读矩阵（预注册三层）与 verdict 见 JSON。", f"判词：{verdict}", "", f"完整数据: {out_path}"]
    (out_dir / "SUMMARY.txt").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
