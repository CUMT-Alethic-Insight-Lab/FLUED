# 04_DEPLOYED_USE｜真实联网定向检索日志

2026-11-08 · sol。目的：补部署使用、因果归因、机制忠实性与上下文利用的标准/反例；不以层级、来源回访或多粒度关键词约束结果。所有外发查询仅为公开机制词/论文题名，没有内部材料、实验数字或项目路径。未用数据源插件，故没有数据源技能/API调用；WebSearch、FetchURL和桌面内置浏览器为实际工具调用。

## 1. 实际查询：8条，不把一次查询结果数当作品数

| Q | 实际WebSearch查询字符串 | 有区分力的命中／处理 |
|---|---|---|
| Q01 | `activation patching metrics methods off distribution denoising noising Zhang Nanda 2024 best practices` | W0533 Best Practices已入库；搜索页还出现综述和聚合站，本轮不以它们作为原始结论依据。 |
| Q02 | `causal mediation language models causal tracing editing localization does not predict model editing 2023` | 2301.04213，定位与编辑目标不同的原始反例；进入N03。 |
| Q03 | `faithfulness explanations NLP sufficiency comprehensiveness ERASER remove and retrain distribution shift ROAR` | ERASER、Goodhart反例、Recursive ROAR；分别核原始来源，进入N04–N06。论文综述未替代原始定义。 |
| Q04 | `2025 2026 activation patching causal faithfulness circuit evaluation self repair interactions` | RelP 2508.21258及“Multiple Mediators”线索；RelP仅方法提速储备；交互新作由Q06精确定位。未将聚合站片段当已读原文。 |
| Q05 | `long context language models actual context use counterfactual semantic reasoning lexical overlap NoLiMa 2025` | W0192 NoLiMa重遇，已有FULL卡及综合，不加新作。也出现NovelQA等旁支，本轮不因名字补篇。 |
| Q06 | `"The Curse of Multiple Mediators" "Activation Patching"` | 定位原始2606.27510v1，后取得HTML正文与元数据；进入N08。 |
| Q07 | `"causal mediation analysis" "interpreting neural" Vig 2020` | 2004.12265，以及正式版另一题名线索；核arXiv作者与版本，进入N01。未逐版比对正式版，不双计。 |
| Q08 | `"Hydra Effect" "Self-repair" language models 2023` | 2307.15771v1，自修复原始工作；进入N02。未把二手课程中的解释细节当作者已核实验。 |

检索年代跨度2020–2026，近期重点2025–2026；同时包含经典工具、对工具的反例与新交互分析。不是完整近12个月系统综述，也未穷尽中文索引、全部白盒归因或大型多模态模型。

## 2. FetchURL逐次台账与实际阅读范围

**15次FetchURL＝12成功＋3次临时网络失败**。临时失败的原始HTML均在同URL重试一次成功，无403、登录墙或付费拒绝；没有绕过。一次成功取得长文不等通读。额外浏览器1篇用来核新作题名、作者、v1日期与§1–4显示内容；共创建1个标签并已关闭，未关闭其他会话标签。首次关闭因控制目标切换报TAB_NOT_ACTIVE，激活自己的标签后成功关闭。

| F | 实际URL | 返回／实际利用 |
|---|---|---|
| F01 | https://arxiv.org/abs/2309.16042v2 | 成功，摘要、版本史；身份再由F12核，正文局部F14。 |
| F02 | https://arxiv.org/html/2606.27510v1 | 临时network error；F06同URL重试成功。 |
| F03 | https://arxiv.org/abs/2004.12265 | 成功，摘要及v1/v2历史；未读全文。 |
| F04 | https://arxiv.org/html/2301.04213v2 | 临时network error；F07同URL重试成功。 |
| F05 | https://arxiv.org/abs/2307.15771 | 成功，摘要、仅v1历史；未读全文。 |
| F06 | https://arxiv.org/html/2606.27510v1 | 成功；长文被工具存为输出工件，实际选读§1–6，含式1–3、排名/IOI案例、讨论；附录A证明/B完整表未读，图未逐点核。另用浏览器DOM核题名、完整作者、2026-06-25与§1–4。不计FULL。 |
| F07 | https://arxiv.org/html/2301.04213v2 | 成功；长文输出工件定向读§4–8，含研究设计、表1、编辑变体、讨论和限制；附录、全部图及§3完整公式未读。不计FULL。 |
| F08 | https://aclanthology.org/2020.acl-main.408/ | 成功；原站摘要、完整作者、ACL2020、DOI、正式PDF链接；未读PDF。 |
| F09 | https://arxiv.org/abs/2308.14272 | 成功，摘要、v1历史；F15补正文局部。 |
| F10 | https://arxiv.org/abs/2110.08412 | 成功，摘要、v1–v3历史；未读全文。 |
| F11 | https://arxiv.org/abs/2508.21258 | 成功，摘要、v1/v2历史；未读全文，不从摘要数值做全面方法排名。 |
| F12 | https://export.arxiv.org/api/query?id_list=2004.12265,2307.15771,2301.04213,2308.14272,2110.08412,2508.21258,2309.16042,2606.27510 | 成功，官方Atom原始元数据，8条ID各自完整题名、作者、版本、首发/更新时间。不是第三方学术数据源API；没有凭摘要页From字段猜作者。 |
| F13 | https://arxiv.org/html/2308.14272v1 | 临时network error；F15同URL重试成功。 |
| F14 | https://arxiv.org/html/2309.16042v2 | 成功，长文输出工件仅定位方法/结果标题并实际读§6 Recommendations；作者建议STR、logit difference和单层优先，滑窗须解释为联合效应。没有全读§3–5及附录，W0533保持已有未完成状态。 |
| F15 | https://arxiv.org/html/2308.14272v1 | 成功，实际选读§1–4中分布外问题、指标定义、包装器构造、主要结果说明及EVAL-X标签编码；附录数表未提取，未逐格核主表。不计FULL。HTML提取漏Jennifer Hsia，作者以F12完整表为准。 |

工具保存的大输出工件位于会话临时存储，只为原始页面的可分页读取，不复制到项目或伪称03阅读卡。无论文代码执行、下载训练数据或模型。本轮没有删除系统工具工件。

## 3. 相对CATALOG去重：8个真新增发现候选

核验方法：对 `02_catalog/CATALOG.md` 全文件搜索稳定ID、确切题名关键词与主要作者/别名。下列8项的ID/实体没有命中；ERASER同时查`1911.03429`、`2020.acl-main.408`和`ERASER`。不因预印本/正式版题名差或v1/v2增加实体。未改CATALOG，不预占W0544之后编号。

### N01｜因果中介原始神经NLP锚

- **题名**：Causal Mediation Analysis for Interpreting Neural NLP: The Case of Gender Bias。
- **作者**（F12）：Jesse Vig、Sebastian Gehrmann、Yonatan Belinkov、Sharon Qian、Daniel Nevo、Simas Sakenis、Jason Huang、Yaron Singer、Stuart Shieber。
- **版本**：arXiv:2004.12265v2，2020-11-22；首发2020-04-26。原文：[v2 PDF](https://arxiv.org/pdf/2004.12265v2)、[元数据](https://arxiv.org/abs/2004.12265v2)。Q07见NeurIPS正式版另一题名 *Investigating Gender Bias in Language Models Using Causal Mediation Analysis*，本轮未逐版核对，不与v2混引或加一篇。
- **实际核验**：官方摘要、身份/版本。摘要明确报告跨组件协同/抑制和直接/间接效应；尚不能引用未读定理或特定数值。
- **价值**：把“组件掉分”落实为哪一种中介估计量，替代只在综合中泛称因果。

### N02｜消融后补偿的直接反例

- **题名**：The Hydra Effect: Emergent Self-repair in Language Model Computations。
- **作者**（F12）：Thomas McGrath、Matthew Rahtz、Janos Kramar、Vladimir Mikulik、Shane Legg。
- **版本**：arXiv:2307.15771v1，2023-07-28；[v1 PDF](https://arxiv.org/pdf/2307.15771v1)、[摘要](https://arxiv.org/abs/2307.15771v1)。
- **实际核验**：摘要/身份。作者报告某注意力层被消融后下游层补偿，以及晚层MLP对高似然token的抑制；无dropout训练也可出现。模型、样本与补偿占比待正文核，不能从二手说明补填。
- **价值**：零效应可能是干预引发的动态补偿，不只是“根本没用过”或静态冗余副本。

### N03｜定位不等最佳修复位置

- **题名**：Does Localization Inform Editing? Surprising Differences in Causality-Based Localization vs. Knowledge Editing in Language Models。
- **作者**（F12）：Peter Hase、Mohit Bansal、Been Kim、Asma Ghandeharioun。
- **版本**：arXiv:2301.04213v2，2023-10-16；首发2023-01-10；元数据注NeurIPS2023。[v2 HTML](https://arxiv.org/html/2301.04213v2)、[v2 PDF](https://arxiv.org/pdf/2301.04213v2)。
- **实际核验**：§4–8局部正文。§4表1在其GPT-J/CounterFact/ROME设置中，层选择比tracing effect更能解释编辑成功；§5的Fact Forcing有较强但仍小的增量解释，不能说所有关系严格为0。§8限短英文事实、两模型、指定层级编辑方法。
- **价值**：修复成功和定位正确是两个问题。FLUED接口改动有效不能自动倒证旧表示坏在那个接口。

### N04｜输入理由的充分性/完整性基准

- **题名**：ERASER: A Benchmark to Evaluate Rationalized NLP Models。
- **作者**（F08）：Jay DeYoung、Sarthak Jain、Nazneen Fatema Rajani、Eric Lehman、Caiming Xiong、Richard Socher、Byron C. Wallace。
- **版本**：ACL2020正式版，pp.4443–4458，DOI 10.18653/v1/2020.acl-main.408；[原站](https://aclanthology.org/2020.acl-main.408/)、[正式PDF](https://aclanthology.org/2020.acl-main.408.pdf)。
- **实际核验**：原站摘要和完整书目；PDF未读。充分性/完整性的具体计算在N05已读正文有复述，但不冒充已核ERASER原公式。
- **价值**：让“忠实性”有可对照的原始操作定义，再配反例，不只引用综述措辞。

### N05｜解释评价指标可被操纵

- **题名**：Goodhart's Law Applies to NLP's Explanation Benchmarks。
- **作者**（F12）：Jennifer Hsia、Danish Pruthi、Aarti Singh、Zachary C. Lipton。
- **版本**：arXiv:2308.14272v1，2023-08-28；[v1 HTML](https://arxiv.org/html/2308.14272v1)、[v1 PDF](https://arxiv.org/pdf/2308.14272v1)。正式发表身份本轮未核。
- **实际核验**：§1–4选读。用检测原输入/理由子集/互补子集的包装器操纵置信度，原输入预测/解释不因此获得改进，却可抬高ERASER指标；EVAL-X也可被按标签编码的理由欺骗。注意该文充分性定义取ERASER的相反号，不能混用方向。
- **价值**：删除性能差不自动衡量自然机制；独立评价器也不等免疫标签泄漏。

### N06｜再训练的用途与估计对象变化

- **题名**：Evaluating the Faithfulness of Importance Measures in NLP by Recursively Masking Allegedly Important Tokens and Retraining。
- **作者**（F12）：Andreas Madsen、Nicholas Meade、Vaibhav Adlakha、Siva Reddy。
- **版本**：arXiv:2110.08412v3，2022-10-31；首发2021-10-15。[v3 PDF](https://arxiv.org/pdf/2110.08412v3)、[摘要](https://arxiv.org/abs/2110.08412v3)。正式版关系本轮未核。
- **实际核验**：摘要、完整元数据，未读全文。Recursive ROAR（递归移除再训练：按重要性递归掩蔽输入后重训并看性能）与随机掩蔽曲线比较；摘要报告4种指标、8数据集及模型/任务依赖。
- **价值**：可处理重新分布/替代特征问题，但不能直接回答原固定模型的部署依赖；具体冗余控制效果待正文核。

### N07｜近似仪器提速，而不是因果金标

- **题名**：RelP: Faithful and Efficient Circuit Discovery in Language Models via Relevance Patching。
- **作者**（F12）：Farnoush Rezaei Jafari、Oliver Eberle、Ashkan Khakzar、Neel Nanda。
- **版本**：arXiv:2508.21258v2，2025-10-30；首发2025-08-28。[v2 PDF](https://arxiv.org/pdf/2508.21258v2)、[摘要](https://arxiv.org/abs/2508.21258v2)。
- **实际核验**：摘要/身份，未读全文。作者以层级相关性传播系数替代局部梯度，报告两次前向/一次反向并更贴近activation patching；更贴近patch分数不等自然路径更正确。
- **价值/优先级**：只有全量精确手术成本成为瓶颈才精读。暂不挤占核心队列，不能因标题“Faithful”把它当评价可靠性定理。

### N08｜近期中介交互与单件/组效应的区别

- **题名**：The Curse of Multiple Mediators: Hidden Interaction Effects in Activation Patching。
- **作者**（F12与浏览器正文）：Sankaran Vaidyanathan、David Arbour、Aaron Mueller、Scott Niekum、David Jensen。
- **版本**：arXiv:2606.27510v1，2026-06-25；[v1 HTML](https://arxiv.org/html/2606.27510v1)、[v1 PDF](https://arxiv.org/pdf/2606.27510v1)。正式发表本轮未知。
- **实际核验**：§1–6选读；§2/3加噪、去噪定义与式1；§4组干预分解；§5 IOI案例与§6局限/未来方向。未读完附录证明/全部数表、未独立认证定理。
- **内容边界**：作者在指定clean/corrupt背景下给出`NIE = PIE + INT`，即自然间接效应、纯间接效应和中介交互的分解；去噪与加噪不是可随意互换。§5.2显示去掉交互同样会漏掉条件机制；§5.3强调IOI功能分组已有独立刻画，不能假定任意模型都有清楚模块。局部二阶近似的条件须后续读证明，不能把它当任意长程模型保证。
- **价值**：比“可能有交互”更具体：何时单件排序会漏备份/条件机制，为什么组恢复分数与各件求和不符；也提醒减少替换距离不是无条件更好，可能消除研究目标的触发条件。

## 4. 重遇、漏读与漏综合的区分

| 发现 | 去重/状态 | 应采取什么 |
|---|---|---|
| Best Practices 2309.16042 | **W0533，已入漏读**；目录摘要核验，无W0533原卡；本轮仅摘要＋§6 | 先补已有作品，不能算第9个新实体。相关操作细节没有进入已审综合的ID链，不能用文库总篇数宣称标准充分。 |
| NoLiMa 2502.05167 | **W0192，已有FULL且已综合**；实读B11卡，专题02/04均引用 | 不新增、不再安排一次整篇普遍重读；需要扩展语义任务才定点返读具体控制。 |
| W0374、W0530、W0532、W0534/0535 | **已有且关键警告已综合** | 本轮贡献是重排四层权限与补缺，不把既有严谨工作说成从未覆盖。 |
| Vig/Hydra/Hase/ERASER/Goodhart/Recursive ROAR/RelP/Multiple Mediators | **8个相对CATALOG新实体候选** | 这里只登记发现与选读范围；正式入库、全文阅读和新W-ID由总负责人后续安排。 |

对整个 `04_synthesis/` 搜索`W0533|W0531|W0373|ERASER|mediation|中介|自修复|self.repair|Hydra|Goodhart`无命中，说明这些**具体原作/关键词**尚未纳入综合，不等同于所有相关思想都不存在。旧稿已有“冗余/互补”“非目标保真”等措辞，应保留并补原始证据，不重复创造名词。

## 5. 停止扩搜的理由与仍未知

本轴已找到足以改变下一步的缺口：操作标准已在库但漏读，交互/补偿与指标操纵有新原始来源。再按题名广撒网不会替代已有作品精读和目标宿主实验，因此本轮停止在8条定向查询，不凑新增数量。

未知继续保留：未逐版核验的正式版关系、未全文读取的附录/图表、未运行的代码与成本；W0050外置补充是否已由作者后来公开，本轮没有重新追索，不凭旧失败断言永远不存在。具体最小阅读队列和完成问题见 `READING_RECOMMENDATIONS.md`。
