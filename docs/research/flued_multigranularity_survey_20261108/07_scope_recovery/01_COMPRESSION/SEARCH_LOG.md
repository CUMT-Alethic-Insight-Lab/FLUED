# 01_COMPRESSION：真实检索与去重日志

2026-11-08｜sol｜查询仅含公开题名/机制词，不发送内部实验、草案、数字或源码。目标为表示压缩/任务充分性，而非限定多粒度回访。未用学术数据源API；使用WebSearch、FetchURL及Kimi Code内置浏览器。

## 1. 本轮可复核数量与边界

- **9条WebSearch**，如下逐字记录；无年份穷尽/引文全图遍历。
- **18次FetchURL：16成功、2临时网络失败**。其中 `2305.17295v2` 同一URL重试一次成功；`1808.07593v4` 经内置浏览器读取同版摘要成功。无403/登录/付费拒绝，无绕过访问控制。
- 内置浏览器同版摘要：1次建页、1次文档文本读取。其后导航/关页因并行控制非活动页报TAB_NOT_ACTIVE，未把失败算来源访问成功或新搜索。
- **6个CATALOG未收录的核验候选N01–N06**；没有新增W-ID，没有改变543实体原台账。作品级标题/稳定ID/正式出版页至少一种已取原始源，不靠二手摘要补作者或结论。
- 5项已有但漏读的关键作品由本轮原站重新确认：W0064/W0066/W0067/W0037/W0055；另W0023搜索重发现，但已有FULL卡并已综合，不计新增。
- 原文读取深度：6项新增均只是摘要或指定局部；**本轮新增FULL=0、复现=0**。检索结果数量不作为覆盖充分性指标。

## 2. WebSearch逐条日志

| 编号 | 实际查询 | 区分目的 | 结果及处置 |
|---|---|---|---|
| Q01 | `representation compression reconstruction prediction sufficiency unknown downstream tasks rate distortion counterexample` | 非回访、不同目标的理论反例 | 命中CVPR2022 Rethinking Minimal Sufficient Representation（N01）、Coding for Machines（N05）；均进一步取原始来源；W0080为已入重发现 |
| Q02 | `Compressive Transformer attention reconstruction loss autoencoding loss memory compression` | 经典主干消费/目标选择 | 原始1911.05507与大量综述/实现；W0023已入且FULL，读取现有卡，不把教程代原始消融 |
| Q03 | `2025 2026 context compression reconstruction downstream task mismatch soft compression` | 近期目标错配、消费者接口 | 命中SAC（N02）、ComprExIT（N04），取固定版正文局部；Thinking as Compression仅搜索线索，未访问不纳入候选数 |
| Q04 | `"task-oriented" "compression" "unknown" tasks representation` | 防止只查LLM/摘要体系 | 命中机器人/分布式定位，未形成直接改变本轴判断的来源；不为数量纳入 |
| Q05 | `"Caveats for Information Bottleneck" deterministic scenarios` | 经典IB反例/确定标签条件 | 重发现W0064；原站Fetch一次网络失败，浏览器同版v4摘要和元数据读取成功 |
| Q06 | `"AUTOENCODING-FREE CONTEXT COMPRESSION"` | 核题名、版本与具体AE消融 | SAC 2510.08907v4，固定v4日期2026-03-11；读取§3–5/表5文字及版次史；不是据标题断言AE普遍有害 |
| Q07 | `"Neural Discrete Representation Learning" posterior collapse decoder` | 离散/连续潜变量、强解码器忽略潜码 | N03，取NeurIPS2017正式PDF与arXiv v2摘要史；其他后验塌缩方法仅线索未计新增 |
| Q08 | `"Coding for Computing" Orlitsky Roche 2001 graph entropy` | 不知道接收端具体输入时的函数压缩经典入口 | 命中IEEE后续文、MIT作者页和引用。原作身份只有二手引文，未取原作，**不计N候选/精读推荐主队列**；后续如需精确无回源函数计算界再核 |
| Q09 | `"Fixing a Broken ELBO" rate distortion representation 2018` | 重建/似然好而潜表示不好的经典证据 | N06，取PMLR正式页，核作者六人/ICML2018/摘要；未读全文定理与实验表 |

检索结果中动态日期与站点归属可能错误；采用正式页或固定arXiv提交史，而不把搜索片段日期当版次。停止泛搜的理由：已经找到能检验关键争点的原始入口，继续增加同类名称不优于先精读W0067/SAC/Broken ELBO。

## 3. 18次FetchURL明细

| F | 实际URL | 结果 / 实际阅读范围 |
|---|---|---|
| 01 | https://arxiv.org/abs/2203.07004 | 成功；摘要、v1/v2史；作者从F08正式页核 |
| 02 | https://arxiv.org/html/2510.08907v4 | 成功，输出较长保存为工具文本；实际读摘要、§1、§3–5及§4.3 AE消融文字；表1–8多数单元缺失，未读附录全体，不算FULL |
| 03 | https://arxiv.org/abs/1711.00937v2 | 成功；摘要、提交史，v2=2018-05-30 |
| 04 | https://arxiv.org/abs/1808.07593v4 | 临时网络错误；内置浏览器同URL合法读取题名/作者/摘要/版本史，v4=2019-02-08；无正文精读 |
| 05 | https://arxiv.org/html/2305.17295v2 | 临时网络错误 |
| 06 | https://arxiv.org/html/2602.03784v4 | 成功；实际读摘要、§1–6.6.1、表1–4、机制式和限制相关文字；输出止于§6.6.2开头，附录未读，不算FULL |
| 07 | https://arxiv.org/html/2305.17295v2 | 原URL重试一次成功；读摘要、引言贡献、§II-A–C定义局部；证明附录/实证全表未读 |
| 08 | https://openaccess.thecvf.com/content/CVPR2022/html/Wang_Rethinking_Minimal_Sufficient_Representation_in_Contrastive_Learning_CVPR_2022_paper.html | 成功；正式页作者、CVPR2022页码、摘要；主文/补充PDF未读 |
| 09 | https://arxiv.org/abs/2510.08907v4 | 成功；摘要、v1–v4史，固定v4=2026-03-11，首版2025-10-10 |
| 10 | https://arxiv.org/abs/2602.03784v4 | 成功；摘要、v1–v4史，固定v4=2026-06-18；摘要仍写代码将公开，HTML写仓库已公开，版本内网页差异保留 |
| 11 | https://proceedings.neurips.cc/paper/7210-neural-discrete-representation-learning.pdf | 成功；正式PDF转文可读，定向读摘要、§1/3/4.1–4.3，核作者/离散码/强解码器与语音例；未完整审图/附录/引用，不算FULL |
| 12 | https://arxiv.org/abs/2610.30493v1 | 成功；W0067摘要/提交日期，2026-10-21 |
| 13 | https://arxiv.org/abs/2504.13191v1 | 成功；W0066摘要/提交日期，2025-04-12 |
| 14 | https://proceedings.mlr.press/v80/alemi18a.html | 成功；正式身份/作者/摘要，ICML2018 PMLR80:159–168 |
| 15 | https://arxiv.org/abs/2305.17295v2 | 成功；摘要、v2日期2025-03-04；正式期刊轨道未核 |
| 16 | https://arxiv.org/html/2610.30493v1 | 成功、工具保存长文本；实际读摘要/引言，并定向检索/读§2条件与目标排序反转段；正文/附录尚未全读，不算FULL |
| 17 | https://arxiv.org/abs/2305.14788v2 | 成功；W0037摘要、v2日期2023-11-04、Accepted EMNLP2023说明；未读正文 |
| 18 | https://arxiv.org/abs/2405.13792v2 | 成功；W0055摘要、v2日期2024-12-09；冻结桥接训练机制只按摘要确认，未读原文实验 |

## 4. 去重后的新增与已有漏读

去重方式：在整个 `02_catalog/CATALOG.md` 精确搜索稳定ID（不含版次）、PMLR键、题名特征/作者词；并在03_reading全文搜索下表6项主键，无命中。**目录无命中不等于整个项目从未提过**；这里仅定义“本次543实体资料库未收录”。不把v1/v2、会议版/预印本、摘要/HTML算不同作品。

| 本地发现键 | 作品/身份核验 | 去重结果 | 内容核验与科学边界 |
|---|---|---|---|
| N01 | *Rethinking Minimal Sufficient Representation in Contrastive Learning*；Haoqing Wang、Xun Guo、Zhi-Hong Deng、Yan Lu；CVPR2022:16041–16050；2203.07004（v2=2022-04-02） | 真新增候选 | 正式摘要明确：若下游依赖跨视图不共享信息，则对另一视图充分的最小表示不足以支持下游。非“所有最小充分表示都不充分”；定理条件/原始实验未读 |
| N02 | *Autoencoding-Free Context Compression for LLMs via Contextual Semantic Anchors*；Xin Liu、Runsong Zhao等，HTML作者栏已取；2510.08907v4 | 真新增候选 | 选原词元锚＋双向压缩注意力＋各层KV，目标LLM冻结；§4.3明确SAC中LM优于AE/AE+LM，且500x的结果混合。§5.1梯度趋近正交不是负迁移的独立因果证明；表5数值未取不填 |
| N03 | *Neural Discrete Representation Learning*；Aaron van den Oord、Oriol Vinyals、Koray Kavukcuoglu；NeurIPS2017正式PDF；arXiv1711.00937v2仅作后续版本关联 | 真新增候选 | 码本量化、直通梯度、均匀先验训练与后学自回归先验；论文讨论强解码器忽略潜变量，具体图像/语音示例，不是语言记忆通用解。正式PDF与v2未逐字对版 |
| N04 | *Context Compression via Explicit Information Transmission*（ComprExIT）；2602.03784v4，2026-06-18 | 真新增候选 | 冻结LLM多层特征＋协调槽分配，不需回源。§6.1写question-unaware；§6.3有单层/无分配消融。重建NLL与QA相关是代理非因果；摘要18.5%在表1是相对改善，不是18.5个百分点。HTML作者栏为Hanqi Yan、Zhenyi Shen、Heng Chang、Ye Mao、Yulan He；原站提交人Jiangnan Ye不是可直接当作者的依据，作者表尚需PDF交叉 |
| N05 | *Rate-Distortion Theory in Coding for Machines and its Applications*；2305.17295v2，2025-03-04 | 真新增候选 | 原始HTML给全输入重建/模型分割特征重建/直接面向后端三种路线，明确任务输出失真不等输入MSE；理想等价/监督最优论证的附录未读。作者抽取页头漏首名，脚注出现Alon Harell；完整作者顺序/正式刊版未知，不由提交人填全 |
| N06 | *Fixing a Broken ELBO*；Alexander Alemi、Ben Poole、Ian Fischer、Joshua Dillon、Rif A. Saurous、Kevin Murphy；ICML2018 PMLR80:159–168，alemi18a | 真新增候选 | 正式摘要明确同ELBO（证据下界：对边缘似然的可优化下界）可有不同表示性质，并讨论强解码器忽略潜码；未核全文构造/完整实证，暂不写精确结论常数 |

**已有、并非新增**：

- W0064：经典IB确定性反例；目录未读、04未作品级引用。
- W0066：分类—重建操作点迁移；目录未读、04未作品级引用。
- W0067：最优目标随码率反转；目录未读、04未作品级引用；本轴最严重的漏读。
- W0037：AutoCompressors的主干软提示消费；目录未读、04无W-ID命中。
- W0055：xRAG原作未读；W0050实验涉及它不能代读原作。
- W0023：经典Compressive Transformer已FULL且专题综合已讨论，无需重开发现/计读。

## 5. 不纳入与未知

- Q08的 *Coding for Computing*：目前只是经典引用链入口，原作URL/版本与完整作者身份尚未由原始页核齐，不凭记忆填DOI、定理或推荐精确URL；不计六项新增。
- Q03的 *Thinking as Compression*、Q07的后验塌缩控制论文及通信/机器人命中：只有搜索片段，本轮不承重、不计新增、不自动扩大队列。
- SAC关键数表HTML抽取缺单元；ComprExIT附录未读；N01/N06仅正式摘要；N05作者/终刊待核。本轮没有把“取到长正文”说成“全部精读”。
- 这些发现足以停止本轮泛搜，转交11篇最小阅读队列。若精读后仍不能隔离目标、接口、训练量和有效位数，应写需新实验，不靠追加题名宣称已解决。
