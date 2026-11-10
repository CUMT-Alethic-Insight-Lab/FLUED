# 配套文档翻译说明与保真核验

**2026年11月9日 · 独立中文翻译 · 仅负责四份配套译稿及本说明**

## 1. 责任范围与当前交付边界

本任务以修订后的五份最终英文文件和三份 FINAL 重检为输入，完整翻译四份配套文件，不撰写英文科学综合，不重复翻译长篇主报告。四份译文不是摘要化改写；保留全部实质段落、表格单元、比较条件、预算维度、停止条件、引用、数值、公式与稳定 ID。本说明是译者核验记录，不是第五份科学综合。

| 英文输入 | 中文交付 |
|---|---|
| [EXECUTIVE_SUMMARY_EN.md](../04_synthesis/EXECUTIVE_SUMMARY_EN.md) | [EXECUTIVE_SUMMARY_ZH.md](EXECUTIVE_SUMMARY_ZH.md) |
| [EXPERIMENT_DECISION_MATRIX_EN.md](../04_synthesis/EXPERIMENT_DECISION_MATRIX_EN.md) | [EXPERIMENT_DECISION_MATRIX_ZH.md](EXPERIMENT_DECISION_MATRIX_ZH.md) |
| [OPEN_EVIDENCE_EN.md](../04_synthesis/OPEN_EVIDENCE_EN.md) | [OPEN_EVIDENCE_ZH.md](OPEN_EVIDENCE_ZH.md) |
| [REVISION_LOG_EN.md](../04_synthesis/REVISION_LOG_EN.md) | [REVISION_LOG_ZH.md](REVISION_LOG_ZH.md) |
| [REPORT_EN.md](../04_synthesis/REPORT_EN.md) | [REPORT_ZH.md](REPORT_ZH.md)，由另一译者负责，不属于本次写入范围 |

`REPORT_ZH.md` 在本配套译稿建立链接时尚未交付，这是初次记录的历史状态。主报告现已存在，本轮已实际复核原先待联调的 15 个链接出现位置：3 处仅指文件，12 处指向 8 个不同显式锚点，全部解析成功。配套文档到主报告的链接待办已关闭；这不认证主报告全文的科学语义，也不代替其独立双语审查。

**十七篇选定官方 ICLR 2027 正文的阅读与结果裁定仍未完成。**三篇相关公开 FULL 版本不把官方缺口变成十四；“十四项没有已确立替代版本”是另一字段。配套译文完成不等于整体研究任务完成，不新增 FULL 信用、会议录用、官方与公开稿件相等性或实验结论。

## 2. 输入版本与只读保证

已完整读取 PLAN、三份 FINAL 重检、四份配套英文及主报告全部 1,297 行。最终重检允许明确标作有边界或部分研究结果的完整翻译，不要求因十七篇官方正文受阻而无限推迟翻译，也未豁免原始正文阅读义务。专题中间草稿未被当作最终翻译底稿。

### 五份最终英文 SHA-256

| `04_synthesis/` 文件 | SHA-256 |
|---|---|
| REPORT_EN.md | `8a9428deb35fa26eb54d05df6136f99d63af621f5eab31c047718fa1515f88d0` |
| EXECUTIVE_SUMMARY_EN.md | `bbde1489b4537f6c4f6ffc2bdea33c42c2c4002c276af30b69731902f7fccd01` |
| EXPERIMENT_DECISION_MATRIX_EN.md | `f4807a7ec936ad21ea505ab0d475e317f64879879282c48d7c4019fd0acc92b8` |
| OPEN_EVIDENCE_EN.md | `433234712cd25d0274bf8fcca1c5abcb758bdece862dbe9f4bb6d236e90d6d3a` |
| REVISION_LOG_EN.md | `903f6c1d4ae3f0af283f09a3ff820ffe2a1907d940c39cd1cda2c160a1b0cce5` |

### 采用的重检快照 SHA-256

| `05_review/` 文件 | SHA-256 |
|---|---|
| [FINAL_BROAD_COVERAGE_RECHECK.md](../05_review/FINAL_BROAD_COVERAGE_RECHECK.md) | `5d141ebde05ab5f6caf66f8643cde49f5d395858f0e4226d584b7b677c5e392f` |
| [FINAL_ICLR_RECENCY_RECHECK.md](../05_review/FINAL_ICLR_RECENCY_RECHECK.md) | `8f3f6611dc2d2533aeae7d0a4a85dbae10868f9654f1971077f5056e4f9018ef` |
| [FINAL_BROAD_RIGOR_RECHECK.md](../05_review/FINAL_BROAD_RIGOR_RECHECK.md) | `9f204e88ec6cf2352331e8daa392f2dbd6612192aa3b101cfa6544e8125cbb18` |

核验前后五份英文输入哈希与重检指定快照一致。仅写入本说明及上表四份中文配套文件；主报告中文、英文来源、目录、卡片、审计、登记表和项目代码不作编辑。

## 3. 标题逐项映射

标题级别和顺序逐项保留。下列各表含文件总标题；章节序号未重排。现有显式锚点 `m26-execution` 原样保留，未依赖中文标题自动生成的片段名来替换它。

### 摘要：12 个标题

| 英文标题 | 中文标题 |
|---|---|
| Executive Summary: Compression, Memory, Reading, Learning, and Transfer | 执行摘要：压缩、记忆、读取、学习与迁移 |
| 1. Main conclusion and scope | 1. 主要结论与范围 |
| 2. Evidence accounting and recent-source limits | 2. 证据计数与近期来源限制 |
| 3. A — Compression and task sufficiency | 3. A — 压缩与任务充分性 |
| 4. B — Native writing, retention, interference, and capacity | 4. B — 原生写入、保持、干扰与容量 |
| 5. C — Addressing and native readout | 5. C — 寻址与原生读出 |
| 6. D — Deployed content use and causal measurement | 6. D — 部署时的内容利用与因果测量 |
| 7. E — Learning history and changing routes | 7. E — 学习历史与路线变化 |
| 8. F — Composition and transfer | 8. F — 组合与迁移 |
| 9. Cross-axis alternatives and latest public evidence | 9. 跨轴替代路线与最新公开证据 |
| 9.1 What the remaining uncertainty means for a research choice | 9.1 剩余不确定性对研究选择意味着什么 |
| 10. Conditional next decisions and stopping rule | 10. 有条件的后续决策与停止规则 |

### 决策矩阵：10 个标题

| 英文标题 | 中文标题 |
|---|---|
| Experiment Decision Matrix: Conditional, Minimal, and Evidence-Discriminating | 实验决策矩阵：有条件、最小化且能判别证据的比较 |
| 1. How to use this matrix | 1. 如何使用本矩阵 |
| Action types and costs | 行动类型与成本 |
| Shared interpretation prerequisites | 共同的解释前提 |
| 2. Instrument and artifact gate | 2. 测量工具与产物闸门 |
| 3. A/B/C: what was retained, and can the native system reach it? | 3. A/B/C：保留了什么，原生系统能否访问？ |
| 4. D/E/F: content dependence, formation, and host composition | 4. D/E/F：内容依赖、形成与宿主组合 |
| 5. Cross-axis alternatives, interfaces, and policy | 5. 跨轴替代路线、接口与策略 |
| M26 execution subcomparison — separate from lifecycle refresh | M26 执行子比较——独立于生命周期刷新 |
| 6. Release and decision record | 6. 发布与决策记录 |

### 待补证据：7 个标题

| 英文标题 | 中文标题 |
|---|---|
| Open Evidence: Sources, Artifacts, and New Experiments | 待补证据：来源、产物与新实验 |
| 1. Current boundary | 1. 当前边界 |
| 2. Seventeen selected official bodies: named, still missing | 2. 十七篇选定官方正文：逐项列名，仍然缺失 |
| 3. Other source and carrying-material gaps | 3. 其他来源及承载材料缺口 |
| 4. Source conflicts and artifact checks after FULL reading | 4. FULL 阅读之后的来源冲突与产物检查 |
| 5. Gaps that require new controlled evidence, not another generic paper | 5. 需要新受控证据、而不是再找一篇泛泛论文的缺口 |
| 6. Release rule and next legitimate action | 6. 发布规则与下一步合法行动 |

### 修订记录：11 个标题

| 英文标题 | 中文标题 |
|---|---|
| Revision Log: Broad English Synthesis v2 | 修订记录：广泛英文综合 v2 |
| 1. What this revision adds | 1. 本次修订增加了什么 |
| 2. Scientific distinctions made explicit | 2. 明确区分的科学概念 |
| 3. Current evidence and corrections integrated | 3. 已整合的当前证据与修正 |
| 4. Recent-source reporting and unresolved scope | 4. 近期来源报告与未决范围 |
| 5. Deliverables and stable translation structure | 5. 交付物与稳定翻译结构 |
| 6. Verification scope | 6. 核验范围 |
| Previous author-pass validation receipt — historical snapshot | 上一轮作者校验回执——历史快照 |
| 7. Itemized response to the three FINAL audits | 7. 对三份 FINAL 审查的逐项响应 |
| Review and translation status | 复审与翻译状态 |
| Revised-snapshot static validation receipt | 修订快照静态校验回执 |

## 4. 术语、权限与关键语义

此处解释译法，不新增研究术语、机制或实验。

| 原文 | 中文与本译稿采用的含义 |
|---|---|
| native / legal | 原生 / 合规：指部署接口原本具备的操作，以及不越过既定信息与时间可见性的权限；不是法律合规性的泛化评价。 |
| source-enabled / no-original-return | 允许访问来源 / 无需返回原始来源：两种保留与访问约定；无需回源不必等于恒定内存，增长的压缩状态也不等于免费来源。 |
| recoverability / native return / dependence / task-correct benefit | 可恢复性 / 原生返回 / 内容依赖 / 符合任务要求的收益：不同观测，不能相互替代。 |
| FULL / PARTIAL / BLOCKED | 保留登记标签：特定版本实质阅读完成 / 范围未全 / 获取受阻；FULL 不译为“全面核实正确”或“已复现”。 |
| fixed student | T05 中译为“同一学生模型”或保留模型身份：指各教师或目标比较使用同一 Qwen3.5-2B 学生架构身份，不是蒸馏时冻结学生权重。 |
| mass / conservation | T05 的概率质量 / 质量守恒不是模型质量分数，也不是无约束整串概率精确性；条件细化与跨多个教师 token 的实际路径下界分开保留。M15 的 denominator mass 则译为“归一化分母中的权重总量（mass）”，不预设该量已经归一化为概率。 |
| assay / positive / negative / power | 测量程序 / 阳性 / 阴性 / 检验效力：阳性用于确认目标效应可检出；统计未拒绝不能证明相等或不存在。 |
| carry / prefill / decode | 递推保存状态 / 预填充 / 解码：只在读出时用低比特副本，与反复以低比特保存状态，不是同一个计算约定。 |
| support | 按语境译“支持集”或“处理支持”：前者是采样可能覆盖的切分；后者要求实际纳入与排除等处理都有观测概率，不由指派随机性自动保证。 |
| reentry | 重新进入：跳过昂贵计算后重新激活；MoR 永久退出，没有重新进入，浅层 KV 共享不等于深层状态已恢复。 |
| evaluation-prior work | M22 保留“评估先验相关工作”；英文标签具体预算对象不够明确，须由英文作者澄清，不擅补“先验模型”等对象，不把未知成本默认为零。 |
| tying / aliases | 权重绑定 / 张量别名：输入输出共享、编码器解码器输入共享、线性或余弦头分别列示，以实际同一张量关系为准。 |
| value bags | 值的多重集：各个值及其出现次数都须保持，不只是去重后集合相同；角色或顺序对照不能悄然改变值频率。 |

AR、EC、EC-B、FD、NT、WL 的英文缩写保留，中文全称与操作边界在矩阵开头解释。EC 没有权重更新，但推断与激活仍有成本；EC-B 包含反向计算但不更新；FD 增加标签、拟合和选择，即使主模型固定也须单独许可；NT 改变主模型学习或形成历史，必须另行明确授权。**分类与提案不授权任何一种执行，包括已有检查点加载或 GPU 工作。**

## 5. 数值、预算、分母及修复语义检查

逐个对齐段落和表格行检查，重点包括：

- 167 的分母维持 A20/B22/C20/D20/E22/F19/I28/R16；这不是 167 项已解决发现。读取原始中文方向清单与目录对照，167 条原始中文 bullet 在目录中各逐字出现一次；本轮只读核对中英文主报告的方向锚点，均为 167 个、唯一且顺序对应，八轴总数一致。本任务没有复制或改写方向清单，也不将锚点结构核对称为中文对照索引的完整语义审查。
- 阅读分母 128=127 项原始工作任务加一项 Scratchpad 更新；103/6/19 与 108/5/15 是不同视图，五个替代版本不增加工作或官方完成。登记表 780 不是历史 772，更不是全部已审阅论文。两轮各 19 项目的性抽查不认证全部阅读卡。
- 官方元数据 50=46+3+1，零项已确立录用。17 篇官方正文仍缺失；3 个公开 FULL 对应候选与 14 个尚无已确立替代版本工作，不能抵扣该 17。note v2、PDFv2、修改时间、撤回事件时间保持分开。
- M01–M30 恰为 30 个唯一主比较行，原顺序不变；M26 执行子比较不是第 31 行。M13/M24/M29/M30 保留“比较族”与第一个独立分岔，不改写成自动全析因训练队列。S01–S08 全部保留。17 个 OpenReview forum ID 与英文一一相同且顺序相同。
- T02 保留 2604.16037v1、37 页与 A–G、6.1%→69.6% 的比较范围、残余攻击与干净负结果；跳过不可拆分尝试不同于理想化计数分布，可行性重归一化也未被说成一般修复；单层对齐界不扩展到深层变长保证。
- PSR 保留 0912.2385v1、78/100 成功、22 失败、仅成功条件下的 18.2 个动作与五坐标背后的资源。`U_hat^T P_hat_H`、`U`、`P_H` 原样保留；维度冲突不译成已观察到实现失败或已完成代码修复。
- T05 保留 GLM-Z1-9B / Qwen3.5-2B / BPM-JSD 无掩码、49%→9%、温度 1.0、每检查点 128 次生成的通过率诊断，与 80 程序 / 1,799 位置的边际探测分母分开。§4.3/Fig.3/Appendix H.2 不改为 §5；Table1 的最佳散度前向 KL 不与该 JSD 失败臂合并。
- RAM 的名义 500M 与展示剂量 500.040M 同时保留，不因账目修正抹掉质量单元格。修订记录中 31,111/2,466、31,733/2,580 及 729/759 等作者验证数字作为历史回执照译，不冒充本译者新做的检查或中文词数。
- M25 失败、截断、硬预算调用、自信遗漏与多余读取保留在分母；M26 不只统计已完成删除请求；M28 保留实际纳入或排除、被替换内容与共同暴露支持，未观测动作不填零。统计精度不替代语义有效性。
- 前向、激活、来源调用、拟合、教师构造与评分、搜索或调参、主模型更新、协方差或缓冲、常驻或活跃状态、原始来源、传输、刷新、失败或被拒工作、冷态或热态或尾延迟分别计入。相等 token、原始字节、FLOPs、延迟或物理状态不是同一个预算；无任何新数值预算、容差、种子数或训练长度被预注册。

## 6. 链接重定位与历史状态处理

- `04_synthesis/` 与 `06_translation/` 是同级目录：指向 `../02_catalog/`、`../03_reading/`、`../05_review/` 及 `../../` 下旧研究目录的链接，保持原相对路径即可解析到相同文件。外部 URL、forum ID、论文版本与页节定位不变。
- 配套导航由同目录 `*_EN.md` 改为 `*_ZH.md`，主报告改为 `REPORT_ZH.md`。`#direction-crosswalk`、`#recent`、`#axis-e`、`#selective-execution`、`#source-alternatives`、`#interfaces`、`#relations`、`#t05-functional-probe` 等显式目标 ID 原样保留；M26 的 `#m26-execution` 在译文实际存在。
- 修订记录第 5 节列的是英文作者实际交付文件，因此五个文件名称仍为 `*_EN.md`，目标重定位至 `../04_synthesis/`，不伪造为作者已经写过中文。第 4 节原来纯文本 `OPEN_EVIDENCE_EN.md` 补上对应中文导航链接，同时保留英文文件名提示。这是导航增强，不改变证据。
- OPEN 末节与 REVISION_LOG 末尾的“待复审／尚未翻译”忠实保留为英文作者快照。各文件顶部独立标明译者说明；本说明引用随后三份 FINAL 重检的通过范围，避免让历史句被误解为当前禁止翻译。没有回写作者文件或偷偷改写历史。

## 7. 静态验证回执与限制

用只读、内存内 Python 检查实际四份交付译文，不生成保留脚本或日志。为比较数值，排除 URL 目标中的路径数字，将英文月份日期与中文年月日规范化，将 seventeen/十七、fourteen/十四规范化到相同数值；不删去科学数字。额外译者说明块单独标注并从逐行正文对齐中排除，显式锚点行另检。

| 文件 | 对齐的非空正文块（含标题、表格行） | 标题数 | 表格行数（含表头、分隔行） | 译文 Markdown 链接数 |
|---|---:|---:|---:|---:|
| EXECUTIVE_SUMMARY_ZH.md | 46 | 12 | 0 | 37 |
| EXPERIMENT_DECISION_MATRIX_ZH.md | 65 | 10 | 38 | 83 |
| OPEN_EVIDENCE_ZH.md | 78 | 7 | 58 | 65 |
| REVISION_LOG_ZH.md | 61 | 11 | 21 | 11 |
| 合计 | 250 | 40 | 117 | 196 |

检查内容：250 个正文块顺序与数量一致；逐块数值多重集一致；表格各行列数一致；标题级别一致；M01–M30 唯一顺序；S01–S08；17 个官方 ID 一致；五个公开替代版本 ID 保留；来源引文链接逐条映射一致；内联公式与命令保留；已有显式锚点保留；严格 UTF-8、末尾换行、无替换字符或行尾空白。196 个链接中，17 个为继承的外部 OpenReview URL，只检查文本相同，不声称网络可访问；179 个本地链接全部离线解析成功，其中 14 次片段引用均匹配实际显式 ID。原列待联调的 15 处主报告链接现已全部通过：3 处仅文件，12 处引用 8 个不同锚点；其余 2 次片段引用是矩阵的 `m26-execution`。本轮重新实际核验，不只沿用审校回执。

已在完成前检查 `git status --short` 与 `git diff --check`。研究根目录、无关提案与四个 bundle 在任务开始即未跟踪；状态不能归属并发修改。未运行构建或 pytest：纯 Markdown 翻译不适用软件构建测试；`git diff --check` 对未跟踪文件不提供覆盖，因此另用逐文件 UTF-8 与空白检查实际译稿。没有新训练、检查点执行、探针拟合、产物运行、网络获取、子代理、安装、提交或推送。

### 四份配套译稿 SHA-256——审校修复后

| 文件 | SHA-256 |
|---|---|
| EXECUTIVE_SUMMARY_ZH.md | `6686a1aa3186d81efc4c07f487454c88e2aaddc96ce8569bc834d1fda98d051d` |
| EXPERIMENT_DECISION_MATRIX_ZH.md | `6f1fa09363396323e5ee6ea950e9ae5dcea80c368a75eeb7388a90fa9bf8b376` |
| OPEN_EVIDENCE_ZH.md | `2079888875f9d6214615247f289d9de64a1962d80b3bdc47cbdc9fdba6cdf96c` |
| REVISION_LOG_ZH.md | `0887281b78b21c53532518342b64f90ab3c64d1f940463b1add1447f34c81537` |

## 8. 省略清单与剩余工作

验证脚本初版曾误要求 OPEN 单份文件出现全部五个替代版 arXiv ID；英文 OPEN 本身并未印出 T03 的 arXiv ID，因此该断言失败不代表漏译。改为在四份配套译文的并集中核对五个版本后，最终全套检查通过。数字初检中路径重定位产生的 `04` 与中英文日期、十七／十四的文字写法，也按上述规则规范化后逐块复核，未通过删除科学数字规避差异。

**对应四份英文的实质省略：无。**没有删除比较、反转对照、条件、公式、数字、预算、分母、表格行、引用、版本或问题 ID。中文为自然语序，不追求英文逐词形式；日期与部分小整数使用中文写法，数值不变。新增内容仅为标注清楚的译者说明、术语释义、链接导航与本核验记录。

**有意不做：**不翻译 REPORT 全文，因为它属于另一译者，并非因长度而缩减交付；不替其他负责人修改目录、来源卡或审查；不执行研究提案。配套到主报告的 15 处链接已联调关闭；主报告全文及 167 条方向的语义保真仍属相应负责人，不由链接或锚点检查代签。17 篇官方正文的合法获取、实际阅读及结果或版本裁定，是仍开放的原始研究义务，不因本次翻译完成而关闭。

## 9. TRANSLATION_SUPPORT_REVIEW 定点修复回执

依据[独立双语审校](../05_review/TRANSLATION_SUPPORT_REVIEW.md)的具体作用域检查全部四份配套活跃段落，未全局替换“或”，也未编辑英文或审校者文件。

| 发现 | 本轮修复及同义活跃段复查 | 保持的边界 |
|---|---|---|
| P1-TS01：PSR 联合假设 | REVISION_LOG 的学习式 PSR 行改为“在所列秩、覆盖与条件数假设下”；摘要原有同一合取表述正确，保留。OPEN 中覆盖与条件数作为待核问题并列，不改成可选假设。 | 公式冲突、78/100、22 次失败、仅成功平均 18.2、资源与语言迁移限制均未删。 |
| P1-TS02：值多重集 | 摘要 §3 和 M06 均明确“值的多重集（各值及其出现次数）”；M06 另保留长度不变。检索全部四份正文及说明，无其他未限定的“值集合”活跃表述；技术用语补入本说明。 | 固定各值及重复次数，不把仅去重集合相等当成同一角色或顺序对照。 |
| P2-TS03：零结果精度 | M02 改为“有效阳性配合估计足够精确的零结果”；复查摘要、M04 及修订记录的统计非拒绝表述，原有“不等于相等或不存在”均保留。 | 未新增等价界、显著性阈值或效应容差，也未声称总体效应严格为零。 |
| P2-TS04：分母中的 mass | M15 改为“归一化分母中的权重总量（mass）”；同义说明区分该量与 T05 的概率质量守恒。 | 不预设分母权重已归一化为概率，不增强整串概率精确性保证。 |

本说明同时撤回对 `evaluation-prior work` 擅补“先验模型”的解释：保留英文具体预算对象待作者澄清，不改写英文或另造实验。四份配套仍为 250 个对应正文块、40 个标题、117 个表格行、30 个主比较和 17 个官方来源行；数值、行动类型、公式与引文映射重新校验通过。上述是译者修复及自检回执，不代替独立审校者的复核裁定。
