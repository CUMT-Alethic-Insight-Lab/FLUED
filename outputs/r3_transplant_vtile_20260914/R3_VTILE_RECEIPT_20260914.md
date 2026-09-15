# R3 丙臂（S0'' 段界器移植 = c1 变长铺瓦）施工与前置门回执

- **日期**：2026-09-14 → 2026-09-15（施工 agent；任务书冻结 v1.0；用户 2026-09-14 指令：5080 不得闲置——本条即 §9.6 承载机开口项对丙臂的修订，4090→本地 5080；20K 主列跨夜 21.08h 于 09-15 收官，判决账同日收官）
- **任务书**：`docs/versions/v3.7/FLUED_V3_7_R3_DELTANET_TRANSPLANT_DRAFT_20260914_CN.md`（冻结 v1.0，§2.3 丙臂 c1 主构造逐字执行）
- **靶机**：**本地 RTX 5080 16G**（env `kda-kernels`：torch 2.13.0+cu130 × triton 3.7.1 × **fla 0.5.2** × transformers 5.14.1 × py 3.12；import 须 `-X utf8`）。**env 指纹与 4090 有 skew（4090=fla 0.5.1/tf 5.15.1/torch 2.12.1）——跨硬件/env 只比方向，读数一律带「同机同 env 内成立」硬件指纹（坑 9 实例④维度）。本 env 兼 FlashKDA 活，全程零改动。**
- **本地 commit 链**：`c281145`（丙臂施工件五文件）→ `0212fcb`（loader 修复：prefix_task/prefix_positions 按 gate2base 在册口径补默认）→ `eb24b15`（无 accelerate 本地装载器 + 启动器/对拍门接线；对拍门全绿）→ `966f78f`（c3 附带件启动器）
- **单源纪律**：`r2_spec.py` 零改动；仪器本体 `tools/analysis/cross_arch/probe_e122_deltanet_book.py` 零触碰（sha256 见门③）；丙节单源 `r3_spec.py`（VTILE_* 节）；新增件全部旗标化（`--vtile` 默认关=不 patch、不建任何东西、**零新增参数**）。
- **语料核验**：`P:\FLUED_corpus\corpus_v3\corpus_v3.txt` sha256 前 16 = **`ed4ab97810776ce7`** ✓（23,777,636,695B 全等）。

---

## §0 施工形态（门①体制核验・file:line 证据）

### §0.1 原件因果角色（§2.0 ①）

S0''=规则蒸馏教师段界器，冻结接管（canonical_v37；权重 `K:\FLUED_archive\s0pp_pro_v4_sft_20260805\latest.pt` 在场 ✓；架构=byte encoder 3 层+segmentor 9×DiTStyleBlock+LayerNorm/Linear 头，boundary_mode=dynamic/temp 0.15，flued/v36/model.py:2431–2434；在册运行点 ~24B/块、172.7 块/窗=E124 门②训练流在册数）。**独立于宿主干网**：只吃原始字节窗、吐切点，无需域适配。毒性链经「变长块→逐块状态行→摘要→寻址」表达；纯线性宿主无这些挂点——c1 构造=把 DeltaNet WY 计算铺瓦从原生 BT=64 改为按 S0'' 切点的变长（chunked delta rule=线性递归的代数精确重排，铺瓦粒度不改函数，逐位差仅 fp 结合序）。

### §0.2 移植构造施工形态（§2.0 ②）

**变长铺瓦（c1 主构造）**：按 S0'' 切点把 WY 铺瓦从原生 BT=64 换成变长段。施工 file:line（fla 0.5.2 于本地 env `C:\Users\74090\Miniconda3\envs\kda-kernels\Lib\site-packages\fla\`；丙件于 `tools/baselines/deltanet_r2/`）：

| 件 | 位置 | 内容 |
| --- | --- | --- |
| tap 点 | patch `fla.layers.delta_net.chunk_delta_rule` 模块级名字（`r3_spec.py:741-745` `_vtile_patched_chunk_delta_rule`；fla 0.5.2 `layers/delta_net.py:20` 模块级 import、`:261` 层内 chunk 模式调用点，全 kwarg 传参） | 唯一 tap；零权重改动 |
| 变长核 | `r3_spec.py:706-738` `vtile_apply`：plan=None 逐位直通原生；否则按段长表切 T 维、逐段 `orig(...)` 并以 **initial_state/final_state 接力**（bf16 handoff=原生 chunk 间状态精度语义；末段 final_state 缺席=核契约漂移响亮停） | fla 0.5.2 核暴露 initial_state/final_state 且 backward 返 dh0 → **逐段接力全链 BPTT 可导，零自写核**（实现路径勘定结论） |
| 计划上下文 | `r3_spec.py:684-703` 模块级单例 `_VTILE` + `set/clear_vtile_plan`（未挂接态设置=响亮停；空/非正/非整/与 T 不齐=响亮停） | 训练器/启动器逐窗 set、前向毕 finally clear（防跨窗泄漏） |
| 挂接/摘挂 | `r3_spec.py:748-788` `attach_vtile`（核验宿主 attn_mode=='chunk' 契约）/`detach_vtile`（patch 场被第三方改写=响亮停） | enabled=False 分支核验无 patch/计划残留后原样返回=与 R2 母列逐位不变路径 |
| S0''→token 计划 | `r3_spec.py:796-859`：`byte_char_boundaries`（前缀解码语义：净窗增量快路径/违例窗逐前缀慢路径）+ `token_plan_from_byte_cuts`（round-right 映射规约：byte 切点 b→字符位 c→首个 start_offset≥c 的 token；byte-0 窗起点标记跳过；BOS 位跳过；去重；段长=相邻边界差） | 映射规约随 config.r3_vtile 落盘 |
| S0'' 装载 | `r3_spec.py:867-918` `load_s0_segmentor`：canonical_v37.json+{seq_len 4096, max_chunks 1024}（ctx4096 口径，E124 门② 172.7 运行口径）建 FLUEDV36，前端四前缀（byte_lookup/encoder_blocks/segmentor_blocks/segmentor_head）strict 形状校验+载入后逐位复核+freeze+eval | `s0_cut_bytes`（:921-942）= v36 `_encode→_cuts` 在册语义（tau_cut 0.94+utf8 续字节过滤+capacity-safe）；容量溢出响亮停 |
| 训练旗标 | `train_deltanet_r3.py:65-67`（`--vtile` store_true 默认关；与 --echo/--summ 两两互斥 loud-fail，:80-83）；`:130-132` attach+stamp；`:325-335` 逐窗计划接线（t_total=len(ids)−1，x/y 错位口径）；`:359-362` log 加 n_segs/n_cuts_byte 仅旗标开时 | 旗标关路径零新增字段（逐位验收合同不受影响） |
| 坑 8 装载 | `r3_spec.py:986-1019` `verify_vtile_reload`（丙特化：零新增参数→**键集=基座全等** loud-fail + 参数锚 48,152,896 + 全量 strict 重载）；`attach_and_reload_vtile`（评测装载器） | 多出/缺失任一键即 RuntimeError「不点火」 |
| 评测装载 | `probe_r3_vtile_book.py`：替换仪器模块级 `load_model_and_tokenizer`（本地装载器）+ `run_window`（逐窗计划注入，a/b1 两臂同一计划=等长 gram 替换保持 T 与位置，计划按位置索引精确迁移）两接缝；逐窗 S0'' 统计落 vtile_window_stats.jsonl | 仪器本体零触碰；窗/选择链/手术/bootstrap/种子全走仪器本体 |
| 本地装载器 | `r3_spec.py:1022-1065` `load_model_and_tokenizer_local`：本地无 accelerate（不许改 env），仪器本体 device_map 路径不可用→`.to(device)` 单卡放置等价；fla 先注册/SDPA shim/两处 _tied_weights_keys 规范化/bf16/eval/use_cache=False/指纹字段逐项等价 | 唯一差异=device_map→.to（无分片，NLL 语义零影响） |

### §0.3 不同构点清单（§2.0 ③，判读引用必带）

1. **函数恒等预期本身**（§4 丙混杂注记在册）：chunked delta rule 是线性递归的代数精确重排，变长铺瓦数学上不改函数——预注册判词预期=不杀；杀=「铺瓦敏感性」真发现，归因改写。
2. **实现路径耦合**：移植件=计算铺瓦重排（零参数、零权重改动），与原件的语义表达链（变长块→状态行→摘要→寻址）**不同构**——本臂排空的是「计算铺瓦粒度」嫌疑维度，不是段界器的语义挂点（那是 (c2)，另立项）。对拍门兜底实现正确性。
3. **段边界来源域**：S0'' 在 byte 空间切（~24B/块在册口径），宿主在 token 空间铺瓦——byte→char→token round-right 映射为规约性投影（§0.2 表）；token 空间段数 ≤ byte 切点数（多 byte 切点并入同一 token 边界，只少不多）。
4. **段内粒度**：段内仍走原生 BT=64 chunk 核（fla 仅收 16/32/64）——「变长」变的是**状态接力边界**，不是段内铺瓦粒度（恒 64=母列粒度）。
5. **硬件/env 维度**（坑 9 实例④同款）：5080×fla 0.5.2×tf 5.14.1×torch 2.13.0 vs 4090 在册指纹——判决账与母列基尺 +0.1040 的比较带硬件指纹注记；意外判死须回 4090 重锚（预注册规则）。

### §0.4 新增参数（§2.0 ④）

**零新增参数**（参数锚 48,152,896 与 R2 母列全等；白名单=空集，checkpoint 键集须与基座全等 loud-fail）。`r2_spec.py`/仪器本体/fla 库文件零修改。

### §0.5 实现路径勘定结论（任务书 §2.3「实现路径先勘定再动工」）

fla 0.5.2 `chunk_delta_rule` **暴露 initial_state/final_state 接口**（`fla/ops/delta_rule/chunk.py`；backward 返 dh0）→ 逐段状态接力全链 BPTT 可导，**零自写核**（masked-tile 备选路径未触发）。数学恒等实证（tests/test_r3_vtile.py 真机用例）：T=640 66 段变长 vs 原生 max|Δo|=3e-3（bf16 噪声带），四路梯度相对差 ≤1.2e-2；in-family 定标=fla 自身 BT64→BT32 粒度差 max 0.203/mean 0.0225，vtile 偏差同量级 1.26×=纯 fp 结合序证据。

---

## §1 丙前置特有件：函数恒等对拍门——**PASS**（先于一切，零训练）

`probe_r3_vtile_parity.py`（R2 母列 20K ckpt 上同窗对拍原生 BT=64 vs 变长铺瓦 NLL；E121 逐位/容差双档先例）：

- **逐位档（直通洁净性）**：挂接态 plan=None 直通 vs 未挂接原生，窗 0 逐 token NLL **逐位相等** ✓。
- **校准档**（8 窗，_uniform64=变长铺瓦跑均匀 64-token 段=与原生同铺瓦网格，隔离「接力 bf16 cast」单一机制）：max|Δ_uniform64| = **5.07e-4** → TOL = max(10×5.07e-4, 0.02) = **0.02 nat/token**（地板生效）。
- **容差档（判决，40 窗 S0'' 计划）**：**全窗过**——max |ΔNLL| = **1.064e-3**（mean 3.62e-4，median 3.48e-4）≪ TOL 0.02；40/40 within_tol。
- **S0'' 直测复核（门②丙补直测项，同窗对拍副产）**：byte 空间切点 mean **148.85**/窗 [117, 183]（窗 0-39），token 空间段数 mean 148.8；在册参照 172.7 段/窗（E124 门② byte 空间、训练流 n=1001）——窗源不同（本测量=corpus_v3 顺序前 40 窗），差 −13.8% 如实登记；切点数只作臂内描述量，不作必要性账分母（禁令照旧）。
- 产物：`parity_gate/parity_summary.json`（全 40 窗逐窗 NLL/段统计在案）；耗时 101.5s。
- **对拍过门 → 允许点火**（任务书：对拍不过=实现有 bug，不许点火——已过）。

## §2 门①体制核验——PASS

- **参数锚 loud-fail**：实例化断言（trainer `build_model`：vtile 档 want=48,152,896 与母列全等，漂移即停）；真机用例 `test_param_anchor_vtile_zero_new_params` 绿。
- **逐键 diff/键集全等**：`verify_vtile_reload` 集合全等校验（file-only/model-only 任一侧非空即响）+ 真机用例 `test_verify_vtile_reload_keys_equal_and_bitexact`（save→reload 逐位复原）/ `..._loudfail_extra_key`（多键拒绝）绿。
- **三件必备单测**（`tests/test_r3_vtile.py` 29 用例）：① flag-off 逐位/逐键不变（mock + 真机 `test_flag_off_forward_bitwise_vs_pure_fla` torch.equal）；② 白名单 loud-fail（丙白名单=空集特化：缺/多/junk 响亮）；③ 铺瓦恒等数学语义（容差一致+接力链契约+byte→token 映射规约确定性+plan=None 直通逐位）。
- **复验记录（本回执）**：py314 纯用例 **20 passed / 9 skipped**（fla 门控）；kda-kernels 门控驱动 `_run_gated_tests.py`（env 无 pytest 的最小 shim 驱动，临时件随案登记）**9/9 ALL GREEN**（含真机 CUDA 前向/接力/重载）；全量回归（除 vtile 件）**897 passed / 20 skipped**（CUDA/fla 门控），零红。
- **语义等价声明**：§0.1–§0.4 四项齐备（因果角色/施工形态 file:line/不同构点五条/新增参数零）。

## §3 门②锚直测借用声明（坑 9）——PASS（本地直测版）

本地锚直测（`anchors_local/summary.json`，本机本 env 本语料同窗同 tokenizer 直测，非借用）：**监督 1630.1 tok/窗（n=512）、原生 chunks/窗 25.98、盲猜地板 6.3903 nats/token（均匀地板 10.3735）、tokens/byte 0.3982、截断 0 窗**——与 4090 在册四数（1630.1/25.98/6.3903/0.3982）逐位同量级（同窗定义同语料，跨硬件方向一致）。166/172.7 等我们体制数未引、未借、未作分母。丙补直测项（S0'' 切点数/窗分布）见 §1 对拍门副产与 §4 冒烟段统计（153.39 段/窗 token 空间，500 窗训练流）。

## §4 门③仪器 baseline 回归——PASS

- **路径注记**：本地无 accelerate（env 不许改）→ 仪器本体 `load_model_and_tokenizer` 的 device_map 路径本地不可用；门③走丙启动器 `probe_r3_vtile_book.py`（母列 ckpt 无 r3_vtile 戳记→仅装载缝换本地等价装载器，run_window 直通原函数），**仪器本体零口径改动**（sha256 见下）。
- R2 母列 20K ckpt 上必要性账 40 窗（`gate3_mother40w_local/`，种子 424242，仪器默认参数）：**point +0.1026 nat，CI95 [+0.0341, +0.1781] 排零**；40/40 窗、0 空窗、0 截断；n_sel=857/n_ctl=775；耗时 13.1s；计分窗前缀 sha256 前 16 `a3fea9c0266c4b1d`。
- **方向带核验**：在册带=R2 池化 +0.1040 [+0.0951,+0.1125]（4090）；甲臂 4090 同门复跑 +0.1020 [+0.0334,+0.1770]。本地 5080 点估与甲 4090 点估差 **0.0006**、CI 近重合、整体为正且与在册带重叠——**方向带内，仪器本地活**（跨硬件/env 只比方向注记随行）。
- **仪器本体零触碰实证**：施工前后 sha256 不变（`probe_e122_deltanet_book.py` = `57ae63ad7bb6a986…` 与甲臂在册 57ae63ad…d950 同件；`r2_spec.py` = `7d20434d88cde7ba…` 与甲在册 7d20434d…5959b 同件——两锚自甲臂起零漂移）。

## §5 门④冒烟 500 步——PASS（双列；flag-off 逐位合同换锚实证）

| 项 | vtile 开启（--vtile） | 旗标关（默认，5080 本地参照列） | 4090 在册参照（R2 母列/甲 flag-off） |
| --- | --- | --- | --- |
| loss 轨迹 | step20 10.441 → step500 6.292 | step20 10.439 → step500 6.292 | 10.441 → 6.293 |
| loss_ema@500 | **6.3762** | **6.3760** | 6.3761 |
| NaN/发散 | 零 NaN，watchdog 零触发（diverged: null） | 同左 | 零触发 |
| skipped_partial | 0 | 0 | 0 |
| 峰值显存 | alloc **2786 MiB** / reserved 4368 MiB | alloc 2455 MiB / reserved 4132 MiB | alloc 2406 / reserved 3844 |
| 参数锚 | 48,152,896（零新增）loud-fail 过 | 48,152,896 loud-fail 过 | 48,152,896 |
| 段统计 | token 空间段 mean **153.39** [112,255]（500 窗训练流）；byte 切点同量随行 | — | — |

- **逐位合同换锚（坑 9 硬件维度，预注册注记）**：「默认关=与 R2 母列逐位不变」的同机验收在 5080 上跨硬件不可达（E121 例：GPU 并发归约下逐位相同不可达）——改锚双件：①**同进程逐位**=对拍门逐位档（plan=None 直通 vs 未挂接逐 token 逐位相等，§1 已过）=flag-off 代码路径零污染的本机实证；②**轨迹带对拍**：5080 flag-off vs 4090 甲 flag-off 拉回日志，25/25 记录窗 token 序列**逐位全等**（数据序同轨实证）、loss 差带 ±1.4e-2 内、终 ema 差 1e-4——跨硬件/env skew（torch 2.13/fla 0.5.2/tf 5.14.1 vs 2.12/0.5.1/5.15.1）量级注记随行。
- **vtile vs flag-off 同机同种子轨迹**：25 记录点 loss 差带 [−1.62e-2, +5.39e-3]（mean −8.0e-4），终 ema 差 +2e-4——fp 结合序噪声经训练放大的预期形态（函数恒等≠逐位同轨迹，预注册在册）。
- **逐键 diff 实证**：flag-off 日志零 vtile 新增字段（n_segs/n_cuts_byte 仅旗标开时落）；两列参数锚同为 48,152,896。
- **种子异源**：resolved_config train_seed=42 / eval_seed=424242（池化 424243）；全套超参照抄 R2（lr 3e-4/warmup 1024/betas (0.9,0.95)/wd 0.1/clip 1.0/watchdog 1000/窗 4096B/截 2048/batch 1）。

## §6 门⑤活性账 40 窗预跑——留档完成（不判读）

vtile 冒烟 ckpt（`smoke500_vtile/latest`）上经启动器 40 窗（`gate5_vtile40w/`，种子 424242）：point **+0.0016**，CI [+0.0001, +0.0031]——与 R2 冒烟件（−0.0010 含 0）、甲回声冒烟件（−7e-07 含 0）同「≈0 族」形态（未训练至必要性行为显形），如实留档不判读。**同卷构成性证据**：n_sel=857/n_ctl=775 与门③母列回归**逐位相同**（选择链不受装载/计划通路影响）。副产品：仪器侧 vtile 装载通路实证（fingerprint `r3_vtile.n_keys=339`、零新增参数锚、S0'' 就位）；逐窗 S0'' 统计 40 窗 cuts mean 148.85 与对拍门一致。耗时 120.3s。

## §7 门⑥报价与显存表——**如实登记（步速超预注册带，见 §9 事故 1 裁定链）**

| 项 | 实测（5080 16G，本地 env） | 参照 |
| --- | --- | --- |
| 步速（整程均值） | vtile **3.85 s/步**；flag-off 本地参照 0.178 s/步（含启动/编译摊销） | R2 母列 4090 在册 81.5 ms/步 |
| vtile 开销（对内同机对：flag-off→vtile） | **×21.6**（3.85/0.178）；对 4090 在册 ×47（跨硬件只比方向） | 预注册起草带 ×1.3–2.5（「待实现路径定型后精算」暂定） |
| 开销归因 | 逐段 python 循环 ~150 段×24 层≈**3600 次顺序 chunk_delta_rule 调用**/步（原生 24 次），kernel-launch bound；段长 mean ~12 token vs 原生 64 | — |
| 20K 墙钟报价 | 20,000 × 3.85s ≈ **77,000 s ≈ 21.4 h**（5080 闲机自有机会成本；跨硬件 GPU·h 口径不与 4090 报价并表） | R2 4090 实测 1,492.7 s（24.9 min） |
| 训练峰值显存 | **alloc 2786 MiB / reserved 4368 MiB**（16G 卡余量充裕） | 4090 alloc 2406 / reserved 3844 |
| 必要性账仪器（vtile 装载，40 窗实测） | 120.3 s（含表扫描+S0'' 逐窗切点）；峰值显存远低于 16G | 门③母列原生 13.1 s |
| 判决仪器全套（4 块×500 窗+池化）报价 | ≈**1.6 h**（4×(~22 min 表扫描+逐窗 ~2.7s×500×2 前向)+池化） | — |

## §8 c3 附带件（§9.3 已采纳，零训练附属读数）——收官

**构造**：`probe_r3_c3_book.py`（commit 966f78f）——模型不动（母列 ckpt 原样，无 vtile patch），仪器「跨段」判定从固定 256-token 网格换锚 S0'' 段号映射（选择链接缝单点换锚；稀有表/池/簇半分/手术/计分位/bootstrap/种子全走仪器本体；items 审计段字段留原生网格，注记在案；holder 缺席响亮停报防静默回落）。

**读数**（母列 20K ckpt，40 窗 0-39，种子 424242，与门③同窗同链——唯一变量=跨段定义）：

| 量 | c3（S0'' 对齐） | 门③（原生 256-token 网格） |
| --- | --- | --- |
| 跨段命中选中 n_sel | 1414 | 857 |
| 对照 n_ctl | 1337 | 775 |
| mean ΔNLL 处理 / 对照 | 0.3398 / 0.1847 | 0.2221 / 0.1195 |
| 池化 contrast | **+0.1551 [+0.0844, +0.2323] 排零** | +0.1026 [+0.0341, +0.1781] 排零 |
| strong 尾（≥1 nat） | 12.23%（173/1414） | 7.47%（64/857） |
| source→repeat 距离中位 | 125 token | 265 token |

机制素材形态（不判负正、不改主判决口径）：S0'' 段均 ~11.7–12.5 token ≪ 256-token 网格 → 跨段口径放宽，n_sel ×1.65、strong 尾 ×1.84、contrast 点估 ×1.51——「跨段必要性」读数对段定义敏感，S0'' 切点定义的段承载更强的跨段依赖信号。附属读数归主会话作机制注记素材。耗时 18.3s；产物 `c3_s0align40w/`（summary/items/audit/c3_window_stats）。

## §9 事故与如实注记

1. **步速超预注册带 ×21.6（对内）——报价带修正与点火裁定链**：预注册 ×1.3–2.5 为「待实现路径定型后精算」的起草暂定值；实现路径定型（fla 0.5.2 原生核逐段接力，零自写核）后实测 ×21.6（同机对内对）——超带 8.6×。裁定链：①任务书 §6 工时护栏「超了先点火再优化」+丙的点火以函数恒等对拍过门为前提（§1 已过）；②用户 2026-09-14 指令（晚于冻结）「5080 不得闲置，能并行的往 5080 放」=承载机修订后成本模型从租用 4090（GPU·h/¥）变自有闲机（墙钟）；③20K 墙钟 ~21.4 h 有界、可逆、本地，且 <2 天工时护栏；④主会话任务书执行口径「报价显存表……各自如实登记」。据此点火并全案登记——**若主会话裁定应优化先行（如段内 fused_recurrent 变体或自写 masked-tile 核），20K 列可按 --resume 中断续跑，零沉没**。
2. **后台任务 600s 默认超时杀冒烟首跑**：vtile 冒烟首跑于 ~step 150 被后台超时终止（EXIT 1）；无烟 checkpoint（ckpt_every 1000）不可续，清目录重跑收官。零数据污染（首跑产物已删）。教训入例：长任务 disable_timeout。
3. **主机/会话中断两起**（甲臂事故 6 同族）：①施工监控会话被 2h 后台超时中断一次（非任务失败）——20K 训练以 disable_timeout detach 形态存活，断点核验（git 链完好、进程在、日志步数连续）后续跑，零重跑零丢失；②监控循环尾声 WaitFor 中止一次，同法核验后续跑。**教训入例兑现：长任务一律 disable_timeout + detach，中断后先核现场再动手**。
4. **env skew 全案随行**：fla 0.5.2/tf 5.14.1/torch 2.13.0（5080）vs fla 0.5.1/tf 5.15.1/torch 2.12.1（4090 在册指纹）——一切读数「同机同 env 内成立」，跨硬件只比方向；与母列基尺 +0.1040 的比较带硬件指纹注记；**意外判死须回 4090 重锚（预注册规则）**。
5. **对拍门 S0'' 直测 vs 在册 172.7**：byte 切点 mean 148.85/窗（窗 0-39）低于在册 172.7（E124 门②训练流 n=1001）−13.8%——窗源不同（corpus_v3 顺序前缀 vs 训练流抽样），描述量不作分母；判决账 2000 窗 vtile_window_stats 将给出大样本复核。
6. **本地无 accelerate**：仪器装载缝换 `load_model_and_tokenizer_local`（device_map→.to 等价；env 不许改——兼 FlashKDA 活）；门③/门⑤/c3/判决账全走此缝，仪器本体零改动。
7. **镜像纪律**：同甲臂注记——本臂件含项目身份词，若主会话将 `tools/baselines/deltanet_r2/` 纳入镜像同步需先扩充身份词表（提交主会话裁定）。

## §10 点火与训练收官——**20,000/20,000 整**

- **点火**：2026-09-14，前置门六件全绿+对拍门全绿后按任务链点火（用户签发令预授权+主会话 5080 承载修订）。命令形态：`train_deltanet_r3.py --corpus P:\FLUED_corpus\corpus_v3\corpus_v3.txt --tokenizer-path outputs/r2_mother_20k_local_20260914/mother20k_latest --out-dir outputs/r3_transplant_vtile_20260914/main20k_vtile --max-steps 20000 --vtile`（后台 detach，disable_timeout；点火前 duplicate 检查：无 python 进程、GPU 桌面占用 14%/2311MiB）。
- **训练事实**：**20,000 / 20,000 整**（零中断、零续跑，skipped_partial=0）；**ema 3.0475**（母列 20K ema 3.0244 同带邻域 +0.023，如实并置）；**看门狗零触发**（diverged: null）；**墙钟 75,885.1 s = 1,264.8 min ≈ 21.08 h ≈ 0.88 GPU·d**（5080 自有闲机墙钟口径；报价 21.4 h 兑现）；峰值显存 **alloc 2918 MiB / reserved 4928 MiB**；里程碑 ckpt（500/1000/…/20000 全 21 档）正常落盘。
- **段统计（训练流 20,000 窗全量）**：token 空间段数 mean **153.65** [100, 330]；S0'' 权重锚 `K:\FLUED_archive\s0pp_pro_v4_sft_20260805\latest.pt`（sha256 前 16 落 `main20k_vtile/vtile_meta.json`）。
- **种子/超参**：train_seed=42 / eval_seed=424242，resolved_config 全套照抄 r2_spec（lr 3e-4/warmup 1024/cosine 0.1×/betas (0.9,0.95)/wd 0.1/clip 1.0/watchdog 1000/窗 4096B/截 2048/batch 1）。

## §11 判决仪器（500 窗×4 块+池化）——**报数完成（判读权归主会话）**

口径：E122 同源仪器零口径改动（`probe_r3_vtile_book.py` 仅装载+逐窗计划注入）；与 R2 收官**同卷**——同窗集（4×500 窗，start-window 0/500/1000/1500）、同选择链（种子 424242）、同池化（2000 次 bootstrap，种子 424243）。**同卷构成性证据**：池化计分位 **n_sel=48,231 / n_ctl=43,810，与 R2 母列收官逐位相同**（同选择链确定性；vtile 装载通路不动选择链，门⑤已双侧实证）。

| 块 | 窗域 | point (nat) | CI95 | 排零 | 窗数 | 违例 | strong 尾 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| b0 | 0-499 | +0.1081 | [+0.0923, +0.1262] | ✓ | 500/500 | 0 | 6.27% |
| b1 | 500-999 | +0.0863 | [+0.0707, +0.1029] | ✓ | 500/500 | 0 | 6.15% |
| b2 | 1000-1499 | +0.0912 | [+0.0752, +0.1082] | ✓ | 500/500 | 0 | 6.31% |
| b3 | 1500-1999 | +0.1092 | [+0.0928, +0.1255] | ✓ | 500/500 | 0 | 6.29% |
| **池化（判决件）** | 2000 窗 | **+0.0990** | **[+0.0907, +0.1068]** | **✓** | 2000 | 0 | — |

- 计分位：池化 mean_sel 0.2037 / mean_ctl 0.1047；仪器自家 verdict 字段原样转录：「跨架构必要性复现实存（弱）——剂量部分在板」。判决账耗时 15:26:06→17:01:00 ≈ 95 min（报价 ~1.6 h 兑现）。
- **2000 窗 S0'' 直测大样本复核**（vtile_window_stats 副产）：byte 切点 mean **153.84**/窗 [112, 268]，token 段 mean 153.82，段长 mean ~10.7 token——与对拍门 40 窗（148.85）同带；在册 172.7（E124 门②训练流 n=1001）差 −10.9% 如实登记（窗源不同；描述量不作分母）。
- **三档判据机械落档**（预注册 §4，判读归主会话；基尺=母列 +0.1040 [+0.0951,+0.1125] 与阳性线 0.05 nat；**比较带硬件指纹注记：本臂=5080×fla 0.5.2×tf 5.14.1×torch 2.13.0，母列=4090×fla 0.5.1×tf 5.15.1×torch 2.12.1，跨硬件/env 只比方向**）：
  - **杀死**（CI 上界 < 0.05）：CI 上界 **+0.1068 > 0.05** → **不落**；
  - **不确定**（CI 与 0.05 相交）：CI 下界 **+0.0907 > 0.05** → CI 不与 0.05 相交 → **不落**；
  - **无辜**（CI 下界>0 且点估 ≥0.05）：下界 +0.0907>0 ✓ 且点估 +0.0990≥0.05 ✓ → **机械落档=无辜档**。
  - **无辜分级注记**（预注册）：本臂 CI [+0.0907, +0.1068] 与母列带 [+0.0951,+0.1125] **重叠**（交集 [+0.0951,+0.1068] 非空）→ **带内无辜**。
- **触发器落档**：杀死未落 → 种子 {1,2} 加固不触发；不确定未落 → 40K 预算升档不触发；无辜不补跑（R2 同例）。**意外判死回 4090 重锚的预注册规则未触发**（未判死）。
- **判读必带混杂注记**（§4 预注册，丙臂两条）：①函数恒等预期本身（不杀=「铺瓦粒度不影响训练动力学」从声明升级为实验事实的兑现形态；杀=铺瓦敏感性真发现）——本臂落「不杀」档；②实现路径耦合（对拍门兜底，§1 全绿）。判词限定范围：「DeltaNet-50M × corpus_v3 × 4096B × 20K × 本仪器族 × 同机同 env（5080 指纹）」。
- 块间形态注记（不判读）：四块 +0.086~+0.109；strong 尾 6.15–6.31% 与母列 6.5–6.8% 同带——素材归主会话。

## §12 产物清单（本地 `outputs/r3_transplant_vtile_20260914/`）

| 路径 | 内容 |
| --- | --- |
| `parity_gate/`（parity_summary.json）+ `.log` | 丙前置对拍门（逐位档+容差档全绿，max 1.064e-3 ≪ TOL 0.02） |
| `anchors_local/` + `.log` | 门②锚直测本地版（1631.1/25.98/6.3903/0.3982） |
| `gate3_mother40w_local/` + `.log` | 门③仪器回归（+0.1026 排零，方向带内） |
| `smoke500_flagoff/` + `.log` | 门④旗标关冒烟（5080 本地参照列，ema 6.3760） |
| `smoke500_vtile/`（含 vtile_meta.json/resolved_config/train_log/summary/latest+model_step500）+ `.log` | 门④ vtile 冒烟（ema 6.3762，3.85s/步报价锚） |
| `gate5_vtile40w/`（含 vtile_window_stats.jsonl）+ `.log` | 门⑤留档（+0.0016 ≈0 族，不判读） |
| `c3_s0align40w/`（含 c3_window_stats.jsonl）+ `.log` | c3 附属读数（+0.1551 [+0.0844,+0.2323]，机制注记） |
| `_run_gated_tests.py` | 门控用例驱动（env 无 pytest 的临时件，随案登记） |
| `run_verdict.sh` | 判决账编排（4 块+池化） |
| `main20k_vtile/`（latest + model_step{500,1000,…,20000} 全 21 档 + optimizer + train_log + summary + resolved_config + vtile_meta）+ `.log` | 20K 主列全量（ema 3.0475，21.08h，权重 ~21 档 ckpt 在本地 E: 待归档盘裁定） |
| `verdict_b{0..3}/`（summary/items/audit/vtile_window_stats）+ `.log` | 判决仪器四块（500 窗×4，零违例，r3_vtile fingerprint 各在案） |
| `necessity_pooled_seen.json` + `pool.log` | 池化判决件（+0.0990 [+0.0907, +0.1068]，种子 424243，n_sel 48,231 逐位同卷实证） |
| `run_verdict.sh` | 判决账编排脚本（4 块+池化，随案登记） |

**硬件指纹**：RTX 5080 16G 本地 × torch 2.13.0+cu130 × triton 3.7.1 × fla 0.5.2 × transformers 5.14.1 × py 3.12（env `kda-kernels`）；一切读数同机同 env 内成立，跨硬件只比方向（坑 9）。
