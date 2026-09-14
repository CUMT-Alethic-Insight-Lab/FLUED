"""R3 判决仪器启动器：probe_e122_deltanet_book 之上注入移植件装载路径。

纪律（任务书 §3.6/点火令）：**仪器零口径改动**——本体文件
``tools/analysis/cross_arch/probe_e122_deltanet_book.py`` 一字节不改（施工回执
附 sha256），本启动器只替换其模块级 ``load_model_and_tokenizer`` 装载函数：

- checkpoint config 带 ``r3_echo.enabled``（甲臂）→ 接回声（r3_spec.attach_echo）
  + 文件全量 state dict strict 白名单重载（坑 8：from_pretrained 对新增键是
  unexpected key 会静默丢弃，必须 strict 重载回训练终态）；
- 带 ``r3_summ.enabled``（乙臂）→ 接 summarizer 双头构造
  （r3_spec.attach_and_strict_reload_summ），同坑 8 通路；
- 两字段皆无（R2 母列/1.3B 复证臂等）→ 原装载路径原样返回。

窗/选择链/手术/bootstrap/种子全走仪器本体（零口径改动），种子谱系由 CLI
--seed 424242（bootstrap 424243）与母列同卷。

Usage（形态与母列收盘逐字同构，仅换启动器与 checkpoint）:
  python tools/baselines/deltanet_r2/probe_r3_echo_book.py \
      --model-path outputs/r3_transplant_summ_20260914/main20k_summ/latest \
      --corpus /workspace/corpus/corpus_v3.txt \
      --n-windows 500 --start-window 0 --seed 424242 --device cuda \
      --out-dir outputs/r3_transplant_summ_20260914/verdict_b0
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import tools.analysis.cross_arch.probe_e122_deltanet_book as e122  # noqa: E402
import tools.baselines.deltanet_r2.r2_spec as r2spec  # noqa: E402
import tools.baselines.deltanet_r2.r3_spec as r3  # noqa: E402

_orig_load = e122.load_model_and_tokenizer


def _load_with_r3_echo(model_path, device):
    model, tok, fp = _orig_load(model_path, device)
    if r3.config_has_echo(model.config):
        report = r3.attach_and_strict_reload(model, model_path)
        fp["r3_echo"] = report
        print(f"[r3] 回声已接通 + strict 白名单重载（{report['n_echo_keys']} 键，"
              f"参数锚 {r2spec.EXPECTED_PARAM_COUNT:,}+{r3.ECHO_NUM_PARAMS}"
              f"={r3.EXPECTED_PARAM_COUNT_ECHO:,}）", flush=True)
    elif r3.config_has_summ(model.config):
        summ_flag = getattr(model.config, "r3_summ", None) or {}
        ctrl = bool(summ_flag.get("ctrl"))
        side = summ_flag.get("side") or "both"
        report = r3.attach_and_strict_reload_summ(model, model_path,
                                                  side=side, ctrl=ctrl)
        fp["r3_summ"] = report
        print(f"[r3] summarizer 已接通（side={side}, ctrl={ctrl}）+ strict 白名单重载"
              f"（{report['n_summ_keys']} 键 / {r3.SUMM_NUM_PARAMS:,} 参数，参数锚 "
              f"{r2spec.EXPECTED_PARAM_COUNT:,}+{r3.SUMM_NUM_PARAMS:,}"
              f"={r3.EXPECTED_PARAM_COUNT_SUMM:,}）", flush=True)
    else:
        print("[r3] checkpoint 无 r3_echo/r3_summ 字段——按原路径装载"
              "（母列/对照底物）", flush=True)
    return model, tok, fp


e122.load_model_and_tokenizer = _load_with_r3_echo

if __name__ == "__main__":
    raise SystemExit(e122.main())
