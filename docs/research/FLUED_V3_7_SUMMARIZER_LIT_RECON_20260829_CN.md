# FLUED v3.7 summarizer/读出/键塌缩文献撞车侦察报告

> 2026-08-29，按 AGENTS.md 协作协议规则 5（架构级臂开 GPU 前必出撞车侦察报告）。
> 侦察主题：**"变长段/块 → 固定槽向量压缩 + 槽读出供下游消费/重建"谱系全扫**——段→槽压缩器
> 家族、线性注意力/delta-rule 状态容量线、读出形式（单槽 vs 多槽/锐化/迭代）、写键几何塌缩
> 缓解、近 12 个月（2025-08 ~ 2026-08）走向。
> 对应痛点：E95（段尾字节不在 memory 行）、写键几何塌缩（E73–E78，μ_max≈0.417）、
> Q19 闭式探针台账（E114：桥损 0.63、decoder 对估计态 OOD 掉到明文水位 42%）、E115 读出
> 可学习性墙（闭式 ~0.33 vs SGD 平台 0.02–0.08）、多槽读出臂（M∈{1,4,8}）排队立项。
> 侦察方式：WebSearch + FetchURL 实时核实（arXiv 为主），全部引文附编号/URL，仅摘要可读的
> 逐条标注（§8）。

## 0. 与既有侦察报告的分工（去重声明）

- `COLLISION_SCOUT_FORK3_SUMMARIZER_FIDELITY_20260820_CN.md`：已覆盖 F2 辅助重建
  （Compressive Transformer/ICAE/SAC 线）、F1 容量扩容（率失真/VQ 坍缩/Perceiver 扫描）、
  F3 池化臂（PMA/Slot Attention 槽坍缩）——**本报告不复述，仅引用其裁定**。
- `COLLISION_SCOUT_S38_ARM_B_20260809_CN.md`：已覆盖残差第二状态线（RDN/HOLA/HAM/Q-Delta）
  与 delta 规则谱系骨架——本报告在其上补**状态容量 scaling 证据**与**读出形式**两个未扫维度。
- `COLLISION_SCOUT_S39_ARCHIVE_QUERY_20260810_CN.md`：已覆盖归档查询/档案馆线
  （Memorizing Transformers/Landmark/ARMT/ICAE 族压缩库存）——本报告不复述。
- `TOKENIZER_FREE_LM_LANDSCAPE_CN.md`：已覆盖 BLT/H-Net/Perceiver 血缘——BLT
  （arXiv:2412.09871，2024-12，字节潜在 Transformer：熵驱动动态分块）与 H-Net
  （arXiv:2507.07955，2025-07，层级网络：可微边界+分块压缩主干）此处仅作族谱锚点列出。

**本报告的新增侦察面**：① 状态容量（head_k×head_v、槽数相对 d_model）的公开 scaling 证据；
② 读出形式学（单槽 vs 多槽、锐化读出、非参数/迭代读出、cross-attention 读出失败模式）；
③ 写键塌缩/槽几何均匀性的缓解件清单；④ 谱系近 12 个月走向综合。

## 1. 代码口径确认（侦察对象真身）

以当前代码为准（`flued/v36/model.py` + `configs/canonical_v36.json` v36.8-20260817）：

- **summarizer = `DiTChunkSummarizer`**（model.py:360）：`summarizer_type: "dit"`，
  `summarizer_dit_layers: 2`。所谓 "one-shot DiT" 在此项目的真实所指 = `DiTStyleBlock`
  （定义在 `flued/v34/model.py:125`）：**双向（非因果）Transformer 块 + RoPE 注意力 +
  标量噪声条件注入 + DiT 式小值残差缩放**（attn_scale/ff_scale 初值 0.1，兼容未来多步扩散
  课程，但当前部署就是一次性前馈——"one-shot"即"只过一个时间步、不迭代"）。
- 结构流：chunk 的 byte 隐态（d_byte=384）→ 2 层 DiTStyleBlock（chunks 间并行独立）→
  池化（默认 masked mean；已有 qpool=4 位置锚查询臂 E100、poswmean 零参数对照）→
  FFN → **1 chunk → 1 条 d_mem=512 memory 行**。
- 读出：KDA 状态机（4 heads × head_k=128 × head_v=256，fla chunk_kda 核）串行消费
  memory 行，终态由 `readout_queries: 1`（k=1 单查询）读出，再经 backbone → decoder
  还原字节。
- 写键侧已有手术位：WriteHead 的 `to_k_center`/`to_k_whiten`（EMA 去均值/白化，E75/E76）、
  `pos_prior_keys`（固定随机位置先验键招募臂）、`split_trunk`（E79 K/V 双干）、
  `recurrence="gdn2"`（S39 擦除/写入门控解耦）。

**同构度校准**：FLUED 的"段→槽"是**学习边界 + 单槽 + 单向量（512 维）+ 串行 delta-rule
状态机消费**，与文献主流的"定长 token 段 → 多压缩 token → softmax 注意力读出"在
段长来源（学习 vs 固定）、槽数（1 vs 多）、读出载体（线性状态机 vs softmax KV）三轴上
全部错开——这是全篇撞车判定的总背景。

## 2. 段→槽压缩器家族（segment-to-slot compressors）

| 工作 | 编号+日期 | 核心机制 | 与我方 summarizer 同构度 | 可借鉴点 | 裁定 |
|---|---|---|---|---|---|
| **Gist tokens** | [2304.08467](https://arxiv.org/abs/2304.08467)（2023-04） | 段尾插 gist token，attention mask 强制信息流进 gist | 中：软注意力装箱同形；但 gist 走主干 softmax 通道、无独立压缩器 | mask 强制装箱的极简形态；S39 报告已警示 "gist" 同名异物 | 不撞（fork3/S39 已登记） |
| **AutoCompressor** | [2305.14788](https://arxiv.org/abs/2305.14788)（2023-05） | 每段产 summary vector，LM 目标训练 | 中 | LM 目标（而非重建）训压缩器的先例 | 不撞（fork3 已登记） |
| **ICAE**（In-context Autoencoder，上下文自编码器） | [2307.06945](https://arxiv.org/abs/2307.06945)（2023-07） | 冻结 LM 产 memory slot，AE+LM 双目标 | 中高：slot 压缩 + 重建目标 | AE 必要性消融；SAC 的反面质疑（fork3 §3 已详） | 不撞（fork3 已登记） |
| **Activation Beacon** | [2401.03462](https://arxiv.org/abs/2401.03462)（2024-01） | 逐段产 beacon token，KV 全程保留供读 | 中 | 压缩 token 与原始 KV **混合读出**的形态先例 | 不撞 |
| **COCOM** | [2407.09252](https://arxiv.org/abs/2407.09252)（2024-07） | RAG 语境单向量/少向量上下文压缩 | 中 | 压缩率-效用扫描口径 | 不撞（S39 已登记） |
| **LLMLingua 系** | LLMLingua [2310.05736](https://arxiv.org/abs/2310.05736)（2023-10，全文已核）/ LongLLMLingua [2310.06839](https://arxiv.org/abs/2310.06839)（2023-10）/ LLMLingua-2 [2403.12968](https://arxiv.org/abs/2403.12968)（2024-03） | **抽取式**压缩：小模型给 token 打分，删留不重组 | 低：抽取式不产新向量，与我方"编译式"（重编码成新表示）本质不同族 | LongLLMLingua 的"位置 bias 修正"与"question-aware 条件化压缩"与我方逐段条件化（E23）有精神同构 | 不撞（异族） |
| **Perceiver / IO / AR** | [2103.03206](https://arxiv.org/abs/2103.03206)（2021-03）/ [2107.14795](https://arxiv.org/abs/2107.14795)（2021-07）/ [2202.07765](https://arxiv.org/abs/2202.07765)（2022-02） | latent query cross-attention 瓶颈 | 高（机制件）：我方旧 ChunkSummarizer 就是 Perceiver 式 latent query | latent 数×宽度扫描范式；Tree Cross Attention 附录（[2309.17388](https://arxiv.org/abs/2309.17388)）的 copy 任务退化警示（fork3 已引） | 不撞（机制件无新颖性可挂） |
| **Slot Attention** | [2006.15055](https://arxiv.org/abs/2006.15055)（2020-06，NeurIPS'20） | 迭代竞争式槽绑定 | 中：竞争分配思想；视觉对象中心语境 | **槽坍缩（slot collapse）是已知失败模式**，缓解见 §5 | 不撞（风险文献） |
| **RMT**（Recurrent Memory Transformer） | [2204.11062](https://arxiv.org/abs/2204.11062)（2022-04） | 段间传 memory token，BPTT | 中 | 段间定长记忆载体的工程先例 | 不撞（S39 已登记 ARMT 支系） |
| **Memorizing Transformer** | [2203.08913](https://arxiv.org/abs/2203.08913)（2022-03） | 精确 KV 库存 + kNN 检索 | 低（精确库存非压缩） | 原文明文"梯度不回传外部记忆"——非可微读出的判例 | 不撞（S39 已登记） |
| **Landmark Attention** | [2305.16300](https://arxiv.org/abs/2305.16300)（2023-05） | landmark token 作块级语义键控 | 中 | 训练软选/推理硬检的双形态 | 不撞（S39 已登记） |
| **InfiniAttention** | [2404.07143](https://arxiv.org/abs/2404.07143)（2024-04，全文已核） | 段级压缩记忆（线性注意力式 delta 规则存储 KV）+ 局部 softmax 注意力门控混合读出 | **高**：压缩记忆 + 局部分段处理的双通道形态与我方"KDA 状态机 + 段处理"最像 | ① 其压缩记忆读出是**每 token 查询压缩 KV 态**（多查询、逐位置），我方是 k=1 终态单查询——我方读出形式的激进处；② 门控标量混合压缩/局部两路读出的平衡件 | 不撞（形态最近邻，差异在边界学习与读出粒度） |
| **Compressive Transformer** | [1911.05507](https://arxiv.org/abs/1911.05507)（2019-11） | 旧激活压成压缩记忆 + 辅助重建 | 高（精神祖先） | fork3 §3.1 已详 | 不撞 |

**小结**：压缩器家族在"定长 token 段→多压缩 token→softmax 读出"格子上拥挤，但**学习边界
byte 段→单向量→delta-rule 状态机**这一整列无占位。InfiniAttention 是机制最近邻，其读出
粒度（逐 token 查询压缩态）反衬我方 k=1 读出是本谱系中最激进的收缩。

## 3. 线性注意力/delta-rule 状态容量线

### 3.1 容量理论与 scaling 证据

| 工作 | 编号+日期 | 与本问题的相关点 | 关键内容 |
|---|---|---|---|
| **Fast Weight Programmers**（DeltaNet 理论原型） | [2102.11174](https://arxiv.org/abs/2102.11174)（2021-02，ICML'21） | 容量极限的首次实测 | 固定 d_key=64，**实测线性注意力可完美存储的不同键数 ≈ d_key 量级**，delta 规则显著优于纯加性写入——"可寻址容量 ~ 键维"是该谱系的定盘星 |
| **Zoology / MQAR**（Multi-Query Associative Recall，多查询联想回忆） | [2312.04927](https://arxiv.org/abs/2312.04927)（2023-12） | 状态尺寸-召回权衡的系统测量 | 次二次架构的召回质量随**状态尺寸**（而非参数量）单调；MQAR 自此成容量标准考场 |
| **Based** | [2402.18668](https://arxiv.org/abs/2402.18668)（2024-02） | 同上 | 线性注意力（大状态）+ 局部门控卷积（精确局部）的混合配方——**"全局压缩态管不精确全局、精确回忆靠旁路"是 2024 后的标准答案** |
| **Jelassi 等 "Repeat After Me"** | [2402.01032](https://arxiv.org/abs/2402.01032)（2024-02，ICML'24） | copying 上界理论 | 定长循环态模型的 copying 能力受**状态维度/序列长**比值约束；与我方 E44-E50 的"短窗冗余、长窗塌"判读一致（AGENTS.md 已记其为我方十条臂复证墙） |
| **GDN**（Gated DeltaNet） | [2412.06464](https://arxiv.org/abs/2412.06464)（2024-12，全文已核） | head 维度扫描 | 400M 消融：head dim 64→128→256 单调改善（Avg-PPL 28.31→27.35→27.13）——**状态维度相对 d_model 的公开 scaling 证据中最直接的一条** |
| **DeltaProduct** | [2502.10297](https://arxiv.org/abs/2502.10297)（2025-02） | 状态表达力 | 每 token 多步 Householder 形 delta 更新，提高状态转移的表达类——不改状态尺寸改"写入质量" |
| **KDA** | [2510.26692](https://arxiv.org/abs/2510.26692)（2025-10） | 我方主干直接上游 | 通道级衰减门控；本项目 interpreter 即此脉 |
| **Log-linear attention** | [2506.04761](https://arxiv.org/abs/2506.04761)（2025-06，仅摘要可读） | 层级记忆 | 对数级增长的层级记忆桶，介于定长态与全 KV 之间 |
| **OSDN** | [2605.13473](https://arxiv.org/abs/2605.13473)（2026-05，HTML 全文可读） | 写入步长精细化 | delta 规则的标量步长升级为**逐维对角预条件**（feature-wise 曲率感知）——直接对应"写入侧优化器升级"，与我方 WriteHead 手术线同向 |
| **KATA**（Kernelized Linear Attention with Symmetric Cones，对称锥核化线性注意力） | [2607.17419](https://arxiv.org/abs/2607.17419)（2026-07，HTML 全文可读） | **"capacity wall"措辞同位** | 标题即"Breaking the Capacity Wall"：用对称锥核扩大有效特征维；其 MQAR 表给出同状态尺寸（32768 维）下 GLA/DeltaNet/GDN/RWKV7 的逐档召回率（如 64 对键值时 DeltaNet 0.526/GDN 0.670）——**同状态尺寸下召回率远低于 1 的公开台账**，可作我方"容量墙"叙事的外部锚 |
| **RAM-Net** | [2602.11958](https://arxiv.org/abs/2602.11958)（2026-02） | 可寻址记忆 | 线性注意力 + 显式可寻址槽，MQAR 随总状态尺寸扫描 |
| **KLA**（Kalman Linear Attention） | [2602.10743](https://arxiv.org/abs/2602.10743)（2026-02） | 写入=贝叶斯滤波 | 把状态更新写成卡尔曼滤波，写入增益由不确定性驱动 |
| **Kaczmarz Linear Attention** | [2605.08587](https://arxiv.org/abs/2605.08587)（2026-05，仅摘要可读） | 写入=迭代投影 | 用 Kaczmarz 迭代（逐行投影解线性系统）替代 delta 规则 |
| **Memory by Design** | [2605.31163](https://arxiv.org/abs/2605.31163)（2026-05） | 概率化状态层 | 概率视角统一序列层设计（附录有 MQAR 细节） |
| **Palimpsa** | [2602.09075](https://arxiv.org/abs/2602.09075)（2026-02） | 覆写管理 | 显式学习"记/学/忘"三操作，MQAR 容量考场 |

### 3.2 判读

- **"可寻址容量 ≈ 键维（head_k），有效值容量 ≈ head_v"** 是该谱系从 2021 到 2026 一以贯之的
  定盘星；我方 4×128×256 状态对 32-256 段的容量问题，文献侧答案是"状态尺寸管下限、写入
  几何（键正交性）管达成率"——与 E73–E76 的实测判词（塌缩在 to_k 单层、键共线吃掉有效秩）
  方向完全一致。
- **改善路径已分化为三股**（§6 走向）：① 状态维度扩容（GDN head-dim 扫描、RAM-Net）；
  ② 写入规则升级（delta→GDN→OSDN 对角预条件→Kaczmarz→Kalman）；③ 读出/表达升级
  （KATA 核化、MesaNet 迭代解，见 §4）。**我方 Q18/Q19 的"闭式可达而 SGD 不可达"判词
  落在第三股，与 MesaNet 直接同源（§4.2）**。

## 4. 读出形式（readout form）

### 4.1 单槽 vs 多槽读出

- 压缩器家族（§2）几乎全员**多槽**：gist/beacon/summary 都是 M 个 token 级槽，softmax
  注意力逐查询消费；Perceiver 系的 latent 数 N 是一等扫描轴。
- delta-rule 谱系的"读出"是 q·S 单点查询，**多查询读出 = 多 q 对同一终态并行点积**，
  无文献专门扫描"读出查询数 k"——**k 作为独立容量轴在公开文献中无占位**；最近的对应物是
  InfiniAttention 的逐 token 读出（k=T 的极端）与我方 k=1（另一极端）。
- **M∈{1,4,8} 多槽读出臂的文献定位**：介于"Perceiver latent 数扫描"（softmax 语境）与
  "delta-rule 多点读出"（无人扫）之间——格子空置，可开；预注册应显式写明这一空档。

### 4.2 锐化读出（sharpened readout）

- **HOLA**（[2607.02303](https://arxiv.org/abs/2607.02303)，2026-07，摘要全文已核）：
  Hippocampal Linear Attention。delta-rule 压缩态之外保留有界精确 KV cache（按
  β·‖e‖ 写入残差准入），**读出侧用解耦的 RMSNorm-γ 把精确 KV 读出"锐化"成硬检索而非
  软平均**——这是"锐化读出"措辞在文献中的唯一明确占位。340M/15B 上 Wikitext PPL
  27.32→22.92，RULER 32k needle 大幅优于 GDN。
- **与我方的关系**：HOLA 的锐化作用于**精确库存**（cache 里是原样 KV），我方要锐化的是
  **压缩态读出**（态里只有叠加的记忆行）——HOLA 证明"读出侧一个归一化件可以把软平均变
  硬检索"，但前提是库存本身未压缩。对我方多槽读出臂的借鉴：读出 q 的尺度/温度是可设计的
  独立件（RMSNorm-γ 式解耦归一化），不必与写入键共用几何。

### 4.3 非参数/迭代读出

- **MesaNet**（[2506.05233](https://arxiv.org/abs/2506.05233)，2025-06/2026-06 v2，全文已核）：
  共轭梯度（CG）迭代读出。**核心同构点：把"从状态 S 读出 v"显式写成解正规方程
  argmin‖Sk−v‖² 的迭代求解**——这正是我方 Q19 用 ridge 回归（闭式解）做的事，MesaNet
  把它做成**层内可并行、可微的 CG 迭代**（推理时可按预算调步数）。序列建模任务上与
  MHA/RNN 竞争。
- mesa-optimization 理论源头：von Oswald 等 [2309.05858](https://arxiv.org/abs/2309.05858)
  （2023-09，揭示 Transformer 内部实现多步 mesa 优化）。
- **对 E115 可学习性墙的含义**：文献证据指向"**闭式解水平可以经由显式迭代结构达成**"
  （MesaNet 的 CG、Kaczmarz 的投影），而"靠普通前馈+SGD 隐式学出闭式解"恰是该谱系里
  没人声称做成的事——E115 的"SGD 摸不到闭式天花板"与文献证据不冲突，甚至互为印证：
  **要闭式水平，就把迭代结构造进读出器，而不是指望前馈学到它**。这是 Q20 及以后最直接的
  可借鉴设计。

### 4.4 cross-attention 读出的已知失败模式

- Perceiver 系：Tree Cross Attention 附录（2309.17388，fork3 已引）——latent 瓶颈上做
  copy 任务，任务难度升则性能急退；瓶颈形态（交叉注意力软写入/软读出）本身限速。
- Slot Attention 系：槽坍缩（多槽绑到同一对象/同一方向），见 §5。
- 上下文压缩界：500xCompressor 类高倍压缩在多查询 QA 上掉点（SAC 2510.08907 复现口径，
  fork3 已引）。
- **我方 decoder 对"估计出来的模糊 memory 行"分布外敏感（Q19 段 3，掉到明文水位 42%）
  的最近文献对应**：压缩界普遍只测"压缩表示→冻结下游"的单一桥，**"桥输出扰动→下游鲁棒
  性"的 OOD 剖面无人报告**——Q19 的三段损耗台账本身是空档贡献（同 fork3 对 E86/E89 的
  判词）。

## 5. 写键塌缩/槽几何均匀性的缓解件

| 缓解件 | 出处 | 机制 | 与我方适配度 |
|---|---|---|---|
| **DNC 使用向量/分配机制** | Graves et al., *Nature* 2016（[doi:10.1038/nature20101](https://www.nature.com/articles/nature20101)） | Differentiable Neural Computer（可微神经计算机）：维护逐槽 usage 向量，写入经"最少使用优先"的分配权重，free gate 显式释放——**从机制上惩罚集中写入** | 高：allocation 机制即"写入分散化"的可微原件；但 DNC 是槽式外存，我方是叠加态——需改造成"键空间使用量"形式 |
| **负载均衡辅助损失** | Switch Transformer [2101.03961](https://arxiv.org/abs/2101.03961)（2021-01） | MoE 路由的 load-balancing loss：鼓励路由均匀——**"辅助损失惩罚坍缩分配"的现代标准件** | 高：键空间的负载均衡损失（如键到码本的分配熵）可直写 |
| **对齐/均匀性损失** | Wang & Isola [2005.10242](https://arxiv.org/abs/2005.10242)（2020-05） | hypersphere 上的 alignment+uniformity 双损失；uniformity 直接惩罚表示聚集 | 中高：键归一化后加 uniformity 项是零新件方案 |
| **句向量白化** | Su et al. BERT-whitening [2103.15316](https://arxiv.org/abs/2103.15316)（2021-03） | 协方差白化修正各向异性 | **已在仓内**：我方 to_k_whiten（E75 手术队列）即此件的在线 EMA 版——文献背书已存在 |
| **Product Key Memory**（乘积键记忆） | Lample et al. [1907.05242](https://arxiv.org/abs/1907.05242)（2019-07） | 键 = 固定码本中选取，查询对码本打分——**"码本键"的经典先例** | 高：E74 手术队列里的"码本键"臂有现成工程形态（乘积分解降低打分成本） |
| **槽坍缩的 OT 缓解** | Zhang et al. MESH, [PMLR v202 zhang23ba](https://proceedings.mlr.press/v202/zhang23ba.html)（2023-07） | 把 slot attention 的 cross-attention 改成最优传输（OT）问题，打破对称性导致的 tie/坍缩 | 中：视觉槽语境；OT 归一化思想可移植到池化/读出分配 |
| **位置先验键** | ——（我方自造，pos_prior_keys） | 固定随机键按绝对段位分配 | 文献侧最近邻是 Landmark 的块级语义键控（2305.16300）与 RoPE 的相对位编码——**固定内容无关键表无直接占位，是我方自建件** |

**判读**：写键塌缩的缓解件在文献里是"杂货铺"状态——DNC allocation（机制）、MoE 负载均衡
（辅助损失）、uniformity/whitening（几何正则）、码本键（结构）四类都有，**但没有人在
delta-rule 线性注意力的写入键上系统对比过这四类**——E74–E78 的逐层定位+手术序列在文献
侧无同形工作，是空档。

## 6. 近 12 个月走向（2025-08 → 2026-08）

1. **delta-rule 谱系进入"写入规则精细化"密集期**：KDA（2510.26692，2025-10）→ GDN-2
   （2605.22791，擦除/写入门控解耦）→ OSDN（2605.13473，对角预条件）→ EDA（2606.26560，
   擦除地址解耦）→ Kaczmarz（2605.08587）/ KLA（2602.10743）。共同叙事：**把 delta 规则
   当在线优化器，逐件升级其步长/预条件/投影几何**。我方 WriteHead 手术线（to_k 去均值/
   白化、split_trunk）与 OSDN 的对角预条件在同一方向，但文献侧全部作用于 **token 级**写入，
   我方是**段级**写入——粒度错位仍在。
2. **"capacity wall"措辞被公开占用**（KATA 2607.17419，2026-07，标题直书 Breaking the
   Capacity Wall）——我方 E114 已退役"容量墙"措辞（改"可学习性墙"），文献走向支持这一
   退役：2026 年"capacity wall"在核化/扩容语境有主。
3. **读出侧升温**：MesaNet（CG 迭代读出，2506.05233 v2 2026-06）、HOLA（锐化读出+残差
   准入，2607.02303）、Q-Delta（2606.08804，读出残差回写）——**"状态有了怎么读"成为
   2026 年的活跃前线**，与我方 Q18/Q19/Q20 队列正面对齐；竞争烈度上升，宜加速占位。
4. **压缩表示界"去重建化"争论未决**（fork3 已详：SAC 2510.08907 vs ICAE）；prompt 压缩
   工程侧（LLMLingua 系）持续迭代但与我方异族。
5. **混合架构成为默认答案**（Based 开启、GDN 论文自带混合臂、HOLA 的"压缩态+精确缓存"
   双通道）——**纯定长态单通道架构在 2026 年已无辩护方**；我方 S39 档案馆线（gist+精确
   归档双通道）与该走向同构，是主流背书而非异端。

## 7. 撞车裁定汇总与差异点

### 7.1 逐侦察面裁定

| 侦察面 | 撞车？ | 最近邻 | 差异一句话 |
|---|---|---|---|
| 段→槽压缩（学习边界+单向量） | **不撞** | InfiniAttention、ICAE | 学习边界 byte 段→单向量→delta-rule 消费的三轴组合无占位 |
| 状态容量 scaling | 不撞（我方是消费者） | GDN head-dim 消融、Zoology、KATA MQAR 台账 | 文献扫的是架构级状态尺寸，我方要的是**固定架构下写入几何对达成率的剖面** |
| 多槽读出（k 扫描） | **不撞，格子空置** | Perceiver latent 扫描（异语境） | delta-rule 终态的读出查询数 k 作为独立容量轴无人扫 |
| 锐化读出 | 措辞有主（HOLA），机制不撞 | HOLA（2607.02303） | HOLA 锐化作用于精确库存，我方要锐化的是压缩叠加态 |
| 迭代/闭式读出 | **最近邻 MesaNet，不撞** | MesaNet（2506.05233） | MesaNet 把 CG 造进序列层内做在线回归；我方语境是"压缩 memory 行的下游读出器"——把迭代解造进**读出器**而非序列层 |
| 写键塌缩缓解 | **不撞，杂货铺无系统对比** | DNC allocation / Switch 负载均衡 / 码本键 | delta-rule 写入键上的四类缓解系统对比无占位 |
| E115 可学习性墙 | **不撞，互为印证** | mesa-optimization 族（2309.05858）、MesaNet | "前馈+SGD 学不到闭式读出、显式迭代结构可以"是文献与实测同向的空档命题 |

### 7.2 我们的差异点一句话（总）

**FLUED 是"学习边界 byte 段→单槽单向量压缩→delta-rule 状态机→k 查询读出"全链路的唯一
占位者；文献在每一单环都有最近邻（压缩器家族/delta-rule 容量线/MesaNet 迭代读出/HOLA
锐化读出），但'段粒度 × 单槽 × 闭式读出差距 × 键几何'的四环联合剖面无人报告——我们的
证据台账（E95/E114/E115、E73–E78）本身就是空档贡献。**

## 8. 存疑项（仅摘要可读/未深读）

1. Log-linear attention（2506.04761）：仅摘要可读，层级桶细节未核。
2. Kaczmarz Linear Attention（2605.08587）：仅摘要可读。
3. MesaNet 细节：HTML 全文可读，已核 CG 机制与训练时延声明；其在**长上下文检索**上的
   数字未逐项核。
4. KATA（2607.17419）：HTML 全文可读，MQAR 台账数字已核；对称锥核的理论细节未深读。
5. DNC（Nature 2016）：经典工作，usage/allocation 机制为常识级确认，未重读原文。
6. LLMLingua-2 之后的系谱新成员（2026 年工程迭代，如 SecurityLingua）：二手来源，未核原文。
7. "读出查询数 k 扫描"的空格判定基于本轮检索零命中——存在漏检可能，若多槽读出臂正式
   立项，建议立项前再跑一次针对性检索（query: "multiple readout queries linear attention
   state" / "number of summary tokens ablation"）。

## 9. 候选术语清单（待登记 TERMS.md，主智能体裁定）

| 候选术语 | 原文 | 中文全称 | 一句话定义 | 首现 | 状态 |
|---|---|---|---|---|---|
| MQAR | Multi-Query Associative Recall | 多查询联想回忆 | Zoology 提出的合成考场：长上下文存多组键值对后按键查值，测联想回忆容量 | 本报告 §3.1 | 候选 |
| MesaNet | MesaNet | MesaNet（共轭梯度读出网络） | 把层内状态读出写成共轭梯度迭代解正规方程的序列模型 | 本报告 §4.3 | 候选 |
| HOLA | Hippocampal Linear Attention | 海马体线性注意力 | delta-rule 压缩态 + 有界精确 KV 缓存双通道，残差准入 + 解耦归一化锐化读出 | 本报告 §4.2 | 候选 |
| 锐化读出 | sharpened readout | 锐化读出 | 读出侧用归一化/温度件把软平均读出压成近似硬检索 | 本报告 §4.2 | 候选 |
| DNC | Differentiable Neural Computer | 可微神经计算机 | Graves 2016 外存架构，usage 向量 + 最少使用优先分配 + free gate | 本报告 §5 | 候选 |
| Product Key Memory | Product Key Memory | 乘积键记忆 | 键从固定码本乘积分解选取的大记忆层（Lample 2019），"码本键"先例 | 本报告 §5 | 候选 |
| KATA | Kernelized Linear Attention with Symmetric Cones | 对称锥核化线性注意力 | 用对称锥核扩大有效特征维以破容量墙的线性注意力（2607.17419） | 本报告 §3.1 | 候选 |
| OSDN | Online Scaled DeltaNet | 在线对角预条件 DeltaNet | delta 规则标量步长升级为逐维对角预条件的写入规则（2605.13473） | 本报告 §3.1 | 候选 |
| GDN | Gated DeltaNet | 门控 DeltaNet | delta 规则 + 标量衰减门控的线性注意力（2412.06464，注意编号非 2412.06461） | 本报告 §3.1 | 候选（S38 报告已用） |
| ICAE | In-context Autoencoder | 上下文自编码器 | 冻结 LM 产 memory slot + AE/LM 双目标的上下文压缩器 | 本报告 §2 | 候选（fork3 已用） |
