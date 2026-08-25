"""Q16 相一断点定位三站探针链（任务书 §1，2026-08-25 冻结，零训练分钟级）。

三对象（同管线同任务形态，Q15 burst 管束：CorpusSampler 现采 R=3 逐字重复 +
末 2-4 CJK 字符遮蔽 + store_block 压缩区剔除，同一管束同一批窗口，n=96，
种子固定）：
  q15  ：主测件（--ckpt-q15，d 格，奖励掰弯过）；
  e103 ：对照件甲（--ckpt-e103，b 格 retrieval 对象，与主测件差两变量
         （格+奖励），只作松约束参照 -- 跨格混杂标注入册）；
  init ：对照件乙零训练本底（Q15 resolved_config 同种子新建 + canonical
         底座前端，probe_induction_score.load_init 口径）——"从未形成"
         地板线。

四站张量（no_grad，need_attn=True 前向，捕获槽 last_block1_ov/last_block1_h）：
  A1 = 每 echo 字节位置注意力 top-1 store 行（跨头跨行 argmax）的原始
       v_rows 行向量（E88 同口径："聚中的行里有没有货"）；
  A2 = last_block1_ov 的 echo chunk 行（pre-o_proj 加权值混合，实际流下去
       的货）；A1 有货而 A2 缺货 = 混合稀释断；A1 缺货 = 写入断；
  B  = last_block1_h 的 echo chunk 行（block-1 完成后隐藏态，传送带）；
  C  = (backbone_out+pos) 的 echo chunk 行（decoder 入口，出口闸）。

探法（复用岭回归 real−garbage 口径）：目标 = 答案字节（257 类 PAD-offset，
按答案字节索引对齐 ≤12 截断；off-grid echo 字节不计）; 闭式 one-vs-all
岭回归 2-fold（偶奇折）+ majority 基线 + 置换 garbage（固定种子），指标 =
real−garbage 增量；分层（机械规则）按答案首字节 chunk 内 slot 分带
head=[0,8)/mid=[8,18)/tail=[18,∞)（对齐 E88 死亡区起点 slot18；段尾组在
探 A 的死亡是先验已知 E95，判读落在段首/段中组）；逐带报增量均值±95% CI
（逐条目配对 real−garbage）。

判死口径（§1 预注册）实现为纯函数 _verdict_gap，只输出描述行——终判词
归主会话。输出 outputs/q16_stations_20260825/：三对象各自 JSON（四站×三带
矩阵 + 逐条目）+ SUMMARY.txt 全矩阵。

Usage:
  python tools/analysis/v3_6/probe_breakpoint_stations.py --device cuda
  CPU 抽查: py -3.14 -X utf8 tools/analysis/v3_6/probe_breakpoint_stations.py --device cpu --max-items 4
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

from flued.data import BYTE_OFFSET, MASK_ID, PAD_ID  # noqa: E402
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402
from tools.analysis.v3_6.probe_oracle_write_verdict import (  # noqa: E402
    build_eval_windows,
    load_model,
)
from tools.analysis.v3_6.probe_induction_score import load_init  # noqa: E402

CKPT_Q15 = "checkpoints/v37ks_d_sm_q15_circuit_20k_ctx4096_20260825b"
CKPT_E103 = "checkpoints/v37ks_b_sm_retrieval_cjk_ex3_A_20k_ctx4096_20260822"
OUT_DIR = "outputs/q16_stations_20260825"
SPLICE_SEED = 20260825
RIDGE_LAM = 1e-2  # 闭式岭回归 λ（仪表内部口径，冻结于本探针）
GARBAGE_SEED = 20260825
BANDS = ("head", "mid", "tail")
STATIONS = ("A1", "A2", "B", "C")
N_CLASSES = 257  # PAD-offset byte vocab


def _band_of_slot(slot: int) -> str:
    """分层机械规则（施工修订 4）: 答案首字节 chunk 内绝对 slot 分带
    head=[0,8) / mid=[8,18) / tail=[18,∞)."""
    if slot < 8:
        return "head"
    if slot < 18:
        return "mid"
    return "tail"


def _verdict_gap(up: float, down: float) -> str:
    """判死口径（§1 预注册, 纯函数, 只出描述行不落终判词）: 站间落差 =
    (上游−下游)/上游 >50% 且下游增量 <0.02（噪声带）→ 断点定位于该两站
    之间; 防双零假落差（施工修订 5）: 上游增量 <0.05 禁算比值, 两端皆零按
    '断在该站或上游'处理."""
    if up < 0.05:
        return f"上游增量 {up:.4f}<0.05: 禁算比值（防双零假落差）——断在该站或上游"
    drop = (up - down) / up
    if drop > 0.5 and down < 0.02:
        return f"落差 {drop:.1%}>50% 且后站 {down:.4f}<0.02 → 断点定位于该两站之间"
    return f"落差 {drop:.1%}（后站 {down:.4f}）——不满足判死口径"


def _ridge_2fold_hits(X: torch.Tensor, y: torch.Tensor, lam: float = RIDGE_LAM, garbage_seed: int = GARBAGE_SEED):
    """闭式 one-vs-all 岭回归 2-fold（偶/奇折互换）: 返回 (hit_real,
    hit_garbage, hit_majority) 三个 (N,) bool 张量（逐样本命中, 调用侧按
    条目分组聚合）. garbage = 固定种子标签置换; majority = 训练折众数类.
    样本 <4 返回 None（条目太少的带不进矩阵）."""
    n = X.size(0)
    if n < 4:
        return None
    X = X.float().cpu()
    y = y.long().cpu()
    perm = torch.randperm(n, generator=torch.Generator().manual_seed(garbage_seed))
    y_g = y[perm]
    hit_real = torch.zeros(n, dtype=torch.bool)
    hit_garbage = torch.zeros(n, dtype=torch.bool)
    hit_majority = torch.zeros(n, dtype=torch.bool)
    idx = torch.arange(n)
    for fold in (0, 1):
        te = idx % 2 == fold
        tr = ~te
        Xtr, Xte, ytr, yte = X[tr], X[te], y[tr], y[te]
        d = Xtr.size(1)
        Y = torch.zeros(Xtr.size(0), N_CLASSES)
        Y[torch.arange(Xtr.size(0)), ytr] = 1.0
        W = torch.linalg.solve(Xtr.T @ Xtr + lam * torch.eye(d), Xtr.T @ Y)
        hit_real[te] = (Xte @ W).argmax(dim=-1) == yte
        Yg = torch.zeros(Xtr.size(0), N_CLASSES)
        Yg[torch.arange(Xtr.size(0)), y_g[tr]] = 1.0
        Wg = torch.linalg.solve(Xtr.T @ Xtr + lam * torch.eye(d), Xtr.T @ Yg)
        hit_garbage[te] = (Xte @ Wg).argmax(dim=-1) == yte
        maj = torch.bincount(ytr, minlength=N_CLASSES).argmax()
        hit_majority[te] = maj == yte
    return hit_real, hit_garbage, hit_majority


def _mean_ci(vals: list[float]) -> tuple[float, float]:
    """均值 ± 95% CI（正态近似 1.96·sd/√n, n>1 样本标准差）."""
    n = len(vals)
    if not n:
        return 0.0, 0.0
    mean = sum(vals) / n
    sd = (sum((v - mean) ** 2 for v in vals) / (n - 1)) ** 0.5 if n > 1 else 0.0
    return mean, 1.96 * sd / (n ** 0.5)


@torch.no_grad()
def _stations_for_item(model, ns, ids: torch.Tensor, meta: dict, device):
    """One burst item, one need_attn=True forward（store_block 剔除经
    burst_metas_q15 同开）→ 四站逐 echo 字节特征. ids = 拼接行有效前缀
    （剥 PAD 尾, 同 probe_burst_route_q15 的宽度纪律）. Returns dict or
    None（echo 全部 off-grid）."""
    ids = ids[ids.ne(PAD_ID)]
    ids_b = ids.unsqueeze(0).to(device)
    byte_mask = torch.zeros_like(ids_b, dtype=torch.bool)
    elo, ehi = meta["echo_span"]
    byte_mask[0, elo:ehi] = True  # 遮蔽段尾（管束形态: 只遮答案, 无常规掩码 -- 纯存在性测量）
    source = ids_b.masked_fill(byte_mask, MASK_ID)
    out = s1.s1_forward(model, source, ns, burst_metas_q15=[meta], need_attn=True)
    chunks = out["chunks"]
    attn = model.backbone.last_block1_attn  # (1, H, C, C) float32
    ov = model.backbone.last_block1_ov  # (1, C, d) pre-o_proj
    h1 = model.backbone.last_block1_h  # (1, C, d) post block-1
    pos = model.chunk_pos.weight.unsqueeze(0)[:, : chunks.chunk_mask.size(1)]
    gate = out["backbone_out"] + pos  # (1, C, d) decoder 入口
    v_rows = out["v_rows"]  # (1, C, d_pack|d_mem) 原始 V 源行
    feats = {st: [] for st in STATIONS}
    targets = []
    slots = []
    n_chunks = attn.size(2)
    for k, t in enumerate(range(elo, min(ehi, elo + 12))):  # ≤12 截断
        qc = int(chunks.chunk_ids[0, t])
        sc = int(chunks.offsets[0, t])
        if qc < 0 or sc < 0:
            continue  # off-grid echo 字节不计
        # A1: 跨头跨行 top-1 store 行的原始 v_rows 行向量
        flat = attn[0, :, qc, :].reshape(-1)  # (H*C,)
        j_star = int(flat.argmax()) % n_chunks
        feats["A1"].append(v_rows[0, j_star].float().cpu())
        feats["A2"].append(ov[0, qc].float().cpu())
        feats["B"].append(h1[0, qc].float().cpu())
        feats["C"].append(gate[0, qc].float().cpu())
        targets.append(int(ids[t]) )  # PAD-offset byte id = 答案字节目标
        slots.append(sc)
    if not targets:
        return None
    return {"feats": feats, "targets": targets, "slots": slots,
            "band": _band_of_slot(slots[0]) if slots else None}


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    p = argparse.ArgumentParser()
    p.add_argument("--ckpt-q15", default=CKPT_Q15)
    p.add_argument("--ckpt-e103", default=CKPT_E103)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--max-items", type=int, default=96)
    p.add_argument("--out-dir", default=OUT_DIR)
    args = p.parse_args()
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    # 三对象: 主测件 / 对照件甲 (跨格混杂标注) / 对照件乙 (零训练本底)
    model_q15, ns, step_q15 = load_model(Path(args.ckpt_q15), device)
    model_e103, ns_e103, step_e103 = load_model(Path(args.ckpt_e103), device)
    model_init = load_init(device, ns)  # Q15 同配置同种子新建 + 底座前端
    if s1._BPE_TOKENIZER is None:
        s1._load_bpe_tokenizer(ns.bpe_tokenizer_path)
    objects = [
        ("q15", model_q15, ns, step_q15),
        ("e103", model_e103, ns_e103, step_e103),
        ("init", model_init, ns, 0),
    ]
    print(f"[q16] objects loaded ({time.time() - t0:.0f}s)", flush=True)

    # 管束: 三对象同一批窗口同一批 splice（种子固定）
    sampler = s1.CorpusSampler(ns.data_path)
    windows = build_eval_windows(ns, args.max_items * 2)
    gen = torch.Generator().manual_seed(SPLICE_SEED)
    harness = []  # (ids_row0, meta, window_idx)
    for wi, clean in enumerate(windows):
        if len(harness) >= args.max_items:
            break
        spliced, metas = s1._splice_burst(
            clean, 1.0, gen, sampler, s1._BURST_REPEAT_FROZEN, s1._BURST_TAIL_MAX_CHARS
        )
        m = metas[0]
        if m is None:
            continue
        harness.append((spliced[0], m, wi))
    print(f"[q16] harness: {len(harness)} items ({time.time() - t0:.0f}s)", flush=True)

    per_object = {}
    for name, model, ns_obj, step in objects:
        records = []  # 逐条目: 四站特征 + 目标 + slot + band
        for ids, m, wi in harness:
            r = _stations_for_item(model, ns_obj, ids, m, device)
            if r is None:
                continue
            r["window"] = wi
            r["answer"] = m["answer_b"].decode("utf-8", errors="replace")
            r["echo_span"] = list(m["echo_span"])
            r["first_slot"] = r["slots"][0]
            records.append(r)
        # 逐 (站, 带) 聚合: 岭回归 real/garbage/majority + 逐条目配对 Δ 均值±CI
        matrix = {}
        per_item_out = []
        for st in STATIONS:
            for band in BANDS:
                rows = [r for r in records if r["band"] == band]
                xs, ys, owners = [], [], []
                for ri, r in enumerate(rows):
                    for k in range(len(r["targets"])):
                        xs.append(r["feats"][st][k])
                        ys.append(r["targets"][k])
                        owners.append(ri)
                if not xs:
                    matrix[f"{st}/{band}"] = None
                    continue
                X = torch.stack(xs)
                y = torch.tensor(ys)
                got = _ridge_2fold_hits(X, y)
                if got is None:
                    matrix[f"{st}/{band}"] = None
                    continue
                hit_r, hit_g, hit_m = got
                # 逐条目配对: item 内命中均值, real−garbage 差, 跨条目均值±CI
                deltas = []
                seen = set()
                for ri in owners:
                    if ri in seen:
                        continue
                    seen.add(ri)
                    sel = torch.tensor([o == ri for o in owners])
                    if int(sel.sum()) < 1:
                        continue
                    deltas.append(
                        float(hit_r[sel].float().mean()) - float(hit_g[sel].float().mean())
                    )
                dmean, dci = _mean_ci(deltas)
                matrix[f"{st}/{band}"] = {
                    "n_items": len(seen),
                    "n_samples": len(ys),
                    "real": round(float(hit_r.float().mean()), 4),
                    "garbage": round(float(hit_g.float().mean()), 4),
                    "majority": round(float(hit_m.float().mean()), 4),
                    "delta": round(dmean, 4),
                    "ci95": round(dci, 4),
                }
        for r in records:
            per_item_out.append(
                {k: v for k, v in r.items() if k != "feats"}
            )
        per_object[name] = {
            "checkpoint_step": step,
            "n_items": len(records),
            "matrix": matrix,
            "items": per_item_out,
        }
        (out_dir / f"{name}.json").write_text(
            json.dumps(per_object[name], ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"[q16] {name}: {len(records)} items probed ({time.time() - t0:.0f}s)", flush=True)

    # SUMMARY: 三对象 × 四站 × 三带 real−garbage 增量全矩阵 + 判死口径描述行
    lines = [
        "Q16 相一断点定位: 三对象 × 四站 × 三带 real−garbage 增量全矩阵",
        f"日期 {time.strftime('%Y-%m-%d %H:%M:%S')}  设备 {device.type}  管束 n={len(harness)}",
        "（段尾带 tail 在探 A 的死亡是先验已知 E95；判读落在 head/mid 带；",
        "  e103 为跨格对照, 混杂两变量, 只作松约束参照；判词归主会话）",
        "",
    ]
    for name, _, _, _ in objects:
        mo = per_object[name]
        lines.append(f"== {name} (step {mo['checkpoint_step']}, n_items={mo['n_items']}) ==")
        lines.append("站/带 | n | real | garbage | majority | Δ=real−garbage ± CI95")
        for st in STATIONS:
            for band in BANDS:
                cell = mo["matrix"].get(f"{st}/{band}")
                if cell is None:
                    lines.append(f"{st}/{band}: — (样本不足)")
                    continue
                lines.append(
                    f"{st}/{band}: n={cell['n_items']} real={cell['real']:.4f} "
                    f"garbage={cell['garbage']:.4f} majority={cell['majority']:.4f} "
                    f"Δ={cell['delta']:.4f}±{cell['ci95']:.4f}"
                )
        # 判死口径描述行（相邻站, head/mid 带; 不落终判词）
        lines.append("判死口径描述行（纯函数 _verdict_gap, 终判词归主会话）:")
        for band in ("head", "mid"):
            for a, b in (("A1", "A2"), ("A2", "B"), ("B", "C")):
                ca, cb = mo["matrix"].get(f"{a}/{band}"), mo["matrix"].get(f"{b}/{band}")
                if ca is None or cb is None:
                    continue
                lines.append(f"  {band} {a}->{b}: {_verdict_gap(ca['delta'], cb['delta'])}")
        lines.append("")
    (out_dir / "SUMMARY.txt").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
