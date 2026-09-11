"""E123 离线选择器预计算（2026-09-07，冻结任务书 v1.3 §4/槽五；surprisal 代理
验证 ρ=0.000 证伪后改真测量版）。

真测量批化：每窗一次 batched 前向（B = 1 基线 + n_real 遮蔽变体），遮蔽变体 =
门②双遮蔽（注意力 block_mask + row_perm_override 前向级逐样本行交换，槽一同码
同源）；每 chunk 信息量 = 其 k∈{1,2} 下游依赖位（valid 字节、网格内）的逐位
ΔNLL_total（direct/backbone 等权）逐距离均值取最大。阈值 0.05 nat（冻结）。
逐窗决策日志落盘（槽五）：遮蔽块字节区间 + 依赖位绝对字节位 + 距离 + 信息量
——训练时零额外前向，决策按 window_id 索引。

每窗 JSONL 字段（2026-09-10 起追加 hard_cut，用户裁定：切点是窗的确定函数，
与遮蔽决策同批预计算产出，训练时零额外前向）：
  window_id / n_real / masked_chunks / info_scores / dependency_pairs（旧五件）
  hard_cut: list[int]（0/1，长度 = 该窗 trimmed 字节数 T）——干净窗（无注意力
    遮蔽）经 _encode→_cuts 的预算后切点；E124 训练侧接线的消费源（读入后
    torch.tensor(..., dtype=torch.bool).unsqueeze(0) 即合 cuts_override 的
    (B=1, T) bool 契约），本脚本只负责落盘，训练侧消费属后续施工。
  同窗测量语义同步：遮蔽变体前向一律 cuts_override=hard_cut（内容缺席、结构
  不动——锚定段界器下遮蔽会翻转切点（实测漂移 95%），不钉则 ΔNLL 被网格
  漂移污染）。

窗流复现：StreamingReconstructionDataset(seq_len=4096, samples_per_worker=50000,
seed=42, batch=1, num_workers=0)——与 v3_7_d1_w1.json 训练流逐项同构。

E124 剂量段（2026-09-10，任务书冻结 v1.0）：E124 生产日志
(outputs/e124_mask_log_seed42.jsonl) 用 --threshold 0.02 --max-blocks 3
--max-chunks-trim 256 重建——τ=0.02 nat 放宽剂量下限、每窗遮蔽 ≤3 块封顶
（按信息量降序取 top-N，平局按 chunk 序保确定性）、截断网格 64→256 承接
4096B 窗 n_real≈173 的新体制（64 会触发负载卫检 RuntimeError）。

E124 候选消偏置（2026-09-11，用户裁定）：--candidate-mode random 时候选按
SHA256(seed:wi:c) 确定性抽样（跨机/跨库版本逐位一致，供双机一致性抽查），
种子 --candidate-seed 与数据流种子分离；每行落 cand_mode/cand_seed/
candidates/hw（硬件指纹）四审计字段。front 为 E123 旧口径复现路径。

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


def _hw_fingerprint(device: torch.device) -> str:
    """硬件指纹（E124 裁定 2026-09-11：mask log 全量带硬件指纹，双机一致性
    抽查与日后追责的审计锚）。"""
    import platform
    gpu = torch.cuda.get_device_name(0) if device.type == "cuda" else "cpu"
    import numpy as _np
    return f"{gpu} | py{platform.python_version()} | torch{torch.__version__} | np{_np.__version__}"


def _det_candidates(n_cand: int, k: int, seed: int, wi: int) -> list[int]:
    """E124 候选消偏置（用户裁定 2026-09-11，坑9位置先验互染条款）：候选不再
    取位置序前 k 块（新体制 173 块/窗下只剩 46% 覆盖且前段偏置，与位置先验
    探针同轴互染），改按 SHA256(seed:wi:c) 排序抽 k 个再按数值升序——纯标准库
    哈希，跨机/跨 numpy/跨 Python 微版本逐位一致（双机一致性抽查的确定性底座）。
    候选抽样种子与数据流种子分离（--candidate-seed 独立于 dataset seed）。"""
    import hashlib
    scored = sorted(range(n_cand),
                    key=lambda c: hashlib.sha256(f"{seed}:{wi}:{c}".encode()).digest())
    return sorted(scored[:k])


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
def measure_window(model, ns, clean, n_variants_max: int = 80,
                   cand_seed: int | None = None, window_id: int | None = None) -> dict:
    """一窗真测量（一次 batched 前向）：返回 {masked: {c: info}, dep_bytes,
    hard_cut}。clean: (1, T) 训练流窗（无 mask）。"""
    out0 = s1.s1_forward(model, clean, ns)
    ca, oa = out0["chunks"].chunk_ids, out0["chunks"].offsets
    n_real = int(out0["chunks"].chunk_mask[0].sum())
    T = clean.size(1)
    # E124（用户裁定 2026-09-10）：干净窗切点随决策同批落盘；同时钉死本窗一切
    # 遮蔽变体前向（内容缺席、结构不动）。前端冻结 → _encode 在 no_grad 下
    # 重算零梯度（model.py:2390），相对整窗变体前向成本可忽略。
    _bs0, conf0, valid0, _ = model._encode(clean)
    hard_cut0, _u8_0, _of0 = model._cuts(clean, conf0, valid0)
    if n_real < 3:
        return {"masked": {}, "n_real": n_real, "hard_cut": hard_cut0, "cands": []}
    if n_real > int(ns.max_chunks):
        raise RuntimeError(f"窗真实 chunk 数 {n_real} > 截断网格 {ns.max_chunks}——"
                           "截断口径不适用（负载卫检，响亮拒绝）")
    k_cand = min(n_real - 1, n_variants_max - 1)
    if cand_seed is not None and window_id is not None:
        cands = _det_candidates(n_real - 1, k_cand, cand_seed, window_id)
    else:
        cands = list(range(k_cand))  # 旧口径：位置序前 k 块（E123 复现路径）

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
                            row_perm_override=perms,
                            cuts_override=hard_cut0.expand(B, -1))
        # 钉死核验（E124）：变体前向已复用干净窗切点，子批内所有行（基线行 +
        # 遮蔽变体行）的网格必须与干净基线逐位一致——不一致 = 钉死接线断了，
        # 响亮报错。（原卫检只查子批基线行 [0]，变体行漂移漏抓；口径随钉死
        # 一并修正为全行核验。）
        if not (bool((out["chunks"].chunk_ids == ca).all())
                and bool((out["chunks"].offsets == oa).all())):
            raise RuntimeError(f"子批 {s0}: 切点钉死后网格仍漂移——"
                               "cuts_override 接线断了（仪器 bug）")
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
    return {"masked": masked, "dep_bytes": dep_bytes, "n_real": n_real,
            "hard_cut": hard_cut0, "cands": cands}


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
    p.add_argument("--max-blocks", type=int, default=0,
                   help="每窗遮蔽块数封顶（0=不封顶=E123 旧口径; >0 时过阈块按信息量 "
                        "降序取 top-N, 平局按 chunk 序保确定性——E124 剂量 3）")
    p.add_argument("--max-chunks-trim", type=int, default=64,
                   help="选择器专用 max_chunks 构建期截断（E123 旧口径 64; E124 新体制 "
                        "n_real≈173 须 256, 否则负载卫检 RuntimeError）")
    p.add_argument("--cell-relaxed", action="store_true")
    p.add_argument("--candidate-mode", default="front", choices=["front", "random"],
                   help="候选口径：front=位置序前 k 块（E123 旧口径复现路径）；"
                        "random=SHA256 确定性随机抽 k 块（E124 生产口径，用户裁定 "
                        "2026-09-11 消位置偏置，与必要性账均匀抽样同轴）")
    p.add_argument("--candidate-seed", type=int, default=20260911,
                   help="候选抽样种子（与数据流种子分离落盘；仅 random 模式生效）")
    args = p.parse_args()
    device = torch.device(
        "cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu"
    )
    model, ns, step = _load_trimmed(Path(args.ckpt), device, max_chunks_trim=args.max_chunks_trim)
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
    hw = _hw_fingerprint(device)
    print(f"[e123-selector] hw: {hw}", flush=True)
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
            rec = measure_window(model, ns, clean, n_variants_max=args.max_candidates,
                                 cand_seed=(args.candidate_seed
                                            if args.candidate_mode == "random" else None),
                                 window_id=wi)
            sel = {c: s for c, s in rec["masked"].items() if s > args.threshold}
            if args.max_blocks > 0 and len(sel) > args.max_blocks:
                # E124 剂量封顶（--max-blocks）: 按信息量降序取 top-N, 平局
                # 按 chunk 序（键序）保确定性
                ranked = sorted(sel.items(), key=lambda kv: (-kv[1], kv[0]))
                sel = dict(ranked[: args.max_blocks])
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
                # E124 落盘字段（2026-09-10）：干净窗预算后切点，0/1 列表、
                # 长度 = 该窗 trimmed 字节数 T；训练侧 cuts_override 消费源。
                "hard_cut": [int(x) for x in rec["hard_cut"][0].tolist()],
                # E124 候选口径落盘（2026-09-11 裁定）：模式 + 抽样种子（与数据流
                # 种子分离）+ 该窗实测候选清单（遮蔽集⊆候选集可审计）。
                "cand_mode": args.candidate_mode,
                "cand_seed": (args.candidate_seed
                              if args.candidate_mode == "random" else None),
                "candidates": rec["cands"],
                "hw": hw,
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
