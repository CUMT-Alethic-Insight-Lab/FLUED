# T01 定向扩展 R2：学习边界、压缩策略与合并学习

日期：2026-11-08。承接[覆盖红队](../../05_review/COVERAGE_AUDIT_R1.md)、[精读红队](../../05_review/READING_AUDIT_R1.md)，只写T01目录，不修改C01–C56、W编号、共享目录或已有证据表。本文是新增发现与摘要初筛；下一轮terra负责全文。实际查询和逐次取回账见[SEARCH_LOG_R2.md](SEARCH_LOG_R2.md)。

## 0. 实计与边界

- **新增32项有效发现候选**：均有原始摘要或作者/出版机构介绍核验，均未命中本轮读取的`02_catalog/CATALOG.md`的384个作品实体。用本地ID `R2-001`—`R2-032`，不自行分配W-ID、不改旧编号；预印本/正式版别名合并记一项。
- 深度：32项摘要核验，其中4项另读定向正文位置（R2-005/012/029/032）；**全文精读0，代码核验0，复现0**。全文被工具返回不表示逐节读过。21项标 **★** 精读优先，逐项问题在卡内。
- 年份覆盖1999—2025，新增没有用2026模型凑数。按本文所列首发年，2010年前3项（1999/2002/2009），2010—2019年14项，2020—2025年15项。年份是作品时间，不是索引抓取日期。
- 非英语发现：实际执行5条中文查询、1条日文查询；新增含1项中文原刊论文（R2-013），另有中文/日文/泰文及极低资源语言考场。日文作者原文另取得1份，但与已收英文半监督谱系关系未消歧，**不计新增作品**；不能用“查到日本/中国作者英文稿”替代非英语检索。
- **有效发现≠结果有效**。摘要确认作品和作者声称；涉及损失最优性、泛化、无损或加速的论断，须经下一轮全文和公平预算核查。作者全表未完整提取者记首作者或“待补”，不把arXiv的From投稿人充作作者。

## 1. 红队意见落到T01的具体改动

1. **经典桥接不再只列现代模型**：补最小描述长度、贝叶斯分段、半监督生成/判别交替，以及用任务损失学习组合顺序的早期工作。它们能排除“边界由语言模型预测自然长出”“连续/离散合并有梯度就是新概念”的替代解释。
2. **强负面而非只摘赢家**：补同代码复核、合成结构诊断、评价长度混杂，以及复核后仍支持语言模型结构归纳的反向结果；不把一个失败案例泛化成所有学边界不可能。
3. **边界/内容/预算拆轴**：合并表示如何产生、哪些位置合并、每层预算多大、哪一部分参数更新是四件事。R2-010/012/020尤其适合补“只训决策表征/只训率/全联合”的比较。
4. **不越权补其它专题**：HMT、来源撤销、数据库维护与读写记忆经典留给相应负责人；本轮仅跟学习信号/训练方式相接的缺口。已有MemWalker/ReadAgent/SSA等不能通过重发现另计。
5. **精读审计边界维持**：不借W0059/W0091的争议数学推步作为学习边界必然失败的依据；不把SpaceByte的中文初试或UTF续字节规则争议扩成所有字节分段无效。新卡继续区分经验、理论、实现与阅读状态。

## 2. 新增作品卡

### R2-001 — Unsupervised Neural Word Segmentation for Chinese via Segmental Language Modeling — ★
- **身份**：2018，Zhiqing Sun、Zhi-Hong Deng（原始检索PDF作者栏）；ACL `D18-1531`，关联arXiv `1810.03167`。来源/摘要[A](https://aclanthology.org/D18-1531/)；[全文](https://aclanthology.org/D18-1531.pdf)。预印本与EMNLP一项，不另计。
- **信号/方式**：无监督字符串生成似然；上下文编码器编码历史、段解码器逐段生成，语言建模与分段联合，不用人工词边界。全分段求和/长度上限的精确算法待全文。
- **对假说作用**：支持“预测信号可诱导中文段界”的历史先例；也要求区分语言学词界恢复和压缩后任务充分性，不将SIGHAN词F值当字节读出效用。
- **精读问题**：段长先验是否必要？边界边缘化、搜索解码、数据划分及中文多标准如何影响排序；同字符预测质量下分段是否仍可不同？

### R2-002 — A Masked Segmental Language Model for Unsupervised Natural Language Segmentation — ★
- **身份**：2021预印本/2022 SIGMORPHON，C.M. Downey、Fei Xia、Gina-Anne Levow、Shane Steinert-Threlkeld；ACL `2022.sigmorphon-1.5`＝arXiv `2104.07829`。来源/摘要[A](https://aclanthology.org/2022.sigmorphon-1.5/)；[全文](https://aclanthology.org/2022.sigmorphon-1.5.pdf)。
- **信号/方式**：跨度遮罩的双向语言模型目标，分段作为副产物，可无监督或轻监督训练；用Transformer替换递归分段器。
- **对假说作用**：比较自回归/双向上下文这一**可见性轴**，不能把分段提高全归新监督；摘要称中文优于递归SLM、英语相近，并非所有语言一致提高。
- **精读问题**：遮罩如何防目标跨度泄漏，轻监督提供多少词边界，结构/目标/数据是否分别消融，分段能力与预测能力是否同向？

### R2-003 — Multilingual unsupervised sequence segmentation transfers to extremely low-resource languages
- **身份**：2021预印本/2022 ACL；C. Downey、Shannon Drizin、Levon Haroutunian、Shivin Thukral；ACL `2022.acl-long.366`＝arXiv `2110.08415`。来源/摘要[A](https://aclanthology.org/2022.acl-long.366/)；[全文](https://aclanthology.org/2022.acl-long.366.pdf)。
- **信号/方式**：多语遮罩段语言模型预训练，再迁移到极低资源K’iche’；比较从零单语、仅Quechua预训练、多语预训练，十种目标数据量。
- **对假说作用**：支持分阶段迁移和类型学知识；摘要仅称6/10设置优于单语，不能省去其余设置。R2-002与本作同模型谱系，两个作品不当两次独立架构复现。
- **待查**：语言类型相似与语料总量、脚本/词长是否分离；零样本F值不代表通用高精度边界，是否借开发集边界选超参？

### R2-004 — Unsupervised Word Segmentation with Bi-directional Neural Language Model
- **身份**：2021预印本；作者待补，不把投稿人当作者；arXiv `2103.01421`，检索关联2022 ACM DOI `10.1145/3529387`但正式版差异未核。来源/摘要[A](https://arxiv.org/abs/2103.01421)；[全文](https://arxiv.org/pdf/2103.01421)。
- **信号/方式**：在所有可能分段下最大化句子生成概率；双向语言模型建上下文、两个解码算法合并双向信息；无需词边界标签。
- **对假说作用**：与R2-001提供上下文可见性变化入口，中文和泰文而非只英语。离线双向分段不能直接作为因果在线分段的公平赢家。
- **待查**：边缘化与近似、未来上下文权限、两个解码器差异、同模型容量与长度先验；正式版ID关联由编目负责人确认。

### R2-005 — Bayesian Unsupervised Word Segmentation with Nested Pitman-Yor Language Modeling — ★
- **身份**：2009 ACL-IJCNLP；Daichi Mochihashi、Takeshi Yamada、Naonori Ueda；ACL `P09-1012`。身份[官方页](https://aclanthology.org/P09-1012/)；摘要与定向正文[A+S](http://chasen.org/~daiti-m/paper/acl2009segment.pdf)；[正式全文入口](https://aclanthology.org/P09-1012.pdf)。官方HTML只取到元数据，PDF提取失败后作者公开PDF可读，不冒充原HTML已有摘要。
- **信号/方式**：生成字符/词序列的概率，嵌套字符拼写模型与词n元模型；块Gibbs采样配动态规划。摘要明确完全无监督，也可给定部分/全部边界。
- **对假说作用**：经典非神经联合分段与语言建模；**定向读§5.2**确认作者指出监督分段可有较好词F值但较差字符困惑度，直接表明两个目标不等价；这是作者结果，不是本轮复现。
- **精读问题**：§4.3长度先验、§5.2 Table 3/4各监督量和同语料比较；训练/测试是否传导式使用，生成似然最优为何不等于人工词界最优？不得外推成预测难度与所有任务效用相反。

### R2-006 — Do latent tree learning models identify meaningful structure in sentences? — ★
- **身份**：2017预印本、2018修订；Adina Williams等（题名检索作者线索，全表待补）；arXiv `1709.01121v2`。来源/摘要[A](https://arxiv.org/abs/1709.01121)；[全文](https://arxiv.org/pdf/1709.01121v2)。
- **信号/方式**：复核两种由下游句子任务训练的隐树模型，在共享代码库比较。
- **对假说作用**：作者报告只有一种胜过传统树模型，随机重启结构不稳定，树更浅且不似标准语法；反驳“任务分数提高即可证明学到稳定语义层级”。不证明这些结构不能预测。
- **精读问题**：两模型训练/搜索预算和种子数、准确率与树一致性的关系；有无随机/平衡/左/右分支结构强基线，重启差异是否统计可靠？

### R2-007 — ListOps: A Diagnostic Dataset for Latent Tree Learning — ★
- **身份**：2018 NAACL学生研究工作坊；Nikita Nangia、Samuel Bowman（原始检索引文，全元数据待补）；ACL `N18-4013`＝arXiv `1804.06028`。来源/摘要[A](https://aclanthology.org/N18-4013/)；[全文](https://aclanthology.org/N18-4013.pdf)。
- **信号/方式**：前缀算术的终局答案监督；诊断隐树合并策略而非提供训练解析树。
- **对假说作用**：作者称当时领先隐树模型无法学会必要结构、低于序列RNN；结构确有价值也不保证弱终局信号能发现。仅针对当时模型和合成考场，不可说所有隐树后来均失败。
- **精读问题**：长度外推、训练分布、已知正确树上界及超参搜索是否匹配；失败来自梯度估计、表达结构还是探索？

### R2-008 — Unsupervised Latent Tree Induction with Deep Inside-Outside Recursive Auto-Encoders — ★
- **身份**：2019 NAACL；Andrew Drozdov、Patrick Verga、Mohit Yadav、Mohit Iyyer、Andrew McCallum；ACL `N19-1116`。来源/摘要[A](https://aclanthology.org/N19-1116/)；[全文](https://aclanthology.org/N19-1116.pdf)。方法DIORA（深层内外递归自编码：以其它位置预测当前词并诱导树）。
- **信号/方式**：给定句子其它词预测每个词；动态规划考虑所有二叉树，推理用CKY（图表式最优二叉解析算法）取树；无解析标签。
- **对假说作用**：重建/遮罩预测与任务终局监督的竞争机制；“autoencoder”未必是原句经单槽再逐字恢复。
- **精读问题**：排除自词泄漏的内外通道、重建损失、训练软树与测试硬树差、计算复杂度；用任务分数还是树F值选检查点？

### R2-009 — Learning to Merge Tokens in Vision Transformers
- **身份**：2022；Cedric Renggli、André Susano Pinto、Neil Houlsby、Basil Mustafa、Joan Puigcerver、Carlos Riquelme（原站题名结果及公开引文）；arXiv `2202.12015v1`。来源/摘要[A](https://arxiv.org/abs/2202.12015)；[全文](https://arxiv.org/pdf/2202.12015)。方法PatchMerger（块合并器：在相邻编码层间减少表示数）。
- **信号/方式**：上游/下游训练适配，学习层间合并；摘要没有逐项给损失，不能补成“重建训练”。
- **对假说作用**：2022已有学得合并模块，和旧C24的无训练匹配对照；重要区别是内容映射可学，而非语义边界已被证明。
- **待查**：可学查询/池化权重、全局或局部合并、同骨干微调预算、大小模型胜负；“matching performance”是否有等效性检验？

### R2-010 — Learning to Merge Tokens via Decoupled Embedding for Efficient Vision Transformers — ★
- **身份**：2024；Dong Hoon Lee、Seunghoon Hong（原始检索引文）；arXiv `2412.10569`，NeurIPS 2024正式版关联见原始搜索，全文版本需锁定。来源/摘要[A](https://arxiv.org/abs/2412.10569)；[全文](https://arxiv.org/pdf/2412.10569)。方法DTEM（解耦合并嵌入：专门为合并学习相似度表示）。
- **信号/方式**：连续松弛合并给专用嵌入梯度；模块式只学合并嵌入，或微调整体端到端。具体损失组成待全文。
- **对假说作用**：**直接补“学策略特征 vs 骨干适应规则”缺口**；表示同时服务编码与合并可能互相牵制，训练合并不能简单以全解冻一项代表。
- **精读问题**：冻结/联合是否同总算量、同合并率；松弛温度、硬匹配测试差、编码特征与专用特征互换手术及蒸馏项是否独立？

### R2-011 — Efficient Transformer Adaptation with Soft Token Merging — ★
- **身份**：2024 CVPR Workshops（非主会）；Xin Yuan、Hongliang Fei、Jinoo Baek；CVF官方URL为稳定入口，pp.3658–3668。来源/摘要[A](https://openaccess.thecvf.com/content/CVPR2024W/ELVM/html/Yuan_Efficient_Transformer_Adaptation_with_Soft_Token_Merging_CVPRW_2024_paper.html)；[全文](https://openaccess.thecvf.com/content/CVPR2024W/ELVM/papers/Yuan_Efficient_Transformer_Adaptation_with_Soft_Token_Merging_CVPRW_2024_paper.pdf)。
- **信号/方式**：端到端可微软合并，加入token inflation（单元回展：把压缩结果映射回较密表示以适配不同层）；摘要未完整列任务损失，不据搜索片段补成唯一信号。
- **对假说作用**：视觉、语言及视文跨模态适配；回展可影响算子和分布，不能把胜负全归“多粒度保信息”。
- **精读问题**：回展有无读原始旁路、是否只还原形状；去回展/换均值/冻结骨干的同率消融；软矩阵额外训练和推理成本。

### R2-012 — Efficient Vision Transformer via Token Merger — ★
- **身份**：2023 IEEE TIP 32，首页4156；Zhanzhou Feng、Shiliang Zhang；稳定来源为作者公开正式PDF（DOI提取未给全，待补）。摘要及定向正文[A+S](https://www.jdl.link/doc/2011/20231127_t-ip2.pdf)；同链接为全文入口。
- **信号/方式**：**定向读§III.C–D/§IV.C（印刷4160–4163）**：分类损失＋计算上限正则＋输入特征重建；元单元门用Gumbel-Softmax（随机可微松弛）训练；先学250轮，再以固定合并率微调50轮，人工率比较为300轮从零训练。
- **对假说作用**：本轮最直接补“重建是否帮合并/比率是否可学/阶段是否混杂”的旧作。§IV.C明确过大的重建权重可能伤分类；不可把辅助重建一概当无害信息保持。
- **精读问题**：Table I/II与Fig.8的准确数值（本轮未逐图提取）和同计算预算；注意**率学完在微调/推理固定**，不能误写逐输入动态率；重建最近邻距离是否掩盖少数重要异常，何处有无原始细节旁路？

### R2-013 — 基于新词发现的跨领域中文分词方法 — ★
- **身份**：2022，《电子与信息学报》44(9)，DOI `10.11999/JEIT210675`；张军等（搜索作者全表存在OCR歧义，仅首作者可靠，不强填）。中文原刊摘要[A](https://jeit.ac.cn/cn/article/doi/10.11999/JEIT210675?viewType=HTML)；[全文](https://jeit.ac.cn/cn/article/pdf/preview/10.11999/JEIT210675.pdf)。
- **信号/方式**：向量增强互信息、加权邻接熵发现新词；自动标注目标域语料，再用对抗训练处理噪声/域差，迁移新闻到医疗/专利/小说。不是端到端任务梯度直接决定每个边界。
- **对假说作用**：中文实际源入口补偏；统计教师→伪标签→网络的多阶段组合，反例焦点是“统计初筛不完美如何传播噪声”。原文参考链带出R2-024，不把中文报道同作重复计数。
- **精读问题**：新词统计和对抗训练各自消融、目标域标签权限、自动标注噪声与OOV（未登录词）率；重训练成本和新闻/专业域学习信号是否改变？

### R2-014 — Efficient Unsupervised Sentence Compression by Fine-tuning Transformers with Reinforcement Learning — ★
- **身份**：2022 ACL；Demian Gholipour Ghalandari、Chris Hokamp、Georgiana Ifrim（原始搜索作者栏）；ACL `2022.acl-long.90`＝arXiv `2205.08221`。来源/摘要[A](https://aclanthology.org/2022.acl-long.90/)；[全文](https://aclanthology.org/2022.acl-long.90.pdf)。
- **信号/方式**：无需金标压缩对，定制目标奖励；把保留/删除作为二值序列标注，用策略梯度微调预训练Transformer。
- **对假说作用**：任务奖励型压缩早于LLM提示压缩；“unsupervised”只是无压缩配对标签，不等于无预训练知识、无人工奖励设计或无评测调参。
- **精读问题**：奖励中语义保持/流畅/长度各项、奖励模型来源、训练采样方差；与测试时离散搜索比较是否把训练花费转到离线，同率质量-速度曲线如何？

### R2-015 — Unsupervised Sentence Compression using Denoising Auto-Encoders
- **身份**：2018 CoNLL；Thibault Fevry、Jason Phang（原始搜索作者栏）；ACL `K18-1040`＝arXiv `1809.02669`。来源/摘要[A](https://aclanthology.org/K18-1040/)；[全文](https://aclanthology.org/K18-1040.pdf)。
- **信号/方式**：人为加噪扩长句子，训练去噪恢复原句，不需原句/压缩句配对。
- **对假说作用**：重建信号靠损坏分布形成“压缩偏好”，不是重建本身自动学会删冗余；摘要明说自动ROUGE落后监督模型，而人工语法/意义评价可比，提供评价目标分歧。
- **待查**：噪声类型、长度控制、重建时可见信息和复制捷径；人工评分是否同输出长度（配R2-032），何种细节删除失败？

### R2-016 — Learning to Discover, Ground and Use Words with Segmental Neural Language Models — ★
- **身份**：2018预印本/2019 ACL；Kazuya Kawakami、Chris Dyer、Phil Blunsom；arXiv `1811.09353v2`＝ACL `P19-1645`。来源/摘要[A](https://arxiv.org/abs/1811.09353)；[全文](https://aclanthology.org/P19-1645.pdf)。
- **信号/方式**：联合词发现、句子预测与可选视觉条件；未切分字符序列中的词是潜变量，而非独立分词预处理。
- **对假说作用**：非语言模态提供的学习来源可改善边界/预测，是多源监督的历史入口；不能称图像条件本身就是词边界教师。
- **精读问题**：记忆/长度正则有无配套对照、图像条件增益是否只是额外信息；同预测损失、同字符预算下词界与任务效用的关联，边缘化成本。

### R2-017 — Segmental Recurrent Neural Networks — ★
- **身份**：2015预印本、2016修订；Lingpeng Kong、Chris Dyer、Noah A. Smith（原始检索引文）；arXiv `1511.06018v2`。来源/摘要[A](https://arxiv.org/abs/1511.06018)；[全文](https://arxiv.org/pdf/1511.06018v2)。
- **信号/方式**：显式段嵌入＋半马尔可夫条件随机场（对变长连续片段联合打分的概率模型）；支持完全监督段界/段标签，也支持仅标签、段界潜在的部分监督。
- **对假说作用**：段界是否观测与段表示是否可学可独立变化；中文分词/词性与手写识别为同模型内不同监督设置的入口。
- **精读问题**：边界边缘化如何求导、最大段长和双向可见性；完全/部分监督是否相同数据与目标，结构归纳先验与标签信号能否分离？

### R2-018 — Unsupervised Discovery of Morphemes — ★
- **身份**：2002 ACL形态/音韵学习工作坊；Mathias Creutz、Krista Lagus（原始检索元数据）；arXiv `cs/0205057v1`＝ACL `W02-0603`。来源/摘要[A](https://arxiv.org/abs/cs/0205057)；[全文](https://aclanthology.org/W02-0603.pdf)。官方ACL页提取仅页脚，摘要由原始arXiv核验。
- **信号/方式**：最小描述长度（同时压缩词典与语料表示的准则，简称MDL）在线优化；另一方法最大似然。芬兰语、英语验证。
- **对假说作用**：不是所有“学习分段”都需下游奖励、梯度或教师；提供先验/码长目标与现代预测损失的对照，词素不是字节块任务效用标准。
- **精读问题**：模型码长和数据码长如何平衡，在线/离线、MDL/似然是否同词典容量，稀有词过分切割与下游性能是否背离？

### R2-019 — Unsupervised Learning of Word Boundary with Description Length Gain
- **身份**：1999 CoNLL；Chunyu Kit、Yorick Wilks；ACL `W99-0701`。作者机构摘要[A](https://scholars.cityu.edu.hk/en/publications/unsupervised-learning-of-word-boundary-with-description-length-ga/)；[全文](https://aclanthology.org/W99-0701.pdf)。ACL网页仅页脚、PDF返回不可读字节流，未当摘要；由CityU机构记录完成身份/摘要核验。
- **信号/方式**：描述长度增益（用某片段做单元后减少的编码长度）作优度，寻找各段增益和最大的分段；不是终局任务监督。
- **对假说作用**：明确补1990年代压缩准则→词界的谱系；语料可压缩与人类词汇对应是经验关系，不是保证任意任务充分。
- **待查**：词典代价/重复计数、贪心与全局求解、与频率/熵及随机切分的预算公平性；无法读取正式PDF正文仍是下一轮访问缺口。

### R2-020 — DiffRate: Differentiable Compression Rate for Efficient Vision Transformers — ★
- **身份**：2023；Mengzhao Chen等（原始检索PDF作者栏）；arXiv `2305.17997v1`。来源/摘要[A](https://arxiv.org/abs/2305.17997)；[全文](https://arxiv.org/pdf/2305.17997)。正式发表轨道待编目补核，不把搜索引文自动当已核终稿。
- **信号/方式**：损失梯度传到每层压缩率，联合丢弃和合并；具体代理、任务/预算损失待原文。
- **对假说作用**：学习**层级预算**而不只是学习配对；摘要“无需fine-tuning”指应用已学率时，不代表获得率不需训练。
- **精读问题**：率是全局可学参数还是每输入自适应，学习率的模型/数据成本；固定率同预算、只丢/只并/混合是否分开，同实际速度下结论是否仍在？

### R2-021 — Learning to Compose Task-Specific Tree Structures — ★
- **身份**：2017预印本/2018 AAAI关联；Jihun Choi、Kang Min Yoo、Sang-goo Lee（原始检索正式引用）；arXiv `1707.02786v4`。来源/摘要[A](https://arxiv.org/abs/1707.02786)；[全文](https://arxiv.org/pdf/1707.02786v4)。
- **信号/方式**：自然语言推断/情感任务反馈；Gumbel Tree-LSTM以直通随机松弛估计器选父节点并为离散决策计算梯度。
- **对假说作用**：典型任务驱动层级合并；与R2-026离散强化、R2-008重建及R2-006/007反例连读，不用任务分数高推出语法稳定。
- **精读问题**：直通梯度偏差、温度、候选合并位置、同率/同结构深度消融；标签任务捷径是否使树可任意，重启结构与性能是否同步？

### R2-022 — Unsupervised Tokenization Learning
- **身份**：2022 EMNLP；Anton Kolonin（原始检索PDF）；ACL `2022.emnlp-main.239`。来源/摘要[A](https://aclanthology.org/2022.emnlp-main.239/)；[全文](https://aclanthology.org/2022.emnlp-main.239.pdf)。
- **信号/方式**：统计转移自由度（作者命名的转移选择丰富程度指标，确切公式待全文）及其导数/方差/峰值变体；非神经统计学习。
- **对假说作用**：摘要称不同语言要不同指标变体、更多语料未必更好、去弱统计证据反而改善；给“越多统计知识越好”与通用熵教师假说负向限定。
- **待查**：各语言选择规则是否偷看测试边界、数据量/词典和调参预算；与互信息/条件概率对照是否一致，指标不能望文生义作数学结论。

### R2-023 — Segment First or Comprehend First? Explore the Limit of Unsupervised Word Segmentation with Large Language Models
- **身份**：2025；作者待补，不以提交人填作者；arXiv `2505.19631v1`。来源/摘要[A](https://arxiv.org/abs/2505.19631)；[全文](https://arxiv.org/pdf/2505.19631)。
- **信号/方式**：预训练LLM提示分词；LLACA把LLM知识与Aho–Corasick（多模式字符串匹配自动机）及动态n元模型结合。
- **对假说作用**：教师/预训练隐知识来源不是无信息先验；“无监督”标签须交代预训练语料、提示和评测调参。为中文分词的现代教师蒸馏补入口，不背书其“极限”。
- **待查**：LLM标注究竟训练什么、规则/教师贡献和调用成本、语料污染，多语言分段标准是否统一；评测语义理解不能只以词F值替代。

### R2-024 — Unsupervised multi-granular Chinese word segmentation and term discovery via graph partition
- **身份**：2020，《Journal of Biomedical Informatics》110:103542；Zheng Yuan等；DOI `10.1016/j.jbi.2020.103542`，PMID `32853795`。来源/摘要[A](https://pubmed.ncbi.nlm.nih.gov/32853795/)；[出版方全文入口](https://www.sciencedirect.com/science/article/pii/S1532046420301702)。由R2-013中文原刊参考链发现，英文发表，不冒充中文正文。
- **信号/方式**：n元统计给图边权、比率割与动态规划分段，改划分数得到多粒度；生成样本训练BERT判别器验证词边界。
- **对假说作用**：**2020已有统计多粒度分段＋生成伪标签边界核验**，但并非模型内部多尺度来源回访。多粒度改善术语发现，不等于改善未知未来任务。
- **待查**：生成样本规则、专家知识/字典是否进入训练，多粒度相对只粗/只细是否同候选数/审核预算；医学术语发现对一般语言模型的适用边界。

### R2-025 — Inducing Meaningful Units from Character Sequences with Dynamic Capacity Slot Attention
- **身份**：2021首发、2024 v3；作者待补；arXiv `2102.01223`。来源/摘要[A](https://arxiv.org/abs/2102.01223)；[全文](https://arxiv.org/pdf/2102.01223)。
- **信号/方式**：无监督分布式学习，动态容量槽（可变数量汇总表示）归纳字符序列对象；摘要明确**不是直接分段**，以前向/反向探针评价。
- **对假说作用**：拆开“发现有意义单元”和“显式段界”假说；探针能恢复不等于部署读者消费，跨语种单元也不当然是语言学词。
- **待查**：训练损失、槽数控制和探针强度、输入来源对应、聚合跨位置是否保持顺序；与显式分段同存储/计算预算是否存在。

### R2-026 — Learning to Compose Words into Sentences with Reinforcement Learning — ★
- **身份**：2016预印本/ICLR 2017引用关联；Dani Yogatama、Phil Blunsom、Chris Dyer、Edward Grefenstette、Wang Ling（原始搜索引文）；arXiv `1611.09100v1`。来源/摘要[A](https://arxiv.org/abs/1611.09100)；[全文](https://arxiv.org/pdf/1611.09100)。
- **信号/方式**：下游任务反馈，用强化学习学树形句子表示与组合顺序；不提供解析树监督。
- **对假说作用**：离散任务策略历史起点，与R2-021松弛梯度、R2-008重建预测组成信号/方式二维对照；摘要已承认树与常规英语语法不同。
- **精读问题**：回报、方差基线、预训练与交替步骤，组合算子/策略是否联合；任务泛化和解析稳定性，复核R2-006比较是否同实现。

### R2-027 — Improving Chinese Word Segmentation with Wordhood Memory Networks
- **身份**：2020 ACL；Yuanhe Tian、Yan Song、Fei Xia、Tong Zhang、Yonggang Wang；ACL `2020.acl-main.734`，官方页列v1/v2。来源/摘要[A](https://aclanthology.org/2020.acl-main.734/)；[全文](https://aclanthology.org/2020.acl-main.734.pdf)。中文机制查询先得到中文报道，再用官方摘要确认，不计报道为另一作品。
- **信号/方式**：成词性统计作为记忆特征加入不同编码/解码分词器；具体统计监督和标签训练须全文区分。
- **对假说作用**：不是“统计或神经”二选一；可检验统计教师作为软特征而非硬边界标签能否缓冲域外错误。此“memory”不是长上下文原文档案。
- **待查**：成词指标如何构建、目标域未标注数据权限、记忆特征/模型容量/外部语料分别消融，v1/v2更改内容。

### R2-028 — Nonparametric Bayesian Semi-supervised Word Segmentation — ★
- **身份**：2017 TACL；Ryo Fujii、Ryo Domoto、Daichi Mochihashi（原始搜索作者PDF）；ACL `Q17-1013`，正式期刊页另有同题。来源/摘要[A](https://aclanthology.org/Q17-1013/)；[全文](https://aclanthology.org/Q17-1013.pdf)。
- **信号/方式**：大量未标注文本的非参数贝叶斯词发现＋已有标签的CRF（条件随机场：按条件概率联合标注序列）约束，生成/判别透明交换信息的半监督框架。
- **对假说作用**：数据驱动自然边界与人工规范不一致时不是只能弃用其一；日语/中文/泰语社交文本提供非英语实证入口。
- **精读问题**：交替更新/伪标签流程和冻结步、数据规模、公平基线；词概率与标签之间的信息转换、输入级未来可见性。下面日文稿不能未消歧就当本作第二次独立证据。

### R2-029 — Sentence Compression by Deletion with LSTMs — ★
- **身份**：2015 EMNLP；Katja Filippova、Enrique Alfonseca、Carlos A. Colmenares、Lukasz Kaiser、Oriol Vinyals；ACL `D15-1042`。身份[元数据](https://aclanthology.org/D15-1042/)；摘要和定向正文[A+S](https://aclanthology.org/D15-1042.pdf)；同链接全文。
- **信号/方式**：新闻中自动抽取的约两百万原句—压缩句配对，监督训练保留/删除序列；不是只因训练数据自动取得就无监督。
- **对假说作用**：**定向读§4/§5（印刷362–367）**：同量训练数据的语法特征基线、基本LSTM和加语法版本；作者报告语法特征未提供收益、模型会学训练压缩率而过删“几乎无可删”的句子。负面原因是作者解释，不是已做因果分离。
- **精读问题**：训练对自动抽取是否注入树剪枝偏好；长度先验/语法辅助/模型容量是否混杂，人工评判和自动单参考评分的胜负为何不同；同压缩率须配R2-032。

### R2-030 — Query-focused Sentence Compression in Linear Time
- **身份**：2019 EMNLP-IJCNLP；作者全表待补（原始搜索见A. Handler）；ACL `D19-1612`＝arXiv `1904.09051`。来源/摘要[A](https://aclanthology.org/D19-1612/)；[全文](https://aclanthology.org/D19-1612.pdf)。
- **信号/方式**：必须保留查询词、满足显示长度的约束压缩；转移式方法在依存树上生长子图，训练信号/算法细节摘要不足。
- **对假说作用**：查询条件压缩和长度约束早有可执行框架，不能以“问题决定保留”作宽泛新颖性；词面强制保留也不等于未知语义证据覆盖。
- **待查**：训练标签、动作合法性、硬词约束、是否学到优化策略还是规则；与整数规划同率/同约束真实延迟及失败句型。

### R2-031 — Grammar Induction with Neural Language Models: An Unusual Replication — ★
- **身份**：2018；Phu Mon Htut、Kyunghyun Cho、Samuel Bowman（原始搜索正式记录）；arXiv `1808.10000`＝EMNLP `D18-1544`，BlackboxNLP短稿`W18-5452`有同题/同作者线索，本轮**不另计**，由总编目消歧扩展差异。来源/摘要[A](https://arxiv.org/abs/1808.10000)；[全文](https://aclanthology.org/D18-1544.pdf)。
- **信号/方式**：复核语言模型目标下的隐树归纳，排除原研究近似测试集调参/训练问题并扩两个数据集。
- **对假说作用**：不是一边倒的负面：作者发现原评测有问题，但公平重测仍支持所测模型优于既有隐树基线。与R2-006/007构成**负面也需校准**的反向证据；不能仅凭方法会泄漏就裁其所有结果无效。
- **精读问题**：泄漏发生在哪个阶段、修复后如何划分/选模型；结构监督与语言模型目标是否真无标签，训练语料/树评测重复，复核成功的精确条件。

### R2-032 — Evaluating Sentence Compression: Pitfalls and Suggested Remedies — ★
- **身份**：2011单语文本生成工作坊；Courtney Napoles、Benjamin Van Durme、Chris Callison-Burch；ACL `W11-1611`。身份[官方页](https://aclanthology.org/W11-1611/)；摘要及定向正文[A+S](https://www.cis.upenn.edu/~ccb/publications/evaluating-sentence-compression-pitfalls-and-suggested-remedies.pdf)；[正式全文](https://aclanthology.org/W11-1611.pdf)。
- **信号/方式**：评价方法研究，非新训练器；比较不同压缩率时的自动/人工评价。
- **对假说作用**：**定向读§3/§4**：作者展示压缩率强预测质量、较长输出可能造成假优势；统一长度后数值排序可反转，但该比较**未显著**，不能升级成模型确定胜负。这个经典反例直接约束“学习策略更好”的证据门槛。
- **精读问题**：相同率控制的方法、人工评分是否见原句、单参考指标偏差、语义/语法两个维度。不要把文本句长的结论不带条件迁移为固定总位数潜表示定理。

## 3. 日文来源补充：取得原文，但不增加作品数

**题名**：条件付確率場とベイズ階層言語モデルの統合による半教師あり形態素解析。中文释义：整合条件随机场与贝叶斯层级语言模型的半监督形态分析。作者：持橋大地、鈴木潤、藤野昭典（原文作者栏）。[作者机构公开PDF](https://www.ism.ac.jp/~daichi/paper/nlp2011semiseg.pdf)。文件名含2011，**完整正式会议信息尚未核验**，因此本轮只作来源线索与定向正文笔记，不按新有效作品计。

实际定向读§1、§3、§4.3与§5的叙述：

- §1作者明确说明无监督语言模型最优化与人工分段规范有时不同，也会分开活用词尾、对低频词较弱；这不是英文摘要的转译推测。
- §3讨论固定一类参数更新另一类参数的交替学习，生成/判别模型“互教”；§4.3说明稀疏高阶模型的不稳定会压低其权重，给定标注分段作先验，并在测试时使用附加伪标签后重训的独立CRF。
- §4.3称直接把语言模型概率加入未知数据解码常因波动反而恶化。**训练时组合有益不等于部署时所有模型输出都应直连**，这是阶段方式与信号相容性的具体负向追查点。

这些仅是定向阅读的作者叙述，数值表未读全、公式抽取有断裂，不引精确百分比为已核结论。它与R2-028的作者/方法谱系相近但不同，是否先期/替代/独立作品未消歧，下一轮由编目先核；不能把日文版和英文扩展当两次独立验证。

## 4. 本专题元数据补查（不改原卡或共享表）

| 既有对象 | R2核销证据 | 应如何给下一轮使用 |
|---|---|---|
| C30/W0030 LapMerge | 本轮实际打开[2610.13858v2](https://arxiv.org/abs/2610.13858v2)，明确v1 2026-10-09、v2 2026-10-12，与发现审计A02一致 | **身份版本冲突可核销，锁v2**；全文版本差异仍未读。六位作者全表可复用`DISCOVERY_AUDIT_R1.md`A02原始身份记录，不能再写该字段完全未知，也不能声称本轮独立重核作者栏 |
| C12/W0012 SOMBRERO | 复用发现审计A01：Pit Neitemeier、Alessio Serra、Jiaze Li、Sascha Wirges、Lukas Balles、Jan Hendrik Metzen；v1 2026-01-30 | 身份作者可供编目回填，复用来源/日期透明，不增加论文数，不把审计摘要复核说成本轮全文 |
| C50/W0050 Evaluating Compressed Memory | 复用发现审计A03：Minsu Oh、Seunghui Jwa、Chanjun Park、Yeo-Chan Yoon；v1 2026-10-14 | 同上；精读红队关于PARTIAL状态仍有效，不据补作者升级FULL |
| C31/W0031 QuickMerge++ | 本轮重取[摘要页](https://arxiv.org/abs/2508.13204)仍给v1摘要/投稿史，提取无撤回评论 | **状态仍未确认**；原列表相邻撤回片段不当本作事实，不重打列表，不写“已撤回”或“性能已认证” |
| C45/W0045 PISCO | 沿用首轮实际取回的预印本48h/正式版24h冲突；本轮未重取训练正文 | 需下一轮锁正式版训练设置后解释，不能挑更优数、不重复计数、不标已经核销 |
| 其它审计修订 | W0059/W0091/W0311/W0169/Merlin/ByT5的数学、统计、实现修订不属于本轮T01新增发现写作权限 | 不改卡；本轮引用这些红队仅作为证据强度约束，原负责人负责回写 |

## 5. 给terra的优先读法与假说分叉

21个★不是又一独立作品统计，而是本轮32项的子集。建议先取下列能改变解释的对照，再沿参考链扩展：

| 争议 | 新入口 | 关键对照/读出 | 对研究选择的影响 |
|---|---|---|---|
| 预测好能否等价于边界对 | R2-001/002/005/016/022 | 相同语料下预测、词界、人类规范三指标；长度先验与双向权限 | 若目标分歧明显，不以熵/预测损失一项给分段定“语义正确” |
| 只用终局任务是否学得可靠结构 | R2-006/007/021/026/031 | 同代码重启、已知真树上界、随机/平衡树、语言建模目标 | 若结构不稳但任务好，先研究可用压缩，不把可视化树当多级语义证据 |
| 重建何时有益/有毒 | R2-008/012/015/029 | 重建对象、辅助权重、损坏分布、下游指标与同率 | 若大权重压坏主任务，优先隔离梯度/阶段而非盲加重建目标 |
| 学到的到底是策略还是适配 | R2-009/010/011/020 | 只训合并嵌入/只训率/冻结骨干/全联合；实时时间与总训练预算 | 若模块式有效，没必要一开始全解冻；若只全联合有效，须防骨干补偿被归因策略 |
| 标签从哪里来，分阶段是否必要 | R2-013/014/017/018/028/029 | 统计伪标签、人工标签、自动平行对、奖励模型成本，联合/交替/固定率适配 | “无监督”须按实际权限重命名，不以类别标签直接选架构 |
| 多粒度收益还是多候选收益 | R2-024/025 | 相同候选数/表示字节/审核预算的单粒度 vs 多粒度 | 若只是多存/多试，不把其当粒度独立效应 |
| 公平评价是否改变胜负 | R2-032并读所有压缩器 | 同压缩率、全成本、评分是否见源、单/多参考 | 若长度/评价解释多数增益，先修评价，不追更复杂策略 |

**不建议本轮立新训练臂。** 最便宜动作是从旧经典和模块式合并论文取真正同码消融；目前“所有信号×所有梯度方式×联合/阶段”仍没有统一公平矩阵。新增多语分词不是字节来源回访证据，非树字符槽也不是源存活与读取机制。T01阶段仍值得定向深入，但新增32项已足以把下一步从堆2026名字转到可证伪的目标/训练方式比较。

## 6. 仍待补与未计数

- AAAI经典句压`Statistics-Based Summarization—Step One: Sentence Compression`官方URL返回题名作者相符、**摘要却是歧义保留文本生成**；本轮不以错配摘要确认，不纳入32项。需下轮取得原PDF或可信出版元数据，不能传播该摘要。
- 中文“融合语法信息的句子压缩”网页取回为出版社主页，未得作品正文/摘要，不纳入。
- 金标/测试集调参、语言模型预测与人工词界/任务收益的关系，仍需全文表格，不据摘要排名。
- 日文稿正式书目及与2017作关系、32项作者全表/部分正式版DOI待统一编目。记录为缺口而不是用联系人补齐。
- 本轮没有新增语音/导航全谱系；红队§6允许暂缓所有语音视频变体，优先能分离学习来源者。后续若T01关键对照仍缺，再从SRNN/DIORA/DTEM参考链定向追。

## 7. 静态验收

**PASS**：本地只读Python确认32个新ID连续、21★、必要字段齐备、32行查询/44行Fetch账连续、UTF-8替代字符0。32个核心题名、自动提取的31个arXiv/ACL标识与41条人工整理的别名/DOI/题名补查，在当前CATALOG均0重复。目录并发从初读384变385实体后已重做去重；共享表变化非本代理，未回写。

`git status --short`仍为原有未跟踪父目录/草案/bundle格局，无跟踪源码改动。本轮仅新建本文与`SEARCH_LOG_R2.md`，旧三个T01文件和旧编号未改；未下载权重、未生成脚本/测试产物、未训练/提交/另派代理。具体快照散列和一次校验命令修正见日志§6。
