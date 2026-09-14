# R3 甲臂（对角护栏移植 = 恒等自读回声）施工与前置门回执

- **日期**：2026-09-14（施工 agent；任务书冻结 v1.0 用户签发令：「甲臂先行施工，前置门六件回执齐了点火」）
- **任务书**：`docs/versions/v3.7/FLUED_V3_7_R3_DELTANET_TRANSPLANT_DRAFT_20260914_CN.md`（冻结 v1.0）
- **靶机**：远端 4090（106.15.75.26:60222，`/workspace/FLUED`，env `/workspace/conda/envs/flued312stable`，fla 0.5.1 × torch 2.12.1+cu130 × transformers 5.15.1 × triton 3.7.1 × py 3.12.14）
- **本地 commit 链**：`05ccd49`（施工件四文件）→ `3f7de99`（修正：canonical 键序 + CUDA 门控 + config 戳）→ `4201853`（autocast bf16）→ `f78027a`（_v_hook 解包 ShortConvolution 元组返回）
- **单源纪律**：`r2_spec.py` 零改动；仪器本体 `tools/analysis/cross_arch/probe_e122_deltanet_book.py` 零触碰（sha256 见门③）；新增件全部旗标化（`--echo` 默认关）。

---

## §0 施工形态（门①体制核验・file:line 证据）

### §0.1 原件因果角色（§2.0 ①）

`allowed | diag_eye`（`flued/v36/model.py:1840` `keep_diag, diag_eye = _causal_keep_mask(n, …)`；`:1844` `allowed = allowed | diag_eye.view(1, 1, n, n)`）——E124 勘定的自读旁路本体：backbone 对 store 行轴的一切注意力中，每个查询行恒可零寻址读自身行；E124 实测 backbone 重建 99% 由自读承载。原件是掩码项、零参数（原位兼有 padded 行防 NaN 职能，本移植不含——DeltaNet 无全掩码行问题）。

### §0.2 移植构造施工形态（§2.0 ②）

**恒等自读回声**：每层状态读出处加恒通旁路 `o_t ← o_t + g_l · v_t`。施工 file:line（fla 0.5.1 于靶机 `/workspace/conda/envs/flued312stable/lib/python3.12/site-packages/fla/`；回声件于 `tools/baselines/deltanet_r2/`）：

| 件 | 位置 | 内容 |
| --- | --- | --- |
| v_t tap 点 | `fla/layers/delta_net.py:213-218`（`v, conv_state_v = self.v_conv1d(x=self.v_proj(hidden_states), …)`）的**输出**，由 `r3_spec.py:148` `attn.v_conv1d.register_forward_hook(_v_hook)` 捕获（`r3_spec.py:139-141`） | use_short_conv 之后（v_conv1d 内含 silu 激活，`:151-156`）；β 门控之前（β 由 `b_proj` `:240-241` 产出、在 delta rule 核内 `:261-270` 作用于写入，v 在其前）——用户终审确认的 tap 点，不引入第二条旁路 |
| o_t tap 点 | `fla/layers/delta_net.py:261-270`（`chunk_delta_rule` 返回的状态读出 o，(B,T,H,D)）与 `:286`（`o = self.o_norm(o)`）之间，由 `r3_spec.py:149` `attn.o_norm.register_forward_pre_hook(_o_pre_hook)` 注入（`r3_spec.py:143-146`，调 `echo_add` `:74-80`） | o_norm/o_proj（`:286-288`）是输出接口适配，不属于状态读取——加法落在读出原值上 |
| 门 g_l | `r3_spec.py:131-137`：`attn.echo_gate = nn.Parameter(torch.full((), 1.0, dtype=ref.dtype, device=ref.device))`，init 1.0（=任务书 §2.1「通道从第 0 步起全强度可用」；进优化器随 `model.parameters()`，R2 超参照抄不特判——含 wd 0.1，即任务书「可学衰减」语义，如实登记） | 每层 1 标量 × 24 层 |
| 训练旗标 | `train_deltanet_r3.py:45`（`--echo` store_true 默认关）；`:58-75` `build_model`：echo 才 `attach_echo`+`stamp_echo_config`，参数锚 loud-fail 双档（关=48,152,896 与 R2 全等，开=48,152,920） | 默认关=不挂任何 hook、不建任何参数 |
| 评测装载 | `probe_r3_echo_book.py:37-51`：替换仪器模块级 `load_model_and_tokenizer`（**仅装载路径**，窗/选择链/手术/bootstrap/种子全走仪器本体）；config 带 `r3_echo` 字段 → `r3.attach_and_strict_reload`（`r3_spec.py:258-264`） | 坑 8：from_pretrained 对回声键是 unexpected key 会静默丢弃，必须文件全量 strict 重载 |
| strict 白名单 | `r3_spec.py:228-256` `strict_load_echo` + `:191-205` `check_key_whitelist`；白名单=`model.layers.{i}.attn.echo_gate`（i∈[0,24)，`:60-63`） | 缺失/白名单外/白名单缺席任一破即 RuntimeError「不点火」 |

### §0.3 不同构点清单（§2.0 ③，判读引用必带）

1. **粒度**：原件是 chunk 行粒度（我们架构 24B/块行级自读）；宿主是 token 粒度（每 token 免寻址读回自己的写入）——任务书 §2.1 在册。
2. **宿主天然局部通道**：宿主残差流 + 短卷积（conv_size=4）已天然承载强局部自读，回声在其上叠加显式加性通道——任务书 §4 混杂注记在册。
3. **掩码项 vs 加性通道**：原件实现为注意力掩码并集（零参数、作用于 softmax 前的可达集）；移植实现为读出侧加性旁路（24 参数、作用于核读出后）。语义对应物（零寻址读自身写入），结构形态按宿主接口适配——§2.1 预注册构造本身。

### §0.4 新增参数（§2.0 ④）

**24 个标量**（`ECHO_NUM_PARAMS = num_layers = 24`，`r3_spec.py:56`；参数锚 48,152,896 + 24 = **48,152,920**）。除此之外任何权重零新增、零改动；`r2_spec.py`/仪器本体/fla 库文件零修改（本臂 commit 触及面=`tools/baselines/deltanet_r2/` 三文件 + `tests/test_r3_echo.py`，四文件全为新增，1019 行净增）。

---

## §1 门①体制核验——PASS

- **参数锚 loud-fail**：实例化双档断言（`train_deltanet_r3.py:71-75`）+ 远端单测 `test_param_anchor_instantiation_both_flags`（关=48,152,896 ✓，开=48,152,920 ✓，靶机实测）。
- **逐键 diff**：两次独立实例化（echo-on）键序列逐键一致 + echo-on 键集 = R2 母列键集 ∪ 白名单恰 24 键、无任何其他差异（`test_key_diff_two_instantiations_echo_on_identical` 靶机绿）。
- **三件必备单测**（`tests/test_r3_echo.py`，本地 21 过 6 fla 门控跳过 → 靶机全量 27/27 绿）：
  - ① flag-off 逐位/逐键不变（mock + 真机 autocast bf16 前向 `torch.equal` 双层）；
  - ② 回声键白名单 loud-fail（缺失/多出/junk/文件缺/无回声键五路 RuntimeError + save→from_pretrained 静默丢弃事故形态复现→strict 重载逐位复原）；
  - ③ g_l 数学语义（g=0 逐位等于母列：mock 挂接态 + 真机形态；echo_add 纯函数；tap 点契约实证=捕获 conv 输出非 proj 输出）。
- **梯度接通**：24 门梯度有限且非零（`test_echo_forward_differs_and_gate_grads_finite` 靶机绿）。

## §2 门②锚直测借用声明（坑 9）——PASS

R2 门②产物（`outputs/r2_deltanet50m_20260913/anchors/summary.json`，R2_RECEIPT §5 在册）：**监督 1630.1 tok/窗、原生 chunks/窗 25.98、盲猜地板 6.3903 nats/token（均匀地板 10.3735）、tokens/byte 0.3982**。借用边界核验：同机（4090 @106.15.75.26）同 env（flued312stable）同语料（corpus_v3，sha256 前 16 `ed4ab97810776ce7`，含 VERIFIED.sha256）同窗（4096B 顺序非重叠）同 tokenizer（Mistral 32K fla-hub 四文件）→ **直接引用不重测**。R2 收官基尺 **+0.1040 nat [+0.0951, +0.1125]**（2000 窗池化，`necessity_pooled_seen.json` 逐位复核于本回执回拉件）同边界借用。166/172.7 等我们体制数未引、未借、未作分母。

## §3 门③仪器 baseline 回归——**PASS**

R2 母列 20K ckpt（`outputs/r2_deltanet50m_20260913/main20k/latest`）上必要性账 40 窗复跑（**原仪器直跑**，非启动器；`gate3_mother40w/`，种子 424242，仪器默认参数）：

- **point +0.1020 nat，CI95 [+0.0334, +0.1770] 排零**；40/40 窗、0 空窗、0 截断；推理耗时 9.2s。
- **方向带核验**（在册带 = R2 池化 +0.1040 [+0.0951, +0.1125]；40 窗功率不足只验方向不判读）：点估 +0.1020 与在册点估差 **0.0020**（几乎落点在册点估上），CI 整体为正且与在册带重叠——**方向带内，仪器活，不翻车**。
- **仪器本体零触碰实证**：`sha256(probe_e122_deltanet_book.py) = 57ae63ad…d950`（施工前后未变；r2_spec.py = 7d20434d…5959b 未变）。

## §4 门④冒烟 500 步——**PASS（含 flag-off 逐位验收）**

两列冒烟（同机同种子同数据序；`smoke500_echo/`、`smoke500_flagoff/`）：

| 项 | 回声开启（--echo） | 旗标关（默认） | R2 母列参照（在册） |
| --- | --- | --- | --- |
| loss 轨迹 | step20 10.423 → step500 5.577 | step20 10.423 → step500 6.293 | 10.441 → 6.293 |
| loss_ema@500 | **5.7938**（漂移如实登记：回声恒通自读使下降更快，不卡 R2 带） | **6.3761** | 6.376 |
| NaN/发散 | 零 NaN，watchdog 零触发（diverged: null） | 同左 | 零触发 |
| skipped_partial | 0 | 0 | 0 |
| 峰值显存 | alloc 2412 MiB / reserved 6080 MiB | alloc 2414 MiB / reserved 6084 MiB | alloc 2406 / reserved 3844 |
| 参数锚 | 48,152,920（+24）loud-fail 过 | 48,152,896 loud-fail 过 | 48,152,896 |

- **flag-off 逐位验收（施工规格硬验收）**：`r3_compare_flagoff.py` 对 R2 母列 `smoke500/train_log.jsonl` 逐记录逐字段比对（step/loss/loss_ema/lr/tokens_in_window 五字段，剔除计时字段）——**BITWISE_MATCH，25/25 记录逐位一致**。默认关=与 R2 母列逐位不变，实证兑现。
- **逐键 diff 实证**：`echo_whitelist.json` 24 键（`model.layers.0.attn.echo_gate` … `model.layers.23.attn.echo_gate`）+ 靶机单测 39/39 绿（含两次实例化键集逐键一致、echo-on 键集=母列键集∪白名单恰 24 键）。
- **种子异源**：`resolved_config.json` train_seed=42 / eval_seed=424242；全套超参照抄 R2（lr 3e-4 / warmup 1024 / betas (0.9,0.95) / wd 0.1 / clip 1.0 / watchdog 1000 / 窗 4096B / 截 2048 / batch 1）。

## §5 门⑤活性账 40 窗预跑——**留档完成（不判读）**

回声冒烟 ckpt（`smoke500_echo/latest`）上经**启动器**（`probe_r3_echo_book.py`）40 窗（`gate5_echo40w/`，种子 424242）：point **−7.0e-07 ≈ 0**，CI [−0.00117, +0.00112] 含 0——与 R2 冒烟件 40 窗（−0.0010 含 0）同「≈0 族」形态（未训练至必要性行为显形的两列同构），如实留档不判读。**本门副产品**：仪器侧回声装载通路实证（summary fingerprint `r3_echo.n_echo_keys=24`，strict 白名单重载在仪器内走通）。

## §6 门⑥报价与显存表——**PASS（报价就绪）**

| 项 | 实测（4090，本机同 env） | R2 参照 |
| --- | --- | --- |
| 步速（整程均值，含 triton 预热） | 回声 **78.5 ms/步**；flag-off 75.1 ms/步 | 81.5 ms/步 |
| 回声开销（对内同码对：flag-off→echo） | **+4.5%**（整程均值口径；高于起草 +1–3% 估计、绝对值仍低于 R2 母列 81.5ms——triton 缓存跨进程复用所致，如实并置） | — |
| 20K 墙钟报价 | 20,000 × 78.5ms ≈ **1,570 s ≈ 26.2 min ≈ 0.44 GPU·h** | 实测 1,492.7 s（24.9 min） |
| 训练峰值显存 | **alloc 2412 MiB / reserved 6080 MiB**（24G 卡余量充裕） | alloc 2406 / reserved 3844 |
| 必要性账仪器（50M 底物，40 窗实测） | 推理 7.5–9.2 s；峰值显存远低于 24G | 50M 底物 40 窗 7.3–23.2 s |
| 判决仪器全套（4 块×500 窗+池化）报价 | ≈25–35 min（表扫描 4×~2 min + 2000 窗×2 前向） | — |

## §7 点火与训练收官

- **点火**：2026-09-14，前置门六件全绿后按预授权直接点火（用户签发令原话：「六件全绿 → 点火授权已预批，直接点」）。命令形态：`nohup python tools/baselines/deltanet_r2/train_deltanet_r3.py --corpus /workspace/corpus/corpus_v3.txt --tokenizer-path /workspace/models/delta_net-1.3B-100B --out-dir outputs/r3_transplant_echo_20260914/main20k_echo --max-steps 20000 --echo > …/main20k_echo.log 2>&1 &`（pid 48862；点火前 duplicate 检查：nvidia-smi 0% / 0 python 进程）。
- **训练事实**：**20,000 / 20,000 整**（零中断、零续跑，skipped_partial=0）；**ema 3.0614**（母列 20K ema 3.0244，同带邻域，如实并置）；**看门狗零触发**（diverged: null）；**墙钟 1,533.7 s = 25.6 min ≈ 0.426 GPU·h**（报价 26.2 min 兑现）；峰值显存 **alloc 2477 MiB / reserved 9086 MiB**；里程碑 ckpt 正常落盘。
- **回声门终值**（`echo_gates_final.json`，24 门，init 1.0）：min **−0.0067** / max **0.9342**——门随训练可学漂移（R2 超参 wd 0.1 照抄不特判，含任务书「可学衰减」语义），逐门值在案可复核。

## §8 判决仪器（500 窗×4 块+池化）——**报数完成（判读权归主会话）**

口径：E122 同源仪器零口径改动（`probe_r3_echo_book.py` 仅装载注入）；与 R2 收官**同卷**——同窗集（4×500 窗，start-window 0/500/1000/1500）、同选择链（种子 424242）、同池化（2000 次 bootstrap，种子 424243）。**同卷构成性证据**：计分位 n_sel=48,231 / n_ctl=43,810，与 R2 母列收官**逐位相同**（同选择链确定性）。

| 块 | 窗域 | point (nat) | CI95 | 排零 | 窗数 | 违例 | strong 尾 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| b0 | 0-499 | +0.0598 | [+0.0494, +0.0712] | ✓ | 500/500 | 0 | 3.06% |
| b1 | 500-999 | +0.0476 | [+0.0374, +0.0587] | ✓ | 500/500 | 0 | 2.69% |
| b2 | 1000-1499 | +0.0520 | [+0.0419, +0.0633] | ✓ | 500/500 | 0 | 2.59% |
| b3 | 1500-1999 | +0.0610 | [+0.0512, +0.0711] | ✓ | 500/500 | 0 | 2.67% |
| **池化（判决件）** | 2000 窗 | **+0.0553** | **[+0.0501, +0.0605]** | **✓** | 2000 | 0 | — |

- 计分位：池化 n_sel=48,231 / n_ctl=43,810；mean_sel 0.1155 / mean_ctl 0.0603；仪器自家 verdict 字段原样转录：「跨架构必要性复现实存（弱）——剂量部分在板」。
- **三档判据机械落档**（预注册 §4，判读归主会话；基尺=母列 +0.1040 [+0.0951,+0.1125] 与阳性线 0.05 nat）：
  - **杀死**（CI 上界 < 0.05）：CI 上界 **+0.0605 > 0.05** → **不落**；
  - **不确定**（CI 与 0.05 相交）：CI 下界 **+0.050105 > 0.05**（超出阳性线 0.000105，紧贴线上）→ CI 不与 0.05 相交 → **不落**；
  - **无辜**（CI 下界>0 且点估 ≥0.05）：下界 +0.0501>0 ✓ 且点估 +0.0553≥0.05 ✓ → **机械落档=无辜档**。
  - **无辜分级注记**（预注册）：本臂 CI [+0.0501, +0.0605] 与母列带 [+0.0951, +0.1125] **无重叠**且点估偏低（0.0553 < 0.0951）→ **带下无辜**（亚临界毒性，登记不展开）。
- **触发器落档**：杀死未落 → 种子 {1,2} 加固不触发；不确定未落 → 40K 预算升档不触发；无辜不补跑（R2 同例）。
- **判读必带混杂注记**（§4 预注册，甲臂两条）：①粒度差（token 级恒通 vs chunk 行级；「粒度更细只强不弱」——无辜判词必带粒度注记）；②宿主残差流+短卷积已天然承载强局部自读，「甲不杀」二义（件无辜 vs 语义被宿主天然饱和）——机制注记不强行归一。判词限定范围：「DeltaNet-50M × corpus_v3 × 4096B × 20K × 本仪器族 × 同机同 env」。
- 块间形态注记（不判读）：四块 +0.048~+0.061 极稳；strong 尾 2.6-3.1% 低于母列 6.5-6.8%——强响应收窄与「带下无辜」分级注记同向，素材归主会话。

## §9 事故与如实注记

1. **远端 GitHub fetch 断连**：`git fetch origin` 连续 5 次重试失败（could not read Username），改走 git bundle 增量通道（`4fe9bbd..05ccd49` 及两个修正 bundle，逐个 scp，对象哈希 verify 过）——内容等价于对齐 origin 分支 `15d22e7` + 本地施工链，remote checkout 于 `4201853`。
2. **远端未跟踪杂物 stash 报备**（禁丢令执行）：`git stash push -u`（stash@{0}，2026-09-14）封存 4 文件：`run_d1_10k_20260904.sh`、`run_d1_smoke_20260904.sh`（远端独有，本地无）、`tests/test_stratify_utf8_necessity.py`、`tools/baselines/deltanet_r2/stratify_utf8_necessity.py`（后两者为 873e0c8 已入库文件的远端旧副本）。
3. **fla 0.5.1 两环境事实**（单测首跑实证，随案登记）：① `ChunkDeltaRuleFunction` 拒收 fp32（"Please use bfloat16"）——训练/仪器/测试前向均须 autocast bf16 或 bf16 权重（R2 训练器 autocast 语义同源）；② fla triton 核 CPU 不可用——fla 门控 forward 用例以 `_HAS_FLA_CUDA` 门控；③ `ShortConvolution.forward` 恒返回 `(x, final_state)` 元组（层内双值解包，`delta_net.py:213-218`）——首版 _v_hook 捕获整元组被真机单测拦截（mock 盖不住的接口细节），f78027a 修正后才进冒烟（**单测链先于点火拦截 bug，前置门体系按设计工作**）。
4. **GPU 共租窗**（如实注记，坑 9 硬件维度）：点火前 ~1.5h 同机另一容器作业占卡（22.2G/97-100%，进程不可见非本会话所有，未触碰）；门③-⑥与点火均在共租结束、GPU 独占空闲（0%/489MiB、0 python 进程复核）后执行。全程同机同 env 硬件指纹不变；冒烟与 20K 期间无共租复现（77-79ms/步稳定，与 R2 81.5ms 同带）。
5. **回声开销超起草报价**：整程均值口径 flag-off→echo = +4.5%（起草 +1–3%）；绝对步速 78.5ms 仍低于 R2 母列 81.5ms（triton 缓存跨进程复用），20K 墙钟报价兑现（实测 25.6min < 报价 26.2min）。如实并置，不回改报价段。
6. **主机会话中断**：施工中途本地主机 Windows 更新重启一次（GPU 等位期，非任何门件/训练中）；恢复后按断点协议核验（本地 commit 完好、远端未点火）后从断点续跑，零重跑零丢失。
7. **镜像纪律（匿名化预检）**：本臂施工件含「R2/R3/DeltaNet/FLUED」等项目身份词——按协作协议 6，主仓文件不进匿名镜像仓的现行自动同步范围外新增无涉；若主会话后续将 `tools/baselines/deltanet_r2/` 纳入镜像同步，身份词表需先扩充（提交主会话裁定）。

## §10 产物清单（远端 `/workspace/FLUED/outputs/r3_transplant_echo_20260914/`；本地同名目录已回拉全量元数据/日志/仪表产物，不含权重）

| 路径 | 内容 |
| --- | --- |
| `R3_ECHO_RECEIPT_20260914.md` | 本回执（远端+本地同名） |
| `gate3_mother40w/`（summary/items/audit）+ `.log` | 门③仪器 baseline 回归（R2 母列 40 窗，+0.1020 排零） |
| `smoke500_echo/`（summary/train_log/resolved_config/echo_whitelist/latest+ckpt）+ `.log` | 门④回声冒烟（ema 5.7938） |
| `smoke500_flagoff/`（同上结构）+ `.log` | 门④旗标关冒烟（BITWISE_MATCH 验收件，`../r3_compare_flagoff.py`） |
| `gate5_echo40w/` + `.log` | 门⑤活性账 40 窗预跑（≈0，留档不判读；仪器内回声装载实证） |
| `main20k_echo/`（latest + model_step{500,1000,…,20000} + optimizer.pt + train_log.jsonl + summary.json + resolved_config.json + echo_whitelist.json + echo_gates_final.json）+ `.log` | 20K 主列全量（权重 ~15G 留远端待归档盘裁定，归档走 K:/N: 纪律） |
| `verdict_b{0,1,2,3}/`（summary/items/audit）+ `.log` | 判决仪器四块（500 窗×4，零违例，r3_echo fingerprint 24 键各在案） |
| `necessity_pooled_seen.json` + `pool.log` + `verdict_chain.log` | 池化判决件（+0.0553 [+0.0501, +0.0605]，种子 424243） |
| `../r3_transplant_echo_20260914_stage345.sh`、`../r3_compare_flagoff.py` | 施工编排与逐位比对脚本（远端 outputs/ 下，随案登记） |

**成本**：冒烟×2（~2 min）+ 20K 主列 0.426 GPU·h + 门③/⑤仪器（~1 min）+ 判决仪器四块+池化（~3 min）≈ **0.5 GPU·h 全案**（不含共租等位 ~1.5h 墙钟等待）。硬件指纹：RTX 4090 24G @106.15.75.26 × fla 0.5.1 × transformers 5.15.1 × torch 2.12.1+cu130 × triton 3.7.1 × py 3.12.14；一切读数同机同 env 内成立，跨硬件只比方向（坑 9）。
