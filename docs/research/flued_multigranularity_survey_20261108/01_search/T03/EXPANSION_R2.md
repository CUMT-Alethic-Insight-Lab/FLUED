# T03 定向扩展 R2：来源生命周期、物化维护与存储层次

日期：2026-11-08。依据[覆盖审计R1](../../05_review/COVERAGE_AUDIT_R1.md)，只补与来源保留/外置/重算/淘汰、派生更新/版本失效、数据库物化视图、存储层次直接相关的缺口，以及草案明确点名的 HMT。**不扩展一般路由理论、价值学习、无源摘要变体或模型发布清单。**

## 0. 交付与实计

- **29 个核验作品簇＝28个目录外新增确认候选＋1个HMT版本补核**，局部 ID `T03-R2-001`—`029`；**20项P1、9项P2**。全部取得原始摘要/官方介绍；全文精读0、代码核验0、复现0。
- 检索：40次WebSearch（39返回、1服务404）；49次FetchURL（40可用、4 HTTP失败、4内容不足、1误取无关作品排除）。详见[逐请求日志](EXPANSION_R2_SEARCH_LOG.md)，包括2条中文检索与原刊中文证据。
- 去重：起始完整读取384实体目录，定向查全八专题首轮候选中稳定ID/规范题名；收尾复查发现目录负责人已并发将HMT v1录为 **W0385**。因此001只补其v3/NAACL2025身份与方法，不新增HMT实体；002—029为当前385实体目录外的28个候选。其他专题已有Landmark/SSA/CacheBlend/CachedAttention不再新增；T04 R2日志中的HMT查询也不计为新作品。并发扩展最终归并仍归目录负责人，本代理不改总表、不宣称全库净增29。
- 保守版本合并：HMT v1—v3/NAACL；DBToaster 2012/2014扩展；DynaMat1999与A Case for Dynamic View Management2001；Lethe不同版本、WiscKey会议/期刊线索均不重复计数。“独立作品”不是“独立实验复现”。
- 修本专题 `CANDIDATES.md` T03-005：原始[BibTeX](https://arxiv.org/bibtex/2507.22925)确认为 **Haoran Sun、Shaoning Zeng**；补H-MEM题名前缀别名及§3局部事实。**收尾只读检查见目录负责人已并发修正W0111的作者/题名前缀；本代理未改总表。HMT的v3/正式版信息仍待其回写。**

## 1. 先给决策相关结论（不是架构裁定）

1. **摘要/向量/键值缓存应当被看成有依赖版本的派生物，而非独立永真记忆。** Why/Where（002）、来源半环（003）、增量维护（005—009）给出经典来源关系和变更传播模型；但其精确关系代数语义不能直接为LLM抽象摘要提供正确性保证。
2. **删除依赖边上的一个来源，不等于应删除整个多源事实。** 005 的Counting/DRed分别处理替代推导和过删后重推导；这能改变“删除源节点就删所有祖先”的朴素协议。003关注如何组合来源，不是任何自然语言真值或因果消费保证。
3. **可见性、时效、物理清除是三种合同。** 010/011拆有效时间与记录时间；014拆异步视图新鲜度与隔离；013检查应用级删除覆盖；015处理磁盘旧副本持久删除延迟。单一timestamp、检索降权、从prompt丢弃都不足以同时履行三合同。
4. **驻留集与来源总量分开，重算也必须有可再生来源。** 016/017给工作集与复用成本；025给基于变换谱系再生的数据抽象；018—024给具体KV/权重外置系统。KV外置解决资源位置，不解决来源事实撤销；把旧源再prefill也不能恢复本已丢失的原始细节。
5. **HMT必须补，但其“recall”不能直接当远程原文回访。** 最新v3/NAACL是六位作者、题名多了Efficient；§3.2回忆对象是滑窗历史摘要embedding的注意力混合，不是按稳定源指针读取任意远端原始token/KV。详细版本核验在001。
6. **经典系统已经联合考虑多级聚合、查询访问、驻留/淘汰和刷新预算。** 027的DynaMat是直接的跨域机制桥接；不能因不是LLM就忽略，也不能把精确SQL聚合能力等同自然语言摘要。它的离线维护窗口等假设必须明列。

### 关键概念（本报告局部说明，不修改项目术语表）

- 来源追溯/数据血缘（provenance/lineage）：记录一个输出由哪些输入、经哪些处理形成；来源“支持”、复制位置、计算依赖、因果必要性并不相同。
- 物化视图（materialized view）：把查询的派生结果预先保存以便重复读取；源变更后须刷新或失效。增量视图维护（IVM）只传播变化而非总是全量重算。
- 双时间（bitemporal）：有效时间描述事实在外部世界何时成立，事务/记录时间描述系统何时持有该记录；晚到纠错不能仅用最新写入值覆盖所有历史。
- 墓碑（tombstone）：标记逻辑删除的记录；它不等于磁盘旧副本已物理回收。租约（lease）是有限时间的缓存使用权，并非随意设TTL就有一致性。
- KV为注意力键—值状态缓存；这里“键值存储系统”的key/value又是数据库地址/载荷，二者不是同一语义对象。

## 2. 候选证据卡

深度A=原始摘要/官方论文介绍核验；A+M=另定向读列明方法/定义，仍非全文精读。未知作者留空；全文入口不代表已读。P1为后续terra优先，不是效果认证。每卡“支持/反例”均为对本专题的候选价值，不把摘要性能词转为我们的实验证据。

### T03-R2-001 · P1 · HMT: Hierarchical Memory Transformer for Efficient Long Context Language Processing
- **身份/版本**：Zifan He、Yingqi Cao、Zongyue Qin、Neha Prakriya、Yizhou Sun、Jason Cong；首版2024-05-09，v3为2025-02-06；NAACL2025，8068–8089。arXiv **2405.06067** = DOI **10.18653/v1/2025.naacl-long.410**，一个作品。
- **来源/全文/深度**：[原始摘要](https://arxiv.org/abs/2405.06067)、[原始BibTeX](https://arxiv.org/bibtex/2405.06067)、[正式页](https://aclanthology.org/2025.naacl-long.410/)、[HTML v3](https://arxiv.org/html/2405.06067v3)、[正式PDF](https://aclanthology.org/2025.naacl-long.410.pdf)；A+M（v3 §3.2—3.3）。v1旧题无Efficient、五作者；审计v1记录不倒填最新版，本轮确认六作者。
- **对象/机制**：内部表示记忆，不是外部文档RAG；segment recurrence保存近期细节、传递memory embedding、检索历史embedding。v3 §3.2 Eq.(1)—(3)以当前段前j个embedding的summary作query，在历史N个memory embedding上交叉注意力，读出单个混合prompt embedding；§3.2明言历史累积摘要对较老信息损失更高。§3.3近期细路径为上一段末k个embedding。
- **生命周期边界**：摘要滑窗外淘汰是否另存原文、本地训练offload与推理持久源不同；正文此路径不构成任意历史原文地址回访。活跃显存下降是作者跨模型/参数设置结果，不能拿2.5–116×作为同模型同总保存权限保证。
- **支持/反例潜力**：补草案漏项；为“层级标签不等于来源树”“历史摘要召回不等于原文召回”提供桥接对照。
- **terra问题**：锁v3与NAACL差异；逐对象核原token/embedding/摘要/缓存N的保存期限和物理位置；是否有源重放；查附录缓存容量与训练/推理offload分账；同backbone、同历史权限、同精度下重做成本解读。不要只问v1已有的问题。

### T03-R2-002 · P1 · Why and Where: A Characterization of Data Provenance
- **身份**：Peter Buneman、Sanjeev Khanna、Wang-Chiew Tan；ICDT2001，316–330；DOI **10.1007/3-540-44503-X_20**。
- **来源/全文/深度**：[Springer原始摘要与作者](https://doi.org/10.1007/3-540-44503-X_20)（同页全文获取入口）；A。
- **对象/机制**：数据库查询派生的来源，适用于关系及XML层级数据；why是影响结果存在的源数据，where是值从何位置抽取。不是LM权重或显存机制。
- **生命周期/价值**：把“摘要连原文”拆为支持集合与源位置，避免仅有文档ID就称全程可解释；摘要没有说明物理驻留、删除协议或任意文本语义支持。
- **terra问题**：原始地址粒度/路径稳定性；源改写后位置如何有效；一对多来源与复制/推导的区别；哪些语义是精确的，迁移到抽象摘要要额外验证什么？

### T03-R2-003 · P1 · Provenance Semirings
- **身份**：Todd J. Green、Grigoris Karvounarakis、Val Tannen；PODS2007，31–40；DOI **10.1145/1265530.1265535**。
- **来源/全文/深度**：[原作者公开PDF](https://web.cs.ucdavis.edu/~green/papers/pods07.pdf)；A（摘要/开头）；出版DOI入口403已记录，不绕过。
- **对象/机制**：关系查询的来源多项式表达替代/联合推导；摘要明确把不完整库、概率库、bag与why-provenance放入同一半环框架，并扩展Datalog。开头§1列正关系代数与递归扩展的边界。
- **生命周期/价值**：可作为多源支持关系的精确参照；**不保证**摘要自然语言正确、任意否定/删除都有同一简单运算，更不代表模型真的消费被引内容。派生来源本身也有存储开销。
- **terra问题**：正查询/递归的条件；更新/删除需要哪些代数扩展；怎样保留替代推导不误删仍有独立支持的事实；来源表达式增长与压缩代价？

### T03-R2-004 · P1 · Provenance as Dependency Analysis
- **身份**：James Cheney、Amal Ahmed、Umut Acar；2007初版，2009修订；**arXiv:0708.2173v2**；出版扩展关系未全部核齐，保守单簇。
- **来源/全文/深度**：[原始摘要](https://arxiv.org/abs/0708.2173)、[BibTeX](https://arxiv.org/bibtex/0708.2173)、[PDF](https://arxiv.org/pdf/0708.2173v2)；A。
- **机制/反例**：把来源视作输入/输出依赖，摘要明确指出其语义刻画的一般形式不可计算，提供动态/静态近似。**反例价值：记录过程序列或source pointer并不自动给出精确最小因果依赖。**
- **生命周期**：近似依赖可用于保守失效，但可能过度重算；这是我们的迁移候选，不是论文已测LLM摘要。
- **terra问题**：不可计算结果的程序模型、依赖定义；近似是sound还是complete、失效误报和漏报怎样区分；源撤销时可以承诺哪一级别？

### T03-R2-005 · P1 · Maintaining Views Incrementally
- **身份**：Ashish Gupta、Inderpal Singh Mumick、V. S. Subrahmanian；SIGMOD1993，157–166；**10.1145/170035.170066**（会议DOI检索关联；SIGMOD Record另有容器DOI，勿拆作）。
- **来源/全文/深度**：[公开原论文PDF](http://www1.cs.columbia.edu/~gravano/Qual/Papers/13%20-%20Maintaining%20Views%20Incrementally.pdf)；A（摘要/Introduction pp.157–158）。
- **机制**：非递归Counting追踪替代推导数量；递归DRed先删可能受影响超集再重推导仍有支持的条目，允许插入/删除/更新、聚合与受约束否定。来源推导数不是原文内容备份。
- **生命周期/反例**：多源支持撤销已有经典机制；开头明确提醒增量更便宜只是heuristic，例如大范围删除可能全量重算更便宜。不能把LLM摘要视为天然可加减聚合。
- **terra问题**：Counting/DRed各自限制；源→事实→摘要递归依赖的映射；有替代支持时怎样免于误删；批量更新何时转全量重算；规则改变与数据改变怎样区别？

### T03-R2-006 · P1 · DBToaster: Higher-order Delta Processing for Dynamic, Frequently Fresh Views
- **身份**：Christoph Koch、Yanif Ahmad、Oliver Kennedy、Milos Nikolic、Andres Nötzli、Daniel Lupei、Amir Shaikhha；2014扩展稿；2012前身作者/版本不同，本轮保守一簇，不作两个独立验证。
- **来源/全文/深度**：[Oxford原作者扩展稿PDF](https://www.cs.ox.ac.uk/files/9137/vldbj2014-dbtoaster-extended.pdf)；A（摘要/开头）。正式DOI待编目补齐。
- **机制/位置**：对查询及高阶delta再物化，维护相互支持的视图；内存运行时/编译触发器，不是GPU语义摘要。开头明确部分不等式join与嵌套查询需要物化/惰性重算折中。
- **支持/反例**：已有“多层派生缓存+维护”先例；辅助视图会增长，更多层不必总划算。其精确查询闭包不能无证替代抽象摘要更新。
- **terra问题**：辅助状态bytes与更新耗时是否一起优化；哪些表达式可有限差分、哪些必须重算；高阶视图失效链；训练非确定性摘要可否只借用依赖调度而不借其等价保证？

### T03-R2-007 · P1 · DBSP: Automatic Incremental View Maintenance for Rich Query Languages
- **身份**：Mihai Budiu、Frank McSherry、Leonid Ryzhyk、Val Tannen；2022预印本；**arXiv:2203.16684v1**；后续正式版关系只作为待核元数据，不另计。
- **来源/全文/深度**：[摘要](https://arxiv.org/abs/2203.16684)、[作者BibTeX](https://arxiv.org/bibtex/2203.16684)、[PDF](https://arxiv.org/pdf/2203.16684)；A。
- **机制**：把查询化为数据流程序，系统推导增量维护；摘要覆盖完整关系查询、分组聚合、单调/非单调递归和流聚合。支持派生图的一致变更思考，不等于替LLM生成器自动求精确delta。
- **生命周期/成本**：非单调变更不能只做追加；流状态、差分和输入源都要记账；真实持久/活跃GPU分布未核。
- **terra问题**：等价定理模型类与终止/有限性；固定点下撤销传播；语言中的外部函数/不确定调用怎么处理；变更batch、乱序、快照语义和物化策略？

### T03-R2-008 · P2 · Differential Dataflow
- **身份**：Frank McSherry、Derek G. Murray、Rebecca Isaacs、Michael Isard；CIDR2013；**官方论文URL**为稳定入口。
- **来源/全文/深度**：[Microsoft Research原始介绍](https://www.microsoft.com/en-us/research/publication/differential-dataflow/)、[会议PDF](https://www.cidrdb.org/cidr2013/Papers/CIDR13_Paper111.pdf)；A。
- **机制/价值**：对动态输入和任意嵌套迭代增量计算，原介绍用变化图的强连通分量示例。非树依赖图的维护不必从零设计。
- **边界**：计算时标与事实有效时间不是同一概念；不是近似摘要正确性证据。下一步：多维迭代进度/时间、负更新、状态回收、重排及最终一致边界；避免把“不全重算”说成每次常数成本。

### T03-R2-009 · P1 · Optimised Maintenance of Datalog Materialisations
- **身份**：Pan Hu、Boris Motik、Ian Horrocks；2017，**arXiv:1711.03987v2**。
- **来源/全文/深度**：[摘要](https://arxiv.org/abs/1711.03987)、[原始BibTeX](https://arxiv.org/bibtex/1711.03987)、[PDF](https://arxiv.org/pdf/1711.03987v2)；A。
- **机制/反例**：DRed与Backward/Forward可能因反向求规则而在微小更新下付出很大开销；混合Counting减少此开销且支持递归。对005的性能限定，不是泛称“更新传播已解决”。
- **生命周期**：多级来源链上小变更仍可能触发昂贵证明/重建；回收物化推导与物理源删除不同。
- **terra问题**：小delta的大开销反例；是否保存证明/计数、额外索引大小；递归环的撤销；如何给摘要/事实依赖链做上界或触发全量重算？

### T03-R2-010 · P1 · Temporal Data Management
- **身份**：Christian S. Jensen、Richard T. Snodgrass；IEEE TKDE11(1),36–44，1999；**DOI10.1109/69.755613**。
- **来源/全文/深度**：[原作者PDF](https://people.cs.aau.dk/~csj/Papers/Files/1999_jensenIEEETKDE.pdf)；A+M（摘要、§2定义）。
- **机制**：§2将valid time定义为事实在世界成立的时段，transaction time为记录在库中current的时段；后者从插入至逻辑删除。不能用到达顺序覆盖事实时间。
- **生命周期/价值**：为晚到事实、纠错、回滚/历史查询提供成熟语义；**保留历史不等于隐私擦除**，双时间记录本身可能需要额外撤销合同。
- **terra问题**：source event、事实版本、模型派生时间分别归哪一轴；当前值/当时已知值/当时实际值三种查询；索引/摘要时段及物理vacuum；如何限制历史副本及存储增长？

### T03-R2-011 · P2 · Language-Integrated Query for Temporal Data (Extended version)
- **身份**：Simon Fowler、Vashti Galpin、James Cheney；2022；**arXiv:2210.12077v1**；GPCE2022短题关联（10.1145/3564719.3568690为检索线索），不另计。
- **来源/全文/深度**：[摘要](https://arxiv.org/abs/2210.12077)、[PDF](https://arxiv.org/pdf/2210.12077)；A。
- **机制**：分别对事务时间、有效时间查询/更新给保语义翻译，到普通关系核心语言，Links实现。相较只存时间戳，提供可检查操作语义。
- **生命周期/边界**：不是LLM记忆系统；下一步：删除/纠错的分段时间处理、sequenced joins及proof条件；能否作为小型来源生命周期参照模型，而不声称其已保证文本摘要时序正确？

### T03-R2-012 · P2 · Self-Adjusting Stack Machines
- **身份**：Matthew A. Hammer、Georg Neis、Yan Chen、Umut A. Acar；OOPSLA2011完整扩展稿；**arXiv:1108.3265v1**。
- **来源/全文/深度**：[摘要](https://arxiv.org/abs/1108.3265)、[BibTeX](https://arxiv.org/bibtex/1108.3265)、[PDF](https://arxiv.org/pdf/1108.3265)；A。
- **机制/价值**：随动态输入变化更新计算，低层栈机语义并证明与全重算一致，提供编译/运行时。适合作为“保留派生轨迹以局部重算”的桥接。
- **边界**：正确性条件不自动容纳随机采样LLM/模型权重改动。下一步：change propagation、memoization、trace内存与释放；外部副作用/非确定生成如何封装；局部维护何时比全重算更贵？

### T03-R2-013 · P1 · DELF: Safeguarding Deletion Correctness in Online Social Networks
- **身份**：Katriel Cohn-Gordon、Georgios Damaskinos、Divino Neto、Joshi Cordova、Benoît Reitz、Benjamin Strahs、Daniel Obenshain、Paul Pearce、Ioannis Papagiannis；USENIX Security2020。
- **来源/全文/深度**：[正式页及原始摘要](https://www.usenix.org/conference/usenixsecurity20/presentation/cohn-gordon)、[PDF](https://www.usenix.org/system/files/sec20-cohn-gordon.pdf)；A。
- **机制**：类型定义上的删除annotations映射到后端异步、可靠、暂时可逆的操作，并静态/动态验证遗漏；官方介绍有三OSN部署，不是仅AI demo。
- **生命周期/反例**：高层“删照片/记忆”要求容易漏到下层存储；**暂时可逆删不是立即物理抹除**。完整删除范围比prompt或向量库一个删除API大。
- **terra问题**：级联对象/副本/派生物枚举、失败重试和过删恢复；何时达到不可逆完成；日志/备份例外；可否迁移为源→摘要→embedding→KV删除合同，哪些部分必须另定义？

### T03-R2-014 · P1 · Streaming Democratized: Ease Across the Latency Spectrum with Delayed View Semantics and Snowflake Dynamic Tables
- **身份**：Daniel Sotolongo、Daniel Mills、Tyler Akidau等（完整作者见原页）；2025-04-14，**arXiv:2504.10438v1**。
- **来源/全文/深度**：[原始摘要和作者](https://arxiv.org/abs/2504.10438)、[PDF](https://arxiv.org/pdf/2504.10438)；A。
- **机制**：delayed view semantics把流计算看作异步提前算派生结果，并为IVM扩展事务隔离/应用不变量；面向秒至分钟延迟而不是所有场景追求毫秒。
- **生命周期/价值**：sleep-time整合不能只说“异步很便宜”，必须选明确陈旧/隔离合同；**跨视图各自最新不必是同一个一致快照**，此为待原文核对的判别轴。
- **terra问题**：视图DAG的目标滞后、祖先快照对齐、读取遇未刷新依赖怎么办；多问摊销与更新队列积压；不变量保证具体是哪种隔离，是否容许混版本？

### T03-R2-015 · P1 · Lethe: A Tunable Delete-Aware LSM Engine
- **身份**：Subhadeep Sarkar、Tarikul Islam Papon、Dimitris Staratzis、Manos Athanassoulis（首版作者检索线索；最新作者栏待全文锁定）；SIGMOD2020；**arXiv:2006.04777v4**，更新题名有Updated Version后缀。2023期刊扩展线索不另计。
- **来源/全文/深度**：[原始摘要/版本史](https://arxiv.org/abs/2006.04777)、[PDF v4](https://arxiv.org/pdf/2006.04777v4)；A。
- **机制**：LSM逻辑删除写墓碑，旧值何时持久删除通常无保证；delete-aware compaction、少量元数据、排序键/删除键交织布局，控制删除持久化延迟。
- **生命周期/反例**：直接反驳“向量/源记录API返回deleted就完成物理擦除”；作者摘要明确以写放大增加交换读取/空间与删除延迟，不能只摘收益。
- **terra问题**：持久删除的精确定义，设备/备份/副本边界；删除时间上限条件；多级compaction与写放大；非主键删除、SSD寿命；如何将源撤销SLA分配给派生库？

### T03-R2-016 · P1 · The Working Set Model for Program Behavior
- **身份**：Peter J. Denning；CACM11(5):323–333，1968（1967会议/修订线索同作）；**DOI10.1145/363095.363141**。
- **来源/全文/深度**：[原作者PDF](http://denninginstitute.com/pjd/PUBS/WSModel_1968.pdf)；A（摘要/开头）。
- **机制/位置**：以近期使用页集合刻画工作集，联合处理器/内存需求；页不在主存并不意味着从辅助存储销毁。原稿开头两级存储、page fault与搬运开销明确。
- **支持/反例**：为“保存不等于活跃加工”提供经典系统锚；但近期性不是任意未来语义query的相关性保证，工作集太小会产生反复换入，不能说稀疏活跃集总更快。
- **terra问题**：工作集窗口、缺页/重入率与带宽/调度的假设；把CPU页换成源文本/KV时哪些性质保留；冷回访与语义热点切换如何测；峰值驻留与总档案分开记账？

### T03-R2-017 · P1 · The Five Minute Rule, Ten Years Later
- **身份**：Jim Gray、Goetz Graefe；1997，MS Research P116；扩展题名 The Five-Minute Rule Ten Years Later, and Other Computer Storage Rules of Thumb 为同报告，**arXiv:cs/9809005**仅搜索关联，不另计。
- **来源/全文/深度**：[原作者机构摘要](https://www.microsoft.com/en-us/research/publication/the-five-minute-rule-ten-years-later/)、[公开报告PDF](https://dsf.berkeley.edu/cs286/papers/fiveminute-tr1997.pdf)；A。
- **机制**：以RAM/磁盘价格与带宽、随机/顺序访问成本求缓存驻留/页大小折中，规则随技术比例可预测变化。
- **生命周期/价值**：给“原文驻留、慢层换入还是重算”的经济模型祖先；**不把1997的五分钟常数套到2026 GPU/SSD**，也不是保证未来使用率的学习理论。
- **terra问题**：页粒度、每次访问成本/持有成本公式；加上重编码、模型变更、网络/SSD寿命后哪些项新增；给单问、重复q次、更新u次的break-even而非只算压缩率？

### T03-R2-018 · P1 · CacheGen: KV Cache Compression and Streaming for Fast Large Language Model Serving
- **身份**：Yuhan Liu、Hanchen Li、Yihua Cheng、Siddhant Ray等（完整14位见原始页）；2023首版，v6为2024-07-19；**arXiv:2310.07240**；SIGCOMM2024检索关联。
- **来源/全文/深度**：[原始摘要/作者/历史](https://arxiv.org/abs/2310.07240)、[PDF v6](https://arxiv.org/pdf/2310.07240v6)；A。
- **机制**：对大KV张量编码为紧凑bitstream，按网络带宽调不同部分压缩级别，以降低跨请求复用的加载延迟。非语义摘要，不等于原文永久保留。
- **生命周期/反例**：KV物化/压缩/传输可比原文重prefill更贵或便宜，依带宽/复用而定；摘要含注释残片提重算，**不能以注释残片当已验证主机制**。
- **terra问题**：失真/无损各配置与精确恢复条件；缓存key是否含模型/位置/上下文前缀；带宽变动下取KV/取token重算的决策；冷启动、源/bitstream/活跃张量三份bytes与尾延迟？

### T03-R2-019 · P2 · Stateful Large Language Model Serving with Pensieve
- **身份**：Lingfan Yu、Jinyang Li（搜索原作作者线索；完整最新作者表待核）；2023首版，v3为2024-10-07；**arXiv:2312.05516**。
- **来源/全文/深度**：[摘要/版本史](https://arxiv.org/abs/2312.05516)、[PDF v3](https://arxiv.org/pdf/2312.05516v3)；A。
- **机制**：跨请求缓存会话状态，多层GPU/CPU缓存；非连续GPU cache支持多个输入token注意力。不是自然语言长期记忆组织。
- **生命周期/边界**：缓存逐出与聊天档案删除分开；跨轮复用只在上下文兼容时成立。下一步：CPU/GPU容量分配、token重放与KV swap边界、会话中断/编辑/截断后的失效范围；吞吐与单请求延迟不可换算。

### T03-R2-020 · P2 · FlexGen: High-Throughput Generative Inference of Large Language Models with a Single GPU
- **身份**：Ying Sheng、Lianmin Zheng、Binhang Yuan等（完整14位见原页）；2023，至v2；**arXiv:2303.06865**；ICML2023检索关联。
- **来源/全文/深度**：[原始作者/摘要](https://arxiv.org/abs/2303.06865)、[PDF v2](https://arxiv.org/pdf/2303.06865v2)；A。
- **机制**：GPU/CPU/磁盘联合存放/调度张量，线性规划选访问模式，权重与attention cache可4bit压缩；目标明确为latency-insensitive的大batch吞吐。
- **边界/反例**：省GPU容量可能以大batch和慢单请求换来；权重offload不等于来源档案回访。下一步：原文/activation/KV/参数分别记账；压缩/调度/批量三轴消融；把其吞吐优势套交互query的条件是否失效？

### T03-R2-021 · P2 · LLM in a Flash: Efficient Large Language Model Inference with Limited Memory
- **身份**：—（未将arXiv From联系人冒充完整作者）；2023首版，v3为2024-07-30；**arXiv:2312.11514**。
- **来源/全文/深度**：[摘要/历史](https://arxiv.org/abs/2312.11514)、[PDF v3](https://arxiv.org/pdf/2312.11514v3)；A。
- **机制**：参数存flash、按需换入DRAM；以flash成本模型、窗口复用激活神经元、row-column bundling降低传输量/增加顺序块。
- **支持/边界**：地址选择、载荷打包和设备访问成本的硬件例；对象主要是模型参数，不是过去原文/KV，不能用它证明源保存方式。下一步：windowing的活跃集和预测失误、读放大、参数更新失效、冷/热访问与总存储。

### T03-R2-022 · P1 · Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving
- **身份**：Ruoyu Qin等（完整最新作者待补）；2024-06-24首版，v5为**2026-10-08**；**arXiv:2407.00079**（编号月份不替代真实首发日）；FAST2025关系为搜索线索。
- **来源/全文/深度**：[摘要/版本史](https://arxiv.org/abs/2407.00079)、[PDF v5](https://arxiv.org/pdf/2407.00079v5)；A；近12个月是版本更新，不伪称新作品。
- **机制**：prefill/decode分离；CPU/DRAM/SSD资源组成KV外置缓存，调度器在延迟目标下优化有效吞吐，超载时可提前拒绝请求。
- **生命周期/反例**：在SLO约束下比较要计拒绝率、源存储与网络；缓存服务不等于无损语义历史库。最新摘要不能倒引2024已有全部实现。
- **terra问题**：锁FAST版/v3/v5差异；何种KV驻留/淘汰；重复query多问摊销与冷命中；跨节点版本key、模型更换/源编辑后的失效；吞吐是已接收请求还是全部到达请求？

### T03-R2-023 · P2 · HiFC: High-efficiency Flash-based KV Cache Swapping for Scaling LLM Inference
- **身份**：Inho Jeong、Sunghyeon Woo、Sol Namkung、Dongsuk Jeon（原论文首页检索线索）；**NeurIPS2025正式卷年**；DOI **10.52202/085713-1587**。
- **来源/全文/深度**：[正式摘要/DOI](https://papers.neurips.cc/paper_files/paper/2025/hash/4431224d3762aa655f0aee4eaf04ff16-Abstract-Conference.html)、[正式PDF](https://papers.neurips.cc/paper_files/paper/2025/file/4431224d3762aa655f0aee4eaf04ff16-Paper-Conference.pdf)；A。
- **机制**：KV存commodity NVMe的pseudo-SLC区域，GPU Direct Storage绕过host DRAM数据路径，细粒度映射控制写入区域与寿命。这里pSLC是伪单层单元闪存运行区，不是语义压缩。
- **生命周期/价值**：把SSD写耐久、扩容成本和数据通路纳入账，而不是仅GPU峰值。下一步：pSLC真实容量折扣、平台兼容、随机/顺序工作负载、写放大与三年成本假设；“DRAM-free swapping”不应扩大为整个服务不用主机内存。

### T03-R2-024 · P1 · LMCache: An Efficient KV Cache Layer for Enterprise-Scale LLM Inference
- **身份**：Yuhan Liu、Yihua Cheng、Jiayi Yao、Yuwei An等（完整11位见原页）；2025-10-08首版，v2为**2025-12-05**；**arXiv:2510.09665**。
- **来源/全文/深度**：[作者/摘要/历史](https://arxiv.org/abs/2510.09665)、[PDF v2](https://arxiv.org/pdf/2510.09665v2)；A；近窗为修订。
- **机制**：从vLLM/SGLang提取KV置于GPU外，跨引擎/query共享；批量搬运与compute/I/O流水；控制API跨GPU、CPU、storage、network编排。
- **支持/反例**：持久KV总量可大于GPU但活跃集仍小；摘要指出context truncation会伤prefix命中，**相同原文集不等于相同缓存重用权限**。作者“first/most efficient”不背书。
- **terra问题**：prefix/content/位置/模型/精度的命名key；跨引擎格式一致性；授权/删除/租户隔离是否传至所有副本；cache controls的失效确认、冷/热fetch与recompute成本、超容量淘汰？

### T03-R2-025 · P1 · Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing
- **身份**：Matei Zaharia、Mosharaf Chowdhury、Tathagata Das、Ankur Dave、Justin Ma、Murphy McCauley、Michael J. Franklin、Scott Shenker、Ion Stoica；NSDI2012，15–28。官网BibTeX的McCauly与作者栏McCauley拼法不同，保留作者栏并交编目核齐，不自行推断身份分裂。
- **来源/全文/深度**：[USENIX原始摘要/作者/BibTeX](https://www.usenix.org/conference/nsdi12/technical-sessions/presentation/zaharia)、[PDF](https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final138.pdf)；A。
- **机制**：内存数据抽象，以粗粒度确定变换而不是任意细粒度共享更新支持容错，Spark实现。变换谱系可作为重算入口需全文锁定，不能只靠系统常识补细节。
- **生命周期/反例**：丢弃派生partition与删原始source不同；重算需要源与变换可重现。对LLM采样、模型变更和远端源消失尤其不是免费恢复。
- **terra问题**：lineage重算所需最小数据/代码、persist/checkpoint/丢弃关系；长依赖链成本；非确定操作限制；源撤销后如何防止被lineage重新生成已撤销内容？

### T03-R2-026 · P2 · WiscKey: Separating Keys from Values in SSD-conscious Storage
- **身份**：Lanyue Lu、Thanumalayan Sankaranarayana Pillai、Andrea C. Arpaci-Dusseau、Remzi H. Arpaci-Dusseau；FAST2016，133–148；**官方URL稳定键**。2017扩展线索不另计。
- **来源/全文/深度**：[正式作者/摘要/BibTeX](https://www.usenix.org/conference/fast16/technical-sessions/presentation/lu)、[PDF](https://www.usenix.org/system/files/conference/fast16/fast16-papers-lu.pdf)；A。
- **机制**：持久LSM-based key-value store把key与value布局分离，减少I/O amplification；SSD顺序与随机特性共同设计。
- **生命周期/价值**：地址/载荷分离本身已有存储经典；但没有学得语义摘要或查询充分性。下一步：key→value地址迁移、value-log垃圾回收/崩溃一致、过期值残留、随机读与范围扫描；借此约束“只搬指针更省”是否漏算载荷回访。

### T03-R2-027 · P1 · A Case for Dynamic View Management
- **身份**：Yannis Kotidis、Nick Roussopoulos；ACM TODS26(4):388–423，**2001**；前身DynaMat: A Dynamic View Management System for Data Warehouses（SIGMOD1999，10.1145/304182.304215）与扩展稿关联，**本轮保守计一簇**。不能按公开PDF文件名TODS2002改年份。
- **来源/全文/深度**：[原论文公开稿PDF](https://courses.cs.duke.edu/cps296.1/spring02/papers/KR-TODS2002.pdf)；A（摘要/开头）。OCR部分分词/数字不佳，后续精读不依此OCR引数字。
- **机制**：专用磁盘view pool保存多层聚合片段，为新query复用；基于依赖计划共享计算；维护窗口内刷新最有益子集，同时考虑incremental与recomputation。多级聚合、查询访问、缓存淘汰/存储预算和维护预算在经典系统中已联合出现。
- **边界/反例**：SQL精确aggregate不是抽象语义摘要；开头明确更新phase为offline、维护中不允许查询的设计假设，不能直接套实时agent。更多物化更好只在不计刷新时成立。
- **terra问题**：view lattice与fragment依赖、miss后回base、准入/替换/刷新各成本项；离线窗口和查询隔离；多问摊销与源更新率；有哪些失效/重新物化情况？与固定摘要树差异应具体而非只说非LLM。

### T03-R2-028 · P2 · 面向区块链的高效物化视图维护和可信查询
- **身份**：蔡磊、朱燕超、郭庆兴、张召、金澈清；《软件学报》**2020,31(3):680–694**；原刊article ID **5914**，DOI **10.13328/j.cnki.jos.005914**为原刊搜索索引关联。收稿2019-08-15、在线2020-01-10，按原刊历史，不采搜索更新日。
- **来源/全文/深度**：[原刊作者/摘要/年份](https://www.jos.org.cn/jos/article/abstract/5914)、[原刊HTML全文](https://www.jos.org.cn/jos/article/html/5914?special_id=20250523142617001)；A（摘要），非全文精读。
- **机制**：源交易跨块分散；物化视图维护与共识并行，字典树支持以区块为单位维护，Merkle校验派生结果未被篡改。
- **生命周期/价值**：中文原刊提供源/链下派生视图、更新批次与验证成本桥接；不是要求草案使用区块链。**源不可篡改并不保证派生内容语义正确，哈希完整也不等于事实有效时间正确。**
- **下一步**：按需/闲时维护和BlockID新鲜度；失效视图读前刷新；验证是否扫全视图、维护/验证/随机I/O全账；append-only限制能否处理修订/撤销；慎用作者“首次”措辞。

### T03-R2-029 · P1 · Leases: An Efficient Fault-Tolerant Mechanism for Distributed File Cache Consistency
- **身份**：Cary G. Gray、David R. Cheriton；SOSP1989，202–210；**DOI10.1145/74850.74870**。
- **来源/全文/深度**：[原论文公开PDF](https://www.cs.cmu.edu/~15712/papers/gray89.pdf)；A+M（摘要、§2 pp.202–203）。
- **机制**：缓存持有内容还须有有效lease才能读取；写入需取leaseholder批准/本地失效或等租期结束。重读续租时如已修改须更新缓存，涉及名称绑定/权限等元数据而不只是内容。§5的时钟与故障假设留terra核。
- **生命周期/反例**：**副本存在≠副本可用**，失效协议与容量淘汰正交；随意TTL只是提示，不满足写时协调不保证一致性。这是缓存一致性经典，不是语义摘要充分性或机器遗忘证明。
- **terra问题**：租期、时钟漂移、分区/崩溃假设；多级派生状态可否按source版本租约读取；撤销可用性延迟；各层续租/失效通知开销；源修订与模型版本修订是否都纳入验证键？

## 3. 新增证据如何对齐草案，不越界代证

| 草案直接缺口 | 新增主证据 | 已支持的机制层 | 仍未证明/必须限制 |
|---|---|---|---|
| 粗节点对应细源 | 002/003/004/027 | 来源位置、推导关系、依赖与聚合层级已有精确区分 | 自然语言摘要的语义蕴含、稳定原始byte跨度、部署因果消费 |
| 原文保留与活跃集分开 | 016/017/019/022/024/025 | 总来源/缓存与活跃页不等同；外置/重放可省快层容量 | 未被选中内容仍有带宽/容量/权限成本；语义路由不具OS精确地址保障 |
| 源追加/修订/撤销后更新派生物 | 005/006/007/008/009 | 精确查询delta、递归物化撤销、替代支持重推导 | 抽象摘要通常不能简单做代数减法；编码器/权重变更失效需要额外合同 |
| 时间更新一致性 | 010/011/014/029 | 有效/记录时间、异步视图隔离、缓存租约 | 时间戳不是全序因果；“最新”须指定轴；跨派生物一致快照未自动获得 |
| 从prompt丢弃与物理删除 | 013/015/026 | 应用对象级删除覆盖、底层墓碑与compaction持久清除 | 备份、远端副本、日志、模型权重残留、再生路径仍须分别界定 |
| 源/派生物外置与重算选择 | 012/017/018/020/022/023/025/027 | 留轨迹重算、取缓存/取原文成本、快慢层、维护预算 | 非确定生成不能自动精确再生；最大吞吐不等同交互尾延迟；重算须源仍在 |
| 草案点名层级记忆Transformer | 001 HMT | 原始段近期细路径+累积摘要+查询相关历史摘要读取，联合训练 | 不等于原文保留的可寻址来源树；不自动原文回访/字节级恢复 |

这里的跨域映射只是约束与对照设计，不将关系数据库定理、存储布局或分布式容错直接移植成语言模型定理。

## 4. 生命周期最小账本：后续逐作品填，不预设实现

建议terra用下列对象图审问每个系统：

`源记录(稳定ID, 内容版本, 有效区间, 记录区间)` → `事件/事实/抽象摘要(支持集合, 生成器版本)` → `embedding/索引(编码器/分块版本)` → `KV(模型, tokenizer/输入, 位置/前缀, 精度)` → `活跃工作集/答案`。

各箭头是独立依赖；实际系统未存此字段就写缺测，不“善意补齐”。

| 动作 | 必须答的对象/权限 | 便宜但不充分的替代 |
|---|---|---|
| 追加 | 哪些父节点/视图/索引受影响，是否允许读旧快照 | 只向向量库add新条目 |
| 修订 | 新source version是否让旧摘要/embedding/KV失效，读者看哪版 | 更新原文后不处理派生物 |
| 撤销支持 | 是否有其他独立支持可保留事实；派生记忆可否重新证明 | 所有祖先全删，或只将源标为不可见 |
| 历史查询 | “当时为真”“当时系统已知”“现在所知的过去”分哪两轴 | max(timestamp)总取最新 |
| 外置 | 载荷在哪里、地址是否仍有效、读入成本和身份验证 | 将CPU/SSD容量当免费无限源 |
| 淘汰 | 只释放当前prompt/GPU，还是删CPU/SSD派生副本/原文 | 都叫forget/discard |
| 重算 | 原文/变换/模型版本可否再现，恢复结果允许什么误差 | 重算被已撤销源重新生成，或以最新版编码静默替代旧版 |
| 物理删除 | 底层旧值、日志、副本/备份、再生路径完成何时可证明 | 删除API返回成功/向量检索不到 |
| 多问摊销 | 构建写入+更新+冷/热读取次数、询问前是否可见未来q | 只报第100次热命中或把离线整合费用省略 |

### 需明确写入后续卡的资源轴

持久源bytes、派生摘要/图/索引/KV bytes、活跃显存峰值、CPU驻留、SSD/网络读写量与耐久、每次写/撤销/刷新、冷/热回访、重编码/全量重建、查询次数/更新次数、并发/拒绝率/尾延迟。**压缩率、选中token少、理论复杂度低和服务实际更快四者不互换。**

## 5. 给terra的定向问题清单与排程

本轮不派代理、不改阅读队列。建议目录负责人按下列5个小批分配；每批输出原节/页/表、版本和未知项，不能只回“已读”。P1共20，P2按具体缺口升级。

| 批次 | P1局部ID | 必须交回的问题与判别结果 |
|---|---|---|
| T03-R2-A 身份/源权限（4） | 001,002,003,004 | HMT v1/v3/正式版对象与六作者；最近细路径vs远端摘要；why/where/how/dependency的适用定义；sources和因果必要性哪个能证明、哪个只能近似 |
| T03-R2-B 派生维护（5） | 005,006,007,009,027 | 更新/删除/规则变化的传播；多源替代证明；辅助状态大小与写放大；增量vs全量临界；DynaMat离线窗口与LLM实时写读冲突；把精确聚合与近似摘要分开 |
| T03-R2-C 时间与删除（5） | 010,013,014,015,029 | 双时间、快照、延迟视图隔离；lease写协调而非TTL；应用对象删到哪些store；墓碑持久清除的合同/上限；历史保留与撤销的冲突 |
| T03-R2-D 活跃集与再生（3） | 016,017,025 | 源不在GPU时是否仍可读；重入/换页成本；复用临界公式；lineage再生的确定性/源存活前提；源撤销后防复活 |
| T03-R2-E 实服务全账（3） | 018,022,024 | token源/压缩KV/分布式缓存的命名和失效；重算vs读缓存；单问/多问、冷/热、拒绝和尾延迟；锁近窗版本差异，不倒引旧稿 |

P2 008/011/012/019/020/021/023/026/028分别用于嵌套迭代、时间更新形式语义、一般增量重算、会话CPU/GPU缓存、极限外置吞吐、参数flash、SSD寿命、键值分离、中文原刊。不是每项都须立即全文精读；若某机制在P1已充分回答，可暂缓相邻P2。

### 跨文献追问（须用原文回答，不由本轮猜）

1. 原始来源保存究竟是逐字原文、token IDs、原KV、提取事件还是用户画像？保留期限和source-address是否稳定？
2. 摘要/源记录可修改时，父节点、事实、ANN索引、已算KV与答案缓存各怎样标脏？有没有反向依赖或代数支持，而非全表扫描？
3. 一个源撤销但事实有另一个独立支持时，是保留、降权、重证明还是误删？支持关系是否本身可能被LLM漏抽？
4. 历史查询、当前查询、晚到纠错同时存在时，哪一层维护有效时间、记录时间和模型版本？不同父节点能否来自不兼容快照？
5. 若摘要生成随机或模型版本改变，局部重算是否允许结果漂移？全量重算是校验oracle还是实际fallback？保存原文不保证编码器状态可重现。
6. 删除合同要求的是“此query不展示”、未来不检索、底层不存、备份到期清除、还是模型权重遗忘？谁承诺哪层，无法承诺处如何限范围？
7. query到来时发现派生状态陈旧，阻塞刷新、读旧、回源还是拒答？质量/时效风险如何进延迟和成本？
8. 多问摊销是否计首次构树/编码、每次源更新及所有未命中的查询？源和派生副本计总bytes，不能只比GPU工作集。
9. SSD/CXL/网络层的预取、传输重叠是不是依赖已知将来访问？层级导航按需串行展开时，这些流水前提是否仍成立？
10. 经典精确地址系统中的cache miss可检测；语义路由没命中相关源往往不可观察。两种“回退”区别是什么，是否需要保留精确源访问旁路？这是与T04交接边界，不在本轮扩为路由论文清单。

## 6. 尚未完成与下一轮只追关键缺口

- **已发现但未确认的经典**：2000 lineage tracing（多入口失败/乱码）、1995 warehouse view maintenance（原站403）、2002 deletion/annotation propagation（只有引文）、LSM-tree1996（返回无摘要）、SQL:2011（只有链接）。不计29，建议由terra/元数据负责人合法取原文，不能凭经典名气升级。
- **端到端源撤销仍缺证据**：关系推导、应用删除与物理compaction各有成熟局部解；本轮没有确认一个LLM系统同时覆盖原文→事实/多级摘要→embedding→KV→所有缓存/备份的可靠撤销协议，也**没有证明不存在**。
- **模型/编码器更新的跨版本失效**：本轮新作主要是数据版本/存储缓存；已有LongMem/CacheBlend/CachedAttention仍需与新作对读。原文再生与旧KV兼容不能用一个source ID免检。
- **真正的原文驻留实验**：多数LM摘要仍不报持久source bytes、缓存副本、读取IO及更新/擦除开销；这是后续精读缺测，不是可由我们补数字的空白。
- **近窗发展未穷尽**：已锁Mooncake2026-10 v5与LMCache2025-12 v2，未逐版比较。此次刻意优先数据库/系统经典，不以2026新模型数量证明时效性。
- **中文证据范围**：原刊028解决查询入口偏置的一部分，不证明中文/多脚本语义检索或字节因果消费已覆盖；该评价缺口归T08，不越权代证。

**建议继续，但不是再加模型清单。**先完成20项P1中的来源/更新合同与全成本核对；再只追“源撤销后再生/缓存复活”“异步多级摘要一致快照”“同源权限下外置/重算临界”三类会改变原型可行性的证据。若原文证实这些已由现成系统涵盖，差异句应改为明确预算/学习/评价条件；若缺测，研究前提应显式限制，不能当已解决基础设施。

## 7. 边界与交付验证

仅本目录新增本报告/日志，原地修T03-005。未改`02_catalog`、审计、草案、生产代码、证据注册表，未提交/推送、训练、另派代理、下载权重或使用付费资源。外部请求未含内部文档、配置或实验内容。

本轮是**发现/摘要初筛+少量方法定向核查**，不是terra精读，也没有实验/代码或性能复现。项目构建/训练/单元测试不验证本交付，不运行；验收使用本地只读Markdown结构、计数、去重和路径检查，结果见日志末尾。
