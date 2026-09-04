# 撞车侦察报告：需求锻造（Demand Forging）三候选形态

- 日期：2026-09-04（E120 验尸后第七季立项前置侦察，协议 5「撞车侦察先行」）
- 范围：甲「跨段续尾」损失重加权 / 乙「实体重命名」数据增强 / 丙配套「权重衰减反记忆化」/ 丁「需求侧总谱系」
- 方法：全程 WebSearch + FetchURL 外部检索，未读本地代码
- 项目代号背景：FLUED（MENTINER 镜像侧别名），~50M 字节级 encoder，六代攻法（E120 止）均为「造必须查内部状态黑板的需求」形态

---

## 甲：「跨段续尾」损失重加权（离线扫稀有串重现位 → 损失加价）

**① 撞车判定：空档确认。** 无同名/同构直接命中。按「语料级稀有 + 跨段重现 → 结构化 lookup 需求」为计价标准的损失重加权未检索到先例。最近邻按距离排序：
- RHO-1 / Selective Language Modeling（Lin et al., NeurIPS 2024）：token 级损失筛选/重加权，但目标为效率与质量（剔除低价值 token），不是制造检索需求，且计价用参考模型损失非语料级稀有度。
- Goldfish Loss（Hans et al., 2024）：丢弃部分 token 的损失防逐字记忆——与甲**反方向**（压记忆而非逼查询），但其存在证明「改损失计价即可操纵记忆/查询行为」这条杠杆被文献承认。
- Chan et al. 2022（burstiness 驱动 in-context learning）：同目标（诱导 induction/上下文回看），但走**数据分布侧**（让事件聚簇），非损失计价侧。
- Bietti et al. 2023「Birth of a Transformer」（bigram→induction 理论谱系）、Bratulić et al. 2026（自然数据分布性质→induction head 形成的实证），说明「重现结构→induction 形
成」因果链已被理论与实证双向确认——给甲的机制假设提供了外部支点。

**② 近 12 个月走向：** token 级重加权活跃但动机全在效率/质量/遗忘三处（RHO-1 后续 SelecTKD 2025、ENT 梯度截断、LLM unlearning 损失重加权 Yang et al. ICML 2025），无一家以「锻造检索需求、强迫状态消费」为目标。

**③ 差异点一句话：** 甲的计价单位是「目标字节延续的是前文出现且语料级稀有的串」（跨文档重复→必须回看），而非参考模型惊喜度；目的态是状态消费而非数据效率，属「需求侧定价」空档。

**④ 关键引文：**
- RHO-1: Not All Tokens Are What You Need, 2024, https://arxiv.org/abs/2404.07965
- Be like a Goldfish, Don't Memorize!, 2024, https://arxiv.org/abs/2406.10209
- Data Distributional Properties Drive Emergent In-Context Learning in Transformers (Chan et al.), NeurIPS 2022, https://arxiv.org/abs/2205.05055
- Exploring Criteria of Loss Reweighting to Enhance LLM Unlearning, ICML 2025, https://arxiv.org/abs/2505.11953
- Unlocking In-Context Learning for Natural Datasets Across Modalities (Bratulić et al.), IJCV 2026, https://link.springer.com/article/10.1007/s11263-026-02913-0

**附：「fable5 的损失重加权路线」查证 —— 未能定位为文献。** 检索无任何以此为题的论文。旁证显示 **Claude Fable 5 是 Anthropic 2026-06-09 发布的模型代号**（API model 名 `claude-fable-5`；Mythos 5 的公开版，[Simon Willison 评测](https://simonwillison.net/2026/Jun/9/claude-fable-5/)、[Infosecurity 报道](https://www.infosecurity-magazine.com/news/fable-5-mythos-class-anthropic/)）。「fable5 路线」极可能是与该模型协作时 AI 给出的内部建议，不是可引用的工作——立项文档中不应作为文献引用。

---

## 乙：「实体重命名」数据增强（每采样替换专名为随机串）

**① 撞车判定：同构撞车（高严重度，需改造）。** 命中一篇直接同构工作：
- **KLLM — Knowledgeless Language Models: Suppressing Parametric Recall for Evidence-Grounded Language Modeling**（Cohen et al., 2026-07, https://arxiv.org/abs/2607.12831）：**预训练期**把语料中命名实体匿名化为占位 token，切断实体级事实监督，显著降低闭卷事实回忆、提升上下文问答/事实核验/幻觉检测，多模型规模验证。这就是「Chan et al. 动态标签线的预训练期自然语料版」本体。
- 次近邻：Env-DocRED「entity variation robust training」（Meng et al., 2024, https://arxiv.org/abs/2406.07444）——每文档把实体名换成 Wikidata 名，机制同构（文档级换名增强），但目标仅 DocRE 鲁棒性、fine-tune 层面，非预训练期。
- 理论锚确认：Chan et al. 2022（NeurIPS 2022）即为用户所指「动态标签线」出处，作者为 DeepMind 系（Chan, Santoro, Lampinen, Wang, Singh, Richemond, McClelland, Hill），用合成数据证明 burstiness/低频簇属性驱动 ICL 与 induction 行为。

**② 近 12 个月走向：** 该方向正从「评估侧」（换名鲁棒性 benchmark，2024）升级到「预训练干预侧」（KLLM，2026-07 刚落地），窗口在被占；另有 ICLR 2025「Toward Understanding In-context vs. In-weight Learning」（Bryan Chan et al., https://arxiv.org/abs/2410.23042）把 in-context/in-weight 切换的理论框架铺好。

**③ 差异点一句话：** KLLM 用**固定占位符**抹平实体（目标是去知识、接地可靠性），我们是**每次采样随机串**、保留字形/字节结构、迫使模型做「上下文内新绑定→状态回看」，考核终点是内部状态消费与边界压缩行为，不是闭卷 QA 的接地可靠性——机制同构、目的态不同，但立项文档必须原地引用 KLLM 并显式切分，否则必撞。

**④ 关键引文：**
- KLLM, 2026, https://arxiv.org/abs/2607.12831
- Env-DocRED / entity variation robust training, 2024, https://arxiv.org/abs/2406.07444
- Chan et al., NeurIPS 2022, https://arxiv.org/abs/2205.05055
- Toward Understanding In-context vs. In-weight Learning (B. Chan et al.), ICLR 2025, https://arxiv.org/abs/2410.23042
- Dual Process Learning: Controlling use of in-context vs. in-weights strategies (Anand et al.), https://arxiv.org/abs/2305.16704

---

## 丙配套：权重衰减反记忆化（「Singh 2023 唯一实证有效」）

**① 撞车判定：出处未能定位 + 引用强度过言。** 多角度检索（author+主题、grokking 谱系、2023 NeurIPS/ICLR）**未找到作者为 Singh 的 2023 年「weight decay 抑制记忆化」论文**；Aaditya K. Singh 是 Chan 2022 共同作者（DeepMind 系），疑为跨论文误挂。该论点的实际文献归属：
- **Omnigrok: Grokking Beyond Algorithmic Data**（Liu et al., ICLR 2023）：weight decay/weight norm 受控时 grokking 普遍发生——权重范数是记忆化→泛化相变的主驱动，这是「WD 反记忆化」的公认锚。
- **Grokking as the Transition from Lazy to Rich Training Dynamics**（Kumar et al., 2023/ICLR 2024）：权重衰减压力把优化器推出高范数记忆解。
- Nanda et al. 2023（Progress Measures for Grokking）提供机制侧进度计。
- 反面证据存在：Is Weight Norm Sufficient to Explain Delayed Generalization?（2023, https://arxiv.org/abs/2310.19470）主张好子网络比权重范数更重要；Andriushchenko et al. NeurIPS 2024（Why Do We Need Weight Decay in Modern Deep Learning?, https://arxiv.org/abs/2310.04415）显示现代 LM 中 WD 的作用微妙（特征学习侧）；Han et al. 2026「Weight Decay Improves LM Plasticity」（https://arxiv.org/abs/2602.11137）把 WD 的当代角色重述为可塑性而非反记忆。

**② 近 12 个月走向：** grokking 解释之争已从「weight norm 充分」退到「不充分、子网络更重要」，2026 年 WD 叙事转向 plasticity/持续学习，纯「反记忆化」主张在弱化。

**③ 差异点一句话：** 无立项差异——这是**引用校准问题**：「唯一实证有效」不成立（goldfish loss、遗忘式重加权等也是实证有效的去记忆化手段；且 WD 证据主要在小规模算法 grokking，LM 预训练尺度下反记忆实证薄弱），建议改挂 Omnigrok + Kumar et al. 并降格为「WD 是最常被复证的常驻辅助手段之一」。

**④ 关键引文：**
- Omnigrok, ICLR 2023, https://arxiv.org/abs/2205.12565
- Grokking as the Transition from Lazy to Rich Training Dynamics, https://arxiv.org/abs/2310.22395
- Progress Measures for Grokking via Mechanistic Interpretability, 2023, https://arxiv.org/abs/2301.05217
- Why Do We Need Weight Decay in Modern Deep Learning?, NeurIPS 2024, https://arxiv.org/abs/2310.04415

---

## 丁：需求侧总谱系

**① 出处勘误与基准确认：**
- **induction heads 相变锚出处勘误：实为 Anthropic，非 DeepMind。** In-context Learning and Induction Heads（Olsson, Elhage, Nanda et al., Transformer Circuits Thread, 2022, https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html）。立项文档引用需改挂。
- **MQAR/Zoology 确认：** Zoology: Measuring and Reproducing Recall in Efficient Language Models（Arora et al., 2023, Princeton, https://arxiv.org/abs/2310.04627）；「recall gap」表述已被 2026 年综述性论文当作标准背景（如 https://arxiv.org/abs/2603.20997）。
- **「训练期造检索需求迫使状态消费」直接同构：未检索到。** 但四条邻接线 2024-2026 同时收紧：① Repeat After Me（Jelassi et al., ICML 2024, https://arxiv.org/abs/2402.01032）——合成复制/召回需求任务判定架构差异；② Dual Process / B. Chan ICLR 2025——in-context vs in-weight 的控制与理论；③ KLLM 2026——预训练期抑制参数通道（见乙）；④ Procedural Pretraining（Jiang et al., 2026, https://arxiv.org/abs/2601.21725）与 To Memorize or to Retrieve: Scaling the Interaction Between Pretraining and Retrieval（2026, https://arxiv.org/abs/2604.00715）——合成/检索通道与参数通道的显式配比开始被 scaling 研究接管。

**② 近 12 个月走向：** 「参数化 vs 上下文」从解释性话题升级为**预训练期可控变量**（KLLM、procedural warm-up、pretraining-vs-retrieval scaling），需求侧锻造的空档正在收窄。

**③ 差异点一句话：** 把「检索需求」作为自然语料上的**损失/数据计价变量**并在**压缩边界（boundary compression）**上考核状态消费，未见面直接占位；但乙形态的一半已被 KLLM 占走，甲形态必须抢在 token 重加权社区转向需求侧之前落证据。

**④ 生存验证提醒（协议 5）：** 上述全部近邻基准（MQAR、Repeat After Me、KLLM 的 QA 组）都在短窗或单跳召回上判词；本项目若开臂，长窗/多页考场必须先排。

---

## 总判（一行）

**甲可开臂**（空档确认，最近邻 RHO-1 属效率动机，预注册引 RHO-1+Chan2022 划界）；**乙需改造**（KLLM 2026-07 已占「预训练期实体匿名化抑制参数回忆」高地，必须以「随机串保留字形+每次采样重绑+状态消费考核」三点显式差异化，否则弃）；**丙建议弃作为立项主张**（仅引用校准：「Singh 2023」查无此文，改挂 Omnigrok/Kumar et al.，「唯一实证有效」降格为「最常复证的常驻辅助手段之一」）。
