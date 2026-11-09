# 01_COMPRESSION：最小高价值阅读队列

2026-11-08｜sol｜11篇，其中5篇已入目录但未读，6篇真新增候选。不是全文完成清单；不分配新W-ID，不更改原状态。原文URL与版本以本轮实际可达的固定版/正式页为准；未核内容明确留待阅读。

**先读前4项即可重写最关键的目标错配问题，再读接口与离散性分支。** 这不是“回访路线前置检查”；每项即使不保留来源，也独立相关。

## 1. 主队列（按改变研究判断的价值排序）

| 优先 | 作品 / 现有状态 | 准确原文URL与版本 | 必须回答的问题；最小阅读终点 |
|---|---|---|---|
| 1 | **W0067** *Optimal Multitask Representations Under a Rate Constraint: An Information Bottleneck Analysis*；Nicholas Stiles、Gregory W. Wornell；已入未读 | [v1摘要](https://arxiv.org/abs/2610.30493v1)、[v1正文](https://arxiv.org/html/2610.30493v1)、[v1 PDF](https://arxiv.org/pdf/2610.30493v1)；2026-10-21；PDF链接为原站规范入口，本轮未另取其字节 | 为什么同一个训练目标在低率/高率的下游排序会反转？任意固定高斯目标的大反悔值依赖哪些任务族/信噪比条件？读§2–4及对应证明、CelebA/dSprites预算匹配和有限位实验；必须区分互信息约束与实际码长。**当前只读摘要、引言及理论局部，不能直接采用其普遍最优性。** |
| 2 | **N02** *Autoencoding-Free Context Compression for LLMs via Contextual Semantic Anchors*；真新增，局部读 | [v4正文](https://arxiv.org/html/2510.08907v4)、[版次史](https://arxiv.org/abs/2510.08907v4)；v4=2026-03-11，首版2025-10-10；ICLR2026正式题名有检索命中，正式PDF与v4未对版 | AE何时有害、何时不是？原词元锚/KV接口、双向编码、取消AE分别贡献多少？优先取表5完整数字＋附录训练量；再读§3、§4.3、§5.1和相关消融。梯度近零并不独立证明干扰，t-SNE（降维可视化）接近也不证明自然消费；不要把作者解释升级成唯一机制。 |
| 3 | **N06** *Fixing a Broken ELBO*；真新增，仅正式摘要 | [ICML2018正式页](https://proceedings.mlr.press/v80/alemi18a.html)、[正式PDF](https://proceedings.mlr.press/v80/alemi18a/alemi18a.pdf)；PMLR80:159–168；本轮未取PDF | 同一证据下界分数如何对应不同信息率/重建/潜码使用？强解码器忽略潜码与目标函数最优性什么关系？读率失真构造、强解码器实例、信息率控制方法及实验；不要把“同ELBO”误写成同重建质量或同下游风险。 |
| 4 | **N01** *Rethinking Minimal Sufficient Representation in Contrastive Learning*；Haoqing Wang、Xun Guo、Zhi-Hong Deng、Yan Lu；真新增，仅正式摘要 | [CVPR2022正式页](https://openaccess.thecvf.com/content/CVPR2022/html/Wang_Rethinking_Minimal_Sufficient_Representation_in_Contrastive_Learning_CVPR_2022_paper.html)、[正式PDF](https://openaccess.thecvf.com/content/CVPR2022/papers/Wang_Rethinking_Minimal_Sufficient_Representation_in_Contrastive_Learning_CVPR_2022_paper.pdf)；16041–16050；[arXiv v2](https://arxiv.org/abs/2203.07004v2)，2022-04-02；正式/预印本未逐版比 | 对“另一增强视图”充分为何不等对未来任务充分？非共享任务信息假设及反例具体是什么？读理论/补充证明、增强和下游任务对照；核输入信息正则改善是否只是更多容量/训练或重建，不能据摘要断言所有最小充分表示都有害。 |
| 5 | **W0064** *Caveats for Information Bottleneck in Deterministic Scenarios*；Artemy Kolchinsky、Brendan D. Tracey、Steven Van Kuyk；已入未读 | [v4原始页](https://arxiv.org/abs/1808.07593v4)、[v4 PDF](https://arxiv.org/pdf/1808.07593v4)；2019-02-08；原页标ICLR2019；本轮浏览器只读摘要/身份 | 确定标签时线性拉格朗日权重为什么不能扫完整瓶颈曲线，平凡解怎样出现？读三项警告及其证明、替代泛函和MNIST实验；防止用“扫β没效果”否定所有信息瓶颈，或将测得互信息曲线当训练机制。 |
| 6 | **W0037** *Adapting Language Models to Compress Contexts*（AutoCompressors）；已入未读 | [v2原始页](https://arxiv.org/abs/2305.14788v2)、[v2 PDF](https://arxiv.org/pdf/2305.14788v2)；2023-11-04；原页明示EMNLP2023接收；本轮未读正文/正式版比 | 压缩向量怎样通过原主干soft prompt（软提示：输入向量而非离散文本的条件）参与续写？无需AE的学习信号、递归积累、随机分段和梯度范围是什么？核PPL（困惑度）收益、压缩示例的上下文学习、重排序三种任务是否同等消费；与ICAE消费者是否共同适配分开。 |
| 7 | **W0055** *xRAG: Extreme Context Compression for Retrieval-augmented Generation with One Token*；已入未读 | [v2原始页](https://arxiv.org/abs/2405.13792v2)、[v2 PDF](https://arxiv.org/pdf/2405.13792v2)；2024-12-09；原作正式发表版差本轮未核 | 冻结检索器和主干、只学桥接怎样带来内容增益？压缩器是否查询无关、教师/任务监督和解码前缀是什么？把原文正结果与W0050供体/常量对照配读；需原源/错源/无源与训练预算，不先判一向量必够或必无用。 |
| 8 | **N04** *Context Compression via Explicit Information Transmission*（ComprExIT）；真新增，局部读 | [v4正文](https://arxiv.org/html/2602.03784v4)、[v4原始页](https://arxiv.org/abs/2602.03784v4)；2026-06-18；完整作者表需PDF交叉，不以提交人代作者 | 最终层槽不如中间层是信息消失还是接口可读性？槽间协调是否在同位数/同预算有独立价值？读§4、§5、表2及附录A.1诊断；核单层探针与自然主干的差别、窗口Sinkhorn（归一化迭代求传输分配）实际范围。18.5%是相对改善，不写18.5pp；重建与F1相关不等因果。 |
| 9 | **N03** *Neural Discrete Representation Learning*（VQ-VAE：向量量化变分自编码器，用码本索引作离散潜码）；真新增，局部读 | [NeurIPS2017正式PDF](https://proceedings.neurips.cc/paper/7210-neural-discrete-representation-learning.pdf)、[arXiv v2](https://arxiv.org/abs/1711.00937v2)；v2=2018-05-30，仅作关联；未对版 | 离散码、先验/后验目标、强解码器不用潜码分别是什么机制？读§3完整训练式、§4强解码器/语音与连续VAE对照；核码率和码本参数是否计费。后验塌缩（后验退化到先验、输入信息未进入潜变量）与码本塌缩（只使用少数码）不可混同。 |
| 10 | **W0066** *Universal Representations for Classification-enhanced Lossy Compression*；已入未读 | [v1原始页](https://arxiv.org/abs/2504.13191v1)、[v1 PDF](https://arxiv.org/pdf/2504.13191v1)；2025-04-12；作者全表/正式刊版本轮未核 | 一个编码器复用到多个分类—重建操作点付多少代价？“universal”是否只是已定任务与约束点，而非未知未来查询？读分类/感知两情形、单个编码器与逐点训练比较、MNIST局限；不要把摘要的显著失真惩罚当普遍不可兼容定理。 |
| 11 | **N05** *Rate-Distortion Theory in Coding for Machines and its Applications*；真新增，局部读 | [v2正文](https://arxiv.org/html/2305.17295v2)、[v2原始页](https://arxiv.org/abs/2305.17295v2)；2025-03-04；作者页头抽取缺首名，完整顺序/终刊待核 | 应重建输入、重建中间特征，还是直接输出后端能用的表示？理想三路线等价需要哪些可实现性条件，有限消费者为什么仍不同？读§II–III与附录A的原始证明、再核标签可用/不可用目标的实证；不能以理想渐近结论宣布特征接口免费等价。 |

PDF规范入口在上表只作为下一步准确定位，未取的均标明，不算本轮访问成功。全文/表格未读不填数；正式版未对比不回填预印本。原始作者、题名、版本和当前阅读范围的核验链见 `SEARCH_LOG.md`。

## 2. 无需重开全文阅读的已有综合锚

这些卡已在本轮读完，可先用现有证据重综合，不应为“完成更多FULL”重复计数：

- W0059 `03_reading/B04/W0059.md`：只用任务不变族的对数损失主线；MSE扩展争议不承重。
- W0091 `03_reading/B04/W0091.md`、W0092 `03_reading/B13/W0092.md`：指定读出族可用性与实际主干利用分开；精确最优/现实训练分开。
- W0038 `03_reading/B24/W0038.md` 对读N02：ICAE中AE+LM有益与SAC中未必有益并不冲突，架构/消费者/预算先配平。
- W0023 `03_reading/B24/W0023.md`：注意力响应重建的经典基线，不必所有目标都先重建文本。
- W0050 `03_reading/B03/W0050.md`：已读部分可用作依赖/效用/内容区分；如要引用九系统完整成本/公平排名，再追同版缺失补充；不阻塞基础概念重写。
- W0080 `03_reading/B24/W0080.md`、W0061 `03_reading/B04/W0061.md`：后到随机细节的有限状态限制与已限定任务正面例并列，不导向强制回源。

## 3. 阅读后应交付的最小比较表

每篇只提取能改变选择的字段，不再按“是否有下钻/来源指针”统一筛文献：

1. 写入器看见什么：具体问题、问题族、标签、未来片段、全序列/因果前缀？压缩后是否只剩Z？
2. 保留目标：输入精确恢复/平均重建、未来预测、任务答案、受限读者响应，或教师行为？
3. 消费者：理想贝叶斯、可训练探针、冻结主干、共同训练主干；适配量与无通道参照？
4. 实际容量：位宽×维数×槽数，量化熵、码本/桥/地址元数据，参数不等样本码率；有无额外残差/缓存逃逸？
5. 目标错配的证据：原始消融是否同时改架构、数据、训练量、查询可见性？有负面项/排序反转/域外失败吗？
6. 最小可采用结论与仍需目标宿主实验的部分。

**停止规则**：若前4篇加现有锚已能清楚分出容量不足、保留目标错配和消费者适配，先重写研究分叉；若要选离散化/特征锚/协调槽，再读对应分支。某路线的原作仍缺公平对照，就转为新实验义务，而不是继续泛搜直到找到赢家。
