# 字节语言接口分类：问题、策略与技术族

英文定稿：[CLASSIFICATION_EN.md](../04_synthesis/CLASSIFICATION_EN.md)。

<a id="1-classification-contract-and-central-interpretation"></a>
## 1. 分类约定与核心解释

296条规范记录描述的领域远不止学习式字节切分，还包括词汇表示、全分辨率序列模型、循环状态、条件计算、编码器压缩、因果生成、适配、概率转换、多语言评价、诊断对照和资源记账。有用的共同问题是：**一项技术改变了语言接口的哪个部分，这一改变处理什么困难？** 小输入字母表本身既不能确定内部计算单位，也不能确定输出分布。

本分类包含三个相连层次：

1. **问题层级：** 六个编辑性分支，包含既有12个可重叠的C01–C12问题族。完整规范成员关系覆盖全部296条BIP记录。
2. **方案策略路线：** 13条紧凑的归属路线，每条记录只分配一次，以便导航。归属路线标识主要技术对象或评价干预，不会把记录变成独立科学问题。
3. **使用/借鉴的技术族：** 在路线内解释机制，并为多用途方法设置交叉链接。“借鉴”指被引工作使用的、可以辨认的AI或统计技术；只有来源确立了技术传承关系时，才断言谱系上的借鉴。确定性标准和资源审计明确列为非神经方法类别。这里的“AI技术工具”不是本助手的软件工具。

这些是**人工、受证据约束的主题标签**，不是算法聚类；没有嵌入、距离度量、学习式划分或统计簇发现。互斥归属路线只是阅读便利；问题标签和实质技术关系仍可多标签。例如，电路草稿同时涉及结构化预测、推测解码、概率记账与系统成本；学习式边界则可能同时涉及聚合、梯度估计、因果时序和语言分配。

文档范围是141个来源实体、140个贡献实体、296条记录，以及92个不同的限定范围FULL来源。来源实体包括标准、一份官方介绍和一项经筛查的提案，并不是141个原生字节语言模型。记录由283条原始来源支持的摘录、3条审计摘录和10条领域补充子发现组成。这些区别以[COUNTS](../02_inventory/COUNTS.md)、[AUTHOR_HANDOFF](../02_inventory/AUTHOR_HANDOFF.md)和[CLAIM_RULES](../05_review/CLAIM_RULES.md)为准。详细的“问题→一句话方案→技术”清单见[DETAILED_INVENTORY](../02_inventory/DETAILED_INVENTORY.md)，中文工作见[DETAILED_INVENTORY_ZH](DETAILED_INVENTORY_ZH.md)；本文组织这些记录，不重复其全部逐条内容。

<a id="2-a-hierarchy-of-parent-questions"></a>
## 2. 上位问题的层级

下表重新组织规范C族，不取代、不改名。数字为**重叠记录成员数/该族内不同工作数**，不能相加后当成独立问题、文献或效果数。

| 编辑性分支与上位问题 | 规范问题族 | 成员数/工作数 | 与综述其他部分的关系 |
|---|---|---:|---|
| A. 接口表示什么？ | [C01——单位、覆盖与编码](../02_inventory/TAXONOMY.md#C01) | 35 / 27 | 比较效用之前，定义字节、码点、字素、字符、子词和混合接口约定。 |
| B. 细粒度文本怎样成为有用表示？ | [C02——组合与聚合](../02_inventory/TAXONOMY.md#C02) | 37 / 27 | 不只识别边界在哪里，还说明存储了什么。 |
| C. 计算分配到哪里？ | [C03——切分与结构先验](../02_inventory/TAXONOMY.md#C03) | 43 / 32 | 谁选择边界，什么提供边界目标？ |
| C. 计算分配到哪里？ | [C04——计算与历史状态](../02_inventory/TAXONOMY.md#C04) | 43 / 28 | 包含全分辨率、循环、层级和字节内替代方案。 |
| D. 可用信息和输出分布是什么？ | [C05——因果对齐与新鲜度](../02_inventory/TAXONOMY.md#C05) | 14 / 10 | 追踪摘要或特征何时可以作为预测条件。 |
| D. 可用信息和输出分布是什么？ | [C06——未来目标与解码](../02_inventory/TAXONOMY.md#C06) | 35 / 25 | 分开训练目标、依赖联合分布和接受策略。 |
| E. 系统如何参数化与学习？ | [C07——共享与读出几何](../02_inventory/TAXONOMY.md#C07) | 33 / 24 | 指明矩阵轴和公式，不从架构血缘推断绑权。 |
| E. 系统如何参数化与学习？ | [C08——优化与梯度路由](../02_inventory/TAXONOMY.md#C08) | 53 / 38 | 包含替代梯度、辅助目标、课程和相邻对照。 |
| E. 系统如何参数化与学习？ | [C09——混合适配](../02_inventory/TAXONOMY.md#C09) | 37 / 18 | 追踪继承检查点、教师、冻结主体和输出转换阶段。 |
| F. 什么构成收益证据？ | [C10——语言/任务效用](../02_inventory/TAXONOMY.md#C10) | 60 / 44 | 区分覆盖、鲁棒性、能力、公平性和实验归因。 |
| F. 什么构成收益证据？ | [C11——概率与解释](../02_inventory/TAXONOMY.md#C11) | 33 / 20 | 指明被评分事件、支持集、规范化与终止约定。 |
| F. 什么构成收益证据？ | [C12——预算与实现](../02_inventory/TAXONOMY.md#C12) | 83 / 53 | 分开匹配文本、参数、FLOPs、内存、时间与质量。 |

这些规范成员关系的并集恰好是BIP-0001–BIP-0296，共506个问题族成员关系。来源账目也恰有506条映射边，但两者是不同关系，不能混淆：问题族成员关系表示记录涉及某个编辑性问题，来源边表示某条来源摘录映射到某条记录。

这一层级不是领域的因果模型。例如，长序列既可促使分组，也可促使稀疏连接、状态空间循环或执行方式调整。鲁棒的输入字母表可以与脆弱的任务行为共存；规范化的块分布也可以与昂贵采样器共存。跨族关系与上位分支同样重要。

<a id="3-complete-compact-home-route-index"></a>
## 3. 完整的紧凑归属路线索引

成员列中每个数字均带前缀**BIP-**；四位数字范围包含两端，链接指向范围内首条记录。13条互斥归属路线**恰好一次覆盖全部296条记录**。其计数是文档导航数，不是语义上独立问题的普查。现有C标签提供重叠次级归属，下文再补充明确的技术与跨族联系。测量记录被放到某机制附近，是为了审计该机制，不表示作者实现了新模型组件。

| 归属路线 | 主要方案策略与技术族 | 数量 | BIP成员 |
|---|---|---:|---|
| 编码 | 改变符号编码、字母表覆盖或统计词表构造；哈希、字节回退、BPE/unigram构造和规范性编码工具 | 20 | [0001–0003](../02_inventory/DETAILED_INVENTORY.md#BIP-0001), [0055](../02_inventory/DETAILED_INVENTORY.md#BIP-0055), [0061](../02_inventory/DETAILED_INVENTORY.md#BIP-0061), [0102](../02_inventory/DETAILED_INVENTORY.md#BIP-0102), [0112](../02_inventory/DETAILED_INVENTORY.md#BIP-0112), [0134](../02_inventory/DETAILED_INVENTORY.md#BIP-0134), [0217–0219](../02_inventory/DETAILED_INVENTORY.md#BIP-0217), [0221](../02_inventory/DETAILED_INVENTORY.md#BIP-0221), [0242–0243](../02_inventory/DETAILED_INVENTORY.md#BIP-0242), [0266](../02_inventory/DETAILED_INVENTORY.md#BIP-0266), [0268–0269](../02_inventory/DETAILED_INVENTORY.md#BIP-0268), [0271](../02_inventory/DETAILED_INVENTORY.md#BIP-0271), [0295–0296](../02_inventory/DETAILED_INVENTORY.md#BIP-0295) |
| 局部组合 | 构建有用局部词汇特征；CNN、循环组合器、highway门、n-gram与稀疏词汇特征 | 22 | [0070–0071](../02_inventory/DETAILED_INVENTORY.md#BIP-0070), [0084–0088](../02_inventory/DETAILED_INVENTORY.md#BIP-0084), [0100–0101](../02_inventory/DETAILED_INVENTORY.md#BIP-0100), [0126–0128](../02_inventory/DETAILED_INVENTORY.md#BIP-0126), [0133](../02_inventory/DETAILED_INVENTORY.md#BIP-0133), [0135–0138](../02_inventory/DETAILED_INVENTORY.md#BIP-0135), [0140](../02_inventory/DETAILED_INVENTORY.md#BIP-0140), [0152–0153](../02_inventory/DETAILED_INVENTORY.md#BIP-0152), [0216](../02_inventory/DETAILED_INVENTORY.md#BIP-0216), [0261](../02_inventory/DETAILED_INVENTORY.md#BIP-0261) |
| 分组 | 缩短或选择表示位置；软混合、累计分配、池化、删除、合并与速率约束 | 21 | [0004–0012](../02_inventory/DETAILED_INVENTORY.md#BIP-0004), [0066–0069](../02_inventory/DETAILED_INVENTORY.md#BIP-0066), [0151](../02_inventory/DETAILED_INVENTORY.md#BIP-0151), [0154–0155](../02_inventory/DETAILED_INVENTORY.md#BIP-0154), [0160–0161](../02_inventory/DETAILED_INVENTORY.md#BIP-0160), [0168](../02_inventory/DETAILED_INVENTORY.md#BIP-0168), [0222–0223](../02_inventory/DETAILED_INVENTORY.md#BIP-0222) |
| 层级分配 | 分配昂贵更新并保留合法信息流；固定/规则/学习式路由、熵/效用策略、替代或策略梯度、移位与临时刷新 | 38 | [0013–0028](../02_inventory/DETAILED_INVENTORY.md#BIP-0013), [0038](../02_inventory/DETAILED_INVENTORY.md#BIP-0038), [0054](../02_inventory/DETAILED_INVENTORY.md#BIP-0054), [0103–0107](../02_inventory/DETAILED_INVENTORY.md#BIP-0103), [0117](../02_inventory/DETAILED_INVENTORY.md#BIP-0117), [0145–0146](../02_inventory/DETAILED_INVENTORY.md#BIP-0145), [0156–0157](../02_inventory/DETAILED_INVENTORY.md#BIP-0156), [0162–0167](../02_inventory/DETAILED_INVENTORY.md#BIP-0162), [0169–0170](../02_inventory/DETAILED_INVENTORY.md#BIP-0169), [0180](../02_inventory/DETAILED_INVENTORY.md#BIP-0180), [0270](../02_inventory/DETAILED_INVENTORY.md#BIP-0270) |
| 序列状态与执行 | 保留、变换或复用序列状态；循环/选择性模型、稠密/稀疏/哈希注意力、潜在数组、循环与训练内存执行 | 31 | [0035–0036](../02_inventory/DETAILED_INVENTORY.md#BIP-0035), [0044](../02_inventory/DETAILED_INVENTORY.md#BIP-0044), [0081–0083](../02_inventory/DETAILED_INVENTORY.md#BIP-0081), [0091–0099](../02_inventory/DETAILED_INVENTORY.md#BIP-0091), [0121–0123](../02_inventory/DETAILED_INVENTORY.md#BIP-0121), [0132](../02_inventory/DETAILED_INVENTORY.md#BIP-0132), [0141–0142](../02_inventory/DETAILED_INVENTORY.md#BIP-0141), [0236–0238](../02_inventory/DETAILED_INVENTORY.md#BIP-0236), [0258](../02_inventory/DETAILED_INVENTORY.md#BIP-0258), [0287–0292](../02_inventory/DETAILED_INVENTORY.md#BIP-0287) |
| 输出与解码 | 每次昂贵调用预测或接受更多未来单位；局部自回归、辅助头、电路、扩散、推测及其成本对照 | 22 | [0029–0034](../02_inventory/DETAILED_INVENTORY.md#BIP-0029), [0041](../02_inventory/DETAILED_INVENTORY.md#BIP-0041), [0045](../02_inventory/DETAILED_INVENTORY.md#BIP-0045), [0052](../02_inventory/DETAILED_INVENTORY.md#BIP-0052), [0089](../02_inventory/DETAILED_INVENTORY.md#BIP-0089), [0108](../02_inventory/DETAILED_INVENTORY.md#BIP-0108), [0171–0179](../02_inventory/DETAILED_INVENTORY.md#BIP-0171), [0181](../02_inventory/DETAILED_INVENTORY.md#BIP-0181), [0183](../02_inventory/DETAILED_INVENTORY.md#BIP-0183) |
| 概率接口 | 定义、转换或诊断被评分事件；边缘化、前缀覆盖、拒绝修正、带标记目标及概率/统计记账 | 22 | [0043](../02_inventory/DETAILED_INVENTORY.md#BIP-0043), [0046](../02_inventory/DETAILED_INVENTORY.md#BIP-0046), [0063–0065](../02_inventory/DETAILED_INVENTORY.md#BIP-0063), [0078](../02_inventory/DETAILED_INVENTORY.md#BIP-0078), [0109–0111](../02_inventory/DETAILED_INVENTORY.md#BIP-0109), [0113](../02_inventory/DETAILED_INVENTORY.md#BIP-0113), [0119](../02_inventory/DETAILED_INVENTORY.md#BIP-0119), [0143](../02_inventory/DETAILED_INVENTORY.md#BIP-0143), [0182](../02_inventory/DETAILED_INVENTORY.md#BIP-0182), [0265](../02_inventory/DETAILED_INVENTORY.md#BIP-0265), [0272–0278](../02_inventory/DETAILED_INVENTORY.md#BIP-0272), [0286](../02_inventory/DETAILED_INVENTORY.md#BIP-0286) |
| 共享与几何 | 复用或约束参数空间；绑权、投影、归一化读出、秩/容量分析与共享规定 | 26 | [0037](../02_inventory/DETAILED_INVENTORY.md#BIP-0037), [0039](../02_inventory/DETAILED_INVENTORY.md#BIP-0039), [0058](../02_inventory/DETAILED_INVENTORY.md#BIP-0058), [0115](../02_inventory/DETAILED_INVENTORY.md#BIP-0115), [0184–0199](../02_inventory/DETAILED_INVENTORY.md#BIP-0184), [0207](../02_inventory/DETAILED_INVENTORY.md#BIP-0207), [0215](../02_inventory/DETAILED_INVENTORY.md#BIP-0215), [0254](../02_inventory/DETAILED_INVENTORY.md#BIP-0254), [0284–0285](../02_inventory/DETAILED_INVENTORY.md#BIP-0284), [0294](../02_inventory/DETAILED_INVENTORY.md#BIP-0294) |
| 目标与梯度控制 | 改变学习内容或起作用的梯度；课程、辅助目标、VQ/VAE损失、梯度投影/门控与扰动 | 14 | [0051](../02_inventory/DETAILED_INVENTORY.md#BIP-0051), [0116](../02_inventory/DETAILED_INVENTORY.md#BIP-0116), [0118](../02_inventory/DETAILED_INVENTORY.md#BIP-0118), [0120](../02_inventory/DETAILED_INVENTORY.md#BIP-0120), [0158–0159](../02_inventory/DETAILED_INVENTORY.md#BIP-0158), [0200–0205](../02_inventory/DETAILED_INVENTORY.md#BIP-0200), [0230](../02_inventory/DETAILED_INVENTORY.md#BIP-0230), [0246](../02_inventory/DETAILED_INVENTORY.md#BIP-0246) |
| 预训练适配 | 跨接口保留有用主体行为；嵌入模仿、上下文/logit蒸馏、超网络、分阶段冻结与任务向量迁移 | 29 | [0047–0049](../02_inventory/DETAILED_INVENTORY.md#BIP-0047), [0206](../02_inventory/DETAILED_INVENTORY.md#BIP-0206), [0208–0214](../02_inventory/DETAILED_INVENTORY.md#BIP-0208), [0244–0245](../02_inventory/DETAILED_INVENTORY.md#BIP-0244), [0247–0253](../02_inventory/DETAILED_INVENTORY.md#BIP-0247), [0255–0257](../02_inventory/DETAILED_INVENTORY.md#BIP-0255), [0259–0260](../02_inventory/DETAILED_INVENTORY.md#BIP-0259), [0262–0264](../02_inventory/DETAILED_INVENTORY.md#BIP-0262), [0293](../02_inventory/DETAILED_INVENTORY.md#BIP-0293) |
| 任务效用与诊断 | 测量或改善可用语言行为；噪声训练、多语言迁移、探针、任务干预与受控评价 | 30 | [0042](../02_inventory/DETAILED_INVENTORY.md#BIP-0042), [0056–0057](../02_inventory/DETAILED_INVENTORY.md#BIP-0056), [0060](../02_inventory/DETAILED_INVENTORY.md#BIP-0060), [0062](../02_inventory/DETAILED_INVENTORY.md#BIP-0062), [0072](../02_inventory/DETAILED_INVENTORY.md#BIP-0072), [0079–0080](../02_inventory/DETAILED_INVENTORY.md#BIP-0079), [0090](../02_inventory/DETAILED_INVENTORY.md#BIP-0090), [0124–0125](../02_inventory/DETAILED_INVENTORY.md#BIP-0124), [0129–0131](../02_inventory/DETAILED_INVENTORY.md#BIP-0129), [0139](../02_inventory/DETAILED_INVENTORY.md#BIP-0139), [0220](../02_inventory/DETAILED_INVENTORY.md#BIP-0220), [0224–0229](../02_inventory/DETAILED_INVENTORY.md#BIP-0224), [0231–0235](../02_inventory/DETAILED_INVENTORY.md#BIP-0231), [0280–0282](../02_inventory/DETAILED_INVENTORY.md#BIP-0280) |
| 预算与选择证据 | 确立比较所控制的因素；成本分解、缩放拟合、分词器代理、保留文本记账与诊断审计 | 16 | [0040](../02_inventory/DETAILED_INVENTORY.md#BIP-0040), [0050](../02_inventory/DETAILED_INVENTORY.md#BIP-0050), [0053](../02_inventory/DETAILED_INVENTORY.md#BIP-0053), [0059](../02_inventory/DETAILED_INVENTORY.md#BIP-0059), [0073–0077](../02_inventory/DETAILED_INVENTORY.md#BIP-0073), [0114](../02_inventory/DETAILED_INVENTORY.md#BIP-0114), [0239–0241](../02_inventory/DETAILED_INVENTORY.md#BIP-0239), [0267](../02_inventory/DETAILED_INVENTORY.md#BIP-0267), [0279](../02_inventory/DETAILED_INVENTORY.md#BIP-0279), [0283](../02_inventory/DETAILED_INVENTORY.md#BIP-0283) |
| 分段结构 | 通过序列概率或编码目标推断词汇结构；描述长度切分与潜在半马尔可夫动态规划 | 5 | [0144](../02_inventory/DETAILED_INVENTORY.md#BIP-0144), [0147–0150](../02_inventory/DETAILED_INVENTORY.md#BIP-0147) |

路线为13条，是因为导航分开了实践设计任务，不是发现了13种天然科学类别。例如，BIP-0110归在概率接口，尽管其拒绝修正也属于解码；BIP-0284归在共享，尽管描述的是MEGABYTE；BIP-0117归在因果分配，尽管实验也涉及学习课程。来源为A/P深度的记录在这些路线中仍受同一上限约束，不会因与FULL来源相邻而升级。

<a id="4-strategy-and-technique-interpretation"></a>
## 4. 策略与技术解释

<a id="41-encoding-remove-a-coverage-bottleneck-not-all-lexical-structure"></a>
### 4.1 编码：去除覆盖瓶颈，而不是消除全部词汇结构

字母表方案改变哪些字符串能进入系统、如何编码，或占用多少模型符号。字节回退、码点哈希、byte-BPE、形态派生编码与依书写系统而变的转码，解决的是这一问题的不同版本。共同点是表示工程，不是共同的生成架构。

[GPT-2窄范围摘录，BIW-0141](../03_reading/FIELD_ADDENDUM/gpt2_official_report_2019.md)，官方报告p.4 §§2.2–2.3，规定先用256字节基底，再按频率合并，并施加类别/空格约束；语言模型预测50,257个合并符号。[CANINE，BIW-0004](../03_reading/R01/BIW-0004.md) §3.1则把Unicode码点哈希到多个学习式表中，避免训练数据派生的输入词表，但接受碰撞；其下游任务头不构成开放字节生成器。BPE和哈希嵌入都是来源实际使用的技术；“都有覆盖”不意味着相同的保真或概率约定。

该路线还包含有意保留的非AI工具：UTF-8合法性、规范化等价与字素边界。合法序列可能含错误标量；规范等价字符串可以有不同原始字节；一个字素可跨多个码点。[BIP-0112/0217/0218](../02_inventory/DETAILED_INVENTORY.md#BIP-0112)规定这些区别，不是新增三项实证失败。

MYTE，[BIW-0104/BIP-0221](../02_inventory/DETAILED_INVENTORY.md#BIP-0221)，使用Morfessor资源与形态派生编码字节，而非原始UTF-8。附录Table 8报告MyT5低资源/总体机器翻译均值21.1/21.8，ByT5为21.9/23.1；正文Table 4的低资源摘要却以20.4对20.1有利于MyT5。总体/聚合之间的关系未解决。因此，更短或更均衡的编码是资源分配论断，其效用仍须检验，不自动带来公平或质量收益。

<a id="42-local-composition-recover-useful-lexical-features-without-confusing-the-sequence-clock"></a>
### 4.2 局部组合：恢复有用词汇特征，同时明确序列时钟

CNN检测短模式，最大池化选择强特征，highway门调节变换，循环组合器保留有序依赖，n-gram哈希增加词汇容量。这些方法应对的是独立学习每种拼写变体的统计低效；主干时钟仍可能按词、子词或字节推进。

[Character-Aware LM，BIW-0055](../03_reading/R02/BIW-0055.md)，Model/Fig.1，以字符CNN和highway层组合外部分词所得词，再用LSTM预测词，不是字节自回归。Table 7具体显示门控作用：PTB大模型无highway困惑度84.6，两层highway为78.9，普通单层MLP为92.6。作者提出优化困难作为解释，实验本身没有证明这一解释。局部组合也比词查表训练慢：报告的PTB大配置约1,500对3,000词词元/s。

[Local Byte Fusion，BIP-0070](../02_inventory/DETAILED_INVENTORY.md#BIP-0070)加入多尺度局部特征，但保留字节序列长度。[T-FREE，BIW-0127](../03_reading/R10/BIW-0127.md) §§3.1–3.2/Appendix A把规则切分的类词单位表示为稀疏哈希三元组集合，通过候选评分解码。即使不考虑哈希碰撞，其二值集合表示也未必是单射：在所述规则下，分析者例子`aaaa`/`aaaaa`具有相同的互异、带填充三元组集合。这是表示限制，不是已测软件碰撞。新词输入哈希不意味着有限词典可以无约束输出新词。

<a id="43-grouping-learn-or-impose-shorter-representations-with-explicit-content-and-rate-pressure"></a>
### 4.3 分组：学习或施加短表示，明确内容与速率压力

池化、删除、合并和软分配都能减少昂贵位置，却保留不同信息。边界标识地址或分组决策，不会告诉我们内容被拼接、平均、注意力聚合、从末状态选取，还是丢弃。

[Charformer，BIW-0005](../03_reading/R01/BIW-0005.md) §2.1用候选宽度软混合，再固定步幅缩减。[MANTa，BIW-0006](../03_reading/R01/BIW-0006.md) §3.1预测伯努利边界，近似累计成员关系，再用逐通道卷积/最大池化组合块。前者软备选不是精确潜在划分；后者高斯不是对全部切分的精确边缘化。MANTa的硬保留长度上限提供关键压缩压力：§6.1报告，没有它就退化为每字节一块。

[DTP，BIW-0007](../../flued_multigranularity_survey_20261108/03_reading/B05/W0007.md) §§3–5区分字符语料上的unigram标签模仿、本模型熵峰、Gumbel任务梯度和空白规则。英语中空白可匹敌学习式方法，芬兰语则不同，实际缩短率也不同。[MrT5，BIP-0066–0069](../02_inventory/DETAILED_INVENTORY.md#BIP-0066)先学软删除，推理时再硬移除；softmax1和控制器处理不同门控学习问题。缩短编码器不会缩短自回归目标。

Token Merging的特征匹配与按大小加权聚合，[BIP-0160/0161](../02_inventory/DETAILED_INVENTORY.md#BIP-0160)，是相邻视觉证据，可启发聚合和重数记账，不是已证实的因果字节切分方法。这条路线的剩余限制不是一种通用“压缩损失”，而取决于内容算子、可见信息、速率、任务与恢复路径。

<a id="44-hierarchical-allocation-choose-expensive-updates-and-make-their-timing-legal"></a>
### 4.4 层级分配：选择昂贵更新，并使其时序合法

固定分块可预测地摊销主干工作；已观察字节规则免去边界训练；独立熵教师按预测不确定性分配计算；上下文路由器使用任务训练状态；得分函数法优化采样决策；效用标签估计大模型收益。它们的决策信息来源不同。

[MEGABYTE，BIW-0008](../03_reading/R03/BIW-0008.md) §2.2拼接固定字节块，分别设置全局块移位与局部字节移位。[BLT，BIW-0010](../../flued_multigranularity_survey_20261108/03_reading/B05/W0010.md)，会议版§§2–4/Appendix H，用独立训练的因果熵模型、字节n-gram和交叉注意力聚合。[H-Net，BIW-0011](../../flued_multigranularity_survey_20261108/03_reading/B05/W0011.md) §2/Appendix E.1选择上下文边界状态，以平滑/直通梯度学习；选择不是DTP的显式均值池化。熵峰与余弦路由器都不应被描述为语义词神谕。

速率压力不同于决策梯度。H-Net比率损失不是逐样本硬配额。REINFORCE，[BIW-0078/BIP-0164/0165](../03_reading/R09/BIW-0078.md)，提供得分函数表述，但实用奖励折扣在降方差时引入偏差。直通估计器优化替代目标；引用强化学习不意味着每个实用梯度都无偏。

因果性涉及所有操作数。[Patching Leaks，BIW-0074](../03_reading/R03/BIW-0074.md) Tables 1–3发现，即便使用因果注意力，卷积和重叠候选均值仍可引入未来信息；其无泄漏填充臂仍翻译失败。Hourglass的[BIP-0104](../02_inventory/DETAILED_INVENTORY.md#BIP-0104)必须保留移位残差限定：只有缩短分支缺少当前组历史，紧邻前一个符号仍可经残差获取。Scratchpad patching，[BIW-0076](../03_reading/R05/BIW-0076.md) §3，又把临时刷新与持久分块数量分开。这些是相连的可用性问题，不是同义的边界错误。

<a id="45-sequence-state-and-execution-alternatives-to-reducing-text-positions"></a>
### 4.5 序列状态与执行：减少文本位置之外的替代方案

这一族是独立领域叙述所必需的，因为长字节序列不一定要靠学习式切分处理。乘性循环改变已观察符号更新状态的方式；选择性状态空间模型控制写入与保留；稠密注意力暴露存储位置；稀疏/哈希注意力减少交互；分段循环复用历史；固定潜在数组把深层工作转到另一组状态。

[BIW-0071](../03_reading/R09/BIW-0071.md) §2扩大普通40层因果字节Transformer。处理后lm1b的似然表明，在该设置中，有竞争力的结果并非内在地以分词为前提；它没有建立等计算或未经处理的原始文本覆盖，因为语料已替换罕见词并打乱句子。[Sparse Transformer，BIW-0118](../03_reading/R09/BIW-0118.md) §7.2/Table 2保留位置：固定稀疏得0.99 BPB，稠密为1.00，跨步稀疏虽Time/Iter更小，却恶化到1.13。模式与任务很重要。

[Reformer，BIW-0139](../03_reading/FIELD_ADDENDUM/arxiv_2001.04451v2.md) §§2–3区分局部敏感哈希（LSH）注意力、可逆激活重建与前馈分块执行。可逆块减少随深度增长的训练存储，不能由此推出推理KV减少；执行块不是语义片段。即使同样大的全注意力对照无法训练，更大模型能装入内存仍是有用证据。

[ACT，BIW-0138](../03_reading/FIELD_ADDENDUM/arxiv_1603.08983v6.md) §§2/3.5在单个字节内增加重复转移。任务损失加计算思考惩罚学习停机，求导时把离散停止计数视为固定。Wikipedia误差仅为训练集结果，使用/不使用ACT相当接近。计算投入轨迹是“不确定性与效用”讨论的先驱，不证明切分或额外转移提高留出集字节质量。状态大小、更新频率、位置内深度和存储且可访问的历史，仍是独立维度。

<a id="46-output-and-decoding-coherence-amortization-and-acceptance-are-separate-jobs"></a>
### 4.6 输出与解码：一致性、摊销与接受各有任务

未来窗口可用局部自回归条件分布、独立边缘分布、依赖电路或去噪块建模，表达力与采样成本不同。辅助未来损失可以改善表示，却未必规定一致联合分布或并行采样器。

MEGABYTE小型局部解码器保留块内字节依赖，同时承担串行局部成本。[LCA，BIW-0015](../03_reading/R05/BIW-0015.md) §3使用片段感知预测和公共头投影；置信阈值输出若未经另行验证，就是改变后的策略。[AU-Net，BIW-0077](../03_reading/R10/BIW-0077.md)通过路由与移位，在同一个下一字节目标下形成不同预测跨度，不是独立的词目标监督。要宣称在线因果，其正则表达式预处理仍需实际的前缀稳定性证据。

[MtPC，BIW-0079](../03_reading/R05/BIW-0079.md) §3/Appendices B–C通过混合、隐马尔可夫模型（HMM）和树电路因子分解提供规范化依赖草稿。表达力有代价：报告的16字节rank-32树投影约730M参数，因子分解投影为21M。接受更多仍可能更慢：EvaByte/L40S采样中，rank 128接受6.02字节，rank 32为5.88，但吞吐分别182.3与191.0字节/s（Table 1；批量1，排除预填充并抑制EOS）。

精确贪心一致、精确保留随机目标分布，以及近似阈值/top-k接受，是不同论断。MtPC普通Algorithm 3规定残差修正；**优化缓存Algorithm 2的随机精确性仍未验证**，见[CLAIM_RULES §3](../05_review/CLAIM_RULES.md#3-mtpc-exact-source-level-qualification-not-a-software-verdict)。这是来源层面的问题，不是已发布代码的缺陷，也不是舍弃实测吞吐的理由。[Block diffusion，BIW-0089](../03_reading/R05/BIW-0089.md)提供另一种生成约定，不会因为损失能按字节表达就成为普通链式负对数似然（NLL）。

<a id="47-probability-interface-correct-the-event-not-merely-the-units-on-the-axis"></a>
### 4.7 概率接口：修正事件，而不只修正坐标轴单位

这一族既有算法，也有方法论区别。规范词元路径、完整字符串边缘概率、任意字节前缀事件、带标记的字节加边界过程和去噪条件分布，不能互换。字节分母只表达分数尺度，不能改变获得概率的事件。

[BIW-0080](../03_reading/R04/BIW-0080.md) §§2–4把切分当成完整文本似然中的潜在路径，使用重要性采样。[BIW-0088](../03_reading/R04/BIW-0088.md) §4/Appendix A则为原始字节前缀条件概率，对相容词元前缀覆盖求和。两者问题相关而不同。后者精确性依赖无损规范支持集假设；把非规范神经概率质量置零后再归一化，会改变原始神经分布。增量复用覆盖减少重复工作，但仍有分词器、词表聚合和覆盖/缓存成本。

[BIW-0132](../03_reading/R04/BIW-0132.md)诊断“条件取规范词元前缀而非原始字符串前缀”的问题；[BIW-0133](../03_reading/R04/BIW-0133.md)用断点回归估计排名截点附近的入词表效应。前者是概率事件问题，后者是在局部设计假设下的统计处理效应问题，不是同一待估量的两次测量。

对相同评分事件，`NLL_nats/(original_bytes × ln 2)`是有效记账。清楚标明后，报告按字节归一化的规范路径分数，而不声称文本边缘概率，也合法。TokSuite的[BIP-0286](../02_inventory/DETAILED_INVENTORY.md#BIP-0286)不同：印出的CE/log₂V不是通用BPB换算，实际Figure 6计算未知。该图不能认证相等，但独立支持的选项排序与文本对照仍可使用。

<a id="48-sharing-and-geometry-distinguish-hard-equality-transformed-reuse-and-gradient-effects"></a>
### 4.8 共享与几何：区分硬相等、变换复用和梯度效应

绑权减少独立参数，归一化改变logit，适配器改变表示自由度，路径梯度分析诊断学习；任何一个都不能决定其他几个。字节紧凑字母表也改变经典词汇子空间论证所涉及的维度。

[Press和Wolf，BIW-0035](../03_reading/R08/BIW-0035.md)区分输入/输出绑权、输出侧投影和编码器/解码器三路词汇共享。[Inan等，BIW-0036](../03_reading/R08/BIW-0036.md) §§3–6分别测试嵌入派生软目标、矩阵复用及两者结合。其有条件的共享列空间论证本身既不证明表格严格相等，也不测试256字节字母表。由这些词语言模型实验推出“绑权改善字节模型”的广泛规则，会超出证据。

[BIW-0091](../03_reading/R08/BIW-0091.md) §2.2说明公式为何重要：`wᵢᵀh/||wᵢ||`保留隐藏状态幅度，不是完整余弦归一化；非对称的输出平方范数缩放又不同。没有FULL支持时，伪逆绑权、nGPT和混合softmax仍只是有范围的A/P背景，其纳入提供技术线索，不是决定性字节结果。

[共享登记表](../02_inventory/TAXONOMY.md#version--and-axis-specific-sharing-register-current)分开MEGABYTE局部字节输入/输出、LCA头/头、Reformer Q/K和ELMo方向间共享。ELMo指定PARTIAL §3.1确立方向间表示共享、方向间softmax共享及分开的方向LSTM，不是输入组合器与词softmax相等。论文规定、静态配置、运行时别名是不同证据层。BLT/H-Net未说明的共享轴仍未知。

<a id="49-objectives-and-gradient-control-a-learning-signal-must-have-a-named-job"></a>
### 4.9 目标与梯度控制：学习信号必须有明确用途

辅助损失可暴露预测结构、约束速率、稳定深度、对齐空间或保留潜变量使用。因此，应按提供的信息与梯度分类训练目标，而不只看“辅助”一词。

[BIW-0108](../03_reading/R08/BIW-0108.md) §§5.1–5.6的临时干预在字节分辨率模型内区分容量、分组暴露、边界提示、位置距离、归一化和子词目标。但四字节阶段除了暴露更多文本，也改变输入分组并压掉四分之三目标位置。大模型运行临近结束时，临时下一子词头仍更差，且有阶段转换/头部混杂；它不是多字节预测的普遍负面结论。离线边界起点和重复RoPE（旋转位置编码）在支持部署论断前也需前缀一致性证据。

[梯度手术，BIP-0200](../02_inventory/DETAILED_INVENTORY.md#BIP-0200)和[梯度相似性门控，BIP-0201](../02_inventory/DETAILED_INVENTORY.md#BIP-0201)是处理目标冲突的背景技术，不是已经证明可修复一切字节路由器的方案。投影/门控作用于共享更新，收益仍须在主任务评价。句子变分自编码器（VAE）记录[BIP-0202–0205](../02_inventory/DETAILED_INVENTORY.md#BIP-0202)涉及随机后验/先验坍缩与推断滞后，不应把每个确定性残差旁路都改称“后验坍缩”。GQ-VAE量化编码与重建回退处理的是另一种内容/保真问题。这条路线故意保留目标的异质性，但精确区分数学对象。

<a id="410-pretrained-adaptation-preserve-function-across-a-changed-interface"></a>
### 4.10 预训练适配：接口改变后保留功能

静态拼写到向量模仿可低成本复用词汇空间，但匹配一个向量不一定复现其在主体内的作用。主要策略进展是**类型级几何→上下文行为→预测分布→完整字节部署**。这些是可分的训练阶段，不是前一阶段必然带来的后果。

[Char2Subword，BIW-0122](../03_reading/R06/BIW-0122.md)拟合余弦/L2/邻域/词元身份目标，再通过冻结mBERT训练。[Bolmo，BIW-0097](../03_reading/R06/BIW-0097.md) §3.2.1在四层冻结网络之后匹配表示，在学习字节加边界输出时蒸馏分块概率。冻结主体仍有向输入反传的工作，其保留后缀表也使参数化仍为混合。§6.2只做第二阶段的对照并不灾难；对齐有帮助，尤其在1B时，但额外全局计算使差异缩小。

[BIW-0098](../03_reading/R06/BIW-0098.md)区分字节输入/词元输出蒸馏与后续字节解码器。[BIW-0099](../03_reading/R06/BIW-0099.md)把不同教师映射到字节监督，但检验指令行为是否实际迁移。[BIW-0103](../03_reading/R06/BIW-0103.md)区分近似前缀目标与带词元结束标记目标；标记历史上的精确性不是无标记边缘概率。来源代码清单未展示预处理，不证明遗漏了EOT展开。

[Zero-Shot Tokenizer Transfer，BIW-0126](../03_reading/R06/BIW-0126.md)用超网络摊销嵌入预测，以预热/重叠锚点稳定学习。ELMo窄范围[BIP-0293](../02_inventory/DETAILED_INVENTORY.md#BIP-0293)是更早的冻结上下文迁移路线，不是字节转换。对于这些方法，继承预训练、教师推理、转换数据、合成任务监督和解冻权限，均属于资源约定。

<a id="411-task-utility-and-diagnostics-distinguish-recoverable-information-from-usable-behavior"></a>
### 4.11 任务效用与诊断：区分可恢复信息和可用行为

评价层问接口是否有利于任务、人群或扰动设置，不只是是否暴露符号。探针、监督干预、自然提示、合法解码和精确复制的终点不同。

[SpellingBee，BIW-0110](../03_reading/R10/BIW-0110.md) Table 1在冻结嵌入上训练非线性字符解码器，使用词元类型留出和过滤，发现可恢复的正字法信息，但主体并未自己执行这种解码。其单独的拼写初始化干预，在报告的运行中几乎不分离掩码语言模型损失（§5）。[Strawberry，BIW-0113](../03_reading/R10/BIW-0113.md)研究受控字符任务与新增字符通道；[CharBench，BIW-0114](../03_reading/R07/BIW-0114.md)区分计数和定位。不能合并成一个“字符感知”分数。

[Synthetic and Natural Noise，BIW-0109](../03_reading/R07/BIW-0109.md) Tables 6–7展示顺序不变均值、字符CNN与混合噪声训练的取舍。对乱序不变性是精确的，却损失区分能力和干净质量；混合训练用专门表现换广泛覆盖。自然噪声过程是编辑词典替换，不是未改动的带噪平行语料。来源涉及字符/词和子词系统，不是原生UTF-8字节前沿。

多语言对照把分词器数据失衡与模型数据失衡分开，[BIP-0226](../02_inventory/DETAILED_INVENTORY.md#BIP-0226)，并衡量本地标注机会，[BIP-0227](../02_inventory/DETAILED_INVENTORY.md#BIP-0227)。方言研究[BIW-0134](../03_reading/R10/BIW-0134.md)的相关关系依赖任务/指标，不是分词器干预。后文关于Llama的正相关句可以指信息平等性；[最新更正](../05_review/CLAIM_RULES.md#7-new-r10-clarification-do-not-manufacture-a-dialect-tp-prose-contradiction)不支持断言词元化平等性符号冲突。合法标量、正确标量、任务答案和公平分配仍是不同结果。

<a id="412-budget-and-selection-evidence-choose-the-comparison-before-declaring-the-winner"></a>
### 4.12 预算与选择证据：先决定比较什么，再宣布胜者

这一条路线包括实证研究设计、统计和系统记账，不是又一种神经架构。等位置控制的资源不同于等原始文本；等总参数可以把容量从词表转移出去；等训练FLOPs不保证等延迟或等内存。

[ByT5卡，BIW-0024](../../flued_multigranularity_survey_20261108/03_reading/B08/W0351.md) §§3/6/Tables 9–10结合相同名义位置、远少于mT5的原始文本暴露，以及任务特定推理成本。Table 10的XNLI不是NER；短标签句对处理很慢，不能只归因于生成答案长。偏重编码器的深度分配是另一项架构干预。

[Compute Optimal Tokenization，BIW-0047](../03_reading/R05/BIW-0047.md)用拟合的FLOP前沿研究字节、压缩与主干规模；其拟合主干参数口径不是整个模型的驻留内存。[BIW-0028/BIP-0050](../02_inventory/DETAILED_INVENTORY.md#BIP-0050)在**3:1 Gated DeltaNet/Gated Softmax Attention混合架构**上，同时保留字节的等参数优势与子词的等训练FLOP优势。“平坦”指无显式局部–全局–局部层级，不是纯注意力Transformer；拟合N包括输出表，但排除输入/哈希表。

[BIW-0049](../03_reading/R08/BIW-0049.md)确实使用成对预测、支持向量机（SVM）校准和排序等统计学习工具，从小规模证据估计分词器效用。[BIW-0131](../03_reading/R08/BIW-0131.md) Tables 2/6/11–14反驳压缩充分性：最少词元切分未必使任务准确率最高。等模型词元训练仍使原始文本暴露不等。代理指标应被归为有迁移限制的预测工具，不能替代匹配实验。

<a id="413-segmental-structure-marginalize-latent-lexical-units-rather-than-equate-boundaries-with-compute-gates"></a>
### 4.13 分段结构：边缘化潜在词汇单位，而不把边界等同计算门

描述长度切分、潜在片段生成和后验MAP边界处理词汇发现。计算路由器可定义有用更新位置而不恢复词汇词；词汇分段模型可恢复类词单位，却没有高效流式部署。这是分段路线与分组、层级保持区别的原因。

[BIW-0043](../03_reading/R02/BIW-0043.md)使用非神经子串频率、经验编码长度和动态规划；期望最大化（EM）与层级分块是提议方向，不是已实现的神经模块。[Segmental Neural LM，BIW-0042](../03_reading/R03/BIW-0042.md) §§2–4混合字符拼写LSTM与学习式词汇记忆分布，在条件半马尔可夫假设下边缘化允许的切分。期望半环惩罚提供长度先验。可选VGG19图像注意力加入外部监督与预训练计算。

同一来源谨慎区分边缘语言似然与整句MAP切分。BR-phono上，Table 1完整模型F1为79.3，去掉记忆和惩罚为42.5；Appendix F在训练/验证/测试并集上评价边界。报告的样本排除训练中未见字符类型。这些条件支持实质性的结构学习结果，不支持开放字节覆盖或纯留出集切分。多位日期/数字的过度切分仍是具体负面结果。其他分段储备保持A/P深度，不继承本来源FULL状态。

<a id="5-cross-family-technique-links-and-duplicate-handling"></a>
## 5. 跨族技术联系与重复处理

最有用的技术索引应描述关系。**CNN**可用于词组合、有序软块池化和局部因果上下文；**注意力**可用于全局检索、潜在聚合和输出查询；**动态规划**可用于编码切分、潜在边缘化、最短路径和概率估计。每次都须说明数学作用。**蒸馏**可以对齐向量、上下文状态、词元logit、字节目标或序列级翻译模式。**门控**可以变换局部特征、在字节内停机、选择主干更新、删除位置或修改辅助梯度。复用技术名称不意味着所解问题相同。

下列相连记录应放在共同讨论中，同时保留来源特定证据：

| 上位讨论 | 应连接记录 | 为什么不是独立重复实验 |
|---|---|---|
| 计算投入与不确定性 | [0054](../02_inventory/DETAILED_INVENTORY.md#BIP-0054)、[0157](../02_inventory/DETAILED_INVENTORY.md#BIP-0157)、[0162](../02_inventory/DETAILED_INVENTORY.md#BIP-0162)、[0289](../02_inventory/DETAILED_INVENTORY.md#BIP-0289) | 效用标签、置信度富集、新颖性代理和ACT轨迹测量不同对象。 |
| 什么内容进入短表示？ | [0010](../02_inventory/DETAILED_INVENTORY.md#BIP-0010)、[0026](../02_inventory/DETAILED_INVENTORY.md#BIP-0026)、[0152–0153](../02_inventory/DETAILED_INVENTORY.md#BIP-0152) | 聚合比较与顺序保持组件涉及相关但不同的算子。 |
| 边界学习 | [0009](../02_inventory/DETAILED_INVENTORY.md#BIP-0009)、[0146](../02_inventory/DETAILED_INVENTORY.md#BIP-0146)、[0164–0165](../02_inventory/DETAILED_INVENTORY.md#BIP-0164) | 替代梯度、得分函数恒等式和方差缩减，不是等价的无偏算法。 |
| 主体兼容性 | [0206](../02_inventory/DETAILED_INVENTORY.md#BIP-0206)、[0210](../02_inventory/DETAILED_INVENTORY.md#BIP-0210)、[0247/0249](../02_inventory/DETAILED_INVENTORY.md#BIP-0247) | 几何、上下文功能和分阶段目标可共享上位问题，但主体和训练权限不同。 |
| 前缀事件解释 | [0111/0182/0278](../02_inventory/DETAILED_INVENTORY.md#BIP-0111)、[0274–0277](../02_inventory/DETAILED_INVENTORY.md#BIP-0274) | 事件定义、修正算法、运行记账、集成和统计处理效应不同。 |
| 合法输出与预期输出 | [0112](../02_inventory/DETAILED_INVENTORY.md#BIP-0112)、[0063–0065](../02_inventory/DETAILED_INVENTORY.md#BIP-0063) | 标准、合法性测试、预期标量测试和混杂分析不是四项模型失败。 |
| 共享与审查例外 | [0284–0286](../02_inventory/DETAILED_INVENTORY.md#BIP-0284)、[0294](../02_inventory/DETAILED_INVENTORY.md#BIP-0294) | 架构规定和开放指标问题，不是额外提出的学习方案。 |

整合者应保留一个上位论述，在子发现改变机制或推断的地方附上它们。在多标题下重复同一卡片段落，不会增加证据独立性。反之，把同一论文所有记录压成一句，也可能擦掉对照：MANTa瓶颈、MEGABYTE局部依赖与额外评分工作、Bolmo无对齐对照，即使分别与其他发现同源，也值得单独处理。

<a id="6-what-this-organization-leaves-open"></a>
## 6. 这一组织方式留下的开放问题

本分类支持一篇没有通用赢家、也不偏好单一架构的长综述。它把历史字符系统、编码器、序列到序列去噪器、因果字节链、字节完备子词和词汇混合接口放到相互关联的位置，却不把其输出转成同一对象。任何实质比较都应保留**输入/内部/输出/监督单位、可见信息、概率或任务事件，以及真正匹配的资源**。

研究机会来自这些交叉点：效用可跨语言/领域变化而保持的速率控制器；学习分组下的顺序/内容保真；在线字节预测器的前缀稳定预处理；与实现相连且有修正约定的一致依赖草稿；同时保留通用和字符敏感任务能力的功能性检查点转换；把字节长度与知识、标注机会分开的多语言评价；以及匹配质量下测量完整标量、精确字符串、预填充、批处理和尾延迟的服务研究。这些是开放问题或覆盖薄弱的交叉区域，不是已测得的普遍失败。

所选语料足以支持严肃的选择性综述，却不是压缩的穷尽历史，也不是统一资源排行榜。未知张量共享仍未知；ELMo/GPT-2有意限定的PARTIAL仍保持窄范围；ACT仅训练集字节证据、Reformer最大对照不匹配等条件仍紧贴各自论断。领域多样性本身有解释价值：分词会一起改变多项约束，而许多成功技术的作用，正是再次把这些约束分开。
