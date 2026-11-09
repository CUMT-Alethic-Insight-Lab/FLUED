# T01 首轮候选：策略的学习来源与学习方式

日期：2026-11-08。范围：发现与摘要层初筛，不是全文综述。**56项去重作品，56项完成作品身份及原始摘要/官方简介核验；全文精读0，代码核验0。精读优先26项。** 每个编号只代表一项作品，预印本、会议网页及更名关联不另计。后文性能和机制表述均为作者摘要/官方简介所述；“潜力”和“核查”是本轮研究判断，不是已复现实证。

## 口径与术语

- **学习信号**：策略依据什么反馈变好，包括语料统计、预测误差、重建误差、教师输出、任务标签/奖励；规则或相似度本身未必是学到的信号。
- **学习方式**：怎样更新决策，包括连续可微优化、离散策略梯度（用采样动作的回报估计梯度）、随机重参数化（把随机采样改写为可求导变换）、联合训练、先预训练后任务适配、冻结骨干只训练接口。训练阶段安排与梯度估计器是两个独立维度。
- **token merging（序列单元合并）**：将多个输入表示聚合成更少表示；不等同丢弃，也不保证信息守恒。
- **task-driven compression（任务驱动压缩）**：用最终任务的预测损失或效用选择保留的信息；不能仅因方法在某任务上评测就这样归类。
- **来源回访**：压缩后仍能沿来源关系访问原始细节；恢复输出形状、解码重建、旁路保留原表示与真正回访原始来源必须分开。
- **A**＝已打开原始摘要或官方介绍。所有56项均为A；搜索摘要与全文入口不提升深度。**P**＝全文精读优先。作者栏“—”表示本轮可见页面提取未完整给出作者，留待元数据负责人补齐，不将arXiv投稿人自动当作者。年份按首次预印本，正式发表年在有可见来源时关联。
- arXiv的`/pdf/编号`、ACL的`.pdf`是**全文入口**，不是本轮已阅读证明。精读必须另取原文页码/章节/图表。

## A. 统计、规则与可学习边界（C01–C15）

### C01 — Neural Machine Translation of Rare Words with Subword Units
- 年份：2015；作者：Rico Sennrich、Barry Haddow、Alexandra Birch（检索所见引文）；稳定ID：arXiv:1508.07909。核验[A](https://arxiv.org/abs/1508.07909)；[全文](https://arxiv.org/pdf/1508.07909)。版本：v1 2015→v5 2016；本轮不另计正式版。
- 信号：语料频率型子词压缩，对照字符n元组；方式：分段预处理与翻译模型分离，不是任务梯度学边界。摘要确认BPE分段与不同分段方案比较；具体合并准则需原文。
- 支持/反例潜力：提供便宜强统计基线，防止把“由数据构建”误称端到端学习；语种与词类差异适合反查语义边界必要性。
- 下一步：同词表大小、长度和翻译计算预算是否分别匹配？

### C02 — Subword Regularization: Improving Neural Network Translation Models with Multiple Subword Candidates
- 年份：2018；作者：Taku Kudo（检索所见）；稳定ID：arXiv:1804.10959。核验[A](https://arxiv.org/abs/1804.10959)；[全文](https://arxiv.org/pdf/1804.10959)。v1。
- 信号：一元语言模型的分段概率；方式：训练时采样多个分段作为正则化，不能等同任务奖励直接优化切分策略。
- 支持/反例潜力：多种分段本身可改善低资源/域外鲁棒性，反对“唯一最优边界”预设。
- 下一步：分段分布是否受下游梯度更新，采样温度与序列长度效应是否分离？

### C03 — SentencePiece: A simple and language independent subword tokenizer and detokenizer for Neural Text Processing
- 年份：2018；作者：Taku Kudo、John Richardson（检索所见）；稳定ID：arXiv:1808.06226。核验[A](https://arxiv.org/abs/1808.06226)；[全文](https://arxiv.org/pdf/1808.06226)。v1。
- 信号：直接从原始句子学习子词模型；方式：独立训练的预处理器。摘要的“end-to-end”指原始句子到分词工具链，不可据此推成语言模型损失联合学边界。
- 支持/反例潜力：解释术语歧义；与C02为不同作品但算法/实现谱系关联。
- 下一步：把实现工具与分段算法去重，勿把同一个一元模型当两种训练信号。

### C04 — CANINE: Pre-training an Efficient Tokenization-Free Encoder for Language Representation
- 年份：2021；作者：Jonathan H. Clark等（检索所见）；稳定ID：arXiv:2103.06874。核验[A](https://arxiv.org/abs/2103.06874)；[全文](https://arxiv.org/pdf/2103.06874)。v1 2021→v4 2022。
- 信号：直接字符预训练，或可选子词软归纳偏置；方式：下采样结合深层编码器。具体固定下采样与两种预训练损失待原文对照，不能把字符接口当学习边界。
- 支持/反例潜力：同字符输入下区分教师/子词偏置与无分词训练；与C05/C06形成候选对照组。
- 下一步：两种预训练是否仅改变监督来源，参数和数据是否一致？

### C05 — Charformer: Fast Character Transformers via Gradient-based Subword Tokenization
- 年份：2021；作者：Yi Tay等（检索所见）；稳定ID：arXiv:2106.12672。核验[A](https://arxiv.org/abs/2106.12672)；[全文](https://arxiv.org/pdf/2106.12672)。v1 2021→v3 2022。
- 信号：语言任务预训练反馈；方式：枚举候选子词块，位置级块评分网络做软梯度分词，并与模型端到端训练。具体损失及硬化行为待原文。
- 支持/反例潜力：多尺度候选不等于自由离散边界；检验软混合与离散分段之间的表达/成本差别。
- 下一步：块长度集合、最终下采样率及软候选额外计算是否计入？

### C06 — MANTa: Efficient Gradient-Based Tokenization for Robust End-to-End Language Modeling
- 年份：2022；作者：Nathan Godey等（检索所见）；稳定ID：arXiv:2212.07284。核验[A](https://arxiv.org/abs/2212.07284)；[全文](https://arxiv.org/pdf/2212.07284)。v1。
- 信号：语言模型反馈；方式：可微分词器与语言模型联合训练，输出可解释显式块分段。
- 支持/反例潜力：字符噪声、域外与通用任务提供跨分布检查；与固定分段、C05比较不应只看摘要速度。
- 下一步：边界梯度路径、训练/推理切分差异、长度正则与语言模型损失的消融。

### C07 — Efficient Transformers with Dynamic Token Pooling — **P**
- 年份：2023；作者：Piotr Nawrot、Jan Chorowski、Adrian Lancucki、Edoardo Maria Ponti；稳定ID/正式版：ACL 2023.acl-long.353。核验[A](https://aclanthology.org/2023.acl-long.353/)；[全文](https://aclanthology.org/2023.acl-long.353.pdf)。
- 信号：子词分段监督、条件熵峰值监督、语言学边界及主任务反馈；方式：自回归预测段界，显式比较随机重参数化端到端学习与监督边界。这是本轮最直接切合T01的比较研究。
- 支持/反例潜力：作者称同计算预算优于固定池化和普通Transformer；可检验“学习来源是否比学习算法更重要”。
- 精读问题：逐项抽取边界目标来源、训练器、固定/动态平均段长及匹配预算；哪种监督在什么语言胜出？固定池化是否同参数/同实际速度？

### C08 — MEGABYTE: Predicting Million-byte Sequences with Multiscale Transformers
- 年份：2023；作者：Lili Yu等（检索所见）；稳定ID：arXiv:2305.07185。核验[A](https://arxiv.org/abs/2305.07185)；[全文](https://arxiv.org/pdf/2305.07185)。v2。
- 信号：自回归预测；方式：局部/全局模型多尺度联合学习，摘要确认切成patch，固定边界细节待全文。
- 支持/反例潜力：强多尺度但非学边界对照；区分层级收益与策略学习收益。
- 下一步：patch大小、全局/局部参数分配和生成并行性是否单独消融？

### C09 — SpaceByte: Towards Deleting Tokenization from Large Language Modeling
- 年份：2024；作者：Kevin Slagle（检索所见）；稳定ID：arXiv:2404.14408。核验[A](https://arxiv.org/abs/2404.14408)；[全文](https://arxiv.org/pdf/2404.14408)。v3 2024-10。
- 信号：预测任务训练表示；方式：按空格等特定字节调度大块计算的规则，不是学得的边界策略。
- 支持/反例潜力：规则在固定训练/推理预算下可接近分词Transformer，反对默认复杂策略必胜。
- 下一步：非空格语种、符号与代码的失效条件；与熵分段同局部模型预算比较。

### C10 — Byte Latent Transformer: Patches Scale Better Than Tokens — **P**
- 年份：2024预印本／2025 ACL；作者：Artidoro Pagnoni等；稳定ID：arXiv:2412.09871＝ACL 2025.acl-long.453。核验[A预印本](https://arxiv.org/abs/2412.09871)、[A正式版](https://aclanthology.org/2025.acl-long.453/)；[全文](https://aclanthology.org/2025.acl-long.453.pdf)。两入口只计一项。
- 信号：下一字节预测熵；方式：按熵确定动态patch，主模型自回归训练。熵估计器的独立预训练/冻结状态必须从原文核验，不以“动态”推成联合学策略。
- 支持/反例潜力：FLOP控制、patch长度随可预测性变化；有机会分离任务梯度边界和预测难度代理边界。
- 精读问题：熵模型成本计入何处？固定长度、空格、熵差/绝对熵的消融是否同平均压缩率？教师及主模型是否共享参数/信息？

### C11 — Dynamic Chunking for End-to-End Hierarchical Sequence Modeling — **P**
- 年份：2025；作者：Sukjun Hwang等（检索所见）；稳定ID：arXiv:2507.07955。核验[A](https://arxiv.org/abs/2507.07955)；[全文](https://arxiv.org/pdf/2507.07955)。v2。
- 信号：主语言模型目标，无显式边界标签（作者摘要）；方式：H-Net动态压缩和多阶段层级联合端到端训练。离散梯度估计器、比例约束不能由摘要确定。
- 支持/反例潜力：多层抽象、内容/上下文相关分段，是最直接机制近邻；不能用其结论替代字节接口下的公平消融。
- 精读问题：路由器各梯度路径、退化段长控制、固定/随机/熵边界是否存在同码同预算对照？层级增加与边界学习分别贡献多少？

### C12 — SOMBRERO: Measuring and Steering Boundary Placement in End-to-End Hierarchical Sequence Models — **P**
- 年份：2026；作者：—；稳定ID：arXiv:2601.22805。核验[A](https://arxiv.org/abs/2601.22805)；[全文](https://arxiv.org/pdf/2601.22805)。v1 2026-01-30；搜索日期曾错标2025，已按投稿史纠正。近期预印本，不背书。
- 信号：下一字节惊异度/预测困难的辅助边界对齐；方式：置信度对齐边界损失，加输入级置信加权平滑。
- 支持/反例潜力：直接挑战“仅主任务损失就会学到理想计算分配”；可能是C11与C10间信号折中。
- 精读问题：边界富集指标是否只是与所用监督自相关？去辅助损失、去输入平滑、同段长控制是否齐全？难位置边界对齐是否因果改善任务？

### C13 — GQ-VAE: A gated quantized VAE for learning variable length tokens — **P**
- 年份：2025-12；作者：—；稳定ID：arXiv:2512.21913。核验[A](https://arxiv.org/abs/2512.21913)；[全文](https://arxiv.org/pdf/2512.21913)。v1。近期预印本。
- 信号：变分自编码/离散重建类，具体损失待全文；方式：可独立预训练、作为现有分词器替代，学习变长离散单元，不必重构整个语言模型。
- 支持/反例潜力：摘要明确在**同压缩率较小词表BPE**下更利下游学习，但普通BPE整体仍更接近其上界；有价值的分阶段训练与公平匹配反例。
- 精读问题：重建对象、码本/边界优化器、同词表与同长度两种匹配如何改变排序？是否实际无监督分段先训练再冻结？

### C14 — Fast Byte Latent Transformer
- 年份：2026；作者：—；稳定ID：arXiv:2605.08044。核验[A](https://arxiv.org/abs/2605.08044)；[全文](https://arxiv.org/pdf/2605.08044)。v1。
- 信号：标准下一字节预测＋辅助分块扩散目标；方式：联合目标支持并行生成，另有自推测与验证变体。
- 支持/反例潜力：压缩训练的真正收益可能被逐字节解码瓶颈吞没；辅助预测改变生成方式不等于改变边界学习。
- 下一步：分块目标有无给分段器梯度？带验证的质量/延迟与带宽估算分开报告。

### C15 — Dynamic Multi-Byte Prediction With Hierarchical Language Models
- 年份：2026；作者：—；稳定ID：arXiv:2608.15454。核验[A](https://arxiv.org/abs/2608.15454)；[全文](https://arxiv.org/pdf/2608.15454)。v2。
- 信号：多字节预测；方式：变长预测窗与层级潜单元对齐，因果注意力遮罩支持并行，不增参数（作者摘要）。
- 支持/反例潜力：预测目标粒度与压缩边界耦合的近期入口；不能因为“对齐”就认为边界受该目标学习。
- 下一步：固定/动态窗与同延迟质量对照；边界参数是否冻结，以及训练可见性是否泄漏。

## B. 离散选择、隐层级与预算（C16–C23）

### C16 — Hierarchical Multiscale Recurrent Neural Networks
- 年份：2016；作者：Junyoung Chung、Sungjin Ahn、Yoshua Bengio（检索所见）；稳定ID：arXiv:1609.01704。核验[A](https://arxiv.org/abs/1609.01704)；[全文](https://arxiv.org/pdf/1609.01704)。v7 2017。
- 信号：字符语言模型/手写序列任务；方式：无显式边界信息发现隐层级，具体直通估计与更新操作待全文。
- 支持/反例潜力：端到端层级/边界并非新概念；为分段器训练稳定性提供早期谱系。
- 下一步：边界更新、复制/清空状态与层级结构消融，是否把结构可视化误作任务充分性。

### C17 — Skip RNN: Learning to Skip State Updates in Recurrent Neural Networks
- 年份：2017；作者：—；稳定ID：arXiv:1708.06834。核验[A](https://arxiv.org/abs/1708.06834)；[全文](https://arxiv.org/pdf/1708.06834)。v3 2018；搜索与页面有“Learning to Skip State Updates…”短标题。
- 信号：任务损失和减少更新的预算约束；方式：学习跳过状态更新，梯度估计器待原文。
- 支持/反例潜力：学习计算策略不必学习信息压缩；降低更新数不代表原始输入被永久丢弃。
- 下一步：输入是否仍逐位读入、预算系数和延迟测量，以及与随机跳步同任务预算比较。

### C18 — Learning to Skim Text — **P**
- 年份：2017；作者：—；稳定ID：arXiv:1704.06877。核验[A](https://arxiv.org/abs/1704.06877)；[全文](https://arxiv.org/pdf/1704.06877)。v2。
- 信号：分类、问答等任务；方式：标准策略梯度训练离散跳跃距离，修改LSTM的阅读行为。
- 支持/反例潜力：本轮明确的离散策略梯度祖先，与可微选择器形成算法轴对照；跳读与合并的决策对象不同。
- 精读问题：回报是否包含长度惩罚、方差控制/基线是什么？若同数据同网络改可微门，任务与速度的差别是否仍存在？

### C19 — Neural Speed Reading via Skim-RNN
- 年份：2017；作者：—；稳定ID：arXiv:1711.02085。核验[A](https://arxiv.org/abs/1711.02085)；[全文](https://arxiv.org/pdf/1711.02085)。v3，页面注明ICLR 2018。
- 信号：下游任务；方式：不重要输入只更新小部分隐状态，训练器待原文，不从任务名称推成策略梯度。
- 支持/反例潜力：保持输入/输出接口、测试时可调速度，与C18“完全跳过”不同；CPU/GPU延迟对照需细查。
- 下一步：小/大状态选择梯度、吞吐与单例延迟、保留细节的隐状态路径。

### C20 — Rationalizing Neural Predictions — **P**
- 年份：2016；作者：Tao Lei、Regina Barzilay、Tommi Jaakkola（检索所见）；稳定ID：arXiv:1606.04155。核验[A](https://arxiv.org/abs/1606.04155)；[全文](https://arxiv.org/pdf/1606.04155)。v2。
- 信号：任务预测充分性＋短小连贯的正则，无训练时理由标签；方式：生成器对文本片段采样，编码器从选中文本预测，联合训练；具体离散优化需原文确认。
- 支持/反例潜力：任务驱动的选择可能学“足以预测”的证据而非忠实保留；可揭示捷径、共同适应与压缩效用的差别。
- 精读问题：选择器能否通过掩码编码标签，连贯/稀疏正则消融是什么？冻结预测器和共同训练是否可比？

### C21 — Interpretable Neural Predictions with Differentiable Binary Variables — **P**
- 年份：2019；作者：Jasmijn Bastings、Wilker Aziz、Ivan Titov；稳定ID：ACL P19-1284＝arXiv:1905.08160。核验[A](https://aclanthology.org/P19-1284/)；[全文](https://aclanthology.org/P19-1284.pdf)。
- 信号：仅从选中文本完成分类＋预指定选择率约束；方式：离散/连续混合潜变量，可用梯度训练、无需REINFORCE，能计算期望稀疏惩罚。
- 支持/反例潜力：同样离散动作不必策略梯度；与C20在信号接近时检验优化算法影响。
- 精读问题：随机重参数化偏差、测试硬决策、长度约束的实际满足程度，是否对比同率的策略梯度？

### C22 — Funnel-Transformer: Filtering out Sequential Redundancy for Efficient Language Processing
- 年份：2020；作者：Zihang Dai等（检索所见）；稳定ID：arXiv:2006.03236。核验[A](https://arxiv.org/abs/2006.03236)；[全文](https://arxiv.org/pdf/2006.03236)。v1。
- 信号：语言预训练与序列/逐位任务；方式：逐层缩短隐序列、解码恢复逐位表示，节省算量可换更深/宽网络。
- 支持/反例潜力：恢复形状并不证明恢复原始信息；模型加宽收益须和压缩策略收益分开。
- 下一步：池化规则是否固定，重建路径有无跳连，计算再投资与压缩的两因素消融。

### C23 — Compressive Transformers for Long-Range Sequence Modelling — **P**
- 年份：2019；作者：Jack W. Rae等（检索所见）；稳定ID：arXiv:1911.05507。核验[A](https://arxiv.org/abs/1911.05507)；[全文](https://arxiv.org/pdf/1911.05507)。v1。
- 信号：长程语言建模；方式：压缩过去记忆。重建/注意力重建等具体辅助损失**尚未由摘要核验**，列为精读问题而非已确认机制。
- 支持/反例潜力：任务足够信息与完整重建的经典比较入口；多时间尺度存储不等于按来源回访。
- 精读问题：压缩器是否单独优化，主损失是否穿透到旧记忆？比较重建原状态与保持注意力响应的损失，截断梯度是否造成不同训练信号？

## C. 合并、任务选择与来源保留（C24–C35）

### C24 — Token Merging: Your ViT But Faster — **P**
- 年份：2022预印本／2023 ICLR；作者：—；稳定ID：arXiv:2210.09461。核验[A](https://arxiv.org/abs/2210.09461)、[官方会议简介](https://iclr.cc/virtual/2023/poster/12173)；[全文](https://arxiv.org/pdf/2210.09461)。v3。两个入口一项。
- 信号：当前表示的相似性，匹配规则无须训练；方式：轻量匹配合并，可直接插入也可在训练中使用。
- 支持/反例潜力：作者明确免训练有效、训练可减少精度下降，是“策略本身学到”与“模型适应固定策略”的关键区分。
- 精读问题：免训练/微调的相同骨干与比例、匹配特征、合并权重、来源映射保留内容；原始细节是否还可读取？

### C25 — Token Pooling in Vision Transformers — **P**
- 年份：2021；作者：—；稳定ID：arXiv:2110.03860。核验[A](https://arxiv.org/abs/2110.03860)；[全文](https://arxiv.org/pdf/2110.03860)。v2；正式版关联待编目补齐。
- 信号：对下采样后表示的重建误差；方式：输入相关的低成本聚类优化，**不直接等于跨样本训练一个策略网络**。
- 支持/反例潜力：与C24/C26比较表示重建、规则相似、任务梯度三类；低通假设给出适用条件。
- 精读问题：重建什么空间、用什么距离，是否利用标签训练中心？聚类成本和端到端实测速率、细粒度任务失效？

### C26 — TokenLearner: What Can 8 Learned Tokens Do for Images and Videos? — **P**
- 年份：2021；作者：Michael S. Ryoo等（检索所见）；稳定ID：arXiv:2106.11297。核验[A预印本](https://arxiv.org/abs/2106.11297)、[A会议摘要](https://proceedings.neurips.cc/paper/2021/hash/6a30e32e56fce5cf381895dfe6ca7b6f-Abstract.html)；[全文](https://arxiv.org/pdf/2106.11297)。预印本v4 2022；NeurIPS 2021短题“TokenLearner: Adaptive Space-Time Tokenization for Videos”摘要亦已打开、核心内容一致，关联但不新增计数；完整扩展差异待精读。
- 信号：视觉任务反馈；方式：自适应学习少量重要视觉单元，具体训练损失待全文。
- 支持/反例潜力：多汇总单元与密集表示交替处理的来源映射近邻；是否真的支持细节回访尚未确认。
- 精读问题：核验TokenFuser（候选中文：单元回融模块，将少量表示回写密集布局）原文结构及有/无消融；回融只重建布局还是读取保留的原表示？

### C27 — DynamicViT: Efficient Vision Transformers with Dynamic Token Sparsification
- 年份：2021；作者：Yongming Rao等（检索所见）；稳定ID：arXiv:2106.02034。核验[A](https://arxiv.org/abs/2106.02034)；[全文](https://arxiv.org/pdf/2106.02034)。v2。
- 信号：视觉任务与可能的教师/比例辅助项（后两者未由摘要确认）；方式：轻量重要性预测器、注意力遮罩支持端到端训练，层级丢弃。
- 支持/反例潜力：与免训练相似合并对照，强调丢弃与合并不同；不能用共同视觉准确率证明机制等价。
- 下一步：蒸馏目标、固定率、软训练/硬推理和参数开销逐项核查。

### C28 — Not All Patches are What You Need: Expediting Vision Transformers via Token Reorganizations
- 年份：2022；作者：Youwei Liang等（检索所见）；稳定ID：arXiv:2202.07800；别名EViT。核验[A](https://arxiv.org/abs/2202.07800)；[全文](https://arxiv.org/pdf/2202.07800)。v2。
- 信号：类单元注意力作为重要性代理；方式：保留高注意力、融合其他单元，集成到训练但无额外参数；不能因此称重要性规则被直接学到。
- 支持/反例潜力：相同参数下检验规则＋模型适应；保留低重要性汇总与直接删去的对照价值高。
- 下一步：融合背景究竟保留多少可用信息，重组和高分辨率算量再投资分开消融。

### C29 — Token Fusion: Bridging the Gap between Token Pruning and Token Merging
- 年份：2023预印本／2024 WACV；作者：Minchul Kim、Shangqian Gao、Yen-Chang Hsu、Yilin Shen、Hongxia Jin；稳定ID：arXiv:2312.01026。核验[A预印本](https://arxiv.org/abs/2312.01026)、[A正式版](https://openaccess.thecvf.com/content/WACV2024/html/Kim_Token_Fusion_Bridging_the_Gap_Between_Token_Pruning_and_Token_WACV_2024_paper.html)；[全文](https://openaccess.thecvf.com/content/WACV2024/papers/Kim_Token_Fusion_Bridging_the_Gap_Between_Token_Pruning_and_Token_WACV_2024_paper.pdf)。预印本v1、正式版pp.1383–1392只计一项。
- 信号：模型对插值的局部敏感性、近线性程度；方式：在丢弃/合并间取舍，保范数合并，可有/无额外训练。
- 支持/反例潜力：明确提供合并不一定优于丢弃的机制性反例；平均操作引入分布偏移不是信息量单轴问题。
- 下一步：相同位置/比例下替换平均算子，范数恢复能否解释多数性能差异？

### C30 — LapMerge: Differentiable Exact-Budget Token Merging in Linear Time — **P**
- 年份：2026；作者：Magdalena Trędowicz、Aleksandra Nowak等（原站检索所见）；稳定ID：arXiv:2610.13858。核验[A](https://arxiv.org/abs/2610.13858)；[全文](https://arxiv.org/pdf/2610.13858)。摘要页投稿史只显示v1 10-09，搜索给v2 10-12；以实际取回摘要为准，版本差异待追。近期预印本。
- 信号：可学质量分布、具体任务损失待原文；方式：按等质量划分为严格N个有序段，Laplace核与前后缀扫描做可微线性聚合，预算可换。
- 支持/反例潜力：连续边界质量、严格预算与线性成本的最近邻；局部有序性是摘要明确的优势条件，不可泛化到任意打乱信息。
- 精读问题：硬边界/软跨段权重、边界梯度、N切换泛化、额外质量网络成本；与无学习同率均匀分段及ToMe对照是否齐全？

### C31 — QuickMerge++: Fast Token Merging with Autoregressive Prior
- 年份：2025；作者：Dong Liu、Yanxuan Yu（原站检索所见）；稳定ID：arXiv:2508.13204。核验[A](https://arxiv.org/abs/2508.13204)；[全文](https://arxiv.org/pdf/2508.13204)。v1。题名QuickMerge++经原站检索再次确认，摘要简称QuickMerge。
- 信号：注意力范数重要性、熵预算代理、下一单元预测；方式：学习合并序列上的轻量自回归先验。
- 支持/反例潜力：规则选择＋可学先验的组合，防止把下游适配训练记为策略学习；性能陈述较笼统，不能背书。
- **状态警示/下一步**：检索原站年度聚合页命中“will be withdrawn for revision”字样，但可能来自相邻记录；原始摘要仍在，聚合页Fetch返回429，**撤回状态未确认，不作为有效性能证据**。先复核单作品评论/版本状态，再核因果合并约束、先验贡献和各模态基线。该项仍计真实作品发现，不计已验证有效性。

### C32 — Recoverable Compression: A Multimodal Vision Token Recovery Mechanism Guided by Text Information — **P**
- 年份：2024预印本，2025 AAAI线索；作者：Yi Chen等（检索所见）；稳定ID：arXiv:2409.01179。核验[A](https://arxiv.org/abs/2409.01179)；[全文](https://arxiv.org/pdf/2409.01179)。v3。AAAI原站被反自动访问页阻挡，正式版元数据未从该页复核。
- 信号：问题文本与视觉单元相似度；方式：**免训练**动态恢复，找回视觉筛选时遗漏的文本相关单元，其余合并。
- 支持/反例潜力：本轮最接近“压缩＋保留可回访细节＋查询引导恢复”的已有组合之一，不宜宣称概念空白。
- 精读问题：原始表示保存在哪里、何时释放？恢复是从原集合选择还是从压缩向量重建？无恢复/无文本指导/无合并是否同预算，OCR和多问复用如何？

### C33 — Reroute, Don’t Remove: Recoverable Visual Token Routing for Vision-Language Models — **P**
- 年份：2026；作者：—；稳定ID：arXiv:2606.12412。核验[A](https://arxiv.org/abs/2606.12412)；[全文](https://arxiv.org/pdf/2606.12412)。v1，近期预印本。
- 信号：重用现有注意力排序和层间调度；方式：免训练，未选视觉单元旁路当前层，在后续决策重新入池。
- 支持/反例潜力：保留—选择—再访问的直接近邻；作者称永久删除对定位敏感，提示单时刻效用标签不可永久使用。
- 精读问题：延后单元的表示过时性、保留成本和位置关系；同理论TFLOPs/缓存“类别”是否真同字节数和延迟？是否查询条件、多粒度，还是仅同粒度延迟计算？

### C34 — CIVIC: End-to-End Sequence Compactness for Efficient Vision-Language Models
- 年份：2026；作者：—；稳定ID：arXiv:2605.28115。核验[A](https://arxiv.org/abs/2605.28115)；[全文](https://arxiv.org/pdf/2605.28115)。v1。
- 信号：文本对齐的分布蒸馏（KL：相对熵，用于对齐教师/学生分布）和空间保留下限；方式：视觉编码器至投影、预填充、缓存全链保持紧凑路径。
- 支持/反例潜力：可恢复操作本身会增加物理开销，与C32/C33构成成本反例；近期模型性能仅摘要声称。
- 下一步：去蒸馏/去保留下限/去紧凑路径消融；缓存、显存、预处理和解码全链计时。

### C35 — Can visual input Be Compressed? A visual input token compression benchmark for large multimodal models — **P**
- 年份：2025-11；作者：Tianfan Peng等；稳定ID：arXiv:2511.02650。核验[A](https://arxiv.org/abs/2511.02650)；[全文](https://arxiv.org/pdf/2511.02650)。v1 11-04，v2 11-15落在近12个月窗口；方法名UniPruneBench（统一视觉单元删减评测）。
- 信号/方式：评测研究，非新学习器；比较十种算法、六类能力、系统级时延。
- 支持/反例潜力：作者报告随机删减很强、无单一方法通吃、文字识别最敏感、比例主导退化；须优先检查学习策略是否真的超出强随机/均匀基线。
- 精读问题：同压缩率与同真实延迟下的排序、重训练是否公平、随机种子波动、任务平均是否遮盖文字细节损失？

## D. 文本/软表示压缩的信号与阶段训练（C36–C56）

### C36 — Learning to Compress Prompts with Gist Tokens — **P**
- 年份：2023；作者：Jesse Mu、Xiang Lisa Li、Noah Goodman（检索所见）；稳定ID：arXiv:2304.08467。核验[A](https://arxiv.org/abs/2304.08467)；[全文](https://arxiv.org/pdf/2304.08467)。v3 2024为NeurIPS 2023定稿。
- 信号：指令微调输出；方式：修改注意力遮罩迫使提示经少量摘要单元传递，不额外增训练阶段。
- 支持/反例潜力：任务监督而非逐字重建；摘要中算量减少与实时时间改善明显不同，成本结论不能混用。
- 精读问题：哪些提示可缓存、任务外泛化与细节复制；遮罩是否彻底切断原文旁路，摘要数和训练目标的独立贡献？

### C37 — Adapting Language Models to Compress Contexts — **P**
- 年份：2023；作者：A. Chevalier、A. Wettig、A. Ajith、D. Chen（检索所见引文；全名待补）；稳定ID：arXiv:2305.14788。核验[A](https://arxiv.org/abs/2305.14788)；[全文](https://arxiv.org/pdf/2305.14788)。v2；方法AutoCompressors。
- 信号：无监督后续语言模型预测；方式：分段处理，先前摘要作为软提示；适配预训练语言模型。
- 支持/反例潜力：不需逐字重建即可利用长文；层间/段间递归压缩不等于来源定位或回访。
- 精读问题：旧摘要梯度是否截断、段长与摘要数课程；先前摘要与当前原文旁路如何安排，重建预训练会否提升任务利用而非只记忆？

### C38 — In-context Autoencoder for Context Compression in a Large Language Model — **P**
- 年份：2023／2024 ICLR；作者：Tao Ge等（检索所见）；稳定ID：arXiv:2307.06945。核验[A](https://arxiv.org/abs/2307.06945)；[全文](https://arxiv.org/pdf/2307.06945)。v4 ICLR定稿；方法ICAE（上下文自编码器，把长文编码为少量记忆槽）。
- 信号：自编码重建＋语言模型预测预训练，再指令任务微调；方式：明确分阶段，约1%附加参数（作者摘要），冻结细节需原文。
- 支持/反例潜力：本轮最清晰的“重建/预测/任务”组合入口；记忆成功不自动说明跨问题充分。
- 精读问题：三目标各自消融、阶段顺序、冻结范围、训练重建与测试QA之间的相关性；相同槽数、总训练算量是否匹配？

### C39 — RECOMP: Improving Retrieval-Augmented LMs with Compression and Selective Augmentation — **P**
- 年份：2023；作者：Fangyuan Xu、Weijia Shi、Eunsol Choi；稳定ID：arXiv:2310.04408。核验[A](https://arxiv.org/abs/2310.04408)；[全文](https://arxiv.org/pdf/2310.04408)。v1；ICLR 2024关联来自检索引文，需总编目补官方元数据。
- 信号：下游语言模型/开放域QA性能；方式：抽取句子或生成摘要的两类压缩器，可输出空串以拒绝无增益检索；具体训练标签构造/优化器待原文。
- 支持/反例潜力：任务压缩与“是否值得读”共同决策的强近邻，未必需要保存全部细节。
- 精读问题：有用句子的标注是否用目标模型困惑度/答案信号；空串动作如何学、跨模型迁移、同摘要长度下抽取/生成公平性。

### C40 — Compressing Context to Enhance Inference Efficiency of Large Language Models
- 年份：2023；作者：Yucheng Li、Bo Dong、Chenghua Lin、Frank Guerin（检索所见）；稳定ID：ACL 2023.emnlp-main.391＝arXiv:2310.06201。核验[A](https://aclanthology.org/2023.emnlp-main.391/)；[全文](https://aclanthology.org/2023.emnlp-main.391.pdf)。方法Selective Context（选择性上下文：删去冗余文本以缩短输入）。
- 信号：信息量代理，具体自信息打分待全文；方式：输入裁剪，摘要未表明学习独立策略。
- 支持/反例潜力：搜索命中逐词/短语/句子粒度比较的原文定位线索，但本轮未读全文，不能把片段当已核验消融。
- 下一步：原文§5.5/Table 5线索，确认固定预算粒度排序及重建/任务评价差别。

### C41 — LongLLMLingua: Accelerating and Enhancing LLMs in Long Context Scenarios via Prompt Compression
- 年份：2023；作者：Huiqiang Jiang等（检索所见）；稳定ID：arXiv:2310.06839。核验[A](https://arxiv.org/abs/2310.06839)；[全文](https://arxiv.org/pdf/2310.06839)。v2 2024。
- 信号：问题关键性与信息密度/位置代理；方式：长上下文压缩，具体问题感知评分与重排恢复步骤待全文。
- 支持/反例潜力：改善性能可能来自去噪、重排和压缩共同作用，不能直接归于学到更好压缩器。
- 下一步：固定同顺序比较与问题无关压缩、多问同源复用时重新压缩成本。

### C42 — LLMLingua: Compressing Prompts for Accelerated Inference of Large Language Models
- 年份：2023；作者：Huiqiang Jiang等（检索所见）；稳定ID：arXiv:2310.05736。核验[A](https://arxiv.org/abs/2310.05736)；[全文](https://arxiv.org/pdf/2310.05736)。v2；EMNLP正式版2023.emnlp-main.825为检索引文关联，未额外抓取。
- 信号：信息量/模型分布对齐；方式：粗到细预算控制、迭代压缩及指令调优对齐。
- 支持/反例潜力：学习模型分布和固定删减规则可组合；不能把调优语言模型与学习删减动作混为一谈。
- 下一步：去对齐、去迭代、固定预算的独立消融及计算压缩本身成本。

### C43 — LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression — **P**
- 年份：2024；作者：Zhuoshi Pan等；稳定ID：arXiv:2403.12968。核验[A](https://arxiv.org/abs/2403.12968)；[全文](https://arxiv.org/pdf/2403.12968)。v2，页面确认Findings ACL 2024。
- 信号：教师生成的抽取压缩数据；方式：将保留/删除变为双向编码器的单元分类，任务无关的监督蒸馏。
- 支持/反例潜力：摘要明确批评单向熵既可能遗漏重要信息又不对齐压缩目标；适合和C10熵边界比较，但用途/接口不同不可直接排名。
- 精读问题：教师压缩的忠实性如何筛选，伪标签偏差、大小模型/单双向结构与目标差异分别贡献多少？

### C44 — TACO-RL: Task Aware Prompt Compression Optimization with Reinforcement Learning — **P**
- 年份：2025；作者：Shivam Shandilya、Menglin Xia、Supriyo Ghosh、Huiqiang Jiang、Jue Zhang、Qianhui Wu、Victor Rühle、Saravan Rajmohan；稳定ID：ACL 2025.findings-acl.81。核验[A](https://aclanthology.org/2025.findings-acl.81/)；[全文](https://aclanthology.org/2025.findings-acl.81.pdf)。搜索索引日期错标2026，按正式卷年2025。
- 信号：摘要、QA、代码摘要的任务特定奖励；方式：已有编码器分类器加轻量REINFORCE（回报加权离散采样的策略梯度方法）。
- 支持/反例潜力：作者称同压缩率和延迟优于任务无关分类；是最直接检验“学习信号对齐是否胜过熵/教师通用压缩”的候选。
- 精读问题：初始分类器是否同C43，奖励与真实评价是否同源过拟合，奖励查询预算、方差和固定同率随机/统计对照。

### C45 — PISCO: Pretty Simple Compression for Retrieval-Augmented Generation — **P**
- 年份：2025；作者：Maxime Louis等（检索所见）；稳定ID：arXiv:2501.16075＝ACL 2025.findings-acl.800。核验[A预印本](https://arxiv.org/abs/2501.16075)、[A正式版](https://aclanthology.org/2025.findings-acl.800/)；[全文](https://aclanthology.org/2025.findings-acl.800.pdf)。一个作品。
- 信号：文档问题的序列级教师输出；方式：不做额外预训练或人工标签，仅蒸馏微调。
- 支持/反例潜力：与C38/C56重建预训练路径直接竞争；“无预训练”不等于不使用预训练底座。
- 精读问题：去重建是否真省总预算、教师生成数据成本、全上下文教师是否可靠；预印本摘要称单A100 48小时，正式版称24小时，必须按版本及训练设置取数，不混引。

### C46 — LoCoCo: Dropping In Convolutions for Long Context Compression
- 年份：2024；作者：Ruisi Cai、Yuandong Tian、Zhangyang Wang、Beidi Chen（检索所见）；稳定ID：arXiv:2406.05317。核验[A](https://arxiv.org/abs/2406.05317)；[全文](https://arxiv.org/pdf/2406.05317)。v2。
- 信号：上下文建模适配，具体目标待全文；方式：一维卷积动态生成缓存槽的混合权重，旧键值与新输入融合，固定缓存大小。
- 支持/反例潜力：数据驱动融合与规则裁剪竞争；槽是存储粒度不必是可寻址来源块。
- 下一步：冻结/训练参数范围、卷积位置感受野、局部细节不可逆丢失、与规则缓存同内存/实时时间匹配。

### C47 — Cramming 1568 Tokens into a Single Vector and Back Again: Exploring the Limits of Embedding Space Capacity — **P**
- 年份：2025；作者：Yuri Kuratov、Mikhail Arkhipov、Aydar Bulatov、Mikhail Burtsev；稳定ID：ACL 2025.acl-long.948＝arXiv:2502.13063。核验[A](https://aclanthology.org/2025.acl-long.948/)；[全文](https://aclanthology.org/2025.acl-long.948.pdf)。
- 信号：逐样本重建；方式：用每样本优化替代通用编码器。
- 支持/反例潜力：作者发现可存在远高于通用编码器实现的压缩率，提醒瓶颈可能是摊销学习而非单向量容量；反过来不能用逐样本优化存在性背书可部署泛化编码。
- 精读问题：向量精度、每样本迭代/时间、解码器先验、原文不确定性；无损标准与任务问答是否不同，是否涉及训练集记忆？

### C48 — A Two-Stage Training Recipe for Soft Context Compression in RAG — **P**
- 年份：2026；作者：—；稳定ID：arXiv:2609.05152。核验[A](https://arxiv.org/abs/2609.05152)；[全文](https://arxiv.org/pdf/2609.05152)。v2；方法DEX-Comp（两阶段压缩：先可靠教师模仿，再失败题探索），近期预印本。
- 信号：教师答对题上的蒸馏、教师答错题上的答案正确性；方式：两阶段，纯蒸馏后结果奖励强化学习。
- 支持/反例潜力：直接反对无条件模仿教师，声称压缩模型可超未调优全上下文模型；未精读不接受其“超越”因果解释。
- 精读问题：教师正确性判定、划分和奖励数据泄漏；同训练算量的全上下文调优、随机划分、全题蒸馏/全题强化、阶段顺序是否齐全？

### C49 — 500xCompressor: Generalized Prompt Compression for Large Language Models
- 年份：2024预印本／2025 ACL；作者：Zongqian Li、Yixuan Su、Nigel Collier（检索所见）；稳定ID：arXiv:2408.03094＝ACL 2025.acl-long.1219。核验[A正式版](https://aclanthology.org/2025.acl-long.1219/)；[全文](https://aclanthology.org/2025.acl-long.1219.pdf)。
- 信号：语料预训练后QA微调；方式：少量附加参数，压入少量特殊单元的键值表示；重建等预训练细节待全文。
- 支持/反例潜力：摘要明确高压缩保留能力并非100%，且键值优于嵌入；压缩率不是跨接口等价信息预算。
- 下一步：同存储字节数比较键值/嵌入、训练测试重叠与细节查询；标题500倍不可简写成无损500倍。

### C50 — Evaluating Compressed Memory: Dependence, Utility, and Content Benefit — **P**
- 年份：2026；作者：—；稳定ID：arXiv:2610.19373。核验[A](https://arxiv.org/abs/2610.19373)；[全文](https://arxiv.org/pdf/2610.19373)。v1，近期预印本。
- 信号/方式：评测研究；结合置零与分别训练的无记忆/常量记忆对照，测试内容收益而非单纯依赖。
- 支持/反例潜力：作者报告一些系统置零下降但仍劣于训练好的无记忆模型；错误文档向量也可能改善答案重叠评分。对学习信号和真实因果消费极重要。
- 精读问题：九系统的训练公平性、生成条件/随机种子和绝对性能；无记忆、常量、错文档、正确来源是否全套匹配，统计不确定性是否支持主要判词？

### C51 — Compressing Sequences in the Latent Embedding Space: K-Token Merging for Large Language Models
- 年份：2026；作者：—；稳定ID：arXiv:2604.15153。核验[A](https://arxiv.org/abs/2604.15153)；[全文](https://arxiv.org/pdf/2604.15153)。v3；初次搜索标题被截断，后续用稳定ID检索原站已补全题名。
- 信号：结构推理、情感分类、代码编辑任务；方式：轻编码器将连续K个嵌入合为一个，语言模型做低秩适配，输出仍原词表。
- 支持/反例潜力：固定粒度＋可学内容压缩，利于分离“边界学不学”与“压缩映射学不学”。
- 下一步：编码器训练信号、固定分组随机偏移、同预算均值/线性映射、任务泛化与因果可见性。

### C52 — Beyond Position Bias: Shifting Context Compression from Position-Driven to Semantic-Driven
- 年份：2026；作者：—；稳定ID：arXiv:2605.09463。核验[A](https://arxiv.org/abs/2605.09463)；[全文](https://arxiv.org/pdf/2605.09463)。v1；方法SeCo（语义一致性上下文压缩：围绕查询相关语义中心聚合）。
- 信号：查询相关性、语义一致性；方式：选中心并加权合并；参数是否训练及具体目标摘要不足。
- 支持/反例潜力：与固定位置压缩相反的近期机制提案；“消除位置偏差”是作者声称，不能据此排除排序、位置编码和分布差异。
- 下一步：按同保留长度、同编码器和同训练预算替换中心选择；多问共享压缩的失效与重新压缩成本。

### C53 — E2LLM: Encoder Elongated Large Language Models for Long-Context Understanding and Reasoning
- 年份：2024；作者：—；稳定ID：arXiv:2409.06679。核验[A](https://arxiv.org/abs/2409.06679)；[全文](https://arxiv.org/pdf/2409.06679)。v3 2026-04；最新摘要不能倒引为2024已有LongBench v2结果。
- 信号：编码器输出重建＋长上下文指令微调；方式：分块压成软提示，经适配器对齐解码器，阶段/冻结细节待全文。
- 支持/反例潜力：重建的是编码器输出而不必是原文，适合检查“重建监督”内部异质性；现成编码器迁移与端到端自学压缩竞争。
- 下一步：重建对象、辅助损失/任务适配有无同预算独立消融，v1/v3结论差异与总编码成本。

### C54 — CompAct: Compressing Retrieved Documents Actively for Question Answering
- 年份：2024；作者：Chanwoong Yoon、Taewhoo Lee、Hyeon Hwang、Minbyul Jeong、Jaewoo Kang；稳定ID：ACL 2024.emnlp-main.1194。核验[A](https://aclanthology.org/2024.emnlp-main.1194/)；[全文](https://aclanthology.org/2024.emnlp-main.1194.pdf)。
- 信号：多跳QA效用，具体教师/训练标签待全文；方式：主动而非单步地凝缩检索文档，可插不同检索器/读出器。
- 支持/反例潜力：压缩后发现缺口、继续取信息的近邻，但摘要不足以确认是否维护细粒度来源映射。
- 下一步：停止/继续规则是否学习、是否重新读原文、证据链/引用保持、总轮次成本与相同预算单步压缩。

### C55 — xRAG: Extreme Context Compression for Retrieval-augmented Generation with One Token
- 年份：2024；作者：Xin Cheng等；稳定ID：arXiv:2405.13792。核验[A](https://arxiv.org/abs/2405.13792)；[全文](https://arxiv.org/pdf/2405.13792)。v2；NeurIPS正式版由搜索官方页面关联，未额外取回。
- 信号：检索表示→语言模型表示对齐；方式：检索器和语言模型均冻结，仅训练模态桥，复用离线文档嵌入。
- 支持/反例潜力：保存/读取/接口分工清晰，与全模型联合训练不同；C50点名该方法，必须配套读其反证。
- 下一步：桥接目标、是否含重建/蒸馏、错文档收益、检索训练先验、精确细节与跨问题复用。

### C56 — Context Embeddings for Efficient Answer Generation in RAG
- 年份：2024；作者：David Rau等（检索所见）；稳定ID：arXiv:2407.09252。核验[A](https://arxiv.org/abs/2407.09252)；[全文](https://arxiv.org/pdf/2407.09252)。v3；WSDM正式版题“...in Retrieval-Augmented Generation”由搜索关联，编目待核官方摘要。方法COCOM（上下文嵌入压缩：用少量嵌入替代检索长文）。
- 信号：QA与压缩训练，具体重建预训练未由摘要证实；方式：可调压缩率、多上下文表示，阶段安排待全文。
- 支持/反例潜力：与C45“无需额外预训练”争议直接相接，且可检验轻编码器与语言模型编码器差异。
- 下一步：预训练/任务训练目标、冻结范围、不同率是否共用参数；多文档融合和来源可追溯性。

## E. 第一轮可比消融地图（不是跨论文性能排名）

| 要分离的因素 | 优先作品 | 必须提取的对照 | 摘要层能/不能得出的结论 |
|---|---|---|---|
| 边界监督来源 vs 梯度方式 | C07、C10、C11、C12 | 固定/子词/语言学/熵/主损失；同段长与同算量 | C07明确有多来源比较；具体优胜条件未核 |
| 学边界 vs 学压缩内容 | C05–C09、C11、C51 | 固定边界＋学聚合；学边界＋同聚合；均匀/随机 | 现有组合覆盖两轴，尚无统一同码因果比较 |
| 规则免训练 vs 模型适应 | C24、C28、C29 | 同骨干、相同比例插入/微调；合并/丢弃 | “训练后好”不证明合并策略本身被学习 |
| 表示重建 vs 任务反馈 | C25、C38、C45、C47、C53 | 原文/隐状态/输出响应三种重建；任务分布外 | 重建目标不是一个同质类别，不能统称保信息 |
| 教师模仿 vs 任务奖励 | C43、C44、C45、C48 | 相同初始压缩器、教师质量、奖励预算与任务 | C48提供教师失误反馈的近期竞争假说 |
| 离散策略梯度 vs 可微近似 | C18、C20、C21、C07、C11 | 同任务/同率、方差、硬化差、训练稳定性 | 有相关技术谱系，尚未跨域统一比较 |
| 联合 vs 分阶段/冻结 | C06、C11、C13、C38、C45、C55 | 相同总训练成本、预训练数据、冻结范围 | 分阶段可兼容现成模型，但性能取决信号与适配 |
| 多粒度＋来源回访 | C26、C32、C33、C54 | 无回访、随机回访、查询回访；原始表示存储成本 | 至少已有相近组合，尚不能说完整同构或不存在 |
| 依赖 vs 内容效用 | C35、C50、C55 | 强随机、另训练无通道/常量、错来源与真来源 | 摘要足以优先安排反例阅读，不足以判死所有压缩 |

**不得混淆**：token域压缩候选不能给字节接口普遍背书；多视觉单元可回访也不能直接证明原始字节来源可回访。学习规则、可学习聚合器、训练骨干适应固定规则，以及可变测试预算，必须分别记账。
