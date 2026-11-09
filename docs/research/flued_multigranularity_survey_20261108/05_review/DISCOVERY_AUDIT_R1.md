# 第一轮发现审计：来源、身份、摘要相符性与计数

日期：2026-11-08。独立抽样审计，不是全量真实性认证；不替代全文精读、代码审计或复现实验。

## 1. 结论与范围

**实核28个不同对象：27篇论文/技术报告、1个官方模型仓库介绍。**8专题各直接抽查至少3项，偏向2026近期、核心最近邻及强正/负结论；不是随机抽样，不能估计419条的错误率。27篇均重新取得原始摘要，并取得官方Atom身份记录；K3重新取得MoonshotAI官方组织仓库介绍。正文定向抽查4篇：DeepSeek-V4、DeepSeek-V4.1、MemWalker、DynaKRAG；V4.1正文提取只到引言。**本审计全文精读0、代码核验0、独立复现0。**

- **P0必须修：1项确定的作者错配。**T03-005 H-MEM的第二作者写成`Sheng Zeng`，原始页面与Atom均为`Shaoning Zeng`；不是同名消歧问题。
- **P1补查/校正：5个抽样对象。**LapMerge版本已可补齐；T03-051漏掉正式题名前缀；DeepSeek-V4日期与编号月份的异常仍在原始来源中；两份DeepSeek模型仓库入口本次均无法访问；K3仓库未固定版本且报告未读。这些不等于虚构作品。
- **其余22项：可用，限于身份和摘要层发现。**不表示其理论或实验结论已经成立。
- **抽样中未发现虚构arXiv ID、ID指向另一作品、把检索片段冒充全文精读的确定事例。**这只涵盖本次27个ID和1个仓库，不可改写为“419条均真实”。
- **最需防止的后续语义升级**：DynaKRAG动作优势标签在正文中是一步支持证据召回效用，不是完整后续策略的终局答案价值；MemWalker已有摘要树、原文叶访问和返回父节点；V4的稀疏访问对象是压缩KV而非任意历史原始KV；AttnRes的块是深度块，不能当文本粒度或真跳算证据。

### 输入隔离与操作边界

先读`PLAN.md`、`COORDINATION.md`，随后仅读已交付的`01_search/T01…T08/CANDIDATES.md`、T04/T07的`SEARCH_LOG.md`及`00_scope/USER_CONCEPT_V01.md`。**未读取02_catalog、03_reading、04_synthesis或其他正在生成的审查产物。**只写本文件，不改草案/候选卡/源码/证据表，不训练、不提交、不派子代理。

核验使用`FetchURL`读取公开来源、官方arXiv Atom记录，以及Kimi Code内置浏览器读取原始页面。未调用数据源插件、未上传内部文本。本文英文作品标题为原名；“一步效用”指只衡量当前动作造成的一步变化，“终局策略价值”指允许后续策略继续执行后的最终收益，二者不可互换。

### 分层样本账

|专题|本报告样本|项数|选样理由|
|---|---|---:|---|
|T01|A01–A03|3|边界监督、严格预算合并、压缩记忆内容效用；均2026|
|T02|A04–A06|3|核心任务充分性、2026多任务强理论主张、单向量限制反方|
|T03|A07–A11|5|H-MEM、ReadAgent、MemWalker、HORMA最近邻及强重排器反例|
|T04|A12–A15|4|草案DeepSeek V4/V4.1、MiTA、K3身份与机制|
|T05|A16–A18|3|2026双侧记忆、精确缓存、正交性强负面主张|
|T06|A19–A21|3|真实速度负结果、2026最新服务成本、AttnRes|
|T07|A22–A25|4|2026非短视/预算理论、训练形成干预、DynaKRAG效用最近邻|
|T08|A26–A28|3|2026熵边界反例及同作者相关工作、共享梯度机制|
|合计|A01–A28|28|27篇作品+1仓库介绍；没有用跨专题复用凑本表项数|

## 2. 逐项原始证据与判断

以下引号内为本次实际返回的原始摘要/正文短摘录。`可用`仅允许进入发现/精读队列。作者来自Atom的`author/name`或原始页面作者栏，**不是`From`提交人**。日期分别记录首发与修订，不能混为首次发现时间。

### T01

#### A01｜T01-C12｜SOMBRERO｜可用

- 原始身份：[2601.22805v1](https://arxiv.org/abs/2601.22805v1)，2026-01-30；Pit Neitemeier、Alessio Serra、Jiaze Li、Sascha Wirges、Lukas Balles、Jan Hendrik Metzen。正式题名为 *SOMBRERO: Measuring and Steering Boundary Placement in End-to-End Hierarchical Sequence Models*。
- 摘要原证：“boundary enrichment B, which measures how strongly chunk starts concentrate on positions with high next-byte surprisal”；“a confidence-alignment boundary loss”；“smoothing at the input level rather than on realized chunks”。
- 与候选对照：边界富集度、辅助对齐损失、输入级平滑均相符；2026年正确。候选留空作者本次可补，不应据提交人Jan Metzen写成单作者。
- 强结论边界：作者声称1B、多种UTF-8语料上的权衡改善；指标对所用监督的自相关、是否因果改善最终任务仍需精读，未证明“惊异度就是正确计算价值”。

#### A02｜T01-C30｜LapMerge｜P1：补版本

- 原始身份：[2610.13858](https://arxiv.org/abs/2610.13858)，*LapMerge: Differentiable Exact-Budget Token Merging in Linear Time*；Magdalena Trędowicz、Aleksandra Nowak、Tomasz Steifer、Łukasz Struski、Szymon Płotka、Jacek Tabor。v1 2026-10-09，**v2 2026-10-12**，摘要页和Atom一致。
- 摘要原证：“exactly N equal-mass segments under a Laplace-kernel density”；“both the forward and the backward pass run in O(M+N) time”；“particularly effective when token order reflects spatial or temporal locality”。
- 与候选对照：题名、作者首二名、精确输出预算、线性扫描与有序性前提相符。候选说摘要页只见v1而搜索给v2，**本次已由原始摘要史和Atom消除此项未知**，应锁定v2。
- 不将“信息守恒”“任意语言任务无损”附加给论文；摘要只是作者在视觉/视觉语言任务上的性能声称。

#### A03｜T01-C50｜Evaluating Compressed Memory｜可用

- 原始身份：[2610.19373v1](https://arxiv.org/abs/2610.19373v1)，2026-10-14；Minsu Oh、Seunghui Jwa、Chanjun Park、Yeo-Chan Yoon。题名 *Evaluating Compressed Memory: Dependence, Utility, and Content Benefit*。
- 摘要原证：“some models rely on memory yet perform worse than the trained alternative”；另一问题文档的xRAG向量使TriviaQA F1“from 19.38 … to 24.78”，正确检索文档为“29.88 F1”；接受答案出现频率上的效应“statistically uncertain”。
- 与候选对照：置零依赖≠内容收益、另训无记忆/常量对照、错来源也可能增加词重叠分数均相符。**正确来源仍更高、另一答案指标不确定**两点必须保留，不能转述为“任意向量都一样”或“所有压缩无用”。九系统不代表九次独立外部复现。

### T02

#### A04｜T02-003｜Lossy Compression for Lossless Prediction｜可用

- 原始身份：[2106.10800](https://arxiv.org/abs/2106.10800)，Yann Dubois、Benjamin Bloem-Reddy、Karen Ullrich、Chris J. Maddison；2021-06-21首发，2022-01-28 v5；Atom注明NeurIPS2021。
- 摘要原证：“all predictive tasks that are invariant under a set of transformations, such as data augmentations”；图像压缩与8数据集下游分类实验。
- 与候选对照：未知任务的正面入口确实受预先给定不变性任务族限制。候选没有把“all”误写成所有未来文本查询；年份/版本关联相符，未因2022修订增加一篇。

#### A05｜T02-011｜Optimal Multitask Representations…｜可用

- 原始身份：[2610.30493v1](https://arxiv.org/abs/2610.30493v1)，2026-10-21；Nicholas Stiles、Gregory W. Wornell；正式题名 *Optimal Multitask Representations Under a Rate Constraint: An Information Bottleneck Analysis*。
- 摘要原证：“For Gaussian inputs and tasks”；“every fixed Gaussian prediction objective incurs arbitrarily large relative regret”；另一目标的界“controlled by maximum task SNR”。
- 与候选对照：高斯、多任务互信息约束、码率变化时优先级反转均相符。其强遗憾主张是**作者摘要声明**，尚未检查相对遗憾分母、量词、定理证明与可学习性，不能升级到任意语言模型不可能性。

#### A06｜T02-015｜On Strengths and Limitations of Single-Vector Embeddings｜可用

- 原始身份：[2603.29519v1](https://arxiv.org/abs/2603.29519v1)，2026-03-31；Archish S、Mihir Agarwal、Ankit Garg、Neeraj Kayal、Kirankumar Shiragur。
- 摘要原证：“2k+1-dimensional vector embeddings suffice for top-k retrieval”；“domain shift and misalignment … are major contributors”；微调后单向量仍较弱，MSMARCO性能“drops by more than 40%”。
- 与候选对照：单向量维数并非唯一解释、存在性与训练泛化的区分、灾难性遗忘均相符。没有据摘要宣布它“推翻”另一检索下界；两者量词需进一步对照原定理。

### T03：核心最近邻与强反例

#### A07｜T03-005｜H-MEM｜P0：确定作者错配

- 原始身份：[2507.22925v1](https://arxiv.org/abs/2507.22925v1)，2025-07-23；*Hierarchical Memory for High-Efficiency Long-Term Reasoning in LLM Agents*；作者栏为 **Haoran Sun, Shaoning Zeng**。Atom亦逐项列出这两人；内置浏览器再次直接读取页面作者栏确认。
- 候选当前写“Haoran Sun、**Sheng Zeng**”（`01_search/T03/CANDIDATES.md:50`），必须改成**Shaoning Zeng**，完整作者已齐，不必保留“完整书目信息待补”来遮蔽错名。本审计只登记，不越权改其文件。
- 摘要原证：“Each memory vector is embedded with a positional index encoding pointing to its semantically related sub-memories in the next layer”；“index-based routing … layer-by-layer retrieval”。
- 机制描述基本相符。索引明确指向**下层子记忆**，不能直接升级为原始文本指针。作者错配不使作品或机制变成虚构，但会污染最终引用、作者聚类和来源责任。

#### A08｜T03-033｜ReadAgent｜可用

- 原始身份：[2402.09727v3](https://arxiv.org/abs/2402.09727v3)，2024-02-15首发，2024-07-22 v3；Kuang-Huei Lee、Xinyun Chen、Hiroki Furuta、John Canny、Ian Fischer；完整题名 *A Human-Inspired Reading Agent with Gist Memory of Very Long Contexts*。
- 摘要原证：“decide what content to store together in a memory episode”；“compress … into … gist memories”；“look up passages in the original text”。
- 与候选对照：明确已有“压缩提示+查询后原文回访”，而非从压缩向量凭空恢复。3.5–20倍为三个阅读理解任务的作者报告，不是通用保证；摘要未说明它有多级树。不能把多专题收录当多个独立系统。

#### A09｜T03-034｜MemWalker｜可用；部分正文确认比摘要更强

- 原始身份：[2310.05029v1](https://arxiv.org/abs/2310.05029v1)，2023-10-08；Howard Chen、Ramakanth Pasunuru、Jason Weston、Asli Celikyilmaz；*Walking Down the Memory Maze: Beyond Context Limit through Interactive Reading*。
- 摘要原证：“first processes the long context into a tree of summary nodes”；“Upon receiving a query … navigates this tree”。
- 本次实际读取[HTML v1](https://arxiv.org/html/2310.05029v1)的§3方法中 *Memory tree construction*、*Navigation*、*Navigational prompt design*、Figure 1/Table 1：构树不依赖查询；逐级摘要；可选子节点或“revert to the parent node”；叶提示明确包含“content of the segment”。原文还说连续三次无法解析动作会终止并返回no answer。
- **已确认不只是“树”字面撞车**：多级摘要、叶原文、按查询导航、返回父节点在同一既有系统中出现。T03/T04原先将回退留作精读问题是诚实未知，本次可定向核销；不等于已审核全部存储更新/因果消费/成本。若后续创新宣称以“加回退”区别它，须先改差异说明。

#### A10｜T03-037｜HORMA｜可用

- 原始身份：[2606.11680v1](https://arxiv.org/abs/2606.11680v1)，2026-06-10；Hao-Lun Hsu、Nikki Lijing Kuang、Boyi Liu、Zhewei Yao、Yuxiong He；*Organize then Retrieve: Hierarchical Memory Navigation for Efficient Agents*。
- 摘要原证：“summarized entities are linked to the corresponding raw trajectories”；“lightweight agent trained with reinforcement learning to select minimal yet sufficient context”。
- 与候选对照：层级组织、原轨迹链接、学习导航确实同作出现，属于高度邻近，不是凭名称想象。摘要的“without losing detailed information”、最多22.17%基线token使用均是作者自述；未审原轨迹持久性、更新/删除传播、延迟与总成本，不能当无损或端到端最优证明。

#### A11｜T03-051｜强重排器反例｜P1：规范题名；机制可用

- 原始身份：[2606.28367v1](https://arxiv.org/abs/2606.28367v1)，2026-06-14；Sadanand Singh、Allam Reddy、Manan Chopra。Atom完整题名是 **Beyond the Reranker: Do RAG Retrieval Enhancements Help Once a Strong Reranker Is Present?** 候选仅保留冒号后部分，需补前缀并保留ID，避免总目录按题名再造一篇。
- 摘要原证：“shared backbone, with bootstrap confidence intervals and multiple-comparison correction”；“only two methods yield reliable gains: query expansion and SSCC”；其他层级摘要、图扩展、路由等“give no reliable gain once that reranker is present”。
- 与候选对照：反例内容相符，限定在HetDocQA及两项控制任务和该实现。未实核统计功效/样本数/候选池预算；不能把未显著增益写成所有层级记忆都无效。摘要“此前未测”也是作者定位，不是本审计完成的文献证明。

### T04：草案四类近期入口

#### A12｜T04-001｜DeepSeek-V4｜P1：日期异常与模型页访问未知；报告机制可用

- 原始身份：[2606.19348v1](https://arxiv.org/abs/2606.19348v1)，DeepSeek-AI及作者团队；题名 *DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence*。内置浏览器直接见`Submitted on 26 Apr 2026`、提交史v1 2026-04-26；Atom亦返回该首发日期。**2606编号与4月提交的异常不是候选作者自行造出的日期，但原因仍未知**；不可据此宣布ID虚构，也不可悄悄改成6月。
- 摘要确有CSA/HCA，Pro 1.6T/49B、Flash 284B/13B、1M上下文等作者配置；性能不在本轮背书范围。
- [HTML v1 §2.3/§2.3.1](https://arxiv.org/html/2606.19348v1)实际短摘录：“first compresses … every m tokens into one entry”；“each query token attends to only k compressed KV entries”。§2.3.2说明HCA重压缩后不使用稀疏选择；§2.3.3滑窗保留近期未压缩KV。
- 与候选对照：T04正确区分压缩条目与历史原始KV；**不能将草案“细节回访”路线上的V4当作远端原始来源可下钻证据**。报告只证明此处读压缩条目+近期滑窗。
- 草案模型入口[DeepSeek-V4-Pro](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro)连续两次Fetch均网络失败；本次没有取得模型卡或权重列表。报告正文确实给该模型仓库的inference链接，但“报告引用该链接”不等于本次模型页已成功访问。

#### A13｜T04-002｜DeepSeek-V4.1-Flash｜P1：模型页不可访问；报告可核验

- 原始身份：[2609.19969v1](https://arxiv.org/abs/2609.19969v1)，2026-09-17，DeepSeek-AI及作者团队；*DeepSeek-V4.1-Flash: Pushing the Limits of KV Cache Compression*。
- 摘要原证：“Causal Encoder-Decoder (CED)”；“cross-layer KV cache reuse in Compressed Sparse Attention 2 (CSA2) with FP4 KV caching”；全局KV“always in HBM … 890 bytes per token”；持久KV“always on SSD or in host memory”。
- 本次[HTML v1](https://arxiv.org/html/2609.19969v1)提取仅到引言，实际见：“CSA2 has three statically assigned modes: Full, Reindex, and Reuse”；Reindex共享KV但重新选索引，Reuse连索引一起复用；每层保有自身query/滑窗KV。SWA Bounded Replay是用近期窗口近似重建滑窗状态。
- 与候选对照：机制和深度声明相符；**静态分配复用模式不等于按需加工深度或未知时在线探索**；890 B/token不包含整个模型、所有局部状态和持久源存储。
- 草案[HF模型页](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash)两次Fetch网络失败。报告摘要/引言直接引用此地址，只能确认链接被作者给出，不能声称本次已读模型卡。

#### A14｜T04-003｜MiTA｜可用

- 原始身份：[2602.01219v6](https://arxiv.org/abs/2602.01219v6)，Qishuai Wen、Zhiyuan Huang、Xianghan Meng、Wei He、Chun-Guang Li；2026-02-01 v1，2026-09-27 v6；*Mixture-of-Top-k Attention: Efficient Attention via Scalable Fast Weights*。Atom备注NeurIPS2026，不作为本审计独立核过会场终稿的证明。
- 摘要原证：“landmark queries to gather top-k attended key-value pairs as query-aware and deformable routed experts”；“compressing … into a narrower shared expert”；“extensive experiments on vision tasks”。
- 与候选及草案对照：MiTA ID与现题名对应，路由集合+共享压缩分支并非虚构。**视觉证据不是因果语言建模证据**，草案已作正确限制。旧题/新版同一ID不能增计作品；本审计未逐版比较内容或独立复核旧题名。

#### A15｜T04-004｜Kimi K3｜P1：官方介绍可用，版本/报告未知

- 来源：[MoonshotAI/Kimi-K3](https://github.com/MoonshotAI/Kimi-K3)，本次成功取得官方组织仓库README的Model Introduction及Model Summary，不是搜索结果/媒体转述。
- 原始文字：“2.8T-parameter … built on Kimi Delta Attention (KDA) and Attention Residuals (AttnRes)”；表格为“69 KDA + 24 Gated MLA”，93层，1,048,576上下文长度。
- 与候选对照：2.8T、69+24组合在当前公开介绍中真实存在。仓库介绍不是独立论文，README+报告+权重不能拆成三篇。
- **未完成**：没有固定commit/发布tag，没有读取`k3_tech_report.pdf`，未核真实发布日期、模型卡版本演化及每项基准。该PDF链接是T04原日志给出的入口，本次不把它升级为已读来源。README没有本次已读的多级摘要来源回访证据；1M上下文、专家路由、KDA混合本身不能补出此机制。

### T05

#### A16｜T05-006｜Dual DeltaNet｜可用

- 原始身份：[2610.38578v1](https://arxiv.org/abs/2610.38578v1)，2026-10-28；Yixiao Qian、Yaxin Zhang、Song Chen、Jiaxu Liu、Shengze Cai、Chao Xu；*Dual DeltaNet: Value-Side Memory Reorganization for Linear Attention*。
- 摘要原证：键侧读`S^T k`取值，值侧读`S e`聚合地址；“two-sided delta rule”；“rank-2 recurrence”。
- 与候选对照：地址和值维度分工、双侧更新和秩二递归均相符，适合来源/地址轴讨论；“strongest overall performance”仍为作者摘要自述，未核控制组及成本。不把“重组地址”写成原文来源可寻址。

#### A17｜T05-010｜HOLA｜可用

- 原始身份：[2607.02303v1](https://arxiv.org/abs/2607.02303v1)，2026-07-02；Wanyun Cui；*A Hippocampus for Linear Attention: An Exact Memory for What the Recurrent State Forgets*。
- 摘要原证：“adds a bounded exact KV cache”；按“beta * ||e||, the prediction residual actually committed to the state”保存；“a decoupled RMSNorm-gamma cache read”。
- 与候选对照：精确缓存+递归压缩状态确实同作出现；写入残差不是任意未来查询效用。缓存有界，不代表保留全部源；标题exact描述保留KV，不构成所有旧事实无损保证。340M/15B、Wikitext改善等本次只确认作者报告的存在。

#### A18｜T05-051｜Attention Is Not Retention｜可用作强主张候选，不能用作一般定理

- 原始身份：[2601.15313v2](https://arxiv.org/abs/2601.15313v2)，2026-01-14首发，2026-02-04 v2；Oliver Zahn、Matt Beton、Simran Chana；*Attention Is Not Retention: The Orthogonality Constraint in Infinite-Context Architectures*。
- 摘要真的声称：“reliable memory requires orthogonal keys”；“no increase in model capacity can overcome interference when keys share semantic overlap”。因此T05不是杜撰该强主张。
- 候选已明确拒绝把它当一般定理，判断合格。**本审计未读其证明、模型类或精确ID哈希基线是否改变任务**；强措辞不因原摘要真实就变成数学事实。作者栏Oliver Zahn来自Atom，非提交人Simran Chana；不存在此次所见的作者错配。

### T06

#### A19｜T06-017｜FlexiDepth｜可用

- 原始身份：[2503.23798v3](https://arxiv.org/abs/2503.23798v3)，2025-03-31首发，2025-10-08 v3；Xuan Luo、Weizhi Wang、Xifeng Yan；*Adaptive Layer-skipping in Pre-trained LLMs*；Atom注明COLM2025。
- 摘要原证：“skips 8 out of 32 layers while maintaining full benchmark performance”；紧接着“does not yet achieve wall-clock speedup due to varied skipping patterns and I/O overhead”。
- 与候选对照：省计算不等于实速的负结果来自作者原摘要，不是审稿人的猜测；“full benchmark performance”仅其基准范围，不能说所有任务无损。

#### A20｜T06-033｜ExactLoop｜可用

- 原始身份：[2611.05150v1](https://arxiv.org/abs/2611.05150v1)，2026-11-03；Dezhen Lu、Runguo Li、Zixiang Ni、Yuchen Tang、Xingquan Kong、Jiaxing Yang、Jiarui Guo、Lingxiang Gao；*What Sets the Serving Speed of Looped Language Models? Measurements and Optimizations Graded by Exactness*。
- 摘要原证：“fusing all loop submissions leaves Ouro throughput at 0.99x”；“5689 small kernels per token”；近似融合“is no faster and misses a one-point GSM8K rule on 87 questions”。
- 与候选对照：非常近期但ID、作者及摘要真实取得；负面数字相符。不同优化/模型/错误处理开关的速度不能拼成统一保证；87题不等于整个基准或独立质量认证。未读实现与表格，不复核逐比特等价声明。

#### A21｜T06-042｜Attention Residuals｜可用

- 原始身份：[2603.15031v1](https://arxiv.org/abs/2603.15031v1)，2026-03-16；Kimi Team及Guangyu Chen、Yu Zhang、Jianlin Su等团队作者；题名 *Attention Residuals*。
- 摘要原证：“softmax attention over preceding layer outputs”；“learned, input-dependent weights”；“Block AttnRes … partitions layers into blocks”；48B总/3B激活、1.4T训练tokens也在原摘要中。
- 与候选及草案对照：身份与跨层选择机制相符；“块”为**层组**，不是原文片段；摘要没有说跳过未选Transformer层。内容条件权重不等于查询下钻原始来源，更不自动产生真实算量节省。候选对此已有正确边界，不能因拿到了PDF链接就升级阅读深度。

### T07：效用与训练形成最近邻

#### A22｜T07-008｜BRiG-AFA｜可用

- 原始身份：[2608.02305v1](https://arxiv.org/abs/2608.02305v1)，2026-08-03；Jiaorong Feng、Qian Li、Ying Li；*BRiG-AFA: Bellman Risk-to-Go Learning for Non-Myopic Active Feature Acquisition*。
- 摘要原证：“separate candidate-conditioned risk-to-go function for every remaining budget”；“fitted backward with Bellman targets”；MiniBooNE“三seed”结果“mixed at small budgets”；“experiments still needed for state-of-the-art comparison”。
- 与候选对照：非短视监督回归入口真实；候选保留了作者自认的局限，没有虚报全面先进比较。文本中`\method`未正确渲染是原摘要的宏残留，不是方法不存在或标题不符的证据。完整标签成本、训练完整观测权限未知。

#### A23｜T07-013｜The Lagrangian Structure…｜可用，理论未复核

- 原始身份：[2610.21919v1](https://arxiv.org/abs/2610.21919v1)，2026-10-15；Joseph Bingham；*The Lagrangian Structure of Cost-Penalized Active Feature Acquisition*。
- 摘要原证：证书“computable when the penalized optimum is tractable”；临床任务“diagnostic rather than a numerical guarantee”；互信息“不一定次模，即使jointly Gaussian”。
- 与候选对照：硬预算和期望成本拉格朗日松弛之分、证书计算限制均相符。没有核定证明、光滑性、次模比率或生成模型KL诊断的可估计性；不能以标题中的Structure背书实际控制器保证。

#### A24｜T07-037｜归纳头形成干预｜可用

- 原始身份：[2404.07129v1](https://arxiv.org/abs/2404.07129v1)，2024-04-10；Aaditya K. Singh、Ted Moskovitz、Felix Hill、Stephanie C. Y. Chan、Andrew M. Saxe；*What needs to go right for an induction head? A mechanistic study of in-context learning circuits and their formation*。
- 摘要原证：“modifying activations throughout training”；“By clamping subsets of activations throughout training … identify three underlying subcircuits”。
- 与候选对照：持续训练干预确实存在，不是由终点消融推断训练史；受控合成模型上的子回路加性，不能迁移成任意读取动作效用可加。作者/年份/ID相符。

#### A25｜T07-039｜DynaKRAG｜可用，但必须保留一步代理效用与终局价值的差异

- 原始身份：[2607.06507v2](https://arxiv.org/abs/2607.06507v2)，2026-07-07首发，2026-08-22 v2；Chenyu Zhou等，Atom完整作者为Chenyu Zhou、Yaqi Wu、Xiaolei Guo、Jiaqi Huang、Xianfa Zhang、Junxu Zhang、Zhuo Yu、Zhubo Shi、Jianghao Lin、Dongdong Ge。
- 摘要确有状态条件动作、可执行动作过滤、继续门、相对立即作答的优势打分。T07据摘要标成“学习型证据动作效用最近邻”有依据，不是虚构最近邻。
- **本次另外实际读取[HTML v2](https://arxiv.org/html/2607.06507v2)的Method → Learning a State-Conditioned Control Policy，公式(1)–(2)**：定义`U(s)=SR(s)`，即金标支持文档召回；每个日志前缀下每个有效动作执行一次取标签。原文明确：“a supervised one-step regression target rather than a trajectory-level Bellman value”。Related Work也明确区别于“rollouts or trajectory-level reward optimization”。
- 继续门另以“完成轨迹相对中间前缀作答的改善”监督；不能把继续门的终局标签嫁接给动作ranker。模型允许动作启用后续动作，不等于训练目标已优化所有多步互补。
- **对综合的约束**：它是CBIU式动作干预/低成本预测器的强公共近邻，但动作标签的代理目标、一步性、支持标注权限与真正终局J差值不同。原候选把完整优势构造留作问题是诚实的；现在这个关键未知已有局部正文答案，应在精读时核销，而非继续仅按摘要讲“真实答案边际价值”。未审核补充材料、代码、完整标签预算及实验表格。

### T08

#### A26｜T08-013｜Easy to anticipate, hard to compute…｜可用

- 原始身份：[2610.11790v1](https://arxiv.org/abs/2610.11790v1)，2026-10-08；Nicolás Vera Zúñiga；完整题名与候选一致。
- 摘要原证：“positions whose type is predictable but whose value must be computed”；“the rise in the model's own loss when a patch start is removed”；“copies and lookups gain little, and values the model cannot compute gain nothing”。
- 与候选对照：删除边界的模型自身loss变化、两字节上下文表、数学计算值上的紧预算现象相符。摘要还报“paired p < 1e-200”；**本审计不为该显著性、样本独立性或训练/评分实现背书**，这是下一轮特别需要看统计单位和共享样本的强结果。

#### A27｜T08-014｜Patch where the text is new…｜可用；不算独立复现

- 原始身份：[2610.22100v1](https://arxiv.org/abs/2610.22100v1)，2026-10-15；Nicolás Vera Zúñiga；题名 *Patch where the text is new: a compression view of where byte-level models should spend compute*。
- 摘要原证：“lookup table over the previous two bytes … no labels, reference model or losses”；“advantage shrinks … ties entropy on source code and on synthetic execution traces”。
- 与候选对照：动机是LZ77式新内容而非On/Off效用；与A26是**不同ID/题名/机制的两个作品记录**，但作者相同，Atom comment均指向`github.com/nicoveraz/segresearch`，不能作为两次独立团队复现。实际语料/模型/日志重叠范围未核；若后续作者确认是替代稿，应合并版本簇。当前没有足够证据强行合成一篇或当两份独立实证。

#### A28｜T08-022｜Weight Tying Biases…｜可用

- 原始身份：[2603.26663v1](https://arxiv.org/abs/2603.26663v1)，2026-03-27；Antonio Lopardo、Avyukth Harish、Catherine Arnett、Akshat Gupta；*Weight Tying Biases Token Embeddings Towards the Output Space*。
- 摘要原证：“output gradients dominate early in training”；“Scaling input gradients during training reduces this bias”；“tuned lens analysis”。
- 与候选对照：共享空间偏输出、早期梯度主导及干预确实来自原摘要。候选正确标为token模型的新近入口，未把它写成字节257词表、余弦输出或FLUED共享的已验证判词；正式ACL版本关联本次未重新核验。

## 3. P0必须修与P1待办登记

### P0-01｜H-MEM作者修正（确定；尚未在源文件核销）

- 位置：`docs/research/flued_multigranularity_survey_20261108/01_search/T03/CANDIDATES.md:50`。
- 必改：`Sheng Zeng` → `Shaoning Zeng`；与Haoran Sun合计2作者。
- 凭据：[原始abs](https://arxiv.org/abs/2507.22925v1)、本文M1 Atom的`author/name`、内置浏览器实际作者栏。无需再广域检索。
- 验收：候选卡、统一引用表、后续证据卡如出现该作者，均用原始拼写；本审计不修改其他所有者文件。

### P1清单（5对象，不误算成5篇坏论文）

|对象|已知问题/未知|最低成本动作|本次状态|
|---|---|---|---|
|A02 LapMerge|原记录版本冲突|用本文原始提交史/Atom锁v2 2026-10-12|可直接核销，不需重搜|
|A11强重排器|候选省略题名前缀Beyond the Reranker|按Atom补完整题名，保留2606.28367为主键|可直接核销，不影响作品存在|
|A12 V4|2606编号与2026-04-26提交异常；模型页不可访问|日期字段保留原值+异常标志；必要时再查官方发布史；模型卡恢复后读|异常原因及模型页内容未知|
|A13 V4.1|HF模型页两次网络失败；HTML只到引言|不把模型卡列已读；精读时合法取得PDF方法§2.2–2.3/§3.2.2|未完成，不绕访问拒绝|
|A15 K3|当前README没有commit、报告未读|固定公开commit/发布tag，取真实报告重点章；区分README与论文|未完成，不虚报PDF阅读|

**另有不计为当前错误的精读阻断条件**：DynaKRAG的一步代理效用不能升为终局价值；MemWalker回退已存在，不能作为未比较的创新；AttnRes深度块不能顶替文本地址粒度；A26/A27不能双算独立复现。现有候选多已写出相关限制，不能为制造“重大缺陷”而把其诚实未知判成造假。

## 4. 全文冒充、虚构ID、作者年份与重复计数检查

### 4.1 有没有把搜索结果当全文

- 8份候选文件均明确全文精读为0；T04-001/002/007/017另列局部正文，不冒充通读。T04日志明确V4.1只提取到引言；本次复取的确也止于引言。**本抽样没有确认到搜索结果冒充全文精读。**
- T03 MemWalker/ReadAgent部分附录线索、T08若干下钻细节被明确标为搜索片段待查，不可因写了精读问题而给它们算正文已读。
- 原始摘要页常被Fetch抽掉题名与作者，仅剩Abstract和From；这是真实工具限制。本文用Atom的author/name补齐，并用原始浏览器作者栏复核H-MEM。只保存摘要纯文本、不保存身份字段，会留下可重复发生的作者错配风险。
- 本文的4次正文入口抓取也不是4篇精读：V4只核§2.3片段，V4.1只核引言，MemWalker只核方法导航段，DynaKRAG只核动作标签与对应相关工作段。未将工具返回长页面自动计作已读全文。

### 4.2 有没有虚构ID或身份错配

- 27个抽样ID均由原始摘要+官方Atom取得匹配题名/摘要；未见指向其他学科作品的错链。
- **DeepSeek-V4编号月份异常本次在原始页面和Atom均复现**；这是需解释的来源异常，不足以判定某方捏造ID。
- 作者错配确定1处（A07）；题名不完整1处（A11）；其他样本没有发现作者/年份冲突。作者原本留空不是错误署名，但进入最终参考文献前仍应补齐。
- arXiv服务与Atom同属一机构，不是两家独立认证；它们能交叉检查页面提取与元数据映射，不能独立证明所有实验为真。

### 4.3 重复计数与证据独立性

- 协调表的419是专题条目总和，218是专题优先项总和，**不是去重后的419篇论文/218篇独立精读**；本次不计算全局独立作品总数，不读取正在生成的去重目录。
- 可在已交付卡片直接看到重复：RAPTOR的同一`2401.18059`至少出现在T02-026、T03-001、T04-005、T07-045、T08-039；ReadAgent同一`2402.09727`出现在T03-033、T04-050、T07-047。它们是交叉专题索引，不是新增论文。
- MiTA v1–v6只一作品；LapMerge v1/v2只一作品；K3 README/PDF/权重只一个系统入口，且不能因此算一篇论文。本审计28对象表中没有重复ID。
- T08-013/014可暂分作品，但已确认同作者、同公共项目仓库，**实证独立性只能记为一个相关证据簇**，实验重叠程度未知。真实作品数量、版本数量、独立实验数量必须三列分开。

## 5. 原始来源取得账本与失败

### 5.1 实际读取的身份元数据

以下4个官方公开Atom URL均本次实际通过FetchURL取得；不是学术插件调用，不以返回顺序关联作品，按`entry/id`关联。摘要页正文作者缺失由这些记录补齐。仅列作者和题名短摘录已在A01–A28逐项给出，不把完整长作者名单倾倒为阅读证据。

- **M1（10条）**：https://export.arxiv.org/api/query?id_list=2601.22805,2610.13858,2610.19373,2610.30493,2603.29519,2106.10800,2606.11680,2507.22925,2402.09727,2606.28367&max_results=10
- **M2（10条）**：https://export.arxiv.org/api/query?id_list=2606.19348,2609.19969,2602.01219,2603.15031,2610.38578,2607.02303,2601.15313,2503.23798,2611.05150,2607.06507&max_results=10
- **M3（6条）**：https://export.arxiv.org/api/query?id_list=2608.02305,2610.21919,2404.07129,2610.11790,2610.22100,2603.26663&max_results=6
- **M4（1条）**：https://export.arxiv.org/api/query?id_list=2310.05029&max_results=1

27篇均另直接访问各A项所列abs原始摘要；DeepSeek-V4该步由内置浏览器取得原始DOM文本，其余26篇由FetchURL。K3由FetchURL取得README，正文4入口见上。没有调用WebSearch补造搜索日志：本次从既有候选独立挑样，直接回第一手来源。

### 5.2 暂时失败与未知

|实际URL|尝试|实际结果|允许得出的结论|
|---|---:|---|---|
|https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro|2次Fetch|均`fetch failed`网络错误|模型卡内容本次未知；不能断言404、仓库不存在或已核模型卡|
|https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash|2次Fetch|均`fetch failed`网络错误|同上；报告可读不消除此入口未知|
|https://arxiv.org/html/2609.19969v1|1次Fetch|文本只到引言尾和图片|仅按引言部分核验；不能声称方法全章已读|

失败后没有使用代理、私有接口、账号或替换域名绕拒绝。公开arXiv报告是独立的正常第一手来源，不声称它等于成功访问HF模型页。没有遇到登录/验证码需处理；没有持续无限重试。临时浏览器标签已关闭。

## 6. 是否扩大审计：建议定向扩大，不宣判系统性虚构

**本次没有证据认定系统性虚构ID或全文冒充；但已确认一个元数据错名，并看到抽取缺作者、题名/版本不完整的共同风险，值得把“身份字段”扩到全候选。**不建议为此把所有419条逐篇全文重读，更不建议先投入200篇精读再处理引用身份。

最省成本顺序：

1. **先在已完成的419专题条目中提取稳定ID，做一次只读规范化与去重。**arXiv去版本号为作品键，保留版本列；正式版关联作别名；仓库/官方博客独立类型。不要拿含参考链/待核线索的全文正则匹配数当论文数。继续沿现有单一目录所有者流程，不新增并发总表写者。
2. **对唯一ID小批获取官方元数据，比对题名、完整作者、published/updated、版本；失败单列，不猜补。**同一作品只查一次。已有成功M1–M4可以直接核销本报告27篇，避免重复费用；重点找作者拼写差、冒号前缀省略、编号月份异常和把修订年当首发年。遵守原站限流，不需要新工具、外部嵌入或上传内部文档。
3. **内容审计只扩至会改变创新/架构选择的少量关键句**：MemWalker/ReadAgent/HORMA/H-MEM的原文对象和回退；DynaKRAG的动作代理效用/继续门区别；DeepSeek的压缩与原始KV对象；AttnRes深度轴；T08同作者统计与实验重叠。每句取原文一段+节号/公式，不为“来源可访问”把整篇标精读。
4. **升级触发条件**：若追加元数据审计再发现多个不同专题的ID→题名错配、作者从提交人误填或摘要内容对不上，暂停受影响条目的已核验标签，按共同生成路径扩大；若发现一条搜索片段被明确记为全文精读，先全查阅读深度字段。当前不能据单一错名把419全判作不可信。
5. **保留最小验收门**：P0-01核销；A02/A11规范；模型页失败和K3报告未知保持可见；对外稿不报419独立论文；强结果有原章节/表格和适用条件后才进入科研判词。该门针对发现质量，不替代后续全文证据卡。

## 7. 交付自检与未完成项

- 仅交付本文件；没有写其它专题、统一目录或审查文件。未运行测试/构建，因为没有代码变更；未创建脚本或训练产物。
- 样本索引A01–A28连续，27个不同arXiv作品ID+1仓库；各专题3/3/5/4/3/3/4/3，合计28。对象级状态1个P0、5个P1、22个可用；P1不等于虚构，且“可用”不等于结论获证。
- 未完成且必须交接：P0作者修复由拥有者执行；V4异常日期原因；两HF模型页内容；K3固定版本/报告；MiTA逐版差异；H-MEM/HORMA来源生命周期；DynaKRAG补充材料/标签总成本；理论定理与强统计结论的全文复核；T08相关实验的重叠。**不把这些追查写成已完成。**
