# 最小高价值阅读队列｜06_COMPOSITION_TRANSFER

2026-11-08｜sol。目标不是读满篇数，而是回答：**同一个压缩/写址部件为什么在一个宿主中不可用，靠什么有限配套能修复，何时值得回到FLUED原生训练链验证？** 不要求论文带有多粒度或原源回访机制。

身份与URL已由官方摘要/Atom/PMLR核验，具体范围见 [SEARCH_LOG](SEARCH_LOG.md)。以下12篇是后续精读/重提取队列；**本轮新增全文精读0**。标注FULL仅指原库既有卡，不是本代理全文读过。这里的低秩适配（LoRA）指把可训练权重增量限制为低秩矩阵乘积；表示拼接（representation stitching）指冻结不同模型两段、仅训受限接口检验接续；分布外指接口输出偏离接收模型自然输入分布。

## 1. 队列（12篇，10项真新增＋2项已入库）

### 第一组：直接改实验合同的六篇，先读

| 优先 | 作品、准确版本和原文URL | 已核到/尚未核到 | 精读必须回答的问题；完成出口 |
|---|---|---|---|
| 1 | **Anna Kuzina、Paul N. Whatmough、Babak Ehteshami Bejnordi；The Key to Going Linear: Analysis-Driven Transformer Linearization**。N06-12；arXiv:2607.07706v1，2026-07-08。[HTML](https://arxiv.org/html/2607.07706v1)／[PDF](https://arxiv.org/pdf/2607.07706v1) | 定向读§3.3/4/App.C。已核：冻结原QKV/骨干、10M token，新件训练后再加短卷积/局部窗/前缀保留；LoRA学习率不同。表1–3与附录证明未全核，代码未核；页眉February不取代提交日 | **宿主配套能否反转核心件排序？** 提取每臂冻结参数、新增参数、训练量、缓存预算、学习率、原有QKV是否可动、逐层/位置误差。尤其核GLA/GDN在无/有卷积下的差分交互，而非只摘组合赢家；不把局部一阶理论当全局行为保证 |
| 2 | **Michael Zhang et al.；LoLCATs: On Low-Rank Linearizing of Large Language Models**。N06-07；2410.10254v3，2025-03-05（Atom注明ICLR2025）。[HTML](https://arxiv.org/html/2410.10254v3)／[PDF](https://arxiv.org/pdf/2410.10254v3) | 已读§3.1–3.3开头、表2四条件。附录训练/分块/窗口全配置未读；无代码验证 | **输出对齐×有限适配是否有不可忽略交互？** 将transfer有/无、LoRA有/无、2+2 epoch vs单阶段4 epoch写成完整表；分清教师给定输入拟合和自然输入链，窗口与特征映射变化另记。完成一份可迁移到DeltaNet的交互设计而非照搬性能数字 |
| 3 | **Aviv Bick et al.；Distilling Quadratic Knowledge to Subquadratic Models**（当前同ID题名前缀为Transformers to SSMs）。N06-08；实际审计版2408.10189v1，2024-08-19。[HTML](https://arxiv.org/html/2408.10189v1)／[PDF](https://arxiv.org/pdf/2408.10189v1)；最新[v2](https://arxiv.org/pdf/2408.10189v2)仅身份已核，版差未知 | 已定向读§4.2–4.4/5.2–5.4；表3等单元格未全提取，正式版与v2未逐页比 | **移植失败是缺配套、层间累积还是整模修复预算不足？** 提取阶段删减并核各臂总token，门设1/卷积恒等/去归一化/权重继承的具体条件；单件、整个块、整模三个监督层次分别能修什么。原生从零有益组件为何在蒸馏移植中被去掉，作者实证与推测分开 |
| 4 | **Jason Yosinski、Jeff Clune、Yoshua Bengio、Hod Lipson；How transferable are features in deep neural networks?**。N06-01；1411.1792v1，2014-11-06。[HTML](https://arxiv.org/html/1411.1792v1)／[PDF](https://arxiv.org/pdf/1411.1792v1) | §2/4.1处理、对照已定向读；图点和补充细节未逐项核 | **怎样估计“切断共同训练本身”的损伤？** 重建BnB、BnB+、AnB、AnB+及随机下层对照，区分同任务自接损失与额外跨任务损失；比较冻结/微调和完整历史成本。出口：本项目自接控制的最小合同，不搬视觉结果作字节证据 |
| 5 | **Kaicheng Xiao、Liran Dong、Haotian Li、Guoliang Xing；Bridging KV-Cache Quantization and Linear Attention: From Theory to Pretrained Weight Migration**。N06-10；2610.11214v1，2026-10-08。[HTML](https://arxiv.org/html/2610.11214v1)／[PDF](https://arxiv.org/pdf/2610.11214v1) | §4–5.3、表4已核；表4由内置浏览器实际读行；App.B2/表6阶段分配、显著性、理论证明未全核。**与W0214不是同一作品** | **删阶段怎样不偷减训练机会？** 精读头级→块级→全模型恢复，删除阶段预算返还规则；完整/删头Wiki PPL 16.33/16.31，平均任务68.1/66.9的指标分离；明确500M是token预算非GPU时等价。出口：恢复阶段成本重分配对照与内容消费量同报方案 |
| 6 | **Aaditya K. Singh et al.；What needs to go right for an induction head? A mechanistic study of in-context learning circuits and their formation**。**W0337，已有FULL卡** `03_reading/B16/W0337.md`；2404.07129v1，2024-04-10。[HTML](https://arxiv.org/html/2404.07129v1)／[PDF](https://arxiv.org/pdf/2404.07129v1) | 本轮读卡及原文摘要/引言。旧卡已读主文/相关附录，不应再排“从零全文补读”；未运行代码 | **制造失败和修复失败如何分账？** 定向重提取§3–5/App.D.1.1–D.1.2、E：终点删除/只留单头、训练中钳制、已训前端种子依赖、理想钳制人为简化；出口：同部件形成期与终点恢复分别统计的实验表 |

### 第二组：排除伪“兼容/不兼容”结论，再读六篇

| 优先 | 作品、准确版本和原文URL | 已核到/尚未核到 | 精读必须回答的问题；完成出口 |
|---|---|---|---|
| 7 | **Songlin Yang、Jan Kautz、Ali Hatamizadeh；Gated Delta Networks: Improving Mamba2 with Delta Rule**。**W0201，已收未精读**；2412.06464v3，2025-03-06。[HTML](https://arxiv.org/html/2412.06464v3)／[PDF](https://arxiv.org/pdf/2412.06464v3)；目录目前无独立卡 | 本轮只核摘要/引言及末段组件说明，不能改FULL。§3.4和附录S.1/S.2完整表未核 | **本地借来的“DeltaNet”究竟是更新规则还是连配套的完整块？** 列短卷积、输出门、归一化、Q/K范数、特征映射、头维、混合层顺序消融与控制预算，核每项是单独删还是联动。再由主代理授权后静态对照本地实际接口，未核部分留未知 |
| 8 | **Yamini Bansal、Preetum Nakkiran、Boaz Barak；Revisiting Model Stitching to Compare Neural Representations**。N06-02；2106.07682v1，2021-06-14。[HTML](https://arxiv.org/html/2106.07682v1)／[PDF](https://arxiv.org/pdf/2106.07682v1) | 摘要/引言；方法全配置和附录未精读 | **什么叫受限兼容测试，而不是重新训练答案器？** 核连接器类/参数/初始化/目标/训练预算、源接收方都冻结的范围，自接与不同种子/任务对照，是否只看任务保持；出口：适配器容量阶梯和随机/常量源对照 |
| 9 | **András Balogh、Márk Jelasity；How not to Stitch Representations to Measure Similarity: Task Loss Matching versus Direct Matching**。N06-03；2412.11299v1，2024-12-15（Atom注明AAAI2025）。[HTML](https://arxiv.org/html/2412.11299v1)／[PDF](https://arxiv.org/pdf/2412.11299v1) | 摘要、§1、§2.1定向读；实验表、分布外检测器训练和正式版差异未全核 | **高拼接性能是否只是接口找到接收方的怪解？** 提取“别层比自身相似”检查、仿射直接匹配与任务损失、OOD诊断、未测任务功能；出口：成功也要过的特异性/自然性控制。不能由该文反向推出任务拟合拼接毫无实际价值 |
| 10 | **Zheda Mai et al.；Revisiting Model Stitching In the Foundation Model Era**。N06-04；实际读2603.12433v1，2026-03-12。[HTML](https://arxiv.org/html/2603.12433v1)／[PDF](https://arxiv.org/pdf/2603.12433v1)；最新[v3](https://arxiv.org/pdf/2603.12433v3)，2026-06-02，Atom注明CVPR2026，版差未知 | 已读§3.2与引言自接说明；表1/图5全部格未核 | **局部特征误差小为何下游仍坏，怎样修且不只是加参数？** 核最终特征预匹配→任务微调、自接同容量控制、浅/深位置差异及教师成本。与Balogh正反对读：实用组合成功和相似度可信是不同估计对象。出口：局部/末端监督的诊断分叉 |
| 11 | **Cody Rushing、Neel Nanda；Explorations of Self-Repair in Language Models**。N06-06；ICML2024正式版。[官方页面](https://proceedings.mlr.press/v235/rushing24a.html)／[正式PDF](https://raw.githubusercontent.com/mlresearch/v235/main/assets/rushing24a/rushing24a.pdf)；本轮文本为[2402.15390v2](https://arxiv.org/html/2402.15390v2) | 官方作者/卷页及v2摘要/引言已核；正式PDF与v2版差、配置/附录未全读 | **小总消融效应是冗余、缩放还是下游补偿？** 提取重采样消融、直接效应/总效应、固定LayerNorm缩放、按prompt分布与成组消融限制；出口：总效应与受控路径诊断并报，不用人为阻止补偿后的损伤冒充正常部署损伤 |
| 12 | **Gábor Melis、Chris Dyer、Phil Blunsom；On the State of the Art of Evaluation in Neural Language Models**。N06-11；1707.05589v2，2017-11-20。[HTML](https://arxiv.org/html/1707.05589v2)／[PDF](https://arxiv.org/pdf/1707.05589v2) | 已定向§5.1/7，未复现调参；其单项消融不含全组合，不能当全因子实例 | **等参数、等默认超参和等优化机会分别回答什么？** 提取预算内嵌入/隐藏分配、选择偏差、复跑地板、各臂调参资源；出口：机制对照固定合同与部署择优前沿两张表，不照搬作者PPL差阈值 |

## 2. 为什么不把另外两项真新增也塞进队列

- **N06-05 Hydra Effect，2307.15771v1**：[原文](https://arxiv.org/pdf/2307.15771v1)。仅摘要，身份已核；它与Rushing2024是不同作品，后者更系统覆盖头/模型/自然分布。先读后者，可按引用需要再回经典，不为补数重复精读。
- **N06-09 Attention Bridge，2510.19266v4**：[原文](https://arxiv.org/pdf/2510.19266v4)。Penghao Wang等，首发2025-10-22、v4 2026-09-16；已核摘要/引言，尚未核表和配平。若MOHAWK/LoLCATs不能回答异构中间监督，才补其直接注入失败、桥接与层匹配消融。不能凭“Any”题名宣称任意宿主可迁移。

## 3. 已有卡不应被不必要地重新全文读一轮

以下直接重提取卡与对应承重段即可，**不计入上述12篇全文队列**：

- `03_reading/B03/W0050.md`（PARTIAL）：先用已读§3–5/附录C/J/K区分依赖、训练收益、内容收益；只在要做九系统公平排名/成本结论时补外置数值材料。无需为了本轴所有实验合同等它转FULL。
- `03_reading/B08/W0374.md`、`03_reading/B26/W0530.md`：把完整性/选择性、任意标签/随机初始化移入适配控制，而不是只留在字节评分综述。
- `03_reading/B16/W0204.md`、`03_reading/B06/W0210.md`、`03_reading/B16/W0214.md`：按“总状态/活动状态/投影参数/训练共同变化/固定值库是否存在”重排现有表格即可；卡已明确写出混杂。
- `03_reading/B13/W0092.md`、`03_reading/B04/W0091.md`：作为读出族/可用信息边界，不在本轴重审全部定理。当前无“失败适配器给出不可读证明”的理论证书。
- W0228（原始DeltaNet，2406.06484v6）：[PDF](https://arxiv.org/pdf/2406.06484v6)是目录现成入口，本轮未联网核该版内容；若主代理发现本地使用无门DeltaNet而非GDN，**用它替换队列第7项或追加接口专项阅读**，不能悄悄把两种宿主合并。

## 4. 精读交付模板与止读条件

每篇只需提取能改变研究选择的字段：

1. 处理的是从零制造、已训网络急性损坏，还是适配恢复？源/接收方哪些权重固定？
2. 单件、整个块、全模型及其配套分别是什么；有无`原样/自接/跨接/随机源/常量源`？
3. 单件×配套、单件×适配能否由表格直接计算；删阶段是否返还训练/开发预算？
4. 局部拟合与自然整链、平均任务与内容特异消费是否都测；失败样本与非目标损伤在哪里？
5. 真正控制的是参数、活动状态、总状态、更新量还是总算时；未知写未知，不补成“公平”。
6. 输出一条可执行判别：什么结果支持修接口、修写入、修组合、转形成期训练，或带最小包回FLUED；不能只写不可外推。

先完成前六项，若已得到自接/恒等控制、组件×适配交互、同预算阶段控制及形成—修复分账，就可冻结**候选实验合同**并停止泛扩搜。第二组六篇用于核验兼容性解释和优化公平，不必等全部读完才重综合既有证据。本轮不定阈值、不签发训练、不宣布这些新作已证明FLUED可行。
