"""R2 臂（DeltaNet-50M × corpus_v3 × 20K，fla 原生 DeltaNet from-scratch）施工件。

任务书：docs/versions/v3.7/FLUED_V3_7_R2_DELTANET_IN_OUR_REGIME_20260913_CN.md（冻结 v1.0）。
- r2_spec.py      冻结规格单源（配置/参数锚/窗语义/LR 出处/看门狗线/种子纪律）。
- train_deltanet_r2.py   训练器（架构零改造：fla DeltaNetForCausalLM 原样 from_config）。
- measure_r2_anchors.py  门②锚直测（坑 9：分母锚全部在本臂体制直测，不引不借在册数）。
"""
