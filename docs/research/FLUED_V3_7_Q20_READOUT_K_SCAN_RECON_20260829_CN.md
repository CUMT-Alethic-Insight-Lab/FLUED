# FLUED v3.7 Q20 多槽读出臂「读出查询数 k 扫描」针对性撞车复核报告

> 2026-08-29，按 AGENTS.md 协作协议规则 5（架构级臂开 GPU 前必出撞车侦察报告）的补充复核。
> 本报告是 `FLUED_V3_7_SUMMARIZER_LIT_RECON_20260829_CN.md`（下称「前报」）的**定向补查**：
> 前报 §8.7 自我怀疑——「读出查询数 k 扫描」的空格判定基于一轮检索零命中，存在漏检可能，
> 要求 Q20（多槽读出臂：每段用 M 个可学习槽位查询各从压缩状态读一根、拼接投影回 decoder，
> M=4 起步、扫 M∈{1,4,8}，写入侧冻结）立项前补一次针对性复核。本报告即该复核。
> 侦察方式：WebSearch + FetchURL 实时核实（arXiv 为主），全部引文附编号/URL；实际跑过的
> 检索查询清单见 §2（零命中协议：没命中要证明找过）。

## 0. 复核问题（钉死，逐字从前报 §8.7 展开）

**在以下谱系里，是否已有「对压缩状态/记忆用每个段多个（k>1）读出查询/读出槽，并把 k 当
扫描轴」的工作：**

1. 线性注意力/delta 规则（delta rule，把状态更新写成在线回归一步的线性注意力更新律）系：
   DeltaNet、GDN（2412.06464）、KDA、MesaNet、HOLA（2607.02303）、OSDN（2605.13473）、
   KATA（2607.17419）——读出面是否都是每位置单查询？有没有人多查询读状态矩阵？
2. 压缩记忆/KV 压缩系：Memorizing Transformer、Landmark Attention、ICAE、AutoCompressor
   系——读出侧查询数怎么处理？
3. 外存/读出机制系：DNC（多 read heads）、Perceiver/Perceiver IO（M 个 latent query 交叉
   注意力读出）、Set Transformer——与 Q20 的差异在哪？
4. MQAR/Based/Zoology 一线的容量分析里，「读出查询数」是否作为变量出现过？

**判定三档**：占位（同构已有）/ 邻接（形态相近需差异化声明）/ 空档。
**不算撞车的已知先例形态**（任务给定）：DNC 多读头、Perceiver latent queries——要回答的是
「在 delta-rule/线性注意力压缩态上按段做 k 槽读出并扫 k」这个具体组合有无占位。

## 1. 与既有报告的分工（去重声明）

- 前报 §4.1 已给出初步判词（「k 作为独立容量轴在公开文献中无占位」），但自列为存疑项
  （前报 §8.7）。本报告用**钉死的复核问题 + 显式查询清单**重扫，并对前报未核的三家
  （RAM-Net、Q-Delta、KVM/SeDeM）做全文/摘要级核实。
- 段→槽压缩器家族（gist/ICAE/AutoCompressor/Beacon）、写键塌缩缓解件、DNC allocation 等
  前报 §2/§5 已裁定者，本报告不复述，仅在新证据触及读出侧时引用。

## 2. 检索协议：实际跑过的查询清单（零命中协议记录）

本轮共执行 12 组 WebSearch + 5 篇 FetchURL 全文/摘要核实。查询清单（原样记录）：

| # | 查询 | 命中要点 |
|---|---|---|
| Q1 | `multiple readout queries linear attention state matrix associative memory arxiv` | HOLA、VLA（2605.11196）、Echo（2605.06997）等；无 k 读出扫描 |
| Q2 | `delta rule readout multiple queries per segment ablation arxiv 2025 2026` | 无相关命中（结果漂移） |
| Q3 | `number of memory tokens ablation per segment AutoCompressor ICAE gist tokens` | ICAE 固定 k=128 memory slots（H2MT 表引）；扫的是**写入侧槽数** |
| Q4 | `MesaNet conjugate gradient readout state matrix arxiv 2506.05233` | MesaNet v1/v2 及引用者（2604.21100、2605.05838）确认 |
| Q5 | `"read heads" ablation number DNC differentiable neural computer copy task performance` | DNC R 读头为固定结构件（R=4 常见），未见 R 作容量轴系统扫描 |
| Q6 | `Perceiver number of latent queries ablation Perceiver IO latents bottleneck` | latent 数扫描在**编码瓶颈**侧；ICLR'24 附录的 copy 任务退化实验 |
| Q7 | `Set Transformer pooling by multihead attention number of seed vectors k ablation` | PMA_k 的 k seed vectors 定义核实（1810.00825） |
| Q8 | `线性注意力 压缩状态 多查询 读出 槽位` | 无相关中文学术命中（结果漂移） |
| Q9 | `"multi-query" OR "multiple queries" readout recurrent state matrix linear attention 2026 arxiv` | Mamba recall scaling（OpenReview）等；MQAR 的 "multi-query" 语义核实 |
| Q10 | `MQAR multi-query associative recall capacity state size number of queries Zoology ablation` | KATA/KLA/RAM-Net/HGRN2 的 MQAR 协议核实：扫描轴=N_pairs/L_seq/state size |
| Q11 | `KDA Kimi delta attention 2510.26692 chunkwise state readout` | KDA 逐 token 单查询读出确认（含第三方推导博客） |
| Q12 | `segment-level memory multiple slot queries per segment readout byte language model 2026` | 无同构命中（结果漂移） |
| Q13 | `"number of summary tokens" ablation compressor long context memory slots` | gist/ICAE 系扫 summary token 数=写入预算；无读出查询数扫描 |
| Q14 | `"multiple read keys" OR "several queries" fast weight programmer delta rule state retrieval arxiv` | SDM（2607.07386）、GDN-2（2605.22791）、Q-Delta（2606.08804）浮出 |
| Q15 | `读出查询数 扫描 压缩记忆 槽位 消融 语言模型` | 无相关中文学术命中 |
| Q16 | `Q-Delta 2606.08804 readout residual writeback linear attention` | Q-Delta 全文核实（见 §3.2） |
| Q17 | `"k queries" OR "multiple readout slots" compressed recurrent state decoder segment arxiv` | KVM（2605.09877）、SeDeM（2608.00311）浮出并核实 |
| Q18 | `"multi-query readout" OR "multiple read heads" compressive memory transformer long context` | MQA/GQA（KV 共享，异族）；无压缩态多读头读出 |
| Q19 | `learnable slot queries read from compressed memory state per segment tokenization-free byte model` | 无同构命中（MambaByte 等 byte 模型无此机制） |

FetchURL 全文/摘要级核实 5 篇：MesaNet v2（2506.05233，前报已核，本轮复核其读出公式）、
RAM-Net（2602.11958，HTML 全文）、Q-Delta（2606.08804，HTML 全文）、KVM（2605.09877，
摘要）、SeDeM（2608.00311，摘要）。

**零命中判定依据**：Q1/Q2/Q12/Q15/Q17/Q19 六组正面查询（中英、同义词族 multi-query
readout / multiple read heads / slot queries / k queries per segment / 读出查询数）均无同构
命中；Q9/Q10/Q14 三组侧面查询（MQAR 语义、fast weight 多读键）确认了相邻概念的边界
（见 §3–§5）。

## 3. 谱系一：线性注意力/delta-rule 系——读出面逐家核

### 3.1 读出面形态核实

| 工作 | 编号+日期 | 读出面形态 | k>1 读出查询？ |
|---|---|---|---|
| DeltaNet / FWP | [2102.11174](https://arxiv.org/abs/2102.11174)（2021-02） | o_t = S_t q_t，逐 token 单查询 | 无 |
| GDN | [2412.06464](https://arxiv.org/abs/2412.06464)（2024-12） | 同上（门控衰减版） | 无 |
| KDA | [2510.26692](https://arxiv.org/abs/2510.26692)（2025-10） | 同上（通道级衰减）；第三方推导（[snowchord.com](https://snowchord.com/blog/linear-attention-visualized/)、[doubleword.ai](https://blog.doubleword.ai/you-could-have-come-up-with-kimi-delta-attention)）佐证逐 token 单查询 | 无 |
| MesaNet | [2506.05233](https://arxiv.org/abs/2506.05233)（2025-06，v2 2026-06） | CG（共轭梯度）迭代解层内回归，**读出仍是逐 token 单查询**，被扫描的是 CG 步数（迭代深度），非查询数 | 无（迭代深度≠查询数） |
| HOLA | [2607.02303](https://arxiv.org/abs/2607.02303)（2026-07，未评审） | 压缩态逐 token 读出 + 精确 KV 缓存锐化读出（RMSNorm-γ）；前报 §4.2 已核 | 无 |
| OSDN | [2605.13473](https://arxiv.org/abs/2605.13473)（2026-05） | 写入侧对角预条件；读出逐 token 单查询 | 无 |
| KATA | [2607.17419](https://arxiv.org/abs/2607.17419)（2026-07） | 对称锥核扩大特征维；读出逐 token 单查询 | 无 |

### 3.2 三家新核实的最近邻（本轮增量）

| 工作 | 编号+日期 | 读出形态 | 与 Q20 的关系 | 裁定 |
|---|---|---|---|---|
| **Q-Delta** | [2606.08804](https://arxiv.org/abs/2606.08804)（2026-06，ICML，HTML 全文已核） | 论文自陈：「existing linear RNN models share a common structural assumption: state evolution is governed primarily by key–value interactions, while the query is used only to read out the evolved state」——**它以「重审议 query 读出角色」为全部立项动机，但做法是把读出 ô_t=S_{t−1}q_t 回写进状态更新律（读出反馈写入侧），读出本身仍是逐 token 单查询** | **强证据：2026 年把「读出」当论文题眼的最近工作，也没有把「读出查询数」当成可扩的轴**；Q-Delta 动的是写入律，Q20 动的是读出宽度且写入侧冻结 | **邻接**（读出话语权最近邻） |
| **RAM-Net** | [2602.11958](https://arxiv.org/abs/2602.11958)（2026-02，HTML 全文已核） | 状态 = M 个显式槽（M=d_p^U 指数级扩容），读地址 r_t 经 Product Softmax+Top-K 得 **K-hot 稀疏地址**——单次读出触碰 K 个槽但输出仍是一根向量 o_t=r_t·(归一化 S_t)；消融轴 = 槽容量 M 与乘积阶 U，**K 固定 Top-8 不扫**；读出逐 token | 「一读多头碰多槽」形态上与「多查询读状态」最近；但其 K 是稀疏寻址宽度（算力/精度权衡），不是每段 k 根独立读出向量拼接，更不扫 k | **邻接**（本轮发现的最贴近读出侧的近邻） |
| **Sparse Delta Memory（SDM）** | [2607.07386](https://arxiv.org/abs/2607.07386)（2026-07） | 稀疏化扩容 delta-rule 状态（状态/写入侧手术） | 写入/状态侧扩容线，与 Q20 读出端正交 | 不撞 |

### 3.3 谱系一判词

**读出面全员逐位置单查询（每 token 一根 q_t 对终态/当前态点积）；「每段 k>1 根读出查询
并扫 k」无占位。** 多头（H heads 各自独立状态）是状态分区并行，不是对同一状态矩阵的多
查询读出。Q-Delta 的存在反而加固了判词：该谱系里「读出」作为一个可设计的对象刚被单独立
项（2026-06），而其设计者也没有把查询数当轴——**这条轴在该谱系内是真空**。

## 4. 谱系二：压缩记忆/KV 压缩系——读出侧查询数怎么处理

| 工作 | 编号+日期 | 读出侧查询处理 | 裁定 |
|---|---|---|---|
| Memorizing Transformer | [2203.08913](https://arxiv.org/abs/2203.08913)（2022-03） | kNN 检索精确 KV 库存，逐 token 单查询；库存非压缩 | 不撞（异族，前报已登记） |
| Landmark Attention | [2305.16300](https://arxiv.org/abs/2305.16300)（2023-05） | softmax 注意力经 landmark 键控访问原始 KV，逐 token 查询 | 不撞 |
| ICAE | [2307.06945](https://arxiv.org/abs/2307.06945)（2023-07） | 下游 LM 以 softmax 注意力读全部 m 个 memory slot；**消融扫的是 slot 数 m（写入/存储预算）**，读出查询数=下游位置数，非设计轴 | 不撞 |
| AutoCompressor | [2305.14788](https://arxiv.org/abs/2305.14788)（2023-05） | 同上：summary vector 数是压缩预算轴 | 不撞 |
| Gist tokens | [2304.08467](https://arxiv.org/abs/2304.08467)（2023-04） | 同上 | 不撞 |
| **KVM**（Key-Value Means，键值均值块循环记忆） | [2605.09877](https://arxiv.org/abs/2605.09877)（2026-05，v5 2026-08，摘要已核） | 块级 KV 均值作压缩态，读出=softmax 注意力扫全部块均值，逐 token 查询；状态可增容 | 不撞（读出查询数非轴） |
| **SeDeM**（选择性解压缩框架） | [2608.00311](https://arxiv.org/abs/2608.00311)（2026-07，摘要已核） | 查询条件化**选择器**挑出相关 memory block 后解压缩喂 decoder；读出=块选择+软注意力，无 k 槽读出 | 不撞 |

**谱系二判词**：该系被系统性扫描的是**写入/存储侧槽数**（gist/summary/memory token 数，
ICA「k=128 memory slots」式固定预算，前报 fork3 已有压缩率-效用扫描口径），**读出侧查询
数从来不是变量**——读出永远是 softmax 注意力逐下游位置查询。Q20「写入侧冻结、只扫读出
查询数 k」在该系里概念上不匹配，无占位。

## 5. 谱系三：外存/读出机制系——已知先例形态与差异点

| 工作 | 编号+日期 | 多读机制 | 与 Q20 的差异 | 裁定 |
|---|---|---|---|---|
| DNC（可微神经计算机） | [Nature 2016](https://www.nature.com/articles/nature20101) | R 个读头各读一根向量拼接回控制器——「多读头+拼接」的**形态先例**；但内存是精确槽式外存、读权重经内容/时序链接寻址、R 是固定结构件（R=4 常见），**未见 R 作为容量轴的系统扫描**（Q5 检索确认） | 读的是精确槽库存非叠加压缩态；不按段；下游非 byte 编解码；R 不当轴扫 | 邻接（已知先例形态，任务给定不算撞车） |
| Perceiver / IO / AR | [2103.03206](https://arxiv.org/abs/2103.03206)/[2107.14795](https://arxiv.org/abs/2107.14795)/[2202.07765](https://arxiv.org/abs/2202.07765) | latent query 交叉注意力；**latent 数 N 是一等扫描轴但在编码瓶颈侧**（压缩比轴）；Perceiver IO 的输出侧查询按输出位置定义（每输出位置一根 query），非「对同一压缩态发 k 根查询」 | 读的载体是 latent 数组（多向量瓶颈）非单一 delta-rule 状态矩阵；交叉注意力非线性状态机；k 扫描在写入/瓶颈侧 | 邻接（已知先例形态） |
| Set Transformer PMA_k | [1810.00825](https://arxiv.org/abs/1810.00825)（2018-10，ICML'19，定义核实） | PMA_k：k 个可学习 seed vector 作查询对集合做多头注意力读出 k 根向量——**「可学习槽查询数 k」作为显式结构超参的先例**，k 是设计面的一部分 | 读的是 softmax 注意力下的 token 集合非 delta-rule 压缩态；非按段读出；下游非 byte 编解码；k 未作容量轴系统扫描 | **邻接**（形态上最贴近「k 槽查询读出」的经典件） |

**谱系三判词**：三家都是「形态先例、组合不撞」。尤其 PMA_k 必须在 Q20 立项书点名——它是
「可学习槽查询组读出」这一**机制件**的正典出处；Q20 的新颖性不在机制件本身，而在
**读出对象（delta-rule 叠加压缩态）× 读出粒度（按段）× 下游（byte 级编解码）× k 作为
容量轴被显式扫描**的四环组合。

## 6. 谱系四：MQAR/Zoology 容量分析——「读出查询数」是否当过变量

- MQAR（Multi-Query Associative Recall，多查询联想回忆，[2312.04927](https://arxiv.org/abs/2312.04927)，2023-12）的 **"multi-query" 指一个序列内呈现多组键值对、尾部给多个查询键**——「多」在被回忆的对数与查询位置数，**每个查询位置仍是单查询读出**；它不是「对压缩态发多根读出查询」的意思（Q9/Q10 检索核实，Naju 2607.21000、KLA 2602.10743、KATA 2607.17419、RAM-Net 2602.11958 的 MQAR 协议一致佐证）。
- 该一线被扫描的轴始终是：**键值对数 N_pairs × 序列长 L_seq × 状态尺寸（state size）**
  （Zoology 原典、HGRN2 2404.07904 的 hyperparameter sweep、RAM-Net 的 MQAR-vs-state-size
  曲线、KATA 的同状态尺寸逐档召回台账）——**「读出查询数」从未作为变量出现**。

**谱系四判词**：空档。MQAR 语义本身还提示一个命名风险：Q20 若用 "multi-query readout"
措辞会与 MQAR 撞词，建议立项书用「多槽读出（multi-slot readout）/ 读出查询数 k」并显式
区分。

## 7. 撞车裁定汇总（三档）

| 谱系 | 裁定 | 代表引用 | 一句话差异点/依据 |
|---|---|---|---|
| 1. 线性注意力/delta-rule 系 | **空档**（读出查询数 k 无占位） | DeltaNet 2102.11174；GDN 2412.06464；KDA 2510.26692；MesaNet 2506.05233；HOLA 2607.02303；OSDN 2605.13473；KATA 2607.17419 | 全员逐位置单查询 o_t=S_t q_t；连以「重审议读出」立项的 Q-Delta（2606.08804）也不扫查询数 |
| 1-邻接 | **邻接 ×2** | Q-Delta 2606.08804；RAM-Net 2602.11958 | Q-Delta 动写入律（读出反馈），Q20 动读出宽度且写入冻结；RAM-Net 的 K-hot 是稀疏寻址宽度（固定 Top-8），非每段 k 根独立读出拼接 |
| 2. 压缩记忆/KV 压缩系 | **空档** | ICAE 2307.06945；AutoCompressor 2305.14788；KVM 2605.09877；SeDeM 2608.00311 | 该系扫的是写入/存储侧槽数（压缩预算），读出侧查询数从来不是变量 |
| 3. 外存/读出机制系 | **邻接（已知先例形态，不撞）** | DNC（Nature 2016）；Perceiver 系 2103.03206/2107.14795/2202.07765；Set Transformer PMA_k 1810.00825 | 多读头/latent/seed 的机制件有主，但读出对象×粒度×下游×k 扫描的四环组合无占位 |
| 4. MQAR 容量分析线 | **空档** | Zoology 2312.04927；HGRN2 2404.07904；KLA 2602.10743；KATA 2607.17419 | 扫描轴恒为 N_pairs/L_seq/state size；「读出查询数」从未作为变量 |

**无一家「占位」。总裁定：空档，Q20 可立项。**

## 8. 对 Q20 立项书的差异化声明草案与建议

### 8.1 差异化声明草案（邻接占位较多，必写）

> 「Q20 在读出端对**单一 delta-rule 压缩状态矩阵**按段施加 k 个可学习槽位查询、各读一根
> 向量后拼接投影，并将 **k 作为独立容量轴显式扫描**（M∈{1,4,8}）；写入侧完全冻结。这与
> Perceiver/PMA_k 的 latent/seed 查询（softmax 集合读出、latent 数扫描在编码瓶颈侧）、
> DNC 多读头（精确槽式外存、读头数不当轴扫）、RAM-Net 的 K-hot 读地址（逐 token 稀疏
> 寻址、K 固定 Top-8）、Q-Delta 的读出反馈（动写入律、读出仍单查询）均不同：读出对象
> 是叠加压缩态、读出粒度是按段、下游是 byte 级编解码重建、k 是被扫描的容量变量。」

### 8.2 仍需警惕的最近邻工作清单（立项后跟踪）

1. **Q-Delta**（2606.08804，ICML 2026）：读出话语权最近邻；若其后续版本把 ô_t 扩展成多
   方向读出，直接逼近 Q20 领土——立项书引用并跟踪 v2。
2. **RAM-Net**（2602.11958）：读出侧多槽触碰的最近形态；其 K 目前是算力旋钮，一旦有人
   把 K 当容量轴扫并拼接多读向量即构成近撞——跟踪。
3. **MesaNet**（2506.05233 v2，2026-06）：迭代读出模板（Q20 设计模板候选）；其 CG 步数
   扫描与 Q20 的 k 扫描在叙事上互补，立项书应写明「迭代深度≠读出宽度」的分工。
4. **HOLA**（2607.02303，未评审）：锐化读出件（RMSNorm-γ）可作为 Q20 各槽查询的解耦
   归一化设计借鉴；同时其「压缩态+精确缓存」双通道是 Q20 结果解读的对照语境。
5. **PMA_k / Perceiver latent 扫描文献**：机制件正典，审稿人必提；差异化声明照 §8.1 写。

### 8.3 命名警示

避免 "multi-query readout" 措辞（与 MQAR 撞词，语义不同）；建议「多槽读出（multi-slot
readout），读出查询数 k」。

## 9. 存疑项与局限

1. RAM-Net 与 Q-Delta 为 HTML 全文级核实；SDM（2607.07386）仅检索摘要级，其读出面未逐
   公式核（判为写入/状态侧，低风险）。
2. DNC 原始论文未重读全文，「R 读头未作容量轴系统扫描」基于 Q5 检索结果与二手实现
   文档；NTM/DNC 后续文献浩繁，存在个别 toy 实验扫读头数的可能（低概率、低相关）。
3. 中文检索（Q8/Q15）命中质量差（结果漂移），中文社区预印本覆盖不能打包票；但目标谱系
   主力文献均在 arXiv 英文线，残余风险低。
4. 2026-08 当月新发预印本可能有漏网（检索时点 2026-08-29）；建议 Q20 预注册文档挂上
   §8.2 清单的跟踪任务。

## 10. 候选术语清单（待登记 TERMS.md，主智能体裁定）

| 候选术语 | 原文 | 中文全称 | 一句话定义 | 首现 | 状态 |
|---|---|---|---|---|---|
| 多槽读出 | multi-slot readout | 多槽读出 | 读出端用 k 个可学习槽位查询各从压缩状态读一根向量、拼接投影回下游的读出形态（Q20 臂） | 本报告 §6 | 候选 |
| RAM-Net | Random Access Memory Network | 随机存取记忆网络 | 用乘积 softmax+Top-K 把输入映射为高维稀疏地址、显式槽化扩容线性注意力状态的架构（2602.11958） | 本报告 §3.2 | 候选 |
| Q-Delta | Q-Delta | 查询感知 delta 规则 | 把查询条件化读出 ô_t=S_{t−1}q_t 混入 delta 规则更新、读出反馈写入侧的线性注意力（2606.08804） | 本报告 §3.2 | 候选 |
| PMA | Pooling by Multihead Attention | 多头注意力池化 | Set Transformer 的集合读出件：k 个可学习 seed vector 作查询对集合做交叉注意力读出 k 根向量（1810.00825） | 本报告 §5 | 候选 |
| KVM | Key-Value Means | 键值均值块循环记忆 | 块级 KV 均值作压缩态、softmax 注意力读全部块均值的可增容块循环注意力（2605.09877） | 本报告 §4 | 候选 |
| SeDeM | Selective Decompression of Hidden-State Memory | 选择性隐态解压缩框架 | 隐态块存储+查询条件化选择器+解压缩喂 decoder 的长上下文框架（2608.00311） | 本报告 §4 | 候选 |
| SDM | Sparse Delta Memory | 稀疏 delta 记忆 | 以稀疏化把门控线性 RNN 状态扩容数个量级的架构（2607.07386） | 本报告 §3.2 | 候选 |
