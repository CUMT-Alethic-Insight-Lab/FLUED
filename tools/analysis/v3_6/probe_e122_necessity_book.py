"""E122 跨段必要性账（零训练判别，判 E121「不确定」格真身；冻结预注册 v1.0
docs/versions/v3_7/FLUED_V3_7_E122_CROSSSEG_NECESSITY_20260906_CN.md）。

判读对象 = D1 选中位（w2 选择图、seed42+9999 eval 窗流、分位数档最稀有 20%、
L=6/T=3 续尾语义与 _d1_build_weight_map 一致）对**源 L-gram 内容**的依赖量。
三臂同批窗同冻结基座，逐位 NLL 全 fp32 无 autocast（cbiu_anchors 先例）：

  (a)  完整窗基线；
  (b1) 外科替换：每个选中位的源 L-gram（窗内最早出现处）替换为同长度、同
       UTF-8 续字节结构（逐字节 0x80-0xBF 续位图案）、同稀有表内的另一 gram
       （随机但记录种子）——必要性总量（路径 A+B 合计）；
  (b2) 源 chunk 行手术：被替换出现处所在 chunk 的 store 行（v_rows 连带
       k_rows，及 views 时的 k_store/v_store）用同窗其他 chunk 的行替换
       （统计匹配、内容错误、行存在性保留；_patch_state_zero 同款机制）——
       显式索引路径（不进主判读表，分层素材）。

对照：同窗未选中位（等量随机抽样）；对照位的手术 = 同窗随机挑一个稀有表
gram 出现处做同款替换（吸收替换本身的 surprisal 位移）。主判读量 =
mean ΔNLL_b1(选中) − mean ΔNLL_b1(对照)，窗级 bootstrap 95% CI。

卫生：eval mask 命中位剔除并计数；b1 分段漂移检查（手术前后 chunk 网格在
计分位不一致的窗整窗剔除并报剔除率）；被替换 span 覆盖的计分位按侧伤剔除；
任务注入零（burst/cloze/retrieval 清零）；坑 8 全键断言（缺键 loud fail，
禁止 build_model 兜底默认）。

主读数面 = codec direct 路径（logits_direct，D1 加权训练的同一表面）。d 格
（coarse V）direct 的靶网格是累积 as-encoded 格（make_cumulative_retention_targets
语义）：未遮蔽字节在全网格的唯一落点是自身 (chunk, slot)（累积格只给**遮蔽**
字节追加召回槽）——本账计分位一律剔除 mask 命中位，故逐位 NLL 取自身槽位即
穷尽；映射代数与累积格对拍见 tests/test_e122_necessity_book.py。

零复制复用：load_model / build_eval_windows / build_masks（probe_oracle_write_
verdict 骨架）+ s1_forward（前向）+ cross_chunk_occurrences（密度账同源 import）
+ _d1_select_rare_grams / _load_d1_rare_table（D1 训练器同函数）。

Usage:
  python tools/analysis/v3_6/probe_e122_necessity_book.py --device cuda \
      --ckpt checkpoints/v37ks_d_sm_q15_circuit_20k_ctx4096_20260825b \
      --rare-table outputs/d1_rare_table_l6_20260904/d1_rare_table_l6.npz \
      --n-windows 500
  CPU 冒烟: --device cpu --n-windows 2
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
import time
from argparse import Namespace
from pathlib import Path

import torch
import torch.nn.functional as F

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from flued.data import BYTE_OFFSET, MASK_ID, PAD_ID  # noqa: E402
from tools.analysis.v3_6.demand_density_book import (  # noqa: E402
    CHUNK as SCAN_CHUNK,
    cross_chunk_occurrences,
)
import tools.train.v3_6.train_v36_s1 as s1  # noqa: E402
from tools.analysis.v3_6.probe_oracle_write_verdict import (  # noqa: E402
    build_eval_windows,
    build_masks,
    load_model,
)

DEFAULT_CKPT = "checkpoints/v37ks_d_sm_q15_circuit_20k_ctx4096_20260825b"
DEFAULT_RARE_TABLE = "outputs/d1_rare_table_l6_20260904/d1_rare_table_l6.npz"

# 判读线（预注册 §4 冻结 v1.0；唯一自由数 = 1.0 nat，弱/无分界 = bootstrap CI）
STRONG_LINE_NAT = 1.0
# 有效跨段密度换算（次判读）：D1 实际监督 ~110 字节/窗、密度账最严口径 54.8 字节/窗
DENSITY_SUPERVISED_BPW = 110.0
DENSITY_STRICT_BPW = 54.8

# 坑 8 全键断言（build_model 兜底默认分别为 v/memory/memory/mean/attn，
# train_v36.py:68-93——resolved_config 缺键即 loud fail，禁止兜底）
CELL_KEYS = {
    "seed_source": "k",
    "k_row_source": "state",
    "v_row_source": "state",
    "summarizer_pool": "qpool",
    "backbone_mode": "slm",
}

_MISSING = object()


# ---------------------------------------------------------------------------
# 坑 8 家族：全键断言
# ---------------------------------------------------------------------------


def assert_cell_keys(ns, model_config=None) -> None:
    """resolved_config（及装载后 model.config）逐键断言 d 格口径；键缺失或值
    漂移一律 ValueError 响亮拒绝——build_model 的 getattr 兜底默认会把纯行为
    静默漂移藏进读数（坑 8, 2026-08-29 冒烟事故同族）。"""

    def check(obj, where: str) -> None:
        bad = []
        for key, want in CELL_KEYS.items():
            got = getattr(obj, key, _MISSING)
            shown = "<键缺失>" if got is _MISSING else repr(got)
            if got != want:
                bad.append(f"{where}.{key}={shown} != {want!r}")
        if bad:
            raise ValueError(
                "E122 坑8 全键断言失败（resolved_config 缺键/错值不许 build_model "
                "兜底，禁静默）: " + "; ".join(bad)
            )

    check(ns, "resolved_config")
    if model_config is not None:
        check(model_config, "model.config")


# ---------------------------------------------------------------------------
# b1 外科替换：三匹配（长度 / UTF-8 续字节结构 / 稀有表内）
# ---------------------------------------------------------------------------


def continuation_pattern(gram: bytes) -> tuple[bool, ...]:
    """逐字节 0x80-0xBF 续位图案（True = UTF-8 continuation byte）。"""
    return tuple(0x80 <= b <= 0xBF for b in gram)


def _cont_mask(gram: bytes) -> int:
    """图案压缩成位串 int（模式索引键，省内存：3.68M gram 表只建一次）。"""
    m = 0
    for i, b in enumerate(gram):
        if 0x80 <= b <= 0xBF:
            m |= 1 << i
    return m


def build_pattern_index(table: dict[bytes, int]) -> dict[int, list[bytes]]:
    """稀有表按续位图案分桶（pick_replacement 的候选域）。"""
    idx: dict[int, list[bytes]] = {}
    for g in table:
        idx.setdefault(_cont_mask(g), []).append(g)
    return idx


def pick_replacement(gram: bytes, pattern_index: dict[int, list[bytes]], rng: random.Random,
                     forbidden: frozenset[bytes] = frozenset(), window: bytes | None = None,
                     max_draws: int = 64) -> bytes:
    """同长度 + 同续位图案 + 表内 + != 原串 + 不在禁集（优先不在窗内已出现——
    避免制造伪跨 chunk 链；抽满 max_draws 仍撞窗则如实接受最后抽样）。候选域
    为空（表内同图案只有原串自己/全被禁）时 ValueError 响亮，不静默回退。"""
    bucket = pattern_index.get(_cont_mask(gram))
    if not bucket:
        raise ValueError(f"rare table 无同图案候选: {gram!r}")
    cand = None
    for _ in range(max_draws):
        c = bucket[rng.randrange(len(bucket))]
        if c == gram or c in forbidden:
            continue
        cand = c
        if window is None or window.find(c) == -1:
            return c
    if cand is None:
        raise ValueError(f"rare table 同图案候选全被禁: {gram!r}")
    return cand


def select_tail_positions(occ: dict[bytes, list[int]], rare: set[bytes], L: int, tail: int,
                          win_len: int) -> tuple[dict[int, tuple[bytes, int]], int]:
    """选中位 = 稀有命中 gram 重复出现处起的 T 个续尾字节（byte 索引 p+L ..
    p+L+T-1，与 _d1_build_weight_map / 密度账 supervised_count 同一 range 语义，
    窗沿截断）。返回 (byte_pos -> (gram, 重复出现 p), 重叠计数)。"""
    sel: dict[int, tuple[bytes, int]] = {}
    overlap = 0
    for g in sorted(rare):
        for p in occ.get(g, ()):
            for t in range(p + L, min(p + L + tail, win_len)):
                if t in sel:
                    overlap += 1
                    continue
                sel[t] = (g, p)
    return sel, overlap


def table_occurrences(raw: bytes, L: int, table: dict[bytes, int]) -> list[tuple[bytes, int]]:
    """窗内全部稀有表 gram 出现处（含最早出现——对照手术与选中手术同域，
    只由 used/protected 排除规则区分）。"""
    out = []
    for p in range(0, len(raw) - L + 1):
        g = raw[p:p + L]
        if g in table:
            out.append((g, p))
    return out


def _overlaps(span: tuple[int, int], spans: list[tuple[int, int]]) -> bool:
    lo, hi = span
    return any(lo < h and l < hi for l, h in spans)


class SurgeryPlan:
    """一窗的 b1 手术单：被替换 span（原 gram、窗内位置、替换 gram）+ 计数。"""

    def __init__(self):
        self.spans: list[tuple[bytes, int, bytes]] = []  # (orig_gram, pos, repl)
        self.control_span: dict[int, int] = {}  # control byte_pos -> spans 下标
        self.n_control_no_occurrence = 0
        self.n_source_overlap_skipped = 0
        self.replacements: dict[bytes, bytes] = {}  # orig -> repl（同窗同串同替换）

    def apply(self, raw: bytes) -> bytes:
        buf = bytearray(raw)
        for g, p, r in self.spans:
            buf[p:p + len(r)] = r
        return bytes(buf)

    def replaced_positions(self) -> set[int]:
        out: set[int] = set()
        for _g, p, r in self.spans:
            out.update(range(p, p + len(r)))
        return out


def plan_window_surgery(raw: bytes, rare: set[bytes], sel: dict[int, tuple[bytes, int]],
                        control_positions: list[int], table: dict[bytes, int],
                        pattern_index: dict[int, list[bytes]], rng: random.Random,
                        L: int, tail: int) -> SurgeryPlan:
    """一窗手术单。

    选中位：每个选中 gram 的**最早出现处**（raw.find = cross_chunk_occurrences
    语义下的 first_chunk 出现）替换——目标位（重复出现处续尾）字节保持不变。
    同串多出现共用一个替换 gram；span 相互重叠的 gram 跳过并计数（其选中位仍
    计分、如实稀释，对照侧同款吸收）。
    对照位：每对照位随机挑一个稀有表 gram 出现处做同款替换；排除规则 = 已用
    span、选中位保护区（选中出现处+续尾，防对照手术污染选中处理）、含该对照
    位自身的 span；无合格出现处 → 该对照位剔除计数。
    原串互为禁集（替换不落回任何被替换原串，杜绝串别名）。"""
    plan = SurgeryPlan()
    n = len(raw)
    used: list[tuple[int, int]] = []
    # 选中位保护区：选中（重复）出现处 + 续尾
    protected = [(p, min(p + L + tail, n)) for _g, p in set(sel.values())]

    # 1) 选中源替换
    sel_originals = {g for g, _p in sel.values()}
    for g in sorted(sel_originals):
        p0 = raw.find(g)  # 最早出现（first_chunk）
        if _overlaps((p0, p0 + L), used):
            plan.n_source_overlap_skipped += 1
            continue
        base = sel_originals | set(plan.replacements) | set(plan.replacements.values())
        r = pick_replacement(g, pattern_index, rng, forbidden=frozenset(base - {g}), window=raw)
        plan.replacements[g] = r
        plan.spans.append((g, p0, r))
        used.append((p0, p0 + L))

    # 2) 对照替换（等量吸收替换本身的 surprisal 位移）
    occ_table = table_occurrences(raw, L, table)
    for q in control_positions:
        eligible = [
            (g, p)
            for g, p in occ_table
            if not _overlaps((p, p + L), used)
            and not _overlaps((p, p + L), protected)
            and not (p <= q < p + L)
            and g not in plan.replacements
        ]
        if not eligible:
            plan.n_control_no_occurrence += 1
            continue
        g, p = eligible[rng.randrange(len(eligible))]
        base = sel_originals | set(plan.replacements) | set(plan.replacements.values())
        r = pick_replacement(g, pattern_index, rng, forbidden=frozenset(base - {g}), window=raw)
        plan.replacements[g] = r
        plan.control_span[q] = len(plan.spans)
        plan.spans.append((g, p, r))
        used.append((p, p + L))
    return plan


# ---------------------------------------------------------------------------
# d 格累积网格：字节位 → (chunk, slot) 映射（make_cumulative_retention_targets 语义）
# ---------------------------------------------------------------------------


def byte_to_grid_slots(chunk_ids: torch.Tensor, offsets: torch.Tensor, byte_mask: torch.Tensor,
                       max_chunks: int, max_span: int):
    """逐字节位自身的网格落点 (c, s) 与可计分性。

    _d1_build_weight_map 的 chunk_ids[t]/offsets[t] 直映射只在 per-chunk 格成立；
    d 格（coarse V）direct 的靶网格是**累积 as-encoded** 格：自身槽 (c,s) 之上，
    遮蔽字节还按 make_cumulative_retention_targets 追加进 row>c 的召回槽——追加
    槽**只装遮蔽字节**，而本账计分位一律剔除 mask 命中位，故未遮蔽字节在全网
    格的唯一落点就是自身槽（完备性代数由单测对拍锁定）。返回 (c_map, s_map,
    valid)：valid = 网格内且非 mask 命中。"""
    in_grid = (
        chunk_ids.ge(0) & chunk_ids.lt(max_chunks) & offsets.ge(0) & offsets.lt(max_span)
    )
    valid = in_grid & ~byte_mask.bool()
    return chunk_ids.long(), offsets.long(), valid


def drifted_positions(ca: torch.Tensor, oa: torch.Tensor, cb: torch.Tensor, ob: torch.Tensor,
                      positions: list[int]) -> list[int]:
    """b1 手术后 chunk 网格在计分位漂移的位清单（预注册 §3：目标位上游分段
    漂移 → 整窗剔除并报剔除率）。"""
    return [
        t for t in positions
        if (int(ca[0, t]), int(oa[0, t])) != (int(cb[0, t]), int(ob[0, t]))
    ]


# ---------------------------------------------------------------------------
# 逐位 NLL（fp32 无 autocast；cbiu_anchors 先例）
# ---------------------------------------------------------------------------


def gather_nll(logits_direct: torch.Tensor, chunk_ids: torch.Tensor, offsets: torch.Tensor,
               positions: list[int], target_ids: list[int]) -> list[float]:
    """主读数面 = codec direct：logits (1, C, S, V) 在各计分位自身槽的
    F.cross_entropy(reduction="none")，fp32、detach（冻结模型确定性读数，
    不开梯度图）。"""
    c = torch.tensor([int(chunk_ids[0, t]) for t in positions], dtype=torch.long)
    s = torch.tensor([int(offsets[0, t]) for t in positions], dtype=torch.long)
    picked = logits_direct[0][c, s].detach().float()  # (N, V)
    tgt = torch.tensor(target_ids, dtype=torch.long).clamp(min=0, max=257)
    nll = F.cross_entropy(picked, tgt, reduction="none")
    return [float(x) for x in nll.tolist()]


# ---------------------------------------------------------------------------
# b2 源 chunk 行手术（_patch_state_zero 同款机制）
# ---------------------------------------------------------------------------


def build_row_perm(source_chunks: set[int], n_real: int) -> list[int]:
    """行置乱置换：source_chunks 的行 ← 同窗其他真实 chunk 的行（确定性轮转；
    统计匹配=同行源同窗、内容错误、行存在性保留）。无其他真实 chunk 时
    ValueError 响亮。"""
    src = sorted(c for c in source_chunks if 0 <= c < n_real)
    perm = list(range(n_real))
    if not src:
        return perm
    src_set = set(src)
    others = [c for c in range(n_real) if c not in src_set]
    if not others:
        raise ValueError("b2 行手术需要至少一个非源真实 chunk")
    for k, i in enumerate(src):
        perm[i] = others[k % len(others)]
    return perm


def patch_store_rows_perm(model, perm: list[int]):
    """实例级包裹 ``_slm_store_rows``：k_rows/v_rows（及 views 时的 k_store/
    v_store）在真实行域内按 perm 重排，memory/index/state_norm 不动。返回
    restore()（删实例属性即还原，_patch_state_zero 同款）。"""
    orig = model._slm_store_rows
    idx = torch.tensor(perm, dtype=torch.long)

    def wrapped(chunks, with_views=False):
        rows = list(orig(chunks, with_views=with_views))
        n_real = int(chunks.chunk_mask[0].sum())
        pi = idx[:n_real].to(rows[0].device)
        for j in (0, 1, 5, 6):  # k_rows, v_rows, k_store, v_store
            if j < len(rows) and rows[j] is not None:
                r = rows[j]
                rows[j] = torch.cat([r[:, pi], r[:, n_real:]], dim=1)
        return tuple(rows)

    model._slm_store_rows = wrapped

    def restore():
        del model._slm_store_rows

    return restore


# ---------------------------------------------------------------------------
# 单窗三臂
# ---------------------------------------------------------------------------


def default_forward(model, source: torch.Tensor, ns) -> dict:
    return s1.s1_forward(model, source, ns)


@torch.no_grad()
def run_window(model, ns, clean_ids: torch.Tensor, byte_mask: torch.Tensor, table: dict[bytes, int],
               scan: Namespace, arms: set[str], rng: random.Random,
               pattern_index: dict[int, list[bytes]], window_id: int,
               forward_fn=None) -> dict:
    """三臂同窗：返回 {status, items, sums, counts}。status ∈ ok / dropped_drift
    / empty。clean_ids/byte_mask: (1, T)（已剥 PAD，模型设备）。"""
    forward_fn = forward_fn or default_forward
    L, tail, quantile = scan.ngram_len, scan.tail, scan.rare_quantile
    max_chunks, max_span = int(ns.max_chunks), int(ns.max_span)
    raw = bytes(int(x) - BYTE_OFFSET for x in clean_ids[0].tolist())
    n = len(raw)

    counts = {
        "n_selected_mask_excluded": 0, "n_control_mask_excluded": 0,
        "n_grid_excluded": 0, "n_selected_collateral": 0, "n_control_collateral": 0,
        "n_control_no_occurrence": 0,
        "n_source_overlap_skipped": 0, "n_selection_overlap": 0,
        "hit_grams": 0, "offtable_grams": 0,
    }
    empty = {"status": "empty", "items": [], "sums": _zero_sums(), "counts": counts}
    if n < L + 1:
        return empty

    occ = cross_chunk_occurrences(raw, L)  # 密度账同源（D1 选择图）
    rare, offtable = s1._d1_select_rare_grams(occ, table, quantile)  # D1 训练器同函数
    counts["hit_grams"] = len(occ)
    counts["offtable_grams"] = offtable
    sel, sel_overlap = select_tail_positions(occ, rare, L, tail, n)
    counts["n_selection_overlap"] = sel_overlap
    if not sel:
        return empty

    free = [t for t in range(n) if t not in sel]
    control_positions = rng.sample(free, min(len(sel), len(free)))
    plan = plan_window_surgery(raw, rare, sel, control_positions, table, pattern_index,
                               rng, L, tail)
    counts["n_control_no_occurrence"] = plan.n_control_no_occurrence
    counts["n_source_overlap_skipped"] = plan.n_source_overlap_skipped
    controls_planned = [q for q in control_positions if q in plan.control_span]

    # 臂 (a)：完整窗基线
    source_a = clean_ids.masked_fill(byte_mask.bool(), MASK_ID)
    out_a = forward_fn(model, source_a, ns)
    ca, oa = out_a["chunks"].chunk_ids, out_a["chunks"].offsets

    def base_valid(t: int) -> bool:
        if 0 <= int(ca[0, t]) < max_chunks and 0 <= int(oa[0, t]) < max_span:
            return True
        return False

    def score_set(positions: list[int]) -> tuple[list[int], list[int]]:
        """拆 mask 命中 / 网格外；返回 (可计分位, target ids)。"""
        keep, tgts = [], []
        for t in positions:
            if bool(byte_mask[0, t]):
                continue
            if not base_valid(t):
                counts["n_grid_excluded"] += 1
                continue
            keep.append(t)
            tgts.append(int(clean_ids[0, t]))
        return keep, tgts

    sel_valid, _sel_tgt = score_set(sorted(sel))
    ctl_valid, _ctl_tgt = score_set(sorted(controls_planned))
    counts["n_selected_mask_excluded"] = sum(1 for t in sorted(sel) if bool(byte_mask[0, t]))
    counts["n_control_mask_excluded"] = sum(1 for t in sorted(controls_planned) if bool(byte_mask[0, t]))
    if not sel_valid:
        return {**empty, "status": "empty"}

    # 侧伤剔除：计分位落在任何被替换 span 内 → 该位字节在 b1 变了，读数不可比
    hit = plan.replaced_positions()
    sel_scored = [t for t in sel_valid if t not in hit]
    ctl_scored = [t for t in ctl_valid if t not in hit]
    counts["n_selected_collateral"] = len(sel_valid) - len(sel_scored)
    counts["n_control_collateral"] = len(ctl_valid) - len(ctl_scored)

    nll_a_sel = dict(zip(sel_scored, gather_nll(out_a["logits_direct"], ca, oa, sel_scored,
                                                [int(clean_ids[0, t]) for t in sel_scored])))
    nll_a_ctl = dict(zip(ctl_scored, gather_nll(out_a["logits_direct"], ca, oa, ctl_scored,
                                                [int(clean_ids[0, t]) for t in ctl_scored])))

    # 臂 (b1)：外科替换（字节面）
    nll_b1_sel, nll_b1_ctl = {}, {}
    if "b1" in arms:
        raw_b1 = plan.apply(raw)
        ids_b1 = torch.tensor([[b + BYTE_OFFSET for b in raw_b1]], dtype=clean_ids.dtype,
                              device=clean_ids.device)
        source_b1 = ids_b1.masked_fill(byte_mask.bool(), MASK_ID)
        out_b1 = forward_fn(model, source_b1, ns)
        cb, ob = out_b1["chunks"].chunk_ids, out_b1["chunks"].offsets
        scored = sel_scored + ctl_scored
        drift = drifted_positions(ca, oa, cb, ob, scored)
        if drift:
            return {
                "status": "dropped_drift",
                "items": [],
                "sums": _zero_sums(),
                "counts": {**counts, "n_drift_positions": len(drift)},
                "drift_positions": drift[:16],
            }
        nll_b1_sel = dict(zip(sel_scored, gather_nll(out_b1["logits_direct"], cb, ob, sel_scored,
                                                     [int(clean_ids[0, t]) for t in sel_scored])))
        nll_b1_ctl = dict(zip(ctl_scored, gather_nll(out_b1["logits_direct"], cb, ob, ctl_scored,
                                                     [int(clean_ids[0, t]) for t in ctl_scored])))

    # 臂 (b2)：源 chunk 行手术（行面；字节不动）
    nll_b2_sel, nll_b2_ctl = {}, {}
    if "b2" in arms and plan.spans:
        src_chunks = {
            int(ca[0, p])
            for _g, p, _r in plan.spans
            if 0 <= int(ca[0, p]) < max_chunks
        }
        n_real = int(out_a["chunks"].chunk_mask[0].sum())
        perm = build_row_perm(src_chunks, n_real)
        restore = patch_store_rows_perm(model, perm)
        try:
            out_b2 = forward_fn(model, source_a, ns)
        finally:
            restore()
        cb2, ob2 = out_b2["chunks"].chunk_ids, out_b2["chunks"].offsets
        nll_b2_sel = dict(zip(sel_scored, gather_nll(out_b2["logits_direct"], cb2, ob2, sel_scored,
                                                     [int(clean_ids[0, t]) for t in sel_scored])))
        nll_b2_ctl = dict(zip(ctl_scored, gather_nll(out_b2["logits_direct"], cb2, ob2, ctl_scored,
                                                     [int(clean_ids[0, t]) for t in ctl_scored])))

    items, sums = [], _zero_sums()
    strong = scan.strong_line
    for role, pos_list, sel_map in (("selected", sel_scored, sel), ("control", ctl_scored, None)):
        for t in pos_list:
            na = nll_a_sel[t] if role == "selected" else nll_a_ctl[t]
            g, p = sel_map[t] if role == "selected" else (b"", -1)
            item = {
                "window_id": window_id,
                "byte_pos": t,
                "role": role,
                "gram": g.hex(),
                "repeat_pos": p,
                "grid_chunk": int(ca[0, t]),
                "grid_slot": int(oa[0, t]),
                "NLL_a": na,
                "NLL_b1": (nll_b1_sel if role == "selected" else nll_b1_ctl).get(t),
                "NLL_b2": (nll_b2_sel if role == "selected" else nll_b2_ctl).get(t),
            }
            items.append(item)
            d1 = item["NLL_b1"] - na if item["NLL_b1"] is not None else None
            d2 = item["NLL_b2"] - na if item["NLL_b2"] is not None else None
            item["delta_b1"] = d1
            item["delta_b2"] = d2
            if role == "selected":
                sums["n_sel"] += 1
                sums["sel_d_b1"] += d1 or 0.0
                sums["sel_d_b2"] += d2 or 0.0
                sums["n_sel_b2"] += int(d2 is not None)
                sums["n_strong"] += int(d1 is not None and d1 >= strong)
            else:
                sums["n_ctl"] += 1
                sums["ctl_d_b1"] += d1 or 0.0
                sums["ctl_d_b2"] += d2 or 0.0
                sums["n_ctl_b2"] += int(d2 is not None)

    return {"status": "ok", "items": items, "sums": sums, "counts": counts}


def _zero_sums() -> dict:
    return {
        "n_sel": 0, "sel_d_b1": 0.0, "sel_d_b2": 0.0, "n_sel_b2": 0, "n_strong": 0,
        "n_ctl": 0, "ctl_d_b1": 0.0, "ctl_d_b2": 0.0, "n_ctl_b2": 0,
    }


# ---------------------------------------------------------------------------
# 聚合：主判读量 + 窗级 bootstrap
# ---------------------------------------------------------------------------


def bootstrap_contrast(window_sums: list[dict], n_boot: int = 2000, seed: int = 20260906,
                       level: float = 0.95) -> dict:
    """主判读量 = mean ΔNLL_b1(选中) − mean ΔNLL_b1(对照)；窗级重抽样 CI。
    逐位 ΔNLL 为冻结模型确定性前向读数，统计性全由抽样端 bootstrap 承担
    （预注册 §4）。"""

    def contrast(sample: list[dict]):
        ns_ = sum(w["n_sel"] for w in sample)
        nc = sum(w["n_ctl"] for w in sample)
        if not ns_ or not nc:
            return None
        return sum(w["sel_d_b1"] for w in sample) / ns_ - sum(w["ctl_d_b1"] for w in sample) / nc

    W = len(window_sums)
    point = contrast(window_sums)
    rng = random.Random(seed)
    boots = []
    for _ in range(n_boot):
        sample = [window_sums[rng.randrange(W)] for _ in range(W)]
        c = contrast(sample)
        if c is not None:
            boots.append(c)
    boots.sort()
    if boots:
        lo = boots[max(0, int((1 - level) / 2 * len(boots)))]
        hi = boots[min(len(boots) - 1, int((1 + level) / 2 * len(boots)) - 1)]
    else:
        lo = hi = None
    return {
        "point": point,
        "ci95_lo": lo,
        "ci95_hi": hi,
        "ci_excludes_zero": bool(point is not None and lo is not None and (lo > 0 or hi < 0)),
        "n_boot": n_boot,
        "n_boot_valid": len(boots),
        "seed": seed,
    }


def verdict(mean_sel: float | None, contrast: dict) -> str:
    """预注册 §4 判读表（冻结 v1.0）。"""
    if mean_sel is None or contrast["point"] is None:
        return "无读数"
    if contrast["point"] < 0:
        return "反常（仪器 bug 或选择图口径错——停，转口径审计）"
    if contrast["ci_excludes_zero"] and mean_sel >= STRONG_LINE_NAT:
        return "必要性实存（强）——剂量打在黑板上，E121 解释 B 成立"
    if contrast["ci_excludes_zero"]:
        return "必要性实存（弱）——剂量部分在板"
    return "剂量未落——E121 改判需求侧误判"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--ckpt", default=DEFAULT_CKPT, help="run dir（resolved_config.json + latest.pt）")
    p.add_argument("--rare-table", default=DEFAULT_RARE_TABLE)
    p.add_argument("--n-windows", type=int, default=500)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--out-dir", default=f"outputs/e122_necessity_book_{time.strftime('%Y%m%d')}")
    p.add_argument("--arms", default="a,b1,b2")
    p.add_argument("--ngram-len", type=int, default=6)
    p.add_argument("--tail", type=int, default=3)
    p.add_argument("--rare-quantile", type=float, default=0.2)
    p.add_argument("--bootstrap", type=int, default=2000)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--strong-line", type=float, default=STRONG_LINE_NAT)
    args = p.parse_args()

    arms = [a.strip() for a in args.arms.split(",") if a.strip()]
    if "a" not in arms:
        raise SystemExit("--arms 必须含基线臂 a（ΔNLL 的参照面）")
    unknown = set(arms) - {"a", "b1", "b2"}
    if unknown:
        raise SystemExit(f"--arms 未知臂: {sorted(unknown)}")
    device = torch.device(
        "cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu"
    )
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    n_table = s1._load_d1_rare_table(args.rare_table)
    pattern_index = build_pattern_index(s1._D1_RARE_TABLE)
    print(f"[e122] rare table {n_table} grams（图案桶 {len(pattern_index)}）", flush=True)

    model, ns, step = load_model(Path(args.ckpt), device)
    assert_cell_keys(ns, model.config)  # 坑 8：缺键/错值 loud fail，不许兜底
    # 任务注入零（预注册 §3 卫生；前向只走 s1_forward，metas 全 None 已零注入，
    # 此处显式清零防下游误读 ns）
    ns.burst_prob = 0
    ns.cloze_prob = 0
    ns.retrieval_prob = 0
    if int(getattr(ns, "bytes_per_chunk", SCAN_CHUNK)) != SCAN_CHUNK:
        raise SystemExit(
            f"bytes_per_chunk={ns.bytes_per_chunk} != 密度账扫描网格 CHUNK={SCAN_CHUNK}"
            "（跨 chunk 条件①定义在 16B 网格上，口径不符响亮拒绝）"
        )
    print(
        f"[e122] ckpt={Path(args.ckpt).name} step={step} device={device.type}"
        f" arms={arms} L={args.ngram_len} T={args.tail} q={args.rare_quantile}",
        flush=True,
    )

    scan = Namespace(ngram_len=args.ngram_len, tail=args.tail, rare_quantile=args.rare_quantile,
                     strong_line=args.strong_line)
    batch_size = max(int(ns.batch_size), 1)
    n_batches = math.ceil(args.n_windows / batch_size)
    batches = build_eval_windows(ns, n_batches)
    masks = build_masks(batches, ns)
    rng = random.Random(args.seed)

    items_path = out_dir / "items.jsonl"
    window_sums: list[dict] = []
    tally = {
        "n_windows_attempted": 0, "n_windows_used": 0, "n_windows_dropped_drift": 0,
        "n_windows_empty": 0,
    }
    totals: dict[str, int] = {}
    wi = 0
    for batch, mbatch in zip(batches, masks):
        for j in range(batch.size(0)):
            if wi >= args.n_windows:
                break
            ids = batch[j]
            cut = int(ids.ne(PAD_ID).sum())
            clean_row = ids[:cut].unsqueeze(0).to(device)
            mask_row = mbatch[j][:cut].unsqueeze(0).to(device)
            rec = run_window(model, ns, clean_row, mask_row, s1._D1_RARE_TABLE, scan,
                             set(arms), rng, pattern_index, wi)
            tally["n_windows_attempted"] += 1
            for k, v in rec["counts"].items():
                totals[k] = totals.get(k, 0) + v
            if rec["status"] == "ok" and rec["sums"]["n_sel"] > 0:
                tally["n_windows_used"] += 1
                window_sums.append(rec["sums"])
                with items_path.open("a", encoding="utf-8") as f:
                    for item in rec["items"]:
                        f.write(json.dumps(item, ensure_ascii=False) + "\n")
            elif rec["status"] == "dropped_drift":
                tally["n_windows_dropped_drift"] += 1
            else:
                tally["n_windows_empty"] += 1
            s = rec["sums"]
            print(
                f"[e122] win {wi:4d} {rec['status']:13s} sel={s['n_sel']:3d} ctl={s['n_ctl']:3d}"
                f" strong={s['n_strong']:3d} ({time.time() - t0:.0f}s)",
                flush=True,
            )
            wi += 1
        if wi >= args.n_windows:
            break

    # 聚合（选中/对照两臂均值差 + 窗级 bootstrap CI + 强命中密度换算）
    n_sel = sum(w["n_sel"] for w in window_sums)
    n_ctl = sum(w["n_ctl"] for w in window_sums)
    mean_sel = sum(w["sel_d_b1"] for w in window_sums) / n_sel if n_sel else None
    mean_ctl = sum(w["ctl_d_b1"] for w in window_sums) / n_ctl if n_ctl else None
    mean_sel_b2 = (
        sum(w["sel_d_b2"] for w in window_sums) / max(sum(w["n_sel_b2"] for w in window_sums), 1)
        if any(w["n_sel_b2"] for w in window_sums) else None
    )
    mean_ctl_b2 = (
        sum(w["ctl_d_b2"] for w in window_sums) / max(sum(w["n_ctl_b2"] for w in window_sums), 1)
        if any(w["n_ctl_b2"] for w in window_sums) else None
    )
    boot = bootstrap_contrast(window_sums, args.bootstrap, args.seed + 1)
    strong_per_window = (
        sum(w["n_strong"] for w in window_sums) / len(window_sums) if window_sums else 0.0
    )
    strong_rate = strong_per_window / DENSITY_SUPERVISED_BPW
    summary = {
        "probe": "E122 跨段必要性账（冻结预注册 v1.0, 2026-09-06）",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "ckpt": {"run": Path(args.ckpt).name, "step": step},
        "rare_table": args.rare_table,
        "params": {
            "n_windows": args.n_windows, "arms": arms, "ngram_len": args.ngram_len,
            "tail": args.tail, "rare_quantile": args.rare_quantile, "seed": args.seed,
            "strong_line_nat": args.strong_line, "scan_chunk": SCAN_CHUNK,
            "eval_mask_seed": getattr(ns, "eval_mask_seed", None),
            "mask_prob": getattr(ns, "mask_prob", None),
        },
        "windows": {
            **tally,
            "drift_drop_rate": round(
                tally["n_windows_dropped_drift"] / max(tally["n_windows_attempted"], 1), 4
            ),
        },
        "selected": {"n": n_sel, "mean_delta_b1": mean_sel, "mean_delta_b2": mean_sel_b2},
        "control": {"n": n_ctl, "mean_delta_b1": mean_ctl, "mean_delta_b2": mean_ctl_b2},
        "contrast_b1": {
            **boot,
            "mean": (mean_sel - mean_ctl) if (mean_sel is not None and mean_ctl is not None) else None,
        },
        "density": {
            "strong_hits_per_window": round(strong_per_window, 4),
            "vs_110_bpw": round(strong_per_window / DENSITY_SUPERVISED_BPW, 4),
            "vs_54_8_bpw_strict": round(strong_per_window / DENSITY_STRICT_BPW, 4),
            "landing_line": round(DENSITY_STRICT_BPW / DENSITY_SUPERVISED_BPW, 4),
            "landing_pass": bool(strong_rate >= DENSITY_STRICT_BPW / DENSITY_SUPERVISED_BPW),
        },
        "exclusions": {
            "mask_hit_selected": totals.get("n_selected_mask_excluded", 0),
            "mask_hit_control": totals.get("n_control_mask_excluded", 0),
            "grid_excluded": totals.get("n_grid_excluded", 0),
            "collateral_selected": totals.get("n_selected_collateral", 0),
            "collateral_control": totals.get("n_control_collateral", 0),
            "selected_unsourced_overlap_skipped": totals.get("n_source_overlap_skipped", 0),
            "control_no_occurrence": totals.get("n_control_no_occurrence", 0),
            "selection_overlap": totals.get("n_selection_overlap", 0),
        },
        "verdict": verdict(mean_sel, boot),
        "b2_note": (
            "b2 不进主判读表（预注册 §4）：ΔNLL_b2 ≈ ΔNLL_b1 → 依赖走显式行索引；"
            "ΔNLL_b2 ≪ ΔNLL_b1 → 依赖被 encoder 隐式混入 own-row。注意 b2 行手术"
            "保留行存在性（长度侧信道容忍，预注册 §5.7）。"
        ),
        "timing_sec": round(time.time() - t0, 1),
    }
    (out_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)
    print(f"[e122] items -> {items_path}", flush=True)


if __name__ == "__main__":
    main()
