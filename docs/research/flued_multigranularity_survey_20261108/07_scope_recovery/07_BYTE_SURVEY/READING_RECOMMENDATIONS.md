# 07_BYTE_SURVEY｜最小高价值独立全文队列

2026-11-08｜sol。**12篇，按缺口排序，不按模型热度排序。** 本轮没有把任何新检索作品记为完整精读；下表是交给后续全文阅读的任务，不是已完成阅读认证。相邻新发现的编号见 [SEARCH_LOG](SEARCH_LOG.md)，覆盖裁定见 [COVERAGE_AUDIT](COVERAGE_AUDIT.md)。

## 1. 最小队列与每篇必须回答的问题

同组内容可交叉提取，但不要拿一个模型的Related Work代替另一篇原文。

| 顺序 | 作品及目录状态 | 准确原文入口/版本 | 为什么现在读；必须抽取的答案 |
|---|---|---|---|
| 1 | **CANINE: Pre-training an Efficient Tokenization-Free Encoder for Language Representation**，W0004；已收未读、无卡 | [arXiv v4 PDF](https://arxiv.org/pdf/2103.06874v4)，2022-05-18；本轮核v4摘要，正式版逐项差异未知 | 码点散列嵌入、下/上采样、CANINE-C/S预测目标分别是什么？可选子词软先验在哪里进入？编码器完整源权限与成本如何影响TyDi QA比较？当前靠W0360转述不够 |
| 2 | **Charformer: Fast Character Transformers via Gradient-based Subword Tokenization**，W0005；已收未读、无卡 | [arXiv v3 PDF](https://arxiv.org/pdf/2106.12672v3)，2022-02-23 | GBST（梯度式子词构造，按位置给候选块评分）怎样生成/混合不同长度块？输入byte、候选块与输出监督单位分别是什么？“固定下采样＋学评分”和“可变长度边界”是否不同？速度收益含哪些模块和任务？有无因果变体，不能默认可直接用于下一字节生成 |
| 3 | **MANTa: Efficient Gradient-Based Tokenization for Robust End-to-End Language Modeling**，W0006；已收未读、无卡 | [原文HTML](https://arxiv.org/html/2212.07284)，[PDF](https://arxiv.org/pdf/2212.07284)；本轮访问当前HTML，**固定版本未知，先锁abs历史** | 软字节—块分配、卷积/最大池化、四倍截断如何共同学习？截断为何关键、损失如何推动段率？编码已缩短而decoder逐byte的瓶颈是什么？模型训练按同原文还是同墙钟？已有局部读取不能代替附录/原表 |
| 4 | **MEGABYTE: Predicting Million-byte Sequences with Multiscale Transformers**，W0008；已收未读、无卡 | [arXiv v2 PDF](https://arxiv.org/pdf/2305.07185v2)，2023-05-19 | 固定patch怎样构造因果表示、块内局部模型怎样预测、全局状态延迟多久？训练与生成并行性分别来自哪里？对BPE同预算、长上下文和多模态证据分别有多强？此文是“必须学边界”的重要竞争基线，不因无回源而降级 |
| 5 | **Using the Output Embedding to Improve Language Models**，W0364；已收未读、无卡 | [EACL2017正式PDF](https://aclanthology.org/E17-2025.pdf)，[正式页](https://aclanthology.org/E17-2025/) | 共享如何改变两条梯度更新，为什么共享表更像输出表？不同词表/模型/正则对困惑度改善贡献如何？翻译三端共享与LM输入输出绑定怎样区别？与W0366并读，避免把经典已知更新方向包装成新“共享失败” |
| 6 | **Tying Word Vectors and Word Classifiers: A Loss Framework for Language Modeling**，W0365；已收未读、无卡 | [arXiv v3 PDF](https://arxiv.org/pdf/1611.01462v3)，2017-03-11 | 理论框架使用什么目标/假设，推出何种共享，不推出什么？辅助损失与共享开关能否分离？PTB大词表经验怎样迁移到256字节表，余弦归一化是否仍在原框架内？不预称定理正确或普遍最优 |
| 7 | **Dynamic Multi-Byte Prediction With Hierarchical Language Models**，W0015；已收未读、无卡 | [arXiv v2 PDF](https://arxiv.org/pdf/2608.15454v2)，2026-08-21；[v2 HTML](https://arxiv.org/html/2608.15454v2) | 可变段的预测窗口怎样形成、mask是否同时保证段级因果和段内依赖？无额外参数具体对哪个基线？单头并行、自己验证、外部验证分别保何种分布/质量？吞吐、缓存权限、接受率与任务长度要配对 |
| 8 | **Scratchpad Patching: Decoupling Compute from Patch Size in Byte-Level Language Models**，N01；真新增，仅读摘要/引言 | [arXiv v1 PDF](https://arxiv.org/pdf/2605.09630v1)，2026-05-10；[v1 HTML](https://arxiv.org/html/2605.09630v1) | 临时块内聚合怎样更新、何时提交/丢弃KV？持久压缩率与计算更新频率能否独立？同FLOPs四类分块的控制、例外及额外head成本是什么？是否存在实际墙钟证据？优先回答“压缩不够好”是否其实“因果状态太旧” |
| 9 | **Fast and Expressive Multi-Byte Prediction with Probabilistic Circuits**，N04；真新增，仅读摘要 | [arXiv v2 PDF](https://arxiv.org/pdf/2511.11346v2)，2026-06-02；[v2摘要](https://arxiv.org/abs/2511.11346v2) | 联合未来字节分布如何参数化；独立假设、概率电路和逐步生成如何在表达力/延迟间权衡？推测验证究竟保证原模型贪心还是完整采样分布，所需假设是什么？共享层、草拟器训练和额外内存是否全计？v1题名Multi-Token与v2属同作 |
| 10 | **Breaking the Token Ceiling: Distilling Smaller, Stronger Byte Models**，N05；真新增，仅读摘要 | [arXiv v1 PDF](https://arxiv.org/pdf/2609.12303v1)，2026-09-11；[v1摘要](https://arxiv.org/abs/2609.12303v1) | token logits到byte logits的近似边缘化与结束token标记方法，分别精确到何种概率对象？同层参数、总参数、教师预算和总FLOPs如何计？低算力区反例与高算力优势哪些是实测、哪些为缩放外推？数据效率和logit存储节约不能掩盖教师成本 |
| 11 | **MYTE: Morphology-Driven Byte Encoding for Better and Fairer Multilingual Language Modeling**，N02；真新增，仅读摘要 | [arXiv v2 PDF](https://arxiv.org/pdf/2403.10691v2)，2024-11-11；关联[ACL正式身份](https://doi.org/10.18653/v1/2024.acl-long.804)，两版内容未比读 | 形态切分和码表来自哪些资源，是否仍有离线分词/语言标签？对99语的压缩分母、生成可逆性和混写如何处理？作者的跨语分母是否控制语义信息量？语言建模收益和公平是否随任务/预算改变？它是替代编码路线，不等同原生UTF-8模型 |
| 12 | **You should evaluate your language model on marginal likelihood over tokenisations**，N08；真新增，仅读正式摘要 | [EMNLP2021正式PDF](https://aclanthology.org/2021.emnlp-main.161.pdf)，[正式页](https://aclanthology.org/2021.emnlp-main.161/)；与arXiv2109.02550版差未知 | 多切分字符串概率如何定义、如何采样估计，估计偏差/方差及计算成本如何控制？域内/域外差距与分词器熵是什么关系？固定token路径归一化成BPB后还缺什么？供旧章概率比较补原始方法而非只给形式警告 |

这12篇中**7篇已在目录但没有独立卡，5篇是本轮新学术候选**。不因已收就称已读，也不因真新增就排到所有经典之前。队列完成后也不自动认证全部效果或理论；至少要实际读方法、实验、限制及承重附录。

## 2. 不排入本轮12篇的材料：为何暂缓

- **N03 AU-Net（2506.14761v1）**：同样高价值，但在先补MEGABYTE、H-Net已有卡和块内滞后后，再读其多层辅助预测；目前摘要不能确认固定词界、可学层级和不同预测跨度各自净效应。
- **N06 深层字符自注意力（1808.04444v2）**：应进入历史综述下一批，固定窗与中间损失是反对“必须显式压缩”的经典基线；但不会替代字节/字符区分。
- **N07 XTREME-UP（2305.11938v2）**：下一批与W0360配对，优先读具体byte/subword表、原文字节暴露和用户任务成本，不能由摘要说88语言就认为能力公平已验证。
- **N09 EvaByte官方介绍**：先按非论文材料引用，固定模型/代码版本后核8个预测头、注意力和真正测速条件；本轮只核到介绍开头，不把“2倍快、5倍少数据”作为比较结论。
- **W0512 Compute Optimal Tokenization、W0515 Beyond Text Compression**：已有未读，独立成本章节扩展时优先；本轮未取原文，不给理论/规模结论。若只能补成本而非生成章节，可与队列中的N05互换，而不是无限扩队列。
- **W0367伪逆共享、W0368专门优化器**：先补两篇经典和已有W0366，再判断是否缺共享替代机制；不要让新名词盖过基础问题。
- **W0353 bGPT、W0354 H-Net++**：任务、语言和多机制混杂需要全文，但不是补齐主干前的数量门。
- **W0050 PARTIAL**：外置补充和全训练预算仍缺；已读部分可作记忆评价边界，不能靠继续引用旧结论冒充缺失材料已到。它不是独立字节接口综述的核心模型依据。

## 3. 原文阅读的最小抽取表

每篇应至少回填这些字段；无证据填未知，不能从模型名补齐：

1. **四种单位**：输入、内部位置/压缩对象、输出符号、监督目标，是否含子词、字符、字节、词界、脚本标记或教师。
2. **编码/解码不对称**：深度、宽度、总参/非嵌入参、输入/输出长度、双向/因果、段完成时间及可见未来权限。
3. **共享实际对象**：输入输出表、编解码输入表、主干层、归一化与尺度，不只一个tied标志。全文不提供时标未知，后续再查固定公开配置。
4. **学习来源与方式**：固定/统计规则、外部标签、模型熵、主任务、重建、教师；近似梯度、连续松弛、阶段训练及损失约简分别记。
5. **概率对象**：逐byte概率链、单token路径、多路径边缘化、独立未来位置、联合分布、验证器贪心/采样目标，不能混作等效下一字节模型。
6. **公平分母**：同原文或同资源、有效监督量/重复量、预处理/规范化/截断、测试上下文、按语言和脚本的份额。
7. **成本分项**：数据预处理、教师、模型训练、预填、串行/并行解码、草拟/验证、峰值显存、变长批次、冷/热负载；理论FLOPs和估算加载量不冒充墙钟。
8. **反例与不确定性**：负向语言/任务、无增益或退化、随机种子、对照共同变化；作者外推与实测分栏，版本差异单独记。

## 4. 队列完成后仍不是靠文献能回答的事

可以据这些文献写独立综述，而不能据此裁定本项目为什么失用压缩记忆。内部因果归因仍需后续同宿主、同文本、同硬件的正交比较：接口、共享/输出几何、监督与损失约简、压缩率与更新频率、编码/解码开销分别变化。先核真实实现身份和原文任务合同，再决定是否需要实验；本轮无训练、无阈值裁定。
