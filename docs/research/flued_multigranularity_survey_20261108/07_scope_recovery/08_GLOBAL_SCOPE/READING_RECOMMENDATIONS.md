# 08_GLOBAL_SCOPE：最小高价值阅读与补证队列

2026-11-08｜12项有序任务，不是要求新增12篇论文：10项已有W-ID（3项已有卡，7项无卡）＋2项已核新发现。FULL/PARTIAL沿实盘卡，不在本轮升级；新原文精读0。队列围绕原始六轴，不以实现多粒度回访作为准入条件。

## 1. 有序12项：读什么、读到能回答什么就停

| 优先/项目 | 精确作品、版本与原文URL | 库内状态/卡路径（相对调研根） | 必须回答的问题与最小产物 |
|---|---|---|---|
| 1，先复用 | **Test-time regression: a unifying framework for designing sequence models with associative memory**，arXiv:2501.12352v3；https://arxiv.org/pdf/2501.12352v3 | W0229，FULL，`03_reading/B06/W0229.md`；本轮读完整卡，原PDF未重读 | 按回归权重、函数类、优化器重排写入/保持/读出；Gram统计缺失与值绑定缺失分别产生什么错误？产出“容量/干扰/优化”机制表，不必重读全篇凑FULL；需要引用公式时回原§3–6核定位 |
| 2，基础漏读 | **Zoology: Measuring and Improving Recall in Efficient Language Models**，arXiv:2312.04927v1；https://arxiv.org/pdf/2312.04927v1 | W0060，无卡；本轮核原摘要/提交史 | 合成关联召回成功为什么未转化为自然语言召回？何种卷积输入、多个query和干扰构成真实差异？原混合结构是否改变访问权限、状态或训练预算？保留能推翻简单“状态小所以全死”的对照 |
| 3，优化反例伴读 | **Revisiting Associative Recall in Modern Recurrent Models**，arXiv:2508.19029v2，2025-10-10；https://arxiv.org/pdf/2508.19029v2 | W0088，储备/无卡；本轮原摘要与版本已核 | 排名对学习率、宽深度、初始化和训练时长多敏感？是否存在充分调参后缩小差距而非增加记忆源的设置？最低产物是调参预算/训练可达性与表达上界的分离表，不把摘要归纳直接套本项目 |
| 4，最近且区分力强 | **Beyond State Capacity: Why Retrieval Breaks in Mamba**，arXiv:2610.19709v1，2026-10-14；https://arxiv.org/pdf/2610.19709v1 | W0213，Q093/无卡；本轮原摘要/史已核 | 先给query时怎样论证容量非瓶颈？门干预是否只显控制力而非自然相关性消费？相关性出现与门响应错位是否有因果对照、匹配深度/预算？产出可被否定的“编码/选择时序”假说；作者完整名单本轮未核齐，交读者补原首页 |
| 5，宿主基础 | **Gated Delta Networks: Improving Mamba2 with Delta Rule**，目录锁arXiv:2412.06464v3（2025-03-06）；https://arxiv.org/pdf/2412.06464v3 | W0201，无卡；版本/题名来自CATALOG，本轮未外部重核 | 门的保持与残差写入各改什么？合成召回、自然文本、硬件扫描分别有哪些直接对照？把原GDN做基础，再决定是否读W0202擦写解耦，不因后者更近期就跳过原始更新式 |
| 6，非回访替代 | **Learning to (Learn at Test Time): RNNs with Expressive Hidden States**，arXiv:2407.04620v4，2025-08-31；https://arxiv.org/pdf/2407.04620v4 | W0242，无卡；本轮核原摘要/完整作者栏/版本史 | 隐状态作为学习器后，状态位数、内层更新、块大小和自监督目标怎么变？TTT-Linear与TTT-MLP的增益能否分离函数类与额外计算？不借复杂模型状态回避访存；与W0229和Atlas同一表比较 |
| 7，另一整合范式 | **Titans: Learning to Memorize at Test Time**，arXiv:2501.00663v1，首发2024-12-31；https://arxiv.org/pdf/2501.00663v1 | W0234，无卡；本轮核原摘要/版本史，未核完整作者栏 | 神经记忆和短程注意力如何串联/并联/门控？遗忘、动量/更新、固定持久参数是否都算状态？哪项实验真正比较相同容量与计算？不能用2M针测试代替任意细节或未知查询充分性 |
| 8，新增经典 | **Predictive Representations of State**，Michael L. Littman、Richard S. Sutton、Satinder Singh；NeurIPS2001入口对应作者公开稿；修订号未知；https://web.eecs.umich.edu/~baveja/Papers/psr.pdf ；原站 https://papers.nips.cc/paper/1983-predictive-representations-of-state | 新发现N1，CATALOG无匹配/无卡；本轮核作者、定义/定理陈述与结论局部 | 预测未来试验作为状态，与重构过去有什么本质不同？有限POMDP存在性要求什么，递归更新误差是否稳定，原作哪些学习优势明确仍是展望？此读完成后才沿学习/稳定性引文做最窄补查，不先扩成整个强化学习综述 |
| 9，新增机制反例 | **Lagging Inference Networks and Posterior Collapse in Variational Autoencoders**，Junxian He、Daniel Spokoyny、Graham Neubig、Taylor Berg-Kirkpatrick；arXiv:1901.05534v2，2019-01-28/ICLR2019；https://arxiv.org/pdf/1901.05534v2 | 新发现N2，无卡；本轮核首页、摘要及§2–4/§6局部，未完成表格/附录 | 相同潜变量容量/架构下，改变推断器和生成器更新速率为什么改变是否使用潜变量？MI、KL、活动维数与预测质量如何不一致？有无等总更新预算反例？2–3倍普通VAE训练成本不能藏；不能把随机潜变量特有KL机制直接认成本项目确定性状态病因 |
| 10，补材料而非换题 | **Evaluating Compressed Memory: Dependence, Utility, and Content Benefit**，arXiv:2610.19373v1；https://arxiv.org/pdf/2610.19373v1 | W0050，PARTIAL，`03_reading/B03/W0050.md`；本轮读完整卡 | 只用已读主文D/U/C区分做立即重综合；若要据其系统对比裁定机制，合法补同版supporting_evidence.pdf、附录O完整训练账，核参数/步数/数据和初始化匹配。未获得时不以相近论文替补，不把找不到等同没有材料 |
| 11，独立字节对照 | **MambaByte: Token-free Selective State Space Model**，arXiv:2401.13660v3/COLM2024；https://arxiv.org/pdf/2401.13660v3 | W0352，FULL，`03_reading/B14/W0352.md`；本轮读完整卡 | 在不分块回访情况下固定状态字节模型支持什么？同原文/同每字节计算、草拟器额外状态和采样精确性怎样记？现卡足够复用§2–4/E/F，不新派整篇重读；只有采用其实际配置时追公开工件 |
| 12，横向基线而非层级先验 | **Memorizing Transformers**，目录锁arXiv:2203.08913v1/ICLR2022；https://arxiv.org/pdf/2203.08913v1 | W0144，储备/无卡；题名/版本来自CATALOG，本轮未外部重核 | 外部旧表示与当前宿主权重怎样配合，检索是否可微，陈旧状态/索引更新如何处理？作为不必建多级摘要的外记忆接入对照，明确历史源权限和完整费用；未读前不据名称填机制 |

**实际核销：12项＝10个已有W-ID＋2个已核新发现；已有10项中3有卡（2 FULL：W0229/W0352，1 PARTIAL：W0050）、7无卡（W0060/W0088/W0213/W0201/W0242/W0234/W0144）。** 不把现有FULL复用称为新增阅读尝试。

## 2. 哪些不应现在扩成另一个大池

- N3 *Beyond Fixed Memory*综述原站验证墙，未核版本和全文；可待合法公开源出现后用来查分类遗漏，但不挤掉上述原始反例。原始入口 https://openreview.net/forum?id=HaT1jGiqrS ，不绕过验证。
- 不立即读完T05的39个无卡条目、T06的45个无卡条目；先根据上表结果决定是否需要W0202擦写解耦、W0216递归岭回归、W0240现代Hopfield、W0235快权重基础等。
- 字节独立综述正式展开时，优先核未读的W0008 MEGABYTE、W0004 CANINE、W0005 Charformer、W0006 MANTa。该部分由独立字节轴定阅读合同，不要求服务于回访；本轮不把四篇再塞入“必须12项”而伪称最小。
- W0092、W0333/W0337、W0204/W0217、W0011已有卡可重综合；最先补的是“未读原作改变判断”，而不是为同一机制找第N篇赢家。

## 3. 文献工作与新实验分界

| 四类裁定 | 具体可立即执行/必须等待的事项 |
|---|---|
| **资料足够可重综合** | 已有卡重写信息存在→有限读出→自然消费链；按回归、保持/干扰、形成/补偿、宿主接口组织，不以回访为中心；字节单位/同文与成本合同独立成篇 |
| **需精读已有** | 上表7个无卡W-ID优先；W0050所需材料只在其系统性结论承重前必须补。基础更新式与强反例可改变下一选择，值得恢复精读，而非以“已219 FULL”冻结 |
| **需定向扩搜** | N1/N2完成固定版本精读后，只追一个决定性机制/稳定性或等预算反例；N3待合法原文。不要再按多粒度/来源词扩大同一家族池 |
| **需新实验** | 同压缩码换读出、同状态位数换写入/遗忘/优化日程、干扰年龄与重复键、自然内容改值与终点/形成期干预、同压缩器跨宿主和字节/token两线。外部论文不替FLUED直接量病因；本轮没有启动或授权这些实验 |

最先要允许被证伪的不是“多粒度比平层强不强”，而是六轴中哪一环导致信息虽可探测却没有成为自然可用记忆。若简单读出/更新/训练次序已修复，来源回访可继续作为另一资源权限下的候选，不需强行拼装。
