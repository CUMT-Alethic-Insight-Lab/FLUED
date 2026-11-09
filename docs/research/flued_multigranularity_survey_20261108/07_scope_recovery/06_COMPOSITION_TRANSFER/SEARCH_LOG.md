# 定向检索日志｜06_COMPOSITION_TRANSFER

2026-11-08｜sol。公开检索只发送英文公开机制/题名/作者词；未发送内部文档、实验名、数值或源码。使用 WebSearch、FetchURL 和 Kimi Code 内置浏览器；未用数据源插件、私人登录浏览器、付费数据库或安装软件。

## 1. 搜索范围与实际查询

**13 个 WebSearch 查询**。覆盖2014共适应经典、2021拼接、2023–2025反例/自修复/架构蒸馏、2026基础模型拼接与Delta线性化。无全域覆盖承诺；未系统搜索模块化多任务、模型合并、所有网络置换理论。查询中多粒度/原源回访不是入选条件。

| # | 实际查询字符串 | 有区分力的目标与结果 |
|---|---|---|
| Q01 | `model stitching revisiting limitations stitching layer similarity random networks 2024 2025` | 同时找正例、反例、近年版；命中 Bansal2021、Balogh2025、Mai2026；后续均取原文入口 |
| Q02 | `How transferable are features in deep neural networks co-adaptation Yosinski 2014` | 原部件特异性 vs 切断共适应；命中 arXiv/NeurIPS/作者PDF，采用 arXiv v1，不用二手总结承重 |
| Q03 | `hydra effect self repair language model ablations component interactions 2023 2024` | 部件消融的下游补偿；命中 Hydra2023、Rushing2024。前者仅摘要，后者正式元数据+定向v2正文 |
| Q04 | `transformer recurrent architecture transplant distillation Mamba attention linear 2025 2026` | 架构配套移植而非泛泛迁移；命中 MOHAWK 链、CAB及2026 KV→RAM迁移；后续取原文 |
| Q05 | `LoLCATs linearizing LLMs linear attention feature transfer 2024 2025` | 输出匹配与低秩适配是否交互；命中2410.10254，固定v3 |
| Q06 | `model stitching How Not to Stitch Representations Measure Similarity Balogh 2025 arxiv` | 确认反例身份；命中2412.11299与AAAI正式PDF；采用arXiv v1及官方Atom身份 |
| Q07 | `parameter matched ablation factorial interaction deep learning research pitfalls hyperparameter optimization 2019 2020` | 寻找参数/优化混杂原始方法；结果偏题（泛调参综述/软件文档），**未采用**，一次改写为Q09，不继续堆泛词 |
| Q08 | `MOHAWK transformers state space models distillation 2024 arxiv` | 锁定原始论文而非复现博客；命中2408.10189，第一次HTML网络失败，原URL重试一次成功 |
| Q09 | `"On the State of the Art of Evaluation in Neural Language Models" Melis Dyer Blunsom` | 针对架构排名对调参敏感的原始反例；命中1707.05589，取v2 §5.1/7 |
| Q10 | `"Explorations of Self-Repair" arxiv` | 确认2402.15390及正式版关联；以PMLR235/rushing24a官方元数据为准，不用翻译站 |
| Q11 | `"Gated Delta Networks" ablation convolution gate delta rule hybrid attention` | 目录已收却未精读的宿主配套；重新发现 W0201，取v3，提示§3.4和附录S.1/S.2需精读 |
| Q12 | `"What needs to go right for an induction head" formation clamping ablation` | 目录已有形成期证据；重新发现 W0337，取v1摘要/引言，仍以原卡列明范围为既有阅读证据 |
| Q13 | `Kuzina 2026 "Gated DeltaNet" linearization` | 由2610.11214 §6.2引用追到2607.07706；最贴本轴的冻结骨干/配套松绑协议，取v1并核Atom作者 |

## 2. FetchURL取回账（22调用；21成功、1临时网络失败）

“成功”只指返回页面/元数据，不等全文已读。下表有意记录截断和漏表。F07/F08为同一URL的一次合法重试，没有拒绝后换通道。

| # | URL | 结果；本轮实际消费范围 |
|---|---|---|
| F01 | https://arxiv.org/abs/1411.1792 | 成功；摘要与提交史v1 |
| F02 | https://arxiv.org/abs/2106.07682 | 成功；摘要与提交史v1 |
| F03 | https://arxiv.org/html/2412.11299v1 | 成功、长返回转工具文本；读摘要、§1、§2.1仿射拼接/直接匹配方法；其余未精读 |
| F04 | https://arxiv.org/html/2603.12433v1 | 成功；返回至§3.2附近；实际读摘要、引言、自接控制说明、§3.1–3.2；表1未完整提取，附录未读 |
| F05 | https://proceedings.mlr.press/v235/rushing24a.html | 成功；正式题名/作者/Cite/PDF链接及摘要 |
| F06 | https://arxiv.org/html/2410.10254v3 | 成功、止于§3.3附近；读摘要、§3.1–3.3开头及**表2所有四条件数值**；大模型成本和附录未全读 |
| F07 | https://arxiv.org/html/2408.10189v1 | 网络错误；未取得正文 |
| F08 | https://arxiv.org/html/2408.10189v1 | 原URL一次重试成功；长返回保存工具文本，定向读§4.2–4.4、§5.2–5.4方法/阶段说明；多表HTML缺格，未宣称表格完整核销 |
| F09 | https://arxiv.org/abs/2410.10254v3 | 成功；v1/v2/v3提交史，v3为2025-03-05 |
| F10 | https://arxiv.org/abs/2603.12433v1 | 成功；v1/v2/v3提交史，正文采用v1，不暗混v3 |
| F11 | https://arxiv.org/html/2510.19266v4 | 成功、长返回；只读题名、摘要、引言/直接注入失败的作者叙述。未读具体表、算法、附录，不援引精确效应 |
| F12 | https://arxiv.org/html/2610.11214v1 | 成功、长返回；定向读§4–5.3、§6.2、§7；**表4的缺格另用内置浏览器补核**；证明与附录训练账未完整读 |
| F13 | https://export.arxiv.org/api/query?id_list=1411.1792,2106.07682,2412.11299,2603.12433,2410.10254,2408.10189,2510.19266,2610.11214,1707.05589,2307.15771 | 成功；10项官方Atom：题名、完整作者、首发/更新日期、当前版本。不是十篇全文 |
| F14 | https://arxiv.org/html/1707.05589v2 | 成功；定向读§5.1参数预算和§7调参/选择/只做单项组件消融范围；非全文精读 |
| F15 | https://arxiv.org/html/1411.1792v1 | 成功；定向读§2处理与对照、§4.1及相关结果讨论；附录仅看到入口，不逐项核训练结果 |
| F16 | https://arxiv.org/html/2106.07682v1 | 成功、长返回；本轮采用摘要/引言，不将正文已到工具缓存冒充已全文读 |
| F17 | https://arxiv.org/html/2402.15390v2 | 成功、长返回；实际读摘要/引言及图1说明；未核完整消融配置/附录 |
| F18 | https://arxiv.org/abs/2307.15771 | 成功；摘要和唯一v1提交史 |
| F19 | https://arxiv.org/html/2412.06464v3 | 成功、长返回；读题名作者、摘要/引言、末段附录组件说明；完整S.1/S.2表尚未核 |
| F20 | https://arxiv.org/html/2404.07129v1 | 成功、长返回；定向摘要/引言，全文范围继续引用既有W0337卡，不算本轮重精读 |
| F21 | https://arxiv.org/html/2607.07706v1 | 成功、长返回；实际读§3.3、§4、附录C关键段，关键词定位理论/预算；表1–3单元格未完整取回，理论附录未审 |
| F22 | https://export.arxiv.org/api/query?id_list=2607.07706 | 成功；完整作者、v1、2026-07-08首发，区别HTML页眉“February 2026”，不自行解释日期差 |

**浏览器补核**：创建自己页 `2610.11214v1`，table角色扫描截断无元素；改用 `#S5.T4` 后 viewport DOM直接读表3/4，核到完整恢复/删头/删块/只全模型四行以及Qwen2.5-1.5B标头。一次导航因并行控制变更报 TAB_NOT_ACTIVE，重新选择自己页后成功，未触碰其他代理页。已关闭自己页。浏览器提示全会话65+标签页可能使侧栏拥挤，本代理未清理他人页。

## 3. 去重、身份与版本核验结果

方法：对全部543条 CATALOG 行按 arXiv/PMLR ID 及精确题名/常见别名检索。下列 N06-* **只是本报告临时定位键，不是新 W-ID**。12项均是“相对于该目录真新增”，不是声称首次发现；不改目录计数。搜索返回的无关项、未采用二手页面、仅在参考文献出现的其它论文不计新增。

| 临时键 | 作品身份（官方元数据已核） | 固定版本/原始URL | 去重与采用级别 |
|---|---|---|---|
| N06-01 | Jason Yosinski、Jeff Clune、Yoshua Bengio、Hod Lipson；How transferable are features in deep neural networks? | 1411.1792v1；2014-11-06；https://arxiv.org/pdf/1411.1792v1 | CATALOG无匹配；真新增；定向正文 |
| N06-02 | Yamini Bansal、Preetum Nakkiran、Boaz Barak；Revisiting Model Stitching to Compare Neural Representations | 2106.07682v1；2021-06-14；https://arxiv.org/pdf/2106.07682v1 | 真新增；摘要/引言，未完成方法/附录精读 |
| N06-03 | András Balogh、Márk Jelasity；How not to Stitch Representations to Measure Similarity: Task Loss Matching versus Direct Matching | 2412.11299v1；2024-12-15；https://arxiv.org/pdf/2412.11299v1 | 真新增；Atom注明AAAI2025；正式版未逐页比，定向正文 |
| N06-04 | Zheda Mai、Ke Zhang、Fu-En Wang、Zixiao Ken Wang、Albert Y. C. Chen、Lu Xia、Min Sun、Wei-Lun Chao、Cheng-Hao Kuo；Revisiting Model Stitching In the Foundation Model Era | 实际读2603.12433v1（2026-03-12）；https://arxiv.org/pdf/2603.12433v1 | 真新增；Atom最新v3 2026-06-02、注明CVPR2026；两版差未核，定向正文 |
| N06-05 | Thomas McGrath、Matthew Rahtz、Janos Kramar、Vladimir Mikulik、Shane Legg；The Hydra Effect: Emergent Self-repair in Language Model Computations | 2307.15771v1；2023-07-28；https://arxiv.org/pdf/2307.15771v1 | 真新增；仅摘要；不与下项重复 |
| N06-06 | Cody Rushing、Neel Nanda；Explorations of Self-Repair in Language Models | ICML2024 PMLR235:42836–42855；https://proceedings.mlr.press/v235/rushing24a.html ；定向文本 https://arxiv.org/html/2402.15390v2 | 真新增；正式元数据、v2摘要/引言。正式PDF与v2差异未全面核 |
| N06-07 | Michael Zhang、Simran Arora、Rahul Chalamala、Alan Wu、Benjamin Spector、Aaryan Singhal、Krithik Ramesh、Christopher Ré；LoLCATs: On Low-Rank Linearizing of Large Language Models | 2410.10254v3；2025-03-05；https://arxiv.org/pdf/2410.10254v3 | 真新增；Atom注明ICLR2025，定向正文/表2；**HTML提取漏第一作者，用Atom补正** |
| N06-08 | Aviv Bick、Kevin Y. Li、Eric P. Xing、J. Zico Kolter、Albert Gu；Transformers to SSMs: Distilling Quadratic Knowledge to Subquadratic Models | 实际读2408.10189v1（2024-08-19）；https://arxiv.org/pdf/2408.10189v1 | 真新增；v1标题短作Distilling…，最新v2 2025-02-08加前缀；未逐版比。HTML漏首名，Atom补正 |
| N06-09 | Penghao Wang、Yuhao Zhou、Mengxuan Wu、Panpan Zhang、Zhangyang Wang、Kai Wang；Data Efficient Any Transformer-to-Mamba Distillation via Attention Bridge | 2510.19266v4；2026-09-16；https://arxiv.org/pdf/2510.19266v4 | 真新增；首发2025-10-22，不能说2026全新首发；摘要/引言。HTML漏首名，Atom补正 |
| N06-10 | Kaicheng Xiao、Liran Dong、Haotian Li、Guoliang Xing；Bridging KV-Cache Quantization and Linear Attention: From Theory to Pretrained Weight Migration | 2610.11214v1；2026-10-08；https://arxiv.org/pdf/2610.11214v1 | 真新增；**不是W0214 2602.11958的新版**；定向正文+表4。HTML漏首名，Atom补正 |
| N06-11 | Gábor Melis、Chris Dyer、Phil Blunsom；On the State of the Art of Evaluation in Neural Language Models | 1707.05589v2；2017-11-20；https://arxiv.org/pdf/1707.05589v2 | 真新增；首发2017-07-18，定向方法/讨论 |
| N06-12 | Anna Kuzina、Paul N. Whatmough、Babak Ehteshami Bejnordi；The Key to Going Linear: Analysis-Driven Transformer Linearization | 2607.07706v1；2026-07-08；https://arxiv.org/pdf/2607.07706v1 | 真新增；近期定向正文；页眉February 2026不作公开首发日期；完整理论与表格未核 |
| W0201 | Songlin Yang、Jan Kautz、Ali Hatamizadeh；Gated Delta Networks: Improving Mamba2 with Delta Rule | 2412.06464v3；https://arxiv.org/html/2412.06464v3 | **已入但漏读**：目录储备/精读0，无登记独立卡；本轮定向取文不升FULL |
| W0337 | Aaditya K. Singh、Ted Moskovitz、Felix Hill、Stephanie C. Y. Chan、Andrew M. Saxe；What needs to go right for an induction head? | 2404.07129v1；https://arxiv.org/html/2404.07129v1 | **已读但可加强本轴综合**：`03_reading/B16/W0337.md`，不是新作品/新精读 |

## 4. 停止与剩余边界

- 本轮找到经典、反例及2026原始方法，且有一个直接以GDN为对象的冻结移植协议、一个删除阶段后返还预算的近期实验；本轴继续泛搜“又一个Mamba/稀疏访问模型”的边际价值低，转入 [READING_RECOMMENDATIONS](READING_RECOMMENDATIONS.md) 的12篇最小队列。
- CAB（N06-09）与Hydra（N06-05）保留为已核身份的相关发现，不强塞进最小12篇；前者须读实际语言建模配平与失败表才能超过MOHAWK/LoLCATs的增量，后者可由更系统Rushing2024优先替代阅读。
- 未核原代码、checkpoint、显著性、所有图坐标、付费原刊或全部正式版差异。没有全文精读新增，没有独立效果复现，不宣称任何路线在FLUED已验证。
- 没有公开访问拒绝；只有F07网络临时失败和并行浏览器控制错误，按原入口一次重试/重新选页已解决，未绕过权限。
