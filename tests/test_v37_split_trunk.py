"""E79 split-trunk tests (flued/v36/model.py WriteHead).

Spec pinned 2026-08-18: default off = shared trunk, bit-identical; on = two
independent trunks (trunk_k -> to_k; trunk_v -> to_v/to_beta/to_b/to_w), so
to_k-side dynamics (to_k_center) cannot deform value content (E79/M3: the
shared trunk let the b-grid surgery cost the K-channel values half their byte
content).
"""

from __future__ import annotations

import pytest
import torch
import torch.nn.functional as F

from flued.v36 import FLUEDV36, V36Config
from flued.v36.model import WriteHead
from tests.test_v37_oracle_probe import _tiny_c_config


def _head(center: bool, split: bool, seed: int = 0, d_mem=96, hidden=128, heads=2, hk=16) -> WriteHead:
    torch.manual_seed(seed)
    c = V36Config(
        d_mem=d_mem, write_hidden=hidden, kda_heads=heads, kda_head_k=hk, kda_head_v=32,
        backbone_mode="slm", summarizer_type="dit", to_k_center=center, split_trunk=split,
    )
    return WriteHead(c)


def _key_loss(wh, rows, tgt):
    """Key-side decorrelation pressure: push keys toward random targets."""
    g = wh(rows)
    return (F.normalize(g["k"][0], dim=-1) - tgt).square().mean()


# 1. default off: bit-identical, no new modules --------------------------------


def test_default_off_bit_identical():
    a = _head(False, False, seed=7).eval()
    b = _head(False, False, seed=7).eval()
    rows = torch.randn(1, 12, 96)
    assert a(rows)["k"].eq(b(rows)["k"]).all()
    assert not hasattr(a, "trunk_k") and not hasattr(a, "trunk_v")
    assert V36Config().split_trunk is False


# 2. isolation: key-side gradients never touch the value trunk ------------------


def test_split_isolates_value_path_from_key_loss():
    shared = _head(False, False, seed=11)
    split = _head(False, True, seed=11)
    split.trunk_k.load_state_dict(shared.trunk.state_dict())
    split.trunk_v.load_state_dict(shared.trunk.state_dict())
    rows = torch.randn(1, 16, 96)
    tgt = F.normalize(torch.randn(16, 2, 16), dim=-1)

    loss = _key_loss(split, rows, tgt)
    loss.backward()
    for n, p in split.named_parameters():
        if n.startswith(("trunk_v", "to_v")):
            assert p.grad is None or p.grad.abs().sum() == 0, f"value path touched: {n}"
    assert split.trunk_k[1].weight.grad.abs().sum() > 0
    assert split.to_k.weight.grad.abs().sum() > 0

    shared_loss = _key_loss(shared, rows, tgt)
    shared_loss.backward()
    assert shared.trunk[1].weight.grad.abs().sum() > 0  # coupling documented: shared trunk moves


# 3. few-step training: value content drift only in the shared variant ---------


def test_value_content_drift_only_when_shared():
    shared = _head(True, False, seed=13)  # to_k_center on, shared trunk (the E79 injury form)
    split = _head(True, True, seed=13)
    split.trunk_k.load_state_dict(shared.trunk.state_dict())
    split.trunk_v.load_state_dict(shared.trunk.state_dict())
    rows = torch.randn(1, 16, 96)
    tgt = F.normalize(torch.randn(16, 2, 16), dim=-1)
    v0_shared = shared(rows)["v"].detach().clone()
    v0_split = split(rows)["v"].detach().clone()
    opt_a = torch.optim.Adam(shared.parameters(), lr=1e-2)
    opt_b = torch.optim.Adam(split.parameters(), lr=1e-2)
    for _ in range(10):
        for wh, opt in ((shared, opt_a), (split, opt_b)):
            opt.zero_grad(set_to_none=True)
            _key_loss(wh, rows, tgt).backward()
            opt.step()
    drift_shared = float((shared(rows)["v"] - v0_shared).norm())
    drift_split = float((split(rows)["v"] - v0_split).norm())
    assert drift_shared > 1e-3, "control should drift (the documented E79 coupling)"
    assert drift_split == 0.0, f"split must NOT drift under key-side pressure, got {drift_split}"


# 4. checkpoint compatibility: strict is loud; trainer-style filtered load works


def test_state_dict_compat():
    off = _head(False, False, seed=17)
    on = _head(False, True, seed=17)
    with pytest.raises(RuntimeError, match="trunk_k"):
        on.load_state_dict(off.state_dict(), strict=True)  # missing trunk_k/trunk_v
    with pytest.raises(RuntimeError, match="trunk_k"):
        off.load_state_dict(on.state_dict(), strict=True)  # unexpected trunk_k/trunk_v
    # trainer init path (compatible keys by name+shape): loads to_k/to_v/alpha, skips trunk
    compat = {k: v for k, v in off.state_dict().items() if k in on.state_dict() and on.state_dict()[k].shape == v.shape}
    on.load_state_dict(compat, strict=False)
    assert torch.equal(on.to_k.weight, off.to_k.weight)


# 5. full model: d grid with both channels split + center, forward finite ------


def test_full_model_split_both_channels_finite():
    torch.manual_seed(0)
    model = FLUEDV36(_tiny_c_config(k_row_source="state", split_trunk=True, to_k_center=True)).train()
    assert hasattr(model.write_head, "trunk_k") and hasattr(model.write_head_k, "trunk_k")
    ids = torch.randint(1, 258, (1, 128))
    out = model(ids)
    assert torch.isfinite(out.logits_direct).all() and torch.isfinite(out.logits_backbone).all()
    # a grid unaffected: no WriteHead at all
    m_a = FLUEDV36(_tiny_c_config(v_row_source="memory", split_trunk=True, to_k_center=True))
    assert not hasattr(m_a, "write_head")


# 6. plumbing: --split-trunk reaches build_model --------------------------------


def test_cli_flag_reaches_model():
    from tools.train.v3_6.train_v36 import build_model, build_parser

    args = build_parser().parse_args(["--split-trunk", "--backbone-mode", "slm", "--k-row-source", "index", "--v-row-source", "state"])
    model = build_model(args)
    assert model.config.split_trunk is True
    assert hasattr(model.write_head, "trunk_k") and not hasattr(model.write_head, "trunk")
    args_off = build_parser().parse_args(["--backbone-mode", "slm", "--k-row-source", "index", "--v-row-source", "state"])
    assert build_model(args_off).config.split_trunk is False
