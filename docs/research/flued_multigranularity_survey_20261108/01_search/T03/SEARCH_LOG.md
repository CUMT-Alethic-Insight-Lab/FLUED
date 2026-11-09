# T03 首轮检索日志

日期：2026-11-08。所有者：T03 研究写作代理。范围：层级/压缩/检索记忆、来源映射、原文保留与回访、外置/重算/淘汰、时间更新一致性。

## 边界与实计

- 已读取本调研 `PLAN.md`；只写本目录的三个 Markdown 文件，未修改源码、现有证据表或术语表，未训练、提交、使用付费资源或另派代理。
- 使用 WebSearch 与 FetchURL；未使用学术数据源、浏览器登录会话或内部资料上传。对外查询均为公共机制词/公开作品名称。
- **40 次实际 WebSearch 调用：38 次返回结果，2 次 HTTP 429。58 次 FetchURL 调用：52 次获得可用摘要/官方介绍，5 次网络失败，1 次 PDF 返回乱码而不可用。52 次可用抓取对应 51 个去重作品，额外一次为 Nemori 的预印本/正式版关联核验。**
- **确认候选 51 个，精读优先 P1 28 个，其余 P2 23 个；全文精读 0、代码核验 0。**部分 HTML 页面返回全文，但本轮只消费其摘要或开头机制简介；没有据此冒充完整阅读。检索发现但未完成身份+摘要双核验的额外线索不计入 51。
- 年份采用首次公开年份，正式版年份另注。题名/版本改动合并；注意 Nemori、CachedAttention、Reliable Post-Retrieval Assembly 三个实例不能按新旧标题重复计数。
- 近 12 个月窗口定义为 **2025-11-08—2026-11-08**。2025-10 的首版不是此窗口的新工作；2026 修订/正式发表只算更新事件。

## 实际检索式

平台均为 WebSearch，日期均为 2026-11-08。下表保留原查询字符串；结果是发现入口，不是论断依据。确认依据见后面的 Fetch 台账与 `CANDIDATES.md`。

| 批次/序号 | 实际查询 | 结果与用途 |
|---|---|---|
| A/Q01 | `hierarchical memory summary source pointers original text retrieval RAPTOR MemTree HAT memory language models` | MemTree、CAM、HAT 线索；HAT 未独立核验，不计数 |
| A/Q02 | `MemGPT MemoryBank Generative Agents HippoRAG hierarchical memory provenance retrieval` | MemoryOS 正式页与记忆系统谱系入口 |
| A/Q03 | `2025 2026 hierarchical memory recursive summaries raw conversations agent memory update consistency` | ReFind 反例、H-MEM；非学术产品页面排除 |
| A/Q04 | `long term memory LLM memory consolidation forgetting temporal update benchmark LongMemEval LoCoMo` | LycheeMemory V2、TiMem、评测线索；厂商排行榜不作证据 |
| B/Q05 | `RAPTOR recursive abstractive processing tree organized retrieval arxiv` | RAPTOR、动态维护后续；检索片段出现错误 arXiv 号，采用主页面核验号 |
| B/Q06 | `MemGPT MemoryBank Generative Agents arxiv memory storage retrieval reflection` | 三个早期记忆系统的引用链与 RMM |
| B/Q07 | `HippoRAG 2 GraphRAG Zep temporal knowledge graph arxiv` | Zep 与时间冲突解决线索 |
| B/Q08 | `LongMem MemoryLLM Long-LLMLingua Compressive Transformer recurrent memory transformer arxiv` | 内部表示记忆/显存边界；LongMem 号与 Memory3 |
| C/Q09 | `"MemGPT" "MemoryBank" "Generative Agents" arxiv 2310 2304` | 多词过约束，有大量无关结果；仅保留可后续主页面核验的入口 |
| C/Q10 | `"HippoRAG" "HippoRAG 2" arxiv` | 2405.14831、2502.14802 与官方代码入口 |
| C/Q11 | `"GraphRAG" "From Local to Global" arxiv` | **失败：HTTP 429**；未原样循环重试，已知公开标识后用原始页面核验 |
| D/Q12 | `"A-MEM: Agentic Memory" arxiv` | A-Mem；另一个同名 Agentic Memory/AgeMem 单独核验 |
| D/Q13 | `"Mem0" "Memory OS" "TiMem" memory arxiv` | TiMem ACL 页与 Mem0 号 |
| D/Q14 | `"Nemori" "Reflective Memory Management" arxiv` | **失败：HTTP 429**；之后分开搜索，不持续重试 |
| E/Q15 | `Compressive Transformer long range sequence modelling arxiv` | 1911.05507；用于内部压缩状态对照 |
| E/Q16 | `LongMem Memorizing Transformers Memory3 MemoryLLM arxiv memory` | LongMem 正式论文、Memory3；发现 **MemoryLLM 同名异作**，2602.00398 未加入确认表 |
| E/Q17 | `LongMemEval LoCoMo MemoryAgentBench Nemori arxiv benchmark` | Nemori 2508.03341 与 ACL 2026 正式版 |
| F/Q18 | `"LongMemEval" "arxiv" "2410"` | 2410.10813；意外发现来源保留最近邻 Eywa |
| F/Q19 | `"Evaluating Very Long-Term Conversational Memory" arxiv` | LoCoMo 2402.17753 |
| F/Q20 | `"MemoryAgentBench" arxiv 2025` | 2507.05257；ForgetEval、LME-V2、LightMem 与未核验评测线索 |
| G/Q21 | `ReadAgent A Human-Inspired Reading Agent with Gist Memory arxiv MemWalker` | **ReadAgent 原文回访最近邻**；附录 H 对树导航的反例线索 |
| G/Q22 | `MemWalker Navigating Long Texts through Interactive Reading arxiv` | MemWalker 2310.05029；树摘要+查询导航 |
| G/Q23 | `HiAgent MemoRAG Hindsight hierarchical memory arxiv original retrieval` | HiAgent、Hindsight 正式页；**HORMA 原轨迹链接最近邻** |
| H/Q24 | `"Memorizing Transformers" arxiv` | 2203.08913 |
| H/Q25 | `"M+: Extending MemoryLLM" arxiv` | 2502.00592、MemoryLLM 2402.04624；ReMemR1 回访线索 |
| H/Q26 | `"InfLLM" "Quest" KV cache arxiv` | 内存层级/块级检索；有片段误引 Quest 为 2402.05074，未采用 |
| I/Q27 | `"Quest: Query-Aware Sparsity" arxiv` | 正确号 **2406.10774** 与官方项目 |
| I/Q28 | `"InfLLM: Training-Free" arxiv` | 2402.04617 |
| J/Q29 | `"H2O: Heavy-Hitter Oracle" arxiv` | 2306.14048；不可恢复淘汰对照 |
| J/Q30 | `"CacheBlend" "AttentionStore" arxiv KV cache` | 2405.16444、2403.19708；选择重算/外置缓存 |
| J/Q31 | `"MemoRAG" arxiv memory inspired knowledge discovery` | 2409.05591；全局压缩记忆引导原始证据检索 |
| K/Q32 | `"Efficient Memory Management" "PagedAttention" arxiv` | 2309.06180；逻辑/物理页映射，不等于语义摘要 |
| K/Q33 | `"Recursively Summarizing Books with Human Feedback" arxiv` | 2109.10862；递归摘要祖先与摘要损失对照 |
| L/Q34 | `"2606.01435" title` | 发现旧题 Don’t Ask… 已改为 Reliable Post-Retrieval Assembly；**新摘要对旧结论显著收窄** |
| L/Q35 | `"2509.23040" title` | ReMemR1 完整题名核对 |
| L/Q36 | `"Memory OS of AI Agent" arxiv` | 2506.06326 与 EMNLP 2025 关联；未核验的 Agent-Native 等留下一轮 |
| M/Q37 | `"2403.19708" "CachedAttention" title` | 旧名 AttentionStore 与新题名同一作品 |
| M/Q38 | `"Reliable Post-Retrieval Assembly for Agent Memory"` | 当前完整题名与新版摘要对齐 |
| M/Q39 | `"RAPTOR" "ICLR 2024" "2401.18059"` | 正式版引用入口；新发现强重排器下层级摘要无显著收益的反例 2606.28367 |

## 原始来源抓取台账

每行列出实际 FetchURL URL，编号对应 `CANDIDATES.md`。未加版本的 arXiv 摘要页按抓取时页面的最新摘要解读；摘要页版本历史可复核。全文入口统一列于候选卡，不表示全文已读。

| ID | 实际可用 FetchURL 来源 | 本轮实际消费范围 |
|---|---|---|
| 001 | https://arxiv.org/abs/2401.18059 | 摘要、v1 日期 |
| 002 | https://arxiv.org/abs/2410.01736 | 摘要、v1 日期 |
| 003 | https://arxiv.org/abs/2410.14052 | 摘要、v1–v3 历史 |
| 004 | https://arxiv.org/abs/2510.05520 | 摘要 |
| 005 | https://arxiv.org/abs/2507.22925 | 重试后摘要 |
| 006 | https://arxiv.org/abs/2310.08560 | 摘要、v1/v2 历史 |
| 007 | https://arxiv.org/abs/2305.10250 | 摘要 |
| 008 | https://arxiv.org/abs/2304.03442 | 摘要 |
| 009 | https://arxiv.org/html/2404.16130v2 | 返回长 HTML，只用摘要与开头介绍；未精读 |
| 010 | https://arxiv.org/html/2405.14831v1 | 返回长 HTML，只用摘要与开头介绍；未精读 |
| 011 | https://arxiv.org/abs/2502.14802 | 摘要、v1/v2 历史 |
| 012 | https://arxiv.org/abs/2501.13956 | 摘要 |
| 013 | https://arxiv.org/abs/2502.12110 | 摘要、v1–v11 历史 |
| 014 | https://arxiv.org/abs/2504.19413 | 摘要 |
| 015 | https://aclanthology.org/2025.emnlp-main.1318/ | 正式题名、作者、摘要、DOI |
| 016 | https://aclanthology.org/2026.findings-acl.1091/ | 正式题名、作者、摘要、DOI |
| 017 | https://aclanthology.org/2025.acl-long.413/ | 正式题名、作者、摘要、DOI |
| 018 | https://arxiv.org/abs/2608.12888 | 最新摘要、v1/v2 历史 |
| 019 | https://arxiv.org/abs/2606.01435 | **v2 摘要**、v1/v2 历史；旧标题仅作关联 |
| 020 | https://arxiv.org/abs/2608.12990 | 最新摘要、v1/v2 历史 |
| 021 | https://arxiv.org/abs/2609.30797 | 摘要 |
| 022 | https://arxiv.org/abs/2601.01885 | 摘要、v1–v3 历史 |
| 023 | https://arxiv.org/abs/1911.05507 | 摘要 |
| 024 | https://arxiv.org/abs/2407.01178 | 作者、摘要、期刊关联 |
| 025 | https://aclanthology.org/2026.acl-long.1607/ ; https://arxiv.org/abs/2508.03341 | 正式版与预印本相同 Nemori 机制及题名演变；计一项 |
| 026 | https://arxiv.org/abs/2410.10813 | 摘要、v1/v2 历史 |
| 027 | https://arxiv.org/abs/2402.17753 | 摘要 |
| 028 | https://arxiv.org/abs/2507.05257 | 摘要、至 v4 的历史 |
| 029 | https://arxiv.org/abs/2605.30771 | 摘要 |
| 030 | https://arxiv.org/abs/2510.18866 | 摘要、至 2026-02 v4 的历史 |
| 031 | https://arxiv.org/abs/2605.12493 | 摘要 |
| 032 | https://arxiv.org/abs/2606.15903 | 摘要、v1/v2 历史 |
| 033 | https://arxiv.org/abs/2402.09727 | 完整题名、摘要、v1–v3 历史 |
| 034 | https://arxiv.org/html/2310.05029 | 返回长 HTML，只用摘要与开头机制介绍；未精读 |
| 035 | https://aclanthology.org/2025.acl-long.1575/ | 正式题名、作者、摘要、DOI |
| 036 | https://aclanthology.org/2026.acl-demo.27/ | 正式题名、作者、摘要、DOI |
| 037 | https://arxiv.org/abs/2606.11680 | 完整题名、摘要 |
| 038 | https://proceedings.neurips.cc/paper_files/paper/2023/hash/ebd82705f44793b6f9ade5a669d0f0bf-Abstract-Conference.html | 正式出版摘要；不用乱码 PDF |
| 039 | https://arxiv.org/abs/2203.08913 | 摘要 |
| 040 | https://arxiv.org/abs/2502.00592 | 摘要、v1/v2 历史 |
| 041 | https://arxiv.org/abs/2402.04624 | 作者、摘要 |
| 042 | https://arxiv.org/abs/2509.23040 | 摘要、至 2026-03 v5 的历史 |
| 043 | https://arxiv.org/abs/2406.10774 | 摘要、v1/v2 历史 |
| 044 | https://arxiv.org/abs/2402.04617 | 摘要、v1/v2 历史 |
| 045 | https://arxiv.org/abs/2306.14048 | 作者、摘要 |
| 046 | https://arxiv.org/abs/2403.19708 | **v3 CachedAttention 摘要**、历史 |
| 047 | https://arxiv.org/abs/2405.16444 | 摘要、v1–v3 历史 |
| 048 | https://arxiv.org/abs/2409.05591 | 最新摘要、v1–v3 历史 |
| 049 | https://arxiv.org/abs/2309.06180 | 摘要 |
| 050 | https://arxiv.org/abs/2109.10862 | 摘要、v1/v2 历史 |
| 051 | https://arxiv.org/abs/2606.28367 | 摘要 |

## 失败、误导片段与停止规则

1. 网络失败：`https://arxiv.org/abs/2507.22925` 首次失败，隔批同 URL 一次重试成功。
2. 网络失败：`https://arxiv.org/abs/2404.16130`、`https://arxiv.org/abs/2405.14831` 各一次；改用公开 arXiv HTML 后成功，没有绕过拒绝访问。
3. 网络失败：`https://arxiv.org/abs/2306.07174` 一次；转正式出版页。首先 Fetch `https://proceedings.neurips.cc/paper_files/paper/2023/file/ebd82705f44793b6f9ade5a669d0f0bf-Paper-Conference.pdf` 返回二进制乱码，**不可作为摘要/全文证据**；随后正式摘要页成功，不再尝试 PDF 转换。
4. 网络失败：`https://arxiv.org/abs/2310.05029` 一次；公开 HTML 成功。
5. Q11/Q14 为服务限流而非“无论文”；不把失败解释成文献空缺。各对象仅按合法公开入口有限追查。
6. 搜索引擎日期存在明显错配，例如带 2026 编号的 HTML 被标成 2024 日期；统一使用 arXiv submission history / ACL 正式年份，不采信搜索结果日期。
7. RAPTOR、Quest 被其他片段错引编号；主页面分别确认 `2401.18059` 与 `2406.10774`。
8. `MemoryLLM: Plug-n-Play Interpretable Feed-Forward Memory for Transformers`（2602.00398）与 2402.04624 不是同一作品。前者只见搜索结果，未抓取摘要，**不计确认候选**，也不与后者合并。
9. 暂存但未核验：HAT、AgentMemBench(2608.00009)、BEAM(2510.27246)、HaluMem(2511.03506)、MemoryArena(2602.16313)、DynamicMem(2606.22877)、Are We Ready For An Agent-Native Memory System?(2606.24775)、MemRefine(2606.13177)、HiFC、LMCache 技术报告、2026-10 的 PARSER、Evidence-Refining Graph Diffusion。均不计数、不转述性能为事实。

## 本轮覆盖与未覆盖

已覆盖：静态/增量摘要树、可回访原文、跨粒度反思、时间图、证据与事实分离、可控原文搜索反例、版本装配边界、遗忘/删除评测、内部向量记忆、缓存分页/外置/选择重算。

尚未完成：逐页全文精读、代码/工件复核、独立复现实验、完整作者表补齐、所有正式版实体页匹配；2026-09—11 的最新工作只做零散发现，不能声称穷尽近 12 个月。持续事务更新、源文档撤销后祖先摘要与缓存级联失效、真实持久存储字节/活跃显存联合账单仍是决定性缺口，详见 HANDOFF。

## 元数据收尾检索

| 批次/序号 | 平台/日期 | 实际查询 | 结果 |
|---|---|---|---|
| N/Q40 | WebSearch / 2026-11-08 | `"HasMem" "2609.30797"` | 原始 arXiv 页面搜索结果补齐完整题名：HasMem: Hard-Origin Adaptively Softened Memory for Long-Term LLM Agents。摘要此前已 Fetch 核验，不新增作品、不新增 Fetch。 |
