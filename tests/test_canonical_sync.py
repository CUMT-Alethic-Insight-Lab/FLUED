"""Guard against configuration drift between three sources of truth.

The training script's argparse defaults, ``configs/canonical_v35.json`` and
``docs/CURRENT_STATE.md`` must agree on the curated key set below. If a future
experiment changes the recommended defaults, all three must be updated in the
same commit; otherwise this test fails.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CANONICAL = REPO_ROOT / "configs" / "canonical_v35.json"
CURRENT_STATE = REPO_ROOT / "docs" / "CURRENT_STATE.md"

CURATED_KEYS = (
    "readout_vectors",
    "use_structured_lookup",
    "use_memory",
    "memory_use_position",
    "memory_position_mode",
    "boundary_mode",
    "boundary_coding_rate_mode",
    "boundary_curriculum_mode",
    "use_prompt_alibi",
    "prompt_position_scale",
    "max_chunks",
    "boundary_bridge_gradient_scale",
    "completion_mask_granularity",
    "decoder_mode",
    "use_emit_controller",
    "emit_forward_mode",
    "emit_threshold",
    "bytes_per_chunk_budget",
    "mask_prob",
    "eval_mask_seed",
)

CURRENT_STATE_MARKERS = (
    ("plain", "byte lookup"),
    ("独立 decoder", "decoder"),
    ("uniform", "boundary"),
    ("关闭", "emit / memory"),
    ("RoPE", "位置"),
)


def _cli_defaults() -> dict:
    from tools.train.v3_4 import train_v34_pos_ar_probe

    argv = sys.argv
    try:
        sys.argv = ["train_v34_pos_ar_probe.py"]
        args = train_v34_pos_ar_probe.parse_args()
    finally:
        sys.argv = argv
    return vars(args)


def test_argparse_defaults_match_canonical() -> None:
    canonical = json.loads(CANONICAL.read_text(encoding="utf-8"))
    defaults = _cli_defaults()
    mismatches = {
        key: (defaults.get(key), canonical.get(key))
        for key in CURATED_KEYS
        if defaults.get(key) != canonical.get(key)
    }
    assert not mismatches, f"CLI defaults drifted from canonical_v35.json: {mismatches}"


def test_current_state_mentions_canonical_version_and_key_defaults() -> None:
    canonical = json.loads(CANONICAL.read_text(encoding="utf-8"))
    text = CURRENT_STATE.read_text(encoding="utf-8")
    assert canonical["canonical_version"] in text, (
        "docs/CURRENT_STATE.md does not reference the canonical_version of configs/canonical_v35.json"
    )
    for marker, label in CURRENT_STATE_MARKERS:
        assert marker in text, f"docs/CURRENT_STATE.md missing {label} marker {marker!r}"


def test_canonical_config_has_required_metadata() -> None:
    canonical = json.loads(CANONICAL.read_text(encoding="utf-8"))
    for key in ("canonical_version", "evidence_base", "supersedes", "usage_note"):
        assert canonical.get(key), f"canonical_v35.json missing metadata field {key}"


# --- v3.6 line: canonical_v36.json must agree with train_v36 CLI defaults,
# --- V36Config dataclass defaults, and docs/CURRENT_STATE.md.

CANONICAL_V36 = REPO_ROOT / "configs" / "canonical_v36.json"

V36_CURATED_KEYS = (
    "d_byte",
    "encoder_layers",
    "segmentor_layers",
    "nhead",
    "ffn_dim",
    "d_mem",
    "summarizer_slots",
    "summarizer_hidden",
    "kda_heads",
    "kda_head_k",
    "kda_head_v",
    "write_hidden",
    "kda_tau_max",
    "readout_queries",
    "d_pack",
    "d_backbone",
    "backbone_layers",
    "backbone_nhead",
    "backbone_ffn",
    "decoder_hidden",
    "decoder_layers",
    "max_chunks",
    "max_span",
    "bytes_per_chunk",
    "tau_cut",
    "tau_trans",
    "boundary_mode",
    "boundary_temperature",
    "boundary_bridge_gradient_scale",
    "max_positions",
    "mask_prob",
    "mask_span_min",
    "mask_span_max",
    "task1_loss_weight",
    "task2_loss_weight",
    "lr",
    "seed",
    "eval_mask_seed",
    "seq_len",
    "stride",
    "batch_size",
    "max_steps",
    "xcache_frac",
    "xcache_gist",
    "xcache_supp",
)


def test_v36_argparse_defaults_match_canonical() -> None:
    canonical = json.loads(CANONICAL_V36.read_text(encoding="utf-8"))
    from tools.train.v3_6.train_v36 import build_parser

    defaults = vars(build_parser().parse_args([]))
    mismatches = {
        key: (defaults.get(key), canonical.get(key))
        for key in V36_CURATED_KEYS
        if defaults.get(key) != canonical.get(key)
    }
    assert not mismatches, f"train_v36 CLI defaults drifted from canonical_v36.json: {mismatches}"


def test_v36_config_dataclass_defaults_match_canonical() -> None:
    import dataclasses

    from flued.v36 import V36Config

    canonical = json.loads(CANONICAL_V36.read_text(encoding="utf-8"))
    defaults = dataclasses.asdict(V36Config())
    mismatches = {
        key: (defaults.get(key), canonical.get(key))
        for key in V36_CURATED_KEYS
        if key in defaults and defaults.get(key) != canonical.get(key)
    }
    assert not mismatches, f"V36Config defaults drifted from canonical_v36.json: {mismatches}"


def test_current_state_mentions_v36_canonical_version() -> None:
    canonical = json.loads(CANONICAL_V36.read_text(encoding="utf-8"))
    text = CURRENT_STATE.read_text(encoding="utf-8")
    assert canonical["canonical_version"] in text, (
        "docs/CURRENT_STATE.md does not reference the canonical_version of configs/canonical_v36.json"
    )


# --- v3.6 S1 layer: train_v36_s1 adds its recipe flags in _add_s1_args on top
# --- of build_parser; these defaults are behavior-critical (the v36.8 recipe
# --- fix lives here) and must drift-guard against canonical_v36.json too.

V36_S1_CURATED_KEYS = (
    "cumulative_mask_retention",
    "mask_mode",
    "mask_char_frac",
    "mask_char_span_max",
    "predict_mode",
    "predict_latent_weight",
    "predict_weight",
    "bpe_tokenizer_path",
    "k_row_source",
    "v_row_source",
    "k_pos_inject",
)


def test_v36_s1_layer_defaults_match_canonical() -> None:
    canonical = json.loads(CANONICAL_V36.read_text(encoding="utf-8"))
    from tools.train.v3_6.train_v36 import build_parser
    from tools.train.v3_6.train_v36_s1 import _add_s1_args

    parser = build_parser()
    _add_s1_args(parser)
    defaults = vars(parser.parse_args([]))
    mismatches = {
        key: (defaults.get(key), canonical.get(key))
        for key in V36_S1_CURATED_KEYS
        if defaults.get(key) != canonical.get(key)
    }
    assert not mismatches, (
        f"train_v36_s1 layer defaults drifted from canonical_v36.json: {mismatches}"
    )


# --- v3.6 坑 8 对偶 pinned 键（2026-09-09 可比性总审计行动 5，用户裁定）：
# --- canonical_v36 早于 E100 qpool 界/v37.2 K-seed 界，summarizer_pool/seed_source
# --- 必须显式钉死历史口径 mean/v。这两键刻意不等于现行 parser 默认（qpool/k），
# --- 故不进 equality 清单（V36_CURATED_KEYS），由 pinned 测试守「显式在册且值未漂移」。

V36_PINNED_KEYS = {
    "summarizer_pool": "mean",
    "seed_source": "v",
}


def test_v36_pinned_keys_explicit_and_undrifted() -> None:
    canonical = json.loads(CANONICAL_V36.read_text(encoding="utf-8"))
    for key, want in V36_PINNED_KEYS.items():
        assert key in canonical, (
            f"canonical_v36.json missing pinned key {key!r} (坑 8 silent-inheritance hole)"
        )
        assert canonical[key] == want, (
            f"canonical_v36.json pinned key {key!r} drifted: {canonical[key]!r} != {want!r}"
        )


# --- v3.7 line: canonical_v37.json must parse through the S1 trainer's
# --- --config mechanism and resolve to the slm a-grid anchor (the v37 mode is
# --- config-gated; v35/v36 guards above are untouched).

CANONICAL_V37 = REPO_ROOT / "configs" / "canonical_v37.json"


def test_v37_canonical_parses_to_slm_a_grid() -> None:
    canonical = json.loads(CANONICAL_V37.read_text(encoding="utf-8"))
    from tools.train.v3_6.train_v36 import build_parser
    from tools.train.v3_6.train_v36_s1 import _add_s1_args

    parser = build_parser()
    _add_s1_args(parser)
    parser.set_defaults(**canonical)
    args = parser.parse_args([])
    assert args.backbone_mode == "slm"
    assert args.k_row_source == "index"
    assert args.v_row_source == "memory"
    assert args.seed_source == "k"  # v37.2: K-seed is the default (E66, user-ruled 2026-08-17)
    assert args.summarizer_pool == "qpool"  # v37.3: qpool is the default (E100, user-ruled 2026-08-23)
    assert canonical.get("canonical_version") == "v37.3-20260823"
    # 坑 8 pinned 对称面（行动 5）：v37 侧两键也必须显式在册，不靠 parser 默认兜底
    assert canonical.get("summarizer_pool") == "qpool"
    assert canonical.get("seed_source") == "k"
