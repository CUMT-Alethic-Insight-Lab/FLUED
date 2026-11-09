# 04_DEPLOYED_USE｜最小高价值阅读队列

2026-11-08 · sol。**10项核心队列，不要求恢复所有未读作品，更不把本轮局部正文选读升级为FULL。** 目标是获得“当前压缩表示为何不被原生模型使用”的可判读诊断，不是证明多粒度回访应当成为总方案。

本轮核过21条相关目录、逐张读12卡（11卡自报FULL、1卡PARTIAL），联网8条查询，发现相对CATALOG的8个新候选。队列综合已有未读、关键缺料、经典原始定义、反例和近期进展，不按新旧篇数配额。N编号对应本目录 `SEARCH_LOG.md`，非全局W-ID。

## 1. 优先次序与逐篇完成问题

作者/版本已经外核的项以官方元数据为准；只从旧卡/目录继承的项明确标出，不冒充本轮再次认证。URL给锁定版本，未取得材料的地址不猜造。

| 顺序 | 作品、身份与准确原文入口 | 本轮/既有状态 | 下一位全文读者必须回答的问题与交付 |
|---|---|---|---|
| 1 | **W0533 — Towards Best Practices of Activation Patching in Language Models: Metrics and Methods**；Fred Zhang、Neel Nanda；arXiv:2309.16042v2，2024-01-17（元数据注ICLR2024）。[v2 PDF](https://arxiv.org/pdf/2309.16042v2)，[v2 HTML](https://arxiv.org/html/2309.16042v2) | 已入未完成卡；本轮外核身份、版本、摘要及§6建议，**非FULL** | 核§3–5、附录实验：高斯噪声/对称token替换改变了什么？概率、logit差、KL对哪些机制敏感？滑窗测的是联合还是单层贡献？交付一张“估计目标—破坏方案—指标—失败模式”表，不照搬自然替换必然分布内的口号。 |
| 2 | **N08 — The Curse of Multiple Mediators: Hidden Interaction Effects in Activation Patching**；Sankaran Vaidyanathan、David Arbour、Aaron Mueller、Scott Niekum、David Jensen；arXiv:2606.27510v1，2026-06-25。[v1 PDF](https://arxiv.org/pdf/2606.27510v1)，[v1 HTML](https://arxiv.org/html/2606.27510v1) | 真新增发现；本轮选读§1–6，附录未读，正式发表未知 | 核式1–3、附录A、IOI完整表：加噪/去噪为何测不同量？局部二阶近似有哪些平滑性/扰动条件？单件交互与组间交互不能混称。何时“去掉交互”反而漏条件机制？交付可在两个记忆通道上实施的有限四格合同，不宣称全组合穷尽。 |
| 3 | **N02 — The Hydra Effect: Emergent Self-repair in Language Model Computations**；Thomas McGrath、Matthew Rahtz、Janos Kramar、Vladimir Mikulik、Shane Legg；arXiv:2307.15771v1，2023-07-28。[v1 PDF](https://arxiv.org/pdf/2307.15771v1) | 真新增；摘要/官方作者版本已核，正文未读 | 干预后补偿是否发生在固定权重推理？怎样量补偿位置/时间、与静态冗余区分？局部直接贡献和允许下游响应的总效应分别是什么？模型/任务范围和失败反例一并记录，不能从摘要补填补偿比例。 |
| 4 | **N04 — ERASER: A Benchmark to Evaluate Rationalized NLP Models**；Jay DeYoung、Sarthak Jain、Nazneen Fatema Rajani、Eric Lehman、Caiming Xiong、Richard Socher、Byron C. Wallace；ACL2020正式版，DOI10.18653/v1/2020.acl-main.408。[正式PDF](https://aclanthology.org/2020.acl-main.408.pdf)，[正式记录](https://aclanthology.org/2020.acl-main.408/) | 真新增；原站摘要/完整身份已核，PDF未读 | 原始充分性/完整性公式、符号方向、预测标签/真值标签、删理由/只留理由的模型权限如何规定？人类证据一致性和模型依赖分开算什么？对照N05，不能把评测提案当可靠性已证。 |
| 5 | **N05 — Goodhart's Law Applies to NLP's Explanation Benchmarks**；Jennifer Hsia、Danish Pruthi、Aarti Singh、Zachary C. Lipton；arXiv:2308.14272v1，2023-08-28。[v1 PDF](https://arxiv.org/pdf/2308.14272v1)，[v1 HTML](https://arxiv.org/html/2308.14272v1) | 真新增；本轮局部读§1–4，附录数表未核，正式版未知 | 包装器如何在原输入预测/解释不改善时提高删除指标？测试分布保留程度、检测误差和标签编码各有什么条件？EVAL-X为何也可能受骗？该文充分性是ERASER相反号，必须标清方向。交付两个具体反例而非“所有删除法都无效”。 |
| 6 | **W0050 — Evaluating Compressed Memory: Dependence, Utility, and Content Benefit**；Minsu Oh、Seunghui Jwa、Chanjun Park、Yeo-Chan Yoon；arXiv:2610.19373v1。[v1 PDF](https://arxiv.org/pdf/2610.19373v1)，[v1 HTML](https://arxiv.org/html/2610.19373v1) | [原卡B03/W0050](../../03_reading/B03/W0050.md)实盘PARTIAL；本轮仅读卡，身份/版本由原卡继承，未再外核 | 优先追作者明确引用的 `supporting_evidence.pdf` 与配置表O：训练预算、参考训练/调参能否匹配？D/U/C哪些是固定系统手术、哪些是改训练系统？供体是否含答案、F1与Match的差别如何解释？补充原URL**未知，不猜**。若仍取不到，用已有主表作限定例，停止完整公平排名。 |
| 7 | **N01 — Causal Mediation Analysis for Interpreting Neural NLP: The Case of Gender Bias**；Jesse Vig、Sebastian Gehrmann、Yonatan Belinkov、Sharon Qian、Daniel Nevo、Simas Sakenis、Jason Huang、Yaron Singer、Stuart Shieber；arXiv:2004.12265v2，2020-11-22。[v2 PDF](https://arxiv.org/pdf/2004.12265v2) | 真新增；原始摘要/完整作者版本已核，正文未读；正式版题名关系未逐版比对 | 处理变量、直接/间接效应、神经元/头集合的干预具体定义是什么？协同/抑制何时可加、何时不行？逐例与平均效应的权限、效应尺度是什么？与N08先统一量，再比较结论，不能只借“因果中介”术语。 |
| 8 | **N03 — Does Localization Inform Editing? Surprising Differences in Causality-Based Localization vs. Knowledge Editing in Language Models**；Peter Hase、Mohit Bansal、Been Kim、Asma Ghandeharioun；arXiv:2301.04213v2，2023-10-16，元数据注NeurIPS2023。[v2 PDF](https://arxiv.org/pdf/2301.04213v2)，[v2 HTML](https://arxiv.org/html/2301.04213v2) | 真新增；本轮选读§4–8，§3/附录/全部图未读 | 定位和编辑分别固定哪些变量？哪些指标/编辑变体存在正关系，哪些没有？跨模型/数据的结果边界？交付“能定位信息经过，不必能选最佳修复点”的具体反例；不升级为一般可解释性无用论。 |
| 9 | **W0531 — RAVEL: Evaluating Interpretability Methods on Disentangling Language Model Representations**；目录记Jing Huang、Zhengxuan Wu、Christopher Potts、Mor Geva；目录版本arXiv:2402.17700v2。[目录锁定v2 PDF](https://arxiv.org/pdf/2402.17700v2) | 已入未读，无同名W-ID卡；本轮未联网再次核作者/版本/正文 | 核“改变目标属性而保留其他属性”的成功口径、训练/测试实体/模板是否独立；评价干预器表达力还是模型原生机制？非目标保真是否只覆盖少数属性？先核身份/版次，未知处不从目录推结论。 |
| 10 | **N06 — Evaluating the Faithfulness of Importance Measures in NLP by Recursively Masking Allegedly Important Tokens and Retraining**；Andreas Madsen、Nicholas Meade、Vaibhav Adlakha、Siva Reddy；arXiv:2110.08412v3，2022-10-31。[v3 PDF](https://arxiv.org/pdf/2110.08412v3) | 真新增；摘要/完整作者版本已核，正文未读，正式版关系未知 | 递归掩蔽如何避免静态重要性/冗余误读？重训和随机掩蔽怎样匹配？它解释的是旧模型还是新训练过程？全成本、任务依赖、反例是什么？只在考虑再训练评价时采用，不能替固定部署模型效应。 |

若只能先读5篇：**1–5**闭合最急的“操作标准—近期交互—补偿—理由指标—指标反例”。第6是现存PARTIAL补料，可并行合法追索；暂取不到不阻止已有范围的谨慎综合。7–10在具体中介、修复或方法选型承重前完成。

## 2. 不重复排全文阅读的已有核心依据

以下原卡已FULL且这次确实读卡，应由综合者复用指定段落，除非版本/具体结论承重变化，不再安排一次泛读：

- [W0369](../../03_reading/B14/W0369.md)：真实任务与固定词型随机标签控制；先管住probe容量/记忆，不把选择性当部署使用。
- [W0372](../../03_reading/B08/W0372.md)：删除、随机同秩、补标签和后续层恢复的具体反例。
- [W0374](../../03_reading/B08/W0374.md)：正式版独立验证探针、完整性/非目标保真；版本变化不能混拼。不要把“复用”当本轮原文复读。
- [W0530](../../03_reading/B26/W0530.md)、[W0532](../../03_reading/B26/W0532.md)：手术器任意标签能力与限定线性消除；二者不能相互核销。
- [W0534](../../03_reading/B26/W0534.md)＋[W0535](../../03_reading/B26/W0535.md)：幻象构造与回应共同保留；不单边判定所有patch有效/无效。
- [W0192 NoLiMa](../../03_reading/B11/W0192.md)：语义桥接相对字面检索、短/长窗、诱饵；已有材料足够提醒定位与使用混杂。
- [W0061](../../03_reading/B04/W0061.md)、[W0383](../../03_reading/B13/W0383.md)、[W0384](../../03_reading/B14/W0384.md)：复制计数的任务前提、全序列信用边界、簇删的效用与限制。

## 3. 条件触发的已有未读，不默认扩队列

| 何时才需要 | 已有作品／目录锁定原文 | 当前未知与限定 |
|---|---|---|
| “信息能恢复但原生读者学不会”的学习复杂度承重 | W0370，[EMNLP2020 MDL probing PDF](https://aclanthology.org/2020.emnlp-main.14.pdf) | 目录作者Elena Voita、Ivan Titov；本轮未外核、未读正文。要算标签/读出训练成本，不取代因果依赖。 |
| 位置效应是主要竞争解释 | W0191，[Lost in the Middle v3](https://arxiv.org/pdf/2307.03172v3) | 已入储备未读，不算新增。需逐题配对长度/位置控制，不能仅看U形曲线就定机制。 |
| 需要覆盖多事实语义操作而非单针/复制 | W0193，[RULER v3](https://arxiv.org/pdf/2404.06654v3)；W0378，[BABILong v2](https://arxiv.org/pdf/2406.10149v2) | 本轮只核目录/无同名卡，不冒充已读协议。按任务需求选其中一篇先读，不强拉全套基准。 |
| 想用更自然反事实减少状态手术偏移 | W0373，[Naturalistic Causal Probing v2](https://arxiv.org/pdf/2205.07043v2) | 作者、详细构造/适用范围本轮未外核，不凭“naturalistic”免审干预副作用。 |
| 精确patch成本确实阻碍筛选 | N07，[RelP v2](https://arxiv.org/pdf/2508.21258v2) | 摘要已核，全文未读。先用小规模精确干预校准，再评近似；更高相关不能自动修正原始估计目标的偏差。 |

## 4. 每篇阅读的最小交付合同

后续全文读者逐项交付，不以下载、摘要或卡片重述代替阅读：

1. 锁定题名、完整作者、版本日期和公开原文URL；正式版/预印本只作已核范围的关联。
2. 标明输入、查询与反事实答案何时可见；实际模型/数据/训练和测试划分、是否新实体/新模板。
3. 写清干预对象、固定背景、继续重算范围、效应尺度、非目标检查；不只写“做了causal test”。
4. 每条承重结论给页/节/公式或表，保留能反驳自身摘要印象的反例；全文范围和未取得附录分开。
5. 解释回答了四层中的哪一层；额外强读者、金标标签、再训练系统与部署系统分账。
6. 给一条能用于FLUED的有限设计和至少一条不能迁移的前提；不要求存在层级访问、不因无回访淘汰论文。
7. 不运行付费调用或论文训练，不改共享证据表；代码、证明、效果认证与阅读状态分开。

## 5. 阅读后仍必须新实验的部分

文献无法告诉我们当前宿主到底在哪个环节失效。应先选择不改结构的诊断：同源/同卷、原样重放、目标A↔B替换、非目标保真、固定路由/允许重算分报，以及两个候选通道的四格/组干预。再在**不回源的固定压缩态**上比较读者、写入目标、键值绑定、局部路径竞争、精度/容量或额外计算。

若这些简单改变即可恢复目标内容依赖，研究价值成立，不需为了符合多粒度草案而另造导航系统；若只有外部原文权限能救，也要把新增存储/访问权限当独立变量。任何一种结果都不能由一次掉分或一次修复成功直接定责。
