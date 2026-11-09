# T02 首轮检索日志

日期：2026-11-08。范围：信息压缩理论、任务充分性、未知查询、单槽/多槽与多粒度表示的能力边界。执行依据：`../../PLAN.md`。本目录只承担发现和摘要初筛，不承担 terra 全文精读或架构裁定。

## 实际口径与数量

- WebSearch：52次调用，51次返回检索结果，1次 HTTP 429。下表保留全部实际检索式；未为失败查询无限重试。
- FetchURL：59次调用。52次取得可读摘要/官方作品介绍，5次网络失败、1次403、1次仅返回页面标题而无摘要。
- 52件去重作品完成身份及摘要核验，列于 `CANDIDATES.md` 的 T02-001—T02-052。没有把搜索命中数当作品数；不同版本不重复计数。
- 核验深度：52项按摘要/官方介绍层计，全文精读0项、代码核验0项。工具返回全文不等于全文已读。三个PDF/长HTML入口也只用于摘要和局部定位。
- 27项列为下一轮精读优先（P1），见 `HANDOFF.md` 的精读问题矩阵。
- 首发处于2025-11-08—2026-11-08的作品7件；另有2件旧作的2026年版本更新入口，分别登记不增作品数。近期覆盖是有偏首批，不是全域扫描。
- 未调用学术数据源API，未使用学术数据源技能；未调用外部浏览器、未上传任何内部文档。检索仅使用公开机制词、公开题名与标识。

## A. WebSearch 实际查询

平台均为内置 WebSearch，执行日均为2026-11-08。关键词来自公共机制或已命中作品；少数熟悉题名/标识只用作定位入口，确认状态只取决于后续公开摘要核验。检索结果日期与作者字段可能错误，年份优先用作品页面的提交历史或正式出版信息。

|编号|实际查询（保留原文）|命中、用途或问题|
|---|---|---|
|S01|`information bottleneck sufficient representations unknown downstream tasks rate distortion multitask compression theory`|发现2610.30493；若干语义通信候选留待扩展。|
|S02|`information bottleneck theory sufficient statistics deterministic representations caveats deep learning Kolchinsky Amjad Geiger`|1808.07593、1802.09766、MASS；优先反例条件。|
|S03|`successive refinement information rate distortion Equitz Cover scalable coding side information Wyner Ziv`|逐级细化、侧信息谱系；2311.03061。|
|S04|`universal representations unknown downstream tasks deficiency Le Cam Blackwell information bottleneck Dubois lossless compression`|1810.11677、Raginsky 2011；未知任务的风险比较。|
|S05|`transformer recurrent memory capacity lower bounds associative recall compression finite precision 2024 2025`|2508.19029等；宽泛查询命中少。|
|S06|`"Zoology" "Recall" arxiv`|2312.04927，正式版入口也出现在结果中。|
|S07|`"repeat after me" transformers state space models copying arxiv`|2402.01032；排除博客强于原文的推广。|
|S08|`"Lossy Compression for Lossless Prediction"`|2106.10800、NeurIPS 2021；结果混有无关图像压缩。|
|S09|`"Compressing Representations for Classification" Dubois`|未找到该精确题名；得到2504.13191。此查询不是已存在作品证明。|
|S10|`"Successive refinement of information" Equitz Cover abstract`|经典逐级细化引用链，首轮未定位作者PDF。|
|S11|`"Deep Sets" "limitations" "latent" Wagstaff`|HTTP429，未当成功检索；后续换较具体检索式S12。|
|S12|`"Deep Sets" "Universal Approximation" "Limitations" Wagstaff arxiv`|Wagstaff 2019、2107.01959；连续性和维度条件。|
|S13|`"single vector" "multi vector" "retrieval" theoretical bottleneck`|2603.29519及LIMIT评论入口；只核验原文。|
|S14|`"information bottleneck" "successive refinement"`|Charvin等2023，PMC10528077；高度相关理论。|
|S15|`"RAPTOR" "Recursive Abstractive" "MemTree"`|RAPTOR、MemTree、2603.21564。|
|S16|`"query" "compression" "rate-distortion" "2026"`|2607.08032、2608.14528；近期未知查询与交接。|
|S17|`"multigranular" "retrieval" "2025" "2026"`|2606.15906，页面与元素图证据；跨专题最近邻。|
|S18|`"information bottleneck" "distributed" "Gaussian" "Estella"`|1709.09082；多编码器不等于单编码器多槽。|
|S19|`"information bottleneck" "self-supervised" "Sufficient" Tsai`|2006.05576、2304.09355；多视图充分性条件。|
|S20|`"What Makes for Good Views for Contrastive Learning" arxiv`|2005.10243。|
|S21|`"Understanding Contrastive Representation Learning through Alignment" arxiv`|2005.10242，仅留相关线索，未进入确认候选。|
|S22|`"Fundamental Limits of Prompt Compression" arxiv`|2407.15504、NeurIPS2024，查询可见性。|
|S23|`"Limitations of Embedding-Based Retrieval" arxiv Weller`|2508.21038；与2026年反驳材料成对。|
|S24|`"2608.14528"`|补核精确题名；arXiv题名与摘要对应。|
|S25|`"2610.30493"`|补核完整副标题：An Information Bottleneck Analysis。|
|S26|`"2603.21564"`|补核题名；会议主会/工作坊说法冲突，交下一轮核验。|
|S27|`"linear attention" "capacity" "2025" "2026" theoretical associative memory`|2602.04852、稀疏扩状态候选；后者未摘要核验。|
|S28|`"MUVERA" "arxiv"`|2405.19504；结果提到2026修订，需核定理论修订。|
|S29|`"Communication Complexity" "Transformers" "memory" Sanford Hsu Telgarsky`|2406.09347及其他表达能力论文，避免混为学习结论。|
|S30|`"To Compress or Not to Compress" "arxiv"`|2304.09355；大量模型权重压缩同名结果排除。|
|S31|`"Decodable Information Bottleneck"`|2009.12789、NeurIPS2020；受限读出器。|
|S32|`"Usable Information" "Predictive" arxiv Xu`|2002.10689；计算受限信息。|
|S33|`"Fundamental Limitations of Measuring Mutual Information"`|实际题名为Formal Limitations…，PMLR108。|
|S34|`"Predictive Information" "Complexity" Bialek arxiv`|physics/0007070；另有早期相关稿不自动合并。|
|S35|`"The Deterministic Information Bottleneck"`|1604.00268；与Decodable IB同缩写但不是同一作品。|
|S36|`"Matryoshka Representation Learning" arxiv`|2205.13147；嵌套维度不等于空间/来源粒度。|
|S37|`"Native Sparse Attention" arxiv`|2502.11089；粗压缩+细选择最近邻。|
|S38|`"Set Transformer" arxiv`|PMLR97/lee19d；诱导点多槽。|
|S39|`"Slot Attention" arxiv`|2006.15055、2406.09196；物体槽的适用域。|
|S40|`"Successive refinement of information" "75242"`|IEEE原始出版标识；Fetch只返回标题。|
|S41|`"Shannon Meets Blackwell and Le Cam"`|参考链命中；作者PDF在S04已出现。|
|S42|`"Coarse-Graining and the Blackwell Order"`|1701.07602；输入粗化与输出退化的区别。|
|S43|`"Information Bottleneck for Gaussian Variables"`|新推广与经典论文引用；经典JMLR入口后续直接核验。|
|S44|`"Fixed-Length Lossy Compression in the Finite Blocklength Regime" arxiv`|1102.3944、Caltech作者仓。|
|S45|`"The rate-distortion function for source coding with side information at the decoder" abstract`|主要是后续引用/扩展；Wyner–Ziv原始作品尚未完成摘要核验，不入确认数。|
|S46|`"multi-granularity" "theory" "information bottleneck" 2026`|2609.14421、粒球聚类等；缺少原文摘要核验，不背书。|
|S47|`"unknown queries" "compression" "lower bound"`|Compression for Quadratic Similarity Queries；零漏召回签名+回访很相关。|
|S48|`"Compression for Quadratic Similarity Queries" authors 2015`|补核年份2015、作者入口和IEEE对应。|
|S49|`"2103.03206" "Perceiver"`|补核精确题名，区分Perceiver IO。|
|S50|`"1802.09766"`|补核当前题名与早期How (Not)…题名关联，不重复计数。|
|S51|`"physics/0004057" "information bottleneck method"`|补核作者、经典原稿入口；1999工作/2000上传分列。|
|S52|`"Successive refinement of information" Equitz Cover Stanford pdf`|定位作者公开PDF0269equi.pdf，弥补IEEE标题壳。|

## B. FetchURL 调用台账

“确认”仅指摘要与作品身份；页面抽取有时省略标题/作者，精确题名由上表对应的检索返回和稳定ID补核。作者未从原始元数据取得时，在候选表明确留待补，不把`From:`提交人当作者。

下表按实际批次顺序编号。`A`=可读摘要/官方介绍；`ERR`=网络失败；`403`=拒绝；`SHELL`=只有标题。目标URL与候选表互相对应，供复跑。

|调用|目标URL|结果/关联作品|
|---|---|---|
|F01|https://arxiv.org/abs/physics/0004057|ERR；F12补成功|
|F02|https://arxiv.org/abs/1612.00410|ERR；F11补成功|
|F03|https://arxiv.org/abs/1808.07593|ERR；F13补成功|
|F04|https://arxiv.org/abs/1802.09766|ERR；F14补成功|
|F05|https://proceedings.mlr.press/v97/cvitkovic19a.html|A；T02-001|
|F06|https://arxiv.org/abs/1810.11677|A；T02-002|
|F07|https://arxiv.org/abs/2106.10800|A；T02-003|
|F08|https://arxiv.org/abs/2312.04927|A；T02-004|
|F09|https://arxiv.org/abs/2402.01032|A；T02-005|
|F10|https://arxiv.org/abs/2504.13191|ERR；F15补成功|
|F11|https://arxiv.org/abs/1612.00410|A；T02-006|
|F12|https://arxiv.org/abs/physics/0004057|A；T02-007|
|F13|https://arxiv.org/abs/1808.07593|A；T02-008|
|F14|https://arxiv.org/abs/1802.09766|A；T02-009|
|F15|https://arxiv.org/abs/2504.13191|A；T02-010|
|F16|https://arxiv.org/abs/2610.30493|A；T02-011|
|F17|https://proceedings.mlr.press/v97/wagstaff19a.html|A；T02-012|
|F18|https://arxiv.org/abs/2107.01959|A；T02-013|
|F19|https://arxiv.org/abs/1703.06114|A；T02-014|
|F20|https://arxiv.org/abs/2603.29519|A；T02-015|
|F21|https://www.mdpi.com/1099-4300/25/9/1355|403；不重试该站；合法公开PMC副本F28|
|F22|https://arxiv.org/abs/2603.21564|A；T02-016|
|F23|https://arxiv.org/abs/1709.09082|A；T02-017|
|F24|https://arxiv.org/abs/2006.05576|A；T02-018|
|F25|https://arxiv.org/abs/2005.10243|A；T02-019|
|F26|https://arxiv.org/abs/2407.15504|A；T02-020|
|F27|https://arxiv.org/abs/2508.21038|A；T02-021|
|F28|https://pmc.ncbi.nlm.nih.gov/articles/PMC10528077/|A；T02-022；长页返回被工具存档，只取摘要|
|F29|https://arxiv.org/abs/2607.08032|A；T02-023|
|F30|https://arxiv.org/abs/2608.14528|A；T02-024|
|F31|https://arxiv.org/abs/2606.15906|A；T02-025|
|F32|https://arxiv.org/abs/2401.18059|A；T02-026|
|F33|https://arxiv.org/abs/2410.14052|A；T02-027|
|F34|https://arxiv.org/abs/2311.03061|A；T02-028|
|F35|https://arxiv.org/abs/2405.19504|A；T02-029|
|F36|https://arxiv.org/abs/2602.04852|A；T02-030|
|F37|https://arxiv.org/abs/2406.09347|A；T02-031|
|F38|https://arxiv.org/abs/2508.19029|A；T02-032|
|F39|https://arxiv.org/abs/2502.16869|A；T02-033|
|F40|https://arxiv.org/abs/1705.02436|A；T02-034|
|F41|https://arxiv.org/abs/2009.12789|A；T02-035|
|F42|https://arxiv.org/abs/2002.10689|A；T02-036|
|F43|https://proceedings.mlr.press/v108/mcallester20a.html|A；T02-037|
|F44|https://arxiv.org/abs/1604.00268|A；T02-038|
|F45|https://arxiv.org/abs/physics/0007070|A；T02-039|
|F46|https://arxiv.org/abs/2304.09355|A；T02-040|
|F47|https://arxiv.org/abs/2205.13147|A；T02-041|
|F48|https://arxiv.org/abs/2502.11089|A；T02-042|
|F49|https://proceedings.mlr.press/v97/lee19d.html|A；T02-043|
|F50|https://arxiv.org/abs/2006.15055|A；T02-044|
|F51|https://ieeexplore.ieee.org/document/75242/|SHELL；不足确认摘要；F59补齐|
|F52|https://maxim.ece.illinois.edu/pubs/raginsky_ISIT11.pdf|A；T02-045；仅摘要初筛|
|F53|https://arxiv.org/abs/1701.07602|A；T02-046|
|F54|https://www.jmlr.org/papers/v6/chechik05a.html|A；T02-047|
|F55|https://arxiv.org/abs/1102.3944|A；T02-048|
|F56|https://pmc.ncbi.nlm.nih.gov/articles/PMC5786438/|A；T02-049；另外定位§I–II的查询模型，不计全文精读|
|F57|https://arxiv.org/abs/2406.09196|A；T02-050|
|F58|https://arxiv.org/abs/2103.03206|A；T02-051|
|F59|https://isl.stanford.edu/~cover/papers/transIT/0269equi.pdf|A；T02-052；另定位§I/§III/§IV，不计全文精读|

## C. 排除、待核验与版本纪律

1. 不纳入确认计数：S09并未证实的题名、S21的2005.10242、S45的Wyner–Ziv原始1976论文、S46的2609.14421、S27的稀疏扩状态论文、S16的2608.04074、S17的若干图检索/多模态系统。它们只是后续搜索入口。
2. 博客、机器摘要、GitHub个人笔记、搜索日期与被引用次数均不作定理或效果证据。尤其S06、S35、S41等的搜索日期明显可能是抓取日期，不能作出版年份。
3. T02-007的1999会议归属与2000上传分开记；T02-006的2016上传/2017会议、T02-003的2021正式版/2022修订、T02-027的2024上传/2025修订等是同一作品。
4. T02-029的2026-06-08 v2已实际看到提交历史；搜索结果提到“corrected version”但未核定改了什么，因此只记有修订，理论保证要读最新版本并逐式检查。
5. T02-021原始2025-08，2026-03-12 v2摘要标Accepted to ICLR'26；T02-015是不同作品的2026反驳，不可互相吞并。
6. T02-016“Published as a conference paper at ICLR 2026”和其他来源的workshop归属不一致，未核实具体轨道，不能当主会接收背书。
7. 页面的`From:`仅代表提交人；候选作者字段缺失时留空或注明只核到首作者，不由提交人补造作者名单。

## D. 本轮边界

本轮完成一批可追溯的52件摘要初筛，不声称覆盖所有信息论、表示论或多粒度系统。未做引用网络穷举、全文证明校验、代码运行、真实延迟验证或项目证据迁移。后续扩展应优先补定理适用条件与反例，而非继续堆一般“压缩有效”案例。
