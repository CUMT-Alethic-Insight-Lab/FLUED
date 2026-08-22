"""锁 v2（协同适应锁）V 形检验·相一：冻结瞬态零步探针（预注册 FLUED_V3_7_LOCK_V2_VTEST_20260821_CN.md，2026-08-21，零训练）。

试验场：40K 收顶 0.3185 对象（retrain_readout_c_tokcenter_40k_20260819 =
基座 v37ks_c_is_v372_cloze_tokcenter_20k_ctx4096_20260818 + 复训
{realign, decoder_in, decoder, backbone} 四模块 overlay，读出链全冻结）。

设计（预注册 §2 相一，杀招所在）：读出链一个参数不动，单次部署几何
**瞬切**（to_k_center 坍缩部署 → to_k_whiten 白化健康部署——同一 to_k
权重，纯 buffer 机制，零训练零步），切换后零步测探针级逐 slot 可读性
（natural_vrows 同款仪表：v_rows = 复训 realign(q·S)，byte_probe
real−garbage）。判死条款：**切换零步若健康几何的可读性不低于坍缩基线
→ 锁判死**（"单边修几何即可"成立，协同跳变主张作废）；健康可读性低于
坍缩基线 → 锁存活（失读期实存，转相二看恢复动力学）。

三臂（同窗同 mask 同 targets，eval seed 1042 十六窗，fp32 硬冻结）：
  C 坍缩基线：to_k_center 部署 → 自然 KDA 态 S → 冻结链读出；
  H 健康瞬切：to_k_whiten 部署（μ≈0.10 档）→ KDA 态 S_w → 同一冻结链读出；
  O oracle 参照：完美累积态（E73-A2 同款，坍缩键不动）→ 同一冻结链读出
    ——oracle_vrows≈0.04 静态签名在本对象的受控复现参照点。

相二（恢复动力学，回升轨迹）另行立项执行，不在本工具范围。

Usage:
  python tools/analysis/v3_6/probe_lock_v2_vtest.py --device cuda
  CPU 冒烟: python tools/analysis/v3_6/probe_lock_v2_vtest.py --device cpu --max-windows 2
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from argparse import Namespace
from pathlib import Path

import torch

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from flued.data import MASK_ID  # noqa: E402
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402
from tools.train.v3_6.train_v36 import build_model  # noqa: E402
from tools.analysis.v3_6.probe_oracle_write_verdict import (  # noqa: E402
    _front_end,
    build_eval_windows,
    build_masks,
    byte_probe,
    load_model,
    oracle_states,
    read_trained,
    trained_states,
)

BASE_RUN = "checkpoints/v37ks_c_is_v372_cloze_tokcenter_20k_ctx4096_20260818"
RETRAIN_PKG = "checkpoints/retrain_readout_c_tokcenter_40k_20260819/retrained_readout.pt"
OUT_DIR = "outputs/lock_v2_vtest_20260821"
PERM_SEED = 20260819
WARM_PASSES = 3


def load_plateau_object(device: torch.device, whiten: bool):
    """Load the base ckpt (optionally with to_k_whiten flipped on — buffers
    are non-persistent so the ckpt loads strict-clean either way) and overlay
    the 40K retrained chain modules. Hard-frozen, eval."""
    cfg = json.loads((Path(BASE_RUN) / "resolved_config.json").read_text(encoding="utf-8"))
    cfg["data_manifest"] = ""
    if device.type != "cuda":
        cfg["kda_impl"] = "torch"
    if whiten:
        cfg["to_k_whiten"] = True  # instant deployment-geometry switch (same weights)
    ns = Namespace(**cfg)
    if s1._BPE_TOKENIZER is None and getattr(ns, "mask_mode", "mixed") == "mixed" and ns.mask_prob > 0:
        s1._load_bpe_tokenizer(ns.bpe_tokenizer_path)
    model = build_model(ns).to(device)
    payload = torch.load(Path(BASE_RUN) / "latest.pt", map_location=device, weights_only=False)
    model.load_state_dict(payload["model"], strict=True)
    pkg = torch.load(RETRAIN_PKG, map_location=device, weights_only=False)
    # the retrain package stores only the RETRAINED keys per module (the
    # shared byte_lookup was excluded from the chain); strict=False overlays
    # keep the base ckpt's shared table, which is exactly the retrain's own
    # semantics — verify no retrained key fails to land instead.
    for name, module in (("realign", model.state_machine.realign),
                         ("decoder_in", model.decoder_in),
                         ("decoder", model.decoder),
                         ("backbone", model.backbone)):
        sd = pkg["modules"][name]
        missing = [k for k in sd if k not in module.state_dict()]
        if missing:
            raise RuntimeError(f"retrain overlay key mismatch on {name}: {missing[:3]}")
        module.load_state_dict(sd, strict=False)
    for p in model.parameters():
        p.requires_grad_(False)
    model.eval()
    return model, ns


@torch.no_grad()
def warm_buffers(model, windows, masks, device, whiten: bool):
    """E75/acceptance 口径: train-mode passes to warm the EMA buffers (center
    or whiten), then back to eval — the deployment geometry being measured.
    只喂真实 chunk 行（对齐 E76/acceptance 协议：padding 行占 max_chunks 的
    ~85%，全量喂会污染 EMA 统计——实测把 c 格部署 μ 从 0.42 抬到 0.81）。"""
    wh = model.write_head
    wh.train()
    for _ in range(WARM_PASSES):
        for clean, bm in zip(windows, masks):
            source = clean.masked_fill(bm.to(clean.device), MASK_ID).to(device)
            chunks, memory, _i = _front_end(model, source)
            n = int(chunks.chunk_mask[0].sum())
            wh(memory[:, :n])
    wh.eval()


@torch.no_grad()
def collect_readouts(model, windows, masks, device, arm: str):
    """Per real chunk: interface readout rows (realign(q·S)) + targets, real
    and garbage (chunk-axis perm). arm: C (natural states), H (whitened-key
    states — model already flipped), O (oracle accumulation, natural keys)."""
    gen = torch.Generator().manual_seed(PERM_SEED)
    xs_r, xs_g, ys, yv, mus = [], [], [], [], []
    for clean, bm in zip(windows, masks):
        source = clean.masked_fill(bm.to(clean.device), MASK_ID).to(device)
        chunks, memory, _index = _front_end(model, source)
        n = int(chunks.chunk_mask[0].sum())
        gates = model.write_head(memory)
        if arm == "O":
            S = oracle_states(gates, n)
        else:
            S = trained_states(model.state_machine, gates, n)
        rows = read_trained(model.state_machine, S)[0].float()
        # key geometry signature of this arm
        kk = gates["k"][0, :n].float()
        per_head = []
        for h in range(kk.size(1)):
            sim = (kk[:, h] @ kk[:, h].T).abs()
            per_head.append(float(sim[~torch.eye(n, dtype=torch.bool, device=kk.device)].mean()))
        mus.append(sum(per_head) / len(per_head))
        bt, bs, _m = s1.make_targets(
            clean.to(device), torch.zeros_like(bm).to(device),
            chunks.chunk_ids, chunks.offsets, model.config.max_chunks, model.config.max_span,
        )
        perm = torch.randperm(n, generator=gen).to(device)
        xs_r.append(rows.cpu())
        xs_g.append(rows[perm].cpu())
        ys.append(bt[0, :n].cpu())
        yv.append(bs[0, :n].cpu())
    return torch.cat(xs_r), torch.cat(xs_g), torch.cat(ys), torch.cat(yv), sum(mus) / len(mus)


def _shape(diff, head=(0, 4), tail=(16, 32)):
    def mean(lo, hi):
        vals = [diff[str(s)] for s in range(lo, hi) if str(s) in diff]
        return round(sum(vals) / len(vals), 4) if vals else None
    h, t = mean(*head), mean(*tail)
    return {"head_mean": h, "tail_mean": t,
            "head_over_tail": round(h / t, 3) if h is not None and t and t > 1e-9 else None}


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    p = argparse.ArgumentParser()
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--max-windows", type=int, default=16)
    p.add_argument("--report-slots", type=int, default=32)
    p.add_argument("--out-dir", default=OUT_DIR)
    args = p.parse_args()
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    model_c, ns = load_plateau_object(device, whiten=False)
    windows = build_eval_windows(ns, args.max_windows)
    masks = build_masks(windows, ns)
    model_h, _ = load_plateau_object(device, whiten=True)
    print(f"[vtest] plateau object loaded (base+retrain overlay, chain frozen) ({time.time() - t0:.0f}s)", flush=True)

    warm_buffers(model_c, windows, masks, device, whiten=False)
    warm_buffers(model_h, windows, masks, device, whiten=True)
    print(f"[vtest] buffers warmed ({time.time() - t0:.0f}s)", flush=True)

    results = {}
    for arm, model in (("C", model_c), ("H", model_h), ("O", model_c)):
        xr, xg, ys, yv, mu = collect_readouts(model, windows, masks, device, arm)
        pr = byte_probe(xr, ys, yv)
        pg = byte_probe(xg, ys, yv)
        diff = {s: round(pr[s]["acc"] - pg[s]["acc"], 4) for s in pr}
        results[arm] = {"diff": diff, "shape": _shape(diff), "key_mu": round(mu, 4)}
        print(f"[vtest] arm {arm}: key_mu={mu:.4f} head/tail="
              f"{results[arm]['shape']['head_mean']}/{results[arm]['shape']['tail_mean']} ({time.time() - t0:.0f}s)", flush=True)

    c, h, o = results["C"], results["H"], results["O"]
    c_mean = sum(c["diff"].values()) / len(c["diff"])
    h_mean = sum(h["diff"].values()) / len(h["diff"])
    # 判死条款（预注册）：切换零步健康几何可读性不低于坍缩基线 → 锁判死
    lock_dead = h_mean >= c_mean
    verdict = (
        f"锁判死：健康几何瞬切零步的可读性（均值 {h_mean:.4f}）不低于坍缩基线（{c_mean:.4f}）——"
        "单边修几何即可，协同跳变主张作废。"
        if lock_dead else
        f"锁存活（相一）：健康几何瞬切零步的可读性（均值 {h_mean:.4f}）低于坍缩基线（{c_mean:.4f}）——"
        "失读期实存，协同适应锁的动力学签名成立；转相二看恢复动力学。"
    )

    report = {
        "probe": "锁 v2 V 形检验·相一（冻结瞬态零步探针，40K 平台格）",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "object": {"base": Path(BASE_RUN).name, "retrain": Path(RETRAIN_PKG).name,
                   "chain": "frozen (realign+decoder_in+decoder+backbone overlay)"},
        "params": {"windows": len(windows), "perm_seed": PERM_SEED, "warm_passes": WARM_PASSES,
                   "eval_mask_seed": ns.eval_mask_seed},
        "arms": {
            "C": "坍缩基线：to_k_center 部署 → 自然 KDA 态 → 冻结链读出",
            "H": "健康瞬切：to_k_whiten 部署（同权重纯 buffer 切换，零训练）→ KDA 态 → 同一冻结链",
            "O": "oracle 参照：完美累积态（坍缩键不动）→ 同一冻结链（oracle_vrows 静态签名复现点）",
        },
        "results": {arm: {"key_mu": r["key_mu"], "shape": r["shape"], "real_minus_garbage": r["diff"]}
                    for arm, r in results.items()},
        "kill_clause": {"healthy_mean": round(h_mean, 4), "collapsed_mean": round(c_mean, 4),
                        "lock_dead": lock_dead},
        "verdict": verdict,
        "timing_sec": round(time.time() - t0, 1),
    }
    out_path = out_dir / "lock_v2_vtest.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "锁 v2 V 形检验·相一（冻结瞬态零步，40K 平台格，读出链全冻结）",
        f"日期 {report['created']}  设备 {device.type}  窗 {len(windows)}  口径 eval seed 1042",
        "",
        f"键几何：C(坍缩基线) μ={c['key_mu']}  H(白化瞬切) μ={h['key_mu']}  O(oracle键不动) μ={o['key_mu']}",
        "",
        "逐 slot 可读性（real−garbage）：slot | C 坍缩 | H 健康 | O oracle",
    ]
    for s in range(min(args.report_slots, len(c["diff"]))):
        k = str(s)
        lines.append(f"  {s:>4d} | {c['diff'].get(k, float('nan')):+.4f} | "
                     f"{h['diff'].get(k, float('nan')):+.4f} | {o['diff'].get(k, float('nan')):+.4f}")
    lines += [
        "",
        f"形态：C head {c['shape']['head_mean']} tail {c['shape']['tail_mean']} 比 {c['shape']['head_over_tail']}",
        f"      H head {h['shape']['head_mean']} tail {h['shape']['tail_mean']} 比 {h['shape']['head_over_tail']}",
        f"      O head {o['shape']['head_mean']} tail {o['shape']['tail_mean']} 比 {o['shape']['head_over_tail']}",
        "",
        f"判死条款（预注册）：切换零步健康可读性（{h_mean:.4f}）≥ 坍缩基线（{c_mean:.4f}）→ 锁判死。",
        f"判词：{verdict}",
        "",
        f"完整数据: {out_path}",
    ]
    summary_path = out_dir / "SUMMARY.txt"
    summary_path.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
