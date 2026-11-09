# 最终综述严谨性复核：四项修订核销与翻译放行

2026-11-09。仅写本文件；不修改作者三份最终文件、修订日志、既有审稿报告或阅读卡。

## 1. 结论

**核销通过，可以进入完整中文翻译。此次复核范围内：P0 残留 0，P1 残留 0；上轮 RIGOR 的 1 项 P1、3 项 P2 均已落实。**

这不是把“此前有条件通过”直接改成无条件背书：本次逐项对照了修订日志、实际作者文本、承载阅读卡，并重新定点抽查三部原作的关键段落。放行的是**当前有明确证据边界的独立领域综述**，不是 MtPC 软件正确性、TokSuite 绘图流水线或所有实验数字的复现认证。

已声明的未决问题可以继续作为未决问题交付。**不要求先实现、更正或运行这些外部论文的算法/软件，不要求解决所有研究问题，也不要求补足某个多粒度方案的覆盖，才允许翻译。** 当前四项修订不需要新增 terra 全文阅读。

## 2. 实际检查范围和快照

完整读取：

- `04_synthesis/REVISION_LOG_EN.md`，55 行；本任务所称 REVISION_LOG 的实际文件名。
- `04_synthesis/EXECUTIVE_SUMMARY_EN.md`，79 行。
- `04_synthesis/OPEN_QUESTIONS_EN.md`，167 行。

定点读取和搜索：

- `04_synthesis/SURVEY_EN.md`，当前 810 行中的相关修订段落、共享表和效率表，以及敏感未决项的保留措辞；**没有把本次工作冒称为重新审读整篇综述**。
- 上轮 `FINAL_SURVEY_RIGOR.md` 的四项问题与核销标准。
- ByT5/W0351、Repeat After Me/W0061、Compute Optimal Tokenization/BIW-0047 的对应卡片段落。
- 原作定点检查见第 4 节。新增 FULL 阅读信用 **0**；下载 **0**；模型/训练/论文代码执行 **0**。

修订日志第 3 行宣布两份审稿的所有项目已处理；本报告**只独立核销 RIGOR 四项**，不把 COVERAGE 的另四项一并当作本次重新核证。日志中的当前长度 19,941 / 2,115 / 2,706，与本次读取三文件后按空白分词的实际计数一致。

以下行号均为本次当前快照，不能继续使用上轮旧行号 615、632、460 等定位新版本。

## 3. 四项核销表

| 原问题 | 修订日志位置 | 实际落点与检查结果 | 核销 |
|---|---|---|---|
| **RIGOR P1-01：复制容量上界缺少读/答协议与状态唯一通路前提** | `REVISION_LOG_EN.md:13` | `SURVEY_EN.md:623` 明确先完整读入、后开始复制；所有输入相关信息影响须经有限可区分状态集合 S；排除未计入状态的源重读、外部缓存、提前写出的输入相关输出流和旁路。采用成功率 ≤ min(1, \|S\|/D^L)，并写出 b=log₂\|S\|、b≥L log₂D+log₂(1−ε)、0≤ε<1。`EXECUTIVE_SUMMARY_EN.md:61` 同步前提；`OPEN_QUESTIONS_EN.md:94–96` 同步前提及重读/缓存/通道预算。没有把随机串界推广为自然语言不可能定理。 | **已关闭** |
| **RIGOR P2-01：ByT5 数字的表号和设备不够就近明确** | `REVISION_LOG_EN.md:14`；误差单位交叉见第 11 行 | `SURVEY_EN.md:171` 就近指定任务 Table 5、预训练 Table 9/TPUv3-64、XNLI 推理 Table 10/TPUv3-32；明确 XSum 改用 TPUv3-128。`SURVEY_EN.md:672` 效率表也保留同一划分。G2P 已明确为 PER，转写为 CER，未将不同误差单位混用；未把 XNLI 叫 NER，未把速度问题全归因于长输出。 | **已关闭** |
| **RIGOR P2-02：第一缩放律 N 的排除项过于笼统** | `REVISION_LOG_EN.md:15` | `SURVEY_EN.md:640` 已点名排除 local encoder/decoder 与 input/output embedding parameters；同时明确总训练 FLOP 比较仍计入这些模块，并说明拟合 N 不等于全驻留参数存储。熵模型预训练/评分的全生命周期账目仍未完整列明，没有被写成零，也没有被误写成所有计算式均排除。 | **已关闭** |
| **RIGOR P2-03：ByT5 配置证据需保留可变工件和运行依赖限制** | `REVISION_LOG_EN.md:16` | `SURVEY_EN.md:468` 明确 Mutable operative gin、Large/XNLI 微调、百万步基座初始化、不是原始预训练日志；链接固定 Mesh commit `4758510b99614c51ecb56166faff9842befac193`，并明确论文运行依赖版本和张量别名未验证、不能外推全部尺寸/移植版。`SURVEY_EN.md:479` 继续区分论文声明、静态配置、固定代码和实际运行验证。 | **已关闭** |

### 三份最终文件的传播是否足够

- **正文**承载四项完整修订。
- **摘要**第 61 行重述了复制界最容易在缩写时丢失的协议前提；没有重复宣称未经限定的复制定理。摘要没有重列 ByT5 设备/config 或此项缩放 N 的细节，故不要求为核销强行新增这三段。
- **开放问题**第 94–96 行把复制协议及存储、访问、遍数预算带入实验设计；没有让允许重读或外存的实验臂继承状态独占上界。第 67–69 行对存储相关别名验证是未来实验的证据要求，不是说当前综述必须完成该实验才可交付。
- 摘要第 67 行的 input/hash 参数排除说的是另一篇 *Byte Language Models*，不是 *Compute Optimal Tokenization*；正文第 640、644 行仍然分别命名两种参数口径，没有把不同论文的 N 混为一谈。

## 4. 本次定点原文检查

### 4.1 复制：原文的 prompt→answer 设置与修订一致

重新通过内置浏览器读取 [Repeat After Me v2 §2.1](https://arxiv.org/html/2402.01032v2#S2.SS1)。原文把输入定义为 **“prompt”**、输出定义为随后生成的 **“answer”**；定义有限状态集合 S、状态更新 `u:S×D→S` 和输出 `r:S→D`。

这支持“完整摄入后，再从计入的状态决定答案”的适用协议，不能推出在线边读边回显也受同一空间界约束。再对照 [W0061 卡第 7–9 行](../../flued_multigranularity_survey_20261108/03_reading/B04/W0061.md)：安全计数结论使用非严格成功率上界，避免照抄原文正文严格不等号的等号边界问题。

独立代数复查：固定一个 retained state，确定性输出最多恰好匹配一个完整输入串；均匀 D^L 个串因此有成功率 ≤ min(1,|S|/D^L)。若成功率 ≥1−ε>0，取二进制对数得到 `b≥L log₂D+log₂(1−ε)`。当前文本还补足了 ε 的有效区间，推导和单位无漂移。**这只是计数论证及协议核对，不是重做论文注意力构造或完整证明审计。**

### 4.2 ByT5：表 9/10 原文直接确认设备划分

重新读取 [ByT5 arXiv v3 §7/Table 9](https://arxiv.org/html/2105.13626v3#S7) 和 [Table 10](https://arxiv.org/html/2105.13626v3#S7.T10)：

- Table 9 原文写 **“pre-training on a TPUv3-64 device”**。Small/Base/Large/XL/XXL 的 mT5→ByT5 sequences/s 为 1646→1232、747→576、306→232、94→70、33→25；与约 .75× 的概括一致。
- Table 10 原文写 **“We use a TPUv3-128 for GEM-XSum, and a TPUv3-32 elsewhere.”** XNLI 表中慢速比为 6.4、7.5、9.5、9.0、8.0×，支持正文的 6.4–9.5× 范围和设备标注。
- Table 9 右侧是前向 einsum operation 计数；当前修订没有把它重新提升为全生命周期训练 FLOP 或端到端服务成本。

此次新抽查用的是明确标识的 arXiv v3；作者正文及 [W0351 卡第 13–15 行](../../flued_multigranularity_survey_20261108/03_reading/B08/W0351.md)引用正式 TACL 表格。两者在本次核对的设备和速度字段上一致，**不据此宣称两版全文逐字节相同**。

配置项则对照 [W0351 卡第 21 行](../../flued_multigranularity_survey_20261108/03_reading/B08/W0351.md)及实际新表格核销：本次未重新下载可变 gin、未读取权重、未执行 Mesh，也未新增运行别名认证。当前正文准确保留了这一静态证据上限；因此无需为了写作核销再去实现运行验证。

### 4.3 参数排除：原文明确区分拟合参数和总计算

直接重读已保存的 [Compute Optimal Tokenization v2 原文提取](../03_reading/R05/sources/BIW-0047.txt)：

- **第 386–390 行，§3.1**：仅考虑 latent module 参数，排除 BLT encoder/decoder 与 subword embedding 参数，并说 latent 参数在固定 recipe 下决定 total 参数。
- **第 1327–1331 行，Appendix B.1**：拟合限于 global latent model，原文明确 **“excluding encoder/decoder and embeddings”**。
- **第 1517–1520 行，Appendix B.2**：第二阶段使用 **“total compute budget … including the cost of the encoder, decoder, and embeddings”**。

正文第 640 行正是这一双层口径，未把“拟合 N 不计入”误译为“所有 FLOP 都不计入”，也未把拟合 N 当成实际显存或全部驻留参数。当前已足够精确，不需再加性能实验来核销这条写作意见。

## 5. P0/P1 残留、已声明未决与翻译门槛

### 本次核销范围的残留

- **P0：0。** 未见必须撤回当前交付主张的修订后错误。
- **P1：0。** 上轮复制容量界的实质前提缺失已消除，并已传播至摘要和 OQ-09。
- **上轮三项 P2：全部关闭。** 不新增阻断翻译的 P2。

### 未决项保留，不阻断交付

抽查当前文本仍保留：

| 项目 | 当前位置 | 应保持的证据边界 |
|---|---|---|
| MtPC 优化 wrapper 的随机目标律 | `SURVEY_EN.md:377`；`OPEN_QUESTIONS_EN.md:123–129` | exactness 未验证；分析反例不是已执行代码缺陷，吞吐不因此失效。 |
| TokSuite Figure 6 实际转换 | `SURVEY_EN.md:437`；`OPEN_QUESTIONS_EN.md:134–138` | 实际 run→log→plot 未知；不拿该图证明统一 BPB/充分训练，其他评价不整体作废。 |
| MYTE 表格聚合/语言集合 | `SURVEY_EN.md:567`；`OPEN_QUESTIONS_EN.md:143–147` | 保留当前表 8 行列值及未协调集合，不制造统一 MT 排名。 |
| 实际边界提示/regex 的前缀稳定性 | `SURVEY_EN.md:331`；`OPEN_QUESTIONS_EN.md:152–156` | 泛化反例或缺少证明不等于已测得实际实现泄漏。 |

`REVISION_LOG_EN.md:55` 明确未把这些科学问题改名为已关闭；`OPEN_QUESTIONS_EN.md:167` 明确无需等每个未知项消失才交付综述。这是正确的停止条件。上述项目不是本轮新增 P1，也不要求作者先改外部软件或运行新实验。

翻译时只需忠实保留“读后输出且计入全部输入相关状态”“静态配置而非运行验证”“拟合 N 与总计算不同口径”，以及这些已声明未决。不得把 scoped FULL 译成复现认证，把配置未验证译成配置错误，或把修订核销译成所有外部算法保证已成立。

## 6. 验证与写入边界

本次开始时记录的作者文件 SHA256：

| 文件 | SHA256 |
|---|---|
| `SURVEY_EN.md` | `45cbcf639e1d5f598f823619313190ef8c2d64725ee5df95517fb754cb55e685` |
| `EXECUTIVE_SUMMARY_EN.md` | `14317c35e9b1318b26e0d6218c7dc6c7eb5d02d619f20de5d5f530bf7633903b` |
| `OPEN_QUESTIONS_EN.md` | `814b75b0c01da61a3df072d7d047d79c982a6495b869d1d7f79b7e46870691e0` |
| `REVISION_LOG_EN.md` | `c3bfa14aa6de861ea091d75a04bde053003b51029982f55129aaf352141c4a76` |

最终检查 **PASS**：标准库 Python 确认四个作者文件/日志哈希未变、四项审稿编号均有核销映射、三个复制界等号情形成立、五个 ByT5 吞吐比在 .7447–.7711 范围，报告 7 个 Markdown 链接中的本地目标均存在，UTF-8 与尾随空白检查通过。`git diff --check` 返回 0；目录本已未跟踪，因此直接内容校验才是实质检查。最终 Git 状态与任务开始时的顶层未跟踪项一致；没有辅助脚本或测试输出留存，本次唯一创建的浏览器标签已关闭。该核查证明文档修订及本次写入边界，不证明论文实验已复现。此 Markdown-only 任务不需要应用构建/pytest；未训练、安装、提交，未启动子代理。

**唯一新建交付文件：`05_review/FINAL_SURVEY_RIGOR_RECHECK.md`。核销结论：可译，无需新增 terra 全文阅读；此次复核以外的 COVERAGE 项目仍由其各自审稿证据承载。**
