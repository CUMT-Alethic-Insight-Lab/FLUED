"""S39 全局二分根节点实验：oracle 写入判决（eval-only 零训练，2026-08-18，
swarm 报告裁定）。判定 E-a（c 格 v=state 内容过状态机即崩盘：eval
direct_acc 0.2972 / direct_ppl 39.95，对照 a 格直读锚 0.7923 / 2.14）的
根因落在哪一层。

被测件：checkpoints/v37_c_is_v371_20k_ctx4096_20260817（c 格：k=index,
v=state；V 通道 = write_head(memory) -> KDA delta 递推 -> 固定 query 读出 ->
realign -> decoder_in -> decoder，direct 任务在累积 as-encoded 网格上：
row i 还原 chunks 0..i，consensus §2 粗粒度格口径）。

臂矩阵（2x2 + 两个对照，全部走模型自己的 decode 链，只换状态/读出）：
  A1 trained 状态 + trained 读出（q·S -> realign）——eval 路径复现
     （锚：0.2972/39.95；amp+fla 口径差异由 A1-amp 对照与 A1/A0 复现度量）。
  A2 oracle 状态 + trained 读出——S_i = Σ_{j≤i} k_j v_jᵀ（无衰减、无 delta
     擦除的累计叠加；按模型逐段读出语义对齐，读出点在吃完 chunk i 之后），
     键值来自 c 格自己训好的 WriteHead。
  A3 trained 状态 + ridge 读出——对每段 i、每头：V̂ = (K Kᵀ + λI)⁻¹ K S_i
     （K = chunks 0..i 的已知键），取回本段 v̂_i（H 头拼接）-> realign ->
     decoder_in -> decoder；λ ∈ {1e-4, 1e-2, 1}。
  A4 oracle 状态 + ridge 读出（2x2 的非对角元，隔离"内容在不在"与
     "读出会不会取"）。
  A5 写入直通对照——v̂_i = v_i（不聚状态、不读出，WriteHead 写值直接进
     realign）：检验 v→realign→decoder_in→decoder 链本身能否解码写值向量
     （ridge 族的 domain 阳性对照）。
  A6 闭式字节探针（诊断，非臂）——one-vs-all 岭回归从 v_i（写值，1024）与
     m_i（memory 行，512，上限对照）线性预测该段 slot 0-3 的字节 id
     （2-fold）。封堵 A4/A5 叶节的域偏移漏洞：v-probe≈majority 基线 ⟹ 写
     值本身不含字节内容；v-probe≈m-probe ⟹ 内容在、是解码链读不出。
  A0 a 格锚（v37_a_im，v=memory 直读）在同 16 窗上复现 direct 锚与逐行曲线。

判决逻辑（哪臂恢复/仍崩导出什么结论；恢复 = 收敛到 a-c 差距的 ≥50%）：
  - A4 恢复、A3 崩（ridge cos 低）⟹ 写入形成、读出可用，**delta 递推侵蚀
    状态**是祸首（动力学问题）。
  - A3 恢复 ⟹ 信息在 trained 状态里、trained 读出（固定 q）没取出来——
    **读出侧问题**（若 A2 不恢复而 A3 恢复，进一步钉死为固定-query 读出
    结构病）。
  - A2/A4 皆崩但 oracle 态 ridge cos(v̂,v)≈1 且 A5（写值直通）恢复 ⟹ 状态
    里代数上有内容、realign/decoder 链用不了 ⟹ **读出结构病**。
  - A4/A5 皆崩 ⟹ 看 A6：v-probe≈majority ⟹ 写值向量本身不含可解码内容，
    **写入侧从未形成**（H1 坐实）；v-probe≈m-probe ⟹ 内容在写值里、是
    realign/decoder 链读不出原始写值（读出结构病的域偏移形态）。
  口径注记：ridge/oracle 读出与 trained 读出共享 realign（读出投影仅指
  固定 query 那一级；keep realign 保持 decoder_in 输入分布在家族内），
  A5 是该选择的域对照。

机制测量（§4）：oracle/ridge 臂逐行字节恢复率曲线（own / recalled 槽位，
10 分位桶，对照 A0 锚曲线）、ridge 取回 cos(v̂,v)（trained/oracle 态）、
终态 SVD 谱有效秩（participation ratio + top-k 能量）、键集中度
（mean |cos(k_i,k_j)|，键塌缩签名）、写值范数/beta/alpha 分布、state_norm、
A6 闭式字节探针。

网格口径注记（实跑发现，判读必读）：a 锚的 direct 是 fine 本段格，c 格的
direct 是累积 as-encoded 格（consensus §2 粗粒度格：row i 还原 chunks
0..i，masked 字节以 MASK_ID 为 target 追加在 row i 尾部）——两个锚的
direct_acc/ppl 绝对值不同形同。同形通道质量对照用 own-slot acc；recalled
槽位（忆回 masked 内容）单独报（as-encoded 视图 target=MASK_ID，另有
clean 视图 acc_recalled_clean）。E-a 的表观崩盘 = own 槽小跌 + recalled
槽全灭 × 网格成分变化，读数分解见 SUMMARY.txt。

纪律：checkpoint 只读硬冻结；零训练（ridge 为闭式代数，非参数训练）；
fp32 主口径（A1-amp 为 bf16 对照）；eval 窗口与 mask 复用训练终评口径
（StreamingReconstructionDataset seed=42+9999 的前 16 窗；_MASK_GENERATOR
重播种 1042 顺序抽签，cloze 关）。

Usage:
  python tools/analysis/v3_6/probe_oracle_write_verdict.py --device cuda
  CPU 冒烟: python tools/analysis/v3_6/probe_oracle_write_verdict.py --device cpu --max-windows 2
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from argparse import Namespace
from pathlib import Path

import torch
import torch.nn.functional as F

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from flued.data import MASK_ID  # noqa: E402
from tools.train.v3_3.train_v33 import StreamingReconstructionDataset  # noqa: E402
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402
from tools.train.v3_6.train_v36 import build_model  # noqa: E402

C_RUN = "checkpoints/v37_c_is_v371_20k_ctx4096_20260817"
A_RUN = "checkpoints/v37_a_im_v371_20k_ctx4096_20260817"


# ---------------------------------------------------------------------------
# model loading (keeps data_path — the eval windows come from the corpus)
# ---------------------------------------------------------------------------


def load_model(run_dir: Path, device: torch.device):
    cfg = json.loads((run_dir / "resolved_config.json").read_text(encoding="utf-8"))
    cfg["data_manifest"] = ""
    if device.type != "cuda":
        cfg["kda_impl"] = "torch"  # fla kernels are GPU-only
    ns = Namespace(**cfg)
    if getattr(ns, "backbone_mode", "") != "slm":
        raise ValueError(f"{run_dir.name}: backbone_mode={ns.backbone_mode!r} != 'slm'")
    if getattr(ns, "recurrence", "kda") != "kda":
        raise ValueError(f"{run_dir.name}: recurrence={ns.recurrence!r} — this probe mirrors the kda update math only")
    if s1._BPE_TOKENIZER is None and getattr(ns, "mask_mode", "mixed") == "mixed" and ns.mask_prob > 0:
        s1._load_bpe_tokenizer(ns.bpe_tokenizer_path)
    model = build_model(ns).to(device)
    payload = torch.load(run_dir / "latest.pt", map_location=device, weights_only=False)
    model.load_state_dict(payload["model"], strict=True)
    for p in model.parameters():  # hard-freeze: no autograd graph anywhere in the pipeline
        p.requires_grad_(False)
    model.eval()
    return model, ns, int(payload.get("step", 0))


# ---------------------------------------------------------------------------
# eval windows + masks: same protocol as the trainer's final evaluate()
# ---------------------------------------------------------------------------


def build_eval_windows(ns, count: int) -> list[torch.Tensor]:
    ds = StreamingReconstructionDataset(
        file_path=ns.data_path,
        seq_len=ns.seq_len,
        samples_per_worker=max(ns.batch_size * ns.max_eval_batches, 512),
        seed=ns.seed + 9999,
    )
    loader = torch.utils.data.DataLoader(ds, batch_size=ns.batch_size, shuffle=False, num_workers=0)
    out = []
    for i, batch in enumerate(loader):
        if i >= count:
            break
        out.append(batch[0])
    return out


def build_masks(cleans: list[torch.Tensor], ns) -> list[torch.Tensor]:
    """evaluate()'s exact mask discipline: one reseed, then per-window draws in
    batch order (cloze off on this checkpoint -> no other consumers)."""
    torch.manual_seed(ns.eval_mask_seed)
    s1._MASK_GENERATOR.manual_seed(ns.eval_mask_seed)
    return [
        s1.make_mixed_mask(
            c,
            ns.mask_prob,
            char_frac=getattr(ns, "mask_char_frac", 0.4),
            char_span_max=getattr(ns, "mask_char_span_max", 3),
            tokenizer=s1._BPE_TOKENIZER,
            generator=s1._MASK_GENERATOR,
        )
        for c in cleans
    ]


# ---------------------------------------------------------------------------
# state construction + readout arms (fp32 reference implementations)
# ---------------------------------------------------------------------------


@torch.no_grad()
def _front_end(model, source: torch.Tensor):
    """_slm_forward's encoder half: masked source -> chunks -> (memory, index)."""
    byte_states, confidence, valid, _ = model._encode(source)
    hard_cut, utf8_cont, _ = model._cuts(source, confidence, valid)
    chunks = model.chunk_builder(byte_states, valid, hard_cut, confidence)
    chunks = model.bridge(chunks, byte_states, confidence, valid, utf8_cont)
    memory, index = model.summarizer.forward_with_index(chunks.span_embeddings, chunks.token_mask)
    return chunks, memory, index


@torch.no_grad()
def trained_states(sm, gates: dict, n_real: int) -> torch.Tensor:
    """Per-chunk KDA states S_i (after consuming chunk i), fp32, mirroring
    KDAStateMachine._forward_torch's update math (kda recurrence; padded rows
    are identity steps, so stopping at n_real is exact). Returns
    (B, n, H, hk, hv)."""
    k, v, alpha, beta = gates["k"], gates["v"], gates["alpha"], gates["beta"]
    bsz, _C, H, hk = k.shape
    hv = v.size(-1)
    kf, vf, bf = k.float(), v.float(), beta.float()
    a = alpha[0].float().unsqueeze(-1)  # (1, H, hk, 1) per-channel decay
    S = k.new_zeros(bsz, H, hk, hv, dtype=torch.float32)
    out = []
    for i in range(n_real):
        ki, vi, bi = kf[:, i], vf[:, i], bf[:, i]
        S = a * S
        kTs = torch.einsum("bhk,bhkv->bhv", ki, S)
        S = S - bi.view(bsz, H, 1, 1) * ki.unsqueeze(-1) * kTs.unsqueeze(-2)
        S = S + bi.view(bsz, H, 1, 1) * ki.unsqueeze(-1) * vi.unsqueeze(-2)
        out.append(S)
    return torch.stack(out, dim=1)


@torch.no_grad()
def oracle_states(gates: dict, n_real: int) -> torch.Tensor:
    """S_i = Σ_{j≤i} k_j v_jᵀ — pure cumulative superposition: no decay, no
    delta erasure. Keys/values from the cell's own trained WriteHead."""
    k, v = gates["k"].float(), gates["v"].float()
    outer = torch.einsum("bchk,bchv->bchkv", k[:, :n_real], v[:, :n_real])
    return outer.cumsum(dim=1)


@torch.no_grad()
def read_trained(sm, states: torch.Tensor) -> torch.Tensor:
    """The model's own readout chain on the given states: fixed readout_query
    -> realign -> nq-mean (the _forward_torch + _slm_store_rows v_rows form).
    (B, n, H, hk, hv) -> (B, n, d_pack)."""
    q = sm.readout_query.float()  # (nq, H, hk)
    bsz, n = states.shape[:2]
    reads = torch.einsum("qhk,bnhkv->bnqhv", q, states)
    read = reads.reshape(bsz, n, q.size(0), -1).to(states.dtype)
    return sm.realign(read).mean(dim=2)


@torch.no_grad()
def ridge_unmix(gates: dict, states: torch.Tensor, lam: float):
    """Per chunk i, per head h: V̂ = (K Kᵀ + λI)⁻¹ K S_i with K = keys of
    chunks 0..i; the row served is the own-chunk recovery v̂_i. Returns
    (v_hat (B, n, H*hv), mean cos(v̂_i, v_i)). Batch-1 eval form."""
    k, v = gates["k"].float(), gates["v"].float()
    assert k.size(0) == 1, "eval form is batch-1"
    n, H = states.size(1), k.size(2)
    hv = v.size(-1)
    v_hat = k.new_zeros(1, n, H, hv)
    cos_sum, cos_cnt = 0.0, 0
    for i in range(n):
        for h in range(H):
            K = k[0, : i + 1, h]  # (n_i, hk), rows already unit-norm (WriteHead)
            S = states[0, i, h]  # (hk, hv)
            A = K @ K.T + lam * torch.eye(i + 1, device=k.device, dtype=torch.float32)
            Vh = torch.linalg.solve(A, K @ S)  # (n_i, hv)
            v_hat[0, i, h] = Vh[-1]
            cos_sum += float(F.cosine_similarity(Vh[-1], v[0, i, h], dim=0))
            cos_cnt += 1
    return v_hat.reshape(1, n, H * hv), cos_sum / max(cos_cnt, 1)


@torch.no_grad()
def read_via_realign(sm, reads: torch.Tensor) -> torch.Tensor:
    """(B, n, H*hv) value-space reads -> realign -> (B, n, d_pack), the same
    downstream form as read_trained (nq=1)."""
    return sm.realign(reads.unsqueeze(2)).mean(dim=2)


@torch.no_grad()
def decode_direct(model, v_rows: torch.Tensor, chunks) -> torch.Tensor:
    """The cell's own direct decode chain: decoder_in(v_rows) + page-local pos
    -> decoder over the real rows (per-chunk independent — slicing is exact)."""
    n = v_rows.size(1)
    pos = model.chunk_pos.weight.unsqueeze(0)[:, :n]
    cond = model.decoder_in(v_rows) + pos
    return model.decoder(cond, chunks.token_mask[:, :n])


# ---------------------------------------------------------------------------
# A6 diagnostic: closed-form linear byte probe (v / m -> slot byte id)
# ---------------------------------------------------------------------------


def byte_probe(X: torch.Tensor, Y: torch.Tensor, valid: torch.Tensor, lam: float = 1.0,
               return_records: bool = False):
    """One-vs-all ridge from feature rows to the chunk's slot byte ids
    (2-fold split, fixed split seed). Returns per-slot (acc, majority baseline).
    Closed-form algebra only — no parameter training.
    return_records=True (审计落盘字段, 默认关=原行为逐位不变): 额外返回逐样本
    held-out 预测/目标/样本选择/折号 —— 聚合数与 accs 同源同一次计算。"""
    out = {}
    records: dict[str, dict] = {}
    for s in range(Y.size(1)):
        m = valid[:, s]
        x, y = X[m].float(), Y[m][:, s].long()
        n = x.size(0)
        if n < 40:
            continue
        x = torch.cat([x, torch.ones(n, 1)], dim=1)
        y1 = F.one_hot(y.clamp(min=0, max=257), 258).float()
        idx = torch.randperm(n, generator=torch.Generator().manual_seed(0))
        accs = []
        preds = torch.zeros(n, dtype=torch.long)
        fold = torch.zeros(n, dtype=torch.uint8)
        for fi, (lo, hi) in enumerate(((0, n // 2), (n // 2, n))):
            te = idx[lo:hi]
            tr = idx[n // 2 :] if lo == 0 else idx[: n // 2]
            W = torch.linalg.solve(
                x[tr].T @ x[tr] + lam * torch.eye(x.size(1)), x[tr].T @ y1[tr]
            )
            p = (x[te] @ W).argmax(dim=-1)
            accs.append(float(p.eq(y[te]).float().mean()))
            preds[te] = p
            fold[te] = fi
        maj = float(y1.mean(dim=0).max())  # majority-class baseline
        out[str(s)] = {"acc": round(sum(accs) / len(accs), 4), "majority": round(maj, 4), "n": n}
        if return_records:
            records[str(s)] = {"preds": preds, "targets": y, "sel": m, "fold": fold}
    if return_records:
        return out, records
    return out


# ---------------------------------------------------------------------------
# metrics on the cumulative as-encoded grid (+ clean-content diagnostic)
# ---------------------------------------------------------------------------


def _arm_metrics(logits, targets, slot_mask, own_mask):
    n = logits.size(1)
    tgt, sm_, om = targets[:, :n], slot_mask[:, :n], own_mask[:, :n]
    pred = logits.argmax(dim=-1)
    recalled = sm_ & ~om
    return {
        "ce": float(s1._ce(logits, tgt, sm_)),
        "acc": float(s1._acc_tensor(pred, tgt, sm_)),
        "acc_own": float(s1._acc_tensor(pred, tgt, om)),
        "acc_recalled": float(s1._acc_tensor(pred, tgt, recalled)),
        "n_slots": int(sm_.sum()),
        "n_recalled_slots": int(recalled.sum()),
    }, pred, tgt


def _per_row_acc(pred, tgt, mask):
    """(B, C, S) -> per-row acc list over real rows (nan for empty rows)."""
    hit = (pred.eq(tgt).float() * mask.float()).sum(dim=-1)
    cnt = mask.float().sum(dim=-1).clamp(min=1.0)
    row = (hit / cnt)[0]
    return [float(x) for x in row]


# ---------------------------------------------------------------------------
# per-window arm matrix
# ---------------------------------------------------------------------------


@torch.no_grad()
def run_window_c(model, ns, clean: torch.Tensor, byte_mask: torch.Tensor, lambdas, first_window=False):
    source = clean.masked_fill(byte_mask, MASK_ID)
    chunks, memory, _index = _front_end(model, source)
    n_real = int(chunks.chunk_mask[0].sum())
    gates = model.write_head(memory)
    sm = model.state_machine

    S_tr = trained_states(sm, gates, n_real)
    S_or = oracle_states(gates, n_real)
    v_tr = read_trained(sm, S_tr)  # A1 (manual reference path)
    v_or = read_trained(sm, S_or)  # A2
    v_pass = read_via_realign(sm, gates["v"][:, :n_real].float().reshape(1, n_real, -1))  # A5

    if first_window:
        # wiring sanity on the real model: manual trained path vs the model's
        # own _slm_store_rows v_rows (fla/torch parity included in the diff)
        v_native = model._slm_store_rows(chunks)[1][:, :n_real]
        diff = (v_tr - v_native.float()).abs().max()
        print(f"[sanity] manual-vs-native v_rows max|Δ|={float(diff):.5f}", flush=True)

    # target grids: c grid = coarse V -> cumulative as-encoded (direct official)
    # + clean cumulative (content diagnostic); own-slot mask from the base grid
    enc_targets, enc_slot, _enc_masked, _t = s1.make_cumulative_retention_targets(
        source, byte_mask, chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
    )
    clean_targets, clean_slot, _cm, _t2 = s1.make_cumulative_retention_targets(
        clean, byte_mask, chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
    )
    _bt, own_slot, _bm = s1.make_targets(
        source, torch.zeros_like(byte_mask), chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
    )

    arms: dict[str, dict] = {}

    def score(tag, v_rows):
        logits = decode_direct(model, v_rows, chunks)
        m, pred, tgt = _arm_metrics(logits, enc_targets, enc_slot, own_slot)
        m["acc_clean"] = float(
            s1._acc_tensor(pred, clean_targets[:, :n_real], clean_slot[:, :n_real])
        )
        # clean-content recall: recalled slots scored against CLEAN bytes (the
        # encoded grid's recalled targets are MASK_ID — the as-encoded view)
        m["acc_recalled_clean"] = float(
            s1._acc_tensor(pred, clean_targets[:, :n_real], (clean_slot[:, :n_real] & ~own_slot[:, :n_real]))
        )
        m["row_acc_own"] = _per_row_acc(pred, tgt, own_slot[:, :n_real])
        arms[tag] = m
        return logits

    score("A1_trained", v_tr)
    score("A2_oracle_state", v_or)
    score("A5_passthrough", v_pass)
    ridge_diag: dict[str, dict] = {}
    for lam in lambdas:
        vh_tr, cos_tr = ridge_unmix(gates, S_tr, lam)
        vh_or, cos_or = ridge_unmix(gates, S_or, lam)
        score(f"A3_ridge_trained_l{lam}", read_via_realign(sm, vh_tr))
        score(f"A4_ridge_oracle_l{lam}", read_via_realign(sm, vh_or))
        ridge_diag[str(lam)] = {"cos_trained": round(cos_tr, 4), "cos_oracle": round(cos_or, 4)}

    # mechanism measurements
    sv_tr = torch.linalg.svdvals(S_tr[0, -1].float())  # (H, min(hk,hv))
    sv_or = torch.linalg.svdvals(S_or[0, -1].float())

    def spec(sv):
        # per-head participation ratio (normalized by the spectrum length),
        # then mean over heads; top-k energy pooled over heads
        e = sv.square()  # (H, S)
        pr_h = sv.sum(dim=1) ** 2 / e.sum(dim=1).clamp(min=1e-12)  # (H,)
        return {
            "participation_ratio": round(float(pr_h.mean() / sv.size(1)), 4),
            "top8_energy": round(float(e[:, :8].sum() / e.sum()), 4),
            "top32_energy": round(float(e[:, :32].sum() / e.sum()), 4),
        }

    # key concentration: mean |cos| between write keys (key-collapse signature)
    kk = gates["k"][0, :n_real].float()  # (n, H, hk)
    kc = []
    for h in range(kk.size(1)):
        kh = kk[:, h]
        sim = (kh @ kh.T).abs()
        off = sim[~torch.eye(kh.size(0), dtype=torch.bool, device=kh.device)]
        kc.append(float(off.mean()))
    key_cos_mean = sum(kc) / len(kc)

    # A6 collectors: write values / memory rows / per-slot clean byte targets
    base_targets, base_slot, _bbm = s1.make_targets(
        clean, torch.zeros_like(byte_mask), chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
    )
    probe_rows = {
        "xs_v": gates["v"][0, :n_real].float().reshape(n_real, -1).cpu(),
        "xs_m": memory[0, :n_real].float().cpu(),
        "ys": base_targets[0, :n_real, :4].cpu(),
        "y_valid": base_slot[0, :n_real, :4].cpu(),
    }

    vnorm = gates["v"][0, :n_real].float().norm(dim=-1)  # (n, H)
    beta = gates["beta"][0, :n_real].float()  # (n, H)
    mech = {
        "state_norm_trained": round(float(S_tr[0, -1].norm(dim=(-2, -1)).mean()), 4),
        "state_norm_oracle": round(float(S_or[0, -1].norm(dim=(-2, -1)).mean()), 4),
        "svd_trained": spec(sv_tr),
        "svd_oracle": spec(sv_or),
        "write_vnorm_mean": round(float(vnorm.mean()), 4),
        "write_vnorm_std": round(float(vnorm.std()), 4),
        "beta_mean": round(float(beta.mean()), 4),
        "beta_std": round(float(beta.std()), 4),
        "alpha_mean": round(float(gates["alpha"].float().mean()), 4),
        "alpha_min": round(float(gates["alpha"].float().min()), 4),
        "ridge_cos": ridge_diag,
        "key_cos_mean": round(key_cos_mean, 4),
        "n_real": n_real,
    }
    return arms, mech, probe_rows


@torch.no_grad()
def run_window_a_anchor(model, ns, clean, byte_mask):
    """a-grid direct anchor on the same window: v_rows = memory rows (fine V,
    base as-encoded grid)."""
    source = clean.masked_fill(byte_mask, MASK_ID)
    chunks, memory, _index = _front_end(model, source)
    n_real = int(chunks.chunk_mask[0].sum())
    v_rows = memory[:, :n_real]
    pos = model.chunk_pos.weight.unsqueeze(0)[:, :n_real]
    cond = model.decoder_in_mem(v_rows) + pos
    logits = model.decoder(cond, chunks.token_mask[:, :n_real])
    targets, slot_mask, _m = s1.make_targets(
        source, torch.zeros_like(byte_mask), chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
    )
    m, pred, tgt = _arm_metrics(logits, targets, slot_mask, slot_mask)
    m["row_acc_own"] = _per_row_acc(pred, tgt, slot_mask[:, :n_real])
    m["n_real"] = n_real
    return m


@torch.no_grad()
def run_window_c_amp_control(model, ns, clean, byte_mask, device):
    """A1 under the anchor's original regime: bf16 autocast + the checkpoint's
    kda_impl (fla on cuda) — quantifies the fp32-manual口径 delta."""
    source = clean.masked_fill(byte_mask, MASK_ID)
    with torch.autocast("cuda", dtype=torch.bfloat16, enabled=device.type == "cuda"):
        out = s1._slm_forward(model, source, ns)
    chunks = out["chunks"]
    enc_targets, enc_slot, _m, _t = s1.make_cumulative_retention_targets(
        source, byte_mask, chunks.chunk_ids, chunks.offsets, ns.max_chunks, ns.max_span
    )
    n = out["logits_direct"].size(1)
    acc = float(s1._acc_tensor(out["logits_direct"].argmax(-1), enc_targets[:, :n], enc_slot[:, :n]))
    ce = float(s1._ce(out["logits_direct"], enc_targets[:, :n], enc_slot[:, :n]))
    return {"acc": acc, "ce": ce}


# ---------------------------------------------------------------------------
# aggregation
# ---------------------------------------------------------------------------


def _bucket_rows(row_accs: list[list[float]], buckets=10):
    """Per-row acc curves -> fractional-position buckets (rows are nan-free
    for real chunks; windows differ in n_real)."""
    agg = [[] for _ in range(buckets)]
    for rows in row_accs:
        n = len(rows)
        for i, a in enumerate(rows):
            agg[min(buckets - 1, int(buckets * i / max(n, 1)))].append(a)
    return [round(sum(b) / len(b), 4) if b else None for b in agg]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--c-run-dir", default=C_RUN)
    p.add_argument("--a-run-dir", default=A_RUN)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--max-windows", type=int, default=16, help="eval windows (16 = the training final-eval protocol)")
    p.add_argument("--lambdas", default="0.0001,0.01,1")
    p.add_argument("--out-dir", default="outputs/oracle_write_verdict_20260818")
    p.add_argument("--skip-a-anchor", action="store_true")
    p.add_argument("--skip-amp-control", action="store_true")
    p.add_argument("--dump-probe-bytes", action="store_true",
                   help="审计落盘字段: A6 逐样本 held-out 预测/目标/折号 → byte_probe_records.npz"
                        "（与聚合 accs 同源同一次计算, 口径零改动）")
    args = p.parse_args()
    device = torch.device("cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    lambdas = [float(x) for x in args.lambdas.split(",")]
    t0 = time.time()

    c_model, c_ns, c_step = load_model(Path(args.c_run_dir), device)
    print(f"[oracle] C model={Path(args.c_run_dir).name} step={c_step} device={device.type}", flush=True)
    windows = build_eval_windows(c_ns, args.max_windows)
    masks = build_masks(windows, c_ns)
    print(f"[oracle] {len(windows)} eval windows + masks ready ({time.time() - t0:.0f}s)", flush=True)

    per_window, mech_rows, amp_rows, probe_rows_all = [], [], [], []
    for wi, (clean, byte_mask) in enumerate(zip(windows, masks)):
        clean_d, bm_d = clean.to(device), byte_mask.to(device)
        arms, mech, prows = run_window_c(c_model, c_ns, clean_d, bm_d, lambdas, first_window=(wi == 0))
        per_window.append({"window": wi, "arms": arms})
        mech_rows.append(mech)
        probe_rows_all.append(prows)
        if not args.skip_amp_control:
            amp_rows.append(run_window_c_amp_control(c_model, c_ns, clean_d, bm_d, device))
        brief = " | ".join(f"{k.split('_')[0]}:{v['acc']:.3f}" for k, v in arms.items() if k.startswith(("A1", "A2", "A5")))
        print(f"[oracle] window {wi} n_real={mech['n_real']} {brief} ({time.time() - t0:.0f}s)", flush=True)

    # aggregate arms over windows (mean of per-window metrics; ppl = exp(mean ce))
    arm_tags = list(per_window[0]["arms"].keys())
    agg = {}
    for tag in arm_tags:
        rows = [w["arms"][tag] for w in per_window]
        agg[tag] = {
            "acc": round(sum(r["acc"] for r in rows) / len(rows), 4),
            "ce": round(sum(r["ce"] for r in rows) / len(rows), 4),
            "ppl": round(math.exp(min(sum(r["ce"] for r in rows) / len(rows), 20.0)), 3),
            "acc_own": round(sum(r["acc_own"] for r in rows) / len(rows), 4),
            "acc_recalled": round(sum(r["acc_recalled"] for r in rows) / len(rows), 4),
            "acc_clean": round(sum(r["acc_clean"] for r in rows) / len(rows), 4),
            "acc_recalled_clean": round(sum(r["acc_recalled_clean"] for r in rows) / len(rows), 4),
            "curve_own_10b": _bucket_rows([r["row_acc_own"] for r in rows]),
        }

    # mechanism aggregates
    def _mmean(key, *path):
        vals = [m[key] for m in mech_rows] if not path else [m[key][path[0]] for m in mech_rows]
        return round(sum(vals) / len(vals), 4)

    mech_agg = {
        "state_norm_trained": _mmean("state_norm_trained"),
        "state_norm_oracle": _mmean("state_norm_oracle"),
        "svd_trained": {k: _mmean("svd_trained", k) for k in mech_rows[0]["svd_trained"]},
        "svd_oracle": {k: _mmean("svd_oracle", k) for k in mech_rows[0]["svd_oracle"]},
        "write_vnorm_mean": _mmean("write_vnorm_mean"),
        "write_vnorm_std": _mmean("write_vnorm_std"),
        "beta_mean": _mmean("beta_mean"),
        "beta_std": _mmean("beta_std"),
        "alpha_mean": _mmean("alpha_mean"),
        "alpha_min": _mmean("alpha_min"),
        "ridge_cos": {
            lam: {
                kk: round(sum(m["ridge_cos"][lam][kk] for m in mech_rows) / len(mech_rows), 4)
                for kk in ("cos_trained", "cos_oracle")
            }
            for lam in mech_rows[0]["ridge_cos"]
        },
        "key_cos_mean": _mmean("key_cos_mean"),
    }

    # A6: closed-form byte probes (v = the WriteHead's write values; m = the
    # pre-state memory rows = ceiling control). v-probe ≈ m-probe ⟹ the write
    # preserves byte content (failure lives downstream); v-probe ≈ majority
    # baseline ⟹ the write value itself never carried the bytes (H1).
    xs_v = torch.cat([r["xs_v"] for r in probe_rows_all], dim=0)
    xs_m = torch.cat([r["xs_m"] for r in probe_rows_all], dim=0)
    ys = torch.cat([r["ys"] for r in probe_rows_all], dim=0)
    y_valid = torch.cat([r["y_valid"] for r in probe_rows_all], dim=0)
    # --dump-probe-bytes (审计落盘字段, 聚合数同源): 逐样本 held-out 记录 → npz
    probe_records: dict | None = None
    if args.dump_probe_bytes:
        mech_agg["byte_probe_from_v"], rec_v = byte_probe(xs_v, ys, y_valid, return_records=True)
        mech_agg["byte_probe_from_m"], rec_m = byte_probe(xs_m, ys, y_valid, return_records=True)
        probe_records = {"v": rec_v, "m": rec_m}
    else:
        mech_agg["byte_probe_from_v"] = byte_probe(xs_v, ys, y_valid)
        mech_agg["byte_probe_from_m"] = byte_probe(xs_m, ys, y_valid)
    bp_v = mech_agg["byte_probe_from_v"].get("0", {})
    bp_m = mech_agg["byte_probe_from_m"].get("0", {})
    print(
        f"[A6] byte-probe slot0: from_v acc={bp_v.get('acc')} (majority {bp_v.get('majority')}) "
        f"| from_m acc={bp_m.get('acc')} (majority {bp_m.get('majority')})",
        flush=True,
    )
    if probe_records is not None:
        import numpy as np

        arrays: dict = {}
        for src, recs in probe_records.items():
            for s, r in recs.items():
                arrays[f"{src}_s{s}_preds"] = r["preds"].numpy().astype(np.int16)
                arrays[f"{src}_s{s}_targets"] = r["targets"].numpy().astype(np.int16)
                arrays[f"{src}_s{s}_sel"] = r["sel"].numpy().astype(np.uint8)
                arrays[f"{src}_s{s}_fold"] = r["fold"].numpy()
        np.savez_compressed(out_dir / "byte_probe_records.npz", **arrays)
        print(f"[A6] per-sample probe records -> {out_dir / 'byte_probe_records.npz'}", flush=True)

    # a-grid anchor on the same windows
    a_anchor = None
    if not args.skip_a_anchor:
        a_model, a_ns, a_step = load_model(Path(args.a_run_dir), device)
        print(f"[oracle] A model={Path(args.a_run_dir).name} step={a_step}", flush=True)
        a_rows = [run_window_a_anchor(a_model, a_ns, w.to(device), m.to(device)) for w, m in zip(windows, masks)]
        a_anchor = {
            "acc": round(sum(r["acc"] for r in a_rows) / len(a_rows), 4),
            "ce": round(sum(r["ce"] for r in a_rows) / len(a_rows), 4),
            "ppl": round(math.exp(min(sum(r["ce"] for r in a_rows) / len(a_rows), 20.0)), 3),
            "curve_own_10b": _bucket_rows([r["row_acc_own"] for r in a_rows]),
        }
        print(f"[oracle] A0 a-grid anchor acc={a_anchor['acc']} ppl={a_anchor['ppl']}", flush=True)
        del a_model
        if device.type == "cuda":
            torch.cuda.empty_cache()

    amp_ctrl = None
    if amp_rows:
        amp_ctrl = {
            "acc": round(sum(r["acc"] for r in amp_rows) / len(amp_rows), 4),
            "ce": round(sum(r["ce"] for r in amp_rows) / len(amp_rows), 4),
            "ppl": round(math.exp(min(sum(r["ce"] for r in amp_rows) / len(amp_rows), 20.0)), 3),
        }

    report = {
        "probe": "S39 oracle write verdict (E-a root-cause bisection)",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "checkpoints": {"c": {"run": Path(args.c_run_dir).name, "step": c_step}, "a": Path(args.a_run_dir).name},
        "anchors": {"a_grid_direct": {"acc": 0.7923, "ppl": 2.141}, "c_grid_direct": {"acc": 0.2972, "ppl": 39.95}},
        "params": {"windows": len(windows), "lambdas": lambdas, "eval_mask_seed": c_ns.eval_mask_seed},
        "arms_agg": agg,
        "a0_anchor_repro": a_anchor,
        "amp_control_A1": amp_ctrl,
        "mechanism": mech_agg,
        "per_window": per_window,
        "mech_per_window": mech_rows,
        "timing_sec": round(time.time() - t0, 1),
    }
    out_path = out_dir / "oracle_write_verdict.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    # one-page human summary with the verdict table
    gap = (a_anchor["acc"] if a_anchor else 0.7923) - agg["A1_trained"]["acc"]

    def rec(tag):
        a = agg[tag]["acc"]
        return (a - agg["A1_trained"]["acc"]) / max(gap, 1e-9)

    lines = [
        "ORACLE WRITE VERDICT — c 格 (v37_c_is, v=state) E-a 根因二分",
        f"日期 {report['created']}  设备 {device.type}  窗口 {len(windows)}  口径 fp32-manual（amp 对照另列）",
        "",
        "锚: a 格 direct 0.7923/2.141（本脚本复现 A0: "
        + (f"{a_anchor['acc']:.4f}/{a_anchor['ppl']}" if a_anchor else "跳过")
        + f"）; c 格崩盘 0.2972/39.95（本脚本复现 A1: {agg['A1_trained']['acc']:.4f}/{agg['A1_trained']['ppl']}"
        + (f"; A1-amp {amp_ctrl['acc']:.4f}/{amp_ctrl['ppl']}" if amp_ctrl else "")
        + ")",
        "⚠ 网格口径: a 锚 direct = fine 本段格; c 格 direct = 累积 as-encoded 格(consensus §2 粗粒度格),",
        "  两锚绝对值不可直接比——同形对照用 own-slot acc（c A1 ≈ a A0 同窗同槽）。",
        "",
        "臂矩阵（direct acc / ppl / own本段 / recalled忆回(as-enc) / recalled(clean) / 恢复率）:",
    ]
    for tag in arm_tags:
        a = agg[tag]
        lines.append(
            f"  {tag:24s} {a['acc']:.4f} / {a['ppl']:8.2f} / {a['acc_own']:.4f} / {a['acc_recalled']:.4f} / {a['acc_recalled_clean']:.4f} / {rec(tag):+.2%}"
        )
    lines += [
        "",
        "机制测量:",
        f"  ridge cos(v̂,v): {json.dumps(mech_agg['ridge_cos'])}",
        f"  state_norm trained/oracle: {mech_agg['state_norm_trained']} / {mech_agg['state_norm_oracle']}",
        f"  SVD 有效秩(PR/dim) trained {mech_agg['svd_trained']['participation_ratio']} top8能量 {mech_agg['svd_trained']['top8_energy']}"
        f" | oracle {mech_agg['svd_oracle']['participation_ratio']} top8 {mech_agg['svd_oracle']['top8_energy']}",
        f"  key 平均|cos|（键塌缩签名）: {mech_agg['key_cos_mean']}",
        f"  写值范数 {mech_agg['write_vnorm_mean']}±{mech_agg['write_vnorm_std']}  beta {mech_agg['beta_mean']}±{mech_agg['beta_std']}  alpha mean/min {mech_agg['alpha_mean']}/{mech_agg['alpha_min']}",
        "  A6 闭式字节探针（acc vs majority 基线, slots 0-3）:",
        f"    from v（写值）: {json.dumps(mech_agg['byte_probe_from_v'])}",
        f"    from m（memory 行, 上限对照）: {json.dumps(mech_agg['byte_probe_from_m'])}",
        "",
        "判决逻辑（docstring §判决逻辑）: A4恢复+A3崩→递推侵蚀; A3恢复→读出侧; A2/A4崩+cos≈1+A5恢复→读出结构病;",
        "A4/A5崩 → 看 A6: v-probe≈majority→写入未形成(H1坐实); v-probe≈m-probe→内容在写值里但解码链读不出(读出结构病)。",
        f"完整数据: {out_path}",
    ]
    summary_path = out_dir / "SUMMARY.txt"
    summary_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[oracle] report -> {out_path}", flush=True)
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
