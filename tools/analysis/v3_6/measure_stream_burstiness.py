"""离线突发性仪表 (任务书 FLUED_V3_7_LR_SCALE_2X2_20260826_CN §0 检查 2,
2026-08-26 冻结): 重放训练数据流 (flued/data.py:130-194
StreamingReconstructionDataset, random.Random(seed) Mersenne twister 跨平台
稳定, num_workers=0 单流), 逐里程碑 ±500 步带 + 全局等距基线计算
**窗内突发性密度** (窗内重复 >=12 字节子串的字节覆盖率, 与
tools/train/v3_6/train_v36_s1.py::_window_burstiness 同一口径), 并与
induction 轨迹 (outputs/induction_scale2x_sweep/*/induction_score.json
trained max ratio) 叠读: 对照表 + Pearson/Spearman 相关 + 判词描述行
(不落终判词, 归主会话会合).

重放必须逐逻辑复演抽取循环的三段 (否则偏移序列错位):
  1. 行首吸附 (mm.rfind(b"\\n", search_from, start + 1));
  2. UTF-8 边界微调 (最多 4 次, 跳过 0x80-0xBF 续字节);
  3. 短读 continue (消耗抽取但不产窗).

用法:
  python tools/analysis/v3_6/measure_stream_burstiness.py \
      --run-dir checkpoints/v37ks_a_im_v373_scale2x_20k_ctx4096_20260826 \
      --induction-dir outputs/induction_scale2x_sweep \
      --out-dir outputs/stream_burstiness_20260826
"""

import argparse
import json
import math
import mmap
import os
import random
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# 同一 12-gram 覆盖口径 —— 直接从 trainer 导入, 杜绝两处分叉
from tools.train.v3_6.train_v36_s1 import _window_burstiness  # noqa: E402


def replay_offsets(file_path: str, seq_len: int, n_windows: int, seed: int,
                   samples_per_worker: int) -> list[int]:
    """逐逻辑复演 StreamingReconstructionDataset.__iter__ (flued/data.py:158-194)
    的抽取序列, 返回前 n_windows 个产窗的语料偏移 (0-based 窗序号 -> start).

    三段逐行对应: 行首吸附 / UTF-8 边界微调 (<=4 次) / 短读 continue
    (消耗一次 rng.randint 但不产窗). num_workers=0 单流 -> worker_seed=seed.
    """
    file_size = os.path.getsize(file_path)
    rng = random.Random(seed)
    offsets: list[int] = []
    with open(file_path, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        max_start = max(0, file_size - seq_len - 2)
        for _ in range(samples_per_worker):
            if len(offsets) >= n_windows:
                break
            start = rng.randint(0, max_start)
            # 段 1: 行首吸附 (与 data.py:176-179 逐行同构)
            search_from = max(0, start - 256)
            line_start = mm.rfind(b"\n", search_from, start + 1)
            if line_start >= 0 and line_start + 1 <= max_start:
                start = line_start + 1
            # 段 2: UTF-8 边界微调 (data.py:180-186)
            for _adjust in range(4):
                if start >= max_start:
                    break
                b0 = mm[start]
                if not (0x80 <= b0 <= 0xBF):
                    break
                start += 1
            # 段 3: 短读 continue (data.py:187-189): raw = mm[start:start+seq_len+1],
            # len(raw) = min(seq_len+1, file_size-start); 不足则消耗抽取不产窗
            if file_size - start < seq_len + 1:
                continue
            offsets.append(start)
    if len(offsets) < n_windows:
        raise SystemExit(
            f"replay exhausted: draws={samples_per_worker} produced {len(offsets)} "
            f"windows < requested {n_windows}"
        )
    return offsets


def _ranks(xs: list[float]) -> list[float]:
    """平均秩 (ties 取均值), Spearman 用."""
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    ranks = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        r = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = r
        i = j + 1
    return ranks


def _pearson(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    if n < 2:
        return float("nan")
    mx = sum(xs) / n
    my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx == 0.0 or syy == 0.0:
        return float("nan")
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return sxy / math.sqrt(sxx * syy)


def _spearman(xs: list[float], ys: list[float]) -> float:
    return _pearson(_ranks(xs), _ranks(ys))


def _induction_step(dirname: str, max_steps: int) -> int | None:
    """m03000 -> 3000; latest -> max_steps."""
    if dirname == "latest":
        return max_steps
    if dirname.startswith("m") and dirname[1:].isdigit():
        return int(dirname[1:])
    return None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run-dir", required=True, help="训练 run 目录 (读 resolved_config.json)")
    ap.add_argument("--induction-dir", default="outputs/induction_scale2x_sweep",
                    help="induction sweep 目录 (*/induction_score.json)")
    ap.add_argument("--out-dir", default="outputs/stream_burstiness_20260826")
    ap.add_argument("--band", type=int, default=500, help="里程碑前后 ±band 步带")
    ap.add_argument("--baseline-n", type=int, default=500, help="全局等距基线窗数")
    ap.add_argument("--milestones", default="",
                    help="逗号分隔里程碑步; 默认 = induction 目录里有的全部里程碑")
    args = ap.parse_args()

    run_dir = Path(args.run_dir)
    cfg = json.loads((run_dir / "resolved_config.json").read_text(encoding="utf-8"))
    seed = int(cfg["seed"])
    seq_len = int(cfg["seq_len"])
    data_path = cfg["data_path"]
    max_steps = int(cfg["max_steps"])
    batch_size = int(cfg.get("batch_size", 1))
    samples_per_worker = int(cfg.get("stream_samples_per_worker", 50000))
    num_workers = int(cfg.get("num_workers", 0))
    if num_workers != 0:
        raise SystemExit(f"replay only valid for num_workers=0 single stream (got {num_workers})")
    if not data_path:
        raise SystemExit("resolved_config data_path empty (manifest 流不在本仪表复演口径内)")

    # induction 轨迹: dir -> (step, trained max ratio)
    ind_dir = Path(args.induction_dir)
    ind_by_step: dict[int, float] = {}
    for sub in sorted(ind_dir.iterdir()):
        js = sub / "induction_score.json"
        if not js.exists():
            continue
        step = _induction_step(sub.name, max_steps)
        if step is None:
            continue
        d = json.loads(js.read_text(encoding="utf-8"))
        ind_by_step[step] = float(d["summary"]["trained"]["max"])
    if not ind_by_step:
        raise SystemExit(f"no induction_score.json under {ind_dir}")

    if args.milestones:
        milestones = sorted(int(x) for x in args.milestones.split(","))
    else:
        milestones = sorted(ind_by_step)

    # 需要的步集合: 里程碑带 + 全局等距基线
    band = int(args.band)
    bands: dict[int, tuple[int, int]] = {}
    need_steps: set[int] = set()
    for m in milestones:
        lo, hi = max(1, m - band), min(max_steps, m + band)
        bands[m] = (lo, hi)
        need_steps.update(range(lo, hi + 1))
    base_n = int(args.baseline_n)
    base_steps = sorted({
        min(max_steps, max(1, round(1 + i * (max_steps - 1) / max(base_n - 1, 1))))
        for i in range(base_n)
    })
    need_steps.update(base_steps)

    n_windows = max_steps * batch_size
    print(f"[burst] replay: seed={seed} seq_len={seq_len} steps={max_steps} "
          f"batch={batch_size} windows={n_windows} data={data_path}", flush=True)
    offsets = replay_offsets(data_path, seq_len, n_windows, seed, samples_per_worker)
    print(f"[burst] replayed {len(offsets)} window offsets; "
          f"fetching bytes for {len(need_steps)} steps", flush=True)

    # 步 -> 窗内突发性密度 (step s 消费窗序号 (s-1)*batch_size .. s*batch_size-1,
    # 批内取均值 —— canonical 臂 batch_size=1)
    file_size = os.path.getsize(data_path)
    burst_by_step: dict[int, float] = {}
    with open(data_path, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        for s in sorted(need_steps):
            vals = []
            for k in range((s - 1) * batch_size, s * batch_size):
                st = offsets[k]
                vals.append(_window_burstiness(bytes(mm[st:st + seq_len])))
            burst_by_step[s] = sum(vals) / len(vals)

    base_vals = [burst_by_step[s] for s in base_steps]
    baseline_mean = sum(base_vals) / len(base_vals)
    baseline_sd = math.sqrt(
        sum((v - baseline_mean) ** 2 for v in base_vals) / max(len(base_vals) - 1, 1)
    )

    rows = []
    for m in milestones:
        lo, hi = bands[m]
        vals = [burst_by_step[s] for s in range(lo, hi + 1)]
        mean = sum(vals) / len(vals)
        rows.append({
            "step": m,
            "band": [lo, hi],
            "n_windows": len(vals),
            "burstiness_mean": mean,
            "burstiness_min": min(vals),
            "burstiness_max": max(vals),
            "z_vs_baseline": (mean - baseline_mean) / baseline_sd if baseline_sd > 0 else float("nan"),
            "induction_trained_max": ind_by_step.get(m),
        })

    paired = [r for r in rows if r["induction_trained_max"] is not None]
    xs = [r["burstiness_mean"] for r in paired]
    ys = [r["induction_trained_max"] for r in paired]
    pearson_r = _pearson(xs, ys)
    spearman_rho = _spearman(xs, ys)

    # 判词描述行 (描述读数, 不落终判词 —— 归主会话会合): 任务书 §0 检查 2
    # 口径: 破线点对应数据热点 -> 瞬态是数据喂养的; 不相关 -> 数据运气排除.
    first = rows[0] if rows else None
    if first is not None and not math.isnan(first["z_vs_baseline"]):
        hotspot = abs(first["z_vs_baseline"]) >= 2.0
        desc = (
            f"读数描述: 首里程碑 step={first['step']} 带均值 {first['burstiness_mean']:.4f} "
            f"vs 全局基线 {baseline_mean:.4f} (z={first['z_vs_baseline']:+.2f}) -> "
            f"{'破线点带突发性偏离基线 (候选热点形态)' if hotspot else '破线点带突发性与基线无显著偏离'}; "
            f"逐里程碑 Pearson r={pearson_r:+.3f} / Spearman rho={spearman_rho:+.3f} (n={len(paired)}) -> "
            f"{'|r|>=0.5 候选相关, 热点对应=数据喂养形态待裁定' if abs(pearson_r) >= 0.5 else '|r|<0.5 候选不相关, 数据运气排除待裁定'}; "
            f"终判词归主会话会合."
        )
    else:
        desc = "读数描述: 样本不足, 无法形成描述; 终判词归主会话会合."

    out = {
        "meter": "stream_burstiness (任务书 FLUED_V3_7_LR_SCALE_2X2_20260826_CN §0 检查 2)",
        "created": __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "run_dir": str(run_dir),
        "replay": {
            "seed": seed, "seq_len": seq_len, "data_path": data_path,
            "file_size": file_size, "max_steps": max_steps, "batch_size": batch_size,
            "n_windows": len(offsets), "gram": 12,
        },
        "baseline": {"n": len(base_vals), "mean": baseline_mean, "sd": baseline_sd},
        "milestones": rows,
        "correlation": {
            "n": len(paired), "pearson_r": pearson_r, "spearman_rho": spearman_rho,
        },
        "verdict_description": desc,
    }
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "stream_burstiness.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "stream burstiness vs induction (任务书 §0 检查 2; 描述行, 终判归主会话)",
        f"run={run_dir.name} seed={seed} seq_len={seq_len} steps={max_steps} band=±{band}",
        f"baseline: n={len(base_vals)} mean={baseline_mean:.4f} sd={baseline_sd:.4f}",
        "",
        f"{'step':>6} {'band':>11} {'burst':>7} {'z':>6} {'ind_max':>8}",
    ]
    for r in rows:
        lo, hi = r["band"]
        ind = r["induction_trained_max"]
        lines.append(
            f"{r['step']:>6} {f'{lo}-{hi}':>11} {r['burstiness_mean']:>7.4f} "
            f"{r['z_vs_baseline']:>+6.2f} {ind if ind is not None else float('nan'):>8.4f}"
        )
    lines += [
        "",
        f"Pearson r={pearson_r:+.4f}  Spearman rho={spearman_rho:+.4f}  (n={len(paired)})",
        desc,
    ]
    summary = "\n".join(lines) + "\n"
    (out_dir / "SUMMARY.txt").write_text(summary, encoding="utf-8")
    print(summary, flush=True)
    print(f"[burst] wrote {out_dir / 'stream_burstiness.json'} and SUMMARY.txt", flush=True)


if __name__ == "__main__":
    main()
