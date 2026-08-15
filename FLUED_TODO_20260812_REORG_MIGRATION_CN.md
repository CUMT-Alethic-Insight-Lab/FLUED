# 文档重组（结构层）+ 大规模数据迁移方案（2026-08-12 主会话）

> 内部工作文件，不进镜像（文件名含 FLUED_TODO，排除清单自动覆盖）。
> 依据：库存盘点三路（2026-08-11）+ 版本文档交叉对比报告（outputs/doc_crosscheck_20260811.md）
> + 泄漏排查结论 + 用户 2026-08-12 裁定（存储布局新规）。

## A. 文档重组方案

### A.0 已完成（内容层，k2.7-code 包 #1/#2 + 主会话）

- 根 README 修 v3.4→S36 当前架构（含 Repository Map/Quick Start/Known Limitations）；
- 索引失配修复六件（configs/tools/docs/results/maintenance README）；
- v3.4 目录 README 按 supersession 链重建 + 21 篇头注规范化；
- 架构发展史落地 `docs/research/ARCHITECTURE_HISTORY_CN.md`（九阶段，指标带出处）。

### A.1 结构层动作（本方案核心）

1. **根目录内部文档归置 → `docs/internal/`**：FLUED_HANDOFF_20260717_CN.md、
   FLUED_HANDOFF_20260802_CN.md、FLUED_TODO_20260805_CN.md、
   FLUED_TODO_20260811_DOCMAINT_PROMPTS_CN.md、FLUED_TODO_20260811_DOCMAINT_PKG2_CN.md、
   session-ses_090d.md、本文件。
   - 镜像安全：排除模式按路径子串匹配（FLUED_TODO/FLUED_HANDOFF/session-），
     移入子目录不影响排除。
   - 引用更新：grep 全仓逐个改（CURRENT_STATE/TODO/规格/AGENTS.md 里的文件名引用）。
   - 分两批降风险：先历史件（HANDOFF×2 + session 导出），后活文件（TODO 族）。
2. **outputs/ 悬空引用修复**：`outputs/s05_k25_qa_spotcheck_20260802.md` 与
   `outputs/s05_pro_qa_spotcheck_20260805.md`（+样本包）迁入
   `docs/research/evidence/s05_qa/`，CURRENT_STATE 引用改路径——证据可追溯原则
   要求引用目标在 git 内。**主会话执行**（迁入即入镜像，先过内容审查：
   教师模型名/语料样本扫描）。
3. **早期版本目录（v0.4/v2/v3.0/v3.1/v3.2）**：零外部引用，保持冻结不动，
   由架构发展史做唯一入口。
4. **audit_export_20260719**（16 docx）：镜像已排除；主仓保留（冻结快照），不删。
5. **HTML**：`.gitattributes` linguist 规则止血（包 #2 Task 4 在跑），不删文件。
6. **规格不拆**（"规格 §X" 引用网遍布全仓，断链风险大于收益）。

### A.2 明确不做

- 不物理删除任何版本文档（交叉对比报告结论：无此必要）；
- 不动 `docs/CURRENT_STATE.md` / `docs/TERMS.md` 的位置与结构（守卫测试+引用网）。

### A.3 验收标准

- `py -3.14 -X utf8 -m pytest tests/ -q` 全绿；
- 全仓 grep 被移动文件的旧路径引用，零断链；
- 镜像重建 + 全词表扫描零命中；
- GitHub 语言统计不再计入 HTML。

## B. 大规模数据迁移方案

### B.0 盘位布局（2026-08-12 用户裁定 + 主会话建议项标注）

| 盘 | 角色 | 内容 |
|---|---|---|
| E: | 代码+文档核心区（裁定） | 仓库本体 |
| P: | 语料盘（裁定） | corpus_v4（原在）；corpus_v3（迁入，B.1） |
| F: | v5 构建产出（**建议保留**，用户未明说） | FLUED_corpus_v5（128.6 GiB，verify 全过） |
| N: | 原始语料源盘 | fineweb 三源 417 GiB（2026-08-12 校验真失败 0） |
| K: | 当前代归档（既有裁定） | S36 全线、保持臂等（含 SHA256SUMS） |
| L: | 历史归档只读（既有裁定） | v3.4/v3.5 及早期 v3.6 |
| W: | 格式化后承接 v3.4 及以前存档点（裁定） | 从 L: 复制（B.3） |
| 两块新盘 | 存档点备份（裁定，用户备盘） | 核心存档点清单（B.4） |
| 待定新盘 | codeparrot 重新下载（裁定） | ~280 GiB（B.5） |

### B.1 corpus_v3 迁移 E:→P:

- 源：`E:\projects\SoulMamba\soulvlm_project\temp\corpus_v3.txt`（借住他项目
  temp 目录，应迁）；目标：`P:\FLUED_corpus\corpus_v3\corpus_v3.txt`。
- 流程：复制 → sha256 双侧校验 → 更新引用 → 确认后才删源。
- 引用清单（执行时全仓 grep "corpus_v3" 核对）：训练命令 `--data-path`、
  AGENTS.md 速查表、launcher 脚本、探针 argparse defaults、canonical 配置。
  **历史文档里的旧命令不改**（历史记录保持原样），只改活配置/活脚本/速查表。
- 镜像侧：替换表 soulvlm_project→datahost_project 随路径消失而失效，新路径
  经 FLUED_corpus→MENTINER_corpus 覆盖；迁移后重建镜像+全词表扫描验证。

### B.2 checkpoints/ 仓内瘦身（E: 仓内 ~150+ run 目录）

- 三档分类：① E 编号在册 run + canonical init（S0″′ 前端）+ 基线锚 = 保留；
  ② `_probe_*`/`_interrupted_*` = 删除候选；③ 其余对照 K: 归档清单，
  已归档的删仓内副本。
- 纪律：显式清单逐个确认、禁通配符；删前清单给用户过目。

### B.3 W: 承接 v3.4 及以前存档点

- 前置（已满足）：W: 内容验证全量在 N:（265 parquet 哈希真失败 0）。
- 流程：用户格式化 W: → 从 L: 复制 v3.4/v3.5 及早期归档 → SHA256SUMS
  逐文件校验 → L: 保持只读不动。

### B.4 核心存档点清单（保留启航的最核心集合，双盘各一份）

- E 编号在册 run 的 checkpoint（E1-E57 引用件）；
- canonical init：S0″′ 前端冻结权重；
- 基线锚：H-Net 复现（BPB 0.653）、GDN-2、KDA-LM 双臂；
- S36 支柱：s36a/s36g2/s36h/s36f + 保持臂双格；
- 每盘写入后 SHA256SUMS 校验。

### B.5 codeparrot 重新下载（X: 源盘缺席后）

- 用户备好格式化盘 → 从 HuggingFace 重新下载 codeparrot/github-code
  （~280 GiB，permissive 过滤口径见配置 notes）→
  `configs/data/corpus_v5_sources_20260808.json` 的 github_code_permissive
  条目 enabled=true、root 改新盘路径 → --validate-only → 增量续跑
  （管线幂等，F: v5 已建库不重来）→ T6 代码域补标 1-2K（DeepSeek v4-pro）
  接其后。

### B.6 v4 版本号切换预案（最终形态确定后执行，用户 2026-08-12 裁定方向）

届时清单：docs/versions/v4.0/ 开门、configs/canonical_v40.json、
CURRENT_STATE 口径行切换、TERMS 登记、镜像重建同步。

## C. 时序与依赖

1. k2.7 包 #2 Task 3-5 收尾（进行中）→ 2. A.1 结构层（等用户裁定后执行）→
3. B.1 corpus_v3 迁移（等用户裁定）→ 4. B.3/B.4 等用户格式化盘/备份盘到位 →
5. B.5 等 codeparrot 盘到位。
