# 字节级语言接口综述：交付入口

本目录为独立领域综述，不以FLUED多粒度草案作为总纲。英文由sol综合，关键论文由terra精读，独立sol红队审稿后，由另外的sol代理完整翻译中文，再经独立双语复审。

## 中文阅读顺序

1. [综述摘要](06_translation/EXECUTIVE_SUMMARY_ZH.md)
2. [完整综述](06_translation/SURVEY_ZH.md)：16节、2附录、8张比较表；对应约19,941词英文主稿。
3. [超级详细问题—方案—AI技术清单](06_translation/DETAILED_INVENTORY_ZH.md)：296条活跃记录完整中文；历史英文提取明确折叠保留。
4. [分类与机制归组](06_translation/CLASSIFICATION_ZH.md)：12个多标签问题家族及13条主阅读路线；不是未经执行的算法聚类。
5. [清单阅读导引](06_translation/INVENTORY_READING_GUIDE_ZH.md)
6. [15项开放研究问题](06_translation/OPEN_QUESTIONS_ZH.md)

“AI技术工具”在清单中指前人采用的CNN、状态空间、潜变量、蒸馏、策略优化等研究技术及其作用，不是本次助理工具。

## 英文及证据

- [英文主稿](04_synthesis/SURVEY_EN.md)
- [英文摘要](04_synthesis/EXECUTIVE_SUMMARY_EN.md)
- [英文开放问题](04_synthesis/OPEN_QUESTIONS_EN.md)
- [规范英文详细清单](02_inventory/DETAILED_INVENTORY.md)
- [作品目录](02_inventory/WORK_CATALOG.md)
- [统计定义](02_inventory/FINAL_AUTHOR_COUNTS.md)
- [阅读证据状态](02_inventory/EVIDENCE_STATUS.md)
- 03_reading/：本轮逐篇证据卡，旧卡引用保留原相对路径。

## 实际规模

- 141个来源实体：136篇论文、1份报告、3项标准、1项官方介绍。
- 296条可追溯问题/机制/证据记录，不等于296个彼此独立的科学问题。
- 92个具有限定版本全文阅读证据的独立来源：本轮62个新FULL＋30个旧FULL复用；另有2项指定范围的PARTIAL核查。
- 全文阅读不等于代码执行、证明独立认证或实验复现。部分清单条目仍基于摘要/局部证据，按条目标注。

## 独立复审

- [英文领域覆盖核销](05_review/FINAL_SURVEY_COVERAGE_RECHECK.md)
- [英文口径严谨性核销](05_review/FINAL_SURVEY_RIGOR_RECHECK.md)
- [详细清单与分类核销](05_review/INVENTORY_CLASSIFICATION_RECHECK.md)
- [中文正文双语核销](05_review/TRANSLATION_MAIN_RECHECK.md)
- [中文清单双语核销](05_review/TRANSLATION_INVENTORY_RECHECK.md)

上述最终复审范围内均无残留P0/P1交付阻断项。MtPC优化采样保证、TokSuite Figure6计算来源、若干预算与实现细节仍是明确开放问题，不以措辞修订冒充技术解决。

## 研究范围说明

之前列出的广域后续方向已完整保存于[后续方向名单](../flued_multigranularity_survey_20261108/07_scope_recovery/FOLLOWUP_DIRECTIONS.md)。本次完成字节接口独立综述，不表示原广域FLUED六轴报告已重新编写完成。未启动实验、修改生产代码或提交/推送。
