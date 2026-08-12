# FLUED v3.4

> 状态：历史主线。v3.4 收尾系列见 [`docs/versions/v3.5/`](../v3.5/)；当前主线见 [`docs/versions/v3.6/`](../v3.6/) 与 [`docs/CURRENT_STATE.md`](../../CURRENT_STATE.md)。
> 本目录按日期链组织。**收口文档**是当前结论的最高优先级入口；其他文档保留为历史证据链。

---

## 收口文档（当前结论入口）

| 日期 | 文档 | 一句话 |
| --- | --- | --- |
| 2026-07-15 | [`FLUED_V3_4_POST_MIGRATION_EXPERIMENTS_20260715_CN.md`](FLUED_V3_4_POST_MIGRATION_EXPERIMENTS_20260715_CN.md) | 硬盘迁移后实验总报告：边界闭环、核心路径、位置/小 AR、编码率、lookup/emit、memory 与 decoder 长程实验的修正版结论汇总。 |
| 2026-07-16 | [`FLUED_V3_4_ATTRIBUTION_MATRICES_RESULTS_20260716_CN.md`](FLUED_V3_4_ATTRIBUTION_MATRICES_RESULTS_20260716_CN.md) | 归因矩阵终评：2×40K 边界课程、3×20K memory 使用率、严格 no-memory 对照、修复后的 memory 干预与下一步架构决策。 |
| 2026-07-17 | [`FLUED_V3_4_CBIU_THREE_ROUND_RESULTS_20260717_CN.md`](FLUED_V3_4_CBIU_THREE_ROUND_RESULTS_20260717_CN.md) | 三轮 CBIU 在线实验正式结论：extra-readout 动作排序改善、latent 真实减少，但校准不足以接管 boundary/memory。 |

---

## 日期链（历史演进）

### 2026-07-10 pilot / 1K 筛选

- [`FLUED_V3_4_RATE_EMIT_CORRECTION_20260710_CN.md`](FLUED_V3_4_RATE_EMIT_CORRECTION_20260710_CN.md)：边际编码率公式、emit 价值定义与 500 步机制验证。**历史筛选口径**。
- [`FLUED_V3_4_ABLATION_RESULTS_20260710_CN.md`](FLUED_V3_4_ABLATION_RESULTS_20260710_CN.md)：1K 组件消融与位置×小 AR 初筛。**历史筛选口径**。

### 2026-07-11 5K 筛选 / 20K 课程

- [`FLUED_V3_4_5K_ABLATION_ANALYSIS_20260711_CN.md`](FLUED_V3_4_5K_ABLATION_ANALYSIS_20260711_CN.md)：5K 全组件消融，L2 边际编码率在 5K 尺度反超 exact。**历史筛选口径**。
- [`FLUED_V3_4_20K_RATE_CURRICULUM_ANALYSIS_20260711_CN.md`](FLUED_V3_4_20K_RATE_CURRICULUM_ANALYSIS_20260711_CN.md)：20K 四策略课程（exact/L2/uniform/curriculum）与切换恢复阈值。**历史筛选口径**。

### 2026-07-12 纠偏 / 路径修正 / memory ROI

- [`FLUED_V3_4_GLOBAL_PATH_CORRECTION_AND_RERUN_20260712_CN.md`](FLUED_V3_4_GLOBAL_PATH_CORRECTION_AND_RERUN_20260712_CN.md)：首次全局根因诊断、8 项代码纠偏清单与 P0–P4 重跑顺序。**历史纠偏口径**。
- [`FLUED_V3_4_PROGRESSIVE_MEMORY_ROI_20260712_CN.md`](FLUED_V3_4_PROGRESSIVE_MEMORY_ROI_20260712_CN.md)：渐进 memory 课程、边界 ROI 审计与动态 chunk 预算公式。**历史中间结论**。
- [`FLUED_V3_4_BOUNDARY_ROI_PROTOCOL_CN.md`](FLUED_V3_4_BOUNDARY_ROI_PROTOCOL_CN.md)：边界 ROI 协议与审计方法。

### 2026-07-13 20K memory/位置分析

- [`FLUED_V3_4_MEMORY_POSITION_20K_ANALYSIS_20260713_CN.md`](FLUED_V3_4_MEMORY_POSITION_20K_ANALYSIS_20260713_CN.md)：P0–P4 串行决策链、memory 归一化与 20K 三路径。**历史中间结论**。

### 2026-07-14 自查 / 修正 / 重跑矩阵

- [`FLUED_V3_4_FULL_SELF_AUDIT_20260714_CN.md`](FLUED_V3_4_FULL_SELF_AUDIT_20260714_CN.md)：代码事实、历史实验观察与未落地设计的逐项审计。**证据审计**。
- [`FLUED_V3_4_CORE_CORRECTION_AND_RERUN_20260714_CN.md`](FLUED_V3_4_CORE_CORRECTION_AND_RERUN_20260714_CN.md)：四项正式修正（confidence 执行、diag 编码率、one-shot 路线、shared-inverse decoder）与 R2–R6 闸门试跑。**正式修正细节**。
- [`FLUED_V3_4_RERUN_MATRIX_20260714_CN.md`](FLUED_V3_4_RERUN_MATRIX_20260714_CN.md)：B0–B5 边界校准、密度/裕量审计、切分比分母修正与执行命令。**操作矩阵**。
- [`FLUED_V3_4_IMPLEMENTATION_BASELINE_CN.md`](FLUED_V3_4_IMPLEMENTATION_BASELINE_CN.md)：迁移前实现基线与 16 条结构保持清单。

### 2026-07-15 迁移后总报告 / 归因计划 / 最小归因

- [`FLUED_V3_4_POST_MIGRATION_EXPERIMENTS_20260715_CN.md`](FLUED_V3_4_POST_MIGRATION_EXPERIMENTS_20260715_CN.md)：当前结论最高优先级入口（**收口文档**）。
- [`FLUED_V3_4_ATTRIBUTION_PLAN_20260715_CN.md`](FLUED_V3_4_ATTRIBUTION_PLAN_20260715_CN.md)：三个最小归因实验（decoder 探针、memory 干预、边界课程梯度）设计。
- [`FLUED_V3_4_MINIMAL_ATTRIBUTION_RESULTS_20260715_CN.md`](FLUED_V3_4_MINIMAL_ATTRIBUTION_RESULTS_20260715_CN.md)：decoder 隔离、memory 干预与梯度路径首轮结果。

### 2026-07-16 CBIU / 归因矩阵

- [`FLUED_V3_4_CBIU_DESIGN_AND_VALIDATION_PLAN_20260716_CN.md`](FLUED_V3_4_CBIU_DESIGN_AND_VALIDATION_PLAN_20260716_CN.md)：CBIU 统一监督定义、数学约束与 V0–V4 验证链。
- [`FLUED_V3_4_CBIU_V0_RESULTS_20260716_CN.md`](FLUED_V3_4_CBIU_V0_RESULTS_20260716_CN.md)：冻结 20K 检查点的首轮 CBIU 离线可辨识性结果。
- [`FLUED_V3_4_ATTRIBUTION_MATRICES_RESULTS_20260716_CN.md`](FLUED_V3_4_ATTRIBUTION_MATRICES_RESULTS_20260716_CN.md)：归因矩阵终评（**收口文档**）。
- [`FLUED_V3_4_ARCHITECTURE_GRADIENT_DECISION_TRACE_CN.md`](FLUED_V3_4_ARCHITECTURE_GRADIENT_DECISION_TRACE_CN.md)：v0.4–v3.4 架构谱系、数据流、梯度路由与关键代码索引。

### 2026-07-17 CBIU 三轮 / 后续实验

- [`FLUED_V3_4_CBIU_THREE_ROUND_RESULTS_20260717_CN.md`](FLUED_V3_4_CBIU_THREE_ROUND_RESULTS_20260717_CN.md)：三轮 CBIU 在线实验正式结论（**收口文档**）。
- [`FLUED_V3_4_FOLLOWUP_EXPERIMENTS_20260717_CN.md`](FLUED_V3_4_FOLLOWUP_EXPERIMENTS_20260717_CN.md)：decoder 解耦廉价方案证伪、CBIU MLP-64 多种子、emit 阶跃 warmup 证伪。

---

## 结果目录

| 目录 | 内容 |
| --- | --- |
| [`../../../results/v3.4/5k_ablation/`](../../../results/v3.4/5k_ablation/) | 5K 全组件消融原始日志与曲线 |
| [`../../../results/v3.4/20k_rate_comparison/`](../../../results/v3.4/20k_rate_comparison/) | 20K 边界策略与 curriculum 日志 |
| [`../../../results/v3.4/progressive_memory_20k/`](../../../results/v3.4/progressive_memory_20k/) | 渐进课程、memory 20K 与边界 ROI |
| [`../../../results/v3.4/memory_position_20k_20260713/`](../../../results/v3.4/memory_position_20k_20260713/) | 20K memory/位置分析 |
| [`../../../results/v3.4/position_memory_rerun_20260712/`](../../../results/v3.4/position_memory_rerun_20260712/) | 位置 memory 纠偏重跑 |
