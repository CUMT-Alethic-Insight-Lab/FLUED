# 文档维护任务包 #2（2026-08-11，主会话整理，供新会话执行）

> 用法：新会话（k2.7-code）在本仓库根目录（`E:/projects/FLUED/FLUED`）打开，
> 粘贴 bootstrap 后按序执行。**每个 Task 完成后停下，展示 diff/产出摘要，等用户
> 确认再继续**；全部完成后由用户决定 commit，你不要自行 git commit/push。
> 本包与任务包 #1（`FLUED_TODO_20260811_DOCMAINT_PROMPTS_CN.md`）独立；#1 只
> 完成了 Task 1（README），其余已被本包吸收或转主会话处理。

## 全局纪律（每个 Task 都适用）

1. **证据表零改动**：`docs/CURRENT_STATE.md` 第 3 节证据注册表（E1-E56 行）内容
   一律不许改/删/重编号。任何涉及该文件的编辑后必须跑
   `grep -n "^| E[0-9]" docs/CURRENT_STATE.md` 核对编号 E1-E56 连续无重号。
2. **守卫测试**：每个 Task 后跑 `py -3.14 -X utf8 -m pytest tests/test_canonical_sync.py -q`
   必须全绿；全部完成后 `py -3.14 -X utf8 -m pytest tests/ -q` 全量绿。
3. **术语纪律**：项目术语以 `docs/TERMS.md` 为准；不许造新术语（需要时用中文白话）。
4. **数字可溯源**：写任何指标数字必须能在 CURRENT_STATE 证据表（E 编号）或版本
   文档里找到出处，不许凭印象写数；拿不准就留空标注"待核"。
5. **范围冻结**：只做本包列出的编辑；不碰 `flued/`、`tools/`、`configs/` 的代码与
   JSON 配置（configs/README.md 除外）；不移动、不删除任何文件（本包全是文内编辑
   与新建）；不碰 git。
6. 单一事实源：与 `docs/CURRENT_STATE.md` 冲突的表述以它为准（2026-08-11 时点）。

## Task 0：版本文档交叉对比 + 架构发展史素材（分析，先行）

产出两份文件：

1. **交叉对比报告**（内部工作件，写到 `outputs/doc_crosscheck_20260811.md`）：
   通读 `docs/versions/` 全树（43 篇 md），对主会话盘点给出的冗余组逐组做
   **内容级**验证（不是标题级）：
   - G1 消融四连稿（v3.4 的 0710 pilot / 0711 5K / 0713 20K / 0715 post-migration）
   - G2 纠偏四篇（GLOBAL_PATH_0712 / SELF_AUDIT_0714 / CORE_CORRECTION_0714 /
     RERUN_MATRIX_0714）
   - G3 memory 三反转（PROGRESSIVE_0712 / MEMORY_POSITION_0713 / POST_MIGRATION §6.1）
   - G5 归因三连、G6 CBIU 三连、G7 v3.1 同题三稿、G8 数据流三处同述
   （IMPLEMENTATION_BASELINE / SELF_AUDIT §2 / TRACE §2）
   每组给：重叠是逐字级还是互补级、各篇独有内容是什么、合并/保留建议
   （留终稿+他篇压缩为附录指针 vs 全部保留仅加头注）。**只出报告，不改文件。**
2. **架构发展史初稿**（对外质量，写到 `docs/research/ARCHITECTURE_HISTORY_CN.md`）：
   v0.4 → v2 → v3.0 → v3.1 → v3.2 → v3.3 → v3.4 → v3.5 → v3.6(S36) 时间线，
   每阶段一段：架构一句话、关键决策、核心指标（带 E 编号或文档名出处）、
   终局判词。素材来源：版本文档 + `docs/CURRENT_STATE.md` 证据表 + changelog。
   文末注明"v3.5 = v3.4 收尾系列、KDA 世代跳号 v3.6"的命名撞车说明。
   中文行文，风格对齐 `docs/research/` 既有文档。

## Task 1：索引与 README 失配修复（按严重度序）

1. `configs/README.md`：canonical_v36 标注 `v36.1-20260731` → 改为
   `v36.7-20260806`（以 configs/canonical_v36.json 与 CURRENT_STATE 第 2 节实际值
   为准，先读再改）。
2. `tools/README.md`：目录块补 `baselines/`、`maintenance/`；"当前主线入口"补
   `tools/train/v3_6/train_v36_s1.py`（canonical 入口），保留 train_v36.py 为早期入口。
3. `tools/maintenance/README.md`：补登记 `anonymize_mirror.py`（匿名镜像单向同步
   脚本，一句话即可，不写运维细节）。
4. `docs/README.md`：① "证据注册表（E1-E20）"→ E1-E56；② 待裁定队列计数与现状
   核对（多数已裁定/搁置，写"见 CURRENT_STATE 第 5 节"即可不列数）；③ 补收
   `docs/research/` 下 RESEARCH_SWEEP_20260808、COLLISION_SCOUT_S38/S39、
   `docs/data/CORPUS_GAP_AUDIT_20260807_CN.md`、audit_export_20260807；
   ④ v3.6 行表述更新为 S36 口径（逐段查询 xattn + k=1 gist + 残差门控缓存）。
5. `results/README.md`：补 `v2/` 与 `v3.6/rd_frontier_20260802/` 条目；
   "v3.6 实验归档在仓库外"措辞修正；归档盘口径补 `K:\FLUED_archive`（新）/
   `L:\FLUED_archive`（存量只读）。
6. 根 `README.md` 残余：① Repository Map 补 `flued/v36/`、`tools/train/v3_6/`、
   `configs/canonical_v36.json`、`results/v3.6/`，删 "v3_4 current entrypoint" 类
   过时措辞；② Known Limitations #5（memory "not yet confirmed…"）改为
   "memory line closed（E7/E13，512-4096B 无可测增益）"；③ Current Position 与
   Quick Start 的 v3.4 权重降压（CBIU 内容标注"历史线（已收尾）"并指向
   CURRENT_STATE）。

## Task 2：v3.4 目录 README 重建 + 头注规范化

1. `docs/versions/v3.4/README.md` 重建为 **supersession 链主结构**：按
   0710→0711→0712→0713→0714→0715→0716→0717 日期链，每篇一行（日期+标题+
   一句话+状态）；终稿三篇（POST_MIGRATION / ATTRIBUTION_MATRICES /
   CBIU_THREE_ROUND）单独标"收口文档"。既有"23 条建议阅读顺序"废止，由链取代。
2. 21 篇逐篇核对头注：缺"以 X 为准/状态"头注的补上（格式：
   `> 【状态：历史/过期】本文结论以 FLUED_V3_4_POST_MIGRATION_EXPERIMENTS_20260715_CN.md
   与 docs/CURRENT_STATE.md 为准。`），已有头注的保留不动。只加头注，不改正文。

## Task 3：v3.5/v3.6 目录 README 新建

1. `docs/versions/v3.5/README.md`：两篇（STAGED_FREEZE 设计草案 +
   PRESCALING_RESULTS），标注"v3.4 收尾系列，历史线"；含命名撞车一句说明。
2. `docs/versions/v3.6/README.md`：当前主线门脸——规格
   `FLUED_V3_6_SPEC_20260725_CN.md`（§1-§26，导读：§21/§22/§26 当前有效）、
   指向 docs/research/ 的侦察报告与 docs/CURRENT_STATE.md。

## Task 4：.gitattributes 语言统计止血

根目录 `.gitattributes` 追加（已有内容保留）：
`*.html linguist-documentation` 和 `FlashKDA/** linguist-vendored` 两行。

## Task 5：断链修复

`docs/versions/v3.1/FLUED_V3_1_SEGMENTAL_LATENT_WORKSPACE.md` 与
`docs/versions/v3.2/FLUED_V3_2_DESIGN_SUPPLEMENT_CN.md` 内有形如
`docs/versions/v3.0/docs\versions\v3.0\FLUED_V3_CONTROL.md` 的拼接错误引用，
修正为正确的仓内相对路径；修完全仓 grep `docs\\versions` 与 `docs/versions/v3.0/docs`
确认零残留。

## 明确不做（主会话/后续包处理）

- G1-G8 的合并/压缩执行（等 Task 0 报告 + 用户裁定）
- 根目录内部协作文档（FLUED_HANDOFF/FLUED_TODO/session-*）的归档移动
- HTML 文件删除（Task 4 的 linguist 规则已止血）
- CURRENT_STATE 引用 outputs/（不在 git）两份质检报告的悬空引用修复

## 验收清单（全部完成后向用户汇报）

- [ ] 每个 Task 的 diff/产出摘要已逐个展示并经用户确认
- [ ] `grep -n "^| E[0-9]" docs/CURRENT_STATE.md` 编号完整（E1-E56）
- [ ] `py -3.14 -X utf8 -m pytest tests/ -q` 全绿
- [ ] 未做任何 git commit/push；未移动/删除任何文件
- [ ] 变更文件清单 + 每个文件一段改动说明
