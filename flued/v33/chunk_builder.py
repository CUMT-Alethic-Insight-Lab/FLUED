from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import nn


@dataclass
class ChunkBatch:
    span_embeddings: torch.Tensor
    confidence_values: torch.Tensor
    chunk_ids: torch.Tensor
    offsets: torch.Tensor
    lengths: torch.Tensor
    chunk_mask: torch.Tensor
    token_mask: torch.Tensor
    transition_markers: torch.Tensor
    force_continue_markers: torch.Tensor
    pack_info: dict


class ChunkBuilder(nn.Module):
    """Pack byte features into executable chunks."""

    def __init__(self, max_chunks: int = 128, max_span: int = 16) -> None:
        super().__init__()
        self.max_chunks = int(max_chunks)
        self.max_span = int(max_span)

    def forward(
        self,
        byte_features: torch.Tensor,
        valid: torch.Tensor,
        hard_cut: torch.Tensor,
        confidence: torch.Tensor | None = None,
        soft_transition: torch.Tensor | None = None,
        force_continue: torch.Tensor | None = None,
    ) -> ChunkBatch:
        bsz, seq_len, dim = byte_features.shape
        device = byte_features.device
        max_chunks, max_span = self.max_chunks, self.max_span
        grid_numel = max_chunks * max_span
        real_numel = bsz * grid_numel

        soft_transition = soft_transition if soft_transition is not None else torch.zeros_like(valid)
        force_continue = force_continue if force_continue is not None else torch.zeros_like(valid)
        confidence = confidence if confidence is not None else byte_features.new_zeros(valid.shape)

        rank = valid.to(torch.long).cumsum(dim=1) - 1
        cuts = hard_cut.bool() & valid
        first = valid.float().argmax(dim=1)
        cuts = cuts.clone()
        cuts[torch.arange(bsz, device=device), first] |= valid.any(dim=1)

        hard_start = torch.cummax(torch.where(cuts, rank, torch.zeros_like(rank)), dim=1).values
        slot_from_hard = rank - hard_start
        span_cut = valid & slot_from_hard.ge(max_span) & ((slot_from_hard % max_span) == 0)
        cuts = cuts | span_cut

        final_start = torch.cummax(torch.where(cuts, rank, torch.zeros_like(rank)), dim=1).values
        slots = rank - final_start
        chunks_for_tokens = torch.cumsum(cuts.to(torch.long), dim=1) - 1
        within = valid & chunks_for_tokens.ge(0) & chunks_for_tokens.lt(max_chunks) & slots.ge(0) & slots.lt(max_span)
        truncated_tokens = (valid & ~within).sum(dim=1)

        # C1 零同步散布 (2026-09-11 效率施工, 提案 §C1): 以静态形状 flat 索引
        # 替换 within.nonzero 的数据依赖形状 —— nonzero 输出形状依赖内容, 每次
        # 都强制全流水线排空 (每步一次硬同步)。前提: 每个 (chunk, slot) 至多
        # 一个源字节 (rank 严格递增 ⇒ 同 chunk 内 slot 互异), 故真实槽无写冲
        # 突、写入确定; 越界/无效位经 torch.where 统一改指各 batch 的 dump 行
        # (每缓冲尾部追加 bsz 行), 重复写只落在 dump 区 —— dump 区被 narrow
        # 截去、从不进入返回张量, 无需清零、值不外泄。
        grid_b = torch.arange(bsz, device=device).unsqueeze(1)
        dst = torch.where(
            within,
            grid_b * grid_numel + chunks_for_tokens * max_span + slots,
            grid_b + real_numel,
        ).reshape(-1)

        span_flat = byte_features.new_zeros((real_numel + bsz, dim))
        span_flat.index_copy_(0, dst, byte_features.reshape(-1, dim))
        span_embeddings = span_flat.narrow(0, 0, real_numel).view(bsz, max_chunks, max_span, dim)

        conf_flat = byte_features.new_zeros((real_numel + bsz,))
        conf_flat.scatter_(0, dst, confidence.to(span_flat.dtype).reshape(-1))
        confidence_values = conf_flat.narrow(0, 0, real_numel).view(bsz, max_chunks, max_span)

        tok_flat = torch.zeros(real_numel + bsz, dtype=torch.bool, device=device)
        tok_flat.scatter_(0, dst, within.reshape(-1))
        token_mask = tok_flat.narrow(0, 0, real_numel).view(bsz, max_chunks, max_span)

        trans_flat = torch.zeros(real_numel + bsz, dtype=torch.bool, device=device)
        trans_flat.scatter_(0, dst, soft_transition.to(torch.bool).reshape(-1))
        transition_markers = trans_flat.narrow(0, 0, real_numel).view(bsz, max_chunks, max_span)

        force_flat = torch.zeros(real_numel + bsz, dtype=torch.bool, device=device)
        force_flat.scatter_(0, dst, force_continue.to(torch.bool).reshape(-1))
        force_markers = force_flat.narrow(0, 0, real_numel).view(bsz, max_chunks, max_span)

        chunk_ids = chunks_for_tokens.masked_fill(~within, -1)
        offsets = slots.masked_fill(~within, 0)

        grid_dst = torch.where(
            within, grid_b * max_chunks + chunks_for_tokens, grid_b + bsz * max_chunks
        ).reshape(-1)
        cm_flat = torch.zeros(bsz * max_chunks + bsz, dtype=torch.bool, device=device)
        cm_flat.scatter_(0, grid_dst, within.reshape(-1))
        chunk_mask = cm_flat.narrow(0, 0, bsz * max_chunks).view(bsz, max_chunks)

        len_flat = torch.zeros(bsz * max_chunks + bsz, dtype=torch.long, device=device)
        len_flat.scatter_reduce_(
            0,
            grid_dst,
            torch.where(within, slots + 1, torch.zeros_like(slots)).reshape(-1),
            reduce="amax",
            include_self=True,
        )
        lengths = len_flat.narrow(0, 0, bsz * max_chunks).view(bsz, max_chunks)

        return ChunkBatch(
            span_embeddings=span_embeddings,
            confidence_values=confidence_values,
            chunk_ids=chunk_ids,
            offsets=offsets,
            lengths=lengths,
            chunk_mask=chunk_mask,
            token_mask=token_mask,
            transition_markers=transition_markers,
            force_continue_markers=force_markers,
            pack_info={"max_chunks": self.max_chunks, "max_span": self.max_span, "truncated_tokens": truncated_tokens},
        )
