# T05 首轮候选目录：递归记忆、键值分工与地址粒度

日期：2026-11-08。范围：公开文献发现和摘要层初筛；遵循本轮 PLAN.md。**52 个去重作品已完成身份与摘要/官方简介核验；另有 1 个待核验作品，不计入 52。精读优先 26 项，全文精读 0，代码核验 0。** 本文件不是最终科研综合或对任何新模型的背书。

## 口径、术语与字段

- **A＝摘要核验**：稳定标识、作品标题与 arXiv 摘要或会议官方介绍已取得。正文入口可用不等于读完正文。52 项均为 A；015 另取得 HTML 正文但仅查看开头，不提升为全文精读。全文链接均为入口，未逐一验证 PDF 下载成功。
- **★＝下一轮优先精读**，共 26 项；没有星号不等于排除。
- **线性注意力**：通过特征映射及矩阵乘法结合律把历史键值压入固定状态的注意力家族；不把所有线性时间模型视为同一机制。
- **快速权重**：随当前序列在线变化、承载暂存关联的权重；与训练期间缓慢学习的参数区分。**Delta rule（差分校正规则）**：先读取当前键对应的预测值，再以预测残差校正关联。
- **状态空间模型（SSM）**：通过递归状态更新处理序列的模型。**联想记忆**：由内容线索找回关联值的存储机制。
- **循环神经网络（RNN）**：用历史状态递归处理输入的网络；**多层感知机（MLP）**：由多层前馈变换组成的网络；**矩阵长短期记忆（mLSTM）**：以矩阵状态保存关联的循环记忆；**浮点运算数（FLOPs）**：衡量算术工作量的计数，不等于真实运行时间。
- **地址聚合**：为一个块或状态形成用于决定是否访问它的键/路由统计；**值聚合**：把块内内容压成待返回的载荷。两者即使共享来源也不必同粒度。
- **多槽读出**：保留多个可区分的槽并按查询读取，不能与把多个头最终平均成一向量混同。**来源回访**：由摘要或路由定位到仍被保留的细粒度原始内容，再读取它。
- **多查询联想召回（MQAR）**：在同一序列中对多个先前键值关联发起检索的任务。**键值缓存（KV cache）**：显式保存历史键和值的存储。**干扰**：其他写入使目标关联读出受到污染。
- “支持/反例”均指**值得验证的潜力**，不是本轮已证结论。摘要中的性能由作者报告，未复现实验。
- 年份取首个公开版本；特别注明编号年份不等于首发年份的情况。只核实到部分作者时列已核作者；未知用“—”，不把投稿联系人自动当作者。作者序列、正式发表场次缺失交给统一目录负责人补齐。

## A. 基础、差分写入与写入保持

### T05-001 ★ Linear Transformers Are Secretly Fast Weight Programmers
- 身份：2021；Imanol Schlag、Kazuki Irie、Jürgen Schmidhuber；[arXiv:2102.11174](https://arxiv.org/abs/2102.11174)，v1 2021-02-22，v3 2021-06-09；ICML/PMLR 版本为同一作品，不另计。[全文入口](https://arxiv.org/pdf/2102.11174)。深度 A。
- 机制：把线性自注意力与快速权重编程对应，明确指出加性外积记忆容量局限，改用差分校正和动态学习率。
- 支持/反例潜力：可以把“多写一些信息”与“修正已有键值映射”分开；不能据此断言差分规则消除有限状态上限。
- 精读问题：容量论证依赖何种键正交性？重复键覆盖与相似键污染分别怎样量化？键维度与值维度的作用是否分开？

### T05-002 ★ Simple linear attention language models balance the recall-throughput tradeoff
- 身份：2024；Simran Arora 等；[arXiv:2402.18668](https://arxiv.org/abs/2402.18668)，v1 2024-02-28、v2 2025-03-07。[全文入口](https://arxiv.org/pdf/2402.18668)。深度 A。
- 机制：BASED（线性注意力与滑动窗口混合架构）以窗口大小、特征维度调整状态规模和召回；摘要直接报告固定状态与召回权衡。
- 支持/反例潜力：是“增状态即可恢复多少召回”的重要基尺，也反对无条件的等质量恒定内存宣称。
- 精读问题：理论是任意算法下界还是特定特征映射上界？性能和吞吐分别在何种上下文、批量、精度下测量？

### T05-003 ★ Repeat After Me: Transformers are Better than State Space Models at Copying
- 身份：2024；Samy Jelassi、David Brandfonbrener、Sham M. Kakade、Eran Malach；[arXiv:2402.01032](https://arxiv.org/abs/2402.01032)，v1 2024-02-01、v2 2024-06-03。[全文入口](https://arxiv.org/pdf/2402.01032)。深度 A。
- 机制：以字符串复制比较二层 Transformer 与固定潜状态的广义状态空间模型，含理论和实验。
- 支持/反例潜力：精确复制是压缩记忆的硬边界；不等价于任务充分摘要不可能。
- 精读问题：精度/位宽、状态大小、字符串分布与允许错误率如何限定定理？可扩展状态、外部缓存、多遍访问是否在模型类外？

### T05-004 Gated Delta Networks: Improving Mamba2 with Delta Rule
- 身份：2024；Songlin Yang、Jan Kautz、Ali Hatamizadeh；[arXiv:2412.06464](https://arxiv.org/abs/2412.06464)，v1 2024-12-09、v3 2025-03-06；ICLR 2025 为同作品。[全文入口](https://arxiv.org/pdf/2412.06464)。深度 A。
- 机制：全局/自适应遗忘与定向差分更新互补，并研究滑窗或 Mamba2 混合结构。
- 支持/反例潜力：适合作为写入保持机制基线；混合臂优势不能全部归于差分状态。下一步：核查门控、差分、混合三类消融和同状态预算比较。

### T05-005 ★ Gated DeltaNet-2: Decoupling Erase and Write in Linear Attention
- 身份：2026；—；[arXiv:2605.22791](https://arxiv.org/abs/2605.22791)，v1 2026-05-21。[全文入口](https://arxiv.org/pdf/2605.22791)。深度 A。
- 机制：把擦除旧键侧关联和提交新值的共用标量门拆为逐通道擦除门、写入门，保留通道衰减与并行算法。
- 支持/反例潜力：高度贴合“保持与写入不是同一控制量”；只核验到作者摘要，未验证其优于其他模型的比较公平性。
- 精读问题：擦除与写入各作用在哪个矩阵轴？与 028 的先后、等价条件和消融差异是什么？增加门自由度是否造成状态谱不稳定？

### T05-006 ★ Dual DeltaNet: Value-Side Memory Reorganization for Linear Attention
- 身份：2026；—；[arXiv:2610.38578](https://arxiv.org/abs/2610.38578)，v1 2026-10-28。[全文入口](https://arxiv.org/pdf/2610.38578)。深度 A。
- 机制：摘要明确区分状态 S 的键侧读 Sᵀk（取值）与值侧读 Se（汇集匹配值特征的地址）；引入双侧差分规则和秩二递归。
- 支持/反例潜力：是本轮“值特征与地址组织分开分析”的最直接新近候选；不是已验证的新默认。
- 精读问题：值侧重组是否改变旧键可检索性？是否有独立控制地址几何和值载荷的实验？收益来自秩二更新还是特定值选择器？

### T05-007 ★ Linear Sequence Modeling with Mixture-of-Memories
- 身份：2025；—；[arXiv:2502.13685](https://arxiv.org/abs/2502.13685)，v1 标题含 MoM 前缀，2025-02-19；v4 2025-11-18，归并为一作品。[全文入口](https://arxiv.org/pdf/2502.13685)。深度 A。
- 机制：Mixture-of-Memories（多记忆混合，以路由器把 token 分配至独立状态）扩大容量、降低交叉干扰。
- 支持/反例潜力：检验“多槽优于单槽”的强近邻，但其地址是 token→状态而非必然的块→来源。
- 精读问题：读路由和写路由是否共享？多个状态是分别读后融合还是先混状态再读？路由失衡、重复键跨槽更新如何处理？

### T05-008 Scaling Linear Attention with Sparse State Expansion
- 身份：2025；—；[arXiv:2507.16577](https://arxiv.org/abs/2507.16577)，v1 2025-07-22、v2 2025-10-01。[全文入口](https://arxiv.org/pdf/2507.16577)。深度 A。
- 机制：行稀疏更新、top-k 硬分类、多分区状态，解耦参数量和上下文状态容量。
- 支持/反例潜力：支持容量扩张并不必线性扩大每次访问成本；混合模型数学成绩不能直接说明精确来源召回。下一步：与 007、014、017 对齐总状态、激活状态、路由和任务。

### T05-009 ★ Log-Linear Attention
- 身份：2025；Han Guo 等（完整序列待补）；[arXiv:2506.04761](https://arxiv.org/abs/2506.04761)，v1 2025-06-05、v3 2026-03-01。[全文入口](https://arxiv.org/pdf/2506.04761)。深度 A。
- 机制：把固定状态改为随长度对数增长的层级状态集，提供矩阵乘法友好的对数线性计算。
- 支持/反例潜力：直接挑战“历史只能压入一个同粒度状态”的假定；状态增量不是免费容量。
- 精读问题：层级覆盖、合并、更新、读取的粒度分别是什么？是否保留原始块以供下钻，还是只能访问分层摘要？

### T05-010 ★ A Hippocampus for Linear Attention: An Exact Memory for What the Recurrent State Forgets
- 身份：2026；—；[arXiv:2607.02303](https://arxiv.org/abs/2607.02303)，v1 2026-07-02。[全文入口](https://arxiv.org/pdf/2607.02303)。深度 A。
- 机制：HOLA（海马补充式线性注意力，以精确缓存补充差分压缩状态）按实际写入预测残差 β‖e‖保留键值，锐化精确缓存读取。
- 支持/反例潜力：本轮最接近“摘要记忆＋有选择保留细节”的组合之一；被保留的精确键值不一定等于可回访全部原始来源。
- 精读问题：缓存选择是否以当前自重建误差替代未来查询效用？与 LoLA 的区别、漏存后能否恢复、完整缓存字节和检索成本是什么？

### T05-011 ★ MARCH: Scaling Recurrent Memory with Content-Routed State Anchors
- 身份：2026；—；[arXiv:2608.12435](https://arxiv.org/abs/2608.12435)，v1 2026-08-12。[全文入口](https://arxiv.org/pdf/2608.12435)。深度 A。
- 机制：周期保存累积状态检查点，每个状态配紧凑内容键；逐 token 用查询聚合因果可见的历史锚和当前状态。
- 支持/反例潜力：明确分开“被保存的状态载荷”与“内容路由键”，接近块地址化；检查点未必对应不重叠原文块。
- 精读问题：累积锚的重叠会否重复计权？键由什么信息学习、能否独立于载荷压缩？是否保留可回访的原始 token？

### T05-012 Linear Sequence Modeling with Relative-Time-Partitioned Memory
- 身份：2026；—；[arXiv:2609.36259](https://arxiv.org/abs/2609.36259)，v1 2026-09-28；方法名 CyFA。[全文入口](https://arxiv.org/pdf/2609.36259)。深度 A。
- 机制：学习时钟把键和值共同循环运输到相对时间槽，提供匹配状态大小下的实验。
- 支持/反例潜力：说明槽组织而非仅槽总数可改变召回；共同运输不等于独立地址/值学习。下一步：查无时钟/随机时钟对照、别名与长距离保留条件。

### T05-013 ★ Multi-State Linear Attention with Generalized Second-Order Routing
- 身份：2026；—；[arXiv:2610.37645](https://arxiv.org/abs/2610.37645)，v1 2026-10-27；方法名 MERLIN。[全文入口](https://arxiv.org/pdf/2610.37645)。深度 A。
- 机制：逐段状态读出之外保存键的一、二阶矩；用查询对块内对齐的均值和方差进行路由，而非只看平均键。
- 支持/反例潜力：目前最直接针对“平均地址掩盖块内少量强匹配”的工作；值摘要和路由统计可独立讨论。
- 精读问题：矩统计是精确还是近似？改变路由而不改变值压缩时提高多少？块内目标被载荷抹去后，改善路由是否仍无效？

### T05-014 ★ Sparse Delta Memory: Scaling the State of Linear RNNs through Sparsity
- 身份：2026；Loic Cabannes 等（作者列表由检索到的论文首页片段部分核验）；[arXiv:2607.07386](https://arxiv.org/abs/2607.07386)，v1 2026-07-08。[全文入口](https://arxiv.org/pdf/2607.07386)。深度 A。
- 机制：大显式记忆上的稀疏读写取代稠密外积；摘要声称同算力、同参数下提高容量有利检索，并研究可学习初始状态。
- 支持/反例潜力：区分参数记忆、序列状态与每步活动规模的重要对照。
- 精读问题：同算力比较包含寻址开销吗？总内存、冲突率与容量曲线如何随槽数变化？稀疏地址有无内容寻址和位置寻址消融？

## B. 容量、干扰、条件边界与反向结果

### T05-015 ★ A Geometry-Based Capacity Theory for Finite-Feature Associative Memory
- 身份：2026；Donghao Zhang 等（HTML 作者区存在姓名/脚注映射待核）；[arXiv:2610.09056](https://arxiv.org/abs/2610.09056)，v1 2026-10-06。[全文入口](https://arxiv.org/html/2610.09056v1)。深度 A；取得全文但只查看开头。
- 机制：有限特征噪声与键核重叠导致的结构干扰分开；相关值情况下检索同时依赖键核和值的 Gram 矩阵（两两内积矩阵）。
- 支持/反例潜力：独立讨论地址几何、值相关性、特征预算的首要理论候选；“增维不能修结构干扰”有适用范围。
- 精读问题：是固定 Hebbian 外积存储还是任意学习规则的边界？精确键查询、随机/各向同性值及相关值分别用了什么假设？

### T05-016 ★ Beyond State Capacity: Why Retrieval Breaks in Mamba
- 身份：2026；—；[arXiv:2610.19709](https://arxiv.org/abs/2610.19709)，v1 2026-10-14。[全文入口](https://arxiv.org/pdf/2610.19709)。深度 A。
- 机制：查询在上下文之前的检索设置中，Mamba 仍落后；门本身有控制力，但相关性信号跨层出现太晚，关键层的门未对齐目标。
- 支持/反例潜力：反对把一切检索失败归因容量；是可见性、表征形成、门控时机的竞争解释。
- 精读问题：如何证明其设置容量不是约束？门干预是否越出可学习分布？查询前置与后置、复制与语义检索的差异多大？

### T05-017 ★ RAM-Net: Expressive Linear Attention with Selectively Addressable Memory
- 身份：2026；—；[arXiv:2602.11958](https://arxiv.org/abs/2602.11958)，v1 2026-02-12、v2 2026-10-06。[全文入口](https://arxiv.org/pdf/2602.11958)。深度 A。
- 机制：固定槽数组与稀疏地址解码器，按键/查询选择少量槽；非重叠地址的写入不会直接叠在相同槽。
- 支持/反例潜力：反向说明“固定状态必在实际规模上失败”过强；总状态容量有限与分区减少干扰可同时成立。
- 精读问题：地址碰撞、读写不一致和未激活槽有何代价？同状态元素访问次数是否掩盖更大总内存？地址解码器训练信号是什么？

### T05-018 Understanding and Enhancing the Expressivity of Kimi Delta Attention
- 身份：2026；Julien Siems 等（官方摘要页列作者）；[arXiv:2609.24797](https://arxiv.org/abs/2609.24797)，v1 2026-09-21。[全文入口](https://arxiv.org/pdf/2609.24797)。深度 A。
- 机制：Complex KDA（扩展门和差分系数取值范围的 KDA）用对角门加单次差分实现旋转，给出有限群状态跟踪表达力结果。
- 支持/反例潜力：表达力限制可通过转移几何改变，不能全部叫“记不住”；状态跟踪不等于任意关联容量。下一步：核定非扩张证明、参数范围和检索任务覆盖。

### T05-019 ★ Gated KalmaNet: A Fading Memory Layer Through Test-Time Ridge Regression
- 身份：首发 2025；—；[arXiv:2511.21016](https://arxiv.org/abs/2511.21016)，v1 2025-11-26、v3 2026-05-17。[全文入口](https://arxiv.org/pdf/2511.21016)。深度 A。
- 机制：维护误差协方差而不是恒等近似，稳态假设下转为在线岭回归，并处理低精度稳定性和条件数。
- 支持/反例潜力：支持键之间的相关结构需要额外统计；反对只靠单次局部残差即可最优更新。
- 精读问题：完整协方差与稳态近似各自计算/内存成本是什么？长上下文收益依赖混合全注意力吗？协方差改善地址几何还是写入保持？

### T05-020 ★ Atlas: Learning to Optimally Memorize the Context at Test Time
- 身份：2025；Ali Behrouz、Zeman Li、Praneeth Kacham、Majid Daliri、Yuan Deng、Peilin Zhong、Meisam Razaviyayn、Vahab Mirrokni（检索结果首页列作者）；[arXiv:2505.23735](https://arxiv.org/abs/2505.23735)，v1 2025-05-29。[全文入口](https://arxiv.org/pdf/2505.23735)。深度 A。
- 机制：把有限容量、只针对最新输入的在线优化、记忆管理表达力分开；用当前及过去 token 优化长期记忆。
- 支持/反例潜力：是“回访过去输入参与再优化”的邻近路线，但不自动等于按查询回访原始来源。
- 精读问题：所谓过去 token 以何形式保留、重用多少次，是否提供完整存储和计算成本？为何能够宣称高容量，理论比较对象是什么？

### T05-021 A Comparison of Memory Mechanisms in World Models
- 身份：2025；—；[arXiv:2512.06983](https://arxiv.org/abs/2512.06983)，v1 2025-12-07、v2 2026-09-26。[全文入口](https://arxiv.org/pdf/2512.06983)。深度 A。
- 机制：MemoryMaze 单环境比较四种编码和五种注入方式；作者摘要给出 mLSTM 编码加加性注入最优、仅此环境且无下游任务评估的限制。
- 支持/反例潜力：不允许从“更复杂测试时学习记忆”推出普遍更强；检索片段称 Titans 编码常落后，仍须原表核实。下一步：辨别编码质量与注入深度混杂，不外推至语言模型。

### T05-022 Restoring Expressivity of Linear Attention via Token-Level Multi-Head
- 身份：2026；—；[arXiv:2601.07832](https://arxiv.org/abs/2601.07832)，v1 2026-01-12、v2 2026-01-14（不能采用检索显示的修订日期作首发）。[全文入口](https://arxiv.org/pdf/2601.07832)。深度 A。
- 机制：沿 token 维度分头，以对抗全局上下文坍缩、维持表示多样性。
- 支持/反例潜力：与“多槽是否只是多样性而非记忆增长”直接相关；多领域成绩不代表因果长程检索。下一步：查是否严格因果、每头覆盖、状态量和复杂度常数。

### T05-023 ★ Zoology: Measuring and Improving Recall in Efficient Language Models
- 身份：2023；Simran Arora 等；[arXiv:2312.04927](https://arxiv.org/abs/2312.04927)，v1 2023-12-08；ICLR 2024 同作品。[全文入口](https://arxiv.org/pdf/2312.04927)。深度 A。
- 机制：分析门控卷积模型与注意力的召回差距，提出 MQAR，展示输入依赖稀疏注意力混合可弥合大量差距。
- 支持/反例潜力：单查询合成成功不能替代多查询召回，是负结果和评价设计的关键来源。
- 精读问题：82% 差距的归因定义和数据标注是什么？理论只针对门控卷积还是包含本轮差分模型？基准是否区分地址失败与值丢失？

## C. 分工、路由、统计量与真实读取成本

### T05-024 Kimi Linear: An Expressive, Efficient Attention Architecture
- 身份：2025；Kimi Team；[arXiv:2510.26692](https://arxiv.org/abs/2510.26692)，v1 2025-10-30、v2 2025-11-01。[全文入口](https://arxiv.org/pdf/2510.26692)。深度 A。
- 机制：KDA（Kimi 差分注意力，以逐通道门细化记忆控制）与 MLA（多头潜注意力，把键值缓存压入潜表示）层级混合。
- 支持/反例潜力：官方宣称的质量/吞吐限于其比较设置，不能视为纯 KDA 已替代所有精确访问。下一步：分离混合全注意力层贡献和状态自身容量；与 005、006、018 对齐机制。

### T05-025 ★ DHA: Learning Decoupled-Head Attention from Transformer Checkpoints via Adaptive Heads Fusion
- 身份：2024；—；[arXiv:2406.06567](https://arxiv.org/abs/2406.06567)，v1 2024-06-03、v2 2024-12-07。[全文入口](https://arxiv.org/pdf/2406.06567)。深度 A。
- 机制：Decoupled-Head Attention（键值解耦头注意力，分别配置键头和值头共享组）采用渐进参数融合转换现有模型。
- 支持/反例潜力：提供“键和值冗余结构不同”的邻近证据，但这是头维度压缩，不能冒充 token/块地址聚合理论。
- 精读问题：键头和值头各自压缩率的独立消融在哪？任务依赖性如何？相同质量下是节省地址容量还是载荷带宽？

### T05-026 Adaptive Memory Decay for Log-Linear Attention
- 身份：2026；—；[arXiv:2605.06946](https://arxiv.org/abs/2605.06946)，v1 2026-05-07。[全文入口](https://arxiv.org/pdf/2605.06946)。深度 A。
- 机制：对层级记忆的衰减改为逐 token、逐层级输入依赖，保持对数线性复杂度。
- 支持/反例潜力：多尺度组织本身未必足够，还涉及各尺度保留策略；摘要明确声称基线可在长程设置退化/坍缩。下一步：查固定衰减与学习衰减的稳定条件和长度外推。

### T05-027 SketchSSM: Write to the Full State, Read from a Compact Sketch
- 身份：2026；—；[arXiv:2609.33051](https://arxiv.org/abs/2609.33051)，v1 2026-09-27、v2 2026-10-06。[全文入口](https://arxiv.org/pdf/2609.33051)。深度 A。
- 机制：全状态写入不变，预先固定基向量并缓存状态对这些基的读出，之后查询仅组合小草图。
- 支持/反例潜力：明确分开“存储多大”和“读取多少”；平均秩八的摘要结果不能保证分布外查询。下一步：核查查询子空间拟合来源、稀有检索误差和全状态重读频率。

### T05-028 FG²-GDN: Enhancing Long-Context Gated Delta Networks with Doubly Fine-Grained Control
- 身份：2026；—；[arXiv:2604.19021](https://arxiv.org/abs/2604.19021)，v1 2026-04-21、v3 2026-08-31。[全文入口](https://arxiv.org/pdf/2604.19021)。深度 A。
- 机制：把标量学习率变逐通道向量，FG²-GDN+ 再解耦键与值缩放，以独立控制擦除和写入。
- 支持/反例潜力：与 005、006 高度邻近，必须比较不同版本的先后，不能归并成一个作品也不能重复计算其方法变体。下一步：看 v1/v3 的机制差异及何时引入 + 变体。

### T05-029 Switching Linear Attention
- 身份：2026；—；[arXiv:2609.39034](https://arxiv.org/abs/2609.39034)，v1 2026-09-30。[全文入口](https://arxiv.org/pdf/2609.39034)。深度 A。
- 机制：在线期望最大化推导混合线性回归；每个输出维度根据输入选择不同线性注意力组件。
- 支持/反例潜力：逐值维选择组件区别于单一查询选一个地址，值得作为多槽读出的替代解释。下一步：组件分配和共享记忆的精确形式、同状态成本及跨维绑定能力。

### T05-030 ★ Memory by Design: Bayesian Layers for Sequence Modeling
- 身份：2026；—；[arXiv:2605.31163](https://arxiv.org/abs/2605.31163)，v1 2026-05-29、v5 2026-10-14。[全文入口](https://arxiv.org/pdf/2605.31163)。深度 A。
- 机制：显式生成假设下做贝叶斯过滤；均值保存记忆，协方差表达关联不确定性，保护高置信记忆并把写入引向不确定方向。
- 支持/反例潜力：摘要同时报告检索提升和 2.5–2.7% 留出困惑度代价，是必须保留的非免费收益边界。
- 精读问题：碰撞实验如何隔离表示几何与更新规则？完整协方差成本和重置近似是什么？改善召回为何损失困惑度，是否可恢复？

### T05-031 Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention
- 身份：2020；Angelos Katharopoulos、Apoorv Vyas、Nikolaos Pappas、François Fleuret；[arXiv:2006.16236](https://arxiv.org/abs/2006.16236)，v1 2020-06-29、v3 2020-08-31；ICML 2020 同作品。[全文入口](https://arxiv.org/pdf/2006.16236)。深度 A。
- 机制：利用核特征映射和结合律递归计算，明确矩阵状态和值归一化的基础来源。
- 支持/反例潜力：提供地址特征维度和输出值维度的起点；早期加速数字不应迁移到现代内核比较。下一步：逐式明确状态、归一化统计和有限特征近似的丢失。

### T05-032 Parallelizing Linear Transformers with the Delta Rule over Sequence Length
- 身份：2024；Songlin Yang、Bailin Wang、Yu Zhang、Yikang Shen、Yoon Kim；[arXiv:2406.06484](https://arxiv.org/abs/2406.06484)，v1 2024-06-10、v6 2025-01-15；NeurIPS 2024 同作品。[全文入口](https://arxiv.org/pdf/2406.06484)。深度 A。
- 机制：用 Householder 矩阵乘积的紧凑表示并行训练差分模型；另研究滑窗和全局注意力混合。
- 支持/反例潜力：块并行是计算分块，不自动引入语义块地址；需避免把内核 chunk 误当信息粒度。下一步：测状态访问、临时缓冲区和反向计算总成本。

### T05-033 ★ Test-time regression: a unifying framework for designing sequence models with associative memory
- 身份：2025；Ke Alexander Wang、Jiaxin Shi、Emily B. Fox；[arXiv:2501.12352](https://arxiv.org/abs/2501.12352)，v1 2025-01-21、v3 2025-05-02。[全文入口](https://arxiv.org/pdf/2501.12352)。深度 A。
- 机制：Test-time regression（测试时回归，把上下文关联写入视为回归拟合再查询）用回归权重、函数类、优化器三轴统一记忆层。
- 支持/反例潜力：摘要直接指出线性注意力忽略 token 间相关性；便于独立描述地址特征、值目标、损失及读函数。
- 精读问题：块内加权回归的充分统计能否与路由统计拆开？何时全局回归与查询局部回归等价？最小条件数与键相关性边界是什么？

### T05-034 Transformers are Multi-State RNNs
- 身份：2024；Matanel Oren 等（检索结果参考文献与官方页身份对应，完整序列待补）；[arXiv:2401.06104](https://arxiv.org/abs/2401.06104)，v1 2024-01-11、v2 2024-06-18。[全文入口](https://arxiv.org/pdf/2401.06104)。深度 A。
- 机制：把 Transformer 看作无界多状态递归网络，固定状态数后得到键值缓存压缩，提出无需训练的注意力丢弃策略。
- 支持/反例潜力：明确“多个显式历史项”与“单一矩阵压缩状态”的区别；丢弃不等于合并。下一步：固定预算下保留粒度和不可恢复信息怎样度量。

### T05-035 Gated Linear Attention Transformers with Hardware-Efficient Training
- 身份：2023；Songlin Yang、Bailin Wang、Yikang Shen、Rameswar Panda、Yoon Kim；[arXiv:2312.06635](https://arxiv.org/abs/2312.06635)，v1 2023-12-11、v6 2024-08-27；ICML 2024 同作品。[全文入口](https://arxiv.org/pdf/2312.06635)。深度 A。
- 机制：输入依赖门控和二维递归状态，强调内存传输与并行度权衡。
- 支持/反例潜力：门决定遗忘但不保证按未来查询效用写入；长度外推困惑度稳定与精确召回须分开。下一步：记录门作用轴、归一化及状态元素总量。

### T05-036 Sharp Capacity Scaling of Spectral Optimizers in Learning Associative Memory
- 身份：2026；Juno Kim、Eshaan Nichani、Denny Wu、Alberto Bietti、Jason D. Lee（检索到首页）；[arXiv:2603.26554](https://arxiv.org/abs/2603.26554)，v1 2026-03-27、v2 2026-04-28。[全文入口](https://arxiv.org/pdf/2603.26554)。深度 A。
- 机制：高斯输入输出、幂律频率下比较 Muon、SGD、Newton 训练线性联想记忆的恢复率、批量阈值与信息极限。
- 支持/反例潜力：容量利用还取决于学习算法，不应只从参数自由度推性能；这主要是学习事实记忆而非因果在线状态。下一步：核对能否迁移到逐 token 快速权重，以及长期收敛是否消除优势。

### T05-037 Understanding Transformer from the Perspective of Associative Memory
- 身份：2025；—；[arXiv:2505.19488](https://arxiv.org/abs/2505.19488)，v1 2025-05-26。[全文入口](https://arxiv.org/pdf/2505.19488)。深度 A。
- 机制：以检索信噪比、核视角分析容量，并统一记忆更新；讨论前馈层的联想记忆解释。
- 支持/反例潜力：适合作理论索引和公式比较入口，不把其关于表达力的反思直接当已证明通用定理。下一步：拆出自有推导和引用结论，追原始定理。

### T05-038 Titans: Learning to Memorize at Test Time
- 身份：**首发 2024**；Ali Behrouz、Peilin Zhong、Vahab Mirrokni；[arXiv:2501.00663](https://arxiv.org/abs/2501.00663)，提交记录 v1 2024-12-31，不能仅按 2501 编号写首发 2025。[全文入口](https://arxiv.org/pdf/2501.00663)。深度 A。
- 机制：学习型长期神经记忆配短期注意力，研究三种记忆结合方式。
- 支持/反例潜力：短期准确访问与长期压缩共存；“可处理超长上下文”不代表全部事实可精确保存。下一步：查训练损失、惊异度写入、遗忘与动量，及原输入生命周期。

### T05-039 Using Fast Weights to Attend to the Recent Past
- 身份：2016；Jimmy Ba、Geoffrey Hinton、Volodymyr Mnih、Joel Z. Leibo、Catalin Ionescu；[arXiv:1610.06258](https://arxiv.org/abs/1610.06258)，v1 2016-10-20、v3 2016-12-05。[全文入口](https://arxiv.org/pdf/1610.06258)。深度 A。
- 机制：介于活动和慢权重之间的快速动态变量存储近期记忆，以避免显式保存所有活动副本。
- 支持/反例潜力：历史优先权与迭代读取的基础；递归读出次数增加是否改善容量而不存来源需区分。下一步：查内部读取循环、归一化、衰减与负载敏感性。

### T05-040 What Attention Recalls and Recurrence Controls in Hybrid Language Models
- 身份：2026；—；[arXiv:2609.04434](https://arxiv.org/abs/2609.04434)，v1 2026-09-03；标题由本轮检索命中与同 ID 摘要关联。[全文入口](https://arxiv.org/pdf/2609.04434)。深度 A。
- 机制：拆分预填充和交换状态干预；摘要报告混合模型中精确检索主要依赖 KV 侧，输出语言/人格更多依赖递归侧。
- 支持/反例潜力：是“混合模型总成绩不能归于递归记忆”的直接反例候选；特定模型/任务中成立不等于功能分工定律。下一步：查混合上下文、分布外状态交换与层选择控制。

### T05-041 ★ LoLA: Low-Rank Linear Attention With Sparse Caching
- 身份：2025；L. McDermott、R. W. Heath Jr.、R. Parhi（作者缩写由 015 参考文献关联，完整拼写待统一目录核验）；[arXiv:2505.23666](https://arxiv.org/abs/2505.23666)，v1 2025-05-29、v3 2026-06-13；检索命中称 TMLR 2026，正式版本链接待补，不另计。[全文入口](https://arxiv.org/pdf/2505.23666)。深度 A。
- 机制：近期局部缓存、难记项目稀疏全局缓存、一般项目递归状态三类存储，以自召回误差管理记忆。
- 支持/反例潜力：最贴近“压缩＋保留细粒度特殊项”的组合；不能声称该组合尚无人研究。
- 精读问题：难记的判定是否偏离未来有用的判定？删除后回访能力如何？三路的路由、独立地址、精确值及总缓存预算各是什么？

## D. 状态空间与内容寻址的邻近基础及最接近组合

### T05-042 Mamba: Linear-Time Sequence Modeling with Selective State Spaces
- 身份：2023；Albert Gu、Tri Dao；[arXiv:2312.00752](https://arxiv.org/abs/2312.00752)，v1 2023-12-01、v2 2024-05-31。[全文入口](https://arxiv.org/pdf/2312.00752)。深度 A。
- 机制：输入依赖状态参数选择性传播或遗忘，硬件友好扫描；动机含离散内容的选择性复制。
- 支持/反例潜力：选择性传播解决一种弱点，不保证任意密集关联召回。下一步：对照 003、016，区分查询已知/未知和选择性复制/全复制。

### T05-043 Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality
- 身份：2024；Tri Dao、Albert Gu；[arXiv:2405.21060](https://arxiv.org/abs/2405.21060)，v1 2024-05-31。[全文入口](https://arxiv.org/pdf/2405.21060)。深度 A。
- 机制：结构化半可分离矩阵连接注意力与状态空间模型，得到 Mamba-2。
- 支持/反例潜力：方便比较各轴状态维度与可并行分块；结构对偶不是信息保留等价。下一步：查块内/块间分解是否改变可寻址粒度，以及复杂度中的状态维度。

### T05-044 Hopfield Networks is All You Need
- 身份：首发 2020；Hubert Ramsauer 等；[arXiv:2008.02217](https://arxiv.org/abs/2008.02217)，提交记录 v1 2020-07-16、v3 2021-04-28；ICLR 2021 同作品，编号月份也不能代替提交记录。[全文入口](https://arxiv.org/pdf/2008.02217)。深度 A。
- 机制：现代连续 Hopfield 记忆与注意力等价，区分全局平均、子集平均、单模式固定点，报告指数级模式容量。
- 支持/反例潜力：不能把保留显式模式集合的指数容量直接搬到固定矩阵压缩记忆；平均固定点提醒多项值混合风险。下一步：核查容量、分离条件、吸引域和存储成本。

### T05-045 Modern Hopfield Networks meet Encoded Neural Representations — Addressing Practical Considerations
- 身份：2024；—；[arXiv:2409.16408](https://arxiv.org/abs/2409.16408)，v1 2024-09-24、v2 2024-10-30。[全文入口](https://arxiv.org/pdf/2409.16408)。深度 A。
- 机制：编码表示提高模式可分性、减少亚稳态，并支持图像与自然语言异联想。
- 支持/反例潜力：几何可通过学习改变，是对 051 的绝对化说法的重要比较项；不直接证明任意语义密度下可行。下一步：查真实模式集合、完美召回指标和地址编码训练成本。

### T05-046 ★ Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention
- 身份：2025；Jingyang Yuan 等；[arXiv:2502.11089](https://arxiv.org/abs/2502.11089)，v1 2025-02-16、v2 2025-02-27。[全文入口](https://arxiv.org/pdf/2502.11089)。深度 A。
- 机制：粗粒度 token 压缩与细粒度 token 选择并存，原生训练、硬件对齐稀疏访问。
- 支持/反例潜力：不是线性递归记忆，但对“多粒度＋来源细节访问”的组合构成强邻近工作，不能只查递归模型。
- 精读问题：压缩分支的键统计如何指导选择原始块？值聚合是否与路由共用？路由漏召回有无保底，源 KV 是否始终保留及总成本多少？

### T05-047 Learning to (Learn at Test Time): RNNs with Expressive Hidden States
- 身份：2024；Yu Sun 等；[arXiv:2407.04620](https://arxiv.org/abs/2407.04620)，v1 2024-07-05、v4 2025-08-31。[全文入口](https://arxiv.org/pdf/2407.04620)。深度 A。
- 机制：Test-Time Training（测试时训练，以自监督学习步骤在线更新隐藏模型），包括线性模型与两层前馈模型两种状态。
- 支持/反例潜力：增大函数类可改善长期信息利用；作者摘要同时说明前馈型状态仍有内存传输挑战。下一步：查训练目标与真实检索效用差距、mini-batch 更新是否影响因果粒度。

### T05-048 Leave No Context Behind: Efficient Infinite Context Transformers with Infini-attention
- 身份：2024；Tsendsuren Munkhdalai、Manaal Faruqui、Siddharth Gopal；[arXiv:2404.07143](https://arxiv.org/abs/2404.07143)，v1 2024-04-10、v2 2024-08-09。[全文入口](https://arxiv.org/pdf/2404.07143)。深度 A。
- 机制：局部遮蔽注意力与长期压缩线性注意力同块结合，处理连续长输入。
- 支持/反例潜力：局部精确＋长期压缩组合已有；“无限输入”不等于无限随机访问。下一步：查旧原文是否丢弃、跨段查询是否能返回源细节，以及密集多项检索。

### T05-049 ★ Random Long-Context Access for Mamba via Hardware-aligned Hierarchical Sparse Attention
- 身份：2025；—；[arXiv:2504.16795](https://arxiv.org/abs/2504.16795)，v1 2025-04-23、v2 2025-11-02；方法名 RAMba。[全文入口](https://arxiv.org/pdf/2504.16795)。深度 A。
- 机制：输入分块、选 top-k 块、层级聚合；以块内细粒度 token 学习 token→块相关性，结合 Mamba 取得随机长程访问。
- 支持/反例潜力：是“块寻址＋细粒度内容检索＋递归主干”的关键近邻，摘要声称近恒定内存尤其需审计。
- 精读问题：64M passkey 是否仅单项稀疏信号？何处保存原始内容，主存/显存/索引如何计？检索粒度和载荷压缩能否独立消融？

### T05-050 ★ Sharp Capacity Thresholds in Linear Associative Memory: From Top-1 Retrieval to Tail-Average Learning
- 身份：2026；Nicholas Barnfield、Juno Kim、Eshaan Nichani、Jason D. Lee、Yue M. Lu（检索作者序列）；[arXiv:2605.05189](https://arxiv.org/abs/2605.05189)，v1 2026-05-06 标题为 From Winner-Take-All to Listwise Retrieval，v2 2026-08-19 改题；一作品。[全文入口](https://arxiv.org/pdf/2605.05189)。深度 A。
- 机制：各向同性高斯嵌入、d×d 线性记忆的同时第一名精确检索阈值为 d²/(n log n)=2；较弱列表目标有不同容量标度。
- 支持/反例潜力：最重要的“先召回候选再回访验证”理论入口；不能把列表进入率当最终精确回答率。
- 精读问题：列表 k/n→r 与实际固定小 k 是否同一极限？列表后验证要保存何种外部目标？有限维/相关键值是否偏离阈值？

### T05-051 ★ Attention Is Not Retention: The Orthogonality Constraint in Infinite-Context Architectures
- 身份：2026；Oliver Zahn 等（检索身份）；[arXiv:2601.15313](https://arxiv.org/abs/2601.15313)，v1 2026-01-14 的旧题 Mind the Gap: Why Neural Memory Fails Under Semantic Density，v2 2026-02-04 改题；一作品。[全文入口](https://arxiv.org/pdf/2601.15313)。深度 A。
- 机制：摘要以语义相近键的干扰攻击纯神经事实记忆，提出带散列身份和版本链的结构化事实对象。
- 支持/反例潜力：强负面主张、几何边界与离散来源标识值得查；“可靠记忆要求正交键”“增容量无法克服”的广泛措辞目前**不接受为一般定理**。
- 精读问题：结论限于固定外积规则还是适用于可学习伪逆/协方差/稀疏寻址？散列对照是否依赖精确已知标识，语义查询是否同任务？与 015、045、050 对照。

### T05-052 ★ Sharp storage capacity of a simplified model of linear associative memory
- 身份：2026；Alessio Giorlandino、Sebastian Goldt、Antoine Maillard；[OpenReview ID zXMvCvXYE0](https://openreview.net/forum?id=zXMvCvXYE0) 遇校验墙；用 [ICLR 2026 官方介绍](https://iclr.cc/virtual/2026/10022391) 核验摘要，不能把会场展示误写为已核主会录用。[全文入口](https://openreview.net/pdf?id=zXMvCvXYE0)。深度 A（会议官方简介）。
- 机制：线性映射下每个输入与全部目标的分离约束；构造竞争输出独立重采样的解耦模型，用统计物理刻画容量；摘要仅称原模型和解耦模型数值相似。
- 支持/反例潜力：对“地址和值目标可否独立处理”提供严格但简化的设置，与 050 的原问题定理不能混为一谈。
- 精读问题：解耦近似与原问题差异是否有证明？分离标准、边缘、噪声、输入输出相关性及缩放常数分别是什么？

## E. 待核验，不计入确认候选

### T05-P01 The Capacity of Modern Hopfield Networks under the Data Manifold Hypothesis
- 发现：搜索 Hopfield 基础工作时命中官方 PDF 首页片段：[arXiv:2503.09518](https://arxiv.org/abs/2503.09518)；片段列 Beatrice Achilli、Luca Ambrogioni、Carlo Lucibello、Marc Mézard、Enrico Ventura，2025。
- 身份已有线索，**摘要不足**：FetchURL 对无版本 abs 和 v1 abs 两次只返回 Bibliographic Tools 页脚，没有摘要。两次后停止，不列为 A。
- 关联潜力：数据流形和相关模式可能限制指数容量，适合补足 044/045 的条件边界。
- 下一步入口：[PDF](https://arxiv.org/pdf/2503.09518)；由精读代理合法取得原文后确认身份与摘要，再决定入库。不能从标题推定其结论。

## 首轮覆盖判断

1. 已有多条“压缩状态＋精确项缓存”“块状态＋独立路由统计”“递归主干＋分块细粒度访问”路线。**尚无依据宣称这些组合本身构成空白**。
2. 值聚合和地址聚合最直接入口为 006、011、013、015、025、033、049、052；025 只触及头维度，不可偷换成块粒度。
3. 精确复制、第一名检索、候选列表检索、语义摘要、状态跟踪是不同目标；容量数字不可直接横比。
4. 最关键未决项仍是：保留哪些来源、是否能按查询恢复丢掉的细节、路由遗漏与载荷丢失如何分别定责，以及包含源存储/路由/训练/读写成本后的优势。摘要不足以收束此专题。
