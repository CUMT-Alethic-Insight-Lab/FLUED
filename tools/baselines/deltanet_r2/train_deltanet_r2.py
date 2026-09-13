"""R2 臂训练器：DeltaNet-50M × corpus_v3 × 4096B 窗 × 20K 步 from-scratch。

任务书：docs/versions/v3.7/FLUED_V3_7_R2_DELTANET_IN_OUR_REGIME_20260913_CN.md（冻结 v1.0）。

体制声明（§1 逐项照抄，架构轴是唯一换件）：
- 语料：corpus_v3 单遍顺序窗流（sha256 前 16 = ed4ab97810776ce7），窗 = 4096B
  非重叠顺序窗（与 E122 必要性账仪器窗定义逐字同构 → 同卷对拍成立）；
- 预算：20K 步 @ batch=1 窗（epoch = 20000×4096B / 语料字节 ≈ 0.0034）；
- 架构：fla DeltaNetForCausalLM 原样 from_config（架构件零改造——本训练器
  不含任何架构代码；实例化参数数 ≠ 预注册锚 48,152,896 即 loud fail 停报）。

超参出处（坑 8：显式声明）见 r2_spec.py 模块注释（LR=3e-4 fla 原生默认等）。

Usage:
  python tools/baselines/deltanet_r2/train_deltanet_r2.py \
      --corpus /workspace/corpus/corpus_v3.txt \
      --tokenizer-path /workspace/models/delta_net-1.3B-100B \
      --out-dir outputs/r2_deltanet50m_20260913/smoke500 \
      --max-steps 500
"""

from __future__ import annotations

import argparse
import json
import math
import shutil
import time
from pathlib import Path

import torch

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import tools.baselines.deltanet_r2.r2_spec as spec

EXIT_DIVERGED = 3


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--corpus", required=True)
    p.add_argument("--tokenizer-path", required=True,
                   help="Mistral 32K tokenizer 目录（sha256 互证过的四文件副本）")
    p.add_argument("--out-dir", required=True)
    p.add_argument("--max-steps", type=int, default=spec.MAX_STEPS)
    p.add_argument("--start-window", type=int, default=0)
    p.add_argument("--seed", type=int, default=spec.TRAIN_SEED)
    p.add_argument("--log-every", type=int, default=spec.LOG_EVERY)
    p.add_argument("--ckpt-every", type=int, default=spec.CKPT_EVERY)
    p.add_argument("--milestones", type=str, default=",".join(map(str, spec.MILESTONE_STEPS)))
    p.add_argument("--resume", action="store_true")
    p.add_argument("--device", default="cuda")
    return p.parse_args()


def build_model(device: str):
    """fla 原生 from_config 实例化（架构件零改造），参数锚 loud fail。"""
    import fla  # noqa: F401  # 先于 transformers：注册 fla 模型类
    from fla.models.delta_net import DeltaNetConfig, DeltaNetForCausalLM

    cfg = DeltaNetConfig(**spec.R2_CONFIG)
    model = DeltaNetForCausalLM(cfg)
    n = sum(p.numel() for p in model.parameters())
    if n != spec.EXPECTED_PARAM_COUNT:
        raise RuntimeError(
            f"[r2] 参数锚不符：实例化 {n:,} != 预注册 {spec.EXPECTED_PARAM_COUNT:,}——停报")
    print(f"[r2] 实例化参数数 = {n:,}（预注册锚一致）", flush=True)
    return model.to(device)


def save_checkpoint(model, tok, opt, step: int, out_dir: Path, args):
    """HF 格 save_pretrained（仪器 AutoModelForCausalLM 直接可载）+ 优化器态。"""
    d = out_dir / f"model_step{step}"
    model.save_pretrained(d)
    for f in ("tokenizer.json", "tokenizer.model", "tokenizer_config.json",
              "special_tokens_map.json"):
        src = Path(args.tokenizer_path) / f
        if src.exists():
            shutil.copy2(src, d / f)
    torch.save({"step": step, "optimizer": opt.state_dict(),
                "torch_rng": torch.get_rng_state(),
                "cuda_rng": torch.cuda.get_rng_state_all()}, d / "optimizer.pt")
    latest = out_dir / "latest"
    if latest.exists():
        shutil.rmtree(latest)
    shutil.copytree(d, latest)
    return d


def main() -> int:
    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    device = args.device
    torch.manual_seed(args.seed)

    resolved = {
        "probe": "R2 DeltaNet-50M × corpus_v3 × 20K from-scratch（任务书冻结 v1.0）",
        "spec_module": "tools/baselines/deltanet_r2/r2_spec.py",
        "expected_param_count": spec.EXPECTED_PARAM_COUNT,
        "config": spec.R2_CONFIG,
        "corpus": str(args.corpus),
        "tokenizer_path": str(args.tokenizer_path),
        "out_dir": str(out_dir),
        "max_steps": args.max_steps,
        "start_window": args.start_window,
        "window_bytes": spec.WINDOW_BYTES,
        "max_tokens": spec.MAX_TOKENS,
        "batch": 1,
        "lr": spec.LEARNING_RATE, "warmup_steps": spec.WARMUP_STEPS,
        "lr_min_ratio": spec.LR_MIN_RATIO, "betas": spec.ADAM_BETAS,
        "eps": spec.ADAM_EPS, "weight_decay": spec.WEIGHT_DECAY,
        "grad_clip": spec.GRAD_CLIP, "divergence_line": spec.DIVERGENCE_LINE,
        "train_seed": args.seed, "eval_seed": spec.EVAL_SEED,
        "milestones": args.milestones,
        "device": device,
        "torch": torch.__version__,
        "gpu": torch.cuda.get_device_name(0) if device == "cuda" else "cpu",
    }
    (out_dir / "resolved_config.json").write_text(
        json.dumps(resolved, ensure_ascii=False, indent=2), encoding="utf-8")

    # 分词器（Mistral 32K BPE；sha256 互证在施工回执）
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(args.tokenizer_path, trust_remote_code=True)

    model = build_model(device)
    opt = torch.optim.AdamW(model.parameters(), lr=spec.LEARNING_RATE,
                            betas=spec.ADAM_BETAS, eps=spec.ADAM_EPS,
                            weight_decay=spec.WEIGHT_DECAY, fused=(device == "cuda"))

    start_step = 0
    if args.resume:
        latest = out_dir / "latest" / "optimizer.pt"
        if latest.exists():
            st = torch.load(latest, map_location="cpu", weights_only=False)
            start_step = st["step"]
            opt.load_state_dict(st["optimizer"])
            torch.set_rng_state(st["torch_rng"])
            if device == "cuda":
                torch.cuda.set_rng_state_all(st["cuda_rng"])
            # 权重回填 latest 模型目录
            from transformers import AutoModelForCausalLM
            import fla  # noqa: F401
            import fla.models.delta_net.modeling_delta_net as _fla_dn_mod
            if isinstance(_fla_dn_mod.DeltaNetForCausalLM.__dict__.get("_tied_weights_keys"), list):
                # tf5.15.1 from_pretrained 对 v4 list 崩溃（484c636 同款规范化，tying 语义不变）
                _fla_dn_mod.DeltaNetForCausalLM._tied_weights_keys = {
                    "lm_head.weight": "model.embeddings.weight"}
            m2 = AutoModelForCausalLM.from_pretrained(out_dir / "latest")
            model.load_state_dict(m2.state_dict(), strict=True)
            del m2
            print(f"[r2] resume 自 step {start_step}", flush=True)
        else:
            print("[r2] --resume 但无 latest/checkpoint，从头训", flush=True)

    milestones = sorted({int(x) for x in args.milestones.split(",") if x.strip()})
    log_path = out_dir / "train_log.jsonl"
    t0 = time.time()
    step = start_step
    loss_ema = None
    diverged = None
    skipped_partial = 0

    window_iter = spec.iter_byte_windows(args.corpus, spec.WINDOW_BYTES, args.start_window)
    log_f = log_path.open("a", encoding="utf-8")

    model.train()
    while step < args.max_steps:
        try:
            _w, raw = next(window_iter)
        except StopIteration:
            raise RuntimeError("[r2] 语料窗尽（不应发生于 20K×4096B ≪ 语料体量）")
        ids = list(tok(spec.window_text(raw))["input_ids"])[:spec.MAX_TOKENS]
        if len(ids) < 2:
            skipped_partial += 1
            continue
        x = torch.tensor([ids[:-1]], dtype=torch.long, device=device)
        y = torch.tensor([ids[1:]], dtype=torch.long, device=device)

        lr = spec.lr_at(step)
        for g in opt.param_groups:
            g["lr"] = lr

        with torch.autocast("cuda", dtype=torch.bfloat16, enabled=(device == "cuda")):
            out = model(input_ids=x)
        logits = out.logits.float()  # 坑 2 对偶：fp32 计算 CE
        loss = torch.nn.functional.cross_entropy(
            logits.reshape(-1, logits.size(-1)), y.reshape(-1))

        if spec.is_diverged(loss.item()):
            diverged = {"step": step, "loss": loss.item()}
            break

        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), spec.GRAD_CLIP)
        opt.step()
        step += 1

        lv = loss.item()
        loss_ema = lv if loss_ema is None else 0.95 * loss_ema + 0.05 * lv
        if step % args.log_every == 0 or step == args.max_steps:
            rec = {"step": step, "loss": lv, "loss_ema": round(loss_ema, 4),
                   "lr": lr, "tokens_in_window": len(ids),
                   "sec_per_step": round((time.time() - t0) / max(1, step - start_step), 4),
                   "elapsed_sec": round(time.time() - t0, 1)}
            log_f.write(json.dumps(rec) + "\n")
            log_f.flush()
            print(f"[r2] step {step}/{args.max_steps} loss {lv:.3f} ema {loss_ema:.3f} "
                  f"lr {lr:.2e} tok {len(ids)} ({rec['sec_per_step']*1000:.0f}ms/step)",
                  flush=True)
        if step % args.ckpt_every == 0 or step in milestones or step == args.max_steps:
            save_checkpoint(model, tok, opt, step, out_dir, args)
            if device == "cuda":
                print(f"[r2] ckpt@{step} peak_mem_alloc "
                      f"{torch.cuda.max_memory_allocated()/2**20:.0f}MiB reserved "
                      f"{torch.cuda.max_memory_reserved()/2**20:.0f}MiB", flush=True)

    log_f.close()
    summary = {
        **resolved,
        "finished_step": step,
        "loss_ema_final": round(loss_ema, 4) if loss_ema is not None else None,
        "skipped_partial_windows": skipped_partial,
        "diverged": diverged,
        "wallclock_sec": round(time.time() - t0, 1),
        "peak_mem_alloc_mib": (torch.cuda.max_memory_allocated() / 2**20) if device == "cuda" else None,
        "peak_mem_reserved_mib": (torch.cuda.max_memory_reserved() / 2**20) if device == "cuda" else None,
    }
    (out_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    if diverged is not None:
        (out_dir / "DIVERGED.json").write_text(
            json.dumps(diverged), encoding="utf-8")
        print(f"[r2] DIVERGED @step {diverged['step']} loss {diverged['loss']}", flush=True)
        return EXIT_DIVERGED
    print(f"[r2] done step {step} ema {loss_ema:.4f} wallclock "
          f"{(time.time()-t0)/60:.1f}min", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
