"""Q18 楔死分层二分复现 (楔死攻坚 2026-08-27; 主会话已排除: 内存物化 (流式
重构只把楔点从 5780 推到 6380 未根治) / 筛子 (sieve-off 照楔) / 环境 (本地
远端同病) / kda 实现 (fla/torch 同病); s1 生产训练器从不犯)。

三级复现臂, 同一数据流 (s1.make_dataloaders, seed 42, 窗规格继承基座 4096B)
同一基座 (Q15 收官 ckpt, q17._q17_load_models 加载; sieve 全程不开):
  L0: 数据循环 + burst 拼接 (无筛子) + 遮蔽 + 基座生产 forward (no_grad)
      ——不训练;
  L1: L0 + 流式双态 q17._q17_stream_encode 双通道 (no_grad 递推 + 带梯度
      readout_query einsum + realign, 链模块解冻但不重初始化) ——dummy
      loss 算出就丢, 不 backward;
  L2: 完整 Q18 步 = 数据循环 + q17._q17_step 全量 (其内部含前端+流式双态+
      backbone/decoder+echo CE; 注意: _q17_step 不含 L0 的生产 forward,
      "L1 +" 按"在流式层之上加训练"读) + backward + Adam (链模块按 Q18 A 臂
      seed42 重初始化 + 解冻, LR 1e-3, warmup 200 + cosine→0 随 1500 步)。
每级 1500 步或楔死即停。

楔死判定 (心跳 + 看门狗线程): 每步开算前写 outputs/_q18_bisect_heartbeat_<level>
(内容 = step + 时间戳); 看门狗线程每 15s 查心跳, >120s 无更新即把当时
faulthandler 全线程堆栈写入 outputs/_q18_bisect_verdict_<level>.txt 并
os._exit(42)。正常收官写 PASS + 步速 + cuda 峰值显存 (训练循环段,
reset_peak_memory_stats 在循环前)。看门狗只罩训练循环段 (setup 段不罩——
历史楔死皆在循环内)。

Usage (串行三级, 一条命令):
  export OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 PYTHONIOENCODING=utf-8
  PY=/c/Users/74090/Miniconda3/envs/soulvlm/python.exe
  $PY -X utf8 tools/debug/q18_wedge_bisect.py --level L0 ; \
  $PY -X utf8 tools/debug/q18_wedge_bisect.py --level L1 ; \
  $PY -X utf8 tools/debug/q18_wedge_bisect.py --level L2
"""

from __future__ import annotations

import argparse
import faulthandler
import json
import os
import sys
import threading
import time
from pathlib import Path

import torch

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from flued.data import MASK_ID, PAD_ID  # noqa: E402
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402
from tools.train.v3_6 import train_q17_oracle_readout as q17  # noqa: E402

BASE_RUN = "checkpoints/v37ks_d_sm_q15_circuit_20k_ctx4096_20260825b"
OUT_DIR = Path("outputs")
SEED = 42


def _start_watchdog(hb_path: Path, verdict_path: Path, level: str, timeout: float):
    """看门狗线程: 心跳 >timeout 无更新 → faulthandler 全线程堆栈落 verdict + os._exit。"""
    stop = threading.Event()

    def _watch():
        while not stop.wait(15.0):
            try:
                stale = time.time() - hb_path.stat().st_mtime
            except FileNotFoundError:
                continue
            if stale > timeout:
                with open(verdict_path, "w", encoding="utf-8") as fh:
                    fh.write(
                        f"WEDGE level={level} heartbeat stale {stale:.0f}s > {timeout:.0f}s "
                        f"@ {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                    )
                    faulthandler.dump_traceback(file=fh)
                os._exit(42)

    t = threading.Thread(target=_watch, daemon=True, name=f"watchdog-{level}")
    t.start()
    return stop


def run_level(level: str, max_steps: int, device: torch.device, timeout: float) -> dict:
    t0 = time.time()
    model, sieve_model, ns, base_step = q17._q17_load_models(Path(BASE_RUN), device)
    del sieve_model  # sieve 不开 (sieve-off 变体照楔已排除, 本复现不载参考模型)
    if device.type == "cuda":
        torch.cuda.empty_cache()
    ns.batch_size = 1
    seed = SEED
    print(f"[bisect {level}] 基座 step={base_step} 加载完成 ({time.time() - t0:.0f}s)", flush=True)

    if s1._BPE_TOKENIZER is None and getattr(ns, "mask_mode", "mixed") == "mixed":
        s1._load_bpe_tokenizer(ns.bpe_tokenizer_path)
    s1._MASK_GENERATOR.manual_seed(seed)
    s1._BURST_GENERATOR.manual_seed(seed + s1._BURST_SEED_OFFSET)
    s1._BURST_SAMPLER = s1.CorpusSampler(ns.data_path)
    s1._BURST_SIEVE_MODEL = None  # sieve 不开
    gen = torch.Generator().manual_seed(seed + 101_077)  # Q18 抽签流同款种子

    opt = None
    sched = None
    trainable = []
    if level in ("L1", "L2"):
        if level == "L2":
            q17._q17_reinit_readout_chain(model, ns, seed)  # Q18 A 臂同款从零 (seed 42)
        trainable = q17._q17_unfreeze_chain(model)  # 读出行带梯度 (L1 建图不反传; L2 全量)
    if level == "L2":
        model.train()
        ns.lr = 1e-3
        opt = s1.build_optimizer(ns, iter(trainable))
        sched = s1._cosine_with_warmup(opt, 200, max_steps)

    train_loader, _eval_loader = s1.make_dataloaders(ns)

    hb_path = OUT_DIR / f"_q18_bisect_heartbeat_{level}"
    verdict_path = OUT_DIR / f"_q18_bisect_verdict_{level}.txt"
    hb_path.write_text(f"setup-done {time.time()}", encoding="utf-8")
    stop = _start_watchdog(hb_path, verdict_path, level, timeout)
    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats()

    step = 0
    nan_skips = 0
    t_loop = time.time()
    try:
        while step < max_steps:
            for batch in train_loader:
                if step >= max_steps:
                    break
                hb_path.write_text(f"{step} {time.time()}", encoding="utf-8")  # 心跳: 步前
                if level == "L2":
                    loss, metrics = q17._q17_step(model, batch[0], ns, device, 1.0, gen)
                    if loss is not None and bool(torch.isfinite(loss)):
                        opt.zero_grad(set_to_none=True)
                        loss.backward()
                        torch.nn.utils.clip_grad_norm_(trainable, ns.grad_clip)
                        opt.step()
                        sched.step()
                    elif loss is not None:
                        nan_skips += 1
                        opt.zero_grad(set_to_none=True)
                else:
                    clean, metas = s1._splice_burst(
                        batch[0], float(getattr(ns, "burst_prob", 1.0)), s1._BURST_GENERATOR,
                        s1._BURST_SAMPLER, s1._BURST_REPEAT_FROZEN, s1._BURST_TAIL_MAX_CHARS,
                        sieve_model=None, stats={"drawn": 0, "spliced": 0, "sieve_measured": 0, "sieve_rejected": 0},
                    )
                    clean = clean.to(device)
                    if getattr(ns, "mask_mode", "mixed") == "mixed":
                        byte_mask = s1.make_mixed_mask(
                            clean.cpu(), ns.mask_prob, char_frac=getattr(ns, "mask_char_frac", 0.4),
                            char_span_max=getattr(ns, "mask_char_span_max", 3),
                            tokenizer=s1._BPE_TOKENIZER, generator=s1._MASK_GENERATOR,
                        ).to(device)
                    else:
                        byte_mask = s1.make_byte_mask(clean.ne(PAD_ID), ns.mask_prob, ns.mask_span_min, ns.mask_span_max)
                    byte_mask = s1._burst_mask_overrides(byte_mask, metas)
                    source = clean.masked_fill(byte_mask, MASK_ID)
                    with torch.no_grad():
                        model(source)  # L0: 基座生产 forward (no_grad)
                    if level == "L1":
                        enc = q17._q17_stream_encode(model, source, 1.0, gen)
                        dummy = float(enc["package_k"].mean() + enc["package_v"].mean())  # 算出就丢
                        del enc, dummy
                step += 1
                print(f"[bisect {level}] step {step} ({time.time() - t_loop:.0f}s loop)", flush=True)
    finally:
        stop.set()
    elapsed = time.time() - t_loop
    verdict = {
        "verdict": "PASS",
        "level": level,
        "steps": step,
        "elapsed_loop_sec": round(elapsed, 1),
        "steps_per_sec": round(step / max(elapsed, 1e-9), 3),
        "nan_skips": nan_skips,
        "cuda_max_mem_gb": round(torch.cuda.max_memory_allocated() / 1e9, 3) if device.type == "cuda" else None,
        "watchdog_timeout_sec": timeout,
        "finished": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    verdict_path.write_text(json.dumps(verdict, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[bisect {level}] PASS {json.dumps(verdict, ensure_ascii=False)}", flush=True)
    return verdict


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    p = argparse.ArgumentParser()
    p.add_argument("--level", required=True, choices=["L0", "L1", "L2"])
    p.add_argument("--max-steps", type=int, default=1500)
    p.add_argument("--device", default="cuda", choices=["auto", "cpu", "cuda"])
    p.add_argument("--timeout", type=float, default=120.0, help="心跳超时 (楔死判定)")
    args = p.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    run_level(args.level, args.max_steps, device, args.timeout)


if __name__ == "__main__":
    main()
