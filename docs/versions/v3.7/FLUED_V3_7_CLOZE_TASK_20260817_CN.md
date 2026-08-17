# FLUED v3.7 — cloze 检索回执任务（第四任务）口径注记

- 裁定日期：2026-08-17（用户裁定；立项记录见 `docs/CURRENT_STATE.md` 2026-08-17（十五））
- 实现：`tools/train/v3_6/train_v36_s1.py`（cloze 段 + `step_model` 接线）、`tools/train/v3_6/train_v36.py`（三个 CLI 旗标 + 旧训练器响亮守卫）
- 单测：`tests/test_v37_cloze.py`；fixture 题库：`tests/fixtures/cloze_bank_tiny.jsonl`（20 条）

## 1. 动机

E64/E66 实锤：现有三任务（direct / 累积 masked 补全 / predict latent）在 4096B 窗内不产生检索压力，K（index）通道零承重。cloze 检索回执把"查不到就丢分"直接写进梯度：窗尾的回执答案被遮罩，唯一信息源是窗前 60% 处插入的 passage——补全条件行必须经 block-1 cross-read 从存储里把答案检索回来。

## 2. 任务形态（钉死口径）

1. 以概率 `--cloze-prob`（默认 0.3；**旗标默认 0.0 = 关闭**）对窗内样本做一次 cloze 拼接：
   - 从题库（`--cloze-bank` JSONL，`tools/data/mine_cloze_bank.py` 契约：`{"id","passage","answer","query","answer_bytes"}`，passage 96–192B、answer 28–36B、query=passage 里 answer 换成恰好一个 `___`）均匀抽一条；
   - passage **插入**原窗有效字节前 60% 的均匀随机字节偏移处（前向 snap 到 UTF-8 字符边界）；
   - 窗尾追加 `\n` + query + `\n答案是：` + answer；**echo 跨度 = 追加尾的 answer 字节段**（约 32B，回执本体）。
2. 编码时掩码覆盖（在常规 mask 生成之后施加，E23 纪律）：
   - passage 内 answer 跨度 **force-UNMASK**——回读测的是已编码内容的保持；
   - echo 跨度 **force-MASK**——不许从窗尾直接抄答案。
3. 损失：echo 跨度各槽位的字节 CE，条件行 = echo 所在 chunk 的主干补全行（与 masked 补全任务同形态，复用同一份 `decoder(backbone_out+pos)` logits 与补全目标网格，Markov 头修正后的最终 logits）。权重 `--cloze-weight`（默认 0.3）**加在**三个主任务之上，不改三任务权重。
4. 指标（train_log 与 eval summary 同schema）：`cloze_loss`、`cloze_byte_acc`（echo 槽位字节命中率）、`cloze_exact`（整段 answer 全对，对命中样本取均值）、`cloze_count`（本窗是否命中，batch 均值即命中率）。任务关闭或无命中样本时为 0 占位（同 codec_final 的 predict 占位纪律）。

## 3. 截断与跳过口径（实现裁定，主会话复核点）

拼接后窗口**允许略超 seq_len**：批次张量按拼接后最大行长加宽、PAD 补齐（v3.7 前端无字节级位置嵌入，chunk_pos 按 max_chunks=1024 配备，4096B+~430B 拼接窗约 283 chunk 远在容量内）。**echo 必须完整落在 chunk 网格内才算数**：任一字节被打包截断（`chunk_ids=-1`/越界）则该样本跳过本任务（cloze_count=0），拼接内容仍服务三个主任务。备选读法（拼接后按 seq_len 截断张量）在满窗语料下 echo 必丢、任务永死，与任务目的冲突，未采用。

## 4. 随机性与确定性

- 专用 CPU 生成器 `_CLOZE_GENERATOR`（与 `_MASK_GENERATOR` 同纪律）：训练由 `args.seed + 101_003` 播种；eval 由 `args.eval_mask_seed + 101_003` 播种（同源固定种子，偏移只为与 mask 流去相关）。逐样本固定抽签序：选中 uniform → 题库序号 → 插入偏移。
- 关闭时零侵入：不消耗任何 cloze RNG、不加宽张量、不改 mask，损失/指标逐比特等于旧路径（单测①锁定）。

## 5. 防捷径设计

- echo force-MASK：窗尾答案不可见，补全行无法从本 chunk 的 V 行抄到答案，只能检索。
- passage answer force-UNMASK：答案以已编码形态进存储（E23 口径），测的是保持+寻址，不是掩码推理。
- 题库侧特异性过滤（挖掘脚本裁定）：answer 含 ≥2 数字/专名样大写/非常见符号至少其一，排除纯虚词——防"不用检索也能蒙"。
- answer 起点落在 passage 的 25%–60% 字节区间：前后必有上下文，定位答案必须读 passage 本体。
- 损失只挂在 echo 槽位、条件行走补全主干行：不引入新参数模块，`build_model` 不动。

## 6. 响亮报错矩阵

- `--cloze-prob>0` + 非 slm 主干（xattn/paged_xattn/draft/attn/mlp）：`main()` SystemExit + `step_model` ValueError（双保险）。
- codec_final/paged/draft/prefix_task 与 slm 的既有互斥报错（`train_v36_s1.py:951-965` 模式）先行触发；cloze 检查文案显式点名这些组合 N/A。
- `--cloze-prob>0` 缺 `--cloze-bank`：SystemExit；题库契约违例：`_load_cloze_bank` 带行号 ValueError。
- `train_v36.py`（旧训练器）传 `--cloze-prob>0`：SystemExit 指向 S1 训练器（cloze 只在 S1 接线，不放任静默无效）。

## 7. 旗标速查

| 旗标 | 默认 | 含义 |
|------|------|------|
| `--cloze-prob` | 0.0 | 每窗 cloze 拼接概率（0 = 关闭，逐比特零侵入） |
| `--cloze-weight` | 0.3 | cloze 损失权重（加性，不压三主任务） |
| `--cloze-bank` | "" | 题库 JSONL 路径（开启时必填） |

正式 a/b 两格训练命令行见主会话安排（v37.2 口径：seed_source=k 默认，cloze 旗标叠加在 canonical_v37 之上）。
