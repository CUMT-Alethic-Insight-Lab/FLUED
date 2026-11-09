# 05_LEARNING_DYNAMICS｜定向公开检索与去重日志

日期：2026-11-08。执行：sol；定位为发现与覆盖审计，不是全文精读。

## 1. 范围、计数与执行

- 中心：压缩表示没有变成实际消费的记忆时，训练全史中的特征竞争、梯度/目标、初始化、辅助监督、形成与退场能否解释；不以多粒度回访为筛选条件。
- 真实查询13个：12次WebSearch、1次Kimi Code内置浏览器Bing搜索并实际读取结果DOM。20次FetchURL，涉及11个保留候选作品及1个身份不符入口；重复取同作品不同版本入口不算新作品。
- 向外仅发送本文件列出的公开机制词、论文题名或公开ID。未发送内部文档、实验数字、路径、源码或项目标识。未用学术数据源/API、未启付费、未下载执行论文代码。
- 浏览器只创建自己的1个研究标签；跨代理期间一次导航收到TAB_NOT_ACTIVE，属于控制权错误，不是网站拒绝或网络失败。没有抢改其他标签或用户会话。其余直接用公开FetchURL核验。未使用用户Chrome/Edge。
- 本次没有公开站点403、登录拒绝或需绕过的墙；没有以关闭证书校验、代理绕墙等办法访问。无临时网络失败需要重试；控制权错误不报作原文访问失败。
- 本日志所有“新”均指**相对本次当前CATALOG未收录**，不是声称学术新颖。没有改动总目录或赋新W-ID。全部11项新增FULL为0。

## 2. 查询逐条记录

| 编号／工具 | 原样查询 | 实际有效命中与取舍 |
|---|---|---|
| Q01／内置浏览器Bing | `posterior collapse lagging inference networks information preference powerful decoder training dynamics` | 原站1901.05534与OpenReview入口；优先核LD-N01，不把二手主题页当正文 |
| Q02／WebSearch | `"Deeply-Supervised Nets" "companion" 2015` | PMLR v38/lee15a与1409.5185；取正式PMLR方法/论文，LD-N02 |
| Q03／WebSearch | `"Critical Learning Periods in Deep Networks" early training information plasticity` | 1711.08856v3、ICLR2019；LD-N03，并保留翻转/标签重排可恢复反例 |
| Q04／WebSearch | `"in-context learning" "transient" 2024 2025 2026` | ICML2025 Strategy Coopetition与2026-10 How Language Models Develop ICL；LD-N05/06 |
| Q05／WebSearch | `2025 2026 feature learning competition aligned gradients auxiliary tasks negative transfer` | 结果多数不相关；ICLR2026目录给Residual Feature Integration线索，后以Q13核LD-N11。不把题名列表当理论已读 |
| Q06／WebSearch | `"posterior collapse" "2025" "2026" training dynamics linear VAE` | 命中2602.09277、2603.10935等近期入口；未全文核验，**不纳入11项保留候选**。优先用经典理论反例LD-N08防止先把故障归罪损失项 |
| Q07／WebSearch | `"Does learning require memorization" "gradient descent" feature competition` | 命中1906.05271长尾记忆理论，但不直接区分本轴路径形成；排出最小队列，不算保留新增。该查询区分力不佳，未继续沿它扩散 |
| Q08／WebSearch | `"Lazy training" "rich" initialization feature learning Chizat 2019` | 2409.14623、2025正式稿线索；取LD-N07原站v2，后Q12核LD-N09原始来源 |
| Q09／WebSearch | `"auxiliary tasks" "positive" "gradient" "negative transfer"` | ForkMerge原站与NeurIPS2023；取LD-N04 §3，直接针对梯度同向/验证迁移 |
| Q10／WebSearch | `"The transient nature of emergent in-context learning in transformers"` | 2311.08360v3和NeurIPS2023正式PDF；LD-N10，与2025机制修正LD-N05配对 |
| Q11／WebSearch | `"Don't Blame the ELBO!" "linear"` | NeurIPS2019与1911.02469；核论文首页、§4–6局部，LD-N08 |
| Q12／WebSearch | `"On Lazy Training in Differentiable Programming"` | 1812.07956v5、HAL作者稿；核原站摘要/版本，LD-N09 |
| Q13／WebSearch | `"Residual Feature Integration is Sufficient to Prevent Negative Transfer"` | 2505.11771与ICLR2026正式介绍；取官方会议摘要，LD-N11，作为保留残差不必有害的跨域对照 |

**经典**覆盖2015深度监督、2019关键学习期/推断滞后/线性VAE/缩放体制；**反例**覆盖正梯度不保证验证收益、弱解码器也会潜变量塌缩、机制出现后消失、去掉竞争策略反而变慢；**最近进展**有2025机制竞合、2025相对初始化尺度、2026会议残差迁移与2026-10检查点研究。最近12个月并非穷尽：优化器噪声/动量、语言模型深度监督与压缩模块特有相变没有做专线全检。

## 3. 保留候选：身份、版本、原文实际核验与缺口

本地临时标识LD-N01–11不属于总目录W系列。作者只写实际原站/论文可核者；未读证明和补充不推FULL。

| 本地ID | 确切题名／作者身份锚 | 固定原文、版本／发表 | 本轮实际读到的内容；未核范围 |
|---|---|---|---|
| LD-N01 | **Lagging Inference Networks and Posterior Collapse in Variational Autoencoders**；Junxian He、Daniel Spokoyny、Graham Neubig、Taylor Berg-Kirkpatrick，核PDF首页 | [v2 PDF](https://arxiv.org/pdf/1901.05534v2)、[v2 HTML](https://arxiv.org/html/1901.05534v2)，2019-01-28，PDF标ICLR2019 | 摘要、§2定义、§3早期后验轨迹、§4编码器内循环、§6.4/6.5分析定向读；不只摘要。编码器跟不上移动后验可使生成器忽略潜变量；多更新编码器不等新增结构。未读全部附录与数表，不计FULL。PDF文本含编辑痕迹/叠文，机制以可读HTML交叉；公式不据损坏文本猜补 |
| LD-N02 | **Deeply-Supervised Nets**；Chen-Yu Lee、Saining Xie、Patrick Gallagher、Zhengyou Zhang、Zhuowen Tu，核PMLR BibTeX和PDF首页 | [正式记录](https://proceedings.mlr.press/v38/lee15a.html)、[正式PDF](https://proceedings.mlr.press/v38/lee15a.pdf)，PMLR38:562–570，AISTATS2015；同作arXiv1409.5185 | 实读§2.1/2.2伴随目标及阈值消退、§2.3局部强凸/共同最优点假设、§3.1深网对照；表格提取有空缺且未独立审全部引理，不计FULL。是中间层直接分类监督，不等重建 |
| LD-N03 | **Critical Learning Periods in Deep Networks**；Alessandro Achille、Matteo Rovere、Stefano Soatto，核HTML作者栏 | [v3 HTML](https://arxiv.org/html/1711.08856v3)，[版本页](https://arxiv.org/abs/1711.08856)，v3 2019-02-25；ICLR2019身份由官方搜索记录关联 | 摘要、§1、定向核§2早期模糊/固定学习率及高层扰动反例、§3 Fisher指标与梯度协方差区分。图不逐点量，附录未读完，不计FULL；视觉分类结果不等字节模型关键期定律 |
| LD-N04 | **ForkMerge: Mitigating Negative Transfer in Auxiliary-Task Learning**；Junguang Jiang、Baixu Chen、Junwei Pan、Ximei Wang、Dapeng Liu、Jie Jiang、Mingsheng Long，核HTML作者栏 | [v3 HTML](https://arxiv.org/html/2301.12618v3)，v3 2023-11-16；NeurIPS2023原站PDF由检索核到 | 实读摘要、§1和§3定义/§3.1–3.2：同中途参数出发的一步实验中，梯度高度一致仍可能负迁移；负梯度也可像正则一样改善验证。不是“两损失从头到尾同向却落同一局部最优”的证明。算法完整成本/附录未读，不推荐照搬分支合并 |
| LD-N05 | **Strategy Coopetition Explains the Emergence and Transience of In-Context Learning**；Aaditya K. Singh、Ted Moskovitz、Sara Dragutinović、Felix Hill、Stephanie C. Y. Chan、Andrew M. Saxe，核HTML作者栏 | [v2 HTML](https://arxiv.org/html/2503.05631v2)、[版本页](https://arxiv.org/abs/2503.05631)，v2 2025-03-10；ICML2025官方海报/口头报告页由搜索关联，未逐页对比正式版 | 实读§2–5全部文本及图1/3/4说明；§6玩具模型只检索定位，附录未通读。两层注意力、Omniglot、固定训练标签；晚期是上下文约束权重学习，仍需标签出现在上下文。第二层回路保留却换用途；竞争策略可先帮助形成。不是自然语言普遍结论 |
| LD-N06 | **How Language Models Develop In-Context Learning**；HTML正文长题前缀为*From Copying to Composition*；Minglai Yang、Xinyu Guo、Renxiong Wang、Sunjie Hou、Daniel Yue Zhang、Yunzhong He，核HTML栏 | [v1版本页](https://arxiv.org/abs/2610.19113v1)、[v1 HTML](https://arxiv.org/html/2610.19113v1)，2026-10-13；正式发表未知 | 摘要、引言与§5–8/Limitations定向实读，检索附录D/E/I/K/L/N/P限制。检查点内容控制先于表现变化；抑制复制不等自动学会构造。直接微调/编码方式反例不同步；补充PDF与完整表未取得/未读，绝不计FULL或给精确阈值背书 |
| LD-N07 | **From Lazy to Rich: Exact Learning Dynamics in Deep Linear Networks**；Clémentine C. J. Dominé、Nicolas Anguita、Alexandra M. Proca、Lukas Braun、Daniel Kunin、Pedro A. M. Mediano、Andrew M. Saxe，核HTML作者栏 | [v2 HTML](https://arxiv.org/html/2409.14623v2)、[版本页](https://arxiv.org/abs/2409.14623)，v2 2025-03-04；搜索出现2025正式机构稿，未逐页比读，不默认等版 | 摘要、引言与§4假设定位：两层线性、输入白化、层间λ平衡等；核相对编码/解码尺度影响轨迹。巨大附录未通读，精确解未复证，不计FULL。不能说深非线性模型换尺度必修复 |
| LD-N08 | **Don't Blame the ELBO! A Linear VAE Perspective on Posterior Collapse**；James Lucas、George Tucker、Roger Grosse、Mohammad Norouzi，核PDF首页 | [v1 PDF](https://arxiv.org/pdf/1911.02469v1)，2019-11-06；[NeurIPS2019摘要](https://proceedings.neurips.cc/paper/2019/hash/7e3315fe390974fcf25e44a9445bd821-Abstract.html) | 摘要、§3–4.2、§6.1/6.2及A.1定向读。线性VAE和概率PCA对应；固定观测噪声影响塌缩驻点稳定，学习噪声时部分驻点成鞍点；无须强自回归解码器也可发生。定理全证明未核，不计FULL，不把所有塌缩都归因KL |
| LD-N09 | **On Lazy Training in Differentiable Programming**；Lénaïc Chizat、Edouard Oyallon、Francis Bach，原站PDF搜索首页身份 | [v5版本页](https://arxiv.org/abs/1812.07956v5)、[v5 PDF](https://arxiv.org/pdf/1812.07956v5)，2020-01-07修订；NeurIPS2019 | 本次仅原站摘要与提交史；缩放使模型近初始化线性化，训练loss好不等特征充分形成。正文未读，不核界常数 |
| LD-N10 | **The Transient Nature of Emergent In-Context Learning in Transformers**；Aaditya K. Singh、Stephanie C. Y. Chan、Ted Moskovitz、Erin Grant、Andrew M. Saxe、Felix Hill，原站/正式PDF搜索身份 | [v3版本页](https://arxiv.org/abs/2311.08360v3)、[v3 PDF](https://arxiv.org/pdf/2311.08360v3)，2023-12-11；NeurIPS2023 | 原站摘要/版本：训练loss持续下降而上下文学习先出现再消失。未读全文；需与LD-N05较晚更细机制说明配对，不将2023简写的“权重学习”当2025排除全部上下文使用 |
| LD-N11 | **Residual Feature Integration is Sufficient to Prevent Negative Transfer**（预印本题名可含REFINE前缀）；Yichen Xu、Ryumei Nakada、Linjun Zhang、Lexin Li，原站搜索身份 | [预印本](https://arxiv.org/abs/2505.11771)；[ICLR2026官方摘要](https://iclr.cc/virtual/2026/poster/10008648)；正式会议版与预印本逐版关系未知 | 本轮只读官方会议摘要。冻结源特征＋可训练目标残差；所述保证是特定目标分布类上相对从头训练的收敛率（忽略对数项），不是所有分布零负迁移。未读定理/证明，不把题名的sufficient当无条件保证 |

术语简释：ELBO为证据下界，即变分方法用于优化数据边缘似然的下界；VAE为变分自编码器，即含潜变量生成模型及近似后验的联合训练系统。Lazy/rich在本日志分别指近初始化线性化、以及内部特征显著变化的学习体制。ICL为上下文学习，指不更新权重而利用当前示例/规则；CIWL为上下文约束的权重学习，指调用权重中映射但仍需要上下文的标签线索。

## 4. 与当前CATALOG去重的实际操作

1. 对当前整份`02_catalog/CATALOG.md`做11个稳定arXiv ID的精确搜索及题名核心词搜索：`1901.05534 / 1409.5185 / 1711.08856 / 2301.12618 / 2503.05631 / 2610.19113 / 2409.14623 / 1911.02469 / 1812.07956 / 2311.08360 / 2505.11771`，均无匹配。
2. 同时搜索ForkMerge、Deeply-Supervised Nets、Critical Learning Periods、Strategy Coopetition、Lagging Inference、From Lazy to Rich、Transient Nature、Residual Feature Integration、Blame the ELBO等题名，均无匹配。不同入口不重复计数；仅以本次目录为去重边界，不保证另一个未编目资料夹无同作。
3. 因而**保留真新增11项**；未改总目录，等待主编决定是否纳入。候选不自动挤入精读队列。
4. 已入未读7项（W0327/0329/0330/0332/0335/0338/0344）与已读漏综合的W0331/0333/0334/0336/0337等另列于COVERAGE_AUDIT，新增数不含它们。

## 5. 排除、错误入口与未覆盖

- 一次探查入口`https://arxiv.org/abs/2412.07080`实际返回**EvRepSL: Event-Stream Representation via Self-Supervised Learning for Event-Based Vision**，不是预想的初始化论文。已由原站身份核验排除，不引其结论、不计新增；后续使用Q08/Q12明确命中的真实ID。此记录保留以防错误链接被继承。
- Q06的近期后验塌缩论文、Q07的长尾记忆理论只有检索线索，未核原文，不作为推荐依据；本轮没有为凑篇数继续收录。
- 对“两个目标始终同向而共同强化局部解”，当前只拿到局部方向／泛化反例与若干潜变量/竞争机制近邻，未核到能直接证明FLUED现象的论文。应补全文与本地实验，不用相关关键词作已证明结论。
- 没有做2026年所有会议的全量筛查；未读完整代码/训练日志；未对最近论文补充下载失败作假定，LD-N06补充状态只是本轮未取未读。

## 6. 20次FetchURL核对表

| 次序 | 实际请求URL | 结果 |
|---|---|---|
| F01 | https://arxiv.org/abs/1901.05534 | 摘要/版本成功 |
| F02 | https://proceedings.mlr.press/v38/lee15a.html | 正式身份/摘要成功 |
| F03 | https://arxiv.org/abs/1711.08856 | 摘要/版本成功 |
| F04 | https://arxiv.org/html/2301.12618v3 | 长文本成功，实际定向读§3 |
| F05 | https://arxiv.org/abs/2503.05631 | 摘要/版本成功 |
| F06 | https://arxiv.org/abs/2610.19113v1 | 摘要/版本成功 |
| F07 | https://arxiv.org/abs/2412.07080 | 身份不符，排除 |
| F08 | https://arxiv.org/abs/2409.14623 | 摘要/版本成功 |
| F09 | https://arxiv.org/html/1901.05534v2 | 长文本成功，定向续读 |
| F10 | https://arxiv.org/html/2503.05631v2 | 长文本成功，定向续读 |
| F11 | https://arxiv.org/html/2610.19113v1 | 长文本成功，定向续读 |
| F12 | https://arxiv.org/html/2409.14623v2 | 长文本成功，假设定位，非通读 |
| F13 | https://proceedings.neurips.cc/paper/2019/hash/7e3315fe390974fcf25e44a9445bd821-Abstract.html | 正式摘要成功 |
| F14 | https://arxiv.org/abs/1812.07956v5 | 摘要/版本成功 |
| F15 | https://arxiv.org/abs/2311.08360v3 | 摘要/版本成功 |
| F16 | https://iclr.cc/virtual/2026/poster/10008648 | 正式摘要成功 |
| F17 | https://arxiv.org/html/1711.08856v3 | 长文本成功，定向读取 |
| F18 | https://proceedings.mlr.press/v38/lee15a.pdf | PDF文本成功，方法/假设局部读取 |
| F19 | https://arxiv.org/pdf/1901.05534v2 | PDF文本成功，首页身份/正文局部交叉核 |
| F20 | https://arxiv.org/pdf/1911.02469v1 | PDF文本成功，首页身份/局部理论实验读取 |

Fetch返回保存长文不等实际读完；本次只对上述逐项标明的部分负责。全文精读、证明复核和代码复现均未新增。

## 7. 交付核验

只读Python校验通过：本目录恰有3个UTF-8文档；查询表13行、Fetch表20行、新候选表11行、阅读队列12行；11个稳定ID与当前CATALOG碰撞0；所有Markdown相对链接缺失0。Git限定本目录状态仅这3个新增文档，无脚本/日志生成物。未运行训练或项目测试（本轮只交审计文档）。尝试关闭自建浏览器研究标签时再次收到TAB_NOT_ACTIVE；为不与并行代理争抢浏览器控制，未继续强行切换，不能宣称已关闭该标签。
