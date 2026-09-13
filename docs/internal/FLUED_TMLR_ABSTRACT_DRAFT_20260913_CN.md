# TMLR 摘要初稿 v0（2026-09-13 晚，主会话起草，待用户终审）

> **口径纪律**：本稿只用三钉死件——体制无责（R2）、需求存在且可学（R2 未见窗同带）、仪器族正例会响（三态分辨）。**「墙在自创架构件」为工作假设**（2026-09-13 晚三审计降级），稿中仅以 working hypothesis + 在途验证形态出现；一切依赖 0.33 族读出数的句子未写入（冻结纪律）。
> **禁用措辞**遵守在册清单（无双零/结构性缺失/规模甜点/全档一致为正/读者类构造）；DeltaNet 活性表述全带规模×预算×体制限定；Kimi Linear ≈0 未引用（逃逸口原则，引用须带全限定句）。
> **死线**：9-15（用户最新口径）。

## 用料登记（每个数的出处）

| 料 | 数 | 出处 |
|---|---|---|
| 体制无责 | DeltaNet-50M × corpus_v3 × 4096B × 20K：必要性账池化 +0.1040 nat，CI95 [+0.0951, +0.1125] 排零 | R2 收官回执（2026-09-13，outputs/r2_deltanet50m_20260913/closing/） |
| 需求存在且可学 | 未见窗块（训练前缀外 30000-30499）+0.1055 [+0.0885, +0.1224]，与在训四块同带 | 同上 |
| 仪器阳性对照 | transformer-340M +0.3331 / DeltaNet-1.3B +0.2806（1.3B 为方向锚、规模差随行）/ 自家三基座 ≈0（E122 降级口径：排除 ≳0.04 nat 平均内容特异依赖） | E122/复证臂在册 |
| 机制（E124） | 硬预算门+定向需求四列阴性；对角护栏（model.py:1844 allowed\|diag_eye）自读旁路：99% 重建由对角自读承载、门选 8 行仅 +0.003 | E124 收官（2026-09-13） |

## 中文主版

**工作题**：体制无责——字节分段语言模型读出墙的跨架构定址

无 tokenizer 的边界压缩要求模型把字节流的内容「写入」循环状态、并在下游「读出」消费。内容消费是否真的发生、失败时墙在何处，历来缺乏端到端可测量的判别仪器。我们建立一组行为侧仪器族（必要性账：物理遮蔽源段、测量目标预测对源内容的特异依赖，bootstrap CI＋预注册门限），其阳性对照稳定会响：transformer-340M 测得 +0.333 nat、标准线性注意力 DeltaNet-1.3B（原体制，方向锚）+0.281 nat，而我们字节分段架构的三基座 ≈0（排除 ≳0.04 nat 的平均内容特异依赖）。随后我们固定语料、窗长、预算与仪器四轴、只换架构轴：标准 DeltaNet-50M 从零训练于我们的体制，发展出统计显著的内容消费（+0.104 nat，CI95 [0.095, 0.113]），且在训练从未见过的窗块上同带成立——语料中确实存在可学的跨段依赖，而体制（数据/窗/预算/仪器）不阻挡标准线性注意力架构学会消费状态内容，体制无责。对偶地，在自家架构上，硬预算检索门＋定向需求双压仍教不会读出；仪器审计把病灶定位到读出结构里一条结构性「自读旁路」（对角护栏）：重建 99% 由零寻址成本的自读承载，检索需求根本到不了检索通道。两组结果合流，把墙的位置从「线性注意力形式之罪」与「训练体制之罪」收窄钉到自创读出件的具体结构（工作假设，组件级移植实验在途）——一个阴性结果由此转为可证伪的、组件粒度的研究纲领。

## English version

**Working title**: *The Regime Is Innocent: Cross-Architecture Attribution Localizes the Readout Wall in Byte-Segmented Language Models*

Tokenizer-free boundary compression requires a model to write byte-stream content into a recurrent state and read it back downstream. Whether such content consumption actually develops—and where it fails when it fails—has lacked end-to-end behavioral instruments. We build a behavioral instrument family (necessity accounts: physically masking source segments and measuring content-specific dependence of target predictions, with bootstrap CIs and pre-registered thresholds) whose positive controls ring reliably: a 340M transformer reads +0.333 nat and a standard linear-attention DeltaNet-1.3B (its native regime; directional anchor) +0.281 nat, while three bases of our byte-segmented architecture sit at ≈0 (excluding ≳0.04 nat average content-specific dependence). Holding corpus, windowing, budget, and instruments fixed and swapping only the architecture axis, we find that a standard DeltaNet-50M trained from scratch in our regime develops significant content consumption (+0.104 nat, CI95 [0.095, 0.113]), with the effect equally strong on windows never seen during training—the corpus does carry learnable cross-segment demand, and the regime (data, window, budget, instrumentation) does not prevent a standard linear-attention architecture from learning to consume state content. Complementarily, on our own architecture, a hard-budget retrieval gate with directed demand still fails to train content readout; instrument audit localizes a structural self-read bypass (a diagonal guardrail): 99% of reconstruction is carried by zero-addressing-cost self-reads, so retrieval demand never reaches the retrieval channel. Together, these results narrow the wall's address from "the linear-attention form" or "the training regime" to specific structures of self-created readout components (a working hypothesis, under component-level transplant verification)—turning a negative result into a falsifiable, component-grained research program.

## 冻结句清单（本稿未写入，分解/移植回来前不得解冻）

1. 一切依赖 0.33 岭回归 / 0.4572 管线 / 0.6045 训练读出件 / 62% 写入的「存储无辜/内容活在状态里」句式。
2. 「墙在自创架构件」的断言式表述（只允许 working hypothesis + 在途验证形态，如上）。
3. Kimi Linear ≈0 的任何引用（逃逸口原则：引用必须带「混合架构整模测量混读者」全限定句，摘要篇幅不值得）。

## 待终审裁决点

1. 工作题两版取舍或另拟。
2. E124 自读旁路在摘要中的篇幅（当前一句；它是机制钩子但不是钉死三件之一，可删）。
3. DeltaNet-1.3B +0.281 在摘要里是否保留具体数值（现稿带「原体制/方向锚」限定随行；也可删数只留方向，进一步省限定词）。
