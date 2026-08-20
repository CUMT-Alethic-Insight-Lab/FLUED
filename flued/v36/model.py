"""FLUED v3.6: whole-prompt compression to a single readout package via KDA state.

Pipeline: bytes -> byte encoder -> slender segmentor (boundary timetable) ->
chunks -> summarizer (projector, one memory per chunk) -> write head ->
KDA state machine (serial, per-sample state) -> readout package (k queries
read the final state) -> backbone -> global span decoder.

v0 uses a pure-PyTorch KDA recurrence (chunk counts are 32-256, kernel
integration is a later acceleration step).
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import warnings

import torch
from torch import nn
import torch.nn.functional as F
from torch.utils.checkpoint import checkpoint as _grad_checkpoint

from flued.data import PAD_ID
from flued.v33.chunk_builder import ChunkBatch, ChunkBuilder
from flued.v34.model import (
    DiTStyleBlock,
    FLUEDV34Probe,
    PlainByteLookup,
    SoftBoundaryBridge,
    _plastic_signed_confidence,
)

try:
    from fla.ops.kda import chunk_kda as _fla_chunk_kda
except Exception:  # fla is optional (tests / non-GPU environments)
    _fla_chunk_kda = None
try:
    from fla.ops.gdn2 import chunk_gdn2 as _fla_chunk_gdn2
except Exception:  # fla < gdn2 build: the torch recurrence remains the fallback
    _fla_chunk_gdn2 = None


@dataclass
class V36Config:
    """Defaults track configs/canonical_v36.json (v36.2-20260805)."""

    d_byte: int = 384
    encoder_layers: int = 3
    segmentor_layers: int = 9
    nhead: int = 6
    ffn_dim: int = 1152
    d_mem: int = 512
    summarizer_slots: int = 4
    summarizer_hidden: int = 1024
    kda_heads: int = 4
    kda_head_k: int = 128
    kda_head_v: int = 256
    write_hidden: int = 1024
    kda_tau_max: float = 256.0
    readout_queries: int = 1
    d_pack: int = 1536
    d_backbone: int = 384
    backbone_layers: int = 3
    backbone_nhead: int = 8
    backbone_ffn: int = 1024
    backbone_mode: str = "attn"  # "attn" = cross-chunk attention (default; E30 baseline). "mlp" = per-readout, JUDGED DEAD by E32 (encoder gradient starvation / anchor blowup) -- retained behind the flag for the causal-attention follow-up.
    # "per_chunk" (default, current form): the backbone consumes all C per-chunk
    # readouts. "final" = k=1 backbone interface (user-ruled 2026-08-06): the
    # backbone consumes ONLY the final state's readout (carries 0..C history);
    # per-chunk readouts stay on the decoder side, which is what per-chunk
    # conditioning was always for (task density, E23). This is also the demand
    # structure for the state channel: with "final", a state-less readout only
    # holds the last chunk, so whole-window completion forces the recurrence.
    # "paged" = /n paging (user-ruled 2026-08-07, the only legal nq widening):
    # the window is divided into n sub-pages, the state is read once at each
    # sub-page boundary (each read causal to its position), and the backbone
    # transforms the n read vectors pointwise (sub-page-level causal honesty).
    # n=1 reproduces "final"; n=C reproduces per-chunk.
    backbone_readout: str = "per_chunk"
    paged_reads: int = 4
    decoder_hidden: int = 1024
    decoder_layers: int = 3
    max_chunks: int = 64
    max_span: int = 64
    bytes_per_chunk: int = 16
    tau_cut: float = 0.94
    tau_trans: float = 0.75
    boundary_mode: str = "dynamic"
    boundary_temperature: float = 0.15
    boundary_bridge_gradient_scale: float = 0.1
    max_positions: int = 64
    per_chunk_readout: bool = True
    summarizer_type: str = "dit"
    summarizer_dit_layers: int = 2
    prefix_task: bool = False
    prefix_positions: int = 4
    kda_impl: str = "fla"  # fla chunk_kda fused kernel (default since v36.6: +15% steps/s at 23 chunks, parity-verified; essential at byte-level lengths for R0). "torch" serial loop retained as fallback.
    # S39 stage-2 write-rule axis (S39_STAGED_MATRIX_PLAN_20260817_CN appendix A):
    # "kda" (default; bit-identical to every historical arm) uses the shared
    # scalar beta for erase+write; "gdn2" decouples them -- a per-K-channel
    # erase gate b and a per-V-channel write gate w replace beta (Gated
    # DeltaNet 2, fla chunk_gdn2). The channel decay (log alpha) and the delta
    # erase form are unchanged: the ONLY mechanism delta is the erase/write
    # gate decoupling (single-variable arm).
    recurrence: str = "kda"
    # R1 relative baseline (spec section 4): when False, each chunk's readout
    # comes straight from its own write (same write head, same realign, same
    # transmitted-scalar budget) -- the serial KDA recurrence is bypassed, so
    # the ONLY difference from the main architecture is the state channel.
    state_channel: bool = True
    # Three-state drafting backbone (spec section 23, user-ruled 2026-08-08):
    # backbone_mode="draft" swaps the backbone for a DiT that refines a fresh
    # thinking matrix over T rounds (T sampled in [think_steps_min,
    # think_steps_max] during training; deterministic stability-stop at eval).
    # think_visibility: "readout" (arm A: thinking sees only the k=1 readout)
    # or "readout_memory" (arm B: thinking may also cross-read pre-state
    # memory rows, strictly causally). think_stop_cos: eval-time halt when the
    # mean cosine between consecutive thinking matrices exceeds it.
    think_steps_min: int = 1
    think_steps_max: int = 16
    think_visibility: str = "readout"
    think_stop_cos: float = 0.995
    # Draft anti-collapse / cold-start levers (research sweep 2026-08-08,
    # docs/research/RESEARCH_SWEEP_20260808_CN.md; arms s34/s35):
    # draft_init "content_seed" = content-preheated slot init h0 += W(content)
    # (SmoothSA 2508.05417 / QSA: noise+pos is the known worst init).
    # draft_inject "concat" = per-round h += W(cat[h, readout]) -- the Huginn
    # re-injection that attention cannot learn to ignore (2502.05171 Bad Run 2).
    # draft_depth_dist "poisson" = 1+Poisson(max/2) clamped, heavy-tail depth
    # sampling instead of uniform (Huginn). draft_trunc_bptt k>0 = backprop
    # only the last k rounds (Huginn k=8). draft_sandwich = post-LN after each
    # sublayer. draft_mem_pos = add chunk position to memory K (shelf row
    # numbers, Retrievit 2603.02874). draft_intermediate_weight>0 = completion
    # loss also at a uniformly sampled in-gradient-zone intermediate round
    # (LoopFormer 2602.11451 short-trajectory CE -- the SUPERVISED arm s35).
    draft_init: str = "noise"
    draft_inject: str = "cross"
    draft_depth_dist: str = "uniform"
    draft_trunc_bptt: int = 0
    draft_sandwich: bool = False
    draft_mem_pos: bool = False
    draft_intermediate_weight: float = 0.0
    # DSpark-style Markov head (2607.05147): rank-r bigram transition bias
    # added to decoder logits, conditioned on the previous byte (teacher-
    # forced). Treats the multi-peak conflict / suffix decay of parallel byte
    # decoding. 0 = off (default; all historical arms are off). NOTE: when
    # on, the decoder sees shifted targets -- metrics become a distinct
    # teacher-forced protocol, not comparable to off-arms.
    decoder_markov: int = 0
    # S36 mainline (user-ruled 2026-08-08): residual-gated exact cache on the
    # s31 hybrid form (HOLA 2607.02303 / HAM 2603.22325). Store = optional
    # k=1 final-readout gist token + the top-frac memory rows ranked by
    # per-chunk direct-decode CE (HAM-style prediction error; computable at
    # deployment since the window bytes are known). xcache_frac=1.0 keeps all
    # rows (= s31 with optional gist token -- the sanity arm).
    xcache_frac: float = 1.0
    xcache_gist: bool = False
    # S39 stage-1 taxonomy 2x2 (S39_STAGED_MATRIX_PLAN_20260817_CN §4, v3 axis
    # semantics): per-side K/V source switches for the xattn backbone store
    # rows. "memory" (default) = project the pre-state memory rows (existing
    # behavior); "state" = project the per-chunk state readouts (content,
    # d_pack wide) through dedicated projections, created only when selected
    # so old checkpoints keep loading strict-clean. Grid mapping:
    # a=(memory,memory) b=(state,memory) c=(memory,state) d=(state,state).
    k_row_source: str = "memory"
    v_row_source: str = "memory"
    # S39 a+pos arm (same plan, appendix C): position-injected keys on the
    # xattn K side -- per key row, sinusoidal features of (segment order,
    # window-relative start byte offset) projected by pos_proj (POS_FEAT_DIM
    # -> d_backbone) and added through a zero-init scalar gate pos_gate, so
    # step 0 is exactly the a-grid anchor and the gate value is itself the
    # diagnostic readout. Memory-source only (k/v_row_source must both be
    # "memory"; the state combination is rejected to protect attribution).
    k_pos_inject: bool = False
    # S39 K-block eval probe (user-ruled 2026-08-17): eval-time-only ablation
    # switch -- zero the aligned K rows so block-1 cross-attention goes uniform
    # (the index channel carries zero information). Tests whether the slm
    # behavioral-only eval probe -- no parameters, checkpoints unaffected.
    k_block_eval: bool = False
    # S39 K-seed arm (user-ruled 2026-08-17): which aligned row seeds the slm
    # backbone hidden state. "v" (default) = seed from the V/memory row
    # (consensus §1.3, bit-preserved); "k" = seed from the INDEX row, so the
    # hidden state starts address-only and content must be retrieved through
    # the K/V store -- the index channel becomes load-bearing (the K-block
    # probe showed it is decorative under "v").
    seed_source: str = "v"
    # E75 key-decollapse hard constraint (user-ruled 2026-08-18; evidence line
    # E73 oracle verdict / E74 key-collapse survey / E75 layerwise
    # decomposition): the write keys' collapse (mean pairwise |cos| ~0.93,
    # Tropp threshold => no addressability from N=2) localizes to a SINGLE
    # shared direction in the to_k output (de-meaning drops mu 0.935 -> 0.307;
    # bias/saturation/dead-dims/weight-rank all cleared). When on, WriteHead
    # subtracts a running center from the to_k output (pre-normalization):
    # training mode keeps an EMA (momentum 0.99, detached) of the batch mean,
    # cold-starting from the first batch (BatchNorm convention); eval mode uses
    # the frozen buffer. The buffer is persistent=False BY RULING: old
    # checkpoints keep loading strict-clean, and the statistic is re-estimated
    # online from zero whenever training (re)starts. Operational caveat of that
    # ruling: a FRESH eval process on a to_k_center-trained checkpoint starts
    # with a zero buffer (centering off until a training-mode forward warms
    # it) — in-training eval on the live model is unaffected. Default False =
    # every legacy path bit-preserved. Covers BOTH WriteHead instances (K and V
    # channels); the a grid has no WriteHead and is unaffected.
    to_k_center: bool = False
    # Hard-constraint gate arm (Q10, user-ruled 2026-08-20; E79 mu-trajectory
    # showed the de-mean-only surgery's residual coherence slowly re-collapses
    # 0.690 -> 0.811 under training — soft repair re-collapses, so the gate
    # upgrades centering to full whitening): WriteHead applies
    # k <- (k - EMA_mean) @ W_pre with W_pre = (EMA_cov + eps*I)^{-1/2}
    # (eigh, fp32, recomputed every training step; 512x512 is sub-ms), pushing
    # the pre-normalization key covariance to identity — pairwise |cos| is
    # crushed toward ~0 by construction instead of being negotiated with the
    # loss. Same buffer discipline as to_k_center (EMA 0.99, detached,
    # BatchNorm-style cold start, persistent=False; eval uses the frozen
    # buffers, so a FRESH eval process starts with identity whitening until a
    # training-mode forward warms the buffers — measurement protocols must
    # warm up first). Superset of to_k_center: when on, the centering branch
    # is subsumed (whitening includes de-meaning); do not stack the flags.
    # Default False = every legacy path bit-preserved.
    to_k_whiten: bool = False
    # fork 2 (user-ruled 2026-08-19; spec docs/versions/v3.7/
    # FLUED_V3_7_FORK2_MULTIVIEW_READOUT_20260819_CN.md): multi-view readout.
    # readout_views=m>1 expands the backbone STORE side of each state channel
    # from one readout row per chunk to m measurement rows per chunk, read with
    # a SEEDED RANDOM ORTHOGONAL FRAME (probe_frame, seed PROBE_FRAME_SEED,
    # training-free by ruling: learned probes degenerate to decoration, E66)
    # rotated once per segment index (frame_rotations table). The direct and
    # predict paths keep the classic single trained readout_query row
    # (bit-untouched, fork 2 §1.3); only the completion/readout path's store
    # is widened. Interface form choice (§4 allows widening realign/decoder_in
    # inputs OR m-way shared weights): SHARED realign/align weights over m
    # store entries per chunk ("m 路共享") — zero new parameters, so m>1
    # checkpoints strict-load into m=1 builds and vice versa, and the
    # backbone/decoder/loss machinery is unchanged (the m expansion lives
    # entirely in the store's causal mask). Default 1 = bit-preserved.
    readout_views: int = 1
    # E79 split-trunk (user-ruled 2026-08-18; evidence M3 write-value probe):
    # the WriteHead trunk was shared by to_k/to_v(/to_beta/to_b/to_w), so the
    # to_k_center surgery's training dynamics deformed to_v's value content
    # through the shared trunk (the b-grid K channel lost ~half its linearly
    # decodable byte content, 0.56->0.23 slot0). When on, the WriteHead holds
    # TWO independent trunks (trunk_k feeds to_k; trunk_v feeds the value/gate
    # heads). Default off = the shared `trunk` and every legacy path
    # bit-preserved (old checkpoints load strict-clean; a split-trunk model
    # does NOT strict-load a shared-trunk state dict — by design, loud).
    # Composes with to_k_center (centering applies to the to_k branch only).
    split_trunk: bool = False
    # v3.7 mode (docs/versions/v3.7/FLUED_V3_7_ARCHITECTURE_CONSENSUS_20260817_CN.md,
    # user-ruled 2026-08-17): backbone_mode="slm" -- fully config-gated; the
    # default stays "attn" and every v36 path is bit-preserved. In slm mode the
    # summarizer owns the K/V interface (§1.1): DiTChunkSummarizer grows a
    # second head producing one index vector per chunk (the K side; the memory
    # row itself IS the standard V). The backbone is a standard small LM
    # (SLMBackbone): block 1 cross-reads the precomputed store rows causally,
    # deeper blocks are standard causal self-attention; Q is self-produced from
    # the backbone hidden state and the seed at position i is align_V(V_i)+pos
    # ("each chunk asks with its own V", §1.3). The interpreter (§1.2) becomes
    # an OPTIONAL per-channel processor: k_row_source in {"index", "state"}
    # ("memory" is ILLEGAL for K in slm mode), v_row_source in {"memory",
    # "state"}; each "state" channel gets its own WriteHead+KDAStateMachine
    # pair (K eats the index rows, V the memory rows). Grid (§3):
    # a=(index,memory) b=(state,memory) c=(index,state) d=(state,state);
    # a+pos=(index+pos,memory) via k_pos_inject (k_row_source="index" only).
    # S38 (user-ruled 2026-08-09): supplementary content-conditioned readouts
    # for the top-N hardest chunks that were NOT cached -- a second, targeted
    # slice of the state per hard chunk (query generated from the chunk's own
    # readout), appended to the store as its own entry. Zero write-side
    # surgery; "under-served content gets its own readout matrix" (RDN-frame
    # with CUIB gating: downstream decode CE decides who gets a second read).
    xcache_supp: int = 0
    # S38B (user-ruled 2026-08-10): the supplementary entries come from a
    # RESIDUAL SECOND STATE S' instead of the main state. S' accumulates
    # decode-CE-gated writes only (beta_i x sigmoid((CE_i - median)/temp),
    # detached -- CUIB pattern: downstream failure drives the write); the
    # readout uses independent content-conditioned queries. The point: a
    # fixed-size residual matrix vs linearly growing verbatim cache rows.
    supp_source: str = "state"  # "state" (arm A) | "residual" (arm B)
    residual_gate_temp: float = 1.0
    # S37 (spec SS24, user-proposed 2026-08-09): backbone_mode="paged_xattn" --
    # page gists (paged_reads pages) + per-page residual cache rows
    # (paged_cache_rows per page) with entry-level causal attention; the
    # decoder conditions each chunk on its page's output row. Needs targets
    # for the residual criterion (S1 trainer path only).
    paged_cache_rows: int = 1


@dataclass
class V36Output:
    logits_direct: torch.Tensor
    logits_backbone: torch.Tensor
    package: torch.Tensor | None  # None in slm mode (the content channel is retired there, consensus §4)
    backbone_out: torch.Tensor
    chunks: ChunkBatch
    boundary_confidence: torch.Tensor
    memory: torch.Tensor
    state_norm: torch.Tensor
    aux: dict
    prefix: list | None = None  # [(position_i, logits_direct_i, logits_backbone_i), ...]


class ChunkSummarizer(nn.Module):
    def __init__(self, c: V36Config) -> None:
        super().__init__()
        self.slots = nn.Parameter(torch.empty(c.summarizer_slots, c.d_byte))
        nn.init.trunc_normal_(self.slots, std=0.02)
        self.q = nn.Linear(c.d_byte, c.d_byte, bias=False)
        self.k = nn.Linear(c.d_byte, c.d_byte, bias=False)
        self.v = nn.Linear(c.d_byte, c.d_byte, bias=False)
        self.ffn = nn.Sequential(
            nn.LayerNorm(c.summarizer_slots * c.d_byte),
            nn.Linear(c.summarizer_slots * c.d_byte, c.summarizer_hidden),
            nn.SiLU(),
            nn.Linear(c.summarizer_hidden, c.d_mem),
        )

    def forward(self, spans: torch.Tensor, token_mask: torch.Tensor) -> torch.Tensor:
        bsz, chunks, span, dim = spans.shape
        q = self.q(self.slots).view(1, 1, self.slots.size(0), dim).expand(bsz, chunks, -1, -1)
        k = self.k(spans)
        v = self.v(spans)
        score = torch.einsum("bcsd,bctd->bcst", q, k) / (dim ** 0.5)
        score = score.masked_fill(~token_mask.unsqueeze(2), -1.0e4)
        attn = score.softmax(dim=-1)
        pooled = torch.einsum("bcst,bctd->bcsd", attn, v)
        return self.ffn(pooled.reshape(bsz, chunks, -1))


class DiTChunkSummarizer(nn.Module):
    """Literal one-shot DiT summarizer: DiTStyleBlock stack over each chunk's
    span (chunks processed in parallel and independently), masked mean pool,
    FFN to one memory vector per chunk. Matches the user's original mental
    model; `slot` (ChunkSummarizer) remains the canonical default.
    """

    def __init__(self, c: V36Config) -> None:
        super().__init__()
        self.blocks = nn.ModuleList(
            [DiTStyleBlock(c.d_byte, c.nhead, c.ffn_dim, True, False) for _ in range(c.summarizer_dit_layers)]
        )
        self.ffn = nn.Sequential(
            nn.LayerNorm(c.d_byte),
            nn.Linear(c.d_byte, c.summarizer_hidden),
            nn.SiLU(),
            nn.Linear(c.summarizer_hidden, c.d_mem),
        )
        # v3.7 (consensus §1.1): the summarizer owns the K interface -- one
        # index vector per chunk, same width as memory (d_mem). Created ONLY in
        # slm mode so pre-v3.7 checkpoints keep loading strict-clean.
        if getattr(c, "backbone_mode", "") == "slm":
            self.index_ffn = nn.Sequential(
                nn.LayerNorm(c.d_byte),
                nn.Linear(c.d_byte, c.summarizer_hidden),
                nn.SiLU(),
                nn.Linear(c.summarizer_hidden, c.d_mem),
            )

    def _pool(self, spans: torch.Tensor, token_mask: torch.Tensor) -> torch.Tensor:
        bsz, chunks, span, dim = spans.shape
        h = spans.reshape(bsz * chunks, span, dim)
        valid = token_mask.reshape(bsz * chunks, span)
        noise = h.new_zeros(h.size(0))
        for block in self.blocks:
            h = block(h, valid, noise)
        denom = valid.sum(dim=1, keepdim=False).clamp(min=1).unsqueeze(-1).to(h.dtype)
        return (h * valid.unsqueeze(-1).to(h.dtype)).sum(dim=1) / denom  # (B*C, d_byte)

    def forward(self, spans: torch.Tensor, token_mask: torch.Tensor) -> torch.Tensor:
        bsz, chunks = spans.shape[0], spans.shape[1]
        return self.ffn(self._pool(spans, token_mask)).view(bsz, chunks, -1)

    def forward_with_index(self, spans: torch.Tensor, token_mask: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """v3.7 slm mode: shared DiT stack + pooling, two heads -- memory (the
        V rows) and index (the K rows), one vector per chunk each."""
        bsz, chunks = spans.shape[0], spans.shape[1]
        pooled = self._pool(spans, token_mask)
        memory = self.ffn(pooled).view(bsz, chunks, -1)
        index = self.index_ffn(pooled).view(bsz, chunks, -1)
        return memory, index


class WriteHead(nn.Module):
    def __init__(self, c: V36Config) -> None:
        super().__init__()
        h, hk, hv = c.kda_heads, c.kda_head_k, c.kda_head_v
        self.heads, self.hk, self.hv = h, hk, hv
        self.recurrence = getattr(c, "recurrence", "kda")
        if self.recurrence not in ("kda", "gdn2"):
            raise ValueError(f"recurrence must be 'kda' or 'gdn2', got {self.recurrence!r}")
        # E79 split-trunk (see V36Config.split_trunk): two independent trunks
        # when on (trunk_k -> to_k; trunk_v -> to_v/to_beta/to_b/to_w), so the
        # to_k-side training dynamics cannot deform the value content through
        # a shared trunk. Default off = the shared `trunk` (bit-preserved).
        self.split_trunk = getattr(c, "split_trunk", False)
        if self.split_trunk:
            self.trunk_k = nn.Sequential(nn.LayerNorm(c.d_mem), nn.Linear(c.d_mem, c.write_hidden), nn.SiLU())
            self.trunk_v = nn.Sequential(nn.LayerNorm(c.d_mem), nn.Linear(c.d_mem, c.write_hidden), nn.SiLU())
        else:
            self.trunk = nn.Sequential(nn.LayerNorm(c.d_mem), nn.Linear(c.d_mem, c.write_hidden), nn.SiLU())
        self.to_k = nn.Linear(c.write_hidden, h * hk)
        self.to_v = nn.Linear(c.write_hidden, h * hv)
        # E75 key-decollapse hard constraint (see V36Config.to_k_center):
        # subtract the running center from the to_k output, pre-normalization.
        self.to_k_center = getattr(c, "to_k_center", False)
        self.to_k_whiten = getattr(c, "to_k_whiten", False)
        if self.to_k_center or self.to_k_whiten:
            self.register_buffer("k_center", torch.zeros(h * hk), persistent=False)
        if self.to_k_whiten:
            # Q10 gate (see V36Config.to_k_whiten): full whitening superset of
            # centering. k_cov = EMA of the pre-normalization key covariance;
            # k_white = (k_cov + eps I)^{-1/2} refreshed every training step.
            self.register_buffer("k_cov", torch.zeros(h * hk, h * hk), persistent=False)
            self.register_buffer("k_white", torch.eye(h * hk), persistent=False)
        tau = torch.exp(
            torch.linspace(0.0, 1.0, h * hk) * (torch.log(torch.tensor(c.kda_tau_max)))
        ).clamp(min=1.0 + 1e-3)
        self.alpha_logit = nn.Parameter(torch.log(tau - 1.0))
        self.to_beta = nn.Linear(c.write_hidden, h)
        nn.init.constant_(self.to_beta.bias, -2.0)
        if self.recurrence == "gdn2":
            # S39 stage-2: erase/write gate decoupling -- b (per K channel)
            # takes over beta's erase role, w (per V channel) its write role.
            # Created only in gdn2 mode so older checkpoints keep loading
            # strict-clean (the xcache_supp conditional-creation precedent);
            # the same -2.0 bias init as to_beta (sigmoid(-2) ~= 0.12).
            self.to_b = nn.Linear(c.write_hidden, h * hk)
            self.to_w = nn.Linear(c.write_hidden, h * hv)
            nn.init.constant_(self.to_b.bias, -2.0)
            nn.init.constant_(self.to_w.bias, -2.0)

    def forward(self, memory: torch.Tensor) -> dict[str, torch.Tensor]:
        bsz, chunks, _ = memory.shape
        if self.split_trunk:
            h_k = self.trunk_k(memory)
            h_v = self.trunk_v(memory)
        else:
            h_k = h_v = self.trunk(memory)
        k = self.to_k(h_k)
        if self.to_k_whiten:
            # Q10 gate: whiten = de-mean + decorrelate + equalize variance
            # (superset of the centering branch). EMA momentum 0.99, detached —
            # the gradient path to to_k stays live. Eval uses the frozen
            # buffers (zero center + identity white = no-op until warmed, same
            # caveat as to_k_center).
            if self.training:
                with torch.no_grad():
                    kd = k.detach().float()
                    m = kd.mean(dim=(0, 1))
                    xc = kd.reshape(-1, kd.size(-1)) - m
                    cov = (xc.T @ xc) / max(xc.size(0), 1)
                    if not bool(self.k_center.any()):
                        self.k_center.copy_(m)
                        self.k_cov.copy_(cov)
                    else:
                        self.k_center.mul_(0.99).add_(m, alpha=0.01)
                        self.k_cov.mul_(0.99).add_(cov, alpha=0.01)
                    d = kd.size(-1)
                    eps = (self.k_cov.diagonal().mean() * 1e-3).clamp_min(1e-8)
                    evals, evecs = torch.linalg.eigh(
                        self.k_cov + eps * torch.eye(d, device=self.k_cov.device, dtype=self.k_cov.dtype)
                    )
                    self.k_white.copy_(
                        (evecs * evals.clamp_min(1e-12).rsqrt()) @ evecs.T
                    )
            k = ((k.float() - self.k_center) @ self.k_white).to(k.dtype)
        elif self.to_k_center:
            # E75: subtract the running center (EMA momentum 0.99, detached —
            # the gradient path to to_k stays live; cold start initializes from
            # the first batch, BatchNorm convention). Eval uses the frozen
            # buffer (a zero buffer is a no-op — see the config docstring).
            if self.training:
                with torch.no_grad():
                    m = k.detach().float().mean(dim=(0, 1))
                    if not bool(self.k_center.any()):
                        self.k_center.copy_(m)
                    else:
                        self.k_center.mul_(0.99).add_(m, alpha=0.01)
            k = k - self.k_center.to(k.dtype)
        k = F.normalize(k.view(bsz, chunks, self.heads, self.hk), dim=-1)
        v = self.to_v(h_v).view(bsz, chunks, self.heads, self.hv)
        alpha = torch.sigmoid(self.alpha_logit).view(1, 1, self.heads, self.hk)
        if self.recurrence == "gdn2":
            b = torch.sigmoid(self.to_b(h_v)).view(bsz, chunks, self.heads, self.hk)
            w = torch.sigmoid(self.to_w(h_v)).view(bsz, chunks, self.heads, self.hv)
            return {"k": k, "v": v, "b": b, "w": w, "alpha": alpha}
        beta = torch.sigmoid(self.to_beta(h_v))
        return {"k": k, "v": v, "beta": beta, "alpha": alpha}


PROBE_FRAME_SEED = 20260819  # fork 2 measurement frame seed (pinned in the spec)
PROBE_FRAME_ROTS = 64  # per-segment rotation table size (segment i uses table[i % 64])


def probe_frame(m: int, heads: int, hk: int, seed: int = PROBE_FRAME_SEED) -> torch.Tensor:
    """fork 2 §1.1: seeded random orthogonal probe frame — m orthonormal probe
    directions per head, (H, m, hk), training-free. Deterministic under the
    pinned seed (same frame in every process, training and eval alike)."""
    gen = torch.Generator().manual_seed(seed)
    frames = []
    for _h in range(heads):
        q, _r = torch.linalg.qr(torch.randn(hk, m, generator=gen))  # (hk, m) orthonormal columns
        frames.append(q.T.contiguous())  # (m, hk) orthonormal rows
    return torch.stack(frames)


def frame_rotations(count: int, hk: int, seed: int = PROBE_FRAME_SEED + 1) -> torch.Tensor:
    """fork 2 §1.1 "按段索引旋转一次": a seeded table of `count` orthogonal
    (hk, hk) rotations; segment i reads the state with frame @ table[i % count]
    so the measurement directions are not shared across segments."""
    gen = torch.Generator().manual_seed(seed)
    rots = []
    for _i in range(count):
        q, _r = torch.linalg.qr(torch.randn(hk, hk, generator=gen))
        rots.append(q.contiguous())
    return torch.stack(rots)


class KDAStateMachine(nn.Module):
    def __init__(self, c: V36Config) -> None:
        super().__init__()
        self.c = c
        # S39 stage-2: "gdn2" swaps the shared scalar beta for decoupled
        # per-K-channel erase (b) / per-V-channel write (w) gates; every
        # readout below branches on this flag, torch reference and fla kernel
        # alike. The decay gate and delta form are unchanged.
        self.gdn2 = getattr(c, "recurrence", "kda") == "gdn2"
        self.readout_query = nn.Parameter(torch.empty(c.readout_queries, c.kda_heads, c.kda_head_k))
        nn.init.trunc_normal_(self.readout_query, std=0.02)
        self.realign = nn.Sequential(
            nn.LayerNorm(c.kda_heads * c.kda_head_v),
            nn.Linear(c.kda_heads * c.kda_head_v, c.d_pack),
            nn.SiLU(),
            nn.Linear(c.d_pack, c.d_pack),
        )
        # S38 supplementary readout head (only when enabled, so older
        # checkpoints keep loading strict-clean): content-conditioned second
        # query per hard chunk -- "ask the state again about THIS chunk"
        if getattr(c, "xcache_supp", 0) > 0:
            self.supp_q = nn.Linear(c.d_pack, c.kda_heads * c.kda_head_k, bias=False)
            self.supp_out = nn.Linear(c.kda_heads * c.kda_head_v, c.d_pack, bias=False)
        # fork 2 multi-view readout (see V36Config.readout_views): seeded
        # orthogonal probe frame + per-segment rotation table. Buffers are
        # persistent=False BY RULING: no new parameters/state, so every
        # checkpoint loads strict-clean either way and the frames are rebuilt
        # from the pinned seed at construction.
        self.readout_views = getattr(c, "readout_views", 1)
        if self.readout_views > 1:
            self.register_buffer(
                "view_frame", probe_frame(self.readout_views, c.kda_heads, c.kda_head_k), persistent=False
            )
            self.register_buffer(
                "view_rots", frame_rotations(PROBE_FRAME_ROTS, c.kda_head_k), persistent=False
            )

    def forward_views(self, gates: dict[str, torch.Tensor], chunk_mask: torch.Tensor) -> torch.Tensor:
        """fork 2 §1.1: per-chunk m measurement rows. Segment i is read with
        the seeded frame rotated by table[i % P]; each view's read passes the
        SHARED realign (m 路共享 — no new parameters). Returns (B, C, m,
        d_pack); padded chunk rows are garbage-but-masked exactly like the
        main path. Only the kda recurrence is wired (gdn2 raises loudly —
        out of fork-2 scope)."""
        if self.gdn2:
            raise ValueError("forward_views (readout_views>1) supports recurrence='kda' only")
        m = self.readout_views
        if m <= 1:
            raise ValueError("forward_views requires readout_views > 1")
        k, v, alpha = gates["k"], gates["v"], gates["alpha"]
        beta = gates["beta"]
        keep = chunk_mask.unsqueeze(-1).unsqueeze(-1).to(k.dtype)
        k = k * keep
        v = v * keep
        bsz, chunks, heads, dk = k.shape
        dv = v.size(-1)
        beta = beta * chunk_mask.unsqueeze(-1).to(beta.dtype)
        g = torch.log(alpha.clamp_min(1.0e-6)).to(k.dtype) * keep
        # per-chunk rotated queries: q[c, h, r] = frame[h, r] @ rots[c % P].
        # NOTE: einsum is autocast-managed and would run bf16 here while the
        # kernel's other operands are fp32 (normalize/sigmoid promote) — the
        # bwd kernel demands uniform dtypes, so compute q outside autocast.
        idx = torch.arange(chunks, device=k.device) % self.view_rots.size(0)
        with torch.autocast(k.device.type, enabled=False):
            q_all = torch.einsum(
                "hro,cok->chrk", self.view_frame.float(), self.view_rots[idx].float()
            ).to(k.dtype)
        outs = []
        if self.c.kda_impl == "fla" and _fla_chunk_kda is not None:
            for r in range(m):
                q_r = q_all[:, :, r].unsqueeze(0).expand(bsz, -1, -1, -1).contiguous()  # (B, C, H, hk)
                o, _ = _fla_chunk_kda(
                    q=q_r, k=k, v=v,
                    g=g.expand(bsz, chunks, -1, -1).contiguous(),
                    beta=beta, scale=1.0, use_qk_l2norm_in_kernel=False,
                    output_final_state=False,
                )
                outs.append(o)  # (B, C, H, hv)
        else:
            # torch reference: serial recurrence, per-chunk rotated reads
            state = k.new_zeros(bsz, heads, dk, dv, dtype=torch.float32)
            kf, vf = k.float(), v.float()
            alpha_eff = 1.0 - chunk_mask.float().view(bsz, chunks, 1, 1, 1) + chunk_mask.float().view(
                bsz, chunks, 1, 1, 1
            ) * gates["alpha"][0].float().unsqueeze(0).unsqueeze(-1)
            bf = beta.float()
            qf = q_all.float()  # (C, H, m, hk)
            per_chunk = []
            for i in range(chunks):
                ki, vi, bi, ai = kf[:, i], vf[:, i], bf[:, i], alpha_eff[:, i]
                state = ai * state
                kTs = torch.einsum("bhk,bhkv->bhv", ki, state)
                state = state - bi.view(bsz, heads, 1, 1) * ki.unsqueeze(-1) * kTs.unsqueeze(-2)
                state = state + bi.view(bsz, heads, 1, 1) * ki.unsqueeze(-1) * vi.unsqueeze(-2)
                per_chunk.append(torch.einsum("hrk,bhkv->bhrv", qf[i], state))  # (B, H, m, hv)
            o = torch.stack(per_chunk, dim=1)  # (B, C, H, m, hv)
            outs = [o[:, :, :, r] for r in range(m)]  # each (B, C, H, hv)
        read = torch.stack(outs, dim=2)  # (B, C, m, H, hv)
        read = read.reshape(bsz, chunks, m, heads * dv).to(k.dtype)
        return self.realign(read)

    def read_residual(
        self,
        content: torch.Tensor,
        gates: dict[str, torch.Tensor],
        chunk_mask: torch.Tensor,
        write_w: torch.Tensor,
    ) -> torch.Tensor:
        """S38B residual second state S': the SAME gated recurrence but with
        write rates modulated by the detached downstream-failure weight
        write_w (B, C) -- only chunks the codec fails on get written hard
        (CUIB pattern: downstream utility drives upstream allocation).
        Readout reuses the content-conditioned supp projections (independent
        from the main state's fixed readout query)."""
        c = self.c
        k, v, alpha = gates["k"], gates["v"], gates["alpha"]
        beta = None if self.gdn2 else gates["beta"]
        keep = chunk_mask.unsqueeze(-1).unsqueeze(-1).to(k.dtype)
        bsz, chunks, heads, dk = k.shape
        q = F.normalize(self.supp_q(content).view(bsz, chunks, heads, dk).float(), dim=-1).to(k.dtype)
        w = write_w.unsqueeze(-1).to(k.dtype)  # (B, C, 1) -- beta shares k's dtype
        kernel = _fla_chunk_gdn2 if self.gdn2 else _fla_chunk_kda
        if c.kda_impl == "fla" and kernel is not None:
            kk = k * keep
            vv = v * keep
            g = torch.log(alpha.clamp_min(1.0e-6)).to(k.dtype) * keep
            if self.gdn2:
                # gdn2: the detached CUIB weight modulates BOTH decoupled gates
                # (collapses to kda's beta*w when b == w == beta).
                mod = (w * chunk_mask.unsqueeze(-1).to(k.dtype)).unsqueeze(-1)  # (B, C, 1, 1)
                o, _ = _fla_chunk_gdn2(
                    q=q.contiguous(),
                    k=kk,
                    v=vv,
                    g=g.expand(bsz, chunks, -1, -1).contiguous(),
                    b=(gates["b"] * mod).contiguous(),
                    w=(gates["w"] * mod).contiguous(),
                    scale=1.0,
                    use_qk_l2norm_in_kernel=False,
                    output_final_state=False,
                )
            else:
                bb = beta * w * chunk_mask.unsqueeze(-1).to(beta.dtype)
                o, _ = _fla_chunk_kda(
                    q=q.contiguous(),
                    k=kk,
                    v=vv,
                    g=g.expand(bsz, chunks, -1, -1).contiguous(),
                    beta=bb,
                    scale=1.0,
                    use_qk_l2norm_in_kernel=False,
                    output_final_state=False,
                )
            read = o.reshape(bsz, chunks, heads * v.size(-1))
        else:
            kf, vf = (k * keep).float(), (v * keep).float()
            alpha_eff = 1.0 - chunk_mask.float().view(bsz, chunks, 1, 1, 1) + chunk_mask.float().view(
                bsz, chunks, 1, 1, 1
            ) * gates["alpha"][0].float().unsqueeze(0).unsqueeze(-1)
            state = k.new_zeros(bsz, heads, dk, v.size(-1), dtype=torch.float32)
            reads = []
            qf = q.float()
            if self.gdn2:
                mod5 = (write_w.float() * chunk_mask.float()).view(bsz, chunks, 1, 1)
                bf = gates["b"].float() * mod5
                wf = gates["w"].float() * mod5
                for i in range(chunks):
                    ki, vi, bi, wi, ai = kf[:, i], vf[:, i], bf[:, i], wf[:, i], alpha_eff[:, i]
                    state = ai * state
                    # gdn2 step: erase along (b * k), commit (w * v) minus the erased read
                    erase = torch.einsum("bhk,bhkv->bhv", bi * ki, state)
                    v_new = wi * vi - erase
                    state = state + ki.unsqueeze(-1) * v_new.unsqueeze(-2)
                    reads.append(torch.einsum("bhk,bhkv->bhv", qf[:, i], state))
            else:
                bf = beta.float() * w.float() * chunk_mask.float().unsqueeze(-1)
                for i in range(chunks):
                    ki, vi, bi, ai = kf[:, i], vf[:, i], bf[:, i], alpha_eff[:, i]
                    state = ai * state
                    kTs = torch.einsum("bhk,bhkv->bhv", ki, state)
                    state = state - bi.view(bsz, heads, 1, 1) * ki.unsqueeze(-1) * kTs.unsqueeze(-2)
                    state = state + bi.view(bsz, heads, 1, 1) * ki.unsqueeze(-1) * vi.unsqueeze(-2)
                    reads.append(torch.einsum("bhk,bhkv->bhv", qf[:, i], state))
            read = torch.stack(reads, dim=1).reshape(bsz, chunks, heads * v.size(-1))
        return self.supp_out(read.to(k.dtype))

    def read_supplementary(
        self, content: torch.Tensor, gates: dict[str, torch.Tensor], chunk_mask: torch.Tensor
    ) -> torch.Tensor:
        """Per-chunk second readout with content-conditioned queries (S38).
        supp_i = normalize(W_q content[i]) . S_i -- a targeted extra slice of
        the state right after chunk i. One extra kernel call."""
        c = self.c
        k, v, alpha = gates["k"], gates["v"], gates["alpha"]
        beta = None if self.gdn2 else gates["beta"]
        keep = chunk_mask.unsqueeze(-1).unsqueeze(-1).to(k.dtype)
        bsz, chunks, heads, dk = k.shape
        q = F.normalize(
            self.supp_q(content).view(bsz, chunks, heads, dk).float(), dim=-1
        ).to(k.dtype)
        kernel = _fla_chunk_gdn2 if self.gdn2 else _fla_chunk_kda
        if c.kda_impl == "fla" and kernel is not None:
            kk = k * keep
            vv = v * keep
            g = torch.log(alpha.clamp_min(1.0e-6)).to(k.dtype) * keep
            if self.gdn2:
                o, _ = _fla_chunk_gdn2(
                    q=q.contiguous(),
                    k=kk,
                    v=vv,
                    g=g.expand(bsz, chunks, -1, -1).contiguous(),
                    b=(gates["b"] * keep).contiguous(),
                    w=(gates["w"] * keep).contiguous(),
                    scale=1.0,
                    use_qk_l2norm_in_kernel=False,
                    output_final_state=False,
                )
            else:
                bb = beta * chunk_mask.unsqueeze(-1).to(beta.dtype)
                o, _ = _fla_chunk_kda(
                    q=q.contiguous(),
                    k=kk,
                    v=vv,
                    g=g.expand(bsz, chunks, -1, -1).contiguous(),
                    beta=bb,
                    scale=1.0,
                    use_qk_l2norm_in_kernel=False,
                    output_final_state=False,
                )
            read = o.reshape(bsz, chunks, heads * v.size(-1))
        else:
            kf, vf = (k * keep).float(), (v * keep).float()
            alpha_eff = 1.0 - chunk_mask.float().view(bsz, chunks, 1, 1, 1) + chunk_mask.float().view(
                bsz, chunks, 1, 1, 1
            ) * gates["alpha"][0].float().unsqueeze(0).unsqueeze(-1)
            state = k.new_zeros(bsz, heads, dk, v.size(-1), dtype=torch.float32)
            reads = []
            qf = q.float()
            if self.gdn2:
                mask4 = chunk_mask.float().view(bsz, chunks, 1, 1)
                bf = gates["b"].float() * mask4
                wf = gates["w"].float() * mask4
                for i in range(chunks):
                    ki, vi, bi, wi, ai = kf[:, i], vf[:, i], bf[:, i], wf[:, i], alpha_eff[:, i]
                    state = ai * state
                    erase = torch.einsum("bhk,bhkv->bhv", bi * ki, state)
                    v_new = wi * vi - erase
                    state = state + ki.unsqueeze(-1) * v_new.unsqueeze(-2)
                    reads.append(torch.einsum("bhk,bhkv->bhv", qf[:, i], state))
            else:
                bf = beta.float() * chunk_mask.float().unsqueeze(-1)
                for i in range(chunks):
                    ki, vi, bi, ai = kf[:, i], vf[:, i], bf[:, i], alpha_eff[:, i]
                    state = ai * state
                    kTs = torch.einsum("bhk,bhkv->bhv", ki, state)
                    state = state - bi.view(bsz, heads, 1, 1) * ki.unsqueeze(-1) * kTs.unsqueeze(-2)
                    state = state + bi.view(bsz, heads, 1, 1) * ki.unsqueeze(-1) * vi.unsqueeze(-2)
                    reads.append(torch.einsum("bhk,bhkv->bhv", qf[:, i], state))
            read = torch.stack(reads, dim=1).reshape(bsz, chunks, heads * v.size(-1))
        return self.supp_out(read.to(k.dtype))

    def read_all_final(
        self, gates: dict[str, torch.Tensor], chunk_mask: torch.Tensor
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """Strict codec-retention arm (user-ruled 2026-08-11, prereg
        FLUED_TODO_20260805 §0.3 item 0): scan the recurrence all the way to
        the FINAL state S_final and read it with the SAME query construction
        as the normal per-chunk path (readout_query -> realign). Every chunk
        row of the window is then served from this single final readout, so
        the fresh per-chunk reads of S_i never enter the loss path and
        retention becomes a trained objective instead of an untested freebie.
        Correctness invariant: for each sample the last valid chunk's normal
        readout already reads S_last == S_final (padded chunks are identity
        steps), so this package must equal the normal per-chunk package at the
        last valid row -- unit-tested at 1e-5. Always uses the serial torch
        scan in fp32: grad-safe under autocast, and independent of whether the
        fla kernel wires a gradient path through its final_state output.
        Returns (package_final, state_norm) with package_final (B, nq, d_pack)
        -- no chunk dim, by construction there is exactly one readout per
        sample."""
        if not self.c.state_channel:
            raise ValueError("read_all_final requires state_channel=True (this arm trains the state channel itself)")
        k, v = gates["k"], gates["v"]
        beta = None if self.gdn2 else gates["beta"]
        keep = chunk_mask.unsqueeze(-1).unsqueeze(-1).to(k.dtype)
        k = k * keep
        v = v * keep
        bsz, chunks, heads, dk = k.shape
        dv = v.size(-1)
        state = k.new_zeros(bsz, heads, dk, dv, dtype=torch.float32)
        kf, vf = k.float(), v.float()
        alpha = gates["alpha"][0].unsqueeze(0).unsqueeze(-1)
        mask5 = chunk_mask.float().view(bsz, chunks, 1, 1, 1)
        alpha_eff = 1.0 - mask5 + mask5 * alpha
        if self.gdn2:
            mask4 = chunk_mask.float().view(bsz, chunks, 1, 1)
            bf = gates["b"].float() * mask4
            wf = gates["w"].float() * mask4
            for i in range(chunks):
                ki, vi, bi, wi, ai = kf[:, i], vf[:, i], bf[:, i], wf[:, i], alpha_eff[:, i]
                state = ai * state
                erase = torch.einsum("bhk,bhkv->bhv", bi * ki, state)
                v_new = wi * vi - erase
                state = state + ki.unsqueeze(-1) * v_new.unsqueeze(-2)
        else:
            beta = beta.float() * chunk_mask.float().unsqueeze(-1)
            for i in range(chunks):
                ki, vi, bi, ai = kf[:, i], vf[:, i], beta[:, i], alpha_eff[:, i]
                state = ai * state
                kTs = torch.einsum("bhk,bhkv->bhv", ki, state)
                state = state - bi.view(bsz, heads, 1, 1) * ki.unsqueeze(-1) * kTs.unsqueeze(-2)
                state = state + bi.view(bsz, heads, 1, 1) * ki.unsqueeze(-1) * vi.unsqueeze(-2)
        q = self.readout_query.float()
        read = torch.einsum("qhk,bhkv->bqhv", q, state)
        read = read.reshape(bsz, q.size(0), heads * dv).to(k.dtype)
        package = self.realign(read)
        return package, state.norm(dim=(-2, -1)).mean()

    def forward(self, gates: dict[str, torch.Tensor], chunk_mask: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        if not self.c.state_channel:
            # R1 relative baseline: bypass the recurrence entirely -- readout
            # per chunk comes from its own write value only. Padded rows are
            # garbage but masked downstream exactly like the main path's
            # stale-state reads, so the comparison stays clean.
            v = gates["v"]
            read = v.reshape(v.size(0), v.size(1), 1, self.c.kda_heads * self.c.kda_head_v)
            return self.realign(read), v.new_zeros((), dtype=torch.float32)
        if self.c.kda_impl == "fla":
            kernel = _fla_chunk_gdn2 if self.gdn2 else _fla_chunk_kda
            if kernel is None:
                warnings.warn(
                    "kda_impl='fla' but fla is unavailable; falling back to the torch recurrence",
                    stacklevel=2,
                )
            else:
                return self._forward_fla(gates, chunk_mask)
        return self._forward_torch(gates, chunk_mask)

    def _forward_fla(self, gates: dict[str, torch.Tensor], chunk_mask: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        k, v, alpha = gates["k"], gates["v"], gates["alpha"]
        beta = None if self.gdn2 else gates["beta"]
        keep = chunk_mask.unsqueeze(-1).unsqueeze(-1).to(k.dtype)
        k = k * keep
        v = v * keep
        bsz, chunks, heads, dk = k.shape
        if not self.gdn2:
            beta = beta * chunk_mask.unsqueeze(-1).to(beta.dtype)
        # g in log space; zero at padded chunks -> decay exp(0)=1 (identity step)
        g = torch.log(alpha.clamp_min(1.0e-6)).to(k.dtype) * keep
        q = self.readout_query
        outs = []
        final_state = None
        for qi in range(q.size(0)):
            if self.gdn2:
                o, final_state = _fla_chunk_gdn2(
                    q=q[qi].to(k.dtype).unsqueeze(0).unsqueeze(0).expand(bsz, chunks, -1, -1).contiguous(),
                    k=k,
                    v=v,
                    g=g.expand(bsz, chunks, -1, -1).contiguous(),
                    b=(gates["b"] * keep).contiguous(),
                    w=(gates["w"] * keep).contiguous(),
                    scale=1.0,
                    use_qk_l2norm_in_kernel=False,
                    output_final_state=True,
                )
            else:
                o, final_state = _fla_chunk_kda(
                    q=q[qi].to(k.dtype).unsqueeze(0).unsqueeze(0).expand(bsz, chunks, -1, -1).contiguous(),
                    k=k,
                    v=v,
                    g=g.expand(bsz, chunks, -1, -1).contiguous(),
                    beta=beta,
                    scale=1.0,
                    use_qk_l2norm_in_kernel=False,
                    output_final_state=True,
                )
            outs.append(o)
        o = torch.stack(outs, dim=2)  # (B, C, nq, H, V)
        read = o.reshape(bsz, chunks, q.size(0), heads * v.size(-1))
        if self.c.per_chunk_readout:
            package = self.realign(read)
        else:
            package = self.realign(read[:, -1])
        return package, final_state.float().norm(dim=(-2, -1)).mean()

    def _forward_torch(self, gates: dict[str, torch.Tensor], chunk_mask: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        k, v, alpha = gates["k"], gates["v"], gates["alpha"]
        beta = None if self.gdn2 else gates["beta"]
        keep = chunk_mask.unsqueeze(-1).unsqueeze(-1).to(k.dtype)
        k = k * keep
        v = v * keep
        bsz, chunks, heads, dk = k.shape
        dv = v.size(-1)
        state = k.new_zeros(bsz, heads, dk, dv, dtype=torch.float32)
        kf, vf = k.float(), v.float()
        alpha = gates["alpha"][0].unsqueeze(0).unsqueeze(-1)
        mask5 = chunk_mask.float().view(bsz, chunks, 1, 1, 1)
        alpha_eff = 1.0 - mask5 + mask5 * alpha
        q = self.readout_query.float()
        per_chunk_reads = []
        if self.gdn2:
            mask4 = chunk_mask.float().view(bsz, chunks, 1, 1)
            bf = gates["b"].float() * mask4
            wf = gates["w"].float() * mask4
            for i in range(chunks):
                ki, vi, bi, wi, ai = kf[:, i], vf[:, i], bf[:, i], wf[:, i], alpha_eff[:, i]
                state = ai * state
                erase = torch.einsum("bhk,bhkv->bhv", bi * ki, state)
                v_new = wi * vi - erase
                state = state + ki.unsqueeze(-1) * v_new.unsqueeze(-2)
                if self.c.per_chunk_readout:
                    # Read the state right after consuming chunk i: each chunk gets
                    # its own conditioning vector instead of the whole-prompt mean.
                    per_chunk_reads.append(torch.einsum("qhk,bhkv->bqhv", q, state))
        else:
            beta = beta.float() * chunk_mask.float().unsqueeze(-1)
            for i in range(chunks):
                ki, vi, bi, ai = kf[:, i], vf[:, i], beta[:, i], alpha_eff[:, i]
                state = ai * state
                kTs = torch.einsum("bhk,bhkv->bhv", ki, state)
                state = state - bi.view(bsz, heads, 1, 1) * ki.unsqueeze(-1) * kTs.unsqueeze(-2)
                state = state + bi.view(bsz, heads, 1, 1) * ki.unsqueeze(-1) * vi.unsqueeze(-2)
                if self.c.per_chunk_readout:
                    # Read the state right after consuming chunk i: each chunk gets
                    # its own conditioning vector instead of the whole-prompt mean.
                    per_chunk_reads.append(torch.einsum("qhk,bhkv->bqhv", q, state))
        if self.c.per_chunk_readout:
            read = torch.stack(per_chunk_reads, dim=1)  # (B, C, q, heads*dv)
            read = read.reshape(bsz, chunks, q.size(0), heads * dv).to(k.dtype)
        else:
            read = torch.einsum("qhk,bhkv->bqhv", q, state)
            read = read.reshape(bsz, q.size(0), heads * dv).to(k.dtype)
        package = self.realign(read)
        return package, state.norm(dim=(-2, -1)).mean()

    def init_stream_state(self, bsz: int, device: torch.device | str) -> torch.Tensor:
        """Zero KDA state for incremental/streaming encoding (inference side)."""
        c = self.c
        return torch.zeros(
            bsz, c.kda_heads, c.kda_head_k, c.kda_head_v, device=device, dtype=torch.float32
        )

    @torch.no_grad()
    def stream_step(
        self, gates_i: dict[str, torch.Tensor], state: torch.Tensor
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """Consume ONE chunk's write gates, read the updated state, carry it on.

        Streaming primitive: encoding chunk-by-chunk with a carried state avoids
        recomputing the recurrence from scratch for every prefix (O(C^2) ->
        O(C)). ``gates_i`` holds one chunk (shapes (B, 1, H, K/V) etc., as
        produced by WriteHead on a single memory row). Returns
        ``(package_i, new_state)`` where ``package_i`` is (B, 1, nq, d_pack),
        matching column i of the batched per-chunk package. Uses the fla
        fused-recurrent kernel when ``kda_impl == "fla"`` (falling back to the
        pure-torch update when fla is unavailable).
        """
        c = self.c
        kernel = _fla_chunk_gdn2 if self.gdn2 else _fla_chunk_kda
        if c.kda_impl == "fla" and kernel is not None:
            k, v, alpha = gates_i["k"], gates_i["v"], gates_i["alpha"]
            bsz = k.size(0)
            g = torch.log(alpha.clamp_min(1.0e-6)).to(k.dtype).expand(bsz, 1, -1, -1).contiguous()
            q = self.readout_query
            outs = []
            new_state = state
            if self.gdn2:
                from fla.ops.gdn2 import fused_recurrent_gdn2

                for qi in range(q.size(0)):
                    o, new_state = fused_recurrent_gdn2(
                        q=q[qi].to(k.dtype).unsqueeze(0).unsqueeze(0).expand(bsz, 1, -1, -1).contiguous(),
                        k=k,
                        v=v,
                        g=g,
                        b=gates_i["b"],
                        w=gates_i["w"],
                        scale=1.0,
                        initial_state=state,
                        output_final_state=True,
                        use_qk_l2norm_in_kernel=False,
                    )
                    outs.append(o)
            else:
                from fla.ops.kda import fused_recurrent_kda

                for qi in range(q.size(0)):
                    o, new_state = fused_recurrent_kda(
                        q=q[qi].to(k.dtype).unsqueeze(0).unsqueeze(0).expand(bsz, 1, -1, -1).contiguous(),
                        k=k,
                        v=v,
                        g=g,
                        beta=gates_i["beta"],
                        scale=1.0,
                        initial_state=state,
                        output_final_state=True,
                        use_qk_l2norm_in_kernel=False,
                    )
                    outs.append(o)
            o = torch.stack(outs, dim=2)  # (B, 1, nq, H, V)
            read = o.reshape(bsz, 1, q.size(0), c.kda_heads * c.kda_head_v)
            return self.realign(read), new_state

        # Pure-torch fallback: same update math as _forward_torch, one chunk.
        k, v = gates_i["k"], gates_i["v"]
        bsz = k.size(0)
        heads, dv = c.kda_heads, c.kda_head_v
        kf, vf = k.float(), v.float()
        ai = gates_i["alpha"][0].float().unsqueeze(-1)  # (1, H, K, 1)
        ki, vi = kf[:, 0], vf[:, 0]
        state = ai * state
        if self.gdn2:
            bi = gates_i["b"].float()[:, 0]  # (B, H, K) — a real chunk, mask == 1
            wi = gates_i["w"].float()[:, 0]  # (B, H, V)
            erase = torch.einsum("bhk,bhkv->bhv", bi * ki, state)
            v_new = wi * vi - erase
            state = state + ki.unsqueeze(-1) * v_new.unsqueeze(-2)
        else:
            bi = gates_i["beta"].float()[:, 0]  # (B, H) — a real chunk, mask == 1
            kTs = torch.einsum("bhk,bhkv->bhv", ki, state)
            state = state - bi.view(bsz, heads, 1, 1) * ki.unsqueeze(-1) * kTs.unsqueeze(-2)
            state = state + bi.view(bsz, heads, 1, 1) * ki.unsqueeze(-1) * vi.unsqueeze(-2)
        q = self.readout_query.float()
        read = torch.einsum("qhk,bhkv->bqhv", q, state)
        read = read.reshape(bsz, 1, q.size(0), heads * dv).to(k.dtype)
        return self.realign(read), state


def _xcache_select(scores: torch.Tensor, chunk_mask: torch.Tensor, frac: float) -> torch.Tensor:
    """S36 residual-gated cache selection (HOLA/HAM): per sample, rank real
    chunks by score (residual) and keep the top round(frac*n_real); returns
    (B, C) long with -1 padding past each sample's keep count (masked by the
    caller). Sync-free: the keep count stays on device and the tensor width
    is the static chunk grid."""
    bsz, n = chunk_mask.shape
    n_real = chunk_mask.long().sum(dim=1)
    if frac <= 0.0:
        # honest zero-row control (methodology fix 2026-08-09): the store is
        # the gist token only; every cache slot is -1 (masked downstream)
        return torch.full((bsz, n), -1, dtype=torch.long, device=chunk_mask.device)
    k_keep = (n_real.float() * frac).round().long().clamp(min=1)  # (B,)
    order = scores.masked_fill(~chunk_mask, float("-inf")).argsort(dim=1, descending=True)
    rank = torch.arange(n, device=chunk_mask.device).unsqueeze(0)
    cache_idx = torch.where(rank < k_keep.unsqueeze(1), order, torch.full_like(order, -1))
    return cache_idx.sort(dim=1).values  # -1 sinks first; masked downstream


POS_FEAT_DIM = 64  # 16 frequencies x (sin, cos) x 2 scalars (segment order, start byte)


def chunk_byte_offsets(token_mask: torch.Tensor) -> torch.Tensor:
    """Window-relative per-chunk start byte offsets (S39 a+pos): exclusive
    cumsum of the per-chunk byte counts derived from token_mask (B, C, S);
    returns (B, C) long. Padded chunks (zero bytes) inherit the running
    offset; they are masked downstream."""
    clen = token_mask.long().sum(dim=2)
    return clen.cumsum(dim=1) - clen


def _pos_features(seg_idx: torch.Tensor, byte_off: torch.Tensor) -> torch.Tensor:
    """Sinusoidal key-row position features (S39 a+pos, same form as the 0a
    probe's position_features): per key row, 16 frequencies x (sin, cos) for
    each of two absolute-position scalars -- the segment order (row index)
    and the segment's window-relative start byte offset; max period 1e4.
    seg_idx/byte_off: (B, n) -> (B, n, POS_FEAT_DIM)."""

    def sincos(x: torch.Tensor) -> torch.Tensor:
        freqs = torch.exp(-math.log(1e4) * torch.arange(16, dtype=torch.float32, device=x.device) / 16)
        ang = x.float().unsqueeze(-1) * freqs
        return torch.cat([ang.sin(), ang.cos()], dim=-1)

    return torch.cat([sincos(seg_idx), sincos(byte_off)], dim=-1)


def paged_boundaries(chunk_mask: torch.Tensor, n: int) -> tuple[torch.Tensor, torch.Tensor]:
    """/n paging geometry (backbone_readout="paged", user-ruled 2026-08-07).

    Returns (boundary, serve):
    - boundary: (B, n) long -- the chunk index whose state read closes sub-page j
      (each read is causal to its position: it contains chunks 0..boundary).
    - serve: (B, C) long -- chunk i is conditioned on the FIRST read whose
      boundary covers it (serve(b,i) = min{ j : boundary(b,j) >= i }), so a read
      never serves a chunk written after it. n=1 reproduces "final" (the whole
      window served by the last read); n=C reproduces per-chunk.
    """
    device = chunk_mask.device
    c_real = chunk_mask.long().sum(dim=1).clamp(min=1)  # (B,)
    j = torch.arange(n, device=device)
    boundary = ((j + 1).unsqueeze(0) * c_real.unsqueeze(1) // n - 1).clamp(min=0)
    boundary = torch.minimum(boundary, (c_real - 1).unsqueeze(1))  # (B, n)
    i = torch.arange(chunk_mask.size(1), device=device)
    serve = (boundary.unsqueeze(2) < i.view(1, 1, -1)).sum(dim=1).clamp(max=n - 1)  # (B, C)
    return boundary, serve


class CrossReadBackbone(nn.Module):
    """Causal cross-read backbone (s31): the backbone issues one query per chunk
    position and retrieves from the encoder's memory rows STRICTLY causally
    (position i sees memory[0..i] only). The Kimi-Linear lesson mapped onto
    FLUED: the KDA state stays the lossy streaming compressor; exact retrieval
    flows through a thin causal channel over the least-processed store
    (pre-state memory). Distinct from s16 on both axes: causal (not
    bidirectional) and reads memory (not state readouts).
    """

    def __init__(self, c: V36Config) -> None:
        super().__init__()
        self.nhead = c.backbone_nhead
        self.in_proj = nn.Linear(c.d_pack, c.d_backbone) if c.d_pack != c.d_backbone else nn.Identity()
        self.q_proj = nn.Linear(c.d_backbone, c.d_backbone, bias=False)
        self.k_proj = nn.Linear(c.d_mem, c.d_backbone, bias=False)
        self.v_proj = nn.Linear(c.d_mem, c.d_backbone, bias=False)
        self.o_proj = nn.Linear(c.d_backbone, c.d_backbone, bias=False)
        # S36 gist token projections (k=1 final readout as the first store
        # entry); created only when the gist is enabled so s31 checkpoints
        # keep loading strict-clean. S37 (paged_xattn) always needs them --
        # page gist entries go through these projections.
        if getattr(c, "xcache_gist", False) or getattr(c, "backbone_mode", "") == "paged_xattn":
            self.gist_k = nn.Linear(c.d_pack, c.d_backbone, bias=False)
            self.gist_v = nn.Linear(c.d_pack, c.d_backbone, bias=False)
        # S39 stage-1 taxonomy 2x2: dedicated d_pack -> d_backbone projections
        # for the "state" K/V source (per-chunk state readouts); created only
        # when selected so (memory,memory) checkpoints keep loading
        # strict-clean (same precedent as gist_k/gist_v above).
        k_src = getattr(c, "k_row_source", "memory")
        v_src = getattr(c, "v_row_source", "memory")
        if k_src not in ("memory", "state") or v_src not in ("memory", "state"):
            raise ValueError(f"k/v_row_source must be 'memory' or 'state', got {k_src!r}/{v_src!r}")
        if (k_src == "state" or v_src == "state") and getattr(c, "backbone_mode", "") == "paged_xattn":
            raise ValueError("k/v_row_source='state' is undefined for paged_xattn (content rows are page-level there)")
        self.k_from_state = k_src == "state"
        self.v_from_state = v_src == "state"
        if self.k_from_state:
            self.k_proj_state = nn.Linear(c.d_pack, c.d_backbone, bias=False)
        if self.v_from_state:
            self.v_proj_state = nn.Linear(c.d_pack, c.d_backbone, bias=False)
        # S39 a+pos arm (appendix C): position-injected keys -- pos_proj maps
        # the sinusoidal (segment order, window-relative start byte) features
        # into the key space, added through the zero-init scalar gate
        # pos_gate (step 0 == the a-grid anchor; the gate value is itself the
        # diagnostic readout). Memory-source only; created only when enabled
        # so old checkpoints keep loading strict-clean.
        self.k_pos_inject = getattr(c, "k_pos_inject", False)
        if self.k_pos_inject:
            if k_src != "memory" or v_src != "memory":
                raise ValueError(
                    "k_pos_inject requires k/v_row_source='memory' "
                    "(a+pos is the a-grid K-side single-variable arm)"
                )
            self.pos_proj = nn.Linear(POS_FEAT_DIM, c.d_backbone, bias=False)
            self.pos_gate = nn.Parameter(torch.zeros(()))
        self.blocks = nn.ModuleList(
            [
                nn.Sequential(
                    nn.LayerNorm(c.d_backbone),
                    nn.Linear(c.d_backbone, c.backbone_ffn),
                    nn.GELU(),
                    nn.Linear(c.backbone_ffn, c.d_backbone),
                )
                for _ in range(c.backbone_layers)
            ]
        )
        self.norm = nn.LayerNorm(c.d_backbone)

    def forward(
        self,
        content: torch.Tensor,
        memory: torch.Tensor,
        chunk_mask: torch.Tensor,
        pos: torch.Tensor,
        cache_idx: torch.Tensor | None = None,
        gist: torch.Tensor | None = None,
        query_pos: torch.Tensor | None = None,
        gist_pos: torch.Tensor | None = None,
        supp: torch.Tensor | None = None,
        supp_idx: torch.Tensor | None = None,
        chunk_byte_off: torch.Tensor | None = None,
    ) -> torch.Tensor:
        bsz, n, _ = content.shape
        h = self.in_proj(content)
        nh = self.nhead
        hd = h.size(-1) // nh
        q = (self.q_proj(h) + pos).view(bsz, n, nh, hd).transpose(1, 2)
        if cache_idx is None and gist is None:
            # legacy s31 path: causal over all real rows; the S39 source
            # switches pick the K/V source tensor per side (memory rows by
            # default, the per-chunk state readouts when "state")
            k_proj = self.k_proj_state if self.k_from_state else self.k_proj
            v_proj = self.v_proj_state if self.v_from_state else self.v_proj
            k_in = content if self.k_from_state else memory
            v_in = content if self.v_from_state else memory
            k_flat = k_proj(k_in)
            if self.k_pos_inject:
                # a+pos: add the sinusoidal key-row features through the
                # zero-init gate, before the head reshape (shared by all heads)
                if chunk_byte_off is None:
                    raise ValueError("k_pos_inject requires chunk_byte_off (window-relative per-chunk start byte offsets)")
                seg_idx = torch.arange(n, device=content.device).unsqueeze(0).expand(bsz, n)
                k_flat = k_flat + self.pos_gate * self.pos_proj(_pos_features(seg_idx, chunk_byte_off))
            k = k_flat.view(bsz, n, nh, hd).transpose(1, 2)
            v = v_proj(v_in).view(bsz, n, nh, hd).transpose(1, 2)
            future = torch.triu(torch.ones(n, n, dtype=torch.bool, device=content.device), diagonal=1)
            allowed = (~future).view(1, 1, n, n) & chunk_mask.view(bsz, 1, 1, n)
            # keep the diagonal even on padded rows: a fully-masked SDPA row yields
            # NaN, and 0*NaN poisons downstream (documented padding-NaN pitfall)
            allowed = allowed | torch.eye(n, dtype=torch.bool, device=content.device).view(1, 1, n, n)
            o = F.scaled_dot_product_attention(q, k, v, attn_mask=allowed)
        else:
            # S36/S36-store path, generalized for S37: the store is
            # [gist entries] + [selected memory rows]. gist may be (B, d_pack)
            # (single token, visible to all) or (B, G, d_pack) with gist_pos --
            # then entry g is visible to query i iff gist_pos[g] <= query_pos[i]
            # (page-level causality for the paged-gist form). Cache rows carry
            # original chunk indices in cache_idx with the same comparison.
            if gist is None:
                raise ValueError("residual-gated cache requires the gist token")
            device = content.device
            if query_pos is None:
                query_pos = torch.arange(n, device=device).unsqueeze(0).expand(bsz, n)
            if gist.dim() == 2:
                gist = gist.unsqueeze(1)
            gsz = gist.size(1)
            ks = [self.gist_k(gist)]
            vs = [self.gist_v(gist)]
            if gist_pos is None:
                allowed_g = torch.ones(bsz, n, gsz, dtype=torch.bool, device=device)
            else:
                allowed_g = gist_pos.view(bsz, 1, gsz) <= query_pos.view(bsz, n, 1)
            allowed_parts = [allowed_g]
            kk = cache_idx.size(1)
            gidx = cache_idx.clamp(min=0).unsqueeze(-1)
            # S39 source switches: the selected store entries take their K/V
            # side inputs from the state readouts (content) when "state" is
            # selected, else from the pre-state memory rows (default)
            if self.k_from_state or self.v_from_state:
                sel_state = content.gather(1, gidx.expand(-1, -1, content.size(-1)))
            if not (self.k_from_state and self.v_from_state):
                sel_mem = memory.gather(1, gidx.expand(-1, -1, memory.size(-1)))
            k_rows = self.k_proj_state(sel_state) if self.k_from_state else self.k_proj(sel_mem)
            if self.k_pos_inject:
                # a+pos: features taken at the selected rows' real chunk indices
                if chunk_byte_off is None:
                    raise ValueError("k_pos_inject requires chunk_byte_off (window-relative per-chunk start byte offsets)")
                sel_idx = cache_idx.clamp(min=0)
                k_rows = k_rows + self.pos_gate * self.pos_proj(
                    _pos_features(sel_idx, chunk_byte_off.gather(1, sel_idx))
                )
            ks.append(k_rows)
            vs.append(self.v_proj_state(sel_state) if self.v_from_state else self.v_proj(sel_mem))
            valid_cache = chunk_mask.gather(1, cache_idx.clamp(min=0)) & (cache_idx >= 0)  # (B, K)
            causal = cache_idx.view(bsz, 1, kk) <= query_pos.view(bsz, n, 1)
            allowed_parts.append(causal & valid_cache.view(bsz, 1, kk))
            if supp is not None and supp_idx is not None:
                # S38 supplementary readout entries (d_pack space -> gist
                # projections); entry for chunk i is visible to query positions
                # with query_pos >= i (chunk-level causality)
                mm = supp_idx.size(1)
                sel_supp = supp.gather(1, supp_idx.clamp(min=0).unsqueeze(-1).expand(-1, -1, supp.size(-1)))
                ks.append(self.gist_k(sel_supp))
                vs.append(self.gist_v(sel_supp))
                valid_s = chunk_mask.gather(1, supp_idx.clamp(min=0)) & (supp_idx >= 0)
                causal_s = supp_idx.view(bsz, 1, mm) <= query_pos.view(bsz, n, 1)
                allowed_parts.append(causal_s & valid_s.view(bsz, 1, mm))
            k = torch.cat(ks, dim=1).view(bsz, -1, nh, hd).transpose(1, 2)
            v = torch.cat(vs, dim=1).view(bsz, -1, nh, hd).transpose(1, 2)
            allowed = torch.cat(allowed_parts, dim=-1).unsqueeze(1)
            o = F.scaled_dot_product_attention(q, k, v, attn_mask=allowed)
        o = o.transpose(1, 2).reshape(bsz, n, nh * hd)
        h = h + self.o_proj(o)
        for block in self.blocks:
            h = h + block(h)
        return self.norm(h)


class SLMBackbone(nn.Module):
    """v3.7 SLM backbone (consensus §1.3, user-ruled 2026-08-17): a standard
    small LM in the traditional decoder-only shape.

    - Block 1 is a causal cross-attention over the PRECOMPUTED store rows
      (Q = each position's hidden state, K/V = the store rows) + FFN; blocks
      2..L are standard causal self-attention + FFN (pre-norm, residual).
    - Seed: the initial hidden state at position i is align_V(V source row_i)
      + chunk_pos[i] -- "each chunk asks with its own V", isomorphic to
      h_i^0 = embedding_i in a traditional LM. The store's V side and the
      seeds share the SAME align_V (one interface).
    - align_K/align_V are PURE dimensional alignments (d_mem or d_pack ->
      d_backbone), NOT content parsers -- content parsing is internalized in
      the summarizer (consensus §1.1).
    - Q is entirely self-produced by the backbone hidden state (q = W_q(h)
      every layer, use-and-discard; "the backbone itself is Q"): in slm mode
      there is no Q-side content channel.
    - Position i sees store rows 0..i only (causal mask with the
      diagonal-keep padding-NaN guard, same pattern as CrossReadBackbone).
    - k_pos_inject (the a+pos arm, consensus §3): pos_gate * pos_proj of the
      sinusoidal (segment order, window-relative start byte) features is added
      to the aligned fine-grained index K rows; zero-init scalar gate, so
      step 0 is exactly the a grid. Legal only for k_row_source="index".
    """

    def __init__(self, c: V36Config) -> None:
        super().__init__()
        d = c.d_backbone
        self.nhead = c.backbone_nhead
        k_src = getattr(c, "k_row_source", "index")
        v_src = getattr(c, "v_row_source", "memory")
        if k_src not in ("index", "state"):
            raise ValueError(
                f"slm k_row_source must be 'index' or 'state', got {k_src!r} "
                "('memory' is illegal for the K channel in slm mode: the memory row is the V standard, consensus §3)"
            )
        if v_src not in ("memory", "state"):
            raise ValueError(f"slm v_row_source must be 'memory' or 'state', got {v_src!r}")
        self.k_from_state = k_src == "state"
        self.v_from_state = v_src == "state"
        k_dim = c.d_pack if self.k_from_state else c.d_mem
        v_dim = c.d_pack if self.v_from_state else c.d_mem
        self.align_k = nn.Linear(k_dim, d, bias=False)
        self.align_v = nn.Linear(v_dim, d, bias=False)
        # block 1: causal cross-attention over the store + FFN
        self.q_proj = nn.Linear(d, d, bias=False)
        self.o_proj = nn.Linear(d, d, bias=False)
        self.ln_ffn1 = nn.LayerNorm(d)
        self.ffn1 = nn.Sequential(nn.Linear(d, c.backbone_ffn), nn.GELU(), nn.Linear(c.backbone_ffn, d))
        # blocks 2..L: standard causal self-attention + FFN (pre-norm)
        self.self_blocks = nn.ModuleList(
            [
                nn.ModuleDict(
                    {
                        "ln_s": nn.LayerNorm(d),
                        "q": nn.Linear(d, d, bias=False),
                        "k": nn.Linear(d, d, bias=False),
                        "v": nn.Linear(d, d, bias=False),
                        "o": nn.Linear(d, d, bias=False),
                        "ln_f": nn.LayerNorm(d),
                        "ffn": nn.Sequential(
                            nn.Linear(d, c.backbone_ffn), nn.GELU(), nn.Linear(c.backbone_ffn, d)
                        ),
                    }
                )
                for _ in range(max(c.backbone_layers - 1, 0))
            ]
        )
        self.norm = nn.LayerNorm(d)
        # a+pos arm: position-injected keys on the fine-grained index rows
        # (zero-init gate -> step 0 bitwise-equals the a grid)
        self.k_pos_inject = getattr(c, "k_pos_inject", False)
        # S39 K-block eval probe: eval-time K-channel ablation (zero keys)
        self.k_block_eval = getattr(c, "k_block_eval", False)
        # S39 K-seed arm: seed the hidden state from the index row (K becomes
        # load-bearing) instead of the V row
        self.seed_source = getattr(c, "seed_source", "v")
        if self.seed_source not in ("v", "k"):
            raise ValueError(f"slm seed_source must be 'v' or 'k', got {self.seed_source!r}")
        if self.k_pos_inject:
            if k_src != "index":
                raise ValueError(
                    "slm k_pos_inject requires k_row_source='index' "
                    "(a+pos = (index+pos, memory), the a-grid K-side single-variable arm, consensus §3)"
                )
            if v_src != "memory":
                raise ValueError(
                    "slm k_pos_inject requires v_row_source='memory' "
                    "(a+pos is the a-grid K-side SINGLE-VARIABLE arm; "
                    "(index+pos, state) would confound attribution, consensus §3)"
                )
            self.pos_proj = nn.Linear(POS_FEAT_DIM, d, bias=False)
            self.pos_gate = nn.Parameter(torch.zeros(()))

    def forward(
        self,
        k_rows: torch.Tensor,
        v_rows: torch.Tensor,
        chunk_mask: torch.Tensor,
        pos: torch.Tensor,
        chunk_byte_off: torch.Tensor | None = None,
    ) -> torch.Tensor:
        """k_rows: (B, C, d_mem|d_pack) K source rows (index or K~);
        v_rows: (B, C, d_mem|d_pack) V source rows (memory or V~);
        pos: (1, C, d_backbone) chunk position embedding. fork 2: a 4-dim
        (B, C, m, d) k_rows/v_rows routes to the multi-view store path."""
        bsz, n = chunk_mask.shape
        kv = k_rows.size(2) if k_rows.dim() == 4 else 1
        vv = v_rows.size(2) if v_rows.dim() == 4 else 1
        if max(kv, vv) > 1:
            return self._forward_views(k_rows, v_rows, chunk_mask, pos, chunk_byte_off, max(kv, vv))
        nh = self.nhead
        hd = pos.size(-1) // nh
        store_v = self.align_v(v_rows)  # (B, C, d) -- shared: store V side AND seeds
        k_flat = self.align_k(k_rows)
        # position seed: default each chunk asks with its own V (consensus
        # §1.3); S39 K-seed arm (user-ruled 2026-08-17) seeds from the INDEX
        # row instead, forcing content to flow through K/V retrieval -- the
        # index channel becomes load-bearing. The seed always uses the plain
        # aligned K rows (pos-injection/k-block below touch attention keys
        # only, never the seed).
        seed = k_flat if self.seed_source == "k" else store_v
        h = seed + pos.to(seed.dtype)
        if self.k_pos_inject:
            # a+pos: sinusoidal key-row features through the zero-init gate
            if chunk_byte_off is None:
                raise ValueError("k_pos_inject requires chunk_byte_off (window-relative per-chunk start byte offsets)")
            seg_idx = torch.arange(n, device=k_rows.device).unsqueeze(0).expand(bsz, n)
            k_flat = k_flat + self.pos_gate * self.pos_proj(_pos_features(seg_idx, chunk_byte_off))
        if self.k_block_eval:
            # S39 K-block probe (user-ruled 2026-08-17): zero the keys so
            # block-1 attention is uniform -- the index channel carries zero
            # information. Absolute: overrides any pos injection above.
            k_flat = torch.zeros_like(k_flat)
        k = k_flat.view(bsz, n, nh, hd).transpose(1, 2)
        v = store_v.view(bsz, n, nh, hd).transpose(1, 2)
        # causal over the store; keep the diagonal even on padded rows (a
        # fully-masked SDPA row yields NaN, and 0*NaN poisons downstream)
        future = torch.triu(torch.ones(n, n, dtype=torch.bool, device=k_rows.device), diagonal=1)
        allowed = (~future).view(1, 1, n, n) & chunk_mask.view(bsz, 1, 1, n)
        allowed = allowed | torch.eye(n, dtype=torch.bool, device=k_rows.device).view(1, 1, n, n)
        # block 1: cross-read; Q self-produced from the hidden state
        q = self.q_proj(h).view(bsz, n, nh, hd).transpose(1, 2)
        o = F.scaled_dot_product_attention(q, k, v, attn_mask=allowed)
        h = h + self.o_proj(o.transpose(1, 2).reshape(bsz, n, nh * hd))
        h = h + self.ffn1(self.ln_ffn1(h))
        # blocks 2..L: standard causal self-attention + FFN
        for blk in self.self_blocks:
            hn = blk["ln_s"](h)
            q = blk["q"](hn).view(bsz, n, nh, hd).transpose(1, 2)
            kk = blk["k"](hn).view(bsz, n, nh, hd).transpose(1, 2)
            vv = blk["v"](hn).view(bsz, n, nh, hd).transpose(1, 2)
            o = F.scaled_dot_product_attention(q, kk, vv, attn_mask=allowed)
            h = h + blk["o"](o.transpose(1, 2).reshape(bsz, n, nh * hd))
            h = h + blk["ffn"](blk["ln_f"](h))
        return self.norm(h)

    def _forward_views(
        self,
        k_rows: torch.Tensor,
        v_rows: torch.Tensor,
        chunk_mask: torch.Tensor,
        pos: torch.Tensor,
        chunk_byte_off: torch.Tensor | None,
        views: int,
    ) -> torch.Tensor:
        """fork 2 multi-view store path (spec §1.1/§1.3): each chunk
        contributes `views` store entries — its m measurement rows from the
        seeded orthogonal frame; a direct/single-view side repeats its row.
        Query positions stay per-chunk; position i sees all views of chunks
        0..i. align_k/align_v/realign are SHARED across views (m 路共享,
        zero new parameters). Seed = per-chunk canonical row (view 0 for K,
        the view mean for V)."""
        bsz, n = chunk_mask.shape
        nh = self.nhead
        hd = pos.size(-1) // nh
        if k_rows.dim() == 3:
            k_rows = k_rows.unsqueeze(2).expand(bsz, n, views, k_rows.size(-1))
        if v_rows.dim() == 3:
            v_rows = v_rows.unsqueeze(2).expand(bsz, n, views, v_rows.size(-1))
        store_v = self.align_v(v_rows.reshape(bsz, n * views, -1))
        k_flat = self.align_k(k_rows.reshape(bsz, n * views, -1))
        # seed from the per-chunk canonical rows (view 0 K / view-mean V)
        seed = self.align_k(k_rows[:, :, 0]) if self.seed_source == "k" else self.align_v(v_rows.mean(dim=2))
        h = seed + pos.to(seed.dtype)
        if self.k_pos_inject:
            if chunk_byte_off is None:
                raise ValueError("k_pos_inject requires chunk_byte_off (window-relative per-chunk start byte offsets)")
            seg_idx = torch.arange(n, device=k_rows.device).repeat_interleave(views).unsqueeze(0).expand(bsz, -1)
            k_flat = k_flat + self.pos_gate * self.pos_proj(
                _pos_features(seg_idx, chunk_byte_off.repeat_interleave(views, dim=1))
            )
        if self.k_block_eval:
            k_flat = torch.zeros_like(k_flat)
        k = k_flat.view(bsz, n * views, nh, hd).transpose(1, 2)
        v = store_v.view(bsz, n * views, nh, hd).transpose(1, 2)
        # store mask: query chunk j sees entries of chunks 0..j (all views);
        # diagonal-keep guard on padded rows (same NaN-poison rule as legacy)
        store_chunk = torch.arange(n, device=k_rows.device).repeat_interleave(views)
        qidx = torch.arange(n, device=k_rows.device)
        causal = store_chunk.view(1, -1) <= qidx.view(-1, 1)  # (n, n*views)
        allowed = causal.view(1, 1, n, n * views) & chunk_mask[:, store_chunk].view(bsz, 1, 1, n * views)
        first_view = (torch.arange(n * views, device=k_rows.device) % views == 0).view(1, -1)
        diag = (store_chunk.view(1, -1) == qidx.view(-1, 1)) & first_view
        allowed = allowed | diag.view(1, 1, n, n * views)
        q = self.q_proj(h).view(bsz, n, nh, hd).transpose(1, 2)
        o = F.scaled_dot_product_attention(q, k, v, attn_mask=allowed)
        h = h + self.o_proj(o.transpose(1, 2).reshape(bsz, n, nh * hd))
        h = h + self.ffn1(self.ln_ffn1(h))
        # blocks 2..L: per-chunk causal self-attention (legacy mask)
        future = torch.triu(torch.ones(n, n, dtype=torch.bool, device=k_rows.device), diagonal=1)
        allowed_self = (~future).view(1, 1, n, n) & chunk_mask.view(bsz, 1, 1, n)
        allowed_self = allowed_self | torch.eye(n, dtype=torch.bool, device=k_rows.device).view(1, 1, n, n)
        for blk in self.self_blocks:
            hn = blk["ln_s"](h)
            q = blk["q"](hn).view(bsz, n, nh, hd).transpose(1, 2)
            kk = blk["k"](hn).view(bsz, n, nh, hd).transpose(1, 2)
            vv = blk["v"](hn).view(bsz, n, nh, hd).transpose(1, 2)
            o = F.scaled_dot_product_attention(q, kk, vv, attn_mask=allowed_self)
            h = h + blk["o"](o.transpose(1, 2).reshape(bsz, n, nh * hd))
            h = h + blk["ffn"](blk["ln_f"](h))
        return self.norm(h)


class DraftBackbone(nn.Module):
    """Three-state drafting backbone (spec SS23, user-ruled 2026-08-08).

    Input state  = ONE k=1 readout vector (its job is gist, not byte fidelity).
    Thinking state = a fresh matrix (B, C, d) seeded from noise + position and
    refined by T DiT rounds; each round sees the readout (and, for
    think_visibility="readout_memory", ALL pre-state memory rows) plus the
    current thinking matrix. Drafting is a global revision: within one
    thinking pass the whole offered store is visible (matches deployment --
    the window is fully encoded before the one-shot output is drafted).
    Causal honesty lives at the INPUT level: the predict rollout is fed the
    penultimate readout with memory truncated at last-1 (train_v36_s1.py),
    so no target-chunk information can enter the draft.
    T is sampled uniformly from [think_steps_min, think_steps_max] per
    training call; at eval a deterministic stability-stop (mean cosine
    between consecutive thinking matrices > think_stop_cos, clamped to the
    same bounds) decides -- the stop mechanism is the backbone's own
    dynamics, no extra supervision.
    Output state = the final thinking matrix, one-shot to the decoder.
    Thinking steps are UNSUPERVISED: only the output matrix eats task loss
    (clean output, dirty thinking -- branching/backtracking allowed).
    """

    def __init__(self, c: V36Config) -> None:
        super().__init__()
        self.c = c
        self.nhead = c.backbone_nhead
        d = c.d_backbone
        self.seed = nn.Parameter(torch.randn(1, 1, d) * 0.02)
        self.time_emb = nn.Embedding(c.think_steps_max + 1, d)
        self.readout_k = nn.Linear(c.d_pack, d, bias=False)
        self.readout_v = nn.Linear(c.d_pack, d, bias=False)
        self.mem_k = nn.Linear(c.d_mem, d, bias=False)
        self.mem_v = nn.Linear(c.d_mem, d, bias=False)
        self.q_proj = nn.Linear(d, d, bias=False)
        self.k_proj = nn.Linear(d, d, bias=False)
        self.v_proj = nn.Linear(d, d, bias=False)
        self.q_mem = nn.Linear(d, d, bias=False)
        self.o_proj = nn.Linear(d, d, bias=False)
        self.o_mem = nn.Linear(d, d, bias=False)
        # s34/s35 levers (docs/research/RESEARCH_SWEEP_20260808_CN.md)
        if c.draft_init == "content_seed":
            self.content_in = nn.Linear(c.d_pack, d, bias=False)
        if c.draft_inject == "concat":
            self.inj_proj = nn.Linear(c.d_pack, d, bias=False)
            self.inj_mix = nn.Linear(2 * d, d, bias=False)
        self.blocks = nn.ModuleList(
            [
                nn.ModuleDict(
                    {
                        "ln_s": nn.LayerNorm(d),
                        "ln_c": nn.LayerNorm(d),
                        "ln_f": nn.LayerNorm(d),
                        "ffn": nn.Sequential(
                            nn.Linear(d, c.backbone_ffn),
                            nn.GELU(),
                            nn.Linear(c.backbone_ffn, d),
                        ),
                        **(
                            {
                                "ln_s2": nn.LayerNorm(d),
                                "ln_c2": nn.LayerNorm(d),
                                "ln_f2": nn.LayerNorm(d),
                            }
                            if c.draft_sandwich
                            else {}
                        ),
                    }
                )
                for _ in range(c.backbone_layers)
            ]
        )
        self.norm = nn.LayerNorm(d)
        self.last_steps = 0  # eval-time bookkeeping for the think-steps metric
        self.last_intermediate = None  # intermediate matrix for the s35 loss

    def _sdpa(self, q, k, v, allowed):
        # allowed: (B, 1 or nh, Nq, Nk) bool. Fully-masked rows would NaN --
        # keep the diagonal so a padded query row stays finite (0*NaN poison).
        o = F.scaled_dot_product_attention(q, k, v, attn_mask=allowed)
        return o

    def think(
        self,
        readout: torch.Tensor,
        memory: torch.Tensor,
        chunk_mask: torch.Tensor,
        pos: torch.Tensor,
        n_steps: int | None = None,
        content: torch.Tensor | None = None,
        round_hook=None,
    ) -> tuple[torch.Tensor, int]:
        """readout: (B, d_pack) k=1 input state. memory: (B, C, d_mem) pre-state
        rows. chunk_mask: (B, C) bool. pos: (1, C, d). content: (B, C, d_pack)
        per-chunk readouts (only used by draft_init="content_seed"). Returns
        the output matrix (B, C, d_backbone) and the number of thinking
        rounds used. round_hook(h, t) is applied after each round (probe
        hook for trajectory stats / perturbation sensitivity)."""
        bsz, n = chunk_mask.shape
        device, dtype = readout.device, readout.dtype
        d = self.c.d_backbone
        self.last_intermediate = None
        # thinking matrix init: learned seed + position + fresh noise.
        # content_seed (SmoothSA/QSA lesson): preheat the cold-start slots with
        # a content projection -- noise+position is the known worst init.
        h = self.seed + pos.to(dtype) + torch.randn(bsz, n, d, device=device, dtype=dtype)
        if self.c.draft_init == "content_seed":
            if content is None:
                raise ValueError("draft_init='content_seed' requires content")
            h = h + self.content_in(content)
        # conditioning store: the readout token is always visible; memory rows
        # (visibility arm B) are visible to all slots (global revision; padded
        # rows excluded). draft_mem_pos adds chunk position to the memory keys
        # -- shelf row numbers (Retrievit lesson).
        rk = self.readout_k(readout).unsqueeze(1)  # (B, 1, d)
        rv = self.readout_v(readout).unsqueeze(1)
        if self.c.think_visibility == "readout_memory":
            mk = self.mem_k(memory)
            if self.c.draft_mem_pos:
                mk = mk + pos.to(dtype)
            ck = torch.cat([rk, mk], dim=1)  # (B, 1+C, d)
            cv = torch.cat([rv, self.mem_v(memory)], dim=1)
            cross_allowed = torch.cat(
                [
                    torch.ones(bsz, n, 1, dtype=torch.bool, device=device),
                    chunk_mask.view(bsz, 1, n).expand(bsz, n, n),
                ],
                dim=-1,
            )
        else:
            ck, cv = rk, rv
            cross_allowed = torch.ones(bsz, n, 1, dtype=torch.bool, device=device)
        self_allowed = chunk_mask.view(bsz, 1, n) & chunk_mask.view(bsz, n, 1)
        self_allowed = self_allowed | torch.eye(n, dtype=torch.bool, device=device).view(1, n, n)
        if n_steps is None:
            if self.training:
                # CPU-side sampling: a GPU randint + .item() here would sync
                # the pipeline twice per step (the E33 sync tax). poisson =
                # Huginn-style heavy-tail depth sampling.
                if self.c.draft_depth_dist == "poisson":
                    lam = max(1, self.c.think_steps_max // 2)
                    n_steps = 1 + int(torch.poisson(torch.tensor(float(lam))))
                    n_steps = min(max(n_steps, self.c.think_steps_min), self.c.think_steps_max)
                else:
                    n_steps = int(
                        torch.randint(self.c.think_steps_min, self.c.think_steps_max + 1, (1,), device="cpu")
                    )
            else:
                n_steps = -1  # stability-stop mode (below)
        max_steps = self.c.think_steps_max
        trunc = self.c.draft_trunc_bptt
        nograd_rounds = max(0, n_steps - trunc) if (self.training and trunc > 0 and n_steps > 0) else 0
        # intermediate round for the s35 supervision: sampled inside the
        # gradient zone so the loss actually reaches the shared weights
        k_mid = -1
        if self.training and self.c.draft_intermediate_weight > 0 and n_steps >= 2:
            k_lo = max(1, nograd_rounds + 1)
            k_mid = int(torch.randint(k_lo, n_steps, (1,), device="cpu"))  # 1-based round
        inj = None
        if self.c.draft_inject == "concat":
            inj = self.inj_proj(readout).unsqueeze(1).expand(bsz, n, d)  # (B, C, d)
        steps_used = 0
        prev = None
        for t in range(max_steps):
            steps_used = t + 1
            if t < nograd_rounds:
                with torch.no_grad():
                    h = self._round(h, inj, ck, cv, self_allowed, cross_allowed, t, dtype)
            else:
                h = self._round(h, inj, ck, cv, self_allowed, cross_allowed, t, dtype)
            if steps_used == k_mid:
                self.last_intermediate = h
            if round_hook is not None:
                h = round_hook(h, t)
            if n_steps >= 0 and steps_used >= n_steps:
                break
            if n_steps < 0 and prev is not None and steps_used >= self.c.think_steps_min:
                with torch.no_grad():
                    a = h.float()[chunk_mask]
                    b = prev.float()[chunk_mask]
                    stab = F.cosine_similarity(a, b, dim=-1).mean()
                if float(stab) > self.c.think_stop_cos:
                    break
            prev = h
        self.last_steps = steps_used
        return self.norm(h), steps_used

    def _round(self, h, inj, ck, cv, self_allowed, cross_allowed, t, dtype):
        """One thinking round: time condition + optional concat re-injection
        (Huginn: the operator must depend on the input EVERY round, and the
        concat form cannot be attentioned away), then the DiT blocks."""
        bsz, n, d = h.shape
        nh, hd = self.nhead, d // self.nhead
        h = h + self.time_emb.weight[min(t, self.c.think_steps_max)].to(dtype)
        if inj is not None:
            h = h + self.inj_mix(torch.cat([h, inj], dim=-1))
        for blk in self.blocks:
            hn = blk["ln_s"](h)
            q = self.q_proj(hn).view(bsz, n, nh, hd).transpose(1, 2)
            k = self.k_proj(hn).view(bsz, n, nh, hd).transpose(1, 2)
            v = self.v_proj(hn).view(bsz, n, nh, hd).transpose(1, 2)
            o = self._sdpa(q, k, v, self_allowed.unsqueeze(1))
            h = h + self.o_proj(o.transpose(1, 2).reshape(bsz, n, d))
            if self.c.draft_sandwich:
                h = blk["ln_s2"](h)
            hn = blk["ln_c"](h)
            qm = self.q_mem(hn).view(bsz, n, nh, hd).transpose(1, 2)
            km = ck.view(bsz, -1, nh, hd).transpose(1, 2)
            vm = cv.view(bsz, -1, nh, hd).transpose(1, 2)
            om = self._sdpa(qm, km, vm, cross_allowed.unsqueeze(1))
            h = h + self.o_mem(om.transpose(1, 2).reshape(bsz, n, d))
            if self.c.draft_sandwich:
                h = blk["ln_c2"](h)
            h = h + blk["ffn"](blk["ln_f"](h))
            if self.c.draft_sandwich:
                h = blk["ln_f2"](h)
        return h

    def forward(
        self,
        readout: torch.Tensor,
        memory: torch.Tensor,
        chunk_mask: torch.Tensor,
        pos: torch.Tensor,
        n_steps: int | None = None,
        content: torch.Tensor | None = None,
    ) -> torch.Tensor:
        return self.think(readout, memory, chunk_mask, pos, n_steps, content)[0]


class PointwiseBackbone(nn.Module):
    """Per-readout backbone (v36.5): each chunk's readout vector is transformed
    independently — cross-chunk sequence modeling belongs to the KDA recurrence,
    not to a second attention stack over the chunk matrix. Completion/prediction
    become strictly causal (no future-chunk leakage), so the training form
    matches streaming generation. The legacy attention backbone remains as
    ``backbone_mode="attn"`` for historical arms. Positional information is
    added downstream (chunk_pos in the caller), so no position embedding here.
    """

    def __init__(self, c: V36Config) -> None:
        super().__init__()
        self.in_proj = nn.Linear(c.d_pack, c.d_backbone) if c.d_pack != c.d_backbone else nn.Identity()
        self.blocks = nn.ModuleList(
            [
                nn.Sequential(
                    nn.LayerNorm(c.d_backbone),
                    nn.Linear(c.d_backbone, c.backbone_ffn),
                    nn.GELU(),
                    nn.Linear(c.backbone_ffn, c.d_backbone),
                )
                for _ in range(c.backbone_layers)
            ]
        )
        self.norm = nn.LayerNorm(c.d_backbone)

    def forward(self, package: torch.Tensor) -> torch.Tensor:
        h = self.in_proj(package)
        for block in self.blocks:
            h = h + block(h)
        return self.norm(h)


class TinyBackbone(nn.Module):
    def __init__(self, c: V36Config) -> None:
        super().__init__()
        self.in_proj = nn.Linear(c.d_pack, c.d_backbone) if c.d_pack != c.d_backbone else nn.Identity()
        self.pos = nn.Embedding(c.max_positions, c.d_backbone)
        layer = nn.TransformerEncoderLayer(
            c.d_backbone,
            c.backbone_nhead,
            c.backbone_ffn,
            dropout=0.0,
            activation="gelu",
            batch_first=True,
            norm_first=True,
        )
        self.encoder = nn.TransformerEncoder(layer, num_layers=c.backbone_layers)
        nn.init.trunc_normal_(self.pos.weight, std=0.02)

    def forward(self, package: torch.Tensor) -> torch.Tensor:
        positions = torch.arange(package.size(1), device=package.device)
        return self.encoder(self.in_proj(package) + self.pos(positions).unsqueeze(0))


class GlobalSpanDecoder(nn.Module):
    def __init__(self, c: V36Config, byte_lookup: PlainByteLookup) -> None:
        super().__init__()
        self.slot = nn.Parameter(torch.empty(c.max_span, c.d_backbone))
        nn.init.trunc_normal_(self.slot, std=0.02)
        self.blocks = nn.ModuleList(
            [DiTStyleBlock(c.d_backbone, c.backbone_nhead, c.backbone_ffn, True, False) for _ in range(c.decoder_layers)]
        )
        self.byte_lookup = byte_lookup
        # k=1 capacity arms (E38): when d_backbone != d_byte the decoder cannot
        # share the byte table directly -- project decoder states back into the
        # byte-table space with a learned map; the table itself stays the fixed
        # public ruler (E31/E34: decoder/table geometry must not be trainable).
        self.out_proj = (
            nn.Linear(c.d_backbone, c.d_byte, bias=False) if c.d_backbone != c.d_byte else nn.Identity()
        )
        # Gradient-checkpoint gate. The frozen-predict path (functional_call with
        # detached params) must NOT checkpoint: the backward recompute would run
        # outside the param substitution and see the live grad-requiring params
        # (CheckpointError metadata mismatch). train_v36_s1 toggles this off
        # around _frozen_decoder_logits.
        self._ckpt_enabled = True
        self.scale = nn.Parameter(torch.tensor(10.0))
        # DSpark Markov head (research sweep 2026-08-08): low-rank bigram
        # transition bias for parallel byte decoding. prev_ids row 258 is the
        # window-start sentinel (no previous byte).
        if c.decoder_markov > 0:
            self.markov_embed = nn.Embedding(259, c.decoder_markov)
            self.markov_out = nn.Linear(c.decoder_markov, 258, bias=False)

    def forward(
        self,
        cond: torch.Tensor,
        token_mask: torch.Tensor,
        prev_ids: torch.Tensor | None = None,
    ) -> torch.Tensor:
        bsz, chunks, dim = cond.shape
        h = self.slot.view(1, 1, *self.slot.shape).expand(bsz, chunks, -1, -1) + cond.unsqueeze(2)
        h = h.reshape(bsz * chunks, self.slot.size(0), dim)
        valid = token_mask.reshape(bsz * chunks, -1)
        noise = h.new_zeros(h.size(0))
        for block in self.blocks:
            # Gradient checkpointing in training: at d_backbone=1536 the decoder
            # blocks dominate activation memory and push the allocator into the
            # thrash zone (observed 15.5GB / ~14s per step); recompute trades
            # ~30% FLOPs for getting back under the red line. Eval and the
            # frozen-predict ruler path skip it (no graph to save).
            if self.training and self._ckpt_enabled and torch.is_grad_enabled():
                h = _grad_checkpoint(block, h, valid, noise, use_reentrant=False)
            else:
                h = block(h, valid, noise)
        h = self.out_proj(h)
        vocab = torch.arange(258, device=h.device)
        table = self.byte_lookup(vocab).to(h.dtype)
        logits = self.scale.clamp(1.0, 100.0) * torch.matmul(
            F.normalize(h, dim=-1), F.normalize(table, dim=-1).transpose(0, 1)
        )
        if prev_ids is not None and hasattr(self, "markov_out"):
            # prev_ids: (B, C, span) long, 258 = window-start sentinel
            bias = self.markov_out(self.markov_embed(prev_ids.reshape(bsz * chunks, -1)))
            logits = logits + bias.to(logits.dtype)
        logits = logits.view(bsz, chunks, self.slot.size(0), -1)
        return logits.masked_fill(~token_mask.unsqueeze(-1), 0.0)


class FLUEDV36(nn.Module):
    def __init__(self, config: V36Config | None = None) -> None:
        super().__init__()
        self.config = config or V36Config()
        c = self.config
        self.byte_lookup = PlainByteLookup(c.d_byte)
        self.encoder_blocks = nn.ModuleList(
            [DiTStyleBlock(c.d_byte, c.nhead, c.ffn_dim, True, True) for _ in range(c.encoder_layers)]
        )
        self.segmentor_blocks = nn.ModuleList(
            [DiTStyleBlock(c.d_byte, c.nhead, c.ffn_dim, True, False) for _ in range(c.segmentor_layers)]
        )
        self.segmentor_head = nn.Sequential(nn.LayerNorm(c.d_byte), nn.Linear(c.d_byte, 1))
        self.chunk_builder = ChunkBuilder(c.max_chunks, c.max_span)
        self.summarizer = ChunkSummarizer(c) if c.summarizer_type == "slot" else DiTChunkSummarizer(c)
        slm = c.backbone_mode == "slm"
        if getattr(c, "recurrence", "kda") not in ("kda", "gdn2"):
            raise ValueError(f"recurrence must be 'kda' or 'gdn2', got {c.recurrence!r}")
        if slm:
            # v3.7 (consensus, user-ruled 2026-08-17): loud rejections for the
            # combinations that are N/A in the new mode -- no silent mismatch.
            if c.summarizer_type != "dit":
                raise ValueError(
                    "backbone_mode='slm' requires summarizer_type='dit' "
                    "(the K-side index head lives on DiTChunkSummarizer, consensus §1.1)"
                )
            if c.k_row_source == "memory":
                raise ValueError(
                    "backbone_mode='slm': k_row_source='memory' is illegal for the K channel "
                    "(consensus §3: K is 'index' or 'state'; the memory row is the V standard)"
                )
            if not c.per_chunk_readout:
                raise ValueError("backbone_mode='slm' requires per_chunk_readout=True")
            if c.backbone_readout != "per_chunk":
                raise ValueError(
                    "backbone_mode='slm' replaces the readout interface; backbone_readout final/paged is N/A"
                )
            if c.prefix_task:
                raise ValueError("prefix_task is N/A for backbone_mode='slm' (v3.7 codec full-coverage law, consensus §2)")
        else:
            self.write_head = WriteHead(c)
            self.state_machine = KDAStateMachine(c)
        if c.backbone_mode == "attn":
            self.backbone = TinyBackbone(c)
        elif c.backbone_mode == "xattn":
            self.backbone = CrossReadBackbone(c)
        elif c.backbone_mode == "paged_xattn":
            self.backbone = CrossReadBackbone(c)
        elif c.backbone_mode == "draft":
            self.backbone = DraftBackbone(c)
        elif slm:
            self.backbone = SLMBackbone(c)
            # interpreter (consensus §1.2): each ENGAGED state channel is an
            # independent WriteHead+KDAStateMachine pair -- the WriteHead as it
            # stands IS the standard KDA write gate, reused unchanged
            # (dimensional alignment only, no extra design). The V channel
            # keeps the legacy attribute names (the standard implementation
            # over the memory rows); the K channel eats the summarizer's index
            # rows (d_mem wide, matching WriteHead's input). The a grid
            # (index, memory) creates NEITHER pair: the interpreter is
            # entirely off the chain there (a ruling, not an omission).
            if c.k_row_source == "state":
                self.write_head_k = WriteHead(c)
                self.state_machine_k = KDAStateMachine(c)
            if c.v_row_source == "state":
                self.write_head = WriteHead(c)
                self.state_machine = KDAStateMachine(c)
            # decoder-side fine-V alignment (direct/predict condition on the
            # memory rows); coarse-V grids use decoder_in instead, so this is
            # created only when engaged (conditional-creation discipline)
            if c.v_row_source == "memory":
                self.decoder_in_mem = nn.Linear(c.d_mem, c.d_backbone)
        else:
            self.backbone = PointwiseBackbone(c)
        self.bridge = SoftBoundaryBridge(
            c.max_chunks, c.tau_cut, c.boundary_temperature, c.boundary_bridge_gradient_scale
        )
        if not slm or c.v_row_source == "state":
            # slm fine-V grids condition the decoder on decoder_in_mem instead;
            # the d_pack decoder_in exists only where a coarse V readout does
            self.decoder_in = nn.Linear(c.d_pack, c.d_backbone) if c.d_pack != c.d_backbone else nn.Identity()
        self.decoder = GlobalSpanDecoder(c, self.byte_lookup)
        self.chunk_pos = nn.Embedding(c.max_chunks, c.d_backbone)
        nn.init.trunc_normal_(self.chunk_pos.weight, std=0.02)

    def _front_end_frozen(self) -> bool:
        mods = (self.byte_lookup, *self.encoder_blocks, *self.segmentor_blocks, self.segmentor_head)
        return all(not p.requires_grad for m in mods for p in m.parameters())

    def _encode(self, token_ids: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        valid = token_ids.ne(PAD_ID)
        # When the whole front end (byte lookup + encoder + segmentor) is frozen,
        # keep it out of the autograd graph: downstream modules only need the
        # values, and dropping the 12-layer attention graph saves gigabytes.
        ctx = torch.no_grad() if self._front_end_frozen() else torch.enable_grad()
        with ctx:
            x = self.byte_lookup(token_ids)
            noise = x.new_zeros(token_ids.size(0))
            for block in self.encoder_blocks:
                x = block(x, valid, noise)
            byte_states = x
            for block in self.segmentor_blocks:
                x = block(x, valid, noise)
            logits = self.segmentor_head(x).squeeze(-1)
            confidence = _plastic_signed_confidence(logits)
        return byte_states, confidence, valid, logits

    def encode_boundary_logits(self, token_ids: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        _, _, valid, logits = self._encode(token_ids)
        return logits, valid

    def _cuts(self, token_ids: torch.Tensor, confidence: torch.Tensor, valid: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        utf8_cont = token_ids.ge(129) & token_ids.le(192) & valid
        if self.config.boundary_mode == "uniform":
            bsz, seq = valid.shape
            cuts = torch.zeros_like(valid)
            first = valid.float().argmax(dim=1)
            cuts[torch.arange(bsz, device=valid.device), first] = True
            position = valid.to(torch.long).cumsum(dim=1)
            cuts = cuts | (valid & position.gt(1) & ((position - 1) % self.config.bytes_per_chunk == 0))
            return cuts & ~utf8_cont, utf8_cont, cuts.new_zeros(1, dtype=torch.float32)
        requested = confidence.gt(self.config.tau_cut) & valid & ~utf8_cont
        first = valid.float().argmax(dim=1)
        requested[torch.arange(valid.size(0), device=valid.device), first] |= valid.any(dim=1)
        executable, overflow = FLUEDV34Probe._capacity_safe_cuts(
            requested, valid, self.config.max_chunks, self.config.max_span
        )
        return executable, utf8_cont, overflow

    def _slm_store_rows(self, chunks: ChunkBatch, with_views: bool = False):
        """v3.7 encoder after the segmentor (consensus §1): the summarizer
        directly produces (memory = the V rows, index = the K rows); each
        channel then either passes through DIRECTLY (fine granularity) or via
        its own KDA-standard interpreter (coarse granularity). Returns
        (k_rows, v_rows, state_norm, memory, index) -- k_rows/v_rows are the
        backbone store source rows; state_norm averages the engaged channels'
        norms, with a 0 placeholder when no state machine exists (the a grid,
        per the ruling).

        fork 2: with_views=True returns TWO extra elements (k_store, v_store):
        the multi-view store rows (B, C, m, d_pack) for each ENGAGED state
        channel, None for direct channels and when readout_views == 1. The
        classic 5-tuple elements are bit-identical either way (direct/predict
        keep the single trained-readout row, fork 2 §1.3)."""
        memory, index = self.summarizer.forward_with_index(chunks.span_embeddings, chunks.token_mask)
        views = getattr(self.config, "readout_views", 1)
        k_store = v_store = None
        norms = []
        if self.config.k_row_source == "state":
            gates_k = self.write_head_k(index)
            package_k, sn_k = self.state_machine_k(gates_k, chunks.chunk_mask)
            k_rows = package_k.mean(dim=2)  # K~ per chunk (B, C, d_pack)
            if with_views and views > 1:
                k_store = self.state_machine_k.forward_views(gates_k, chunks.chunk_mask)
            norms.append(sn_k)
        else:
            k_rows = index
        if self.config.v_row_source == "state":
            gates_v = self.write_head(memory)
            package_v, sn_v = self.state_machine(gates_v, chunks.chunk_mask)
            v_rows = package_v.mean(dim=2)  # V~ per chunk (B, C, d_pack)
            if with_views and views > 1:
                v_store = self.state_machine.forward_views(gates_v, chunks.chunk_mask)
            norms.append(sn_v)
        else:
            v_rows = memory
        if norms:
            state_norm = torch.stack([n.float() for n in norms]).mean()
        else:
            state_norm = memory.new_zeros((), dtype=torch.float32)
        if with_views:
            return k_rows, v_rows, state_norm, memory, index, k_store, v_store
        return k_rows, v_rows, state_norm, memory, index

    def _forward_slm(self, chunks: ChunkBatch, confidence: torch.Tensor, valid: torch.Tensor, hard_cut: torch.Tensor, cut_overflow: torch.Tensor) -> V36Output:
        """v3.7 slm forward (consensus §1-2): the SLM backbone reads the
        summarizer-owned store; the decoder conditions on the SAME V source
        rows as the backbone store (direct), and completion reads the
        backbone's output matrix -- three tasks, one V (§1.4)."""
        k_rows, v_rows, state_norm, memory, _index, k_store, v_store = self._slm_store_rows(chunks, with_views=True)
        n_chunks = chunks.chunk_mask.size(1)
        pos = self.chunk_pos.weight.unsqueeze(0)[:, :n_chunks]
        chunk_byte_off = (
            chunk_byte_offsets(chunks.token_mask) if getattr(self.config, "k_pos_inject", False) else None
        )
        # fork 2: the store carries the multi-view rows when readout_views > 1
        backbone_out = self.backbone(
            k_store if k_store is not None else k_rows,
            v_store if v_store is not None else v_rows,
            chunks.chunk_mask, pos, chunk_byte_off=chunk_byte_off,
        )
        cond_backbone = backbone_out + pos
        dec_in = self.decoder_in if self.config.v_row_source == "state" else self.decoder_in_mem
        cond_direct = dec_in(v_rows) + pos
        logits_direct = self.decoder(cond_direct, chunks.token_mask)
        logits_backbone = self.decoder(cond_backbone, chunks.token_mask)
        aux = {
            "truncated_tokens": chunks.pack_info["truncated_tokens"].float(),
            "cut_capacity_overflow": cut_overflow.float().sum(),
            "chunks_per_sample": chunks.chunk_mask.float().sum(dim=1),
            "boundary_confidence_mean": confidence[valid].mean() if valid.any() else confidence.mean(),
            "hard_cut_fraction": hard_cut.float()[valid].mean() if valid.any() else hard_cut.float().mean(),
            "state_norm": state_norm,
        }
        return V36Output(
            logits_direct=logits_direct,
            logits_backbone=logits_backbone,
            package=None,
            backbone_out=backbone_out,
            chunks=chunks,
            boundary_confidence=confidence,
            memory=memory,
            state_norm=state_norm,
            aux=aux,
            prefix=None,
        )

    def forward(self, token_ids: torch.Tensor) -> V36Output:
        byte_states, confidence, valid, _logits = self._encode(token_ids)
        hard_cut, utf8_cont, cut_overflow = self._cuts(token_ids, confidence, valid)
        chunks = self.chunk_builder(byte_states, valid, hard_cut, confidence)
        chunks = self.bridge(chunks, byte_states, confidence, valid, utf8_cont)
        if self.config.backbone_mode == "slm":
            # v3.7 slm mode: dedicated path (summarizer-owned K/V + SLM
            # backbone + decoder on the same V); the legacy content channel
            # below is bypassed entirely.
            return self._forward_slm(chunks, confidence, valid, hard_cut, cut_overflow)
        memory = self.summarizer(chunks.span_embeddings, chunks.token_mask)
        gates = self.write_head(memory)
        package, state_norm = self.state_machine(gates, chunks.chunk_mask)
        if self.config.per_chunk_readout:
            # package: (B, C, q, d_pack) — one conditioning vector per chunk.
            content = package.mean(dim=2)
            n_chunks = chunks.chunk_mask.size(1)
            pos = self.chunk_pos.weight.unsqueeze(0)[:, :n_chunks]
            cond_direct = self.decoder_in(content) + pos
            if self.config.backbone_mode == "paged_xattn":
                raise ValueError(
                    "paged_xattn (S37) requires per-chunk residuals; use the S1 trainer path"
                )
            if self.config.backbone_mode == "xattn":
                # causal cross-read: queries = per-chunk content, K/V = memory,
                # position i sees memory[0..i] only. S36: optional gist token +
                # residual-gated cache (frac<1 needs targets -> S1 trainer only)
                cache_idx, gist = None, None
                if self.config.xcache_gist or self.config.xcache_frac < 1.0:
                    last = chunks.chunk_mask.long().sum(dim=1).clamp(min=1) - 1
                    ar = torch.arange(content.size(0), device=content.device)
                    gist = content[ar, last] if self.config.xcache_gist else None
                    if self.config.xcache_frac < 1.0:
                        raise ValueError(
                            "xcache_frac<1 requires per-chunk residuals; use the S1 trainer path"
                        )
                    cache_idx = _xcache_select(chunks.chunk_mask.float(), chunks.chunk_mask, 1.0)
                # S39 a+pos: window-relative per-chunk start byte offsets
                # (None = feature off)
                chunk_byte_off = (
                    chunk_byte_offsets(chunks.token_mask)
                    if getattr(self.config, "k_pos_inject", False)
                    else None
                )
                backbone_out = self.backbone(
                    content, memory, chunks.chunk_mask, pos, cache_idx, gist, chunk_byte_off=chunk_byte_off
                )
                cond_backbone = backbone_out + pos
            elif self.config.backbone_mode == "draft":
                # three-state drafting (spec SS23): input = the k=1 final
                # readout; the DiT backbone refines a fresh thinking matrix
                # over T rounds; the output matrix conditions each chunk row.
                last = chunks.chunk_mask.long().sum(dim=1).clamp(min=1) - 1
                ar = torch.arange(content.size(0), device=content.device)
                backbone_out = self.backbone(
                    content[ar, last], memory, chunks.chunk_mask, pos, content=content
                )
                cond_backbone = backbone_out + pos
            elif self.config.backbone_readout == "final":
                if self.config.prefix_task:
                    raise ValueError("prefix_task requires backbone_readout='per_chunk'")
                last = chunks.chunk_mask.long().sum(dim=1).clamp(min=1) - 1
                ar = torch.arange(content.size(0), device=content.device)
                backbone_out = self.backbone(content[ar, last].unsqueeze(1))
                cond_backbone = backbone_out + pos  # (B,1,d) broadcasts over chunks
            elif self.config.backbone_readout == "paged":
                if self.config.prefix_task:
                    raise ValueError("prefix_task requires backbone_readout='per_chunk'")
                boundary, serve = paged_boundaries(chunks.chunk_mask, self.config.paged_reads)
                reads = content.gather(1, boundary.unsqueeze(-1).expand(-1, -1, content.size(-1)))
                paged_out = self.backbone(reads)  # (B, n, d_bb) — pointwise per read
                backbone_out = paged_out
                cond_backbone = paged_out.gather(
                    1, serve.unsqueeze(-1).expand(-1, -1, paged_out.size(-1))
                ) + pos
            else:
                backbone_out = self.backbone(content)
                cond_backbone = backbone_out + pos
            prefix = None
            if self.config.prefix_task:
                # Streaming prefix task: at position i, condition on the readout
                # of S_i and restore ALL bytes of chunks 0..i. Positions are
                # sampled among REAL chunks only (padding rows would just burn
                # memory and trigger allocator thrash).
                real_max = int(chunks.chunk_mask.float().sum(dim=1).max().item())
                real_max = max(real_max, 1)
                if self.training:
                    k = min(self.config.prefix_positions - 1, max(real_max - 1, 0))
                    interior = (
                        torch.randperm(real_max - 1, device=token_ids.device)[:k].add(1).tolist()
                        if k > 0
                        else []
                    )
                    positions = sorted(set(interior + [real_max - 1]))
                else:
                    stride = max(1, real_max // 8)
                    positions = sorted(set(list(range(0, real_max, stride)) + [real_max - 1]))
                prefix = []
                for i in positions:
                    mask_i = chunks.token_mask[:, : i + 1]
                    cond_d_i = self.decoder_in(content[:, i]).unsqueeze(1) + pos[:, : i + 1]
                    cond_b_i = backbone_out[:, i].unsqueeze(1) + pos[:, : i + 1]
                    prefix.append((i, self.decoder(cond_d_i, mask_i), self.decoder(cond_b_i, mask_i)))
        else:
            backbone_out = self.backbone(package)
            n_chunks = chunks.chunk_mask.size(1)
            pos = self.chunk_pos.weight.unsqueeze(0)[:, :n_chunks]
            cond_direct = self.decoder_in(package.mean(dim=1)).unsqueeze(1) + pos
            cond_backbone = backbone_out.mean(dim=1).unsqueeze(1) + pos
        logits_ctx = (
            torch.no_grad()
            if self.config.prefix_task and self.training and self.config.per_chunk_readout
            else torch.enable_grad()
        )
        with logits_ctx:
            # In prefix training these full-path logits are metrics-only, so
            # they must not build an autograd graph (two of the biggest tensors
            # per step).
            logits_direct = self.decoder(cond_direct, chunks.token_mask)
            logits_backbone = self.decoder(cond_backbone, chunks.token_mask)
        aux = {
            "truncated_tokens": chunks.pack_info["truncated_tokens"].float(),
            "cut_capacity_overflow": cut_overflow.float().sum(),
            "chunks_per_sample": chunks.chunk_mask.float().sum(dim=1),
            "boundary_confidence_mean": confidence[valid].mean() if valid.any() else confidence.mean(),
            "hard_cut_fraction": hard_cut.float()[valid].mean() if valid.any() else hard_cut.float().mean(),
            "state_norm": state_norm,
        }
        return V36Output(
            logits_direct=logits_direct,
            logits_backbone=logits_backbone,
            package=package,
            backbone_out=backbone_out,
            chunks=chunks,
            boundary_confidence=confidence,
            memory=memory,
            state_norm=state_norm,
            aux=aux,
            prefix=prefix if self.config.per_chunk_readout else None,
        )
