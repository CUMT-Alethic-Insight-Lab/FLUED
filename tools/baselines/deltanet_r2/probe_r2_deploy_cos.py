"""R2 仪表③ companion：部署终态隐态 → 目标 token 嵌入的方向余弦（参考读数）。

地位声明（坑 9 / §6 空置声明纪律）：任务书 §4 仪表③「部署查询方向余弦」的
在册仪器族（probe_fixed_query_cos_perhead / probe_e120_t0）是我们架构专用件
（slot_query × 解混通道），DeltaNet-50M 无部署查询件可测 → **本臂无此件**。
本脚本不冒充该仪器，只按 **②闭式读出仪器同款 cos 公式**（cos_rows：模型内部
向量 vs 目标 token 输入嵌入，fp32、无 autocast、同窗流同种子谱系）作用于
**部署终态隐态**（lm_head 实际消费的 hidden_states[-1]），产出参考读数：
- real：cos(h_t, E[ids[t+1]])（下一 token 语义）逐监督位均值；
- ctrl：同窗内目标置换（各向同性对照，对应 b/d 格锚 0.1044/0.07 的「各向同性」
  读法在该模型上的对应物）；uplift = real − ctrl。
判读权在主会话；本脚本输出不进预注册判读表。

Usage:
  python tools/baselines/deltanet_r2/probe_r2_deploy_cos.py \
      --model-path <ckpt_dir> --corpus /workspace/corpus/corpus_v3.txt \
      --n-windows 250 --seed 424242 --out-dir outputs/.../closing/deploy_cos
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
from pathlib import Path

import torch
import torch.nn.functional as F

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from tools.analysis.cross_arch import probe_e122_deltanet_book as e122  # 装载/窗口径单源复用

import tools.baselines.deltanet_r2.r2_spec as spec


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--model-path", required=True)
    p.add_argument("--corpus", required=True)
    p.add_argument("--n-windows", type=int, default=250)
    p.add_argument("--start-window", type=int, default=0)
    p.add_argument("--seed", type=int, default=spec.EVAL_SEED)
    p.add_argument("--out-dir", required=True)
    args = p.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    t0 = time.time()

    model, tok, fingerprint = e122.load_model_and_tokenizer(args.model_path, device)
    emb = model.get_input_embeddings().weight.detach().float()  # [V, d]

    rng = random.Random(args.seed)
    per_win_real: list[float] = []
    per_win_ctrl: list[float] = []
    n_pos = 0
    with open(args.corpus, "rb") as f:
        for wi in range(args.n_windows):
            w_abs = args.start_window + wi
            f.seek(w_abs * spec.WINDOW_BYTES)
            raw = f.read(spec.WINDOW_BYTES)
            if len(raw) < spec.WINDOW_BYTES:
                break
            ids = list(tok(spec.window_text(raw))["input_ids"])[:spec.MAX_TOKENS]
            x = torch.tensor([ids], dtype=torch.long, device=device)
            with torch.no_grad():
                out = model(x, output_hidden_states=True)
            h = out.hidden_states[-1][0].detach().float()      # [L, d]（部署终态）
            tgt = torch.tensor(ids[1:], dtype=torch.long, device=device)
            e_tgt = emb[tgt]                                    # [L-1, d]
            cos = F.cosine_similarity(h[:-1], e_tgt, dim=-1)    # [L-1]
            perm = torch.tensor(rng.sample(range(len(ids) - 1), len(ids) - 1),
                                dtype=torch.long, device=device)
            cos_ctrl = F.cosine_similarity(h[:-1], e_tgt[perm], dim=-1)
            per_win_real.append(cos.mean().item())
            per_win_ctrl.append(cos_ctrl.mean().item())
            n_pos += cos.numel()
            if (wi + 1) % 50 == 0:
                print(f"[r2-dc] {wi+1}/{args.n_windows} 窗 ({time.time()-t0:.0f}s)",
                      flush=True)

    def agg(v: list[float]) -> dict:
        sv = sorted(v)
        return {"mean": sum(v) / len(v), "p50": sv[len(sv) // 2],
                "min": sv[0], "max": sv[-1], "n_windows": len(v)}

    summary = {
        "probe": "R2 仪表③ companion：部署终态隐态→目标嵌入 cos（参考读数，非预注册）",
        "status_note": "仪表③在册仪器族为我架构专用（slot_query×解混通道），DeltaNet 无部署查询件"
                       "→ 本臂无此件；本读数=②族同公式作用于部署终态，判读权在主会话",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "model_fingerprint": fingerprint,
        "hardware_note": "同机同 env 内成立",
        "params": {"n_windows": args.n_windows, "seed": args.seed,
                   "window_bytes": spec.WINDOW_BYTES, "max_tokens": spec.MAX_TOKENS,
                   "n_positions": n_pos},
        "real": agg(per_win_real),
        "ctrl_within_window_perm": agg(per_win_ctrl),
        "uplift_real_minus_ctrl": sum(per_win_real) / len(per_win_real)
                                  - sum(per_win_ctrl) / len(per_win_ctrl),
        "anchor_note": "任务书对照锚=我们 b 格 0.1044 / d 格 0.07（我们架构的固定查询件读数，"
                       "跨架构只比方向不比绝对值）",
        "timing_sec": round(time.time() - t0, 1),
    }
    (out_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
