# 08_GLOBAL_SCOPE：真实检索与去重记录

2026-11-08｜只发公开机制词；未发送项目内部草案、实验数字、代码或文档。sol定向发现，不计原文全文精读。

## 1. 已执行查询（6条不同文本）

平台：前5条用Kimi Code Desktop内置浏览器Bing搜索并实际读取搜索结果DOM；第6条使用WebSearch作精确题名/原始链接补查。搜索引擎自动摘要不作为论文结果证据；下节另列成功取到的原始来源。

| # | 实际查询 | 要区分的问题 | 观察与下一步 |
|---|---|---|---|
| Q1 | `predictive state representations sufficient statistic dynamical systems learning memory Littman Sutton Singh 2001` | 记忆是否必须重建历史？可否直接保存未来预测的充分状态？ | 命中NeurIPS原站与作者机构PDF；原站浏览器超时，Fetch可读局部，作者PDF成功核题名、作者、定义和结论 |
| Q2 | `2025 2026 test time training Titans memory compression recurrent learning expressive hidden states survey` | 不回访原细源的强替代范式是否被忽略？ | 命中Titans原站、OpenReview和TTT线索；后续取arXiv原始摘要/版本；目录内W0234/W0242已有但无卡 |
| Q3 | `"posterior collapse" "Lagging Inference Networks" 2019` | 信息通道不被使用能否仅因优化时序、而非容量或粒度？ | 命中arXiv:1901.05534；取v2摘要、HTML及PDF首页/方法局部核验 |
| Q4 | `"state space models" "copying" "Zoology" recall 2024 2025` | 固定状态的形式容量与已训模型检索失败是否同一原因？ | 命中Revisiting Associative Recall；原站摘要揭示学习率/宽深度敏感；Zoology原摘要给自然召回与合成任务差异，两者都已在库无卡 |
| Q5 | `2026 "memory" "test-time training" survey neural sequence models` | 最近是否有以状态/测试期适配而非多粒度访问组织的综述？ | 命中Beyond Fixed Memory综述、test-time regression等；综述仅发现；另定向复核目录已有2026 W0213的query-first反例原摘要 |
| Q6 | `"Beyond Fixed Memory" "Survey" "Neural Memory"` | 核精确题名、作者/原始URL，防把第三方总结当综述 | WebSearch返回OpenReview `HaT1jGiqrS`及NeurIPS PALM线索；原站Fetch为验证墙，未绕过，不作已读/已核原文 |

Q5后对W0213的原站访问是目录定向核查，不伪计为另一条搜索查询。本轮没有做系统性全领域检索、引文网络穷尽、中文/跨语检索或2026全部新论文扫描。

## 2. 成功原始来源核验：7个去重作品

| 作品/身份 | 实际取到的原始URL/版本 | 本轮真实范围与可用结论 | CATALOG去重 |
|---|---|---|---|
| Predictive Representations of State；Michael L. Littman、Richard S. Sutton、Satinder Singh；NeurIPS 2001入口所指原作 | https://papers.nips.cc/paper/1983-predictive-representations-of-state ；作者机构PDF https://web.eecs.umich.edu/~baveja/Papers/psr.pdf | 原站Fetch局部；作者PDF解析文本含§1定义、定理1、§3结论。定向核作者栏/摘要、PSR定义与“学习优势仍待未来验证”的结论；未逐式审证明/图、未作FULL。预测状态以多步动作条件未来观测预测作充分统计；有限POMDP（部分可观测马尔可夫决策过程：用隐状态描述受动作影响的观测系统）存在性不等语言学习保证。PDF稿无本轮确认的修订号 | **真新增N1**：精确题名/预测状态词在CATALOG无命中；不分配新W-ID |
| Lagging Inference Networks and Posterior Collapse in Variational Autoencoders；Junxian He、Daniel Spokoyny、Graham Neubig、Taylor Berg-Kirkpatrick | https://arxiv.org/abs/1901.05534v2 ；https://arxiv.org/html/1901.05534v2 ；https://arxiv.org/pdf/1901.05534v2 | v2=2019-01-28、首页ICLR2019；作者从PDF首页核。读摘要、引言/§2–4与§6方法/成本局部，未逐表与附录完成。后验塌缩（模型忽略潜变量且推断分布趋向先验）可有推断滞后机制；其方法改内外更新次序，不添加新模型组件。§6.3同时说比普通VAE慢2–3倍，不可叫免费修复；不报告未核表格精确性能 | **真新增N2**：稳定ID/题名/塌缩检索在CATALOG无命中 |
| Titans: Learning to Memorize at Test Time | https://arxiv.org/abs/2501.00663 | 原摘要＋提交史，v1首发2024-12-31。确认神经长期记忆与注意力组合、多个整合变体，未核全部机制/实验/作者栏；不采用引擎AI摘要里的规模与性能作为实证 | **已入漏读W0234**；无卡，非新增/PARTIAL |
| Learning to (Learn at Test Time): RNNs with Expressive Hidden States；Yu Sun等（原页列完整作者） | https://arxiv.org/abs/2407.04620 ；https://arxiv.org/abs/2407.04620v4 | 原摘要＋版本史，v4=2025-08-31；隐状态本身是模型、更新为自监督学习步；TTT-MLP访存困难也在摘要中。未读全文，不将长上下文摘要胜负升级同预算定律 | **已入漏读W0242**；无卡 |
| Zoology: Measuring and Improving Recall in Efficient Language Models | https://arxiv.org/abs/2312.04927 | v1=2023-12-08；读原摘要。自然召回差距与合成AR成功不一致、提出多查询关联召回及混合结构。摘要量化不在本审计用作跨架构公平排名；完整作者/方法与实验仍待精读 | **已入漏读W0060**；无卡 |
| Revisiting Associative Recall in Modern Recurrent Models | https://arxiv.org/abs/2508.19029 | 原摘要＋史，v2=2025-10-10；学习率和宽深度影响排名，不能把一次差距都归状态位数。完整作者本轮未从原作者栏核齐；不凭提交人填作者 | **已入漏读W0088**；无卡 |
| Beyond State Capacity: Why Retrieval Breaks in Mamba | https://arxiv.org/abs/2610.19709 | 原摘要＋史，v1=2026-10-14；先给查询的设定下仍有差距，作者把它与相关性信号跨深度迟到、选择门时序相联。只作为需精读的强反解释，不声称已核干预实验；完整作者栏未核齐 | **已入漏读W0213**；无卡 |

核验分母是作品，不是请求次数：同篇abs/HTML/PDF和作者镜像不重复计。**7＝2已核新增＋5既有漏读；新FULL＝0。** W0229等已有FULL卡属于本地重综合输入，不与本表重复称新精读。

## 3. 未核候选与失败

- **N3，待核，不计已核新增**：*Beyond Fixed Memory: A Survey of Neural Memory Mechanisms and Test-Time Learning for Sequence Modeling*。原站URL https://openreview.net/forum?id=HaT1jGiqrS 。WebSearch显示Narges Mokhtari、Farzan Haddadi及2026-10-01线索；检索又见PALM2026 workshop线索。**作者/日期/会场仅检索元数据，未由可读原站原文核验，不据此认定录用或版本**。Fetch返回“Complete the check … Sign in”，停止，不借PDF/API/身份会话绕过。精确题名/ID在CATALOG无命中。它提示替代的分类视角，但本审计不借其综述措辞认证任何原始机制。
- PSR原站内置浏览器导航超时；相同公开页面Fetch成功取得局部、作者机构PDF成功，属于合法原始来源补取，不是绕过拒绝。
- 另尝试过NeurIPS 2001备用hash地址 `https://proceedings.neurips.cc/paper/2001/hash/6ef80bb237adf4b6f77d0700e1255907-Abstract.html`，网络失败；该备用路径未获原站元数据认证，不作为身份/年份依据，也不将此失败记成论文无全文。
- 浏览器因8代理并行控制曾返回`TAB_NOT_ACTIVE`；重新激活后继续读取自己的tab，没有读取其他代理页面内容作为证据。这不是网页拒绝或论文访问失败。
- 搜索结果中AI总结、博客、Github清单、vixra无关结果均未作为一手证据；不为增加篇数补进目录。

## 4. 去重和检索后的最小决策变化

1. N1把“充分性”从重构旧内容/任意问答移到可递归更新的未来预测统计；这是可与回访并列的路线，而非证明回访无用。
2. N2提供优化不均衡而非添加层级/容量的原始竞争解释；VAE（变分自编码器：通过潜变量模型与近似后验共同优化数据似然下界）与本项目确定性压缩器并不相同，须先精读适用边界。
3. W0234/W0242/W0060/W0088/W0213说明**先补读比泛扩搜更值钱**：搜索发现的强替代和反例多数已在543实体里，只是未进入实读/综合。
4. 精确Grep检索`Titans|W0234|W0242|W0088|W0213|W0199|W0201|Predictive Representations|1901.05534|posterior collapse`于旧`04_synthesis`无命中，支持“这组具体来源未被显式综合”，但不是所有同类机制完全未被提及；Atlas/回归卡已有并应复用。
5. 不修改CATALOG，N1/N2/N3为本报告临时发现编号，不能与全局W-ID相加成546“已入库作品”。

浏览器收尾：本轮只创建4个后台研究tab（Q4/Q5复用同tab）；尝试关闭均返回TAB_NOT_ACTIVE，未关闭其他来源tab。并行控制会切换活动目标；未为清理研究页强占其他代理控制。当前全局后台标签很多（超过10个会使侧栏拥挤），这些4页非额外阅读成果。
