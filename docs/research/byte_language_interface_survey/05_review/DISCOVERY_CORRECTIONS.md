# Discovery corrections — 六项 P1 的独立修订证据

2026-11-09。角色：独立修订证据负责人；面向中央目录维护者、英文综述作者及 terra 选读负责人。

## 0. 范围、阅读深度与采用方式

先完整读取 [PLAN.md](../PLAN.md) 和 [DISCOVERY_INVENTORY_AUDIT.md](DISCOVERY_INVENTORY_AUDIT.md)，再按审计 §3 的 P1-01–06 回查相关 S 流、旧卡及公开原始材料。**本任务唯一写入本文件；以下是可采用修订，不是声称已替他人改完文件。** 不修改 PLAN、审计、S 流、旧卡、旧大报告或生产文件，不派代理、不训练、不安装、不提交。

本轮是定点纠错：实际核到 **9 篇论文的指定原文范围、4 张完整旧卡、同一固定代码版本的 3 个源码文件**；新论文 FULL 数为 **0**。没有全盘复核八流、没有重算去重后的总量、没有执行论文代码。核心全文缺口仍交 terra，不能用本轮更准确的段落摘要核销。

证据层级在本文按普通含义区分：**论文规格**是原文公式/明确陈述；**配置**是特定发布版本的开关；**代码静态检查**是读取相应定义/调用；**运行验证**是实际权重和执行中的参数关系。本轮没有最后一项。稳定 W ID 沿用旧目录；S08 的 W16/W27/W34 是流内编号，不能无前缀当全局 W ID。

### 采用总表

| 审计项 | 本轮结论 | 目录维护者采用位置 | 综述作者采用内容 | 尚不能关闭的部分 |
|---|---|---|---|---|
| P1-01 | 确认 NER/XNLI 串位；正式 PDF 已视觉复核 | S01-R42 / W0351，记录其 Table 10 引用 | XNLI 长输入、单数字输出也会显著慢；输入与输出成本分开 | 不将此倍率外推到另一论文的 NER 或现代层级模型 |
| P1-02 | 确认混合主干身份；附录另补未共享输入/输出表 | W0356 全局 work 记录及七流受影响记录 | flat 指无显式局部—全局—局部层级，不指纯 softmax 注意力 | 不把参数前沿叫全系统同总参数，不删等训练 FLOPs 的负结果 |
| P1-03 | R060 是诚实标记的综合，但非原子问题记录 | S08-R060 移综合关系；两篇分别链接原子记录 | 预算控制和方言任务相关性分开叙述 | 不机械新增净记录数；相关表/附录仍待 terra |
| P1-04 | 可补四条直接字节模型论文规格；ByT5 旧配置另列 | S04 共享轴台账及跨流链接 | 局部输入/输出共享、两头共享、明确不共享不是同一轴 | 版本/实际权重别名未认证；不存在共享好坏的统一消融 |
| P1-05 | TokSuite C.2 错误单位措辞在 v2 **PDF p.21** 也存在，不只是 HTML 问题 | W0518 工作级备注、S03/S05/S06/S08 相关来源备注 | 暂不采用 Figure 6 证明跨 tokenizer 等 BPB/等训练充分性 | Figure 6 实际后处理链未定位，不能判其代码或全部任务结果错误 |
| P1-06 | 三条核心早期路线仍缺完整原始阅读；S02 已有补充 PARTIAL，但非 FULL | 合并跨流 terra 队列，一文一负责卡 | 可写准确机制身份，不能写全领域证据闭合 | CANINE、Charformer、MANTa 全文及历史路线的实质缺口保留 |

## 1. P1-01 — ByT5 时延任务名与输入/输出归因

### 回查定位

- [S01 inventory](../01_discovery/S01/PROBLEM_SOLUTION_TECHNIQUE_INVENTORY.md) **:75，S01-R42 / W0351**：现写 `large NER/summary slowdown`。
- [旧 W0351 卡](../../flued_multigranularity_survey_20261108/03_reading/B08/W0351.md) **:13–15**：已经正确写 XNLI，卡本身不用改成 NER。
- [ByT5 正式 PDF](https://aclanthology.org/2022.tacl-1.17.pdf)，**印刷 p.300 / PDF 第10页 Table 10；p.301 / 第11页 §7 续文**。本轮直接视觉读取表头、倍率及解释，不依赖摘要。

Table 10 四项是 Grapheme-to-Phoneme、Dakshina、XNLI、GEM-XSum；XNLI 减速 **6.4–9.5×**，XSum **3.7–6.4×**。§7 将 XNLI 明说为较坏情形：输入是句对，标签为单数字 `{0,1,2}`；相对 mT5，ByT5 在短输入和/或长目标任务上推理速度更有竞争力。后一句是该文架构下的**相对速度观察**，不等于长输出的绝对串行成本更小。

### 可直接采用

**目录行局部替换：**

> Task inference ranges from near-parity G2P to substantial XNLI and summarization slowdowns. In Table 10, XNLI is 6.4–9.5× slower and GEM-XSum 3.7–6.4× slower under the reported TPU settings. XNLI has sentence-pair inputs and a single-digit label, so its slowdown is not evidence that long byte outputs alone cause the cost.

**作者段落：**

> Byte-level input processing and byte-level output generation impose distinct costs. ByT5's encoder-heavy allocation does not make long sentence-pair classification cheap: XNLI remains a particularly slow case despite its single-digit output. Comparisons should therefore separate source length and encoder work from autoregressive target length, rather than attributing all task latency to longer generated strings.

NER 的另一个来源是 **W0360**：[旧卡 B08/W0360.md:13](../../flued_multigranularity_survey_20261108/03_reading/B08/W0360.md)，原文入口 [EACL Findings 2023 PDF](https://aclanthology.org/2023.findings-eacl.128.pdf)，§3.2 / Appendix Table 3。旧卡报单 V100、100 个英文样本、batch 1，ByT5/mT5 的 XNLI 为 36.49/40.94ms，NER 为 333.72/171.99ms。**这组数本轮只复核旧卡，未重看 W0360 原始表图**；它用于辨明不同证据对象，不用来覆盖 ByT5 的 TPU 数值。S03-R21、S06-R027、S07-R13 等输出成本讨论无需因此删除，只须不用 XNLI 倍率单独证明长输出瓶颈。

## 2. P1-02 — W0356 的主干、dense/flat 与前沿口径

### 回查定位与新增证据

受影响记录：S01-R45、S03-R43、S04-R032、S05-050、S06-R030、S07-R44–45、S08-W27/R047，以及各流 WORKS 中的 W0356。定位分别见各流 [S01](../01_discovery/S01/PROBLEM_SOLUTION_TECHNIQUE_INVENTORY.md)、[S03](../01_discovery/S03/PROBLEM_SOLUTION_TECHNIQUE_INVENTORY.md)、[S04](../01_discovery/S04/PROBLEM_SOLUTION_TECHNIQUE_INVENTORY.md)、[S05](../01_discovery/S05/PROBLEM_SOLUTION_TECHNIQUE_INVENTORY.md)、[S06](../01_discovery/S06/PROBLEM_SOLUTION_TECHNIQUE_INVENTORY.md)、[S07](../01_discovery/S07/PROBLEM_SOLUTION_TECHNIQUE_INVENTORY.md)、[S08](../01_discovery/S08/PROBLEM_SOLUTION_TECHNIQUE_INVENTORY.md)。[旧 W0356 卡:5–8](../../flued_multigranularity_survey_20261108/03_reading/B14/W0356.md) 支持课程/预算/模拟接受数，但未充分携带以下主干身份。

[2610.05978v1](https://arxiv.org/html/2610.05978v1) 本轮读到的直接锚：

1. **§1** 将 flat 明确定义为没有显式 local–global–local hierarchy。
2. **§2.1** 直接说两类模型都从头训练于 mixed attention model；字节版将 **Gated DeltaNet 的卷积宽从4增至16**。Gated DeltaNet 是带门控的增量状态更新注意力模块，不是普通全注意力层的别名。
3. **Appendix A.4 “Dense model configuration”**：Qwen3.5 text architecture；**Gated DeltaNet : Gated Softmax Attention = 3:1**，深度按四层递增以保此比例；明确 `All models are trained from scratch with untied input and output embeddings.` 后者也是 P1-04 可用的直接不共享证据。
4. **§2.2 / Figure 1**：同论文参数计数的最优前沿 Byte 更好；同训练 FLOPs 的最优前沿 Subword 始终更好，限所测范围/配方。
5. **A.4 / C.2 Eq.(11)**：参数 `N` 是 unique active parameters，含输出表但不含输入/哈希表；FLOPs 另计全注意力和 Gated DeltaNet 循环运算，排除 lookup、hash、bag averaging、loss、optimizer。不是所有部署存储参数或全系统耗时。

### 可直接采用

**中央 work 主干字段：**

> Resolution-preserving, non-hierarchical hybrid-attention backbone following the Qwen3.5 text architecture, with Gated DeltaNet and Gated Softmax Attention in a 3:1 layer ratio. The byte recipe additionally uses early four-byte token-superposition training, hashed n-gram inputs and a wider Gated DeltaNet convolution. Input and output embeddings are untied according to Appendix A.4.

**作者段落：**

> W0356 is a flat model in the sense that it does not impose an explicit local–global–local hierarchy; it is not a pure full-softmax-attention control. Its hybrid recurrent/attention backbone preserves byte resolution after the initial grouped-training phase. The reported byte advantage at the parameter-optimal frontier coexists with a subword advantage throughout the evaluated training-FLOP-optimal frontier, under the paper's stated parameter and operation accounting.

中央分类至少分开 `resolution/hierarchy`、`sequence-mixing backbone`、`dense-or-MoE feedforward`、`training recipe`。原文 dense configuration 与 MoE configuration 对举，也不能据 dense 推定每层都做 softmax 全注意力。这个修订**不抹掉负结果**，也不把 W0356 的全部观察重新归因为 Gated DeltaNet；代码/消融未支持这样的因果拆分。

## 3. P1-03 — S08-R060 的综合关系与两篇原子记录

### 回查定位

- [S08 inventory:89 / R060](../01_discovery/S08/PROBLEM_SOLUTION_TECHNIQUE_INVENTORY.md) 同时引用流内 **W34 = 全局 W0518 TokSuite** 和 **W16 = Tokenization and Representation Biases in Multilingual Models on Dialectal NLP Tasks**。
- [S08 WORKS:47,65](../01_discovery/S08/WORKS.md) 明确二者身份与不同单位/任务；R060 自己已标记 pairing 为分析者综合。不是伪造共同实验，而是中央问题记录的粒度不合 PLAN。
- TokSuite 的 [旧 W0518 卡:4,7,14](../../flued_multigranularity_survey_20261108/03_reading/B22/W0518.md) 与本轮直接读到的 [v2 §3.3 / G.2](https://arxiv.org/html/2512.20757v2#A7.SS2) 一致：主实验同 token 不同原文；同文子集为 **Llama-3.2、Gemma-2、Comma、Qwen-3**，不含 ByT5。G.2 承认每语 token 数不受控、采样带来批次顺序细微差异。不是十四模型严格同文/同 FLOPs。
- 方言论文 **没有本轮发现的可复用旧 FULL 卡**；本轮视觉核 [EMNLP 2025 正式 PDF](https://aclanthology.org/2025.emnlp-main.1224.pdf) **p.23995 / PDF第4页 §4.1、p.23997 / 第6页 §5.2**。解码器用四位量化 LoRA（低秩适配：训练低秩增量而非全部权重），编码器全量微调；任务和适配预算不同。

§5.2 的具体反例是：**mBERT 与 Phi-3.5 的 tokenization parity（以英语为参照的词元长度比）和方言识别表现为正相关**，也就是更高相对碎片化对应更好表现；Llama-3.2 才呈预期负相关，且其该任务表现较低。Phi-3.5 上 information parity 与方言识别又为相反于预期的关系。这里是作者的 Pearson 相关分析，不是字节模型实验，也不是随机操纵分词器的因果结论。本轮没有视觉核全部相关热图或 Appendix F Table 8，故不补造相关系数/显著性。

### 推荐处理：R060 退出问题计数，保留为综合链接

**综合关系文本，不计独立问题/实证效果：**

> Training-exposure controls and downstream parity analyses address different validity questions. Link TokSuite's text-budget control to the dialect study's task-dependent correlation analysis; this connection is the survey authors' synthesis, not a joint experiment or an additional work.

**TokSuite 原子内容，优先链接/合并已有 S05-040、S06-R043：**

> Problem: Equal training-token budgets expose tokenizer variants to unequal amounts of source text. Solution: Reconstruct a common training-text stream for a four-tokenizer subset and adjust training duration. Evidence: TokSuite v2 §3.3 and G.2; the subset excludes the ByT5 tokenizer and does not equalize training FLOPs.

**方言研究独立原子内容，中央去重后再发 ID：**

> Problem: Token-length parity is not a task-independent predictor of downstream quality. Solution: Measure tokenization/information parity and correlate each with separately fine-tuned dialect identification, topic classification and extractive QA performance. Evidence: the dialect study §4.1/§5.2; the sign reverses for dialect identification in mBERT and Phi-3.5. This is an association across settings with different pretraining and adaptation, not an isolated tokenizer intervention.

不直接把 S08 的60改61：预算内容已在跨流出现，综合关系的退出和方言原子记录的加入都要经过中央语义去重。原始 discovery 计数可以留作历史，不冒充中央净计数。R060 的显示 glyph 说明也不是此新原子记录的实验效果；若正文要展开“显示乱码与可逆 byte-BPE”的论证，另交 terra 对 §5.3 原例和具体 tokenizer 做核验，不用本轮未重看的图例充数。

## 4. P1-04 — 可用的直接字节共享轴，不再只有旧 Large 配置

### 应回连的流位置

[S04 WORKS §Configuration findings:49–55](../01_discovery/S04/WORKS.md)、[S04-R003:28–32 及末尾 T 类缺口](../01_discovery/S04/PROBLEM_SOLUTION_TECHNIQUE_INVENTORY.md)；跨流回连 **S02-026–027 / S03-R08（MEGABYTE）**、**S03-R25（LCA）**、**S06-R043 / S08-W34（TokSuite）**，并将 §2 新核到的 W0356 录入。S08-R060 只能作为迁出前的旧位置，不再当共享证据自身。

### 可直接录入的台账

| 模型/版本与实际接口 | 共享轴 | 当前可采用状态与原文定位 | 未证明的内容 |
|---|---|---|---|
| **MEGABYTE / W0008，2305.07185v2**；global fixed patches + local byte AR | **local byte input ↔ local output** | **论文规格 shared**。本轮直接读 §2.2 Eq.(4) 使用 `E_local-embed` 输入前一 byte；Eq.(6) 用同一矩阵作词表投影，形状 `V × D_L`。见 [原文](https://arxiv.org/html/2305.07185v2)。 | 不推出 global/local 两张输入表相同，或 global/local Transformer 层共享；未核实现/权重别名 |
| **TokSuite / W0518，2512.20757v2** 的 **ByT5-tokenizer arm**；因果 Llama 风格 LM | **输入表 ↔ 输出表** | **论文规格 untied**。本轮直接核 §3.3：十四臂均按 Lingua Llama-3.2-1B `untied embeddings` 配置；§3.1 包含 ByT5 tokenizer。见 [原文](https://arxiv.org/html/2512.20757v2)。 | 不是原始 ByT5 encoder–decoder；跨模型共享初始化也不等于训练时共享参数存储 |
| **LCA-MBP / W0015，2608.15454v2**；byte hierarchical LM | **next-byte head ↔ multi-byte head 的输出表** | **论文规格 shared**。本轮直接核 §3，紧接目标右移说明：`Both decoder heads share a single unembedding matrix.` 见 [原文](https://arxiv.org/html/2608.15454v2)。 | 不推出 byte input ↔ output 共享；也不证明两头 Transformer 子模块相同或采样精确 |
| **W0356，2610.05978v1**；3:1 hybrid byte LM | **输入表 ↔ 输出表** | **论文规格 untied**。本轮新增直接证据：Appendix A.4，明确 `untied input and output embeddings`。见 [原文](https://arxiv.org/html/2610.05978v1)。 | 不将其哈希表、looped Subword 跨深度共享或 MoE 专家共享混为词表 tying |
| **原始 ByT5-Large 的 XNLI operative gin**，从1M步 checkpoint 初始化 | **encoder input ↔ decoder input**；**decoder input ↔ softmax** | **旧卡限定静态配置证据：前者 shared、后者 untied**。本轮完整重读 [B08/W0351.md:21](../../flued_multigranularity_survey_20261108/03_reading/B08/W0351.md)，不冒称新抓 gin。 | 未认证论文运行依赖 commit、其它尺寸/移植版本或实际权重别名；保留旧证据层级 |

**可直接给作者的总结：**

> Direct byte models already provide both shared and unshared readout specifications. MEGABYTE reuses its local byte embedding matrix for local output projection, while TokSuite's causal byte arm and W0356 specify untied input/output embeddings. LCA instead shares one output matrix between two decoder heads. These examples establish distinct implementation choices, not a controlled finding that tying helps or hurts byte modeling.

台账最少保存 `work_id / actual_model_or_port / source_version / sharing_axis / state / evidence_level / exact_location / unknowns`。运行验证保持 unknown，不能用“论文有一条公式”升级为 tensor alias 实证。

审计提到的 HF ByT5-Small `main/config.json` 仍只是前一审计的动态配置旁证；本轮没有重新读取、固定 revision 或核类定义。不把它列为本轮新增证据，不将其 vocab_size=384 替换论文原始字节/特殊 ID 口径。旧 Large gin 的来源和后续窄核见 §7；此处没有“所有 ByT5 均如此”的结论。

## 5. P1-05 — TokSuite 的 BPB：PDF 措辞已核，Figure 6 实算仍未知

BPB 即 bits per byte（每原文字节的负对数概率，以 bit 为单位）；CE 即 cross-entropy（交叉熵，这里指有明确标签事件、掩码和平均分母的预测损失）。

### 5.1 源头与本轮实际进展

应挂工作级备注的位置：**S03-R47、S05-040、S06-R043–44、S08-W34 / 迁出前的 R060**。这些行本来的预算或任务结论不因工作级备注自动删除。[旧 B22/W0518.md](../../flued_multigranularity_survey_20261108/03_reading/B22/W0518.md) 的 FULL 标签记录了主要正文/附录阅读，但没有承载 C.2 此公式的检查；不能凭标签替它认证。

- **[v2 HTML C.2](https://arxiv.org/html/2512.20757v2#A3.SS2)**：本轮在页面上读到 `BPB normalizes the cross-entropy loss by log_2 |V|`。
- **[v2 PDF p.21，C.2 首段](https://arxiv.org/pdf/2512.20757v2)**：本轮视觉复核同样的 `log_2 |V|` 原句。故已排除“仅 HTML 抽取把正确 PDF 公式弄错”的解释；**没有排除论文写错但作图算对**。
- C.2 随后用相近 BPB 曲线说明模型 comparably well-trained，并将下游差异归于 tokenizer 而非 training stability/capabilities；在图的实际换算未核前，不采纳这一跨模型归因。即使 BPB 算对，相近密度损失本身也不保证各任务能力等同。

本轮沿论文公开仓库做到一个有界代码检查，而非止于摘要：论文链接的 `r-three/lingua` 的 `toksuite` 分支，访问时最新提交为 **[0db0ba5648a4fa4efae010a94f69fc1042a354aa](https://github.com/r-three/lingua/commit/0db0ba5648a4fa4efae010a94f69fc1042a354aa)**。只读了以下三文件的返回全文：

| 固定源码 | 定位与实际读到的东西 | 对 BPB 疑点的意义 |
|---|---|---|
| [apps/main/train.py](https://raw.githubusercontent.com/r-three/lingua/0db0ba5648a4fa4efae010a94f69fc1042a354aa/apps/main/train.py) | `train`：`loss = model(input_ids, labels)`；梯度累计缩放后，日志恢复 loss，并写 `to_sync["loss/out"] = loss.item()` | 所查日志路径记录模型损失，没有在这里进行原文字节换算；不是 Figure 6 后处理认证 |
| [apps/main/transformer.py](https://raw.githubusercontent.com/r-three/lingua/0db0ba5648a4fa4efae010a94f69fc1042a354aa/apps/main/transformer.py) | `LMTransformer.forward`：`return cross_entropy(logits, target)`；`LMTransformerArgs.weight_tying=False`，构造时可切换 tied/untied | 明确 loss 调用来源；默认配置不是已运行 checkpoint 的别名核验 |
| [lingua/transformer.py](https://raw.githubusercontent.com/r-three/lingua/0db0ba5648a4fa4efae010a94f69fc1042a354aa/lingua/transformer.py) | `cross_entropy`：`F.nll_loss(F.log_softmax(...float(), -1), target.flatten(...), **kwargs)` | 所查基本损失是自然对数的 token 平均；此函数不等于 BPB，也未看到在此除 `log_2 |V|` |

没有定位 Figure 6 绘图脚本、原日志和当年运行 commit 的对应关系。**不能从这三文件没有该除法，推出全仓没有该除法；不能把当前公开 commit 当成论文执行版本。** 固定源码给 terra 一个可复用调用入口，不构成已查明实现错误的结论。

### 5.2 正确换算与适用条件

设同一受评文本的原始 UTF-8 字节数为 `B`，实际被评分的因果标签事件为 `e_1,...,e_N`，其概率在各自合法可见上下文 `c_i` 下计算。对这些事件的记账分数：

```text
L_nats = - Σ_i ln q(e_i | c_i)
BPB_event = L_nats / (B ln 2)
         = CE_mean_nats × N / (B ln 2)
```

这里的 `N` 必须是 CE 真正平均的**有效标签数**，不是包含 padding、未评分 prompt 或重复窗口的数组总长；若 CE 已按 bit 计则不再除 `ln 2`。有不同权重/平滑/辅助目标的训练损失不能不经还原当成观察文本的 NLL。跨样本要先聚合 loss 总和与对应 byte 总数，不能随意平均不同长度样本的 BPB。

`log_2 |V|` 不是原文字节数，也不是 token→byte 的倍率。若对以 bit 计的 CE 除此值，得到的是相对均匀词表预测上限的尺度，而非 BPB；例如均匀256-byte模型应为8 BPB，`8 / log_2 256 = 1` 并没有每 byte 8 bit 的正确单位。

采用上述分母还需把**概率对象**说清：

1. **原生逐 byte 链**：无有损文本变换、每个所评分 byte 恰计一次时，链上的 NLL/原 byte 数可给出相应 byte 序列或续文事件的 BPB。完整字符串是否另含 EOS、有限上下文怎样截断、prompt 是否只条件不计分，应显式记录。
2. **规范 token 路径**：对确定分词 `t(x)` 的 `-log q(t(x))/B` 是该路径的 byte-normalized 编码分数。它可以作为明示口径的路径分数使用，但**除 byte 数并不会把它变成所有可解码为 x 的路径概率之和**。
3. **文本边缘概率或原始 byte 前缀条件概率**：前者须明确合法路径、终止事件与求和，后者须对任意部分-token前缀正确条件化；两者不能只靠更换分母获得。相关证明/算法仍交 terra。
4. **有损 normalization / UNK 替换**：若模型其实给变换后字符串评分，不能直接称原始字符串精确概率；需要说明变换的原像/丢失信息及任务权限。原始 byte 分母可用于透明成本记账，但不能恢复被删的概率事件。
5. **公平性**：相同 BPB 单位不自动匹配训练原文、各语保留量、原文上下文、总参数、训练 FLOPs 或推理成本。必须另列这些预算。

### 5.3 不把 C.2、选择题和精确 byte 算法混成一个结论

本轮直接读到 **[Appendix F 首段及 Exact Byte-Level Probabilities 小节](https://arxiv.org/html/2512.20757v2#A6)**：主要评估把每个选项当 context continuation，以 **byte-length-normalized log-likelihood** 评分；大多数扰动改输入、选项不变。这是选项排序协议，不是 C.2 的训练曲线公式，也不是已证明的全路径文本边缘概率。

F 的额外精确 byte 评估只对 **Gemma-2-tokenizer 模型**执行，受公开实现对 SentencePiece/空格分隔和非拉丁语种的限制；40例需数小时，对照标准评估数分钟；作者报告扰动表现改善但 canonical 正确率下降。本文核了这些**文字范围**，未重核全部 Table 20–21 数值或算法证明。不要把这一额外评估扩大为十四模型的精确 byte 评分，更不能由 C.2 单位措辞直接宣布 Table 1、G.2 或所有鲁棒结论无效。

**可直接采用的中央备注：**

> TokSuite v2 Appendix C.2 (PDF p.21) describes BPB as cross-entropy divided by log₂|V|, which is not a general conversion to bits per original UTF-8 byte. The same wording occurs in HTML and PDF. The released trainer path inspected at commit 0db0ba5 logs token cross-entropy, but the Figure 6 transformation and its link to the paper's runs remain unverified. Do not use that figure to certify cross-tokenizer BPB equality or equal training sufficiency until the original log-to-figure pipeline is checked. This issue does not by itself invalidate the separately defined multiple-choice evaluation or its four-tokenizer text-budget control.

## 6. P1-06 — 核心选读缺口不以局部机制纠正结案

审计是七流初审且明确没审 S02。本轮只读取了 S02 的相关机制记录 **013–019、026–027** 及其选读交接，不能把“现在找到 S02 PARTIAL”写成先前审计漏掉完整卡，更不能称本轮已全面审完 S02。

跨流需合并的精确记录/队列：

| 原始作品 | 对应记录与旧卡状态 | 本轮原文核到的身份，可先用于分类 | 全文缺口仍在哪里 |
|---|---|---|---|
| **W0004 CANINE，2103.06874v4** | S01-R34–35；S02-013–014；S07-R08；S01 handoff第5项 / S02第5项 / S07第7项；没有此次查到的独立旧 FULL 卡 | [§3.1–3.2.1](https://arxiv.org/html/2103.06874v4)：输入 Unicode codepoints，多哈希嵌入，局部注意力后 stride4 卷积；编码器，不是原始 byte 因果生成器；两类 masked supervision 分开 | 全部实验/关键表图、C/S与 n-gram 消融、真实速度与数据条件、相关附录，以及 headline 版本/指标差异 |
| **W0005 Charformer，2106.12672v3** | S01-R36；S02-015–016；S07-R09；S06 handoff第6项；没有此次查到的独立旧 FULL 卡 | [v3 §2.1.1–2.1.5 / §2.2](https://arxiv.org/html/2106.12672v3)：候选块 mean pooling、逐位置评分/软混合、最后固定 stride 降采样；不是已证明的可变长度硬分区 | v3完整实验/速度口径、输出监督单位、可见上下文/校准、tall模型预算、关键图表及附录。**本轮v3 HTML成功访问，不等于已完成v2→v3全版本比较** |
| **W0006 MANTa，2212.07284v1** | S01-R37；S02-017–019；S07-R10；S06 handoff第9项；没有此次查到的独立旧 FULL 卡 | [§3.1–3.2.1](https://arxiv.org/html/2212.07284v1)：局部 Transformer 预测frontier概率；Gaussian近似byte-block分配、加权卷积/max pooling；K=4硬长度截断施压；输出仍是 byte/sentinel AR span reconstruction | 完整§4–6、速度/同文或同时间预算、无截断退化消融、各类噪声/OOD负例、Appendices A–D；不能把只用LM loss说成没有额外硬瓶颈 |

**可给作者的覆盖说明：**

> The early encoder-side routes are structurally distinct: CANINE compresses codepoint representations, Charformer learns soft block preferences before fixed-rate downsampling, and MANTa learns soft explicit byte-block assignments subject to a hard length bottleneck. Their presence in the inventory establishes coverage of mechanisms, not completion of the original experiments, budgets or appendices. Selected full readings remain necessary before detailed cross-route comparisons.

[ByteNet / S01-H07](../01_discovery/S01/WORKS.md) 仍主要是摘要级字符先行工作；“ByteNet”名称不解决实际字母表、码点/byte与解码掩码。历史压缩及非神经概率分段也不因这三篇机制补正而齐备。此处不补造全文认证或领域完整率。

## 7. 必须交 terra 的问题、具体来源与关闭证据

以下是交接任务，**没有在本轮启动代理或新增全文名额统计**。中央负责人应先与既有 S 流队列去重；同一作品一份完整卡回连所有记录。窄核与完整阅读分开，不为了新增 FULL 重读已经足够的旧论文。

| 优先与类型 | 必须回答的问题 | 具体来源/范围 | 可以关闭什么，不能替代什么 |
|---|---|---|---|
| **T1 / 最高，TokSuite定点证据链** | Figure 6究竟从哪个run、哪个commit、哪个loss字段作图？CE基底、有效token数、每原文byte数、EOS/PAD、重复曝光、语言混合如何计？除log₂V是论文勘误还是实算？ | [2512.20757v2 PDF p.21 C.2 / Figure 6](https://arxiv.org/pdf/2512.20757v2)；本文§5固定commit的三文件；论文链接仓库 [r-three/TokSuite](https://github.com/r-three/TokSuite) 与 [r-three/lingua toksuite](https://github.com/r-three/lingua/tree/toksuite) 的作图/评估入口。需定位真实生成脚本和原日志，不执行训练 | 交付实际公式、字段及run→figure映射；仅有正确新公式或新示例不能认证作者原图。若资源未公开，明确留未知，并把跨tokenizer等BPB论据留出 |
| **T2 / ByT5窄配置核** | 将encoder/decoder输入共享、decoder输入/output共享、类定义、port和版本逐一锁定；不要把Large/XNLI推为所有尺寸 | [Large operative gin](https://storage.googleapis.com/t5-data/pretrained_models/byt5/large/operative_config.gin)；[旧卡:21](../../flued_multigranularity_survey_20261108/03_reading/B08/W0351.md) 中固定Mesh定义；官方 [HF Small config候选入口](https://huggingface.co/google/byt5-small/blob/main/config.json)，必须另锁revision再读类定义 | 只能新增相应版本的配置/代码结论；未检查checkpoint时runtime unknown。本轮未重新访问gin/HF，不把前轮失败冒充本轮失败 |
| **T3 / 核心完整阅读** | CANINE的C/S监督、hash/stride/up选项、真实速度/原文预算与headline差异 | [2103.06874v4 PDF](https://arxiv.org/pdf/2103.06874v4)，完整方法/实验/关键表图/Appendix；并按S01 handoff核正式身份/版本差别 | 关闭W0004全读缺口，回连S01/S02/S07；不冒充因果byte LM证据 |
| **T4 / 核心完整阅读** | Charformer的GBST软混合、固定降采样、校准可见范围、byte输出、速度分母、scaled架构与v2→v3差异 | [2106.12672v3 PDF](https://arxiv.org/pdf/2106.12672v3)；§2–4及相关Appendix，与S02已用v2机制相对照 | 关闭W0005全读缺口；本轮读v3方法不足以关闭实验/附录 |
| **T5 / 核心完整阅读** | MANTa的近似分配、硬截断作用、无截断负例、梯度与byte decoder瓶颈、同时间/同数据比较 | [2212.07284v1 PDF](https://arxiv.org/pdf/2212.07284v1)，§3–6，全部关键表图，Appendices A–D | 关闭W0006全读缺口；不可仅用摘要的“end-to-end”代替约束说明 |
| **T6 / 合并现有全文队列，MEGABYTE** | local tying是哪些发布实现实际采用？普通/strided BPB、双层shift、部分prompt、EOS和语言生成速度预算如何对应？ | [2305.07185v2 PDF](https://arxiv.org/pdf/2305.07185v2)，§2 Eq.(4–6)、§3、完整实验/相关附录及对应官方实现；S02/S03/S06既有队列 | 本轮足够登记local共享论文规格；完整实验/实现仍缺，不为这一个公式重复发第二份完整阅读 |
| **T7 / 合并现有全文队列，LCA** | 两头共享unembedding之外，MBP的tensor/target依赖、组内条件独立、阈值与verification、缓存条件和参数预算到底是什么？ | [2608.15454v2 PDF](https://arxiv.org/pdf/2608.15454v2)，§2–3、Algorithm1/Figs1–2、全部结果、Appendix A/B；S03-R25–27与S06 handoff第5项 | 共享输出表规格可先用，不能代替概率分解/精确采样证明或服务速度认证 |
| **T8 / 方言研究完整/关键表补读** | TP/IP和各任务的相关系数、样本/显著性、预训练与LoRA/FFT预算、§5.3显示glyph的真实含义如何区分？ | [2025.emnlp-main.1224.pdf](https://aclanthology.org/2025.emnlp-main.1224.pdf)，§3–5、Figure5、Appendix E/F Table8及相关原例；S08-W16为PARTIAL且无本轮查到旧FULL | 关闭原子方言记录的定量/适配细节；不把该相关性和TokSuite合成一项实证 |
| **T9 / 概率方法完整阅读，若采用精确性结论则必做** | 规范token路径、完成字符串边缘概率、任意raw-byte prefix条件概率在何假设下相同/不同？normalization与非规范路径、EOS质量如何处理？ | [Exact Byte-Level Probabilities… 2410.09303v2](https://arxiv.org/pdf/2410.09303v2)，§3–4及证明附录；[EMNLP2021 marginal likelihood](https://aclanthology.org/2021.emnlp-main.161.pdf)，§2/实验/估计器；TokSuite Appendix F只作调用方观察 | 回连S03-N16/N05与S08概率记录；不得以TokSuite F的二手方法介绍认证上游定理。这是两篇、不同概率问题，中央应保留各自卡 |
| **T10 / 历史覆盖，正文若展开则必做** | ByteNet的各实验真实字母表/编码、encoder/decoder掩码、感受野、线性复杂度与实测预算是什么？ | [1610.10099v2 PDF](https://arxiv.org/pdf/1610.10099v2)，完整方法/实验及相关附录；S01-H07目前摘要级 | 没读完就保持字符先行工作/范围缺口；不能靠名字升级成通用UTF-8 byte LM |

### 本轮来源账与验证边界

- **9篇原始论文的实际定点阅读**：ByT5正式PDF Table10/§7；W0356 v1 §1/2.1/2.2、A.4/C.2；TokSuite v2 §3.1/3.3、C.2 HTML及PDF p.21、F/G.2文字；MEGABYTE v2 §2.2 Eq.(4–6)与相邻方法；LCA v2 §3；方言论文正式PDF §4.1/5.2；CANINE v4 §3.1–3.2.1；Charformer v3 §2.1–2.2；MANTa v1 §3.1–3.2.1。返回材料中其它段落的可见存在不等于全部实读。上表仅作为未来任务给出的PDF/代码/配置入口，不一律计本轮已访问。
- **4张旧卡实际完整读取**：B08/W0351、B08/W0360、B14/W0356、B22/W0518；路径均已在对应段落给出。没有把旧FULL加到新FULL数。
- **源码只读固定3文件**，符号定位见§5.1。没有全仓搜索认证、没有权重下载/执行、没有作图重算。没有主动下载转换中间文件；浏览器自动截图缓存不是交付来源。
- 联网只用内置浏览器访问公开论文与论文所链公开代码；没有上传内部材料、调用付费源或登录墙。若截图渲染超时，只重试一次；一次控制失效后重新激活自己的标签成功，没有持续争抢。新建并复用的唯一标签 `panel-tab-1900` 已成功关闭；未动原有标签。
- 交付为Markdown，不涉及可执行代码，故不运行build/pytest或训练。交付检查只做本文件UTF-8、六项P1/十项terra任务、相对链接存在性与git状态观察；这不是论文事实的自动证明，也不证明中央作者已采用全部修订。

**最终状态：六项P1均有可采用的修订表述和定位；原子记录/共享规格的证据已补，TokSuite已把疑点推进到PDF与固定源码入口，但图的实际换算尚未关闭；核心选读仍交terra。没有全面复核、全文完成或所有问题已关闭的宣称。**
