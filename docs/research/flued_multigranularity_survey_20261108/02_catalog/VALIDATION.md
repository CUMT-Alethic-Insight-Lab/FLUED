# 目录交付验收记录（R1/R2历史＋最新R3）

最新R7定版读取快照2026-11-08 07:28:11 +0800：230唯一尝试219FULL/11PARTIAL；此前R1–R6为历史。本轮不新增候选、W-ID或批次，不以期望代逐卡核验。
日期：2026-11-08。以下R1验收保留作历史，不表示当前项目仍全文0。当前阅读状态见[READING_STATUS](READING_STATUS.md)，身份核销见[METADATA_UPDATES_R2](METADATA_UPDATES_R2.md)，本轮验收见文末R2。目录本人未精读论文、不作科学综合。

## 交付文件与职责

所有路径共同前缀：`docs/research/flued_multigranularity_survey_20261108/02_catalog/`。

| 文件 | 交付内容 |
|---|---|
| `CATALOG.md` | W0001–W0384、原生稳定键、标题、论文/官方介绍类型、已有作者/年份/版本与原始入口、419条local映射、阅读主深度、全文入口及排程状态 |
| `COUNTS.md` | 419→384的去重依据；382篇论文+2项官方介绍；30个交叉作品/65次出现；首批40、后续167、储备175；阅读和元数据缺口 |
| `READING_QUEUE.md` | 8批首轮派工入口、167篇逐项后续候选、全文URL/具体问题/参考专题；全部204篇去重优先论文均已排程，另提升3篇必要反例/伴读 |
| `IDENTITY_AND_VERSIONS.md` | 30个跨专题重复实体表；不能误合并的同名/同缩写；39项具体版本/身份风险；未确认入口和访问阻塞；作者/正式版补核未完成项 |
| `batches/B01.md` | 5篇：SSA/H-SSA、Landmark、NSA、HISA、AttentionIndex；模型内部粗细寻址、原始KV、索引漏召回及完整成本 |
| `batches/B02.md` | 5篇：MemWalker、ReadAgent、RAPTOR、H-MEM、HORMA；外部多级摘要、源映射、下钻/回退和源生命周期 |
| `batches/B03.md` | 5篇：SCT、ReFind、强重排器反例、InMind、Evaluating Compressed Memory；强反例与内容收益 |
| `batches/B04.md` | 5篇：Repeat After Me、Lossy Compression for Lossless Prediction、Decodable IB、Successive Refinement、Quadratic Similarity Queries；理论权限与边界 |
| `batches/B05.md` | 5篇：Dynamic Token Pooling、BLT、H-Net、SpaceByte、boundary dependence；字节边界信号与计算效用 |
| `batches/B06.md` | 5篇：Test-time regression、MERLIN、MARCH、LoLA、Geometry-Based Capacity；地址/值载荷/缓存/键几何 |
| `batches/B07.md` | 5篇：Mixture-of-Recursions、Attention Residuals、Dynamic Parameterization、DynaKRAG、AFABench；动态执行、控制回放、非短视效用 |
| `batches/B08.md` | 5篇：ByT5、多维无分词评价、Rate–Utility Frontiers、Amnesic Probing、Causal Probing Reliability；字节公平和干预可靠性 |
| `VALIDATION.md` | 本验收记录、确切批次路径、验证结果与未完成边界 |

## 主代理可直接分派的8个确切路径

1. `docs/research/flued_multigranularity_survey_20261108/02_catalog/batches/B01.md`
2. `docs/research/flued_multigranularity_survey_20261108/02_catalog/batches/B02.md`
3. `docs/research/flued_multigranularity_survey_20261108/02_catalog/batches/B03.md`
4. `docs/research/flued_multigranularity_survey_20261108/02_catalog/batches/B04.md`
5. `docs/research/flued_multigranularity_survey_20261108/02_catalog/batches/B05.md`
6. `docs/research/flued_multigranularity_survey_20261108/02_catalog/batches/B06.md`
7. `docs/research/flued_multigranularity_survey_20261108/02_catalog/batches/B07.md`
8. `docs/research/flued_multigranularity_survey_20261108/02_catalog/batches/B08.md`

每批均有确切W-ID/原生ID/论文题名/全文URL、5篇逐项问题、全部参考专题路径和统一验收字段。40篇跨批不重复；8专题全部有原始local映射。主代理按PLAN分配原文阅读负责人，本目录未派子代理。

## 已执行验证

以本地Python标准库读取实际Markdown进行独立结构检查，未运行项目构建/单元测试（本任务无生产代码变更，项目测试不验证文献目录）。验证脚本是本目录内临时工具，交付前删除，只保留Markdown；没有安装依赖或网络请求。

执行的验证入口：`PYTHONIOENCODING=utf-8 python docs/research/flued_multigranularity_survey_20261108/02_catalog/_validate_catalog.py`。实际输出均为PASS：

- 8个CANDIDATES的56/52/51/53/52/55/55/45卡逐卡回读，合计419；每个local ID恰映射一次，未丢失、未重复认领。
- CATALOG恰有384个唯一W-ID和384个唯一原生键，W0001–W0384连续；382论文+2官方介绍。主键与源卡原始标识相符，论文/介绍未混计。
- 跨专题重复30个实体、65次出现，多计35；优先出现218次去重205个实体，含204篇论文+1官方介绍。
- B01–B08各5篇、40个唯一W-ID，每篇有具体问题和参考专题路径；每篇在CATALOG状态与批次一致，所排原生ID与全文URL/正式版关联相符。
- Q001–Q167连续，167个唯一论文ID，原生键/状态与CATALOG一致；与首批40完全不交叉；阅读候选总207，论文储备175。
- 全部204个去重优先论文都在207篇队列内；另提升3篇为T07-044、T08-044、T05-028，不利用未确认入口凑数。
- 所有Markdown相对链接目标存在，所有`#L`参考定位到真实候选标题行；批次的`../../01_search/`相对层级已核对。
- 每专题首次出现/重复分摊从独立local映射重算一致；文档UTF-8无替代字符。

初次生成与校验中发现并修正：PMC正文入口/OpenReview全文URL格式；T02/T07题名前的分隔符；批次相对路径；《Lost in the Middle》正式版—预印本重复；一次临时计数格式化误改标识。最终独立检查从源卡到目录及全文链接逐项对照，已全部通过，未将失败的中间生成结果交付。没有由此更改01_search原始资料。

Git检查：开始时仓库已有未跟踪调研根目录、原研究草案和4个bundle；本轮只在02_catalog创建文件。完成后用`git status --short --untracked-files=all -- <02_catalog路径>`及最终文件枚举确认交付只有上述13个Markdown，临时脚本删除；未执行git提交/重置/推送。共享目录其他代理的文件均未修改或清理。

## 不能由静态PASS推出的事项

- 未逐项独立网络核验标题/作者、DOI、会议轨道、首发日期；继承的是8专题的原始来源记录。源卡空作者/日期异常/会议身份缺口已原样留痕，不从arXiv提交人补作者。
- 全文URL只是入口，未逐条下载；全文精读0、代码核验0、独立复现0，不以下载入口或摘要细节冒充证据卡。
- QuickMerge++撤回状态、LapMerge/MUVERA/HISA/MiTA版本、DeepSeek/Bridge-RAG日期异常、相邻字节边界两作的独立性仍待追查；K3报告与LongCat2技术材料不能因官方介绍存在而视为读过论文。
- 207篇阅读候选足够排程约200篇，不代表证据闭合。广域500篇参考下界尚差118篇不同论文；应围绕漏召回可观测回退、源撤销失效链、同位预算单/多槽、UTF-8内容因果仪器、真实byte共享对照和标签/系统完整成本扩展，而非只补新标题。
- 不改源码、不训练、不提交、不另派代理、不输出最终科学综合；未完成的元数据及全文任务必须由主代理后续安排。


## R2续轮验收（2026-11-08；覆盖R1当前状态）

### 本轮改动路径

共同前缀 `docs/research/flued_multigranularity_survey_20261108/02_catalog/`：

- 更新 `CATALOG.md`、`COUNTS.md`、`READING_QUEUE.md`、`IDENTITY_AND_VERSIONS.md`、`VALIDATION.md`。
- 更新 `batches/B01.md`–`batches/B08.md` 的阅读状态/已核身份提醒，不改03_reading卡或01_search源卡。
- 新增 `READING_STATUS.md`、`METADATA_UPDATES_R2.md`。
- 新增 `batches/B09.md`、`batches/B10.md`、`batches/B11.md`、`batches/B12.md`、`batches/B13.md`、`batches/B14.md`、`batches/B15.md`、`batches/B16.md`。

### 主代理下一轮8个确切批次路径

1. `docs/research/flued_multigranularity_survey_20261108/02_catalog/batches/B09.md`
2. `docs/research/flued_multigranularity_survey_20261108/02_catalog/batches/B10.md`
3. `docs/research/flued_multigranularity_survey_20261108/02_catalog/batches/B11.md`
4. `docs/research/flued_multigranularity_survey_20261108/02_catalog/batches/B12.md`
5. `docs/research/flued_multigranularity_survey_20261108/02_catalog/batches/B13.md`
6. `docs/research/flued_multigranularity_survey_20261108/02_catalog/batches/B14.md`
7. `docs/research/flued_multigranularity_survey_20261108/02_catalog/batches/B15.md`
8. `docs/research/flued_multigranularity_survey_20261108/02_catalog/batches/B16.md`

每批10篇，80篇全部来自原167，和首批40完全不交叉；Q/W/原生ID不重编号。MoG、ReMemR1、MAGE-RAG、A-RAG被前移，生命周期/双时间/冷回访、遗漏与预算、非短视标签、理论权限、字节脚本、系统和形成史按红队F1–F8覆盖。经典/中文原池缺口不能靠调序解决，见METADATA_UPDATES_R2。

### 当前实计及核销

- 40卡实际落盘；38 FULL、2 PARTIAL（W0050、W0339），整篇阻塞0、缺卡0。B02起初4/1，工作期间W0142实际补Table 7–8/Figure 1–3且卡/总结同步FULL，最终5/0。按文件更新统计，不按任务超时/派工回执推算。
- 发现审计28对象身份记录已回填目录；H-MEM作者二人/题名前缀、W0156前缀、LapMerge v2明确核销。证据卡补首作者的字段标“目录未独立重核”，科学疑点不升格论文错误。
- 原419→384去重账不变；HMT按覆盖审计v1身份核验查重后追加W0385。当前385实体=383论文+2官方介绍；候选208=首批40+原167+HMT1，储备175。HMT最新版本待锁、无terra卡，X001补充待排，不占80。
- 80新排+87原队列待分批+2部分+HMT1，共170个候选尚未完整完成；不是宣称120篇已读。
- ByT5限定Large配置静态核验1，实验复现0；目录本人没有精读论文、运行实验或作最终综合。

### 验证方法与未完成边界

使用本目录临时Python标准库校验器 `_validate_r2.py` 从交付Markdown与实际03_reading文件独立复算：作品/原生ID唯一、419映射保留、40状态/指纹/批总结一致、80×来源/题名/问题/全文链接、8×10且不与40重复、Q167不丢/剩87、HMT不偷占名额、相对路径与源卡行号、错名仅历史记录、版本已核/未核边界和仅MD交付。实际执行结果：上述六组检查全部PASS；40张卡的SHA12与文件一致，原167拆80＋87及8×10均通过。校验器运行后删除，不保留脚本/缓存。项目无生产代码变更，不运行与文献目录无关的构建、单测或训练。

静态PASS不验证论文定理、原始数据或第三方卡的意见；没有网络重抓全文/作者页。HMT最新版、各卡数学/统计疑点、两张PARTIAL补充材料及尚缺中文/经典正式源仍需主代理分别派给拥有者。T03源卡已由其所有者并发修正H-MEM，目录只读复查并刷新419个local ID的行号引用，未修改外部文件。Git只读状态检查与MD内容校验同时做；未跟踪文件的diff空输出不能单独证明内容正确。

## R3：R2扩展归并、120卡和B17–B24验收

### 本轮触及的全部文件（仅02_catalog）

- CATALOG.md、COUNTS.md、READING_QUEUE.md、READING_STATUS.md、IDENTITY_AND_VERSIONS.md、METADATA_UPDATES_R2.md、VALIDATION.md：更新当前总账、版本和状态；新建EXPANSION_MERGE_R2.md。
- batches/B01.md–B16.md：同步实际卡状态和已核版次主标题；历史提问不冒充当前未知或新阅读。
- 新建batches/B17.md–B24.md：各10篇、共80，与前120和批间互斥。

### 主代理八批确切路径

- `docs/research/flued_multigranularity_survey_20261108/02_catalog/batches/B17.md`
- `docs/research/flued_multigranularity_survey_20261108/02_catalog/batches/B18.md`
- `docs/research/flued_multigranularity_survey_20261108/02_catalog/batches/B19.md`
- `docs/research/flued_multigranularity_survey_20261108/02_catalog/batches/B20.md`
- `docs/research/flued_multigranularity_survey_20261108/02_catalog/batches/B21.md`
- `docs/research/flued_multigranularity_survey_20261108/02_catalog/batches/B22.md`
- `docs/research/flued_multigranularity_survey_20261108/02_catalog/batches/B23.md`
- `docs/research/flued_multigranularity_survey_20261108/02_catalog/batches/B24.md`

### 实计、验证及剩余边界

- 5专题扩展实际152卡，不是151卡；HMT1为既有W0385的v3/正式版更新。逐主键/明确别名/规范题名去重后净新151＝论文/报告150＋博士论文1，未发现另一跨扩展重复；不是先信151再加。536实体＝533论文/报告＋1博士论文＋2官方介绍。
- 120实际证据卡/16批总结，FULL117、PARTIAL3、BLOCKED0、缺卡0。逐卡SHA12和范围链接在READING_STATUS；补读/新版不重复作品，FULL不认证理论/实现。
- 本轮80＝扩展净新66＋已有未读14（HMT1、首轮余优先13），原Q剩74、扩展净新剩85；总候选359＝已尝试120＋新80＋未排159，原175储备不变。任务书累计200不是已读200。
- 身份更新包括HMT六作者/题名/正式DOI、SATFormer v3题名和作者、MemoRAG v3题名/作者顺序、DISRetrieval v1/v5及ReMemR1/MemTree后版范围；保留旧版本，不从题名或作者变化造新作。RDD/DiskANN/中文作者/DOI异常未猜补。
- 先前理论争议仅按READING_AUDIT_R1具体范围交接，不新增科学裁决。新卡的形式/统计疑点仍待独立红队；未因材料读到就核准证明，也未因未复证就降为未读。
- 用本目录临时标准库校验器 `_validate_r3.py` 从实际Markdown独立复算扩展映射/主键唯一/旧ID冻结/类型/120状态指纹/80互斥/精确来源和问题/旧Q及扩展候选不丢/所有相对链接与源行号/UTF-8。实际执行六组独立检查全部PASS：536主键/571映射、152扩展去重、120卡状态/指纹、8×10互斥来源、359候选分解和32份Markdown链接/UTF-8均通过。运行后删除3个本轮临时脚本，只交付Markdown。
- 未运行项目pytest/构建/训练：无生产代码改动且这些测试不验证文献结论。没有联网重抓全文/身份、执行论文代码、提交或改02_catalog之外文件；用git只读状态与内容校验共同验收，不把未跟踪diff空结果当内容证明。


## R4：200卡当前快照、审计回填与补证20

### 触及文件（均仅02_catalog）

- 更新CATALOG.md、COUNTS.md、READING_STATUS.md、READING_QUEUE.md、IDENTITY_AND_VERSIONS.md、METADATA_UPDATES_R2.md、VALIDATION.md；B01–B24任务书仅同步状态/现行标题。
- 新增STATUS_AND_NEXT.md、SYNTHESIS_INPUTS.md、AUDIT_METADATA_SYNC.md及batches/B25.md、batches/B26.md。其他目录未写。

### 实际数与决策合同

- 快照2026-11-08 05:20:47 +0800，前200不同W-ID卡/24总结实际存在；FULL190/PARTIAL10/BLOCKED0/缺卡0。初查05:11:30为183/17，恢复状态可变，当前以卡指纹/范围而非旧审计回执。
- 536实体＝533论文/报告＋1博士论文＋2官方介绍不变。359候选＝200尝试＋20新补证＋139未排；原储备175不变。累计220任务书不等220已读，更不以达200FULL为停止合同。
- B25 10篇安全评分/尾部召回/维护/双时间/再生/地址载荷/付费信息/知识梯度；B26 10篇跨语种/脚本/原生QA/多语检索/因果表达力和争论双方。均是已有确认身份且公开全文可追踪的高价值剩余项，未下载验证不冒充精读。
- 审计R1/R2/R3的身份修正仅用已核原字段；冲突双记，卡独有新身份标未独立审计；科学争议索引不代替原审计，新疑点不升错误，W0483解除回写。

### 验证

本目录临时标准库校验器_validate_r4.py独立核200实际状态/范围摘要/卡与总结SHA12、24旧批和新20的220互斥、536主键/571local映射不丢、未排候选139、审计同步/作者冲突与解除提示、综合路径、Markdown链接/行号/UTF-8。实际六组检查全部PASS：冻结身份/571映射、200卡与总结指纹、20补证互斥和精确来源、候选分解、审计/综合路径以及37份Markdown链接/UTF-8均通过；完成后删除3个本轮临时脚本，最终只交MD。项目无源码改动不运行无关pytest/构建/训练，不提交/执行论文代码/修改外部文件。

R4最终快照补记：2026-11-08 05:20:47 +0800；05:18:14 B22卡10/0而总结旧3/7，最终总结也已同步10/0；READING_STATUS保留变化过程，卡的实际补读范围决定读取数；B24卡已10/0。WAND出版方入口本轮未取而暂缓，B25改Multi-probe LSH公开VLDB入口，避免给“全文可得”未经核验的背书。


## R5：当前220尝试同步、OPEN_ITEMS和暂停新增

### 触及路径（仅02_catalog）

- 更新CATALOG、COUNTS、READING_STATUS、READING_QUEUE、STATUS_AND_NEXT、SYNTHESIS_INPUTS、AUDIT_METADATA_SYNC、IDENTITY_AND_VERSIONS、METADATA_UPDATES_R2、VALIDATION；B01–B26任务书只同步实际状态头，不改历史提问/科学结论。
- 新建OPEN_ITEMS.md；没有创建B27、精读卡或新科研综合稿，没有修改03_reading/05_review/源码。

### 当前实计与类别

- 读取时间2026-11-08 05:53:34 +0800，536唯一实体＝534学术（533论文/报告＋博士论文1）＋2官方，571local映射/原生主键/归并总账不变。
- 220尝试/220实际不同W-ID卡/26总结：FULL210/PARTIAL10/BLOCKED0/缺卡0；卡及总结SHA12、时间和不同步提醒见READING_STATUS；B25/B24补读可改变后续状态。
- 非FULL互斥主因A材料未取或版本未锁5、B作者自有承重证明未提供5、C材料可取尚未读完0，总10；交叉标签不再加数。不是全部访问失败，不把未取得证明当命题错误。
- 220选为四阶段40＋80＋80＋20决策样本：近邻/反例/理论权限/byte仪器→剩余重点→经典/扩展缺口→最后20补证，不是FULL数量配额。359候选＝220尝试＋139未编批；再加175储备＝534，官方2另列。

### 覆盖红队和数学边界

- 已读COVERAGE_AUDIT_R2：可开始有条件综合、不声称饱和或H1–H5已证。D1–D12依强主张触发补查，不要求把所有未读或自有证明补齐再写概念综合。
- 只保留/回填已核身份，作者冲突双记；覆盖R2未新增外部身份访问不能当新作者认证。R3历史表算术/抽样8与9差异按其§1.3登记，不改其文件。
- 目录不复证/核销数学争议，R1/R2/R3局部裁决和解除点按具体范围引用；FULL非理论认可，缺证明非反例。

### 验证

用本目录临时标准库校验器_validate_r5.py复算536主键/571local、534学术＋2官方、220尝试/状态及卡/总结指纹、26批不增不丢、OPEN_ITEMS互斥主因与实例事实/活动非FULL映射、候选139/储备175层级、所有Markdown路径/源行号/UTF-8和纯MD最终交付。实际执行六组检查全部PASS：536身份/571映射、220卡与26总结指纹、10项分类A5/B5/C0、未读层级、红队/元数据边界、38份MD路径/UTF-8均通过。运行后删2个本轮临时脚本，仅留Markdown。没有运行项目pytest/构建/训练：这些不验证文献状态；未执行论文代码、提交或写目录外文件。


## R6：最终补充去重/路径索引与读取快照

### 触及文件（仅02_catalog；不改任何03_reading名）

- 更新CATALOG、COUNTS、READING_STATUS、OPEN_ITEMS、READING_QUEUE、STATUS_AND_NEXT、SYNTHESIS_INPUTS、AUDIT_METADATA_SYNC、IDENTITY_AND_VERSIONS、METADATA_UPDATES_R2、VALIDATION；新增FINAL_ADDENDUM_INDEX.md。原B01–B26任务书不再新派工，未创建B27，不改FINAL原文件路径。

### 实计和归并依据

- 快照2026-11-08 07:03:23 +0800，7 relation候选的主键/规范题名/明确别名在旧536无匹配，新增W0537–W0543；6实际卡都是前6新作品，第7RD07只发现。背景review不计。
- FINAL_RECENT四卡映射既有W0157/58/59/60，新增实体0；NSA只复核旧W0098卡，不是第11张最终卡/第231个新尝试/FULL。
- K3固定报告已得，README/Git blob/raw PDF关联同W0160，新增Git稳定来源别名不新编号；类型从仅介绍变技术报告（与旧介绍关联），报告/main README同版和日期未核。
- 当前543实体＝541论文/技术报告＋博士论文1＋纯官方介绍1＝542学术＋1介绍；旧536＋7，不因K3来源/类型变更新增实体。
- 旧220 FULL210/PARTIAL10未被目录随意升级；最终关系6 FULL4/PARTIAL2，近期4 FULL1/PARTIAL3；共230唯一尝试 FULL215/PARTIAL15/BLOCKED0。两FINAL在补读，指纹锁当前。
- 候选367＝230尝试＋137未尝试候选；原175储备保持，学术542＝230＋137＋175。原571local＋RD7＝578映射，原W/主键冻结。

### 验证及科学边界

使用本目录临时标准库校验器_validate_r6.py核全部W/原生主键/类型、578local、RD7与六路径及4既有路径/NSA0增量、K3稳定Git别名/同实体类型重分类、230实际状态和旧初期PARTIAL/摘要/审计未自动升FULL、所有卡/总结SHA12、候选分解、Markdown路径/行号/UTF-8及纯MD最终交付。实际六组检查均PASS：543身份/578映射、K3同实体Git别名及类型、230实际卡与28总结指纹、旧10PARTIAL不自动升级/NSA零增量、候选分解及39份Markdown路径/行号/UTF-8均通过。完成后删除3个本轮临时脚本，最终纯Markdown。

已读最新R4/CLAIM_RESTRICTIONS/两终审；只把R4撤回旧误判和CRC引用门列索引，不重新裁数学。关系r与元数k/加工L/尺度G/时间T不混、点名路径补读不自动核销终审P1、更不证明H1–H5/首创/全域文献已完成。没有训练、运行论文代码、提交或修改目录外文件；无源码变更不运行不能验证文献目录的pytest/构建。


## R7：台账定版同步与可引用数字

### 触及文件（仅02_catalog）

更新COUNTS、READING_STATUS、OPEN_ITEMS、FINAL_ADDENDUM_INDEX、SYNTHESIS_INPUTS、VALIDATION，并同步CATALOG及相邻STATUS_AND_NEXT/READING_QUEUE/IDENTITY_AND_VERSIONS/AUDIT_METADATA_SYNC的现行状态头，避免同一台账互相矛盾。没有新增候选、稳定ID、批次、原文卡或综合正文，也不修改03_reading文件名/内容。

### 实际核验结果

- 时间2026-11-08 07:28:11 +0800。从230实际原卡逐项识别阅读状态、范围及原生路径，再校验两SUMMARY，得到旧220=210FULL/10PARTIAL；FINAL_RELATION6=6FULL；FINAL_RECENT4=3FULL/1PARTIAL；合计230=219FULL+11PARTIAL+0BLOCKED，缺卡0。先逐卡读，再对照用户预计，不反向填卡。
- 升级来自W0537、W0540、W0157、W0158四张原卡实际补读，219不是新增4项作品/尝试；NSA只旧W0098复核，新增读数0。K3仍同W0160固定报告PARTIAL，不升级FULL。
- K3前次已合法取得并读部分，临时件清理后本次两轮curl(56)连接reset未取HTTP码，非403/登录墙/来源不存在；代码未核/效果未复现单列，不当未读。11PARTIAL互斥主因A缺材料/同版对应5、B自有证明省略/外置/TODO5、C可得尚未读0、R工具reset1。
- 543实体=542学术(541论文/技术报告+1博士论文)+1纯介绍；原578local映射、Q167/E152和RD7、新旧稳定主键不变。候选367=230尝试+137未尝试；学术542=230+137+175储备；候选未完整148、学术未完整323不作继续阅读配额。

### 验证与边界

本目录临时标准库校验器_validate_r7.py独立复算543身份/类型/578映射、230实际状态/范围/路径与卡+28总结SHA12、原初期10PARTIAL不升级、四补读FULL和K3reset语义、NSA去重、11原因分类、最终索引与六指定文档数字/相对链接/行号/UTF-8及纯Markdown最终交付。实际执行六组检查全部PASS：543身份/578映射、230原卡及28总结指纹、关系6FULL/近期3FULL+K3PARTIAL与NSA零增量、11项主因A5/B5/C0/R1、总作者引用数字及索引/快照同步、39份Markdown路径/源行号/UTF-8均通过。完成后精确删除本轮_sync_r7.py和_validate_r7.py两个临时脚本，仅留Markdown。没有运行论文代码、训练、源码pytest/构建或提交；没有重新裁数学、核销终审P1或宣布全域研究完成。
