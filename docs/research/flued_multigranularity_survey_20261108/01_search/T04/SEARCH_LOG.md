# T04 首轮文献发现：检索日志

日期：2026-11-08。范围：查询条件粗到细检索、动态稀疏访问、压缩后路由、摘要遗漏、探索与回退、漏召回。执行依据：`../../PLAN.md`；仅写本目录，不改源码、现有证据表或总目录，不训练、不提交、不再派代理。

## 1. 实际完成量与口径

- 去重确认 **53 个候选作品/系统**：**52 篇论文/技术报告 + 1 个官方模型仓库介绍**（Kimi K3）。全部达到身份与摘要/官方介绍核验，不把仓库介绍计为论文。
- 阅读深度：**48 篇仅摘要核验，4 篇有定向全文片段核查，1 个仅官方仓库介绍；全文精读 0，代码核验 0**。4 篇为 T04-001/002/007/017。
- **26 项标记“精读优先”**，逐项问题见 `CANDIDATES.md`，建议排程见 `HANDOFF.md`。
- 首次公开日期处于近12个月（2025-11-08—2026-11-08）的论文 **14 篇**，另有2026年的 K3 官方介绍；HiQA 的2026年更新不再计新作品。
- 实际执行 **30 条 WebSearch**：29 条返回结果，1 条 HTTP 429；后以带 PISA 的改写查询取得结果，不无限重试。
- 实际执行 **64 次 FetchURL**：52 个 arXiv 摘要页、1 个官方 GitHub、4 个 arXiv HTML、4 个公开 Atom 元数据 URL、2 个正式出版摘要页、1 个 OpenReview 页面。最后一项只返回验证墙，不算取得论文内容；其余取得用于核验的内容。HTML 取得不等于整篇读完。
- 使用内置浏览器补查 K3 官方仓库的 Full Report 链接，确认指向 `k3_tech_report.pdf`；未阅读该 PDF。临时浏览器页已关闭。
- 未使用专用学术数据源工具；公开 arXiv Atom URL 仅通过 FetchURL 取得元数据，不调用数据源插件、不上传任何内部文件。

术语说明：本报告中的“摘要失明”只是用户问题的中文简称，指用于路由的摘要没有保留未来问题所需细节，不在此新注册机制名。KV 指注意力中的键/值状态；RAG 指检索增强生成，即先访问外部文本再供模型生成；预填充指处理已有输入前缀的阶段。英文作品名与其作者提出的机制在候选卡中配中文释义，不代表项目术语转正。

## 2. 实际查询记录

平台均为 WebSearch，日期均为2026-11-08；保持实际查询字符串，不将补写的理想检索式当成已执行记录。Q编号表示调用顺序，不表示完整学术覆盖。

| ID | 实际查询 | 返回/用途 |
|---|---|---|
| Q01 | `DeepSeek V4 V4.1 CSA HCA CSA2 CED sparse attention technical report` | 找到2606.19348、2609.19969及二手解读；只以原报告确认机制 |
| Q02 | `arxiv 2602.01219 MiTA` | 找到MiTA摘要、v1/v6及官方代码入口 |
| Q03 | `MoonshotAI Kimi-K3 github technical report` | 找到官方组织/仓库；二手参数口径不一致，不据此取值 |
| Q04 | `hierarchical retrieval summary coarse to fine source documents RAPTOR HiRAG QuIM RAG` | 找到HiRAG及2026树检索线索；未核实的QuIM不入确认表 |
| Q05 | `dynamic sparse attention query compression routing missed tokens Quest SparQ MoBA NSA` | 找到SSA、DashAttention、Twilight及后续稀疏检索线索 |
| Q06 | `RAPTOR Tree Organized Retrieval 2401.18059 HiQA HiRAG HippoRAG 2 LongRAG arxiv` | 确认RAPTOR入口；另得动态RAPTOR维护2410.01736，未进一步核验，不计候选 |
| Q07 | `2026 hierarchical retrieval summary blind spots coarse fine routing source recovery attention arxiv` | 找到HiKEY、AttentionIndex、PISA线索 |
| Q08 | `"Quest" "SparQ" "MoBA" "Native Sparse Attention" arxiv` | 返回多篇参考文献及Twilight；只作导航 |
| Q09 | `"Block Sparse Attention with Log-Linear Complexity"` | **失败：HTTP 429 rate_limit_reached_error**；没有结果，不作发现证据 |
| Q10 | `"InfLLM-V2" "arxiv"` | 确认为2509.24663；避免把猜测ID当成作品 |
| Q11 | `"HiQA" "LongRAG" hierarchical arxiv` | 确认HiQA 2402.01767、MAL 2501.16952；LongRAG存在同名歧义，本轮未收入 |
| Q12 | `"Block Sparse Attention with Log-Linear Complexity" PISA` | Q09的定向改写；确认2609.31093 |
| Q13 | `"HippoRAG 2" arxiv` | 确认2502.14802；另得Breaking the Static Graph线索，未核验 |
| Q14 | `"summary" "retrieval" "blind" "2026" compression arxiv` | 找到InMind、压缩后重取成本、透明压缩、A-RAG线索 |
| Q15 | `"SSA" "Simplified Sparse Attention" arxiv gist` | 核对SSA完整标题及v2、官方代码入口 |
| Q16 | `"AttentionIndex" "2611.02508"` | 核对完整标题；搜索有无关结果，不纳入 |
| Q17 | `"DeepSeek-V4" "2606.19348" technical report` | 核对完整标题与原报告HTML；不依赖媒体架构图 |
| Q18 | `"Semantic Compression Trees" "2608.21610"` | 核对SCT完整标题和原文入口 |
| Q19 | `"FLARE" "Adaptive-RAG" "Self-Route" retrieval arxiv` | 返回多为综述/博客；后直接取各原作摘要，不把综述当原作 |
| Q20 | `"Lost in the Middle" "NoLiMa" "RULER" long context benchmark` | 确认NoLiMa并导向原作；覆盖非字面匹配反例 |
| Q21 | `"PLAID" "ColBERT" "Routing Transformer" "Memorizing Transformers"` | 联合查询效果弱，主要返回Memorizing Transformers；后使用已知标题/ID的原始摘要页核验 |
| Q22 | `"Landmark Attention" "ReadAgent" gist retrieval` | 找到ReadAgent官方项目及出版入口；发现二手会议标注不一致 |
| Q23 | `"ReadAgent" "arxiv"` | 找到2402.09727，但也有错误题名/错误引用；以原文和PMLR纠正 |
| Q24 | `"MemWalker" "arxiv"` | 找到2310.05029；部分综述错作者/截断ID不采信 |
| Q25 | `"Mix-of-Granularity" chunking retrieval arxiv` | 找到2406.00456和COLING2025正式版 |
| Q26 | `"Landmark Attention: Random-Access Infinite Context Length for Transformers"` | 确认标题、作者与NeurIPS2023相关版本，不重复计数 |
| Q27 | `"PLAID: An Efficient Engine for Late Interaction Retrieval"` | 确认标题、作者与ACM DOI，避免将2025网页日期误作发表年 |
| Q28 | `"DashAttention" "2605.18753"` | 确认完整标题、作者和官方仓库 |
| Q29 | `"HISA" "2603.28458"` | 确认标题；与AttentionIndex的HiSA比较关联，版本需继续核对 |
| Q30 | `"A Human-Inspired Reading Agent" site:proceedings.mlr.press` | 确认ReadAgent正式版为ICML2024/PMLR235，而非搜索中出现的ICLR会议页口径 |

## 3. 逐批原始来源账本

以下每个ID均实际调用过 `https://arxiv.org/abs/<ID>`，不是仅凭记忆登记。标题、作者、最新版本后用公开Atom元数据补齐。每个作品卡给出摘要/版本/PDF链接，避免在本日志重复53张卡。

| 批次 | 实际取得的原始摘要ID/页面 | 作用 |
|---|---|---|
| F01 | 2606.19348；2609.19969；2602.01219；https://github.com/MoonshotAI/Kimi-K3 | 草案近期入口独立核验 |
| F02 | 2401.18059；2503.10150；2604.20920；2611.02508 | 树检索、摘要词元展开、最新索引 |
| F03 | 2502.11089；2502.13189；2406.10774；2312.04985；2409.10516；2402.04617 | 可训练/推理时稀疏访问与原缓存回访 |
| F04 | 2605.18753；2605.29606；2608.21610；2502.02770 | 自适应预算、结构路由、直接反例 |
| F05 | 2509.24663；2609.31093；2402.01767；2502.14802；2603.28458；2404.16130；2501.16952 | 多层索引、知识图、不同抽象级别 |
| F06 | 2306.14048；2404.14469；2309.17453；2407.02490；2502.20766；2503.16428；2401.15884；2310.11511 | 永久裁剪对照、预填充稀疏、纠错/自反思 |
| F07 | 2305.06983；2403.14403；2407.16833；2212.10509；2602.03442；2607.24368；2608.16370；2610.20116 | 探索、策略切换、隐式关联、回访成本 |
| F08 | 2307.03172；2502.05167；2404.06654；2004.12832；2205.09707；2203.08913；2003.05997 | 反例评价与经典内容路由 |
| F09 | 2305.16300；2402.09727；2306.07174；2310.05029；2406.00456 | 地标、gist来源回看、记忆树、粒度路由 |

### 公开元数据补查（FetchURL）

四个实际URL，均返回Atom条目与摘要；仅用来补齐身份、作者、版本和出版备注。API返回顺序不等于请求顺序，按arXiv ID关联。

1. https://export.arxiv.org/api/query?id_list=2606.19348,2609.19969,2602.01219,2401.18059,2503.10150,2604.20920,2611.02508,2605.18753,2605.29606,2608.21610,2502.02770,2609.31093,2402.01767,2502.14802,2501.16952&max_results=15
2. https://export.arxiv.org/api/query?id_list=2502.11089,2502.13189,2406.10774,2312.04985,2409.10516,2402.04617,2509.24663,2603.28458,2404.16130,2306.14048,2404.14469,2309.17453&max_results=12
3. https://export.arxiv.org/api/query?id_list=2407.02490,2502.20766,2503.16428,2401.15884,2310.11511,2305.06983,2403.14403,2407.16833,2212.10509,2602.03442,2607.24368,2608.16370&max_results=12
4. https://export.arxiv.org/api/query?id_list=2610.20116,2307.03172,2502.05167,2404.06654,2004.12832,2205.09707,2203.08913,2003.05997,2305.16300,2402.09727,2306.07174,2310.05029,2406.00456&max_results=13

### 正式版本/定向全文入口（FetchURL）

- https://arxiv.org/html/2604.20920v2 ：取得HTML；实际定向核查摘要、图1说明、§3.5–3.6及相关检索片段，**不是全文精读**。
- https://arxiv.org/html/2608.21610v1 ：取得HTML；实际定向核查摘要与§7，**不是全文精读**。
- https://arxiv.org/html/2606.19348v1 ：取得HTML；实际核查§2.3相关片段，**不是全文精读**。
- https://arxiv.org/html/2609.19969v1 ：提取仅到引言；可核验CSA2三模式与CED介绍，不能声称已读方法全章。
- https://aclanthology.org/2025.coling-main.384/ ：正式版摘要与作者、页码、PDF；与2406.00456合并计1项。
- https://proceedings.mlr.press/v235/lee24c.html ：正式版摘要与完整引用；与2402.09727合并计1项。
- https://openreview.net/forum?id=GN921JHCRw ：只返回“Complete the check below”验证墙；不登录、不绕过、不重复抓取。RAPTOR仍有arXiv摘要核验，正式出版页核验深度不足须保留。
- K3浏览器所见报告入口：https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf 。**没有读取PDF内容或固定commit**；不能将当前README等同于完整报告的技术结论。

## 4. 失败、排除与未核验线索

- Q09一次429；Q12改写后成功。其他搜索未发现需要无限重试的情况。
- OpenReview验证墙未绕过。工具把arXiv HTML保存到会话缓存并不表示研究文件已保存整篇；交接统一给公开URL，不依赖本机临时路径。
- 本地Atom整理第一次因Windows默认GBK输出作者重音字符失败，设置 `PYTHONIOENCODING=utf-8` 后成功；仅处理公开元数据，没有修改项目脚本。
- Q22/Q23的一些页面把ReadAgent误写成别的标题、别的arXiv编号或ICLR；原始2402.09727和PMLR为准。
- K3二手页面出现2.6T等不同数字，**本轮仅记录官方README当前2.8T口径及其69 KDA + 24 Gated MLA表格**；版本演变/首次发布时间未核实，性能表不外推。
- 动态RAPTOR维护2410.01736、Breaking the Static Graph 2602.01965、LongRAG同名作品、HiChunk、PageIndex、LongMemEval-V2、SpargeAttention2、SLA2、SpecSA、Lighthouse：本轮只发现入口，未逐一取得身份+摘要，**全部不计53项**。供下一轮按机制缺口择取，不把二手综述引文直接升级为确认。
- 尚未系统检索经典近似最近邻搜索的召回保证、可认证稀疏注意力、探索预算理论、稀有数值/否定事实/跨语种反例；未核验的标题不填充确认表。

## 5. 阶段判断

本轮形成真实首批，而非一页种子表，也不是全域覆盖。最接近“压缩表示定位→按需读原始细节”的已核验作品至少包括Landmark Attention、ReadAgent、MemWalker、NSA、SSA/H-SSA、A-RAG；它们的训练、存储、因果约束很不相同，不能用一个“多粒度”标签宣告同构或创新。SCT、InMind、AttentionIndex和压缩后交互成本论文构成必须并行精读的反例链。建议继续**定向扩展并先精读**，原因是已出现可能改变架构选择的最近邻与反例，而不是为了凑更多篇数。
