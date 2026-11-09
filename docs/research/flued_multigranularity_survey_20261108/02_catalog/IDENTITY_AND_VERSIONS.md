# 身份归并、版本冲突与未完成追查（历史记录＋最新核销）

当前定版快照2026-11-08 07:28:11 +0800：543实体、230实际卡219FULL/11PARTIAL；身份/主键及K3同实体类型口径不变，当前范围优先FINAL_ADDENDUM_INDEX/READING_STATUS。
日期：2026-11-08。来源为8专题CANDIDATES/HANDOFF的可追溯记录；本轮不把继承的摘要核验升级独立外部审计。此文件不做科学综合。

## 30个跨专题重复实体（多计35次）

| W-ID | 原生键 | 主标题 | 全部专题local映射 | 出现/多计 |
|---|---|---|---|---|
| W0004 | arxiv:2103.06874 | CANINE: Pre-training an Efficient Tokenization-Free Encoder for Language Representation | [T01:C04](../01_search/T01/CANDIDATES.md#L35)、[T08-002](../01_search/T08/CANDIDATES.md#L16) | 2/1 |
| W0008 | arxiv:2305.07185 | MEGABYTE: Predicting Million-byte Sequences with Multiscale Transformers | [T01:C08](../01_search/T01/CANDIDATES.md#L59)、[T08-003](../01_search/T08/CANDIDATES.md#L22) | 2/1 |
| W0009 | arxiv:2404.14408 | SpaceByte: Towards Deleting Tokenization from Large Language Modeling | [T01:C09](../01_search/T01/CANDIDATES.md#L65)、[T08-005](../01_search/T08/CANDIDATES.md#L36) | 2/1 |
| W0010 | arxiv:2412.09871 | Byte Latent Transformer: Patches Scale Better Than Tokens | [T01:C10](../01_search/T01/CANDIDATES.md#L71)、[T08-007](../01_search/T08/CANDIDATES.md#L50) | 2/1 |
| W0011 | arxiv:2507.07955 | Dynamic Chunking for End-to-End Hierarchical Sequence Modeling | [T01:C11](../01_search/T01/CANDIDATES.md#L77)、[T08-008](../01_search/T08/CANDIDATES.md#L57) | 2/1 |
| W0014 | arxiv:2605.08044 | Fast Byte Latent Transformer | [T01:C14](../01_search/T01/CANDIDATES.md#L95)、[T08-011](../01_search/T08/CANDIDATES.md#L78) | 2/1 |
| W0016 | arxiv:1609.01704 | Hierarchical Multiscale Recurrent Neural Networks | [T01:C16](../01_search/T01/CANDIDATES.md#L109)、[T06-005](../01_search/T06/CANDIDATES.md#L37) | 2/1 |
| W0017 | arxiv:1708.06834 | Skip RNN: Learning to Skip State Updates in Recurrent Neural Networks | [T01:C17](../01_search/T01/CANDIDATES.md#L115)、[T06-006](../01_search/T06/CANDIDATES.md#L43) | 2/1 |
| W0023 | arxiv:1911.05507 | Compressive Transformers for Long-Range Sequence Modelling | [T01:C23](../01_search/T01/CANDIDATES.md#L151)、[T03-023](../01_search/T03/CANDIDATES.md#L160) | 2/1 |
| W0060 | arxiv:2312.04927 | Zoology: Measuring and Improving Recall in Efficient Language Models | [T02-004](../01_search/T02/CANDIDATES.md#L37)、[T05-023](../01_search/T05/CANDIDATES.md#L149) | 2/1 |
| W0061 | arxiv:2402.01032 | Repeat After Me: Transformers are Better than State Space Models at Copying | [T02-005](../01_search/T02/CANDIDATES.md#L43)、[T05-003](../01_search/T05/CANDIDATES.md#L33) | 2/1 |
| W0082 | arxiv:2401.18059 | RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval | [T02-026](../01_search/T02/CANDIDATES.md#L169)、[T03-001](../01_search/T03/CANDIDATES.md#L25)、[T04-005](../01_search/T04/CANDIDATES.md#L45)、[T07-045](../01_search/T07/CANDIDATES.md#L296)、[T08-039](../01_search/T08/CANDIDATES.md#L273) | 5/4 |
| W0083 | arxiv:2410.14052 | Dynamic Tree Memory Representation for LLMs | [T02-027](../01_search/T02/CANDIDATES.md#L175)、[T03-003](../01_search/T03/CANDIDATES.md#L37) | 2/1 |
| W0098 | arxiv:2502.11089 | Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention | [T02-042](../01_search/T02/CANDIDATES.md#L265)、[T04-009](../01_search/T04/CANDIDATES.md#L72)、[T05-046](../01_search/T05/CANDIDATES.md#L273) | 3/2 |
| W0115 | arxiv:2404.16130 | From Local to Global: A Graph RAG Approach to Query-Focused Summarization | [T03-009](../01_search/T03/CANDIDATES.md#L74)、[T04-024](../01_search/T04/CANDIDATES.md#L172) | 2/1 |
| W0117 | arxiv:2502.14802 | From RAG to Memory: Non-Parametric Continual Learning for Large Language Models | [T03-011](../01_search/T03/CANDIDATES.md#L86)、[T04-022](../01_search/T04/CANDIDATES.md#L159) | 2/1 |
| W0138 | arxiv:2402.09727 | A Human-Inspired Reading Agent with Gist Memory of Very Long Contexts | [T03-033](../01_search/T03/CANDIDATES.md#L222)、[T04-050](../01_search/T04/CANDIDATES.md#L341)、[T07-047](../01_search/T07/CANDIDATES.md#L308) | 3/2 |
| W0139 | arxiv:2310.05029 | Walking Down the Memory Maze: Beyond Context Limit through Interactive Reading | [T03-034](../01_search/T03/CANDIDATES.md#L228)、[T04-052](../01_search/T04/CANDIDATES.md#L354) | 2/1 |
| W0143 | arxiv:2306.07174 | Augmenting Language Models with Long-Term Memory | [T03-038](../01_search/T03/CANDIDATES.md#L254)、[T04-051](../01_search/T04/CANDIDATES.md#L348) | 2/1 |
| W0144 | arxiv:2203.08913 | Memorizing Transformers | [T03-039](../01_search/T03/CANDIDATES.md#L260)、[T04-047](../01_search/T04/CANDIDATES.md#L322) | 2/1 |
| W0148 | arxiv:2406.10774 | Quest: Query-Aware Sparsity for Efficient Long-Context LLM Inference | [T03-043](../01_search/T03/CANDIDATES.md#L286)、[T04-011](../01_search/T04/CANDIDATES.md#L86) | 2/1 |
| W0149 | arxiv:2402.04617 | InfLLM: Training-Free Long-Context Extrapolation for LLMs with an Efficient Context Memory | [T03-044](../01_search/T03/CANDIDATES.md#L292)、[T04-014](../01_search/T04/CANDIDATES.md#L106) | 2/1 |
| W0150 | arxiv:2306.14048 | H₂O: Heavy-Hitter Oracle for Efficient Generative Inference of Large Language Models | [T03-045](../01_search/T03/CANDIDATES.md#L298)、[T04-026](../01_search/T04/CANDIDATES.md#L186) | 2/1 |
| W0182 | arxiv:2310.11511 | Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection | [T04-033](../01_search/T04/CANDIDATES.md#L231)、[T07-040](../01_search/T07/CANDIDATES.md#L266) | 2/1 |
| W0183 | arxiv:2305.06983 | Active Retrieval Augmented Generation | [T04-034](../01_search/T04/CANDIDATES.md#L237)、[T07-041](../01_search/T07/CANDIDATES.md#L272) | 2/1 |
| W0184 | arxiv:2403.14403 | Adaptive-RAG: Learning to Adapt Retrieval-Augmented Large Language Models through Question Complexity | [T04-035](../01_search/T04/CANDIDATES.md#L243)、[T07-042](../01_search/T07/CANDIDATES.md#L278) | 2/1 |
| W0191 | arxiv:2307.03172 | Lost in the Middle: How Language Models Use Long Contexts | [T04-042](../01_search/T04/CANDIDATES.md#L291)、[T08-038](../01_search/T08/CANDIDATES.md#L265) | 2/1 |
| W0192 | arxiv:2502.05167 | NoLiMa: Long-Context Evaluation Beyond Literal Matching | [T04-043](../01_search/T04/CANDIDATES.md#L297)、[T08-036](../01_search/T08/CANDIDATES.md#L251) | 2/1 |
| W0193 | arxiv:2404.06654 | RULER: What's the Real Context Size of Your Long-Context Language Models? | [T04-044](../01_search/T04/CANDIDATES.md#L304)、[T08-034](../01_search/T08/CANDIDATES.md#L239) | 2/1 |
| W0340 | arxiv:2411.06037 | Sufficient Context: A New Lens on Retrieval Augmented Generation Systems | [T07-043](../01_search/T07/CANDIDATES.md#L284)、[T08-043](../01_search/T08/CANDIDATES.md#L300) | 2/1 |

RAPTOR出现5次、多计4次；ReadAgent/NSA各出现3次、多计2次；其余27个交叉作品各出现2次、多计1次。合计4+2+2+27=35。所有已知论文/正式版别名在CATALOG原卡身份列保留。

## 不能因同名/相近机制强并的作品

- T02-012与013：2019集合函数限制和2021/2022通用逼近为不同作品；Deep Sets是第三作。
- T02-035 Decodable IB与T02-038 Deterministic IB：同缩写DIB，目标/ID不同。
- T02-021 LIMIT理论限制与T02-015单向量强弱讨论：不同作品，理论量词尚未对齐，不能说互相推翻或同一稿。
- H-Net与H-NET++；A-Mem与AgeMem；MemoryLLM 2402.04624与未确认的2602.00398；HippoRAG与HippoRAG2；InfLLM与InfLLM-V2：分别保留不同作品，系统名相近不强并。
- FG²-GDN/FG²-GDN+属2604.19021同作变体；Gated DeltaNet-2 2605.22791、Dual DeltaNet 2610.38578是另外两作。机制优先权需逐版核，不因都解耦擦写而合并。
- LoLA与HOLA、MARCH与MERLIN分别不同作品；压缩载荷/地址统计的形式差别尚待全文。
- SSA/H-SSA、MoG/MoGG、BLT-D/S/DV、ToMe预印本/会议、TokenLearner长短题均按原卡关联一作；不是多篇。

## 已知版本/身份冲突与必须执行的下一步

| 本地线索/映射 | 风险/不能作的推断 | 下一步及目前状态 |
|---|---|---|
| T01-C30 / W0030 / arxiv:2610.13858 | LapMerge历史版本冲突已由发现审计A02核销：v1 2026-10-09、v2 2026-10-12。 | 身份版本已解决；[审计凭据](../05_review/DISCOVERY_AUDIT_R1.md)；全文改钉v2，正文版差仍待读，不能继续把已核身份说未知。 |
| T01-C31 / W0031 / arxiv:2508.13204 | QuickMerge++撤回提示可能来自相邻列表，原站429；既不能说已撤回也不能视作有效性能证据。 | 合法核单作品comment/版本；历史发现仍计，性能引用冻结；未完成。 |
| T01-C45 / W0045 / arxiv:2501.16075 | PISCO arXiv摘要48小时、ACL摘要24小时，不能混引最有利数字。 | 钉正式版设置与硬件/数据，必要时逐版成本表；未完成。 |
| T01-C53 / W0053 / arxiv:2409.06679 | E2LLM 2024首发、2026 v3，最新评测不能倒填首发。 | v1/v3的训练、评测及目标差异；未完成。 |
| T01-C26 / W0026 / arxiv:2106.11297 | TokenLearner NeurIPS短题与扩展长题明确关联，但扩展贡献差异未读。 | 同W-ID保留版本比较，不新增作品；未完成。 |
| T01-C32 / W0032 / arxiv:2409.01179 | Recoverable Compression的AAAI正式页反自动访问阻断。 | 不绕过，使用合法公开正式索引/作者稿核对应；arXiv入口保留；未完成。 |
| T02-029 / W0085 / arxiv:2405.19504 | MUVERA 2024稿到2026 v2可能有证明修订；不把搜索“corrected”当证明错误已定位。 | 必须读v2，记录相较v1的具体修正与保证；未完成。 |
| T04-023 / W0174 / arxiv:2603.28458 | HISA v1–v5，AttentionIndex可能比较旧版；HiSA大小写非新作品。 | B01已有全文卡及v1–v5局部比较；仍缺AttentionIndex实际HISA版本/commit、同预算代码核查，不把旧版比较当v5反证。 |
| T04-003 / W0159 / arxiv:2602.01219 | MiTA v1 Efficient Fast-Weight Scaling…到v6 Mixture-of-Top-k Attention…；摘要实验在视觉。 | 归并一ID，逐版机制/会议终稿/因果掩码核验；未完成。 |
| T04-001 / W0157 / arxiv:2606.19348 | DeepSeek-V4编号2606与所见公开日期04-26不一致，不能自行校正首发。 | 原始历史与官方报告交叉核，来源审计反馈后再修；未完成。 |
| T04-002 / W0158 / arxiv:2609.19969 | V4.1仅引言读取；890 bytes/token为global KV，非全部持久/局部状态。 | 补完整方法与表项边界，不从引言填机制细节；未完成。 |
| T04-004 / W0160 / official:github.com/MoonshotAI/Kimi-K3 | K3 README/报告入口已发现，报告未读、commit未固定。 | 仍按官方介绍实体不计论文；固定版本后读真实报告；未完成。 |
| T06-049 / W0294 / official:longcat.chat/blog/longcat-2.0/ | LongCat2只有官方发布页，暂无本轮核验的论文ID/报告。 | 不占论文精读配额，追官方报告/实现及分级索引消融；未完成。 |
| T03-019 / W0125 / arxiv:2606.01435 | 2606.01435 v1 Don’t Ask…到v2 Reliable Post-Retrieval Assembly…，主结论收窄。 | 同W-ID；读v2及v1，分离抽取/执行与freshness收益；未完成。 |
| T03-003 / W0083 / arxiv:2410.14052 | MemTree旧长题/新短题、2024/2025版本；不是两篇。 | 主标题用新短题，保留旧题映射；版本内容未比。 |
| T03-025 / W0130 / arxiv:2508.03341 | Nemori 2508.03341旧题Self-Organizing…与ACL2026 What Deserves Memory…。 | 同W-ID，正式摘要/旧稿两端已由专题关联，正文差异未核。 |
| T03-046 / W0151 / arxiv:2403.19708 | AttentionStore旧题与CachedAttention新题。 | 同2403.19708，位置编码/重定位保证仍待读。 |
| T03-047 / W0152 / arxiv:2405.16444 | CacheBlend早期题不含for RAG、2025 v3。 | 同2405.16444，不能引用更新功能为初稿结果；未比。 |
| T03-016 / W0122 / arxiv:2601.02845 | TiMem 2026正式页与2601.02845关系来自搜索，最早日期尚未独立核。 | 保一实体，待正式元数据核作者/预印本对应；未完成。 |
| T03-036 / W0141 / acl:2026.acl-demo.27 | Hindsight有ACL2026 demo正式页，首次预印本ID/日期待补。 | 保正式ACL稳定键，未来只挂别名不新增；未完成。 |
| T05-005 / W0202 / arxiv:2605.22791 | Gated DeltaNet-2与FG²-GDN+擦写解耦优先权需对齐v1/v3。 | Q中提升T05-028作伴读，逐式逐版比，尚未判定。 |
| T05-038 / W0234 / arxiv:2501.00663 | Titans编号2501但源卡记首发2024-12-31；编号不代替投稿史。 | 保源卡时间冲突提醒，正式引用前核历史；未完成。 |
| T05-044 / W0240 / arxiv:2008.02217 | Hopfield编号2008与源卡所记v1 2020-07-16不一致。 | 不自行推断日期，核版本史；不拆作品；未完成。 |
| T05-050 / W0245 / arxiv:2605.05189 | Sharp Capacity Thresholds旧/新题，目标由top-1到列表有不同条件。 | 同2605.05189；版本贡献、k/n极限与固定小k不可混引；未完成。 |
| T05-051 / W0246 / arxiv:2601.15313 | Attention Is Not Retention旧题Mind the Gap…，绝对正交必要措辞未接受。 | 同2601.15313，核固定外积规则/任意线性学习的量词；未完成。 |
| T05-052 / W0247 / openreview:zXMvCvXYE0 | OpenReview验证码墙；ICLR官方简介不是已核主会录用证明。 | 保OpenReview稳定ID，合法全文入口，核轨道/作者；未完成。 |
| T06-018 / W0263 / arxiv:2510.13876 | GateSkip预印本What Layers When…与正式Learning to Skip Compute…。 | 同2510.13876；正式版差异未比。 |
| T06-024 / W0269 / arxiv:2510.25741 | Ouro v1–v6、学深度不等于公开实现真早停。 | 钉v6与执行实现，旧稿不同训练/评价不可混引；未完成。 |
| T06-028 / W0273 / arxiv:2607.15456 | Looped Latent Attention的exact是缓存量核算，不是输出无损。 | 记录精确性对象，读时重建和输出影响另报；未完成。 |
| T07-003 / W0303 / arxiv:1003.3967 | Adaptive Submodularity v5修复Theorem13证明，并附加强条件/较弱覆盖保证。 | 只引用v5，旧版覆盖界不能直接引用；全文复核未完成。 |
| T07-009 / W0309 / pmlr:r15/pu17a | Learning to Acquire Information的2026 PMLR重刊非新作品。 | 首发UAI2017不改；原稿公开链接保留，正式页历史待核。 |
| T07-034 / W0334 / arxiv:2403.03375 | Complexity Matters预印本含Dynamics…、正式版删去Dynamics。 | 同2403.03375；题名异名保一作，正文差异未比。 |
| T07-048 / W0343 / arxiv:2512.24601 | Recursive Language Models v3可能新增后训练结果。 | v3和v1分列证据时间，不把v3结果倒填2025首发；未完成。 |
| T07-018 / W0318 / arxiv:2412.08052 | CANDOR 2024稿到2026 v2及CHIL身份待正式实体页确认。 | 同2412.08052；正式题名、作者、标签结论/设置差异未核。 |
| T08-013 / W0357 / arxiv:2610.11790 | 2610.11790与2610.22100不同ID、同作者相邻研究，可能重用数据/实验。 | 发现审计A26/A27确认两ID同作者/仓库；B05 W0357卡称后作引用并复用流水线/语料。暂两作品一相关簇，目录未独立裁决替代/非替代；W0358独立卡仍待B14。 |
| T08-041 / W0381 / arxiv:2603.26668 | Bridge-RAG编号2603与源卡所记v1=01-12不一致。 | 核原始元数据/版本史，不按编号自动改日期；未完成。 |
| T08-030 / W0374 / arxiv:2408.15510 | 2408.15510早期长题与2025.ijcnlp-long.47正式短题。 | B08卡已读正式版及v1/v3/v4/v5局部比较，完整阅读可计；v2未读、逐版全文差分未做，不称版本全部审完。 |
| T08-042 / W0382 / arxiv:2410.12380 | Attribution Bias早版题名无Generator-Aware、正式题名增修。 | 同2410.12380/2025.findings-acl.1087，不新增；正文差异未比。 |
| T08-001 / W0351 / arxiv:2105.13626 | ByT5 config两次失败，MambaByte/bGPT源码失败或猜路径404。 | ByT5 W0351卡已作Large配置限定静态核验：编码/解码输入共享、输出头不共享；不能外推其他尺寸/依赖commit。MambaByte/bGPT仍未核，分别保留未知。 |

## 已在其他专题确认的“未核线索”：回指而不新增

- T04待核2410.01736、T08 adRAP：已由T03-002确认为 **W0109** Recursive Abstractive Processing for Retrieval in Dynamic Datasets；全局只计一次。
- T02待核“Scaling Linear Attention Capacity with Sparse State Expansion”可能指 **W0205** arXiv:2507.16577（已确认题名Scaling Linear Attention with Sparse State Expansion）；标题相近但缺原始入口对应，先核是否同作，不另计未确认作品。
- T05交接推测MoM/LoLA/MARCH等“很可能被他专题发现”不作为事实；本快照实际映射只有CATALOG所列，不凭推测造重复。

## R2历史未确认入口与阻塞登记（当时385实体/208候选；部分已由本轮升级，见EXPANSION_MERGE_R2）

以下是追查任务，不声称额外有这么多独立论文；同一主题短语可能没有单篇作品，题名截断处保持截断。入口来自已读取的HANDOFF，T07 U1–U7另核SEARCH_LOG原表。

| 来源 | 入口/问题 | 追查动作与未完成原因 |
|---|---|---|
| T01 | DTM-Codec；TR-PTS；PuMer；视频合并/导航/模仿学习压缩 | 仅检索发现未核摘要；先确认原始题名/ID，再评是否提供同码信号比较。 |
| T02 | Wyner–Ziv1976；Rimoldi1994；Gray–Wyner1974 | 只有参考链，补原始稿/摘要与编码权限；三经典方向不按二手引文加确认数。 |
| T02 | 2609.14421；OpenReview TUKrrXWMN2的Granular Information Bottleneck for Deep Multi-… | 身份/完整题名、状态或摘要未核；不要按名字granular认同构。 |
| T02 | 2005.10242；2608.04074 | 只有发现/片段，后者精确身份不明；按训练几何/KV相关性决定追查。 |
| T03 | MemoryArena2602.16313；DynamicMem2606.22877；Agent-Native Memory System2606.24775 | 未取原始摘要，先核身份及是否测真正源删除/控制面。 |
| T03 | HaluMem2511.03506；AgentMemBench2608.00009；BEAM2510.27246；2026-10 PARSER | 仅线索，完整题名/状态未核；不要当已有确认作品补数。 |
| T03 | HiFC；LMCache技术报告；2026 SSD serving；query-driven selective recomputation | 只有系统/关键词线索，先消歧版本/论文/官方介绍，补冷存储和失效成本。 |
| T03 | MemoryLLM2602.00398；二手综述HAT | 同名异作/身份未核；不得同2402.04624强并或按缩写计数。 |
| T04 | Breaking the Static Graph2602.01965；HiChunk；Hierarchical Re-ranker Retriever | 题名/摘要或身份未核，先找原始页；后两者不补猜ID。 |
| T04 | VectifyAI PageIndex；LongRAG同名多副标题 | 先确认官方系统/报告及作者ID，不作为论文实体默认入库。 |
| T04 | SpargeAttention2 2602.13515；SLA2 2602.12675；SpecSA2605.19893；Lighthouse2605.06554 | 原摘要未取，按稀疏路由/投机/块召回缺口逐一核。 |
| T04 | Certified Sparse Attention via Perturbed Retrieval | 只公开PDF线索、年份/定理未核；不能称已有可用召回保证。 |
| T05 | The Capacity of Modern Hopfield Networks under the Data Manifold Hypothesis 2503.09518 | 两次abs只得页脚；下一轮合法PDF/作者稿核身份与摘要，不无限重试。 |
| T06 | 2605.05222；2609.17251；OpenReview0SF6Kr1lrx | 仅发现，动态路由/持续状态/Leap-of-Thought方向先身份核验。 |
| T06 | 2605.13190；2604.18396；2610.00815；2402.13934 | 仅发现，精确早退/KV共享/真省算，先核exact所指对象。 |
| T06 | 2603.19714；2605.12466；2605.20670；TF-Engram2607.07388 | LoopRPT/固定点/线性循环/SSD路线只作入口，未核摘要。 |
| T06 | Phased LSTM；2506.21103；γ-MoD | 身份/摘要未核，不凭熟悉标题补齐细节或计数。 |
| T07 U1 | Learning Robot Metareasoning… https://arxiv.org/html/2610.23662v1 | 只搜索片段，核真实计算预算和semi-MDP前提。 |
| T07 U2 | Uncertainty-Guided Counterfactual Sensor Selection… https://arxiv.org/html/2610.35344v1 | 只搜索片段，核固定识别响应与自然反事实效应。 |
| T07 U3 | Evaluation of Active Feature Acquisition Methods for Time-… http://jmlr.org/papers/volume26/23-1635/23-1635.pdf | 题名截断；先核完整身份及与静态AFA同作/伴作关系。 |
| T07 U4 | Doubly-Robust Estimation of Counterfactual Policy Mean Embeddings https://neurips.cc/virtual/2025/poster/120338 | 未Fetch官方介绍；分布型估计是否补尾部效用待核。 |
| T07 U5 | Adaptive Sequence Submodularity https://arxiv.org/html/1902.05981v2 | 只发现，核顺序动作保证而非集合效用。 |
| T07 U6 | Deep GraphRAG… https://arxiv.org/html/2601.11144v3 | 未核身份/摘要/来源回访，不能按层级名收同构。 |
| T07 U7 | EventMemAgent: Hierarchical Event-Centric Memory… https://media.eventhosts.cc/Conferences/ECCV2026/pdfs/11561.pdf | 标题截断、作者/状态待核；不补猜正式题名。 |
| T07 | Just a Good Task Weighting | 尚未定位；错误2202.01093已确认是X射线研究并排除，不重新当候选。 |
| T08 | MrT5 2410.20771；Tokenizer Tax2607.24276；EntropyMoE2608.06398 | 只发现或引用命中，先原摘要再决定相关性。 |
| T08 | Token-Native Storage2608.02376 | 仅搜索片段且日期矛盾，先原始元数据核验。 |

## 仍未完成的元数据工程

- R2当时385个实体并不都已有完整作者表、DOI和正式会议版本；本轮已复用发现审计28对象身份记录，见METADATA_UPDATES_R2。源卡未知作者明确保留“—/待补”，不从提交人猜作者；CATALOG逐专题身份记录可回溯缺字段。T07-029完整作者尤其需要正式PDF/BibTeX补核。
- T07-024正式ICLR页、T07-018 CHIL页、T07-046 AAAI DOI及多项只经arXiv comment的会议身份尚未逐项核完；以预印本稳定键保留，不扩大正式录用主张。
- 本负责人本轮未新增网络查询/下载，故没有虚构新的检索日志或称外链全部可用。需要主代理将独立来源审计的新证据按W-ID回填；遇暂时失败1–2次重试，拒绝不绕过。
- R2当时实际terra卡FULL38/PARTIAL2，限定ByT5配置静态核验1、实验复现0；详见READING_STATUS。目录本人没有精读或科学裁决，旧“精读0”仅属R1整合历史。

## R2历史已核销身份及当时缺口

- H-MEM W0111作者为Haoran Sun、Shaoning Zeng，题名补H-MEM:；W0156补Beyond the Reranker:前缀；旧短题别名不新增作品。LapMerge版本已核身份不再阻塞。详细逐对象凭据见[METADATA_UPDATES_R2](METADATA_UPDATES_R2.md)。
- HMT按覆盖审计v1身份/定向正文新增W0385，最新版未核、无terra完整卡；X001补充待排，不占原167中本次80。
- LoCoMo会话/问题数、B04证明与B03统计等卡列争议仅待核；本目录未亲自检查原文，不宣布论文错误。

## 最新：R2扩展入库及120卡版差核销

- 152扩展卡逐项入EXPANSION_MERGE_R2：HMT复用W0385，151净新追加W0386–W0536。T07-072/082的旧比较ID不是别名，不能误合并；其它跨扩展同键/明确别名/规范题名未检出重复。保守合簇继续保守，不为数量拆稿。
- HMT v3/NAACL2025含Efficient题名、六作者包括Yingqi Cao，旧v1五作者另记；原X001已入B20，不再称v3全未知。目录仅复用T03第一手记录，未亲自精读。
- SATFormer W0288按v3改题Learning When to Use Early Value Residuals…并补作者；MemoRAG W0153按v3/WWW新题与七作者记主行、保v1旧题/五作者；DISRetrieval W0380的v1/v5不同题名和增作者不拆作品。ReMemR1/MemTree/MemoRAG卡已补读后版，不等于所有版逐字审过。
- MrT5、Geva/Berant、LMCache、HiFC、T07时变特征评价、DBSP等原待核引用链已升级确认实体，旧待核表仅历史线索，具体local→W/全文入口见EXPANSION_MERGE_R2；Wald/Weitzman/Russell等仍未达专题摘要核验者不补猜。
- RDD McCauley/McCauly、DiskANN Fnu Devvrit、中文作者OCR和非标准DOI留待锁原PDF/作者栏，不把名字近似拆人或猜全；博士论文PDF未取得不算全文。
- 阅读者提出的数学/统计/实现疑点请转[独立红队](../05_review/READING_AUDIT_R1.md)按分类和范围处理；本目录未验证新反例，不将曾疑点升级错误，也不将已定位的局部问题泛化整作失效。


## 最新R4：审计回填与补证

- 参见[AUDIT_METADATA_SYNC](AUDIT_METADATA_SYNC.md)：只回R1/R2/R3明确已核身份字段，不联网猜全；W0425按所核v2二作者规范并留历史差异，DeepControl五/四作者冲突分版双记，PISCO同正式版24/48h并列；W0483旧R3解除已撤销，现以R4局部符号/可修复边界为准。
- B22/B24恢复中读取快照不得由旧审计PARTIAL固定；当前READING_STATUS给卡/总结指纹。B25/B26补20而非200FULL数量目标，全部与前200互斥，作品总数不增。
- 新卡理论/统计疑点指向独立审计；未经核销不升为错误，已核局部问题也不推翻整作。


## 最新R5：停新增批次、保留身份和未读分类

所有W-ID及主键不变，534学术＋2官方按实盘复核；B01–B26实际220尝试。覆盖R2没有新增外部作者认证，已核书目保留、冲突不擅定。OPEN_ITEMS区分材料未取/作者未给自有证明/尚未读，未尝试候选139和储备175另列，不叫访问失败。当前先综合/红队再决定是否定向补查，不新造B27或裁定数学争议。


## 最新R6归并与待核

- 新7 relation实体W0537–W0543，6卡只占其中6；4近期卡复用W0157/58/59/60，NSA只旧W0098卡复核；主/正式/arXiv/Git别名不重复计作品。
- K3旧official主键保留为历史稳定键，类型已升固定技术报告，Git commit锁对象不等发布日期或main README完全同版；无额外W-ID。新类型账542学术＋1介绍对比旧534＋2差7发现＋1重分类，详FINAL_ADDENDUM_INDEX。
- R4撤回R3 W0483解除、DeepControl基线错误解释；最新终审CRC还需可达端点，不把历史解除/待核文字当最新事实。目录不自行核销数学争议、原初期PARTIAL按卡不升级。
