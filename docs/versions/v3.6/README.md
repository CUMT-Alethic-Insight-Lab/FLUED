# FLUED v3.6

> 状态：**当前主线**。单一事实源见 [`docs/CURRENT_STATE.md`](../../CURRENT_STATE.md)；术语见 [`docs/TERMS.md`](../../TERMS.md)。

## 当前主线规格

- [`FLUED_V3_6_SPEC_20260725_CN.md`](FLUED_V3_6_SPEC_20260725_CN.md)：v3.6（KDA 世代 / S36）唯一规格书，§1–§26。
  - **当前有效设计**：§21（k=1 正本）、§22（智能密度纲领）、§26（S39 档案馆内容寻址远程查询接口预注册）。
  - **已闭环历史决策**：§13–§20、§23–§25。
  - **原始规格**：§1–§12，多处已被后续节修订。

## 关键证据与研究材料

| 文档 | 用途 |
| --- | --- |
| [`docs/research/ARCHITECTURE_HISTORY_CN.md`](../../research/ARCHITECTURE_HISTORY_CN.md) | v0.4 到 S36 的架构发展史 |
| [`docs/research/RESEARCH_SWEEP_20260808_CN.md`](../../research/RESEARCH_SWEEP_20260808_CN.md) | 九路文献侦察（检索墙 / 循环塌缩 / 锥形网络等） |
| [`docs/research/COLLISION_SCOUT_S38_ARM_B_20260809_CN.md`](../../research/COLLISION_SCOUT_S38_ARM_B_20260809_CN.md) | S38 残差状态矩阵的撞车侦察 |
| [`docs/research/COLLISION_SCOUT_S39_ARCHIVE_QUERY_20260810_CN.md`](../../research/COLLISION_SCOUT_S39_ARCHIVE_QUERY_20260810_CN.md) | S39 档案馆内容寻址远程查询接口的撞车侦察 |

## 训练入口

```text
tools/train/v3_6/train_v36_s1.py         # 当前 canonical 训练器
tools/train/v3_6/train_v36.py            # 早期训练器（v36.0 形态，历史兼容）
tools/train/v3_6/train_s0_segmentor.py   # S0 segmentor 预训
```

默认配置：[`configs/canonical_v36.json`](../../../configs/canonical_v36.json)。
