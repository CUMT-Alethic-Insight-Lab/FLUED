# T04 R2 实际检索与来源日志

日期：2026-11-08。配套报告：[EXPANSION_R2.md](EXPANSION_R2.md)。本轮只写T04目录；不改全局目录/阅读队列/证据表，不训练、不提交、不派代理。精读交terra，本轮全文精读0。

## 1. 先查输入与去重

- 完整读取 `../../PLAN.md`、`../../05_review/COVERAGE_AUDIT_R1.md`、`../../02_catalog/CATALOG.md`（400行，分3次读完），检查本调研目录下无新增AGENTS.md。
- 以审计F1为主，补F2历史桥接及F7访问成本；校准保证的对象必须与“遗漏检测”分开。不因有返回父节点接口就称已解决未知遗漏。
- 实际全局目录快照为384个W-ID。先人工按题名/机制排除已收的MemWalker、ReadAgent、RAPTOR、SSA、HISA、AttentionIndex、CRAG、Self-RAG、FLARE、Adaptive-RAG、Self-Route、IRCoT、DynaKRAG、Sufficient Context、Conformal Risk Control、MUVERA等；不将它们再计新增。
- 后用只读Grep查新增方法名/正式ID，零命中；只读Python又核23个arXiv主/别名ID与9个正式/DOI别名均不在CATALOG。此为**该快照内去重**，不保证其他专题并发R2没有独立发现相同作品；本代理不分配新W-ID。
- 审计点名HMT（2405.06067）主要属T03/T05桥接，本轮不抢补、不重复追近期模型；把摘要召回与原始源访问的分类提醒保留在报告。

## 2. 实际工作量

- **30项新增确认论文/报告**，R2-001—R2-030；29项身份+摘要核验A，1项ConANN有定向正文边界核查P；完整精读0、代码核验0、复现0。
- **31次WebSearch：30次返回结果，1次429**。3条含中文，其余英文；中文查询结果主要是博客/二手说明，只有沿其线索取得的原作摘要入确认表，不据此声称中文正式论文覆盖已补齐。
- **40次FetchURL：39次取得相关内容，1次ACM 403**。细分：18个arXiv摘要页、3个公开Atom元数据请求、14个出版方/作者机构摘要页、2个公开论文PDF、2个Crossref身份元数据、1个失败的ACM页面。
- 只消费摘要/身份；ConANN额外核了§2.2/§3.1及§5.1.3的保障对象边界，不读整篇，不将工具返回长全文算精读。Block-Max PDF只用于首页作者/年份/摘要，本轮未审算法或实验表。
- 无专用学术数据源调用；Atom/Crossref均为FetchURL公开URL。外部只发送公共机制词、标题和ID，没有上传内部文档。

## 3. 实际WebSearch查询（全部2026-11-08）

| Q | 实际查询字符串 | 结果与处理 |
|---|---|---|
| R2Q01 | `层级检索 摘要遗漏 漏召回 回退 扩大搜索 论文` | 多为博客/二手材料；得到Mnemis及预算探索线索，不直接确认为原作 |
| R2Q02 | `learning to search long documents document structure Geva Berant 2018` | COLING2018正式页及1806.03529；补历史学得导航 |
| R2Q03 | `retrieval augmented generation conformal retrieval recall risk control TRAQ C-RAG` | TRAQ、C-RAG原作/正式入口 |
| R2Q04 | `DRAGIN SeaKR dynamic retrieval uncertainty active retrieval arxiv` | DRAGIN、SeaKR；Adaptive Retrieval Without Self-Knowledge已在目录，不新增 |
| R2Q05 | `approximate nearest neighbor adaptive search termination recall guarantee cost HNSW DiskANN` | Worst-case、Tao及动态终止线索 |
| R2Q06 | `"CONFLARE" conformal retrieval` | 2404.04287，直接面向检索阈值校准 |
| R2Q07 | `"query decomposition" "exploration" "retrieval" "budget" paper` | 2510.18633与EACL2026正式版 |
| R2Q08 | `"Improving Approximate Nearest Neighbor Search through Learned Adaptive Early Termination"` | SIGMOD2020作者机构摘要；另找到DARTH、ProS |
| R2Q09 | `"Coarse-to-Fine Question Answering for Long Documents"` | ACL2017正式页；另有2019/2021类似标题但本轮未核，不入表 |
| R2Q10 | `"conformal" "retrieval" "recall" candidate set 2025 2026` | CAS、Principled Context Engineering等线索，后者未核不计 |
| R2Q11 | `"HNSW" "DiskANN" "ScaNN" original paper` | 返回多为比较文章；只用作定位，不把博客速度对比当原论文 |
| R2Q12 | `"DiskANN: Fast Accurate Billion-point Nearest Neighbor Search on a Single Node"` | 找到NeurIPS2019原摘要地址 |
| R2Q13 | `"Accelerating Large-Scale Inference with Anisotropic Vector Quantization"` | PMLR119正式摘要/作者，关联1908.10396 |
| R2Q14 | `"Multi-Probe LSH" "Efficient Indexing"` | Princeton机构书目摘要/VLDB2007公开PDF |
| R2Q15 | `"Near-Optimal Hashing Algorithms" "Nearest Neighbor"` | 仅弱二手结果；未进一步核验，不收入确认，不反复重试 |
| R2Q16 | `"ProS" "progressive" "similarity" "quality guarantees"` | 原作2212.13310及VLDBJ出版线索 |
| R2Q17 | `"检索" "共形预测" "召回" 论文` | 中文结果噪声大，没有可直接确认的新中文原作；如实留缺口 |
| R2Q18 | `"ConANN" "Conformal" approximate nearest neighbor` | PVLDB19(1)原始PDF及VLDB2026程序入口 |
| R2Q19 | `"Stop" "retrieval" "sufficient" "evidence" adaptive RAG 2025 2026` | Stop-RAG、Cost-Aware等线索；DynaKRAG已收，不重复 |
| R2Q20 | `"Budget" "Search-R1" "retrieval" search cost 2025 2026` | AnySearch、FrugalRAG；未把Search-R1顺带占新增名额 |
| R2Q21 | `"摘要" "遗漏" "检索" "Mnemis"` | 官方博客/媒体；再查原作2602.15313和ACL正式摘要核验 |
| R2Q22 | `"Stop-RAG: Value-Based Retrieval Control for Iterative RAG"` | 2510.14337；Atom标NeurIPS2025 workshop，不写成主会 |
| R2Q23 | `"FrugalRAG" arxiv` | 2507.07634v1/v3及ICLR2026线索；同作去重，旧题保别名 |
| R2Q24 | `"Precise Zero-Shot Dense Retrieval without Relevance Labels" "Query2doc"` | **HTTP429失败**，未获得结果；不无限重试。HyDE随后Fetch原始ID，Query2doc改精确题名Q27 |
| R2Q25 | `"Efficient Query Evaluation Using a Two-Level Retrieval Process"` | IBM研究摘要、DOI；Crossref补完整作者 |
| R2Q26 | `"Faster Top-k Document Retrieval Using Block-Max Indexes"` | ACM出版页及作者NYU公开稿；ACM 403后只取作者主动公开稿 |
| R2Q27 | `"Query2doc" "Query Expansion"` | EMNLP2023原作与2303.07678 |
| R2Q28 | `"summary" "retrieval" "false negatives" evidence` | 主要命中训练负样本误标，与部署漏召回不是同问题；不以其充数 |
| R2Q29 | `"Mnemis: Dual-Route Retrieval" site:aclanthology.org` | 正式版2026.acl-long.1096，与预印本归并 |
| R2Q30 | `"TRAQ: Trustworthy" site:aclanthology.org` | 正式版2024.naacl-long.210，与预印本归并 |
| R2Q31 | `"Interactive Machine Comprehension with Information Seeking Agents" site:aclanthology.org` | 正式版2020.acl-main.211，与1908.10449归并 |

## 4. 实际FetchURL访问账（40次）

“摘要”意味着本轮消费范围，不表示服务器仅返回摘要。F编号仅本轮访问顺序，PDF入口未访问的仍只写候选卡入口。

| F | 实际URL | 状态/用途 |
|---|---|---|
| R2F01 | https://aclanthology.org/C18-1014/ | 成功；001正式摘要/完整作者 |
| R2F02 | https://arxiv.org/abs/2403.10081 | 成功；005摘要/版本史 |
| R2F03 | https://arxiv.org/abs/2406.19215 | 成功；006摘要 |
| R2F04 | https://arxiv.org/abs/2307.04642 | 成功；014摘要/版本 |
| R2F05 | https://proceedings.mlr.press/v235/kang24a.html | 成功；015正式摘要/作者/页码 |
| R2F06 | https://arxiv.org/abs/2310.19126 | 成功；027摘要 |
| R2F07 | https://arxiv.org/abs/2110.00696 | 成功；023摘要 |
| R2F08 | https://aclanthology.org/P17-1020/ | 成功；002正式摘要/作者 |
| R2F09 | https://arxiv.org/abs/2404.04287 | 成功；016摘要 |
| R2F10 | https://aclanthology.org/2026.eacl-long.322/ | 成功；009正式摘要/作者 |
| R2F11 | https://www.pdl.cmu.edu/PDL-FTP/BigLearning/mod0246-liA_abs.shtml | 成功；022作者机构摘要，SIGMOD2020 |
| R2F12 | https://arxiv.org/abs/2505.19001 | 成功；025摘要；搜索HTML日期与版本史不一致，以版本史分列 |
| R2F13 | https://arxiv.org/abs/2608.20771 | 成功；017摘要 |
| R2F14 | https://arxiv.org/abs/2507.00379 | 成功；028摘要/修订 |
| R2F15 | https://arxiv.org/abs/1603.09320 | 成功；018摘要/版本 |
| R2F16 | https://papers.nips.cc/paper_files/paper/2019/hash/09853c7fb1d3f8ee67a61b6bf4a7f8e6-Abstract.html | 成功；019正式摘要/作者；保留出版社拼写 |
| R2F17 | https://proceedings.mlr.press/v119/guo20h.html | 成功；020正式摘要/作者 |
| R2F18 | https://collaborate.princeton.edu/en/publications/multi-probe-lsh-efficient-indexing-for-high-dimensional-similarit/ | 成功；021机构书目/摘要，2007；不是2024同名新作 |
| R2F19 | https://arxiv.org/abs/2212.13310 | 成功；024摘要；2022线上/2023卷期不额外计作品 |
| R2F20 | https://www.vldb.org/pvldb/vol19/p29-horchidan.pdf | 成功；026首页摘要与§2.2/3.1/5.1.3保障对象定向核查P；不精读 |
| R2F21 | https://arxiv.org/abs/2602.15313 | 成功；004摘要/作者/版本 |
| R2F22 | https://arxiv.org/abs/2609.00813 | 成功；012摘要，确切标题有One Policy, Any Budget前缀 |
| R2F23 | https://aclanthology.org/2026.findings-emnlp.413/ | 成功；013完整正式题名为When Knowledge Is Not Free: Cost-Aware Evidence Selection in Retrieval-Augmented Generation |
| R2F24 | https://arxiv.org/abs/2212.10496 | 成功；007摘要 |
| R2F25 | https://arxiv.org/abs/2510.14337 | 成功；010摘要 |
| R2F26 | https://arxiv.org/abs/2507.07634 | 成功；011最新v3摘要；不得倒填为v1已有结果 |
| R2F27 | https://research.ibm.com/publications/efficient-query-evaluation-using-a-two-level-retrieval-process | 成功；029研究机构摘要 |
| R2F28 | https://dl.acm.org/doi/10.1145/2009916.2010048 | **失败403**；不重试、不登录、不绕过出版方限制 |
| R2F29 | https://aclanthology.org/2023.emnlp-main.585/ | 成功；008正式摘要；提取未带作者，后Atom补齐 |
| R2F30 | https://arxiv.org/abs/1908.10449 | 成功；003摘要 |
| R2F31 | 公开Atom请求A1（完整URL见下） | 成功；10个作品身份、作者、标题、版本，按ID关联 |
| R2F32 | 公开Atom请求A2（完整URL见下） | 成功；10个作品身份及别名 |
| R2F33 | https://research.engineering.nyu.edu/~suel/papers/bmw.pdf | 成功；030作者主动公开稿首页作者/摘要/年份，A；全文虽返回未精读 |
| R2F34 | https://api.crossref.org/works/10.14778/3772181.3772184 | 成功；026四位作者、卷期、印刷/在线日期分列 |
| R2F35 | https://arxiv.org/abs/2303.07678v2 | 成功；008版本史与摘要 |
| R2F36 | 公开Atom请求A3（完整URL见下） | 成功；008/015/020别名及作者 |
| R2F37 | https://aclanthology.org/2026.acl-long.1096/ | 成功；004正式题名/作者/摘要 |
| R2F38 | https://aclanthology.org/2024.naacl-long.210/ | 成功；014正式摘要；正文未读 |
| R2F39 | https://aclanthology.org/2020.acl-main.211/ | 成功；003正式摘要、作者/年份；Chris/Christopher保版本差异 |
| R2F40 | https://api.crossref.org/works/10.1145/956863.956944 | 成功；029完整作者/年份/页码/DOI别名 |

A1：https://export.arxiv.org/api/query?id_list=2403.10081,2406.19215,2307.04642,2310.19126,2110.00696,2404.04287,2505.19001,2608.20771,2507.00379,1603.09320&max_results=10

A2：https://export.arxiv.org/api/query?id_list=2212.13310,2602.15313,2609.00813,2510.14337,2507.07634,2212.10496,1908.10449,2510.18633,1806.03529,1611.01839&max_results=10

A3：https://export.arxiv.org/api/query?id_list=2303.07678,2402.03181,1908.10396&max_results=3

## 5. 身份/口径异常与暂缓队列

- **ConANN日期**：Crossref列published-print=2025-09、published-online=2026-01-08，VLDB程序为2026；三者分列，不按节目年份改写首发，不把两年拆两作。标题“distribution-free”不消除可交换性要求，平均FNR也不保证每个困难查询过线。
- **FrugalRAG题名变更**：v1/v2为Learning to retrieve and reason for multi-hop QA；v3为Less is More in RL Finetuning for Multi-Hop Question Answering；按2507.07634归并。ICLR2026入口只在搜索看见，未读取正式全文，不能宣称已核其全部结果。
- **Coarse-to-Fine QA**：ACL P17-1020题名与Atom的1611.01839v2题名Hierarchical Question Answering for Long Documents不同，作者/摘要高度对应，作为同一作品别名关联；正式版作者顺序以ACL为准。精读者须锁版本，不能混用页码。
- **Stop-RAG**：元数据为NeurIPS2025 MTI-LLM Workshop，不写成NeurIPS2025主会。
- **DARTH**：首稿2025-05-25、v2 2025-08-18；搜索HTML日期曾给2024-11-26，不采用。SIGMOD2026/DOI来自Atom备注和检索，正式版差异仍未读。
- **DiskANN作者**：NeurIPS页原拼写包含Fnu Devvrit与Ravishankar Krishnawamy；报告不从记忆静默替换，精读/编目者可进一步用PDF作者栏规范姓名。
- **待核而不计30项**：Near-Optimal Hashing Algorithms（Q15弱结果）；Principled Context Engineering for RAG（Q03/Q10）；Recall-Aware Early Termination（Q08机构入口）；HNSW with Accuracy Guarantees（Q05）；训练负样本误标2401.00165（Q28，与部署漏召回不同，暂缓）；GISA、Zero-Mem等中文搜索二手提及。未用未核作品补足数量。
- **近期模型**：本轮未新增追查V4/V4.1/K3。R1及审计的未读报告/版本疑点继续未知；不为核不稳的模型名耗尽预算。

## 6. 验收口径

报告只声明新增30项相对384项目录快照无冲突，不将它们擅自写入CATALOG或报告新的全项目总数。最后做只读检查：ID连续无重复、主键/别名与目录零重叠、30张卡的原始摘要与全文入口齐全、29A/1P、31查询/40访问行齐全、UTF-8与局部Git状态。无代码变更，不运行训练/构建/单元测试来替代文献核验；验证结果见扩展报告末节。
