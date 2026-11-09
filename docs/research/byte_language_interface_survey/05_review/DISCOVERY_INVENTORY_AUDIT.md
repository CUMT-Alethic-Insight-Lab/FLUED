# Discovery / granular inventory：独立初步来源审计

审查日期：2026-11-09。审查者：独立 sol；不是七流作者或综述作者。本文件是抽样来源审计，不是论文批量全文认证、算法证明认证或实验复现。

## 1. 结论先行

**可以进入去重、分类与选读；不能据此宣布独立长综述已完成。** 七流已经形成不同于项目提案验收的领域框架：历史字符路线、直接字节模型、Unicode 码点编码器、混合接口、生成与采样、优化、跨语言评估、计算与部署。多数抽样条目正确区分了“论文实际使用的技术”与分析者类比，以及参数、原文暴露、理论运算量和实测时间。

- 全部读取 `PLAN.md`，以及 **S01、S03–S08 各四文件，共 28 个交付文件**。S02 不在本轮范围，未等待、未据其暂缺作负面裁定。
- **实质抽审 28 条记录，每流 4 条**；对照 **26 个原始来源实体（25 篇论文、1 份标准）**，并实际读完 **8 张相关旧 FULL 卡**。一张卡复用多次不是多项独立证据。
- 确认一处明确任务名错误、一个会影响主干分类的重要缺项、一条非原子记录，以及共享权重和概率核算的待补证据。见 §3 的六项 P1。
- **未确认 P0 级捏造来源、把字符全面冒充字节、或把摘要冒充本轮全文的事实。** §2 列的是后续交付的 P0 阻断条件，不冒充已经发生的错误。
- 独立综述的**初步发现覆盖合格，最终证据覆盖未闭合**。尤其 CANINE / Charformer / MANTa 等核心早期路线仍缺完整原始阅读；ByteNet 主要为摘要级。不能只把近期动态分段论文读深，就宣称全领域已读透。

**本次唯一写入文件就是本文件。** 不修改七流、旧卡、计划、项目状态或术语表；不读多粒度草案来验收，不派代理、不训练、不安装、不提交。原始来源的提案相关性不参与判定。

## 2. P0：发布前阻断条件，不是已证实违规

定义：P0 是一旦出现在最终综述中，会改变研究对象或证据性质、必须阻止交付的错误；P1 是本轮应修订或补上明确边界的问题。

| 编号 | 阻断条件 | 当前证据与应落位置 | 解除条件 |
|---|---|---|---|
| P0-G1 | 将七流原始行数当成去重后发现数、独立论文数或实证成功数 | 七流共 **367 个本地记录 ID**，不是 367 项独立效果；同一 ByT5、MambaByte、W0356、UTF-8 validity 等跨流反复出现。应在 `02_inventory/` 合并层及 `04_synthesis/` 总计处约束 | 建立稳定 work ID / 别名 / record ID 对照；分别报告独立作品、实质问题记录、背景/标准、读深，不累加本地“新发现” |
| P0-G2 | 将未知或背景结论升级成字节模型通则 | S04 已正确限制词级共享、随机潜变量坍缩背景及单一 ByT5-Large 配置；S03 已区分贪心等价、精确采样与阈值接受 | 合成时保留条件：word≠byte，码点≠byte，字节 BPE≠逐字节；阈值接受≠保目标分布；配置/公式≠运行时张量别名认证 |
| P0-G3 | 在核心原始证据仍为 A/P 时称最终独立综述或“全文审查”完成 | 七流本身均报告本轮新 FULL=0，这是诚实状态，不是缺陷。源卡 FULL 也有附录范围限制 | 完成选读队列中决定主要结论的缺口，或在最终综述中按实际证据深度明确限定；不得把获取全文的字节数计作阅读 |

目前没有足够证据指控七流已经触发上述 P0。建议协调者将它们作为合并与最终审查的硬门，而不是要求发现流返工成另一份提案评审。

## 3. 六项 P1：具体修订位置与最小修改

### P1-01：ByT5 的 NER / XNLI 时延串位——明确事实错误

**位置：** `01_discovery/S01/PROBLEM_SOLUTION_TECHNIQUE_INVENTORY.md:75`，S01-R42 的 “large NER/summary slowdown”。该行工作 ID 为 W0351，不是 W0360。

**核对：** [ByT5 正式版](https://aclanthology.org/2022.tacl-1.17.pdf) §7、Table 10、p.300–301：时延任务是 G2P、Dakshina、GEM-XSum、**XNLI**；原文给 XNLI 6.4–9.5×、XSum 3.7–6.4×。旧 `B08/W0351.md:15` 也写 XNLI。NER 时延另见 W0360，不能无声移到 W0351。

**最小修订：** 将该处 NER 改成 XNLI，并补一句：XNLI 是较长句对输入、单数字标签输出；该巨大减速不能单归因于输出字节串变长。ByT5 §7 明说相对速度在“短输入和/或长目标”时更有竞争力。

**波及而非判错：** S03-R21、S06-R027、S07-R13 的输出瓶颈讨论可以保留，但后续不要用 XNLI 倍率单独证明“长输出导致减速”。编码深度、输入分辨率、输出步数应分账。

### P1-02：W0356 主干不是未加说明的普通全注意力 Transformer

**位置：** S01-R45；S03-R43；S04-R032；S05-050；S06-R030；S07-R44–45；S08-W27/R047，以及各自 WORKS 的 W0356 条。旧卡 `B14/W0356.md:5–6` 也没有完整列出此主干身份。本审查只登记修订，不改旧卡。

**核对：** [2610.05978v1](https://arxiv.org/html/2610.05978v1) §2.1、脚注1明确：按 Qwen3.5 设置，**Gated DeltaNet 与 Gated Softmax Attention 按 3:1 交错**；作者称 flat 是相对显式 local–global–local 层级而言。卷积宽 4→16 指的是其中的 Gated DeltaNet。§2.2 原文确实说同训练 FLOPs 最优前沿 Subword 始终更好，不能因主干补正删掉这一负结果。

**最小修订：** WORKS 写为“无显式局部—全局层级的混合注意力主干（Gated DeltaNet : Gated Softmax Attention = 3:1）”；inventory 的 dense/flat 要定义为“全分辨率/无显式层级”，不得让读者误读为纯稠密 softmax 注意力。保留四字节早期包目标、哈希输入和卷积宽差异的实际角色。

**影响：** 这不是认定现有 dense 一词必然虚假，而是一个重要分类歧义。若综述以此当“现代纯全注意力字节基线”，就会把已经使用的循环/线性注意力技术漏算，也会破坏与 MambaByte 的主干对比。

### P1-03：S08-R060 一行含两篇论文、两个不同问题——应移为综合关系或拆分

**位置：** `01_discovery/S08/PROBLEM_SOLUTION_TECHNIQUE_INVENTORY.md:89`；S08 的四文件表头和计数说明随中央处理同步。

**核对：** R060 同时装入 W34 TokSuite 的同文本预算和 W16 方言研究的 parity–任务相关性，两项无共同实验。该行诚实说明 pairing 是分析者综合，因此**不是虚构共同实验**；但不满足 PLAN“一个具体问题/行”的严格可审计性。

**最小修订：** 首选将其改为不计问题条数的综合关系：TokSuite 部分链接已有预算记录，方言相关性另建独立记录；或拆成子记录并先与既有预算行去重。**不要机械从 60 增为 61**，更不能把两篇文献并列当多一项独立效果。

跨流同义问题也应合并：W0356 的“同参数胜、同算力败”、W0351 的固定位置原文暴露、W0509 的部分/严格合法性，在多流有实质重复。相反，CharacterBERT 的局部输入、封闭 MLM 监督和噪声评测是不同问题，允许一文多行，不应为去重把它们压成一个模型名。

### P1-04：共享权重章缺少可用的直接字节正例/反例，不能只留下一个旧 Large 配置

**位置：** S04 WORKS §“Configuration findings”、inventory R003 与末尾 T 类缺口；交叉链接 S03-R08/R25、S08-R060。

已有 ByT5-Large 的限定写法是正确的：旧卡只静态对过 Large/XNLI operative gin，未读取权重、未证运行时依赖 commit。此次同一 [gin URL](https://storage.googleapis.com/t5-data/pretrained_models/byt5/large/operative_config.gin) 再抓仍不能提取，**没有新增原始 gin 认证**。

但本轮原文已经给出两项应进入共享轴的证据，而不是继续把其他直接字节模型一律放进未知：

1. [MEGABYTE v2](https://arxiv.org/html/2305.07185v2) §2.2，local 输入用 `E_local-embed`，式(6)输出投影复用同名矩阵——**论文规格层面的 local 输入/输出共享证据**，不是运行实现认证。
2. [TokSuite v2](https://arxiv.org/html/2512.20757v2) §3.3 直接说十四模型使用 **untied embeddings** 的 Llama-3.2-1B 配置，其中包含 ByT5 **tokenizer** 臂。这是“因果字节 LM、TokSuite 架构、ByT5 分词接口”，绝不是原始 ByT5 编码器—解码器 checkpoint。

另 [LCA v2](https://arxiv.org/html/2608.15454v2) §3 明确两个预测头共享单个 unembedding；这是**头与头共享**，不是输入表与输出表共享。应作为另一独立轴登记。

此次内置浏览器确实读到官方 [ByT5-Small 当前 config](https://huggingface.co/google/byt5-small/raw/main/config.json)：`tie_word_embeddings=false`，12/4 层，`T5ForConditionalGeneration`，vocab_size=384。此为**可变 main 的配置旁证**；为锁 commit 请求公开模型 API 失败，未做类定义或张量别名核验，故不能升级为版本固定的全部模型结论，也不能将该 port 的 384 直接替换论文原始 256+3/sentinel 设计。

**最小修订：** 在中央共享台账分别加 `sharing_axis`、`paper_spec/config/code/runtime`、实际模型/port/version、`known/unknown`。把可直接确认的三项论文规格录入，配置动态旁证单列待锁版本。无需训练任何共享消融。

### P1-05：TokSuite 原文 C.2 的 BPB 解释有待核异常，旧 FULL 卡并未覆盖这一问题

**位置：** S03-R47、S05-040、S06-R043–44、S08-R060 的工作级来源备注，以及相应选读/定点复核队列；不改这些条目已正确记载的主要任务成绩。

**原文异常：** [2512.20757v2 HTML](https://arxiv.org/html/2512.20757v2) Appendix C.2 说 “BPB normalizes the cross-entropy loss by `log_2 |V|`”。一般而言，原文字节平均负对数概率应为

`BPB = -sum(log2 p(event)) / original_UTF8_byte_count`。

若 CE 为每 token 的自然对数平均，还要乘 token 数/原文字节数并除 ln 2；除以 log2 词表大小本身不是该换算。该原句与正确 BPB 定义不符；**可能是写作公式错误，不等于已证其代码这样算**。

本次获取 PDF 的抽取内容未到 C.2；HTML 的正文注释/附录顺序也不完整。旧 `B22/W0518.md` 确有正文、主要表和同文预算的 FULL 阅读范围，但卡中没有讨论此句。故本审查只登记原文疑点，不作实现错误、所有 BPB 无效或选择题结论无效的裁定。

**最小修订：** 在工作级备注挂“C.2 BPB prose requires PDF/code formula check”；下一位只需定点核 PDF C.2/图6计算代码，明确概率事件、单位和原始 byte 分母，再决定是勘误还是实算问题。主要 option scoring 与精确 byte scoring 的附录 F 是另一个证据对象，不要混在一起。

### P1-06：核心全文缺口仍会使最终覆盖失衡，选读队列应跨流合并而非累加

**位置：** `01_discovery/S01/READING_HANDOFF.md:15–17`、S06 的第6/9项、S07 第7–9项；协调者下一轮的 `03_reading/` 分配和 `04_synthesis/` 覆盖说明。

CANINE / Charformer / MANTa 分别代表码点哈希/降采样、候选块混合、显式可微字节分块。七流已列它们，但大量支持仍是 A 或 P；完整技术比较不能由近期 BLT/H-Net 的旧卡替代。ByteNet、历史字符压缩及非神经/概率分段路线也明显浅于近期 patch 系列。

**最小修订：** 同一原文跨流只分配一次，完整卡回连所有 affected records；先为上述三条早期主路线闭合单位、学习信号、输出端与真实速度条件，再追补最近论文的同义描述。若时间不足，把未闭合项留成准确的范围限制，不能称穷尽。

这是一项最终覆盖的整改，不是要求发现流各自增加 FULL 数，也不是因为 S02 尚未恢复而否定它。

## 4. 28 条定点样本：原文、旧卡与判定

以下位置均相对于 `docs/research/byte_language_interface_survey/`。原文键 P01–P26 在 §5 给出固定版本 URL；旧卡键 C1–C8 在 §6 给出项目内路径。**“一致”只对应本行主张，不是整篇论文认证。** 数值仅卡可核时明确写“卡一致”，不伪装本轮重读了图表。

| 样本 | 修订定位 / 主张 | 此次原始来源实际检查 | 旧卡与审查结果 |
|---|---|---|---|
| A01 | S01-R24，inventory:50；CharacterBERT 的字符名/字节实质 | P01 §3.1 脚注6：UTF-8 转 bytes，263含special，最长50；CNN/池化/两层highway | 无旧 FULL 卡。**一致**；是预分词词内 byte composition，不是原始字节流 LM |
| A02 | S01-R25，inventory:51；开放输入、封闭监督与预训练成本 | P01 §5.1.1：top100K临时词目标，词表外从不mask，BERT 26.5h/CharacterBERT 55h；NCE仅未来工作 | 无旧卡。**一致**；与A01是不同问题，不是为一文强拆同义行；输入/监督/成本需一起引用 |
| A03 | S01-R29，inventory:55；embeddingless 的收益是否来自dropout | P02 §6：同调token dropout后 En→X近同；反向去embedding平均−0.45 BLEU，subword领先0.76 | 无旧卡。**一致**；明确作者实际采用token dropout，不把“参数少”自动解释为正则化因果 |
| A04 | S01-R42，inventory:75；ByT5 输入/输出计算非对称 | P03 §7/Table10：G2P/Dakshina/XSum/XNLI，长输入短标签可最慢 | C1也写XNLI。**修订P1-01**：该行NER不受此源支持；保留3:1层比分配及非等原文条件 |
| A05 | S03-R04，inventory:24；池化后的因果掩码 | P04 §2.2/Fig4–5：正常右移1后，shortening前另移k−1，避免未来泄漏 | 无旧卡。**一致**；精确索引对齐，不是“加causal mask便够”；未重证附录证明 |
| A06 | S03-R08，inventory:33；MEGABYTE组内联合分布 | P05 §2.2、§2.4：global移一个patch、local移一个byte；local AR使输出依赖前面真实byte | 无旧卡。**一致**；训练时多patch并行≠组内采样独立；式(6)还提供局部I/O共享规格 |
| A07 | S03-R26，inventory:56；LCA置信接受 | P06 §3.1阈值式、§4.4及§6.1：左到右阈值接受，首byte必收；单B200/batch1，IFEval采样不同于其他任务 | 无旧卡。**一致**；阈值方案没有目标采样律保持保证；保持与另行verification消融分开 |
| A08 | S03-R39，inventory:74；MambaByte speculative 2.6× | P07 Table8说明/AppendixF定位：110M subword drafter、3subwords、8192输出bytes、top3验证 | C2一致。**一致**；2.6×不是无额外模型、也不是精确采样提速；表值/设备条件沿用卡与该表说明 |
| A09 | S04-R003，inventory:28–32；ByT5两种sharing | P03论文只支持接口/模型预算，非gin；原gin抓取失败；当前Small官方config由浏览器读到false但未锁commit | C1只支持Large/XNLI限定静态检查。**原有谨慎写法合格；P1-04补证**，不要把“不能新抓gin”等同旧证据伪造 |
| A10 | S04-R011，inventory:78–82；output-path约70% | P08 §5.3读取gradient hooks与范数比例；Fig1均值.719/.525；AppendixE文字也承认缩放后任务混合 | C3一致。**一致**；范数占比不是Adam实际更新占比；不是byte-specific证据 |
| A11 | S04-R013，inventory:90–94；伪逆共享的维数条件 | P09 §4式4–6：Z为V×d、ZᵀZ=I、E=ZT⁻¹；SPD/Cholesky操作确为作者技术 | 无旧卡。**一致**；V≥d是审查/分析者线性代数推论，不伪装论文在256byte上做过实验 |
| A12 | S04-R017，inventory:114–118；所谓cosine输出头 | P10 §2.2.4式28仅除行向量范数，仍乘隐藏状态范数；§3.2文字有.41 BLEU | 无旧卡。**一致**；不能归入固定温度、两端全归一化cosine。未独立审核所有结果表 |
| A13 | S05-002，inventory:18；grapheme/码点/byte | P11 rev47 §1–3：grapheme近似用户字符、需版本与tailoring，不保证每语言绝对一致 | 无旧卡。**一致**；规范算法不是AI方法，不计模型效果；不将CP编辑距离称G编辑距离 |
| A14 | S05-018，inventory:39；MAGNET高压缩负结果 | P12 §5.1支持压缩/任务权衡，§2.2脚注10明确单script假设；具体44.62/44.61/41.06及语种值本轮抽取未呈现表格数字 | C4数值一致。**限定通过**：数值为旧卡继承；不是本轮视觉重验。压缩率公平不能替代每语质量；未知code-switching不能写支持 |
| A15 | S05-022，inventory:43；random byte ensemble “robustness” | P13 §3.4给逆映射对齐概率再平均；§5.4为z∈{1,2,4,6,8}、每z五次 | 无旧卡。**一致**；这里是编码/运行方差与ensemble，不是自然typo鲁棒；模型份数带来预算增长 |
| A16 | S05-041，inventory:72；UTF-8部分/严格合法性 | P14 §4明8,000BPE+fallback，§5.1.1正文96.21/95.26/86.97；严格数字的表格本轮HTML未给出 | C5严格50.47/30.24/33.33一致。**限定通过**；严格数值仍是卡继承，不能当纯byte LM失败证据；未本轮复核abs/PDF冲突 |
| A17 | S06-R004，inventory:22；Sparse Transformer负对照 | P15 §7.2/Table2：12288byte、95M；dense1.00/fixed.99/strided1.13；Time/Iter1.31/.55/.35无明示单位 | 无旧卡。**一致**；固定/跨步拓扑不是等效，训练迭代不是服务延迟；百万长度来自音频可行性不冒充文本 |
| A18 | S06-R020，inventory:48；BLT外部entropy成本 | P16 §4确认100M/14层/512窗口、§10明确不联合训、真实wall-clock可能不平价；本次PDF抽取未到AppendixH | C6支持主算式未单列entropy生命周期。**限定通过**：方法原文已核，附录“漏项”本轮卡级核，不称完整端到端成本已闭合 |
| A19 | S06-R030，inventory:63；同参数/同FLOPs前沿 | P17 §2.1脚注1及§2.2原文：混合注意力3:1、TST/hash、同FLOPs Subword始终更好 | C7前沿一致、主干描述不足。**P1-02补主干身份**；不可称只换tokenizer或纯全注意力比较 |
| A20 | S06-R038，inventory:81；Compute Optimal Tokenization | P18 §2/§3.1–3.2：988+320、50M–6.7B、4B–1.1Tbytes；α=.465、β=.471，N仅latent参数 | 无旧卡。**一致但有强边界**；不是所有域/模型的普适bytes/parameter常数，也不是teacher-inclusive成本认证 |
| A21 | S07-R23，inventory:48；frozen-mBERT MLM接入 | P19 §3.2：上层固定、原输出E固定，15%subwords字符mask、1M×512、有效batch2000 | 无旧卡。**一致**；冻结参数不消除对composer的反传；输出仍旧subword，非byte生成 |
| A22 | S07-R32，inventory:57；ZeTT模仿warmup/anchor | P20 §3.1与AppendixB相关段：warmup模仿旧embedding；untied-GPT2无aux loss发散；不是所有条件都发散 | 无旧卡。**一致**；作者明确称MIMICK-style，确有技术沿用证据，不仅分析类比；不能推成共享普遍必要 |
| A23 | S07-R48，inventory:78；fallback≠合法UTF-8 | P14 §4/§5.1检查实际模型单位与部分合法性；相同源再次用于不同流 | C5同一张卡，不是新一项独立验证。**限定通过**；同A16的严格数字与版本冲突边界不能在合并时丢掉 |
| A24 | S07-R51，inventory:96；历史分阶段训练 | P21 §2.5明确引用greedy layer-wise deep-network训练；先word lookup+attention/V2C、再C2W平方距离模仿、最终全调 | 无旧卡。**一致**；真正作者借用AI训练技术，不是后人类比；额外阶段成本未知；仍是字符/词结构混合 |
| A25 | S08-R019，inventory:38；end-boundary未来信息 | P22 §5.3：完整Llama3 BPE边界提示、end优势较大；start无泄漏仅作者论断 | 无旧卡。**一致且保留待证**；作者未提供本轮可核的prefix-stability证明，不能把offline start flags无条件称因果；与合法token链问题分开 |
| A26 | S08-R030，inventory:54；canonical路径与文字串marginal | P23 §2、§4.1：importance sampling、128samples/document、18层1024、停用TXL memory、分母whitespace词；1.9%为相对PPL | 无旧卡。**一致**；有限sample不是精确全路径；EOS/非规范化/估计量条件继续未知，不偷换成BPB或新训练byte模型 |
| A27 | S08-R035，inventory:59；因果估计与因果注意力 | P24 §3–6：RD、cutoff continuity、离散rank、57M/32K/50k、2.88nats局部效应 | 无旧卡。**一致**；统计因果识别有假设，不是随机词表试验，也不是所有词条/所有byte模型17倍 |
| A28 | S08-R060，inventory:89；两工作拼一行 | P25 §3.3确认同token但不同rawbytes及untied配置；G.2具体同文表本轮继承C8；P26 §4.1/5.2确认LoRA与FFT不同、较强DI模型TP相关性反向 | C8支持四个非byte tokenizer同文子集。**P1-03拆/移综合；P1-05加BPB疑点**。两篇对照不能当一个作者研究、也不能计作重复新增效果 |

## 5. 本轮实际联网来源账

只做题名/版本已知的定点访问；没有泛搜索、没有声称系统检索或全文覆盖。以下 P01–P26 都实际返回了原始材料；大响应只检索并读指定章节，未读完剩余正文/附录。表格缺失的范围按 §4 明示。重复 HTML/PDF 访问不是独立作品。

| 键 | 实际公开URL / 版本 | 本轮用途 |
|---|---|---|
| P01 | https://arxiv.org/html/2010.10392v3 | CharacterBERT §3.1/5.1.1；单位、监督、时间 |
| P02 | https://aclanthology.org/2021.naacl-main.17.pdf | Embeddingless NMT §3/4/6，dropout控制 |
| P03 | https://aclanthology.org/2022.tacl-1.17.pdf | ByT5 §3/7、Table10说明；不是共享配置源码 |
| P04 | https://arxiv.org/html/2110.13711v2 | Hourglass §2.2–2.3右移与表达性段 |
| P05 | https://arxiv.org/html/2305.07185v2 | MEGABYTE §2.2、式4–6、§2.3–2.4 |
| P06 | https://arxiv.org/html/2608.15454v2 | LCA §3/3.1/4.4/6与AppendixB cache相关段 |
| P07 | https://arxiv.org/html/2401.13660v3 | MambaByte Table8说明及AppendixF相关位置 |
| P08 | https://arxiv.org/html/2603.26663v1 | output gradient §5.3、AppendixE结果解释 |
| P09 | https://arxiv.org/html/2602.04556v2 | PIT §4式4–6，未证全文/所有实验 |
| P10 | https://arxiv.org/html/2001.07885v2 | normalization §2.2.4/§3.2；非完整结果表审核 |
| P11 | https://www.unicode.org/reports/tr29/tr29-47.html | UAX29 rev47介绍、conformance/字素范围；非实现验证 |
| P12 | https://arxiv.org/pdf/2407.08818v2 | MAGNET §2.2脚注10、§5.1；数表值卡级继承 |
| P13 | https://aclanthology.org/2022.coling-1.388.pdf | BMNMT §3.4/4.1/5.4 |
| P14 | https://arxiv.org/html/2606.14122v2 | UTF-8 validity §4/5.1、8k+fallback身份 |
| P15 | https://arxiv.org/html/1904.10509v1 | Sparse §4/5/7.2、Table2 |
| P16 | https://aclanthology.org/2025.acl-long.453.pdf | BLT §3/4/10；附录H未在本次抽取中读取 |
| P17 | https://arxiv.org/html/2610.05978v1 | W0356 §2.1脚注1/§2.2；完整主干与前沿原文 |
| P18 | https://arxiv.org/html/2605.01188v2 | scaling §2及§3.1–3.2；参数定义/拟合值 |
| P19 | https://arxiv.org/html/2010.12730v3 | Char2Subword §3.2；冻结与监督 |
| P20 | https://arxiv.org/html/2405.07883v2 | ZeTT §3.1及AppendixB warmup/aux段 |
| P21 | https://arxiv.org/html/1511.04586v1 | Character-based NMT §2.5–2.6；标题不等于Finding Function in Form |
| P22 | https://arxiv.org/html/2604.27263v2 | Decoupling §5.2–5.6；机制分离、边界提示权限 |
| P23 | https://aclanthology.org/2021.emnlp-main.161.pdf | marginal likelihood §2/4.1；未把抽取当FULL |
| P24 | https://aclanthology.org/2025.acl-long.1374.pdf | Lesci §3–6、连续性/窗口与局部效应 |
| P25 | https://arxiv.org/html/2512.20757v2 | TokSuite §3.3、C.2；G.2表本轮未在HTML中读到 |
| P26 | https://aclanthology.org/2025.emnlp-main.1224.pdf | 方言研究§4.1/5.2–5.3，相关非因果/显示glyph非不可逆损坏 |

**额外访问与失败：**

- https://arxiv.org/pdf/2512.20757v2 ：合法复核同一作品的PDF；抽取未达C.2，不能声称已视觉复核该公式或G.2表。
- https://storage.googleapis.com/t5-data/pretrained_models/byt5/large/operative_config.gin ：抓取失败，未产生新的gin证据。
- https://huggingface.co/api/models/google/byt5-small/revision/main ：公开API请求失败，未锁定config commit。
- 内置浏览器独立新建本任务后台tab，读取 https://huggingface.co/google/byt5-small/raw/main/config.json 的完整可见JSON，随后成功关闭；没有接管其他任务/用户tab。浏览器报告共享侧已有远超10个tab，侧栏拥挤；本任务只新增并关闭自己的1个tab。
- 本轮共 **29次FetchURL请求：27次返回材料、2次失败**；其中26个来源实体，TokSuite HTML/PDF为同一论文。另1个浏览器配置读取，不算新论文。没有登录墙、付费访问、绕墙或不受限重试；没有主动下载、转换或在项目外写临时文件。工具自动缓存响应不作为交付引用，持久定位只用上述公开URL/章节。

## 6. 实际旧 FULL 卡核对账

均为 `docs/research/flued_multigranularity_survey_20261108/03_reading/` 下现存文件，只读。使用这些卡不等于使用多粒度草案验收。

| 键 | 卡路径（项目内） | 本轮核对要点 |
|---|---|---|
| C1 | `docs/research/flued_multigranularity_survey_20261108/03_reading/B08/W0351.md` | 输入/输出sharing分轴；Large/XNLI限制；Table10是XNLI；byte/text预算 |
| C2 | `docs/research/flued_multigranularity_survey_20261108/03_reading/B14/W0352.md` | 110M drafter、top3、2.6×；非精确采样；30B/80B不等文本 |
| C3 | `docs/research/flued_multigranularity_survey_20261108/03_reading/B14/W0366.md` | 范数比例非更新比例、数据/模型混杂、gradient×5任务不单调 |
| C4 | `docs/research/flued_multigranularity_survey_20261108/03_reading/B26/W0510.md` | 单script权限、高压缩语种损失、图表口径疑点仍保留 |
| C5 | `docs/research/flued_multigranularity_survey_20261108/03_reading/B22/W0509.md` | BPE+fallback、严格/部分/正确性、abs/PDF冲突的实际旧复核范围 |
| C6 | `docs/research/flued_multigranularity_survey_20261108/03_reading/B05/W0010.md` | separate entropy teacher、主FLOPs式范围、架构/边界混杂、未全读附录 |
| C7 | `docs/research/flued_multigranularity_survey_20261108/03_reading/B14/W0356.md` | 前沿反转、TST/hash、oracle；本轮新发现的混合主干信息不在卡中充分表达 |
| C8 | `docs/research/flued_multigranularity_survey_20261108/03_reading/B22/W0518.md` | 原同文子集四tokenizer、ByT5不在其中；不替作者认证每语言截断 |

七流复用卡时普遍保留了旧读者范围，没有把 FULL 等同代码/证明通过。此次也出现真实“来源虽读过、卡未承载”的信息（W0356主干、TokSuite C.2）。因此 FULL 卡只能按其记载字段复用，不能当该论文一切潜在主张的万能担保。

## 7. 单位、技术沿用、因果与预算的横向裁定

### 7.1 单位：本次未发现系统性 byte / character 冒名

可保留的关键纠偏：CharacterBERT 名称字符但实现词内UTF-8 bytes；CANINE是码点；DTP历史清理字符不等于所有UTF-8；BBPE、UTF-8/16后BPE和fallback是混合或子词；BMNMT是byte输入/输出；字节标注模型输出的是span/label而不是下一文本byte。UAX29是字素边界标准，不是神经模型。

中央表必须把 `input / internal / output / supervision` 四元组实际展开，不能只拷贝byte标签。各流WORKS继承模式作为本地关系表合理；合并时若丢掉WORKS，记录就会失去这些约束。

### 7.2 “真正借用AI技术”有可核例子，不应把类比算进去

- 明确作者沿用：CharacterBERT用ELMo Character-CNN/highway；ZeTT称MIMICK-style embedding warmup；Character-based NMT直接援引greedy layer-wise训练并另用IBM4对齐监督。
- 作者实际用、但未必证明特定思想传承：卷积、局部/交叉注意力、状态空间递归、straight-through、LoRA、辅助CE、蒸馏、梯度门控。记“使用技术及作用”即可，不自动写成某论文首创或从某工作借来。
- 非AI机制但可以是合法研究记录：Unicode校验、原文byte分母、耗时测量、平行句长度统计、RD因果估计。它们可填“无神经技术/统计或评估方法”，不能为了让technique栏非空改称模型模块。
- 分析者类比：将任意残差支路称潜变量坍缩、将字节组装称检索、将pooling称来源回访。七流大体已禁止；合成时不要再引回。

### 7.3 因果是至少三种不同问题

1. **时间可见性：** 完整source的双向编码、masked prediction、字节前缀AR、离线全串边界标签、suffix允许的FIM，不同权限。
2. **生成分布：** 组内AR、独立未来offset heads、diffusion joint、阈值近似、greedy verification、精确sampling correction，不同概率对象。
3. **实验归因：** dropout控制、matched-rate/compute、统计RD连续性假设、单次训练干预。前缀因果正确不自动证明实验单因素归因。

28样本中这些区分总体保住了。Hourglass右移、LCA阈值、Mamba top3是特别有价值的反混淆锚，不宜在综述中缩成一句“多字节更快”。

### 7.4 预算应给结果类型，不拼跨论文倍数排行榜

最少分开：原文字节/唯一文本与重复暴露、原文context、模型位置、总参数与latent参数、训练专用头、teacher/drafter历史与在线成本、主算式FLOPs、实测训练迭代、decode wall-clock、persistent cache与总内存。

现有材料已经包含原文暴露不等、纯参数优势在FLOPs下反转、encoder-only节省被长目标稀释、oracle accepted positions不是实速等实质反例。未知全系统成本不等于成本为零，也不意味着论文的局部预算结果无效。

## 8. 是否覆盖独立综述：按领域轴而非草案功能验收

| 领域轴 | 七流已具备 | 未闭合/下一步 |
|---|---|---|
| 历史与表示接口 | 早期RNN/LSTM、字符CNN、词内composition、直接byte annotation/LM/NMT、码点与字素标准 | ByteNet、深字符压缩主要摘要；非神经压缩与正式segmental LM历史薄，不称穷尽 |
| 可微分组与边界 | 已列CANINE/Charformer/MANTa、DTP、fixed/rule/entropy/learned hierarchy | S02不在本轮；前三条原始全读需共享卡闭合，不能由新H-Net/BLT代替 |
| 因果生成与输出 | Hourglass/MEGABYTE、MTP/LCA/MtPC、diffusion/speculation、概率prefix问题 | 关键joint/sampler证明、partial prompt、EOS、缓存实现仍多未完整检查 |
| 权重与优化 | 表共享/归一化/秩/梯度、辅助目标/分阶段接入；背景与byte分开 | 直接byte tying census稀疏；本轮补出的MEGABYTE/TokSuite/LCA分轴证据应整合 |
| 多语与鲁棒 | 历史多语NMT、低资源反例、UTF-8合法性、normalization、字素标准、方言相关 | mixed-script causal routing、非ASCII numeracy、长自然多语逐字复现证据薄；缺少不能反推失败 |
| 计算与服务 | 稀疏注意力、byte SSM、分层更新、encoder删减、实测与代理成本分离 | W0356混合主干需标清；缺统一质量匹配的现代batch serving账，不制造排行榜 |
| 混合与适配 | 字符/词fallback、frozen-host geometry、hypernetwork、蒸馏与分阶段训练 | 临时byte监督与最终byte部署要分开；T-FREE输出/OOV等仍需选读 |
| 方法与反例 | marginal概率、RD、同文本子集、机会/随机基线、跨模态排除 | 中央别名/record去重尚需完成；TokSuite BPB异常是下一项窄复核 |

**综合判词：** 这些材料足以支撑一篇真正独立综述的提纲、问题清单和分类，不再只能围绕某项目机制讲故事；但当前是发现/盘点阶段。接受“发现阶段可用”，不接受“全领域全文证据已闭合”。任何FLUED含义只能作为最后有界讨论，不能倒过来决定哪些先行工作有价值。

## 9. 最小关闭清单与本轮验证

协调者关闭本审查只需：

1. 修正S01-R42的NER→XNLI并保留输入/目标成本条件。
2. 中央W0356条补3:1混合注意力主干，避免flat/dense歧义跨流传播。
3. R060去原子化问题修复；全局按work与实质problem去重，不将367当净记录数。
4. 三种直接共享证据分轴录入，当前Small配置只作未锁版本旁证。
5. 定点核TokSuite C.2 PDF/实现的BPB计算，不先判所有结果错误。
6. 合并核心选读任务，补主要路线的缺失证据并保留尚未知；S02恢复后单独接入，不由本审查代写。

**验证实际完成：** 用只读Python按各流主记录行匹配，S01/S03/S04/S05/S06/S07/S08分别51/51/51/54/48/52/60，每流ID无重复，共367；这只验证本地结构，不是语义去重或学术正确性。28样本与26来源的定位已列明，8张旧卡实际读完。报告中的本地输入存在性、样本计数与UTF-8/空白通过交付前静态检查；最终git状态仅用于观察，不把共享未跟踪目录的状态当独占写入证明。

不运行build/pytest：本轮交付只有来源审查Markdown，没有改代码或可执行实验。没有后台任务；本任务浏览器tab已关闭。原有未跟踪语料、其他流文件及bundle均未清理或修改。未把发现的P1直接改进他人文件；修订责任和位置已在本报告交接。
