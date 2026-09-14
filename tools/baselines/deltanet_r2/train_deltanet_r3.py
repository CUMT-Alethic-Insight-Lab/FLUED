"""R3 甲臂训练器：R2 DeltaNet-50M + 恒等自读回声（旗标化，默认关）。

任务书：docs/versions/v3.7/FLUED_V3_7_R3_DELTANET_TRANSPLANT_DRAFT_20260914_CN.md
（冻结 v1.0，§1 体制裁定：宿主=R2 母列同款，超参/窗/种子/语料逐项照抄 r2_spec.py，
单变量=所移植之件；§2.1 构造见 r3_spec.py 模块注释）。

旗标纪律（§2.1）：``--echo`` 默认关=不挂任何 hook、不建任何参数，与 R2 母列
逐位不变（同种子同数据序下 loss 轨迹逐位一致为验收，本训练器不含任何其他
改动）；开启才接回声（24 标量门，init 1.0，参数锚 48,152,920 loud-fail）。

Usage:
  python tools/baselines/deltanet_r2/train_deltanet_r3.py \
      --corpus /workspace/corpus/corpus_v3.txt \
      --tokenizer-path /workspace/models/delta_net-1.3B-100B \
      --out-dir outputs/r3_transplant_echo_20260914/smoke500_echo \
      --max-steps 500 --echo
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import torch

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import tools.baselines.deltanet_r2.r2_spec as spec
import tools.baselines.deltanet_r2.r3_spec as r3
from tools.baselines.deltanet_r2.train_deltanet_r2 import (
    EXIT_DIVERGED, save_checkpoint)

SPEC_MODULE = "tools/baselines/deltanet_r2/r3_spec.py"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--corpus", required=True)
    p.add_argument("--tokenizer-path", required=True,
                   help="Mistral 32K tokenizer 目录（R2 互证四文件）")
    p.add_argument("--out-dir", required=True)
    p.add_argument("--echo", action="store_true",
                   help="恒等自读回声旗标（默认关=与 R2 母列逐位不变）")
    p.add_argument("--max-steps", type=int, default=spec.MAX_STEPS)
    p.add_argument("--start-window", type=int, default=0)
    p.add_argument("--seed", type=int, default=spec.TRAIN_SEED)
    p.add_argument("--log-every", type=int, default=spec.LOG_EVERY)
    p.add_argument("--ckpt-every", type=int, default=spec.CKPT_EVERY)
    p.add_argument("--milestones", type=str, default=",".join(map(str, spec.MILESTONE_STEPS)))
    p.add_argument("--resume", action="store_true")
    p.add_argument("--device", default="cuda")
    return p.parse_args()


def build_model(device: str, echo: bool):
    """fla 原生 from_config 实例化；echo=True 才挂回声（r3_spec.attach_echo），
    参数锚 loud-fail 双档（关=48,152,896 与 R2 全等；开=+24=48,152,920）。"""
    import fla  # noqa: F401  # 先于 transformers：注册 fla 模型类
    from fla.models.delta_net import DeltaNetConfig, DeltaNetForCausalLM

    cfg = DeltaNetConfig(**spec.R2_CONFIG)
    model = DeltaNetForCausalLM(cfg)
    echo_keys: list[str] = []
    if echo:
        echo_keys = r3.attach_echo(model, True)
        r3.stamp_echo_config(model.config, num_layers=len(echo_keys))
    n = sum(p.numel() for p in model.parameters())
    want = r3.expected_param_count(echo)
    if n != want:
        raise RuntimeError(
            f"[r3] 参数锚不符（echo={echo}）：实例化 {n:,} != 预注册 {want:,}——停报")
    print(f"[r3] 实例化参数数 = {n:,}（预注册锚一致，echo={echo}，"
          f"回声键 {len(echo_keys)}）", flush=True)
    return model.to(device), echo_keys


def main() -> int:
    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    device = args.device
    torch.manual_seed(args.seed)

    resolved = {
        "probe": "R3 甲臂（恒等自读回声移植）× R2 DeltaNet-50M × corpus_v3 × 20K "
                 "from-scratch（任务书冻结 v1.0 §2.1 主构造）",
        "spec_module": SPEC_MODULE,
        "base_spec_module": "tools/baselines/deltanet_r2/r2_spec.py",
        "echo": bool(args.echo),
        "echo_gate_init": r3.ECHO_GATE_INIT if args.echo else None,
        "echo_num_params": r3.ECHO_NUM_PARAMS if args.echo else 0,
        "expected_param_count": r3.expected_param_count(args.echo),
        "expected_param_count_base": spec.EXPECTED_PARAM_COUNT,
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

    # 分词器（Mistral 32K BPE；R2 互证四文件）
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(args.tokenizer_path, trust_remote_code=True)

    model, echo_keys = build_model(device, args.echo)
    spec.normalize_tied_weights_keys()  # 任何 save_pretrained 前置（tf5.15.1 list 崩溃在案）
    opt = torch.optim.AdamW(model.parameters(), lr=spec.LEARNING_RATE,
                            betas=spec.ADAM_BETAS, eps=spec.ADAM_EPS,
                            weight_decay=spec.WEIGHT_DECAY, fused=(device == "cuda"))
    if args.echo:
        (out_dir / "echo_whitelist.json").write_text(
            json.dumps({"keys": echo_keys, "num_params": len(echo_keys),
                        "gate_init": r3.ECHO_GATE_INIT,
                        "expected_param_count": r3.EXPECTED_PARAM_COUNT_ECHO},
                       ensure_ascii=False, indent=2), encoding="utf-8")

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
            # 权重回填 latest 模型目录（回声列走 r3 strict 白名单重载，坑 8）
            from transformers import AutoModelForCausalLM
            import fla  # noqa: F401
            spec.normalize_tied_weights_keys()
            m2 = AutoModelForCausalLM.from_pretrained(out_dir / "latest")
            if args.echo:
                report = r3.strict_load_echo(model, out_dir / "latest", attach=True)
                print(f"[r3] 回声 strict 重载：{report['n_echo_keys']} 键", flush=True)
            else:
                model.load_state_dict(m2.state_dict(), strict=True)
            del m2
            print(f"[r3] resume 自 step {start_step}", flush=True)
        else:
            print("[r3] --resume 但无 latest/checkpoint，从头训", flush=True)

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
            raise RuntimeError("[r3] 语料窗尽（不应发生于 20K×4096B ≪ 语料体量）")
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
            print(f"[r3] step {step}/{args.max_steps} loss {lv:.3f} ema {loss_ema:.3f} "
                  f"lr {lr:.2e} tok {len(ids)} ({rec['sec_per_step']*1000:.0f}ms/step)",
                  flush=True)
        if step % args.ckpt_every == 0 or step in milestones or step == args.max_steps:
            save_checkpoint(model, tok, opt, step, out_dir, args)
            if args.echo and step == args.max_steps:
                gates = {k: float(v) for k, v in
                         ((k, p.detach()) for k, p in model.named_parameters()
                          if k.split(".")[-1] == r3.ECHO_PARAM_NAME)}
                (out_dir / "echo_gates_final.json").write_text(
                    json.dumps({"step": step, "gates": gates},
                               ensure_ascii=False, indent=2), encoding="utf-8")
            if device == "cuda":
                print(f"[r3] ckpt@{step} peak_mem_alloc "
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
        print(f"[r3] DIVERGED @step {diverged['step']} loss {diverged['loss']}", flush=True)
        return EXIT_DIVERGED
    print(f"[r3] done step {step} ema {loss_ema:.4f} wallclock "
          f"{(time.time()-t0)/60:.1f}min", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
