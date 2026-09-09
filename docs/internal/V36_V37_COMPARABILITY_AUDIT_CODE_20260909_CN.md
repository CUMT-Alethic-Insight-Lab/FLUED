# v3.6 线 vs v3.7 线 代码/配置层可比性审计报告

审计对象：`flued/v36/model.py`、`tools/train/v3_6/train_v36_s1.py`、`tools/train/v3_6/train_v36.py`、`tools/train/v3_3/train_v33.py`（共享数据/网格件）、`flued/data.py`、`configs/canonical_v36.json`、`configs/canonical_v37.json`、`tests/test_canonical_sync.py`。两条线共用同一训练器与同一 `V36Config`，分岔全部由 `backbone_mode` 驱动（slm 与否），这是理解全部 7 轴的总钥匙。

---

## 轴 1 损失语义差

**结论：completion 目标网格在两代 canonical 之间语义不同；direct 同形不同条件；predict 同形不同锚；frozen-decoder CE 只在 v36 线存在且已判负禁用。**

- 基网格共用：`make_targets`（tools/train/v3_3/train_v33.py:159-171），(B, max_chunks, max_span) per-chunk 布局。
- **v36 线（attn/xattn/paged/draft）**：completion 网格由 `--cumulative-mask-retention` 控制，现行默认 True（tools/train/v3_6/train_v36_s1.py:3171 else 分支、3848-3858；configs/canonical_v36.json:74）。v36.8 的语义变化确切内容在 `make_cumulative_retention_targets`（train_v36_s1.py:2470-2544）：**第 i 行不再只还原 chunk i 的遮蔽字节，而是追加还原 0..i-1 段全部遮蔽字节**（pre-v36.8 为 per-chunk"零保持"配方，docstring 2478-2496 自陈三任务保持信号恰为零）；超 max_span 截断计入 `retention_truncated_slots`。`_completion_target_grids`（2547-2566）是开关分发点。canonical_v36.json:5 usage_note 的"语义已变"即此。
- **v3.7 线（slm）**：`--cumulative-mask-retention` **失效**，分形改由 `v_row_source` 驱动——`slm_coarse_v = (v_row_source=="state")`（train_v36_s1.py:3170-3171）：a/b 格（v=memory）completion 用 **per-chunk 基网格**（联合监督达成全覆盖，consensus §2），c/d 格（v=state）completion **和 direct** 都用累积网格（3162-3168 注释、3194-3201 coarse direct 走 `make_cumulative_retention_targets(source, ...)` 的 as-encoded 累积版）。canonical_v37.json:5 明示"旗标只管 xattn 旧路径"。
- **direct**：两线目标同为 as-encoded（遮蔽位目标=MASK_ID，3193-3205），但条件不同——v36 线 `decoder_in(content)+pos`，content=KDA 状态机 per-chunk 读出 S_i（2569:2609-2615）；v37 a/b 格 `decoder_in_mem(memory)+pos`、c/d 格 `decoder_in(V~)+pos`（2895、2914、model.py:2495-2496）。
- **predict**：两线默认都是 latent MSE（`predict_mode=latent`，两 canonical:62）。锚不同：v36 线锚 `decoder_in(content)[:,1:]`（3347-3356）；slm 锚 `dec_in(v_rows)[:,1:]`（3321-3346）。frozen-decoder CE（`predict_mode=decode`，3363-3378，经 `_frozen_decoder_logits` 3012-3029 全 detach decoder）只在非 slm 路径可达，且被标注为"E34-poisoned loss form"（4063-4072）；slm 模式响亮拒绝（3327-3332、4081-4085）。codec_final 臂 predict 整个关闭（3265-3272、4363-4371）。

**判词：canonical_v36 vs canonical_v37 的 completion_loss/backbone 系指标不可比（累积网格 vs per-chunk 网格，分母与任务需求都不同）；direct 带注记可比（目标同形同 mask 流，条件通道不同）；predict 带注记可比（同形 MSE、不同锚）；v36.8 前后绝对值不可比（官方自陈）。**

## 轴 2 指标定义差

**结论：train_log/summary 同 schema（零占位纪律），但同键不同义的坑真实存在，集中在 backbone 系与 state_norm。**

- 指标字典统一构造于 step_model（train_v36_s1.py:3626-3676），臂列"关态零占位"纪律贯穿（3677-3761 各处注释）。
- `direct_acc`（3633）：同定义（对 encoded 网格 argmax 命中率），但 slm c/d 格 encoded 网格是累积版（3194-3201）→ 跨格同键不同分母；a/b 格与 v36 线同形。
- `backbone_acc`/`backbone_masked_acc`/`backbone_unmasked_acc`（3634-3636）：基于 comp 网格 → 继承轴 1 的网格差，**跨线同键不同义**。
- eval 键：`evaluate` 统一加 `eval_` 前缀（3794-3816），`eval_backbone_ppl=exp(eval_completion_loss)`、`eval_direct_ppl=exp(eval_direct_loss)`（3817-3818）→ PPL 直接继承损失口径差。
- `state_norm`：v36 线恒为真实状态范数；slm a 格无状态机时是**零占位**（model.py:2468-2471、trainer 注释 2430-2433）→ 同键一实一零。
- `key_mu/key_mu_k` 等 E80 仪表只在 slm 模式注入（3762-3765，`_key_geometry_metrics` 2950-2998），v36 线 log 里无此键（缺席非零）。
- `predict_cos` 同键不同锚（轴 1）。`content` 通道在 slm 退役（2931，consensus §4）。
- eval 确定性：两线共用 `eval_mask_seed=1042`（两 canonical:22；evaluate 3796-3806 重播 mask/cloze/retrieval/burst 四条流）→ eval 遮蔽面同口径。

**判词：direct_acc/eval_direct_ppl 带注记可比；backbone_acc/eval_backbone_ppl/predict_cos/state_norm 跨线不可比或仅在严格同格内可比；key_* 系列不可跨线引用（v36 线缺席）。**

## 轴 3 数据管线差

**结论：数据管线代码与流种子两代完全同源；窗流由 seed 决定与线无关；但语料版本不由配置层钉死（data_path 是占位符），跨线比较必须在启动命令层核对。**

- 两代共用 `make_dataloaders`（tools/train/v3_3/train_v33.py:489-530，经 train_v36_s1.py:180 import）。两 canonical 数据键逐键相同：streaming_train/eval=true、seq_len=512、stride=512、batch=8、stream_samples_per_worker=50000、seed=42（canonical_v36.json:9-21 vs canonical_v37.json:9-21）。
- 流式窗= mmap 随机偏移抽样（flued/data.py:130-194），worker_seed=seed+id×10000（161-163）；**eval 流固定 seed+9999**（train_v33.py:500-504）——两代同流，同 seed 同窗序列。坑 9 注记成立：窗流随训练 seed 变，跨 seed 判读须同卷复测。
- mask 配方两代逐键相同：mask_mode=mixed、mask_prob=0.05、char 40%/BPE-word 60%（两 canonical:55-60；`make_mixed_mask` train_v36_s1.py:2400-2456；`_MASK_GENERATOR` seed=args.seed，4379）。
- 语料版本：两 canonical 的 `data_path` 均为占位符 `"data/corpus.txt"` 且 usage_note 要求显式传（:8、:5）。S0'' init 是 v4 教师产物（`s0pp_pro_v4_sft_20260805`），训练主流语料为 corpus_v3（docs/CURRENT_STATE.md:1246"23.8GB v3 语料"）；v4 仅作域外复测（:119 E51）。**配置层不锁定语料**——跨线可比性由运行命令保证，不由 repo 保证。
- E123 的窗索引=训练流序，硬性要求 batch_size=1+streaming（train_v36_s1.py:4299-4302），其决策日志不可跨 batch/跨流式设置迁移。

**判词：同 seed+同 --data-path 下带注记可比（同流同 mask 同 eval 窗）；语料路径/版本是配置外变量，引用时必须显式核对。**

## 轴 4 段界器与编码器处置

**结论：两代 canonical 的 S0'' 冻结接管完全同款（同 init、同 freeze_prefixes），此轴上两代 canonical 彼此可比；from-scratch 臂与冻结接管臂是两种体制，绝对值不可比。**

- S0'' 预训练器：`tools/train/v3_6/train_s0_segmentor.py`——教师标签窗打包（41-72）、per-byte BCE（pos_weight=12，219-225）、可训范围=byte_lookup/encoder_blocks/segmentor 前缀（195）。
- 接管：两 canonical `init_checkpoint` 同指 `K:\FLUED_archive\s0pp_pro_v4_sft_20260805\latest.pt`（v36:85、v37:86），`freeze_prefixes` 同为 `byte_lookup,encoder_blocks,segmentor_blocks,segmentor_head`（v36:86、v37:87）。加载走静默形状过滤（train_v36_s1.py:4448-4458），冻结在 4476-4488；全冻时前端整体出 autograd 图（model.py:2376-2401 `_front_end_frozen`）。
- from-scratch 臂（freeze_prefixes 空+init_checkpoint 空，如 E121 a 格 43.9M 臂，CURRENT_STATE:192）：前端参训 → 段界分布在训练中漂移 → chunk 网格与冻结基座不同分布，codec 读数与冻结接管臂绝对值不可比（E121 自己注明"from-scratch 10K 骨干 burst 能力未成熟，Δ=0 与骨干未熟不可分离"）。
- 体制切换的代码先例：E120 乙列强制清空 freeze_prefixes 转全解冻（train_v36_s1.py:4203-4210），并打印覆写——体制变化是显式事件，不是静默漂移。

**判词：两代 canonical 之间可比（同基座同冻结面）；from-scratch ↔ 冻结接管跨体制不可比绝对值，只能比臂内 Δ。**

## 轴 5 KDA 状态机在场性

**结论：v36 线状态机恒在且是 content 通道唯一来源；v37 线状态机是按格条件创建的可选 interpreter，a 格结构性缺席；E119/E120 改装件全部挂在 v37 线。**

- v36 线（非 slm）：`write_head`+`state_machine` 无条件创建（model.py:2264-2266），`content=package.mean(dim=2)`（train_v36_s1.py:2609-2612）喂 direct 与全部 backbone 形态。
- v37 slm：按通道创建——`k_row_source=="state"` → `write_head_k`/`state_machine_k`；`v_row_source=="state"` → `write_head`/`state_machine`；**a 格 (index,memory) 两者都不建**（model.py:2286-2291，注释 2283-2285"a ruling, not an omission"）。`_slm_store_rows`（2425-2474）：state 通道行=KDA 读出 K~/V~，直通通道行=index/memory 本体；a 格 `state_norm` 零占位（2468-2471）。
- `kda_impl` fla/torch：`KDAStateMachine._forward_fla`/`_forward_torch`（model.py:959/1006；fork2 多视图分支 689-717）。两 canonical 均 fla（v36:90、v37:91），**但 a 格无状态机 → kda_impl 在 a 格是死键**，只在 b/c/d 格与 v36 线有意义。
- `readout_query`/`realign`：KDAStateMachine 生产读出件（model.py:630-637），v36 线是唯一读出；slm c/d 格同件；E120 换件时照跑但出链外只留 state_norm 诊断（model.py:2456-2462）。
- 改装件挂载：**E119/Q20 多槽读出**=b 格（k=state,v=memory）K 通道 post-state→direct 口，独立 `model.multislot_readout`（model.py:2336-2351；trainer 2905-2913、`_multislot_readout_rows` 1648-1656）；**E120 换件**=d 格 V 通道 v_rows 整行换源（model.py:335 config、2456-2460、E120WarmReadout 1293-1348；trainer 4158-4210）。两者结构性要求 slm，v36 线不存在挂载点。fork2 `readout_views>1` 同理只作用于 state 通道（model.py:644-656、_slm_forward 2886-2893）。

**判词：状态机在场性本身是 grid 变量——a 格 vs v36 attn 之间"KDA 贡献"归因不可比；c 格与 v36 线最接近（均有 V 状态机+同一 readout_query/realign），但读出消费拓扑不同（store 行 vs content 通道），只带注记可比。**

## 轴 6 配置兼容与 parser 默认漂移

**结论：`--config` 经 `parser.set_defaults(**json)` 合并（train_v36_s1.py:4048-4055），老 resolved_config 缺键=现行默认静默填补——坑 8 的对偶敞口在跨代加载时系统性存在；互斥校验覆盖面良好。**

- **summarizer_pool**：parser 默认已翻 qpool（train_v36.py:384-393），V36Config 默认 qpool（model.py:250）。canonical_v37.json:92 显式钉 qpool；**canonical_v36.json 无此键** → v36 线 canonical run 也静默吃 qpool，而 v36 证据基线（E30 等）全部早于 v37.3/E100。v37.1 及更早基座的 resolved_config 无此键 → 老配置新 parser 下 summarizer 架构静默翻转（ffn/index_ffn 输入宽变，model.py:402、236-238），坑 8 实例的原文场景。qpool↔mean ckpt 互不加载是 loud by design，但"老配置+新默认+通用 init 加载"路径会把缺键静默跳过。
- **build_model 双重默认分叉**：`build_model` 对 summarizer_pool 的 getattr 兜底是 `"mean"`（train_v36.py:93），与 parser 默认 qpool 不一致——绕过 CLI 直接调 build_model 与走 CLI 行为不同。
- **seed_source**：parser 默认 `"v"`（train_v36.py:338-346），canonical_v37 显式 `"k"`（:72）；v37.1 老配置无此键 → 静默回 v（种子语义翻转：seed=align_K(index) vs align_V(memory)，model.py:1747-1748）。
- 新增臂旗标默认全关+条件创建，老配置安全（train_v36.py:102-106 getattr 兜 False；model.py:2336、2356）。
- 互斥校验覆盖：slm×codec_final/predict-decode/prefix（train_v36_s1.py:4073-4087）；denoise/Q20/E120/D1/E123/Q18 各自响亮校验（4113-4314），E123 与 11 个历史臂显式互斥（4303-4314）；模型构造层再守一道（model.py:2243-2263、2337-2351、2356-2366）。
- Q18 的 `_q18_base_config_defaults` 把基座 resolved_config 回填 parser defaults（2229-2240）——与坑 8 注记同款敞口：基座之后新增的键仍由现行默认填。
- 守卫：test_canonical_sync.py 守 v35、v36（curated keys 95-141、S1 层 184-196）、v37 解析锚（224-238）；但 v36 侧 curated 清单不含 summarizer_pool/seed_source → 该漂移面不受守卫。

**判词：跨代加载老 resolved_config 必须显式携带历史口径旗标（--summarizer-pool mean、--seed-source v 等），否则不可比且静默；现行两 canonical 自身在 qpool 下同形。**

## 轴 7 checkpoint 兼容

**结论：两代 state_dict 键集结构性不同；strict 路径（eval_only、resume、臂内全键校验）安全且响亮，通用 init_checkpoint 路径静默形状过滤——跨代加载会静默丢键产残缺基座。**

- 键集差：slm 特有 `summarizer.index_ffn.*`（仅 slm 创建，model.py:415-421）、`decoder_in_mem`（仅 slm 细 V，2295-2296）、SLMBackbone 的 `align_k/align_v/q_proj/self_blocks.*`（1621-1663）；按格条件创建 `write_head(_k)`/`state_machine(_k)`（2286-2291）；`decoder_in` 只在非 slm 或 coarse-V 存在（2302-2305）；v36 线则是恒在的 write_head/state_machine+TinyBackbone/CrossReadBackbone。qpool 改变 `summarizer.ffn.1`/`index_ffn.1` 输入宽（model.py:402-411）→ 同线跨池化也不兼容（loud by design，236-238）。
- 先例（条件创建纪律）：aux_recon（2309-2329）、multislot_readout（2330-2351）、e120_readout（2352-2367）、readout_views/to_k_center/to_k_whiten 用 persistent=False buffer 保老 ckpt strict-clean（197-203、644-656）。
- 加载路径分三级：①`--eval-only` strict=True（train_v36_s1.py:4442）→ 跨代直接炸（安全）；E120 甲列豁免新件键但双向核对（4415-4433）。②`--init-checkpoint` 通用路径=形状过滤 compatible dict（4450-4458）→ **跨代加载静默丢键**（index_ffn/decoder_in_mem/align_* 全部跳过，只打印 skipped 计数），坑 8 的 0.05 水位事故即此路径。③臂级 loud-fail 全键全形校验：denoise 4498-4508、Q20 4522-4543、E120 4552-4573（豁免各自新件前缀）。④resume `load_state_dict(payload["model"])` 隐式 strict（4650）→ 同 run 安全。
- tied 嵌入注记：decoder.byte_lookup 与模型级 byte_lookup 同参，Q18 模式跳过 freeze_prefixes 块避免重冻（4477-4482）。

**判词：跨代加载只有 strict 系路径可比性安全；任何经通用 init_checkpoint 的跨代点火必须加臂级全键校验，否则产出不可比且难以察觉。**

---

## 跨线引用证据红线清单

1. **completion/backbone 系禁止跨线直比**：v36.8=累积保持网格，v37 a/b 格=per-chunk 网格，v37 c/d 格=累积网格——`completion_loss`/`backbone_acc`/`backbone_masked_acc`/`eval_backbone_ppl` 同键不同义（train_v36_s1.py:3170-3171）。
2. **v36.8 界**：该日之前（零保持 per-chunk）与之后（累积保持）的补全读数绝对值不可比，canonical 自陈（canonical_v36.json:5）。
3. **E100 界**：qpool（v37.3）与 mean（v37.2 及之前）的 codec 类读数禁止混排；canonical_v36.json 无 summarizer_pool 键，现行默认下 v36 线也吃 qpool——引用 v36 历史证据必须核对当时池化口径（canonical_v37.json:3、train_v36.py:384-393）。
4. **v37.2 界**：seed_source v↔k 翻转种子语义；老配置无键静默回 v（train_v36.py:338-346）。
5. **direct 系带注记**：direct_acc/eval_direct_ppl 目标同形，但 v36 条件=KDA content 读出、v37 a 格条件=memory 行直通——测的是不同通道，引用须挂条件注记；c/d 格 direct 网格是累积版，与 a 格同键不同分母。
6. **predict 系带注记**：latent MSE 同形但锚不同（content vs v_rows）；`predict_mode=decode` 是 E34 判负形态，禁与 latent 混排。
7. **零占位键**：state_norm（a 格）、key_*（v36 线缺席）、cloze/retrieval/burst/q15/q20/e123 各臂列在关态=0——跨线引用前先确认该键在该臂是实义还是占位。
8. **窗流随 seed**：eval 流=seed+9999，跨 seed 判读一律先同卷复测再判（坑 9 纪律；train_v33.py:500-504）。
9. **语料是配置外变量**：data_path 占位符，跨线比较必须在命令层核对实际语料（v3 训练主流/v4 仅域外复测）与 corpus 版本。
10. **体制红线**：from-scratch 臂（freeze/init 双空）与 S0'' 冻结接管臂段界分布不同，codec 绝对值不可比，只能比臂内 Δ；E120 乙列全解冻是第三种体制（train_v36_s1.py:4203-4210）。
11. **加载红线**：跨代/跨格点火禁走裸 `--init-checkpoint`（静默形状过滤 4450-4458）；必须用 eval_only strict 或臂级全键校验模式；教师前端接管读数只在 skipped 键=预期白名单时有效。
12. **死键红线**：a 格无状态机——kda_impl/state_norm/readout_* 在 a 格全为死键或零占位，"fla vs torch""状态机贡献"类论证对 a 格无效；E119/E120/E123 等改装件全部只存在于 v37 线，无 v36 对偶。
13. **臂协议红线**：decoder_markov（teacher-forced 协议）、Q15 三件套、E120 三列仪表、E123 batch=1 窗序日志——各自成协议，只臂内可比（train_v36_s1.py:3251、4299-4302）。