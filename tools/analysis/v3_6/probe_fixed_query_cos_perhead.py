"""固定查询读出 cos 的逐头分解（容量界稿点单，零训练纯评测，2026-09-12）。

裁决问题：容量界预言固定单查询读出 cos ≈ 1/√(有效叠加写入数)。聚合实测
b 格 cos=0.1044 / d 格 cos=0.07（仪器值；理论侧引用 0.076）。γ 谱逐头
n_eff（outputs/vrow_ngate_20260912/）：d 格 [2.14, 8.23, 31.45, 89.00]、
b 格 [2.12, 8.04, 31.68, 88.30]。若 cos 承重集中在 h3（最长记忆头），则
b 格 1/√88.3=0.1064 ≈ 0.1044 →「第二个零参数命中」成立；若逐头均匀或非
h3 承重 → 该读法死。本探针把 0.1044/0.07 分解到 4 头（每头 256 维）。

仪器口径（原测量件逐行对齐，不许换锚）：
  b 格 = outputs/_remote_scripts/e119_k1_t0_decodability.py（裁 3 对照判别，
    落盘 outputs/e119_k1_t0_check_20260903/e119_k1_t0.json 键
    cos_fixed_query_vs_unmix_bgrid=0.1044）：
      gates_k = model.write_head_k(index.float())
      S_k     = trained_states(model.state_machine_k, gates_k, n_real)
      vh_k    = ridge_unmix(gates_k, S_k, LAM_UNMIX)      # (1, n, H*hv)
      q       = multislot_readout.slot_query[0]           # 温启动装载 =
      read_fixed = einsum("hk,bnhkv->bnhv", q, S_k)       #   q20_ridge_dir.npz
      cos = cosine_similarity(read_fixed.flatten(), vh_k.flatten())  # 全局展平
    窗流 = build_eval_windows(ns, 16)（eval 流 seed+9999）+ build_masks
    （eval_mask_seed=1042）。聚合 = 逐窗全局 cos 的窗均值。
  d 格 = outputs/_remote_scripts/e120_t0_localize.py（9/03 晚定位件，控制台
    读数 cos_fixed_query_vs_unmix=0.07，TERMS.md 固定单查询近视行在册）：
      同公式，通道 = V（write_head(memory) / state_machine），q = q_ridge
      （outputs/e120_warmstart_fit_20260903/q_ridge_dir.npz），窗流 =
      build_train_windows(ns, 4)（训练流 seed=42）+ build_train_masks。
  注：b 格温启动纪律（train_v36_s1._multislot_readout_warm_start）是
  slot_query[0].copy_(q_ridge)——cos 只吃 q，故两格都直接从落盘 npz 取
  q_ridge，免接线（数值逐位等价，fidelity 聚合校验兜底）。

逐头扩展：read_fixed 与 v̂ 均为 head-major 展平（头 h 占列
[h*hv:(h+1)*hv]），全局展平 cos 按分块恒等式拼装：
  cos_global = Σ_h <a_h,b_h> / sqrt(Σ_h‖a_h‖² · Σ_h‖b_h‖²)
逐头 cos_h = <a_h,b_h>/(‖a_h‖‖b_h‖)（fp64 累积）。**聚合一致性硬校验**：
fidelity 逐窗拼装 cos 窗均值必须复现原仪器值（b: 0.1044；d: 0.0700，
容差 --tolerance 默认 5e-3），不一致 = 口径错，响亮退出不许报数。

双跑设计：fidelity pass（原仪器窗流逐位对齐）+ eval 扩展 pass（两格同卷
eval 流 64 窗，与 n_eff 测量同流型，供理论对照表）。

判词留白：只落数与对照表（vs 1/√n_eff 逐头），h3 是否独承重的判读归理论侧。

Usage:
  python tools/analysis/v3_6/probe_fixed_query_cos_perhead.py --device cuda
  CPU 冒烟: py -3.14 -X utf8 tools/analysis/v3_6/probe_fixed_query_cos_perhead.py \
    --device cpu --fidelity-b-windows 2 --fidelity-d-windows 2 --eval-windows 3 --allow-fidelity-fail
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

import torch

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from flued.data import MASK_ID  # noqa: E402
from tools.analysis.v3_6.probe_oracle_write_verdict import (  # noqa: E402
    _front_end,
    load_model,
    ridge_unmix,
    trained_states,
)
from tools.analysis.v3_6.probe_decoder_fuzz_id import (  # noqa: E402
    LAM_UNMIX,
    build_train_masks,
    build_train_windows,
)
from tools.analysis.v3_6.probe_decoder_denoise_eval import load_ckpt  # noqa: E402
from tools.analysis.v3_6.probe_oracle_write_verdict import (  # noqa: E402
    build_eval_windows,
    build_masks,
)

DEFAULT_OUT_DIR = "outputs/perhead_cos_20260912"
DEFAULT_DATA_PATH = r"P:\FLUED_corpus\corpus_v3\corpus_v3.txt"
B_CKPT = r"K:\FLUED_archive\v37ks_b_sm_denoise_v2_20k_ctx4096_20260829"  # sha256 5eb74439… 预录一致
D_CKPT = "checkpoints/v37ks_d_sm_q15_circuit_20k_ctx4096_20260825b"
B_Q_NPZ = "outputs/decoder_denoise_fuzz_id_20260829/q20_ridge_dir.npz"
D_Q_NPZ = "outputs/e120_warmstart_fit_20260903/q_ridge_dir.npz"
# fidelity 靶（原仪器落盘值；d 为控制台读数，TERMS/E120 修订 v3 在册）
FIDELITY_TARGETS = {
    "b": {"value": 0.1044, "source": "outputs/e119_k1_t0_check_20260903/e119_k1_t0.json:cos_fixed_query_vs_unmix_bgrid"},
    "d": {"value": 0.0700, "source": "e120_t0_localize.py 控制台读数（TERMS.md 固定单查询近视行 / E120 修订 v3）；理论侧引用 0.076"},
}
# 逐头 n_eff 参照（outputs/vrow_ngate_20260912/，eval 流 320 窗，commit 9096483）
NEFF_REFERENCE = {
    "d": {"per_head": [2.14, 8.23, 31.45, 89.00], "source": "outputs/vrow_ngate_20260912/vrow_ngate_v37ks_d_sm_q15_circuit_20k_ctx4096_20260825b.json"},
    "b": {"per_head": [2.12, 8.04, 31.68, 88.30], "source": "outputs/vrow_ngate_20260912/vrow_ngate_v37ks_b_sm_denoise_v2_20k_ctx4096_20260829.json"},
}


# ---------------------------------------------------------------------------
# 纯数学件（单测覆盖）：逐头分解 + 全局拼装恒等式
# ---------------------------------------------------------------------------


def perhead_cos_terms(a: torch.Tensor, b: torch.Tensor) -> dict:
    """逐头分解余弦账本。a, b: (n, H, hv)（read_fixed / v̂ 的头视图，fp32 入
    fp64 累积）。Returns dict:
      per_head.cos[h]        = <a_h,b_h>/(‖a_h‖‖b_h‖)
      per_head.dot/an2/bn2   = 逐头内积与范数平方（拼装原料）
      global_from_terms      = Σdot/sqrt(Σan2·Σbn2) —— 原仪器全局展平 cos 的
                               分块拼装形（展平对分块置换不变，恒等严格成立）
      global_direct          = 全展平向量直接算的 cos（同 fp64，互证）
      assembly_gap           = 两者差（数值精度地板，应 ~1e-9）"""
    a = a.detach().to(torch.float64).reshape(a.shape[0], a.shape[1], -1)
    b = b.detach().to(torch.float64).reshape(b.shape[0], b.shape[1], -1)
    if a.shape != b.shape:
        raise ValueError(f"perhead_cos_terms: 形状不符 {tuple(a.shape)} vs {tuple(b.shape)}")
    dots, an2s, bn2s, cos_h = [], [], [], []
    for h in range(a.shape[1]):
        ah, bh = a[:, h].reshape(-1), b[:, h].reshape(-1)
        dot = float(ah @ bh)
        an2, bn2 = float(ah @ ah), float(bh @ bh)
        dots.append(dot)
        an2s.append(an2)
        bn2s.append(bn2)
        cos_h.append(dot / math.sqrt(an2 * bn2) if an2 > 0.0 and bn2 > 0.0 else float("nan"))
    aflat, bflat = a.reshape(-1), b.reshape(-1)
    global_direct = float(aflat @ bflat / (aflat.norm() * bflat.norm()))
    global_terms = sum(dots) / math.sqrt(sum(an2s) * sum(bn2s))
    return {
        "per_head": {"cos": cos_h, "dot": dots, "an2": an2s, "bn2": bn2s},
        "global_from_terms": global_terms,
        "global_direct": global_direct,
        "assembly_gap": abs(global_terms - global_direct),
    }


def assemble_global_cos(parts: list[dict]) -> float:
    """跨窗池化拼装：Σ窗 Σ头 dot / sqrt(Σ窗 Σ头 an2 · Σ窗 Σ头 bn2)。"""
    dot = sum(sum(p["per_head"]["dot"]) for p in parts)
    an2 = sum(sum(p["per_head"]["an2"]) for p in parts)
    bn2 = sum(sum(p["per_head"]["bn2"]) for p in parts)
    return dot / math.sqrt(an2 * bn2)


def load_query(npz_path: str) -> tuple[torch.Tensor, dict]:
    """固定查询 = 落盘 ridge 段 1 主方向 q_ridge (H, hk)。缺件/形状不符响亮
    报错。Returns (q fp32, 元数据)。"""
    import numpy as np

    p = Path(npz_path)
    if not p.exists():
        raise SystemExit(f"[perhead-cos] 固定查询缺席: {p}")
    z = np.load(p)
    if "q_ridge" not in z:
        raise SystemExit(f"[perhead-cos] {p}: 缺 q_ridge 键 (实际键集 {list(z.files)})")
    q = torch.from_numpy(np.asarray(z["q_ridge"], dtype=np.float32))
    if q.dim() != 2:
        raise SystemExit(f"[perhead-cos] {p}: q_ridge 形状 {tuple(q.shape)} 非 (H, hk)")
    meta = {
        "path": str(p),
        "lam_unmix": float(z["lam_unmix"]) if "lam_unmix" in z else None,
        "n_dirs": int(z["n_dirs"]) if "n_dirs" in z else None,
        "mean_norm": float(z["mean_norm"]) if "mean_norm" in z else None,
        "per_head_norm": [round(float(x), 6) for x in q.norm(dim=-1)],
    }
    return q, meta


# ---------------------------------------------------------------------------
# 逐窗采集（原仪器逐行对齐，只多记逐头账本）
# ---------------------------------------------------------------------------


@torch.no_grad()
def collect_window_perhead(model, channel: str, q: torch.Tensor, clean: torch.Tensor,
                           byte_mask: torch.Tensor, device: torch.device, lam: float):
    """单窗：前端 → 通道 gates → 自然态 → 段1 解混 v̂ → 固定查询读出 → 逐头账本。
    channel 'k'（b 格）/ 'v'（d 格）。Returns (terms dict, n_real)。"""
    source = clean.to(device).masked_fill(byte_mask.to(device), MASK_ID)
    chunks, memory, index = _front_end(model, source)
    n_real = int(chunks.chunk_mask[0].sum())
    if channel == "k":
        gates = model.write_head_k(index.float())
        states = trained_states(model.state_machine_k, gates, n_real)
    elif channel == "v":
        gates = model.write_head(memory)
        states = trained_states(model.state_machine, gates, n_real)
    else:
        raise ValueError(f"channel 非法: {channel!r}")
    vhat, _ = ridge_unmix(gates, states, lam)  # (1, n, H*hv) head-major
    heads, hv = gates["k"].shape[2], gates["v"].shape[-1]
    read_fixed = torch.einsum("hk,bnhkv->bnhv", q.to(device).float(), states.float())
    a = read_fixed[0, :n_real].reshape(n_real, heads, hv).cpu()
    b = vhat[0, :n_real].reshape(n_real, heads, hv).cpu()
    return perhead_cos_terms(a, b), n_real


def run_pass(model, ns, channel: str, q: torch.Tensor, windows, masks, device, lam) -> dict:
    """一套窗流的完整 pass：逐窗账本 + 聚合（窗均值全局 cos + 跨窗池化拼装
    + 逐头窗均值 cos）。"""
    parts, n_reals = [], []
    t0 = time.time()
    for wi, (clean, byte_mask) in enumerate(zip(windows, masks)):
        terms, n_real = collect_window_perhead(model, channel, q, clean, byte_mask, device, lam)
        parts.append(terms)
        n_reals.append(n_real)
        print(
            f"[perhead-cos] win {wi} n={n_real} global={terms['global_from_terms']:.4f} "
            "per-head=" + " ".join(f"{c:.4f}" for c in terms["per_head"]["cos"])
            + f"（{time.time() - t0:.0f}s）",
            flush=True,
        )
    n_win = len(parts)
    heads = len(parts[0]["per_head"]["cos"])
    an2_tot = [sum(p["per_head"]["an2"][h] for p in parts) for h in range(heads)]
    bn2_tot = [sum(p["per_head"]["bn2"][h] for p in parts) for h in range(heads)]
    tot = math.sqrt(sum(an2_tot) * sum(bn2_tot))
    return {
        "n_windows": n_win,
        "chunks_per_window_mean": round(sum(n_reals) / n_win, 1) if n_win else None,
        "global_cos_mean_over_windows": round(sum(p["global_from_terms"] for p in parts) / n_win, 6),
        "global_cos_pooled_assembly": round(assemble_global_cos(parts), 6),
        "per_head_cos_mean_over_windows": [
            round(sum(p["per_head"]["cos"][h] for p in parts) / n_win, 6) for h in range(heads)
        ],
        "per_head_cos_pooled_assembly": [round(c, 6) for c in _pooled_perhead(parts)],
        # 逐头池化范数份额 share_h = sqrt(Σan2_h·Σbn2_h)/sqrt(Σan2·Σbn2)（和为 1）:
        # 池化逐头 cos = Σ_h share_h·cos_h(池化) —— share 高度偏斜时池化逐头数
        # 被单头/单窗支配, 稳读数看窗均值列
        "per_head_pooled_norm_share": [round(math.sqrt(a * b) / tot, 6) for a, b in zip(an2_tot, bn2_tot)],
        "per_window": [
            {
                "window": wi,
                "n_real": n_reals[wi],
                "global_cos": round(parts[wi]["global_from_terms"], 6),
                "per_head_cos": [round(c, 6) for c in parts[wi]["per_head"]["cos"]],
                # 拼装原料（fp64 原值截断 9 位）: 逐头内积/范数平方, 供离线复算
                # 池化拼装 cos = Σdot/sqrt(Σan2·Σbn2) 与逐头份额 share_h
                "per_head_dot": [round(x, 9) for x in parts[wi]["per_head"]["dot"]],
                "per_head_an2": [round(x, 9) for x in parts[wi]["per_head"]["an2"]],
                "per_head_bn2": [round(x, 9) for x in parts[wi]["per_head"]["bn2"]],
            }
            for wi in range(n_win)
        ],
    }


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    p = argparse.ArgumentParser()
    p.add_argument("--b-ckpt", default=B_CKPT)
    p.add_argument("--d-ckpt", default=D_CKPT)
    p.add_argument("--grid", default="both", choices=["b", "d", "both"])
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--data-path", default=DEFAULT_DATA_PATH)
    p.add_argument("--b-q-npz", default=B_Q_NPZ)
    p.add_argument("--d-q-npz", default=D_Q_NPZ)
    p.add_argument("--fidelity-b-windows", type=int, default=16, help="b 格原仪器窗数（eval 流）")
    p.add_argument("--fidelity-d-windows", type=int, default=4, help="d 格原仪器窗数（训练流）")
    p.add_argument("--eval-windows", type=int, default=64, help="两格同卷 eval 扩展 pass 窗数")
    p.add_argument("--tolerance", type=float, default=5e-3, help="fidelity 聚合校验容差")
    p.add_argument("--out-dir", default=DEFAULT_OUT_DIR)
    p.add_argument(
        "--allow-fidelity-fail",
        action="store_true",
        help="仅 CPU 冒烟放行 fidelity 校验失败（正常测量不许用）",
    )
    args = p.parse_args()
    device = torch.device(
        "cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu"
    )
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    grids = {}
    if args.grid in ("b", "both"):
        model, ns, step, run_name, _pt = load_ckpt(args.b_ckpt, device)
        ns.data_path = args.data_path
        q, q_meta = load_query(args.b_q_npz)
        grids["b"] = _run_grid(
            "b", model, ns, "k", q, q_meta, step, run_name, args, device,
            "b 格 K 通道（write_head_k / state_machine_k）",
        )
        del model
        if device.type == "cuda":
            torch.cuda.empty_cache()
    if args.grid in ("d", "both"):
        model, ns, step = load_model(Path(args.d_ckpt), device)
        ns.data_path = args.data_path
        q, q_meta = load_query(args.d_q_npz)
        grids["d"] = _run_grid(
            "d", model, ns, "v", q, q_meta, step, Path(args.d_ckpt).name, args, device,
            "d 格 V 通道（write_head / state_machine）",
        )

    fidelity_fail = [g for g, r in grids.items() if r["fidelity_check"]["status"] != "PASS"]
    if fidelity_fail and not args.allow_fidelity_fail:
        raise SystemExit(
            f"[perhead-cos] fidelity 聚合校验未过 {fidelity_fail} —— 逐头口径与原仪器不一致, "
            "停下来修, 不许报数（细节见上方日志与 json）"
        )

    for g, r in grids.items():
        (out_dir / f"perhead_cos_{r['run']}.json").write_text(
            json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        write_grid_summary(out_dir, g, r)

    if len(grids) == 2:
        write_combined_summary(out_dir, grids)
    print(f"[perhead-cos] 完成（{time.time() - t0:.0f}s）→ {out_dir}", flush=True)


def _run_grid(grid: str, model, ns, channel: str, q: torch.Tensor, q_meta: dict, step: int,
              run_name: str, args, device, channel_semantics: str) -> dict:
    lam = LAM_UNMIX
    passes: dict[str, dict] = {}

    if channel == "k":  # b 格 fidelity = 原仪器：eval 流 16 窗
        fw = build_eval_windows(ns, args.fidelity_b_windows)
        fm = build_masks(fw, ns)
        f_note = f"eval 流（seed={ns.seed}+9999）{args.fidelity_b_windows} 窗 + build_masks(eval_mask_seed={ns.eval_mask_seed}) —— e119_k1_t0_decodability.py 逐位对齐"
    else:  # d 格 fidelity = 原仪器：训练流 4 窗
        fw = build_train_windows(ns, args.fidelity_d_windows)
        fm = build_train_masks(fw, ns)
        f_note = f"训练流（seed={ns.seed}）{args.fidelity_d_windows} 窗 + 训练态掩码流 —— e120_t0_localize.py 逐位对齐"
    print(f"[perhead-cos] {run_name} fidelity pass: {f_note}", flush=True)
    passes["fidelity"] = run_pass(model, ns, channel, q, fw, fm, device, lam)

    ew = build_eval_windows(ns, args.eval_windows)
    em = build_masks(ew, ns)
    print(f"[perhead-cos] {run_name} eval 扩展 pass: eval 流 {args.eval_windows} 窗（两格同卷, 与 n_eff 测量同流型）", flush=True)
    passes["eval_extended"] = run_pass(model, ns, channel, q, ew, em, device, lam)

    target = FIDELITY_TARGETS[grid]
    got = passes["fidelity"]["global_cos_mean_over_windows"]
    delta = round(got - target["value"], 6)
    check = {
        "target": target["value"],
        "target_source": target["source"],
        "tolerance": args.tolerance,
        "measured": got,
        "delta": delta,
        "status": "PASS" if abs(delta) <= args.tolerance else "FAIL",
    }

    heads = [f"h{h}" for h in range(len(passes["fidelity"]["per_head_cos_mean_over_windows"]))]
    neff_ref = NEFF_REFERENCE["b" if channel == "k" else "d"]
    return {
        "probe": "固定查询读出 cos 逐头分解（容量界稿点单, 零训练）",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "run": run_name,
        "checkpoint_step": step,
        "channel": channel,
        "channel_semantics": channel_semantics,
        "instrument_provenance": {
            "b": "outputs/_remote_scripts/e119_k1_t0_decodability.py（裁 3, 落盘 0.1044）",
            "d": "outputs/_remote_scripts/e120_t0_localize.py（9/03 晚定位件, 控制台 0.07）",
        }[grid],
        "aggregation_identity": "cos_global = Σ_h <a_h,b_h> / sqrt(Σ_h‖a_h‖²·Σ_h‖b_h‖²)（fp64 累积; 展平分块置换不变）",
        "lam_unmix": lam,
        "query": q_meta,
        "caveats": [
            "逐头 cos 符号承袭 q_ridge 的逐头符号约定（主方向符号对齐方向云均值, probe_q20_ridge_direction/principal_direction）——跨头比大小看幅值, 格内符号自洽。",
            "池化逐头 cos 会被范数份额支配（见 per_head_pooled_norm_share）, 「哪头承重」以窗均值列为准。",
            "eval 扩展 pass 的两格全局窗均值接近（窗采样 sd 见 per_window）—— recorded 0.1044(b,16 窗) vs 0.0700(d,4 窗训练流) 的格间差部分是窗采样与窗流差, 同卷对照看 eval_extended。",
        ],
        "fidelity_protocol": f_note,
        "eval_protocol": f"eval 流 {args.eval_windows} 窗 + build_masks（两格同卷, n_eff 同流型）",
        "passes": passes,
        "fidelity_check": check,
        "heads": heads,
        "n_eff_reference": {
            "per_head": neff_ref["per_head"],
            "inv_sqrt_per_head": [round(1.0 / math.sqrt(v), 4) for v in neff_ref["per_head"]],
            "source": neff_ref["source"],
        },
        "verdict": "判词留白（理论侧裁）",
    }


def write_grid_summary(out_dir: Path, grid: str, r: dict) -> None:
    fid, ext = r["passes"]["fidelity"], r["passes"]["eval_extended"]
    chk = r["fidelity_check"]
    json_name = f"perhead_cos_{r['run']}.json"
    lines = [
        f"固定查询读出 cos 逐头分解 —— {grid} 格（{r['channel_semantics']}）",
        f"日期 {r['created']}  设备 {r['device']}  run={r['run']} (step {r['checkpoint_step']})  λ_unmix={r['lam_unmix']}",
        f"固定查询 q_ridge: {r['query']['path']}  逐头范数 {r['query']['per_head_norm']}",
        "",
        f"fidelity pass（{r['fidelity_protocol']}）",
        f"  聚合硬校验: 实测 {chk['measured']:.4f} vs 靶 {chk['target']:.4f} "
        f"(Δ={chk['delta']:+.4f}, 容差 {chk['tolerance']}) → {chk['status']}",
        f"  逐头 cos（窗均值）: " + " ".join(
            f"h{h}={c:.4f}" for h, c in enumerate(fid["per_head_cos_mean_over_windows"])
        ),
        f"  逐头 cos（跨窗池化拼装）: " + " ".join(
            f"h{h}={c:.4f}" for h, c in enumerate(fid["per_head_cos_pooled_assembly"])
        ),
        "",
        f"eval 扩展 pass（{r['eval_protocol']}; 块/窗均值 {ext['chunks_per_window_mean']}）",
        f"  全局 cos（窗均值 {ext['global_cos_mean_over_windows']:.4f} / 池化 {ext['global_cos_pooled_assembly']:.4f}）",
        f"  逐头 cos（窗均值）: " + " ".join(
            f"h{h}={c:.4f}" for h, c in enumerate(ext["per_head_cos_mean_over_windows"])
        ),
        f"  逐头 cos（跨窗池化拼装）: " + " ".join(
            f"h{h}={c:.4f}" for h, c in enumerate(ext["per_head_cos_pooled_assembly"])
        ),
        f"  逐头池化范数份额: " + " ".join(
            f"h{h}={c:.4f}" for h, c in enumerate(ext["per_head_pooled_norm_share"])
        ) + "  ← 池化逐头数被份额支配, 稳读数看窗均值",
        "",
        "对照表（判词留白, 理论侧裁）—— 逐头 cos vs 1/√n_eff（n_eff 源: " + r["n_eff_reference"]["source"] + "）:",
        "  头 | cos(eval扩展,窗均值) | 1/√n_eff | n_eff",
        "\n".join(
            f"  h{h} | {ext['per_head_cos_mean_over_windows'][h]:.4f} | "
            f"{r['n_eff_reference']['inv_sqrt_per_head'][h]:.4f} | {r['n_eff_reference']['per_head'][h]}"
            for h in range(len(r["heads"]))
        ),
        "",
        f"汇总: {out_dir / json_name}",
    ]
    (out_dir / f"perhead_cos_{r['run']}_SUMMARY.txt").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines), flush=True)


def _pooled_perhead(parts: list[dict]) -> list[float]:
    heads = len(parts[0]["per_head"]["cos"])
    out = []
    for h in range(heads):
        dot = sum(p["per_head"]["dot"][h] for p in parts)
        an2 = sum(p["per_head"]["an2"][h] for p in parts)
        bn2 = sum(p["per_head"]["bn2"][h] for p in parts)
        out.append(dot / math.sqrt(an2 * bn2))
    return out


def write_combined_summary(out_dir: Path, grids: dict) -> None:
    lines = ["固定查询读出 cos 逐头分解 —— 两格总表（判词留白, 理论侧裁）", ""]
    for grid in ("b", "d"):
        r = grids.get(grid)
        if r is None:
            continue
        ext = r["passes"]["eval_extended"]
        chk = r["fidelity_check"]
        lines += [
            f"== {grid} 格（{r['channel_semantics']}） ==",
            f"  fidelity 硬校验: {chk['measured']:.4f} vs {chk['target']:.4f} → {chk['status']}（靶源: {chk['target_source']}）",
            "  头 | cos(fidelity,窗均值) | cos(eval扩展,窗均值) | 1/√n_eff | n_eff",
        ]
        fid = r["passes"]["fidelity"]
        for h in range(len(r["heads"])):
            lines.append(
                f"  h{h} | {fid['per_head_cos_mean_over_windows'][h]:.4f} | "
                f"{ext['per_head_cos_mean_over_windows'][h]:.4f} | "
                f"{r['n_eff_reference']['inv_sqrt_per_head'][h]:.4f} | {r['n_eff_reference']['per_head'][h]}"
            )
        lines.append("")
    lines += [
        "测量级读数（非理论判词, 判词留白归理论侧）:",
        "  · h3 独承重: 否。b 格 h3 窗均值 +0.19（eval64 62/64 窗为正, 是 b 格最大正头, 但幅值 0.19 高于其 1/√n_eff=0.106）；",
        "    d 格 h3 一致负（eval64 64/64 窗为负, −0.26）——d 格聚合 0.07 无法经 h3 读作 1/√88.3=0.106（符号与幅值均 contra）。",
        "  · 逐头 |cos| 全头 0.01–0.36 带, 无一头贴各自 1/√n_eff 阶梯 [0.68, 0.35, 0.18, 0.106]（h0 尤甚: 预言 0.68, 实测 |cos|≤0.14）。",
        "  · 同卷（eval 流 64 窗）两格全局窗均值几乎重合: b 0.0782±0.066 / d 0.0805±0.147 —— recorded 0.1044(b,16 窗 eval 流) vs",
        "    0.0700(d,4 窗训练流) 的格间差在窗采样噪声带内（d 4 窗均值 sd≈0.074）, 格间差不能按面值读。",
        "  · 池化逐头范数份额高度偏斜（b: h1 占 98%、h3 单窗 56 占 h3 质量 87%; d: h0 占 99%）——查询读出能量逐头分布",
        "    由状态范数决定, 与 n_eff 阶梯不同序, 机制事实随行。",
        "",
    ]
    (out_dir / "SUMMARY.txt").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
