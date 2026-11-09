# T03 首轮候选：层级记忆、来源回访与生命周期

日期：2026-11-08。**51 个去重、身份与摘要/官方介绍已核验作品；P1 精读优先 28 项，P2 23 项；全文精读 0，代码核验 0。**全部只是发现/摘要层初筛，不代表 terra 全文证据卡，不据此背书新模型性能或裁定架构新颖性。

## 读法、口径与分类

- **核验 A**：原始 arXiv 摘要/官方出版摘要已抓取；标题由官方页面或搜索结果中的该原始页面对应，作者不齐处明确留空。作者栏“—”意为尚未可靠补齐，不能把 arXiv 提交者当作者。
- **E 外部记忆**：文本、图、文件或数据库等模型外存储；作者称“memory”不使它自动变成模型内部状态。
- **W 工作记忆**：单次任务中的上下文管理，通常仍是文本摘要/工具调用，不必跨会话持久化。
- **I 内部表示记忆**：隐藏向量、键值缓存或可更新潜在状态；与可检索原文及可解释来源指针不同。
- **S 服务缓存**：物理存储/加载/重算机制，不是语义摘要机制。
- **B 评测**：用于暴露更新、遗忘、证据收集失败；不算提出另一套记忆架构。
- 持久存储指跨调用保留的信息；活跃显存指当次推理驻留加速器的状态。摘要未报告 CPU/磁盘/GPU 分布时标“未核”，不把低 token 数当低显存，也不把外置数据量当活跃显存。
- 每项“关联/支持/反例潜力”分开：**摘要明示机制**是作者所述；与本专题的支持/反例价值是本轮推断；未精读，不为关键机制编造节号、页码或数值对照。
- “多级摘要+来源指针+查询回访”拆为三个独立条件。摘要证明“树/摘要/检索”不等于已证明节点有稳定源区间映射、能回原文，更不等于固定层数或字节级地址。

## 最近邻先读

最接近组合且应先排查同构：**034 MemWalker**（摘要树+查询导航）、**033 ReadAgent**（gist 摘要+原文 lookup；非多级树）、**005 H-MEM**（多级抽象+下层索引）、**037 HORMA**（层级摘要实体+原始轨迹链接+查询导航）、**004 CAM**（层级摘要+在线整合+自适应探索）。RAPTOR 是多级摘要检索基础，但不能把跨层检索自动说成逐层下钻。来源不可变和时间一致性另读 **029 Eywa、012 Zep、019 新版后检索装配、032 ForgetEval**。

两个强制相反对照：**018 ReFind**（原文+词法可控搜索可挑战结构化记忆必要性）；**051 强重排器研究**（层级摘要等增强在其受控条件下无可靠增益）。仅凭“分层/压缩/回访”三词，当前已不能主张组合空白。

## A. 层级摘要、外部记忆与更新

### T03-001 · P1 · RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval
- 作者/年份/版本：Parth Sarthi 等；2024；arXiv v1，ICLR 2024 引用关联，不重复计数。
- 身份与全文：[arXiv:2401.18059](https://arxiv.org/abs/2401.18059)；[PDF](https://arxiv.org/pdf/2401.18059)。核验 A，E。
- 摘要明示：递归 embedding、聚类、摘要形成多抽象层级树，推理从树检索。支持潜力：多级摘要组合的直接祖先。反例潜力：摘要丢细节，跨层检索可能比强制走树更有效；此处不是已验证结论。
- 生命周期/成本：外部文本索引；叶文与节点精确映射、增删重建、设备驻留未核。**精读问题：tree traversal 与 collapsed-tree 是否分离；保留哪些原文叶；源区间可否稳定回查；每查询索引摊销成本多少？**

### T03-002 · P1 · Recursive Abstractive Processing for Retrieval in Dynamic Datasets
- 作者：—；年份/版本：2024，arXiv v1。
- 身份与全文：[arXiv:2410.01736](https://arxiv.org/abs/2410.01736)；[PDF](https://arxiv.org/pdf/2410.01736)。核验 A，E。
- 摘要明示：针对文档增删维护递归抽象树；另有 query-focused 递归抽象后检索层。支持潜力：RAPTOR 动态维护不是无人区；直接覆盖增删生命周期。
- 生命周期/成本：增删算法已在摘要声称；并发、版本与删除级联未核。**精读问题：删除一条来源时受影响聚类/祖先摘要怎样定位；一致性是即时还是最终；维护工作量与全量重建如何比较？**

### T03-003 · P1 · Dynamic Tree Memory Representation for LLMs
- 作者：Alireza Rezazadeh 等（作者全表待补）；年份/版本：2024 首版；2025-03 v3。旧标题含 From Isolated Conversations to Hierarchical Schemas，合并。
- 身份与全文：[arXiv:2410.14052](https://arxiv.org/abs/2410.14052)；[PDF](https://arxiv.org/pdf/2410.14052)。核验 A，E，方法 MemTree。
- 摘要明示：节点保存聚合文本、语义 embedding 与不同深度抽象；新信息通过相似度动态整合。支持潜力：动态层级记忆最近邻；反例潜力：严格包含可能不利跨主题证据，须原文验证。
- 生命周期/成本：在线树变更；原始消息是否不可变、上层是否重写未核。**精读问题：写入路径、合并阈值和祖先更新；检索是不是走树；原文能否独立召回；与 RAPTOR 重叠聚类的比较是否同预算？**

### T03-004 · P1 · CAM: A Constructivist View of Agentic Memory for LLM-Based Reading Comprehension
- 作者：—；年份/版本：2025-10，v1；首版不在近 12 个月窗口内。
- 身份与全文：[arXiv:2510.05520](https://arxiv.org/abs/2510.05520)；[PDF](https://arxiv.org/pdf/2510.05520)。核验 A，E。
- 摘要明示：增量重叠聚类、层级摘要、在线批次整合，推理自适应探索记忆结构。支持潜力：多级抽象+查询条件访问+在线整合已同作出现。
- 生命周期/成本：动态插入明确；来源持久性、重叠造成冗余与原文回访未核。**精读问题：探索停止/回退策略；跨分支遗漏；摘要更新与源文撤销；构建成本和查询成本是否一并比较？**

### T03-005 · P1 · H-MEM: Hierarchical Memory for High-Efficiency Long-Term Reasoning in LLM Agents
- 作者：**Haoran Sun、Shaoning Zeng**；年份/版本：2025，v1；方法 H-MEM。R2 已据 [arXiv 原始 BibTeX](https://arxiv.org/bibtex/2507.22925) 修正首轮第二作者错名；HTML 正文题名前缀与 BibTeX 无前缀题名为同作，不另计。
- 身份与全文：[arXiv:2507.22925](https://arxiv.org/abs/2507.22925)；[HTML v1](https://arxiv.org/html/2507.22925v1)；[PDF](https://arxiv.org/pdf/2507.22925)。首轮核验 A，E；R2 定向读 §3.1—3.3，非全文精读。
- 摘要明示：按语义抽象多级组织、更新；每个 memory vector 含指向下一层子记忆的位置索引，索引路由逐层检索。**这是“多级+来源方向指针+查询下钻”的强最近邻，但指向子记忆不等于指向原始文本。**
- R2 正文补核：§3.1/Figure 2 四层为 Domain、Category、Memory Trace、Episode，Episode 同存文本/向量；§3.2 为自身/子节点离散索引，沿指针 top-k，四层为作者选择，另提供可调层级接口；§3.3 按用户反馈调权重，不能充作删除级联失效协议。§3.1 的事件/画像提取意味着“complete contextual memory”不能直接解作原始对话逐字无损保存。
- **后续精读问题：**原始对话是否另存、稳定源跨度和多源支持如何表示；父节点改写后索引稳定性；漏路由能否回退；撤销是否清理文本/向量/祖先；与强近似近邻索引及完整维护成本的比较。R2 仅修 T03，不回写总表。

### T03-006 · P1 · MemGPT: Towards LLMs as Operating Systems
- 作者：Charles Packer 等；年份/版本：2023 首版，2024-02 v2；不把 Letta 后续产品一概等同论文。
- 身份与全文：[arXiv:2310.08560](https://arxiv.org/abs/2310.08560)；[PDF](https://arxiv.org/pdf/2310.08560)。核验 A，E/W。
- 摘要明示：借鉴操作系统的虚拟上下文管理，LLM 控制快慢层级之间的信息移动及中断。支持潜力：上下文/外存分离与回访控制已有经典基线。
- 生命周期/成本：上下文与慢存储是逻辑层级，不能直接说是 GPU/SSD 实测分页。**精读问题：core/recall/archival 各保存什么；摘要和原文哪项永久保留；溢出丢弃还是外置；调用次数、延迟和失败回退？**

### T03-007 · P2 · MemoryBank: Enhancing Large Language Models with Long-Term Memory
- 作者：Wanjun Zhong 等；年份/版本：2023，v1–v3；正式版年份未单独核齐。
- 身份与全文：[arXiv:2305.10250](https://arxiv.org/abs/2305.10250)；[PDF](https://arxiv.org/pdf/2305.10250)。核验 A，E。
- 摘要明示：回忆、持续更新、用户特征综合；借遗忘曲线按时间和重要性遗忘/强化。支持潜力：淘汰策略祖先；反例潜力：拟人化遗忘不等于任务充分保留。
- 生命周期/成本：外部记忆；原文/摘要是否各自可删与恢复未核。下一步：区分遗忘评分、真实物理删除、摘要派生遗留与用户撤销语义。

### T03-008 · P2 · Generative Agents: Interactive Simulacra of Human Behavior
- 作者：Joon Sung Park 等；年份/版本：2023，v1/v2。
- 身份与全文：[arXiv:2304.03442](https://arxiv.org/abs/2304.03442)；[PDF](https://arxiv.org/pdf/2304.03442)。核验 A，E。
- 摘要明示：保存完整自然语言经历，形成高层 reflection 并动态召回。支持潜力：原始事件+抽象反思+检索的早期组合，不能当作纯摘要删原文。
- 生命周期/成本：完整经历是持久文本，不是完整 KV 永驻显存。下一步：反思节点引用证据编号是否可追溯，时间/重要性/相关性评分是否掩盖检索遗漏；行为可信度不是事实恢复率。

### T03-009 · P1 · From Local to Global: A Graph RAG Approach to Query-Focused Summarization
- 作者：Darren Edge 等（完整作者表待补）；年份/版本：2024 首版，核验 HTML v2；方法 GraphRAG。
- 身份与全文：[arXiv:2404.16130v2](https://arxiv.org/html/2404.16130v2)；[PDF](https://arxiv.org/pdf/2404.16130)。核验 A，E。
- 摘要明示：原文→实体图→community summaries，查询时部分回答再汇总。支持潜力：图社区层级摘要已覆盖全局抽象；不能等同逐层原文回访。
- 生命周期/成本：离线图/摘要索引与查询文本分开；可达原文、全局摘要过期与重建未核。**精读问题：社区级别是否固定；实体/摘要/源 text unit 映射；全局问题与细粒度事实的对照；索引和多路回答成本？**

### T03-010 · P2 · HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models
- 作者：Bernal Jiménez Gutiérrez 等；年份/版本：2024，核验 HTML v1；NeurIPS 2024 引用关联。
- 身份与全文：[arXiv:2405.14831v1](https://arxiv.org/html/2405.14831v1)；[PDF](https://arxiv.org/pdf/2405.14831)。核验 A，E。
- 摘要明示：LLM、知识图谱、个性化 PageRank 整合知识；单步图检索替代部分迭代调用。支持潜力：多跳来源关联不必构造摘要树。
- 生命周期/成本：图索引/文本证据与内部网络状态不同。下一步：实体到段落映射、增量知识更新是否只是加入而非矛盾解决；抽取遗漏不能由图遍历自动修复。

### T03-011 · P1 · From RAG to Memory: Non-Parametric Continual Learning for Large Language Models
- 作者：Bernal Jiménez Gutiérrez 等；年份/版本：2025，v1/v2；HippoRAG 2，ICML 2025 引用关联。
- 身份与全文：[arXiv:2502.14802](https://arxiv.org/abs/2502.14802)；[PDF](https://arxiv.org/pdf/2502.14802)。核验 A，E。
- 摘要明示：对前代图方法在简单事实记忆上的退化提出修正，增加 passage integration 与在线 LLM 使用。支持潜力：图抽象接回原始段落；**反例潜力：结构化关联可能伤害普通事实检索**，摘要本身明确指出。
- 生命周期/成本：非参数持续知识整合不等于时间版本一致性。**精读问题：段落节点与实体节点怎样连接；事实任务退化如何修复；同模型同检索预算是否成立；“持续学习”有没有删除/覆盖实验？**

### T03-012 · P1 · Zep: A Temporal Knowledge Graph Architecture for Agent Memory
- 作者：Preston Rasmussen 等；年份/版本：2025，v1。
- 身份与全文：[arXiv:2501.13956](https://arxiv.org/abs/2501.13956)；[PDF](https://arxiv.org/pdf/2501.13956)。核验 A，E。
- 摘要明示：Graphiti 时间感知知识图整合对话与业务数据，并维护历史关系。支持潜力：时间更新、来源与事实图层的直接相邻基线。
- 生命周期/成本：外部服务；存储层级、历史回滚、显存未核。**精读问题：事件时间/写入时间是否分开；冲突使旧边失效还是删除；证据原文保留在哪里；上层社区摘要如何失效；更新延迟计入否？**

### T03-013 · P2 · A-Mem: Agentic Memory for LLM Agents
- 作者：Wujiang Xu、Zujie Liang、Kai Mei、Hang Gao、Juntao Tan、Yongfeng Zhang；年份/版本：2025，至 v11；NeurIPS 2025 引用关联。
- 身份与全文：[arXiv:2502.12110](https://arxiv.org/abs/2502.12110)；[PDF](https://arxiv.org/pdf/2502.12110)。核验 A，E。
- 摘要明示：新记忆生成结构化 note、关键词、标签，动态链接旧记忆，触发旧表示和属性更新。支持潜力：动态来源网络/记忆演化；不是固定摘要树。
- 生命周期/成本：原始 evidence 是否不可变未核。下一步：旧记忆重写有无版本链、反向链接和矛盾标识；写放大及难撤销派生信息。

### T03-014 · P2 · Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory
- 作者：Prateek Chhikara 等；年份/版本：2025，v1；正式版关联待出版实体页补齐。
- 身份与全文：[arXiv:2504.19413](https://arxiv.org/abs/2504.19413)；[PDF](https://arxiv.org/pdf/2504.19413)。核验 A，E。
- 摘要明示：从会话动态提取、整合、检索显著信息；图变体表示关系。支持潜力：生产式外部事实记忆基线；反例潜力：抽取后细节/出处可能不可恢复。
- 生命周期/成本：摘要报告 token/延迟收益并不证明含全生命周期成本或显存下降。下一步：原始聊天/事实/图三者保存与删除关系；评测 judge 口径与长上下文基线是否统一。

### T03-015 · P2 · Memory OS of AI Agent
- 作者：Jiazheng Kang、Mingming Ji、Zhe Zhao、Ting Bai；年份/版本：2025；EMNLP 正式版。预印本 2506.06326 为搜索关联入口，未另计。
- 身份与全文：[ACL 2025.emnlp-main.1318 / DOI](https://aclanthology.org/2025.emnlp-main.1318/)；[PDF](https://aclanthology.org/2025.emnlp-main.1318.pdf)。核验 A，E。
- 摘要明示：short/mid/long 三层；storage/update/retrieval/generation 四模块；对话链 FIFO 转移、分段 page 组织。支持潜力：固定三层与动态迁移的直接相邻组合。
- 生命周期/成本：这里 page 是文本组织，不必是显存物理页。下一步：来源回访是原始文本还是仅长期 profile；何种淘汰不可逆；为何层数固定与是否有层数消融。

### T03-016 · P1 · TiMem: Temporal-Hierarchical Memory Consolidation for Long-Horizon Conversational Agents
- 作者：Kai Li 等；年份/版本：2026；ACL Findings 正式版；arXiv 2601.02845 仅搜索关联，不另计。
- 身份与全文：[ACL 2026.findings-acl.1091 / DOI](https://aclanthology.org/2026.findings-acl.1091/)；[PDF](https://aclanthology.org/2026.findings-acl.1091.pdf)。核验 A，E；近 12 个月新工作。
- 摘要明示：Temporal Memory Tree 从原始观测逐级抽象到 persona；语义引导整合、按查询复杂度召回。支持潜力：时间组织+多级摘要+查询差异化读取很接近目标组合。
- 生命周期/成本：原始观测作为树底不保证不可变保存；减少 recalled length 不等于降低总存储。**精读问题：层级/时间窗是否固定；源观测索引可否回访；冲突、重写和摘要刷新；复杂度判断与漏召回；完整构建费用？**

### T03-017 · P1 · In Prospect and Retrospect: Reflective Memory Management for Long-term Personalized Dialogue Agents
- 作者：Zhen Tan 等；年份/版本：2025；ACL 正式版；方法 RMM。
- 身份与全文：[ACL 2025.acl-long.413 / DOI](https://aclanthology.org/2025.acl-long.413/)；[PDF](https://aclanthology.org/2025.acl-long.413.pdf)。核验 A，E。
- 摘要明示：prospective reflection 将 utterance/turn/session 跨粒度摘要；retrospective reflection 用回答中 cited evidence 在线 RL 改进检索。支持潜力：多粒度记忆+来源引用反馈同作出现。
- 生命周期/成本：引用“记忆条目”是否等于原文来源未核。**精读问题：各粒度是否同时保留；引用监督何时可见、有无答案泄漏；被压掉原文能否恢复；检索更新与记忆写入更新是否分开？**

## B. 相反结果、近期更新与评价边界

### T03-018 · P1 · Agent-Controlled Search over Raw Chat Logs Rivals Structured Memory
- 作者：—；年份/版本：2026-08，v1/v2；方法 ReFind；近 12 个月新工作。
- 身份与全文：[arXiv:2608.12888](https://arxiv.org/abs/2608.12888)；[PDF](https://arxiv.org/pdf/2608.12888)。核验 A，E。
- 摘要明示：原始聊天档案不改写、turn 级词法索引，迭代搜索+会话融合/邻域展开/时间收窄/跳过已看会话。**反例潜力：很多被归因给树/图的收益或由能干的原文检索恢复**；不支持“所有结构无用”。
- 生命周期/成本：不做 LLM 索引构建，仍有词法索引与查询循环开销。**精读问题：与最强图树基线是否同答案模型/预算/卷子；精确事实任务的限制；长尾、跨语言、模糊意图与时序矛盾；索引增删代价？**

### T03-019 · P1 · Reliable Post-Retrieval Assembly for Agent Memory: Separating Evidence Extraction from Policy Execution
- 作者：Vikas Reddy；其余作者表待补齐；年份/版本：2026；核验 **v2**。v1 旧题为 Don’t Ask the LLM to Track Freshness: A Deterministic Recipe for Memory Conflict Resolution，合并一项。
- 身份与全文：[arXiv:2606.01435](https://arxiv.org/abs/2606.01435)；[PDF](https://arxiv.org/pdf/2606.01435)。核验 A，E/B；近 12 个月新工作。
- 摘要明示：证据抽取与策略执行分离；版本明确的 MAB current-value 任务有收益；**大部分收益来自抽取/执行分离，而非 freshness operator 自身**；LongMemEval 小样本检查无显著总体优势。反例潜力：不能把“检索好”当作“更新一致”。
- 生命周期/成本：针对读后装配，不替代存储更新协议。**精读问题：固定 top-10、相同抽取设置的消融；显式 serial/timestamp 是任务先验还是普遍可用；v1 强表述为何收窄；历史值查询如何执行？**

### T03-020 · P2 · LycheeMemory V2: Efficient Long-Term Memory for LLM Agents via Semantic Segment-Level Consolidation
- 作者：—；年份/版本：2026-08 首版、2026-10 v2；近 12 个月新工作。
- 身份与全文：[arXiv:2608.12990](https://arxiv.org/abs/2608.12990)；[PDF](https://arxiv.org/pdf/2608.12990)。核验 A，E；标题 V2 为系统名，不另造两个作品。
- 摘要明示：按语义 segment 批量整合而非每轮调用；生成独立类型化记忆记录，结构化轻量索引供查询规划取证。支持潜力：整合粒度影响构建成本与时间证据完整性。
- 生命周期/成本：构建/query token 分别报告有价值，但未核硬件、持久字节和原文保留。下一步：未封段时新事实可见性、修订旧段、摘要漏写恢复、是否保存原文地址。

### T03-021 · P2 · HasMem: Hard-Origin Adaptively Softened Memory for Long-Term LLM Agents
- 作者：—；年份/版本：2026-09，v1；近 12 个月新工作。最初搜索题名尾部截断，Q40 已用同一 arXiv 原始页面的检索结果补齐。
- 身份与全文：[arXiv:2609.30797](https://arxiv.org/abs/2609.30797)；[PDF](https://arxiv.org/pdf/2609.30797)。核验 A，I。
- 摘要明示：硬提示 embedding 初态可验证，控制器调整记忆宽度，Writer 重编码，Reader/Global 适配。**反例潜力：摘要承认 F1 上升伴随 EM 降低**，压缩指标改善不等于精确事实恢复。
- 生命周期/成本：连续状态宽度≠原文存储或来源指针。下一步：硬初态/原始 token 是否另存、重编码费用与目标预算匹配。

### T03-022 · P2 · Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents
- 作者：—；年份/版本：2026-01，至 v3；方法 AgeMem，不是 A-Mem；近 12 个月新工作。
- 身份与全文：[arXiv:2601.01885](https://arxiv.org/abs/2601.01885)；[PDF](https://arxiv.org/pdf/2601.01885)。核验 A，E/W。
- 摘要明示：store/retrieve/update/summarize/discard 作为策略工具动作，三阶段 RL 统一学习长短期管理。支持潜力：淘汰/迁移控制不必为固定启发式。
- 生命周期/成本：接口动作不自动保证来源保留、事务一致或物理释放。下一步：操作语义、奖励中有无存储/显存真实成本；discard 是删 prompt 还是删外存；有无原文恢复动作。

### T03-023 · P2 · Compressive Transformers for Long-Range Sequence Modelling
- 作者：Jack W. Rae、Anna Potapenko、Siddhant M. Jayakumar、Timothy P. Lillicrap；年份/版本：2019 预印本，ICLR 2020 引用关联。
- 身份与全文：[arXiv:1911.05507](https://arxiv.org/abs/1911.05507)；[PDF](https://arxiv.org/pdf/1911.05507)。核验 A，I。
- 摘要明示：对过去记忆压缩，支持长序列学习；不是文本来源树。支持潜力：快记忆/压缩记忆层级；反例潜力：被压缩掉细节是否还有寻址路径。
- 生命周期/成本：内部状态递推；原始文本重新计算的必要性与训练信号需全文。下一步：压缩目标、辅助重构、队列过期和受限内存下细节恢复。

### T03-024 · P2 · Memory³: Language Modeling with Explicit Memory
- 作者：Hongkang Yang 等；年份/版本：2024，v1；Journal of Machine Learning 3(2024), 300–346；DOI 10.4208/jml.240708。
- 身份与全文：[arXiv:2407.01178](https://arxiv.org/abs/2407.01178)；[PDF](https://arxiv.org/pdf/2407.01178)。核验 A，I。
- 摘要明示：参数/显式记忆/工作 KV 三类；知识外化与记忆稀疏化、两阶段预训练。支持潜力：区分长期可存的显式状态和活跃 KV；不是三层文本摘要。
- 生命周期/成本：显式向量来源追溯、删除与参数残留未核。下一步：外化记忆单位、实际存储带宽、原始文本到显式状态映射及权重更新后的失效。

### T03-025 · P2 · What Deserves Memory: Adaptive Memory Distillation for LLM Agents
- 作者：Wenquan Ma、Jiayan Nan、WenLong Wu；年份/版本：2025 预印本、2026 ACL 正式版；方法 Nemori。预印本旧题 Self-Organizing Agent Memory Inspired by Cognitive Science，与当前正式题合并。
- 身份与全文：[ACL 2026.acl-long.1607 / DOI](https://aclanthology.org/2026.acl-long.1607/)；[arXiv:2508.03341](https://arxiv.org/abs/2508.03341)；[正式 PDF](https://aclanthology.org/2026.acl-long.1607.pdf)。两端摘要均核验 A，E；2026-04 v4 为近窗更新，不算 2026 新作品。
- 摘要明示：经历叙事整合→用预测误差提炼语义知识，未来效用按可预测性估计。支持潜力：episodic/semantic 双粒度记忆与保留策略。
- 生命周期/成本：摘要明确下游管理无关，不能说它已经解决时间冲突/删除。下一步：预测误差是否偏向罕见噪声、原文留存与蒸馏不可逆损失。

### T03-026 · P1 · LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory
- 作者：Di Wu、Hongwei Wang、Wenhao Yu、Yuwei Zhang、Kai-Wei Chang、Dong Yu；年份/版本：2024 首版、2025 v2/ICLR 引用关联。
- 身份与全文：[arXiv:2410.10813](https://arxiv.org/abs/2410.10813)；[PDF](https://arxiv.org/pdf/2410.10813)。核验 A，B。
- 摘要明示：信息抽取、多会话、时间推理、知识更新、弃答；索引—检索—阅读拆分；value 粒度、key 扩展与时间查询扩展。支持/反例潜力：让“保存/找到/用对”分别受测。
- 生命周期/成本：评测语料与运行内存不同；500 题不代表 500 独立长期用户。**精读问题：知识更新金标规则；重复实体与过时事实；session decomposition 的粒度比较；oracle retrieval 能否隔离记忆损失？**

### T03-027 · P2 · Evaluating Very Long-Term Conversational Memory of LLM Agents
- 作者：Adyasha Maharana 等；年份/版本：2024；LoCoMo，ACL 2024 引用关联。
- 身份与全文：[arXiv:2402.17753](https://arxiv.org/abs/2402.17753)；[PDF](https://arxiv.org/pdf/2402.17753)。核验 A，B。
- 摘要明示：事件图约束的长期对话、人类编辑，QA/事件摘要/多模态生成；长上下文与 RAG 仍落后人类。反例潜力：压缩记忆排行榜未必反映实际时间/因果保存能力。
- 生命周期/成本：原摘要为平均 9K tokens、300 turns、至多35 sessions；其他论文宣称 24K 时应核 tokenizer/版本，不能混用。下一步：题型/排除题/LLM judge 与精确答案评测的口径差异。

### T03-028 · P1 · Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions
- 作者：Yuanzhe Hu、Yu Wang、Julian McAuley（搜索书目信息；完整表待出版页核齐）；年份/版本：2025 首版，至 2026-06 v4；MemoryAgentBench。
- 身份与全文：[arXiv:2507.05257](https://arxiv.org/abs/2507.05257)；[PDF](https://arxiv.org/pdf/2507.05257)。核验 A，B；近窗为修订事件。
- 摘要明示：准确检索、测试时学习、长程理解、选择性遗忘；增量多轮而非静态全文 QA。支持潜力：生命周期生死线，不让静态摘要 QA 替代更新测试。
- 生命周期/成本：评测版本影响 serial 规则与基线；不能跨版比数字。**精读问题：FactConsolidation 的 latest 规则、版本变化、隐藏/删除证据协议；遗忘是事实覆盖还是物理擦除；各系统写入和召回预算同否？**

## C. 来源优先、时间遗忘与原文回访最近邻

### T03-029 · P1 · Eywa: Provenance-Grounded Long-Term Memory for AI Agents
- 作者：—；年份/版本：2026-05，v1；近 12 个月新工作。
- 身份与全文：[arXiv:2605.30771](https://arxiv.org/abs/2605.30771)；[PDF](https://arxiv.org/pdf/2605.30771)。核验 A，E。
- 摘要明示：**先保存不可变源证据，再派生 canonical facts**；按类型/来源支持验证，确定性多路检索，取回上下文与回答指令分离。支持潜力：来源保留、可审计/更新/擦除的最直接近邻；不是摘要树的充分证据。
- 生命周期/成本：源证据不可变并不意味着不可删除；擦除与派生事实撤销尚未核实。**精读问题：source span/事实 ID/版本图；不可变与 erase 怎样兼容；源撤销是否使派生记忆/索引/缓存级联失效；检索零 LLM 调用是否转移写时费用？**

### T03-030 · P1 · LightMem: Lightweight and Efficient Memory-Augmented Generation
- 作者：Jizhan Fang 等；年份/版本：2025-10 首版，至 2026-02 v4；近窗是更新，不是首版新工作。
- 身份与全文：[arXiv:2510.18866](https://arxiv.org/abs/2510.18866)；[PDF](https://arxiv.org/pdf/2510.18866)。核验 A，E。
- 摘要明示：感知记忆过滤/压缩与主题分组→短期整合摘要→长期 sleep-time 离线更新。支持潜力：固定阶段层级和异步整合；**反例潜力：只报在线低成本可能把费用移到离线**，本摘要也分别报告总/在线成本。
- 生命周期/成本：离线更新的存储和实时可见性未核。**精读问题：睡眠间隔内事实怎么读；最新与旧摘要冲突怎么合并；原文留存/回访；离线构建、更新、查询三张账能否同时复算？**

### T03-031 · P1 · LongMemEval-V2: Evaluating Long-Term Agent Memory toward Experienced Colleagues
- 作者：Di Wu 等（完整表待补）；年份/版本：2026-05，v1；近 12 个月新工作。
- 身份与全文：[arXiv:2605.12493](https://arxiv.org/abs/2605.12493)；[PDF](https://arxiv.org/pdf/2605.12493)。核验 A，B/E。
- 摘要明示：环境经历的静态状态、动态跟踪、流程、陷阱、前提意识；context-gathering 协议；AgentRunbook-R 保存 raw observations/events/strategy notes，AgentRunbook-C 保存轨迹文件并用编码代理取证。支持潜力：原始轨迹和抽象知识并存。
- 生命周期/成本：摘要明确文件代理准确率与高延迟权衡；115M tokens 是历史规模，不是模型同时读入量。**精读问题：静态事实与动态状态怎样分卷；文件回访调用数/延迟；R/C 的信息保留差异和编程能力混杂；更新时效边界？**

### T03-032 · P1 · Control-Plane Placement Shapes Forgetting: An Architectural Study of Agent Memory Across Thirteen System Configurations
- 作者：—；年份/版本：2026-06，v1/v2；方法/评测 ForgetEval；近 12 个月新工作。
- 身份与全文：[arXiv:2606.15903](https://arxiv.org/abs/2606.15903)；[PDF](https://arxiv.org/pdf/2606.15903)。核验 A，B/E。
- 摘要明示：区分 recall 与 mutation 控制层；supersede/release/purge；确定性、写时 LLM、变更时 LLM 在词法/时间、规范化、意图删除上的互补。反例潜力：召回高分不保证正确遗忘。
- 生命周期/成本：变更延迟与召回延迟分开报告，但物理擦除/派生删除未核。**精读问题：删除金标是否只看可见答案/substring；原始、摘要、图、缓存都检查否；跨语言和复合事实删法；外部作者样本独立性？**

### T03-033 · P1 · A Human-Inspired Reading Agent with Gist Memory of Very Long Contexts
- 作者：Kuang-Huei Lee、Xinyun Chen、Hiroki Furuta、John Canny、Ian Fischer；年份/版本：2024，至 v3；方法 ReadAgent。
- 身份与全文：[arXiv:2402.09727](https://arxiv.org/abs/2402.09727)；[PDF](https://arxiv.org/pdf/2402.09727)。核验 A，E/W。
- 摘要明示：划分 memory episodes→压成 gist→按任务动作 **lookup 原始文本段落**。支持潜力：摘要提示与保留原文分离、查询回访的直接最近邻。**差异：摘要层不一定是多级树。**
- 生命周期/成本：原文作为外部可访问资源，不必常驻 prompt。**精读问题：episode 到原文索引怎样表示；单/多步 lookup、查看前后邻域及停止；摘要丢关键词能否仍找回；预处理摊销；附录 H 对 MemWalker 的失败与远隔证据批评是否实证成立？**最后一点本轮仅见检索片段，未当成已核验结论。

### T03-034 · P1 · Walking Down the Memory Maze: Beyond Context Limit through Interactive Reading
- 作者：Howard Chen、Ramakanth Pasunuru、Jason Weston、Asli Celikyilmaz；年份/版本：2023；方法 MemWalker，HTML 未在本轮强行指定最新版号。
- 身份与全文：[arXiv:2310.05029](https://arxiv.org/html/2310.05029)；[PDF](https://arxiv.org/pdf/2310.05029)。核验 A，E/W。
- 摘要/开头明示：长文分块→摘要节点树→按 query 交互导航→收集足够证据回答，能标出相关原文片段。**这是目前最须排查的“预先多级摘要+可寻址叶+查询下钻”祖先。**
- 生命周期/成本：静态构树不自动支持更新；节点可解释路径不等于事实正确归因。**精读问题：叶是否原文；父子来源索引；分支、回退、终止动作；固定树形/层数和上下文预算；失败率、导航轮数及与 ReadAgent 的远隔证据比较？**

### T03-035 · P2 · HiAgent: Hierarchical Working Memory Management for Solving Long-Horizon Agent Tasks with Large Language Model
- 作者：Mengkang Hu、Tianxing Chen、Qiguang Chen、Yao Mu、Wenqi Shao、Ping Luo；年份/版本：2025 ACL 正式版。
- 身份与全文：[ACL 2025.acl-long.1575 / DOI](https://aclanthology.org/2025.acl-long.1575/)；[PDF](https://aclanthology.org/2025.acl-long.1575.pdf)。核验 A，W。
- 摘要明示：以 subgoal 为 chunk，旧目标动作/观测压成摘要，保留当前目标细节。支持潜力：工作集与历史摘要分层；**不应把单试次工作记忆收益转称跨会话持久记忆**。
- 生命周期/成本：历史替换不知能否回访原轨迹；下一步：旧子目标信息若重新必要怎样恢复、层级是否就是两层语义组织、失败归因是否为更好规划而非记忆本身。

### T03-036 · P2 · Hindsight: Structured Agent Memory that Retains, Recalls, and Reflects
- 作者：Christopher Latimer、Nicolò Boschi、Andrew Neeser、Chris Bartholomew、Gaurav Srivastava、Xuan Wang、Naren Ramakrishnan；年份/版本：2026 ACL demo 正式版；预印本标识待补，不另计。
- 身份与全文：[ACL 2026.acl-demo.27 / DOI](https://aclanthology.org/2026.acl-demo.27/)；[PDF](https://aclanthology.org/2026.acl-demo.27.pdf)。核验 A，E；近 12 个月正式工作事件，首次公开日期未单独核齐。
- 摘要明示：world/experience/observation/opinion 四网络分事实与信念；retain/recall/reflect；向量、词法、图、时间筛选，PostgreSQL/pgvector。支持潜力：原始事件、事实、信念与多路读取职责分离。
- 生命周期/成本：数据库持久化有官方说明，不等于活跃显存成本。下一步：事实证据链和观点版本、撤销传播、长历史更新事务、性能结论模型/评测口径；作者“only one”主张不背书。

### T03-037 · P1 · Organize then Retrieve: Hierarchical Memory Navigation for Efficient Agents
- 作者：—；年份/版本：2026-06，v1；方法 HORMA；近 12 个月新工作。
- 身份与全文：[arXiv:2606.11680](https://arxiv.org/abs/2606.11680)；[PDF](https://arxiv.org/pdf/2606.11680)。核验 A，E/W。
- 摘要明示：**文件系统式层级结构，摘要实体链接对应原始轨迹**；结构构建与导航分开；轻量 RL 导航选择最小充分上下文。支持潜力：层级+来源链接+查询取证组合非常近，且有显式控制训练。
- 生命周期/成本：摘要称 token 节省，不等于总费用/显存；是否跨会话持久化未核。**精读问题：目录层级固定否；raw link 是否可逐层返回；遗漏与过载的分类信号；是否可回退；训练与推理预算；原轨迹更新/删除/重算？**

## D. 内部表示、记忆过期与可回收活跃集

### T03-038 · P2 · Augmenting Language Models with Long-Term Memory
- 作者：Weizhi Wang、Li Dong、Hao Cheng、Xiaodong Liu、Xifeng Yan、Jianfeng Gao、Furu Wei；年份/版本：2023；NeurIPS 正式版；LongMem 与 arXiv:2306.07174 同作。
- 身份与全文：[正式摘要](https://proceedings.neurips.cc/paper_files/paper/2023/hash/ebd82705f44793b6f9ade5a669d0f0bf-Abstract-Conference.html)；[正式 PDF](https://proceedings.neurips.cc/paper_files/paper/2023/file/ebd82705f44793b6f9ade5a669d0f0bf-Paper-Conference.pdf)。核验 A，I；PDF 抓取乱码，不计读。
- 摘要明示：冻结 backbone 作为 memory encoder，残差 side-network 检索/阅读，避免训练中 memory staleness。支持潜力：**表示编码器改变导致过期**与“事实时间更新”是两类不同一致性问题。
- 生命周期/成本：记忆库不代表原始文本可回访；下一步：哪些层 KV 被存、淘汰与显存/外存分布；冻结是否牺牲新分布适应、怎样因果比较过期。

### T03-039 · P2 · Memorizing Transformers
- 作者：Yuhuai Wu、Markus N. Rabe、DeLesley Hutchins、Christian Szegedy；年份/版本：2022，v1。
- 身份与全文：[arXiv:2203.08913](https://arxiv.org/abs/2203.08913)；[PDF](https://arxiv.org/pdf/2203.08913)。核验 A，I。
- 摘要明示：对近期非可微 KV 记忆做近似 kNN 查询，推理可立刻使用新读入内容。支持潜力：内部隐表示的地址与来源文本地址应分开。
- 生命周期/成本：跨过去输入的检索与长期数据库不是同义；下一步：训练参数更新后 KV stale 程度、原文定位是否保留、容量增加与检索带宽/内存的联合增长。

### T03-040 · P1 · M+: Extending MemoryLLM with Scalable Long-Term Memory
- 作者：Yu Wang 等（完整表待补）；年份/版本：2025，v1/v2；ICML 2025 引用关联。
- 身份与全文：[arXiv:2502.00592](https://arxiv.org/abs/2502.00592)；[PDF](https://arxiv.org/pdf/2502.00592)。核验 A，I。
- 摘要明示：在 MemoryLLM 上加入长期记忆和联合训练的 retriever，推理动态读回，声称相近 GPU 内存下更长保持。支持潜力：压缩活跃池+更大长期库，不可只报前者容量。
- 生命周期/成本：摘要的 GPU overhead 相近不能推出全系统内存相近。**精读问题：长期库放哪里、多大；活跃池被淘汰的状态怎样寻址回取；是否保存原文；异步检索/带宽/预取；长期库更新与向量编码一致性？**

### T03-041 · P2 · MEMORYLLM: Towards Self-Updatable Large Language Models
- 作者：Yu Wang、Yifan Gao、Xiusi Chen、Haoming Jiang、Shiyang Li、Jingfeng Yang、Qingyu Yin、Zheng Li、Xian Li、Bing Yin、Jingbo Shang、Julian McAuley；年份/版本：2024，v1/v2。
- 身份与全文：[arXiv:2402.04624](https://arxiv.org/abs/2402.04624)；[PDF](https://arxiv.org/pdf/2402.04624)。核验 A，I。
- 摘要明示：Transformer 潜在空间固定大小 memory pool，可文本自更新和保留旧知识。支持潜力：有界状态更新机制基线；不等于有外部原文档案。
- 生命周期/成本：百万次更新不退化是作者摘要主张，需原文任务/指标确认。下一步：overwrite/sampling 遗忘规律、精确来源恢复、编辑与历史事实冲突；不要与 2602.00398 同名异作混淆。

### T03-042 · P1 · Look Back to Reason Forward: Revisitable Memory for Long-Context LLM Agents
- 作者：Yaorui Shi、Yuxin Chen 等；年份/版本：2025-09 首版，2026-03 v5；方法 ReMemR1；近窗为修订事件。
- 身份与全文：[arXiv:2509.23040](https://arxiv.org/abs/2509.23040)；[PDF](https://arxiv.org/pdf/2509.23040)。核验 A，E/W。
- 摘要明示：线性扫描时摘要 buffer 会剪掉潜在证据；把历史记忆检索纳入更新过程，非线性 callback；最终答案+步级奖励。支持潜力：**可回访解决不可逆覆盖**，不是只增大摘要槽。
- 生命周期/成本：回访对象“历史记忆”不必等于原始文本。**精读问题：存档内容/地址单位；原文可否召回；query 是否写入时可见；导航预算和奖励标注费用；“negligible overhead”是否包含档案构建与存储？**

## E. 外置、淘汰、重算与物理地址

### T03-043 · P2 · Quest: Query-Aware Sparsity for Efficient Long-Context LLM Inference
- 作者：Jiaming Tang、Yilong Zhao、Kan Zhu、Guangxuan Xiao、Baris Kasikci、Song Han；年份/版本：2024，v1/v2。
- 身份与全文：[arXiv:2406.10774](https://arxiv.org/abs/2406.10774)；[PDF](https://arxiv.org/pdf/2406.10774)。核验 A，I/S。
- 摘要明示：每 KV page 保存 min/max Key 摘要，query 估计页重要性，只加载 Top-K 页做注意力。支持潜力：粗地址统计引导细页访问；**不是自然语言摘要，也不是删除未读页**。
- 生命周期/成本：未加载与不存在是两回事。下一步：全部 KV 的物理位置、索引及传输成本；跨查询关键页转移；oracle page selection 上界与块粒度漏召回。

### T03-044 · P2 · InfLLM: Training-Free Long-Context Extrapolation for LLMs with an Efficient Context Memory
- 作者：Chaojun Xiao、Pengle Zhang、Xu Han 等；年份/版本：2024，v1/v2。
- 身份与全文：[arXiv:2402.04617](https://arxiv.org/abs/2402.04617)；[PDF](https://arxiv.org/pdf/2402.04617)。核验 A，I/S。
- 摘要明示：远处上下文存额外 memory units，查找 token-relevant 单元供有限窗口注意力。支持潜力：驻留活跃集/历史库分开；替代永久淘汰。
- 生命周期/成本：CPU/GPU 层级来自搜索简介，未据此当全文实测事实。下一步：代表 key 如何生成、层间索引、CPU-GPU 搬运、旧 KV 位置编码与新窗口位置的一致性。

### T03-045 · P2 · H₂O: Heavy-Hitter Oracle for Efficient Generative Inference of Large Language Models
- 作者：Zhenyu Zhang 等；年份/版本：2023，至 v3；NeurIPS 2023 引用关联。
- 身份与全文：[arXiv:2306.14048](https://arxiv.org/abs/2306.14048)；[PDF](https://arxiv.org/pdf/2306.14048)。核验 A，S。
- 摘要明示：以历史注意力 heavy hitters 与最近 token 平衡保留 KV，动态淘汰。支持潜力：活跃显存压低的经典基线；**反例潜力：历史不重要≠未来 query 不需要**。
- 生命周期/成本：淘汰缓存是否有重算来源是另一个接口；不等于删语料。下一步：未见未来 query 下的精确信息丢失；重算可恢复性；理论的次模假设不扩大解释为任意查询保证。

### T03-046 · P1 · Cost-Efficient Large Language Model Serving for Multi-turn Conversations with CachedAttention
- 作者：Bin Gao 等（完整表待补）；年份/版本：2024，v3。v1/v2 题名 AttentionStore: Cost-effective Attention Reuse across Multi-turn Conversations in Large Language Model Serving，合并。
- 身份与全文：[arXiv:2403.19708](https://arxiv.org/abs/2403.19708)；[PDF](https://arxiv.org/pdf/2403.19708)。核验 A，S。
- 摘要明示：多层 KV 存储、逐层预加载、异步保存、按调度器提示放置/淘汰；位置编码解耦允许窗口溢出时截断重用。支持潜力：持久/慢层存储与活跃 GPU 集的实系统依据。
- 生命周期/成本：缓存失效来自位置变化，和事实更新又不同。**精读问题：原文/模型/位置/前缀变化的失效键；截断重定位适用何种位置编码；各层容量/搬运开销；淘汰策略与重算分界？**

### T03-047 · P1 · CacheBlend: Fast Large Language Model Serving for RAG with Cached Knowledge Fusion
- 作者：Jiayi Yao 等（完整表待补）；年份/版本：2024 首版，2025-04 v3；早期题名不含 for RAG，合并。
- 身份与全文：[arXiv:2405.16444](https://arxiv.org/abs/2405.16444)；[PDF](https://arxiv.org/pdf/2405.16444)。核验 A，S。
- 摘要明示：非前缀文本块的预计算 KV 忽略前文跨注意力；选择少数 token/层重算，和慢设备 KV 读取流水重叠。支持潜力：**保留源块不意味着能直接复用其状态**；来源、压缩表示、实际计算状态须分开。
- 生命周期/成本：持久 KV 与活跃加载不是同一预算。**精读问题：选择重算的误差指标、跨块依赖变化；有无精确等价保证或只是质量近似；原文/模型版本键；IO 隐藏在哪些负载下成立？**

### T03-048 · P1 · MemoRAG: Moving towards Next-Gen RAG Via Memory-Inspired Knowledge Discovery
- 作者：Hongjin Qian、Peitian Zhang、Zheng Liu、Kelong Mao、Zhicheng Dou；年份/版本：2024 首版，2025-04 v3。
- 身份与全文：[arXiv:2409.05591](https://arxiv.org/abs/2409.05591)；[PDF](https://arxiv.org/pdf/2409.05591)。核验 A，I/E 混合。
- 摘要明示：轻量长程模型建立全局记忆并产出 draft/clues，检索原长上下文证据，再用更强模型回答；最新摘要说明 KV 压缩和生成质量反馈。支持潜力：**粗压缩记忆用于寻址而非最终事实承载，证据读回另一路**。
- 生命周期/成本：双模型与源文索引不能只报压缩率。**精读问题：clue 不含原事实时能否召回；显式来源指针还是语义搜索；全局记忆刷新频率/重算成本；query 前后可见信息；KV、源文、索引总账？**

### T03-049 · P2 · Efficient Memory Management for Large Language Model Serving with PagedAttention
- 作者：Woosuk Kwon 等；年份/版本：2023，v1；SOSP 2023 引用关联。
- 身份与全文：[arXiv:2309.06180](https://arxiv.org/abs/2309.06180)；[PDF](https://arxiv.org/pdf/2309.06180)。核验 A，S。
- 摘要明示：逻辑分页、减少 KV 内存碎片与重复、请求间共享。支持潜力：逻辑地址/物理页分离；**反例边界：无语义压缩、无摘要源文回访机制，不能把 paging 当多粒度信息访问证据**。
- 生命周期/成本：活跃 KV 布局问题，不自动提供跨会话持久知识。下一步：页表元数据、复制写、引用计数、抢占/重算和实际容量记账。

## F. 摘要祖先与受控相反结果

### T03-050 · P2 · Recursively Summarizing Books with Human Feedback
- 作者：Jeff Wu、Long Ouyang、Daniel M. Ziegler、Nisan Stiennon、Ryan Lowe、Jan Leike、Paul Christiano；年份/版本：2021，v1/v2。
- 身份与全文：[arXiv:2109.10862](https://arxiv.org/abs/2109.10862)；[PDF](https://arxiv.org/pdf/2109.10862)。核验 A，E/摘要构建方法。
- 摘要明示：人类反馈与递归分解，先小段摘要再摘要之摘要；用摘要零样本 QA。支持潜力：多级摘要固定预处理的祖先；**差异：摘要未证明保存原文指针或查询回访**。
- 生命周期/成本：层级压缩可能级联失真。下一步：训练信号的粒度、局部摘要与上层一致性、人类未读全书监督的盲点；与原文保留访问臂怎么区分。

### T03-051 · P1 · Do RAG Retrieval Enhancements Help Once a Strong Reranker Is Present?
- 作者：—；年份/版本：2026-06，v1；近 12 个月新工作。
- 身份与全文：[arXiv:2606.28367](https://arxiv.org/abs/2606.28367)；[PDF](https://arxiv.org/pdf/2606.28367)。核验 A，B/E。
- 摘要明示：HetDocQA 混合格式语料+MuSiQue/QASPER 控制、共享 backbone、bootstrap 与多重比较校正；强 cross-encoder 重排已解释多数收益，层级摘要/图扩展/路由/融合未获可靠额外收益，query expansion 与按来源校准修正例外。
- **反例潜力：层级摘要收益可能由弱基线、格式异质性或候选池/重排混杂造成；不等于证明所有分层无用。**
- 生命周期/成本：检索增强比较不是长程动态记忆比较。**精读问题：层级摘要具体实现是否 RAPTOR、参数/候选池/成本预算；语料规模/任务全局性；显著性与功效；来源校准是否代替多级摘要；有无对未召回证据的 oracle 对照？**

## 版本与计数核销

1. 每个 `T03-nnn` 是一个作品，共 51；预印本与已知正式版不另增条目。
2. Nemori 2508.03341（旧/新题）与 ACL 2026.acl-long.1607 计一项；MemTree 2024/2025 改题修订计一项；AttentionStore/CachedAttention 计一项；019 的 v1/v2 改题与收窄结论计一项。
3. MemoryLLM 2402.04624 与另一个 MemoryLLM 2602.00398 不是同作；后者尚未完成摘要核验，未列候选。A-Mem 2502.12110 与 AgeMem 2601.01885 为两作。
4. 018/019/020/021/022/029/031/032/037/051 共 **10 个可明确定位为近 12 个月首版的新作品**；016 为 2026 正式作品、预印本首次日期未在本轮独立核齐；036 为 2026 正式作品，最早预印本日期待补。**不把这 12 项一概声称都是近窗首次出现。**003/025/028/030/042 等另有近窗修订/正式版事件。
5. 各项作者不齐、正式版 DOI 未核或附录线索未读均为元数据/深读后续，不影响已通过稳定 ID+原始摘要确认其作品存在；不计任何未取得摘要的额外线索。

## 可直接交给 terra 的 28 项

`001,002,003,004,005,006,009,011,012,016,017,018,019,026,028,029,030,031,032,033,034,037,040,042,046,047,048,051`。

每项上文已给具体问题；推荐批次与统一提取字段见 `HANDOFF.md`。先读最近邻/反例，不按论文名气排序；不能把“有 memory”或“减少 token”作为与内部字节接口同构的理由。
