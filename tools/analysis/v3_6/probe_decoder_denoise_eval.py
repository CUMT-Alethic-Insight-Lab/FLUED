"""decoder 去噪臂四列收官探针（任务书 2026-08-29 冻结 v1.1 + 修订 v2:
docs/versions/v3.7/FLUED_V3_7_DECODER_DENOISE_20260829_CN.md §2 判读表的评测仪器——
点火后发现收官仪器缺口补建, 零训练纯评测, 任一里程碑 ckpt 可喂）。

考场（§2 冻结）: eval 窗 seed+9999 前 N 窗（E60–E68 同口径, 经
probe_oracle_write_verdict.build_eval_windows/build_masks 复演 evaluate() 的
窗口+掩码纪律, eval_mask_seed=1042）, fine 细格 echo byte_acc（as-encoded 主
口径: make_targets(source, zeros) + slot_mask, 与 fuzz_id 探针端口锚及训练器
eval_direct_acc 同函数链）。

四列同测（每窗全部实 chunk 行整列替换后过 direct 腿 decode_rows_donor 打分;
与训练态的行子集混合不同——测量列是全行替换, 申报为口径注记 M1）:
  clean       干净行: 真 memory 行原样（水位锚, 基座应 ≈0.7917, E68 口径）;
  noise_s*    统计匹配噪声行: ṽ = ρ·m + s·(z@Lᵀ), s∈{0.5,1.0,2.0} 三档各报
              （修订 v2 档语义; L/ρ 来自 fuzz_id 的 λopt=1.0 部署桥采样件;
              同窗三档共享同一 z 抽签——列间只差标量倍率, 剂量-响应干净）;
  mhat        m̂ 岭估计行: K 态段1 解混 + λopt 部署桥整行替换
              (mhat_from_window, 训练器列②同函数, 零域移）;
  scrambled   置乱行: 实行在窗内随机置换（边缘分布保留、行↔chunk 绑定摧毁）,
              地板门 ≤0.10（先验 0.071 同档; 漏 = decoder 学会无视条件行, 读数作废）。

Q20 五列形态（E119, 任务书冻结 v1 §2/§3.6——ckpt 的 resolved_config 带
multislot_readout=True 即自动切换, 旗标关 = 四列旧行为逐位不变）:
  q20_k       多槽读出行（本臂产出）过练钝端口端到端——主判据列, 唯一硬通货
              (行生产与训练器 _multislot_readout_rows 同链, 零域移);
  q20_e68     同读出行过 E118 前未练钝端口 (E68 基座 ckpt, --q20-e68-ckpt;
              eval-only)——辅助归因列, 端口练钝贡献分账, 非硬通货;
  mhat        降级为闭式参照列 (同函数不动, E118 收官值 0.4572 同场复测)。
  自检门修订: clean ∈ 0.8323±2pp (换 E118 锚) 且 scrambled ≤0.10。

监护列（§2 唯一硬指标随测, 工具臂不承诺张开）: 逐条目 Δ = burst_tail 源段
完好−置乱, 复用 probe_burst_route_q15 的 run_arm/_splice_burst/_delta_aggregate
原函数（intact/src_scrambled 两臂, 压缩区剔除同开, SPLICE_SEED 同源）——
判词「去噪不得进一步压 Δ」只与同窗基线比相对移动。

落盘: items.jsonl（kind=column_window 逐窗四列读数 + kind=delta_item 监护逐条目）
+ summary.json + SUMMARY.txt。

自检门（--self-check, 仅基座 t=0 用）: clean ∉ [0.7917±0.02] 或
scrambled > 0.10 → 探针本身有 bug, 非零退出, 不许交付。

Usage:
  python tools/analysis/v3_6/probe_decoder_denoise_eval.py --ckpt <run_dir 或里程碑.pt> --device cuda
  基座自检: ... --ckpt checkpoints/v37ks_b_sm_v371_20k_ctx4096_20260817 --self-check
  CPU 冒烟: py -3.14 -X utf8 tools/analysis/v3_6/probe_decoder_denoise_eval.py --device cpu --ckpt <run_dir> --max-windows 2 --delta-items 2
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
    _front_end,
    build_eval_windows,
    build_masks,
)
from tools.analysis.v3_6.probe_closed_form_readout import decode_rows_donor, grid_metrics  # noqa: E402
from tools.analysis.v3_6.probe_decoder_fuzz_id import mhat_from_window  # noqa: E402
import tools.analysis.v3_6.probe_burst_route_q15 as q15p  # noqa: E402

DEFAULT_FUZZ = "outputs/decoder_denoise_fuzz_id_20260829"
DEFAULT_OUT = "outputs/decoder_denoise_eval_20260829"
S_LADDER = (0.5, 1.0, 2.0)  # 修订 v2 冻结档 (轻/中/重)
NOISE_SEED = 20260829  # 独立抽签流 (与训练器 101087 偏移、q15 SPLICE_SEED 不混)
SCRAMBLE_SEED = 20260830
CLEAN_REF, CLEAN_TOL = 0.7917, 0.02  # E68 收官水位 ±2pp (自检门)
CLEAN_REF_Q20 = 0.8323  # E118 收官水位 (Q20 五列形态自检门锚, 任务书 §3.6 修订)
Q20_E68_CKPT = "checkpoints/v37ks_b_sm_v371_20k_ctx4096_20260817"  # q20×E68 归因列的未练钝端口 donor (E68 b 格)
FLOOR_GATE = 0.10  # 置乱地板门 (先验 0.071 同档, §2 冻结)

DECLARED_NOTES = [
    "M1: 测量列 = 每窗全部实 chunk 行整列替换; 训练态是 batch 级触发 + 行子集混合 (p=0.5/0.25, row_frac=0.5), 两者不混。",
    "M2: 噪声三档同窗共享同一 z 抽签 (列间只差标量倍率 s); z 从 CPU generator 抽后 .to(device), 设备无关确定。",
    "M3: m̂ 列桥 = fuzz_id 落盘的 λopt=1.0 部署桥 (训练窗拟合); eval 窗 m̂ 由该桥产出 (Q19 §1 段2 纪律: 评测窗 held-out)。",
    "M4: 监护列 Δ 复用 probe_burst_route_q15 原函数 (两臂 intact/src_scrambled, 剔除同开); 本探针只报相对移动, 不落 Δ 判词。",
]


# ---------------------------------------------------------------------------
# 列构造（纯函数, 单测直打）
# ---------------------------------------------------------------------------


def noise_rows(m: torch.Tensor, chol: torch.Tensor, rho: float, s: float, gen: torch.Generator) -> torch.Tensor:
    """统计匹配噪声行 (修订 v2 合成式): ṽ = ρ·m + s·(z@Lᵀ), z~N(0,I) CPU 抽。"""
    z = torch.randn(m.shape, generator=gen)
    return rho * m + s * (z @ chol.float().T)


def scramble_rows(m: torch.Tensor, gen: torch.Generator) -> tuple[torch.Tensor, torch.Tensor]:
    """置乱行: 实行窗内随机置换 (边缘分布保留, 行↔chunk 绑定摧毁)。
    Returns (置乱后行, perm)。"""
    perm = torch.randperm(m.size(0), generator=gen)
    return m[perm], perm


def column_rows(model, m: torch.Tensor, index: torch.Tensor, chunk_mask: torch.Tensor, fuzz: dict,
                gen_noise: torch.Generator, gen_scr: torch.Generator, s_ladder=S_LADDER) -> dict[str, torch.Tensor]:
    """四列行变体 (输入 m = (n_real, d_mem) 真实 memory 行, fp32 任意设备;
    噪声/置乱抽签在 CPU 故设备无关)。Returns {列名: (n_real, d_mem) 与 m 同设备}。
    Q20 五列形态 (E119): 模型带 multislot_readout 件 (臂 ckpt) 时 clean 之后
    追加 q20_k 列——多槽读出行 (与训练器 _multislot_readout_rows 同链); 模型
    无该件 = 四列旧行为逐位不变。"""
    device = m.device
    z = torch.randn(m.shape, generator=gen_noise)  # 同窗三档共享 z (M2)
    L = fuzz["chol"].float().cpu()
    cols = {"clean": m}
    if hasattr(model, "multislot_readout"):
        n_real = int(chunk_mask[0].sum())
        cols["q20_k"] = s1._multislot_readout_rows(model, index, chunk_mask)[0, :n_real]
    for s in s_ladder:
        cols[f"noise_s{s:g}"] = (fuzz["rho"] * m.cpu() + s * (z @ L.T)).to(device)
    scr, _perm = scramble_rows(m.cpu(), gen_scr)
    cols["scrambled"] = scr.to(device)
    cols["mhat"] = mhat_from_window(model, index.float(), chunk_mask, fuzz["W"], fuzz["scale"])[0].to(device)
    return cols


def self_check_failures(clean_acc: float, scrambled_acc: float, clean_ref: float = CLEAN_REF) -> list[str]:
    """基座 t=0 自检门 (任务书 §2 + 交接验收): clean 贴水位锚 ±2pp (旧行为 =
    E68 锚 0.7917; Q20 五列形态换 E118 锚 0.8323, 任务书 §3.6 修订),
    scrambled 贴地板 ≤0.10。Returns 失败原因列表 (空 = 过)。"""
    fails = []
    if not (clean_ref - CLEAN_TOL <= clean_acc <= clean_ref + CLEAN_TOL):
        fails.append(f"clean={clean_acc:.4f} 不在 [{clean_ref - CLEAN_TOL:.4f}, {clean_ref + CLEAN_TOL:.4f}] (水位锚 {clean_ref}±2pp)")
    if scrambled_acc > FLOOR_GATE:
        fails.append(f"scrambled={scrambled_acc:.4f} 漏地板门 (> {FLOOR_GATE}; 先验 0.071 同档)")
    return fails


# ---------------------------------------------------------------------------
# ckpt 装载 (run dir 或里程碑 .pt 皆可) + 逐窗四列打分
# ---------------------------------------------------------------------------


def load_ckpt(ckpt: str, device: torch.device):
    """--ckpt 接受 run dir (吃 latest.pt) 或具体里程碑 .pt (配置吃同目录
    resolved_config.json)。装载纪律与 probe_oracle_write_verdict.load_model
    同款 (slm/kda 接口断言 + hard-freeze + eval)。"""
    from argparse import Namespace

    from tools.train.v3_6.train_v36 import build_model

    p = Path(ckpt)
    run_dir, pt = (p, p / "latest.pt") if p.is_dir() else (p.parent, p)
    if not pt.exists():
        raise SystemExit(f"--ckpt {ckpt}: {pt} 缺席")
    cfg = json.loads((run_dir / "resolved_config.json").read_text(encoding="utf-8"))
    cfg["data_manifest"] = ""
    if device.type != "cuda":
        cfg["kda_impl"] = "torch"  # fla kernels are GPU-only
    ns = Namespace(**cfg)
    if getattr(ns, "backbone_mode", "") != "slm":
        raise ValueError(f"{run_dir.name}: backbone_mode={ns.backbone_mode!r} != 'slm'")
    if getattr(ns, "recurrence", "kda") != "kda":
        raise ValueError(f"{run_dir.name}: recurrence={ns.recurrence!r} != 'kda'")
    if s1._BPE_TOKENIZER is None and getattr(ns, "mask_mode", "mixed") == "mixed" and ns.mask_prob > 0:
        s1._load_bpe_tokenizer(ns.bpe_tokenizer_path)
    model = build_model(ns).to(device)
    payload = torch.load(pt, map_location=device, weights_only=False)
    model.load_state_dict(payload["model"], strict=True)
    for param in model.parameters():  # hard-freeze: no autograd graph anywhere
        param.requires_grad_(False)
    model.eval()
    return model, ns, int(payload.get("step", 0)), run_dir.name, pt.name


@torch.no_grad()
def eval_window_columns(model, ns, clean: torch.Tensor, byte_mask: torch.Tensor, device, fuzz: dict,
                        gen_noise: torch.Generator, gen_scr: torch.Generator, s_ladder=S_LADDER,
                        donor=None, collect_bytes: bool = False) -> dict:
    """单窗四列: 前端 → 真 memory 行 → 列变体 → direct 腿 (decode_rows_donor)
    → fine 细格 echo byte_acc (as-encoded 主口径 + clean 视图备查)。batch=1。
    Q20 五列形态 (donor 在岗时): q20_k 行再过 donor (E68 未练钝端口) 的
    decode 链得 q20_e68 归因列 (eval-only, 非硬通货)——前端位级同源 (写入侧/
    前端全冻), token_mask 取本窗 chunks (decode_rows_donor D1 借口同款)。
    collect_bytes=True (审计落盘字段, 默认关=行为逐位不变): rec["_bytes"]
    附逐列 argmax 预测/as-encoded 目标/真字节目标/槽掩码/掩码位 —— 聚合数
    与 grid_metrics 同源同一次前向。"""
    source = clean.masked_fill(byte_mask, MASK_ID)
    chunks, memory, index = _front_end(model, source)
    n_real = int(chunks.chunk_mask[0].sum())
    m = memory[0, :n_real].float()
    cols = column_rows(model, m, index, chunks.chunk_mask, fuzz, gen_noise, gen_scr, s_ladder)
    zeros = torch.zeros_like(byte_mask)
    targets_enc, slot_mask, _m = s1.make_targets(
        source, zeros, chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
    )
    if collect_bytes:
        targets_true, _sm_t, masked_true = s1.make_targets(
            clean, byte_mask, chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
        )
    rec = {"n_real": n_real}
    byte_recs: dict = {}
    for name, rows in cols.items():
        logits = decode_rows_donor(model, rows.unsqueeze(0).float(), chunks.token_mask)
        gm = grid_metrics(
            logits, targets_enc.to(device), slot_mask.to(device),
            targets_enc.to(device), torch.zeros_like(slot_mask).to(device),
        )
        rec[name] = {"acc": round(gm["acc"], 4), "acc_clean": round(gm["acc_clean"], 4), "n_slots": gm["n_slots"]}
        if collect_bytes:
            n = logits.size(1)
            byte_recs[name] = {
                "preds": logits.argmax(dim=-1)[:, :n].to(torch.int16).cpu(),
                "targets_enc": targets_enc[:, :n].to(torch.int16).cpu(),
                "targets_true": targets_true[:, :n].to(torch.int16).cpu(),
                "slot_mask": slot_mask[:, :n].to(torch.uint8).cpu(),
                "masked_true": masked_true[:, :n].to(torch.uint8).cpu(),
                "n": n,
            }
        if name == "q20_k" and donor is not None:
            logits_e68 = decode_rows_donor(donor, rows.unsqueeze(0).float(), chunks.token_mask)
            gm_e68 = grid_metrics(
                logits_e68, targets_enc.to(device), slot_mask.to(device),
                targets_enc.to(device), torch.zeros_like(slot_mask).to(device),
            )
            rec["q20_e68"] = {
                "acc": round(gm_e68["acc"], 4), "acc_clean": round(gm_e68["acc_clean"], 4), "n_slots": gm_e68["n_slots"]
            }
            if collect_bytes:
                n = logits_e68.size(1)
                byte_recs["q20_e68"] = {
                    "preds": logits_e68.argmax(dim=-1)[:, :n].to(torch.int16).cpu(),
                    "targets_enc": targets_enc[:, :n].to(torch.int16).cpu(),
                    "targets_true": targets_true[:, :n].to(torch.int16).cpu(),
                    "slot_mask": slot_mask[:, :n].to(torch.uint8).cpu(),
                    "masked_true": masked_true[:, :n].to(torch.uint8).cpu(),
                    "n": n,
                }
    if collect_bytes:
        rec["_bytes"] = byte_recs
    return rec


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    p = argparse.ArgumentParser()
    p.add_argument("--ckpt", required=True, help="run dir (吃 latest.pt) 或里程碑 .pt 路径")
    p.add_argument("--fuzz-id", default=DEFAULT_FUZZ, help="前置测量产物目录 (λopt 部署桥 + 残差 Cholesky + ρ)")
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--max-windows", type=int, default=16, help="eval 窗数 (E60–E68 口径 = 16)")
    p.add_argument("--delta-items", type=int, default=48, help="监护列 Δ 条目数 (probe_burst_route_q15 同默认)")
    p.add_argument("--s-ladder", default=",".join(f"{s:g}" for s in S_LADDER), help="噪声档 CSV (修订 v2 冻结 0.5,1,2)")
    p.add_argument("--out-dir", default=DEFAULT_OUT)
    p.add_argument("--self-check", action="store_true",
                   help="基座 t=0 自检门: clean 贴水位锚 ±2pp (E68 0.7917; Q20 形态换 E118 0.8323) 且 scrambled ≤0.10, 不过非零退出")
    p.add_argument("--q20-e68-ckpt", default=Q20_E68_CKPT,
                   help="Q20 五列形态的 q20×E68 归因列 donor (E68 未练钝端口基座; 仅 q20 模式装载)")
    p.add_argument("--data-path", default=None,
                   help="覆盖 resolved_config 的语料路径（远端基座回本地重跑用, E122 探针同款; 窗口流=同语料同 seed 逐位复演）")
    p.add_argument("--dump-bytes", action="store_true",
                   help="审计落盘字段: 逐窗逐列 argmax 预测/目标/掩码 → items_bytes.npz"
                        "（与 grid_metrics 同源同一次前向, 口径零改动）")
    args = p.parse_args()
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    s_ladder = [float(x) for x in args.s_ladder.split(",")]

    model, ns, step, run_name, pt_name = load_ckpt(args.ckpt, device)
    if args.data_path:
        ns.data_path = args.data_path  # 远端基座回本地重跑: 窗口流语料路径覆盖（同语料同 seed = 同窗）
    if getattr(ns, "v_row_source", "") != "memory" or not hasattr(model, "decoder_in_mem"):
        raise SystemExit(f"{run_name}: 预期 b 格 v_row_source='memory' + decoder_in_mem 在岗 (去噪臂作用端口缺席)")
    # Q20 五列形态 (E119 任务书冻结 v1 §2/§3.6): ckpt 的 resolved_config 带
    # multislot_readout=True → q20_k 主判据列 + q20×E68 归因列; 否则四列旧
    # 行为逐位不变
    q20_mode = bool(getattr(ns, "multislot_readout", False))
    donor = None
    donor_name = ""
    if q20_mode:
        if not hasattr(model, "multislot_readout"):
            raise SystemExit(f"{run_name}: resolved_config 开 multislot_readout 但模型缺件 —— 装载事故, 响亮退出")
        donor, _dns, _dstep, donor_name, _dpt = load_ckpt(args.q20_e68_ckpt, device)
    fuzz = s1._load_decoder_denoise_fuzz(args.fuzz_id)  # λopt=1.0 部署桥单采样器 (修订 v2)
    print(
        f"[denoise-eval] ckpt={run_name}/{pt_name} step={step} device={device.type} "
        f"fuzz={args.fuzz_id} (tag={fuzz['tag']}, lam={fuzz['lam']}, ρ={fuzz['rho']:.4f}) s_ladder={s_ladder}"
        + (f" | Q20 五列形态: k={getattr(ns, 'multislot_readout_k', '?')} donor={donor_name}" if q20_mode else ""),
        flush=True,
    )

    # --- 四列同测: eval 窗 + eval 掩码 (E60–E68 口径复演) ---
    windows = build_eval_windows(ns, args.max_windows)
    masks = build_masks(windows, ns)
    gen_noise = torch.Generator().manual_seed(NOISE_SEED)
    gen_scr = torch.Generator().manual_seed(SCRAMBLE_SEED)
    col_names = ["clean"] + (["q20_k", "q20_e68"] if q20_mode else []) + [f"noise_s{s:g}" for s in s_ladder] + ["mhat", "scrambled"]
    items_path = out_dir / "items.jsonl"
    items_fp = items_path.open("w", encoding="utf-8")
    win_recs = []
    byte_buf: dict[str, list] = {c: [] for c in col_names} if args.dump_bytes else {}
    for wi, (clean, byte_mask) in enumerate(zip(windows, masks)):
        rec = eval_window_columns(
            model, ns, clean.to(device), byte_mask.to(device), device, fuzz, gen_noise, gen_scr, s_ladder,
            donor=donor, collect_bytes=args.dump_bytes,
        )
        bytes_rec = rec.pop("_bytes", None)
        rec = {"kind": "column_window", "window": wi, **rec}
        win_recs.append(rec)
        if bytes_rec is not None:
            for c, b in bytes_rec.items():
                byte_buf[c].append(b)
        items_fp.write(json.dumps(rec, ensure_ascii=False) + "\n")
        items_fp.flush()
        print(
            f"[denoise-eval] window {wi} n_real={rec['n_real']} "
            + " ".join(f"{c}={rec[c]['acc']:.4f}" for c in col_names)
            + f"（{time.time() - t0:.0f}s）",
            flush=True,
        )
    if args.dump_bytes:
        import numpy as np

        arrays: dict = {}
        for c, rows in byte_buf.items():
            arrays[f"{c}_preds"] = torch.cat([b["preds"] for b in rows], dim=1).numpy()
            arrays[f"{c}_targets_enc"] = torch.cat([b["targets_enc"] for b in rows], dim=1).numpy()
            arrays[f"{c}_targets_true"] = torch.cat([b["targets_true"] for b in rows], dim=1).numpy()
            arrays[f"{c}_slot_mask"] = torch.cat([b["slot_mask"] for b in rows], dim=1).numpy()
            arrays[f"{c}_masked_true"] = torch.cat([b["masked_true"] for b in rows], dim=1).numpy()
            arrays[f"{c}_row_counts"] = np.asarray([int(b["n"]) for b in rows], dtype=np.int64)
        np.savez_compressed(out_dir / "items_bytes.npz", **arrays)
        print(f"[denoise-eval] per-byte records -> {out_dir / 'items_bytes.npz'}", flush=True)
    col_acc = {c: round(sum(r[c]["acc"] for r in win_recs) / len(win_recs), 4) for c in col_names}
    col_acc_clean = {c: round(sum(r[c]["acc_clean"] for r in win_recs) / len(win_recs), 4) for c in col_names}

    # --- 监护列: 逐条目 Δ (burst_tail 源段完好−置乱, probe_burst_route_q15 原函数口径) ---
    if s1._BPE_TOKENIZER is None:
        s1._load_bpe_tokenizer(ns.bpe_tokenizer_path)
    sampler = s1.CorpusSampler(ns.data_path)
    kstate_ok = getattr(model.config, "k_row_source", "memory") == "state"
    vstate_ok = getattr(model.config, "v_row_source", "memory") == "state"
    gen_splice = torch.Generator().manual_seed(q15p.SPLICE_SEED)
    d_items = []
    d_windows = build_eval_windows(ns, args.delta_items * 2)  # oversample: inactive rows skipped
    for wi, clean in enumerate(d_windows):
        if len(d_items) >= args.delta_items:
            break
        spliced, metas = s1._splice_burst(
            clean, 1.0, gen_splice, sampler, s1._BURST_REPEAT_FROZEN, s1._BURST_TAIL_MAX_CHARS
        )
        meta = metas[0]
        if meta is None:
            continue
        ids = spliced[0]
        raw = bytes(int(x) - 1 for x in ids.tolist() if int(x) != PAD_ID)  # 剥 PAD 尾 (q15 探针同款)
        rec = {
            "kind": "delta_item",
            "window": wi,
            "answer": meta["answer_b"].decode("utf-8", errors="replace"),
            "swap_identity": q15p._swap_identity(raw, meta),
        }
        skip = False
        for arm in ("intact", "src_scrambled"):
            r = q15p.run_arm(model, ids, meta, arm, device, 1042 + wi, ns, kstate_ok, vstate_ok, excise=True)
            if r is None:
                skip = True  # echo off-grid: 条目不激活
                break
            rec[arm] = r
        if skip:
            continue
        rec["delta"] = round(rec["intact"]["byte_acc"] - rec["src_scrambled"]["byte_acc"], 4)
        d_items.append(rec)
        items_fp.write(json.dumps(rec, ensure_ascii=False) + "\n")
        items_fp.flush()
        if len(d_items) % 8 == 0:
            print(f"[denoise-eval] delta items {len(d_items)}/{args.delta_items}（{time.time() - t0:.0f}s）", flush=True)
    items_fp.close()
    delta = q15p._delta_aggregate(d_items)

    # --- 聚合 + 自检门 + 落盘 ---
    clean_ref = CLEAN_REF_Q20 if q20_mode else CLEAN_REF  # 自检门修订 (任务书 §3.6): Q20 形态换 E118 锚
    fails = self_check_failures(col_acc["clean"], col_acc["scrambled"], clean_ref=clean_ref) if args.self_check else []
    floor_ok = col_acc["scrambled"] <= FLOOR_GATE
    col_defs = {"clean": "干净行 (水位锚)", "noise_s*": "统计匹配噪声 ṽ=ρ·m+s·(z@Lᵀ)",
                "mhat": "m̂ 岭估计行 (λopt 部署桥整行替换)", "scrambled": "置乱行 (地板门 ≤0.10)"}
    if q20_mode:
        col_defs["q20_k"] = "多槽读出行 (本臂产出) 过练钝端口端到端 —— 主判据列, 唯一硬通货"
        col_defs["q20_e68"] = f"同读出行过 E68 未练钝端口 ({donor_name}, eval-only) —— 辅助归因列, 非硬通货"
    report = {
        "probe": "decoder 去噪臂四列收官探针 (任务书 §2 判读表评测仪器, 修订 v2 s 档)",
        "spec": "docs/versions/v3.7/FLUED_V3_7_DECODER_DENOISE_20260829_CN.md",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "checkpoint": {"run": run_name, "file": pt_name, "step": step},
        "fuzz_id": {"dir": args.fuzz_id, "tag": fuzz["tag"], "lam": fuzz["lam"], "rho": fuzz["rho"]},
        "params": {"windows": len(win_recs), "s_ladder": s_ladder, "noise_seed": NOISE_SEED,
                   "scramble_seed": SCRAMBLE_SEED, "delta_items": len(d_items),
                   "delta_splice_seed": q15p.SPLICE_SEED, "eval_mask_seed": ns.eval_mask_seed},
        "declared_notes": DECLARED_NOTES,
        "columns": {
            "byte_acc": col_acc,  # as-encoded 主口径 (E60–E68 fine 细格 echo)
            "byte_acc_clean_view": col_acc_clean,
            "defs": col_defs,
        },
        "floor_gate": {"scrambled": col_acc["scrambled"], "gate": FLOOR_GATE, "pass": floor_ok},
        "delta_monitor": delta,  # 监护列: 逐条目 Δ 聚合 (q15 口径; 只报相对移动)
        "self_check": {"requested": bool(args.self_check), "clean_ref": clean_ref, "failures": fails, "pass": not fails},
        "items_path": str(items_path),
        "timing_sec": round(time.time() - t0, 1),
    }
    if q20_mode:
        # Q20 形态注记 (E119): 新口径边界 (任务书 §3.5)——本 ckpt 的列读数不与
        # E60–E118 的 b 格锚混排, 对比读数须标注「多槽读出口径」
        report["q20"] = {
            "mode": True, "k": str(getattr(ns, "multislot_readout_k", "?")),
            "e68_donor": donor_name,
            "spec": "docs/versions/v3.7/FLUED_V3_7_Q20_MULTISLOT_READOUT_20260829_CN.md",
            "primary_column": "q20_k",
            "note": "多槽读出口径: 本表读数不与 E60–E118 的 b 格锚混排 (新口径边界, 任务书 §3.5)",
        }
    (out_dir / "summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    def fmt(v):
        return "N/A" if v is None else f"{v:.4f}"

    q20_col_str = (
        f"q20_k {fmt(col_acc['q20_k'])} (主判据) | q20_e68 {fmt(col_acc['q20_e68'])} (归因) | " if q20_mode else ""
    )
    lines = [
        "decoder 去噪臂四列收官探针（任务书 §2 判读表仪器, 修订 v2 s 档, fine 细格 echo byte_acc）"
        + ("—— Q20 五列形态 (E119 多槽读出口径)" if q20_mode else ""),
        f"日期 {report['created']}  设备 {device.type}  ckpt={run_name}/{pt_name} (step {step})  "
        f"eval 窗 {len(win_recs)} (seed+9999, mask_seed={ns.eval_mask_seed})",
        f"fuzz_id={args.fuzz_id} (λopt 部署桥 tag={fuzz['tag']}, ρ={fuzz['rho']:.4f})",
        "",
        f"{'五' if q20_mode else '四'}列 byte_acc (as-encoded 主口径):",
        f"  clean {fmt(col_acc['clean'])} | " + q20_col_str
        + " | ".join(f"noise_s{s:g} {fmt(col_acc[f'noise_s{s:g}'])}" for s in s_ladder)
        + f" | mhat {fmt(col_acc['mhat'])} (闭式参照) | scrambled {fmt(col_acc['scrambled'])}",
        f"地板门: scrambled {fmt(col_acc['scrambled'])} ≤ {FLOOR_GATE} → {'过' if floor_ok else '漏 (读数作废, 不发判词)'}",
        "",
        f"监护列 Δ (burst_tail 完好−置乱, q15 口径): {delta['mean']:.4f} ± {delta['ci95']:.4f} "
        f"(95% CI, n={delta['n']}, swap_identity 剔除 {delta['n_swap_identity_excluded']} 条) — 只报相对移动, 不落 Δ 判词",
        "",
        "已申报口径注记:",
        *[f"  {d}" for d in DECLARED_NOTES],
    ]
    if args.self_check:
        lines += ["", f"自检门 (基座 t=0): {'过' if not fails else '不过 —— 探针本身有 bug, 不许交付:'}"]
        lines += [f"  {f}" for f in fails]
    lines += ["", f"汇总: {out_dir / 'summary.json'}  逐条目: {items_path}"]
    (out_dir / "SUMMARY.txt").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines), flush=True)
    if fails:
        raise SystemExit(f"[denoise-eval] 自检门不过: {fails}")


if __name__ == "__main__":
    main()
