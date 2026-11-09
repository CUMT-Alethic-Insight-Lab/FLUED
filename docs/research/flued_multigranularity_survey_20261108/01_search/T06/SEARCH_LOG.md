# T06 首轮检索日志

日期：2026-11-08。执行边界：仅本目录；发现与摘要层初筛，不是 terra 全文精读。已先读 ../../PLAN.md；未改源码、证据表、术语表；未训练、提交、派生代理或上传内部文档。外部查询仅含公开题名、机制词和公开编号。

## 实际工作量与口径

- WebSearch 实际调用 **41 次**：39 次返回搜索结果，2 次工具失败（Q23 HTTP 429；Q34 HTTP 404）。返回结果不保证相关，Q36 为明显无关命中。
- FetchURL 实际调用 **57 次**：55 次成功取得一个作品的 arXiv 摘要页、ACL 摘要页或官方发布介绍；2 次网络失败，均各重试一次成功。成功结果覆盖 **55 个去重作品**，不是 57 篇。
- 确认候选 **55 项**：53 项以 arXiv 稳定编号登记、1 项以 ACL DOI 登记、1 项为 LongCat-2.0 官方发布介绍（不是同行评审论文）。完整身份与摘要/官方介绍均已取回；作者字段未完整抽取处明确留待补齐，不把提交人当作者。
- 深度：**54 项论文摘要核验、1 项官方介绍核验；全文精读 0，代码核验 0，独立复现 0**。LongCat-2.0 的介绍含系统设计小节，但仍按官方介绍而非全文实验核验。
- 精读优先 **28 项**，在 CANDIDATES.md 用 `★` 标记，并逐项给出问题。其余27项是扩展/对照队列，不是已排除。
- 本轮首次公开于近12个月（2025-11-08—2026-11-08）的确认候选 **19 项**；更早作品的2026修订不再计新作品。不是近12个月全域清单。
- 版本按稳定作品编号去重；Ouro、GateSkip 等改题/修订不重复计数。会议版本只在来源明确时挂关联，未逐一核对所有正式版差异。

## 检索平台与实际查询

全部 Q 项：平台 WebSearch；日期均为2026-11-08。顺序按实际检索批次；为可读性批次内部按主题列出。引号保留实际查询的公共关键词。搜索结果只作发现，候选确认另经下方 FetchURL。

### 批次1：用户草案入口与广域发现（Q01—Q04）

|编号|实际检索式|结果/去向|
|---|---|---|
|Q01|`"Attention Residuals" "2603.15031"`|找到 arXiv 原页；第三方 GitHub、Gist 不作官方证据。确认 T06-042。|
|Q02|`"LongCat2.0" technical report dynamic computation`|找到官方 longcat.chat/blog/longcat-2.0/；百度云、社区分析不作机制效果依据。确认 T06-049。|
|Q03|`transformer adaptive computation mixture depths token skipping recurrent depth actual latency`|发现 MoR；2605.05222 仅搜索发现，不计确认。|
|Q04|`transformer copy transform separate layers dynamic depth token routing memory reactivation`|发现 MoM；2609.17251、Leap-of-Thought 仅发现未确认。|

### 批次2：真跳算、成本与基础谱系（Q05—Q07）

|编号|实际检索式|结果/去向|
|---|---|---|
|Q05|`"copy" "transform" "layers" "2025" transformer LayerSkip`|发现 FlexiDepth、GateSkip、Balcony、近期服务论文。|
|Q06|`"mixture of depths" "skip" "latency" arxiv`|发现 M2R2、MoDification；2605.13190、γ-MoD 留待追查。|
|Q07|`adaptive computation time universal transformer depth adaptive transformer early exit CALM PonderNet`|基础种子 ACT、UT、PonderNet、Depth-Adaptive Transformer；综述及个人博客不作候选确认。|

### 批次3：共享层、跨层读取、零计算专家（Q08—Q13）

|编号|实际检索式|结果/去向|
|---|---|---|
|Q08|`"Adaptive Computation Time" "Universal Transformers" "PonderNet" arxiv`|取得公开编号1603.08983、1807.03819、2107.05407；CTM为待扩展。|
|Q09|`"DenseFormer" "LAuReL" "Hyper-Connections" arxiv`|找到 DenseFormer、LAuReL、DCA、mHC、SATFormer、LIMe、Depth-Attention、DAGFormer。|
|Q10|`"Skipping" "SkipDecode" "CALM" "LayerSkip" arxiv`|找到 LayerSkip；搜索摘要出现 River-LLM、SafeDepth，未取回摘要不计。|
|Q11|`"Huginn" "Ouro" "looped" transformers arxiv recurrent depth`|发现 LoopCD；若干第三方综述和模型传闻不背书。|
|Q12|`"LongCat-Flash" "zero" experts arxiv`|找到2509.01322；Flash-Thinking/Omni不因共享机制重复扩展计数。搜索日期错误，以原页提交史为准。|
|Q13|`"copy" "transform" "transformers" "layers" dynamic computation paper`|命中2402.13934反例入口，尚未取回摘要；术语检索偏宽。|

### 批次4：明确原始作品编号（Q14—Q21）

|编号|实际检索式|结果/去向|
|---|---|---|
|Q14|`"Scaling up Test-Time Compute with Latent Reasoning"`|确认 Huginn 公开编号2502.05171。|
|Q15|`"Ouro" "Looped Language Models" arxiv`|确认2510.25741；发现 LLA、MELT 与两跳检索干预研究。第三方关于“先算完再选出口”的说法仅列代码审计问题，不当已核实事实。|
|Q16|`"Confident Adaptive Language Modeling" "SkipDecode" arxiv`|找到2307.02628、1910.10073及引用线索。|
|Q17|`"Skip RNN" "Skipping State Updates" "Clockwork RNN"`|找到1708.06834。|
|Q18|`"copy" "transform" "LongCat" "Engram"`|找到 Engram/LongCat-Lite实现问题讨论，只作检索线索。|
|Q19|`"Mixture-of-Transformers" "copy" "2025"`|多为多模态专家复制，与本题carry/transform分离不同；未纳入候选。|
|Q20|`"Hyper-Connections" "MUDDFormer" arxiv`|找到2409.19606、2502.12170、2611.05984。|
|Q21|`"Depth-Adaptive Transformer" "Schwartz" "CALM"`|取得CALM编号2207.07061；Schwartz关键词未形成确认项。|

### 批次5：多时间尺度、静态查表、批调度与反例（Q22—Q29）

|编号|实际检索式|结果/去向|
|---|---|---|
|Q22|`"Highway Networks" "2015" arxiv carry transform`|找到1505.00387与1612.07771，避免将copy仅理解为输出复制。|
|Q23|`"A Clockwork RNN" "Phased LSTM" "Hierarchical Multiscale" arxiv`|**失败：HTTP429**；稍后Q30原式重试一次成功。|
|Q24|`"Learning to Skip for Language Modeling" arxiv`|找到2311.15436；2506.21103待追查。|
|Q25|`"conditional memory" "Engram" arxiv scalable lookup`|找到2601.07372、2603.10087、2605.20948，确认静态查表与计算分离入口。|
|Q26|`"Recurrent Transformer" "stale" "reactivation" token skipping`|无有效论文命中，多为软件订阅/代理重启的stale问题；不计，不继续原式重试。|
|Q27|`"looped" "depth-wise batching" "2026" inference`|找到CDB 2608.09444、WFD 2609.23033、TaH2 2609.35748；第三方列表只作定位。|
|Q28|`"ShortGPT" "The Unreasonable Ineffectiveness" layers arxiv`|找到2403.03853、2403.17887，作为静态剪层对照。|
|Q29|`"Reinforcement Pre-Training" "Inner Thinking Transformer" arxiv`|发现LoopRPT、ITT等；本轮仅继续确认ITT，不扩展所有潜在思维模型。|

### 批次6：重激活及最近邻（Q30—Q33）

|编号|实际检索式|结果/去向|
|---|---|---|
|Q30|`"A Clockwork RNN" "Phased LSTM" "Hierarchical Multiscale" arxiv`|Q23重试成功：找到1402.3511、1609.01704；Phased LSTM尚未获得完整身份+摘要，不计。|
|Q31|`"Inner Thinking Transformer" arxiv`|找到2502.13842及ACL2025正式版链接。|
|Q32|`"token" "reactivation" transformer pruning recycling`|找到2306.07050，含保留/重新激活的直接机制；跨模态证据，不能直接迁移语言结论。|
|Q33|`"Balcony: A Lightweight Approach" arxiv`|找到2503.05005；引用结果亦提供CoLT5编号2303.09752。|

### 批次7：元数据补齐与词义排错（Q34—Q37）

|编号|实际检索式|结果/去向|
|---|---|---|
|Q34|`"2605.20948" "2605.07721"`|**失败：HTTP404**。Q38、Q39拆为独立编号追查，非绕过访问限制。|
|Q35|`"LAuReL" "2411.07501" "authors"`|原始arXiv结果给出三位作者，补齐字段。|
|Q36|`"2402.02622" "2502.09245" "authors"`|结果明显无关，未采信；改用题名Q40/Q41。|
|Q37|`"copy transform" "language model" computation`|同名视觉贴图等无关结果；未找到该措辞对应的统一语言模型机制，不造术语谱系。|

### 批次8：确切标题与作者追查（Q38—Q41）

|编号|实际检索式|结果/去向|
|---|---|---|
|Q38|`"2605.20948"`|原始arXiv题名：Memory Grafting: Scaling Language Model Pre-training via Offline Conditional Memory。另发现TF-Engram 2607.07388，未确认。|
|Q39|`"2605.07721"`|确认MELT全题；引用中出现LT2、Solve the Loop，留待扩展。|
|Q40|`"DenseFormer: Enhancing Information Flow" authors`|原始arXiv/EPFL/NeurIPS元数据与作者信息；不额外计数。|
|Q41|`"You Do Not Fully Utilize Transformer's Representation Capacity" authors`|补齐LIMe作者；发现EMNLP2026正式版，关联而不另计。|

## FetchURL 确认台账

下列每行各成功Fetch一次，读取范围为页面提取出的摘要及提交历史；均非PDF全文精读。CANDIDATES.md 给出版本、机制、全文入口。除注明的2次失败重试外，无重复抓取。

|候选ID|实际成功请求URL|读取范围|
|---|---|---|
|T06-001|https://arxiv.org/abs/1603.08983|摘要/提交史|
|T06-002|https://arxiv.org/abs/1807.03819|摘要/提交史|
|T06-003|https://arxiv.org/abs/2107.05407|摘要/提交史|
|T06-004|https://arxiv.org/abs/1402.3511|摘要/提交史|
|T06-005|https://arxiv.org/abs/1609.01704|摘要/提交史|
|T06-006|https://arxiv.org/abs/1708.06834|摘要/提交史|
|T06-007|https://arxiv.org/abs/1505.00387|摘要/提交史|
|T06-008|https://arxiv.org/abs/1612.07771|摘要/提交史|
|T06-009|https://arxiv.org/abs/1910.10073|摘要/提交史|
|T06-010|https://arxiv.org/abs/2207.07061|摘要/提交史|
|T06-011|https://arxiv.org/abs/2307.02628|摘要/提交史|
|T06-012|https://arxiv.org/abs/2311.15436|摘要/提交史|
|T06-013|https://arxiv.org/abs/2404.02258|摘要/提交史|
|T06-014|https://arxiv.org/abs/2410.14268|摘要/提交史|
|T06-015|https://arxiv.org/abs/2404.16710|摘要/提交史|
|T06-016|https://arxiv.org/abs/2502.02040|摘要/提交史|
|T06-017|https://arxiv.org/abs/2503.23798|摘要/提交史|
|T06-018|https://arxiv.org/abs/2510.13876|摘要/ICLR2026标注/提交史|
|T06-019|https://arxiv.org/abs/2503.05005|摘要/提交史|
|T06-020|https://arxiv.org/abs/2403.03853|摘要/提交史|
|T06-021|https://arxiv.org/abs/2403.17887|摘要/提交史|
|T06-022|https://arxiv.org/abs/2410.20672|摘要/ICLR2025标注/提交史|
|T06-023|https://arxiv.org/abs/2502.05171|摘要/提交史|
|T06-024|https://arxiv.org/abs/2510.25741|摘要/提交史|
|T06-025|https://arxiv.org/abs/2507.10524|摘要/提交史|
|T06-026|https://arxiv.org/abs/2502.13842|摘要/提交史|
|T06-027|https://arxiv.org/abs/2605.07721|摘要/提交史|
|T06-028|https://arxiv.org/abs/2607.15456|摘要/提交史|
|T06-029|https://arxiv.org/abs/2608.09444|摘要/提交史|
|T06-030|https://arxiv.org/abs/2609.23033|摘要/提交史|
|T06-031|https://arxiv.org/abs/2610.02185|摘要/提交史|
|T06-032|https://arxiv.org/abs/2609.35748|摘要/提交史|
|T06-033|https://arxiv.org/abs/2611.05150|摘要/提交史|
|T06-034|https://arxiv.org/abs/2610.34639|摘要/提交史|
|T06-035|https://arxiv.org/abs/2402.02622|摘要/提交史|
|T06-036|https://arxiv.org/abs/2411.07501|摘要/提交史|
|T06-037|https://arxiv.org/abs/2502.06785|摘要/提交史|
|T06-038|https://arxiv.org/abs/2409.19606|摘要/提交史|
|T06-039|https://arxiv.org/abs/2512.24880|摘要/提交史；首次网络失败、原URL重试成功|
|T06-040|https://arxiv.org/abs/2502.12170|摘要/提交史|
|T06-041|https://arxiv.org/abs/2502.09245|摘要/提交史|
|T06-042|https://arxiv.org/abs/2603.15031|摘要/提交史|
|T06-043|https://arxiv.org/abs/2605.03953|摘要/提交史|
|T06-044|https://arxiv.org/abs/2606.05014|摘要/提交史|
|T06-045|https://arxiv.org/abs/2610.19625|摘要/提交史|
|T06-046|https://arxiv.org/abs/2611.05984|摘要/提交史|
|T06-047|https://arxiv.org/abs/2607.26192|摘要/提交史|
|T06-048|https://arxiv.org/abs/2509.01322|摘要/提交史；首次网络失败、原URL重试成功|
|T06-049|https://longcat.chat/blog/longcat-2.0/|官方发布介绍全文，包括架构/训练/推理小节；非论文精读|
|T06-050|https://arxiv.org/abs/2601.07372|摘要/提交史|
|T06-051|https://arxiv.org/abs/2603.10087|摘要/提交史|
|T06-052|https://arxiv.org/abs/2605.20948|摘要/提交史|
|T06-053|https://arxiv.org/abs/2303.09752|摘要/提交史|
|T06-054|https://arxiv.org/abs/2306.07050|摘要/提交史|
|T06-055|https://aclanthology.org/2024.emnlp-main.1164/|ACL摘要/作者/正式版元数据|

## 已发现但未确认/暂缓入口（不计55）

|入口|发现来源|本轮状态与原因|
|---|---|---|
|Adaptive Computation Depth via Learned Token Routing，2605.05222|Q03/Q07|仅搜索结果；身份与摘要未Fetch，不采信TSA效果。|
|Persistent Recurrent Memory Between Transformer Layers，2609.17251|Q04|仅发现；跨层状态是否保持原来源待查。|
|Leap-of-Thought，OpenReview `0SF6Kr1lrx`|Q04|仅发现；题名/版本/摘要均待确认。|
|N-vium，2605.13190|Q06|仅发现；“exact”及退出分布保证待查。|
|γ-MoD，ICLR2025结果链接|Q06|未取回原始摘要，正式标题/编号待补。|
|Do Efficient Transformers Really Save Computation?，2402.13934|Q13|仅发现；可补理论下界/反例，不能先写结论。|
|River-LLM，2604.18396；SafeDepth，2610.00815|Q10|KV缺层与安全代价扩展入口，未确认。|
|Continuous Thought Machines，2505.05522|Q08|非标准Transformer循环，需单独比较同步/状态成本，未确认。|
|LoopRPT，2603.19714；Solve the Loop，2605.12466；LT2，2605.20670|Q29/Q39|潜在训练/线性成本扩展，未确认。|
|Learning to Skip the Middle Layers，2506.21103|Q24|仅发现；与静态剪层、动态路由的区别待查。|
|Phased LSTM|Q23/Q30|题名线索，未完整核验编号+摘要；不得计确认。|
|TF-Engram，2607.07388|Q38|仅发现；SSD后备和预取的真实成本优先追查。|
|LongCat-Flash-Lite|Q18|仅实现讨论线索；未独立核验官方报告，不把讨论当模型证据。|

这些入口只是已发生检索的留痕，不是穷尽式排除表。没有结果不等于机制不存在。首轮已达到有效候选目标，但最近邻组合、长窗重激活与真实延迟仍有可能改变研究方向，必须扩展/精读，不能阶段终结。
