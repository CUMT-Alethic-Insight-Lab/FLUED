# T05 实际检索与核验日志

执行日期：2026-11-08。执行范围：线性注意力、快速权重、差分校正规则、状态空间、联想记忆；写入保持/干扰、键值分工、逐 token 与块地址、多槽读出及容量边界。

## 0. 实际工具与计数

- 阅读了 `../../PLAN.md` 及项目术语规范；未向外部服务发送内部文档、项目名称、实验结果或草案文本。搜索仅含公共机制词、公开作品标题/标识。
- 平台：`WebSearch`（工具内置网络搜索；后端具体索引未披露），`FetchURL`（公开页面提取）。**没有使用学术数据源、付费资源、登录会话或浏览器，也没有派代理。**
- WebSearch **36 次调用**：28 次返回结果，8 次 HTTP 429 失败。失败没有被伪记为已检索成功。后续在 FetchURL 核验间隔后，部分以收紧检索式重查；没有无限重试。
- FetchURL **56 次调用**：52 个不同确认作品各取得一次可用官方摘要/介绍；另 1 次对已确认 015 的 HTML 正文获取；2 次对 P01 仅取得无关页脚；1 次 OpenReview 校验墙。
- **去重确认 52 个作品；待核验 1 个；优先精读 26 个；全文精读 0；代码核验 0。** 版本、方法变体、预印本/正式版不另计。
- “52”只表示本轮选入并核验的作品，不是搜索命中总量。无关网页、参考文献片段和模型名单不作为独立确认项。
- 按首发日期，近 12 个月（2025-11-08—2026-11-08）确认作品 **24 个**；旧作的新版本单独记录，不重复计入新作品。002/007/009/024/028/041/047/049 等版本变化由 CANDIDATES.md 具体记录，不能以检索页面日期替代首发。

## 1. 分批实际检索式

以下编号记录实际调用次序（同一批并行请求的返回顺序可能不同），不是事后编造的建议检索式。来源列保留主要有效原始入口；所有入选作品的逐项 URL 和摘要核验见第 2 节及 CANDIDATES.md。

### B01：广域机制与检索边界（4 次成功）

| 调用 | 原样查询 | 实际结果与采用/排除 |
|---|---|---|
| Q01 | `linear attention fast weight programmers delta rule associative memory capacity interference` | 命中 2102.11174、PMLR 正式页、快速权重综述；选入 001。Semantic Scholar 显示 2017 日期与作品不符，改信 arXiv 提交史。未把综述片段当原始定理。|
| Q02 | `linear attention copying retrieval lower bound memory capacity Zoology associative recall` | 命中 2402.18668、2605.06946；博客有“from memory”引文，不采其结论。选入 002、026 并逐项取摘要。|
| Q03 | `linear attention key value compression separate address value aggregation multi slot memory` | 结果多为主题站和注意力教程，未直接核实独立地址/值理论；引导后续机制收紧，不将主题页计为论文。|
| Q04 | `2026 2025 Gated DeltaNet Kimi Delta Attention fast weight memory` | 命中 2605.22791、FLA 实现列表、Kimi Linear 公开标识；只将列表作线索，不把 Kimi K3/Qwen 新模型的二手宣传当确认候选。|

### B02：2026 新作、扩状态与近邻组合（6 次成功）

| 调用 | 原样查询 | 实际结果与采用/排除 |
|---|---|---|
| Q05 | `site:arxiv.org linear attention "2026" "memory" "capacity"` | 命中 SDM 2607.07386、MARCH 2608.12435、HOLA 2607.02303、RAM-Net 2602.11958、MERLIN 2610.37645、几何容量 2610.09056、SketchSSM 2609.33051、MHLA 2601.07832；均后续摘要核验。排除 NPUs/新模型架构宣传类结果，未验证则不背书。|
| Q06 | `site:arxiv.org "Log-Linear Attention" "Mixture-of-Memories"` | 命中 2502.13685 多版本、2507.16577、2506.04761、2609.36259、2609.39034；多个 MoM 标题版本归并。未另计仅参考文献提及的 SMat。|
| Q07 | `site:arxiv.org "DeltaNet" "Gated Delta Networks"` | 命中 2412.06464、2604.19021、2610.38578；TreeWY/量化等系统方向暂不纳入本专题核心候选。|
| Q08 | `site:arxiv.org "Zoology" "Repeat After Me"` | 命中 2610.19709、2609.04434 及含 2402.01032 的参考文献；三者后续摘要核验。不能仅从参考文献命中计作品。|
| Q09 | `site:arxiv.org "Titans" "ATLAS" "memory"` | 命中 2505.23735、2512.06983；后者作为相反/条件边界候选。综述与 MANAR 只保留为未展开方向，不计确认。|
| Q10 | `site:arxiv.org "key" "value" "compression" "Decoupled" attention` | 命中 DHA 2406.06567；图像生成压缩等结果暂未展开，不把头共享问题偷换为块路由问题。|

### B03：基础理论补查（1 次成功，5 次 429）

| 调用 | 原样查询 | 实际结果 |
|---|---|---|
| Q11 | `site:arxiv.org Zoology Measuring Improving Recall Efficient Language Models` | HTTP 429，未取得结果。后用 Q17 收紧查询。|
| Q12 | `site:arxiv.org Transformers RNNs Fast Autoregressive Transformers Linear Attention` | HTTP 429；后 Q18 重查。|
| Q13 | `site:arxiv.org Parallelizing Linear Transformers Delta Rule 2024` | 成功但多为参考文献命中：出现 Memory by Design 2605.31163、CKDA 2609.24797、GKA 2511.21016；后均取摘要。对 2406.06484 用 Q19 收紧。|
| Q14 | `site:arxiv.org learning memorize surprise Titans 2501` | HTTP 429；后 Q21 用完整标题。|
| Q15 | `site:arxiv.org "test-time regression" "2025"` | HTTP 429；后 Q19 参考文献取得 2501.12352，再核验摘要。|
| Q16 | `site:arxiv.org "Hopfield Networks is All You Need" "Using Fast Weights"` | HTTP 429；后拆 Q22/Q28。|

在本批失败后转入已有稳定 URL 的 FetchURL 核验，而非立即循环请求。

### B04：召回基准身份补核（1 次成功）

| 调用 | 原样查询 | 实际结果 |
|---|---|---|
| Q17 | `"Zoology: Measuring and Improving Recall" "arxiv"` | 取得 2312.04927 官方页，选入 023。其他文章参考文献中含 2406.XXXX 占位符，未采该占位符。|

### B05：快速权重基础、回归框架、容量理论（3 次成功）

| 调用 | 原样查询 | 实际结果 |
|---|---|---|
| Q18 | `"Transformers are RNNs" "arxiv"` | 取得 2006.16236、2401.06104 官方入口；选入 031、034。|
| Q19 | `"Parallelizing Linear Transformers" "arxiv"` | 取得 2406.06484、参考文献中的 2501.12352、2312.06635、2505.19488；选入 032、033、035、037，全部后取摘要。|
| Q20 | `"A Geometry-Based Capacity Theory" "Sharp" "associative"` | 命中 2603.26554；选入 036。|

### B06：历史优先权与多粒度邻近工作（2 次成功，3 次 429）

| 调用 | 原样查询 | 实际结果 |
|---|---|---|
| Q21 | `"Titans: Learning to Memorize at Test Time"` | 官方 2501.00663，选入 038；检索日期及提交史为 2024-12-31，不能仅看 arXiv 编号年份。|
| Q22 | `"Using Fast Weights to Attend to the Recent Past"` | 官方 1610.06258、NeurIPS 及作者页；选入 039。|
| Q23 | `"Sharp storage capacity" "linear associative memory"` | HTTP 429；后 Q32 重查。|
| Q24 | `"Hopfield Networks is All You Need"` | HTTP 429；后 Q28 收紧。|
| Q25 | `"Native Sparse Attention" "arxiv"` | HTTP 429；后 Q29 收紧。|

随后 FetchURL：Titans、Ba 2016、几何容量 HTML、混合模型功能分工、LoLA。几何容量 HTML 获取耗时约 203 秒，输出被工具存为本次会话临时结果；只检查开头用于发现，不算精读，未把该工具缓存复制为项目文件。

### B07：SSM 基础与 Hopfield 实际容量（3 次成功）

| 调用 | 原样查询 | 实际结果 |
|---|---|---|
| Q26 | `"Mamba" "Linear-Time Sequence Modeling with Selective State Spaces"` | 官方 2312.00752，选入 042。|
| Q27 | `"Transformers are SSMs" "Structured State Space Duality"` | 官方 2405.21060，选入 043。|
| Q28 | `"Hopfield Networks is All You Need" arxiv` | 得到 2008.02217 真实标识、2409.16408 和 2503.09518；选入 044、045，后者仅页脚列为 P01。部分二手参考文献给出错误 2112.09038，不采用。|

### B08：块寻址＋细粒度访问邻近组合（3 次成功）

| 调用 | 原样查询 | 实际结果 |
|---|---|---|
| Q29 | `"Native Sparse Attention" arxiv compression selection` | 从结果确定 2502.11089，后官方摘要核验，选入 046。未把第三方实现当作者代码核验。|
| Q30 | `"Learning to (Learn at Test Time): RNNs with Expressive Hidden States"` | 官方 2407.04620 多版本，选入 047；二手站部分年份失真，采用提交史。|
| Q31 | `"Infini-attention" "Leave No Context Behind"` | 官方 2404.07143，及 RAMba 2504.16795；选入 048、049。|

### B09：精确检索 vs 列表检索、语义相关性（3 次成功）

| 调用 | 原样查询 | 实际结果 |
|---|---|---|
| Q32 | `"Sharp storage capacity" "linear associative memory"` | 成功取得 2605.05189 与 OpenReview zXMvCvXYE0、ICLR 官方 10022391；选入 050、052；052 的 OpenReview 被校验墙挡住，合法会议介绍足以核验摘要，但发表类型待补。|
| Q33 | `"linear associative memory" "Zahn"` | 得到 2601.15313、2603.17781 相关线索；只对前者取得摘要并选入 051，后者未核验不计数。|
| Q34 | `"key" "value" "aggregation" "linear attention" capacity` | 命中 MHLA 与主题页；没有获得新的、已核实的独立值/地址聚合通用定理。OpenReview 仅 PDF 片段没有足够身份，不收为候选。|

### B10：标题/版本关联补核（2 次成功）

| 调用 | 原样查询 | 实际结果 |
|---|---|---|
| Q35 | `"2601.15313" "Attention" "Retention"` | 官方最新题 Attention Is Not Retention，与旧题 Mind the Gap 关联为同一作品。|
| Q36 | `"2609.04434"` | 官方完整标题 What Attention Recalls and Recurrence Controls in Hybrid Language Models，与摘要身份核对；无关财务/法律数字命中排除。|

## 2. FetchURL 实际来源台账（56 调用）

“A”表示取得摘要/官方介绍；“正文开头”不计精读。每个编号均对应实际调用，不以“计划抓取”代替。

| 调用 | 原样 URL | 结果/候选 |
|---|---|---|
| F01 | https://arxiv.org/abs/2102.11174 | A / 001 |
| F02 | https://arxiv.org/abs/2402.18668 | A / 002 |
| F03 | https://arxiv.org/abs/2402.01032 | A / 003 |
| F04 | https://arxiv.org/abs/2412.06464 | A / 004 |
| F05 | https://arxiv.org/abs/2605.22791 | A / 005 |
| F06 | https://arxiv.org/abs/2610.38578 | A / 006 |
| F07 | https://arxiv.org/abs/2502.13685 | A / 007 |
| F08 | https://arxiv.org/abs/2507.16577 | A / 008 |
| F09 | https://arxiv.org/abs/2506.04761 | A / 009 |
| F10 | https://arxiv.org/abs/2607.02303 | A / 010 |
| F11 | https://arxiv.org/abs/2608.12435 | A / 011 |
| F12 | https://arxiv.org/abs/2609.36259 | A / 012 |
| F13 | https://arxiv.org/abs/2610.37645 | A / 013 |
| F14 | https://arxiv.org/abs/2607.07386 | A / 014 |
| F15 | https://arxiv.org/abs/2610.09056 | A / 015 |
| F16 | https://arxiv.org/abs/2610.19709 | A / 016 |
| F17 | https://arxiv.org/abs/2602.11958 | A / 017 |
| F18 | https://arxiv.org/abs/2609.24797 | A / 018 |
| F19 | https://arxiv.org/abs/2511.21016 | A / 019 |
| F20 | https://arxiv.org/abs/2505.23735 | A / 020 |
| F21 | https://arxiv.org/abs/2512.06983 | A / 021 |
| F22 | https://arxiv.org/abs/2601.07832 | A / 022 |
| F23 | https://arxiv.org/abs/2312.04927 | A / 023 |
| F24 | https://arxiv.org/abs/2510.26692 | A / 024 |
| F25 | https://arxiv.org/abs/2406.06567 | A / 025 |
| F26 | https://arxiv.org/abs/2605.06946 | A / 026 |
| F27 | https://arxiv.org/abs/2609.33051 | A / 027 |
| F28 | https://arxiv.org/abs/2604.19021 | A / 028 |
| F29 | https://arxiv.org/abs/2609.39034 | A / 029 |
| F30 | https://arxiv.org/abs/2605.31163 | A / 030 |
| F31 | https://arxiv.org/abs/2006.16236 | A / 031 |
| F32 | https://arxiv.org/abs/2406.06484 | A / 032 |
| F33 | https://arxiv.org/abs/2501.12352 | A / 033 |
| F34 | https://arxiv.org/abs/2401.06104 | A / 034 |
| F35 | https://arxiv.org/abs/2312.06635 | A / 035 |
| F36 | https://arxiv.org/abs/2603.26554 | A / 036 |
| F37 | https://arxiv.org/abs/2505.19488 | A / 037 |
| F38 | https://arxiv.org/abs/2501.00663 | A / 038 |
| F39 | https://arxiv.org/abs/1610.06258 | A / 039 |
| F40 | https://arxiv.org/html/2610.09056v1 | 已确认 015 的 HTML 正文取得，只查看开头；不是新增作品或精读 |
| F41 | https://arxiv.org/abs/2609.04434 | A / 040 |
| F42 | https://arxiv.org/abs/2505.23666 | A / 041 |
| F43 | https://arxiv.org/abs/2312.00752 | A / 042 |
| F44 | https://arxiv.org/abs/2405.21060 | A / 043 |
| F45 | https://arxiv.org/abs/2008.02217 | A / 044 |
| F46 | https://arxiv.org/abs/2409.16408 | A / 045 |
| F47 | https://arxiv.org/abs/2503.09518 | 仅 Bibliographic Tools 页脚，P01，未确认 |
| F48 | https://arxiv.org/abs/2502.11089 | A / 046 |
| F49 | https://arxiv.org/abs/2407.04620 | A / 047 |
| F50 | https://arxiv.org/abs/2404.07143 | A / 048 |
| F51 | https://arxiv.org/abs/2504.16795 | A / 049 |
| F52 | https://arxiv.org/abs/2503.09518v1 | 仍只页脚，P01，不再重试 |
| F53 | https://arxiv.org/abs/2605.05189 | A / 050 |
| F54 | https://openreview.net/forum?id=zXMvCvXYE0 | 校验墙，未绕过；052 用 F56 |
| F55 | https://arxiv.org/abs/2601.15313 | A / 051 |
| F56 | https://iclr.cc/virtual/2026/10022391 | 会议官方摘要 A / 052 |

## 3. 去重、初筛与来源局限

- arXiv HTML、abs、PDF 是同一作品的不同入口；Search/Fetch 调用数不等于作品数。
- MoM v1/v4、050 的 Winner-Take-All→Top-1/Tail-Average 改题、051 的 Mind the Gap→Attention Is Not Retention 均明确关联。
- 005 GDN-2、028 FG²-GDN、006 Dual DeltaNet 是不同作品，机制近似不合并；同一作品内 + 变体不另计。
- 015 的正文作者显示区与脚注姓名映射存在不清晰之处，不把投稿联系人替作作者。大部分摘要提取不含作者列表，CANDIDATES.md 已留空，交下一轮目录补元数据；不影响标题/标识/摘要的作品核验层级。
- 052 的会议页有官方摘要，但未核对主会/工作坊属性、正式 proceedings 和预印本对应；保持“官方简介核验”，不臆称主会录用。
- 检索结果中的二手主题站、个人教程、第三方代码实现只能作词汇和入口；没有作为模型性能或理论结论的最终依据。
- 没有对已获取的 HTML 进行完整通读，没有读取/核验作者代码，也没有复现实验；摘要数字、定理措辞必须由下一轮 terra 原文核查。

## 4. 当前检索空白

- 没找到一个已核验、覆盖所有学习规则的“值聚合与地址聚合完全独立最优”通用定理；015/033/052 是受条件限制的近邻，006/013 是机制新作。
- 多粒度路线已有组合，但完整“来源存活→查询路由→细粒度回访→失败回退”的统一生命周期与总成本尚未核定。
- 1980–1990 年代相关矩阵记忆、早期快速权重、稀疏分布式记忆的原始文献未系统追溯；不能声称发现了多槽或内容寻址的起源。
- 检索量达到首批目标不表示覆盖收束；下一步应围绕 HANDOFF.md 的争议补读和引用追踪，不按数量机械补齐。
