# T04 首轮候选：查询条件访问、下钻与漏召回

日期：2026-11-08。**53个去重项 = 52篇论文/技术报告 + 1个官方模型仓库介绍；26项精读优先；全文精读0、代码核验0。**

## 使用说明

- A＝身份、作者元数据和原始摘要已核验；P＝在A之外定向核对了正文片段，并非全文精读；O＝官方仓库介绍已核验，不当论文计数。48项A、4项P、1项O。
- 以下“支持/反例潜力”是本轮初筛判断，不是已经建立的因果结论。“作者报告”与“本轮问题”分开；没有段落证据的机制细节不擅自补全。
- arXiv ID为去重键，版本号记录此次所见最新版；预印本、正式版、改标题与代码入口不重复计数。作者超过3人通常记首作者等；提交人不冒充作者。
- KV＝注意力键/值状态；RAG＝检索增强生成；gist＝用少量词元或文字保留一段内容要点的摘要表示；top-k＝选评分最高的固定数量项目，top-p＝按累计评分质量阈值决定选择数量；“地标”＝为一组内容提供路由入口的代表词元或查询；预填充＝处理已有输入前缀。这些是原作机制的中文说明，不登记新项目术语。
- 作品标题保留原文，以链接核验。所有“全文”均为公开入口，**不代表本轮已全文阅读**。

## A. 草案近期入口：独立核验，不从名称推断机制

### T04-001｜精读优先｜DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence
- **身份/版本**：DeepSeek-AI等，2026；arXiv:2606.19348v1。所见元数据公开日为2026-04-26，编号月份与该日期不一致，照录来源而不自行修正；必要时复核版本历史。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2606.19348v1)；[HTML](https://arxiv.org/html/2606.19348v1)；[PDF](https://arxiv.org/pdf/2606.19348v1)。**深度P：摘要、§2.3相关片段**。
- **机制关联**：CSA（压缩稀疏注意力）先把多个词元KV压成条目，再在**压缩条目**中选择；HCA（重压缩注意力）更强压缩后做稠密访问，另有局部滑窗。不能把这里的“dense”读成对全历史原始KV稠密访问。
- **支持/反例潜力**：支持压缩内容的查询条件路由；不自动支持“摘要定位后恢复远端原始细节”。后者与SSA/NSA的检索对象不同。
- **精读问题**：§2.3.1–2.3.4中选择对象、压缩比例和因果掩码如何定义？全局压缩能否回原始来源，还是只剩局部细节？HCA对CSA漏召回提供何种补偿？性能提升能否分离总参数、数据与结构效应？

### T04-002｜精读优先｜DeepSeek-V4.1-Flash: Pushing the Limits of KV Cache Compression
- **身份/版本**：DeepSeek-AI等，2026；arXiv:2609.19969v1，2026-09-17。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2609.19969v1)；[HTML](https://arxiv.org/html/2609.19969v1)；[PDF](https://arxiv.org/pdf/2609.19969v1)。**深度P：摘要和提取到的引言，方法章未读**。
- **机制关联**：CED（因果编码器—解码器）将解码器全局KV从编码器最终状态投影；CSA2（第二代压缩稀疏注意力）跨层共享全局KV/索引。引言列Full、Reindex、Reuse三模式：分别生成并索引、复用KV但重选索引、两者均复用；各层仍有自己的查询与局部滑窗KV。
- **支持/反例潜力**：说明“存什么”“每次重路由什么”“计算哪些层”可以分开；复用索引也可能因查询变化产生陈旧选择。SWA Bounded Replay是滑窗状态近似重建，不等于全局漏召回探索回退。
- **精读问题**：§2.2、§2.3.1–2.3.2的层间共享是否降低路由灵活性？层级索引何时漏选？§3.2.2重放保存何种原始输入、重建误差如何测？890 bytes/token的计数是否只含global KV，与持久化/局部状态边界如何区分？

### T04-003｜精读优先｜Mixture-of-Top-k Attention: Efficient Attention via Scalable Fast Weights
- **身份/版本**：Qishuai Wen、Zhiyuan Huang、Xianghan Meng等，2026；arXiv:2602.01219，v1—v6合并，最新v6为2026-09-27；Atom备注NeurIPS2026，未另核会议终稿。
- **原始来源/全文**：[摘要v6](https://arxiv.org/abs/2602.01219v6)；[PDF](https://arxiv.org/pdf/2602.01219v6)；[官方代码入口](https://github.com/QishuaiWen/MiTA)。**深度A**。
- **机制关联**：MiTA（Top-k注意力混合）由少量地标查询收集可复用、形状不固定的KV集合，并保留压缩共享分支；从固定块专家转向可变集合。早期版本题名为Efficient Fast-Weight Scaling via a Mixture of Top-k Activations，按同一ID计一项。
- **支持/反例潜力**：接近“压缩全局+稀疏细节”的组合；摘要实验是**视觉任务**，不是已证实的因果语言建模方案。
- **精读问题**：地标查询收集集合时是否看未来？动态集合构造是否仍全扫原始键？共享压缩分支能否补救未入专家的细节？v1与v6机制/评价是否实质变化？

### T04-004｜Kimi K3 官方模型介绍（非论文）
- **身份/版本**：MoonshotAI，2026；稳定仓库[MoonshotAI/Kimi-K3](https://github.com/MoonshotAI/Kimi-K3)。本轮未固定commit；不以搜索到的首次日期作为可靠发布日期。**深度O：README和报告链接，PDF未读、代码未审**。
- **原始来源/全文**：[官方介绍](https://github.com/MoonshotAI/Kimi-K3)；浏览器确认的[报告PDF入口](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)。不将README与PDF另计两项。
- **机制关联**：官方当前介绍为2.8T总参数、69层KDA（Kimi Delta Attention，门控递归状态注意力）+24层Gated MLA（门控多头潜在注意力），含AttnRes与潜在专家路由。这里只确认介绍存在和公开表述。
- **支持/反例潜力**：可作为递归/全局访问混合的系统参照；**不能凭“1M上下文”或专家路由断言其含摘要下钻、来源回访、CSA式上下文路由**。参数专家路由不等于历史地址路由。
- **下一步**：固定仓库版本、读真实报告中注意力/记忆/压缩章节，再决定T04相关性；性能表和媒体介绍不背书。官方报告内容目前仍不可得于本轮阅读。

## B. 最近邻组合：摘要、层级、来源回访

### T04-005｜精读优先｜RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval
- **身份/版本**：Parth Sarthi、Salman Abdullah、Aditi Tuli等，2024；arXiv:2401.18059v1；搜索关联ICLR2024，[OpenReview](https://openreview.net/forum?id=GN921JHCRw)本轮遇验证墙，未独立核对正式页面正文。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2401.18059v1)；[PDF](https://arxiv.org/pdf/2401.18059v1)。**深度A**。
- **机制关联**：递归嵌入、聚类、总结构成多级摘要树；查询时跨抽象层检索。
- **支持/反例潜力**：多粒度索引的重要近邻；“建树”不必意味着部署时只沿单一路径下钻，须核对检索模式，不把所有结果归因顶向下搜索。
- **精读问题**：树遍历与跨层平铺检索各贡献多少？召回的是原始叶片还是生成摘要？父节点遗漏能否被独立叶检索绕过？索引生成成本与来源映射如何计算？

### T04-006｜Retrieval-Augmented Generation with Hierarchical Knowledge（HiRAG）
- **身份/版本**：Haoyu Huang等，2025；arXiv:2503.10150v3；Atom备注EMNLP2025 Findings，早期题名含HiRAG前缀，同一作品。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2503.10150v3)；[PDF](https://arxiv.org/pdf/2503.10150v3)。**深度A**。
- **机制关联**：用层级知识加强知识图索引和检索，主张改善语义与结构捕获。
- **支持/反例潜力**：支持跨层语义关联候选；摘要不足以确认原文来源回访与丢失信息恢复。应核对层级图是不是比层级摘要更能覆盖长尾证据。

### T04-007｜精读优先｜Simplified Sparse Attention via Gist Tokens
- **身份/版本**：Yuzhen Mao、Michael Y. Li、Emily B. Fox，2026；arXiv:2604.20920v2，2026-06-26。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2604.20920v2)；[HTML](https://arxiv.org/html/2604.20920v2)；[PDF](https://arxiv.org/pdf/2604.20920v2)。**深度P：摘要、图1、§3.5–3.6及部分方法检索片段**。
- **机制关联**：SSA（简化稀疏注意力）先以插入式gist词元和受限掩码续训，再按查询对gist评分，展开被选块的**原始KV**；H-SSA（层级变体）增加gist-of-gist，由粗到细筛选原始块。是本轮最接近“多粒度压缩+来源回访”的架构级近邻。
- **支持/反例潜力**：支持摘要路由与精细恢复组合；作者报告比压缩/推理稀疏基线好，不等于对任意问题保召回。§3.5的对数路由推导与§3.6的线性元数据扫描需分开核算。
- **精读问题**：原始KV保存在哪里、生命周期多长？固定top-k漏选是否有重试/扩预算？gist训练是否得到细节可检索性监督？多层原始读取的因果可见性如何保证？§3.6明确有O(n)元数据压紧扫描，完整实现成本能否仍称对数每步？首层不做展开、分组查询共享选择的影响是什么？

### T04-008｜精读优先｜AttentionIndex: Accelerating Learned Sparse Attention with a Causal Inverted-File Index
- **身份/版本**：Jeongmin Brian Park、Wen-mei Hwu，2026；arXiv:2611.02508v1，2026-11-02。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2611.02508v1)；[PDF](https://arxiv.org/pdf/2611.02508v1)。**深度A**。
- **机制关联**：将索引键按相似性分组，用倒排索引粗筛，再用原索引器细评分；预填充期间动态建索引，只向查询暴露其前缀形成的簇。
- **支持/反例潜力**：摘要直接指出连续块两阶段筛选在固定候选预算下随长度增长丢召回；作者报告百万上下文相对HiSA更高top-k召回与任务准确率，是对块代表路由的重要挑战。
- **精读问题**：聚簇/维护/重用是否计入吞吐？前缀因果性如何保证？不同候选预算下是质量、延迟还是两者对齐？HiSA基线对应HISA哪个版本？遗漏高值但低相似性的键能否被发现？

### T04-009｜精读优先｜Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention
- **身份/版本**：Jingyang Yuan等，2025；arXiv:2502.11089v2。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2502.11089v2)；[PDF](https://arxiv.org/pdf/2502.11089v2)。**深度A**。
- **机制关联**：NSA（原生稀疏注意力）动态层级策略，组合粗粒度词元压缩、细粒度选择，强调端到端训练和硬件匹配。
- **支持/反例潜力**：不能把“压缩+选择”作为未经比较的新增机制；压缩分支与细读分支提供可分离对照。
- **精读问题**：压缩评分如何传给选择、各分支梯度/门控如何训练？全局压缩分支能否挽救未被选中的细节？平均任务持平是否掩盖罕见事实漏召回？原始KV常驻成本计入哪里？

### T04-010｜精读优先｜MoBA: Mixture of Block Attention for Long-Context LLMs
- **身份/版本**：Enzhe Lu等，2025；arXiv:2502.13189v1。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2502.13189v1)；[PDF](https://arxiv.org/pdf/2502.13189v1)。**深度A**。
- **机制关联**：MoBA（块注意力混合）把专家路由原则用于上下文块选择，强调减少预设局部结构、可在全/稀疏注意力间切换。
- **支持/反例潜力**：查询条件块路由的强基线；块代表并不等价于未来任务充分摘要。
- **精读问题**：块代表是否均值池化、路由学习信号是什么？块内少数关键键会否被平均淹没？与SSA、MiTA比较时固定块边界、集合重用、选择成本分别贡献多少？所谓切换是预定义日程还是可触发的在线回退？

### T04-011｜精读优先｜Quest: Query-Aware Sparsity for Efficient Long-Context LLM Inference
- **身份/版本**：Jiaming Tang等，2024；arXiv:2406.10774v2；元数据关联ICML2024，合并计数。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2406.10774v2)；[PDF](https://arxiv.org/pdf/2406.10774v2)。**深度A**。
- **机制关联**：为KV页保存逐维键的最小/最大值，用当前查询估计页重要性，只加载top-k页。
- **支持/反例潜力**：提供不靠自然语言摘要的粗评分；保留原KV使后续查询仍有回访机会，与永久逐出对照不同。
- **精读问题**：页上界有何严格保证，top-k截断又损失何种保证？最坏情况边界松弛会否全扫？多页证据聚合、查询分布变化时召回如何？论文摘要中的2.23倍注意力与7.03倍总体延迟来自什么不同配置？

### T04-012｜SparQ Attention: Bandwidth-Efficient LLM Inference
- **身份/版本**：Luka Ribar等，2023/2024；arXiv:2312.04985v6，初稿2023、更新2024，按一项计。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2312.04985v6)；[PDF](https://arxiv.org/pdf/2312.04985v6)。**深度A**。
- **机制关联**：选择性取得历史缓存以降低传输，无需重训。作为查询/特征维近似评分后读取完整KV的经典比较入口；细节须全文确认。
- **支持/反例潜力**：支持区分“节省访问带宽”与“删除存储”；8倍传输减少是作者摘要报告，不作跨硬件保证。后续核查近似评分误排与最终输出误差关系。

### T04-013｜精读优先｜RetrievalAttention: Accelerating Long-Context LLM Inference via Vector Retrieval
- **身份/版本**：Di Liu等，2024；arXiv:2409.10516v3。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2409.10516v3)；[PDF](https://arxiv.org/pdf/2409.10516v3)。**深度A**。
- **机制关联**：CPU保存KV并建近似最近邻索引，在生成期间取相关KV；特别处理查询与键的分布不一致。
- **支持/反例潜力**：说明一般向量检索不能直接视作可靠注意力检索；原始KV可得与索引召回是两个条件。
- **精读问题**：注意力感知索引如何处理查询—键分布差异？建索引是否读未来查询或离线校准？CPU/GPU搬运、索引重建和缓存命中计入什么成本？ANN漏召回是否有可检测或可修复指标？

### T04-014｜InfLLM: Training-Free Long-Context Extrapolation for LLMs with an Efficient Context Memory
- **身份/版本**：Chaojun Xiao等，2024；arXiv:2402.04617v2。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2402.04617v2)；[PDF](https://arxiv.org/pdf/2402.04617v2)。**深度A**。
- **机制关联**：将远端上下文存为附加记忆单元，再按词元相关性查找用于注意力，不做额外训练。
- **支持/反例潜力**：来源还在、只限制活跃视野的比较方案；长序列外推不等于无限可靠检索。下一步核实单元代表/块召回/原始KV保存与重加载，以及相关性评分是否遗漏潜在多跳证据。

### T04-015｜精读优先｜DashAttention: Differentiable and Adaptive Sparse Hierarchical Attention
- **身份/版本**：Yuxiang Huang、Nuno M. T. Gonçalves、Federico Alvetreti等，2026；arXiv:2605.18753v1。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2605.18753v1)；[PDF](https://arxiv.org/pdf/2605.18753v1)。**深度A**。
- **机制关联**：用α-entmax（可产生精确零权重的概率变换）选择随查询变化的块数，并将粗层结果作为细层softmax的先验，试图让整条层级可微。
- **支持/反例潜力**：针对固定top-k预算与粗细层梯度断裂的明确竞争方法；“non-dispersive”是原作属性名称，暂不当普遍不漏召回定理。
- **精读问题**：可微覆盖的到底是选择概率、被选块内容还是所有路径？不分散性质假设及其与召回的关系？动态块数的最坏成本是什么？摘要速度数值提取缺失，必须查原表，不能自行补数。

### T04-016｜精读优先｜HiKEY: Hierarchical Multimodal Retrieval for Open-Domain Document Question Answering
- **身份/版本**：Joongmin Shin、Gyuho Shim、Jeongbae Park等，2026；arXiv:2605.29606v1；元数据标注ACL2026 Main，尚未核正式页。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2605.29606v1)；[PDF](https://arxiv.org/pdf/2605.29606v1)。**深度A**。
- **机制关联**：恢复文档父子结构，先全局路由，再多模态段落细检，最后在词元预算内打包证据子图。
- **支持/反例潜力**：来源结构+粗细访问的近邻；摘要明确把错文档路由与证据碎片化分成两类瓶颈。
- **精读问题**：全局入口使用何种摘要/文档卡，是否错过未写进卡片的数值细节？结构恢复错误如何传播？12.9%召回增益与6.8%问答增益的分母/口径、成本、各消融是什么？失败时可否跨父节点回退？

### T04-017｜精读优先｜Semantic Compression Trees: Multi-Resolution Knowledge Retrieval via Hierarchical Semantic Residuals
- **身份/版本**：Junaid Farooq，2026；arXiv:2608.21610v1。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2608.21610v1)；[HTML](https://arxiv.org/html/2608.21610v1)；[PDF](https://arxiv.org/pdf/2608.21610v1)。**深度P：摘要与§7 Analysis**。
- **机制关联**：SCT（语义压缩树）各节点只存比父节点新增的语义内容，沿树下钻。作者把“已给文档”与“需选文档”两种协议分开。
- **支持/反例潜力**：**直接反例优先**。摘要报告需选文档时，顶向下文档路由20.2%，平面检索39.3%；问答F1 0.122 vs 0.165。§7固定残差改为平面检索后路由0.202→0.347，F1 0.122→0.147；说明本设定中残差表示与树遍历不能合并判功过。
- **精读问题**：50篇/173问的样本、统计与文档拆分有何局限？根摘要只1–2句是否公平比较多槽/多入口？“适用于任何严格顶向下索引”的泛化是作者解释，是否有定理或跨任务数据支持？摘要改写的逐字证据召回下降是否混淆语义保留？平面选文档后树内粒度控制是作者未评估建议，不能当结果。

### T04-018｜精读优先｜Twilight: Adaptive Attention Sparsity with Hierarchical Top-p Pruning
- **身份/版本**：Chaofan Lin、Jiaming Tang、Shuo Yang等，2025；arXiv:2502.02770v5，最新2025-11-04（早于近12个月窗口4天）；元数据备注NeurIPS2025 spotlight。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2502.02770v5)；[PDF](https://arxiv.org/pdf/2502.02770v5)。**深度A**。
- **机制关联**：把累计注意力质量阈值用于自适应稀疏预算，替代固定数量。
- **支持/反例潜力**：动态预算和回退的算法入口；保留高注意力质量不一定保住少量低注意力但因果必需的事实。
- **精读问题**：质量阈值如何在未算全注意力时估计，保证来自何处？阈值欠校准/平坦注意力时是否扩到全量？尾部遗漏的输出误差和长程多步误差如何界定？层级初筛已丢的项能否被top-p再发现？

### T04-019｜InfLLM-V2: Dense-Sparse Switchable Attention for Seamless Short-to-Long Adaptation
- **身份/版本**：Weilin Zhao等，2025；arXiv:2509.24663v1，2025-09-29。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2509.24663v1)；[PDF](https://arxiv.org/pdf/2509.24663v1)。**深度A**。
- **机制关联**：重用稠密注意力参数，短输入用稠密、长输入切稀疏；强调兼容先短预训练后长微调。
- **支持/反例潜力**：挑战“必须新参数/从头稀疏训练”的假设。作者对NSA收敛/开销的批评只是作者定位，需同预算比较；长度切换不等于在线不确定性回退。

### T04-020｜精读优先｜Block Sparse Attention with Log-Linear Complexity
- **身份/版本**：Bohao Tang、Zhen Qin、Yuqi Pan等，2026；arXiv:2609.31093v1。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2609.31093v1)；[PDF](https://arxiv.org/pdf/2609.31093v1)。**深度A**。
- **机制关联**：PISA（原作给出的金字塔选择方法名）把键池化成粗细层级，每层只对有界候选以LogSumExp评分并top-k，提出O(N log N)总复杂度。
- **支持/反例潜力**：非常接近层级筛选；早期层的错剪能否挽回是关键。注意PISA也被别的检索软件用作名称，按本arXiv ID区分。
- **精读问题**：LogSumExp如何从池化代表估计块内强键？有界候选下是否有召回保证？复杂度包含池化、掩码、重排和训练反传吗？多针、低词面重叠、跨块聚合时是否失效？

### T04-021｜HiQA: A Hierarchical Contextual Augmentation RAG for Multi-Documents QA
- **身份/版本**：Xinyue Chen、Pengyu Gao、Jiangjiang Song等，2024；arXiv:2402.01767v4；2026-08-25更新备注为作者元数据修正，与v3正文不变，不计新方法。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2402.01767v4)；[PDF](https://arxiv.org/pdf/2402.01767v4)。**深度A**。
- **机制关联**：为文本块加标题、段落路径等层级上下文，结合语义、词法、关键词/实体多路检索。
- **支持/反例潜力**：来源路径可能防止相似文档误路由；多路检索是逃出单一语义评分盲点的候选。不是已经证明的摘要树下钻，需核对是否真的先剪父节点。

### T04-022｜From RAG to Memory: Non-Parametric Continual Learning for Large Language Models（HippoRAG 2）
- **身份/版本**：Bernal Jiménez Gutiérrez、Yiheng Shu、Weijian Qi等，2025；arXiv:2502.14802v2；元数据关联ICML2025。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2502.14802v2)；[PDF](https://arxiv.org/pdf/2502.14802v2)。**深度A**。
- **机制关联**：在图上做个性化PageRank（从查询关联节点出发的带重启随机游走），更深整合段落与在线模型使用。
- **支持/反例潜力**：作者指出先前图RAG改善关联但牺牲基本事实记忆；该权衡本身必须保留。图扩散可能找到不与查询直接相似的证据，但也可能带入干扰；不能按图标签直接认定无漏召回。

### T04-023｜精读优先｜HISA: Efficient Hierarchical Indexing for Fine-Grained Sparse Attention
- **身份/版本**：Yufei Xu、Fanxu Meng、Fan Jiang等，2026；arXiv:2603.28458v5，最新2026-11-03；元数据标注COLM2026。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2603.28458v5)；[PDF](https://arxiv.org/pdf/2603.28458v5)。**深度A**。
- **机制关联**：以池化块代表做粗筛，再只对保留块运行原词元级索引器，替换全历史扫描，无需微调。
- **支持/反例潜力**：支持把“选择的选择”层级化；与AttentionIndex构成直接支持/挑战对。摘要说保留同样词元稀疏模式，不能擅自理解为对所有查询精确返回同一top-k集合。
- **精读问题**：v1—v5何处改动？如何选择池化与候选预算，误筛何时发生？AttentionIndex使用的HiSA究竟哪个版本与实现？摘要速度数字缺失，去原表核验，不补写。是否存在失败后扩大候选池？

### T04-024｜From Local to Global: A Graph RAG Approach to Query-Focused Summarization
- **身份/版本**：Darren Edge等，2024；arXiv:2404.16130v2，更新2025。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2404.16130v2)；[PDF](https://arxiv.org/pdf/2404.16130v2)。**深度A**。
- **机制关联**：GraphRAG先建实体图及社区摘要，再按问题生成局部响应并汇总；主要面向全局理解问题。
- **支持/反例潜力**：与细节检索互补，不能把全局主题覆盖改善外推为精确数字召回。应核对作者查询时是否遍历全部社区摘要，而非低成本层级导航。

### T04-025｜Multiple Abstraction Level Retrieve Augment Generation
- **身份/版本**：Zheng Zheng、Xinyi Ni、Pengyu Hong，2025；arXiv:2501.16952v1。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2501.16952v1)；[PDF](https://arxiv.org/pdf/2501.16952v1)。**深度A**。
- **机制关联**：MAL（多抽象级别检索）同时使用多句、段、节、文档级块，面向糖科学问答。
- **支持/反例潜力**：检索粒度不应固定的实证候选；摘要的25.739%是AI评判的领域问答正确性，不能当一般召回率提升。须核实有无查询条件粒度决策及原始证据链接。

## C. 永久裁剪与预填充近似：不可混同可回访稀疏访问

### T04-026｜H₂O: Heavy-Hitter Oracle for Efficient Generative Inference of Large Language Models
- **身份/版本**：Zhenyu Zhang等，2023；arXiv:2306.14048v3。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2306.14048v3)；[PDF](https://arxiv.org/pdf/2306.14048v3)。**深度A**。
- **机制关联**：平衡最近词元与高累计注意力词元的缓存逐出策略，摘要称有温和假设下的动态次模保证。
- **支持/反例潜力**：反事实基线：过去不重要不代表未来不需要；永久逐出后原KV是否仍可重建，必须与“只是不访问”分清。理论保证不自动等价于任意未来任务充分性。

### T04-027｜SnapKV: LLM Knows What You are Looking for Before Generation
- **身份/版本**：Yuhong Li等，2024；arXiv:2404.14469v2。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2404.14469v2)；[PDF](https://arxiv.org/pdf/2404.14469v2)。**深度A**。
- **机制关联**：从输入末端观察窗推断各头关注位置，聚合重要KV并压缩缓存，无需微调。
- **支持/反例潜力**：对“查询已经充分给定”的预选择可能有效；多轮后续问题改题时的观察窗盲区值得反证，不预设其为完全查询无关。

### T04-028｜Efficient Streaming Language Models with Attention Sinks
- **身份/版本**：Guangxuan Xiao等，2023/2024；arXiv:2309.17453v4；元数据关联ICLR2024。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2309.17453v4)；[PDF](https://arxiv.org/pdf/2309.17453v4)。**深度A**。
- **机制关联**：StreamingLLM保留起始注意力汇聚词元和有限窗口，恢复流式语言建模稳定性。
- **支持/反例潜力**：稳定处理百万级流不等于读取任意旧事实；注意力汇聚词元不因高注意力就有语义重要性，是高分代理与内容效用分离的经典提醒。

### T04-029｜MInference 1.0: Accelerating Pre-filling for Long-Context LLMs via Dynamic Sparse Attention
- **身份/版本**：Huiqiang Jiang等，2024；arXiv:2407.02490v2；元数据关联NeurIPS2024 spotlight。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2407.02490v2)；[PDF](https://arxiv.org/pdf/2407.02490v2)。**深度A**。
- **机制关联**：为头离线选择A形、纵斜线、块稀疏模式，在线生成稀疏索引以加速预填充。
- **支持/反例潜力**：代表“先以少量信号预测注意力支持集”的比较线；它省预填充计算，不直接提供生成期间的原始来源回访/回退。预填充漏读的状态误差会否传到后续路由需核查。

### T04-030｜FlexPrefill: A Context-Aware Sparse Attention Mechanism for Efficient Long-Sequence Inference
- **身份/版本**：Xunhao Lai等，2025；arXiv:2502.20766v1；元数据关联ICLR2025 Oral。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2502.20766v1)；[PDF](https://arxiv.org/pdf/2502.20766v1)。**深度A**。
- **机制关联**：按查询/头动态选择稀疏模式与预算，利用散度和累计注意力阈值，而非一律固定掩码。
- **支持/反例潜力**：自适应计算预算先例；须核查用于估计累计质量的样本是否足以发现稀有事实，估计失败时是否可退到稠密。

### T04-031｜XAttention: Block Sparse Attention with Antidiagonal Scoring
- **身份/版本**：Ruyi Xu、Guangxuan Xiao、Haofeng Huang等，2025；arXiv:2503.16428v1。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2503.16428v1)；[PDF](https://arxiv.org/pdf/2503.16428v1)。**深度A**。
- **机制关联**：用注意力块反对角线分数作为块重要性代理，保留关键区域。
- **支持/反例潜力**：无需语义摘要的稀疏块筛选对照；采样几何可能遗漏偏离样本位置的强关联。13.5倍是作者注意力计算加速，不是全系统加速保证。

## D. 探索、纠错、策略升级与相反结果

### T04-032｜精读优先｜Corrective Retrieval Augmented Generation
- **身份/版本**：Shi-Qi Yan、Jia-Chen Gu、Yun Zhu、Zhen-Hua Ling，2024；arXiv:2401.15884v3。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2401.15884v3)；[PDF](https://arxiv.org/pdf/2401.15884v3)。**深度A**。
- **机制关联**：CRAG（纠错检索增强生成）评估已取文档质量，按置信度触发不同知识访问动作，包括网络扩检和分解重组证据。
- **支持/反例潜力**：显式回退先例；回退是否成功取决于能否发现“看似相关但漏关键”的情形。
- **精读问题**：评价器能否在没有金标准时诊断漏召回，而不只是无关文本？误接受率和误触发成本如何？回退访问域扩大与只增加同一索引预算的效果能分离吗？

### T04-033｜Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection
- **身份/版本**：Akari Asai等，2023；arXiv:2310.11511v1。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2310.11511v1)；[PDF](https://arxiv.org/pdf/2310.11511v1)。**深度A**。
- **机制关联**：通过反思词元学习何时检索、检索内容是否相关、生成是否有支持，推理阶段可调控制。
- **支持/反例潜力**：访问与效用判断可学习的先例；自评“不需检索”在自信错误时可能阻断探索。后续核验反思训练标签、成本与置信校准，不把自反思当可靠性证明。

### T04-034｜Active Retrieval Augmented Generation
- **身份/版本**：Zhengbao Jiang等，2023；arXiv:2305.06983v2；元数据关联EMNLP2023。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2305.06983v2)；[PDF](https://arxiv.org/pdf/2305.06983v2)。**深度A**。
- **机制关联**：FLARE（前瞻主动检索增强生成）预生成下一句，以低置信词元触发检索并重生成该句。
- **支持/反例潜力**：查询随加工结果改变，而非一次路由终身固定；低置信能抓未知，却可能抓不住高置信错答。需要可控的“自信但遗漏来源”反例评价。

### T04-035｜Adaptive-RAG: Learning to Adapt Retrieval-Augmented Large Language Models through Question Complexity
- **身份/版本**：Soyeong Jeong等，2024；arXiv:2403.14403v2；元数据关联NAACL2024。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2403.14403v2)；[PDF](https://arxiv.org/pdf/2403.14403v2)。**深度A**。
- **机制关联**：用较小模型分类问题复杂度，在不检索、单步、迭代检索之间选择，标签来自模型实际结果和数据偏置。
- **支持/反例潜力**：预算分级/访问策略路由先例；标签可能学习题面难度而非当前记忆必要性，未必能诊断摘要里丢了什么。

### T04-036｜精读优先｜Retrieval Augmented Generation or Long-Context LLMs? A Comprehensive Study and Hybrid Approach
- **身份/版本**：Zhuowan Li、Cheng Li、Mingyang Zhang等，2024；arXiv:2407.16833v2；元数据关联EMNLP2024 Industry。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2407.16833v2)；[PDF](https://arxiv.org/pdf/2407.16833v2)。**深度A**。
- **机制关联**：Self-Route（自反思路由）在低成本RAG和完整长上下文处理之间分流。
- **支持/反例潜力**：相反结果：作者报告充分资源下长上下文平均优于RAG，但检索成本低；支持将全量读取保留为策略升级而不是宣告检索万能。
- **精读问题**：路由何时错误地接受RAG？全上下文“回退”能否识别漏召回且不使用答案信息？成本包括所有反思、重复调用与长上下文编码吗？当前更强模型是否改变此权衡？

### T04-037｜Interleaving Retrieval with Chain-of-Thought Reasoning for Knowledge-Intensive Multi-Step Questions
- **身份/版本**：Harsh Trivedi等，2022预印本/2023正式版；arXiv:2212.10509v2；元数据注明ACL2023 camera-ready，计1项。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2212.10509v2)；[PDF](https://arxiv.org/pdf/2212.10509v2)。**深度A**。
- **机制关联**：IRCoT（检索与思维链交错）用中间推理改变下一步检索，再用所得证据修正推理。
- **支持/反例潜力**：单步查询并不足以暴露所有相关信息；有序探索可逐渐揭露关联。但早期错误推理也可能导向错误检索闭环，需分离检索召回与回答改善。

### T04-038｜精读优先｜A-RAG: Scaling Agentic Retrieval-Augmented Generation via Hierarchical Retrieval Interfaces
- **身份/版本**：Mingxuan Du、Benfeng Xu、Chiwei Zhu等，2026；arXiv:2602.03442v1。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2602.03442v1)；[PDF](https://arxiv.org/pdf/2602.03442v1)。**深度A**。
- **机制关联**：直接给模型关键词搜索、语义搜索、块读取三类工具，使其自行选择不同粒度的访问，不预设单次召回或固定流程。
- **支持/反例潜力**：多粒度接口+按需原块读取的系统级最近邻；摘要的“hierarchical”是接口层次，不应未经核验就说是层级压缩树。
- **精读问题**：细读工具能否访问未通过摘要筛选的块？探索策略是否有额外训练，还是依靠基础模型？同检索词元预算是否漏算多轮推理/索引开销？失败时是否扩范围、回父级或重新表述查询？

### T04-039｜精读优先｜Keep It InMind: Benchmarking the Implicit-Association Blind Spot in Agent Memory
- **身份/版本**：Ruizhe Li、Mingxuan Du、Benfeng Xu、Zhendong Mao，2026；arXiv:2607.24368v1。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2607.24368v1)；[PDF](https://arxiv.org/pdf/2607.24368v1)。**深度A**。
- **机制关联**：InMind（隐含关联记忆基准）将存储遗漏、桥接知识不足、已存但未取出三类错误分开；例为坚果过敏与马卡龙需求之间经杏仁原料连接。
- **支持/反例潜力**：强反例：作者摘要报告直接可见记忆时84.0%，通过六类记忆系统检索时最高14.4%；更高维嵌入提升检索指标但未消除问答缺口。挑战“相关事实必与查询相似”。
- **精读问题**：125题/113有外部出处的来源与配对控制是否足够独立？把记忆置前的诊断是否改变提示或计算？能否区别路由召回、语义桥接与因果使用？是否能设计不使用答案的探索策略修复？

### T04-040｜精读优先｜What Does Context Compression Cost an Agent? Interaction Costs Unrevealed by Task-Completion Metrics
- **身份/版本**：Shuyu Liu，2026；arXiv:2608.16370v1。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2608.16370v1)；[PDF](https://arxiv.org/pdf/2608.16370v1)。**深度A**。
- **机制关联**：用受控状态删除/保留/恢复，测压缩造成的重新取得信息成本，把检索调用与执行调用分开。
- **支持/反例潜力**：作者报告5倍压缩时完成率变化不显著但检索调用增加；另一个ALFWorld环境未见检索激增，说明**回访成本依环境而变**，不能一概判定压缩坏或回访免费。
- **精读问题**：固定24轮上限是否隐藏溢出失败？恢复干预是何种oracle，随机保留为何可与事后oracle相当？任务完成统计不显著是否真的等效？如何把重新编码/工具往返/等待时间纳入完整成本？

### T04-041｜Maximising Transparency in Context Compaction Improves Retention of Facts and Commitments for Lightweight Coding Agents
- **身份/版本**：Felix Woolford，2026；arXiv:2610.20116v1。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2610.20116v1)；[PDF](https://arxiv.org/pdf/2610.20116v1)。**深度A**。
- **机制关联**：transparent-compact（透明压缩）保留用户/助手原文，显式标记信息被移除的位置，对比模型写摘要与另一确定性压缩。
- **支持/反例潜力**：让模型知道“有内容丢失”或有助降低自信错误，是回退触发的辅助信号；不是已证明会恢复丢掉内容。核实预算匹配、原文保留量和任务是否偏向规则记忆。

## E. 评价、经典索引与必须回溯的早期近邻

### T04-042｜Lost in the Middle: How Language Models Use Long Contexts
- **身份/版本**：Nelson F. Liu等，2023；arXiv:2307.03172v3；元数据注明TACL接受，正式出版年份本轮未另核，不能用搜索网页更新日期代替。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2307.03172v3)；[PDF](https://arxiv.org/pdf/2307.03172v3)。**深度A**。
- **机制关联**：多文档问答与键值检索中改变证据位置，发现中间位置易退化。
- **支持/反例潜力**：证据在上下文中也不保证被消费，原始回访成功不能替代回答因果使用测试。不是针对摘要路由的直接定理。

### T04-043｜精读优先｜NoLiMa: Long-Context Evaluation Beyond Literal Matching
- **身份/版本**：Ali Modarressi等，2025；arXiv:2502.05167v3；元数据注明ICML2025。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2502.05167v3)；[PDF](https://arxiv.org/pdf/2502.05167v3)。**深度A**。
- **机制关联**：用问题与证据最小词面重叠，逼模型通过潜在关联查找证据，而非依赖字串匹配。
- **支持/反例潜力**：作者报告32K时多数模型低于自身短窗成绩的一半；适合检验摘要/索引错过罕见关联，而非只测针形复制。
- **精读问题**：关联必须由模型已有知识补齐吗？怎样分离桥接知识不足与长窗路由错误？基准中多跳、干扰、位置与词面重叠轴能否独立控制？全文方法是否允许原始数据授权复用？

### T04-044｜RULER: What's the Real Context Size of Your Long-Context Language Models?
- **身份/版本**：Cheng-Ping Hsieh等，2024；arXiv:2404.06654v3；元数据注明COLM2024。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2404.06654v3)；[PDF](https://arxiv.org/pdf/2404.06654v3)。**深度A**。
- **机制关联**：可调长度、针数、多跳追踪和聚合，超越单针搜索。
- **支持/反例潜力**：对比平均回访与多证据完整召回；需与NoLiMa/InMind互补，不能以合成字面匹配成功免除隐含关联挑战。

### T04-045｜ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT
- **身份/版本**：Omar Khattab、Matei Zaharia，2020；arXiv:2004.12832v2；元数据注明SIGIR2020。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2004.12832v2)；[PDF](https://arxiv.org/pdf/2004.12832v2)。**深度A**。
- **机制关联**：查询/文档独立编码，但保留细粒度词元表示以做后期交互，避免过早压成单向量。
- **支持/反例潜力**：多向量是对单摘要失明的重要对照；支持“地址表示细化”而不一定支持建摘要树。下一步核查索引存储与细节覆盖的完整权衡。

### T04-046｜PLAID: An Efficient Engine for Late Interaction Retrieval
- **身份/版本**：Keshav Santhanam、Omar Khattab、Christopher Potts、Matei Zaharia，2022；arXiv:2205.09707v1；搜索关联ACM DOI `10.1145/3511808.3557325`，不把2025网页日期另计新论文。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2205.09707v1)；[PDF](https://arxiv.org/pdf/2205.09707v1)；[DOI入口](https://doi.org/10.1145/3511808.3557325)（本轮未Fetch该DOI）。**深度A**。
- **机制关联**：用质心交互与质心裁剪快速筛低分段落，再进行晚交互检索。
- **支持/反例潜力**：粗压缩代理筛选后细评分的经典系统近邻；应看何种压缩和裁剪规则能保持召回，不能只拿语义摘要作唯一粗表示。

### T04-047｜Memorizing Transformers
- **身份/版本**：Yuhuai Wu、Markus N. Rabe、DeLesley Hutchins、Christian Szegedy，2022；arXiv:2203.08913v1；元数据注明ICLR2022 spotlight。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2203.08913v1)；[PDF](https://arxiv.org/pdf/2203.08913v1)。**深度A**。
- **机制关联**：对过去内部KV做非可微近似近邻查询，模型不需通过参数更新才能利用新定义。
- **支持/反例潜力**：保存内容与查询地址分离的早期基线；记忆增大而语言建模改善不代表任意稀有事实可召回。需核查索引陈旧、梯度、近邻近似与原始来源可追溯程度。

### T04-048｜Efficient Content-Based Sparse Attention with Routing Transformers
- **身份/版本**：Aurko Roy、Mohammad Saffar、Ashish Vaswani、David Grangier，2020；arXiv:2003.05997v5；元数据注明TACL2020。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2003.05997v5)；[PDF](https://arxiv.org/pdf/2003.05997v5)。**深度A**。
- **机制关联**：在线k-means（按向量距离动态分簇）学习内容稀疏路由，结合局部注意力。
- **支持/反例潜力**：避免把内容路由称作近期才出现；训练/推理因果聚簇、桶容量与簇边缘错误是与2026倒排索引比较的重要轴。

### T04-049｜精读优先｜Landmark Attention: Random-Access Infinite Context Length for Transformers
- **身份/版本**：Amirkeivan Mohtashami、Martin Jaggi，2023；arXiv:2305.16300v2；元数据与搜索关联NeurIPS2023正式版，标题亦见Random-Access Infinite Context Length for Transformers，合并计1项。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2305.16300v2)；[PDF](https://arxiv.org/pdf/2305.16300v2)；[正式版PDF](https://proceedings.neurips.cc/paper_files/paper/2023/file/ab05dc8bf36a9f66edbff6992ec86f56-Paper-Conference.pdf)（搜索所见，未Fetch正文）。**深度A**。
- **机制关联**：每块加入地标词元，训练注意力利用地标选择相关块，再读取完整上下文中的相应部分，保留随机访问能力。
- **支持/反例潜力**：架构级“块代表+来源块检索”的早期最近邻，优先于把SSA/NSA称起点。
- **精读问题**：路由概率的归一化/分组如何与普通注意力兼容？训练信号能否使代表保留未来查询可检索性？所称任意长是地址能力、储存能力还是实测成功？冷存取、位置外推、错选后的回退分别如何处理？

### T04-050｜精读优先｜A Human-Inspired Reading Agent with Gist Memory of Very Long Contexts
- **身份/版本**：Kuang-Huei Lee、Xinyun Chen、Hiroki Furuta、John Canny、Ian Fischer，2024；arXiv:2402.09727v3；正式版ICML2024/PMLR235:26396–26415，与预印本计1项。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2402.09727v3)；[PMLR正式摘要](https://proceedings.mlr.press/v235/lee24c.html)；[PDF](https://arxiv.org/pdf/2402.09727v3)。**深度A：两份摘要核验，不是全文精读**。
- **机制关联**：ReadAgent（要点记忆阅读代理）自己分页、生成gist、必要时查回原文段落；无须将每次访问全部内容保持在活跃上下文。
- **支持/反例潜力**：**系统级最接近“多粒度+来源回访”之一**。作者报告有效上下文3.5–20倍扩展；这是实验结果，不是全域保证，也未说明所有索引/摘要成本均计入该倍数。
- **精读问题**：摘要未包含查询线索时为何/何时仍会回看正确页？顺序/并行回查、最大页数、搜索失败停止规则是什么？分页和摘要成本单问与多问如何摊销？原文删除/修订会怎样影响地址有效性？

### T04-051｜Augmenting Language Models with Long-Term Memory
- **身份/版本**：Weizhi Wang等，2023；arXiv:2306.07174v1。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2306.07174v1)；[PDF](https://arxiv.org/pdf/2306.07174v1)。**深度A**。
- **机制关联**：LongMem（长时记忆增强）冻结原主干作记忆编码器，以可适应侧网络检索和读取过去内容，试图避免表征陈旧。
- **支持/反例潜力**：检索器与读器分工、历史编码稳定性的重要基线；“无限长度记忆库”是容量设计表述，不等于无限查找可靠性。需要核查粒度、索引更新、内容更新和真实内存量。

### T04-052｜精读优先｜Walking Down the Memory Maze: Beyond Context Limit through Interactive Reading
- **身份/版本**：Howard Chen、Ramakanth Pasunuru、Jason Weston、Asli Celikyilmaz，2023；arXiv:2310.05029v1。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2310.05029v1)；[PDF](https://arxiv.org/pdf/2310.05029v1)。**深度A**。
- **机制关联**：MemWalker（记忆树导航阅读）先建立摘要节点树，再由模型根据问题交互导航，取得足够信息后回答，并标出相关文本位置。
- **支持/反例潜力**：非常接近“摘要导航→原文证据”；是否能够回父节点/换兄弟分支以及其停止条件，必须读方法而不是据名称补全。
- **精读问题**：节点摘要错失细节时如何找到正确分支？是否支持回溯、最大探索步数/访问预算多大？原始叶内容一直保留吗？与RAPTOR的跨层平铺检索/ReadAgent扁平gist回看相比，树形导航独立收益多少？

### T04-053｜精读优先｜Mix-of-Granularity: Optimize the Chunking Granularity for Retrieval-Augmented Generation
- **身份/版本**：Zijie Zhong、Hanwen Liu、Xiaoya Cui、Xiaofan Zhang、Zengchang Qin，2024初稿/2025正式；arXiv:2406.00456v2与COLING2025同作，不重复计数。
- **原始来源/全文**：[摘要](https://arxiv.org/abs/2406.00456v2)；[ACL正式版](https://aclanthology.org/2025.coling-main.384/)；[正式PDF](https://aclanthology.org/2025.coling-main.384.pdf)。**深度A：两份摘要核验**。
- **机制关联**：MoG（粒度混合）以路由器按输入问题选择知识源粒度，用软标签训练；MoGG（其图扩展）帮助取得位置遥远的片段，与主方法计1项。
- **支持/反例潜力**：已经存在直接查询条件的粒度学习；不代表同时维护层级摘要或具备多轮下钻，需分机制比较。
- **精读问题**：软标签由何种实际效用/答案信号得到，有无标签泄漏？粒度只单选还是可组合？跨语料源、罕见细节、已选粗粒度仍不足时可否重路由？额外索引存储与路由成本是否同预算？

## 数量与边界复核

- 唯一作品ID连续为T04-001—T04-053，无重复；T04-004为唯一非论文项。
- 精读优先26项：001、002、003、005、007、008、009、010、011、013、015、016、017、018、020、023、032、036、038、039、040、043、049、050、052、053。
- 首次公开在近12个月的14篇论文：001、002、003、007、008、015、016、017、020、023、038、039、040、041。K3单列官方介绍，HiQA更新单列版本。
- 未将草案待核验模型按传闻登记；也不将检索相关博客、重复版本、代码仓库另计论文。尚未完成的正式版逐一对应、完整来源生命周期、召回保证与最低回退预算，见`HANDOFF.md`。
