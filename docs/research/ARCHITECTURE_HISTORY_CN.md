# FLUED 架构发展史（v0.4 – S36）

> 本文档按版本线梳理 FLUED 的架构形态、关键决策、核心指标与终局判词。
> 单一事实源以 `docs/CURRENT_STATE.md` 证据注册表为准；本文数字均标注出处。
> 命名说明：v3.5 是 v3.4 收尾系列，KDA 世代直接跳号为 v3.6。

---

## v0.4 / v1：软边界自编码器

**架构一句话**：以 tied-weight Transformer encoder-decoder 对字节流做软分段自编码，拟在统一 352.9M LM 主体下与 BPE/BLT 做公平对比。

**关键决策**：提出“统一 LM 主体、仅换输入接口”的公平对比框架；规划三种子、全量 22GB `corpus_v3`、E1 40K / E3 30K 统一步数；差异仅 embedding（FLUED frozen encoder vs BPE tokenizer vs BLT encoder+ByteLM）。

**核心指标**：

| 指标 | 数值 | 出处 |
| --- | ---: | --- |
| recon_acc | 0.9999 | `docs/research/FLUED_RESEARCH_RETROSPECTIVE_CN.md` §2 |
| m/n | 0.379 | 同上 |
| 压缩倍数 | 约 2.64x | 同上 |
| 历史 E3 FLUED BPB | 1.2114 | 同上 |
| 历史 E3 BPE BPB | 1.4786 | 同上 |

**终局判词**：确立了“可微 byte boundary 可以学习”的最小假设，并留下一个历史下游阳性信号；但 tied decoder 与压缩控制的动力学冲突在后续版本才被揭示，v1 BPB 信号未在当前公平协议下复现。

---

## v2：去噪重建与 tied inverse

**架构一句话**：328M tied encoder-decoder（SDPA+SwiGLU，d=1024，24L），在 PAD-offset+MASK_ID 词表上做 clean/denoising 重建，带 banded soft assignment 与五类边界先验。

**关键决策**：去噪重建为主目标；`latent_consistency_weight=0.0`（因 0.03 会爆炸）；`assignment_window=128`；长度感知压缩；保留 tied inverse。

**核心指标**：

| 指标 | 数值 | 出处 |
| --- | ---: | --- |
| 三 seed recon_acc | 0.9991 / 0.9993 / 0.9996 | `FLUED_RESEARCH_RETROSPECTIVE_CN.md` §3 |
| 三 seed m/n | 0.470 / 0.498 / 0.491 | 同上 |
| 公平 D1 FLUED v2 BPB | 0.8732 | `FLUED_RESEARCH_RETROSPECTIVE_CN.md` §4 |
| 公平 D1 BPE-8K BPB | 0.8066 | 同上 |
| 公平 D1 BLT BPB | 2.3996 | 同上 |

**终局判词**：稳定学到可微 byte 边界和高精度重建，但公平比较仍落后 BPE；tied decoder、压缩权重与去噪比例的动力学冲突为 v3 转向“语言编码器”提供了核心动机。

---

## v3.0：控制流形与因果 surprise

**架构一句话**：提出“流式 byte-to-latent 转导器 + 显式 prefill/generation 语义”，用低维控制流形（高维 payload / 低维 control z）分离边界、记忆、预算决策。

**关键决策**：否决激进可学 Mapping Controller（Version A），推荐固定投影 Φ + 小控制头（Version B）；边界控制应消费因果 surprise 估计而非同位 residual；先跑小探针再集成。

**核心指标**：

| 指标 | 数值 | 出处 |
| --- | ---: | --- |
| native boundary vs residual corr | 0.033 | `docs/versions/v3.0/FLUED_V3_CONTROL.md` |
| oracle FMC boundary corr | 0.773 | 同上 |
| causal learned surprise probe corr | 0.753–0.795 | 同上 |
| surprise-assisted E1 eval_acc (w=0.20) | 0.328 | 同上 |

**终局判词**：把 v3 从“大控制器”收敛为“因果 surprise → boundary 辅助”的小桥，验证了低维控制信号的诊断价值，但未证明完整 memory-matrix 架构；FMC Boundary 因依赖 oracle residual 被搁置。

---

## v3.1：语言编码器 / codec 闭环

**架构一句话**：将 FLUED 重新定位为语言编码器/codec：byte 流 → 弱边界分段 → 共享段表示 → readout latent（给 backbone）+ summary latent（内部 memory）→ 显式长度/槽分配器 → latent-to-byte decoder。

**关键决策**：backbone 只看 readout latent，不看 FLUED memory；decoder 不读 encoder memory；先训 codec、后冻 codec 训 backbone；用 strict masked-source backbone 对比。

**核心指标**：

| 指标 | 数值 | 出处 |
| --- | ---: | --- |
| 2M codec 10k recon_acc | 0.5063 | `docs/versions/v3.1/FLUED_V3_1_ARCHITECTURE_CN.md` |
| 2M codec 10k length_acc | 0.9725 | 同上 |
| 2M codec 10k units/byte | 0.1170 | 同上 |
| min backbone 3k latent mask_acc | 0.1784 | 同上 |
| min backbone 3k byte baseline | 0.1498 | 同上 |
| mean_first_last 10k streaming recon | 0.6469 | 同上 |

**终局判词**：首次跑通 byte→segment→readout→decoder 完整闭环，latent backbone 在公平 segment-mask 下略超 byte baseline；但 long span 重建与 fixed-text 泛化弱、memory 依赖小，证明不能只优化 reconstruction。

---

## v3.2：memory-free 默认主线

**架构一句话**：明确五条约束：boundary 无记忆、interpretation 可读取过去 memory、summary 因果只追加、backbone 只看 readout、decoder 不依赖 encoder memory。

**关键决策**：16×16 factorized byte coordinate seed；segmentor memory-free；interpreter 可读 past memory；memory pool 为 chunk 追加序列，固定 r=2/4 slots；top-k sparse retrieval；no-memory masked-source codec 作为最强最简主线。

**核心指标**：

| 指标 | 数值 | 出处 |
| --- | ---: | --- |
| v3.2.1 no-memory mask_acc | 0.1898 | `FLUED_RESEARCH_RETROSPECTIVE_CN.md` §6 |
| byte baseline mask_acc | 0.1440 | 同上 |
| Δ mask_acc | +0.0458 | 同上 |
| no-memory CE | 3.1424 | 同上 |
| byte baseline CE | 3.3782 | 同上 |

**终局判词**：以 strict masked-source 堵住 clean-encode 侧漏，确认 no-memory latent 接口可降低小 backbone 学习难度；但 active memory/top-k retrieval 未证明为默认主线收益，为 v3.3 公开 skeleton 定界。

---

## v3.3：公开可运行的 byte-to-latent decision interface

**架构一句话**：结构化 byte lookup → signed segmentor → 双阈值切分 → memory-conditioned interpreter → readout + 低秩序列 memory → 外部 backbone → tied-inverse decoder。

**关键决策**：segmentor 不读 memory；interpreter 可读 other-chunk memory 但屏蔽 self；prompt encoding 默认 parallel-local memory bank；memory 是分支不是默认主线；strict masked-source 为底线。

**核心指标**：本阶段主要是 skeleton 与原则固化，新实验证据直接继承 v3.2.1：no-memory mask_acc 0.1898 vs byte 0.1440。

**终局判词**：给出可复现的公开代码 skeleton 和清晰架构边界，把 memory 明确降格为实验分支；本身未产出新的 scaling 证据，v3.4 在此基础上引入并行 memory 与真实计算门控。

---

## v3.4：并行 memory 与真实压缩门控

**架构一句话**：并行 local memory + 双级容量决策（边界用边际编码率、readout 用 emit 控制器）+ 独立/共享 decoder 对照的 ~38M 组件归因阶段。

**关键决策**：hard compact 真实压缩；L2 边际编码率；RoPE + 小 AR；plain byte lookup；硬 emit 前向+连续 ST 反传；验证独立 decoder vs shared inverse。

**核心指标**：

| 指标 | 数值 | 出处 |
| --- | ---: | --- |
| shared inverse + diag recon | 21.00% | `FLUED_V3_4_POST_MIGRATION_EXPERIMENTS_20260715_CN.md` §6.2 |
| independent decoder + diag recon | 40.92% | 同上 |
| shared inverse PPL | 43.37 | 同上 |
| independent decoder PPL | 30.83 | 同上 |
| pos+AR recon | 21.51% | 同上 §5.2 |
| memory 20K no-memory recon | 21.00% | 同上 §6.1 |
| memory 20K other-memory recon | 18.28% | 同上 |
| 5K L2 marginal coding rate recon | 0.7041 | `FLUED_RESEARCH_RETROSPECTIVE_CN.md` §11 |
| 5K L2 masked completion | 0.1477 | 同上 |
| 5K L2 actual latent/byte | 0.6804 | 同上 |

**终局判词**：在 ~38M 上完成组件归因，独立 decoder、RoPE+小 AR、plain lookup、硬 emit 被验证，共享逆与当前 memory 路径被证伪；但动态边界/L2 仍有溢出与梯度冲击，未形成同时满足共享逆 claim、边界过闸、无溢出、任务最优的默认配置。

---

## v3.5：分级冻结与离线反事实效用

**架构一句话**：分级冻结协议 L0-L5：L0 codec 本体 → L1 接口转移 → L2 离线反事实效用集 → L3 统一预算分配器 → L4 memory 举证 → L5 可选联合微调。

**关键决策**：共享逆判死，接受独立 decoder；boundary 与 emit 合并为统一预算分配器；memory 移出 scaling 主线；离线 CBIU 用 ≥8 mask draws + 类级聚合；分位数预算退火作为 emit 平滑引入方式。

**核心指标**：

| 指标 | 数值 | 出处 |
| --- | ---: | --- |
| L0 recon（两 seed） | 0.9930 / 0.9924 | CURRENT_STATE E1 |
| order swap/subst 探针 | 0.695 / 0.702 | CURRENT_STATE E1 |
| 线性可读性探针 | 98.5% | `FLUED_V3_5_PRESCALING_RESULTS_20260717_CN.md` §1 |
| 共享逆 order 探针 | 0.039 | CURRENT_STATE E3 |
| 独立 decoder order 探针 | 1.170 | CURRENT_STATE E4 |
| 分位数退火 0.257 latent/byte 重建 | 0.9584 | CURRENT_STATE E6 |
| 分位数退火 PPL | 20.35 | `FLUED_V3_5_PRESCALING_RESULTS_20260717_CN.md` §2 |
| L3 可加因子模型 AUC | 0.625 | 同书 §4 |

**终局判词**：分级冻结把联合共适应拆成平稳阶段，L0 codec 两 seed 饱和、独立 decoder 平反、分位数退火首个平滑压缩机制成立；但 L3 类级分配器 AUC 未过闸，memory 举证失败，投稿叙事走接口+协议+CBIU，不主张分块机制原创。

---

## v3.6 / S36：KDA 世代与精确检索通道

**架构一句话**：KDA 世代：byte 流 → byte embedder → DiT Segmentor → chunks → Summarizer projector → write head → KDA 状态机（串行逐通道更新）→ k=1 readout 包给主干；decoder 侧用逐段条件化做任务密度；S0′′ 双源教师前端 + S1.0 三任务；S36 主线 = 因果 cross-read 主干 + 按解码残差门控的精确缓存。

**关键决策**：整条 prompt 恰好 1 个 readout 包（k=1 主干接口）；逐段条件化仅限 decoder 侧任务密度；40/60 混合 mask；预测任务默认 latent MSE；S0 段落预训 + S0.5 GRPO 边界微调；独立 decoder；状态通道 R1 消融；分页/档案馆模型面向长上下文。

**核心指标**：

| 指标 | 数值 | 出处 |
| --- | ---: | --- |
| S0 F1 vs 教师 | 0.886 | CURRENT_STATE E17 |
| 组件预训 A/B（acc / PPL） | 0.189 / 34.2 vs 0.131 / 35.9 | CURRENT_STATE E18 |
| S0′′ direct / unmasked / PPL | 0.836 / 0.830 / 2.25 | CURRENT_STATE E30 |
| S0′′ masked | 0.160 | CURRENT_STATE E30 |
| R0 KDA-LM BPB | 1.80 / 1.85 | CURRENT_STATE E36 |
| H-Net 复现 BPB | 0.653 | CURRENT_STATE E36 |
| k=1 backbone | 0.206 | CURRENT_STATE E38 |
| s31 因果 cross-read backbone | 0.797 | CURRENT_STATE E44 |
| S36a (512B) backbone | 0.7981 | CURRENT_STATE E47 |
| S36g2 (4096B, batch 4) backbone | 0.8134 | CURRENT_STATE E52 |
| S36h gist-only backbone | 0.7910 | CURRENT_STATE E50 |
| 4096 存储拐点 gist-only vs 25% cache | 0.7956 vs 0.8134 (+1.78pp) | CURRENT_STATE E55 |
| P0 RULER needle 还原率 | 0.848 | CURRENT_STATE E53 |
| S39 形态 2 判死 | exact 0.00 | CURRENT_STATE E56 |

**终局判词**：v3.6 以 KDA 状态机为核心 interpreter，S0′′ 前端 + DiT summarizer + 逐段条件化 + S1.0 三任务使 512B/20K direct 0.836 / PPL 2.25；经 E38–E44 查明 0.206 平台死因是“缺逐段查询通道”而非容量，s31 精确通道 + S36 残差门控缓存成为主线；长文本至 4096 可行、域外复现成立，但生成线字节可读性仍是缺口（E42 冻结预测读头探针 BPB 4.96 / acc 0.15），S39 档案馆远程查询接口为下一战场。

---

## 命名撞车说明

v3.5 不是独立的下一代主干，而是 v3.4 收尾系列（L0-L5 分级冻结、CBIU、离线效用数据集）。KDA 世代因架构范式切换（状态机 + KDA + 单 readout 包）直接跳号为 v3.6。阅读文献引用时应注意：v3.5 文档讨论的是 v3.4 线的收尾工作，不是 v3.6 的前置阶段。
