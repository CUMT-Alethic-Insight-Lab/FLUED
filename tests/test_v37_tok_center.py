"""E75 to_k_center hard-constraint tests (flued/v36/model.py WriteHead).

Spec pinned 2026-08-18: default off = bit-identical; on = subtract the running
center (EMA 0.99, detached, cold-start from first batch) from to_k output
pre-normalization; persistent=False buffer (old checkpoints strict-clean).
"""

from __future__ import annotations

import torch

from flued.v36 import FLUEDV36, V36Config
from flued.v36.model import WriteHead
import tools.analysis.v3_6.measure_key_collapse as kc  # row_geometry
from tests.test_v37_oracle_probe import _tiny_c_config


def _head(center: bool, seed: int = 0, d_mem=96, hidden=128, heads=2, hk=16) -> WriteHead:
    torch.manual_seed(seed)
    c = V36Config(
        d_mem=d_mem, write_hidden=hidden, kda_heads=heads, kda_head_k=hk, kda_head_v=32,
        backbone_mode="slm", summarizer_type="dit", to_k_center=center,
    )
    return WriteHead(c)


def _key_mu(wh: WriteHead, rows: torch.Tensor) -> float:
    k = wh(rows)["k"][0]  # (C, H, hk)
    return sum(kc.row_geometry(k[:, h])["mu"] for h in range(k.size(1))) / k.size(1)


# 1. default off: bit-identical forward, no buffer -----------------------------


def test_default_off_bit_identical_and_bufferless():
    a = _head(False, seed=7)
    b = _head(False, seed=7)
    b.eval()
    a.eval()
    rows = torch.randn(1, 12, 96)
    assert a(rows)["k"].eq(b(rows)["k"]).all()
    assert not hasattr(a, "k_center")
    # and the config default is off (legacy bit-preservation)
    assert V36Config().to_k_center is False


# 2. synthetic collapsed inputs: mu drops sharply with centering ---------------


def test_centering_de_collapses_keys():
    torch.manual_seed(3)
    shared = torch.randn(1, 1, 96) * 3.0
    rows = shared + 0.01 * torch.randn(1, 24, 96)  # single shared direction => collapse-prone
    off = _head(False, seed=11).eval()
    on = _head(True, seed=11)
    on.load_state_dict(off.state_dict(), strict=True)  # same weights, only the flag differs
    mu_off = _key_mu(off, rows)
    on.train()
    on(rows)  # cold start: buffer := batch mean
    on(rows)  # EMA warm
    mu_on = _key_mu(on, rows)
    assert mu_off > 0.9, f"synthesis should collapse uncentered keys, got {mu_off}"
    assert mu_on < mu_off - 0.4, f"centering should de-collapse, got {mu_on} vs {mu_off}"


# 3. EMA update in train mode, frozen in eval ----------------------------------


def test_ema_update_and_eval_freeze():
    wh = _head(True, seed=5)
    wh.train()
    rows_a = torch.randn(1, 8, 96) + 2.0
    k_a = wh.to_k(wh.trunk(rows_a)).detach().float().mean(dim=(0, 1))
    wh(rows_a)  # cold start
    assert torch.allclose(wh.k_center, k_a, atol=1e-6)
    rows_b = torch.randn(1, 8, 96) - 1.0
    k_b = wh.to_k(wh.trunk(rows_b)).detach().float().mean(dim=(0, 1))
    wh(rows_b)  # EMA step: 0.99 old + 0.01 new
    assert torch.allclose(wh.k_center, 0.99 * k_a + 0.01 * k_b, atol=1e-6)
    wh.eval()
    frozen = wh.k_center.clone()
    wh(torch.randn(1, 8, 96) + 10.0)  # eval: no update
    assert wh.k_center.eq(frozen).all()


# 4. gradient flows through the centering (unlike a regularizer arm) -----------


def test_gradient_flows_to_to_k():
    wh = _head(True, seed=9)
    wh.train()
    gates = wh(torch.randn(1, 8, 96))
    gates["k"].square().mean().backward()
    assert wh.to_k.weight.grad is not None and wh.to_k.weight.grad.abs().sum() > 0
    assert wh.to_k.bias.grad is not None and wh.to_k.bias.grad.abs().sum() > 0
    assert wh.k_center.grad is None  # buffer stays a statistic, never a parameter


# 5. checkpoint compatibility both directions (persistent=False ruling) --------


def test_state_dict_cross_compatibility():
    off = _head(False, seed=13)
    on = _head(True, seed=13)
    assert "k_center" not in on.state_dict()  # non-persistent: never saved
    on.load_state_dict(off.state_dict(), strict=True)  # old ckpt -> new flag model
    off.load_state_dict(on.state_dict(), strict=True)  # new-era ckpt -> old model
    # full-model level (tiny d grid: BOTH channels carry the buffer)
    torch.manual_seed(0)
    m_on = FLUEDV36(_tiny_c_config(k_row_source="state", to_k_center=True))
    assert m_on.write_head.to_k_center and m_on.write_head_k.to_k_center
    assert not any("k_center" in k for k in m_on.state_dict())
    torch.manual_seed(0)
    m_off = FLUEDV36(_tiny_c_config(k_row_source="state", to_k_center=False))
    m_off.load_state_dict(m_on.state_dict(), strict=True)
    m_on.load_state_dict(m_off.state_dict(), strict=True)
    # a grid: no WriteHead at all, flag is a no-op
    m_a = FLUEDV36(_tiny_c_config(v_row_source="memory", to_k_center=True))
    assert not hasattr(m_a, "write_head")


# 6. plumbing: --to-k-center reaches the built model ---------------------------


def test_cli_flag_reaches_model():
    from tools.train.v3_6.train_v36 import build_model, build_parser

    args = build_parser().parse_args(["--to-k-center", "--backbone-mode", "slm", "--k-row-source", "index"])
    model = build_model(args)
    assert model.config.to_k_center is True
    # a grid has no WriteHead; d grid would have two — a-grid build is enough
    assert not hasattr(model, "write_head")
    args_off = build_parser().parse_args(["--backbone-mode", "slm", "--k-row-source", "index"])
    assert build_model(args_off).config.to_k_center is False
