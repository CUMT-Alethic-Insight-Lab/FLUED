# 文档维护任务包（2026-08-11，主会话整理，供新会话执行）

> 用法：新会话（k2.7-code）在本仓库根目录（`E:/projects/FLUED/FLUED`）打开，
> 粘贴 bootstrap 指令后按序执行。**每个 Task 完成后停下，展示 diff 摘要，等用户
> 确认再继续下一个**；全部完成后由用户决定 commit，你不要自行 git commit/push。

## 全局纪律（每个 Task 都适用）

1. **证据表零改动**：`docs/CURRENT_STATE.md` 第 3 节证据注册表（E1-E56 行）
   内容一律不许改、不许删行、不许改编号。任何涉及 CURRENT_STATE.md 的编辑后，
   必须立刻跑 `grep -n "^| E[0-9]" docs/CURRENT_STATE.md` 核对编号清单
   （E1 到 E56 连续无重号无缺行），两次事故教训（E47 被整行覆盖、E49 行首被吃）。
2. **守卫测试**：每个 Task 完成后跑 `py -3.14 -X utf8 -m pytest tests/test_canonical_sync.py -q`
   必须全绿；全部 Task 完成后跑全量 `py -3.14 -X utf8 -m pytest tests/ -q`。
3. **术语纪律**：行文用到项目术语以 `docs/TERMS.md` 为准；不许造新术语
   （确有必要时在行文用中文白话，不登记）。
4. **范围冻结**：只做本包列出的编辑，不顺手"改进"其他内容；不碰 `flued/`、
   `tools/`、`configs/`、`tests/` 任何代码与配置。
5. 单一事实源原则：凡与 `docs/CURRENT_STATE.md` 冲突的表述，以 CURRENT_STATE 为准。

## Task 1：README.md 修复（v3.4 → 当前架构）【最高优先，匿名镜像同步前置】

现状问题：README 的架构详述停在 v3.4（"FLUED v3.4 Architecture" 整节），
v3.6 表格行还是 k=1 时代旧口径（已被 S36 取代）。

先读（按序）：`docs/CURRENT_STATE.md` 第 2 节（canonical 默认）+ 第 3 节
证据表 E36 起各行 + 第 6 节 changelog 末尾、`FLUED_TODO_20260805_CN.md` §0.3、
`AGENTS.md` 的架构段。

修复规格（保持 README 既有英文行文风格与整体结构，最小侵入）：

1. **架构段更新为当前主线形态**（事实以 CURRENT_STATE 为准，以下为
   2026-08-11 口径摘要，供直接采用）：
   - 当前主线 = v3.6 线 S36 形态：encoder = segmentor（S0″ 双源教师标注
     预训、冻结接管）+ DiT summarizer（段→memory 行）+ interpreter
     （KDA 状态机）；主干 = 逐段查询 xattn（严格因果）+ k=1 gist token +
     残差门控精确缓存（解码 CE 判据）；训练入口
     `tools/train/v3_6/train_v36_s1.py`，canonical `configs/canonical_v36.json`（v36.7）。
   - 最强数字（工程口径，单 seed）：s36g2（4096B/batch4）backbone 0.8134
     全线最高；s36a（512B）0.7981；P0 评测集 RULER needle 还原 0.848；
     v4 域外语料复现三臂一致。
   - 关键判词：0.206 平台死因 = 固定单查询取址墙（E50）；存储冗余律
     512B/2048B 冗余、4096B 拐点 +1.78pp（E55）；基线锚 H-Net 复现
     BPB 0.653 / KDA-LM 1.80 / GDN-2 1.828。
   - 进行中：S39 档案馆内容寻址远程查询接口（规格 §26 预注册，
     `docs/versions/v3.6/FLUED_V3_6_SPEC_20260725_CN.md`）。
2. **v3.4 架构详述节压缩**：保留节标题与 3-5 句定位摘要，细节引导到
   `docs/versions/v3.4/README.md`（版本文档不动）。
3. **版本表**：v3.6 行改为 S36 口径（上摘数字）；v3.4/v3.5 行保留。
4. 顶部"当前状态唯一事实源"指引保留不动。

## Task 2：CURRENT_STATE.md 拆分 changelog

现状：文件 638 行，其中第 6 节 changelog ~490 行（77%），且只会继续涨。

执行：
1. 新建 `docs/CURRENT_STATE_CHANGELOG.md`，头部写：本文是 CURRENT_STATE.md
   第 6 节的迁出存档（2026-08-11 拆分），维护规则同源（新证据落地必须追加
   带日期记录）；迁入全部 changelog 条目（2026-07-17 起全量，逐字搬迁不改写）。
2. 原文件第 6 节保留节标题，替换为：指向新文件的一行指引 + 最近 3 条
   条目原地保留（2026-08-10/08-11 的三条）。
3. 第 1 节维护规则第 1 条中"并在第 6 节 changelog 追加一行带日期的记录"
   改为指向新文件；全文 grep 检查其他对"第 6 节"的引用并同步修正。
4. 完成后跑全局纪律第 1、2 条检查。

## Task 3：FLUED_TODO_20260805_CN.md 瘦身

原则：只压缩带明确关闭标记的块，活项一字不动。

1. §0（v36.3-attn 时代最强数字快照）：整节已带"作废标注（2026-08-07 审计 B3）"
   ——压缩为 2 行：指向 CURRENT_STATE 证据表 + 作废说明保留。
2. §0.1（基线裁定三选项）：已被规格 §21 正本改写——压缩为一行指引。
3. §0.2 队列第 1-6 项（全部标"已闭环/已推翻"）：每项压成一行结论+证据号
   （如 E33/E34/E41/E36/E39），细节不保留（在 CURRENT_STATE 里有全文）。
4. §1 讨论已定论项、T1（已闭环）：各压成一行。
5. **不动**：§0.3（接力锚点）、T2/T5/T6、§2 待办、§3 环境速查、§4 生成线
   （含作废标注的段落保留标注本身）。

## Task 4：规格文档**不拆**，只加导读

`docs/versions/v3.6/FLUED_V3_6_SPEC_20260725_CN.md`（928 行，§1-§26）不拆分
——"规格 §X"的交叉引用遍布全仓（CURRENT_STATE/TODO/侦察报告），拆开即断链。
改为在文件顶部（标题后）加一段 10 行内的导读：① 单一事实源是
CURRENT_STATE.md，本文是决策与预注册记录；② 当前有效设计：§21（k=1 正本）
/§22（智能密度纲领）/§26（S39 预注册，最新）；③ §13-§20、§23-§25 为已闭环
的历史决策记录；④ §1-§12 为原始规格，多处已被后续节修订。

## Task 5：docs/README.md 索引核对

读 `docs/README.md`，核对索引与实际文件一致（重点：新建的
`docs/CURRENT_STATE_CHANGELOG.md`、`docs/research/` 下 2026-08 新增报告），
缺的补上、指向错误的修正。行文风格与现有一致。

## 验收清单（全部完成后向用户汇报）

- [ ] 每个 Task 的 diff 摘要已逐个展示并经用户确认
- [ ] `grep -n "^| E[0-9]" docs/CURRENT_STATE.md` 编号完整（E1-E56）
- [ ] `py -3.14 -X utf8 -m pytest tests/ -q` 全绿
- [ ] 未做任何 git commit/push
- [ ] 变更文件清单 + 每个文件一段改动说明
