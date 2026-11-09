# T06 候选作品：按需加工、跨层读取与真实系统成本

日期：2026-11-08。**55个去重作品；54篇论文摘要核验+1项官方介绍核验；28项★精读优先；全文精读0。** 检索与抓取调用明细见 SEARCH_LOG.md，下一轮分工建议见 HANDOFF.md。

## 阅读口径与初筛坐标

- `A`：已Fetch原始摘要页并读摘要/提交历史；`O`：已读官方介绍。都不意味着读过论文正文、核验代码或复现实验。版本为本轮所见最新提交历史；年份优先写首发年，后附修订/正式版。完整作者未抽取处记`—`，不从“From/提交人”推断作者。
- `★`只表示下一轮全文阅读优先，不是质量背书。所有数值均为**作者摘要或官方自报**，目前证据位置为原页Abstract或明确的官方小节；尚不具备正文页码、表号或独立复核。
- **加工深度**：同一位置执行多少次变换；**信息粒度**：被保存/寻址/读取的对象是原始位置、片段、汇总还是多级对象。二者可独立变化；循环多次不自动产生多粒度存储，深层表征不自动等于更粗语义单位。
- **跨层读取**：读早层状态或K/V（键/值向量）；**来源回访**：能按地址回到保留的原始位置或更细对象。前者可能保持逐位置坐标，但不自动具备后者的多级地址与生命周期保证。
- **真跳算**：执行路径确实不运行未选模块，而不是先算出结果再乘小门值；摘要说“skip”只记为作者声称，代码/执行轨迹仍待查。静态剪层、动态门值、条件执行、采样分布精确性、墙钟收益分别标注，不能互相代替。

## A. 基础：选择更新、时钟、copy与transform（8项）

### T06-001 ★ Adaptive Computation Time for Recurrent Neural Networks
- 身份：Alex Graves；2016；arXiv:1603.08983，v6（2017-02-21）。核验A。[原始摘要](https://arxiv.org/abs/1603.08983)；[全文PDF入口](https://arxiv.org/pdf/1603.08983)。
- 机制：每输入与输出之间学习内部迭代步数。选择的是加工次数，不是把输入按信息粒度重建。摘要还指出计算集中于词间空格和句末等难预测转折。
- 支持/反例潜力：支持任务依赖计算；**字符语言建模没有明显性能增益**是摘要直接承认的限制，不能只引用合成题收益。
- 精读问题：停止损失怎样权衡成本？所有位置是否仍运行到批中最深步？边界相关性是后验观察还是可控分段信号？

### T06-002 ★ Universal Transformers
- 身份：Mostafa Dehghani、Stephan Gouws、Oriol Vinyals、Jakob Uszkoreit、Łukasz Kaiser（Q08公开引用线索；完整书目待统一目录再校）；2018首发/ICLR2019；arXiv:1807.03819，v3（2019-03-05）。核验A。[摘要](https://arxiv.org/abs/1807.03819)；[PDF](https://arxiv.org/pdf/1807.03819)。
- 机制：位置并行、深度递归的共享自注意力模型，带逐位置停止机制。重复共享层不等于压缩地址。
- 支持/反例潜力：长度外推/算法任务是支持线；图灵完备性有假设，不可外推成固定预算下的高效性。翻译提升并非通用系统加速证明。
- 精读问题：已停位置仍能作为K/V被读吗？停止后的状态能否重激活？深度步编码和最大步数如何改变容量与计算匹配？

### T06-003 PonderNet: Learning to Ponder
- 身份：Andrea Banino、Jan Balaguer、Charles Blundell；2021；arXiv:2107.05407，v2（2021-09-02）。核验A。[摘要](https://arxiv.org/abs/2107.05407)；[PDF](https://arxiv.org/pdf/2107.05407)。
- 机制：学习计算步骤数，在预测准确率、计算成本与泛化间折衷；改变加工深度而非地址粒度。
- 支持/反例潜力：合成任务外推和问答是支持；摘要未提供LLM连续批处理下的墙钟结果。下一步查停止分布、先验、训练与推理执行量差异及比ACT稳定的适用域。

### T06-004 A Clockwork RNN
- 身份：Jan Koutník、Klaus Greff、Faustino Gomez、Jürgen Schmidhuber（Q30公开引用）；2014；arXiv:1402.3511，v1。核验A。[摘要](https://arxiv.org/abs/1402.3511)；[PDF](https://arxiv.org/pdf/1402.3511)。
- 机制：隐藏层分组，不同组按各自固定时钟更新；明确多时间尺度，但并非查询条件的细粒度来源读取。
- 支持/反例潜力：固定调度是减少路由开销的强对照；只验证音频生成/TIMIT等任务，不能直接作语言多级记忆结论。下一步查跨组连接、状态保留和报告加速的硬件/批量。

### T06-005 ★ Hierarchical Multiscale Recurrent Neural Networks
- 身份：Junyoung Chung、Sungjin Ahn、Yoshua Bengio（Q30公开引用）；2016首发/ICLR2017；arXiv:1609.01704，v7（2017-03-09）。核验A。[摘要](https://arxiv.org/abs/1609.01704)；[PDF](https://arxiv.org/pdf/1609.01704)。
- 机制：通过更新机制捕捉不同时间尺度/潜在层级，字符语言建模与手写序列，无显式边界监督。
- 支持/反例潜力：比纯深度循环更接近“层级+选择更新”；但层级状态不是原始来源可恢复索引，也可能只是有效时间常数。
- 精读问题：COPY/UPDATE/FLUSH三类动作的确切条件及梯度估计是什么？哪些状态被覆盖不可逆？边界和信息粒度是否有独立因果证据？真实执行是否跳过未更新组？

### T06-006 Skip RNN: Learning to Skip State Updates in Recurrent Neural Networks
- 身份：Víctor Campos等（Q17原始搜索结果）；2017首发/2018修订；arXiv:1708.06834，v3（2018-02-05）。核验A。[摘要](https://arxiv.org/abs/1708.06834)；[PDF](https://arxiv.org/pdf/1708.06834)。
- 机制：学习跳过状态更新，可施加更新预算；保留状态与变换状态分离，选择轴为时间更新。
- 支持/反例潜力：直接支持“不必每次写入”；不证明跳过输入的信息仍被保存可回访。下一步查跳过输入是否永久遗失、梯度估计、预算塌缩、稀疏更新和实际延迟。

### T06-007 Highway Networks
- 身份：Rupesh Kumar Srivastava、Klaus Greff、Jürgen Schmidhuber；2015；arXiv:1505.00387，v2（2015-11-03）。核验A。[摘要](https://arxiv.org/abs/1505.00387)；[PDF](https://arxiv.org/pdf/1505.00387)。
- 机制：门控信息通路，使深层网络更易训练；是保留通路/变换通路分离的基础入口。
- 支持/反例潜力：门控保留可以改善梯度，但连续门不保证计算分支关闭。下一步查carry/transform门耦合公式与稀疏门是否真的触发条件执行，不把“高速公路”比喻当延迟结果。

### T06-008 Highway and Residual Networks Learn Unrolled Iterative Estimation
- 身份：—（作者元数据待补；不将网页提交人冒认为完整作者）；2016首发/2017修订；arXiv:1612.07771，v3（2017-03-14）。核验A。[摘要](https://arxiv.org/abs/1612.07771)；[PDF](https://arxiv.org/pdf/1612.07771)。
- 机制：连续层可以迭代精化同一特征，不必逐层产生越来越抽象的新表示。
- 支持/反例潜力：直接反对“层深=语义粒度”必然对应；作者称为替代解释/初步实验，不能升级成所有Transformer的定律。下一步查实验域及可区分层级抽象与同特征精化的干预。

## B. 动态深度、跳层、早退与静态对照（13项）

### T06-009 Depth-Adaptive Transformer
- 身份：Maha Elbayad、Jiatao Gu、Edouard Grave、Michael Auli（Q16公开引用）；2019首发/2020修订；arXiv:1910.10073，v4（2020-02-14）。核验A。[摘要](https://arxiv.org/abs/1910.10073)；[PDF](https://arxiv.org/pdf/1910.10073)。
- 机制：不同层可预测输出并估计序列所需计算；与UT共享层重复不同，深度变化同时改变可用参数容量。
- 支持/反例潜力：翻译中少于四分之一解码层可匹配基线是作者结论；计算/参数不可混为同轴。下一步查出口损失、批处理等待及decoder历史缺层状态处理。

### T06-010 Confident Adaptive Language Modeling
- 身份：Tal Schuster、Adam Fisch、Jai Gupta、Mostafa Dehghani、Dara Bahri、Vinh Tran、Yi Tay、Donald Metzler（Q16/Q21公开引用）；2022；arXiv:2207.07061，v2（2022-10-25）；NeurIPS2022关联。核验A。[摘要](https://arxiv.org/abs/2207.07061)；[PDF](https://arxiv.org/pdf/2207.07061)。
- 机制：按输入和生成步动态分配计算，校准出口置信度，将局部早退决策连接序列质量约束，处理过去token缺失隐藏状态。
- 支持/反例潜力：对缺层读取有直接价值；摘要写的是最高3倍**潜在**加速，不是当前服务栈已实现吞吐。下一步查保证针对哪一种质量分布、复制缺层状态的误差和校准迁移。

### T06-011 SkipDecode: Autoregressive Skip Decoding with Batching and Caching for Efficient LLM Inference
- 身份：Luciano Del Corro、Allie Del Giorno、Saurabh Agarwal、Bin Yu、Ahmed Awadallah、Subhabrata Mukherjee（Q16公开引用）；2023；arXiv:2307.02628，v1。核验A。[摘要](https://arxiv.org/abs/2307.02628)；[PDF](https://arxiv.org/pdf/2307.02628)。
- 机制：批内同位置使用一致出口，出口深度单调减少；跳低/中层、保留上层，避免重算过去K/V。
- 支持/反例潜力：直接指出逐token早退受批内最慢者限制；对照说明更强调度限制可能比更精细路由更快。作者报OPT模型2—5倍加速，须核实质量/批量/长度和非适应性部分。

### T06-012 Learning to Skip for Language Modeling
- 身份：Dewen Zeng、Nan Du、Tao Wang、Yuanzhong Xu、Tao Lei、Zhifeng Chen、Claire Cui；2023；arXiv:2311.15436，v1。核验A。[摘要](https://arxiv.org/abs/2311.15436)；[PDF](https://arxiv.org/pdf/2311.15436)。
- 机制：二元路由器允许任意位置跳过层/模块，不限于单调早退。
- 支持/反例潜力：支持跳过后还能继续后层加工；但作者强调24任务1-shot提高、推理仅轻微额外成本，不是“动态所以更快”。下一步查路由因果性、硬跳过执行与等FLOPs对照。

### T06-013 ★ Mixture-of-Depths: Dynamically Allocating Compute in Transformer-Based Language Models
- 身份：David Raposo、Sam Ritter、Blake Richards、Timothy Lillicrap、Peter Conway Humphreys、Adam Santoro（Q06公开引用）；2024；arXiv:2404.02258，v1。核验A。[摘要](https://arxiv.org/abs/2404.02258)；[PDF](https://arxiv.org/pdf/2404.02258)。
- 机制：每层最多k个token参加注意力和MLP，位置动态但总量/张量尺寸已知。真跳算机制的直接种子，不是压缩原始信息粒度。
- 支持/反例潜力：固定预算可兼容静态图；作者报采样步可快50%以上，须区分预填充与逐步解码以及非因果top-k。
- 精读问题：序列top-k如何避免未来信息？训练/推理路由替代误差多大？未选位置K/V如何保留、何时可重入？把路由/聚散/缓存算全后收益还剩多少？

### T06-014 ★ MoDification: Mixture of Depths Made Easy
- 身份：Chen Zhang、Meizhi Zhong、Qimeng Wang等（原页作者表）；2024；arXiv:2410.14268，v1。核验A。[摘要](https://arxiv.org/abs/2410.14268)；[PDF](https://arxiv.org/pdf/2410.14268)。
- 机制：将top-k选择改为threshold-p阈值选择，并配合架构和数据转换已有LLM。
- 支持/反例潜力：明确反例：原MoD不经昂贵训练难以转换现有模型；作者报约1.2倍延迟加速、1.8倍内存下降，不能套用MoD更大速度数字。
- 精读问题：阈值是否可逐token因果执行？预算波动怎样影响批量/图捕获？保留哪部分全局读取？训练成本和长上下文收益是否分开报？

### T06-015 ★ LayerSkip: Enabling Early Exit Inference and Self-Speculative Decoding
- 身份：Mostafa Elhoushi、Akshat Shrivastava等（原页作者表）；2024；arXiv:2404.16710，v4（2024-10-18）；ACL2024正式版见 https://aclanthology.org/2024.acl-long.681/ （搜索确认关联）。核验A。[摘要](https://arxiv.org/abs/2404.16710)；[PDF](https://arxiv.org/pdf/2404.16710)。
- 机制：层dropout+共享早退出口；浅层起草、深层核验纠错，复用激活与计算。
- 支持/反例潜力：真省计算可以来自起草/验证调度，而非直接删掉所有深层；作者报任务相关1.82—2.16倍，非跨任务统一保证。
- 精读问题：直接早退与自投机分别损失多少质量/采样精确性？校验会重算什么？接受率、内存、峰值批量、最坏延迟和训练开销如何量？

### T06-016 Mixture of Multi-Rate Residuals for Efficient Transformer Inference
- 身份：Nikhil Bhendawade等（Q06 OpenReview作者线索，完整作者待补）；2025；arXiv:2502.02040，v1。核验A。[摘要](https://arxiv.org/abs/2502.02040)；[PDF](https://arxiv.org/pdf/2502.02040)。
- 机制：不仅调残差经过层数，还调其演化速度，使浅层早对齐深层；结合自投机和专家预加载。
- 支持/反例潜力：支持“更少步但更大变换”与“少读信息”是不同机制；2.8倍/2.9倍为不同配置作者值。下一步查残差速度定义、训练损失、加载提前量及与专用kernel贡献分离。

### T06-017 ★ Adaptive Layer-skipping in Pre-trained LLMs
- 身份：—（作者元数据待补）；2025；FlexiDepth，arXiv:2503.23798，v3（2025-10-08）；原页标明COLM2025。核验A。[摘要](https://arxiv.org/abs/2503.23798)；[PDF](https://arxiv.org/pdf/2503.23798)。
- 机制：冻结原参数、加路由器/适配器，按token类型与不确定度调层数；Llama3-8B可跳8/32层而保持基准结果。
- 支持/反例潜力：**作者明确承认尚无墙钟加速：异质跳层模式和I/O开销抵消计算节省。** 本轮最直接系统反例之一。
- 精读问题：哪项I/O、批量和kernel造成瓶颈？跳层模式是否能块状/批内对齐？所报“全性能”涵盖哪些长推理及安全任务？

### T06-018 What Layers When: Learning to Skip Compute in LLMs with Residual Gates
- 身份：Filipe Laitenberger等（Q05正式版作者线索；完整作者待补）；2025首发/ICLR2026；GateSkip，arXiv:2510.13876，v3（2026-02-07）。核验A。[摘要](https://arxiv.org/abs/2510.13876)；[PDF](https://arxiv.org/pdf/2510.13876)。
- 机制：注意力/MLP残差支路加连续门；推理按门值对token排序、用逐层预算跳过低重要性者。
- 支持/反例潜力：长推理15%计算节省却仅保留90%以上基线准确率，质量约束不可忽略；指令模型近50%省计算是不同考场。下一步审查用输出门值决定跳过是否需先跑支路、因果可部署代理与真实kernel。
- 版本关联：搜索中正式版题名为Learning to Skip Compute in LLMs with Residual Gates，按同一arXiv作品只计一次。

### T06-019 Balcony: A Lightweight Approach to Dynamic Inference of Generative Language Models
- 身份：Benyamin Jamialahmadi、Parsa Kavehzadeh、Mehdi Rezagholizadeh等（Q33公开引用）；2025；arXiv:2503.05005，v2（2025-03-10）；EMNLP2025关联仅搜索确认，差异待查。核验A。[摘要](https://arxiv.org/abs/2503.05005)；[PDF](https://arxiv.org/pdf/2503.05005)。
- 机制：冻结LLM，在指定出口插入额外层并自蒸馏，按预算使用子模型。
- 支持/反例潜力：是预算可伸缩基线，不自动是逐查询效用最优路由；额外出口层占用参数/计算。下一步查出口选择粒度、出口训练成本、与LayerSkip硬件/批量是否同口径。

### T06-020 ShortGPT: Layers in Large Language Models Are More Redundant Than You Expect
- 身份：Xin Men、Mingyu Xu、Qingyu Zhang、Bingning Wang、Hongyu Lin、Yaojie Lu、Xianpei Han、Weipeng Chen（Q28公开书目）；2024；arXiv:2403.03853，v3（2024-10-11）。核验A。[摘要](https://arxiv.org/abs/2403.03853)；[PDF](https://arxiv.org/pdf/2403.03853)。
- 机制：按Block Influence删除低影响层，是静态剪枝而非动态按需算。
- 支持/反例潜力：动态路由必须胜过静态便宜对照，否则“不同token不同深度”不一定有净价值。下一步查长推理、域迁移与删除后的质量；相似度不能直接推出功能冗余。

### T06-021 The Unreasonable Ineffectiveness of the Deeper Layers
- 身份：Andrey Gromov、Kushal Tirumala、Hassan Shapourian、Paolo Glorioso、Daniel A. Roberts（Q28公开引用）；2024首发/2025修订；arXiv:2403.17887，v2（2025-03-03）。核验A。[摘要](https://arxiv.org/abs/2403.17887)；[PDF](https://arxiv.org/pdf/2403.17887)。
- 机制：按跨层相似性选择连续剪层区间，再轻量微调“修复”；部分常见问答基准去掉接近半层仍少损伤。
- 支持/反例潜力：对“更深总更好”构成限定反例；作者明确语境是部分模型/常见问答，不等于推理或保真复制能力不需深度。下一步查修复算力、模型家族与评价盲区。

## C. 共享层循环、缓存与实际调度（13项）

### T06-022 ★ Relaxed Recursive Transformers: Effective Parameter Sharing with Layer-wise LoRA
- 身份：Sangmin Bae、Adam Fisch、Hrayr Harutyunyan、Ziwei Ji、Sungnyun Kim、Tal Schuster（Q08公开引用）；2024首发/ICLR2025；arXiv:2410.20672，v3（2025-02-28）。核验A。[摘要](https://arxiv.org/abs/2410.20672)；[PDF](https://arxiv.org/pdf/2410.20672)。
- 机制：把现成LLM转成重复共享块，用逐深度低秩适配松绑；提出连续深度批处理。
- 支持/反例潜力：参数共享与层专用容量可分开调；摘要的2—3倍吞吐是**理论分析的潜力**，不能当已实现结果。
- 精读问题：共享初始化/逐层LoRA分别贡献多少？训练与推理算量是否仍等同原深度？连续深度批处理的理论上界假设何种出口先验/同步/内存带宽？

### T06-023 ★ Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach
- 身份：Jonas Geiping、Sean McLeish、Neel Jain、John Kirchenbauer、Siddharth Singh、Brian R. Bartoldson、Bhavya Kailkhura、Abhinav Bhatele、Tom Goldstein；2025；Huginn，arXiv:2502.05171，v2（2025-02-17）。NeurIPS2025条目在Q14发现，未逐版核对。核验A。[摘要](https://arxiv.org/abs/2502.05171)；[PDF](https://arxiv.org/pdf/2502.05171)。
- 机制：重复潜在空间块，测试时加深，无须专用思维链训练数据；3.5B/800B-token概念验证模型。
- 支持/反例潜力：支持增加知识加工而不生成显式推理token；摘要“相当于50B计算负荷”不是50B知识容量或相同延迟。
- 精读问题：噪声初始化、输入反复注入、截断反传怎样稳定循环？额外步在什么任务无益/有害？逐循环K/V占用、停止准则和长窗系统成本是什么？

### T06-024 ★ Scaling Latent Reasoning via Looped Language Models
- 身份：Rui-Jie Zhu、Zixuan Wang、Kai Hua等（原页作者表）；2025首发/2026修订；Ouro，arXiv:2510.25741，v6（2026-10-11）。核验A。[摘要](https://arxiv.org/abs/2510.25741)；[PDF](https://arxiv.org/pdf/2510.25741)。
- 机制：共享栈反复加工，熵正则学习深度分配，预训练7.7T tokens。作者把收益归于知识操作而非知识容量。
- 支持/反例潜力：重要支持“存储与加工分离”；摘要的learned depth并不证明公开实现真早停，不能只看选中的输出层。
- 精读问题：训练深度分布与推理出口如何实施？未选循环是否仍执行？知识容量/操作的控制实验是否排除总训练FLOPs差异？v1—v6机制或评价有何变化？

### T06-025 ★ Mixture-of-Recursions: Learning Dynamic Recursive Depths for Adaptive Token-Level Computation
- 身份：Sangmin Bae、Yujin Kim、Reza Bayat、Sungnyun Kim、Jiyoun Ha、Tal Schuster、Adam Fisch、Hrayr Harutyunyan、Ziwei Ji、Aaron Courville、Se-Young Yun；2025；arXiv:2507.10524，v3（2025-10-25）。NeurIPS2025关联由搜索发现，正文差异待核。核验A。[摘要](https://arxiv.org/abs/2507.10524)；[PDF](https://arxiv.org/pdf/2507.10524)。
- 机制：共享层+逐token递归深度路由；注意力只在仍活跃token间计算，选择性保存K/V；另有首次循环K/V复用变体。
- 支持/反例潜力：同时碰到选择加工和读取可见性，是最直接邻近基线；活跃集缩小可能省算也可能切断早停位置的信息。
- 精读问题：停止token是否还能被后续活跃token读取？有无重新入场？训练/解码路由因果性、选择性缓存丢失、K/V共享质量、同训练FLOPs及实测吞吐如何拆开？

### T06-026 Inner Thinking Transformer: Leveraging Dynamic Depth Scaling to Foster Adaptive Internal Thinking
- 身份：Yilong Chen、Junyuan Shang、Zhenyu Zhang、Yanxi Xie、Jiawei Sheng、Tingwen Liu、Shuohuan Wang、Yu Sun、Hua Wu、Haifeng Wang（Q31公开引用）；2025；arXiv:2502.13842，v2（2025-02-23）；ACL2025正式版入口 https://aclanthology.org/2025.acl-long.1369.pdf 。核验A。[摘要](https://arxiv.org/abs/2502.13842)；[PDF](https://arxiv.org/pdf/2502.13842)。
- 机制：自适应token路由、残差思考连接和步骤编码，在小参数模型内加深关键token。
- 支持/反例潜力：支持以深度换参数/数据，但162M—466M实验不能直接保证大型服务模型收益；96.5%性能不等于逐任务无损。下一步查路由标签、等算力/等参数区分及实际延迟而非只有弹性FLOPs。

### T06-027 ★ Memory-Efficient Looped Transformer: Decoupling Compute from Memory in Looped Language Models
- 身份：Victor Conchello Vendrell、Arnau Padres Masdemont、Niccolo Grillo、Jordi Ros-Giralt、Arash Behboodi、Fabio Valerio Massoli（Q39公开引用）；2026；MELT，arXiv:2605.07721，v3（2026-09-28）。核验A。[摘要](https://arxiv.org/abs/2605.07721)；[PDF](https://arxiv.org/pdf/2605.07721)。
- 机制：每层单份K/V跨循环共享、门控更新；分块训练+插值迁移+注意力对齐蒸馏，从Ouro改造。
- 支持/反例潜力：直接处理循环越多缓存越大的隐性成本；但覆盖旧K/V与逐循环地址保真之间存在可能冲突，摘要的“constant-memory”是对循环轴，不是对序列长度。
- 精读问题：缓存更新因果时序是什么？历史循环内容是否永久覆盖？长窗、细节检索、重复推理和相同质量下吞吐是否均保持？迁移训练与蒸馏总成本多少？

### T06-028 ★ Looped Latent Attention: Cross-Loop KV Compression for Looped Transformers
- 身份：—（作者元数据待补）；2026；arXiv:2607.15456，v2（2026-07-24）。核验A。[摘要](https://arxiv.org/abs/2607.15456)；[PDF](https://arxiv.org/pdf/2607.15456)。
- 机制：循环轴K/V低秩潜变量压缩，读时重建循环专属K/V；SVD初始化后蒸馏。
- 支持/反例潜力：关键相反结果：**低秩并不意味着能安全塌成一个状态**，作者称优于单最终循环复用等对照。摘要“cache reduction is exact”仅表示存储量核算，不能误读为输出无损精确。
- 精读问题：压缩后如何保存循环地址？读时重建成本与增大批量收益各多少？32倍近无损限定何种离线评价？生成分布自蒸馏为何改变长推理表现？

### T06-029 ★ Depth-adaptive Inference of Looped Language Models via Continuous Depth Batching
- 身份：Kristian Schwethelm、Daniel Rückert、Georgios Kaissis；2026；arXiv:2608.09444，v2（2026-09-25）。核验A。[摘要](https://arxiv.org/abs/2608.09444)；[PDF](https://arxiv.org/pdf/2608.09444)。
- 机制：循环之间重组批次、管理循环K/V、预测出口以异步准备下一批；解决异深度token不能普通批处理的问题。
- 支持/反例潜力：把共享层的潜在吞吐转成系统执行；摘要也指出较大的非共享前后置层/输出头会拖慢调度。99%是估计可用上界的比例，不是绝对99%加速。
- 精读问题：出口预测错误付出何代价？短长窗、吞吐与p95/p99延迟如何变化？上界是否含CPU调度、重批、缓存搬运？Huginn与Ouro差异来自架构还是实现？

### T06-030 ★ WaveFront Decoding: Parallelized Self-Speculative Decoding for Looped Language Models
- 身份：—（作者元数据待补）；2026；arXiv:2609.23033，v2（2026-09-26）。核验A。[摘要](https://arxiv.org/abs/2609.23033)；[PDF](https://arxiv.org/pdf/2609.23033)。
- 机制：不同位置/循环深度的状态混批，浅循环起草与深循环验证同时前进；可选跨循环K/V共享降低流量。
- 支持/反例潜力：作者报2.42/3.54倍以及共享K/V后4.81倍，不得把不同模型/变体速度拼接成单一保证；投机纠错与改造缓存的分布影响须分开。
- 精读问题：何种采样算法保持目标分布？共享K/V变体改变模型吗？拒绝恢复、长窗KV流量、接受率和波前宽度怎样相互制约？

### T06-031 Decoding Looped Transformers Better for (Almost) Free
- 身份：—（作者元数据待补）；2026；LoopCD，arXiv:2610.02185，v1。核验A。[摘要](https://arxiv.org/abs/2610.02185)；[PDF](https://arxiv.org/pdf/2610.02185)。
- 机制：用较早循环作为弱预测、最终循环作为强预测做对比解码，可在logit或隐藏状态空间操作。
- 支持/反例潜力：复用中间状态可提高同计算质量；“zero output overhead”仅隐藏态方案的输出头口径，不自动零总成本。摘要说前向FLOPs降22.5—48.2%，未据此断言真实延迟。下一步查任务选择、额外读写、同温度同采样比较及改变输出分布的代价。

### T06-032 ★ Improving Test-Time Scaling with Adaptive Looped Transformers
- 身份：—（作者元数据待补）；2026；TaH2，arXiv:2609.35748，v1。核验A。[摘要](https://arxiv.org/abs/2609.35748)；[PDF](https://arxiv.org/pdf/2609.35748)。
- 机制：在线生成“多迭代是否改善预测”的前瞻标签，联合训练骨干与迭代决策器，按受益token加算。
- 支持/反例潜力：作者明确报告：已有循环模型斜率可更陡，但**同算力仍可能弱于非循环基线**。收益斜率和同预算绝对能力必须分开。
- 精读问题：前瞻标签构造会否看到未来正确答案/teacher？标签计算成本计入了吗？“不受益token”的任务/长度规律、策略迁移及实际跳算可执行性如何？

### T06-033 ★ What Sets the Serving Speed of Looped Language Models? Measurements and Optimizations Graded by Exactness
- 身份：—（作者元数据待补）；2026；ExactLoop，arXiv:2611.05150，v1（2026-11-03）。核验A。[摘要](https://arxiv.org/abs/2611.05150)；[PDF](https://arxiv.org/pdf/2611.05150)。
- 机制：在开源循环模型引擎上分别量循环提交、微kernel、KV槽、前缀复用、噪声、图缓存和预填充/解码分离的成本，并按逐比特等价到需准确率复核分级。
- 支持/反例潜力：批1仅合并循环提交吞吐0.99倍；近似融合不更快且未过作者质量规则。说明“少调度调用”也不一定解除真实瓶颈；非常新预印本，全部数值仍待复核。
- 精读问题：5689小kernel/token在哪个模型配置？rounding fences怎样保证等价？基线引擎是否充分优化？同机质量门、请求量、错误处理关闭与开启的速度差如何影响结论？

### T06-034 ★ How Later Loops Redirect Two-Hop Retrieval in the Ouro Looped Language Models
- 身份：—（作者元数据待补）；2026；arXiv:2610.34639，v1（2026-10-25）。核验A。[摘要](https://arxiv.org/abs/2610.34639)；[PDF](https://arxiv.org/pdf/2610.34639)。
- 机制：同层/同头/同末位位置的跨循环query移植，测试后循环能否重新指向桥接实体；区分query改写与key/value改写。
- 支持/反例潜力：本轮最贴近“循环后回访同一来源”的因果入口之一；**自然问题的救援较弱且只在Ouro-2.6B复现，交叉交换未建立桥接重定向**。摘要明确不定位桥实体在哪计算、不证明单向量交接。
- 精读问题：合成场景的90%/97%救援是否受候选打分/位置混杂驱动？自然问答全文/生成检验如何？多源地址是否真的被选择，还是同位置特征的再参数化？

## D. 跨层读取、残差保留与动态性审计（13项）

### T06-035 DenseFormer: Enhancing Information Flow in Transformers via Depth Weighted Averaging
- 身份：Matteo Pagliardini、Amirkeivan Mohtashami、François Fleuret、Martin Jaggi；2024；arXiv:2402.02622，v2（2024-03-21）；NeurIPS2024正式版关联。核验A。[摘要](https://arxiv.org/abs/2402.02622)；[PDF](https://arxiv.org/pdf/2402.02622)。
- 机制：每块后对当前与过去表示做可学习深度加权平均；可复用远层激活，权重不是必然输入条件。
- 支持/反例潜力：证明早层再读取有价值的静态基线；作者报同困惑度下内存/时间更好，须对照更浅模型，而非声称同架构免费。下一步查保存层数、稀疏深度间隔、隐藏态读写和负权重作用。

### T06-036 LAuReL: Learned Augmented Residual Layer
- 身份：Gaurav Menghani、Ravi Kumar、Sanjiv Kumar；2024首发/2025修订；arXiv:2411.07501，v4（2025-06-24）。核验A。[摘要](https://arxiv.org/abs/2411.07501)；[PDF](https://arxiv.org/pdf/2411.07501)。
- 机制：残差连接的可学习增强，以很少参数改善视觉与LLM；不同变体须正文拆分。
- 支持/反例潜力：低参数开销不意味着低访存开销或条件执行；同等质量/占用比较比单数值提升重要。下一步查增强读哪些早层、系数是否动态、速度是否实测与参数增量是否含缓存。

### T06-037 ★ DeepCrossAttention: Supercharging Transformer Residual Connections
- 身份：—（作者元数据待补；摘要提取仅给提交人，未冒认为作者）；2025；arXiv:2502.06785，v2（2025-07-23）；ICML2025关联 https://icml.cc/virtual/2025/poster/44325 。核验A。[摘要](https://arxiv.org/abs/2502.06785)；[PDF](https://arxiv.org/pdf/2502.06785)。
- 机制：输入条件权重动态组合任意早层输出，深度方向交叉注意力。
- 支持/反例潜力：与AttnRes非常近，不可把“注意力读早层”当2026新空白。作者还给层秩总量/环境维度阈值条件下的理论优势，非无条件更强。
- 精读问题：与AttnRes具体在哪个张量上注意、query如何生成？所谓同质量训练快3倍含何种规模/预算？理论秩条件可测且现实成立吗？保留激活成本与块化怎样比较？

### T06-038 Hyper-Connections
- 身份：—（作者元数据待补；不从提交人补全作者）；2024首发/2025修订；arXiv:2409.19606，v3（2025-03-18）。核验A。[摘要](https://arxiv.org/abs/2409.19606)；[PDF](https://arxiv.org/pdf/2409.19606)。
- 机制：扩展残差连接，使不同深度特征连接强度可调；摘要称可动态重排层。
- 支持/反例潜力：动态连线与扩宽残差是保存/加工分离的邻近设计，但不证明删算或原始来源可寻址。下一步查“重排”是代数混合还是执行顺序、身份映射稳定性及扩展状态访存。

### T06-039 mHC: Manifold-Constrained Hyper-Connections
- 身份：Zhenda Xie、Yixuan Wei、Huanqi Cao等（原页作者表）；2025-12首发/2026修订；arXiv:2512.24880，v2（2026-01-05）。核验A。[摘要](https://arxiv.org/abs/2512.24880)；[PDF](https://arxiv.org/pdf/2512.24880)。
- 机制：约束HC连接空间到特定流形，恢复身份映射性质并优化系统执行。
- 支持/反例潜力：作者指出原HC破坏身份映射、训练不稳定、访存显著；是“更丰富跨层通路并非无代价”的直接反证线。下一步查投影/归一化代价、规模稳定性压力测试及和SimpleHC的同口径比较。

### T06-040 MUDDFormer: Breaking Residual Bottlenecks in Transformers via Multiway Dynamic Dense Connections
- 身份：—（作者元数据待补；公开引用仅给Xiao等，未从提交人补全）；2025；arXiv:2502.12170，v2（2025-05-28）。核验A。[摘要](https://arxiv.org/abs/2502.12170)；[PDF](https://arxiv.org/pdf/2502.12170)。
- 机制：按位置与流（query/key/value/residual）分别生成动态跨层连接权重，避免所有计算使用同一混合。
- 支持/反例潜力：Q/K/V/保留流解耦高度相关；0.4%额外计算并不自动等于0.4%延迟。下一步和T06-047配读，核实输入条件赋权确有功能作用但仍全层执行、激活保存与流拆分访存成本。

### T06-041 You Do Not Fully Utilize Transformer's Representation Capacity
- 身份：Gleb Gerasimov、Yaroslav Aksenov、Nikita Balagansky、Viacheslav Sinii、Daniil Gavrilov；2025首发/2026修订；LIMe，arXiv:2502.09245，v3（2026-08-31）；EMNLP2026关联 https://aclanthology.org/2026.emnlp-main.2641/ （搜索元数据）。核验A。[摘要](https://arxiv.org/abs/2502.09245)；[PDF](https://arxiv.org/pdf/2502.09245)。
- 机制：利用既有K/V缓冲，按头/层路由权重整合早层表示，减轻表征塌缩与值向量熵下降。
- 支持/反例潜力：明确把跨层复用放在注意力记忆中；隐藏状态宽度不增不等于持久缓存或读取流量不增。下一步查路由是否查询条件、熵/可分离性对任务收益是否因果，以及新版与旧版成本口径。

### T06-042 ★ Attention Residuals
- 身份：Kimi Team（Guangyu Chen、Yu Zhang、Jianlin Su等，原页完整作者列表）；2026；arXiv:2603.15031，v1（2026-03-16）。核验A。[原始摘要](https://arxiv.org/abs/2603.15031)；[PDF](https://arxiv.org/pdf/2603.15031)。
- 机制：以对早层输出的softmax注意力替换单位残差累加；Block AttnRes按深度块汇聚，降低内存/通信，结合缓存流水通信和两阶段计算。摘要含Kimi Linear 48B总量/3B激活、1.4T训练token的自报验证。
- 支持/反例潜力：**入口身份已核验**；支持内容条件跨深度选读与块级组织，但此处“块”是深度层组，不是文本片段粒度；并未在摘要声称跳过Transformer层。不能据此背书真按需计算或原始信息回访。
- 精读问题：注意权重是否按位置、头、层变化？块内/块间的可读对象与丢失信息是什么？相对DCA/MUDDFormer的实质差异？“minimal overhead”含哪些训练/推理、激活/通信项？早层输出保存多久、长窗读写如何增长？

### T06-043 ★ Transformers with Selective Access to Early Representations
- 身份：Skye Gunasekaran等（Q09原始搜索第一作者，完整作者待补）；2026；SATFormer，arXiv:2605.03953，v3（2026-10-26）。核验A。[摘要](https://arxiv.org/abs/2605.03953)；[PDF](https://arxiv.org/pdf/2605.03953)。
- 机制：保留第一层value通路、用上下文条件门控制访问；把早表征复用视为检索，而非所有token/头统一静态混合。
- 支持/反例潜力：本轮“保留细节→按需再读取”的最贴近入口之一，检索任务增益更强；不过固定第一层value仍不是可下钻多级存储，门值稀疏也非条件执行证据。
- 精读问题：门是否依赖当前query？原始位置地址和信息保真保存到何程度？对随机门/静态均值/跨样本重排是否有对照？所谓近基线吞吐/内存在哪种上下文和实现上成立？

### T06-044 ★ Depth-Attention: Cross-Layer Value Mixing for Language Models
- 身份：—（作者元数据待补）；2026；arXiv:2606.05014，v2（2026-06-13）。核验A。[摘要](https://arxiv.org/abs/2606.05014)；[PDF](https://arxiv.org/pdf/2606.05014)。
- 机制：当前query先在同一token位置跨早层key选择并混合value，再做序列注意力；混合值覆盖常规cache槽，不新增持久推理状态/参数。
- 支持/反例潜力：对“早层读取必额外留全部hidden states”的反例；但缓存不增不保证读取/重算不增，也不代表原始value仍可恢复。
- 精读问题：跨深度打分在prefill/decode如何执行？旧层key/value何时覆盖、能否再回访未混合来源？小于0.01%算术FLOPs与墙钟/带宽是否一致？与LIMe/SATFormer的地址和选择差异？

### T06-045 DAGFormer: Global Topology Prediction for Transformer Cross-Layer Connections
- 身份：—（作者元数据待补）；2026；arXiv:2610.19625，v1（2026-10-14）。核验A。[摘要](https://arxiv.org/abs/2610.19625)；[PDF](https://arxiv.org/pdf/2610.19625)。
- 机制：联合训练全模型拓扑预测器，按输入token整体规划早层到晚层直连强度，而非各层独立选择。
- 支持/反例潜力：可能降低局部路由短视；仍需区分规划连线权重与动态跳层。摘要75M—1B/OLMo2对照，未证明生产规模。下一步查预测拓扑是否因果、预测器本身成本、剪枝稳健性与多级文本来源无关部分。

### T06-046 On the Design of Hyper-Connections: Simplification, Stability, and Scalability
- 身份：Xiangdong Zhang、Xiaohan Qin、Sunan Zou等（原页作者表）；2026；SimpleHC，arXiv:2611.05984，v1（2026-11-04；以提交史而非搜索日期11-06为准）。核验A。[摘要](https://arxiv.org/abs/2611.05984)；[PDF](https://arxiv.org/pdf/2611.05984)。
- 机制：去残差混合、保留读写门，组内共享入口状态以批读/延迟写，标量修正保持先前子层贡献。
- 支持/反例潜力：作者发现扩宽状态重复访问即主要开销；较简单门控可匹配mHC，最大尺度额外端到端训练时间2.4%。是对“复杂混合必需”的新反例，不是独立复现。
- 下一步：查精确等价的范围、分组共享改变可用信息的程度、15B—30B MoE压力条件、推理时间是否另报。

### T06-047 ★ Dynamic Parameterization Is Not Dynamic Inference
- 身份：—（作者元数据待补）；2026；arXiv:2607.26192，v1（2026-07-28）。核验A。[摘要](https://arxiv.org/abs/2607.26192)；[PDF](https://arxiv.org/pdf/2607.26192)。
- 机制：缓存未干预轨迹上的完整控制系数，关闭控制器后跨输入重分配、token打乱、静态校准轮廓回放，分离系数变化、功能依赖和条件执行。
- 支持/反例潜力：FeatureGate静态层轮廓保留大多数增益，却仍全层执行且作者实测慢30.8%；MUDDPythia对内容赋权确敏感但也全层执行。明确不能由“动态权重”推出省算。
- 精读问题：冻结轨迹干预避免了哪些反馈混杂，仍遗漏哪些反事实？静态校准是否独立同域？基线实现公平吗？如何把同类审计用于SATFormer/AttnRes而不先推断其动态性真假？

## E. 最近邻组合：条件查表、分层索引、来源保留与重激活（8项）

### T06-048 LongCat-Flash Technical Report
- 身份：Meituan LongCat Team等（原页作者表）；2025；arXiv:2509.01322，v2（2025-09-19）。核验A。[摘要](https://arxiv.org/abs/2509.01322)；[PDF](https://arxiv.org/pdf/2509.01322)。
- 机制：零计算专家允许动态激活预算；Shortcut-connected MoE扩大计算/通信重叠窗口。总560B，每token激活18.6—31.3B（平均27B），均为作者自报。
- 支持/反例潜力：真正有不执行变换的候选路径，且明确做系统重叠；零专家并不意味着所有注意力/路由/通信均省掉。下一步查零专家实际选中率与上下文关系、all-to-all通信和负载平衡、TPS的硬件/并发/延迟口径。

### T06-049 ★ Introducing LongCat-2.0
- 身份：Meituan LongCat官方发布；2026-06-30；稳定官方URL，无本轮已核验arXiv编号。核验**O**。[原始官方介绍/全文入口](https://longcat.chat/blog/longcat-2.0/)。本项是技术发布，不冒充论文或独立评测。
- 机制（官方Architecture、LongCat Sparse Attention小节）：LSA稀疏注意力包括Streaming-aware Indexing（硬件对齐连续+随机读取）、Cross-Layer Indexing（训练蒸馏、推理跨相邻层复用索引）、Hierarchical Indexing（先块级粗召回再块内token选择）；HI仅在选定超长任务推理启用。另有N-gram Embedding，n=5、135B参数，不能与HI的块混为一谈。
- 支持/反例潜力：**入口真实性和机制介绍已外部核验**。这是本轮“粗→细+原位置选择+跨层复用+系统带宽”的最强最近邻之一；但网页无足够数值消融分离三种索引、没有由独立复现确认。官方把稀疏专家继续加参收益变小作为改用N-gram容量的理由，属于发布方结论，不直接推广。
- 精读/追查问题：取得对应技术报告、实现和HI召回率/失误回退实验；块到token来源映射如何保留？跨层共享索引是否漏掉新query需要的来源，是否可重激活？HI训练免费是否把索引构建/存储成本转移了？与逐层检索在同硬件的TTFT/TPOT/尾延迟、1M KV内存、通信/预取/索引器总成本如何对齐？
- 口径边界：总1.6T/约48B激活是发布方配置；不从“adaptive reasoning experts”措辞推断循环层或真动态停止；本轮未验证新模型基准成绩、开源权重完整性或实用可部署性。

### T06-050 ★ Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models
- 身份：Xin Cheng、Rui Tian、Wangding Zeng、Damai Dai等（原页作者表）；2026；Engram，arXiv:2601.07372，v2（2026-07-12）。核验A。[摘要](https://arxiv.org/abs/2601.07372)；[PDF](https://arxiv.org/pdf/2601.07372)。
- 机制：经典N-gram现代化的条件记忆查表，以确定地址和预取将静态模式检索与神经加工分开；讨论MoE计算与Engram静态容量间U形资源分配关系。
- 支持/反例潜力：支持“查表≠重复变换”的正交稀疏轴；但N-gram表是训练所得静态记忆，不是当前输入可追溯原始片段，O(1)寻址不代表O(1)端到端I/O。
- 精读问题：上下文门与表内容各贡献什么？“释放早层”是干预证据还是表征指标？主机预取何时失效？稀疏分配最优点是否依赖规模、词表/语言和CPU带宽？等参数/等FLOPs是否含所有内存资源？

### T06-051 Pooling Engram Conditional Memory in Large Language Models using CXL
- 身份：Ruiyang Ma、Teng Ma、Zhiyuan Su等（原页作者表）；2026；arXiv:2603.10087，v1。核验A。[摘要](https://arxiv.org/abs/2603.10087)；[PDF](https://arxiv.org/pdf/2603.10087)。
- 机制：利用CXL（计算快速链接，一类主机与设备间内存互连）池化Engram表，集成SGLang，针对稀疏细粒度预取访问比较RDMA路径。
- 支持/反例潜力：“接近DRAM端到端性能”是特定系统作者值；表容量成本不能只看GPU驻留字节。下一步查CXL拓扑、随机访问带宽、预取命中/并发、尾延迟、失效处理、是否存在主机缓存命中优势。

### T06-052 ★ Memory Grafting: Scaling Language Model Pre-training via Offline Conditional Memory
- 身份：Runxi Cheng等（Q38原始题名/作者首名线索；完整作者待补）；2026；arXiv:2605.20948，v1。核验A。[摘要](https://arxiv.org/abs/2605.20948)；[PDF](https://arxiv.org/pdf/2605.20948)。
- 机制：离线运行供体模型，把常见n-gram末位隐藏态存为记忆，接收模型做最长精确后缀匹配、投影/门控读取，无匹配则Engram回退。
- 支持/反例潜力：明确把昂贵计算移到离线，并含不同长度匹配+回退；是多粒度地址/保存加工分离的近邻，但存的不是当前长窗原始来源，不可等同可追溯源回访。
- 精读问题：不同长度n-gram是否保存共同来源关系？离线供体总成本/表容量/构建数据泄漏是否计入？O(1)期望寻址依赖何假设？冻结记忆何时过时，回退触发可诊断吗？

### T06-053 ★ CoLT5: Faster Long-Range Transformers with Conditional Computation
- 身份：Joshua Ainslie、Tao Lei、Michiel de Jong、Santiago Ontañón等（原页作者表）；2023；arXiv:2303.09752，v3（2023-10-24）。核验A。[摘要](https://arxiv.org/abs/2303.09752)；[PDF](https://arxiv.org/pdf/2303.09752)。
- 机制：长输入里并非每个token需要昂贵注意力和FFN，将更多资源分给重要位置；摘要报告训练/推理更快、可用64k输入。
- 支持/反例潜力：和MoD相比更直接关乎全量轻路径+少量重路径，可能避免只保留活跃集而失去来源；具体轻重分支结构仍须正文核查，不能由摘要补齐。
- 精读问题：所有位置是否持续保留轻量状态？被重读的地址和原始位置如何对应？路由随query变化吗？局部/全局读取粒度、长窗基线与端到端实测成本怎样拆分？

### T06-054 ★ Revisiting Token Pruning for Object Detection and Instance Segmentation
- 身份：Yifei Liu等（Q32原始搜索结果及CVF作品身份，完整作者待补）；2023首发/WACV2024；arXiv:2306.07050，v3（2023-12-12）。核验A。[摘要](https://arxiv.org/abs/2306.07050)；[PDF](https://arxiv.org/pdf/2306.07050)；[正式版入口](https://openaccess.thecvf.com/content/WACV2024/papers/Liu_Revisiting_Token_Pruning_for_Object_Detection_and_Instance_Segmentation_WACV_2024_paper.pdf)。
- 机制：被剪token不丢弃而留在特征图，可在后层重新激活；动态剪率、轻量两层MLP决策。明确把保存、加工和重用分开。
- 支持/反例潜力：最直接的来源保留/重激活先例，作者报整网最高快34%、骨干46%；反对“低重要性即可永久删除”。但视觉空间坐标+双向任务与因果语言模型差异很大。
- 精读问题：重激活如何判定、拿到的是旧特征还是重算原像素？保留未算token占用多少带宽？因果流式任务缺少全图时能否运行？必须避免把视觉成功直接当字节接口结论。

### T06-055 Mixture-of-Modules: Reinventing Transformers as Dynamic Assemblies of Modules
- 身份：Zhuocheng Gong、Ang Lv、Jian Guan、Wei Wu、Huishuai Zhang、Minlie Huang、Dongyan Zhao、Rui Yan；2024；ACL Anthology:2024.emnlp-main.1164，DOI:10.18653/v1/2024.emnlp-main.1164。核验A。[正式摘要/元数据](https://aclanthology.org/2024.emnlp-main.1164/)；[正式版PDF](https://aclanthology.org/2024.emnlp-main.1164.pdf)。
- 机制：注意力和FFN模块池各有路由器，反复选择所需模块，打破固定深度顺序；可调模块数/深度，参数减冗余。
- 支持/反例潜力：跨模块复用与可学习执行图的直接近邻；动态组装不自动有良好GPU局部性。作者报GPT2-774M相当质量下省16%TFLOPs、42%前向内存，须查是否有实际吞吐。下一步审查路由开销、模块重入/共享、异质批次和因果性。

## 跨作品筛选结论（摘要层推断，不作架构裁定）

|研究问题|优先比较的作品|本轮能说什么|仍不能说什么|
|---|---|---|---|
|加工次数与信息粒度能否拆开？|001、002、008、025、032|多步可以精化同一对象；时钟/停止只定义更新频率|不能由更多循环推出更多语义粒度、可寻址源或更高知识容量|
|保存与变换能否分开？|005、006、007、043、054|冻结/携带旧状态、保留早层/被剪token都有先例|门控为小不等于支路不执行；旧状态不等于原始信息无损|
|最接近“多粒度+来源回访”的组合？|049、054、043、052、053、034|分别提供块→token选址、保留重激活、早value访问、变长查表回退、轻重路径和循环改写query的邻近机制|尚无本轮已全文核实的单一作品同时实现完整多级来源映射、按查询下钻、可回退和全成本验证；**这不是文献空白的证明**|
|跨层选择是否省算？|037、040、042、044、047|跨层内容选择可以有功能作用|可仍全层执行；需要执行轨迹、控制器回放、静态/重排对照|
|真省算为何不快？|011、014、017、022、029、030、033、046|异质批次、I/O、microkernel、KV增长、重批和反复访存均有直接入口|FLOPs、参数、KV字节、吞吐、请求延迟互不可代替|
|循环缓存是否可统一覆盖？|025、027、028|共享/覆盖省存储；低秩重建保留循环专属地址|不能把压缩后的低秩轨迹无条件当一份最终状态|
|动态路由是否必要？|004、020、021、035、047|固定时钟/静态剪枝/静态混合必须做强对照|不因路由熵高、系数多变就断言按需控制有价值|

## 年份与去重补充

近12个月首发的19项：T06-027、028、029、030、031、032、033、034、039、042、043、044、045、046、047、049、050、051、052。其余36项不是“近一年新论文”，即使2026有修订/正式版也按原作品计。

已明确挂接正式版但不重复计数的入口包括UT、HM-RNN、CALM、LayerSkip、Relaxed Recursive、ITT、FlexiDepth、GateSkip、DenseFormer、LIMe、重激活视觉论文和MoM；其中部分会议信息只经搜索结果识别，版本差异待统一书目/全文阅读核查。完整作者、正式出版DOI和版本差异是目录后处理任务，不影响本轮已取回原始摘要的55项身份确认，但不得把待补元数据写成已完成。
