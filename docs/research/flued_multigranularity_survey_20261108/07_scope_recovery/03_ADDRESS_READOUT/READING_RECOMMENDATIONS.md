# 03_ADDRESS_READOUT：最小高价值阅读队列

2026-11-08｜sol。**12篇封顶，不新增批量精读配额。** 目的不是补齐“回访路线”，而是决定压缩状态、地址、query、读出算子和学习路径各自是否有问题。A01–A06仅为本审计局部候选编号；未写入原CATALOG。以下区分“旧卡已读，可按问题复核”与“真正待全文精读”，不重新计算FULL。

## 1. 第一优先：最直接改变病因解释的6篇

| 顺序 / 对象 | 准确原文与锁定版本 | 当前证据权限 | 阅读必须回答的问题 / 产物 |
|---|---|---|---|
| 1 **W0229** Test-time regression: a unifying framework for designing sequence models with associative memory，Ke Alexander Wang、Jiaxin Shi、Emily B. Fox | [2501.12352v3](https://arxiv.org/html/2501.12352v3)；[PDF](https://arxiv.org/pdf/2501.12352v3)，2025-05-02；沿[原卡](../../03_reading/B06/W0229.md)固定版本，非本次重新取原文 | 原卡FULL；本次读卡，不需再泛读整篇 | §3–4和§6：Gram校正、query构造、delta残差更新分别改变什么？把离线已知地址岭回归、原生query读取、可训练在线读者列成三种权限。产物是可实施的同bank读出对照，不是“反演可解所以模型会解” |
| 2 **A02** Dynamic Neural Turing Machine with Soft and Hard Addressing Schemes，Caglar Gulcehre等4人 | [1607.00036v2 PDF](https://arxiv.org/pdf/1607.00036v2)、[HTML](https://arxiv.org/html/1607.00036v2)，2017-03-17；HTML首页题名Continuous and Discrete，保留同ID差异 | 新候选；本次定向读§2–4、§6.1–6.3，非全文 | §4.3的“只把地址当参数、忽略动态内容”怎样发现？读写一致性正则是否有独立消融？软/硬地址和课程训练分别影响可表达性还是训练可达？必须读负项和GRU/前馈比较，不只引用平均胜NTM |
| 3 **A03** Homogeneous Keys, Heterogeneous Values: Exploiting Local KV Cache Asymmetry for Long-Context LLMs，Wanyun Cui、Mingwei Xu | [2506.05410v2 HTML](https://arxiv.org/html/2506.05410v2)、[PDF](https://arxiv.org/pdf/2506.05410v2)，2025-11-06 | 新候选；只定向读§3.1–3.2及§4.6少量，非全文 | 等键替换后“求和值+计数分母”与原不同键合并的近似分界在哪？重复广播缺计数修正造成什么误差？完整读取Hessian/Fisher/删梯度项及§4.6 K/V交叉消融，并核一次prefill梯度构建成本。不能承诺原值可逆重建 |
| 4 **W0214** RAM-Net: Linear-Time Sequence Modeling with Sparsely Addressable State，Kaicheng Xiao等4人 | [2602.11958v2 PDF](https://arxiv.org/pdf/2602.11958v2)，2026-10-06；题名按[原卡](../../03_reading/B16/W0214.md)实读版，目录旧题Selectively Addressable Memory属同作 | 原卡FULL；本次读卡；原文按问题复核 | §3和附录B：读写q/k独立到什么程度？读写配额失衡为何失败？每head独立槽是否控制了总状态而不只是活动量？列出重复key、同槽冲突、未命中写址的三种失败，不用top-K这个数字混称 |
| 5 **A05** Perceiver IO: A General Architecture for Structured Inputs & Outputs，Andrew Jaegle等15人 | [2107.14795v3 HTML](https://arxiv.org/html/2107.14795v3)、[PDF](https://arxiv.org/pdf/2107.14795v3)，2022-03-15 | 新候选；本次只核§3.1–3.2/图3文字，非全文 | query带位置、模态、任务、输入特征时分别有何权限？哪些结果靠输入特征捷径，哪些只用位置query？对比“先平均latent再一次读”与“不同位置query直接读同一bank”，说明可用记忆不必靠来源回访；因果长期记忆未被该文代证 |
| 6 **W0219** MHLA: Restoring Expressivity of Linear Attention via Token-Level Multi-Head，Kewei Zhang等8人 | [2601.07832v2 HTML](https://arxiv.org/html/2601.07832v2)、[PDF](https://arxiv.org/pdf/2601.07832v2)，2026-01-14；首发01-12 | 目录储备未读；本次读§4局部，不升级阅读状态 | “头”是token块还是通道头？§4.2学得系数矩阵由块索引确定，是否还有实际输入生成的混合？读附录因果块内掩码、流式推理与复杂度常数；当前块内未来信息如何排除？分开静态位置混合、内容query内积、输入动态路由三种来源 |

## 2. 第二优先：补反例、经典和跨层合同的6篇

| 顺序 / 对象 | 准确原文与锁定版本 | 当前证据权限 | 必须回答的问题 |
|---|---|---|---|
| 7 **W0086** On State Reduction in Linear Attention | [2602.04852v3摘要](https://arxiv.org/abs/2602.04852v3)、[PDF](https://arxiv.org/pdf/2602.04852v3)，2026-09-29 | 目录未读；本次仅原始摘要/版史。首作Philipp Nazari沿目录，本次返回未给完整作者栏，完整名单未知 | 理论约束的是状态矩阵秩、键/值投影秩还是注意力矩阵秩？剪枝后哪些任务/长度失败？训练后可减状态是“冗余未使用”证据，不是“原状态信息越少越好”；需看检索而不只困惑度 |
| 8 **A06** The Devil in Linear Transformer，Zhen Qin等7人 | [EMNLP2022正式版](https://aclanthology.org/2022.emnlp-main.473/)、[PDF](https://aclanthology.org/2022.emnlp-main.473.pdf)，7025–7041；DOI10.18653/v1/2022.emnlp-main.473；arXiv2210.10340关联未逐版比读 | 新候选；正式元数据/摘要核验，正文未读 | 无界梯度的精确对象和分母条件是什么？归一化是否只救尺度，不救地址绑定？早层对角局部机制能否与归一化独立归因？用作者原始消融而不是综述“linear attention不稳定”概括 |
| 9 **A01** Neural Turing Machines，Alex Graves、Greg Wayne、Ivo Danihelka | [1410.5401v2 HTML](https://arxiv.org/html/1410.5401v2)、[PDF](https://arxiv.org/pdf/1410.5401v2)，2014-12-10 | 新候选；本次读§3–4.1及部分4.2，非全文 | 地址序列、内容匹配、位置平移和锐化在复制/关联召回中各起什么作用？单/多读头与有状态/前馈控制器提供何种不同计算？读全实验局限，不能把可微误写成必然能学会 |
| 10 **A04** Reducing Transformer Key-Value Cache Size with Cross-Layer Attention，William Brandon等5人 | [2405.12981v1 HTML](https://arxiv.org/html/2405.12981v1)、[PDF](https://arxiv.org/pdf/2405.12981v1)，2024-05-21 | 新候选；本次读§2与表头，非全文 | 同一KV被多个层重读，哪些query保持独立？共享写者实际有几个？对照是否同头数/维数/总参数？核完整训练质量—KV字节前沿；§2.3已明确带宽不随共享自动下降，不能把2倍少存写成2倍加速 |
| 11 **W0203** Dual DeltaNet: Value-Side Memory Reorganization for Linear Attention，Yixiao Qian等6人 | [2610.38578v1摘要](https://arxiv.org/abs/2610.38578v1)、[PDF](https://arxiv.org/pdf/2610.38578v1)，2026-10-28 | 目录Q061未读；本次只核原始摘要/Atom身份 | 值侧selector从什么输入产生？值侧重组织与key侧残差校正能否分离？rank-2递归怎样改变覆盖/遗忘？原文全部效果和额外开销未知，不用摘要最强排行裁本项目。此为不回访路线 |
| 12 **W0210** Multi-State Linear Attention with Generalized Second-Order Routing，Hee Seung Hwang等5人 | [2610.37645v1 HTML](https://arxiv.org/html/2610.37645v1)、[PDF](https://arxiv.org/pdf/2610.37645v1)，2026-10-27；沿[原卡](../../03_reading/B06/W0210.md)固定版 | 原卡FULL；本次读卡，非新全文 | 冻结同一value bank时，专用路由Q/K、二阶矩、温度/门各能贡献多少？论文分别续训不等该干预。未满段的固定1/m与已见样本均值差异、段数增长及全段读取费用须核实现；不把二阶矩当答案保持证明 |

上述新作的“可读PDF URL”是准确固定入口，不表示本轮逐页打开该PDF；已获取的HTML/摘要范围以SEARCH_LOG为准。正式会议信息未知者保留未知，不从聚合页补录。

## 3. 无需重新精读即可重综合的既有材料

- [W0204 MoM](../../03_reading/B16/W0204.md)：在其共享query、线性读取条件下，先混状态与先逐态读取后混合代数等价。其收益不能直接归因独立头读出。
- [W0287 Attention Residuals](../../03_reading/B07/W0287.md)：固定伪query与输入动态query已分列，多头版本也未自动更好。与[W0289 Depth-Attention](../../03_reading/B15/W0289.md)共同整理“跨层读什么、原值还在否”；不因非回访就降低其在原问题中的价值。
- [W0237 LoLA](../../03_reading/B06/W0237.md)：压缩主体+精确例外及共享分母可直接提供非统一替换路线；缓存例外不等原文回访。
- [W0197 Landmark](../../03_reading/B01/W0197.md)与[W0174 HISA](../../03_reading/B01/W0174.md)：已足够说明地址粗不等载荷粗，不必再搜一批粗到细检索系统。
- [W0092 Usable Information](../../03_reading/B13/W0092.md)、[W0050 PARTIAL](../../03_reading/B03/W0050.md)：可读、可学、实际用的区分已有。W0050缺补充须保留，但不需要等它全篇核销才停止把probe当消费。

## 4. 阅读必须产出的比较表，而非更多模型名

每篇只需统一填：

1. **写入对象**：原token、投影KV、外积矩阵、可独立槽、重复前缀快照、跨层混合值；一个“槽”到底是一向量还是矩阵。
2. **地址与query权限**：内容/位置/时间/层索引，当前输入、任务身份、目标位置、额外监督是否可见；路由query与值读取query是否分开。
3. **真正的独立性**：不同投影不等统计独立；多个槽不等多个query；不同query不等保有不同载荷；多个层重读不等多个层写入。
4. **算子**：写入次数、擦除/累加/delta覆盖、门与归一化位置；重复副本对应的分母质量与单次写入是否匹配。
5. **理论对象**：状态秩、未掩码相似度矩阵秩、因果掩码后矩阵秩、Gram条件数、任务相关信息、实际内容收益分别报告。**未掩码QK^T低秩不能直接当因果三角掩码后注意力矩阵同样低秩的证明；状态低秩也不等于某任务信息缺失。** 不混用固定加性外积、delta递归和任意非线性读者的界。
6. **证据层级**：离线已知地址解码、另训query/读者、原生闭环读取、内容自洽替换。列出真实负对照、失败任务以及训练与驻留总账。

## 5. 队列停止规则与实验义务

读到足以判别上述变量就停止对应扩搜；不是必须把12篇都宣告FULL才能重综合。优先避免再次把新增6篇变成新的“总纲”。

文献不能替代以下项目内证据：

- **query问题**：同一冻结bank，在严格留出来源/身份上比较原生q、学得q、已知地址q；另训读者的监督/参数/步数单列，query不得偷带未来答案。
- **替换/广播问题**：原K原V、粗K原V、原K粗V、粗K粗V交叉；同一摘要重复更新与每块单写分列。注意力的重复质量恒等不自动适用于delta状态更新。
- **独立读出问题**：等总位数、同一写入下共享q/独立q、混合前后非线性及归一化分别控制；不要只增加头数又同时扩大状态。
- **训练可达问题**：同训练预算的原生端到端学习与离线补读分开；正内容干预与另训无通道对照回答不同问题。收官点梯度不能替全训练轨迹。

这些只为后续可证伪设计，不在本轮启动训练或修改任何内部裁定。
