# R3 乙臂（summarizer 双头构造移植）施工、前置门与判决回执

- **日期**：2026-09-14（施工 agent；任务书冻结 v1.0，乙臂预授权在册：前置门六件回执齐了点火；判死触发器=种子 {1,2} 加固＋参数匹配对照列＋去消融变体，2026-09-14 用户终审裁定）
- **任务书**：`docs/versions/v3.7/FLUED_V3_7_R3_DELTANET_TRANSPLANT_DRAFT_20260914_CN.md`（冻结 v1.0 §2.2 乙臂、§3 前置门、§4 判读、§9.5 触发条件）
- **靶机**：远端 4090（106.15.75.26:60222，`/workspace/FLUED`，env `/workspace/conda/envs/flued312stable`，fla 0.5.1 × torch 2.12.1+cu130 × transformers 5.15.1 × triton 3.7.1 × py 3.12.14——与 R2/甲臂同一硬件指纹，全周期同机同 env）
- **本地 commit 链**（本地=远端，git bundle 通道同步）：`26928d3`（施工件四文件）→ `bb54859`（真机测试修正：use_cache=False）→ `2cb6053`（attach 对齐宿主 device/dtype）→ `459d323`（判死触发件：--summ-side/--summ-ctrl）→ `3bc9ccb`（触发件装载通路 ctrl 直传）→ `46c2715`（收尾：装载通路 **side 直传修复**——strict_load_summ/attach_and_strict_reload_summ 加 side 参、启动器按戳记 `r3_summ.side` 选接线；side 回归测试 +1；事故录 §10.9）
- **单源纪律**：`r2_spec.py` 零改动（sha256 `7d20434d…5959b` 未变）；仪器本体 `tools/analysis/cross_arch/probe_e122_deltanet_book.py` 零触碰（sha256 `57ae63ad…d950` 未变）；新增件全部旗标化（`--summ` 默认关=与 R2 母列逐位不变，与 `--echo` 互斥 loud-fail）。

---

## §0 施工形态（门①体制核验・file:line 证据）

### §0.1 原件因果角色（§2.0 ①）

`DiTChunkSummarizer`（`flued/v36/model.py:391-475`；canonical_v37 形态：type=dit／dit_layers=2／pool=qpool 4 位置锚定查询 temp 16.0／backbone_mode=slm 创建 index_ffn）——对每块字节段特征做 2 层 DiT 编码+位置锚定池化，经**双头 FFN** 产出 ①memory 头 `ffn` → 段记忆向量（进 write head→KDA 状态内容）②index 头 `index_ffn` → 段索引向量（slm 态，consensus §1.1「summarizer owns the K interface」）。**嫌疑点=双头构造整体**。

### §0.2 移植构造施工形态（§2.0 ②）

**单点摘要+双头全接**（§2.2 主构造逐字执行）。施工 file:line（fla 0.5.1 于靶机 `/workspace/conda/envs/flued312stable/lib/python3.12/site-packages/fla/`；移植件于 `tools/baselines/deltanet_r2/`，commit `3bc9ccb` 终态行号）：

| 件 | 位置 | 内容 |
| --- | --- | --- |
| 构造单源 | `r3_spec.py:303-364`（常量节+解析式精算锚） | `SUMM_D=320 / SUMM_HEADS=5 / SUMM_FFN_DIM=768 / SUMM_HIDDEN=768 / SUMM_D_MEM=320`，`SUMM_NUM_PARAMS=4,972,932`（解析式），`EXPECTED_PARAM_COUNT_SUMM=53,125,828` |
| summarizer 本体 | `r3_spec.py:463` `build_summarizer(ctrl=False)` → **原类零重实现**：`from flued.v36.model import DiTChunkSummarizer`，配置投影 `_summ_cfg()`（320 维宿主适配 + qpool + slm 双头）；类常量核验 `(QPOOL_QUERIES, QPOOL_ANCHOR_TEMP)==(4, 16.0)` loud-fail；init 纪律随原件（pool_queries trunc_normal 0.02，其余默认） | 构造同构=实类实例化，非结构仿写 |
| 汇总点 | `r3_spec.py:489` `attach_summ` → `:546` `base.embeddings.register_forward_hook(_embed_hook)`：embedding 输出（层栈前 span 特征）按 **64-token 块**（`SUMM_CHUNK_TOKENS=r2spec.NATIVE_CHUNK_TOKENS=64`=fla `wy_fast.py:226` BT=64 原生铺瓦）reshape→`summ.forward_with_index(spans, valid)` → m_c/k_c per chunk；尾块不足 64 位置以 valid mask 处理（训练窗 2047 常态） | 单点摘要：每窗前向汇总一次，全 24 层共享 |
| 值侧 tap | `r3_spec.py:552` `attn.v_conv1d.register_forward_hook(_replace_hook("m_c"))`：fla `delta_net.py:213-218` `v_conv1d(x=self.v_proj(hidden_states))` 的**输出**（proj 后短卷积后、delta rule 核前）替换为 m_c 块内广播；q/k/β 原生保留（β 由 `b_proj(hidden_states)` 产出 `delta_net.py:241`，与 v 无关——源码级实证） | `v_t ← m_c`（所属块摘要替换原生 v 投影输出） |
| 地址侧 tap | `r3_spec.py:550` `attn.k_conv1d.register_forward_hook(_replace_hook("k_c"))`：fla `delta_net.py:207-212` `k_conv1d(x=self.k_proj(hidden_states))` 的输出替换为 k_c 块内广播；读侧 q 原生 | `k_t ← k_c` 广播（写侧寻址块粒度）；核内 `use_qk_l2norm_in_kernel` 对 k 的 L2 属宿主原生写址处理，k_c 同受 |
| 广播算子 | `r3_spec.py:378` `broadcast_per_chunk(pc, ref)`：`out[b,t] = pc[b, t//64]`（index_select 逐位拷贝），形状不符 loud-fail | 值侧/地址侧共享形态 |
| tap 契约 | `r3_spec.py:398` `_summ_tap_contract`：逐层核验 `q/k/v_proj+b_proj+q/k/v_conv1d` 在场、`g_proj` 禁现（use_gate=False 分支） | 结构漂移即停报 |
| 训练旗标 | `train_deltanet_r3.py:52`（`--summ` store_true 默认关）；`:70` 与 `--echo` 互斥 loud-fail；`:77-95` `build_model`：summ 才 `attach_summ`+`stamp_summ_config`，参数锚 loud-fail（关=48,152,896 与 R2 全等；开=53,125,828） | 默认关=不挂任何 hook、不建任何参数 |
| 触发件旗标 | `train_deltanet_r3.py:56-66`：`--summ-side {both,value,addr}`（乙-v2 仅值侧/乙-v3 仅地址侧：模块整体在场参数锚不变，只摘另一头 tap，`r3_spec.py:489` side 分支）；`--summ-ctrl`（参数匹配对照，`r3_spec.py:433` `PseudoDualHeadMLP`：masked mean 池化+LN+双 MLP hidden=3878+pad 56 零函数注册垫，参数 4,972,932 与主构造**精确匹配**，同 tap 点同广播机制） | §4 杀死档自动触发三件的施工形态 |
| 评测装载 | `probe_r3_echo_book.py:47-56`：config 带 `r3_summ.enabled` → 按戳记 `ctrl` 字段选挂接构造 → `r3.attach_and_strict_reload_summ`（`r3_spec.py:627`）；窗/选择链/手术/bootstrap/种子全走仪器本体（零口径改动） | 键集=构造指纹：pseudo 键集对 DiT 挂接 loud fail（单测 `test_ctrl_strict_reload_roundtrip_and_wrong_construction_loudfail`） |
| strict 白名单 | `r3_spec.py:598` `strict_load_summ` + 甲臂 `check_key_whitelist` 复用；白名单=`model.r3_summ.*` 模块参数穷举（45 键） | 缺失/白名单外/文件新增键≠白名单任一破即 RuntimeError「不点火」 |

### §0.3 不同构点清单（§2.0 ③，判读引用必带）

1. **输入域**：原件 summarizer 吃 byte-encoder 384 维特征；移植吃宿主 token embedding 320 维——**byte encoder 不入件**（件边界=池化+双头构造组，§9.2 用户裁定）。
2. **qpool 运行点漂移**：锚定查询在 64 token/块（≈161 B/块 @0.3982 tok/B）上运行；原件 ≈24 B/块——位置锚跨度大幅拉长。
3. **参数量混杂**：+4,972,932（=+10.3%），高于起草 +5% 估计——混杂④如实升级登记；归因由参数匹配对照列（`--summ-ctrl`）承接。
4. **状态无行结构**：m_c 值侧广播=语义投影非结构移植（DeltaNet 逐 token 写值 vs FLUED 逐块状态行）；k_c 广播经宿主核内 L2（原生写址处理的一部分）。
5. **噪声条件**：DiT 块的 noise_cond 以零噪声一次性评估（原件 one-shot 部署形态同款），构造保留。
6. **生成路径边界**：k/v tap 在 use_cache（增量解码）下 conv_state 语义不保——本臂只支持全窗前向（训练与判决仪器均是），不支持生成，如实登记。

### §0.4 新增参数（§2.0 ④，施工精算）

**4,972,932**（解析式 `summ_param_count_analytic()` `r3_spec.py:338` = 实例化互证，远端单测 `test_summ_instantiation_matches_analytic_anchor` 绿）：

| 分项 | 参数 |
| --- | --- |
| DiT 2 层（d=320, heads=5, ffn 768，含 norm1/norm2/attn.qkv/attn.out/ff_in/ff_out/noise_cond/attn_scale/ff_scale） | 2,506,756 |
| qpool 4 锚定查询（4×320） | 1,280 |
| memory 头 FFN（LN(1280)+Linear(1280→768)+SiLU+Linear(768→320)） | 1,232,448 |
| index 头 FFN（同构） | 1,232,448 |
| **合计** | **4,972,932**（=+10.3%；锚 53,125,828） |

宽度裁定注记：任务书钉死 d=320/heads=5/ffn 768；双头 FFN 隐宽取 768=宿主 intermediate_size 同宽（原件 summarizer_hidden=1024 是 d_byte=384 体制内宽，随输入域适配一并宿主化）；qpool 4 锚 temp 16.0 原件常量原值保留；d_mem=320=宿主 v/k 投影宽（expand=1.0）。

---

## §1 门①体制核验——PASS

- **参数锚 loud-fail**：实例化双档断言（训练器 `build_model`）+ 靶机单测 `test_param_anchor_instantiation_summ_flag`（关=48,152,896 ✓，开=53,125,828 ✓）+ `test_param_anchor_instantiation_ctrl_flag`（ctrl 列同锚 ✓）。
- **逐键 diff**：两次独立实例化（summ-on）键序列逐键一致 + summ-on 键集 = R2 母列键集 ∪ `model.r3_summ.*` 白名单恰 45 键、无任何其他差异（`test_key_diff_two_instantiations_summ_on_identical` 靶机绿）。
- **单测**（`tests/test_r3_summ.py`，本地 27 过 6 fla 门控跳过 → 靶机全量 **29/29 绿**；另甲臂 28/28 无回归）：
  - ① flag-off 逐位/逐键不变（mock + 真机 autocast bf16 前向 `torch.equal` 双层）；
  - ② 白名单 loud-fail（缺失/多出/junk/无 summarizer 键/错构造挂接五路 RuntimeError + save→from_pretrained 静默丢弃事故形态复现→strict 重载逐位复原）；
  - ③ 双头数学语义（summarizer 常数化 → m_c≡c_m/k_c≡c_k ⇒ 每层 h←h+2·(c_k⊙c_m) 闭式逐位可控形态；全零 summarizer ⇒ 层恒等逐位=embeddings→head；广播纯函数 t//64 映射；真机 fused_recurrent 与 chunk 双核路径块内逐位恒等+块向量=独立复算 summarizer 输出）。
- **梯度接通**：summarizer 全参数梯度有限且非零（qpool/双头 FFN/DiT 全在链上，真机 `test_summ_on_differs_from_mother_and_grads_finite` 绿）。

## §2 门②锚直测借用声明（坑 9）——PASS

R2 门②产物（`outputs/r2_deltanet50m_20260913/anchors/summary.json` 在机复核）：**监督 1630.1 tok/窗（1630.11328/512 窗）、原生 chunks/窗 25.98（mean 25.9766）、盲猜地板 6.3903 nats/token（均匀地板 10.3735）、tokens/byte 0.3982**。借用边界核验：同机（4090 @106.15.75.26）同 env（flued312stable）同语料（corpus_v3，sha256 前 16 `ed4ab97810776ce7`）同窗（4096B 顺序非重叠）同 tokenizer（Mistral 32K fla-hub 四文件）→ **直接引用不重测**。R2 收官基尺 **+0.1040 nat [+0.0951, +0.1125]**（`necessity_pooled_seen.json` 逐位复核）与阳性线 0.05 nat 同边界借用。166/172.7 等我们体制数未引、未借、未作分母。

## §3 门③仪器 baseline 回归——PASS

R2 母列 20K ckpt 上必要性账 40 窗复跑（**原仪器直跑**，`gate3_mother40w/`，种子 424242，仪器默认参数）：**point +0.1020 nat [+0.0334, +0.1770] 排零**；40/40 窗、0 空窗、0 截断；推理 7.4s。落点与在册参照（+0.1020 [+0.0334,+0.1770]，甲臂门③同数）一致——方向带内（在册带=池化 +0.1040 [+0.0951,+0.1125]），仪器活。仪器本体 sha256 施工前后未变（见单源纪律）。

## §4 门④冒烟 500 步——PASS（含 flag-off 逐位验收）

两列冒烟（同机同种子同数据序；`smoke500_summ/`、`smoke500_flagoff/`）：

| 项 | 乙开启（--summ） | 旗标关（默认） | R2 母列参照（在册） |
| --- | --- | --- | --- |
| loss_ema@500 | **6.0278**（漂移如实登记：summarizer 改信息流，下降更快，不卡 R2 带） | **6.3761** | 6.376 |
| NaN/发散 | 零 NaN，watchdog 零触发（diverged: null） | 同左 | 零触发 |
| skipped_partial | 0 | 0 | 0 |
| 峰值显存 | alloc 2379 MiB / reserved 5938 MiB | alloc 2414 MiB / reserved 6084 MiB | alloc 2406 / reserved 3844 |
| 参数锚 | 53,125,828 loud-fail 过 | 48,152,896 loud-fail 过 | 48,152,896 |

- **flag-off 逐位验收（硬验收）**：对 R2 母列 `smoke500/train_log.jsonl` 逐记录逐字段比对（step/loss/loss_ema/lr/tokens_in_window 五字段，剔计时字段）——**BITWISE_MATCH，25/25 记录逐位一致**。
- **种子异源**：`resolved_config.json` train_seed=42 / eval_seed=424242；全套超参照抄 R2（lr 3e-4 / warmup 1024 / betas (0.9,0.95) / wd 0.1 / clip 1.0 / watchdog 1000 / 窗 4096B / 截 2048 / batch 1）。
- **白名单落盘**：`summ_whitelist.json` 45 键（`model.r3_summ.pool_queries` … `model.r3_summ.index_ffn.3.bias`）。

## §5 门⑤活性账 40 窗预跑——留档完成（不判读）

乙冒烟 ckpt（`smoke500_summ/latest`）上经**启动器**（`probe_r3_echo_book.py` 乙档装载）40 窗（`gate5_summ40w/`，种子 424242）：point **+4.6e-05 ≈ 0**，CI [−0.000448, +0.000594] 含 0——与甲臂冒烟件 40 窗（≈0 族）同形态（未训练至必要性行为显形），如实留档不判读。**副产品**：仪器侧乙档装载通路实证（fingerprint `r3_summ.n_summ_keys=45`，strict 白名单重载在仪器内走通）。

## §6 门⑥报价与显存表——PASS（报价兑现）

| 项 | 实测（4090，本机同 env） | R2 参照 |
| --- | --- | --- |
| 步速（整程均值） | 乙 **72.4 ms/步**；flag-off 75.6 ms/步 | 81.5 ms/步 |
| 乙开销（对内同码对） | **≈0（噪声内不可分辨，−4%~+0%）**——起草 +6–10% 未兑现：summarizer 单点 ≈2 layer-equivalent 前向（batch 1、32 块）淹没在 kernel launch 噪声内；绝对步速同甲臂低于 R2 母列（triton 缓存跨进程复用，甲臂 §9.5 同款如实并置） | — |
| 20K 墙钟报价 | 20,000×72.4ms ≈ 24.1 min ≈ 0.40 GPU·h | 实测 1,492.7s |
| 训练峰值显存 | **alloc 2444 MiB / reserved 8922 MiB**（24G 卡余量充裕） | alloc 2406 / reserved 3844 |
| 判决仪器全套（4 块×500 窗+池化） | 实测 ≈8 min | — |

## §7 点火与训练收官

- **点火**：2026-09-14，前置门六件全绿后按预授权直接点火。命令形态：`nohup python tools/baselines/deltanet_r2/train_deltanet_r3.py --corpus /workspace/corpus/corpus_v3.txt --tokenizer-path /workspace/models/delta_net-1.3B-100B --out-dir outputs/r3_transplant_summ_20260914/main20k_summ --max-steps 20000 --summ > …/main20k_summ.log 2>&1 &`（点火前 duplicate 检查：GPU 0%/98MiB、0 python 进程）。
- **训练事实**：**20,000 / 20,000 整**（零中断，skipped_partial=0）；**ema 4.8126**（母列 3.0244 / 甲臂 3.0614——乙改信息流，绝对 loss 大幅漂移**如实登记不判读**：全部 v 写值被 32 块摘要替换，信息瓶颈显形于 LM 损失；仍在盲猜地板 6.39 之下）；**看门狗零触发**（diverged: null）；**墙钟 1,440.5 s = 24.0 min ≈ 0.400 GPU·h**（报价 24.1 min 兑现）；峰值显存 alloc 2444 / reserved 8922 MiB；里程碑 ckpt 正常落盘。
- **同卷构成**：判决仪器与 R2 收官同款同种子（424242 选择链/424243 bootstrap），计分位 n_sel=48,231 / n_ctl=43,810 与母列/甲臂**逐位相同**。

## §8 判决仪器（500 窗×4 块+池化）——报数完成（判读权归主会话）

口径：E122 同源仪器零口径改动（启动器仅装载注入）；与 R2 收官**同卷**（同窗集 start-window 0/500/1000/1500、同选择链、同池化 2000 次 bootstrap 种子 424243）。

| 块 | 窗域 | point (nat) | CI95 | 排零 | 窗数 |
| --- | --- | --- | --- | --- | --- |
| b0 | 0-499 | +0.00038 | [−0.00030, +0.00102] | ✗ | 500/500 |
| b1 | 500-999 | +0.00026 | [−0.00060, +0.00108] | ✗ | 500/500 |
| b2 | 1000-1499 | +0.00047 | [−0.00033, +0.00138] | ✗ | 500/500 |
| b3 | 1500-1999 | −0.00034 | [−0.00120, +0.00048] | ✗ | 500/500 |
| **池化（判决件）** | 2000 窗 | **+0.00019** | **[−0.00023, +0.00059]** | **✗（CI 含零）** | 2000 |

- 计分位：池化 n_sel=48,231 / n_ctl=43,810（与母列/甲臂逐位相同）；mean_sel 0.00048 / mean_ctl 0.00029；仪器自家 verdict 字段原样转录：「剂量未落——DeltaNet 跨架构复证未过（CI 含 0）」。
- **三档机械落档**（预注册 §4；基尺=母列 +0.1040 [+0.0951,+0.1125] 与阳性线 0.05 nat）：
  - **杀死**（CI 上界 < 0.05）：CI 上界 **+0.00059 < 0.05** → **落**；
  - 不确定（CI 与 0.05 相交）：上界 0.00059 < 0.05，不相交 → 不落；
  - 无辜：不落。
  - **机械落档=杀死档**。极端子格注记：CI 上界 <0 未落，但 **CI 含零**（账点估 +0.00019 ≈ 0）——「手术毒性使必要性效应完全消失」形态，比「部分压低」更强，如实登记归主会话。
- **触发器落档**：杀死落 → 冻结令三件**全部自动触发**，见 §9。
- **判读必带混杂注记**（§4 预注册，乙臂四条）：①输入域不同构（byte-encoder 384 维 → 宿主 embedding 320 维，byte encoder 不入件）；②qpool 运行点漂移（64 tok/块 ≈161B vs 原件 ≈24B/块）；③参数量 +10.3%（高于起草 +5%，对照列已跑）；④状态无行结构=语义投影。判词限定范围：「DeltaNet-50M × corpus_v3 × 4096B × 20K × 本仪器族 × 同机同 env」。

## §9 判死触发链执行（冻结令自动三件；预算 3.5 GPU·h 封顶内调度）

编排：`outputs/r3_transplant_summ_20260914_trigger_chain.sh`（远端串行单卡；全链日志 `trigger_chain.log`）。

### §9.1 种子加固 s1（seed 1，同卷）

- 训练：20,000/20,000 整，**ema 4.8613**，看门狗零触发，墙钟 24.1 min（0.401 GPU·h），alloc 2444 MiB。
- 判决池化（同卷同种子谱系）：**+0.00013 [−0.00020, +0.00046]**，CI 含零——**与主列同格复现**（≈0 族）。

### §9.2 种子加固 s2（seed 2，同卷）

- 训练：20,000/20,000 整，**ema 5.0935**，看门狗零触发（diverged: null），skipped_partial=0，墙钟 1,425.0 s = 23.7 min（0.396 GPU·h），峰值 alloc 2444 / reserved 8924 MiB。
- 判决四块（500 窗×4，同卷）：b0 +0.00022 [−0.00030, +0.00073]／b1 +0.00034 [−0.00022, +0.00093]／b2 +0.00046 [−0.00005, +0.00103]／b3 +0.00019 [−0.00045, +0.00084]，窗数全 500/500。
- 判决池化：**+0.00030 [+0.00004, +0.00058]**，n_sel=48,231 / n_ctl=43,810（逐位同主列），n_boot_valid=2000，种子 424243。
- **机械落档**：CI 上界 **+0.00058 < 0.05** → **死档，与主列同格复现（2/2）**。
- **如实注记**：本列 CI 排零（`ci_excludes_zero=true`），仪器自家判词=「跨架构必要性复现实存（弱）——剂量部分在板」；但机械三档尺=预注册绝对线 0.05 nat（§4；坑 9 实例③注记：判据是绝对预注册线、同种子同卷，无跨种子换锚问题），点估 +0.00030 ≪ 0.05 → 死档落格不变。仪器判词与机械线语义不同源，分歧原样并置，判读归主会话。

### §9.3 参数匹配对照列（--summ-ctrl，seed 42）

- 构造：`PseudoDualHeadMLP`（masked mean 池化+LN+双 MLP hidden=3878+pad 56 零函数注册垫），参数 **4,972,932 与主构造精确匹配**，参数锚同 53,125,828 loud-fail 过；同 tap 点同广播机制，仅摘要器本体替换（`summ_construction.component` 字段在案）。
- 训练：20,000/20,000 整，**ema 2.4745**（远低于主列 4.8126——对照构造训练动力学不同源，如实登记不判读），看门狗零触发，skipped_partial=0，墙钟 1,373.1 s = 22.9 min（0.381 GPU·h），峰值 alloc 2379 / reserved 8636 MiB。
- 判决四块（同卷）：b0 −0.00158 [−0.00901, +0.00546]／b1 +0.00062 [−0.00641, +0.00767]／b2 −0.00362 [−0.00927, +0.00232]／b3 +0.00162 [−0.00376, +0.00702]，窗数全 500/500。
- 判决池化：**−0.00075 [−0.00399, +0.00233]**，CI 含零，n_sel/n_ctl 逐位同主列。
- **机械落档**：CI 上界 **+0.00233 < 0.05** → **死档**。归因语义（素材归主会话）：参数精确匹配对照同落死档 → 「+10.3% 参数量」与「双头构造」两假设在本列不可分（对照构造均值通道同被杀），判读引用必带。
- 形态注记（不判读）：ctrl 列 mean_sel 0.01868 / mean_ctl 0.01943，较主列（0.00048/0.00029）大约 40×，CI 带宽约 8×——对照构造两侧术前损失水平与主列不同源，contrast 口径仍可比，绝对水平差异如实登记。

### §9.4 去消融变体（--summ-side value / addr，seed 42）

模块整体在场、参数锚不变（53,125,828 loud-fail 双列均过），只摘另一头 tap——头级归因件。

**乙-v2 仅值侧（value，k 地址侧 tap 不挂）**：

- 训练：20,000/20,000 整，**ema 4.2792**，看门狗零触发，skipped_partial=0，墙钟 1,512.1 s = 25.2 min（0.420 GPU·h），峰值 alloc 2515 / reserved 8822 MiB。
- 判决四块（同卷，side 直传修复后重跑，指纹 side=value 在案）：b0 −0.00044 [−0.00288, +0.00177]／b1 −0.00051 [−0.00252, +0.00143]／b2 −0.00069 [−0.00276, +0.00144]／b3 −0.00013 [−0.00226, +0.00211]，窗数全 500/500。
- 判决池化：**−0.00044 [−0.00152, +0.00059]**，CI 含零，n_sel/n_ctl 逐位同主列 → CI 上界 **+0.00059 < 0.05** → **机械死档**。
- 订正注记：本列判决首跑曾踩装载通路缺侧 bug（以双头全接评测，得 −0.00026 [−0.00119, +0.00069]），修复后按原命令形态同卷重跑订正为上数；错构产物归档 `_incident_side_loader_bug_20260914/`（事故录 §10.9）。

**乙-v3 仅地址侧（addr，v 值侧 tap 不挂）**：

- 训练：20,000/20,000 整，**ema 3.0689**，看门狗零触发（diverged: null），skipped_partial=0，墙钟 1,506.4 s = 25.1 min（0.419 GPU·h），峰值 alloc 2511 / reserved 9060 MiB。
- 判决四块（同卷，side 直传修复后由链自动执行，指纹 side=addr 在案）：b0 −0.00004 [−0.00435, +0.00439]／b1 −0.00240 [−0.00786, +0.00280]／b2 −0.00284 [−0.00750, +0.00153]／b3 +0.00030 [−0.00305, +0.00370]，窗数全 500/500。
- 判决池化：**−0.00122 [−0.00335, +0.00097]**，CI 含零，n_sel/n_ctl 逐位同主列 → CI 上界 **+0.00097 < 0.05** → **机械死档**。
- 形态注记（不判读）：addr 列 mean_sel 0.01169 / mean_ctl 0.01292，较主列约 24×——地址侧单接时两侧术前损失水平整体抬高（块内同址写引发的检索地基变形），contrast 口径仍可比，绝对水平差异如实登记。

### §9.5 触发链六列机械落档总表（判读归主会话）

| 列 | seed | 池化 point (nat) | CI95 | 机械落档（0.05 预注册线） |
| --- | --- | --- | --- | --- |
| 主列 both | 42 | +0.00019 | [−0.00023, +0.00059] | **死档**（上界 0.00059<0.05） |
| 种子加固 s1 | 1 | +0.00013 | [−0.00020, +0.00046] | **死档，同格复现 1/2** |
| 种子加固 s2 | 2 | +0.00030 | [+0.00004, +0.00058] | **死档，同格复现 2/2**（CI 排零注记 §9.2） |
| 参数对照 ctrl | 42 | −0.00075 | [−0.00399, +0.00233] | **死档**（上界 0.00233<0.05） |
| 去消融 value | 42 | −0.00044 | [−0.00152, +0.00059] | **死档**（订正后，§10.9） |
| 去消融 addr | 42 | −0.00122 | [−0.00335, +0.00097] | **死档** |

六列 2000 窗池化 CI 上界全在 0.05 线下 ≥2 个数量级——乙臂主构造、两单头变体、参数匹配对照在本体制内全灭（机械事实陈述，结局格归因判读归主会话）。

## §10 事故与如实注记

1. **远端 GitHub 认证持续断连**：`git fetch origin` 于远端连续失败（could not read Username）——本臂全程走 git bundle 增量通道（5 只 bundle：`f78027a..26928d3`、测试修正、device 修正、触发件、装载通路，逐只 sha256 对拍 + `git bundle verify` 过），本地（可认证 GitHub）`origin/copilot/implement-stage-a-experiments` = ee57f9c 未动，本地=远端=3bc9ccb。
2. **远端未跟踪杂物**：`run_d1_10k_20260904.sh`、`run_d1_smoke_20260904.sh`（远端独有，甲臂 §9.2 在册同款）——同步 stash 往返后原样保留未触碰。
3. **fla 0.5.1 × transformers 5.15.1 新坑（本臂新增第三、四坑，随案登记）**：③ eval 态前向（use_cache 默认开）进 fla 缓存路径撞 transformers 5.15.1 缓存 API（`fla/models/utils.py:399` FLALayer 抽象类缺 `get_max_length` 实现崩溃）——测试/仪器前向一律 `use_cache=False` 或训练态（首跑单测拦截，f78027a）；④ 仪器装载序=模型已 bf16 CUDA 就位后挂接，新模块须对齐宿主 device/dtype（`attach_summ` 内 `next(model.parameters())` 对齐，2cb6053——首跑门⑤拦截）。
4. **pseudo 构造广播 bug 被单测拦截（点火前）**：`PseudoDualHeadMLP` 池化分母 `keepdim=True`+`unsqueeze(-1)` 双重致 (B*C,1,1)，LN/MLP 广播出跨块污染——参数锚不受影响但前向形状/语义错，`test_pseudo_ctrl_param_anchor_exact` 形状断言拦截后修正（459d323）。甲臂教训③（单测链先于点火拦截 bug）同款复证。
5. **loss 大幅漂移如实登记**：乙 20K ema 4.8126 vs 母列 3.0244（+1.79 nat）——信息流改变（全部 v 写值=32 块摘要/窗）的直接后果，冒烟条款「不卡绝对带」适用（§3.4）；必要性账测手术效应非绝对损失，两账独立。
6. **门⑤首跑 device 错**（见注记 3④）：判 «仪器先拦截、修正后续跑»，无产出污染。
7. **GPU 共租**：本臂全周期无共租（点火前与全链执行中 GPU 独占复核，72-74ms/步稳定）。
8. **镜像纪律（匿名化预检）**：本臂施工件含项目身份词，同甲臂 §9.7 注记——若纳入镜像同步范围需先扩充身份词表（提交主会话裁定）。
9. **装载通路缺 side 直传事故（收尾 agent 侦获+修复，46c2715）**：判决装载通路（`probe_r3_echo_book.py` 乙档 → `attach_and_strict_reload_summ` → `strict_load_summ`）只读戳记 `ctrl`、**从不读 `side`**，`attach_summ` 恒以默认 both 挂接——value/addr 去消融列的判决若照跑将以「双头全接」评测（错构造）。侦获时点：value 列判决已按错构跑完（−0.00026 [−0.00119,+0.00069]），addr 列判决未点火。处置：①装载链三级加 side 直传（缺省 both 回退保老戳记兼容），fingerprint 增 side 字段留档；②mock 级直传验证+回归测试 `test_side_threading_through_eval_loader`（value/addr/both 三态 hook 在场性断言），远端 31/31 绿；③修复于 addr 判决前落位 → addr 四块由链自动以正构执行（log「side=addr」、指纹在案）；④value 四块+池化按原命令形态同卷重跑订正（−0.00044 [−0.00152,+0.00059]），错构产物全量归档 `_incident_side_loader_bug_20260914/`（权重无涉——训练期 side 接线由训练器正确传递，事故仅限评测装载面）。落档档位不受订正影响（两跑同属死档），但点估/CI 数值以订正后为准。教训谱系：甲臂坑 8（from_pretrained 静默丢键）同款「装载面最后一厘米」族——装载通路的旗标直传完整性自此入回归测试。
10. **远端工作树状态注记**：远端 repo 停于 3bc9ccb + 本次 side 修复两文件的工作树改动（未 commit，内容与本地 46c2715 语义全等；远端 r3_spec.py 不含本地 3bc9ccb 后的丙节内容，两版本 summ 装载区逐字一致）；tests/test_r3_summ.py 已 scp 同步（与本地逐位一致）。主会话统一推本地链后，远端以 stash/ checkout  reconcile（无冲突面）。

## §11 产物清单（远端 `/workspace/FLUED/outputs/r3_transplant_summ_20260914/`；本地同名目录回拉全量元数据/日志/仪表产物，不含权重）

| 路径 | 内容 |
| --- | --- |
| `R3_SUMM_RECEIPT_20260914.md` | 本回执（远端+本地同名） |
| `gate3_mother40w/`（summary/items/audit）+ `.log` | 门③仪器 baseline 回归（+0.1020 排零） |
| `smoke500_summ/`（summary/train_log/resolved_config/summ_whitelist/latest+ckpt）+ `.log` | 门④乙冒烟（ema 6.0278） |
| `smoke500_flagoff/` + `.log` | 门④旗标关冒烟（BITWISE_MATCH 验收件） |
| `gate5_summ40w/` + `.log` | 门⑤40 窗预跑（≈0 留档；仪器内乙档装载实证） |
| `main20k_summ/`（latest + model_step{500..20000} + summary/resolved_config/summ_whitelist）+ `.log` | 20K 主列全量（权重留远端待归档盘裁定，归档走 K:/N: 纪律） |
| `verdict_b{0,1,2,3}/`（summary/items/audit）+ `.log`、`necessity_pooled_seen.json` + `pool.log` | 判决仪器四块+池化（+0.00019 [−0.00023,+0.00059]） |
| `main20k_summ_s{1,2}/` + `verdict_s{1,2}_b{0..3}/` + `necessity_pooled_s{1,2}.json` | 种子加固两列全量 |
| `main20k_summ_ctrl/` + `verdict_ctrl_*` + `necessity_pooled_ctrl.json` | 参数匹配对照列全量 |
| `main20k_summ_{value,addr}/` + `verdict_{value,addr}_*` + `necessity_pooled_{value,addr}.json` | 去消融两列全量（value 判决=side 修复后订正跑；addr 判决=修复后链自动跑） |
| `_incident_side_loader_bug_20260914/`（错构 value 四块+池化+log 全量） | 事故 9 证据归档（装载通路缺 side 直传的错构首跑产物，不丢令） |
| `../r3_transplant_summ_20260914_stage.sh`、`../r3_transplant_summ_20260914_trigger_chain.sh` + `trigger_chain.log` | 施工编排与触发链编排（远端 outputs/ 下，随案登记） |

**成本**：冒烟×2（~2 min）+ 门③/⑤（~1 min）+ 20K 主列 0.400 GPU·h + 判决仪器主列（~8 min）+ 触发链五列训练 7,260.9 s ≈ 2.017 GPU·h（s1 1,444.3 / s2 1,425.0 / ctrl 1,373.1 / value 1,512.1 / addr 1,506.4 s）+ 触发列判决六套（5×~2.5 min + value 订正重跑 2.4 min）≈ 0.25 GPU·h ≈ **2.7 GPU·h 全案 < 3.5 封顶**。硬件指纹：RTX 4090 24G @106.15.75.26 × fla 0.5.1 × transformers 5.15.1 × torch 2.12.1+cu130 × triton 3.7.1 × py 3.12.14；一切读数同机同 env 内成立，跨硬件只比方向（坑 9）。
