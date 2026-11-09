# 02_STATE_MEMORY｜最小高价值原文阅读队列

2026-11-08｜sol。以下是交给全文阅读代理的**12篇上限队列**，不是本轮已经读完12篇原文。先读前6篇，若已足够区分容量、优化与写忘接口，就停止扩数量；后6篇分别补机制替代或未决分支。卡状态沿用现有文件，官方摘要核验不会升级FULL。

这里的键是关联地址，值是载荷；残差是当前值减去记忆预测值；Gram矩阵是键向量内积/协方差统计；测试时训练指在新序列内用学习目标更新暂时记忆；保持正则指限制新写入对旧状态的改变。文献系统名保留原名，不引入新项目术语。

## 1. 先读6篇：建立原始问题的判别骨架

| 顺序 | 作品、固定版本与准确原文URL | 已有状态／本轮核验 | 必须回答的问题与可交付证据 |
|---|---|---|---|
| 1 | **W0199 Linear Transformers Are Secretly Fast Weight Programmers**；ICML2021/PMLR139正式版；[落地页](https://proceedings.mlr.press/v139/schlag21a.html)，[PDF](https://proceedings.mlr.press/v139/schlag21a/schlag21a.pdf)；关联arXiv 2102.11174v3，不假定两版逐字相同 | 目录未精读；本轮PMLR作者/题名/摘要已核 | 直接加性外积何时串扰？Delta究竟擦掉/改正哪一方向？重复键、非正交键的理论条件和原始合成对照是什么？列实际状态大小、归一化、误差指标，不能只写“容量改善” |
| 2 | **W0201 Gated Delta Networks: Improving Mamba2 with Delta Rule**；2412.06464v3，2025-03-06；[固定摘要](https://arxiv.org/abs/2412.06464v3)，[PDF](https://arxiv.org/pdf/2412.06464v3) | 目录未精读；本轮v3摘要/历史已核 | 门控保持和残差写入的更新顺序如何？快速清除与准确修正分别由什么消融支持？多条目/长延迟改善是否与短卷积或训练配方联动？区分同权重手术与分别重训 |
| 3 | **W0088 Revisiting associative recall in modern recurrent models**；2508.19029v2，2025-10-10；[固定摘要](https://arxiv.org/abs/2508.19029v2)，[HTML](https://arxiv.org/html/2508.19029v2)，[PDF](https://arxiv.org/pdf/2508.19029v2) | 目录未精读；本轮官方摘要和版本已核；作者Destiny Okpekpe、Antonio Orvieto由官方检索结果确认 | 学习率调优能推翻多少“状态架构不好”的排序？宽度与深度如何改变召回？卷积删去后是否仍能学会？逐项提训练/测试分布、调参公平性、多种子及失败区间，不把可学性反例泛化为容量无约束 |
| 4 | **W0213 Beyond State Capacity: Why Retrieval Breaks in Mamba**；2610.19709v1，2026-10-14；[固定摘要](https://arxiv.org/abs/2610.19709v1)，[HTML](https://arxiv.org/html/2610.19709v1)，[PDF](https://arxiv.org/pdf/2610.19709v1) | 目录未精读；本轮官方摘要已核；完整作者表未复核，不补填 | 查询先给、容量不应是主要约束时，为何还失败？相关性何时出现、门何时能用它，原始干预是否排除表示副损伤？与W0061查询先给成功的模型/训练差别是什么？不要仅凭探针相关就认定唯一病因 |
| 5 | **N02-3 Anatomy of Associative Recall in Fixed-State Recurrences: A Matched-State Decomposition, an Interference Wall, and a Curriculum That Breaks It**；2609.16183v1，2026-09-14；[固定摘要](https://arxiv.org/abs/2609.16183v1)，[HTML](https://arxiv.org/html/2609.16183v1)，[PDF](https://arxiv.org/pdf/2609.16183v1) | 真新增；本轮只抽读§1–6；Julian Boesch、Andrew Wee，官方页核验；初步预印本，非效果复现 | 条目数与间隔是否真正独立？“固定状态”控制了哪些成本，哪些未控？调优后卷积/转移差值还有多大？课程究竟提升均值、成功种子比例还是最优个例？补读§7–10和附录，核因果/双向权限、重复键真值、未见符号和长窗边界 |
| 6 | **W0060 Zoology: Measuring and Improving Recall in Efficient Language Models**；2312.04927v1，2023-12-08；[固定摘要](https://arxiv.org/abs/2312.04927v1)，[PDF](https://arxiv.org/pdf/2312.04927v1) | 目录未精读；本轮固定v1官方摘要已核；后续正式版差异未知 | 合成单查询成功为何不能代表真实多查询回忆？多查询关联召回如何构造，参数/状态/计算比较各是什么？把82%等摘要归因数字的对象、分母与局限恢复到原文，不直接拿作本项目损失份额 |

## 2. 再读6篇：不保存原文的设计分支

| 顺序 | 作品、固定版本与准确原文URL | 已有状态／本轮核验 | 必须回答的问题与读取优先条件 |
|---|---|---|---|
| 7 | **W0242 Learning to (Learn at Test Time): RNNs with Expressive Hidden States**；2407.04620v4，2025-08-31；[固定摘要](https://arxiv.org/abs/2407.04620v4)，[PDF](https://arxiv.org/pdf/2407.04620v4) | 目录未精读；官方作者、摘要与v4史已核 | 线性与非线性隐藏模型的收益到底来自函数类、更新步还是局部输入构造？较好困惑度是否伴随长延迟多条目/OOD查询使用？内学习标签、优化状态和内存读写费用分别多少？若选择表达力路线则优先 |
| 8 | **W0234 Titans: Learning to Memorize at Test Time**；2501.00663v1，实际首发2024-12-31；[固定摘要](https://arxiv.org/abs/2501.00663v1)，[PDF](https://arxiv.org/pdf/2501.00663v1) | 目录未精读；本轮摘要/首发日期已核 | 惊讶/梯度驱动写入与未来查询价值有什么差别？动量和遗忘如何保持或破坏旧事实？2M针测试的查询形式、训练接触、状态与局部注意力成本是什么？不以“long-term”题名认定已证明长期消费 |
| 9 | **N02-1 It's All Connected: A Journey Through Test-Time Memorization, Attentional Bias, Retention, and Online Optimization**；MIRAS，2504.13173v1，2025-04-17；[固定摘要](https://arxiv.org/abs/2504.13173v1)，[PDF](https://arxiv.org/pdf/2504.13173v1) | 真新增；Ali Behrouz、Meisam Razaviyayn、Peilin Zhong、Vahab Mirrokni；仅官方摘要/身份核验 | 将保持解释为正则后，哪些具体目标确实改善保留—适应权衡？近似求解怎样保证数值稳定？新模型是否有同预算、同骨干、长延迟/非平稳原始消融？这是研究框架原文，不拿统一措辞代实际证据 |
| 10 | **N02-2 HiPPO: Recurrent Memory with Optimal Polynomial Projections**；2008.07669v2，2020-10-23；[固定摘要](https://arxiv.org/abs/2008.07669v2)，[PDF](https://arxiv.org/pdf/2008.07669v2) | 真新增；Albert Gu、Tri Dao、Stefano Ermon、Atri Rudra、Christopher Ré；仅官方摘要/身份核验 | 记忆“最优”的函数类、时间测度和失真是什么？有界梯度/时间尺度鲁棒要求何条件？离散化和有限精度会否改变？为什么信号重建/分类不等于未知事实查询可用？若研究长期稳定性则优先 |
| 11 | **N02-4 Erase-then-Delta Attention: Decoupling Erase and Write Addresses in Delta-Rule Linear Attention**；2606.26560v1，2026-06-25；[固定摘要](https://arxiv.org/abs/2606.26560v1)，[HTML](https://arxiv.org/html/2606.26560v1)，[PDF](https://arxiv.org/pdf/2606.26560v1) | 真新增；Xiao Li、Chengruidong Zhang、Hao Luo等作者与v1已核；仅摘要 | 学得擦除方向如何识别旧内容，是否误删仍有用关联？状态稳定性的更新约束是什么？与W0202“门强度分开”相比是否真正同预算消融？长延迟多条目和新旧事实冲突能否直接举证，而非只有综合榜分？ |
| 12 | **W0203 Dual DeltaNet: Value-Side Memory Reorganization for Linear Attention**；2610.38578v1，2026-10-28；[固定摘要](https://arxiv.org/abs/2610.38578v1)，[HTML](https://arxiv.org/html/2610.38578v1)，[PDF](https://arxiv.org/pdf/2610.38578v1) | 已入未读；官方摘要与版本本轮核验；作者完整序列沿目录，本轮未另取全栏 | 值侧重组是否真正减少相关载荷对地址的干扰，还是额外更新/参数/训练所致？键侧与值侧分别改了什么？读取正确内容的原始消融和长流稳定性是什么？若写入路线已能解释失败，此项可后置 |

上述PDF是固定原文入口；本轮没有实际读取这些PDF，不能因链接存在宣称逐页可提取、附录完整或数学式已核。精读遇拒绝不绕过；临时网络错误只重试1–2次，仍不可取就交代未知。

## 3. 已有FULL的复用包：不再重复算阅读量

- **W0229** [B06/W0229.md](../../03_reading/B06/W0229.md)：回归权重、函数类、优化器；相关键、非平稳回归及MQAR预构造，可立即给队列1/2/7/9作术语与公式坐标。
- **W0212** [B06/W0212.md](../../03_reading/B06/W0212.md)＋**W0245** [B21/W0245.md](../../03_reading/B21/W0245.md)：分别是固定外积精确键几何、随机键线性排序；用来限定容量主张，不互相拼成一般神经容量定理。
- **W0061** [B04/W0061.md](../../03_reading/B04/W0061.md)：有限状态位数、查询先后。既有形式警告应保留；不必再读一篇复制下界来凑经典数量。
- **W0204/W0214/W0210/W0208**：总状态、活动访问、独立地址及快照重叠的已有原始卡；重综合先行，仅在争议口径处回核原表。
- **W0237/W0207**：残差选精确例外的两种机制已有完整卡及对比。作为有界精细历史分支，而非所有纯压缩态的必要解法。
- **W0050 PARTIAL** [B03/W0050.md](../../03_reading/B03/W0050.md)：仅复用已取得部分的依赖/效用/内容区分；未取得补充不自动安排无边界重试，更不冒升FULL。

## 4. 原文阅读的统一提取模板与停止规则

每篇只交六项：①真实保存对象与全状态位/优化器位；②直接特征、残差或内目标的写入公式；③保持、覆盖与擦除时序；④条目数、延迟、干扰相关性三轴是否分开；⑤精确存储键、未见键、噪声/语义查询、先给/后给查询分别测了什么；⑥外接恢复、部署读取、目标预测内容特异收益分别有什么原始控制。未报留空，不凭理论容量补表。

先补已有W0199/W0201/W0088/W0213/W0060，形成可重综合的最短链，再由问题选后6篇。若不足只剩本宿主同位/同训练的因果隔离，转为**需新实验**，不继续无限搜论文；若缺有限精度、长期稳定性或新查询族原始证据，才做限定词定向扩搜。
