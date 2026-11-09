# T04 R2：摘要遗漏、召回校准与有预算的探索/回退

日期：2026-11-08。任务层级：**发现与摘要初筛，精读交terra**。依据[总计划](../../PLAN.md)和[覆盖审计R1](../../05_review/COVERAGE_AUDIT_R1.md)，先完整读取[384项目录快照](../../02_catalog/CATALOG.md)，再补相邻谱系。

**新增确认30项论文/报告**，与所读CATALOG按题名、原生ID及正式版别名去重无冲突；不自行增加W-ID或修改总数。**29项A（原始摘要及身份），1项P（ConANN额外定向核正文保障对象）；全文精读0、代码核验0、复现0。20项标精读优先。** 实际31次WebSearch（1次429）、40次FetchURL（1次403），逐条见[SEARCH_LOG_R2.md](SEARCH_LOG_R2.md)。数量不是覆盖充分性证明，仍需与其他专题并发扩展再统一去重。

## 0. 审计要求怎样落到本轮

1. **不再把回退接口当空白**：审计已定向确认MemWalker有返回父节点且有纠错使用；ReadAgent有顺序查页和STOP；SSA有学得多级要点及原始KV展开。本轮不重复“是否存在”，转查未知遗漏能否被发现、校准目标、预算与失败条件。
2. **补历史桥接**：2017粗到细句选择、2018学得文档树导航、2019/2020部分可见交互阅读，与近期多粒度访问并列，不用“LLM/RAG不同”避开机制先例。
3. **补另一条最近邻**：Mnemis将相似检索与层级遍历合并；“两个互补入口”本身也不是未有先例。摘要没有建立任意未来问题完备性，官方博客的“无遗漏”表述不作定理背书。
4. **把漏召回拆开**：原始源缺失、表征/评分不识别必要证据、近似索引未取回应有近邻、候选截断、读者未消费，不能共用一个召回指标。T04重点后四类，生命周期问题向T03对接。
5. **来源与语言**：新增正式ACL/PMLR/NeurIPS、数据库与作者机构来源；实际加3条中文机制查询，但结果多为二手资料，不声称已补齐中文正式文献和跨语种评价缺口。
6. **暂缓近期模型**：本轮未继续追V4/V4.1/K3；R1未知项继续未知，不用其作为新增证据承重点。

## 1. 使用口径与机制词

- 每卡给稳定键、作者/年份/版本、原始摘要、全文入口、机制关联、支持/反例潜力及待精读问题。预印本/正式版、标题变更只算同一作品；正式来源只读摘要，不冒充正文已核。
- A/P是本轮实际阅读深度，不是可靠性评分。作者报告的效果/理论主张仍需terra核原假设和结果；不把“统计覆盖”改写为每个问题必然正确。
- ANN（approximate nearest neighbor，近似最近邻搜索）指节省扫描以近似返回给定向量距离下的近邻；**不是语义必要证据的同义词**。IVF（倒排文件向量索引）将向量划为簇，查询只访问部分簇；HNSW（层级可导航小世界图）用多尺度近邻图导航；LSH（局部敏感哈希）使近向量更可能进入相同桶。
- 共形预测指用校准样本构造有统计覆盖的集合；共形风险控制指校准给定损失的期望风险。分布无关不表示无需可交换性或不受自适应查询/分布变化影响。保障的准确类型由原文定理决定。
- RAG＝检索增强生成；KV＝注意力键/值状态；oracle＝实验中有额外正确答案/完整源权限的理想参照，不作为部署可用触发器。下文“摘要失明”是中文问题简称，不注册新项目术语。

## 2. 新增候选卡

### R2-001｜精读优先｜Learning to Search in Long Documents Using Document Structure
- **稳定键**：`acl:C18-1014`；别名arXiv:1806.03529v2。Mor Geva、Jonathan Berant；2018，COLING2018，v2备注为camera-ready后加致谢。
- **原始摘要**：[ACL](https://aclanthology.org/C18-1014/)；**全文入口**：[正式PDF](https://aclanthology.org/C18-1014.pdf)。**深度A**。
- **机制/关联**：文档表示为树，代理学习在快速树导航与昂贵答案抽取之间交错；以基于DQN（深度Q学习）的训练节点采样鼓励探索。
- **支持/反例潜力**：直接补学得文档导航的早期先例；摘要还报告与强检索基线集成继续改善，说明树导航和独立检索可能互补，不能只跟弱平层模型比。
- **待核**：节点可见内容、动作/回溯、训练探索与部署探索是否相同？答案监督是否同时教会“查哪里”和“何时停”？同源权限与总阅读成本下集成增益从何而来？

### R2-002｜精读优先｜Coarse-to-Fine Question Answering for Long Documents
- **稳定键**：`acl:P17-1020`；别名arXiv:1611.01839v2，Atom题名为Hierarchical Question Answering for Long Documents。Eunsol Choi、Daniel Hewlett、Jakob Uszkoreit、Illia Polosukhin、Alexandre Lacoste、Jonathan Berant（正式版顺序）；2016预印本/2017 ACL。
- **原始摘要**：[ACL](https://aclanthology.org/P17-1020/)；**全文入口**：[PDF](https://aclanthology.org/P17-1020.pdf)。**深度A**。
- **机制/关联**：轻量粗模型选句，较贵RNN细读；将句选择视为隐变量，只用答案监督通过强化学习联合训练。
- **支持/反例潜力**：“主任务答案教会选择性细读”已有早期实现；句级固定选择并不等于任意查询可恢复或可靠回退。
- **待核**：选择覆盖/召回与读者能力是否分别报告？未选句得到什么学习信号？是否限制只能选一个证据句，跨句互补何时失败？与全读对比是否相同模型/预算？

### R2-003｜Interactive Machine Comprehension with Information Seeking Agents
- **稳定键**：`acl:2020.acl-main.211`；别名arXiv:1908.10449v3。Xingdi Yuan、Jie Fu、Marc-Alexandre Côté、Yi Tay、Chris Pal、Adam Trischler；2019预印本/2020 ACL。预印本作者栏Christopher Pal与正式版Chris保留版本差别，不计两人/两作。
- **原始摘要**：[ACL](https://aclanthology.org/2020.acl-main.211/)；[arXiv](https://arxiv.org/abs/1908.10449v3)；**全文入口**：[PDF](https://aclanthology.org/2020.acl-main.211.pdf)。**深度A**。
- **机制/关联**：遮蔽大部分文档，以命令逐步揭示局部内容，把静态阅读改成部分可见的序贯信息获取。
- **支持/反例潜力**：适合拆“信息没给”与“模型不知道去哪里看”；是主动读取评价先例，不必先造摘要树才能测试策略。
- **待核**：动作集、有限步数、窥视范围与奖励是什么？能否在无提示线索情况下探索？工具动作成本是否计入效率，停止时是否能判断仍缺证据？

### R2-004｜精读优先｜Mnemis: Dual-Route Retrieval on Hierarchical Graphs for Long-Term LLM Memory
- **稳定键**：`arxiv:2602.15313`，v2（2026-04-10），首版2026-02-17；正式版`2026.acl-long.1096`同作。Zihao Tang、Xin Yu、Ziyu Xiao等；2026。
- **原始摘要**：[正式ACL](https://aclanthology.org/2026.acl-long.1096/)；[arXiv](https://arxiv.org/abs/2602.15313v2)；**全文入口**：[PDF](https://aclanthology.org/2026.acl-long.1096.pdf)。**深度A**。
- **机制/关联**：基础图相似检索，加层级图上的Global Selection（全局选择：有意沿语义层级遍历），组合两路语义/结构相关记忆。
- **支持/反例潜力**：直接针对相似检索无法覆盖全部相关信息；对“平面＋层级旁路”是必须比较的已有组合。成绩不能直接与不同LoCoMo划分横比，亦不能以官方中文解读声称完备。
- **待核**：两个入口各能绕开对方何种漏召回？底层是否保留逐字源；Global Selection是否允许跨父节点、全后代展开和回溯？两路消融有无总调用/读取预算匹配？所谓覆盖是否形式保证、结构可达，还是有限离线结果？

### R2-005｜精读优先｜DRAGIN: Dynamic Retrieval Augmented Generation based on the Information Needs of Large Language Models
- **稳定键**：`arxiv:2403.10081`，v3（2024-09-21）；Weihang Su、Yichen Tang、Qingyao Ai、Zhijing Wu、Yiqun Liu；2024。
- **原始摘要**：[arXiv](https://arxiv.org/abs/2403.10081v3)；**全文入口**：[PDF](https://arxiv.org/pdf/2403.10081v3)。**深度A**。
- **机制/关联**：分别决定何时检索与检索什么，避免只依据最近一句或几个词元构建查询，强调全上下文的实时信息需要。
- **支持/反例潜力**：与既有FLARE形成触发/查询构建对照；摘要的“实时需要”不是直接测到未见证据的保障。
- **待核**：触发器输入和监督究竟是什么？“自信但错误”是否会不检索？将触发改进与查询扩展分开消融后，召回改善来自哪一项？是否可复用于摘要根不含线索的场景？

### R2-006｜精读优先｜SeaKR: Self-aware Knowledge Retrieval for Adaptive Retrieval Augmented Generation
- **稳定键**：`arxiv:2406.19215`，v1；Zijun Yao、Weijian Qi、Liangming Pan等；2024。
- **原始摘要**：[arXiv](https://arxiv.org/abs/2406.19215v1)；**全文入口**：[PDF](https://arxiv.org/pdf/2406.19215v1)。**深度A**。
- **机制/关联**：从模型内部状态估不确定性，高不确定触发检索，并按能降低不确定性的程度重排片段/选择推理策略。
- **支持/反例潜力**：有部署可见的触发信号；但“让模型更确定”的证据可能只是顺从先验而非正确来源，是重要反证轴。
- **待核**：内部状态估计成本、采样次数与校准如何？能否区分知识未知、上下文缺失和证据冲突？错误但降低不确定性的文档能否误导重排？同预算下比固定周期/随机探索强多少？

### R2-007｜Precise Zero-Shot Dense Retrieval without Relevance Labels
- **稳定键**：`arxiv:2212.10496`，v1；Luyu Gao、Xueguang Ma、Jimmy Lin、Jamie Callan；2022预印本，正式版未另核。
- **原始摘要**：[arXiv](https://arxiv.org/abs/2212.10496v1)；**全文入口**：[PDF](https://arxiv.org/pdf/2212.10496v1)。**深度A**。
- **机制/关联**：HyDE（假想文档嵌入）先按问题生成可能含错误细节的伪文档，再编码并在真实语料中检索其近邻；摘要覆盖多任务和sw/ko/ja等语言。
- **支持/反例潜力**：可以先生成桥接语义再定位源，不必仅扩大同一查询的搜索深度；“编码瓶颈过滤错误”是作者解释，不作普适保障。
- **待核**：假想答案对长尾/未知事实会否把检索引向错误簇？多样伪文档能否补召回，额外生成成本多大？跨语种成绩是否在同源权限、同预算下成立？

### R2-008｜Query2doc: Query Expansion with Large Language Models
- **稳定键**：`arxiv:2303.07678`，v2（2023-10-11）；正式版`2023.emnlp-main.585`同作。Liang Wang、Nan Yang、Furu Wei；2023。
- **原始摘要**：[ACL](https://aclanthology.org/2023.emnlp-main.585/)；[arXiv](https://arxiv.org/abs/2303.07678v2)；**全文入口**：[PDF](https://aclanthology.org/2023.emnlp-main.585.pdf)。**深度A**。
- **机制/关联**：少样本提示生成伪文档扩查询，同时增强词法/稠密检索，无需微调。
- **支持/反例潜力**：查询重述/词法旁路是复杂层级控制器必须打败的便宜替代解释；生成词错时可能扩大偏差。
- **待核**：原始查询是否始终保留，错误实体与罕见数字能否被生成覆盖掉？检索改善是定位必要证据还是排名指标？扩查询与直接多路取并集的净成本如何？

### R2-009｜精读优先｜Query Decomposition for RAG: Balancing Exploration-Exploitation
- **稳定键**：`arxiv:2510.18633`，v1；正式版`2026.eacl-long.322`同作。Roxana Petcu、Kenton Murray、Daniel Khashabi、Evangelos Kanoulas、Maarten de Rijke、Dawn Lawrie、Kevin Duh；2025首稿/2026 EACL。
- **原始摘要**：[正式ACL](https://aclanthology.org/2026.eacl-long.322/)；**全文入口**：[PDF](https://aclanthology.org/2026.eacl-long.322.pdf)。**深度A**。
- **机制/关联**：将逐文档获取作为更新子查询效用信念的过程，在继续挖当前子问题和探索另一个子问题之间分配预算，比较多种老虎机式学习方法。
- **支持/反例潜力**：直接补“预算搜索＋探索利用”；正式摘要说最有效相关性估计用排名与人类判断，**不能不核权限就当成零标签部署策略**。
- **待核**：人类判断在训练、离线评价还是在线每步可见？探索收益是否只因更广覆盖、更多调用？奖励是逐文档相关性还是最终答案效用？互补证据单看无价值时是否被过早放弃？

### R2-010｜精读优先｜Stop-RAG: Value-Based Retrieval Control for Iterative RAG
- **稳定键**：`arxiv:2510.14337`，v1；Jaewan Park、Solbee Cho、Jay-Yoon Lee；2025。Atom标NeurIPS2025 **MTI-LLM Workshop**，非主会证明。
- **原始摘要**：[arXiv](https://arxiv.org/abs/2510.14337v1)；**全文入口**：[PDF](https://arxiv.org/pdf/2510.14337v1)。**深度A**。
- **机制/关联**：有限时域决策过程，以完整轨迹的forward-view Q(λ)目标训练价值型检索停止器，而非把当前答案置信度当后续检索收益。
- **支持/反例潜力**：对“继续取源值不值”是直接学习先例；能早停不表示能发现完全不在现轨迹上的分支。
- **待核**：轨迹标签/全宽展开成本、可见金标是什么？学到的是继续既定策略的值，还是替代分支的最优值？部署策略变化、未知预算或错误早停时校准是否保留？

### R2-011｜精读优先｜FrugalRAG: Less is More in RL Finetuning for Multi-Hop Question Answering
- **稳定键**：`arxiv:2507.07634`，v3（2026-02-28）；Abhinav Java、Srivathsan Koundinyan、Nagarajan Natarajan、Amit Sharma；2025首稿/2026更新。v1/v2旧题Learning to retrieve and reason for multi-hop QA，计1项；ICLR2026线索未读正式稿。
- **原始摘要**：[arXiv v3](https://arxiv.org/abs/2507.07634v3)；**全文入口**：[PDF](https://arxiv.org/pdf/2507.07634v3)。**深度A**。
- **机制/关联**：先监督训练广探索子查询策略，再以强化学习按问题难度裁搜索深度，联合奖励正确与节省。
- **支持/反例潜力**：摘要明确反对“越多推理/检索越好”，提供先覆盖后剪枝的训练次序候选；约1000例与检索减半均只作为作者报告。
- **待核**：全探索教师怎样生成、是否拥有答案/支持文档？哪些查询因裁剪而失败？模型/读取/总生成预算一致时仍有优势吗？v1/v3分离了什么新结果，不能混引。

### R2-012｜精读优先｜One Policy, Any Budget: Internalizing Budget-Aware Search via Reinforcement Learning
- **稳定键**：`arxiv:2609.00813`，v1；Xiaowei Sun、Jin Li、Yili Hong、Yikun Fu、Yanghua Xiao；2026-09-01。
- **原始摘要**：[arXiv](https://arxiv.org/abs/2609.00813v1)；**全文入口**：[PDF](https://arxiv.org/pdf/2609.00813v1)。**深度A**。
- **机制/关联**：AnySearch先显式注入预算状态和训练支架，再移去支架，以抽样预算续训；准确率与预算效率组合奖励。
- **支持/反例潜力**：直接考察一个策略跨部署预算，而非每个预算单独训练；可对照固定k和按风险扩读两种设计。
- **待核**：预算是调用数、输入/输出token还是实际延迟？训练外预算如何定义，是否含零/极低预算？奖励是否掩盖困难问题的过早退出？自适应效率权重需什么标签？

### R2-013｜精读优先｜When Knowledge Is Not Free: Cost-Aware Evidence Selection in Retrieval-Augmented Generation
- **稳定键**：`acl:2026.findings-emnlp.413`；DOI原页列`10.18653/2026.findings-emnlp.413`（缺常见v1段，照录不擅修）。Mingyan Wu、Han Yang、Omer Ben-Porat、Yftah Ziser；2026，Findings EMNLP。
- **原始摘要**：[ACL](https://aclanthology.org/2026.findings-emnlp.413/)；**全文入口**：[PDF](https://aclanthology.org/2026.findings-emnlp.413.pdf)。**深度A**。
- **机制/关联**：为证据源设置访问成本等级，在显式预算中决定何时检索、访问哪档、何时停。
- **支持/反例潜力**：作者报告没有静态选择器普遍占优，更多预算也不稳定改善；代理表现模型/任务依赖。补“原源不免费”的直接反方，而不是仅看推理FLOPs。
- **待核**：成本层级是否真实许可/延迟测量，还是人工访问摩擦代理？源质量/领域匹配与成本有没有混淆？预算增长引入噪声还是策略失配？如何迁移到SSD/重编码成本？

### R2-014｜精读优先｜TRAQ: Trustworthy Retrieval Augmented Question Answering via Conformal Prediction
- **稳定键**：`arxiv:2307.04642`，v2（2024-04-05）；正式版`2024.naacl-long.210`同作。Shuo Li、Sangdon Park、Insup Lee、Osbert Bastani；2023首稿/2024 NAACL。
- **原始摘要**：[ACL](https://aclanthology.org/2024.naacl-long.210/)；[arXiv](https://arxiv.org/abs/2307.04642v2)；**全文入口**：[正式PDF](https://aclanthology.org/2024.naacl-long.210.pdf)。**深度A**。
- **机制/关联**：分别构造检索器/生成器预测集合并组合，用贝叶斯优化缩小集合，目标是语义正确答案在集合内的统计覆盖。
- **支持/反例潜力**：保障是“集合包含正确响应”，不等于单个最终答案必对、不等于全部必要证据召回。可改变是否选择风险受控的多候选回退。
- **待核**：校准样本是否需要正确文档/答案，全库比较与候选截断怎样处理？边际/条件覆盖是哪一种？何时集合大到超读取预算，截断后保证还剩什么？语义等价判定谁提供？

### R2-015｜精读优先｜C-RAG: Certified Generation Risks for Retrieval-Augmented Language Models
- **稳定键**：`arxiv:2402.03181`，v5（2024-07-30）；正式版`pmlr:v235/kang24a`同作。Mintong Kang、Nezihe Merve Gürel、Ning Yu、Dawn Song、Bo Li；2024，ICML/PMLR235:22963–23000。
- **原始摘要**：[PMLR](https://proceedings.mlr.press/v235/kang24a.html)；**全文入口**：[PDF](https://raw.githubusercontent.com/mlresearch/v235/main/assets/kang24a/kang24a.pdf)。**深度A**。
- **机制/关联**：对生成风险给上置信界，并讨论何种检索器/Transformer条件下RAG比单一模型风险低，含分布变化下有界风险的理论主张。
- **支持/反例潜力**：不是“检索必然降风险”的无条件定理，也不是逐查询漏召回报警器。**C-RAG与已收CRAG（Corrective Retrieval Augmented Generation）不同作**，按ID分开。
- **待核**：non-trivial质量条件具体是什么，可部署估计吗？风险函数是否体现必要证据完整性？分布变化允许的范围/已知量是什么？保证生成风险时是否仍可漏掉低概率关键事实？

### R2-016｜精读优先｜CONFLARE: CONFormal LArge language model REtrieval
- **稳定键**：`arxiv:2404.04287`，v1；Pouria Rouzrokh、Shahriar Faghani、Cooper U. Gamble、Moein Shariatnia、Bradley J. Erickson；2024。
- **原始摘要**：[arXiv](https://arxiv.org/abs/2404.04287v1)；**全文入口**：[PDF](https://arxiv.org/pdf/2404.04287v1)。**深度A**。
- **机制/关联**：用知识库内可答问题校准相关片段相似度阈值，推理时取得超过阈值的所有块，而非固定top-k。
- **支持/反例潜力**：非常贴近“检索风险校准”；但“所有超过阈值”可能要求广搜索，阈值之外的ANN漏候选不自动被校准保证吸收。
- **待核**：校准问题是否LLM生成，答案支持标签怎样可靠获得？对互补多块证据是单块命中还是全证据覆盖？ANN先剪或总预算截断时是否重新校准？哪些查询族能满足可交换性？

### R2-017｜精读优先｜CAS: Conformalized Agentic Search via Adaptive Retrieval and Policy Weighting
- **稳定键**：`arxiv:2608.20771`，v1；Zixi Zhu、Jiayuan Su、Jian Zhang、Yu Lin、Hongwei Wang；2026-08-21。
- **原始摘要**：[arXiv](https://arxiv.org/abs/2608.20771v1)；**全文入口**：[PDF](https://arxiv.org/pdf/2608.20771v1)。**深度A**。
- **机制/关联**：检索侧用自适应预测集动态截文档，训练侧用自适应共形推断的置信集合调策略梯度轨迹权重。
- **支持/反例潜力**：将检索候选覆盖与训练可靠性共同处理，是2026年的直接发展；摘要的“guarantees”仍须逐定理核验，自适应训练会否破坏所需统计条件未知。
- **待核**：校准集是否随策略更新、阈值是否看金标答案？检索集合保证覆盖的是支持文档还是排序前缀？一条轨迹筛选/再加权后覆盖怎样变化？预算耗尽时的退出策略可保哪一层风险？

### R2-018｜Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs
- **稳定键**：`arxiv:1603.09320`，v4（2018-08-14）；Yu. A. Malkov、D. A. Yashunin（按元数据缩写，不由提交人字段扩名）；2016首稿/2018修订，正式版关联本轮未单独核。
- **原始摘要**：[arXiv](https://arxiv.org/abs/1603.09320v4)；**全文入口**：[PDF](https://arxiv.org/pdf/1603.09320v4)。**深度A**。
- **机制/关联**：随机层级的多尺度近邻图，从上层导航到细层；是强平层向量检索实际上可能已含索引层级的经典基线。
- **支持/反例潜力**：不能把“多级导航对线性扫描快”当作充分系统优势；摘要的对数缩放不能当所有数据最坏情况保证，需配027。
- **待核**：搜索宽度、内存与召回如何共同变化？所称robust是否平均经验性质？层级是空间尺度而非语义摘要，迁移到来源关系时哪些性质不再成立？

### R2-019｜DiskANN: Fast Accurate Billion-point Nearest Neighbor Search on a Single Node
- **稳定键**：`neurips:2019/09853c7fb1d3f8ee67a61b6bf4a7f8e6`；Suhas Jayaram Subramanya、Fnu Devvrit、Harsha Vardhan Simhadri、Ravishankar Krishnawamy、Rohan Kadekodi（出版社网页原拼写，姓名规范待编目核PDF）；2019 NeurIPS。
- **原始摘要**：[NeurIPS](https://papers.nips.cc/paper_files/paper/2019/hash/09853c7fb1d3f8ee67a61b6bf4a7f8e6-Abstract.html)；**全文入口**：[PDF](https://papers.nips.cc/paper_files/paper/2019/file/09853c7fb1d3f8ee67a61b6bf4a7f8e6-Paper.pdf)。**深度A**。
- **机制/关联**：SSD索引与Vamana近邻图，使大规模高召回检索不必全部驻内存。
- **支持/反例潜力**：原源外置/分层存储的成熟强对照；单机低内存、高吞吐是作者指定数据/硬件结果，不是外源回访恒成本证明。
- **待核**：压缩代理、图、完整向量分别存哪里？冷访问/随机SSD I/O、建图与维护代价如何？其近邻召回能否保护真实任务证据？配027核“快/慢预处理”版本差异。

### R2-020｜Accelerating Large-Scale Inference with Anisotropic Vector Quantization
- **稳定键**：`arxiv:1908.10396`，v5；正式版`pmlr:v119/guo20h`同作。Ruiqi Guo、Philip Sun、Erik Lindgren、Quan Geng、David Simcha、Felix Chern、Sanjiv Kumar；2019首稿/2020 ICML。
- **原始摘要**：[PMLR](https://proceedings.mlr.press/v119/guo20h.html)；**全文入口**：[PDF](https://proceedings.mlr.press/v119/guo20h/guo20h.pdf)。**深度A**。
- **机制/关联**：各向异性向量量化，惩罚与高内积查询更相关的残差方向，而非只最小化重建距离；与ScaNN索引实现关联，不另计一个系统作品。
- **支持/反例潜力**：压缩保真目标应面向排序效用的经典先例；低表示重建误差不等于路由召回好。
- **待核**：查询分布的统计假设、量化学习和任务语义差距是什么？与普通PQ同位预算时高分尾部召回怎样？注意力查询—键分布不一致会否破坏其适用假设？

### R2-021｜Multi-probe LSH: Efficient indexing for high-dimensional similarity search
- **稳定键**：`vldb:2007/p950-lv`；Q. Lv、W. Josephson、Z. Wang、M. Charikar、K. Li（机构书目缩写）；2007，VLDB pp.950–961。
- **原始摘要**：[Princeton机构书目](https://collaborate.princeton.edu/en/publications/multi-probe-lsh-efficient-indexing-for-high-dimensional-similarit/)；**全文入口**：[VLDB公开PDF](https://www.vldb.org/conf/2007/papers/research/p950-lv.pdf)。**深度A**。
- **机制/关联**：不只命中一个哈希桶，而是有序探查多个可能相关桶，以较少表换取更多有针对性的探测。
- **支持/反例潜力**：多入口扩搜/空间—时间—召回折衷早有明确先例；概率近邻保障不等于语义查漏保障。
- **待核**：探测次序如何估计命中概率，预算用尽后剩余漏召回可否量化？与增加独立表相比何时更划算？其度量/独立性假设迁移到学得索引后是否保留？

### R2-022｜精读优先｜Improving Approximate Nearest Neighbor Search through Learned Adaptive Early Termination
- **稳定键**：`doi:10.1145/3318464.3380600`；Conglong Li、Minjia Zhang、David G. Andersen、Yuxiong He；2020 SIGMOD，pp.2539–2554。
- **原始摘要**：[作者机构CMU](https://www.pdl.cmu.edu/PDL-FTP/BigLearning/mod0246-liA_abs.shtml)；**全文入口**：[公开PDF](https://www.pdl.cmu.edu/PDL-FTP/BigLearning/mod0246-liA.pdf)。**深度A**。
- **机制/关联**：利用搜索中间结果等运行时特征，梯度提升树按查询预测何时停止；同精度目标下减少总搜索。
- **支持/反例潜力**：直接先例：不必复杂神经导航器，轻量进度特征就可能改善预算；“同平均精度”未必保护困难查询。
- **待核**：训练标签是否需要精确全量近邻，收集成本多少？运行时特征有没有重复全局计算？误停后有没有恢复路径？在语义分布漂移、缓存冷热和新查询族中如何校准？

### R2-023｜Tao: A Learning Framework for Adaptive Nearest Neighbor Search using Static Features Only
- **稳定键**：`arxiv:2110.00696`，v1；Kaixiang Yang、Hongya Wang、Bo Xu、Wei Wang、Yingyuan Xiao、Ming Du、Junfeng Zhou；2021。
- **原始摘要**：[arXiv](https://arxiv.org/abs/2110.00696v1)；**全文入口**：[PDF](https://arxiv.org/pdf/2110.00696v1)。**深度A**。
- **机制/关联**：先从查询预测局部内在维数，再预测所需搜索终止条件，不依赖搜索运行时特征。
- **支持/反例潜力**：与022构成“先估难度”vs“边搜边估进度”的直接竞争解释；静态难度容易漏掉当前源/摘要状态变化。
- **待核**：局部内在维数的标签/预测是否有额外全量访问？静态模型能否适应新增记忆、索引重建或后续改题？同目标召回的尾部风险与在线特征法有何差异？

### R2-024｜ProS: Data Series Progressive k-NN Similarity Search and Classification with Probabilistic Quality Guarantees
- **稳定键**：`arxiv:2212.13310`，v1；Karima Echihabi、Theophanis Tsandilas、Anna Gogolou、Anastasia Bezerianos、Themis Palpanas；2022原文/线上，VLDBJ后续卷期与DOI`10.1007/s00778-022-00771-z`仅检索关联，本轮未另核出版页。
- **原始摘要**：[arXiv](https://arxiv.org/abs/2212.13310v1)；**全文入口**：[PDF](https://arxiv.org/pdf/2212.13310v1)。**深度A**。
- **机制/关联**：对欧氏/动态时间规整数据序列的逐渐改进近邻结果估最终质量并决定停止，有概率质量主张。
- **支持/反例潜力**：逐步访问＋进度估计不是新问题；适用域是数据序列度量，不应未经验证套到语义向量或多跳证据。
- **待核**：概率界条件、校准/学习样本、是否需要确切最近邻完成标签？保证的是距离、召回还是分类结果？在长尾/非平稳查询下能否主动扩搜而不失标称风险？

### R2-025｜精读优先｜DARTH: Declarative Recall Through Early Termination for Approximate Nearest Neighbor Search
- **稳定键**：`arxiv:2505.19001`，v2（2025-08-18）；DOI`10.1145/3749160`关联同作。Manos Chatzakis、Yannis Papakonstantinou、Themis Palpanas；2025首稿；Atom标SIGMOD2026，正式差异未读。
- **原始摘要**：[arXiv](https://arxiv.org/abs/2505.19001v2)；**全文入口**：[PDF](https://arxiv.org/pdf/2505.19001v2)。**深度A**。
- **机制/关联**：用用户给定召回目标而非算法专有超参控制ANN搜索，通过自适应提前终止避免简单问题过度搜索。
- **支持/反例潜力**：非常贴近“按风险/召回而非按固定k分预算”；摘要的目标达成是经验报告，未核为逐查询理论保证。
- **待核**：声明召回如何在不知道真近邻时估算？目标是均值、分位数还是每查询？困难问题持续失准怎么办？与ConANN保障范围、校准/训练成本、索引适用范围如何不同？

### R2-026｜精读优先｜ConANN: Conformal Approximate Nearest Neighbor Search
- **稳定键**：`doi:10.14778/3772181.3772184`；Sonia Horchidan、Fabian Zeiher、Henrik Boström、Paris Carbone。PVLDB19(1):29–42；Crossref列印刷2025-09、在线2026-01-08，会议程序2026，分列不强行消歧。
- **原始摘要/全文入口**：[PVLDB公开PDF](https://www.vldb.org/pvldb/vol19/p29-horchidan.pdf)；[Crossref身份/日期](https://api.crossref.org/works/10.14778/3772181.3772184)。**深度P：摘要＋§2.2/§3.1及§5.1.3保障对象，非精读**。
- **机制/关联**：对IVF逐簇探测的中间结果校准停止阈值，使用共形风险控制约束相对精确近邻集合的错误；不必逐查询固定探测数。
- **支持/反例潜力**：已不是“完全没有召回校准方法”。但§3.1目标明确为**跨查询期望FNR（漏检率）**；§5.1.3也区分其平均FNR与另一方法最大FNR。不能写成任何困难查询均达标，更不能替必要语义证据校准背书。
- **待核**：可交换性/查询分布假设、正则化与阈值单调性、重复停步是否保持保证？校准需精确近邻的全扫成本多少？层级语义摘要漏掉概念时，ANN层校准是否根本无从触及？分布变化/索引更新/硬预算截断是否要重校？

### R2-027｜精读优先｜Worst-case Performance of Popular Approximate Nearest Neighbor Search Implementations: Guarantees and Limitations
- **稳定键**：`arxiv:2310.19126`，v1；Piotr Indyk、Haike Xu；2023。Atom标NeurIPS2023，正式版差异未核。
- **原始摘要**：[arXiv](https://arxiv.org/abs/2310.19126v1)；**全文入口**：[PDF](https://arxiv.org/pdf/2310.19126v1)。**深度A**。
- **机制/关联**：给出图ANN特定版本的条件性保证及困难实例；慢预处理DiskANN在有界内在维数下可有多对数查询，若干快预处理/HNSW/NSG变体存在达合理精度需线性步骤的实例。
- **支持/反例潜力**：直接限制“层级/图索引天然对数且可靠”的宽泛主张；不能反过来把构造性最坏情况当自然语料一定线性。
- **待核**：困难实例对距离/维度/建图/随机性的要求是什么？近似比与Recall@k如何关联？构建成本、搜索宽度的哪一部分换来了保证？实际任务可否检测进入困难区？

### R2-028｜精读优先｜Towards Robustness: A Critique of Current Vector Database Assessments
- **稳定键**：`arxiv:2507.00379`，v2（2026-04-02）；Zikai Wang、Qianxi Zhang、Baotong Lu、Qi Chen、Cheng Tan；2025首稿/2026修订。
- **原始摘要**：[arXiv](https://arxiv.org/abs/2507.00379v2)；**全文入口**：[PDF](https://arxiv.org/pdf/2507.00379v2)。**深度A**。
- **机制/关联**：Robustness-δ@K量达某召回阈值的查询比例，而非只看平均召回；研究相同平均召回下的下游任务差异。
- **支持/反例潜力**：为“平均召回守住却少数问题彻底漏”的风险提供可操作评价；和026的期望风险形成必要互补，不等于新保证本身。
- **待核**：RAG证据/问答集、查询难度与模型差异如何控制？尾部召回与最终质量是否因果而非相关？若目标改为覆盖率或极端低召回比例，各索引/控制器排名会否反转？

### R2-029｜Efficient query evaluation using a two-level retrieval process
- **稳定键**：`doi:10.1145/956863.956944`，Crossref另给别名`10.1145/956943.956944`。Andrei Z. Broder、David Carmel、Michael Herscovici、Aya Soffer、Jason Zien；CIKM2003 pp.426–434。
- **原始摘要**：[IBM Research](https://research.ibm.com/publications/efficient-query-evaluation-using-a-two-level-retrieval-process)；[Crossref身份](https://api.crossref.org/works/10.1145/956863.956944)；**全文入口**：[出版方PDF](https://dl.acm.org/doi/pdf/10.1145/956863.956944)（本轮未取）。**深度A**。
- **机制/关联**：WAND（Weak AND，弱合取检索算子）以廉价部分评分筛候选，再完整求精确分数，允许按分配时间控制裁剪。
- **支持/反例潜力**：两阶段筛选/验证和预算控制的早期先例。原摘要报告大幅少算且几乎不损召回，**不能只凭该摘要给全部WAND设置零漏召回保证**。
- **待核**：精确/近似阈值模式如何区分，哪些评分可分解为安全上界？其“完整评分”只保证排序函数不是任务证据，怎样与后来的语义路由公平对照？

### R2-030｜精读优先｜Faster Top-k Document Retrieval Using Block-Max Indexes
- **稳定键**：`doi:10.1145/2009916.2010048`；Shuai Ding、Torsten Suel；SIGIR2011 pp.993–1002。
- **原始摘要/全文入口**：[作者NYU公开PDF](https://research.engineering.nyu.edu/~suel/papers/bmw.pdf)；出版页[DOI](https://doi.org/10.1145/2009916.2010048)本轮Fetch403。**深度A：首页作者/年份/摘要，未精读算法**。
- **机制/关联**：Block-Max索引为压缩倒排块保存最大贡献上界，使未解压内容也可被安全跳过；摘要明确目标是与穷举析取查询返回相同结果。
- **支持/反例潜力**：不是所有粗代理筛选都必然漏掉原评分top-k；**可证上界与学习语义摘要不是一回事**，提供可证候选过滤的强基线/对照思想。
- **待核**：安全性的评分可分解/非负/上界条件有哪些，维护成本与紧度如何？学习摘要是否能同时提供语义索引与不漏关键键的界？精确保持BM25 top-k仍可能漏语义必要事实，这个剩余缺口怎样测？

## 3. 改变架构选择的具体问题，而非模块愿望清单

以下是待全文/后续研究裁定的问题。本轮不运行实验、不改默认、不把建议写成已有结果。

### D1：瓶颈是近似索引，还是地址表征根本没有给必要证据高分？

- **竞争解释**：相同表示的精确扫描可找到必要证据，但ANN过早停/粗簇漏选；或者精确扫描也把不相关内容排前，因为摘要/查询不能表达必要关联。
- **最低成本判别**：对固定公开检索任务、固定表示和读者，用精确评分、ANN、oracle证据位置三种既有结果/离线索引对比；分别报近邻集合召回、金标证据召回、全证据集完整命中和条件于证据正确的答案表现。
- **会改变什么**：前者优先改搜索宽度/动态探测/索引；后者增加ef/nprobe或ConANN校准不够，应改地址表示、生成桥接查询、词法旁路或常驻重要信息。主要伴读026/028、007/008、R1 InMind/NoLiMa。

### D2：需要“任务摘要”，还是“可搜索的上界/多向量地址”，两者必须同槽吗？

- **竞争解释**：任务摘要擅长整体理解却遗漏未来数字/否定例外；服务于搜索的多向量/最大值/词法统计更能保存检索入口，不必承担值内容的全部保真。
- **最低成本判别**：全文先提取020、021、030、R1 Quest/ColBERT/SSA的地址与载荷独立存储权限；再设计同总字节、同原始源保留权的候选表：摘要地址、多向量地址、词法/统计旁路，读出器不变。
- **会改变什么**：若便宜地址旁路已补核心漏召回，未必先做更深摘要树；若需界的前提不适用于语义必要性，就不能以数学保top-k声称任务充分。

### D3：回退触发器能否发现“自信且漏证据”，而不先看答案或全源？

- **竞争解释**：模型低置信只是难题指标；错误片段也可降低不确定性；真正有价值的触发应预示继续探索的边际收益或缺证概率。
- **最低成本判别**：在相同已有读取轨迹上，比较不确定性触发、Stop-RAG式继续值、证据冲突/不足判断、固定预算和强制少量独立探索；不得给部署触发器看金标。用oracle后续收益只做离线标签/上界，标签成本单列。
- **会改变什么**：如果控制器不能在同总读取成本下降低漏证据尾部，保留简单固定覆盖/全量升级，不优先加复杂效用头。005/006/010/022及R1 CRAG/Self-Route是必须比较而非重新发明的策略。

### D4：平均风险达标，是否允许少数问题完全失守？

- **竞争解释**：ConANN等边际/期望风险控制已满足目标；但研究任务要求每类查询或高风险例外也有可接受召回。
- **最低成本判别**：terra逐原定理写清概率对谁取、损失定义、校准/测试的可交换性、条件覆盖与最坏情况；同结果同时报均值、达δ召回的查询比例、全证据集完整命中、最差查询族，并用罕见例外/换题/长度增长挑战。
- **会改变什么**：若只可保证平均，不得称“模型会可靠自检遗漏”；可以采用风险受控但明确有限适用域的升级路径，或固定保留高风险事实可见性。014/015/016/017/025/026/028形成不同保障对象，不能混引。

### D5：有校准的回退能否承受硬预算，以及多级选择如何合成风险？

- **竞争解释**：统计保证靠自动变大的集合/更多簇实现；部署硬上限会重新裁断该集合。层级每一步局部达标也不自动保证整条来源路径达标。
- **最低成本判别**：读014/016/017/026的集合大小分布、最大成本、预算溢出处理；对每级错剪事件与最终证据遗漏分开建账，不能把相关阶段的边际覆盖率直接相乘。仅当各阶段保障确实适用于同一部署分布和事件定义时才讨论有效联合界。
- **会改变什么**：若保障频繁超预算，需改变目标（拒答/转人工/延迟读取）、保留可扩上限或限定查询域；不能将校准层接在固定k后面就宣称获得端到端保障。

### D6：探索应跨语义分支，还是继续加深当前结果列表？

- **竞争解释**：沿当前摘要分支多读可以补证；或初始路线已经错，继续加深只巩固错误，必须换查询、词法入口、兄弟分支或独立图路线。
- **最低成本判别**：用009及004的实际策略/消融，固定证据预算比较“加深”“新子查询”“独立入口并集”；将必要多源互补题和单源细节题分开。人类相关性反馈若在线可见，另列oracle，不与无标签策略直接比。
- **会改变什么**：若跨入口比树深重要，首版优先强平层检索＋局部结构调粒度，而非严格自上而下唯一入口；若同预算树导航能稳定找到互补证据，再保留层级控制。001/003也提供无需LLM记忆树的早期学习对照。

### D7：更少工具调用是否真的更便宜，更大预算是否真的更好？

- **竞争解释**：少调用节省开销；但一个更宽检索/更长自我推理/全源重编码可能更慢；相反更多读取可能带噪声而降准确。
- **最低成本判别**：012/013/019/022/023/025配T06，全账分索引构建、校准金标、存储副本、冷/热I/O、解压/重编码、生成token、总墙钟与尾延迟；单问与多问摊销分列。成本模型中的付费等级、调用数和SSD字节不视为可互换。
- **会改变什么**：若只在热缓存/重复查询才有净收益，限制适用场景；若静态轻量预测已匹配进度控制，不优先训练复杂控制器；若强预算迁移有效才考虑可调预算统一策略。

## 4. 推荐terra小批精读顺序（20项，不是配额）

| 组 | 优先ID | 必须交回的原文证据 |
|---|---|---|
| A 最近邻与旧机制 | 001、002、004 | 选择/导航/回退动作、节点可见信息、原始源保留、答案监督/探索奖励；Mnemis两路消融；接审计已有MemWalker/ReadAgent而不重复问已证存在性 |
| B 触发与预算 | 005、006、009、010、011、012、013 | 触发/继续值的部署可见输入，标签/教师权限；人类判断位置；硬预算/费用定义；自信漏证据失败；训练/部署预算变更 |
| C 不同保障对象 | 014、015、016、017、025、026 | 原定理/算法/校准集字段；召回vs生成风险vs答案集合；边际/期望/条件保证；分布/策略漂移与候选先剪/预算后截后还剩什么 |
| D 强索引与反例 | 022、027、028、030 | 精确近邻/给定评分的top-k和语义证据之别；静态/运行特征；最坏情况实例条件；尾部指标、索引/标签/冷访问成本 |

储备010的正式会场为workshop，不以主会权重对待；不是按会场排除，而是对理论/效果强主张额外核证。023/024可在022/025/026精读时按引用定向补读，018—021作强基线背景，不要求全都先全文读完。

## 5. 剩余缺口、停止规则与交接边界

- 这30项足以改变“无可靠回退相关工作”和“ANN成本可忽略”的初始认识，但尚不能证明校准已解决摘要语义失明。
- **中文/跨语种仍薄**：只补了中文检索入口，未得到本轮独立确认的中文正式原作；HyDE摘要有多语结果，不替中文罕见数字、实体别名、跨语种源回访的内容特异证据作证。
- **源更新与自适应分布**：查询向量分布随生成/索引更新/层级改写变化时，标准校准假设能否保留仍是核心缺口；没有从摘要推断已解决。
- **非短视互补**：009/010/011不等于已实现严格动作反事实终局效用；对接T07核标签、完整轨迹成本及策略变化。单步相关性与整组证据必要性仍分开。
- **统计保障需原文审**：尤其ConANN正则化、停止规则、有限样本校准和期望对象；CAS的自适应训练与覆盖保证；C-RAG的分布变化范围。本文没有验定其证明正确。
- **近期模型不耗死**：不重新背书V4/V4.1/K3，不把R1的未读报告判为不存在。只有明确涉及源生命周期、可回退索引或完整成本的新原文才重开。
- 建议下一轮**先读上述批次再定向扩展**，不是为了达到500/2000加标题。若新增只重复固定top-k＋代理置信度、不能改变D1—D7，则停止该族；若有逐查询/查询族风险、硬预算回退、动态查询下召回保证的新证据，则继续追。

## 6. 静态验收与未执行项

只验证报告可追溯结构，不运行代码构建/项目测试，因为没有代码变更。验收对象为：30个R2 ID连续无重复；29A/1P；20优先项；每卡有稳定键、原始摘要与全文入口；主/别名ID与所读384项目录零重叠；日志31查询/40访问；UTF-8无替代字符；局部文件状态。未下载模型、未训练、未做全文精读或代码复现；未改CATALOG、审计文件、原R1卡或任何现有证据表。

**实际静态验收PASS**：只读Python确认30卡连续、20优先、29A/1P、每卡四类必备字段齐全，23个arXiv主/别名与384行CATALOG无重叠，日志31查询/40访问，UTF-8无替代字符；此前正式ID/DOI别名及题名Grep也零重叠。局部Git状态只有T04的5份未跟踪Markdown，其中3份为保留的R1文件、本轮仅新增`EXPANSION_R2.md`和`SEARCH_LOG_R2.md`。未生成脚本、测试输出或训练文件；C-RAG全文入口使用正式页面实际给出的公开PDF地址，未将链接存在当下载/精读完成。
