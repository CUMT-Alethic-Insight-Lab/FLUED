# 丙臂 fla/CUDA 门控用例驱动（kda-kernels env 无 pytest；临时件，随回执登记）
import sys, tempfile, traceback, contextlib, types
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

# 最小 pytest shim（skipif 装饰器 + raises 上下文）
pytest_shim = types.ModuleType("pytest")
def _skipif(cond, reason=None):
    def deco(fn):
        if cond:
            fn._r3_skip_reason = reason
        return fn
    return deco
pytest_shim.mark = types.SimpleNamespace(skipif=_skipif)
@contextlib.contextmanager
def _raises(exc, match=None):
    try:
        yield
    except exc as e:
        if match and match not in str(e):
            raise AssertionError(f"match {match!r} not in {e!r}") from e
        return
    raise AssertionError(f"{exc} not raised")
pytest_shim.raises = _raises
@contextlib.contextmanager
def _fixture(*a, **k):
    def deco(fn):
        return fn
    return deco
pytest_shim.fixture = _fixture
sys.modules["pytest"] = pytest_shim

import tools.baselines.deltanet_r2.r2_spec as r2spec
import tools.baselines.deltanet_r2.r3_spec as r3
r2spec.normalize_tied_weights_keys()
import test_r3_vtile as t

GATED = [
    "test_param_anchor_vtile_zero_new_params",
    "test_double_attach_loudfail",
    "test_flag_off_after_attach_with_patch_loudfail",
    "test_verify_vtile_reload_keys_equal_and_bitexact",
    "test_verify_vtile_reload_loudfail_extra_key",
    "test_flag_off_forward_bitwise_vs_pure_fla",
    "test_passthrough_plan_none_bitwise_after_attach",
    "test_vtile_forward_tolerant_vs_native_and_grads_flow",
    "test_uniform64_plan_close_to_native",
]
fails = skipped = 0
for name in GATED:
    fn = getattr(t, name)
    if getattr(fn, "_r3_skip_reason", None):
        skipped += 1
        print(f"SKIP {name} ({fn._r3_skip_reason})", flush=True)
        continue
    try:
        # 用例间状态卫生（shim 无法跑 autouse fixture，驱动侧复位）
        r3.clear_vtile_plan()
        if r3._VTILE["patched"]:
            r3.detach_vtile()
        needs_tmp = "reload" in name
        with tempfile.TemporaryDirectory() as td:
            if needs_tmp:
                fn(Path(td))
            else:
                fn()
        print(f"PASS {name}", flush=True)
    except Exception:
        fails += 1
        print(f"FAIL {name}\n{traceback.format_exc()}", flush=True)
    finally:
        r3.clear_vtile_plan()
        if r3._VTILE["patched"]:
            r3.detach_vtile()
print(f"{'ALL GREEN' if fails == 0 else str(fails) + ' FAILED'} "
      f"({len(GATED)} gated: {len(GATED)-fails-skipped} run, {skipped} skip)")
sys.exit(1 if fails else 0)
