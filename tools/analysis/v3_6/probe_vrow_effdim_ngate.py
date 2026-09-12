"""容量界稿终审两直测（零训练纯评测，2026-09-12 理论侧点单，agent-208 施工）。

理论背景（任务书原文口径，不许换锚）：模型 KDA 线性注意力把每个 chunk 写成
状态矩阵的一次叠加写入（每头 S∈R^{hk×hv}，4 头，d_v=hv/头）。容量界预言固定
单查询读出 cos ≈ 1/√(有效叠加写入数)。已有实测：d 格 V 通道 cos=0.076
（1/√172.7=0.0761，172.7=S0'' 实测块/窗，非名义 256）；b 格 K 通道
cos=0.1044（靶心 n_eff≈92，1/√92=0.1043）。本探针零训练直测两件事：

  测量1 —— V 行有效维数（参与比，逐头）：收集数百窗写入 KDA 状态的 V 行
    （WriteHead 的 gates["v"]，形状 (B, chunks, H, hv)；d 格抽取点 =
    _slm_store_rows 的 ``gates_v = self.write_head(memory)``（model.py），
    b 格 = ``gates_k = self.write_head_k(index)``），逐头算协方差特征谱，
    报参与比 PR=(Σλ)²/Σλ²、top-1 特征值份额、90%/95% 能量秩。名义 hv 是
    天花板，有效值越低越好（不预设方向）。
  测量2 —— 门控 γ 谱 → n_eff（能量口径）：读码确认 γ=sigmoid(alpha_logit)
    是【静态】逐 (头, K通道) 权重（model.py WriteHead.__init__/_gates_from_k；
    g=log(γ) 进 fla 核逐 chunk cumsum），不输入相关 → 直接从 ckpt 读。窗内
    写入 s 的残余权重 g_s=Π_{u>s} γ_u = γ^(n-1-s)（静态 γ），n_eff=Σ_s g_s²
    = (1-γ^{2n})/(1-γ²)（每通道闭式，γ²→1 时=n）。报 γ 分布
    （mean/median/p5/p95）与 n_eff（窗/通道平均）。

窗流：probe_oracle_write_verdict.build_eval_windows（= 训练终评口径，
StreamingReconstructionDataset seed=seed+9999），mask 同 build_masks
（eval_mask_seed 顺序抽签）——与 0.076/0.1044 的测量件（e120 t0 / e119）
同窗同 mask 口径。

判词留白：本探针只落数，1/√n_eff vs 实测 cos 的对照表进 SUMMARY，
判读归理论侧。

Usage:
  python tools/analysis/v3_6/probe_vrow_effdim_ngate.py --ckpt <run_dir> --device cuda
  CPU 冒烟: py -3.14 -X utf8 tools/analysis/v3_6/probe_vrow_effdim_ngate.py --ckpt <tiny_run> --windows 2 --device cpu
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
    build_eval_windows,
    build_masks,
)
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402
from tools.train.v3_6.train_v36 import build_model  # noqa: E402

DEFAULT_OUT_DIR = "outputs/vrow_ngate_20260912"
# 对照靶（任务书钉死，不在此判读）
COS_TARGETS = {
    "v": {"measured_cos": 0.076, "theory_anchor_chunks": 172.7, "note": "d 格 V 通道 0.076 vs 1/√172.7=0.0761"},
    "k": {"measured_cos": 0.1044, "theory_anchor_chunks": None, "note": "b 格 K 通道 0.1044（靶心 n_eff≈92, 1/√92=0.1043）"},
}


# ---------------------------------------------------------------------------
# 纯数学件（单测覆盖）
# ---------------------------------------------------------------------------


def select_channel(cfg, override: str | None) -> str:
    """读出对象通道：v_row_source=state → V 通道（d 格），否则 k_row_source=
    state → K 通道（b 格）。双 state（d 格两通道都在）默认 v（对照 0.076 钉
    V 通道），--channel 可覆写。两通道皆非 state = 结构性 N/A，响亮报错。"""
    if override not in (None, "v", "k"):
        raise ValueError(f"--channel 非法: {override!r} (auto|v|k)")
    v_state = getattr(cfg, "v_row_source", "memory") == "state"
    k_state = getattr(cfg, "k_row_source", "memory") == "state"
    if override is not None:
        ch = override
    elif v_state:
        ch = "v"
    elif k_state:
        ch = "k"
    else:
        raise ValueError("k/v_row_source 皆非 'state'：无 KDA 状态写入，两测量均 N/A")
    if ch == "v" and not v_state:
        raise ValueError("--channel v 但 v_row_source != 'state'（V 通道无状态机）")
    if ch == "k" and not k_state:
        raise ValueError("--channel k 但 k_row_source != 'state'（K 通道无状态机）")
    return ch


def channel_module(model, channel: str):
    """通道 → 生产 WriteHead（V 通道吃 memory 行，K 通道吃 index 行）。"""
    mod = model.write_head if channel == "v" else model.write_head_k
    if mod is None:
        raise ValueError(f"channel={channel} 的 WriteHead 未创建（格别不符）")
    return mod


def neff_energy(gamma2: torch.Tensor, n: torch.Tensor) -> torch.Tensor:
    """能量口径 n_eff = Σ_{j=0}^{n-1} γ^{2j} = (1-γ^{2n})/(1-γ²)（逐通道）。

    gamma2: (C,) 每通道 γ²；n: 标量或 (W,) 窗块数。返回 (C,) 或 (W, C)。
    γ²→1 的极限 = n（sigmoid 严格 <1，仅数值护栏）。"""
    g2 = gamma2.to(torch.float64)
    n = n.to(torch.float64)
    denom = (1.0 - g2).clamp_min(1e-300)
    safe = (1.0 - g2.unsqueeze(0).pow(n.unsqueeze(-1))) / denom
    near1 = g2 > 1.0 - 1e-12
    if near1.any():
        n_full = n.unsqueeze(-1).expand_as(safe)
        safe = torch.where(near1.expand_as(safe), n_full, safe)
    return safe


def spectrum_stats(evals: torch.Tensor) -> dict:
    """协方差特征谱 → 参与比口径数表。evals: 升序特征值 (d,) float。
    PR=(Σλ)²/Σλ²；top1 份额=λmax/Σλ；rank90/95 = 最小 k 使前 k 大特征值
    能量占比过阈。"""
    ev = evals.to(torch.float64).clamp_min(0.0)
    total = float(ev.sum())
    pr = total * total / float((ev * ev).sum()) if total > 0 else float("nan")
    desc = torch.flip(ev, dims=[0])
    cum = torch.cumsum(desc, dim=0) / total if total > 0 else desc
    rank90 = int((cum < 0.90).sum()) + 1
    rank95 = int((cum < 0.95).sum()) + 1
    return {
        "dim": int(ev.numel()),
        "sum": total,
        "participation_ratio": pr,
        "top1_share": float(desc[0]) / total if total > 0 else float("nan"),
        "rank90_energy": rank90,
        "rank95_energy": rank95,
        "eigenvalues_desc": [float(x) for x in desc],
    }


class SecondMomentAccumulator:
    """流式二阶矩累积器（float64）：cov = M/n - m mᵀ（中心化）与
    second = M/n（非中心化，含 DC 方向——理论干涉用的是原始写值向量）。"""

    def __init__(self, dim: int) -> None:
        self.dim = dim
        self.m = torch.zeros(dim, dtype=torch.float64)
        self.mm = torch.zeros(dim, dim, dtype=torch.float64)
        self.count = 0

    def update(self, x: torch.Tensor) -> None:
        x = x.reshape(-1, self.dim).to(torch.float64)
        self.m += x.sum(dim=0)
        self.mm += x.T @ x
        self.count += x.size(0)

    def covariance(self) -> torch.Tensor:
        assert self.count > 1
        mean = self.m / self.count
        return self.mm / self.count - torch.outer(mean, mean)

    def second_moment(self) -> torch.Tensor:
        assert self.count > 0
        return self.mm / self.count


def writehead_gamma(write_head) -> torch.Tensor:
    """静态衰减门 γ=sigmoid(alpha_logit)（逐 (头, K通道)），(C,) float64。
    静态性依据：model.py WriteHead._gates_from_k —— alpha 只由参数经 sigmoid
    产生、对 batch/chunk 广播，无输入依赖；g=log(γ) 进 fla 核逐 chunk cumsum。
    （先升 float64 再 sigmoid：与生产前向 fp32 口径差 ~1e-8，谱口径取高精度。）"""
    with torch.no_grad():
        return torch.sigmoid(write_head.alpha_logit.detach().to(torch.float64)).reshape(-1)


def gamma_init_reference(heads: int, hk: int, tau_max: float) -> torch.Tensor:
    """WriteHead.__init__ 的 α 初始化谱（同公式复算，float32 与生产同序）：
    tau=exp(linspace(0,1,H·hk)·ln tau_max).clamp(min=1.001)，γ=sigmoid(log(tau−1))。
    用途：对照训后谱，量化「门控被训练动过多少」——静态参数的谱若停在 init
    附近，任何 gate 基 n_eff 都是架构参数化的性质而非训练塑造。"""
    tau = torch.exp(torch.linspace(0.0, 1.0, heads * hk) * torch.log(torch.tensor(tau_max))).clamp(
        min=1.0 + 1e-3
    )
    return torch.sigmoid(torch.log(tau - 1.0)).to(torch.float64)


def gamma_distribution(gamma: torch.Tensor) -> dict:
    g = gamma.to(torch.float64)
    q = torch.quantile(g, torch.tensor([0.05, 0.5, 0.95], dtype=torch.float64))
    return {
        "n_channels": int(g.numel()),
        "mean": float(g.mean()),
        "median": float(q[1]),
        "p5": float(q[0]),
        "p95": float(q[2]),
        "frac_ge_0.99": float((g >= 0.99).float().mean()),
        "frac_ge_0.90": float((g >= 0.90).float().mean()),
        "frac_le_0.10": float((g <= 0.10).float().mean()),
        "min": float(g.min()),
        "max": float(g.max()),
    }


# ---------------------------------------------------------------------------
# 模型装载（resolved_config.json 缺席时回退 latest.pt 内嵌 args——b 格只拉
# latest.pt 的口径；train_v36_s1 存盘 payload={"step","model","args"}）
# ---------------------------------------------------------------------------


def load_run(run_dir: Path, device: torch.device):
    from argparse import Namespace

    cfg_path = run_dir / "resolved_config.json"
    payload = torch.load(run_dir / "latest.pt", map_location=device, weights_only=False)
    if cfg_path.exists():
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        cfg_source = "resolved_config.json"
    else:
        cfg = dict(payload["args"])
        cfg_source = "latest.pt:args"
    cfg["data_manifest"] = ""
    if device.type != "cuda":
        cfg["kda_impl"] = "torch"  # fla 核仅 GPU
    ns = Namespace(**cfg)
    if getattr(ns, "backbone_mode", "") != "slm":
        raise ValueError(f"{run_dir.name}: backbone_mode={ns.backbone_mode!r} != 'slm'")
    if getattr(ns, "recurrence", "kda") != "kda":
        raise ValueError(f"{run_dir.name}: recurrence={ns.recurrence!r} — 两测量口径按 kda 递推钉死")
    model = build_model(ns).to(device)
    model.load_state_dict(payload["model"], strict=True)
    for p in model.parameters():
        p.requires_grad_(False)
    model.eval()
    return model, ns, int(payload.get("step", 0)), cfg_source


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------


@torch.no_grad()
def collect(model, ns, windows: int, device: torch.device, channel: str):
    """跑窗流，抓 (V 行, beta, chunk_mask)。返回逐窗 chunk 数列表 + 累积器。"""
    write_head = channel_module(model, channel)
    hv = int(ns.kda_head_v)
    heads = int(ns.kda_heads)
    cleans = build_eval_windows(ns, windows)
    if getattr(ns, "mask_mode", "mixed") == "mixed" and ns.mask_prob > 0 and s1._BPE_TOKENIZER is None:
        s1._load_bpe_tokenizer(ns.bpe_tokenizer_path)
    masks = build_masks(cleans, ns)
    accs = [SecondMomentAccumulator(hv) for _ in range(heads)]
    acc_pool = SecondMomentAccumulator(heads * hv)
    captured: dict = {}
    handle = write_head.register_forward_hook(lambda _m, _i, out: captured.__setitem__("gates", out))
    chunk_counts: list[int] = []
    betas: list[torch.Tensor] = []
    try:
        for clean, mask in zip(cleans, masks):
            # clean 已是 (1, T)（build_eval_windows 的 loader batch 口径，与
            # e120 t0 同款），不再叠维
            source = clean.to(device).masked_fill(mask.to(device), MASK_ID)
            chunks, memory, index = _front_end(model, source)
            if channel == "v":
                write_head(memory)
            else:
                write_head(index)
            gates = captured["gates"]
            keep = chunks.chunk_mask[0].bool()
            v = gates["v"][0][keep].detach().to("cpu")
            for h in range(heads):
                accs[h].update(v[:, h])
            acc_pool.update(v.reshape(v.size(0), -1))
            betas.append(gates["beta"][0][keep].detach().to("cpu").reshape(-1))
            chunk_counts.append(int(keep.sum()))
    finally:
        handle.remove()
    return accs, acc_pool, chunk_counts, torch.cat(betas)


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    p = argparse.ArgumentParser()
    p.add_argument("--ckpt", required=True, help="run dir (resolved_config.json + latest.pt；后者缺席回退内嵌 args)")
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--windows", type=int, default=320, help="≥300（任务书）")
    p.add_argument("--channel", default="auto", choices=["auto", "v", "k"], help="读出对象通道；d 格默认 v，b 格默认 k")
    p.add_argument("--out-dir", default=DEFAULT_OUT_DIR)
    p.add_argument(
        "--data-path",
        default=None,
        help="覆盖语料路径（默认用 ckpt 配置内的 data_path；远端拉回的基座须指到本地同款语料）",
    )
    args = p.parse_args()
    device = torch.device(
        "cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu"
    )
    if args.windows < 300:
        raise SystemExit(f"--windows={args.windows} < 300：任务书窗数下限，不许静默放行")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    run_dir = Path(args.ckpt)
    t0 = time.time()

    model, ns, step, cfg_source = load_run(run_dir, device)
    if args.data_path:
        ns.data_path = args.data_path
    if not Path(ns.data_path).exists():
        raise SystemExit(f"语料缺席: {ns.data_path}（--data-path 指到本地同款语料）")
    channel = select_channel(model.config, None if args.channel == "auto" else args.channel)
    heads, hv, hk = int(ns.kda_heads), int(ns.kda_head_v), int(ns.kda_head_k)
    write_head = channel_module(model, channel)

    accs, acc_pool, chunk_counts, betas = collect(model, ns, args.windows, device, channel)

    # --- 测量1：V 行参与比（逐头中心化协方差为主口径；非中心化二阶矩为 caveat 列） ---
    per_head = {}
    for h, acc in enumerate(accs):
        evals_c = torch.linalg.eigvalsh(acc.covariance())
        evals_u = torch.linalg.eigvalsh(acc.second_moment())
        per_head[str(h)] = {
            "n_rows": acc.count,
            "cov_centered": spectrum_stats(evals_c),
            "second_moment_raw": spectrum_stats(evals_u),
        }
    evals_pool_c = torch.linalg.eigvalsh(acc_pool.covariance())
    evals_pool_u = torch.linalg.eigvalsh(acc_pool.second_moment())
    pooled = {
        "n_rows": acc_pool.count,
        "cov_centered": spectrum_stats(evals_pool_c),
        "second_moment_raw": spectrum_stats(evals_pool_u),
    }

    # --- 测量2：静态 γ 谱 → n_eff（能量口径） ---
    gamma = writehead_gamma(write_head).cpu()
    gamma_by_head = gamma.reshape(heads, hk)
    gamma_init = gamma_init_reference(heads, hk, float(ns.kda_tau_max)).cpu()
    n_w = torch.tensor(chunk_counts, dtype=torch.float64)
    neff_per_channel_per_window = neff_energy(gamma, n_w)  # (W, C)
    neff_per_channel = neff_per_channel_per_window.mean(dim=0)  # 窗平均
    neff_by_head = neff_per_channel.reshape(heads, hk)
    mean_chunks = float(n_w.mean())
    g2_mean = float((gamma * gamma).mean())
    neff_from_mean_g2 = float(neff_energy(torch.tensor([g2_mean]), n_w.mean().unsqueeze(0)).item())
    n_eff_table = {
        "definition": "n_eff = Σ_{s} g_s², g_s = Π_{u>s} γ_u = γ^(n_w-1-s)（静态 γ，窗终点口径；不含 β 与 delta 擦除）",
        "n_windows": len(chunk_counts),
        "chunks_per_window_mean": mean_chunks,
        "chunks_per_window_min": int(n_w.min()),
        "chunks_per_window_max": int(n_w.max()),
        "chunks_per_window": chunk_counts,
        "per_channel_mean_over_windows": {
            "mean": float(neff_per_channel.mean()),
            "median": float(torch.quantile(neff_per_channel, 0.5)),
            "p5": float(torch.quantile(neff_per_channel, 0.05)),
            "p95": float(torch.quantile(neff_per_channel, 0.95)),
        },
        "per_head_mean": [float(neff_by_head[h].mean()) for h in range(heads)],
        "from_mean_gamma2": neff_from_mean_g2,
        "inv_sqrt": {
            "per_channel_mean": 1.0 / math.sqrt(float(neff_per_channel.mean())),
            "per_channel_median": 1.0 / math.sqrt(float(torch.quantile(neff_per_channel, 0.5))),
            "per_head_mean": [1.0 / math.sqrt(float(v)) for v in neff_by_head.mean(dim=1)],
            "from_mean_gamma2": 1.0 / math.sqrt(neff_from_mean_g2),
            "from_chunks_mean": 1.0 / math.sqrt(mean_chunks),
        },
    }

    target = COS_TARGETS[channel]
    comparison = {
        "channel": channel,
        "channel_semantics": (
            "V 通道状态机（write_head 吃 memory 行；对照 d 格实测 cos=0.076）"
            if channel == "v"
            else "K 通道状态机（write_head_k 吃 index 行；对照 b 格实测 cos=0.1044）"
        ),
        "measured_cos_target": target["measured_cos"],
        "target_note": target["note"],
        "inv_sqrt_neff_variants": n_eff_table["inv_sqrt"],
    }

    report = {
        "probe": "容量界终审两直测：V 行有效维数（参与比）+ 门控 γ 谱 → n_eff（能量口径）",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "checkpoint": {"run": run_dir.name, "step": step, "cfg_source": cfg_source},
        "config_facts": {
            "k_row_source": getattr(ns, "k_row_source", None),
            "v_row_source": getattr(ns, "v_row_source", None),
            "recurrence": getattr(ns, "recurrence", "kda"),
            "kda_impl_effective": getattr(ns, "kda_impl", None),
            "kda_heads": heads,
            "kda_head_k": hk,
            "kda_head_v": hv,
            "kda_tau_max": getattr(ns, "kda_tau_max", None),
            "readout_queries": getattr(ns, "readout_queries", None),
            "seq_len": getattr(ns, "seq_len", None),
            "data_path": getattr(ns, "data_path", None),
            "seed": getattr(ns, "seed", None),
        },
        "gamma_parameterization": {
            "static": True,
            "evidence": "WriteHead.alpha_logit (model.py)：alpha=sigmoid(alpha_logit) 逐 (头,K通道) 静态参数，无输入依赖；g=log(alpha)*keep 进 fla chunk_kda 逐 chunk cumsum",
            "gamma": gamma_distribution(gamma),
            "gamma_per_head_mean": [float(gamma_by_head[h].mean()) for h in range(heads)],
            "gamma_init_reference": {
                "note": (
                    "WriteHead init 谱（同公式复算, kda_tau_max=%.1f）：对照训后谱，量化『门控被训练动过多少』——"
                    "静态参数的谱若停在 init 附近，gate 基 n_eff 是架构参数化的性质而非训练塑造" % float(ns.kda_tau_max)
                ),
                "gamma": gamma_distribution(gamma_init),
                "gamma_per_head_mean": [float(gamma_init.reshape(heads, hk)[h].mean()) for h in range(heads)],
            },
        },
        "beta_write_strength_context": {
            "note": "上下文列（非任务口径）：写入强度 β 分布；n_eff 定义不含 β",
            "mean": float(betas.to(torch.float64).mean()),
            "median": float(betas.to(torch.float64).median()),
            "p5": float(torch.quantile(betas.to(torch.float64), 0.05)),
            "p95": float(torch.quantile(betas.to(torch.float64), 0.95)),
        },
        "measurement1_vrow_participation_ratio": {
            "extraction_point": (
                "gates_v = write_head(memory)['v'] (B, chunks, H, hv)" if channel == "v" else "gates_k = write_head_k(index)['v'] (B, chunks, H, hv)"
            ),
            "n_windows": len(chunk_counts),
            "per_head": per_head,
            "pooled_all_heads": pooled,
            "nominal_ceiling": hv,
        },
        "measurement2_gamma_neff": {
            "gamma_source": "ckpt alpha_logit（静态，直接读）",
            **n_eff_table,
        },
        "comparison": comparison,
        "verdict": "判词留白（理论侧裁）",
        "timing_sec": round(time.time() - t0, 1),
    }
    stem = f"vrow_ngate_{run_dir.name}"
    json_path = out_dir / f"{stem}.json"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    def f3(x):
        return f"{x:.3f}"

    lines = [
        "容量界终审两直测（零训练）—— " + report["probe"],
        f"日期 {report['created']}  设备 {device.type}  checkpoint={run_dir.name} (step {step}, cfg={cfg_source})",
        f"通道 {channel}（{comparison['channel_semantics']}）  窗数 {len(chunk_counts)}  语料 {ns.data_path}",
        "",
        "测量1 —— V 行有效维数（参与比 PR=(Σλ)²/Σλ²，中心化协方差；名义天花板 hv=%d）" % hv,
        "  头 | PR | top1份额 | rank90 | rank95 | 行数",
        "\n".join(
            f"  h{h} | {f3(per_head[str(h)]['cov_centered']['participation_ratio'])} | "
            f"{f3(per_head[str(h)]['cov_centered']['top1_share'])} | "
            f"{per_head[str(h)]['cov_centered']['rank90_energy']} | "
            f"{per_head[str(h)]['cov_centered']['rank95_energy']} | {per_head[str(h)]['n_rows']}"
            for h in range(heads)
        ),
        f"  聚合(H·hv={heads * hv}) | {f3(pooled['cov_centered']['participation_ratio'])} | "
        f"{f3(pooled['cov_centered']['top1_share'])} | {pooled['cov_centered']['rank90_energy']} | "
        f"{pooled['cov_centered']['rank95_energy']} | {pooled['n_rows']}",
        "  非中心化二阶矩（含 DC 方向，caveat 列）：逐头 PR "
        + ", ".join(f"h{h}={f3(per_head[str(h)]['second_moment_raw']['participation_ratio'])}" for h in range(heads))
        + f", 聚合={f3(pooled['second_moment_raw']['participation_ratio'])}",
        "",
        "测量2 —— 门控 γ 谱 → n_eff（能量口径 n_eff=Σ_s g_s², g_s=γ^(n-1-s)，γ 静态逐 (头,K通道)）",
        "  γ 分布: mean={:.4f} median={:.4f} p5={:.4f} p95={:.4f}  (≥0.99 占比 {:.3f}, ≥0.90 占比 {:.3f}, ≤0.10 占比 {:.3f})".format(
            report["gamma_parameterization"]["gamma"]["mean"],
            report["gamma_parameterization"]["gamma"]["median"],
            report["gamma_parameterization"]["gamma"]["p5"],
            report["gamma_parameterization"]["gamma"]["p95"],
            report["gamma_parameterization"]["gamma"]["frac_ge_0.99"],
            report["gamma_parameterization"]["gamma"]["frac_ge_0.90"],
            report["gamma_parameterization"]["gamma"]["frac_le_0.10"],
        ),
        "  γ 逐头均值: " + ", ".join(f"h{h}={f3(v)}" for h, v in enumerate(report["gamma_parameterization"]["gamma_per_head_mean"])),
        "  init 参照谱（同公式复算）: mean={:.4f} median={:.4f} 逐头均值 {}".format(
            report["gamma_parameterization"]["gamma_init_reference"]["gamma"]["mean"],
            report["gamma_parameterization"]["gamma_init_reference"]["gamma"]["median"],
            "[" + ", ".join(f"{v:.3f}" for v in report["gamma_parameterization"]["gamma_init_reference"]["gamma_per_head_mean"]) + "]",
        ),
        "  实测块/窗: mean={:.1f} (min {}, max {})  [eval 流 seed=seed+9999 口径；172.7=训练流实测锚]".format(
            mean_chunks, n_eff_table["chunks_per_window_min"], n_eff_table["chunks_per_window_max"]
        ),
        "  n_eff（窗/通道平均）: mean={:.1f} median={:.1f} p5={:.1f} p95={:.1f}".format(
            n_eff_table["per_channel_mean_over_windows"]["mean"],
            n_eff_table["per_channel_mean_over_windows"]["median"],
            n_eff_table["per_channel_mean_over_windows"]["p5"],
            n_eff_table["per_channel_mean_over_windows"]["p95"],
        ),
        "  n_eff 逐头均值: " + ", ".join(f"h{h}={f3(v)}" for h, v in enumerate(n_eff_table["per_head_mean"])),
        "  n_eff(平均γ²口径)={:.1f}  1/√(实测块/窗)={:.4f}".format(
            neff_from_mean_g2, n_eff_table["inv_sqrt"]["from_chunks_mean"]
        ),
        "",
        "对照表（判词留白，理论侧裁）:",
        "  实测 cos 靶: {:.4f}  ({})".format(target["measured_cos"], target["note"]),
        "  1/√n_eff 变体: 逐通道均值 {:.4f} | 逐通道中位 {:.4f} | 逐头均值 {} | 平均γ²口径 {:.4f}".format(
            n_eff_table["inv_sqrt"]["per_channel_mean"],
            n_eff_table["inv_sqrt"]["per_channel_median"],
            "[" + ", ".join(f"{v:.4f}" for v in n_eff_table["inv_sqrt"]["per_head_mean"]) + "]",
            n_eff_table["inv_sqrt"]["from_mean_gamma2"],
        ),
        "",
        f"汇总: {json_path}",
    ]
    summary_path = out_dir / f"{stem}_SUMMARY.txt"
    summary_path.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
