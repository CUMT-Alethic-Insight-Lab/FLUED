# AGENTS.md — FLUED Project Guide for AI Coding Agents

> **单一事实源：[`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md)**——默认配置、证据注册表、闸门与待裁定队列。
> 任何实验默认起点是 canonical 配置（v3.6 线 `configs/canonical_v36.json` 为当前默认，`canonical_v35.json` 旧口径保留有效）；`tests/test_canonical_sync.py` 持续校验
> CLI 默认值 == canonical 配置 == CURRENT_STATE.md（v35/v36 两线均受守卫），三处漂移会红灯。新证据落地必须原地更新 CURRENT_STATE.md 并写 changelog。

> **术语注册表：[`docs/TERMS.md`](docs/TERMS.md)**——一切项目术语的唯一登记处，与 CURRENT_STATE 同级。两条长期法则：
> 1. **原地登记**：新术语（缩写、英文造词、非日常名词）落地必须先登记 TERMS.md（原文/中文全称/一句话定义/首现/提出方/日期/状态），否则视为不存在（黑户）；
> 2. **未注册词禁用**：写报告或回复时，凡不在 TERMS.md 的词，首次出现必须内联给出中文全称+一句话定义；英文造词必须挂中文语义锚。AI 提名的术语默认"候选"，用户点头才转正（候选→已注册，与证据状态机同构）。

> **FLUED** (FLexible Unified Encoder-Decoder): Tokenization-free learned boundary compression for language modeling.
> Semantic units are dynamically compiled by the model during encoding, not predefined by an external tokenizer.

## Quick Reference

| Task | Command |
|------|---------|
| Run tests | `python -m pytest tests/` |
| Smoke test E1 | `python -m flued.e1_stage_a --preset smoke_cpu` |
| v3.4 trainer help | `python tools/train/v3_4/train_v34_pos_ar_probe.py --help` |
| v3.4 matrix help | `python tools/launcher/v3_4/run_v34_pos_ar_matrix.py --help` |
| Check GPU | `nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader` |
| Check running procs | `Get-Process python*` |
| Read checkpoint step | `python -c "import torch; c=torch.load('checkpoints/e1_latest.pt', map_location='cpu', weights_only=False); print(c.get('global_step',0))"` |

## Environment

- **Python**: 3.11+; local validated environments currently use Python 3.12 for CUDA and Python 3.14 for tests.
- **PyTorch**: CUDA 12.8-compatible build for RTX 50-series GPU work.
- **GPU**: RTX 5080, 16 GB VRAM, CUDA 13.2
- **CPU**: Set `$env:OMP_NUM_THREADS=4; $env:MKL_NUM_THREADS=4` before training to avoid thread explosion.

## Architecture (3-stage pipeline)

```
E1 (Stage A)  →  E2 (Comparison)  →  E3 (Downstream LM)
   FLUED DSC       FLUED vs BPE/BLT     Frozen encoder + causal LM
   reconstruction   perplexity/cloze     next-byte prediction
```

- **FLUED**: Single Transformer encoder+decoder with **tied weights**. Boundary detection via `sigmoid(Linear(ΔH))`. Soft assignment matrix A does O(T²) pooling — fine for T≤512.
- **BLT** (baseline): Byte Latent Transformer — uses a pre-trained Byte LM's entropy to determine patches.
- **BPE** (baseline): Standard encoder-decoder Transformer on BPE tokens (vocab 8192).

Full project status: [README.md](README.md) · Versioned documentation: [docs/README.md](docs/README.md)

## Key Files

| File | Role |
|------|------|
| `flued/model.py` | `FLUEDAutoencoder` v0.4 — legacy core model (749 lines; v3.6 mainline is `flued/v36/`) |
| `flued/config.py` | `ModelConfig`, `TrainConfig`, `SIZE_CONFIGS`, CLI parsing |
| `flued/data.py` | `ByteReconstructionDataset`, PAD-offset encoding (PAD=0, byte b→b+1, vocab=257) |
| `flued/e1_stage_a.py` | E1 training loop (standalone, not using `train.py` Trainer) |
| `flued/e2_compare.py` | E2: multi-model comparison |
| `flued/e3_train.py` | E3: downstream causal LM training |
| `flued/e3_downstream.py` | `FLUEDDownstream`, `BLTDownstream`, `BPEDownstream` wrappers |
| `flued/v33/` | v3.3 codec implementation |
| `flued/v34/` | v3.4 parallel-memory and rate/emit extension |
| `flued/v36/` | v3.6 KDA-generation mainline model (`FLUEDV36`) |
| `tools/baselines/` | Baseline reproductions: `bpe_baseline/`, `blt_baseline/`, `hnet_repro/` (H-Net BPB 0.653 anchor), `hnet/` trainer |
| `tools/train/v3_6/train_v36.py` | v3.6 train/eval entrypoint (`--config` eats `configs/canonical_v36.json`) |
| `tools/train/v3_6/train_v36_s1.py` | v3.6 S1.0 three-task trainer (current canonical entrypoint, v36.2) |
| `tools/train/v3_6/train_s0_segmentor.py` | S0 segmentor pretraining entrypoint |
| `tools/train/v3_4/train_v34_pos_ar_probe.py` | v3.4 train/eval entrypoint |
| `configs/v3_4/` | v3.4 reproducible experiment matrices |
| `results/v3.4/5k_ablation/` | Public raw logs and curve artifacts |

## Conventions

- **Checkpoint naming**: `{model}_step{NNNNN}.pt` and `{model}_latest.pt`
- **PAD-offset encoding**: vocab_size=257, PAD=0, byte b → id b+1
- **Tied inverse**: blocks reversed, MHA/FFN subtracted instead of added. Forward and inverse share parameters. `dropout=0.0` in E1 (tied inverse is dropout-sensitive).
- **E1 presets**: `smoke_cpu`, `small_gpu`, `class300m_16gb` — defined in `flued/e1_stage_a.py`
- **skip_hard**: Always pass `skip_hard=True` during training/eval. Hard segmentation is for logging only.
- **归档盘（2026-08-06 起）**：新归档落 `K:\FLUED_archive\<run_name>`（含 SHA256SUMS）；~~存量 `L:\FLUED_archive` 只读、不迁移~~（2026-08-12 迁移修订：L: 499G 已迁 `N:\FLUED_archive_migration_20260812\`，canonical init `s0pp_pro_v4_sft_20260805` 原地保留；历史文档中的 L: 路径经 `outputs/migration_manifest_20260812.json` 映射到新位置）。
- **存储布局（2026-08-12 用户裁定）**：代码/文档在 E: 核心区；语料在 P:（v3 由 E: 迁入、v4 原在 P:）；存档点由用户提供的两块盘单独备份；W: 内容已验证全量在 N:（fineweb 三源 265 parquet，哈希校验真失败 0）→ 格式化后承接 v3.4 及以前的存档点；X: 源盘缺席且无撤离副本，codeparrot 需用户提供盘后重新下载。
- **存储布局（2026-08-16 用户裁定修订）**：旧 N:（623G 迁移存档）已拔盘离线保管；新换盘挂 N: 字母，`N:\FLUED_archive` = L: 全量 + K: v3.6 世代的验证副本（106 目录 SHA256 全绿，159G）。同日 v3.6 世代存档从 L: **归并迁移**至 K: 统一管理（34 目录校验后删源，逐目录显式路径；映射见 `outputs/migration_manifest_20260816.json`）；例外：`s0pp_pro_v4_sft_20260805`（canonical init）已随 `canonical_v36.json` `init_checkpoint` 翻转引用至 K: 路径，L: 原件删除。L: `FLUED_archive` 已清空（v3.4/v3.5 存档在 N: 均有验证副本；flashkda_msvc_patch 移 K:）。

## 协作协议（2026-08-06 与用户共同制定）

1. **假设先行，不直接裁定**：用户给出观察/直觉/验证方式/推理链，AI 登记为编号候选假设（与证据状态机同构：候选 → 已验证/已证伪），并设计最便宜的可证伪臂；证据落地后才改默认值。架构级"裁定"一律走此流程，不跳级。
2. **凭证管理**：API token 一律经 repo 外文件或 KMS 引用，永不进对话/文档/commit；已暴露的立即轮换。
3. **高带宽消息**：单条消息多决策多问题是正常形态（强模型协作的必然）；AI 的职责是解析成清单逐项跟踪，单条消息行动项超过三个时先复述清单再执行。
4. **中断协议**：用户以软暂停（Ctrl+S 或普通排队消息）代替 Esc 硬中断；AI 收到暂停信号后执行固定收尾——安全停/等 GPU 任务 → 当前状态原地入文档 → 交还控制权。
5. **撞车侦察先行（2026-08-09 与用户共同制定）**：任何架构级实验臂（新主干形态/新机制/新接口）立项并占用 GPU 之前，必须先产出**撞车侦察报告**——文献空档核查：是否已有同名/同构工作、近 12 个月谱系走向、我们的差异点一句话；报告入 `docs/research/` 并在该臂预注册文档中引用。**差异点说不清就不开臂**。侦察可委派 subagent 并行进行。目的：杜绝"先撞墙、后侦察"——检索墙（Zoology/MQAR 2023、copying 上界 2024，十条臂复证）、循环塌缩（Huginn 2025-02，E45 复证）、残差状态（RDN 2025-09，S38 提案后才发现）三次学费的教训。同时确立**生存验证原则**：任何组件（状态机/缓存/通道）若只在短窗冗余，其生死线考场必须排到长窗/多页，不许在短窗判词上安息。
6. **匿名镜像纪律（2026-08-09 用户裁定，ICLR 双盲投稿；代号 2026-08-10 起改为 MENTINER）**：匿名镜像仓（代号 **MENTINER**）由 `tools/maintenance/anonymize_mirror.py` 从主仓**单向**同步——快照式历史（无原作者元数据）、身份词表全量替换（项目名/用户名/邮箱/其他项目名/高校名/主页域名）、内部协作文档（handoff/TODO/session 导出）不进镜像。**镜像侧一切内容永不含 FLUED 及任何身份字样**；镜像永不回并主仓；托管只走匿名渠道（anonymous.4open.science 或一次性账号），**严禁推送到本人实名账号名下**（项目名已公开挂在个人主页与实验室站点）。新增身份词 → 立即扩充脚本替换表并重新同步。**同步前验证规程（2026-08-11 泄漏事故教训入例）**：每次重建后、推送前必跑全词表 grep 求零命中，并覆盖字符串替换的三类盲区——① 二进制附件（docx/pdf 永不入镜）；② 代码注释/docstring 层的裁定话语与日期叙事（"user-ruled 2026-08-06"式括注，由正则中性化）；③ 镜像运维自身的记录（changelog 运维条目、本条规则，由内容过滤器拦截——匿名设施的存在性本身不向审稿人暴露）。发现泄漏即修即重推，不等批次。

## 可选代码检索：XERJ

XERJ 用于降低陌生代码定位和跨文件探索的成本，不替代当前源码、Git diff、运行日志、测试或实际调用链验证。不要为增加工具使用率而调用它。

### 何时使用

优先考虑 XERJ：
- 任务涉及不熟悉的模块，尚不清楚实现入口；
- 需要查找跨模块逻辑、既有类似实现或相关测试；
- 已有搜索结果过多，直接阅读会显著扩大上下文；
- 多个智能体正在重复探索同一套稳定源码。

优先直接读取或精确搜索：
- 已有准确文件路径、符号位置、错误堆栈或小范围 diff；
- 任务只涉及少数已知文件；
- 目标内容未被索引，或索引版本与当前任务不一致。

### 使用前检查

首次需要索引检索时，检查：
1. CLI 或项目封装是否可用，服务是否可达；
2. 本项目是否有登记的语料与查询入口；
3. 索引覆盖哪些目录、排除哪些内容；
4. 索引对应的源码版本、更新时间及当前任务是否匹配。

同一任务内不必每次查询都重复检查。源码版本变化、节点重启或结果明显异常时重新核验。

没有索引时，不自动全盘扫描。优先使用项目现有封装；否则先检查本机 CLI 帮助，再对明确授权的源码范围 dry-run。仅在范围、资源和数据边界清楚时建立索引。

### 查询与核验

- 优先限定到相关项目、版本和模块。
- 从少量结果开始，默认约3条短片段；需要时再扩大。
- 已知符号且定义检索能力经过验证时，可使用 def；否则使用具体模块名、标识符和行为描述查询。
- 命中后读取实际源码，确认版本、位置和必要上下文。
- 索引路径来自快照时，按语料映射回实际源码，不将旧行号直接当现行位置。
- 一次改写仍无有效结果，或覆盖/版本不可靠时，转用 Grep、Glob、Read 或其他合适工具，不反复重试。
- 未命中不等于代码不存在；检索结果不是完整调用图或安全证明。

### 索引维护与多智能体协作

- 每个语料登记来源、覆盖范围、版本、更新时间及结果路径映射。
- 不同项目或不同源码版本不得混写同一共享索引命名空间。
- 多智能体共用语料时，指定一个维护者，其他智能体默认只读查询。
- 合并、更新依赖或切换被索引版本后，维护者按需增量更新。
- 未提交修改默认直接读取；除非已有明确方案，不为每个小任务创建新索引。
- 任务交接只传语料标识、版本、覆盖限制和少量入口，不转发大量检索原文。

### 数据与运行边界

- 排除密钥、凭据、环境秘密、客户资料、数据库、备份、运行日志、依赖缓存和构建产物，除非用户对具体数据范围另有明确授权。
- 不因为目录被忽略而整体取消忽略规则；需要的源码使用白名单或独立快照。
- 不自动安装软件、启用外部嵌入服务、下载模型、上传源码或发送反馈。
- 保持项目规定的认证和网络边界，不打印密钥或可能含凭据的节点日志。
- 不自动删除或替换其他索引；不绕过工具的预算或范围确认。
- XERJ 不可用时继续完成任务，不把修复可选检索工具变成主任务。

### 简短反馈

任务交付中，只有使用过 XERJ或遇到相关限制时，简短记录：
- 使用的语料与版本；
- 是否帮助定位了实际源码；
- 主要问题：无关命中、覆盖不足、版本过时或工具不可用。

不得在没有对照证据时声称节省了 token、提高了召回率或完成了全面搜索。

## ⚠️ Critical Pitfalls

1. **Never use wildcards to delete checkpoints.** Always list and verify exact paths first. Keep the latest checkpoint and analysis milestones.

2. **FP16 entropy/log underflow**: When computing entropy over the byte vocabulary in FP16, cast to `.float()` before logarithms.

3. **GradScaler overflow**: On overflow skip, metrics must not advance as if an optimizer step succeeded.

4. **CUDA context corruption**: After force-stopping a GPU process, wait for the CUDA context to clear before launching another run.

5. **Duplicate process check**: Always inspect active Python/GPU processes before launching training.

6. **Versioned paths**: v3 experiment code lives under `tools/*/v3_*`; do not reintroduce pre-reorganization import paths.

7. **证据表编辑序号核对（2026-08-09 两次事故的教训）**：编辑 `docs/CURRENT_STATE.md` 证据注册表后，必须立刻核对序号完整性——`grep -n "^| E[0-9]" docs/CURRENT_STATE.md` 对比编辑前后的编号清单，确认无丢行、无重号。整行替换式 Edit 的 new_string 必须显式带回原行内容（事故 1：E48 登记时 E47 行被原地替换，缺席 5 个 commit 才被发现；事故 2：E50 登记时吃掉 E49 行首）。并发会话（fork/主）同编一表时风险加倍，提交前再核一次。

8. **parser 默认漂移 × 老 resolved_config（2026-08-29 冒烟事故）**：用 `--config <老 run 的 resolved_config.json>` 起老基座时，parser 现行默认值会填补老配置缺失的键（实例：`summarizer_pool` 默认已随 v37.3 转正为 qpool，吃 v37.1 老配置时 summarizer 6 个权重键被形状过滤**静默跳过**，水位塌到 0.05 才暴露）。纪律：① 点火老基座必须显式带上历史口径旗标（如 `--summarizer-pool mean`）；② 基座加载做全键全形校验、不齐 loud fail，禁止静默过滤。已知同款敞口：Q18 `_q18_base_config_defaults` 路径对 2026-08-23 前的基座。

9. **条款换臂必换锚（2026-09-03/04 两次同构口径错位的教训，用户裁定为明文纪律）**：判读条款从一种臂形态套到另一种臂形态时，判读基尺必须重新锚定，否则必然漏抓或冤抓——实例 ①：E120 预跑 t=0 判读线 0.5778 的参照带量的是「逐位 ridge 解混→桥」行，部署链是「固定 q_ridge 单查询→桥」行，不同源，t=0 冒烟 0.1963 冤拒发；实例 ②：冒烟条款「干净列回落 <2pp」为冻结基座臂所写，套到全解冻臂上两列皆破（对照列 direct −16.1pp、burst_tail 归零 vs 乙列 −4.8pp），回落主凶是全解冻瞬态非换件毒性，改锚「乙列回落 ≤ 对照列回落」才是「新件是否有毒」的正确语义。实例 ③（2026-09-04，种子轴）：E119 种子加固 s1 异卷地板门破（scrambled 0.1327>0.1）——口径事实=探针考场窗流随训练 seed（seed+9999，三列异卷），用 seed42 窗集校准的门判 seed1 的卷子属同款错位；同卷复测 s1 → 0.0801 过门。纪律：任何判读条款迁移臂形态（冻结↔全解冻、t=0↔N 步、格间迁移、**种子迁移**）时，先答「这条款在原臂上量的是什么」，再定新锚；换锚只放宽对应阶段的判读，臂级收官护栏不随阶段换锚松绑。**地板门/有效性门按种子各自窗流校准；异卷破门一律先同卷复测再判**（地板门测的是臂的品性，不是卷子的难度——同一类错误已换三件马甲，不能再有第四次）。实例 ④（2026-09-09，**硬件迁移**维度，枚举自此收录本维度）：E123 本地 5080 与远端 4090 同种子同码同数据，from-scratch a 格段界器跨硬件体制分盆（step 20 逐位一致排除数据/代码；step 5000 碎切 993 块/窗 vs 兜底 64 块/窗）——本地乱序对照列作废、远端同机重跑方有效；体制判词一律带「同机同 env 内成立」硬件指纹（from-scratch 考场臂特有，主线 S0'' 冻结接管免疫）。同族先例：E121 冒烟条款②「500 步逐位相同」在 GPU 并发归约下不可达 → 改锚「发散≤同码复跑地板」。
