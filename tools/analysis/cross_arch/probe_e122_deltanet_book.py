"""E122 跨段必要性账 · DeltaNet 跨架构复证仪器（标准开源线性注意力上的同构移植）。

目的（审稿防御件）：FLUED 自家模型的多臂证据显示线性状态通道「写入内容但解码
端近乎读不出」（读者类墙）。本仪器把 E122 簇级同体半分对照设计
（tools/analysis/v3_6/probe_e122_necessity_book.py，冻结预注册 v1.0–v1.3a）移植
到社区标准架构 DeltaNet（fla-hub/delta_net-1.3B-100B，FLA chunked DeltaNet，
token 级 Mistral 系 tokenizer），在非自造架构上复证同一现象，防审稿死法二
「这是你们架构的失败不是线性注意力的性质」。

移植设计（四条施工注记 = 硬约束）：
1. 遮蔽形态换锚：纯线性架构无窗内注意力可遮，遮蔽落**输入侧**——span 替换为
   同 token 数的诱饵 token 序列。DeltaNet 是 token 级（Mistral 系 tokenizer），
   粒度 = token span；gram 概念映射为 token 级 n-gram（n=2-3，按 tokenizer 后
   序列算）。
2. 诱饵合格域条款（第一天就在）：诱饵替换落点集合 ∩ 任何源 span 集合 = ∅，
   且「源 span」按 E122 红队血训（旧贪心把诱饵压在对照簇的移位兄弟源上，
   87.6% 压中）取最强口径：**任何被测 gram 家族的任何出现区间**（最早出现处、
   重复出现处、移位兄弟压线区间）都不可作为诱饵落点，且诱饵内容本身（含拼接
   缝）不得产生任何被测 n-gram 家族成员。仪器逐窗落审计字段（源 span 列表 /
   诱饵落点列表 / 两者距离），落点压源即 RuntimeError 响亮，并有对抗单测锁定
   零压源（tests/test_e122_deltanet_book.py）。
3. 同卷纪律：窗从语料**顺序**抽取——纯文本按字节切 window_bytes(默认 4096)B
   窗，utf-8(errors='replace') 解码后 tokenize（tokenizer 默认加 BOS），截到
   max_tokens；窗定义与语料前缀 SHA256 全文落 summary.json，供日后与我们
   44M 模型同窗对拍；跨模型只比方向不比绝对值（词表/分数面不同，绝对值不可
   比）。
4. 判读口径与 E122 同构：主判读量 = mean ΔNLL(处理) − mean ΔNLL(对照)
   （ΔNLL = 术后 − 术基线，逐位 fp32、无 autocast），窗级 bootstrap 95% CI
   （默认 2000 次重采样），+ 强响应尾（ΔNLL ≥ strong_line(1 nat) 位点比例）；
   判序 CI 在先（E122 收官裁定 2026-09-06）。

与 E122 的结构差（如实记录，供跨架构并表）：
- 无 b2 行手术臂：DeltaNet 无显式分块状态行接口可外科置换，只跑基线 a + 输入
  侧手术 b1 两臂；簇级同体半分对照结构原样保留。
- 无格位漂移概念：token-for-token 等长替换，计分位在两臂间**位置恒定**，ΔNLL
  逐位直接可比，无需 E122 的术后重映射续计分与 drifted 分层。
- 「跨段」定义 = token 段（--segment-tokens，默认 256）：gram 出现段**严格晚
  于**其最早出现段才算跨段重复（E122 的 16B chunk 网格 → token 段网格）。
- 稀有表 = 开跑前对语料前 --table-windows 窗的 token n-gram 计数扫描（E122 的
  D1 rare table 同角色，表按 int 打包有界）；替换池 = 表内最稀有
  --pool-quantile 档。
- 硬件指纹（AGENTS 坑 11 纪律）：summary 记 GPU/torch/fla/transformers/dtype，
  体制判词一律「同机同 env 内成立」。

Usage:
  python tools/analysis/cross_arch/probe_e122_deltanet_book.py \
      --model-path /root/autodl-tmp/models/delta_net-1.3B-100B \
      --corpus /root/autodl-tmp/corpus/corpus_v3.txt \
      --n-windows 40 --device cuda \
      --out-dir /root/autodl-tmp/outputs/e122_deltanet_book_<date>
  CPU 冒烟: --device cpu --n-windows 2
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import time
from pathlib import Path

import torch

# 判读线（与 E122 冻结 v1.0 同源：唯一自由数 = 1.0 nat，弱/无分界 = bootstrap CI）
STRONG_LINE_NAT = 1.0


# ---------------------------------------------------------------------------
# gram 编码：稀有表用 int 打包（定长 n 的多项式基 V，保序；核心逻辑一律 tuple）
# ---------------------------------------------------------------------------


def pack_gram(g, v: int) -> int:
    """定长 n-gram → int（多项式基 v）。仅在同长度 gram 之间使用（表/池定长）。"""
    h = 0
    for t in g:
        h = h * v + t
    return h


def unpack_gram(h: int, n: int, v: int) -> tuple[int, ...]:
    g = []
    for _ in range(n):
        g.append(h % v)
        h //= v
    return tuple(reversed(g))


def find_first(ids: list[int], g) -> int:
    """gram（token 元组）在窗内的最早出现位置；不在则 -1。"""
    n = len(g)
    t0 = g[0]
    for p in range(len(ids) - n + 1):
        if ids[p] == t0 and tuple(ids[p:p + n]) == g:
            return p
    return -1


# ---------------------------------------------------------------------------
# 选择链：跨段扫描 → 稀有档 → 续尾选中位（E122 同语义的 token 段同构）
# ---------------------------------------------------------------------------


def cross_segment_occurrences(ids: list[int], n: int, seg_tokens: int) -> dict[tuple, list[int]]:
    """{gram: [跨段重复出现位置]}——出现段严格晚于该 gram 最早出现段才算
    （E122 密度账 cross_chunk_occurrences 的 token 同构：CHUNK→seg_tokens、
    bytes→token 元组）。同段内重复不计。"""
    first_seg: dict[tuple, int] = {}
    occ: dict[tuple, list[int]] = {}
    for p in range(0, len(ids) - n + 1):
        g = tuple(ids[p:p + n])
        c = p // seg_tokens
        fc = first_seg.get(g)
        if fc is None:
            first_seg[g] = c
        elif fc < c:
            occ.setdefault(g, []).append(p)
    return occ


def select_rare_grams(occ: dict[tuple, list[int]], table: dict[int, int],
                      quantile: float, v: int) -> tuple[set[tuple], int]:
    """镜像 train_v36_s1._d1_select_rare_grams：窗内命中 gram 按语料表计数升序取
    最稀有 quantile 档（floor，平局按 (计数, gram) 稳定排序）。表中缺席的命中
    视为非稀有（诚实边界），计数返回。返回 (稀有 gram 集, 表外命中 gram 数)。"""
    hits = list(occ.keys())
    k = int(len(hits) * quantile)
    if k <= 0:
        return set(), 0
    counted: list[tuple[int, tuple]] = []
    off_table = 0
    for g in hits:
        c = table.get(pack_gram(g, v))
        if c is None:
            off_table += 1
        else:
            counted.append((c, g))
    if not counted:
        return set(), off_table
    counted.sort()
    return {g for _c, g in counted[:k]}, off_table


def select_tail_positions(occ: dict[tuple, list[int]], rare: set[tuple], n: int,
                          tail: int, tk: int) -> tuple[dict[int, tuple[tuple, int]], int]:
    """选中位 = 稀有命中 gram 跨段重复出现处起的 T 个续尾 token（位置 p+n ..
    p+n+tail-1，与 E122 select_tail_positions 同一 range 语义，窗沿截断）。
    返回 (token_pos -> (gram, 重复出现 p), 重叠计数)。"""
    sel: dict[int, tuple[tuple, int]] = {}
    overlap = 0
    for g in sorted(rare):
        for p in occ.get(g, ()):
            for t in range(p + n, min(p + n + tail, tk)):
                if t in sel:
                    overlap += 1
                    continue
                sel[t] = (g, p)
    return sel, overlap


def build_source_clusters(sel: dict[int, tuple[tuple, int]], ids: list[int],
                          n: int) -> list[frozenset[tuple]]:
    """选中 gram 按**源 span（最早出现处 n 个 token）重叠链**并簇（区间扫描合并）
    ——E122 build_source_clusters 的 token 同构：同一短语的移位 n-gram 家族源
    span 互相重叠成簇；split/手术的诚实单位是簇不是 gram（同簇尾位相邻、内容
    依赖同一，不许分进两半）。"""
    grams = sorted({g for g, _p in sel.values()})
    spans = sorted((find_first(ids, g), g) for g in grams)  # 源位升序
    clusters: list[list[tuple]] = []
    cur: list[tuple] = []
    cur_hi = -1
    for p0, g in spans:
        if cur and p0 < cur_hi:
            cur.append(g)
            cur_hi = max(cur_hi, p0 + n)
        else:
            if cur:
                clusters.append(cur)
            cur, cur_hi = [g], p0 + n
    if cur:
        clusters.append(cur)
    return [frozenset(c) for c in clusters]


def split_selected_clusters(sel, ids, rng: random.Random, n: int):
    """簇级同体半分（E122 v1.3a 裁定同构）：簇集洗牌对半——处理簇全体成员源
    联合替换；对照簇源不动 + 等量诱饵。奇数簇时处理半多一簇。
    返回 (处理 gram 集, 对照 gram 集, 处理簇表, 对照簇表)。"""
    clusters = sorted(build_source_clusters(sel, ids, n), key=min)
    rng.shuffle(clusters)
    k = (len(clusters) + 1) // 2
    treat_cl, ctrl_cl = clusters[:k], clusters[k:]
    treat = frozenset().union(*treat_cl) if treat_cl else frozenset()
    ctrl = frozenset().union(*ctrl_cl) if ctrl_cl else frozenset()
    return treat, ctrl, treat_cl, ctrl_cl


# ---------------------------------------------------------------------------
# 红队条款域：家族一切出现区间 + 拼接缝检查（诱饵/替换内容不得产生家族成员）
# ---------------------------------------------------------------------------


def family_occurrence_spans(ids: list[int], families, n: int) -> list[tuple[int, int]]:
    """红队条款域：被测 gram 家族的**一切出现区间**（不止最早出现处——E122 红队
    血训：移位兄弟源/重复出现处同样是源内容本体，诱饵压上即毁对照）。"""
    fam = set(families)
    spans = []
    for p in range(0, len(ids) - n + 1):
        if tuple(ids[p:p + n]) in fam:
            spans.append((p, p + n))
    return spans


def seam_creates_family(buf: list[int], start: int, end: int, n: int,
                        families) -> bool:
    """替换 [start,end) 后，检查修改序列上所有压线 n-gram 是否撞被测家族
    （拼接缝检查——诱饵/替换内容本身不得产生任何被测家族成员，缝上同样不算
    合格）。"""
    lo = max(0, start - n + 1)
    hi = min(len(buf) - n, end - 1)
    for p in range(lo, hi + 1):
        if tuple(buf[p:p + n]) in families:
            return True
    return False


def span_gap(a: tuple[int, int], b: tuple[int, int]) -> int:
    """区间间隔（token 数）；重叠/相接 → 0（审计「两者距离」口径）。"""
    return max(b[0] - a[1], a[0] - b[1], 0)


def _overlaps(span: tuple[int, int], spans) -> bool:
    lo, hi = span
    return any(lo < h and l < hi for l, h in spans)


def pick_replacement(orig: tuple, pool: list[tuple], rng: random.Random,
                     families: set, used_values: set, buf: list[int], start: int,
                     n: int, window_grams: set, max_draws: int = 64) -> tuple:
    """替换串挑选（E122 pick_replacement 的 token 同构 + 红队条款强化）：
    同 token 数（池即定长 n-gram）、池内、≠ 原串、**非任何被测家族成员**、非已
    用替换值、**拼接缝不产生家族成员**；优先不在基线窗内任何处出现（防伪跨段
    复制链；抽满 max_draws 仍撞窗则如实接受最后一个合格抽样）。合格候选尽 →
    ValueError 响亮，不静默回退。"""
    cand = None
    for _ in range(max_draws):
        r = pool[rng.randrange(len(pool))]
        if r == orig or r in families or r in used_values:
            continue
        trial = buf[:start] + list(r) + buf[start + n:]
        if seam_creates_family(trial, start, start + n, n, families):
            continue
        cand = r
        if r not in window_grams:
            return r
    if cand is None:
        raise ValueError(f"替换池候选尽（池空或全被禁）: orig={orig}")
    return cand


# ---------------------------------------------------------------------------
# 手术单（v1.3a 簇级同体半分的 token 同构 + 红队条款第一天就在）
# ---------------------------------------------------------------------------


class SurgeryPlan:
    """一窗手术单：处理簇源联合替换 + 对照簇等量诱饵 + 红队审计字段。

    spans: 处理源替换 (orig_gram, start, repl)；decoys: 对照诱饵落点审计记录；
    family_spans: 红队域快照（家族一切出现区间）；violations: 收尾断言违例
    （恒空——非空即响亮 RuntimeError，不静默进读数）。"""

    def __init__(self):
        self.spans: list[tuple[tuple, int, tuple]] = []
        self.decoys: list[dict] = []
        self.decoy_of: dict[tuple, list[int]] = {}  # 对照 gram -> 其诱饵下标表
        self.replacements: dict[tuple, tuple] = {}
        self.n_source_overlap_skipped = 0  # v1.3a 同款：按**簇**计数（全有或全无）
        self.n_control_no_decoy = 0
        self.family_spans: list[tuple[int, int]] = []
        self.source_spans: list[tuple[int, int]] = []

    def apply(self, ids: list[int]) -> list[int]:
        buf = list(ids)
        for _g, p, r in self.spans:
            buf[p:p + len(r)] = list(r)
        for d in self.decoys:
            p, r = d["start"], d["replacement"]
            buf[p:p + len(r)] = list(r)
        return buf

    def replaced_spans(self) -> list[tuple[int, int]]:
        return ([(p, p + len(r)) for _g, p, r in self.spans]
                + [(d["start"], d["start"] + len(d["replacement"])) for d in self.decoys])


def plan_window_surgery(ids: list[int], sel: dict[int, tuple[tuple, int]],
                        treat_grams: frozenset, ctrl_grams: frozenset,
                        table: dict[int, int], pool: list[tuple], rng: random.Random,
                        n: int, tail: int, v: int,
                        treat_clusters=None, ctrl_clusters=None,
                        max_draws: int = 64) -> SurgeryPlan:
    """一窗手术单（E122 v1.3a plan_window_surgery 的 token 同构 + 红队条款）。

    处理簇：全体成员源 span（最早出现处）**联合替换**——短语源整体灭活（簇内
    重叠 span 升序写入、后写覆盖、接缝语义与 E122 一致）；任一成员源 span 压
    保护区（两半的重复出现处+续尾，E122 同款）或已用区 → **整簇跳过**（全有或
    全无，其续尾位仍计分、如实稀释）并计数。
    对照簇：源**不动**；诱饵 = 离簇源锚最近的合格表内出现处起、与簇成员数等量
    的逐处替换——几何匹配「源区域被扰动」噪音，内容非特异。诱饵合格域（红队
    条款，最强口径）：落点 gram 非任何被测家族成员；落点 span ∩ 家族一切出现
    区间 = ∅；∩ 计分位 = ∅；∩ 已用区 = ∅；替换串同 pick_replacement 三禁。
    零合格出现处 → n_control_no_decoy 计数。
    收尾断言（响亮）：任何诱饵落点与家族一切出现区间/源 span **重叠**（压线，
    E122 `_overlaps` 同款语义：落点毁掉任何家族内容即违规）或压计分位 →
    RuntimeError，不静默进读数；与家族区间**相邻**（gap=0 但不重叠）不违规、
    只进审计距离字段；术后全窗拼接缝家族复核同样响亮。"""
    tk = len(ids)
    families = set(treat_grams) | set(ctrl_grams)
    family_spans = family_occurrence_spans(ids, families, n)
    source_spans = sorted((find_first(ids, g), find_first(ids, g) + n) for g in families)
    scoring = set(sel.keys())
    # 保护区（E122 同款：两半的重复出现处+续尾）——处理源受它约束
    protected = [(p, min(p + n + tail, tk)) for _g, p in set(sel.values())]
    used: list[tuple[int, int]] = []
    window_grams = {tuple(ids[p:p + n]) for p in range(tk - n + 1)}
    buf = list(ids)

    plan = SurgeryPlan()
    plan.family_spans = list(family_spans)
    plan.source_spans = source_spans

    if treat_clusters is None or ctrl_clusters is None:
        all_cl = build_source_clusters(sel, ids, n)
        treat_clusters = [c for c in all_cl if c <= treat_grams]
        ctrl_clusters = [c for c in all_cl if c <= ctrl_grams]

    # 1) 处理簇：全体成员源联合替换（全有或全无）
    for cluster in sorted(treat_clusters, key=min):
        members = sorted((find_first(ids, g), g) for g in cluster)  # 源位升序，接缝确定
        if any(
            _overlaps((p0, p0 + n), used) or _overlaps((p0, p0 + n), protected)
            for p0, _g in members
        ):
            plan.n_source_overlap_skipped += 1  # 整簇跳过（如实稀释+计数）
            continue
        for p0, g in members:
            r = pick_replacement(g, pool, rng, families, set(plan.replacements.values()),
                                 buf, p0, n, window_grams, max_draws)
            plan.replacements[g] = r
            plan.spans.append((g, p0, r))
            buf[p0:p0 + n] = list(r)
            used.append((p0, p0 + n))

    # 2) 对照簇：源不动；诱饵 = 离簇源锚最近合格表内出现处起等量逐处替换
    table_sites = [
        (tuple(ids[p:p + n]), p)
        for p in range(tk - n + 1)
        if pack_gram(ids[p:p + n], v) in table
    ]
    for cluster in sorted(ctrl_clusters, key=min):
        anchor = min(find_first(ids, g) for g in cluster)
        eligible = sorted(
            (
                (g2, p2) for g2, p2 in table_sites
                if g2 not in families
                and g2 not in plan.replacements
                and not _overlaps((p2, p2 + n), family_spans)
                and not any(t in scoring for t in range(p2, p2 + n))
                and not _overlaps((p2, p2 + n), used)
            ),
            key=lambda gp: (abs(gp[1] - anchor), gp[1]),  # 最近优先；平局按位次
        )
        if not eligible:
            plan.n_control_no_decoy += 1
            continue
        picked: list[int] = []
        for g2, p2 in eligible:
            if len(picked) >= len(cluster):
                break
            if _overlaps((p2, p2 + n), used):
                continue  # 贪心途中 used 在长，逐处复查
            r = pick_replacement(g2, pool, rng, families, set(plan.replacements.values()),
                                 buf, p2, n, window_grams, max_draws)
            plan.replacements[g2] = r
            buf[p2:p2 + n] = list(r)
            used.append((p2, p2 + n))
            plan.decoys.append({
                "cluster_anchor": anchor,
                "site_gram": list(g2),
                "start": p2,
                "end": p2 + n,
                "replacement": list(r),
                "gap_to_nearest_family_span": min(span_gap((p2, p2 + n), fs)
                                                  for fs in family_spans),
                "gap_to_nearest_source_span": min(span_gap((p2, p2 + n), ss)
                                                  for ss in source_spans),
                "gap_to_nearest_scoring_pos": min((span_gap((p2, p2 + n), (t, t + 1))
                                                   for t in scoring), default=None),
            })
            picked.append(len(plan.decoys) - 1)
        for g in cluster:
            plan.decoy_of[g] = picked  # 对照 gram -> 其簇诱饵下标表

    # 3) 红队条款收尾断言（响亮，不静默）+ 术后拼接缝家族全窗复核。
    # 条款语义 = 压线重叠才违规（落点毁掉家族内容）；相邻（gap=0 不重叠）合法、
    # 只进审计距离字段——2026-09-11 远端首跑实证修正：首版误把「相邻」当违规。
    for d in plan.decoys:
        dspan = (d["start"], d["end"])
        if _overlaps(dspan, family_spans) or _overlaps(dspan, source_spans):
            raise RuntimeError(f"诱饵落点压家族出现区间/源 span {dspan}（红队条款违规，响亮拒绝）")
        if any(t in scoring for t in range(d["start"], d["end"])):
            raise RuntimeError(f"诱饵落点压计分位 {dspan}（红队条款违规，响亮拒绝）")
    applied = plan.apply(ids)
    for lo, hi in plan.replaced_spans():
        if seam_creates_family(applied, lo, hi, n, families):
            raise RuntimeError(f"术后拼接缝产生被测家族成员 @{(lo, hi)}（响亮拒绝）")
    return plan


# ---------------------------------------------------------------------------
# 逐位 NLL（fp32、无 autocast；E122 cbiu_anchors 先例；坑 2 对偶守卫：半精度
# logits 先 cast .float() 再 log_softmax）
# ---------------------------------------------------------------------------


def token_nll(logits: torch.Tensor, ids: list[int]) -> list[float | None]:
    """逐位 NLL：位置 t 的读数 = logits[t-1] 对 ids[t] 的 CE；位置 0 无预测 →
    None。fp32、detach（冻结模型确定性读数，不开梯度图）。"""
    lg = logits[0].detach().float()
    logp = torch.log_softmax(lg, dim=-1)
    tgt = torch.tensor(ids[1:], dtype=torch.long, device=logp.device)
    picked = logp.gather(1, tgt.unsqueeze(1)).squeeze(1)
    out: list[float | None] = [None]
    out.extend((-picked).tolist())
    return out


@torch.no_grad()
def real_forward_nll(model, ids: list[int], device: torch.device) -> list[float | None]:
    x = torch.tensor([ids], dtype=torch.long, device=device)
    return token_nll(model(x).logits, ids)


# ---------------------------------------------------------------------------
# 模型/分词器装载（fla 必须先 import 注册模型类；transformers 惰性 import——
# 本地单测环境无 transformers/fla，核心逻辑零依赖可测）
# ---------------------------------------------------------------------------


def _install_sdpa_attn_shim() -> str:
    """flash-attn 缺席时，给 fla.layers.attn 挂 SDPA 等价 shim（跨架构对照臂用：
    fla-hub/transformer-* 的 Attention 层在 __init__ 硬依赖 flash_attn import）。
    数学等价性：causal 稠密分支 == SDPA(is_causal=True)；varlen 分支按 cu_seqlens
    逐段 SDPA。滑窗（window_size ≠ (-1,-1)）不支持，loud fail。返回实际后端名。"""
    import fla.layers.attn as _attn_mod

    if getattr(_attn_mod, "flash_attn_func", None) is not None:
        return "flash-attn"
    import torch.nn.functional as F

    def _sdpa_flash_attn_func(q, k, v, dropout_p=0.0, softmax_scale=None,
                              causal=False, window_size=(-1, -1),
                              alibi_slopes=None, deterministic=False,
                              return_attn_probs=False):
        assert window_size in ((-1, -1), (None, None)), f"SDPA shim 不支持滑窗 {window_size}"
        qh, kh, vh = (t.transpose(1, 2) for t in (q, k, v))  # [b,h,s,d]
        if qh.shape[1] != kh.shape[1]:  # GQA：KV 按 group 复制（flash-attn 语义）
            n = qh.shape[1] // kh.shape[1]
            kh = kh.repeat_interleave(n, dim=1)
            vh = vh.repeat_interleave(n, dim=1)
        o = F.scaled_dot_product_attention(qh, kh, vh, dropout_p=dropout_p,
                                           is_causal=causal, scale=softmax_scale)
        return o.transpose(1, 2)

    def _sdpa_flash_attn_varlen_func(q, k, v, cu_seqlens_q, cu_seqlens_k,
                                     max_seqlen_q, max_seqlen_k, dropout_p=0.0,
                                     softmax_scale=None, causal=False,
                                     window_size=(-1, -1), alibi_slopes=None,
                                     deterministic=False, return_attn_probs=False):
        assert window_size in ((-1, -1), (None, None)), f"SDPA shim 不支持滑窗 {window_size}"
        cq = cu_seqlens_q.tolist()
        ck = cu_seqlens_k.tolist()
        outs = []
        for (s0, s1), (t0, t1) in zip(zip(cq[:-1], cq[1:]), zip(ck[:-1], ck[1:])):
            qs = q[s0:s1].transpose(0, 1).unsqueeze(0)
            ks = k[t0:t1].transpose(0, 1).unsqueeze(0)
            vs = v[t0:t1].transpose(0, 1).unsqueeze(0)
            outs.append(F.scaled_dot_product_attention(
                qs, ks, vs, dropout_p=dropout_p, is_causal=causal,
                scale=softmax_scale).squeeze(0).transpose(0, 1))
        return torch.cat(outs, dim=0)

    _attn_mod.flash_attn_func = _sdpa_flash_attn_func
    _attn_mod.flash_attn_varlen_func = _sdpa_flash_attn_varlen_func
    print("[dn122] flash-attn 缺席 → SDPA shim 已挂载到 fla.layers.attn（跨架构臂专用）")
    return "sdpa-shim"


def load_model_and_tokenizer(model_path: str, device: torch.device):
    import fla  # noqa: F401  # 先于 transformers：注册 fla 模型类
    import transformers
    from transformers import AutoModelForCausalLM, AutoTokenizer

    attn_backend = _install_sdpa_attn_shim()
    # transformers 5.x 要求 _tied_weights_keys 为 dict（v5 格式）；fla 0.5.2 仍是
    # v4 list。仅 tie_word_embeddings=True 的模型踩雷（DeltaNet=false 侥幸绕过，
    # fla-hub/transformer-* =true 必炸）。此处规范化为等价 dict 映射， tying 语义不变。
    import fla.models.transformer.modeling_transformer as _fla_tf_mod

    if isinstance(_fla_tf_mod.TransformerForCausalLM.__dict__.get("_tied_weights_keys"), list):
        _fla_tf_mod.TransformerForCausalLM._tied_weights_keys = {
            "lm_head.weight": "model.embeddings.weight"
        }
        print("[dn122] fla TransformerForCausalLM._tied_weights_keys list→dict 已规范化"
              "（transformers 5.x 兼容，tying 语义不变）")
    # 2026-09-13（R2 施工，5.15.1 实测新增，484c636 同族）：transformers 5.15.1 的
    # from_pretrained 无条件走 _get_tied_weight_keys（modeling_utils.py:382 对
    # list 调 .keys() 崩溃）——tie=false 同样炸，5.17.0 无此路径。DeltaNet 同款
    # 规范化，tying 语义不变。
    import fla.models.delta_net.modeling_delta_net as _fla_dn_mod

    if isinstance(_fla_dn_mod.DeltaNetForCausalLM.__dict__.get("_tied_weights_keys"), list):
        _fla_dn_mod.DeltaNetForCausalLM._tied_weights_keys = {
            "lm_head.weight": "model.embeddings.weight"
        }
        print("[dn122] fla DeltaNetForCausalLM._tied_weights_keys list→dict 已规范化"
              "（transformers 5.15.1 from_pretrained 兼容，tying 语义不变）")
    tok = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_path, trust_remote_code=True, dtype=torch.bfloat16, device_map=str(device)
    )
    model.eval()
    # 2026-09-13（R2 施工新增，fla 0.5.1 × transformers 5.15.1 实测）：no_grad 前向
    # 默认 use_cache=True 会走 FLAGenerationCache 层复制路径，而 fla 0.5.1 的
    # FLALayer 未实现 tf5.15.1 新增抽象方法 get_max_length → TypeError 崩溃
    # （训练态带梯度自动关 cache 故不触发）。本仪器单窗单前向、无生成，关 cache
    # 对 NLL/状态读数语义零影响。
    model.config.use_cache = False
    fingerprint = {
        "model_path": str(model_path),
        "vocab_size": int(model.config.vocab_size),
        "max_position_embeddings": int(model.config.max_position_embeddings),
        "dtype": "bfloat16",
        "attn_backend": attn_backend,
        "gpu": torch.cuda.get_device_name(0) if device.type == "cuda" else "cpu",
        "torch": torch.__version__,
        "fla": getattr(fla, "__version__", "unknown"),
        "transformers": transformers.__version__,
    }
    return model, tok, fingerprint


def tokenize_window(tok, text: str, max_tokens: int) -> tuple[list[int], int]:
    """窗文本 → token ids（tokenizer 默认加 special tokens，Mistral 系加 BOS），
    截到 max_tokens。返回 (ids, 截断前长度)。"""
    ids = list(tok(text)["input_ids"])
    return ids[:max_tokens], len(ids)


# ---------------------------------------------------------------------------
# 稀有表与替换池（E122 D1 rare table 同角色；语料前缀扫描，确定性）
# ---------------------------------------------------------------------------


def build_rare_table(tok, corpus: Path, n_windows: int, window_bytes: int, n: int,
                     v: int, max_tokens: int) -> tuple[dict[int, int], int]:
    """语料前 n_windows 个顺序窗的 token n-gram 计数表（int 打包，有界）。
    返回 (表, 实际扫描窗数)——语料不足时如实少扫（前缀 dd 顺序写，读前缀安全）。"""
    table: dict[int, int] = {}
    scanned = 0
    with corpus.open("rb") as f:
        for _ in range(n_windows):
            raw = f.read(window_bytes)
            if len(raw) < window_bytes:
                break
            ids, _full = tokenize_window(tok, raw.decode("utf-8", errors="replace"),
                                         max_tokens)
            for p in range(len(ids) - n + 1):
                h = pack_gram(ids[p:p + n], v)
                table[h] = table.get(h, 0) + 1
            scanned += 1
            if scanned % 512 == 0:
                print(f"[dn122] 表扫描 {scanned}/{n_windows} 窗，表 {len(table)} gram",
                      flush=True)
    return table, scanned


def build_replacement_pool(table: dict[int, int], n: int, v: int,
                           quantile: float) -> list[tuple]:
    """替换池 = 表内最稀有 quantile 档（(计数, 打包 int) 升序 = (计数, gram 字典序)，
    打包保序）。E122 的稀有表即替换池同角色。"""
    items = sorted((c, h) for h, c in table.items())
    k = int(len(items) * quantile)
    return [unpack_gram(h, n, v) for _c, h in items[:k]]


# ---------------------------------------------------------------------------
# 单窗双臂（基线 a + 输入侧手术 b1；E122 run_window 同构）
# ---------------------------------------------------------------------------


def _zero_sums() -> dict:
    return {"n_sel": 0, "sel_d_b1": 0.0, "n_strong": 0,
            "n_ctl": 0, "ctl_d_b1": 0.0}


def run_window(model, ids: list[int], scan, rng: random.Random, table: dict[int, int],
               pool: list[tuple], v: int, window_id: int, forward_fn=None,
               split_override=None) -> dict:
    """单窗双臂：选中跨段稀有 gram → 簇级半分 → 处理簇源联合替换 / 对照簇等量
    诱饵 → 同一术后窗逐位 ΔNLL（计分位两臂位置恒定，直接可比）。
    返回 {status, items, sums, counts, audit, split}；status ∈ ok / empty。"""
    forward_fn = forward_fn or real_forward_nll
    n, tail = scan.ngram_len, scan.tail
    tk = len(ids)
    counts = {
        "hit_grams": 0, "offtable_grams": 0, "n_selection_overlap": 0,
        "n_treatment_grams": 0, "n_control_grams": 0,
        "n_treatment_clusters": 0, "n_control_clusters": 0,
        "n_treatment_clusters_skipped": 0, "n_control_no_decoy": 0,
        "n_decoys": 0,
    }
    empty = {"status": "empty", "items": [], "sums": _zero_sums(), "counts": counts,
             "audit": None, "split": None}
    if tk < n + 1:
        return empty

    occ = cross_segment_occurrences(ids, n, scan.segment_tokens)
    rare, offtable = select_rare_grams(occ, table, scan.rare_quantile, v)
    counts["hit_grams"] = len(occ)
    counts["offtable_grams"] = offtable
    sel, sel_overlap = select_tail_positions(occ, rare, n, tail, tk)
    counts["n_selection_overlap"] = sel_overlap
    if not sel:
        return empty

    if split_override is not None:
        treat_grams, ctrl_grams = split_override
        all_cl = build_source_clusters(sel, ids, n)
        treat_cl = [c for c in all_cl if c <= treat_grams]
        ctrl_cl = [c for c in all_cl if c <= ctrl_grams]
    else:
        treat_grams, ctrl_grams, treat_cl, ctrl_cl = split_selected_clusters(sel, ids, rng, n)
    counts["n_treatment_grams"] = len(treat_grams)
    counts["n_control_grams"] = len(ctrl_grams)
    counts["n_treatment_clusters"] = len(treat_cl)
    counts["n_control_clusters"] = len(ctrl_cl)

    plan = plan_window_surgery(ids, sel, treat_grams, ctrl_grams, table, pool, rng,
                               n, tail, v, treat_clusters=treat_cl, ctrl_clusters=ctrl_cl,
                               max_draws=scan.max_draws)
    counts["n_treatment_clusters_skipped"] = plan.n_source_overlap_skipped
    counts["n_control_no_decoy"] = plan.n_control_no_decoy
    counts["n_decoys"] = len(plan.decoys)
    split_audit = {
        "treatment_clusters": [sorted(list(g) for g in c) for c in
                               sorted(treat_cl, key=min)],
        "control_clusters": [sorted(list(g) for g in c) for c in
                             sorted(ctrl_cl, key=min)],
        "treatment_replaced": sorted(list(g) for g in treat_grams if g in plan.replacements),
        "control_decoy_placed": sorted(list(g) for g in plan.decoy_of if plan.decoy_of[g]),
    }

    # 臂 (a)：完整窗基线；臂 (b1)：输入侧手术（处理源替换 + 对照诱饵，同一术后窗）
    nll_a = forward_fn(model, ids)
    ids_b1 = plan.apply(ids)
    nll_b1 = forward_fn(model, ids_b1)

    items, sums = [], _zero_sums()
    for role, pos_list in (("selected", sorted(t for t, (g, _p) in sel.items()
                                               if g in treat_grams)),
                           ("control", sorted(t for t, (g, _p) in sel.items()
                                              if g in ctrl_grams))):
        for t in pos_list:
            na, nb = nll_a[t], nll_b1[t]
            g, p = sel[t]
            src_pos = find_first(ids, g)
            delta = (nb - na) if (na is not None and nb is not None) else None
            item = {
                "window_id": window_id,
                "token_pos": t,
                "role": role,
                "gram": list(g),
                "repeat_pos": p,
                "source_pos": src_pos,
                "source_segment": (src_pos // scan.segment_tokens) if src_pos >= 0 else None,
                "repeat_segment": p // scan.segment_tokens,
                "source_repeat_distance": (p - src_pos) if src_pos >= 0 else None,
                "NLL_a": na,
                "NLL_b1": nb,
                "delta_b1": delta,
                "strong": bool(delta is not None and delta >= scan.strong_line),
            }
            if role == "control":  # 诱饵手术审计（对照源保持不动）
                ds = plan.decoy_of.get(g) or []
                item["decoy_start"] = plan.decoys[ds[0]]["start"] if ds else None
                item["decoy_site_gram"] = (plan.decoys[ds[0]]["site_gram"]) if ds else None
                item["decoy_n_spans"] = len(ds)
            items.append(item)
            if role == "selected":
                sums["n_sel"] += 1
                sums["sel_d_b1"] += delta if delta is not None else 0.0
                sums["n_strong"] += int(delta is not None and delta >= scan.strong_line)
            else:
                sums["n_ctl"] += 1
                sums["ctl_d_b1"] += delta if delta is not None else 0.0

    audit = {
        "window_id": window_id,
        "source_spans": [
            {"gram": list(g), "start": s, "end": s + n,
             "segment": s // scan.segment_tokens,
             "role": "treatment" if g in treat_grams else "control",
             "replaced": g in plan.replacements}
            for g in sorted(set(treat_grams) | set(ctrl_grams))
            for s in (find_first(ids, g),)
        ],
        "family_occurrence_spans": [list(sp) for sp in plan.family_spans],
        "decoy_landings": plan.decoys,
        "zero_press_violations": 0,  # plan_window_surgery 收尾断言非零即 raise，恒 0
        "counts": counts,
        "split": split_audit,
    }
    return {"status": "ok", "items": items, "sums": sums, "counts": counts,
            "audit": audit, "split": split_audit}


# ---------------------------------------------------------------------------
# 聚合：主判读量 + 窗级 bootstrap（E122 bootstrap_contrast/verdict 同构）
# ---------------------------------------------------------------------------


def bootstrap_contrast(window_sums: list[dict], n_boot: int = 2000, seed: int = 42,
                       level: float = 0.95) -> dict:
    """主判读量 = mean ΔNLL_b1(处理) − mean ΔNLL_b1(对照)；窗级重抽样 CI。
    逐位 ΔNLL 为冻结模型确定性前向读数，统计性全由抽样端 bootstrap 承担。"""

    def contrast(sample: list[dict]):
        ns = sum(w["n_sel"] for w in sample)
        nc = sum(w["n_ctl"] for w in sample)
        if not ns or not nc:
            return None
        return (sum(w["sel_d_b1"] for w in sample) / ns
                - sum(w["ctl_d_b1"] for w in sample) / nc)

    w_total = len(window_sums)
    point = contrast(window_sums)
    rng = random.Random(seed)
    boots = []
    for _ in range(n_boot):
        sample = [window_sums[rng.randrange(w_total)] for _ in range(w_total)]
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
    """判读表（判序 CI 在先，E122 收官裁定 2026-09-06 同构）：
    CI 含 0 → 剂量未落；CI 不含 0 且 point<0 → 反常；其余按强/弱分档。"""
    if mean_sel is None or contrast["point"] is None:
        return "无读数"
    if not contrast["ci_excludes_zero"]:
        return "剂量未落——DeltaNet 跨架构复证未过（CI 含 0）"
    if contrast["point"] < 0:
        return "反常（对照>处理——仪器 bug 或选择口径错，停，转口径审计）"
    if mean_sel >= STRONG_LINE_NAT:
        return "跨架构必要性复现实存（强）——DeltaNet 同款剂量打在黑板上"
    return "跨架构必要性复现实存（弱）——剂量部分在板"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--model-path", default="/root/autodl-tmp/models/delta_net-1.3B-100B")
    p.add_argument("--corpus", default="/root/autodl-tmp/corpus/corpus_v3.txt")
    p.add_argument("--n-windows", type=int, default=40)
    p.add_argument("--start-window", type=int, default=0,
                   help="起始窗序号（窗 w = 语料字节 [w*window_bytes, (w+1)*window_bytes)）")
    p.add_argument("--window-bytes", type=int, default=4096)
    p.add_argument("--max-tokens", type=int, default=2048,
                   help="窗 token 截断上限（≤ 模型 max_position_embeddings）")
    p.add_argument("--segment-tokens", type=int, default=256,
                   help="跨段定义：token 段大小（gram 出现段须严格晚于最早出现段）")
    p.add_argument("--ngram-len", type=int, default=3, choices=[2, 3, 4],
                   help="token n-gram 长度（施工注记 1：n 取 2-3）")
    p.add_argument("--tail", type=int, default=3,
                   help="计分续尾 token 数（E122 T=3 同构）")
    p.add_argument("--rare-quantile", type=float, default=0.2,
                   help="窗内命中 gram 的最稀有档比例（D1 同款分位数档）")
    p.add_argument("--pool-quantile", type=float, default=0.1,
                   help="替换池 = 稀有表最稀有档比例")
    p.add_argument("--table-windows", type=int, default=2048,
                   help="稀有表扫描的语料前缀窗数")
    p.add_argument("--strong-line", type=float, default=STRONG_LINE_NAT)
    p.add_argument("--bootstrap", type=int, default=2000)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--max-draws", type=int, default=64)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--out-dir",
                   default=f"outputs/e122_deltanet_book_{time.strftime('%Y%m%d')}")
    args = p.parse_args()

    if args.tail < 1 or args.segment_tokens < 1 or args.max_tokens < 64:
        raise SystemExit("--tail/--segment-tokens ≥1 且 --max-tokens ≥64")
    if not (0 < args.rare_quantile <= 1 and 0 < args.pool_quantile <= 1):
        raise SystemExit("--rare-quantile/--pool-quantile ∈ (0, 1]")

    device = torch.device(
        "cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda"
        else "cpu"
    )
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    corpus = Path(args.corpus)
    if not corpus.exists():
        raise SystemExit(f"corpus 不存在: {corpus}")

    model, tok, fingerprint = load_model_and_tokenizer(args.model_path, device)
    v = fingerprint["vocab_size"]
    print(f"[dn122] model={Path(args.model_path).name} device={device.type} "
          f"V={v} fp={fingerprint['gpu']}", flush=True)

    need_windows = max(args.table_windows, args.start_window + args.n_windows)
    table, table_scanned = build_rare_table(tok, corpus, need_windows, args.window_bytes,
                                            args.ngram_len, v, args.max_tokens)
    pool = build_replacement_pool(table, args.ngram_len, v, args.pool_quantile)
    if not pool:
        raise SystemExit("替换池为空（表过小或 --pool-quantile 过小），响亮拒绝")
    print(f"[dn122] 稀有表 {len(table)} gram（扫 {table_scanned} 窗），池 {len(pool)}",
          flush=True)

    scan = args  # run_window 所需字段（ngram_len/tail/segment_tokens/…）CLI 全带

    def forward(model_, ids):
        return real_forward_nll(model_, ids, device)

    rng = random.Random(args.seed)
    items_path = out_dir / "items.jsonl"
    audit_path = out_dir / "audit.jsonl"
    window_sums: list[dict] = []
    tally = {"n_windows_attempted": 0, "n_windows_used": 0, "n_windows_empty": 0,
             "n_windows_truncated": 0}
    totals: dict[str, int] = {}
    max_byte_touched = 0
    sel_distances: list[int] = []
    decoy_gaps: list[int] = []

    with corpus.open("rb") as f:
        for wi in range(args.n_windows):
            w_abs = args.start_window + wi
            f.seek(w_abs * args.window_bytes)
            raw = f.read(args.window_bytes)
            if len(raw) < args.window_bytes:
                print(f"[dn122] 语料前缀尽（窗 {w_abs} 不足 {args.window_bytes}B），停",
                      flush=True)
                break
            max_byte_touched = max(max_byte_touched, (w_abs + 1) * args.window_bytes)
            ids, full_len = tokenize_window(
                tok, raw.decode("utf-8", errors="replace"), args.max_tokens)
            if full_len > args.max_tokens:
                tally["n_windows_truncated"] += 1
            rec = run_window(model, ids, scan, rng, table, pool, v, w_abs, forward_fn=forward)
            tally["n_windows_attempted"] += 1
            for k, val in rec["counts"].items():
                totals[k] = totals.get(k, 0) + val
            if rec["status"] == "ok" and rec["sums"]["n_sel"] > 0:
                tally["n_windows_used"] += 1
                window_sums.append(rec["sums"])
                sel_distances.extend(
                    it["source_repeat_distance"] for it in rec["items"]
                    if it["role"] == "selected" and it["source_repeat_distance"] is not None
                )
                decoy_gaps.extend(
                    d["gap_to_nearest_family_span"] for d in rec["audit"]["decoy_landings"]
                )
                audit_rec = {
                    "byte_offset": w_abs * args.window_bytes,
                    "n_bytes": args.window_bytes,
                    "n_tokens": len(ids), "n_tokens_full": full_len,
                    "truncated": full_len > args.max_tokens,
                    "segment_tokens": args.segment_tokens,
                    **rec["audit"],
                }
                with audit_path.open("a", encoding="utf-8") as fa:
                    fa.write(json.dumps(audit_rec, ensure_ascii=False) + "\n")
                with items_path.open("a", encoding="utf-8") as fi:
                    for item in rec["items"]:
                        fi.write(json.dumps(item, ensure_ascii=False) + "\n")
            else:
                tally["n_windows_empty"] += 1
            s = rec["sums"]
            print(f"[dn122] win {w_abs:5d} {rec['status']:5s} sel={s['n_sel']:3d} "
                  f"ctl={s['n_ctl']:3d} strong={s['n_strong']:3d} "
                  f"decoy={rec['counts']['n_decoys']:2d} ({time.time() - t0:.0f}s)",
                  flush=True)

    # 同卷锚：计分窗字节前缀 SHA256（dd 顺序写语料下，读过的前缀字节已定终）
    prefix_sha = None
    if max_byte_touched:
        h = hashlib.sha256()
        with corpus.open("rb") as f:
            remain = max_byte_touched
            while remain:
                chunk = f.read(min(1 << 20, remain))
                if not chunk:
                    break
                h.update(chunk)
                remain -= len(chunk)
        prefix_sha = h.hexdigest()

    n_sel = sum(w["n_sel"] for w in window_sums)
    n_ctl = sum(w["n_ctl"] for w in window_sums)
    mean_sel = sum(w["sel_d_b1"] for w in window_sums) / n_sel if n_sel else None
    mean_ctl = sum(w["ctl_d_b1"] for w in window_sums) / n_ctl if n_ctl else None
    boot = bootstrap_contrast(window_sums, args.bootstrap, args.seed + 1)
    n_strong = sum(w["n_strong"] for w in window_sums)
    distances = sel_distances

    summary = {
        "probe": "E122 跨段必要性账 · DeltaNet 跨架构复证（输入侧遮蔽 + 簇级同体半分对照）",
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": device.type,
        "model_fingerprint": fingerprint,
        "hardware_note": "体制判词一律「同机同 env 内成立」（AGENTS 坑 11 纪律）",
        "corpus": {
            "path": str(corpus),
            "window_bytes": args.window_bytes,
            "start_window": args.start_window,
            "scored_prefix_bytes": max_byte_touched,
            "scored_prefix_sha256": prefix_sha,
            "corpus_size_at_run": os.path.getsize(corpus),
        },
        "window_definition": {
            "window": "corpus[w*4096 : (w+1)*4096] 顺序字节窗（纯文本）",
            "decode": "utf-8 errors=replace",
            "tokenize": "tokenizer 默认 special tokens（Mistral 系加 BOS）",
            "truncation": f"ids[:{args.max_tokens}]",
            "segment": f"token 段 = {args.segment_tokens} tokens，跨段 = 出现段严格晚于最早出现段",
            "note": "同卷纪律：窗定义+前缀 SHA256 落此，供日后与我们 44M 模型同窗对拍；"
                    "跨模型只比方向不比绝对值（词表/分数面不同）",
        },
        "params": {
            "n_windows": args.n_windows, "ngram_len": args.ngram_len, "tail": args.tail,
            "segment_tokens": args.segment_tokens, "rare_quantile": args.rare_quantile,
            "pool_quantile": args.pool_quantile, "seed": args.seed,
            "strong_line_nat": args.strong_line, "max_draws": args.max_draws,
            "bootstrap": args.bootstrap, "table_windows_requested": args.table_windows,
            "table_windows_scanned": table_scanned,
        },
        "rare_table": {"n_grams": len(table), "pool_size": len(pool)},
        "windows": tally,
        "selected": {"n": n_sel, "mean_delta_b1": mean_sel},
        "control": {"n": n_ctl, "mean_delta_b1": mean_ctl},
        "contrast_b1": {
            **boot,
            "mean": (mean_sel - mean_ctl) if (mean_sel is not None and mean_ctl is not None) else None,
        },
        "strong_tail": {
            "n_strong": n_strong,
            "rate_of_selected": (n_strong / n_sel) if n_sel else None,
            "per_window_mean": (n_strong / len(window_sums)) if window_sums else 0.0,
        },
        "source_repeat_distance": {
            "n": len(distances),
            "min": min(distances) if distances else None,
            "median": (sorted(distances)[len(distances) // 2] if distances else None),
            "max": max(distances) if distances else None,
        },
        "red_team_audit": {
            "clause": "诱饵落点 ∩ 家族一切出现区间 = ∅ 且 ∩ 源 span = ∅ 且 ∩ 计分位 = ∅"
                      "（压线重叠才违规；相邻 gap=0 不违规只进距离字段）；"
                      "诱饵内容（含拼接缝）不含任何被测家族成员；非零违例即 RuntimeError",
            "n_decoys_total": totals.get("n_decoys", 0),
            "min_decoy_gap_to_family_span": min(decoy_gaps) if decoy_gaps else None,
            "n_overlap_violations": 0,
            "n_control_no_decoy": totals.get("n_control_no_decoy", 0),
            "n_treatment_clusters_skipped": totals.get("n_treatment_clusters_skipped", 0),
        },
        "exclusions": {
            "offtable_hit_grams": totals.get("offtable_grams", 0),
            "selection_overlap": totals.get("n_selection_overlap", 0),
        },
        "verdict": verdict(mean_sel, boot),
        "b2_note": "无 b2 行手术臂：DeltaNet 无显式分块状态行接口可外科置换；本仪器只跑 "
                   "基线 a + 输入侧手术 b1，簇级同体半分对照结构与 E122 v1.3a 同构。",
        "timing_sec": round(time.time() - t0, 1),
    }
    (out_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)
    print(f"[dn122] items -> {items_path}\n[dn122] audit -> {audit_path}", flush=True)


if __name__ == "__main__":
    main()
