"""OOD 门测量（招募臂预注册 OOD 判定标准可操作化，2026-08-22，零训练）。

E98 有效性门未过（任务理解层失败）后的规定动作：给模型 K ∈ {0, 4, 8} 条
in-context 完整示例（同任务形式、答案可见），再测查询实例——判定任务
形式对该模型是否可读：

  门（预注册）：答案格式合规率 ≥90% 且内容准确率超盲猜先验一个预注册边际。
  过不了这门，任何"模型没学会"的读数不许归因于记忆机制（任务形式不可读，
  须重设计任务形式而非判 K 通道死刑）。

文档构造（同窗 bytes，无剔除、无 store_block——测的是形式可读性，不是
状态路由）：K 条示例 `\\n前文'<F_i 中 W_i→___>'空格处是什么？\\n答案是：<W_i>`
（答案可见）+ 查询 `\\n前文'<F 中 W→___>'空格处是什么？\\n答案是：<W>`（echo
在窗尾，编码时遮蔽，逐槽预测计分）。F/F_i 均取自 corpus_v3 eval 流，W 为
CJK 小片段（_cjk_candidates 同款）。盲猜先验臂：查询来源段全程遮蔽。

格式合规（可操作化）：echo 预测非退化（非单字节重复循环）且为合法 UTF-8。
计分：byte_acc + 归一化 exact（cloze 同 schema）。n=48/K 档。

Usage:
  python tools/analysis/v3_6/probe_ood_gate.py --device cuda --run-dir checkpoints/v37ks_b_sm_retrieval_cjk_20k_ctx4096_20260822
  CPU 冒烟: py -3.14 -X utf8 tools/analysis/v3_6/probe_ood_gate.py --device cpu --max-items 4 --levels 0,4
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
from tools.analysis.v3_6.probe_oracle_write_verdict import build_eval_windows, load_model  # noqa: E402

DEFAULT_RUN = "checkpoints/v37ks_b_sm_retrieval_cjk_20k_ctx4096_20260822"
OUT_DIR = "outputs/ood_gate_20260822"
SPLICE_SEED = 20260822
Q_PRE = "\n前文'".encode("utf-8")
Q_POST = "'空格处是什么？".encode("utf-8")
E_PRE = "\n答案是：".encode("utf-8")


def _pick_fragment(raw: bytes, gen: torch.Generator):
    """Draw a 32-64B UTF-8-snapped fragment + a CJK answer segment inside it."""
    n = len(raw)
    if n < 40:
        return None
    frag_len = int(torch.randint(32, min(64, n) + 1, (1,), generator=gen))
    start = int(torch.randint(0, n - frag_len + 1, (1,), generator=gen))
    while start < n and (raw[start] & 0xC0) == 0x80:
        start += 1
    end = min(start + frag_len, n)
    while end > start and end < n and (raw[end] & 0xC0) == 0x80:
        end -= 1
    frag = raw[start:end]
    cands = s1._cjk_candidates(frag)
    if not cands:
        return None
    a_lo, a_hi = cands[int(torch.randint(len(cands), (1,), generator=gen))]
    return frag, (a_lo, a_hi)


def build_doc(raw: bytes, k: int, gen: torch.Generator, mask_source: bool):
    """K visible examples + one masked-echo query. Returns (ids_tail_masked,
    echo_lo, answer) or None."""
    picks = []
    for _ in range(k + 1):
        p = _pick_fragment(raw, gen)
        if p is None:
            return None
        picks.append(p)
    doc = b""
    for frag, (a_lo, a_hi) in picks[:k]:
        doc += Q_PRE + frag[:a_lo] + b"___" + frag[a_hi:] + Q_POST + E_PRE + frag[a_lo:a_hi]
    frag, (a_lo, a_hi) = picks[k]
    answer = frag[a_lo:a_hi]
    shown = frag if not mask_source else (frag[:a_lo] + frag[a_hi:])
    doc += Q_PRE + shown[:a_lo] + b"___" + shown[a_hi:] + Q_POST + E_PRE + answer
    echo_lo = len(doc) - len(answer)
    return doc, echo_lo, answer


@torch.no_grad()
def score_doc(model, doc: bytes, echo_lo: int, answer: bytes, device):
    ids = torch.tensor([[b + 1 for b in doc]], dtype=torch.long, device=device)
    n = ids.size(1)
    max_c = model.config.max_chunks
    if n > 4096:
        return None
    mask = torch.zeros_like(ids, dtype=torch.bool)
    mask[0, echo_lo:] = True  # echo masked at encoding
    source = ids.masked_fill(mask, MASK_ID)
    out = model(source)
    chunks = out.chunks
    # echo byte positions -> (chunk, slot) via chunk_ids/offsets
    t = torch.arange(echo_lo, n, device=device)
    j = chunks.chunk_ids[0, t]
    s = chunks.offsets[0, t]
    ok = j.ge(0) & s.ge(0)
    if not bool(ok.all()):
        return None
    pred = out.logits_backbone.argmax(dim=-1)
    hits = pred[0, j, s].cpu() == torch.tensor([b + 1 for b in answer])
    tgt_utf8_ok = True
    try:
        pred_bytes = bytes(int(x) - 1 for x in pred[0, j, s].cpu().tolist())
        pred_bytes.decode("utf-8")
    except (UnicodeDecodeError, ValueError):
        tgt_utf8_ok = False
    degenerate = bool((pred[0, j, s].cpu() == pred[0, j, s].cpu()[0]).all()) if int(j.numel()) > 1 else False
    return {
        "byte_acc": float(hits.float().mean()),
        "exact": bool(hits.all()),
        "format_ok": tgt_utf8_ok and not degenerate,
        "echo_lo": echo_lo,
        "doc_len": len(doc),
    }


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    p = argparse.ArgumentParser()
    p.add_argument("--run-dir", default=DEFAULT_RUN)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--max-items", type=int, default=48)
    p.add_argument("--levels", default="0,4,8")
    p.add_argument("--out-dir", default=OUT_DIR)
    args = p.parse_args()
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    model, ns, step = load_model(Path(args.run_dir), device)
    windows = build_eval_windows(ns, args.max_items * 2)
    levels = [int(x) for x in args.levels.split(",")]
    print(f"[ood] model={Path(args.run_dir).name} step={step} levels={levels} ({time.time() - t0:.0f}s)", flush=True)

    gen = torch.Generator().manual_seed(SPLICE_SEED)
    results = {k: [] for k in levels}
    prior = []
    wi = 0
    while any(len(v) < args.max_items for v in results.values()) and wi < len(windows):
        raw = bytes(int(x) - 1 for x in windows[wi][0].tolist() if int(x) > 0)
        wi += 1
        built = {}
        for k in levels:
            d = build_doc(raw, k, gen, mask_source=False)
            if d is None:
                break
            built[k] = d
        else:
            d0 = build_doc(raw, 0, gen, mask_source=True)
            for k, (doc, echo_lo, answer) in built.items():
                r = score_doc(model, doc, echo_lo, answer, device)
                if r is not None:
                    results[k].append(r)
            if d0 is not None:
                r = score_doc(model, d0[0], d0[1], d0[2], device)
                if r is not None:
                    prior.append(r)
        if wi % 16 == 0:
            print(f"[ood] windows {wi}, items={ {k: len(v) for k, v in results.items()} } ({time.time() - t0:.0f}s)", flush=True)

    def agg(rows, key):
        return round(sum(r[key] for r in rows) / max(len(rows), 1), 4) if rows else None

    summary = {}
    for k in levels:
        rows = results[k]
        summary[k] = {
            "n": len(rows),
            "byte_acc": agg(rows, "byte_acc"),
            "exact": agg(rows, "exact"),
            "format_ok_rate": agg(rows, "format_ok"),
        }
    prior_acc = agg(prior, "byte_acc")
    # 门（预注册）：格式合规率 ≥90% 且内容准确率超盲猜先验一个预注册边际（0.10）
    MARGIN = 0.10
    best_k = max(levels, key=lambda k: (summary[k]["byte_acc"] or 0.0))
    gate_ok = (
        summary[best_k]["format_ok_rate"] is not None
        and summary[best_k]["format_ok_rate"] >= 0.90
        and prior_acc is not None
        and (summary[best_k]["byte_acc"] - prior_acc) >= MARGIN
    )
    verdict = (
        f"OOD 门{'过' if gate_ok else '未过'}：最佳示例档 K={best_k} byte_acc={summary[best_k]['byte_acc']} "
        f"vs 盲猜先验 {prior_acc}（边际线 {MARGIN}），格式合规率 {summary[best_k]['format_ok_rate']}（线 0.90）。"
        + ("任务形式可读——训练失败归因于可学习性而非形式；可议任务形态继续。"
           if gate_ok else
           "任务形式对该模型不可读——任何'没学会'的读数不许归因记忆机制，须重设计任务形式。")
    )

    report = {
        "probe": "OOD 门测量（in-context 示例可读性，招募臂预注册 OOD 判定标准）",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "checkpoint": {"run": Path(args.run_dir).name, "step": step},
        "levels": summary,
        "per_item": {str(k): v for k, v in results.items()},
        "blind_prior_byte_acc": prior_acc,
        "gate": {"margin": MARGIN, "format_line": 0.90, "ok": gate_ok},
        "verdict": verdict,
        "timing_sec": round(time.time() - t0, 1),
    }
    out_path = out_dir / "ood_gate.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "OOD 门测量（in-context 示例可读性）",
        f"日期 {report['created']}  设备 {device.type}  checkpoint={Path(args.run_dir).name}",
        "",
        f"盲猜先验（来源遮蔽）byte_acc: {prior_acc}",
    ]
    for k in levels:
        s = summary[k]
        lines.append(f"K={k}: n={s['n']} byte_acc={s['byte_acc']} exact={s['exact']} format_ok={s['format_ok_rate']}")
    lines += ["", f"判词：{verdict}", "", f"完整数据: {out_path}"]
    (out_dir / "SUMMARY.txt").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
