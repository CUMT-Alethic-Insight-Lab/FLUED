"""E120 链外件梯度隔离单测（红队补测 2026-09-11）。

设计意图（flued/v36/model.py `_slm_store_rows` 的 E120 分支注释钉死）：
`--e120-readout-swap` 开 = d 格 V 通道生产读出**整行换源**——v_rows 来自温启动
读出件 e120_readout，被替换的生产读出（KDAStateMachine.readout_query/realign）
「照跑但出链外——package_v 本体不再进任何损失路径」。此前 test_e120_readout_swap
覆盖了新件收梯度（乙列全解冻）与关态无新键，未覆盖**被替换件的零梯度账**。

Covers:
  (1) flag-off：模型无 e120 参数（零路径差：无属性、无 state_dict 键、
      strict-load 干净）——关态语义前提；
  (2) flag-on + 真训练步 backward：链外件（state_machine.readout_query /
      realign）grad 为 None 或恰零（不该收梯度的件没收梯度）；同前向里链内
      对照件照常收梯度（K 通道 state_machine_k.readout_query；新件
      e120_readout.slot_query）——隔离是换源所致而非前向未跑；
  (3) flag-off 对照：同一生产读出在关态 grad 非 None 且非零——(2) 的 None
      确由 e120 换源造成，不是普遍性伪迹。
"""

from __future__ import annotations

from types import SimpleNamespace

import torch

from flued.v36 import FLUEDV36
import tools.train.v3_6.train_v36_s1 as s1
from tests.test_e120_readout_swap import _ids, _tiny_d_config

DEVICE = torch.device("cpu")

# 与 test_e120_readout_swap::test_readout_piece_gets_gradient_in_full_unfreeze
# 同一 step_model 参数口径（乙列全解冻训练步）
_STEP_ARGS = SimpleNamespace(
    mask_prob=0.0, mask_span_min=1, mask_span_max=8, mask_mode="byte_span",
    max_chunks=32, max_span=16, task1_loss_weight=1.0, task2_loss_weight=1.0,
    predict_weight=1.0, predict_mode="latent", amp=False,
)


def _model(e120_on: bool, seed: int = 0) -> FLUEDV36:
    torch.manual_seed(seed)
    return FLUEDV36(_tiny_d_config(e120_readout_swap=e120_on)).eval()


def _train_step_and_backward(model: FLUEDV36) -> torch.Tensor:
    loss, _metrics = s1.step_model(model, (_ids(),), _STEP_ARGS, DEVICE, train=True)
    assert torch.isfinite(loss)
    loss.backward()
    return loss


def _grad_mass(p: torch.nn.Parameter) -> float:
    return 0.0 if p.grad is None else float(p.grad.abs().sum())


# --- 1. flag-off：零路径差（无 e120 参数） -----------------------------------------


def test_flag_off_has_no_e120_params():
    model = _model(e120_on=False)
    assert not hasattr(model, "e120_readout")
    assert not any(k.startswith("e120_readout.") for k in model.state_dict())
    model.load_state_dict(model.state_dict(), strict=True)  # 老 ckpt strict-load 干净


# --- 2. flag-on：链外件不收梯度；链内对照件照常收 -----------------------------------


def test_flag_on_replaced_readout_out_of_chain():
    model = _model(e120_on=True)
    _train_step_and_backward(model)
    # 链外件（被替换的 V 通道生产读出）：grad None 或恰零
    assert _grad_mass(model.state_machine.readout_query) == 0.0
    for name, p in model.state_machine.realign.named_parameters():
        assert _grad_mass(p) == 0.0, f"链外件 {name} 收到了梯度（出链纪律破）"
    # 链内对照 ①：K 通道状态机照常在生产读出链上（k_rows = package_k.mean）
    assert _grad_mass(model.state_machine_k.readout_query) > 0.0
    # 链内对照 ②：新件是 v_rows 唯一源，必收梯度（前提非空）
    assert _grad_mass(model.e120_readout.slot_query) > 0.0


# --- 3. flag-off 对照：同一读出在关态在链上 -----------------------------------------


def test_flag_off_same_readout_is_in_chain():
    model = _model(e120_on=False)
    _train_step_and_backward(model)
    assert _grad_mass(model.state_machine.readout_query) > 0.0
    assert any(_grad_mass(p) > 0.0 for p in model.state_machine.realign.parameters())
