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

对照（v1.3a 簇级同体半分，用户裁定 2026-09-06——v1.0 随机自由位对照被口径
审计证伪：每窗 31–55% 字节腐蚀 × 对照位无保护区 → 对比估计量结构性负偏；
v1.2 gram 级半分再被证伪：跨段稀有内容以 1–5 字节移位 gram **簇**存在，
gram 级独立手术只毁源 6 字节、54% 跳过稀释集中处理侧、同簇尾位相邻混杂跨
半）：选中 gram 先按**源 span 重叠链并簇**（union 扫描），簇集洗牌对半——
处理簇全体成员源 span **联合替换**（短语源整体灭活，全有或全无：任一成员
压 used/protected 整簇跳过并计数）；对照簇源**不动**、改在离簇源锚最近合
格位置做与簇成员数等量的**诱饵**替换。两侧计分位同型（跨段稀有 gram 续
尾）、同保护、同腐蚀暴露；对比 = 「源内容整体被打掉 − 同区域等量无关替
换」= 内容特异性依赖。主判读量 =
mean ΔNLL_b1(处理) − mean ΔNLL_b1(对照)，窗级 bootstrap 95% CI。

卫生：eval mask 命中位剔除并计数；b1 分段漂移改「术后窗重映射续计分」（裁定
2026-09-06：目标字节与局部上下文未变，分段响应是模型对手术的合法中介效应，
机械网格噪声由处理/对照对比吸收——逐位记 drifted 布尔进分层稳健性读数，原
「整窗剔除」废止）；两半的重复出现处+续尾全进保护区且**处理源替换同样受保
护区约束**（v1.2 起）；被替换 span 覆盖的计分位按侧伤剔除；落在被置换源
chunk 内的计分位从 b2 分层剔除（对角自读污染，b1 照常计）；任务注入零
（burst/cloze/retrieval 清零）；坑 8 全键断言（缺键 loud fail，禁止
build_model 兜底默认）。

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


def assert_cell_keys(ns, model_config=None, strict: bool = True) -> None:
    """resolved_config（及装载后 model.config）逐键断言；键缺失或值漂移一律
    ValueError 响亮拒绝——build_model 的 getattr 兜底默认会把纯行为静默漂移
    藏进读数（坑 8, 2026-08-29 冒烟事故同族）。

    strict=True（默认，d 格主基座）：五键全按 CELL_KEYS 值断言。
    strict=False（a 格副基座，冻结预注册 §3 规定的次基座）：五键**必须显式在**
    （缺键即拒，禁 build_model 兜底）+ 通用键（seed_source=k / backbone_mode=
    slm）值必须对；行源三键允许世代差（a 格 = index/memory），实际值由调用方
    进 summary 如实记录——放宽只及键值域，不放宽存在性。"""

    universal = {"seed_source": CELL_KEYS["seed_source"], "backbone_mode": CELL_KEYS["backbone_mode"]}
    enforce = CELL_KEYS if strict else universal

    def check(obj, where: str) -> None:
        bad = []
        for key in CELL_KEYS:  # 存在性：两档都全键必查
            if strict or key in universal:
                want = enforce[key]
                got = getattr(obj, key, _MISSING)
                shown = "<键缺失>" if got is _MISSING else repr(got)
                if got != want:
                    bad.append(f"{where}.{key}={shown} != {want!r}")
            elif getattr(obj, key, _MISSING) is _MISSING:
                bad.append(f"{where}.{key}=<键缺失>（a 格亦须显式携带，禁兜底）")
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
    """一窗的 b1 手术单（v1.2）：被替换 span（原 gram、窗内位置、替换 gram）
    + 对照 gram → 诱饵 span 映射 + 计数。"""

    def __init__(self):
        self.spans: list[tuple[bytes, int, bytes]] = []  # (orig_gram, pos, repl)
        self.decoy_span: dict[bytes, list[int]] = {}  # 对照 gram -> 其簇诱饵 spans 下标表
        self.n_control_no_decoy = 0
        self.n_source_overlap_skipped = 0  # v1.3a 起按**簇**计数（全有或全无）
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


def build_source_clusters(sel: dict[int, tuple[bytes, int]], raw: bytes,
                          L: int) -> list[frozenset[bytes]]:
    """选中 gram 按**源 span（最早出现处 L 字节）重叠链**并簇（区间扫描合并）：
    跨段重复稀有内容以簇存在——同一稀有词/短语的 1–L-1 字节移位 gram 家族源
    span 互相重叠（审计 2026-09-06：v1.2 冒烟 54% 处理源跳过的真身）。v1.3a
    裁定：split 与手术的诚实单位是簇不是 gram（同簇尾位 1 字节相邻、内容依赖
    同一，不许分进两半；簇外源 span 才可独立灭活）。"""
    grams = sorted({g for g, _p in sel.values()})
    spans = sorted((raw.find(g), g) for g in grams)  # p0 升序
    clusters: list[list[bytes]] = []
    cur: list[bytes] = []
    cur_hi = -1
    for p0, g in spans:
        if cur and p0 < cur_hi:
            cur.append(g)
            cur_hi = max(cur_hi, p0 + L)
        else:
            if cur:
                clusters.append(cur)
            cur, cur_hi = [g], p0 + L
    if cur:
        clusters.append(cur)
    return [frozenset(c) for c in clusters]


def split_selected_clusters(sel: dict[int, tuple[bytes, int]], raw: bytes,
                            rng: random.Random, L: int):
    """v1.3a 簇级同体半分（用户裁定 2026-09-06）：簇集洗牌对半——处理簇全体
    成员源联合替换，对照簇源不动+等长诱饵替换。奇数簇时处理半多一簇。
    返回 (处理 gram 集, 对照 gram 集, 处理簇表, 对照簇表)。"""
    clusters = sorted(build_source_clusters(sel, raw, L), key=lambda c: min(c))
    rng.shuffle(clusters)
    k = (len(clusters) + 1) // 2
    treat_cl, ctrl_cl = clusters[:k], clusters[k:]
    treat = frozenset().union(*treat_cl) if treat_cl else frozenset()
    ctrl = frozenset().union(*ctrl_cl) if ctrl_cl else frozenset()
    return treat, ctrl, treat_cl, ctrl_cl


def plan_window_surgery(raw: bytes, rare: set[bytes], sel: dict[int, tuple[bytes, int]],
                        treat_grams: frozenset[bytes], ctrl_grams: frozenset[bytes],
                        table: dict[bytes, int],
                        pattern_index: dict[int, list[bytes]], rng: random.Random,
                        L: int, tail: int,
                        treat_clusters: list[frozenset[bytes]] | None = None,
                        ctrl_clusters: list[frozenset[bytes]] | None = None) -> SurgeryPlan:
    """一窗手术单（v1.3a 簇级同体半分，用户裁定 2026-09-06——v1.0 随机自由位
    对照被口径审计证伪（高腐蚀×保护不对称→对比结构性负偏）；v1.2 gram 级半分
    再被证伪（跨段稀有内容以移位 gram 簇存在，gram 级独立手术只毁源 6 字节、
    簇内欠强+54% 跳过稀释集中处理侧、同簇尾位 1 字节相邻跨半混杂）。

    处理簇：全体成员源 span（各自最早出现处）**联合替换**——短语源整体灭活
    （簇内重叠 span 顺序写入，交叠字节以后写为准，接缝处图案匹配放宽、如实
    记录）；任一成员源 span 压 used/protected → **整簇跳过**（全有或全无，
    其续尾位仍计分、如实稀释，两侧同款对称）并计数。
    对照簇：源**不动**；诱饵 = 离簇源锚（成员源最小 p0）最近的合格稀有表出现
    处起、与簇成员数等量的逐处替换——几何匹配「源区域被扰动」噪音，内容非
    特异。诱饵合格域：非任何选中 gram（防毁掉两侧自身依赖）、未被替换过、
    不压 used/protected。零合格出现处 → 整簇无诱饵计数。
    保护区 = 两半的重复出现处+续尾（全部计分位及其 gram 出现处），处理源与
    诱饵同受约束。原串互为禁集（替换不落回任何被替换原串，杜绝串别名）。"""
    plan = SurgeryPlan()
    n = len(raw)
    used: list[tuple[int, int]] = []
    sel_originals = {g for g, _p in sel.values()}
    # 保护区：两半的（重复）出现处 + 续尾——全部计分位及其 gram 出现处
    protected = [(p, min(p + L + tail, n)) for _g, p in set(sel.values())]
    if treat_clusters is None or ctrl_clusters is None:
        treat_clusters = [c for c in (build_source_clusters(sel, raw, L))
                          if c <= treat_grams]
        ctrl_clusters = [c for c in (build_source_clusters(sel, raw, L))
                         if c <= ctrl_grams]

    # 1) 处理簇：全体成员源联合替换（全有或全无）
    for cluster in sorted(treat_clusters, key=lambda c: min(c)):
        members = sorted(cluster, key=lambda g: raw.find(g))  # 源位升序，接缝确定
        member_spans = [(g, raw.find(g)) for g in members]
        if any(
            _overlaps((p0, p0 + L), used) or _overlaps((p0, p0 + L), protected)
            for _g, p0 in member_spans
        ):
            plan.n_source_overlap_skipped += 1  # 整簇跳过（如实稀释+计数）
            continue
        for g, p0 in member_spans:
            base = sel_originals | set(plan.replacements) | set(plan.replacements.values())
            r = pick_replacement(g, pattern_index, rng, forbidden=frozenset(base - {g}),
                                 window=raw)
            plan.replacements[g] = r
            plan.spans.append((g, p0, r))
            used.append((p0, p0 + L))

    # 2) 对照簇：源不动；诱饵 = 离簇源锚最近合格处起等量逐处替换
    occ_table = table_occurrences(raw, L, table)
    for cluster in sorted(ctrl_clusters, key=lambda c: min(c)):
        anchor = min(raw.find(g) for g in cluster)
        eligible = sorted(
            (
                (g2, p2)
                for g2, p2 in occ_table
                if g2 not in sel_originals
                and g2 not in plan.replacements
                and not _overlaps((p2, p2 + L), used)
                and not _overlaps((p2, p2 + L), protected)
            ),
            key=lambda gp: abs(gp[1] - anchor),
        )
        if not eligible:
            plan.n_control_no_decoy += 1
            continue
        picked = []
        for g2, p2 in eligible:
            if len(picked) >= len(cluster):
                break
            if _overlaps((p2, p2 + L), used):
                continue  # 贪心途中 used 在长，逐处复查
            base = sel_originals | set(plan.replacements) | set(plan.replacements.values())
            r = pick_replacement(g2, pattern_index, rng, forbidden=frozenset(base - {g2}),
                                 window=raw)
            plan.replacements[g2] = r
            picked.append(len(plan.spans))
            plan.spans.append((g2, p2, r))
            used.append((p2, p2 + L))
        for g in cluster:
            plan.decoy_span[g] = picked  # 对照 gram -> 其簇的诱饵 span 下标表
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
    """b1 手术后 chunk 网格在计分位漂移的位清单（v1.1 修订 2026-09-06：整窗剔除
    废止，漂移位重映射续计分并逐位记 drifted 布尔进分层读数）。"""
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
    tgt = torch.tensor(target_ids, dtype=torch.long,
                       device=picked.device).clamp(min=0, max=257)  # CUDA 线靶同设备
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
               forward_fn=None, split_override: tuple[frozenset, frozenset] | None = None) -> dict:
    """三臂同窗：返回 {status, items, sums, counts, split}。status ∈ ok / empty。
    漂移门（2026-09-06 裁定：重映射续计分，整窗剔除废止）——目标字节与局部
    上下文未变，分段响应是模型对手术的合法中介效应，机械网格噪声由处理/对照
    对比吸收：b1 术后在术后窗重算格位取 NLL，逐位记 drifted 布尔进分层读数。
    v1.2 同体半分对照（用户裁定 2026-09-06）：split = 处理/对照 gram 分组审计
    （正册逐窗可复诊）；split_override 为复现/测试钩子（钉死分组，绕过 rng）。
    clean_ids/byte_mask: (1, T)（已剥 PAD，模型设备）。"""
    forward_fn = forward_fn or default_forward
    L, tail, quantile = scan.ngram_len, scan.tail, scan.rare_quantile
    max_chunks, max_span = int(ns.max_chunks), int(ns.max_span)
    raw = bytes(int(x) - BYTE_OFFSET for x in clean_ids[0].tolist())
    n = len(raw)

    counts = {
        "n_selected_mask_excluded": 0, "n_control_mask_excluded": 0,
        "n_grid_excluded": 0, "n_post_grid_excluded": 0,
        "n_selected_collateral": 0, "n_control_collateral": 0,
        "n_b2_own_chunk_selected": 0, "n_b2_own_chunk_control": 0,
        "n_control_no_decoy": 0,
        "n_treatment_clusters_skipped": 0, "n_selection_overlap": 0,
        "n_treatment_grams": 0, "n_control_grams": 0,
        "n_treatment_clusters": 0, "n_control_clusters": 0,
        "hit_grams": 0, "offtable_grams": 0,
    }
    empty = {"status": "empty", "items": [], "sums": _zero_sums(), "counts": counts,
             "split": None}
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

    # v1.3a 簇级同体半分（用户裁定 2026-09-06）：跨段稀有内容以移位 gram 簇
    # 存在——split/手术单位=簇；两半续尾位全部计分（同型同保护同腐蚀暴露）。
    if split_override is not None:
        treat_grams, ctrl_grams = split_override
        treat_cl = [c for c in build_source_clusters(sel, raw, L) if c <= treat_grams]
        ctrl_cl = [c for c in build_source_clusters(sel, raw, L) if c <= ctrl_grams]
    else:
        treat_grams, ctrl_grams, treat_cl, ctrl_cl = split_selected_clusters(sel, raw, rng, L)
    counts["n_treatment_grams"] = len(treat_grams)
    counts["n_control_grams"] = len(ctrl_grams)
    counts["n_treatment_clusters"] = len(treat_cl)
    counts["n_control_clusters"] = len(ctrl_cl)
    plan = plan_window_surgery(raw, rare, sel, treat_grams, ctrl_grams, table,
                               pattern_index, rng, L, tail,
                               treat_clusters=treat_cl, ctrl_clusters=ctrl_cl)
    counts["n_control_no_decoy"] = plan.n_control_no_decoy
    counts["n_treatment_clusters_skipped"] = plan.n_source_overlap_skipped
    treat_positions = sorted(t for t, (g, _p) in sel.items() if g in treat_grams)
    ctl_positions = sorted(t for t, (g, _p) in sel.items() if g in ctrl_grams)
    split_audit = {
        "treatment_clusters": [sorted(g.hex() for g in c) for c in
                               sorted(treat_cl, key=lambda c: min(c))],
        "control_clusters": [sorted(g.hex() for g in c) for c in
                             sorted(ctrl_cl, key=lambda c: min(c))],
        "treatment_replaced": sorted(g.hex() for g in treat_grams if g in plan.replacements),
        "control_decoy_placed": sorted(g.hex() for g in plan.decoy_span),
    }

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

    sel_valid, _sel_tgt = score_set(treat_positions)
    ctl_valid, _ctl_tgt = score_set(ctl_positions)
    counts["n_selected_mask_excluded"] = sum(1 for t in treat_positions if bool(byte_mask[0, t]))
    counts["n_control_mask_excluded"] = sum(1 for t in ctl_positions if bool(byte_mask[0, t]))
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

    # 臂 (b1)：外科替换（字节面）。术后窗重映射续计分（漂移门裁定 2026-09-06）：
    # 目标字节逻辑位与内容不变，在其术后新格位取 NLL；漂移位进分层读数。
    nll_b1_sel, nll_b1_ctl = {}, {}
    drift_flags: dict[int, bool] = {}
    if "b1" in arms:
        raw_b1 = plan.apply(raw)
        ids_b1 = torch.tensor([[b + BYTE_OFFSET for b in raw_b1]], dtype=clean_ids.dtype,
                              device=clean_ids.device)
        source_b1 = ids_b1.masked_fill(byte_mask.bool(), MASK_ID)
        out_b1 = forward_fn(model, source_b1, ns)
        cb, ob = out_b1["chunks"].chunk_ids, out_b1["chunks"].offsets
        _c1, _s1, valid_b = byte_to_grid_slots(cb, ob, byte_mask, max_chunks, max_span)
        sel_b1 = [t for t in sel_scored if bool(valid_b[0, t])]
        ctl_b1 = [t for t in ctl_scored if bool(valid_b[0, t])]
        counts["n_post_grid_excluded"] = (len(sel_scored) - len(sel_b1)) + (len(ctl_scored) - len(ctl_b1))
        for t in drifted_positions(ca, oa, cb, ob, sel_b1 + ctl_b1):
            drift_flags[t] = True
        nll_b1_sel = dict(zip(sel_b1, gather_nll(out_b1["logits_direct"], cb, ob, sel_b1,
                                                 [int(clean_ids[0, t]) for t in sel_b1])))
        nll_b1_ctl = dict(zip(ctl_b1, gather_nll(out_b1["logits_direct"], cb, ob, ctl_b1,
                                                 [int(clean_ids[0, t]) for t in ctl_b1])))

    # 臂 (b2)：源 chunk 行手术（行面；字节不动）。读数面 = completion/backbone
    # （logits_backbone）——slm direct 面上 chunk c 的解码只条件于自身状态行
    # v_rows[c]（_slm_forward: cond_direct=dec_in(v_rows)+pos），行手术对非源
    # chunk 的 direct 读数恒等 0，路径 B（backbone block1 跨行因果 cross-read,
    # 预注册 §2）只在 backbone 面出读数。落在被置换源 chunk 内的计分位从 b2
    # 分层剔除（对角自读污染，裁定 2026-09-06——b1 不受影响照常计）。
    nll_b2_sel, nll_b2_ctl = {}, {}
    nll_b2_base_sel, nll_b2_base_ctl = {}, {}
    b2_on = "b2" in arms and bool(plan.spans)
    b2_keep_sel, b2_keep_ctl = sel_scored, ctl_scored
    if b2_on:
        # v1.2：行手术只处置**处理半**源 chunk（诱饵手术是 b1 字节面噪音匹配件，
        # 不进 b2）；对照半源行保持不动——b2 对比 = 处理续尾 vs 对照续尾同型几何
        src_chunks = {
            int(ca[0, p])
            for g, p, _r in plan.spans
            if g in treat_grams and 0 <= int(ca[0, p]) < max_chunks
        }
        b2_keep_sel = [t for t in sel_scored if int(ca[0, t]) not in src_chunks]
        b2_keep_ctl = [t for t in ctl_scored if int(ca[0, t]) not in src_chunks]
        counts["n_b2_own_chunk_selected"] = len(sel_scored) - len(b2_keep_sel)
        counts["n_b2_own_chunk_control"] = len(ctl_scored) - len(b2_keep_ctl)
        n_real = int(out_a["chunks"].chunk_mask[0].sum())
        perm = build_row_perm(src_chunks, n_real)
        restore = patch_store_rows_perm(model, perm)
        try:
            out_b2 = forward_fn(model, source_a, ns)
        finally:
            restore()
        cb2, ob2 = out_b2["chunks"].chunk_ids, out_b2["chunks"].offsets
        # ΔNLL_b2 = 背骨面术后 − 背骨面基线（同面对照）
        nll_b2_base_sel = dict(zip(b2_keep_sel, gather_nll(out_a["logits_backbone"], ca, oa, b2_keep_sel,
                                                           [int(clean_ids[0, t]) for t in b2_keep_sel])))
        nll_b2_base_ctl = dict(zip(b2_keep_ctl, gather_nll(out_a["logits_backbone"], ca, oa, b2_keep_ctl,
                                                           [int(clean_ids[0, t]) for t in b2_keep_ctl])))
        nll_b2_sel = dict(zip(b2_keep_sel, gather_nll(out_b2["logits_backbone"], cb2, ob2, b2_keep_sel,
                                                      [int(clean_ids[0, t]) for t in b2_keep_sel])))
        nll_b2_ctl = dict(zip(b2_keep_ctl, gather_nll(out_b2["logits_backbone"], cb2, ob2, b2_keep_ctl,
                                                      [int(clean_ids[0, t]) for t in b2_keep_ctl])))
        # NLL_b2/NLL_b2_base 存原始读数（backbone 面），Δ 在 item 循环内同面相减
        # ——与 b1 的「存原始、算 delta」口径一致，items.jsonl 保留可审计原值。

    items, sums = [], _zero_sums()
    strong = scan.strong_line
    for role, pos_list in (("selected", sel_scored), ("control", ctl_scored)):
        keep_b2 = b2_keep_sel if role == "selected" else b2_keep_ctl
        for t in pos_list:
            na = nll_a_sel[t] if role == "selected" else nll_a_ctl[t]
            g, p = sel[t]  # v1.2：两半计分位同型（都是跨段稀有 gram 续尾）
            item = {
                "window_id": window_id,
                "byte_pos": t,
                "role": role,
                "gram": g.hex(),
                "repeat_pos": p,
                "grid_chunk": int(ca[0, t]),
                "grid_slot": int(oa[0, t]),
                "drifted": drift_flags.get(t, False),
                "b2_own_chunk_excluded": (t not in keep_b2) if b2_on else (False if "b2" in arms else None),
                "NLL_a": na,
                "NLL_b1": (nll_b1_sel if role == "selected" else nll_b1_ctl).get(t),
                "NLL_b2": (nll_b2_sel if role == "selected" else nll_b2_ctl).get(t),
                "NLL_b2_base": (nll_b2_base_sel if role == "selected" else nll_b2_base_ctl).get(t),
            }
            if role == "control":  # 诱饵手术审计（对照源保持不动）
                ds = plan.decoy_span.get(g)
                item["decoy_gram"] = plan.spans[ds[0]][0].hex() if ds else None
                item["decoy_pos"] = plan.spans[ds[0]][1] if ds else None
                item["decoy_n_spans"] = len(ds) if ds else 0
            items.append(item)
            d1 = item["NLL_b1"] - na if item["NLL_b1"] is not None else None
            # b2 读数面=backbone（行手术对非源 chunk 的 direct 面恒等 0）：同面基线相减
            d2 = (item["NLL_b2"] - item["NLL_b2_base"]) if item["NLL_b2"] is not None else None
            item["delta_b1"] = d1
            item["delta_b2"] = d2
            drifted = bool(item["drifted"])
            if role == "selected":
                sums["n_sel"] += 1
                sums["sel_d_b1"] += d1 or 0.0
                sums["sel_d_b2"] += d2 or 0.0
                sums["n_sel_b2"] += int(d2 is not None)
                sums["n_strong"] += int(d1 is not None and d1 >= strong)
                sums["n_sel_drift"] += int(d1 is not None and drifted)
                sums["sel_d_b1_drift"] += d1 if (d1 is not None and drifted) else 0.0
                sums["n_sel_nodrift"] += int(d1 is not None and not drifted)
                sums["sel_d_b1_nodrift"] += d1 if (d1 is not None and not drifted) else 0.0
            else:
                sums["n_ctl"] += 1
                sums["ctl_d_b1"] += d1 or 0.0
                sums["ctl_d_b2"] += d2 or 0.0
                sums["n_ctl_b2"] += int(d2 is not None)
                sums["n_ctl_drift"] += int(d1 is not None and drifted)
                sums["ctl_d_b1_drift"] += d1 if (d1 is not None and drifted) else 0.0
                sums["n_ctl_nodrift"] += int(d1 is not None and not drifted)
                sums["ctl_d_b1_nodrift"] += d1 if (d1 is not None and not drifted) else 0.0

    return {"status": "ok", "items": items, "sums": sums, "counts": counts,
            "split": split_audit}


def _zero_sums() -> dict:
    return {
        "n_sel": 0, "sel_d_b1": 0.0, "sel_d_b2": 0.0, "n_sel_b2": 0, "n_strong": 0,
        "n_sel_drift": 0, "sel_d_b1_drift": 0.0, "n_sel_nodrift": 0, "sel_d_b1_nodrift": 0.0,
        "n_ctl": 0, "ctl_d_b1": 0.0, "ctl_d_b2": 0.0, "n_ctl_b2": 0,
        "n_ctl_drift": 0, "ctl_d_b1_drift": 0.0, "n_ctl_nodrift": 0, "ctl_d_b1_nodrift": 0.0,
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
    p.add_argument("--data-path", default=None,
                   help="覆盖 resolved_config 的 data_path（远端语料路径与老 config "
                        "Windows 路径不同时用；缺省不覆盖）")
    p.add_argument("--cell-relaxed", action="store_true",
                   help="a 格副基座档：五键仍须显式在+通用键（seed_source/backbone_mode）"
                        "值必须对，行源三键允许世代差并如实入 summary（默认 strict=d 格全值）")
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
    assert_cell_keys(ns, model.config, strict=not args.cell_relaxed)  # 坑 8：缺键/错值 loud fail，不许兜底
    cell_actual = {k: getattr(ns, k, None) for k in CELL_KEYS}
    if args.data_path:
        ns.data_path = args.data_path
    if not Path(ns.data_path).exists():
        raise SystemExit(f"data_path 不存在: {ns.data_path}（--data-path 覆盖或修 resolved_config）")
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
    splits_path = out_dir / "splits.jsonl"  # v1.2 逐窗处理/对照分组审计
    window_sums: list[dict] = []
    tally = {"n_windows_attempted": 0, "n_windows_used": 0, "n_windows_empty": 0}
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
                with splits_path.open("a", encoding="utf-8") as f:
                    f.write(json.dumps({"window_id": wi, **rec["split"]},
                                       ensure_ascii=False) + "\n")
            else:
                tally["n_windows_empty"] += 1
            s = rec["sums"]
            print(
                f"[e122] win {wi:4d} {rec['status']:5s} sel={s['n_sel']:3d} ctl={s['n_ctl']:3d}"
                f" strong={s['n_strong']:3d} drift={s['n_sel_drift']:3d} ({time.time() - t0:.0f}s)",
                flush=True,
            )
            wi += 1
        if wi >= args.n_windows:
            break

    # 聚合（选中/对照两臂均值差 + 窗级 bootstrap CI + 漂移分层 + 强命中密度换算）
    n_sel = sum(w["n_sel"] for w in window_sums)
    n_ctl = sum(w["n_ctl"] for w in window_sums)
    mean_sel = sum(w["sel_d_b1"] for w in window_sums) / n_sel if n_sel else None
    mean_ctl = sum(w["ctl_d_b1"] for w in window_sums) / n_ctl if n_ctl else None

    def _strat(role: str, key: str) -> dict:
        nk, sk = f"n_{role}_{key}", f"{role}_d_b1_{key}"
        n_ = sum(w[nk] for w in window_sums)
        return {
            "n": n_,
            "mean_delta_b1": (sum(w[sk] for w in window_sums) / n_) if n_ else None,
        }

    sel_drift, sel_nodrift = _strat("sel", "drift"), _strat("sel", "nodrift")
    ctl_drift, ctl_nodrift = _strat("ctl", "drift"), _strat("ctl", "nodrift")
    drift_stratification = {
        "selected": {"drifted": sel_drift, "non_drifted": sel_nodrift},
        "control": {"drifted": ctl_drift, "non_drifted": ctl_nodrift},
        "contrast_drifted": (
            sel_drift["mean_delta_b1"] - ctl_drift["mean_delta_b1"]
            if sel_drift["mean_delta_b1"] is not None and ctl_drift["mean_delta_b1"] is not None
            else None
        ),
        "contrast_non_drifted": (
            sel_nodrift["mean_delta_b1"] - ctl_nodrift["mean_delta_b1"]
            if sel_nodrift["mean_delta_b1"] is not None and ctl_nodrift["mean_delta_b1"] is not None
            else None
        ),
        "note": "漂移门裁定（2026-09-06）：术后窗重映射续计分，drifted=术前术后格位变化位；分层只作稳健性读数",
    }
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
    # v1.2 同体半分的密度锚折算（用户裁定 2026-09-06）：处理半只覆盖 D1 监督集
    # 的 realized 份额 f = n_sel/(n_sel+n_ctl)——强命中原始口径按 1/f 折算回全集
    # 当量再对 54.8（=110 监督字节/窗 × 50% 落点线）判算术关自洽
    treat_frac = (n_sel / (n_sel + n_ctl)) if (n_sel + n_ctl) else None
    strong_full_equiv = (strong_per_window / treat_frac) if treat_frac else None
    summary = {
        "probe": "E122 跨段必要性账（冻结预注册 v1.0 + v1.1 漂移门 + v1.3a 簇级同体半分对照, 2026-09-06）",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "ckpt": {"run": Path(args.ckpt).name, "step": step},
        "cell_keys_actual": cell_actual,
        "rare_table": args.rare_table,
        "params": {
            "n_windows": args.n_windows, "arms": arms, "ngram_len": args.ngram_len,
            "tail": args.tail, "rare_quantile": args.rare_quantile, "seed": args.seed,
            "strong_line_nat": args.strong_line, "scan_chunk": SCAN_CHUNK,
            "eval_mask_seed": getattr(ns, "eval_mask_seed", None),
            "mask_prob": getattr(ns, "mask_prob", None),
        },
        "windows": {**tally},
        "selected": {"n": n_sel, "mean_delta_b1": mean_sel, "mean_delta_b2": mean_sel_b2},
        "control": {"n": n_ctl, "mean_delta_b1": mean_ctl, "mean_delta_b2": mean_ctl_b2},
        "contrast_b1": {
            **boot,
            "mean": (mean_sel - mean_ctl) if (mean_sel is not None and mean_ctl is not None) else None,
        },
        "drift_stratification": drift_stratification,
        "density": {
            # 判读主锚（裁定 2026-09-06）：强命中字节/窗全集当量 ≥ 54.8（算术关
            # 自洽原始形式）；原始口径（处理半）与份额 f 同报
            "strong_bytes_per_window": round(strong_per_window, 4),
            "treatment_share_f": round(treat_frac, 4) if treat_frac is not None else None,
            "strong_full_set_equivalent": (round(strong_full_equiv, 4)
                                           if strong_full_equiv is not None else None),
            "landing_pass_absolute": bool(strong_full_equiv is not None
                                          and strong_full_equiv >= DENSITY_STRICT_BPW),
            "vs_110_bpw": (round(strong_full_equiv / DENSITY_SUPERVISED_BPW, 4)
                           if strong_full_equiv is not None else None),
            "vs_54_8_bpw_strict": (round(strong_full_equiv / DENSITY_STRICT_BPW, 4)
                                   if strong_full_equiv is not None else None),
            "landing_line_ratio": round(DENSITY_STRICT_BPW / DENSITY_SUPERVISED_BPW, 4),
        },
        "exclusions": {
            "mask_hit_selected": totals.get("n_selected_mask_excluded", 0),
            "mask_hit_control": totals.get("n_control_mask_excluded", 0),
            "grid_excluded": totals.get("n_grid_excluded", 0),
            "post_surgery_grid_excluded": totals.get("n_post_grid_excluded", 0),
            "collateral_selected": totals.get("n_selected_collateral", 0),
            "collateral_control": totals.get("n_control_collateral", 0),
            "b2_own_chunk_selected": totals.get("n_b2_own_chunk_selected", 0),
            "b2_own_chunk_control": totals.get("n_b2_own_chunk_control", 0),
            "treatment_clusters_skipped": totals.get("n_treatment_clusters_skipped", 0),
            "control_no_decoy": totals.get("n_control_no_decoy", 0),
            "selection_overlap": totals.get("n_selection_overlap", 0),
            "treatment_grams": totals.get("n_treatment_grams", 0),
            "control_grams": totals.get("n_control_grams", 0),
            "treatment_clusters": totals.get("n_treatment_clusters", 0),
            "control_clusters": totals.get("n_control_clusters", 0),
        },
        "verdict": verdict(mean_sel, boot),
        "b2_note": (
            "b2 不进主判读表（预注册 §4）：ΔNLL_b2 ≈ ΔNLL_b1 → 依赖走显式行索引；"
            "ΔNLL_b2 ≪ ΔNLL_b1 → 依赖被 encoder 隐式混入 own-row。行手术保留行存在性"
            "（长度侧信道容忍，预注册 §5.7）；v1.2 起行手术只处置处理半源 chunk，"
            "落在被置换源 chunk 内的计分位从 b2 分层剔除（对角自读污染，裁定 "
            "2026-09-06，b1 照常计）。"
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
