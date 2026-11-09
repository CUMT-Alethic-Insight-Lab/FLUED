# T07 扩展 R2：非可加效用、闭环反事实与成本敏感获取的经典桥接

日期：2026-11-08。角色：发现／摘要层初筛，非terra全文精读。依据上层PLAN及 `05_review/READING_AUDIT_R1.md`、`COVERAGE_AUDIT_R1.md` 定向补洞。所有新内容仅写T07目录，不修改总目录、源码、原证据或他人阅读卡。

## 0. 实计、去重与红队约束

- **新增33个有效作品实体：T07-056–088；身份与摘要／作者机构介绍核验33；精读优先20；全文精读0、代码核验0、复现0。** 其中32项论文／综述，1项博士论文（085）。专题R1已有55项，本专题本地两轮合计88项；这不是全局目录已增加33或已验收88项结论。
- 新增项与 `02_catalog/CATALOG.md` 的384实体快照按原生ID、DOI、正式题名及主要别名只读比对，无命中；不自行分配W-ID。正式版／预印本合并，Nan两高度重叠预印本保守合为一个待消歧簇，Shim异名预印本／正式版同计1。所有比较以本轮读取快照为准，其他代理并发扩展仍需总目录负责人二次归并。
- 阅读深度：`A`为摘要／官方介绍初筛；`M`为原始元数据补核。Howard使用ADS所载原文摘要并辅以IEEE身份页，明确不是直接取得正式全文；博士论文依据作者机构页面介绍。个别页面返回整篇文本，本轮只消费题名、摘要和明确注明的开头片段，不因此计全文精读。
- 非英语入口已实际执行：**中文6次（含1次429及其一次重试）、日文2次、法文1次**；其余英文36次。有效新增含中文原刊综述1、日文原刊综述1、法国作者机构法文论文介绍1；翻译聚合页不当独立作品，不声称消除了语言／渠道偏差。
- 访问与失败逐条见 `SEARCH_LOG_R2.md`：45次WebSearch（44成功、1次429），47次FetchURL（45返回文本、2错误）；其中标题空壳／无摘要页明确不算核验通过。浏览器仅补核J-STAGE身份，使用后关闭自建1页，未动其他会话标签。

### W0311／W0059：本扩展的强制引用隔离

本轮**不以W0311的精确最优值、贪心闭式、线性增长率或最坏值为理论基础**；已有红队指出Case B文字与递归不一致、最优性下界尚未核准。不以“未证最优”升级成“最优值已被证伪”。R1 `CANDIDATES.md` 对T07-011的摘要介绍只能作历史发现记录；本文件和红队限制优先于将其提升为已核理论的任何解读。

本轮**不引用W0059有反例的均方误差投影步骤、二值失真断言或据此延伸的率失真适用性**。也不把这些局部问题误杀其对数损失主定理；本轮不新增关于该主定理正确性的裁定。R2的经典理论桥接不依赖W0059。

已执行勘误线索查询 `"AFABench" "erratum" "CUBE-NM"`，未找到明确作者更正，返回普通作品／仓库／学位论文。不把没有搜到勘误解释为从未更正，也不替作者修公式。W0311正式版及原型精确枚举、W0059修订／后续争议仍交原terra负责人。W0091等其他红队限制同样保留，不通过换引文洗掉适用条件问题。

## 1. 扩展带来的决策变化（初筛推断）

1. **非可加不是2026新基准才出现的现象。** Howard 1966摘要已明确联合消除独立因素不确定性的价值可不等于单项之和（056）；Lindley 1956把求知识的实验信息量与决策比较区分（057）；Chen与Waggoner给决策问题中的信息替代／互补正式入口（063）。这些入口降低对W0311争议常数的依赖，但定理适用条件仍需terra核验。
2. **非短视、闭环和模型训练成本是三根轴。** 060区分预先选集合与依观察值改变后续动作的条件计划；076／077处理策略引起的状态分布变化；082区分获取不改变特征本身与历史获取无隐藏混杂。不能以一个“反事实”词代替这些条件。
3. **无偏评价器不等于安全的策略学习目标。** 081官方摘要直接指出复杂策略类中的倾向过拟合；080指出自适应采样均值在一定规则下可系统负偏；078的效率结果利用马尔可夫无记忆结构。策略挑选、重复校准和同卷选优应与一次固定策略评估分开。
4. **“取得更多就更好”“最优就一定停止”均有边界。** 061摘要给出最优计算策略不保证所有轨迹都结束的反例；065在允许不检查就选时不再有普遍简单排序最优规则。它们不能自动否定有限预算系统，却能阻止无条件停止／排序承诺。
5. **出现一个需立即前移的近期最近邻：087 DeepControl。** 官方摘要直接写状态相关信息边际价值、检索继续与细节分辨率两轴、层级粒度控制及训练期退火控制强制。不能继续以“效用学习＋停止＋粒度”组合本身作未有先例；尚未确认其等于严格闭环总效应或可回访细源接口，必须全文对照而非摘要背书。
6. **中文检索不是英文预印本翻译的另一个计数口。** 083原刊覆盖代价定义及经典引文，084日文综述以真实临床成本和反向归纳连接样本量／停止，085法文机构介绍公开承认增加训练复杂度。它们是桥接入口，不是直接证明多粒度语言系统有效。

## 2. 33项新增作品卡

“支持／反例潜力”仅表示下一轮值得核查的用途；摘要中的数学或经验声称均不等于本轮独立核定。全文入口是可追踪地址，不表示已下载或精读。

### T07-056 — Information Value Theory — 精读优先
- 身份：Ronald A. Howard；1966；IEEE Transactions on Systems Science and Cybernetics 2(1):22–26；DOI `10.1109/TSSC.1966.300074`。[IEEE身份页](https://ieeexplore.ieee.org/document/4082064/)；[ADS原摘要](https://ui.adsabs.harvard.edu/abs/1966ITSSC...2...22H/abstract)。全文入口：[DOI](https://doi.org/10.1109/TSSC.1966.300074)。深度A（ADS原文摘要；IEEE只返回题名，非全文）。
- 机制：把概率与经济后果联合起来定义信息价值，原摘要明确指出**即使因素独立，联合消除不确定性的价值也可异于分别消除的价值之和**。
- 支持／反例潜力：非可加效用的直接经典来源；不能将独立来源、互信息可分或单项评分当作可加决策价值。
- terra问题：核原文的决策者、先验、免费信息可忽略条件；给出哪类互补／替代实例？取得信息的成本和付费上限怎样进入？ADS摘要可以定位主张，最终理论引文须回正式原文。

### T07-057 — On a Measure of the Information Provided by an Experiment — 精读优先
- 身份：D. V. Lindley；1956；Annals of Mathematical Statistics 27(4):986–1005；DOI `10.1214/aoms/1177728069`。[官方摘要／全文入口](https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-27/issue-4/On-a-Measure-of-the-Information-Provided-by-an-Experiment/10.1214/aoms/1177728069.full)。A。
- 机制：基于先验的实验信息量，比较实验并联系设计；摘要最后明确应用目标是增进知识，而非作出决策。
- 支持／反例潜力：信息增益与具体行动效用的经典区别，防止把降熵自动写成答案收益。
- terra问题：信息量与期望后验／先验差的准确形式；Blackwell比较在什么意义下不同？用任务无关高熵变量能否构造“多信息零决策收益”的例子？

### T07-058 — Equivalent Comparisons of Experiments — 精读优先
- 身份：David Blackwell；1953；Annals of Mathematical Statistics 24(2):265–272；DOI `10.1214/aoms/1177729032`。[官方摘要／全文入口](https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-24/issue-2/Equivalent-Comparisons-of-Experiments/10.1214/aoms/1177729032.full)。A。非现有W0101/W0102后续论文，源头作品单独实体。
- 机制：比较实验的等价刻画，去除有限结果限制，并引入k决策问题的较弱比较。
- 支持／反例潜力：“更多信息不伤害”的适用模型需有足够决策能力及允许忽略信息；不是受限读者加上下文的保证。
- terra问题：实验、随机化、行动集合、风险顺序及可测性条件；固定解码器、访问成本、关闭动作会改后续策略时，还能引用哪个方向？不从摘要复述完整定理。

### T07-059 — Near-optimal Nonmyopic Value of Information in Graphical Models — 精读优先
- 身份：Andreas Krause、Carlos E. Guestrin；UAI 2005；2012归档arXiv `1207.1394v1`，不是2012新研究。[摘要](https://arxiv.org/abs/1207.1394)；[全文](https://arxiv.org/pdf/1207.1394v1)。A+M。
- 机制：次模结构、随机估计和样本界支持非短视变量子集选择的近似算法，并讨论近似困难度。
- 支持／反例潜力：可作老且强的简单选择基线；不能把摘要的近似因子泛化到任意相关证据或闭环动作。
- terra问题：目标是哪些隐／观测变量？条件独立如何使次模性成立？先定子集与依结果再选策略的保证是否相同？成本异质时哪个定理适用？

### T07-060 — Optimal Nonmyopic Value of Information in Graphical Models – Efficient Algorithms and Theoretical Limits — 精读优先
- 身份：Andreas Krause、Carlos Guestrin；IJCAI 2005，作品137。[官方摘要](https://ijcai.org/proceedings/2005/137)；[正式全文](https://www.ijcai.org/proceedings/2005/0137.pdf)。A，另定向消费§1对开环子集／闭环条件计划的区别；未精读其余证明。
- 机制：链图／HMM上分别求最优子集与条件计划，区分过滤与平滑；摘要同时给出推广到多树时的信息价值及条件熵计算困难。
- 支持／反例潜力：闭环信息获取已有经典精确定义；局部奖励能沿链分解不意味着所有动作效用可加。
- terra问题：链独立性、可观测节点、每轨迹硬预算条件；奖励函数类和复杂度输入规模；正式摘要中“可从链推广多树”的一句与随后困难结果存在表述张力，须以§6定理为准，不沿用抽取摘要的字面泛化。

### T07-061 — Selecting Computations: Theory and Applications — 精读优先
- 身份：Nicholas Hay、Stuart Russell、David Tolpin、Solomon Eyal Shimony；UAI 2012；arXiv `1408.2048v1`为2014归档。[摘要](https://arxiv.org/abs/1408.2048)；[全文](https://arxiv.org/pdf/1408.2048v1)。A+M。
- 机制：以贝叶斯选择而非通常赌博机回报框架分析模拟计算选择，特定场景有限采样界；摘要报告最优策略未必在所有情况下最终决策的反例。
- 支持／反例潜力：防止把最优期望回报误写成逐轨迹停止／有限尾时延保证。
- terra问题：不停止事件的概率、期望计算量与路径上界怎么区分？反例是否允许零成本或无限动作？正成本及有限预算如何改变结论？

### T07-062 — An Approximate Nonmyopic Computation for Value of Information — 精读优先
- 身份：David Heckerman、Eric J. Horvitz、Blackford Middleton；UAI 1991原稿，arXiv `1303.5720v2`（2015）；作者机构另列1993相关期刊作品，不计第二项。[归档摘要](https://arxiv.org/abs/1303.5720)；[作者机构介绍](https://www.microsoft.com/en-us/research/publication/approximate-nonmyopic-computation-value-information/?lang=ja)；[所锁全文](https://arxiv.org/pdf/1303.5720v2)。A+M；会议／期刊实质差异待terra。
- 机制：指出传统一步近似即使允许多次测试仍假定仅一次，以大样本统计构造非短视近似。
- 支持／反例潜力：是非短视获取及停止的早期直接桥接，不必依赖2026方法来证明问题存在。
- terra问题：大样本、测试独立性及候选序列选择前提？评估一组测试的近似与选择最优组的保证不能混淆；1991／1993版本差别要留表。

### T07-063 — Informational Substitutes — 精读优先
- 身份：Yiling Chen、Bo Waggoner；FOCS 2016，arXiv `1703.08636v1`为完整扩展。[摘要](https://arxiv.org/abs/1703.08636)；[FOCS入口](https://ieee-focs.org/FOCS-2016-Papers/3933a239.pdf)；[全文](https://arxiv.org/pdf/1703.08636v1)。A+M；FOCS PDF只是检索入口，未另Fetch。
- 机制：在指定决策／优化问题中定义信息替代与互补，并联系次模、几何、信息论和自适应获取近似；含正反设计结果。
- 支持／反例潜力：比仅用PID源头更直接覆盖**任务效用**而非信息量的交互；信号相同、任务损失不同可有不同互补性。
- terra问题：弱／强替代、粗化、随机化的定义是否不同？定理对哪些决策者普遍成立？零单步值而正联合值的条件与贪心失败怎么精确定位？

### T07-064 — The Price of Information in Combinatorial Optimization
- 身份：Sahil Singla；2017预印本，SODA 2018（官方元数据关联）；arXiv `1711.00405v1`。[摘要](https://arxiv.org/abs/1711.00405)；[全文](https://arxiv.org/pdf/1711.00405v1)。A+M。
- 机制：付费探测未知边成本／奖励后求树、匹配、覆盖等组合解，把探测费与终局效用共同计账，并处理探测约束／成组探测。
- 支持／反例潜力：成本并非只计最后选中的信息；探测过但没用的来源仍应付费。组合选择不同于单个最大值搜索。
- 下一步：核独立随机量、可选择未探测项与否、承诺约束、近似因子及是否能表示语言多源互补。

### T07-065 — Pandora's Problem with Nonobligatory Inspection — 精读优先
- 身份：Hedyeh Beyhaghi、Robert Kleinberg；EC 2019，arXiv `1905.01428v1`完整稿。[摘要](https://arxiv.org/abs/1905.01428)；[全文](https://arxiv.org/pdf/1905.01428v1)。A+M。
- 机制：允许不支付检查费用就直接选择某项时，原经典问题的简单排序最优性不再普遍成立；研究可高效求的承诺策略近似。
- 支持／反例潜力：把“可凭已有知识作答”作为合法选择会改变搜索问题，不可直接移植查完才选的索引规则。
- terra问题：非检查选择、奖励分布、独立性和成本条件；排序不可能的确切反例？这些结果仅对哪个策略类／时点成立？

### T07-066 — Beyond Adaptive Submodularity: Approximation Guarantees of Greedy Policy with Adaptive Submodularity Ratio — 精读优先
- 身份：Kaito Fujii、Shinsaku Sakaue；ICML 2019；PMLR97:2042–2051，关联arXiv `1904.10748`。[官方摘要](https://proceedings.mlr.press/v97/fujii19a.html)；[全文](https://proceedings.mlr.press/v97/fujii19a/fujii19a.pdf)。A。
- 机制：通过自适应次模比率拓宽贪心可保证的范围，并界定自适应差距。
- 支持／反例潜力：反向限制“不是严格次模就该放弃简单贪心”；但比率可能很小，不能只报存在一个界。
- terra问题：比率按历史、预算和策略哪个集合取下确界？能否有效估计？协同/XOR式例子比率是否退化，成本权重条件如何加入？

### T07-067 — A Knowledge-Gradient Policy for Sequential Information Collection
- 身份：Peter I. Frazier、Warren B. Powell、Savas Dayanik；2008；SIAM Journal on Control and Optimization47(5):2410–2439；DOI `10.1137/070693424`。[作者机构摘要](https://collaborate.princeton.edu/en/publications/a-knowledge-gradient-policy-for-sequential-information-collection/)；[作者全文入口](https://optimallearning.princeton.edu/Papers/FrazierPowellDayanik_KnowledgeGradientSICON.pdf)。A。
- 机制：独立正态、已知共同方差的贝叶斯排序选择中，按终局效用定义一步测量增益；单期、无穷期及某些特殊有限期最优，其余场景分析次优性。
- 支持／反例潜力：一步规则也能是理论强对照；不得把单期／极限最优改写成一般有限预算最优。
- 下一步：核样本终局价值、重复测量、噪声与独立性；检索证据的相关性／变成本对结论的影响。

### T07-068 — Integrating Learning from Examples into the Search for Diagnostic Policies — 精读优先
- 身份：Valentina Bayer-Zubek、Thomas G. Dietterich；JAIR24:263–303，2005；DOI `10.1613/jair.1512`，arXiv `1109.2127v1`归档。[官方摘要](https://jair.org/index.php/jair/article/view/10420)；[全文](https://arxiv.org/pdf/1109.2127v1)。A+M。
- 机制：以MDP／AO*搜索学习完整诊断策略，合并测量及误诊成本；同时研究从有限数据估计测试概率带来的过拟合与正则化，比较系统搜索和改进贪心。
- 支持／反例潜力：信息获取、停止、有限样本学习和训练过拟合早有一体化经典；不是只在完整已知分布中求策略。
- terra问题：训练数据是否全特征／全标签？搜索阶段概率估计是否造成自我确认？可采纳启发式的前提、剪枝成本、测试联合信息如何表示？

### T07-069 — Joint Active Feature Acquisition and Classification with Variable-Size Set Encoding
- 身份：Hajin Shim、Sung Ju Hwang、Eunho Yang；NeurIPS2018；原题预印本 **Why Pay More When You Can Pay Less: A Joint Learning Framework for Active Feature Acquisition and Classification**，arXiv `1709.05964v1`（2017）。[官方摘要](https://proceedings.neurips.cc/paper/2018/hash/e5841df2166dd424a57127423d276bbe-Abstract.html)；[正式全文](https://proceedings.neurips.cc/paper_files/paper/2018/file/e5841df2166dd424a57127423d276bbe-Paper.pdf)。A+M；异名同作合1。
- 机制：联合学习分类器与决定“停止预测／收集新特征”的RL策略，用顺序不变的集合编码表示已获取特征。
- 支持／反例潜力：学习停止不是新近LLM专属；集合编码省略顺序不等于获取策略没有顺序依赖。
- 下一步：核分类器／策略交替更新造成的目标非平稳、合成互补任务、终局回报与额外训练预算。

### T07-070 — Classification with Costly Features using Deep Reinforcement Learning
- 身份：Jaromír Janisch、Tomáš Pevný、Viliam Lisý；2017首发，AAAI2019，arXiv `1711.07364v2`（2018）。[摘要](https://arxiv.org/abs/1711.07364)；[全文](https://arxiv.org/pdf/1711.07364v2)。A+M。
- 机制：动作是请求特征或终止并分类，用神经Q学习替代先前线性近似；可调用预训练高性能分类器。
- 支持／反例潜力：明确“更多获取”与“更强读者”可能一起改变，模型切换是必须拆开的替代解释。
- 下一步：核预训练完整特征分类器的训练与运行成本、特征单价与错分罚项、停止规则的泛化。

### T07-071 — EDDI: Efficient Dynamic Discovery of High-Value Information with Partial VAE
- 身份：Chao Ma、Sebastian Tschiatschek、Konstantina Palla、Jose Miguel Hernandez-Lobato、Sebastian Nowozin、Cheng Zhang；ICML2019；PMLR97:4234–4243，关联arXiv `1809.11142`。[官方摘要](https://proceedings.mlr.press/v97/ma19c.html)；[全文](https://proceedings.mlr.press/v97/ma19c/ma19c.pdf)。A。
- 机制：部分变分自编码器处理任意观测子集，以目标变量期望信息增益选择获取，源自贝叶斯实验设计。
- 支持／反例潜力：补神经生成模型式价值估计谱系；目标信息增益不是闭环真实答案净收益，条件生成误差和采样开销不可略去。
- 下一步：核获取函数是否只看一步、完整训练矩阵假设、估计器采样次数与成本敏感版本。

### T07-072 — Active Feature Acquisition with Generative Surrogate Models
- 身份：Yang Li、Junier B. Oliva；2020首发，v2（2021），arXiv `2010.02433`；ICML2021正式关联由检索所见引文，正文版本差异待核。[摘要](https://arxiv.org/abs/2010.02433)；[全文](https://arxiv.org/pdf/2010.02433v2)。A+M。不同于现有W0305／`2006.07701`，稳定ID、题名及RL中间奖励机制均不同。
- 机制：生成代理模型刻画输入特征依赖，给获取策略中间奖励和辅助信息以缓解稀疏回报／高维动作。
- 支持／反例潜力：训练信号塑形可能更便宜，也可能优化代理而非任务效用；模型学到“有信息”不代表“对答案有用”。
- 下一步：核奖励塑形是否保持最优策略、生成器失败时的错误动作链及标签／采样账。

### T07-073 — Supervised Sequential Classification Under Budget Constraints — 精读优先
- 身份：Kirill Trapeznikov、Venkatesh Saligrama；AISTATS2013，PMLR31:581–589。[官方摘要](https://proceedings.mlr.press/v31/trapeznikov13a.html)；[全文](https://proceedings.mlr.press/v31/trapeznikov13a.pdf)。A。
- 机制：不同成本传感器／模态的逐阶段获取；每阶段选择继续或分类，把拒绝／继续决策转为监督二分类，并研究泛化界。
- 支持／反例潜力：无需通用RL也能学停止；更复杂控制器须击败这种直接监督强对照。
- terra问题：是否固定阶段顺序？预算是期望约束还是逐样本上限？继续标签需多昂贵下游评估、怎样处理后续策略改变？

### T07-074 — Adaptive Classification for Prediction Under a Budget
- 身份：Feng Nan、Venkatesh Saligrama；2017，arXiv `1705.10194v1`。[摘要](https://arxiv.org/abs/1705.10194)；[全文](https://arxiv.org/pdf/1705.10194v1)。A+M。
- 版本簇：官方admin note称与 `1704.07505`实质文字重叠；后者题名 **Dynamic Model Selection for Prediction Under a Budget**，首发2017-04-25，[已读摘要](https://arxiv.org/abs/1704.07505)。**本轮保守只计1个研究簇，目录负责人应做作品／版本归并，不假定已逐式证明两稿完全相同。**
- 机制：先训强高成本模型，再学低成本门控及预测器，在容易区域近似强模型，联合经验损失与成本约束。
- 支持／反例潜力：节省可能来自预测器／蒸馏替换，不必来自更优信息访问；教师训练与全标签数据必须计入。
- 下一步：正式版与两预印本实验重叠、门控标签生成成本、均值成本与尾部成本差异。

### T07-075 — Active Information Acquisition
- 身份：He He、Paul Mineiro、Nikos Karampatziakis；2016；arXiv `1602.02181v1`。[摘要](https://arxiv.org/abs/1602.02181)；[全文](https://arxiv.org/pdf/1602.02181v1)。A+M。注意实际作者**不是**最初查询记忆中的Daumé／Eisner，已由Atom纠正。
- 机制：在Learning to Search框架中学任务导向的动态顺序获取；情感分析／图像识别中困难样本可出现更多注意的行为。
- 支持／反例潜力：已有语言任务的获取学习桥接；无需人为训练某种注意模式不等于无需监督／rollout成本。
- 下一步：核搜索归约的专家／代价标签、动作空间、终止及数据分布匹配，不把表面注意行为当因果消费。

### T07-076 — A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning — 精读优先
- 身份：Stéphane Ross、Geoffrey J. Gordon、J. Andrew Bagnell（PMLR简记Drew Bagnell）；AISTATS2011，PMLR15:627–635，关联arXiv `1011.0686`。[官方摘要](https://proceedings.mlr.press/v15/ross11a.html)；[全文](https://proceedings.mlr.press/v15/ross11a/ross11a.pdf)。A；别名不增作者／作品。
- 机制：动作影响后续输入，单纯独立同分布监督假设失效；交互式数据聚合在学习者诱导分布下训练策略，含附加归约假设。
- 支持／反例潜力：在固定教师访问轨迹上标注效用，部署换策略后可能失准；不能认为只要DAgger就免费解决。
- terra问题：需要专家在哪些新状态给标签？每轮样本和专家调用；性能保证的损失、视界、混合策略条件；读控制器是否符合该归约？

### T07-077 — Reinforcement and Imitation Learning via Interactive No-Regret Learning — 精读优先
- 身份：Stephane Ross、J. Andrew Bagnell；2014预印本，arXiv `1406.5979v1`；官方元数据为当时投稿状态，不补猜正式录用。[摘要](https://arxiv.org/abs/1406.5979)；[全文](https://arxiv.org/pdf/1406.5979v1)。A+M。AggreVaTe相关方法归在本作品，不另计。
- 机制：把动作成本／后续成本信息纳入交互模仿学习，并连接强化学习及近似策略迭代。
- 支持／反例潜力：比只预测专家下一动作更接近终局成本敏感效用，但后续成本来自哪种策略决定估计对象。
- terra问题：cost-to-go标签如何rollout、采用专家还是学习者后续策略？廉价高方差和昂贵精确标签如何比较？一步替换标签能否处理互补动作？

### T07-078 — Double Reinforcement Learning for Efficient Off-Policy Evaluation in Markov Decision Processes — 精读优先
- 身份：Nathan Kallus、Masatoshi Uehara；JMLR21(167):1–63，2020，稳定键`jmlr:19-827`。[官方摘要](https://www.jmlr.org/papers/v21/19-827.html)；[全文](https://www.jmlr.org/papers/volume21/19-827/19-827.pdf)。A。检索另有相近ICML题名，不另计，实质版本关系待terra。
- 机制：借马尔可夫无记忆结构，以交叉拟合的Q函数和边缘密度比估计离策略价值，分析半参数效率及双重稳健。
- 支持／反例潜力：闭环评估可做，但需要历史状态具有所需记忆；压缩历史若不充分，不能自动沿用无记忆收益。
- terra问题：行为／目标策略、状态可见性、密度比支持覆盖、估计率条件；对用同数据挑最佳策略是否仍保证？

### T07-079 — Counterfactual Off-Policy Evaluation with Gumbel-Max Structural Causal Models — 精读优先
- 身份：Michael Oberst、David Sontag；ICML2019，PMLR97:4881–4890；关联arXiv `1905.05824`。[官方摘要](https://proceedings.mlr.press/v97/oberst19a.html)；[全文](https://proceedings.mlr.press/v97/oberst19a/oberst19a.pdf)。A。
- 机制：以结构因果模型生成有限部分可观测MDP的反事实轨迹，将策略差异定位到具体病例／轨迹用于调试。
- 支持／反例潜力：同一初始轨迹的反事实结果并非由观察分布唯一给定，结构假设很重要；反事实重放不能冒充随机干预真值。
- terra问题：Gumbel-Max与反事实稳定性的识别／假设角色；潜变量耦合、隐藏状态、模型错设及被筛选的极端效用轨迹如何影响判断？

### T07-080 — Why Adaptively Collected Data Have Negative Bias and How to Correct for It — 精读优先
- 身份：Xinkun Nie、Xiaoying Tian、Jonathan Taylor、James Zou；AISTATS2018，PMLR84:1261–1269；关联arXiv `1708.01977`。[官方摘要](https://proceedings.mlr.press/v84/nie18a.html)；[全文](https://proceedings.mlr.press/v84/nie18a/nie18a.pdf)。A。
- 机制：当历史观测影响后续数据收集时，在特定自然条件下样本均值产生系统负偏；提出选择推断式校正。
- 支持／反例潜力：控制器偏爱早期成功地址后，直接汇总“已读收益”可能失真；**不是所有自适应采样偏差都负向**。
- terra问题：导致负偏的精确采样／停止条件、估计对象和校正适用性；策略挑选产生乐观偏差与逐动作样本均值负偏要分开。

### T07-081 — The Self-Normalized Estimator for Counterfactual Learning — 精读优先
- 身份：Adith Swaminathan、Thorsten Joachims；NeurIPS2015；稳定键`neurips:39027dfad5138c9ca0c474d71db915c3`。[官方摘要](https://proceedings.neurips.cc/paper_files/paper/2015/hash/39027dfad5138c9ca0c474d71db915c3-Abstract.html)；[作者身份／介绍](https://www.cs.cornell.edu/~adith/)；[全文](https://www.cs.cornell.edu/~tj/publications/swaminathan_joachims_15d.pdf)。A。
- 机制：传统反事实风险估计器虽用于无偏评估，优化复杂策略类时却可倾向过拟合；改为自归一化估计并构建Norm-POEM。
- 支持／反例潜力：直接反驳“有无偏动作标签／评价式，训练选优也无偏”；自归一化不能补历史从未尝试的动作支持。
- terra问题：效用平移／尺度、等变性和过拟合反例；自归一化引入的偏差、泛化界、有限样本分母退化以及轨迹扩展。

### T07-082 — Evaluation of Active Feature Acquisition Methods for Time-varying Feature Settings — 精读优先
- 身份：Henrik von Kleist、Alireza Zamanian、Ilya Shpitser、Narges Ahmidi；2023预印本`2312.01530`，JMLR26(60):1–84，2025，稳定键`jmlr:23-1635`。[官方摘要](https://www.jmlr.org/papers/v26/23-1635.html)；[全文](https://www.jmlr.org/papers/volume26/23-1635/23-1635.pdf)。A。R1 U3待核入口现核销为有效新增，不重复现有静态作品W0307／`2312.03619`。
- 机制：部署获取策略触发分布变化；区分无直接效应（获取不影响真实特征）、无未观察混杂（历史决定仅依已见值）；分别使用缺失数据／离线RL，两者同时成立时使用更弱正性条件的半离线方法。
- 支持／反例潜力：**获取不改变世界状态，也可能改变策略和可见性分布**；不能把两种“无影响”混为一谈。
- terra问题：自然源变化、获取副作用、历史策略是否看了未记录特征；正性／支持覆盖的精确定义和三种估计量的辨识条件；语言来源回访可满足哪些？

### T07-083 — 代价敏感学习方法综述
- 身份：万建武、杨明；《软件学报》2020,31(1):113–136；在线2019-08-12，稳定键`jos:5871`；英文名 **Survey on Cost-sensitive Learning Method**。[原刊身份／摘要](https://jos.org.cn/jos/article/abstract/5871)；[全文入口](https://jos.org.cn/html/2020/1/5871.htm)。A，另仅消费§1.1代价类别入口；不计全文精读。
- 机制：综述错分代价、数据获取、标注、计算、存储与交互等成本，主体偏错分敏感分类，可向前追决策树／测量成本谱系。
- 支持／反例潜力：真实中文原刊桥接，不是主动序贯信息获取的直接同构实证；不以语言覆盖为由抬升相关性。
- 下一步／局部警戒：返回正文开头出现“代价矩阵所有元素为1退化普通错误率”等表述，按期望损失定义会成为常数而非0/1损失，另有min/argmin记号疑点。**本轮不将该综述的公式或理论叙述作为基础**，只作成本分类及原始引文入口；局部疑点交terra核原页／勘误，不宣布整篇失效。

### T07-084 — ベイズ流決定理論を用いる臨床試験：効用とサンプルサイズ設計
- 身份：坂巻顕太郎、兼清道雄、大和田章一、松浦健太郎、柿爪智行、高橋文博、高沢翔、萩原駿祐、森田智視；《計量生物学》2020,41(1):55–91；DOI `10.5691/jjb.41.55`。英文题名 **Bayesian decision theory for clinical trials: Utility and sample size determination**。[日文官方摘要](https://www.jstage.jst.go.jp/article/jjb/41/1/41_55/_article/-char/ja/)；[英文摘要](https://www.jstage.jst.go.jp/article/jjb/41/1/41_55/_article/-char/en)；[全文](https://www.jstage.jst.go.jp/article/jjb/41/1/41_55/_pdf)。A+官方DOM身份补核。
- 机制：用成本、收益、疾病影响定义效用，通过反向归纳讨论序贯临床决策／样本量；不只按假设检验确定继续或终止。
- 支持／反例潜力：标签／测量预算和未来决策效用共同规划的非英语桥接；临床风险不是语言证据消费的自动保证。
- 下一步：沿原刊参考文献追信息价值式多阶段样本量设计；区分统计显著、决策净值、样本获取成本与未来受益人口。

### T07-085 — A General Sequential Model for Constrained Classification
- 身份：Gabriel Dulac-Arnold；博士论文，2014-02-07答辩；作者机构法文介绍标题 **Modèles Sequentiels pour la Classification Multiclasse, Sparse et Budgetée**，出版清单列上述英文名。稳定入口`lip6:person-D1131/thesis-2014`。[机构身份／法文介绍及全文追踪入口](https://www.lip6.fr/actualite/personnes-fiche.php?ident=D1131)。A（官方论文介绍，尚未取得论文PDF）；只计1项博士论文，不把该页所有列出的论文计入有效新增。
- 机制：datum-wise顺序信息获取与决策，以RL政策实现稀疏／预算分类；官方介绍明确成本约束带来显著学习复杂度，并讨论廉价次优学习方法。
- 支持／反例潜力：法国来源入口及2011—2014谱系桥接；提醒部署少读可能换来训练更贵。
- 下一步：从机构原刊链取2011文本顺序阅读、2012法文文档阅读与完整学位PDF，区分派生论文的实验重叠；本轮未将这些题名旁列当作已读摘要。

### T07-086 — A Survey on Active Feature Acquisition Strategies
- 身份：Linus Aronsson、Arman Rahbar、Morteza Haghir Chehreghani；2025首发，v2（2026-02-10）；arXiv `2502.11067`。[摘要](https://arxiv.org/abs/2502.11067)；[全文](https://arxiv.org/pdf/2502.11067v2)。A+M。检索另见IJCAI2026页，未Fetch不自行核定正式状态。
- 机制：用明确POMDP框架关联成本敏感预测器、模型式、无模型及混合获取，联系结构化信息采集和自适应随机优化，承认许多既有方法缺保证。
- 支持／反例潜力：追经典链的重要综述；与W0311等有共同作者，是导览而非独立复证，也不采用其“首次统一”等优先权声称作为结论。
- 下一步：向原始引用追查，不用综述中转的保证替代定理原文；重点核成本、停止及不完整训练数据的定义变化。

### T07-087 — Adaptive Information Control for Search-Augmented LLM Reasoning — 精读优先
- 身份：Siheng Xiong、Oguzhan Gungordu、Blair Johnson、James Clayton Kerce、Faramarz Fekri；Findings EMNLP2026，pp.1036–1078；ACL `2026.findings-emnlp.52`，官方页DOI字段为`10.18653/2026.findings-emnlp.52`（按返回原值登记，不默默补成/v1）。[官方摘要](https://aclanthology.org/2026.findings-emnlp.52/)；[全文](https://aclanthology.org/2026.findings-emnlp.52.pdf)。A；2026-10近期正式页面，未读方法，不背书新模型／指标。
- 机制：方法DeepControl，以状态相关信息效用估计获取证据的边际价值，控制**是否继续检索与暴露多少细节**；包含层级粒度控制及退火控制强制，训练后测试不依赖外部控制。
- 支持／反例潜力：与效用、学习停止、粒度的组合高度邻近，需前移而非当普通router；仍未确认严格来源回访、互补估计、固定／重滚后续策略和全成本。
- terra问题：效用由什么标签／模型估计，是否金标／全信息可见？边际值是一步还是闭环终局？粒度操作是否保留原源可回访？课程是否导致旁路／机制替换？教师、检索、token、总墙钟及失败重试是否齐账？按同预算比较无效用、固定粒度、纯停止、贪心与随机控制。

### T07-088 — Bayesian Experimental Design: A Review
- 身份：Kathryn Chaloner、Isabella Verdinelli；1995；Statistical Science10(3):273–304；DOI `10.1214/ss/1177009939`。[官方摘要／全文入口](https://projecteuclid.org/journals/statistical-science/volume-10/issue-3/Bayesian-Experimental-Design-A-Review/10.1214/ss/1177009939.full)。A。
- 机制：以决策论统一贝叶斯线性／非线性设计，说明先验和效用改变时最佳设计如何变化。
- 支持／反例潜力：获取目标函数不是固定熵的自然唯一选择；同一数据源在不同任务损失下信息价值可不同。
- 下一步：分实验设计、顺序设计与实际停止；沿综述返回原始定理，并区分参数知识、模型判别与终局行动效用。

## 3. 不依赖争议论证的最小辨别例与测量约束

以下是本轮整理者给下一轮的**自建说明例／评估问题**，不是外部论文实验、不声称新定理，不进入文献计数。

### 3.1 独立输入也可以联合有用、单看无用

令独立公平比特X1、X2，标签Y=X1 XOR X2，0/1错误损失；先验最优错误率为1/2。只看任一比特后Y仍公平，错误率仍1/2；看两者后错误率0。若每次获取代价c且0<c<1/4，两个动作的联合净收益为1/2−2c>0，但一步收益减成本为−c，纯一步贪心可能直接停。

这只说明**一个明确任务／损失／预算下**单步和联合值不同，不证明所有语言多跳都属这种互补，更不证明某新控制器能学到它。地址动作可另构“首动作揭示应读哪个位置，后动作读该位置”；四格对照必须把闭环允许重新选址与钳住后续地址分开。以上无需W0311精确最优值或W0059均方误差断言。

冗余对照则令两来源是同一标签的重复副本：各自可有收益，第二份在第一份已知时边际收益为0。联合值由任务和已见历史决定，不能把全局归因分数直接当顺序动作Q值。

### 3.2 至少四个不同估计对象

1. **受控局部差**：同一已训练模型、同历史、关闭／替换某动作，同时钳住后续读取与计算；量局部消费。
2. **固定策略闭环差**：干预当前动作后让同一后续策略根据变化后的状态再决策；量Qπ(h,a)相对于Qπ(h,a0)，成本应含全部后续动作。
3. **重新优化差**：分别在有／无动作权限下训练／优化策略，再比较终局效用；含机制形成、适应和训练费用。
4. **数据选优后的部署价值**：用同一批历史／反事实标签挑选了策略或阈值以后，在独立部署分布上的价值；无偏的固定策略估计不自动覆盖这个选择步骤（081）。

不要把“同随机种子”当作反事实已识别；共享随机性是某种耦合／降方差设计，反事实轨迹分布还需要状态、结构和观测条件（079、082）。关闭读取通常不改原始文本，却改变策略可见信息、缓存及后续路由；这不等价于获取没有直接环境效应。

### 3.3 全成本标签账

下一轮逐篇必须列：

- 标签生成前是否读取了所有特征／完整原文／金标答案；每个历史、候选动作、预算需多少次完整rollout。
- cost-to-go来自专家、当前学习者、冻结旧策略还是分别重训的策略；策略变化后旧标签是否仍对应目标。
- 模型式估计的训练、采样与偏差，交互式标注在学习者新状态上的专家调用，离策略估计的重叠支持及有效样本量。
- 未被选中或获取失败的探测费用、控制器本身计算、额外读者／强教师训练、建索引及重试。
- 硬预算、期望成本、尾时延和跨查询摊销分开；便宜规则若在同全成本前沿上相当，不优先加复杂效用头。

## 4. terra精读交接（20项优先）

| 包 | 本轮local ID | 主要核查与期望交回 |
|---|---|---|
| R2-A（6） | 056、057、058、059、060、063 | 决策效用／信息量、替代／互补的精确定义；次模与链结构条件；开环／闭环；给出可引用页、公式、反例，禁止互换保证。 |
| R2-B（4） | 061、062、065、066 | 最优策略是否停止、非短视近似与排序失效、次模比率退化；经典反例与可用边界，不传播摘要的普遍化。 |
| R2-C（3） | 068、073、087 | 经典搜索／监督学习停止与新近粒度效用控制的接口对照；训练标签可见性和调用账；087立即前移，与W0339/HORMA/ReadAgent并读。 |
| R2-D（7） | 076、077、078、079、080、081、082 | 状态分布变化、cost-to-go策略对象、反事实可识别性、隐混杂／无直接效应、训练选优偏差；最便宜且仍有效的标签方案。 |

总计20项，非已读20。083中文综述局部公式疑点、W0311勘误／正式版、W0059修订均可附随交给原terra理论负责人，不把本发现代理的说明当数学审计验收。

### 已取得身份但仍不计有效新增的经典空白

- **Wald，Sequential Tests of Statistical Hypotheses（1945）**，DOI `10.1214/aoms/1177731118`：[官方页](https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-16/issue-2/Sequential-Tests-of-Statistical-Hypotheses/10.1214/aoms/1177731118.full)只返回身份／首页入口，无摘要；未取得／读到原始介绍，不计有效作品。后续terra取原PDF并明确简单假设、采样独立性、错误控制与最优停止的条件，不把SPRT直接当多动作获取策略。
- **Weitzman，Optimal Search for the Best Alternative（1979，1978工作稿）**，DOI检索线索`10.2307/1910412`：[RePEc官方书目](https://ideas.repec.org/a/ecm/emetrp/v47y1979i3p641-54.html)明确无摘要且出版全文受限；不因大量后续引用就计为摘要核验。064／065是独立新作品，不能冒充已精读Weitzman。后续合法取得原文或作者摘要，再核独立箱、最高单项收益、检查义务和保留值条件。
- **Russell、Wefald，Principles of Metareasoning（1989会议／1991期刊）**，期刊DOI`10.1016/0004-3702(91)90015-C`：ScienceDirect本轮HTTP400；[作者机构概述](https://people.eecs.berkeley.edu/~russell/research-bo.html)可读并列作品，但不是锁定该篇原始摘要，故保守不计有效新增。作者概述自己也强调精确元推理可能比原任务更难；后续取确切版本再谈定理。

## 5. 还缺什么、是否继续扩展

**值得继续，但下一步应优先读经典条件与087新近邻，不再堆宽泛路由模型。** 原始信息保留／回访和动作效用学习的接口仍需合并核对；33项新发现补了经典与负面机制，尚未证明任何策略在真实长文多源互补下胜出。

仍有决策影响的缺口：

1. 高阶互补、重复来源与不可靠来源同时存在时，便宜可估的动作值结构；严格次模／近次模条件在语言证据中不能预设。
2. 从完整信息教师转向部分日志、廉价rollout后，闭环效用标签的偏差／覆盖和总预算；金标支持重合不是终局消费。
3. 策略选择、重复校准和源分布变化之后的风险约束；固定策略OPE与选优后的保证需要分开。
4. 经典排序／停止源头尚有三项未达摘要核验；本轮已如实保留，而非为补经典名额降低门槛。
5. 中文／日文／法文入口虽然落地，相关非英语原始算法与跨语言证据获取实证仍不足；中文综述不等于中文源回访已验证，检索失败／噪声也不能推断该领域不存在。
6. 新近087的效用标签、粒度权限和完整成本未读；若已覆盖主要增强组合，应改差异点及最小判别实验，而非添加条件逃避最近邻。

交付检查：UTF-8、连续local ID、优先标记20、33条作品主键与目录无重复、版本簇不增计数、实际日志查询45条及47个FetchURL请求；只读脚本核对，不运行项目测试／训练。没有新增全局W-ID、没有更改旧发现卡或他人全文卡，旧文档保持历史快照，本文件明确新增限制并交接总目录负责人。

### 交付时目录复核

交付校验期间，总目录由并发负责人补入HMT W0385，从最初384变为385实体；已重新对**385实体**检查33个新增主键及正式题名，仍无重复。本轮文件未修改目录，也未将HMT计入T07新增。静态检查PASS：33项／20优先／45查询／47抓取请求、语言计数与UTF-8一致。全项目已读状态以目录及terra卡为准，本文件的“精读0”只指本发现代理R2，不是全项目状态。
