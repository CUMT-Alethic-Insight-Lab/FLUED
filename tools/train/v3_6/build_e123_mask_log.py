"""E123 离线选择器预计算（2026-09-07，冻结任务书 v1.3 §4/槽五；surprisal 代理
验证 ρ=0.000 证伪后改真测量版）。

真测量批化：每窗一次 batched 前向（B = 1 基线 + n_real 遮蔽变体），遮蔽变体 =
门②双遮蔽（注意力 block_mask + row_perm_override 前向级逐样本行交换，槽一同码
同源）；每 chunk 信息量 = 其 k∈{1,2} 下游依赖位（valid 字节、网格内）的逐位
ΔNLL_total（direct/backbone 等权）逐距离均值取最大。阈值 0.05 nat（冻结）。
逐窗决策日志落盘（槽五）：遮蔽块字节区间 + 依赖位绝对字节位 + 距离 + 信息量
——训练时零额外前向，决策按 window_id 索引。

窗流复现：StreamingReconstructionDataset(seq_len=4096, samples_per_worker=50000,
seed=42, batch=1, num_workers=0)——与 v3_7_d1_w1.json 训练流逐项同构。

用法：
  python tools/train/v3_6/build_e123_mask_log.py --ckpt <a-w1> --data-path ... \
      --n-windows 10000 --threshold 0.05 --out outputs/e123_mask_log_seed42.jsonl \
      --cell-relaxed
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # repo root
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # tools/

from flued.data import PAD_ID, StreamingReconstructionDataset  # noqa: E402
from tools.analysis.v3_6.probe_e122_necessity_book import (  # noqa: E402
    assert_cell_keys,
    gather_nll,
)
from tools.analysis.v3_6.gate_e123_necessity_v2 import row_swap_perm  # noqa: E402
from tools.analysis.v3_6.probe_oracle_write_verdict import load_model  # noqa: E402
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402

MAX_DIST = 2  # 依赖带（回执二直方图：k=1 占 30%、k=2 占 70%、k≥3≈0）


def _load_trimmed(ckpt: Path, device: torch.device, max_chunks_trim: int = 64):
    """选择器专用装载：max_chunks 构建期截断（解码网格从 1024 缩到 64，前向
    ~15× 提速）——真实行前 n_real 读数与默认构建逐位一致（本地对拍 max|Δ|=0），
    chunk_pos 截到前 64 行（实窗 n_real ≤ 64，截掉的全是未用 padding 槽）。
    只用于零训练测量，不进训练臂。"""
    import json
    from argparse import Namespace
    from tools.train.v3_6.train_v36 import build_model

    cfg = json.loads((ckpt / "resolved_config.json").read_text(encoding="utf-8"))
    cfg["data_manifest"] = ""
    if device.type != "cuda":
        cfg["kda_impl"] = "torch"
    cfg["max_chunks"] = max_chunks_trim
    ns = Namespace(**cfg)
    model = build_model(ns).to(device)  # 先搬设备（漏搬=CPU 模型吃 CUDA 输入，第二次咬）
    payload = torch.load(ckpt / "latest.pt", map_location=device, weights_only=False)
    payload["model"]["chunk_pos.weight"] = payload["model"]["chunk_pos.weight"][:max_chunks_trim]
    model.load_state_dict(payload["model"], strict=True)
    for p_ in model.parameters():
        p_.requires_grad_(False)
    model.eval()
    return model, ns, int(payload.get("step", 0))


class _ForwardSlice:
    """子批前向的单变体视图（ld/lb/ca/oa）。"""

    def __init__(self, out: dict, v: int):
        self.ld = out["logits_direct"][v:v+1]
        self.lb = out["logits_backbone"][v:v+1]
        self.ca = out["chunks"].chunk_ids[v:v+1]
        self.oa = out["chunks"].offsets[v:v+1]


@torch.no_grad()
def measure_window(model, ns, clean, n_variants_max: int = 80) -> dict:
    """一窗真测量（一次 batched 前向）：返回 {masked: {c: info}, dep_bytes}。
    clean: (1, T) 训练流窗（无 mask）。"""
    out0 = s1.s1_forward(model, clean, ns)
    ca, oa = out0["chunks"].chunk_ids, out0["chunks"].offsets
    n_real = int(out0["chunks"].chunk_mask[0].sum())
    T = clean.size(1)
    if n_real < 3:
        return {"masked": {}, "n_real": n_real}
    if n_real > int(ns.max_chunks):
        raise RuntimeError(f"窗真实 chunk 数 {n_real} > 截断网格 {ns.max_chunks}——"
                           "截断口径不适用（负载卫检，响亮拒绝）")
    cands = list(range(min(n_real - 1, n_variants_max - 1)))  # 末 chunk 无下游

    # 子批化（显存护栏）：alibi 偏置 (B,H,T,T) 随 B 平方级占显存（B=65 实测 OOM
    # 24GB）；子批 ≤7 变体/前向，结果拼回。返回 outs[v] = 变体 v 的前向行。
    outs = [None] * (1 + len(cands))
    outs[0] = out0
    SLICE = 7  # 截断网格后解码成本消减 15×，B=8 的 alibi 偏置 ≈3.2GB 为约束
    for s0 in range(0, len(cands), SLICE):
        sub = cands[s0:s0 + SLICE]
        B = 1 + len(sub)
        src = clean.repeat(B, 1)
        masks = torch.zeros(B, 1, 1, T, dtype=torch.bool, device=clean.device)
        perms: list[list[int] | None] = [None]
        for i, c in enumerate(sub):
            v = i + 1
            for t in range(T):
                if int(ca[0, t]) == c:
                    masks[v, 0, 0, t] = True
            perms.append(row_swap_perm(c, n_real))
        out = s1.s1_forward(model, src, ns, attn_block_mask=masks,
                            row_perm_override=perms)
        # 卫检：子批内所有变体分段与基线逐位一致
        cb0, ob0 = out["chunks"].chunk_ids[0], out["chunks"].offsets[0]
        if not bool((cb0 == ca[0]).all()):
            raise RuntimeError(f"子批 {s0}: 分段漂移——仪器 bug")
        for i, c in enumerate(sub):
            outs[1 + s0 + i] = _ForwardSlice(out, i + 1)

    # 逐块信息量：k∈{1,2} 依赖位逐位 ΔNLL_total（direct/backbone 等权）的
    # 逐距离均值取最大
    masked = {}
    dep_bytes = {}
    for i, c in enumerate(cands):
        out_v = outs[1 + i]
        info = {}
        for d in range(1, MAX_DIST + 1):
            pos = [t for t in range(T)
                   if int(ca[0, t]) == c + d
                   and 0 <= int(oa[0, t]) < int(ns.max_span)]
            if not pos:
                continue
            ids = [int(clean[0, t]) for t in pos]
            d_d = sum(gather_nll(out_v.ld, out_v.ca, out_v.oa, pos, ids)) \
                - sum(gather_nll(out0["logits_direct"][0:1], ca, oa, pos, ids))
            d_b = sum(gather_nll(out_v.lb, out_v.ca, out_v.oa, pos, ids)) \
                - sum(gather_nll(out0["logits_backbone"][0:1], ca, oa, pos, ids))
            info[d] = 0.5 * (d_d + d_b) / len(pos)  # 逐位均值（两面等权）
        if info:
            best_d = max(info, key=lambda d: info[d])
            masked[c] = round(info[best_d], 5)
            src_pos = [t for t in range(T) if int(ca[0, t]) == c]
            dep_bytes[c] = {
                "distance": best_d,
                "src_byte_range": [min(src_pos), max(src_pos) + 1] if src_pos else None,
                "positions": [t for t in range(T)
                              if int(ca[0, t]) == c + best_d
                              and 0 <= int(oa[0, t]) < int(ns.max_span)],
            }
    return {"masked": masked, "dep_bytes": dep_bytes, "n_real": n_real}


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    p = argparse.ArgumentParser()
    p.add_argument("--ckpt", required=True)
    p.add_argument("--data-path", required=True)
    p.add_argument("--n-windows", type=int, default=10000)
    p.add_argument("--threshold", type=float, default=0.05)
    p.add_argument("--out", required=True)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--max-candidates", type=int, default=80,
                   help="每窗测量变体上限（候选 chunk 数；冒烟用小值）")
    p.add_argument("--cell-relaxed", action="store_true")
    args = p.parse_args()
    device = torch.device(
        "cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu"
    )
    model, ns, step = _load_trimmed(Path(args.ckpt), device)
    assert_cell_keys(ns, model.config, strict=not args.cell_relaxed)
    ns.burst_prob = 0
    ns.cloze_prob = 0
    ns.retrieval_prob = 0
    ns.data_path = args.data_path

    ds = StreamingReconstructionDataset(
        file_path=ns.data_path, seq_len=int(ns.seq_len),
        samples_per_worker=int(getattr(ns, "stream_samples_per_worker", 50000)),
        seed=int(ns.seed),
    )
    loader = torch.utils.data.DataLoader(ds, batch_size=1, shuffle=False, num_workers=0)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    wi = 0
    n_sel = 0
    with out_path.open("w", encoding="utf-8") as f:
        for batch in loader:
            if wi >= args.n_windows:
                break
            ids = batch[0][0]  # DataLoader 出 (src, tgt) 对 → src 批的首行 (T+1,)
            cut = int(ids.ne(PAD_ID).sum())
            clean = ids[:cut].unsqueeze(0).to(device)
            rec = measure_window(model, ns, clean, n_variants_max=args.max_candidates)
            sel = {c: s for c, s in rec["masked"].items() if s > args.threshold}
            deps = []
            for c in sorted(sel):
                d = rec["dep_bytes"][c]
                deps.append({
                    "src_chunk": c,
                    "src_byte_range": rec["dep_bytes"][c]["src_byte_range"],
                    "distance": d["distance"],
                    "positions": d["positions"],
                    "info": sel[c],
                })
            f.write(json.dumps({
                "window_id": wi,
                "n_real": rec["n_real"],
                "masked_chunks": sorted(sel),
                "info_scores": {str(c): sel[c] for c in sorted(sel)},
                "dependency_pairs": deps,
            }, ensure_ascii=False) + "\n")
            n_sel += len(sel)
            wi += 1
            if wi % 200 == 0:
                print(f"[e123-selector] win {wi} sel_total={n_sel} "
                      f"({time.time()-t0:.0f}s)", flush=True)
    print(json.dumps({
        "n_windows": wi, "n_selected_chunks": n_sel,
        "blocks_per_window": round(n_sel / max(wi, 1), 3),
        "timing_sec": round(time.time() - t0, 1),
    }, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
