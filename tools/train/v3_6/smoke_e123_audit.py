"""E123 冒烟四条款之 ①②③ 审计（任务书冻结 v1.3 §7；在 500 步冒烟 ckpt 上执行）：

① 遮蔽接通：遮蔽字节值改动后，未遮位的 _encode 输出逐位不变（被遮键注意力
   权重恰为零的模型级证据；单元级语义已由 tests/test_e123_gates.py 钉死，
   本条款审的是真实模型的接线贯通）。
② 梯度路径：同窗同遮蔽、λ=1 vs λ=0 双 backward——decoder_in_mem（部署查询
   投影）与编码侧参数的梯度差须非零（第七性质：稠密监督经读出件回传源行）。
   审计在 λ>0 形态执行（λ=0 起步期必然零差——冒烟条款②注记）。
③ 逐键 diff：冒烟 ckpt 与参照基座（a-w1）的 model 键集逐键一致（E123 纯接线
   零新参数；嵌套 ckpt['model'] 键层）。

用法：
  python tools/train/v3_6/smoke_e123_audit.py --ckpt <冒烟run目录> \
      --ref-ckpt checkpoints/v37ks_a_d1_w1_10k_ctx4096_20260904 \
      --mask-log outputs/e123_mask_log_seed42.jsonl --data-path <语料>
"""
from __future__ import annotations

import argparse
import json
import sys
from argparse import Namespace
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # repo root
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # tools/

from flued.data import PAD_ID, StreamingReconstructionDataset  # noqa: E402
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402
from tools.train.v3_6.train_v36 import build_model  # noqa: E402


def _load(ckpt: Path, device):
    cfg = json.loads((ckpt / "resolved_config.json").read_text(encoding="utf-8"))
    cfg["data_manifest"] = ""
    if device.type != "cuda":
        cfg["kda_impl"] = "torch"
    ns = Namespace(**cfg)
    model = build_model(ns).to(device)
    payload = torch.load(ckpt / "latest.pt", map_location=device, weights_only=False)
    model.load_state_dict(payload["model"], strict=True)
    return model, ns, payload


def _window(data_path: str, seq_len: int, seed: int, wi: int, device) -> torch.Tensor:
    ds = StreamingReconstructionDataset(file_path=data_path, seq_len=seq_len,
                                        samples_per_worker=50000, seed=seed)
    loader = torch.utils.data.DataLoader(ds, batch_size=1, shuffle=False, num_workers=0)
    for i, batch in enumerate(loader):
        if i == wi:
            ids = batch[0][0]
            return ids[: int(ids.ne(PAD_ID).sum())].unsqueeze(0).to(device)
    raise ValueError(f"窗 {wi} 超数据流长")


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    p = argparse.ArgumentParser()
    p.add_argument("--ckpt", required=True)
    p.add_argument("--ref-ckpt", required=True)
    p.add_argument("--mask-log", required=True)
    p.add_argument("--data-path", required=True)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    args = p.parse_args()
    device = torch.device(
        "cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu"
    )
    model, ns, payload = _load(Path(args.ckpt), device)
    model.train()  # 条款②要梯度图；dropout=0（E1 纪律），形态无差

    # --- 条款③：逐键 diff（先做，最便宜） ---
    ref = torch.load(Path(args.ref_ckpt) / "latest.pt", map_location="cpu", weights_only=False)
    k_new, k_ref = set(payload["model"]), set(ref["model"])
    only_new, only_ref = sorted(k_new - k_ref), sorted(k_ref - k_new)
    c3 = {"pass": not only_new and not only_ref, "only_smoke": only_new[:10], "only_ref": only_ref[:10],
          "n_smoke": len(k_new), "n_ref": len(k_ref)}
    print(f"[条款③ 逐键diff] pass={c3['pass']} n={len(k_new)} vs {len(k_ref)} "
          f"only_smoke={only_new[:5]} only_ref={only_ref[:5]}", flush=True)

    # --- 选审计窗：决策日志中第一个有 distance<=1 依赖对的窗（冒烟 K_max=1 档形态） ---
    entry = None
    wi = -1
    for line in open(args.mask_log, encoding="utf-8"):
        rec = json.loads(line)
        if [p for p in rec.get("dependency_pairs", []) if int(p["distance"]) <= 1]:
            entry, wi = rec, int(rec["window_id"])
            break
    if entry is None:
        raise SystemExit("决策日志无 distance<=1 依赖对——审计窗缺席，响亮拒绝")
    pairs = [p for p in entry["dependency_pairs"] if int(p["distance"]) <= 1]
    clean = _window(args.data_path, int(ns.seq_len), int(ns.seed), wi, device)
    T = int(clean.size(1))
    mask = torch.zeros(1, 1, 1, T, dtype=torch.bool, device=device)
    for pr in pairs:
        s, e = (int(x) for x in pr["src_byte_range"])
        mask[0, 0, 0, s:min(e, T)] = True
    print(f"[审计窗] window_id={wi} pairs={len(pairs)} masked_bytes={int(mask.sum())}", flush=True)

    # --- 条款①：遮蔽接通（遮位字节值扰动 → 未遮位 byte_states 逐位不变） ---
    model.eval()
    with torch.no_grad():
        bs1 = model._encode(clean, attn_block_mask=mask)[0]
        clean2 = clean.clone()
        mflat = mask[0, 0, 0]
        clean2[0, mflat] = (clean2[0, mflat] + 7) % 256  # 遮位值扰动（保持非 PAD）
        clean2[0, mflat] = clean2[0, mflat].clamp(min=1)
        bs2 = model._encode(clean2, attn_block_mask=mask)[0]
        diff = (bs1 - bs2).abs().amax(dim=-1)[0]  # (T,)
        unmasked = ~mflat
        max_unmasked = float(diff[unmasked].max()) if bool(unmasked.any()) else 0.0
        n_changed = int((diff[unmasked] > 0).sum())
    c1_pass = max_unmasked == 0.0
    print(f"[条款① 遮蔽接通] pass={c1_pass} 未遮位最大|Δ|={max_unmasked} 变动位数={n_changed} "
          f"(遮位自身变=预期, 未遮位必须恰零)", flush=True)

    # --- 条款②：梯度路径（λ=1 vs λ=0 双 backward，同窗同遮蔽） ---
    model.train()
    dep_pos = sorted({int(x) for pr in pairs for x in pr["positions"] if int(x) < T})
    metas = [[{"src_range": [int(x) for x in pr["src_byte_range"]],
               "positions": [int(x) for x in pr["positions"]],
               "lam": 1.0, "donor_row": None} for pr in pairs]]
    tgt = clean[0].clamp(min=0, max=257)

    def _dep_loss(lam_scale: float) -> torch.Tensor:
        model.zero_grad(set_to_none=True)
        ms = [[{**m, "lam": m["lam"] * lam_scale} for m in metas[0]]]
        out = s1.s1_forward(model, clean, ns, attn_block_mask=mask, e123_inject=ms, train=True)
        out0 = out["chunks"]
        logits = out["logits_direct"][0].float()
        c = torch.tensor([int(out0.chunk_ids[0, t]) for t in dep_pos], dtype=torch.long, device=device)
        s = torch.tensor([int(out0.offsets[0, t]) for t in dep_pos], dtype=torch.long, device=device)
        picked = logits[c, s]
        return torch.nn.functional.cross_entropy(picked, tgt[dep_pos])

    # 探针三点：部署查询投影（dec_in）+ 编码侧最深处（byte_lookup）+ 状态行
    # 生产者（summarizer）——注入梯度须贯通整条「读出件←状态行←编码链」
    probe_params = [("decoder_in_mem", model.decoder_in_mem),
                    ("byte_lookup", model.byte_lookup),
                    ("summarizer", model.summarizer)]
    loss1 = _dep_loss(1.0)
    loss1.backward()
    g1 = {n: [p.grad.detach().clone() for p in m.parameters() if p.grad is not None]
          for n, m in probe_params if m is not None}
    loss0 = _dep_loss(0.0)
    loss0.backward()
    g0 = {n: [p.grad.detach().clone() for p in m.parameters() if p.grad is not None]
          for n, m in probe_params if m is not None}
    c2 = {}
    for n in g1:
        dmax = max(float((a - b).abs().max()) for a, b in zip(g1[n], g0[n])) if g1[n] else 0.0
        c2[n] = dmax
    c2_pass = all(v > 0 for v in c2.values()) and len(c2) == len([m for _, m in probe_params if m is not None])
    print(f"[条款② 梯度路径] pass={c2_pass} λ1-vs-λ0 梯度最大差={c2} "
          f"(deploy 投影与编码侧均须 >0; loss1={float(loss1.detach()):.4f} loss0={float(loss0.detach()):.4f})", flush=True)

    verdict = {"clause1_mask": c1_pass, "clause2_grad": c2_pass, "clause3_keydiff": c3["pass"],
               "all_pass": c1_pass and c2_pass and c3["pass"]}
    print("[E123 冒烟审计] " + json.dumps(verdict, ensure_ascii=False), flush=True)
    sys.exit(0 if verdict["all_pass"] else 1)


if __name__ == "__main__":
    main()
