"""段尾信息丢失定位测量包（用户裁定的审计前置项，2026-08-19，零训练纯测量）。

测量 1（两发合一 + 两个对照臂，同窗同探针一次跑完）：把"段首集中"（E86 在 b
格 k_rows 上实测的自然态逐 slot 剖面：slot0 +0.126 → slot18-31 ~0.02-0.05）
定位到三个嫌疑人之一——summarizer 压缩 / 状态机写入 / 接口选择（读出路径）。

  对象：c 格 checkpoints/v37_c_is_v371_20k_ctx4096_20260817 的 V 通道
  （v_row_source="state"：summarizer memory 行 -> WriteHead -> KDA delta 递推
  -> 固定 query 读出 -> realign -> v_rows）。四个剖面臂（全部 E73-A6 口径：
  2-fold one-vs-all 岭回归，real−garbage，段内 slot 0..max_span-1，摘要报
  0..31）：

    memory_rows    summarizer 出口原始 V 行（还没进状态机）——嫌疑人 1
    write_values   WriteHead 写值 v_i（1024 = H*hv）——嫌疑人 2 的写入形成半
    oracle_vrows   oracle 态 S_i=Σ_{j≤i} k_jv_jᵀ（无衰减无擦除累计叠加）走
                   trained 读出（read_trained = realign(q·S)，S39-A2 臂同款）
                   ——隔离"递推侵蚀"与"读出路径位置偏置"
    natural_vrows  trained 自然态走同一读出——生产接口向量（护栏二同张量，
                   slot0-3 必须复测 +0.4723/+0.3758/+0.3251/+0.4777 作锚）

  补充对照臂（防 oracle+trained 读出臂退化成全零后判词失据——S39 已知固定
  query 读出读不动 oracle 叠加态（A2 崩、键塌缩 0.9354），此时"oracle 平"
  不能解释为"信息均匀保留"）：
    oracle_ridge   oracle 态 ridge 解混取回本段 v̂_i（λ=0.01，A4 同款行，
                   探针本身是线性的、不受 A4 解码域偏移影响）——态内信息上限
    natural_ridge  trained 态同一 ridge 解混——递推后段内各 slot 实际留存

  判词逻辑：
    memory 已段首集中            → summarizer 压缩（嫌疑人 1）；
    memory 平、写值集中           → 写入形成（WriteHead，嫌疑人 2 的成形半）；
    写值平、natural_ridge 集中    → delta 递推侵蚀段尾（嫌疑人 2 的动力学半）；
    natural_ridge 平、natural 读出集中 → 读出路径位置偏置 = 接口选择（嫌疑人 3）；
    oracle+trained 读出臂全零     → 读出选择失败旁证（键塌缩下 q·k 近似均匀，
                                   own-chunk 份额≈1/i，接口选择嫌疑的另一种形态）。
  （"平/集中"按各臂 real−garbage 曲线的 head(0-3)/tail(16-31) 均值比判，
  绝对档级跨臂可比：同一探针同一批 chunk 同一批目标。）

  garbage 纪律：同一批行沿 chunk 轴打乱（边际分布不变、chunk-内容配对打碎）。
  读出逐 chunk 独立 ⟹ 打乱读出行 ≡ 打乱状态再读出（与护栏二逐位同构，
  排列种子 20260819、每窗一抽、窗序一致——四臂共享同一组排列，跨臂差不含
  置换采样噪声）。

测量 2（对账，不是新测量）：护栏二 +0.47（接口=状态读出行 realign 后，c 格）
vs 逐 slot 剖面 +0.126（slot0，接口=k_rows，b 格手术版）——逐项列出两数的
探针输入张量/被测对象/格/数据 split/指标定义/slot 定义/单位，给换算关系与
对账结论。数据从两个源 json 原地取数，协议事实来自两个源脚本与两边
resolved_config.json（本脚本 docstring 末节表格即对账表，json 里同构落地）。

口径：16 窗 eval seed 1042（build_eval_windows/build_masks，与接口探针/
oracle 判决/消费剖面同源）；fp32、无 autocast、checkpoint 只读硬冻结。

Usage:
  python tools/analysis/v3_6/measure_tail_loss_localization.py --device cuda
  CPU 冒烟: python tools/analysis/v3_6/measure_tail_loss_localization.py --device cpu --max-windows 2
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

from flued.data import MASK_ID  # noqa: E402
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402
from tools.analysis.v3_6.probe_oracle_write_verdict import (  # noqa: E402
    _front_end,
    build_eval_windows,
    build_masks,
    byte_probe,
    load_model,
    oracle_states,
    read_trained,
    ridge_unmix,
    trained_states,
)

C_RUN = "checkpoints/v37_c_is_v371_20k_ctx4096_20260817"
RIDGE_LAM = 0.01  # S39: best cos(v̂,v) regime for both state types (0.78/0.96)
ARM_ORDER = ("memory_rows", "write_values", "oracle_ridge", "natural_ridge", "oracle_vrows", "natural_vrows")
PERM_SEED = 20260819  # same seed + same per-window draw order as the interface probe
IFACE_JSON = "outputs/interface_probe_20260818/interface_probe.json"
E86_JSON = "outputs/consumption_profile_20260819/consumption_profile.json"
OUT_DIR = "outputs/audit_measurements_20260819"

# 护栏二锚（measure_interface_probe.py 实测，同窗同探针同 garbage 种子）：
# natural_vrows 臂的 slot0-3 real−garbage 必须复测到这四个数（±0.01）。
IFACE_ANCHOR_DIFF = {"0": 0.4723, "1": 0.3758, "2": 0.3251, "3": 0.4777}


# ---------------------------------------------------------------------------
# row collection: four arms over the same windows, one shared permutation set
# ---------------------------------------------------------------------------


@torch.no_grad()
def collect_arm_rows(model, windows, masks, device, seed: int = PERM_SEED):
    """Per real chunk, four arm rows on the c-grid V channel + per-slot clean
    byte targets (ALL slots 0..max_span-1). The same per-window permutations
    (one randperm per window, drawn in window order from `seed`) produce every
    arm's garbage rows — cross-arm differences carry no permutation noise.
    Readout is per-chunk, so permuting post-readout rows is bit-identical to
    the interface probe's permute-states-then-read."""
    gen = torch.Generator().manual_seed(seed)
    arms = ("memory_rows", "write_values", "oracle_ridge", "natural_ridge", "oracle_vrows", "natural_vrows")
    xs = {f"{a}_{kind}": [] for a in arms for kind in ("real", "garbage")}
    ys, yvalid = [], []
    mech = []
    sm = model.state_machine
    q = sm.readout_query[0].float()  # (H, hk) — readout_queries == 1 on this grid
    for clean, bm in zip(windows, masks):
        source = clean.masked_fill(bm.to(clean.device), MASK_ID).to(device)
        chunks, memory, _index = _front_end(model, source)
        n = int(chunks.chunk_mask[0].sum())
        gates = model.write_head(memory)
        S_tr = trained_states(sm, gates, n)
        S_or = oracle_states(gates, n)
        vh_or, cos_or = ridge_unmix(gates, S_or, RIDGE_LAM)  # (1, n, H*hv) own-chunk recovery
        vh_tr, cos_tr = ridge_unmix(gates, S_tr, RIDGE_LAM)
        rows = {
            "memory_rows": memory[0, :n].float(),
            "write_values": gates["v"][0, :n].float().reshape(n, -1),
            "oracle_ridge": vh_or[0].float(),
            "natural_ridge": vh_tr[0].float(),
            "oracle_vrows": read_trained(sm, S_or)[0].float(),
            "natural_vrows": read_trained(sm, S_tr)[0].float(),
        }
        perm = torch.randperm(n, generator=gen).to(device)  # one perm per window, shared by all arms
        for a in arms:
            xs[f"{a}_real"].append(rows[a].cpu())
            xs[f"{a}_garbage"].append(rows[a][perm].cpu())
        bt, bs, _m = s1.make_targets(
            clean.to(device), torch.zeros_like(bm).to(device),
            chunks.chunk_ids, chunks.offsets, model.config.max_chunks, model.config.max_span,
        )
        ys.append(bt[0, :n].cpu())
        yvalid.append(bs[0, :n].cpu())

        # mechanism: key-collapse signature + oracle own-chunk readout share
        kk = gates["k"][0, :n].float()  # (n, H, hk), rows unit-norm (WriteHead)
        kc = []
        for h in range(kk.size(1)):
            sim = (kk[:, h] @ kk[:, h].T).abs()
            off = sim[~torch.eye(n, dtype=torch.bool, device=kk.device)]
            kc.append(float(off.mean()))
        # oracle readout: row_i = realign(Σ_{j≤i} (q·k_j) v_j) — own-chunk
        # weight share = |own term| / total weight mass (uniform keys -> 1/i)
        w = torch.einsum("hk,nhk->hn", q, kk)  # (H, n): per-head readout weights
        mass = w.abs().cumsum(dim=1)  # (H, n): Σ_{j≤i} |w_j|
        share = (w.abs() / mass.clamp_min(1e-9)).mean(dim=0)  # (n,) mean over heads
        idx = torch.arange(1, n + 1, device=device, dtype=torch.float32)
        mech.append({
            "n_real": n,
            "key_cos_mean": round(sum(kc) / len(kc), 4),
            "state_norm_trained": round(float(S_tr[0, -1].norm(dim=(-2, -1)).mean()), 4),
            "state_norm_oracle": round(float(S_or[0, -1].norm(dim=(-2, -1)).mean()), 4),
            "oracle_own_share_mean": round(float(share.mean()), 4),
            "uniform_share_mean": round(float((1.0 / idx).mean()), 4),
            "readout_weight_mean": round(float(w.mean()), 4),
            "ridge_cos_oracle": round(cos_or, 4),
            "ridge_cos_trained": round(cos_tr, 4),
        })
    out = {k: torch.cat(v) for k, v in xs.items()}
    return out, torch.cat(ys), torch.cat(yvalid), mech


# ---------------------------------------------------------------------------
# profile shaping helpers
# ---------------------------------------------------------------------------


def _shape(diff: dict[str, float], head=(0, 4), tail=(16, 32)):
    """Head/tail means of the real−garbage curve + concentration ratio."""
    def mean(lo, hi):
        vals = [diff[str(s)] for s in range(lo, hi) if str(s) in diff]
        return round(sum(vals) / len(vals), 4) if vals else None
    h, t = mean(*head), mean(*tail)
    return {
        "head_mean": h,
        "tail_mean": t,
        "head_over_tail": round(h / t, 3) if h is not None and t and t > 1e-9 else None,
    }


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")  # GBK consoles cannot encode U+2212 (real−garbage)
    p = argparse.ArgumentParser()
    p.add_argument("--run-dir", default=C_RUN)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--max-windows", type=int, default=16, help="eval windows (16 = the training final-eval protocol)")
    p.add_argument("--report-slots", type=int, default=32)
    p.add_argument("--out-dir", default=OUT_DIR)
    p.add_argument("--iface-json", default=IFACE_JSON)
    p.add_argument("--e86-json", default=E86_JSON)
    args = p.parse_args()
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    model, ns, step = load_model(Path(args.run_dir), device)
    windows = build_eval_windows(ns, args.max_windows)
    masks = build_masks(windows, ns)
    print(f"[tail] model={Path(args.run_dir).name} step={step} device={device.type} windows={len(windows)} "
          f"({time.time() - t0:.0f}s)", flush=True)

    xs, ys, yv, mech = collect_arm_rows(model, windows, masks, device)
    print(f"[tail] rows collected ({time.time() - t0:.0f}s); probes running...", flush=True)

    profiles: dict[str, dict] = {}
    for arm in ARM_ORDER:
        pr = byte_probe(xs[f"{arm}_real"], ys, yv)
        pg = byte_probe(xs[f"{arm}_garbage"], ys, yv)
        diff = {s: round(pr[s]["acc"] - pg[s]["acc"], 4) for s in pr}
        profiles[arm] = {
            "probe_real": pr, "probe_garbage": pg,
            "real_minus_garbage": diff, "shape": _shape(diff),
        }
        print(f"[tail] arm={arm} slots={len(diff)} head/tail="
          f"{profiles[arm]['shape']['head_mean']}/{profiles[arm]['shape']['tail_mean']} ({time.time() - t0:.0f}s)", flush=True)

    # sanity anchor: natural_vrows must reproduce the interface probe slot0-3
    anchor_check = {}
    for s, ref in IFACE_ANCHOR_DIFF.items():
        got = profiles["natural_vrows"]["real_minus_garbage"].get(s)
        anchor_check[s] = {"ref": ref, "got": got, "abs_delta": round(abs(got - ref), 4) if got is not None else None}
    anchor_ok = all(v["abs_delta"] is not None and v["abs_delta"] <= 0.01 for v in anchor_check.values())
    print(f"[tail] anchor vs 护栏二: {json.dumps(anchor_check)} ok={anchor_ok}", flush=True)

    mech_agg = {
        "key_cos_mean": round(sum(m["key_cos_mean"] for m in mech) / len(mech), 4),
        "state_norm_trained": round(sum(m["state_norm_trained"] for m in mech) / len(mech), 4),
        "state_norm_oracle": round(sum(m["state_norm_oracle"] for m in mech) / len(mech), 4),
        "oracle_own_share_mean": round(sum(m["oracle_own_share_mean"] for m in mech) / len(mech), 4),
        "uniform_share_mean": round(sum(m["uniform_share_mean"] for m in mech) / len(mech), 4),
        "readout_weight_mean": round(sum(m["readout_weight_mean"] for m in mech) / len(mech), 4),
        "ridge_cos_oracle": round(sum(m["ridge_cos_oracle"] for m in mech) / len(mech), 4),
        "ridge_cos_trained": round(sum(m["ridge_cos_trained"] for m in mech) / len(mech), 4),
        "ridge_lambda": RIDGE_LAM,
    }

    # E86 reference curve (b-grid natural k_rows), imported for the comparison block
    e86 = json.loads(Path(args.e86_json).read_text(encoding="utf-8"))
    e86_diff = e86["slot_profile"]["real_minus_garbage"]
    iface = json.loads(Path(args.iface_json).read_text(encoding="utf-8"))

    report = {
        "probe": "段尾信息丢失定位（审计前置测量包 测量1）: oracle/summarizer-exit 逐 slot 剖面, c 格 V 通道",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "checkpoint": {"run": Path(args.run_dir).name, "step": step},
        "params": {"windows": len(windows), "perm_seed": PERM_SEED, "eval_mask_seed": ns.eval_mask_seed},
        "arms": {
            "memory_rows": "summarizer 出口原始 V 行（512，未进状态机）——嫌疑人1 summarizer 压缩",
            "write_values": "WriteHead 写值 v_i（1024=H*hv）——嫌疑人2 写入形成半",
            "oracle_ridge": f"oracle 态 ridge 解混本段取回 v̂_i（λ={RIDGE_LAM}，1024）——态内信息上限（对照臂）",
            "natural_ridge": f"trained 态同一 ridge 解混（λ={RIDGE_LAM}，1024）——递推后逐 slot 实际留存（对照臂）",
            "oracle_vrows": "oracle 态 S_i=Σk_jv_jᵀ 走 trained 读出（1536，S39-A2 同款）——隔离递推侵蚀 vs 读出位置偏置",
            "natural_vrows": "trained 自然态同一读出（1536，护栏二同张量，slot0-3 复测锚）",
        },
        "protocol": "E73-A6: 2-fold one-vs-all ridge, real−garbage, all slots 0..max_span-1, clean byte ids; "
        "garbage = 同一组 per-window chunk 轴排列（六臂共享）; 读出逐 chunk 独立 ⟹ 打乱行 ≡ 打乱状态再读出",
        "anchor_check_vs_interface_probe": {"ok": anchor_ok, "slots": anchor_check},
        "profiles": profiles,
        "mechanism": mech_agg,
        "mech_per_window": mech,
        "e86_reference_b_grid_natural_k_rows": {
            "source": args.e86_json,
            "checkpoint": e86["checkpoint"],
            "channel": e86["slot_profile"]["channel"],
            "real_minus_garbage": e86_diff,
            "shape": _shape(e86_diff),
        },
        "timing_sec": round(time.time() - t0, 1),
    }
    out_path = out_dir / "tail_loss_localization.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    # ------------------------------------------------------------------
    # measurement 2: unit reconciliation (bookkeeping from the two source
    # jsons + protocol facts from the two source scripts/configs)
    # ------------------------------------------------------------------
    recon = {
        "probe": "单位换算核对（审计前置测量包 测量2）: 护栏二 +0.47 vs 逐 slot 剖面 +0.126 对账",
        "created": report["created"],
        "numbers": {
            "A_interface_probe_slot0": {
                "value": iface["real_minus_garbage"]["0"],
                "source": args.iface_json,
                "probe_input_tensor": "v_rows = realign(q·S_trained).mean(nq=1)，post-realign / pre-decoder_in，d_pack=1536",
                "measured_object": "c 格 v37_c_is_v371_20k_ctx4096_20260817 step20000，V 通道（v_row_source=state，WriteHead 吃 memory 行）",
                "grid": "c（k=index 直通, v=state）canonical v37.1",
                "data_split": "corpus_v3 流式 eval 前 16 窗（dataset seed 42+9999），mask seed 1042（mixed 0.05/char0.4/span3）",
                "metric": "2-fold one-vs-all 岭回归（λ=1.0）acc，real−garbage；garbage = 状态序列沿 chunk 轴排列后读出",
                "slot_definition": "段内字节位置（as-encoded chunk 格），slot0 = 段首字节；该源仅探 slot0-3",
                "unit": "Δacc（概率点）",
            },
            "B_consumption_profile_slot0": {
                "value": e86["slot_profile"]["real_minus_garbage"]["0"],
                "source": args.e86_json,
                "probe_input_tensor": "k_rows = state_machine_k(write_head_k(index)) 读出行 package.mean(nq=1)，post-realign / pre-align_k，d_pack=1536",
                "measured_object": "b 格手术版 v37ks_b_sm_v372_cloze_tokcenter_20k_ctx4096_20260818，K 通道（k_row_source=state，WriteHead 吃 index 行）",
                "grid": "b（k=state, v=memory 直通）canonical v37.2，手术格",
                "data_split": "corpus_v3 流式 eval 前 16 窗（dataset seed 42+9999），mask seed 1042（mixed 0.05/char0.4/span3）——同窗同 mask；两格前端同冻结（同 init 同 freeze_prefixes）⟹ 同一 chunk 网格",
                "metric": "2-fold one-vs-all 岭回归（λ=1.0）acc，real−garbage；garbage = 读出行沿 chunk 轴排列（≡ 排列状态再读出，逐 chunk 独立）",
                "slot_definition": "段内字节位置（as-encoded chunk 格），slot0 = 段首字节；该源探 slot0..63",
                "unit": "Δacc（概率点）",
            },
        },
        "conversion": "无需换算：两数本来就是同一单位（Δacc real−garbage @ slot0）。数值比 "
        + f"{iface['real_minus_garbage']['0'] / max(e86['slot_profile']['real_minus_garbage']['0'], 1e-9):.2f}× "
        "不是口径系数，是不同张量、不同通道、不同 checkpoint 的实测差。",
        "verdict": "不是同一块张量（c 格 V 通道读出行 vs b 格 K 通道读出行）、不是同一 checkpoint（v371 自然格 vs v372 手术格，"
        "手术已被 M3 证实误伤写值）⟹ 两数无矛盾，且无单位换算关系可求（单位本就相同）。"
        "验收线重锚必须按通道×checkpoint 分别锚定。段尾丢失的具体定位见测量 1 的判词（tail_loss_localization.json）。",
    }
    recon_path = out_dir / "unit_reconciliation.json"
    recon_path.write_text(json.dumps(recon, ensure_ascii=False, indent=2), encoding="utf-8")

    # ------------------------------------------------------------------
    # verdict logic (three suspects) — from the four arm shapes
    # ------------------------------------------------------------------
    sh = {a: profiles[a]["shape"] for a in profiles}

    def _v(a):
        return f"head {sh[a]['head_mean']} tail {sh[a]['tail_mean']} 比 {sh[a]['head_over_tail']}"

    # auto verdict: concentrated := ratio>2 & head>0.05; degenerate := head<0.02
    def _cls(a):
        h, r = sh[a]["head_mean"], sh[a]["head_over_tail"]
        if h is None or h < 0.02:
            return "退化(≈0)"
        return "段首集中" if (r is not None and r > 2) else "平"

    cls = {a: _cls(a) for a in ARM_ORDER}
    if cls["memory_rows"] == "段首集中":
        verdict = "嫌疑人1 summarizer 压缩：memory 行剖面已段首集中，段尾信息在进状态机之前已丢。"
    elif cls["write_values"] == "段首集中":
        verdict = "嫌疑人2（写入形成半）：memory 平而 WriteHead 写值已段首集中，段尾信息在写值成形时丢。"
    elif cls["natural_ridge"] == "段首集中":
        verdict = "嫌疑人2（动力学半）：写值平而 trained 态 ridge 取回剖面段首集中，delta 递推侵蚀段尾。"
    elif cls["natural_vrows"] == "段首集中":
        verdict = "嫌疑人3 接口选择：trained 态内逐 slot 留存均匀（ridge 平）， trained 固定读出剖面段首集中——读出路径位置偏置。"
    else:
        verdict = "未判明：各臂形态不满足判词逻辑任一一枝，需人工读表。"

    lines = [
        "段尾信息丢失定位 + 单位换算核对 — 审计前置测量包（c 格 v37_c_is V 通道，16 窗，E73-A6 口径）",
        f"日期 {report['created']}  设备 {device.type}  排列种子 {PERM_SEED}（六臂共享同一组 per-window 排列）",
        "",
        "锚校验：natural_vrows 臂 slot0-3 real−garbage 复测 vs 护栏二（容差 ±0.01）：",
        f"  {json.dumps(anchor_check)}  -> {'OK' if anchor_ok else '✗ 漂移，先查口径'}",
        "",
        "逐 slot 信息剖面（real−garbage，段内 slot 0..31；六臂同窗同探针同排列）：",
        "  slot | memory | write_v | or_ridge | na_ridge | or_vrows | na_vrows | E86参照b格k",
    ]
    for s in range(min(args.report_slots, max((int(k) for k in profiles["natural_vrows"]["real_minus_garbage"]), default=0) + 1)):
        key = str(s)
        row = f"  {s:>4d} |"
        for a in ARM_ORDER:
            row += f" {profiles[a]['real_minus_garbage'].get(key, float('nan')):+.4f} |" if key in profiles[a]["real_minus_garbage"] else "    -    |"
        row += f" {e86_diff.get(key, float('nan')):+.4f}" if key in e86_diff else "    -"
        lines.append(row)
    lines += [
        "",
        "形态指标（head=slot0-3 均值, tail=slot16-31 均值, 比值=head/tail；分类阈值 比>2且head>0.05）：",
        f"  memory_rows    {_v('memory_rows')}  -> {cls['memory_rows']}",
        f"  write_values   {_v('write_values')}  -> {cls['write_values']}",
        f"  oracle_ridge   {_v('oracle_ridge')}  -> {cls['oracle_ridge']}",
        f"  natural_ridge  {_v('natural_ridge')}  -> {cls['natural_ridge']}",
        f"  oracle_vrows   {_v('oracle_vrows')}  -> {cls['oracle_vrows']}",
        f"  natural_vrows  {_v('natural_vrows')}  -> {cls['natural_vrows']}",
        f"  E86 b格k_rows  head {report['e86_reference_b_grid_natural_k_rows']['shape']['head_mean']} "
        f"tail {report['e86_reference_b_grid_natural_k_rows']['shape']['tail_mean']} "
        f"比 {report['e86_reference_b_grid_natural_k_rows']['shape']['head_over_tail']}",
        "",
        "机制量：",
        f"  key 平均|cos|（键塌缩签名）: {mech_agg['key_cos_mean']}",
        f"  state_norm trained/oracle: {mech_agg['state_norm_trained']} / {mech_agg['state_norm_oracle']}",
        f"  oracle 读出 own-chunk 权重份额 mean: {mech_agg['oracle_own_share_mean']}（均匀键基线 {mech_agg['uniform_share_mean']}）"
        f"  readout q·k 均值 {mech_agg['readout_weight_mean']}",
        f"  ridge 取回 cos(v̂,v) λ={RIDGE_LAM}: oracle {mech_agg['ridge_cos_oracle']} / trained {mech_agg['ridge_cos_trained']}",
        "",
        "判词逻辑：memory 已集中→summarizer 压缩；memory 平+写值集中→写入形成（WriteHead）；",
        "写值平+natural_ridge 集中→递推侵蚀段尾；natural_ridge 平+natural 读出集中→读出路径位置偏置（接口选择）；",
        "oracle+trained 读出臂全零→读出选择失败旁证（键塌缩下 q·k 近似均匀，own-chunk 份额≈1/i）。",
        f"定位判词：{verdict}",
        "",
        "—— 测量 2：单位换算核对（护栏二 +0.47 vs 逐 slot 剖面 +0.126）——",
        "  项            | A 护栏二 slot0                          | B 逐 slot 剖面 slot0",
        f"  数值          | {iface['real_minus_garbage']['0']:+.4f}（slot0；slot1-3: "
        f"{iface['real_minus_garbage']['1']:+.4f}/{iface['real_minus_garbage']['2']:+.4f}/{iface['real_minus_garbage']['3']:+.4f}）"
        f"              | {e86['slot_profile']['real_minus_garbage']['0']:+.4f}",
        "  探针输入张量  | v_rows=realign(q·S).mean(nq) post-realign/pre-decoder_in | k_rows=package.mean(nq) post-realign/pre-align_k",
        "  被测对象      | c 格 v37_c_is（v371）V 通道，WriteHead 吃 memory | b 格手术版 v37ks_b_sm（v372 cloze+tokcenter）K 通道，WriteHead 吃 index",
        "  split        | corpus_v3 eval 前16窗 seed 1042（两边同窗同 mask 同 chunk 网格——前端同冻结）| 同左",
        "  指标/单位     | 2-fold 岭回归 acc，real−garbage，Δacc（概率点）| 同左（单位相同，无换算系数）",
        "  garbage 形态  | 状态沿 chunk 轴排列后读出 ≡ 读出行排列（逐 chunk 独立，严格同构）| 读出行排列",
        "",
        "  对账结论：两数测的不是同一块张量（c 格 V 通道读出行 vs b 格 K 通道读出行）、不是同一个 checkpoint",
        "  （v371 自然格 vs v372 手术格，手术已被 M3 证实误伤写值）——单位本就相同（Δacc real−garbage @ slot0），",
        "  无换算系数可求，两数无矛盾。+0.47 是 c 格 V 接口的档级，+0.126 是 b 格手术版 K 接口的档级，",
        "  验收线重锚必须按通道×checkpoint 分别锚定，不能互用。",
        "",
        f"完整数据: {out_path} ; {recon_path}",
    ]
    summary_path = out_dir / "SUMMARY.txt"
    summary_path.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
