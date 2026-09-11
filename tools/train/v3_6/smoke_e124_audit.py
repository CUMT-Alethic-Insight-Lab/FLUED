"""E124 冒烟六条款之 ①②③ 审计（任务书冻结 v1.0 2026-09-09；在冒烟 ckpt 上执行）:

① 门接通（双半）: (a) 硬模式（rt_hard=True + rt_budget=9）last_block1_attn
   逐真实查询行命中数 == min(k, 因果候选数)、未命中行权重恰 0.0；(b) 退火起点
   恒等——同模型 e124_rt_progress=0（全量预算 → bypass）前向与临时关gate
   （bb.e124_gate=False, legacy 路径）前向逐位一致。
② 梯度路径审计: 软门（rt_hard=False, rt_budget=9 强制激活）单步 backward,
   decoder_in_mem / backbone.q_proj / backbone.align_k / summarizer.index_ffn /
   backbone.e124_alpha_raw 的梯度张量名 + L1 量级落盘——均须非零有限
   （「部署查询←命中分布←index(K) 行」全链贯通证据）。
③ 逐键 diff: E124 冒烟 ckpt 与同架构参照（gate2 基座 = v37 slm a 格 qpool
   同形态）的 model 键集逐键对比——only_smoke 必须恰为
   {backbone.e124_alpha_raw}（门唯一新件）、only_ref 必须为空。

（条款④⑤⑥归属：④ 选择器落盘 schema 由 build_e123_mask_log.py 的 E124 剂量段
冒烟覆盖；⑤ cuts_override 恒等/钉死语义由 tests/test_e124_cuts_override.py
钉死；⑥ entmax 数值/梯度由 tests/test_e124_entmax.py + 官方包对拍
outputs/e124_entmax_parity/parity_report.json 覆盖。）

用法:
  python tools/train/v3_6/smoke_e124_audit.py --ckpt <E124冒烟run目录> \
      --ref-ckpt checkpoints/v37ks_a_gate2base_v373_20k_ctx4096_20260910 \
      --data-path P:\\FLUED_corpus\\corpus_v3\\corpus_v3.txt
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
    p.add_argument("--data-path", required=True)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    args = p.parse_args()
    device = torch.device(
        "cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu"
    )
    model, ns, payload = _load(Path(args.ckpt), device)
    bb = model.backbone
    if not getattr(bb, "e124_gate", False):
        raise SystemExit("冒烟 ckpt 的 backbone 无 e124 门件——该 run 非 E124 gate 列, 响亮拒绝")

    # --- 条款③：逐键 diff（先做，最便宜） ---
    ref = torch.load(Path(args.ref_ckpt) / "latest.pt", map_location="cpu", weights_only=False)
    k_new, k_ref = set(payload["model"]), set(ref["model"])
    only_new, only_ref = sorted(k_new - k_ref), sorted(k_ref - k_new)
    c3_pass = only_new == ["backbone.e124_alpha_raw"] and not only_ref
    print(f"[条款③ 逐键diff] pass={c3_pass} n={len(k_new)} vs {len(k_ref)} "
          f"only_smoke={only_new[:5]} only_ref={only_ref[:5]} "
          f"(期望 only_smoke==['backbone.e124_alpha_raw'])", flush=True)

    clean = _window(args.data_path, int(ns.seq_len), int(ns.seed), 0, device)
    print(f"[审计窗] window_id=0 T={int(clean.size(1))}", flush=True)

    # --- 条款①a：硬模式未命中恰零 + 命中数 = min(k, 候选数) ---
    model.eval()
    K_PROBE = 9
    with torch.no_grad(), torch.autocast(
        "cuda", dtype=torch.bfloat16, enabled=bool(getattr(ns, "amp", False)) and device.type == "cuda"
    ):
        bb.e124_rt_budget = K_PROBE
        bb.e124_rt_hard = True
        out = s1.s1_forward(model, clean, ns, need_attn=True)
        attn = bb.last_block1_attn
        assert attn is not None, "硬门 + need_attn 未寄存 last_block1_attn"
        cm = out["chunks"].chunk_mask[0]  # (C,) 真实块
        n_real = int(cm.sum())
        C = int(cm.size(0))
        hit = bb.last_e124_hit
        assert hit is not None, "硬门 + need_attn 未寄存 last_e124_hit（命中集审计口）"
        # 条款①a 换锚（2026-09-11 冒烟复核）：「非零数 == min(k,候选)」是 softmax
        # 语义的错误期望——α-entmax 的设计行为就是给命中集内低分行精确零（任务书
        # §2「低分行拿精确零」）。条款①的正确可验形式 = ①结构性不可见（非零 ⊆
        # 命中集，非命中恰零）+ ②top-k 构造（命中数恰 = min(k,候选)）; 命中集内
        # 被 α 稀疏化的行数只报不判（副仪表 A 同族机制读数）。
        bad_rows = 0
        sparse_rows = 0
        for i in range(n_real):  # 逐真实查询行（padded 行走对角护栏, 不在此条款）
            nz = attn[0, :, i, :] > 0  # (H, C)
            h = hit[0, :, i, :]  # (H, C) 命中集（per-head top-k, 随头独立）
            expect = min(K_PROBE, i + 1)
            if not bool((nz <= h).all()):  # 非命中恰零（否决项）
                bad_rows += 1
            if not bool((h.sum(dim=-1) == expect).all()):  # top-k 构造（否决项）
                bad_rows += 1
            if bool((nz.sum(dim=-1) < expect).any()):  # α 稀疏化（注记）
                sparse_rows += 1
        c1a_pass = bad_rows == 0
        print(f"[条款①a 硬门恰零] pass={c1a_pass} n_real={n_real} 坏行={bad_rows} "
              f"α稀疏化行(注记不判)={sparse_rows} "
              f"k={K_PROBE} last_e124_k={float(bb.last_e124_k)}", flush=True)

        # --- 条款①b：退火起点恒等（全量预算 bypass == 临时关gate legacy 路径） ---
        bb.e124_rt_budget = None
        bb.e124_rt_progress = 0.0
        bb.e124_rt_hard = True
        out_full = s1.s1_forward(model, clean, ns)
        bb.e124_gate = False  # 临时关件 = 真 legacy 路径（同权重, α 不进图）
        out_legacy = s1.s1_forward(model, clean, ns)
        bb.e124_gate = True  # 恢复
        c1b_pass = torch.equal(out_full["logits_backbone"], out_legacy["logits_backbone"]) \
            and torch.equal(out_full["logits_direct"], out_legacy["logits_direct"])
        print(f"[条款①b 退火起点恒等] pass={c1b_pass} (progress=0 全量预算 == 关gate legacy, 逐位)",
              flush=True)
    c1_pass = c1a_pass and c1b_pass

    # --- 条款②：软门梯度路径（rt_budget=9 强制激活, backward 全链审计） ---
    model.train()
    bb.e124_rt_budget = K_PROBE
    bb.e124_rt_hard = False
    bb.e124_rt_temp = 1.0
    model.zero_grad(set_to_none=True)
    with torch.autocast(
        "cuda", dtype=torch.bfloat16, enabled=bool(getattr(ns, "amp", False)) and device.type == "cuda"
    ):
        out = s1.s1_forward(model, clean, ns, train=True)
        # 双腿并押: logits_backbone 贯通 backbone 门链 (q_proj/align_k/α),
        # logits_direct 经 decoder_in_mem (部署查询投影) —— 只押 backbone 腿
        # 时 decoder_in_mem 无梯度属预期, 条款② 要的是全链贯通证据
        loss = out["logits_backbone"].float().square().mean() \
            + out["logits_direct"].float().square().mean()
    loss.backward()
    probes = {
        "decoder_in_mem.weight": model.decoder_in_mem.weight,
        "backbone.q_proj.weight": bb.q_proj.weight,
        "backbone.align_k.weight": bb.align_k.weight,
        "backbone.e124_alpha_raw": bb.e124_alpha_raw,
        "summarizer.index_ffn.0.weight": model.summarizer.index_ffn[0].weight,
    }
    report = {}
    c2_pass = True
    for name, p_ in probes.items():
        g = p_.grad
        mag = float(g.abs().sum()) if g is not None else None
        finite = bool(torch.isfinite(g).all()) if g is not None else False
        report[name] = {"grad_l1": mag, "finite": finite}
        if mag is None or not finite or mag == 0.0:
            c2_pass = False
    print(f"[条款② 梯度路径] pass={c2_pass} " + json.dumps(report, ensure_ascii=False), flush=True)
    print(f"          (loss={float(loss.detach()):.4f} α={float(bb.e124_alpha_value().detach()):.4f} "
          f"soft_k={float(bb.last_e124_k)})", flush=True)

    verdict = {"clause1_gate": c1_pass, "clause1a_hard_zeros": c1a_pass,
               "clause1b_anneal_start_identity": c1b_pass,
               "clause2_grad": c2_pass, "clause3_keydiff": c3_pass,
               "all_pass": c1_pass and c2_pass and c3_pass}
    print("[E124 冒烟审计] " + json.dumps(verdict, ensure_ascii=False), flush=True)
    sys.exit(0 if verdict["all_pass"] else 1)


if __name__ == "__main__":
    main()
