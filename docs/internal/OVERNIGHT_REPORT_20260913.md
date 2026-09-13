# 夜班晨报 + 压缩续命包 2026-09-13（早）

> 用途：① 给用户的一夜战果汇报；② 主会话压缩后的续命锚。判词一律留白等用户终审。
> 上一日晨报：`OVERNIGHT_REPORT_20260912.md`；操作手册：`OVERNIGHT_OPS_20260911.md`（§A 现役）。

## 一、一夜战果

### 1. Kimi Linear 复证臂三探针全收官（A79 双卡 PRO 6000，原尺寸 BF16 Base，同卷锚 a3fea9c0…，40 窗冒烟级）

| 探针 | 读数（原样） | 判读留白 |
|---|---|---|
| book 必要性账（整模，输入侧遮蔽+簇级同体半分对照） | 40窗/用30；selected n=130 mean Δ=−0.0008 nat；contrast **−0.00055 nat CI[−0.0019,+0.0005] 含 0**；n_strong=0；诱饵审计零违例 | CI 半宽 ~0.001 nat，比 DeltaNet +0.28 小两个数量级；但 MLA 7 层在场=整模测量混读者（任务书逃逸口条款在案） |
| surgery KDA 状态置零解离（全 20 KDA 层置零） | 40窗/用12；remote n=194 +0.00757 vs local n=97 +0.00071（remote≈10× local）；contrast +0.0069 CI[−0.0083,+0.0225] 含 0；n_strong=1 | 方向对、剂量不足（28/40 窗空）；仪器自述转 500 窗/换层集 |
| readout KDA 状态闭式读出（哨兵全过 max rel_err 0.0051«0.05） | 40窗/用39，n_samples=169；remote_j0 cos uplift：**early（层0-8）+0.0166，min p=0.00024，6/7 层 p<0.05**；mid +0.0068（2/7）；deep +0.0072（1/6）；near_lag1 阳性对照全层组 +0.013~+0.027 | 信号最強在 **early** 非 deep |

**仪器文案两勘误（2026-09-13 午已修，数据不动）**：
- book 的 verdict 串误写「DeltaNet 跨架构复证未过」（实为 kimi122 臂）——根因=复用 DeltaNet 臂 verdict 函数；已改本地 `_verdict_kimi`（混合架构逃逸口全限定措辞）；
- readout 的 verdict 自称「深部 KDA 层远程内容线性可读」，与自家 layer_groups 数据（early 最强 6/7 层）不符——已改按层组多数显著性点名（实测仅 early 显著）；存量 summary.json 的旧 verdict 串不回刷（数据字段为准），代码修复见本日 commit。

产物：本地 `outputs/kimi_probes_20260913/`（15 文件 716K，三 summary+items+probes+samples 齐）；远端 A79 `/root/autodl-tmp/outputs/kimi_probes_20260913/` 同份。

### 2. 连夜三 bug 修复（commits e1ef4dc / a9b5029，测试 814+4 全绿，已推）

1. `kda_chunk_boundary_states` 入口挤 B=1 batch 维（捕获直出 [1,T,H,*]；非 1 batch 响亮 ValueError）；
2. surgery `build_window_sums`+items 写出坐标系错位（nll_* 是 suffix 局部坐标，j=t−split）；
3. readout `states_all` 按捕获序返回而主循环用绝对层号索引（层 24/25 越界）→ `map_states_to_layers` 映射+层数响亮校验。

各带回归测试。附坑入册：bash `echo "...$(date)... exit=$?"` 的 `$?` 被命令替换吞成 0——退出码必须先存 `rc=$?`。

### 3. E124 链：面具 log 收官 → 密度闸门过线 → 四列点火（在跑）

- 面具 log：10000/10000 窗、29839 遮蔽 chunk（2.984 块/窗）、42.4h、sha256 `276c2e69b749418d6778e2c58b24de284575fe0b8db7636556535d937d338906`、字段审计全过（cand_mode=random / cand_seed=20260911 / hw=4090）。
- **密度闸门：73.93 B/窗 ≥ 54.8 过线**（口径=逐窗 Σ(src_byte_range 末−初+1)；与定稿预期 71B/1.30× 吻合）——不需剂量重裁。
- 四列串行（5080，驱动 `outputs/_e124_ignite_4cols.sh`，任务 bash-6mqi5eqd，11:02 全收官 E124_4COLS_ALL_DONE，全 rc=0 零 NaN）：comb（07:26 点火，60min：**eval_direct_acc 0.7486 / eval_backbone_acc 0.6957 / eval_loss 2.035 / masked 0.1163**）→ gate（08:25，55min：**0.7629 / 0.7076 / 1.957 / masked 0.1109**）→ demand（09:20，55min：**0.7561 / 0.7026 / 1.978 / masked 0.1120**）→ cont（10:15，48min：**0.7591 / 0.7053 / 1.965 / masked 0.1166**）。
- 列间双标志硬校验（summary.json+latest.pt），断列即断链报用户；基座全键全形校验每列过（loaded=287）。

### 4. E124 五仪表雏形读数包（11:20 落地，agent-210 施工+跑数，判词留白）

仪器 `tools/analysis/v3_6/readout_e124_five_instruments.py`（commit `ce72b4d`，本地未推；测试 seam4+gate6+新9 共 19 绿），产物 `outputs/e124_readout_20260913/<instrument>/<run>/{summary,items}`（5×4=20 组，eval 流+seed1042+硬门终点姿态，16 窗同卷）。覆盖：①②③⑤ 仅 comb/gate（demand/cont 无门结构 skip，原因已入各 summary）；④ 四列全。

- **① RD 曲线**：comb/gate 全档平（comb k=1→0.6951、k=9→0.6957、k=173→0.6959；gate 同形），无拐点亦无塌；k=173 档 16 窗中 11 窗 bypass（n_real<173，语义=全量读锚点）。
- **② K 侧置乱 Δ**：comb 五档 Δmasked≈+0.0445（CI 全不含零）、**Δoverall≈+0.607**（置乱后 backbone 整体塌到 ~0.089）；gate 同形（+0.039/+0.621）。
- **③ 位置先验**：k=9 命中集 vs 因果最近-k 预测器重合率 comb 0.2150 / gate 0.2251（完全命中率 ~0.056）；lag0 占 25.2%（comb）/34.8%（gate）。
- **④ 遮蔽位读出**：收官 eval 锚 comb 0.1163 / gate 0.1109 / demand 0.1120 / cont 0.1166；自锚地板 majority 0.0974 / uniform 0.0039 → gap comb +0.0190 vs **cont +0.0192**（同水位）。注意前提偏差：train_log 无 eval 行（评估只在收官跑一次），轨迹段是训练姿态步点（峰值 comb 0.1968 后回落），eval 姿态只有收官锚——仪器 summary 的 log_note 已分标未混充。
- **⑤ 消融双跑**：先行对拍逐位过。**仪器语义勘定（主会话审计 model.py:1844）：`allowed | diag_eye` 对角护栏 → 全局臂实为「仅自读」而非「全剔」**。comb：全局 Δmasked=−0.0020（CI 含零）/Δunmasked=+0.0031；定向 Δmasked=+0.0006/Δunmasked=+0.0004；direct 腿全零（构造性不读 store）。
- ②/⑤ 张力已解：读错行剧毒（−0.607，V 读出内容敏感的铁证）vs 仅自读几乎无损（−0.003）——**backbone_acc 几乎全由对角自读承载**；两读数不矛盾，但 ⑤ 的「全局」字段名与真实语义不符，判读时必须带此注记。

待用户终审：五面判读（任务书 §4 主判据组合 + §5 结局格）、条件列裁定（阳性才跑乱序 5K）、种子 {1,2}。

## 二、机器状态（09-13 早）

| 机 | 状态 | 说明 |
|---|---|---|
| 本地 5080 | **E124 四列在跑** | ~62min/列，~11:40 全收官 |
| A79（15970，双 PRO 6000） | **已关机**（GPU 计费停，磁盘留 15 天释放窗） | 三探针产物已回拉；98G Kimi 权重在数据盘。无卡模式菜单 webbridge 合成事件吃不进（Ant Design portal），要 ssh 存取就控制台一键「更多→无卡模式开机」 |
| 4090（60222，flued_partner_ed25519） | 面具 log 进程已自然退出，机在闲 | 语料/repo 在机 |
| B26 / A39 | 已关机 | 无任务 |

## 三、待用户裁定（判词留白清单）

1. **Kimi 三探针读数定性**——尤其 book 的近零（−0.0006±0.001）vs DeltaNet +0.28 的对置怎么进叙事（混合架构逃逸口条款已自我援引）。
2. **E124 四列收官判读包**（五仪表：RD 曲线/k_rows 置乱/位置先验/遮蔽位读出/定向消融）——收官后我出雏形，判读初稿审核+红队裁决是用户权。
3. 数学线悬念：b 格「第二个零参数命中」升格已被 agent-209 证伪（h3 不独承重）；γ 谱≈init 谱（门控没被训练动过）——理论侧裁。
4. d1 翻负判别件（全窗一致 vs 子集驱动）排 E124 收官后判读间隙做。

## 四、压缩续命锚（给压缩后的我）

- **现役 cron 只有一台**：`:13`（01M289CWA089BP04662BEY6BQ1）= §A 监控四列（train_log 尾+NaN+进程+GPU；E124_4COLS_ALL_DONE → 五仪表雏形 → 原样报）。:33/:47 已删（push 兜底完成、Kimi 链完结）。
- **四列收官后动作**（§A 步骤 8）：五仪表雏形判读（RD 曲线/k_rows 置乱/位置先验/遮蔽位读出/定向消融）→ 读数原样报用户，判词留白。E124 判读后紧接：条件列裁定（阳性才跑乱序+纯续训 5K）、种子 {1,2} 加固排队。
- **测试基线 814+4**；证据表 123 行（`grep -c "^| E[0-9]* |" docs/CURRENT_STATE.md` 核对）。
- Git 已推净（至本晨报 commit）。再断连照旧挂每小时兜底 cron（推成自删）。
- 用户授权「先斩后奏」有效期至 09-13 中午；之后判词级动作恢复停等。
- 摘要死线 9-18、go/no-go 9-21、全文 9-25。复证臂现状：DeltaNet 必要性账+闭式读出已收官（+0.2806 / 24层全显著）；Kimi 三探针 40 窗冒烟级已收官（上文）——9-21 前条件触发件=surgery 转 500 窗（若用户裁）。

## 五、09-13 午：A79 无卡复机 + 150M 两列规格空缺立案

**A79 复机经过**：webbridge 控制台灯「开机」→ 主机 0 空闲 GPU（按量计费关机即释放 GPU，已被他人租走；对话框给三选项=克隆/无卡模式/等释放）→ 按「无卡干活、挂卡等裁」教义走**无卡模式开机（¥0.10/h）**。ssh -p 15970 凭证沿用有效。webbridge 坑两条入册：①后台标签 rAF 节流 → 动画卡 enter-from/按钮零尺寸/setTimeout 假死 300s；②窗口变窄后按钮在视野外（x=1909 > vw=1072），CDP 坐标打空。定式=截图定场 → scrollIntoView(inline:center) → CDP trusted → 卡死就 Page.bringToFront → 菜单走键盘（focus→Enter 开→CDP 点项）。

**数据盘核验（全绿）**：

| 件 | 状态 |
|---|---|
| corpus_v3.txt | 23,777,636,695 B + VERIFIED.sha256（ed4ab978…c0fce）✓ |
| 150M 三 seed 基座 | latest.pt+resolved_config+summary+train_log ×3 ✓ |
| repo | bundle 同步 fa1554f→**de79f59**（=本地 HEAD），py_compile 过 ✓ |
| e124_mask_log_seed42.jsonl | 上传，sha256=276c2e69…338906 与登记值逐位一致 ✓ |
| bpe_tokenizer_128k_v4 | 在机 ✓ |
| GPU/torch 环境 | 无卡模式无 GPU；torch env 不在 base conda，挂卡时核（150M 训练世代 env 位置待查） |

**150M 两列规格空缺（立案待裁）**：E124@150M 两列无冻结任务书，E124 已阴性（自读旁路格/no-go），施工岔路不可避免：

- **方案 A（钉切点复用 44M 面具 log）**：e123_cuts_pin=true 使窗流/切点/遮蔽与 44M 四列逐位相同（172.7 chunk/窗，k_final=9 照用）——最干净的 scaling 复刻；但 150M 基座 20K 在自身 64B 退化网格（64.0 chunk/样本、hard_cut≈0.0002、boundary_conf −0.999，summary 实测）上训出，起点语义与钉入的 S0'' 切点错配（44M 列的 s0pp 基座原生适配 S0'' 切点，无此污染）。
- **方案 B（150M 原生分段+新面具 log）**：与 150M 前置门（+0.00385）同体制；但 64 chunk/窗检索几何变（k_final=⌈64×5%⌉=4），密度账/退火表全数重推导，且制 log 估 20-40h（44M 的 42.4h/10K 窗 @4090 参照）。
- **成本表**：A=两列 10K×2，~1.5-2 步/s → ~3-4h ≈ ¥42-56；B=制 log ¥280-560 + 同 A；缓行=0（R2 DeltaNet-50M 进体制换序提前，卡A 语料/repo 已就绪，R2 是 TMLR 转向后更承重的件——三轴混淆第一刀/死法二终极版）。
- 队列史：R2 注册时排序在 150M 两列后（09-12 用户裁定），该排序先于 E124 阴性判词。

**机器现状**：A79 无卡运行中（¥0.10/h，ssh 15970）；A39/B26 关机（**A39 主机有「GPU充足」标**——若急用 GPU，A79→A39 同区互传或再克隆是加速候选，数据盘 81.6% 满余 ~31G）；4090/5080 空闲无排产。GPU 监视 cron 已挂（A79 行出现「GPU充足」→ 报用户）。

**待用户裁定（新）**：150M 两列=A/B/缓行三择；GPU 出现时是否直接挂卡烧 A（若裁 A 且授权挂卡即烧，回话「挂卡烧 A」即可全自动链：挂卡→冒烟四条款→两列串行→判读包）。
