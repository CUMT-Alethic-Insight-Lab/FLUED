"""Q10 to_k_whiten hard-constraint tests (flued/v36/model.py WriteHead).

Spec pinned 2026-08-20 (user-ruled gate arm): default off = bit-identical; on =
whiten the to_k output pre-normalization, k <- (k - EMA_mean) @ (EMA_cov +
eps I)^{-1/2} (eigh, fp32, refreshed every training step). Superset of
to_k_center (includes de-meaning). persistent=False buffers (old checkpoints
strict-clean; fresh eval starts identity until warmed).
"""

from __future__ import annotations

import torch

from flued.v36 import FLUEDV36, V36Config
from flued.v36.model import WriteHead
import tools.analysis.v3_6.measure_key_collapse as kc  # row_geometry
from tests.test_v37_oracle_probe import _tiny_c_config


def _head(whiten: bool, seed: int = 0, d_mem=96, hidden=128, heads=2, hk=16) -> WriteHead:
    torch.manual_seed(seed)
    c = V36Config(
        d_mem=d_mem, write_hidden=hidden, kda_heads=heads, kda_head_k=hk, kda_head_v=32,
        backbone_mode="slm", summarizer_type="dit", to_k_whiten=whiten,
    )
    return WriteHead(c)


def _key_mu(wh: WriteHead, rows: torch.Tensor) -> float:
    k = wh(rows)["k"][0]  # (C, H, hk)
    return sum(kc.row_geometry(k[:, h])["mu"] for h in range(k.size(1))) / k.size(1)


# 1. default off: bit-identical forward, no buffers ----------------------------


def test_default_off_bit_identical_and_bufferless():
    a = _head(False, seed=7)
    b = _head(False, seed=7)
    a.eval()
    b.eval()
    rows = torch.randn(1, 12, 96)
    assert a(rows)["k"].eq(b(rows)["k"]).all()
    assert not hasattr(a, "k_white") and not hasattr(a, "k_cov") and not hasattr(a, "k_center")
    assert V36Config().to_k_whiten is False


# 2. whitening decorrelates: post-transform covariance ~ identity --------------


def test_whitening_makes_covariance_identity():
    wh = _head(True, seed=11)
    wh.train()
    torch.manual_seed(3)
    shared = torch.randn(1, 1, 96) * 3.0
    rows = shared + 0.5 * torch.randn(1, 256, 96)  # collapse-prone shared direction
    for _ in range(3):  # cold start + EMA warm
        wh(rows)
    with torch.no_grad():
        k = wh.to_k(wh.trunk(rows)).detach().float()
        xw = (k.reshape(-1, k.size(-1)) - wh.k_center) @ wh.k_white
        cov = (xw.T @ xw) / xw.size(0)
        ident = torch.eye(cov.size(0))
        # off-diagonal CORRELATION crushed vs the raw (unwhitened) one — the
        # collapse signature is cos-scale, so compare corr, not raw cov
        def _off_corr(cov):
            d = cov.diagonal().clamp_min(1e-12)
            corr = cov / (d.sqrt().unsqueeze(0) * d.sqrt().unsqueeze(1))
            return (corr - torch.eye(cov.size(0))).abs().mean()
        raw = k.reshape(-1, k.size(-1))
        raw_c = raw - raw.mean(dim=0)
        cov_raw = (raw_c.T @ raw_c) / raw_c.size(0)
        off_raw = _off_corr(cov_raw)
        off_white = _off_corr(cov)
        assert off_white < off_raw * 0.05, f"whitening should crush off-diagonal corr: {off_white} vs {off_raw}"
        # diagonal equalized toward 1 (allowing eps-ridge slack on near-null dirs)
        d = cov.diagonal()
        assert float(d.mean()) > 0.5 and float(d.std()) < 0.5, f"diag not equalized: {d}"


# 3. synthetic collapsed inputs: mu drops below the centering-only level -------


def test_whitening_de_collapses_keys_harder_than_centering():
    torch.manual_seed(3)
    shared = torch.randn(1, 1, 96) * 3.0
    rows = shared + 0.01 * torch.randn(1, 64, 96)  # single shared direction => collapse-prone
    off = _head(False, seed=11).eval()
    on = _head(True, seed=11)
    on.load_state_dict(off.state_dict(), strict=True)  # same weights, only the flag differs
    mu_off = _key_mu(off, rows)
    on.train()
    on(rows)  # cold start
    on(rows)  # EMA warm
    mu_on = _key_mu(on, rows)
    assert mu_off > 0.9, f"synthesis should collapse unwhitened keys, got {mu_off}"
    assert mu_on < 0.35, f"whitening should de-collapse hard, got {mu_on} vs {mu_off}"


# 4. EMA update in train mode, frozen buffers in eval --------------------------


def test_ema_update_and_eval_freeze():
    wh = _head(True, seed=5)
    wh.train()
    rows_a = torch.randn(1, 64, 96) + 2.0
    k_a = wh.to_k(wh.trunk(rows_a)).detach().float()
    m_a = k_a.mean(dim=(0, 1))
    xa = (k_a.reshape(-1, k_a.size(-1)) - m_a)
    cov_a = (xa.T @ xa) / xa.size(0)
    wh(rows_a)  # cold start
    assert torch.allclose(wh.k_center, m_a, atol=1e-6)
    assert torch.allclose(wh.k_cov, cov_a, atol=1e-6)
    rows_b = torch.randn(1, 64, 96) - 1.0
    k_b = wh.to_k(wh.trunk(rows_b)).detach().float()
    m_b = k_b.mean(dim=(0, 1))
    xb = (k_b.reshape(-1, k_b.size(-1)) - m_b)
    cov_b = (xb.T @ xb) / xb.size(0)
    wh(rows_b)  # EMA step
    assert torch.allclose(wh.k_center, 0.99 * m_a + 0.01 * m_b, atol=1e-6)
    assert torch.allclose(wh.k_cov, 0.99 * cov_a + 0.01 * cov_b, atol=1e-6)
    wh.eval()
    frozen = (wh.k_center.clone(), wh.k_cov.clone(), wh.k_white.clone())
    wh(torch.randn(1, 64, 96) + 10.0)  # eval: no update
    assert wh.k_center.eq(frozen[0]).all() and wh.k_cov.eq(frozen[1]).all() and wh.k_white.eq(frozen[2]).all()


# 5. gradient flows through the whitening (buffer stays a statistic) -----------


def test_gradient_flows_to_to_k():
    wh = _head(True, seed=9)
    wh.train()
    gates = wh(torch.randn(1, 16, 96))
    gates["k"].square().mean().backward()
    assert wh.to_k.weight.grad is not None and wh.to_k.weight.grad.abs().sum() > 0
    assert wh.to_k.bias.grad is not None and wh.to_k.bias.grad.abs().sum() > 0
    assert wh.k_center.grad is None and wh.k_cov.grad is None and wh.k_white.grad is None


# 6. checkpoint compatibility both directions (persistent=False ruling) --------


def test_state_dict_cross_compatibility():
    off = _head(False, seed=13)
    on = _head(True, seed=13)
    assert not any(k in on.state_dict() for k in ("k_center", "k_cov", "k_white"))
    on.load_state_dict(off.state_dict(), strict=True)  # old ckpt -> new flag model
    off.load_state_dict(on.state_dict(), strict=True)  # new-era ckpt -> old model
    # full-model level (b grid: write_head_k carries the buffers)
    torch.manual_seed(0)
    m_on = FLUEDV36(_tiny_c_config(k_row_source="state", to_k_whiten=True))
    assert m_on.write_head.to_k_whiten and m_on.write_head_k.to_k_whiten
    assert not any("k_white" in k or "k_cov" in k for k in m_on.state_dict())
    torch.manual_seed(0)
    m_off = FLUEDV36(_tiny_c_config(k_row_source="state", to_k_whiten=False))
    m_off.load_state_dict(m_on.state_dict(), strict=True)
    m_on.load_state_dict(m_off.state_dict(), strict=True)
    # a grid: no WriteHead at all, flag is a no-op
    m_a = FLUEDV36(_tiny_c_config(v_row_source="memory", to_k_whiten=True))
    assert not hasattr(m_a, "write_head")


# 7. plumbing: --to-k-whiten reaches the built model ---------------------------


def test_cli_flag_reaches_model():
    from tools.train.v3_6.train_v36 import build_model, build_parser

    args = build_parser().parse_args(["--to-k-whiten", "--backbone-mode", "slm", "--k-row-source", "index"])
    model = build_model(args)
    assert model.config.to_k_whiten is True
    args_off = build_parser().parse_args(["--backbone-mode", "slm", "--k-row-source", "index"])
    assert build_model(args_off).config.to_k_whiten is False
