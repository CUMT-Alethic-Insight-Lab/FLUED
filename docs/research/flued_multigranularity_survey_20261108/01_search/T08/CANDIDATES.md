# T08 首轮确认候选：字节接口、多语言公平评价、内容因果消费与探针局限

日期：2026-11-08。**45 个去重作品；27 个精读优先；全文精读 0。** 全部确认项已实际获取原始摘要或作者官方介绍，确认只指作品身份和摘要关联，不表示其结论得到独立复现。作者未从本轮返回内容明确提取者写 `—`，不把 arXiv 提交人冒充作者。检索与失败见 `SEARCH_LOG.md`；下一轮问题汇总见 `HANDOFF.md`。

深度：**A**=原始摘要核验；**O**=作者官方项目介绍核验。多版本仍只计一个作品；未逐版对比的方法变化不宣称相同。`P`=精读优先（27项），不是已精读。每项“支持/反例”均是潜力或作者摘要主张，不是本轮全文判决。页面已提供的 PDF 为全文入口，本轮未逐页阅读。下文技术词解释：byte=字节；token=分词单元；权重共享=输入嵌入与输出分类矩阵使用同一组参数；因果消费=改变目标内容会特异性改变最终预测；探针=额外训练或拟合的表示读出器；FLOPs=浮点运算次数；BPB=每原文字节的比特数；UTF-8=一种可变长度Unicode编码。

## A. 字节/字符接口与粒度机制（15）

### T08-001 · P · ByT5: Towards a Token-Free Future with Pre-trained Byte-to-Byte Models
- 作者/年份：Linting Xue et al.；2021预印本 / 2022 TACL。标识：arXiv:2105.13626；TACL 2022.tacl-1.17，合计一作。
- 核验：A；[原摘要](https://arxiv.org/abs/2105.13626) 已获取；[正式版身份入口](https://aclanthology.org/2022.tacl-1.17/) 经搜索核验。全文：[PDF](https://arxiv.org/pdf/2105.13626)。
- 机制关联：最小改动Transformer直接处理字节，显式讨论参数、训练FLOPs与推理速度；适合建立byte/token比较的基准。
- 支持/反例潜力：作者称鲁棒性、拼写/发音任务受益；不代表等参数即可等成本，也不证明任意细节因果消费。
- 精读问题：提取参数拆分、编码/解码长度与任务差异；输入共享与输出头共享分别是什么？本轮两次公共config获取失败，**未独立核验权重共享配置**；无效UTF-8的解码处置是否改变评分？

### T08-002 · CANINE: Pre-training an Efficient Tokenization-Free Encoder for Language Representation
- 作者/年份：—；2021预印本 / 2022 TACL。arXiv:2103.06874v4；DOI 10.1162/tacl_a_00448，同作。
- 核验：A；[官方摘要及期刊关系](https://arxiv.org/abs/2103.06874)。全文：[PDF](https://arxiv.org/pdf/2103.06874)。
- 机制关联：字符输入、下采样、深层编码器；对照mBERT及TyDi QA。**字符不是原始字节**，需单独标识。
- 支持/反例潜力：作者报参数更少且QA更好；非自回归生成证据，不可直接映射生成成本。下一步：提取字符散列、下/上采样、软分词监督及任务边界。

### T08-003 · P · MEGABYTE: Predicting Million-byte Sequences with Multiscale Transformers
- 作者/年份：Lili Yu et al.；2023。arXiv:2305.07185v2；NeurIPS2023身份由搜索命中，版本内容差异未读。
- 核验：A；[原摘要](https://arxiv.org/abs/2305.07185)。全文：[PDF](https://arxiv.org/pdf/2305.07185)。
- 机制关联：固定patch内局部模型与patch间全局模型，显式多尺度字节计算。
- 支持/反例潜力：作者称可与子词模型竞争；可测试固定粒度是否已足够，反对“必须学习边界”的先验。
- 精读问题：局部原始字节路径保留了什么？全局表示是压缩瓶颈还是另有旁路？同FLOPs是否统一训练原文量、上下文覆盖、全局/局部参数和解码开销？有无来源回访，而非仅局部重建？

### T08-004 · P · MambaByte: Token-free Selective State Space Model
- 作者/年份：Junxiong Wang, Tushaar Gangavarapu, Jing Nathan Yan, Alexander M. Rush；2024。arXiv:2401.13660v3；官方仓标CoLM24，不另计。
- 核验：A+O；[摘要](https://arxiv.org/abs/2401.13660)；[官方仓介绍与指标换算示例](https://github.com/jxiw/MambaByte) 均获取，未审模型源码。全文：[PDF](https://arxiv.org/pdf/2401.13660)。
- 机制关联：纯字节状态空间模型；token草拟、byte验证的推测解码。
- 支持/反例潜力：作者报告字节模型可竞争、解码加速；可反驳字节接口或递归形式必然无效，不代表固定状态能保留任意精确历史。
- 精读问题：逐数据集检查token/byte换算分母、训练量、有效上下文及草拟器额外成本；官方README的换算片段本身不能替代复算。共享/不共享实际配置尚未核验，公共源码获取失败。

### T08-005 · P · SpaceByte: Towards Deleting Tokenization from Large Language Modeling
- 作者/年份：Kevin Slagle；2024。arXiv:2404.14408v3；页面/索引亦用无SpaceByte前缀标题，视同一作。
- 核验：A；[摘要](https://arxiv.org/abs/2404.14408)。全文：[PDF](https://arxiv.org/pdf/2404.14408)。
- 机制关联：在空格等边界字节后执行更大的全局块，以规则选择加工位置。
- 支持/反例潜力：作者称固定训练/推理计算预算下约匹配分词模型；是学习式分组的廉价竞争解释。
- 精读问题：无空格文字、中文、多字节首/续位如何调度？是否严格控制总原文量和生成字节数？边界规则是不是把语言先验直接放进算法？

### T08-006 · Beyond Language Models: Byte Models are Digital World Simulators（bGPT）
- 作者/年份：Shangda Wu, Xu Tan, Zili Wang, Rui Wang, Xiaobing Li, Maosong Sun；2024。arXiv:2402.19155（作者官方BibTeX确认）。
- 核验：O；[官方仓模型介绍、引用与架构说明](https://github.com/sanderwood/bgpt)。全文：[PDF](https://arxiv.org/pdf/2402.19155)。
- 机制关联：12层patch decoder与3层byte decoder、下一字节预测、多模态/CPU状态任务。
- 支持/反例潜力：精确二进制任务可帮助构造非语言先验考场；官方“任意计算任务”表述不可当作已验证能力边界。
- 下一步：读正文任务生成器、错误率分母与泛化划分；共享状态**未核验**，本轮猜测文件路径404，未以其推断实现。

### T08-007 · P · Byte Latent Transformer: Patches Scale Better Than Tokens（BLT）
- 作者/年份：Artidoro Pagnoni et al.；2024预印本 / ACL2025。arXiv:2412.09871 = 2025.acl-long.453，同一作。
- 核验：A；[预印本摘要](https://arxiv.org/abs/2412.09871) 与[正式摘要](https://aclanthology.org/2025.acl-long.453/) 均获取。全文：[正式PDF](https://aclanthology.org/2025.acl-long.453.pdf)。
- 机制关联：下一字节熵分patch，局部编码/解码与昂贵全局主干分离；摘要报8B参数、4T训练字节、FLOP控制扩展。
- 支持/反例潜力：字节模型规模证据；熵路由与真实任务效用是否对齐是反例入口。
- 精读问题：小熵模型训练及在线成本是否全计？patch内信息如何被全局读取？细节来自保留原字节、重算还是latent？有无严格byte/token同内容、延迟和共享消融？

### T08-008 · P · Dynamic Chunking for End-to-End Hierarchical Sequence Modeling（H-Net）
- 作者/年份：Sukjun Hwang et al.；2025。arXiv:2507.07955v2；本轮未核正式版关系。
- 核验：A；[摘要](https://arxiv.org/abs/2507.07955)。全文：[PDF](https://arxiv.org/pdf/2507.07955)。
- 机制关联：端到端、内容/上下文依赖分组，可迭代多层；byte与BPE同计算/数据比较。
- 支持/反例潜力：“多粒度必须靠外部监督”反例；也可能已有与草案部分同构的层级机制，但摘要未确认来源回访。
- 精读问题：层级表示、下采样、残差/反向展开到底保留什么？Query能否重新访问低层源？论文的同计算/数据如何计数？中文与代码优势是否只在特定预训练分布成立？

### T08-009 · Hierarchical Dynamic Chunking for Tokenizer-Free Language Modelling in Morphologically-Rich Languages（H-NET++）
- 作者/年份：—；2025。arXiv:2508.05628v1；单独作品，非H-Net版本。
- 核验：A；[摘要](https://arxiv.org/abs/2508.05628)。全文：[PDF](https://arxiv.org/pdf/2508.05628)。
- 机制关联：波斯语动态分组、跨chunk mixer、两级latent hyper-prior、正字法特殊处理与课程训练。
- 支持/反例潜力：形态丰富语言与ZWNJ（零宽非连接符）是比英语空格更强的边界考场；同时多个新增机制使归因不洁。
- 下一步：核查语料/训练预算、基线重训、公平性、代码可得性；摘要“无显式监督”与专门正字法处理需区分。只确认身份，不背书SOTA。

### T08-010 · P · When Tokenizers Fail: Byte-Level Chunking for Zero-Shot Transfer to Low-Resource Languages
- 作者/年份：—；2026。arXiv:2608.27658v1；搜索发现2026.emnlp-main.2139，正式关联待正文核。
- 核验：A；[原摘要](https://arxiv.org/abs/2608.27658)。全文：[PDF](https://arxiv.org/pdf/2608.27658)。
- 机制关联：从冻结子词模型初始化byte嵌入、chunk对齐损失、词性监督引导边界；六语言形态任务。
- 支持/反例潜力：对“无需token教师/词级监督即可迁移”构成条件提醒；byte粒度与词级任务存在接口错配。
- 精读问题：zero-shot针对哪条轴？教师、POS标注、对齐目标、语言数据是否算入预算？词级F1改善能否推出自回归LM或因果细节消费改善？

### T08-011 · P · Fast Byte Latent Transformer
- 作者/年份：Julie Kallini et al.；2026。arXiv:2605.08044v1；正式接收信息本轮只见二手/索引，未作确认结论。
- 核验：A；[摘要](https://arxiv.org/abs/2605.08044)。全文：[PDF](https://arxiv.org/pdf/2605.08044)。
- 机制关联：块扩散、局部decoder自草拟、扩散加自回归验证三条加速路线，BLT-D/S/DV为同作变体。
- 支持/反例潜力：修正“字节必逐字节串行”的过强假设；摘要说的是**估算内存带宽成本**降50%以上，不能替代墙钟。
- 精读问题：质量损失、额外训练目标、接受率、硬件、批量与真实延迟如何变化？所有分支是否仍保持相同概率分布？patch边界成本是否不变？

### T08-012 · P · Byte Language Models: Scaling, Emergent Abstractions, and Information Allocation
- 作者/年份：Jie Wang, Shiwei Luo, Qi Zhang, Yuanbin Wu；2026。arXiv:2610.05978v1。
- 核验：A；[摘要](https://arxiv.org/abs/2610.05978)。全文：[PDF](https://arxiv.org/pdf/2610.05978)。
- 机制关联：token-superposition训练、hash嵌入；普通byte Transformer涌现局部抽象，限制部分中间层计算仍保持下游表现。
- 支持/反例潜力：反对“必须专门层级架构才学得到分组”；也可能把训练或接口改动当成byte接口收益。
- 精读问题：token-superposition是否引入分词先验？拷贝探针与真实预测分别有何证据？限制25%中间层的操作、成本、任务范围与对照是什么？未核全文前不宣称一般性byte优势。

### T08-013 · P · Easy to anticipate, hard to compute: boundary dependence finds the computed outputs that entropy patching misses
- 作者/年份：Nicolás Vera Zúñiga；2026。arXiv:2610.11790v1。
- 核验：A；[摘要](https://arxiv.org/abs/2610.11790)。全文：[PDF](https://arxiv.org/pdf/2610.11790)。
- 机制关联：删除patch起点引起的自身loss变化作为边界依赖信号；两字节上下文查表对齐低成本在线决策。
- 支持/反例潜力：**最贴近“可预测不等于不需要计算”及真实On/Off效用**的近期候选；作者报紧预算下熵边界漏掉数学计算值。
- 精读问题：干预重算冻结哪些随机性/状态？标签构建成本、时序泄漏与分布变化？同patch数是否同FLOPs？复制/查找负例为何增益小？限定数学结果，不外推所有LM。

### T08-014 · P · Patch where the text is new: a compression view of where byte-level models should spend compute
- 作者/年份：Nicolás Vera Zúñiga；2026。arXiv:2610.22100v1。与013为不同标识/题名/方法的关联作品，**可能复用实验/语料，不作为独立复现**。
- 核验：A；[摘要](https://arxiv.org/abs/2610.22100)。全文：[PDF](https://arxiv.org/pdf/2610.22100)。
- 机制关联：借LZ77重复性观点，从前两字节查表预测新内容起点，无标签/参考模型；对照熵patch。
- 支持/反例潜力：因果效用之外的廉价规则竞争者；摘要明确代码上优势缩小、部分方案无效，适合收集反例。
- 精读问题：其与013是否版本演化/实验重叠到应合并？通用预训练表是否泄漏任务？域外代码、执行轨迹为何不胜？从数学高增益到通用语言的可迁移条件是什么？

### T08-015 · P · Universal Byte-Level Encoding: UTF-8/UTF-16 Routing to Reduce Cross-Script Token-Budget Disparities
- 作者/年份：Hyunsik Kim, Youngmoon Jung（官方仓索引）；2026。arXiv:2610.01984v2；正式会议状态不以仓标签单独背书。
- 核验：A；[摘要](https://arxiv.org/abs/2610.01984)。全文：[PDF](https://arxiv.org/pdf/2610.01984)；[官方项目入口](https://samsung.github.io/UBE/)，后者仅搜索发现。
- 机制关联：双字母表按字符确定性路由UTF-8/UTF-16，再执行标准BPE；编码地板与脚本公平性。
- 支持/反例潜力：说明UTF-8本身也有长度偏差；**这是BPE表示层改造，不是无分词byte LM的直接同构证据**。
- 精读问题：Unicode标量/字素/字符区别、合法性、混合脚本、回环可逆性与byte-native实验是否齐全？是否公平控制原文量、总词表和实际训练/推理成本？

## B. 多语言/内容匹配评价（4）

### T08-016 · P · A Multi-dimensional Evaluation of Tokenizer-free Multilingual Pretrained Models
- 作者/年份：Jimin Sun, Patrick Fernandes, Xinyi Wang, Graham Neubig；2022预印本 / EACL Findings2023。arXiv:2210.07111 = 2023.findings-eacl.128，同作。
- 核验：A；[正式摘要](https://aclanthology.org/2023.findings-eacl.128/)。全文：[PDF](https://aclanthology.org/2023.findings-eacl.128.pdf)。
- 机制关联：微调数据效率、内存、推理速度与准确率联合比较。
- 支持/反例潜力：**反向结果**：子词模型在不少实际设置更优，防止只引用byte正面工作。
- 精读问题：哪些任务/语言/规模导致排序翻转？训练数据、模型类型、编码器/解码器与参数拆分是否混淆？这些结论在现代patch模型上哪些仍适用？

### T08-017 · P · Language Model Tokenizers Introduce Unfairness Between Languages
- 作者/年份：Aleksandar Petrov et al.（其余作者本轮未提取）；2023。arXiv:2305.15425v2。
- 核验：A；[摘要](https://arxiv.org/abs/2305.15425)。全文：[PDF](https://arxiv.org/pdf/2305.15425)。
- 机制关联：同义平行文本的token长度差，成本/可用上下文；摘要明确字符和字节方案仍有超过4倍差异。
- 支持/反例潜力：**反驳byte天然多语言公平**，必须把词表覆盖、公平成本和原文覆盖分开。
- 精读问题：平行数据质量、语言长度内在差异、译文方向、单位与统计量如何定？字符或byte差异怎样与UTF-8位置/脚本分层结合？

### T08-018 · Do All Languages Cost the Same? Tokenization in the Era of Commercial Language Models
- 作者/年份：Orevaoghene Ahia, Sachin Kumar, Hila Gonen, Jungo Kasai, David Mortensen, Noah Smith, Yulia Tsvetkov；2023。arXiv:2305.13707 = EMNLP2023.emnlp-main.614。
- 核验：A；[正式摘要](https://aclanthology.org/2023.emnlp-main.614/)。全文：[PDF](https://aclanthology.org/2023.emnlp-main.614.pdf)。
- 机制关联：22种语言、API费用与下游效用分开核算。
- 支持/反例潜力：高费用与低质量可以同时发生；API定价不等于硬件成本，不可拿收费token数代替FLOPs。下一步：提取配对内容、经济可负担性和任务效用的独立定义。

### T08-019 · P · Rate–Utility Frontiers for Language Encodings: Comparing Tokens, Bytes, and Pixels Under Controlled Linguistic Content
- 作者/年份：Ingo Ziegler, Martin Krebs, Desmond Elliott；2026。arXiv:2607.16117v1。
- 核验：A；[摘要](https://arxiv.org/abs/2607.16117)。全文：[PDF](https://arxiv.org/pdf/2607.16117)。
- 机制关联：13语言/5脚本平行句、共享瓶颈容量扫描，区分输入位置数、latent容量和任务效用。
- 支持/反例潜力：作者结论无一种编码处处占优；正对“等参数/等位置就公平”的反例候选。
- 精读问题：共享瓶颈是不是人为偏置某接口？表面重建、跨语言对齐、主题分类与生成LM的外推界线；总计算、字节数与归一化怎样记录？

## C. 输入/输出权重共享（5）

### T08-020 · P · Using the Output Embedding to Improve Language Models
- 作者/年份：Ofir Press, Lior Wolf；2016预印本 / EACL2017（正式关系由检索引文确认）。arXiv:1608.05859v3。
- 核验：A；[摘要](https://arxiv.org/abs/1608.05859)。全文：[PDF](https://arxiv.org/pdf/1608.05859)。
- 机制关联：输入/输出embedding共享及更新规则，输出矩阵本身作为词向量。
- 支持/反例潜力：经典共享正面证据；其大词表参数节省不必适用于256字节表，点积共享不等于余弦归一化共享。
- 精读问题：词表、隐藏宽、参数/正则化、perplexity比较是否匹配？共享梯度偏输出是否已在原文提出？应与022配对而非制造矛盾。

### T08-021 · Tying Word Vectors and Word Classifiers: A Loss Framework for Language Modeling
- 作者/年份：Hakan Inan, Khashayar Khosravi, Richard Socher（正式作者列表需下一轮核）；2016预印本 / 2017版本。arXiv:1611.01462v3。
- 核验：A；[原摘要](https://arxiv.org/abs/1611.01462)。全文：[PDF](https://arxiv.org/pdf/1611.01462)。
- 机制关联：从loss框架推出输入embedding/输出投影共享，Penn Treebank实验。
- 支持/反例潜力：共享的理论动机与任务条件；不是字节接口因果消融。下一步：明确框架假设及辅助损失是否随共享一起改变。

### T08-022 · P · Weight Tying Biases Token Embeddings Towards the Output Space
- 作者/年份：Antonio Lopardo, Avyukth Harish, Catherine Arnett, Akshat Gupta；2026。arXiv:2603.26663v1；检索关联2026.findings-acl.2027，同作，正式全文差异未读。
- 核验：A；[原摘要](https://arxiv.org/abs/2603.26663)。全文：[PDF](https://arxiv.org/pdf/2603.26663)。
- 机制关联：早期输出梯度主导，共享空间偏输出；输入梯度缩放干预及tuned-lens（校准后的层间词表读出）分析。
- 支持/反例潜力：**最直接的新近共享负效应证据候选**；并非已证明字节接口共享有害。
- 精读问题：比较模型是否只差共享？输出梯度缩放的优化器/尺度效应是否另有解释？token模型、余弦输出、字节小词表三者能否分离？层间探针结论是否有部署行为佐证？

### T08-023 · Rethinking Weight Tying: Pseudo-Inverse Tying for LM Stable Training and Updates
- 作者/年份：—；2026。arXiv:2602.04556v2。
- 核验：A；[摘要](https://arxiv.org/abs/2602.04556)。全文：[PDF](https://arxiv.org/pdf/2602.04556)。
- 机制关联：共享latent token memory、正交记忆与正定变换，保持伪逆一致接口。
- 支持/反例潜力：共享不是简单二元开关；摘要同时承认从零训练时一致性与自由优化存在权衡。下一步：总参数/算力、继续预训练与从零训练分开；词表探针稳定不等于最终内容消费。

### T08-024 · AF-Muon: An AdamW-Free Muon Optimizer for Tied-Embedding Models
- 作者/年份：—；2026。arXiv:2610.01395v1；页面称较短版workshop接收，不计为独立作品。
- 核验：A；[摘要](https://arxiv.org/abs/2610.01395)。全文：[PDF](https://arxiv.org/pdf/2610.01395)。
- 机制关联：共享词表同时承受稀疏输入/稠密输出梯度，专门优化器几何。
- 支持/反例潜力：共享收益/损害可能与优化器适配交互；摘要报约1%步时开销而非免费。下一步：是否有真正tied/untied配对，还是只比较tied模型的优化器？未经配对不能作共享有益结论。

## D. 探针、干预与解释的可靠性（9）

### T08-025 · P · Designing and Interpreting Probes with Control Tasks
- 作者/年份：John Hewitt, Percy Liang；2019。D19-1275 = arXiv:1909.03368。
- 核验：A；[正式摘要](https://aclanthology.org/D19-1275/)。全文：[PDF](https://aclanthology.org/D19-1275.pdf)。
- 机制关联：随机词型控制任务，区分表示可读性与探针记忆能力；选择性而非单一accuracy。
- 支持/反例潜力：外加探针高分不能直接证明模型部署使用了信息。
- 精读问题：如何将词型控制改为字节/位置/语种/文档身份控制而不引入泄漏？样本外窗、随机表与模型初始化地板怎样设置？控制任务仍不能补出因果消费，需要哪些后续手术？

### T08-026 · Information-Theoretic Probing with Minimum Description Length
- 作者/年份：Elena Voita, Ivan Titov；2020。2020.emnlp-main.14 = arXiv:2003.12298。
- 核验：A；[正式摘要](https://aclanthology.org/2020.emnlp-main.14/)。全文：[PDF](https://aclanthology.org/2020.emnlp-main.14.pdf)。
- 机制关联：最小描述长度将预测质量与取得质量的数据/模型代价一起计算。
- 支持/反例潜力：能修正随机表示也可探出高分的问题；仍是可恢复性度量，不是消费证明。下一步：在线编码的划分顺序和语言/UTF-8类别比例如何影响比较？

### T08-027 · Probing Classifiers: Promises, Shortcomings, and Advances
- 作者/年份：Yonatan Belinkov；2021预印本 / Computational Linguistics2022。arXiv:2102.12452v4；DOI10.1162/coli_a_00422（正式索引），一作。
- 核验：A；[原摘要](https://arxiv.org/abs/2102.12452)。全文：[PDF](https://arxiv.org/pdf/2102.12452)。
- 机制关联：探针方法学综述，可作为精读防遗漏索引。
- 支持/反例潜力：梳理控制、容量、相关/因果边界，不能替代每个原始实验的证据。下一步：从其引用链补非线性探针/负结果，但不重复计数综述中未核验作品。

### T08-028 · P · Amnesic Probing: Behavioral Explanation with Amnesic Counterfactuals
- 作者/年份：Yanai Elazar et al.（完整作者未提取）；2020预印本 / 2021版本。arXiv:2006.00995v3。
- 核验：A；[摘要](https://arxiv.org/abs/2006.00995)。全文：[PDF](https://arxiv.org/pdf/2006.00995)。
- 机制关联：移除表示中某属性，观察下游预测；摘要称传统probe性能与任务重要性不相关。
- 支持/反例潜力：直接建立可读≠可用的实验路线；反面风险是删除不完整或伤及其他属性。
- 精读问题：随机同秩消融、属性相关性、分布外改变、剩余非线性信息如何控制？删除后无下降可排除多大效应，不可写成“信息不存在”？

### T08-029 · Naturalistic Causal Probing for Morpho-Syntax
- 作者/年份：—；2022。arXiv:2205.07043v2。
- 核验：A；[摘要](https://arxiv.org/abs/2205.07043)。全文：[PDF](https://arxiv.org/pdf/2205.07043)。
- 机制关联：在自然句输入层改性别/数，尽量保持其余句子不变；西班牙语多模型。
- 支持/反例潜力：自然输入替换可避免部分隐藏态分布外手术；但语法改变可能连带token长度/语义。下一步：提取成对生成、可交换性与混杂条件，作为内容替换对照的模板而非套用因果标签。

### T08-030 · P · How Reliable are Causal Probing Interventions?
- 作者/年份：Marc E. Canby, Adam Davies, Chirag Rastogi, Julia Hockenmaier；2024预印本 / IJCNLP-AACL2025。
- 标识/版本：arXiv:2408.15510早期题名 **Measuring the Reliability of Causal Probing Methods: Tradeoffs, Limitations, and the Plight of Nullifying Interventions**；=2025.ijcnlp-long.47。**题名变化去重为一作**。
- 核验：A；[arXiv摘要/版本历史](https://arxiv.org/abs/2408.15510) 与[正式摘要](https://aclanthology.org/2025.ijcnlp-long.47/) 均获取。全文：[正式PDF](https://aclanthology.org/2025.ijcnlp-long.47.pdf)。
- 机制关联：干预完整性、非目标保留的选择性、二者调和均值作为可靠性。
- 支持/反例潜力：**对“做过消融就因果证明”的直接反制**；作者称非线性干预往往更可靠。
- 精读问题：如何有独立真值测完整/选择性？目标内容替换、随机消融、诱饵、语种/位置保持能否形成相应控制？可靠性高是否足以识别通道必要性？

### T08-031 · P · Inference Time Causal Probing in LLMs
- 作者/年份：—；2026。arXiv:2605.07631v1。
- 核验：A；[摘要](https://arxiv.org/abs/2605.07631)。全文：[PDF](https://arxiv.org/pdf/2605.07631)。
- 机制关联：不用外接probe，依模型原生输出的margin梯度干预hidden state；含lookahead变体与完整性/选择性评价。
- 支持/反例潜力：回应“探针几何和部署预测几何错位”；但强制推向答案不等于证明原模型本就依赖该属性。
- 精读问题：定向操纵与自然消费的识别条件是什么？lookahead引入未来目标信息如何避免被误报因果能力？原生输出端相较probe的对照是否匹配干预强度？

### T08-032 · Attention is not Explanation
- 作者/年份：Sarthak Jain, Byron C. Wallace；2019。N19-1357 = arXiv:1902.10186。
- 核验：A；[正式摘要](https://aclanthology.org/N19-1357/)。全文：[PDF](https://aclanthology.org/N19-1357.pdf)。
- 机制关联：注意力权重与梯度重要性不一致，不同权重可同输出。
- 支持/反例潜力：路由/注意力图漂亮不等于内容实际消费；不可把旧RNN实验扩大成所有注意力必不可解释。下一步：与033配对读操作定义及全模型对照。

### T08-033 · Attention is not not Explanation
- 作者/年份：Sarah Wiegreffe, Yuval Pinter；2019。D19-1002 = arXiv:1908.04626。
- 核验：A；[正式摘要](https://aclanthology.org/D19-1002/)。全文：[PDF](https://aclanthology.org/D19-1002.pdf)。
- 机制关联：均匀权重、随机种子方差、冻结权重诊断、端到端对抗四测试。
- 支持/反例潜力：**反对把032当无条件定理**；解释可用性依定义和全模型测试而定。下一步：提取何种干预保持模型条件，哪些测试测必要/充分或仅可替代性。

## E. 长上下文检索评价（5）

### T08-034 · RULER: What's the Real Context Size of Your Long-Context Language Models?
- 作者/年份：Cheng-Ping Hsieh et al.；2024。arXiv:2404.06654v3。
- 核验：A；[摘要](https://arxiv.org/abs/2404.06654)。全文：[PDF](https://arxiv.org/pdf/2404.06654)。
- 机制关联：13任务，多针、多跳追踪、聚合；可控长度/复杂度。
- 支持/反例潜力：检索到一条随机串不代表完整长上下文理解；仍可能利用字面匹配。下一步：构造等原文字节长度版本、随机答案、相关内容替换并保留难度对照。

### T08-035 · BABILong: Testing the Limits of LLMs with Long Context Reasoning-in-a-Haystack
- 作者/年份：Yuri Kuratov et al.；2024。arXiv:2406.10149v2。
- 核验：A；[摘要](https://arxiv.org/abs/2406.10149)。全文：[PDF](https://arxiv.org/pdf/2406.10149)。
- 机制关联：20种事实推理任务嵌入长自然文本，含链式事实、归纳、计数等。
- 支持/反例潜力：分离单事实读取与组合推理，摘要报RAG单事实表现并非足够。下一步：训练/微调与无需训练的比较分层；事实更新、干扰项和分词长度的控制方式。

### T08-036 · P · NoLiMa: Long-Context Evaluation Beyond Literal Matching
- 作者/年份：Ali Modarressi et al.；2025。arXiv:2502.05167v3。
- 核验：A；[摘要](https://arxiv.org/abs/2502.05167)。全文：[PDF](https://arxiv.org/pdf/2502.05167)。
- 机制关联：最小化问题与needle的字面重叠，必须通过潜在关联定位证据。
- 支持/反例潜力：**摘要失明/路由漏召回最有区分力的考场之一**；不能把失败纯归注意力稀释，知识/关联推断同样可能是瓶颈。
- 精读问题：短窗基线、无上下文/置换关联/Oracle证据怎样分离定位与知识？若摘要没线索但原文有，是否强制需要回退？去字面匹配如何跨语言保持同难度？

### T08-037 · P · HELMET: How to Evaluate Long-Context Language Models Effectively and Thoroughly
- 作者/年份：Howard Yen et al.；2024预印本 / ICLR2025（官方/会议索引）。arXiv:2410.02694v3，同作。
- 核验：A；[摘要](https://arxiv.org/abs/2410.02694)。全文：[PDF](https://arxiv.org/pdf/2410.02694)。
- 机制关联：七类应用、可控长上下文、base模型可用的评估；59模型研究。
- 支持/反例潜力：作者发现NIAH与下游相关性不足、不同任务排序也不同；防止只在合成检索胜出就宣布架构优越。
- 精读问题：LLM评判可靠性、长度截断/输出限制、RAG快速开发任务为何能预测下游？byte/token必须怎样重建内容匹配而非照抄token长？

### T08-038 · Lost in the Middle: How Language Models Use Long Contexts
- 作者/年份：Nelson F. Liu et al.；2023预印本 / TACL2024。arXiv:2307.03172 = 2024.tacl-1.9。
- 核验：A；[正式摘要](https://aclanthology.org/2024.tacl-1.9/)。全文：[PDF](https://aclanthology.org/2024.tacl-1.9.pdf)。
- 机制关联：QA与键值检索的证据位置变化，首尾优于中部。
- 支持/反例潜力：相同证据不同位置即可改变答案；位置先验与内容依赖须分离。下一步：检查新架构有效性是否只来自重排证据，保持内容、距离、查询难度的成对对照。

## F. 多粒度来源回访与因果归因最近邻（7）

### T08-039 · P · RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval
- 作者/年份：Parth Sarthi et al.；2024。arXiv:2401.18059v1；正式版关系本轮未单独核。
- 核验：A；[摘要](https://arxiv.org/abs/2401.18059)。全文：[PDF](https://arxiv.org/pdf/2401.18059)。
- 机制关联：原文块递归嵌入、聚类、摘要构树，检索不同抽象层。
- 支持/反例潜力：**多粒度+源块保留组合的近邻，不能忽略**；摘要没有证明查询必先粗后细，或有漏召回回退。
- 精读问题：collapsed-tree与逐层遍历是否都回到叶子？可追溯父子映射、源块生命周期、失败回退、构树成本和更新成本是什么？是外部RAG非端到端latent，差异须据原文列而非靠名称。

### T08-040 · P · Beyond Chunking: Discourse-Aware Hierarchical Retrieval for Long Document Question Answering
- 作者/年份：Huiyao Chen et al.（搜索一作确认）；2025初版 / 2026修订。arXiv:2506.06313v5。
- 核验：A；[摘要/版本历史](https://arxiv.org/abs/2506.06313)，题名经官方搜索核。全文：[PDF](https://arxiv.org/pdf/2506.06313)。
- 机制关联：修辞结构树、LLM增强节点、结构指导层级检索；搜索片段提到内部节点向叶子展开。
- 支持/反例潜力：比“多种摘要并排检索”更接近**来源下钻**；下钻细节仅检索片段，尚未当全文证据。
- 精读问题：查询如何触发展开、叶子可恢复是否有保障？跨语言依赖解析质量如何控制？需要完整计入解析/增强/索引成本，确认任务是否评罕见精确细节而非只有泛QA。

### T08-041 · Bridge-RAG: An Abstract Bridge Tree Based Retrieval Augmented Generation Algorithm
- 作者/年份：—；2026。arXiv:2603.26668v2。页面版本史给v1=2026-01-12，与编号月份不一致，保留原标识，**日期待元数据复核**。
- 核验：A；[官方摘要/历史](https://arxiv.org/abs/2603.26668)。全文：[PDF](https://arxiv.org/pdf/2603.26668)。
- 机制关联：实体—摘要—文档块桥接、多级检索、Cuckoo Filter实体定位。
- 支持/反例潜力：显式讨论层级定位额外开销与恢复检索效率；可能是草案低成本来源路由的近邻。下一步：实体不存在/别名/摘要遗漏时是否回退，O(1)实体查找不能冒充总检索O(1)。

### T08-042 · Evaluation of Attribution Bias in Generator-Aware Retrieval-Augmented Large Language Models
- 作者/年份：Amin Abolghasemi, Leif Azzopardi, Seyyed Hadi Hashemi, Maarten de Rijke, Suzan Verberne；2024预印本 / ACL Findings2025。
- 标识/版本：arXiv:2410.12380（早版题名无Generator-Aware）=2025.findings-acl.1087，一作。
- 核验：A；[正式摘要](https://aclanthology.org/2025.findings-acl.1087/)。全文：[PDF](https://aclanthology.org/2025.findings-acl.1087.pdf)。
- 机制关联：变换来源作者元数据的反事实比较；引用质量/作者偏好变化。
- 支持/反例潜力：**正确引用或来源标注不等于真正依赖内容**，非内容元数据能改归因。下一步：把证据内容替换与元数据替换做正交控制；不要把作者偏好实验冒充内容必要性实验。

### T08-043 · P · Sufficient Context: A New Lens on Retrieval Augmented Generation Systems
- 作者/年份：Hailey Joren et al.；2024预印本 / ICLR2025（官方项目索引）。arXiv:2411.06037v3。
- 核验：A；[摘要](https://arxiv.org/abs/2411.06037)。全文：[PDF](https://arxiv.org/pdf/2411.06037)。
- 机制关联：先判上下文是否足够回答，再区分检索不足与生成器利用失败，含拒答。
- 支持/反例潜力：Oracle来源可回答但系统失败，与源本身缺信息是不同归因；自动充分性评判不等于因果使用证明。
- 精读问题：充分性自动判别是否有人工真值和域外校准？上下文仅部分有用时如何避免误归因？Oracle检索仍失败应测哪条消费路径？拒答收益是否牺牲覆盖率？

### T08-044 · Barriers to Counterfactual Credit Attribution for Autoregressive Models
- 作者/年份：—；2026。arXiv:2605.01425v1。
- 核验：A；[摘要](https://arxiv.org/abs/2605.01425)。全文：[PDF](https://arxiv.org/pdf/2605.01425)。
- 机制关联：部署时RAG来源信用归因；下一token归因条件不自动组合成整段生成归因，黑盒补归因存在复杂度下界。
- 支持/反例潜力：反对把单步删除效用加总当成完整答案来源贡献；**不是所有删除实验不可能**。下一步：读定理的弱最优条件、输出长度、访问权限及反事实信用定义，严格限制理论外推。

### T08-045 · P · Evidence Contextualization and Counterfactual Attribution for Conversational QA over Heterogeneous Data with RAG Systems（RAGONITE）
- 作者/年份：Rishiraj Saha Roy et al.（完整列表见后续）；2024预印本 / WSDM2025，DOI10.1145/3701551.3704126。
- 标识/版本：arXiv:2412.10571v3；会议身份由ACM搜索结果核，一作。
- 核验：A；[摘要](https://arxiv.org/abs/2412.10571)。全文：[PDF](https://arxiv.org/pdf/2412.10571)。
- 机制关联：源元数据和周边上下文增强；删除单条证据重新生成并比较答案；ConfQuestions英/德300会话问题、215公开Confluence页面。
- 支持/反例潜力：**来源定位+严格重新生成评估的直接近邻**，但相似度归因对同义改写/冗余证据仍可能失真。
- 精读问题：删除时随机性、prompt长度、顺序和其他来源是否固定？答案相似度如何校准为贡献？冗余来源单删无效、多删有效如何处理？与层级检索组合是否已存在，以及额外重算成本多大？

## 计数与版本复核说明

- 15 + 4 + 5 + 9 + 5 + 7 = **45**；A类中字符CANINE、BPE表示UBE与原生byte LM分别标明，不能一锅计作byte-native直接证据。
- 精读优先ID：001、003、004、005、007、008、010、011、012、013、014、015、016、017、019、020、022、025、028、030、031、036、037、039、040、043、045，共**27**。
- arXiv/正式版合并：ByT5、CANINE、BLT、Sun等多维评价、Ahia、Press/Wolf、权重偏输出、control tasks、MDL、probe综述、因果可靠性、双attention、HELMET、Lost-in-Middle、归因偏差、Sufficient Context、RAGONITE；未核实正式全文差异者明说未核。
- 013/014为同作者前后相邻研究，本轮按不同作品收录，独立证据簇只记一个；下一轮若作者明确视为替代稿，应合并作品计数而非保住数字。
- 未进入确认计数的线索：MrT5（2410.20771，仅检索引用命中）、2026 Tokenizer Tax（2607.24276，仅搜索发现）、Token-Native Storage（2608.02376，日期元数据异常）、adRAP（2410.01736，未读摘要）、EntropyMoE（2608.06398，未读摘要）、用户草案中的新模型链接（本专题未核）。没有用这些补数。
