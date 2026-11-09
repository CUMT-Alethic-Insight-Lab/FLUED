# T02 候选作品：压缩、充分性、未知查询与多粒度能力边界

日期：2026-11-08。去重确认52件；精读优先P1共27件；全文精读0件。ID为本专题稳定本地标识，跨专题去重请使用arXiv号、正式作品URL或DOI，不要用本地ID计全局数。

## 阅读口径

- **A**：已实际取得原始作品摘要/出版方介绍，并核对题名或稳定标识。即使工具返回整篇PDF/HTML，也不代表全文精读。以下52件均按A计；少量顺手定位正文位置在卡内明示。
- **P1**：建议terra下一轮精读，不代表已精读或已验证结论。具体问题见 `HANDOFF.md`。
- 每卡“支持/反例潜力”只是摘要层研究线索；作者报告的实验效果、定理概述与我们的迁移推断分开写。未核定的定理假设不补猜。
- 作者栏“—”表示本次原始页面抽取缺失作者元数据，留待补全；不把arXiv的提交人当作者。部分首作者只由搜索元数据取得，明确标注，正式引用仍需核对完整名单。
- arXiv全文链接是下一轮入口，不表示本轮下载/通读过；正式发表身份只在已出现明确来源时登记，未明者保留预印本身份。

## 本目录内使用的公共术语锚

信息瓶颈（Information Bottleneck，IB）：给定相关目标变量，在压缩输入信息与保留目标信息间求权衡。任务充分性：给定任务、分布和损失，表示保留达到原输入最佳决策所需的信息。逐级细化（successive refinement）：先给粗码，再给增量细码，研究各级能否同时达到各自最优率失真点。统计试验比较/Blackwell序：通过任意决策任务的最佳风险比较观测通道。信息亏损（deficiency）：以另一个通道模拟目标通道时的不足及相应风险差。单槽/多槽：一份输入经一个/多个可分别读取的向量表示；必须同时说明总维度、位宽和读取规则。来源回访：保留原始项并在查询时重新读取，不能与从有损码重建混同。

## I. 已核验候选（按发现顺序；非质量排名）

### T02-001 — Minimal Achievable Sufficient Statistic Learning [P1]
- 身份：2019；Milan Cvitkovic、Günther Koliander；ICML/PMLR97:1465–1474。原始来源及稳定ID：[PMLR cvitkovic19a](https://proceedings.mlr.press/v97/cvitkovic19a.html)。深度：A（正式摘要）。
- 机制关联：把“最小充分”限定在可优化函数类，提出适用于确定连续映射的Conserved Differential Information（保守微分信息，作者提出的替代信息量）。
- 支持/反例潜力：支持把可实现读出能力写入充分性定义；反对用抽象最小充分统计量直接证明任意网络可学。摘要只声称目标极小值的性质，不是任意优化轨迹保证。
- 全文入口：[PDF](https://proceedings.mlr.press/v97/cvitkovic19a/cvitkovic19a.pdf)。下一步：核定可达函数类、全局极小值、连续变量条件。

### T02-002 — The Variational Deficiency Bottleneck [P1]
- 身份：2018首发，2020 v3/IJCNN；作者：—；[arXiv:1810.11677](https://arxiv.org/abs/1810.11677)，页面关联正式DOI [10.1109/IJCNN48605.2020.9206900](https://doi.org/10.1109/IJCNN48605.2020.9206900)。深度：A。
- 机制关联：用通道信息亏损而不是仅互信息构造瓶颈；摘要给出最佳决策风险差的操作含义，分类是特例。
- 支持/反例潜力：适合比较未知任务族下“表示还能做什么”；变分上界及单次Monte Carlo时与VIB重合，不应将估计目标当真实亏损或部署性能。
- 全文入口：[PDF](https://arxiv.org/pdf/1810.11677)。下一步：核定风险族、亏损方向、随机模拟器和近似误差。

### T02-003 — Lossy Compression for Lossless Prediction [P1]
- 身份：2021/NeurIPS2021，2022 v5；Yann Dubois等（检索元数据；完整作者待补）；[arXiv:2106.10800](https://arxiv.org/abs/2106.10800)。深度：A。
- 机制关联：刻画对一组变换不变的所有预测任务保持高性能所需码率，进而设计无监督神经压缩目标。
- 支持/反例潜力：这是未知下游任务仍可压缩的强正面邻居，但任务族受不变性约束；摘要的图像分类结果不证明任意文本查询无损。关键不是“未知”二字，而是预先知道哪些差异永不相关。
- 全文入口：[PDF](https://arxiv.org/pdf/2106.10800)。下一步：核定任务族、变换轨道/不变量和最优码率假设。

### T02-004 — Zoology: Measuring and Improving Recall in Efficient Language Models
- 身份：2023首发，2024 ICLR相关正式入口见检索；Simran Arora等（检索元数据）；[arXiv:2312.04927](https://arxiv.org/abs/2312.04927)。深度：A。
- 机制关联：多查询关联回忆（MQAR，即同一上下文出现多个键值查询的合成任务）区分注意力与门控卷积，兼有自然语言关联回忆分析。
- 支持/反例潜力：提示查询数量、键值分布与输入依赖读出很重要；不能把特定合成任务或参数效率比较推广为所有递归模型、所有压缩任务的不可学。
- 全文入口：[PDF](https://arxiv.org/pdf/2312.04927)。下一步：区分表达下界、训练失败与评测构造；与T05去重交叉阅读。

### T02-005 — Repeat After Me: Transformers are Better than State Space Models at Copying [P1]
- 身份：2024，v2 2024-06-03；Samy Jelassi、David Brandfonbrener、Sham M. Kakade、Eran Malach（检索元数据）；[arXiv:2402.01032](https://arxiv.org/abs/2402.01032)。深度：A。
- 机制关联：固定大小潜状态在上下文复制上的理论与实验限制；与能回访输入位置的两层注意力构造比较。
- 支持/反例潜力：支撑有限容量状态与来源回访不是同一能力；必须精读精度、序列长度、误差及状态位数条件。表达构造和经验效果分开，不由“有路径”推出“学会使用路径”。
- 全文入口：[PDF](https://arxiv.org/pdf/2402.01032)。下一步：逐字核定GSSM模型类及上下界规模。

### T02-006 — Deep Variational Information Bottleneck
- 身份：2016首发，2017会议版本线索，2019 v7；Alexander A. Alemi等（S02/S31引用元数据）；[arXiv:1612.00410](https://arxiv.org/abs/1612.00410)。深度：A。
- 机制关联：IB变分近似、神经参数化和重参数化训练；摘要报告正则化、泛化和对抗鲁棒性。
- 支持/反例潜力：给理论目标如何变成训练损失的桥梁；不能把变分目标下降、KL正则或实测分类性能等同于精确充分性，更不等同于未知查询充分。
- 全文入口：[PDF](https://arxiv.org/pdf/1612.00410)。下一步：分开真实互信息、变分界、优化所得和测试性能。

### T02-007 — The Information Bottleneck Method [P1]
- 身份：1999工作/2000 arXiv上传；Naftali Tishby、Fernando C. Pereira、William Bialek（作者公开稿检索）；[arXiv:physics/0004057](https://arxiv.org/abs/physics/0004057)。深度：A。
- 机制关联：给定联合分布X,Y，短码保留关于目标Y的相关信息；自洽编码方程和迭代求解。
- 支持/反例潜力：核心前提是先定义何为相关目标；不能将“对Y充分”换成“对任何后来查询充分”。码率/互信息不是自动的槽数、显存或延迟量。
- 全文入口：[作者PDF](https://www.princeton.edu/~wbialek/our_papers/tishby+al_99.pdf)、[arXiv PDF](https://arxiv.org/pdf/physics/0004057)。下一步：核定源/目标、编码随机性、目标约束和操作解释。

### T02-008 — Caveats for Information Bottleneck in Deterministic Scenarios [P1]
- 身份：2018首发，2019 v4；Artemy Kolchinsky、Brendan D. Tracey、Steven Van Kuyk（检索元数据）；[arXiv:1808.07593](https://arxiv.org/abs/1808.07593)。深度：A。
- 机制关联：Y是X确定函数时，通常IB拉格朗日扫描不能恢复整条曲线，并存在平凡解及多层压缩解释问题。
- 支持/反例潜力：直接反对“压得更少、目标信息越多就能解释层级学习”的泛化。注意是确定标签情形，不是对一切IB用途否定。
- 全文入口：[PDF](https://arxiv.org/pdf/1808.07593)。下一步：精读三个限制的条件及近确定情形推广。

### T02-009 — Learning Representations for Neural Network-Based Classification Using the Information Bottleneck Principle [P1]
- 身份：2018首发，2019 v6，TPAMI2020引用线索；Rana Ali Amjad、Bernhard C. Geiger（检索元数据）；[arXiv:1802.09766](https://arxiv.org/abs/1802.09766)。旧题名How (Not) To Train Your Neural Network…是同一ID，不另计。深度：A。
- 机制关联：确定DNN的IB泛函可能无穷或分段常数；双射不变性也不能刻画希望获得的简单性/鲁棒性。
- 支持/反例潜力：信息保存量不等于可优化性或易读性；随机化、决策规则与替代目标只部分修复。不能把维度变小当互信息必减。
- 全文入口：[PDF](https://arxiv.org/pdf/1802.09766)。下一步：核对连续分布、网络映射及实测估计器分别落在哪类条件。

### T02-010 — Universal Representations for Classification-enhanced Lossy Compression [P1]
- 身份：2025-04-12，v1；作者：—；[arXiv:2504.13191](https://arxiv.org/abs/2504.13191)。深度：A。
- 机制关联：单编码器复用到不同重建/分类/感知约束操作点；率失真分类与率失真感知权衡。
- 支持/反例潜力：摘要同时给正反结果：感知任务复用损失小，分类—失真操作点变化时可出现显著失真罚。反对“一个压缩表示对全部粒度/效用天然通用”。
- 全文入口：[PDF](https://arxiv.org/pdf/2504.13191)。下一步：核对“universal”究竟跨操作点还是跨任务、数据/编码器约束及反例范围。

### T02-011 — Optimal Multitask Representations Under a Rate Constraint: An Information Bottleneck Analysis [P1]
- 身份：2026-10-21，v1；Nicholas Stiles等（检索元数据；完整名单待补）；[arXiv:2610.30493](https://arxiv.org/abs/2610.30493)。深度：A；近期预印本，不作证明或效果背书。
- 机制关联：高斯输入/任务、多任务IB、互信息预算；低/高码率下专家与重建通才排名可反转，固定高斯预测目标可有大相对遗憾。
- 支持/反例潜力：非常贴近未知下游任务分配问题；摘要还给平均任务信息矩阵的受限遗憾界。不能把高斯最优表示或数据集例证变成真实语言、多槽训练保证。
- 全文入口：[PDF](https://arxiv.org/pdf/2610.30493)。下一步：核定任务族、SNR条件、相对遗憾分母和最优解可达性。

### T02-012 — On the Limitations of Representing Functions on Sets [P1]
- 身份：2019；Edward Wagstaff、Fabian Fuchs、Martin Engelcke、Ingmar Posner、Michael A. Osborne；ICML/PMLR97:6487–6494；[正式页](https://proceedings.mlr.press/v97/wagstaff19a.html)。深度：A。
- 机制关联：通过连续映射汇总集合时，潜空间维数必须足够大；反驳任意增长集合仍可固定潜维的朴素解释。
- 支持/反例潜力：单个汇总向量的连续表达能力存在条件化下界；集合、置换不变、连续映射及最大集合大小都是条件，不可直接把“至少元素数”换成语言中“至少同数槽”。
- 全文入口：[PDF](https://proceedings.mlr.press/v97/wagstaff19a/wagstaff19a.pdf)。下一步：核定输入元素维数、定义域和一般化边界。

### T02-013 — Universal Approximation of Functions on Sets [P1]
- 身份：2021首发，2022 JMLR正式版检索线索；Edward Wagstaff等（检索元数据）；[arXiv:2107.01959](https://arxiv.org/abs/2107.01959)。深度：A；与012是不同作品，不是预印本/正式版重复。
- 机制关联：Deep Sets潜维比必要维度小一维时，存在分段仿射函数，其最坏误差不优于常数基线；讨论Janossy池化（用元素排列上的函数再对称化的集合表示范式）。
- 支持/反例潜力：最坏情形能力边界很强，但不是实际任务分布平均表现结论。必须避免从“缺一维的困难函数存在”跳成“任何单槽一定失败”。
- 全文入口：[PDF](https://arxiv.org/pdf/2107.01959)。下一步：核定一致逼近、误差范数、输入域及对其他集合模型的适用性。

### T02-014 — Deep Sets
- 身份：2017首发，2018 v3；Manzil Zaheer等（题名检索及原文引用链）；[arXiv:1703.06114](https://arxiv.org/abs/1703.06114)。深度：A。
- 机制关联：置换不变函数的结构表示与置换等变条件，集合汇总的经典表达构造。
- 支持/反例潜力：正面表达定理必须与012/013的连续性、定义域和维度限制一起读；本身不证明槽绑定可学、信息容易读出或真实模型会使用聚合支路。
- 全文入口：[PDF](https://arxiv.org/pdf/1703.06114)。下一步：按原定理逐项比对可数/连续输入域和基数条件。

### T02-015 — On Strengths and Limitations of Single-Vector Embeddings [P1]
- 身份：2026-03-31，v1；作者：—；[arXiv:2603.29519](https://arxiv.org/abs/2603.29519)。深度：A；近期预印本。
- 机制关联：质疑LIMIT失败可仅由维度解释；摘要引用2k+1维足以实现top-k检索的结果，强调分布漂移、相关性错配、微调及多向量优势。
- 支持/反例潜力：是021必须配套的反方，不宜先判其“推翻”。存在性嵌入、可训练编码器、自然查询泛化与遗忘不同；摘要报告单向量微调后其他任务遗忘更重。
- 全文入口：[PDF](https://arxiv.org/pdf/2603.29519)。下一步：核定2k+1结论的构造和前提是否与021的固定文档/全子集问题相同。

### T02-016 — Toward a Theory of Hierarchical Memory for Language Agents [P1]
- 身份：2026-03-23，v1；作者：—（完整原始作者名单待补，检索仅核到Y. Talebirad等）；[arXiv:2603.21564](https://arxiv.org/abs/2603.21564)。深度：A；会议轨道未确认。
- 机制关联：提取、粗化、遍历三个算子；粗化含分组与代表，代表的自足性谱约束合适检索策略；摘要称覆盖11个系统。
- 支持/反例潜力：与“多粒度代表+来源回访”概念最接近的形式化之一；目前只确认框架介绍，未确认是否有必要/充分定理、因果消费证据或完整成本。
- 全文入口：[PDF](https://arxiv.org/pdf/2603.21564)。下一步：明确代表自足与索引导航两用途、遗漏回退、原子来源保留及成本定义。

### T02-017 — Distributed Information Bottleneck Method for Discrete and Gaussian Sources
- 身份：2017首发，2018 IZS版本线索，v3；Inaki Estella Aguerri、Abdellatif Zaidi（检索元数据）；[arXiv:1709.09082](https://arxiv.org/abs/1709.09082)。深度：A。
- 机制关联：多个独立编码器压缩观测，集体保留目标信息；特定离散无记忆源与向量高斯源的信息—码率区域。
- 支持/反例潜力：提供分布式多份表示的理论参照，但多编码器拥有不同观测，不等价于同一编码器将一个片段拆成多槽；单字母条件和相关结构待查。
- 全文入口：[PDF](https://arxiv.org/pdf/1709.09082)。下一步：核定条件独立/联合分布、总码率约束和分散编码收益。

### T02-018 — Self-Supervised Learning from a Multi-View Perspective
- 身份：2020首发，2021 v4；Y.-H. H. Tsai、Y. Wu、R. Salakhutdinov、L.-P. Morency（检索引用元数据；名字全拼待原始作者栏补全）；[arXiv:2006.05576](https://arxiv.org/abs/2006.05576)。深度：A。
- 机制关联：把输入与自监督信号看作冗余视图，分析任务相关/无关信息保留并构造复合目标。
- 支持/反例潜力：相关信息可从共享视图提取是一条有条件的学习来源；新查询需要视图私有细节时不能借冗余假设免责。摘要另有超出多视图的经验探索，不等于定理覆盖。
- 全文入口：[PDF](https://arxiv.org/pdf/2006.05576)。下一步：核定任务信息在视图间冗余的精确定义。

### T02-019 — What Makes for Good Views for Contrastive Learning?
- 身份：2020，v3/NeurIPS2020；Yonglong Tian等（检索元数据）；[arXiv:2005.10243](https://arxiv.org/abs/2005.10243)。深度：A。
- 机制关联：减少视图间互信息，同时保留任务相关信息；学习增强视图，验证视觉下游任务。
- 支持/反例潜力：能解释在已知相关性前提下删冗余的正面情形；相反面是“保任务信息”是约束而非压缩后自动满足。不能直接搬成未知查询的合并策略。
- 全文入口：[PDF](https://arxiv.org/pdf/2005.10243)。下一步：核定最优视图条件、使用监督量及经验任务范围。

### T02-020 — Fundamental Limits of Prompt Compression: A Rate-Distortion Framework for Black-Box Language Models [P1]
- 身份：2024，v2 2024-12-11/NeurIPS2024；Alliot Nagle、Adway Girish等（检索元数据）；[arXiv:2407.15504](https://arxiv.org/abs/2407.15504)。深度：A。
- 机制关联：黑盒模型硬提示压缩的失真—码率线性规划；比较查询已知与未知压缩，提出变率查询感知策略。
- 支持/反例潜力：直接关系写入时是否可见问题。摘要报告查询可见性很关键；有限合成与小自然语言实验不能证明所有软状态架构的优势。
- 全文入口：[PDF](https://arxiv.org/pdf/2407.15504)。下一步：核定压缩器动作集、失真定义、固定消费模型、查询分布及训练/部署信息模式。

### T02-021 — On the Theoretical Limitations of Embedding-Based Retrieval [P1]
- 身份：2025首发，v2 2026-03-12；摘要页标Accepted to ICLR'26；Orion Weller等（检索元数据）；[arXiv:2508.21038](https://arxiv.org/abs/2508.21038)。深度：A。
- 机制关联：固定维向量可产生的top-k文档子集受到限制，构造LIMIT数据并直接优化自由嵌入。
- 支持/反例潜力：揭示读出规则与可表达相关性族的边界；自由嵌入优化失败是否等于严格下界，必须原文分离。与015相反表述都只先登记，不能用模型榜单替代数学条件比对。
- 全文入口：[PDF](https://arxiv.org/pdf/2508.21038)。下一步：固定文档、任意查询、k和维度的量词顺序，以及训练失败/严格不可能的界线。

### T02-022 — Exact and Soft Successive Refinement of the Information Bottleneck [P1]
- 身份：2023；H. Charvin、N. Catenacci Volpi、D. Polani（作者PDF检索片段，名字全拼待原始元数据补全）；Entropy25(9):1355；[PMC官方全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC10528077/)，[DOI](https://doi.org/10.3390/e25091355)。深度：A；没有把长HTML返回计全文精读。
- 机制关联：同一相关目标、不同粒度的IB最优表示能否无损复用；给若干二元/高斯/确定相关变量情形及软化损失度量。
- 支持/反例潜力：非常接近“粗到细无需丢弃已有信息”的理论；并非所有IB问题都可精确逐级细化，摘要称数值损失小但非零。未知新任务不在“同一相关变量”前提内。
- 全文入口：[PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10528077/)。下一步：核定各特例定理、Blackwell条件及软化量的操作含义。

### T02-023 — A Rate–Distortion View of Memory Compaction in LLMs and Agents [P1]
- 身份：2026-07-09，v1；Ashwin G. Colaco等（检索元数据，完整名单待补）；[arXiv:2607.08032](https://arxiv.org/abs/2607.08032)。深度：A；近期综述/理论提案，不作效果背书。
- 机制关联：将KV缓存、提示、递归状态、代理记忆统一成上下文信息预算下的效用保持问题；摘要提出跨层下界、分类轴、重复压缩评测。
- 支持/反例潜力：未知查询前不可逆删除与重复压缩是直接相关缺口；摘要的跨社区概括“到处都是注意力/近因”需要反例审查，不能照抄成全域结论。
- 全文入口：[PDF](https://arxiv.org/pdf/2607.08032)。下一步：核定下界的对象、可比较预算轴和来源回访是否改变问题设置。

### T02-024 — Handover of In-Context Learning State Across Session Boundaries [P1]
- 身份：2026-08-14，v1；Masahiro Kato、Taka Kato（检索元数据，待原始作者栏确认）；[arXiv:2608.14528](https://arxiv.org/abs/2608.14528)。深度：A；近期理论预印本。
- 机制关联：任务相对的上下文学习状态交接；在外生性条件下用预测等价刻画最粗确定充分交接，分析写入先于真实下游查询的代价。
- 支持/反例潜力：直接区分精确恢复旧材料与保持目标分布；摘要提出“精确决策/约束+任务统计量+未被统计量保留的原始观察”。非参数例子还提示有限充分状态不是普遍事实。
- 全文入口：[PDF](https://arxiv.org/pdf/2608.14528)。下一步：核定外生性、量词、固定比特要求和继续过程假设。

### T02-025 — MAGE-RAG: Multigranular Adaptive Graph Evidence for Agentic Multimodal RAG in Long-Document QA [P1]
- 身份：2026-06-14，v1；作者：—（不将提交人Xunkai Li当作者）；[arXiv:2606.15906](https://arxiv.org/abs/2606.15906)。深度：A；近期系统预印本。
- 机制关联：离线页/元素图保留包含、顺序、布局、层级和语义关系；查询时显式预算下迭代激活、打开、搜索、剪枝，再构造读者输入。
- 支持/反例潜力：最接近“多粒度+来源回访”组合的已核验系统之一。摘要性能数字只算作者报告，尚未核定控制组、公平预算或消费因果性；PDF图像文档不等于字节语言表示。
- 全文入口：[PDF](https://arxiv.org/pdf/2606.15906)。下一步：原始页面/元素是否一直保留、导航漏召回、下钻动作监督与端到端成本。

### T02-026 — RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval [P1]
- 身份：2024；Parth Sarthi等（检索元数据）；[arXiv:2401.18059](https://arxiv.org/abs/2401.18059)。深度：A。
- 机制关联：文本块递归嵌入、聚类、摘要，形成多层抽象树，查询时跨层检索。
- 支持/反例潜力：证明“多层摘要树+跨粒度读取”不是空白；摘要未证明自适应下钻一定优于扁平跨层检索，也未说明原始细节在哪一步获得消费。其20个百分点例子不迁移为理论保证。
- 全文入口：[PDF](https://arxiv.org/pdf/2401.18059)。下一步：区分树遍历与所有层扁平索引、叶子保留、召回/预算公平性。

### T02-027 — From Isolated Conversations to Hierarchical Schemas: Dynamic Tree Memory Representation for LLMs
- 身份：2024首发，2025 v3/ICLR2025引用线索；Alireza Rezazadeh、Zichao Li、Wei Wei、Yujia Bao（检索元数据）；[arXiv:2410.14052](https://arxiv.org/abs/2410.14052)。深度：A；简称MemTree与完整题名关联，不另计。
- 机制关联：节点同时保存聚合文本、语义向量和抽象层次，随新信息动态更新树。
- 支持/反例潜力：多粒度动态记忆组织的重要邻居；摘要不能确定来源映射是否无损、更新是否覆盖旧细节、查询是否按需要下钻，不能预设它已经解决来源生命周期。
- 全文入口：[PDF](https://arxiv.org/pdf/2410.14052)。下一步：与T03/T04交叉去重，核定叶保留、更新成本和检索协议。

### T02-028 — Learned Layered Coding for Successive Refinement in the Wyner-Ziv Problem
- 身份：2023首发，2024正式出版线索；Boris Joukovsky等（检索元数据）；[arXiv:2311.03061](https://arxiv.org/abs/2311.03061)。深度：A。
- 机制关联：连续源逐层编码、带相关侧信息解码；用循环网络优化变分率失真界，学习分层分箱。
- 支持/反例潜力：理论多层描述到可训练编码的正面参照；摘要明确二次高斯与理想Slepian–Wolf编码假设（即侧信息辅助的理想无损分布式编码），不能等同真实有限长任意语言学习。
- 全文入口：[PDF](https://arxiv.org/pdf/2311.03061)。下一步：核定理想编码与真实码长、侧信息可见端及可实现层数。

### T02-029 — MUVERA: Multi-Vector Retrieval via Fixed Dimensional Encodings [P1]
- 身份：2024首发/NeurIPS2024线索，2026-06-08 v2；Laxman Dhulipala、Majid Hadian、Rajesh Jayaram、Jason Lee、Vahab Mirrokni（检索元数据）；[arXiv:2405.19504](https://arxiv.org/abs/2405.19504)。深度：A；修订需专项核对。
- 机制关联：将多向量相似度用查询/文档不对称固定维编码的内积近似，利用现有最大内积搜索。
- 支持/反例潜力：反对“多向量绝不可能压成一个向量”的口号。保证是指定相似度的近似，不是任意任务信息无损，也不自动免除重新评分/保留原向量成本。摘要报告的端到端效果待正文核验。
- 全文入口：[PDF，须锁定v2](https://arxiv.org/pdf/2405.19504v2)。下一步：维度随误差/集合规模如何增长、保证种类、候选回访与精排成本，及v1/v2证明差异。

### T02-030 — On State Reduction in Linear Attention
- 身份：2026-02-04首发，2026-09-29 v3；Philipp Nazari等（检索元数据）；[arXiv:2602.04852](https://arxiv.org/abs/2602.04852)。早期检索题名The Key to State Reduction in Linear Attention: A Rank-based Perspective，同ID不另计。深度：A。
- 机制关联：键和值决定递归矩阵状态的秩；依据预训练后低秩结构剪枝键/查询矩阵并适配硬件。
- 支持/反例潜力：容量上界不等于实际占用，可能存在大量未用状态；但低秩和小困惑度退化不证明长窗稀有查询也无损，须核对任务与长度。
- 全文入口：[PDF](https://arxiv.org/pdf/2602.04852)。下一步：训练后观察、理论秩条件、容量与鲁棒性分开，交T05/T06。

### T02-031 — Separations in the Representational Capabilities of Transformers and Recurrent Architectures
- 身份：2024，v1；作者：—（完整原始作者栏待补）；[arXiv:2406.09347](https://arxiv.org/abs/2406.09347)。深度：A。
- 机制关联：索引查询、近邻、括号语言、相等和不交等任务上的模型规模分离，使用通信复杂度归约。
- 支持/反例潜力：双向分离：某些检索任务注意力有利，某些有界括号语言循环结构有利。有效反对只选一类记忆任务宣布统一优劣；表达能力结果不等于优化收敛。
- 全文入口：[PDF](https://arxiv.org/pdf/2406.09347)。下一步：核定精度、层数、宽度、序列长度和构造权重的规模。

### T02-032 — Revisiting Associative Recall in Modern Recurrent Models
- 身份：2025-08-26，v2 2025-10-10；作者：—；[arXiv:2508.19029](https://arxiv.org/abs/2508.19029)。深度：A。
- 机制关联：检查关联回忆中的学习率、宽度/深度、注意力层数和归纳头形成。
- 支持/反例潜力：对“测不出来=记忆容量不可能”的强反例提醒；摘要称循环模型学习率敏感、单层注意力也可能失败。并不取消有限位状态的严格信息下界。
- 全文入口：[PDF](https://arxiv.org/pdf/2508.19029)。下一步：与004/005/031区分评测任务和优化预算，不直接套相同门槛。

### T02-033 — Successive Refinement for Lossy Compression of Individual Sequences
- 身份：2025-02-24，v1；Neri Merhav（检索元数据）；[arXiv:2502.16869](https://arxiv.org/abs/2502.16869)。深度：A。
- 机制关联：个体序列、有限状态编码器、两阶段粗细编码的外界；扩展到多描述编码。
- 支持/反例潜力：补独立同分布渐近理论之外的资源限制；有限状态编码约束比任意最优编码强。仍不是神经网络能学到某种分层压缩的证明。
- 全文入口：[PDF](https://arxiv.org/pdf/2502.16869)。下一步：状态数、序列级失真、块长及下界松紧。

### T02-034 — Nonlinear Information Bottleneck
- 身份：2017首发，2019 v9；Artemy Kolchinsky、Brendan D. Tracey、David H. Wolpert（公开PDF检索元数据）；[arXiv:1705.02436](https://arxiv.org/abs/1705.02436)。深度：A。
- 机制关联：离散/连续任意分布、非线性编码解码，用非参数互信息上界训练神经模型。
- 支持/反例潜力：放宽高斯/小离散空间求解限制的正面路线；使用上界和优化算法仍不等于精确IB边界，需与008/009/037测量困难共同阅读。
- 全文入口：[PDF](https://arxiv.org/pdf/1705.02436)。下一步：噪声、界的紧性、维度与估计稳定性。

### T02-035 — Learning Optimal Representations with the Decodable Information Bottleneck [P1]
- 身份：2020首发/NeurIPS2020，2021 v2；Yann Dubois、Douwe Kiela、David J. Schwab、Ramakrishna Vedantam（检索元数据）；[arXiv:2009.12789](https://arxiv.org/abs/2009.12789)。深度：A。
- 机制关联：对指定预测器族定义可解码信息及充分/最小性，连接期望测试风险和可估计目标。
- 支持/反例潜力：最重要的“保存≠易读”理论参照之一；这里的DIB是Decodable，不是038的Deterministic。指定读出族、统计学习保证与具体已训模型确实消费必须分开。
- 全文入口：[PDF](https://arxiv.org/pdf/2009.12789)。下一步：预测族闭包条件、最优表示存在性、泛化界及训练可达性。

### T02-036 — A Theory of Usable Information Under Computational Constraints [P1]
- 身份：2020/ICLR2020引用线索；Yilun Xu、Shengjia Zhao、Jiaming Song、Russell Stewart、Stefano Ermon（检索元数据）；[arXiv:2002.10689](https://arxiv.org/abs/2002.10689)。深度：A。
- 机制关联：预测V-信息（对受限预测函数族可利用的信息）把观察者计算能力纳入；可经计算增加，不服从Shannon互信息的同一数据处理关系。
- 支持/反例潜力：保存的总信息与下游能读取的信息必须区分。不能写成“计算凭空创造Shannon信息”，也不能把某预测族可利用等同部署消费者已利用。
- 全文入口：[PDF](https://arxiv.org/pdf/2002.10689)。下一步：预测族定义、条件可用信息、PAC保证与实际干预的关系。

### T02-037 — Formal Limitations on the Measurement of Mutual Information
- 身份：2020/AISTATS；David McAllester、Karl Stratos；PMLR108:875–884；[正式页](https://proceedings.mlr.press/v108/mcallester20a.html)。2018 arXiv:1811.04251是同一作品，不另计。深度：A。
- 机制关联：从N个样本得出的分布无关高置信互信息下界有O(log N)限制。
- 支持/反例潜力：反对用神经估计器数值饱和宣布“压缩已无损”或“信息已归零”。限制是指定分布无关置信下界，不是说所有结构化估计都不可能。
- 全文入口：[PDF](https://proceedings.mlr.press/v108/mcallester20a/mcallester20a.pdf)。下一步：核定概率、常数、分布假设以及对特定估计器的可迁移范围。

### T02-038 — The Deterministic Information Bottleneck
- 身份：2016首发，2017 Neural Computation引用线索；D. Strouse、David J. Schwab（检索元数据）；[arXiv:1604.00268](https://arxiv.org/abs/1604.00268)。深度：A。
- 机制关联：用表示熵而非互信息衡量压缩，得到硬聚类/确定编码，并连到软聚类。
- 支持/反例潜力：提示“码长/状态熵”与“输入—表示互信息”不是可随意替换的目标；评价优劣依赖采用哪种成本函数。与035缩写相同但非同一概念。
- 全文入口：[PDF](https://arxiv.org/pdf/1604.00268)。下一步：核对熵的编码解释、连续变量与训练实现限制。

### T02-039 — Predictability, Complexity and Learning
- 身份：2000首发，2001 v3；作者：—（完整原始作者元数据待补）；[arXiv:physics/0007070](https://arxiv.org/abs/physics/0007070)。深度：A。
- 机制关联：过去与未来的互信息随观察长度的增长，联系有限参数与非参数模型复杂度。
- 支持/反例潜力：支持按“对未来有预测价值”而非重建所有过去选择状态；然而未来分布、时间序列结构与后续任意检索查询不是同一任务族。摘要渐近规律不直接给定长神经槽的实践容量。
- 全文入口：[PDF](https://arxiv.org/pdf/physics/0007070)。下一步：核定预测窗、平稳性及渐近与有限样本区别。

### T02-040 — To Compress or Not to Compress—Self-Supervised Learning and Information Theory: A Review
- 身份：2023预印本，2024 Entropy26(3):252正式版线索；Ravid Shwartz-Ziv、Yann LeCun（检索元数据）；[arXiv:2304.09355](https://arxiv.org/abs/2304.09355)。早期题名Self-Supervised Learning and Information Theory: A Review，同ID不另计。深度：A。
- 机制关联：统一自监督信息论问题，讨论压缩、保留、估计及现有学习方式。
- 支持/反例潜力：作为扩展引用地图，避免只搜IB支持论；是综述，不作为其引用定理的第一手证明，不用它替代003/018/019原文。
- 全文入口：[PDF](https://arxiv.org/pdf/2304.09355)。下一步：按相关假设追原始文献，重点查视图共享不成立时的反例。

### T02-041 — Matryoshka Representation Learning [P1]
- 身份：2022首发/NeurIPS2022线索，2024 v4；Aditya Kusupati、Gantavya Bhatt、Aniket Rege等（原始页作者栏）；[arXiv:2205.13147](https://arxiv.org/abs/2205.13147)。深度：A。
- 机制关联：同一向量的嵌套前缀支持不同计算预算和粗细表示，应用分类与级联检索。
- 支持/反例潜力：最接近“学习多个预算级别、先粗后细”的表示训练邻居之一；粒度轴是向量维度，不是来源片段/地址粒度。摘要没有证明任意未知任务都能用同一前缀无损完成。
- 全文入口：[PDF](https://arxiv.org/pdf/2205.13147)。下一步：多级监督、级联候选保留、增量读成本及与独立低维表示对照。

### T02-042 — Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention [P1]
- 身份：2025-02-16，v2 2025-02-27；Jingyang Yuan、Huazuo Gao、Damai Dai等（原始页作者栏）；[arXiv:2502.11089](https://arxiv.org/abs/2502.11089)。深度：A。
- 机制关联：粗粒度token压缩与细粒度token选择组合的动态层级稀疏注意力，强调原生训练及硬件对齐。
- 支持/反例潜力：不能声称“粗摘要指导细读取”没有先例。摘要说明组合与端到端训练，但未据此确认来源映射、选择监督、漏召回恢复或各分支真实消费。
- 全文入口：[PDF](https://arxiv.org/pdf/2502.11089)。下一步：粗分支怎样指导选择、原KV保存、局部/粗/细支路消融与完整开销；交T04/T06。

### T02-043 — Set Transformer: A Framework for Attention-based Permutation-Invariant Neural Networks
- 身份：2019/ICML；Juho Lee、Yoonho Lee、Jungtaek Kim、Adam Kosiorek、Seungjin Choi、Yee Whye Teh；PMLR97:3744–3753；[正式页](https://proceedings.mlr.press/v97/lee19d.html)。深度：A。
- 机制关联：建模集合元素交互，诱导点注意力把元素数的计算复杂度从平方降为线性；编码与解码均用注意力。
- 支持/反例潜力：多中间槽/多种子汇总的邻近设计；固定诱导点带来的能力约束、注意力池化槽数与通用逼近条件仍需原文核对，不等同于任意集合信息无损。
- 全文入口：[PDF](https://proceedings.mlr.press/v97/lee19d/lee19d.pdf)。下一步：诱导点数、输出种子数、总维度及理论条件。

### T02-044 — Object-Centric Learning with Slot Attention
- 身份：2020/NeurIPS2020，v2；Francesco Locatello等（检索元数据）；[arXiv:2006.15055](https://arxiv.org/abs/2006.15055)。深度：A。
- 机制关联：竞争式多轮注意力将感知特征绑定到可交换物体槽；无监督发现/监督属性预测上的组合泛化。
- 支持/反例潜力：说明多槽分工存在学习实现，但视觉物体先验、重建/属性训练与任意语言信息绑定不是一回事；槽数、位宽和总参数必须控制，不能由多槽效果推信息论优越。
- 全文入口：[PDF](https://arxiv.org/pdf/2006.15055)。下一步：交换性、分配竞争、槽坍缩、物体数变化和读出监督。

### T02-045 — Shannon Meets Blackwell and Le Cam: Channels, Codes, and Statistical Experiments
- 身份：2011/IEEE ISIT；Maxim Raginsky；[作者公开PDF](https://maxim.ece.illinois.edu/pubs/raginsky_ISIT11.pdf)。深度：A；另定位§III的通道比较定义，不计全文精读。搜索参考页码与PDF页码不一致，正式页码待出版方核定。
- 机制关联：统计试验最佳风险、Blackwell序与Le Cam信息亏损，扩展到编码/解码通道比较。
- 支持/反例潜力：把“对所有决策更有信息”与单一互信息大小区分；原文标准Borel字母表等条件与随机模拟器要保留。不要把编码前处理可用性误当部署模型有这类权限。
- 全文入口：同作者PDF。下一步：区分Blackwell与Shannon序、亏损方向、最坏/平均风险，以及计算不受限前提。

### T02-046 — Coarse-Graining and the Blackwell Order
- 身份：2017，v3；Johannes Rauh、Pradeep Kr. Banerjee、Eckehard Olbrich、Jürgen Jost、Nils Bertschinger、David Wolpert（检索元数据）；[arXiv:1701.07602](https://arxiv.org/abs/1701.07602)。深度：A。
- 机制关联：输入粗化与输出退化不一样；互信息意义的“less capable”不必等价于决策风险的Blackwell劣序。
- 支持/反例潜力：重要概念反例：不能凭互信息排序所有任务效用。作者的输入粗化反例不违反固定马尔可夫链下的数据处理不等式，迁移时必须分清改动了哪一端。
- 全文入口：[PDF](https://arxiv.org/pdf/1701.07602)。下一步：复现最小反例并核对共享输入、先验和效用函数。

### T02-047 — Information Bottleneck for Gaussian Variables
- 身份：2005/JMLR6:165–188；Gal Chechik、Amir Globerson、Naftali Tishby、Yair Weiss（原始页作者栏）；[正式页](https://www.jmlr.org/papers/v6/chechik05a.html)。深度：A。
- 机制关联：联合高斯变量的解析最优连续表示为带噪线性投影；压缩权衡决定维度/特征方向和相变。
- 支持/反例潜力：很适合解释不同预算保留不同预测方向，不等同于“每个方向就是一个语义槽”。高斯解析最优性对语言非线性、多任务未知目标不直接成立。
- 全文入口：[PDF入口](https://www.jmlr.org/papers/volume6/chechik05a/chechik05a.pdf)。下一步：高斯、线性/随机编码、谱阈值及与011的关系。

### T02-048 — Fixed-Length Lossy Compression in the Finite Blocklength Regime
- 身份：2011首发，2012 IEEE TIT线索，2014 v3；Victoria Kostina、Sergio Verdú（检索元数据）；[arXiv:1102.3944](https://arxiv.org/abs/1102.3944)。深度：A。
- 机制关联：有限块长n及超失真概率ε下的最优码率，给任意固定块长界；无记忆平稳/可分失真的二阶近似含码率离散度。
- 支持/反例潜力：直接制止用渐近R(D)断言短块多粒度编码无额外成本；均值失真与尾部失败门也不能混用。数学码长预算不自动包含寻址、元数据和延迟。
- 全文入口：[PDF](https://arxiv.org/pdf/1102.3944)。下一步：核定有限长余项、源条件、超失真概率与真实小块实验可比性。

### T02-049 — Compression for Quadratic Similarity Queries [P1]
- 身份：2015/IEEE TIT，作者仓与PMC对应；Amir Ingber、Thomas Courtade、Tsachy Weissman（检索元数据）；[PMC官方全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC5786438/)。深度：A；另定位§I–II查询定义，不计全文精读。
- 机制关联：数据库压缩签名只回答平方距离相似性的no/maybe，禁止假阴性；maybe可触发原库进一步验证，不要求从签名重建数据。
- 支持/反例潜力：这是“压缩导航+保留来源+回访”的强理论邻居，不限神经系统。成立于指定相似性、数据/查询模型和渐近可靠性；不是任意语义检索的零漏召回证明，也未包含计算成本。
- 全文入口：[作者PDF](https://people.eecs.berkeley.edu/~courtade/pdfs/IngberEtAl_TIT2015.pdf)、同PMC。下一步：核对零漏条件、独立查询与源分布、签名率和maybe回访负载。

### T02-050 — Adaptive Slot Attention: Object Discovery with Dynamic Slot Number
- 身份：2024-06-13，v1；Ke Fan等（检索元数据）；[arXiv:2406.09196](https://arxiv.org/abs/2406.09196)。深度：A。
- 机制关联：复杂度感知物体自编码器，离散选择槽数、屏蔽未选槽；动态匹配实例复杂度。
- 支持/反例潜力：说明槽数可成为被学习的资源决策，不必固定；摘要物体发现结果不能证明学习出的槽数是任意任务的率失真最优点，或者消费端利用了每个槽。
- 全文入口：[PDF](https://arxiv.org/pdf/2406.09196)。下一步：槽数成本项、梯度估计、候选槽上限及固定总位预算对照。

### T02-051 — Perceiver: General Perception with Iterative Attention
- 身份：2021，v2；Andrew Jaegle等（检索元数据）；[arXiv:2103.03206](https://arxiv.org/abs/2103.03206)。深度：A；不与Perceiver IO合并。
- 机制关联：非对称注意力反复将大输入蒸馏到紧潜瓶颈，多感知模态分类；关注输入规模与隐变量数量解耦。
- 支持/反例潜力：固定多潜槽的正面工程实现，提醒“潜瓶颈仍可完成很多任务”；但反复读输入与单次不可逆压缩不是同一访问模式，分类竞争力不是全细节可恢复保证。
- 全文入口：[PDF](https://arxiv.org/pdf/2103.03206)。下一步：输入能回访几次、潜槽/深度成本、监督目标与任意查询外推。

### T02-052 — Successive Refinement of Information [P1]
- 身份：1991/IEEE Transactions on Information Theory37(2):269–275；William H. R. Equitz、Thomas M. Cover（作者PDF首页）；DOI [10.1109/18.75242](https://doi.org/10.1109/18.75242)；[作者公开PDF](https://isl.stanford.edu/~cover/papers/transIT/0269equi.pdf)。深度：A；另外定位§I/§III/§IV，不计全文精读。
- 机制关联：粗描述+增量细描述的各级率失真最优性，以最优测试通道的马尔可夫兼容性刻画；摘要给正例与非普适反例。
- 支持/反例潜力：最直接的多粒度“免费细化并非总成立”基准。正文§I还明确单个高斯量最优量化嵌套失败不矛盾于长独立同分布块可细化；不能跳过块长、失真和源条件。
- 全文入口：同作者PDF。下一步：优先核对§III定理2与§IV反例，再对照022、028、048；不把有细码与从粗码自行恢复细节混同。

## II. 去重与近期版本索引

- 首发在最近12个月内的7件：011（2026-10）、015（2026-03）、016（2026-03）、023（2026-07）、024（2026-08）、025（2026-06）、030（2026-02）。它们均只摘要核验，不以新颖名字作背书。
- 最近12个月的旧作修订另有021（2026-03 v2）和029（2026-06 v2）；仍各只计1件。
- 007（1999工作/2000上传）、006（2016/2017）、003（2021/2022）、013（2021/2022）、027（2024/2025）、028（2023/2024）、037（2018/2020）、038（2016/2017）、040（2023/2024）、048（2011/2012）都已在卡内合并版本。
- 012与013虽同作者、同主题，题名与贡献不同，保留两件；014是更早基础作品。
- 035与038均可能缩写DIB，但不同题名/ID/目标，不合并。
- 021与015是一组相反论述；026、027、025、042是不同系统；029是相似度近似的检索算法，不归并为多向量编码模型。

## III. 尚不进入确认计数的扩展入口

这些只出现在实际检索结果或参考链中，身份/摘要核验尚不足，不作确认候选、不背书：

|待追入口|本轮为何未计|下一步最小动作|
|---|---|---|
|Wyner–Ziv 1976，The Rate-Distortion Function for Source Coding with Side Information at the Decoder|S45主要返回后续引用，未取原始摘要|找出版方/作者仓原始稿，核编码器/解码器的侧信息权限|
|Rimoldi 1994，Successive Refinement of Information: Characterization of Achievable Rates|S03/S10仅参考链|核原摘要与区域，补非可细化场景的代价|
|Gray–Wyner 1974，Source Coding for a Simple Network|052参考链，未独立摘要核验|核共同/私有描述的网络假设，防把多槽误作多接收端|
|arXiv:2609.14421，A Unified Information-Theoretic View of Multimodal Learning|S46仅检索片段|先取原摘要，检验与任务充分性是否直接相关|
|OpenReview TUKrrXWMN2，Granular Information Bottleneck for Deep Multi-…|S46题名被截断，年份/状态不明|先核完整身份；不可因名称含granular就归入同构|
|Scaling Linear Attention Capacity with Sparse State Expansion，ICLR2026 PDF入口见S27|只搜索命中、无摘要核验|交T05先取原摘要及状态规模条件|
|arXiv:2005.10242，Understanding Contrastive Representation Learning through Alignment and Uniformity on the Hypersphere|S21只检索发现，相关性次于018/019|若需训练几何桥梁再核摘要，不为凑数补入|
|arXiv:2608.04074|S16只有变换量化参考片段，精确身份未核|先核题名与摘要；偏KV量化则交T06|

不把上述8个入口称为8件已确认论文；全局目录负责人需先做作品身份与版本去重。
