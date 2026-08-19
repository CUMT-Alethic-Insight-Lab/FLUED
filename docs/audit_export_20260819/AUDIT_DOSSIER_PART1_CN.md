# FLUED 审计对账档案 · 第一部分（E73–E87 世代，2026-08-19 汇编）

> 编制纪律：本文件一切数字均从仓库文件原样读出，逐项标注出处（路径 + 字段/行号）；未落盘的项目标"**悬空**"。
> 主要来源：
> - 证据登记行：`docs/CURRENT_STATE.md:142-156`（E73–E87 行，下文简称"登记行"并给行号）；
> - 训练 run：`checkpoints/<run_id>/resolved_config.json`（完整 CLI args）、`summary.json`（终评）、`train_log.jsonl`（逐步）；
> - 复训 run：`checkpoints/retrain_readout_c_*/train_log.jsonl`、`stdout.log`、`retrained_readout.pt`（内嵌 `args` 字段）；
> - 探针报告：`outputs/` 下对应目录的 JSON/SUMMARY/log；
> - 代码：`tools/analysis/v3_6/probe_oracle_write_verdict.py`、`tools/train/v3_6/retrain_readout_chain.py`、`flued/v36/model.py`、`tools/train/v3_6/train_v36.py`、`tools/eval/forward_verifier.py`。

---

## 1. E73–E87 完整登记页

每条格式：目的 / 配置 / 命令 / 关键指标 / 结论。登记行原文不复制，仅以对账后的展开形式呈现；与登记行有出入处显式标注（汇总见 §7）。

### E73 — oracle 写入判决（c 格三臂零训练根因二分）

- **登记**：`docs/CURRENT_STATE.md:142`；数据：`outputs/oracle_write_verdict_20260818/SUMMARY.txt`、`oracle_write_verdict.json`；脚本：`tools/analysis/v3_6/probe_oracle_write_verdict.py`。
- **目的**：判定 E-a（c 格 v=state 内容崩盘：登记锚 eval direct_acc 0.2972 / direct_ppl 39.95，对照 a 格 0.7923 / 2.14，脚本 docstring `probe_oracle_write_verdict.py:2-4`）的根因层：写入未形成（H1）/ delta 递推侵蚀 / 读出侧 / 读出结构病。
- **配置**：eval-only 零训练（ridge 为闭式代数，`probe_oracle_write_verdict.py:60`）；16 评估窗、eval_mask_seed 1042、cloze 关（`:61-63`）；fp32 主口径 + A1-amp bf16 对照；被测件 `checkpoints/v37_c_is_v371_20k_ctx4096_20260817`（c 格 k=index, v=state, seed=v），A0 锚 `v37_a_im_v371_20k_ctx4096_20260817`（`:92-93`）。臂矩阵 A1–A5 + 诊断 A6（`:11-29`）。
- **命令**：`python tools/analysis/v3_6/probe_oracle_write_verdict.py --device cuda`（`:65-67` Usage 行）。
- **关键指标**（SUMMARY.txt 臂矩阵表，direct acc / ppl / own 本段 / recalled(as-enc) / recalled(clean)）：
  - 管线保真：A0 复现 0.7935/2.131（锚 0.7923/2.141）；A1 复现 0.2965/40.134（锚 0.2972/39.95）；A1-amp 0.2974/39.913。
  - A1 trained 态+trained 读出：0.2965 / 40.13 / own 0.7095 / recalled 0.0000。
  - A2 oracle 完美叠加态+trained 读出：0.0482 / 274.20 / own 0.1163。
  - A5 原始写值直通：0.0426 / 217.65 / own 0.1030。
  - A3 trained 态+ridge 读出 λ∈{1e-4, 1e-2, 1}：0.2476/50.99、0.2675/45.65、0.2855/42.17（处处 ≤A1）。
  - A4 oracle 态+ridge 读出：0.0418/220.46、0.0300/261.65、0.0250/259.06（λ 同上，全灭）。
  - ridge 取回质量 cos(v̂,v)：λ=1e-4 → trained 0.6473 / oracle 0.9968；λ=1e-2 → 0.7754/0.9615；λ=1 → 0.7598/0.6664。
  - state_norm trained/oracle = 4.9498 / 997.3514；SVD 有效秩（PR/dim）trained 0.0168（top8 能量 1.0）、oracle 0.0137（top8 0.9996）。
  - 键集中度 mean|cos(k_i,k_j)| = 0.9354（键塌缩签名）；写值范数 11.4157±4.1934；beta 0.2503±0.4181；alpha mean/min 0.8139/0.001。
  - A6 闭式字节探针（2-fold 岭回归，acc vs majority）：写值 v → slot0-3 = 0.6185/0.3727/0.3223/0.6092（majority 0.2138/0.0377/0.0423/0.1825，n=2676/2597/2578/2554）；memory 行上限对照 m → 0.7096/0.4628/0.3809/0.6273。登记行"保留 memory 行 82% 线性信息增量"按 slot0 计 = (0.6185−0.2138)/(0.7096−0.2138) = 0.4047/0.4958 ≈ 0.816（本档案按 SUMMARY 数字复算）。
- **结论**（登记行判决 + SUMMARY 判决逻辑 `probe_oracle_write_verdict.py:31-44`）：读出结构病为主病（同样的 v 线性探针读 0.62 档、trained 链读 0.10 档；ridge cos≈1 时 A4/A5 仍灭）；键塌缩（0.9354）为写入侧次主；递推侵蚀为从犯；H1"写入未形成"值侧证伪。口径级修正：c 格 direct 为累积 as-encoded 格、a 锚为本段格，绝对值不同形（`:52-58`），同形对照真差距 own 槽 −8.4pp，崩盘主体是 recalled 槽 0.0000 × 网格成分。

### E74 — 键塌缩全盘点（12 checkpoint 因子设计，零训练）

- **登记**：`docs/CURRENT_STATE.md:143`；数据：`outputs/key_collapse_survey_20260818/SUMMARY.txt`、`key_collapse_survey.json`；脚本：`tools/analysis/v3_6/measure_key_collapse.py`（Usage `:26-28`）。
- **目的**：测量写入键几何 μ = mean off-diag |cos|（16 窗 × 4 头，eval seed 1042 同口径，`key_collapse_survey.json` `/protocol` 字段），判定 cloze 训练压力与 seed_source 各自对键几何的作用。
- **命令**：`python tools/analysis/v3_6/measure_key_collapse.py --device cuda`。
- **关键指标**（SUMMARY.txt 因子表；JSON `results[]` 逐项复核一致）：
  - WriteHead 键全塌深区：b 格 K 键 0.9271±0.070（v371）/ 0.9199±0.047（ks）/ 0.9037±0.084（ks+cloze）；c 格 V 键 0.9354±0.038 / 0.9578±0.045 / 0.9568±0.042；d 格 K 键 0.8252±0.102 / 0.7820±0.161 / 0.8220±0.157；d 格 V 键 0.9304±0.043 / 0.9568±0.030 / 0.8772±0.131。
  - clozeΔ ∈ [−0.0796, +0.0400]（四通道全部留在塌区）；seedΔ 与 clozeΔ 分行见 SUMMARY 分解列。
  - a 格 index 行（summarizer 直产，无 WriteHead）：0.9325±0.050（V-seed）→ 0.1736±0.020（K-seed），seedΔ −0.7589。
  - 继承对照（输入行）：b 格 index 行 0.8583→0.1251（K-seed 后健康）而 K 键仍塌 0.9199——压塌定位在 WriteHead.to_k 自身；c 格 memory 行 0.1577→0.2279（全世代健康区 0.16–0.23）。
- **结论**：cloze 压力臂判负（fork 倒向几何硬约束）；键塌缩是 WriteHead.to_k 的结构性压塌、与输入无关；K-seed 对 index 行的几何分化是 v37.2 默认形态正确性的独立证据。

### E75 — 塌缩逐层定位（3 格 × 6 层分解）

- **登记**：`docs/CURRENT_STATE.md:144`；数据：`outputs/key_collapse_survey_20260818/SUMMARY.txt`（LAYERWISE DECOMPOSITION 节）、`layerwise_decomposition.json`；脚本：`tools/analysis/v3_6/measure_key_collapse_layerwise.py`（Usage `:29-31`）。
- **目的**：把塌缩钉到具体层（L0 输入行→L1 LayerNorm→L2 Linear→L3 SiLU→L4 to_k→L5 归一化），排除 bias 支配 / SiLU 饱和 / 死维等替代解释。
- **关键指标**（SUMMARY.txt）：
  - 逐层 μ：c-v371 v@memory 0.158→0.158→0.166→0.259→**0.935**→0.935；c-cloze 0.231→0.231→0.295→0.421→**0.957**→0.957；b-v371 k@index 0.858→0.860→0.887→0.884→**0.927**→0.927。塌缩全部发生在 to_k 一层；L4==L5 恒等（逐行归一化不改余弦）。
  - 排除项（16 窗均值）：L3 死维 0.0/1024（三格均）；SiLU 饱和率 0.000/0.000/0.053；bias 支配度/头 0.0015–0.017（≪1 两个数量级）。登记行另载 W_to_k SVD 有效秩 361–374/512（登记行 `:144`；JSON 同目录）。
  - 去均值对照（to_k 输出去均值后 μ）：c-v371 0.307、c-cloze 0.312、b-v371 0.816——c 格塌缩主体是单一共享方向；b 格为多方向相干（去均值剂量不足）。
- **结论**：初始化臂被证据否决（会再塌）；硬约束臂（to_k 输出去均值/白化，EMA 统计）上岗，V 通道先开（c 格）、K 通道在 ks 世代开（b 格）。

### E76 — to_k 手术 c 格（v37.2+cloze+to_k_center，20K@4096B）

- **登记**：`docs/CURRENT_STATE.md:145`；run：`checkpoints/v37ks_c_is_v372_cloze_tokcenter_20k_ctx4096_20260818/`；验收：`outputs/key_collapse_survey_20260818/tokcenter_acceptance.json`（+ SUMMARY 同名单元）。
- **目的**：对 c 格 V 通道部署 E75 首选硬约束（to_k 输出去均值，EMA 0.99），检验键几何修复是否复活寻址/codec。
- **配置**（`resolved_config.json` args 字段）：canonical_v37.json 基线 + `--v-row-source state --to-k-center --cloze-prob 0.3 --cloze-weight 0.3 --cloze-bank P:\FLUED_corpus\cloze_bank_v1.jsonl --seq-len 4096 --stride 2048 --batch-size 1 --max-chunks 1024 --max-steps 20000 --data-path P:\FLUED_corpus\corpus_v3\corpus_v3.txt`；k_row_source=index、seed_source=k（v37.2 默认）；params 48,363,688；init `K:\FLUED_archive\s0pp_pro_v4_sft_20260805\latest.pt`，freeze_prefixes=byte_lookup,encoder_blocks,segmentor_blocks,segmentor_head；lr 2e-4、warmup 200、grad_clip 1.0、fused_adamw、amp。
- **命令**（由 resolved_config.json args 还原；入口 `tools/train/v3_6/train_v36_s1.py`，cloze 任务文档 `docs/versions/v3.7/FLUED_V3_7_CLOZE_TASK_20260817_CN.md:4` 指明实现文件）：
  `python tools/train/v3_6/train_v36_s1.py --config configs/canonical_v37.json --run-id v37ks_c_is_v372_cloze_tokcenter_20k_ctx4096_20260818 --v-row-source state --to-k-center --cloze-prob 0.3 --cloze-weight 0.3 --seq-len 4096 --stride 2048 --batch-size 1 --max-chunks 1024 --max-steps 20000 --data-path P:\FLUED_corpus\corpus_v3\corpus_v3.txt --cloze-bank P:\FLUED_corpus\cloze_bank_v1.jsonl`
- **关键指标**：
  - 验收（SUMMARY.txt TO_K_CENTER c 格单元，暖 buffer 口径 16 窗）：未手术对照 μ=0.9568±0.042（PR/n 0.0066）；手术格 raw μ=0.9680±0.049（PR/n 0.0065）；手术格 centered μ=**0.4171±0.147**（PR/n 0.0322，Gram 有效秩 ×5）。
  - 终评（`summary.json`）：eval_direct_acc 0.3054 / backbone_acc 0.2882 / masked 0.0047 / direct_ppl 38.777 / backbone_ppl 41.988（对照未手术 E71 锚 0.3072/0.2898——任务级纹丝不动）；cloze_byte_acc 0.0799、exact 0.0；state_norm 13.199（未手术 5.63，写入量 2.3×）；nan_skips 0；2.610 step/s、7661.9s。
  - 档案馆 K 侧与未手术同档（hit1 0.25/0.00/0.08，登记行）；V 侧回读 0.52–0.57 持平（登记行）。
- **结论**：手术机械生效但寻址/codec 零复活——键塌缩被排除为容量墙瓶颈，读出链锁死坐实为唯一主病；残余 μ 0.417 高于单窗预测 0.31（多方向轻相干，E75 残余项坐实）。

### E77 — 读出链锁死定量图 + 复训器建成

- **登记**：`docs/CURRENT_STATE.md:146`；数据：`outputs/readout_lockin_20260818/SUMMARY.txt`、`lockin_curve.json`；脚本：`tools/analysis/v3_6/measure_readout_lockin_curve.py`（Usage `:23-25`）；复训器：`tools/train/v3_6/retrain_readout_chain.py`。
- **目的**：对 c 格未手术 checkpoint 构 μ 响应曲线（真实写值 + 键从塌缩 μ=0.935 连续扫到近正交 0.071，oracle 累计态喂 trained 链，ridge 线为天花板对照），定位锁死点；并建成读出链复训器。
- **关键指标**（SUMMARY.txt；参考行 A1 自然态 trained-q acc=0.2965 own=0.7095 recalled=0.0）：λ 档 0.00→1.00（realized μ 0.935→0.071）下 trained-q acc 0.0482→0.0475（末档 0.0333）、ridge acc 0.0299→0.0399，两线全轴**平**；ridge_cos 全程 0.962–0.986。
  - 复训器建成态属性（登记行 + 脚本）：冻结面=仅 realign+decoder_in+decoder（剔共享 byte_lookup）可训；oracle/自然态余弦退火混合；eval 双态双报 + 地板常量 0.6185 随行（验收线=超过地板，`retrain_readout_chain.py:75`）；CPU 冒烟 20 步单调降零 NaN；单测 7 项、全量 338+4 绿。
- **结论**：锁死点不在键几何、不在状态质量，在 realign/decoder 接口本身；只有复训能检验"每段单向量"接口形态的容量上限。
  - ⚠ 口径注记：登记行写"退火 0.8→0.1"（建成时点口径，E80 首跑 args 存证 `oracle_frac_end=0.1`）；现行脚本默认已改为 0.8→0.3（`retrain_readout_chain.py:347`，"修正一 2026-08-19"），E81 起各 run args 均为 0.3。

### E78 — to_k 手术 b 格（K 通道去均值，主线格首个 D=64 非零寻址）

- **登记**：`docs/CURRENT_STATE.md:147`；run：`checkpoints/v37ks_b_sm_v372_cloze_tokcenter_20k_ctx4096_20260818/`；验收：`outputs/key_collapse_survey_20260818/tokcenter_acceptance_v37ks_b_sm_v372_cloze_tokcenter_20k_ctx4096_20260818.json`；档案馆：`outputs/s39_addressing_probe_v37_20260818/report_v37ks_b_sm_v372_cloze_tokcenter_20k_ctx4096_20260818.json`。
- **目的**：对 b 格（k=state, v=memory）K 通道部署 to_k_center，检验主线格寻址是否复活。
- **配置**（`resolved_config.json`）：canonical_v37.json + `--k-row-source state --to-k-center --cloze-prob 0.3 --cloze-weight 0.3 --seq-len 4096 --stride 2048 --batch-size 1 --max-chunks 1024 --max-steps 20000`（v_row_source 保持 memory；seed_source=k）；params 47,970,472；其余同 E76。
- **命令**（args 还原）：`python tools/train/v3_6/train_v36_s1.py --config configs/canonical_v37.json --run-id v37ks_b_sm_v372_cloze_tokcenter_20k_ctx4096_20260818 --k-row-source state --to-k-center --cloze-prob 0.3 --cloze-weight 0.3 --seq-len 4096 --stride 2048 --batch-size 1 --max-chunks 1024 --max-steps 20000 --data-path P:\FLUED_corpus\corpus_v3\corpus_v3.txt --cloze-bank P:\FLUED_corpus\cloze_bank_v1.jsonl`
- **关键指标**：
  - 验收（SUMMARY.txt b 格单元）：未手术对照 K 键 μ=0.9037±0.084（PR/n 0.0075）；手术格 raw μ=**1.0000±0.000**（残余即全部内容）；centered μ=0.8108±0.210（PR/n 0.0105）——多方向相干，去均值剂量不足。
  - 终评（`summary.json`）：direct_acc 0.7808 / backbone_acc 0.7285 / masked 0.1271 / unmasked 0.7625 / direct_ppl 2.2159 / backbone_ppl 2.8324（对照无手术 b 格锚 direct 0.7913——codec 微让位）；cloze_byte_acc 0.0764；state_norm **358.4**（未手术 6.2，58×）；nan_skips 0；7874.9s。
  - 档案馆（report JSON `k_side[0].levels`，k_rows(state)，n=12/档，train_loss 6.6734→5.9747）：D=4 hit1/3/5 = 0.1667/0.25/0.25（rand1 0.0016）；D=16 = 0.0833/0.4167/0.4167；D=64 = **0.1667**/0.25/0.4167（rand1 0.0014）——E-c 开考以来首个 D=64 档非零 hit@1。
  - V 侧回读裂口（report JSON `v_side.<D>.arms`，byte_acc direct vs backbone）：D=4 0.6548 vs 0.4643；D=16 0.6905 vs 0.4762；D=64 0.6071 vs 0.4048——backbone 臂掉 15–21pp（未手术格无此裂口，登记行）。
- **结论**：b 格 K 通道有几何响应（E74"cloze 没动几何"在 b 格部分修正）；需更强硬约束（码本键/稀疏扩展）；V 回读裂口为手术引入的新失败模式（E79 解剖）。

### E79 — E78 审计三测量（μ 轨迹 / per-item 谓词 / 写值误伤）

- **登记**：`docs/CURRENT_STATE.md:148`；数据：`outputs/key_collapse_survey_20260818/SUMMARY.txt`（M1/M2 单元 + LAYERWISE 解耦冒烟）、`mu_trajectory_tokcenter.json`、`outputs/s39_addressing_probe_v37_20260818/report_v37ks_b_tokcenter_peritem.json`、`outputs/oracle_write_verdict_20260818/write_value_probe_bgrid.json`（+ SUMMARY.txt M3 单元）。
- **目的**：审计 E78 手术格的三个疑点——复塌与否、per-item 可恢复性谓词、V 回读裂口机制。
- **关键指标**：
  - M1 μ 训练轨迹（暖 buffer 口径，3K–20K 里程碑）：b 格 raw→centered 恒 1.000→0.690(3K)/0.757/0.795/0.780/0.795/0.803/**0.811(20K)**；c 格 0.880→0.342(3K)/0.294(6K)/0.314/0.331/0.389/0.410/**0.417(20K)**——两格 centered 自 6K 最优点单调缓升（非立即复塌，残余多方向相干随训练爬回）。
  - M2 per-item 谓词（μ_i = needle 行 max_{j≠i}|<k_i,k_j>| 的最小值；n=12/档）：D=4 hits=2/12（hit_share@低μ四分位 0.5 vs null 0.25）；D=16 hits=1/12（1.0）；D=64 hits=2/12（0.0，两个 hit 反在高 μ 区）；检索空间 μ_i 挤在 0.53–0.71 窄带——**谓词证伪**，μ_i 不是命中的决定变量。
  - M3 写值字节探针（b 格 K 通道，2-fold 岭回归 slot0-3，写值 v vs 输入行对照）：手术格 v = 0.230/0.174/0.030/0.283（未手术 0.560/0.327/0.273/0.472；输入行两侧均 ~0.72/0.49/0.44/0.61 不变）——**手术误伤坐实**：to_k_center 只碰 to_k，但 trunk 是 to_k/to_v 共享，去均值经共享 trunk 训练动力学连带打掉 to_v 值内容。
  - 附（解耦冒烟对照，30 步 c 格）：split vs shared trunk 逐层几何与值内容无显著差异；机制层由单测锁定（split 下键侧损失对值支路梯度恰为零）。
- **结论**：去均值剂量不足升级为硬约束（白化/码本键）必要的直接证据；V 回读裂口机制=手术误伤（"读出统计漂移"主嫌疑排除）；继续手术线必须先解耦 to_k/to_v trunk。

### E80 — 读出链复训首跑（c 格双对象，各 5K 步）

- **登记**：`docs/CURRENT_STATE.md:149`；run：`checkpoints/retrain_readout_c_v371_20260818/`、`checkpoints/retrain_readout_c_tokcenter_20260818/`。
- **目的**：检验冻结主干下 realign+decoder_in+decoder 读出链的可学性（direct 形态损失）。
- **配置**（`retrained_readout.pt` 内嵌 args 还原——复训 run 无 resolved_config.json）：对象 1 = `v37_c_is_v371_20k_ctx4096_20260817` step 20000（未手术）；对象 2 = `v37ks_c_is_v372_cloze_tokcenter_20k_ctx4096_20260818` step 20000（手术）；steps 5000、lr 1e-3（恒定，该版本无 warmup 字段）、oracle_frac 0.8→0.1 余弦退火、无 μ 课程（mu_lambda_grid=None）、eval_every 200 / 16 窗、seed 42、grad_clip 1.0；可训 10,318,215 params / 58 tensors（两对象 stdout.log 首行一致）。
- **命令**：**悬空**（命令行原文未落盘；等效形式 = `python tools/train/v3_6/retrain_readout_chain.py --run-dir <对象 ckpt> --steps 5000 --out-dir <run>`，参数以 pt 内嵌 args 为准）。
- **关键指标**（train_log.jsonl eval 记录，direct_acc_natural/oracle，地板 0.6185 全程 below_floor）：
  - 对象 1（未手术）：0.0513@200 → 0.1343@4400 → **0.1641@5000**（oracle 0.0621）。
  - 对象 2（手术）：0.0303@200 → 0.1759@4400 → **0.2042@5000**（oracle 0.0613）。
  - 完整逐步表见 §6。⚠ 登记行"0.134→0.164 / 0.176→0.204"的起点读数对应 ~4.4K 步处，非首评（首评 0.0513/0.0303@200）。
- **结论**：链确实在学但 5K 远未到地板；手术版复训更快（与几何更健康自洽）；oracle 态 eval ~0.06 停滞（退火终点 0.1 嫌疑参数，修正一后调 0.3）；触发防翻车设计 2（延长训练 + 放开主干末层）。

### E81 — μ 课程版复训双对象（各 20K 步）

- **登记**：`docs/CURRENT_STATE.md:150`；run：`checkpoints/retrain_readout_c_v371_mucurr_20260818/`、`retrain_readout_c_tokcenter_mucurr_20260818/`。
- **配置**（pt args）：steps 20000、oracle_frac 0.8→**0.3**（修正一）、mu_lambda_grid = "0.2,0.45,0.65,0.85,1.0"（μ 课程：oracle 态键按 λ 与随机方向相干混合，每步均匀抽档）、余下同 E80；direct 形态、主干冻结。
- **关键指标**（train_log.jsonl）：对象 1 natural 0.1898@20K / plateau 0.1916（oracle 0.0702）；对象 2 natural 0.1837 / plateau 0.1807（oracle 0.0645）。双对象收敛同一区间；两条轨迹 18K→20K 仍爬坡（0.1835→0.1898；0.1771→0.1837），**未饱和**；oracle 态全程 0.06–0.07 停滞。逐步表见 §6。
- **结论**：冻结主干下 direct 读出链能力边界实测 ~0.19 平台（按预注册纪律报平台位置）；μ 课程未明显改变轨迹；下一步 = 放开主干末层（设计 2）。口径注记（登记行）：地板 0.62 是 slot0 线性探针口径，direct_acc 是全槽位含 recalled 槽口径，非同分母。

### E82 — 放开主干末层复训（ubb1，防翻车设计 2 执行）

- **登记**：`docs/CURRENT_STATE.md:151`；run：`checkpoints/retrain_readout_c_v371_ubb1_20260818/`、`retrain_readout_c_tokcenter_ubb1_20260818/`。
- **配置**（pt args）：同 E81 + `unfreeze_backbone_last_n=1`；可训 11,697,415 params / 70 tensors（stdout.log 首行；比 E81 多 1,379,200 = 主干末块）。
- **关键指标**：双对象 20K 终评与 E81 **逐位相同**（0.1898/0.1916 与 0.1837/0.1807，oracle 0.0702/0.0645）。
- **结论**：v37 direct 条件 = decoder_in(状态读出行)+pos，主干只服务补全/预测路径、不在 direct 损失路径——直接损失下主干梯度恒零，旋钮结构性惰（非 bug）；direct 链 0.19 平台坐实；对照补全路径（含主干）同格 backbone_acc 0.29 > 0.19，复训要突破须换补全形态损失（fork 1 的直接起因）。

### E83 — fork 1 补全形态复训双对象（主干真入链，各 20K 步）

- **登记**：`docs/CURRENT_STATE.md:152`；run：`checkpoints/retrain_readout_c_v371_completion_ubb_20260819/`、`retrain_readout_c_tokcenter_completion_ubb_20260819/`。
- **目的**：把复训损失从 direct 形态换成补全形态（cond = backbone_out + pos，累积保持 CLEAN 目标网格），让梯度真正流进主干（`retrain_readout_chain.py:1-11` docstring）。
- **配置**（pt args）：steps 20000、lr 1e-3 恒定（**加固前版本：无 warmup/无 NaN 护栏字段**）、oracle_frac 0.8→0.3、μ 课程档同上、freeze_backbone=False（主干全放）；可训 14,947,335 params / 94 tensors（由 E86 同配方 stdout.log 首行确认该冻结面的参数量；本两条 run 无 stdout.log——**档案缺口**）。
- **命令**：**悬空**（同 E80；这两条 run 目录仅有 train_log.jsonl + retrained_readout.pt）。
- **关键指标**（train_log.jsonl 四臂 eval，floor 0.6185 参照）：
  - 对象 2（手术版）：干净爬坡 0.2425@1K → 0.2922@10K → 0.2999@20K（plateau_acc 0.300）；20K 终评四臂 completion_acc natural_full 0.2999 / natural_stateonly 0.2999 / oracle_full 0.2999 / oracle_stateonly 0.2999——K 消融无差异、oracle/自然无差异。
  - 对象 1（未手术版）：10K 前缓爬贴 0.068–0.069，**train loss 于 step 12300 起连续 NaN**（train_log.jsonl，12.3K–20K 共 155 条 NaN-loss 记录），eval 自 13K 起四臂全 0.0000 收官。⚠ 登记行（`:152`）写"15K 处 loss NaN 发散归零"、E86 登记行（`:155`）写"12.4K NaN 发散点"——两处不一致；train_log 实测首个 NaN 在 **12300**（12.3K）。
  - 护栏二（E83 前置，`outputs/interface_probe_20260818/SUMMARY.txt`）：接口向量信息充足——real−garbage slot0 +0.4723 > 0.4 标尺（slot1-3：+0.3758/+0.3251/+0.4777；对照写值探针 slot0 0.6185、majority 0.2138）→ fork 2 暂缓解除。
- **结论**：主干入链无增量——复训撞的是接口形态天花板（每段单向量条件化）；按预注册结局矩阵 fork 2 扶正为主线；0.62 地板与 0.30 饱和之间的缺口 = 接口形态容量缺口的定量测量；对象 1 发散如实登记（E86 证明其直接起因是安全带缺失）。

### E84 — fork 2 实施落地 + 前向校验器首测（判负）

- **登记**：`docs/CURRENT_STATE.md:153`；spec：`docs/versions/v3.7/FLUED_V3_7_FORK2_MULTIVIEW_READOUT_20260819_CN.md`；校验器脚本：`tools/eval/forward_verifier.py`；数据：`outputs/forward_verifier_firsttest_20260819.log`、`outputs/forward_verifier_firsttest_20260819/verify_v37ks_b_sm_v372_cloze_tokcenter_20k_ctx4096_20260818.json`；冒烟 run：`checkpoints/_smoke_views4_c_20260819/`。
- **目的**：① fork 2（多视角读出 m-way + 前向校验器）全链代码落地；② 校验器首测——检验"hit@5 池 → 前向校验兑换 hit@1"在 E78 手术 b 格（D=64 hit@5 0.4167 / hit@1 0.1667 的缺口）上是否成立。
- **实施清单**（登记行 + 代码存证）：
  - `--readout-views` / `--verify-topl` CLI 接线（`tools/train/v3_6/train_v36.py:359-380`：readout_views 默认 1，m>1 时每个状态通道的主干存储行扩为 m 路测量行、播种正交帧免训练、direct/predict 路径位不变；verify_topl 默认 0=关，仅 train_v36.py evaluate()、slm + v=state 格）。
  - 多视角存储路径 `SLMBackbone._forward_views`（`flued/v36/model.py:1398-1450`：align_k/align_v/realign m 路共享零新参数；种子=view-0 K 行 / view 均值 V 行）；`forward_views`（`model.py:504` 起）；`_slm_store_rows` 的 with_views 扩展（`model.py:1944-1987`，5 元组元素位不变）。
  - 校验器最小实现（`tools/eval/forward_verifier.py` docstring）：候选=档案馆探针检索器 top-L key 行对应的段；write(cand)=该段 WriteHead 写值 v；target=问句末段写值；比对空间=写值空间经播种正交帧投影（帧种子 `VERIFY_FRAME_SEED = 20260819_1000` 钉死，`:38`；completion-pass 常量 VERIFY_FRAME_DIM=32、VERIFY_MAX_CHUNKS_PER_SAMPLE=8，`:41-42`）；全状态范数比对被立项书明确禁用、未实现。命令（docstring Usage）：`python tools/eval/forward_verifier.py --device cuda --run-dir checkpoints/v37ks_b_sm_v372_cloze_tokcenter_20k_ctx4096_20260818`。
  - 14 新单测、全量 370+4 绿（登记行）；c 格 m=4 冒烟 30 步零 NaN（`_smoke_views4_c_20260819/summary.json`：steps 30、nan_skips 0、14.8s、seq_len 512、readout_views=4、k=index/v=state/seed=k、to_k_center=false）。
- **首测配置**（verify JSON `params` + log）：ckpt = E78 手术 b 格 step 20000（readout_views=1 的旧格）；channel=k；haystack=corpus_v3.txt；pages 4、level D=64、topl 5、eval_docs 12、retriever_steps 1000；比对形态 "write-replay: candidates' WriteHead value vectors vs the query's last-chunk write value, compared under a seeded orthogonal frame (32 × H*hv)"（JSON `form` 字段）；检索器 trained loss 6.44→5.65（log）。
- **首测结果**（JSON `aggregate`）：n_docs 12；hit1_before 0.1667、hit5_before 0.4167、**hit1_after_verify 0.0833**、**false_peak_rate 0.8**——校验反把 hit@1 压半。逐 doc 明细（JSON `docs[]`）：12 doc 中 hit5 池内 5 doc（QX-1425/7129/2718/7264/0727），校验后仅 QX-0727 保住 hit@1（picked=7，margin 0.4112）；两个原 hit@1 doc（QX-2718 picked=5 margin 1.7805、QX-7264 picked=451 margin 1.1899）均被伪峰顶掉。总耗时 21.7s。
- **结论**：红队"错误候选重嵌入也接近目标状态"的伪峰警告首次实测兑现（伪峰率 0.8，残余相干 μ=0.81 几何下校验器无判别力）；校验兑现的前提是几何更干净（硬约束臂）或测量空间更大（m>1 训练格）——单挂校验器于旧格无效；fork 2 的第一桶金在 m=4 多视角训练格本身（→ E85）。

### E85 — fork 2 首臂 b 格 m=4 多视角（20K@4096B，否定读数）

- **登记**：`docs/CURRENT_STATE.md:154`；run：`checkpoints/v37ks_b_sm_v372_cloze_tokcenter_views4_20k_ctx4096_20260819/`；档案馆：`outputs/s39_addressing_probe_v37_20260817/report_v37ks_b_sm_v372_cloze_tokcenter_views4_20k_ctx4096_20260819.json`（探针 log：`outputs/s39_addressing_probe_v37_20260818/run_views4_b.log`——⚠ 报告落在 0817 日期目录，与 run 日期 0819 不一致，路径以 log 末行为准）。
- **目的**：fork 2 首臂——b 格（k=state, v=memory）K 通道存储行扩为 m=4 测量行（共享权重、零新参数），检验多视角是否买到寻址。
- **配置**（`resolved_config.json` 关键字段全录）：canonical_version v37.2-20260817；k_row_source=state、v_row_source=memory、seed_source=k、**to_k_center=true、readout_views=4、verify_topl=0**（校验器不参与训练）、split_trunk=false；cloze_prob=0.3、cloze_weight=0.3、cloze_bank=P:\FLUED_corpus\cloze_bank_v1.jsonl；seq_len 4096、stride 2048、batch_size 1、max_chunks 1024、max_span 64、max_steps 20000；d_byte 384、encoder_layers 3、segmentor_layers 9（冻结）、summarizer DiT slots 4/hidden 1024/dit_layers 2、d_mem 512；kda_heads 4、head_k 128、head_v 256、write_hidden 1024、tau_max 256；readout_queries 1、d_pack 1536；backbone slm：d_backbone 384、layers 3、nhead 8、ffn 1024、per_chunk readout；decoder hidden 1024、layers 3；mask mixed（prob 0.05、char_frac 0.4、char_span_max 3）；predict latent（weight 1.0、latent 0.1）；lr 2e-4、wd 0.01、fused_adamw、warmup 200、grad_clip 1.0、amp；seed 42、eval_mask_seed 1042；init `K:\FLUED_archive\s0pp_pro_v4_sft_20260805\latest.pt`、freeze byte_lookup,encoder_blocks,segmentor_blocks,segmentor_head；params 47,970,472（与 m=1 手术 b 格相同——四路共享权重零新参数，存证一致）。
- **命令**（args 还原）：`python tools/train/v3_6/train_v36_s1.py --config configs/canonical_v37.json --run-id v37ks_b_sm_v372_cloze_tokcenter_views4_20k_ctx4096_20260819 --k-row-source state --to-k-center --readout-views 4 --cloze-prob 0.3 --cloze-weight 0.3 --seq-len 4096 --stride 2048 --batch-size 1 --max-chunks 1024 --max-steps 20000 --data-path P:\FLUED_corpus\corpus_v3\corpus_v3.txt --cloze-bank P:\FLUED_corpus\cloze_bank_v1.jsonl`
- **关键指标**：
  - 终评（`summary.json`）：direct_acc **0.7418** / backbone_acc **0.6867** / masked 0.1198 / unmasked 0.7188 / direct_ppl 2.619 / backbone_ppl 3.399（对照 m=1 E78：0.7808/0.7285/2.216/2.832——codec 全线让位 ~4pp）；cloze_byte_acc 0.0680、exact 0.0；predict_cos 0.8585（E78 为 0.6522，升高）；state_norm 14.94；eval 键几何 key_mu_k 0.7309 / key_mu_max_k 0.9998 / key_pr_k 0.0098；nan_skips 0；2.949 step/s、6781.7s。
  - 训练曲线（train_log.jsonl，逐千步训练窗指标；注意：train_log 为训练批次口径，与 summary 的 16 窗 eval 口径不同——20K 处 train direct_acc 0.7265 vs eval 0.7418）：

    | step | loss | direct_acc | backbone_acc | cloze_byte_acc | key_mu_k | state_norm |
    |---|---|---|---|---|---|---|
    | 1000 | 7.1434 | 0.2973 | 0.2475 | 0.0716 | 0.8204 | 2.46 |
    | 2000 | 6.1600 | 0.3462 | 0.3004 | 0.0345 | 0.7387 | 4.48 |
    | 3000 | 5.5379 | 0.3984 | 0.3531 | 0.0513 | 0.6800 | 10.64 |
    | 4000 | 4.8518 | 0.4467 | 0.4337 | 0.0404 | 0.8286 | 23.97 |
    | 5000 | 4.6874 | 0.4911 | 0.4440 | 0.0187 | 0.9599 | 19.35 |
    | 6000 | 4.4072 | 0.5489 | 0.4961 | 0.0672 | 0.7423 | 36.82 |
    | 7000 | 4.0098 | 0.5602 | 0.5174 | 0.0477 | 0.9843 | 52.29 |
    | 8000 | 3.7789 | 0.5868 | 0.5427 | 0.0384 | 0.9125 | 29.43 |
    | 9000 | 3.6135 | 0.6106 | 0.5647 | 0.0321 | 0.9190 | 29.73 |
    | 10000 | 3.6956 | 0.6309 | 0.5792 | 0.0905 | 0.8285 | 14.60 |
    | 11000 | 3.2990 | 0.6476 | 0.5969 | 0.0326 | 0.7547 | 9.19 |
    | 12000 | 3.1278 | 0.6622 | 0.6119 | 0.0336 | 0.8855 | 11.27 |
    | 13000 | 3.2815 | 0.6675 | 0.6182 | 0.0550 | 0.5396 | 15.61 |
    | 14000 | 3.0034 | 0.6712 | 0.6209 | 0.0251 | 0.5767 | 16.09 |
    | 15000 | 2.6713 | 0.6980 | 0.6570 | 0.0218 | 0.7462 | 20.92 |
    | 16000 | 2.8534 | 0.7251 | 0.6727 | 0.0559 | 0.8413 | 28.75 |
    | 17000 | 2.9424 | 0.7095 | 0.6566 | 0.0616 | 0.7512 | 20.23 |
    | 18000 | 2.7453 | 0.6995 | 0.6519 | 0.0312 | 0.6439 | 18.65 |
    | 19000 | 2.6923 | 0.7157 | 0.6664 | 0.0369 | 0.6934 | 16.09 |
    | 20000 | 2.5840 | 0.7265 | 0.6783 | 0.0361 | 0.7465 | 14.14 |
  - 档案馆（report JSON `k_side[0].levels`，n=12/档，检索器 train_loss 6.6806→6.2952）：D=4 hit1/3/5 = 0.00/0.25/0.3333；D=16 = 0.0833/0.1667/0.1667；**D=64 = 0.00/0.00/0.00**（rand1 0.0014）——m=1 手术 b 格的 D=64 hit@1 0.1667 / hit@5 0.4167 信号归零。V 侧 byte_acc（`v_side.<D>.arms` direct/backbone）：D=4 0.5714/0.5833；D=16 0.5833/0.5952；D=64 0.5476/0.5238——E78 的 direct−backbone 裂口（15–21pp）在 m=4 下闭合到噪声带。
- **结论**：按预注册验收（D=64 hit@1 显著超 0.17）未达到且方向为负——m=4 首臂既没买到寻址又亏 codec ~4pp（每段条件可能被稀释）；m 扫描 {1,2,8} 补齐后才能判多视角轴平/负；非终局判词（终考需 n≥48 三 seed 协议）。

### E86 — 复训器加固版重跑未手术对象 + 附录 A 消费剖面

- **登记**：`docs/CURRENT_STATE.md:155`；run：`checkpoints/retrain_readout_c_v371_completion_ubb_hardened_20260819/`；剖面：`outputs/consumption_profile_20260819/SUMMARY.txt`、`consumption_profile.json`（脚本 `tools/analysis/v3_6/measure_consumption_profile.py`）。
- **目的**：① 以加固复训器（§4 清单）重跑 E83 发散的未手术对象，分离"发散是几何必然还是安全带缺失"；② 附录 A：手术 b 格的层级消费 + 逐 slot 信息剖面。
- **配置**（pt args）：同 E83 对象 1 + 加固四件（grad_clip 1.0、nan_abort_after 10、warmup_steps 200 + cosine、resume 结构）；可训 14,947,335 params / 94 tensors（stdout.log 首行，freeze_backbone=False）。
- **关键指标**：
  - 重跑：全程 **nan_skips=0**（stdout.log 末行，4047s），平安通过 E83 的 12.3K 发散点；饱和 natural_full **0.0722**@20K（plateau 0.0722；natural_stateonly 0.0715、oracle_full 0.0687、oracle_stateonly 0.0688）。对照手术版同配方 0.300——**同预算同配方 4 倍饱和上限差距**（"几何健康度→可训练性"副产物，仅补全复训路径成立）。完整逐千步曲线见 §6。
  - 附录 A 层级消费（手术 b 格 16 窗，shuffle 干预，baseline acc 0.3056）：置乱 k_rows 仅掉 3.5pp（0.2705，K 装饰性互证到 b 格）；置乱 v_rows 崩到 0.0411（Δ 0.2644，内容旁路承重）；bb_cross1 0.0502、bb_self0/1 0.0373、dec0-2 0.0372/0.0254/0.0272（Δ 0.255–0.280，KL 1.98–2.34）。
  - 逐 slot 信息剖面（接口=k_rows 状态读出行，岭回归 2-fold，real−garbage）：slot0 +0.1264（real 0.2777 vs garbage 0.1513）→ slot8 +0.0884 → slot16 +0.0469 → slot24 +0.0185 → slot31 +0.0505；majority 基线 slot0 0.2138——**信息密度集中段首**，slot18-31 掉到 ~0.02–0.05（fork 2 m 扫描预测器：多视角边际收益天然有限，E85 否定读数的上游解释之一）。
- **结论**：E83 对象 1 发散的直接起因是安全带缺失（无 clip/无 NaN 保护）而非几何必然；修复后浮出 4 倍饱和上限差距；消费剖面支撑 E-d 自发分工均衡再证。

### E87 — 40K 延长臂（手术版补全复训，链条边界实测闭环）

- **登记**：`docs/CURRENT_STATE.md:156`；run：`checkpoints/retrain_readout_c_tokcenter_40k_20260819/`。
- **目的**：E81 遗留"边界未定"（20K 处仍爬坡）——同配方延长到 40K，实测补全形态读出链的饱和平台。
- **配置**（pt args）：对象 = 手术 c 格 ckpt；steps 40000、lr 1e-3（warmup 200 + cosine 到 0）、oracle_frac 0.8→0.3、μ 课程档同前、freeze_backbone=False；含 resume 结构（`retrain_state_latest.pt` 落盘）；可训 14,947,335 params / 94 tensors。
- **关键指标**（train_log.jsonl）：0.2605@1K → 0.2812@4K → 0.3075@20K（E83"20K 处仍在爬"属实）→ 0.3155@30K → **0.3185@39K–40K 走平**（plateau_acc 0.3185，末 2K 逐位不变）；全程 nan_skips=0（stdout.log 末行，7977s）；四臂终评全 0.3185；lr 末端 0.0（cosine 到 0 存证）。逐千步全表见 §6。
- **结论**：读出链（补全形态+主干入链+加固+μ 课程）能力边界实测 **0.3185**——E81"边界未定"闭环为"边界已实测"；与 0.6185 线性探针地板之间的 0.30 缺口 = 接口形态容量缺口的定量定格；单向量接口形态是限速墙的证据链完整（E83 初测 0.30 → E87 实测 0.3185 饱和）。

---

## 2. 三张配置卡

### 2.1 配置卡一：E73 oracle 判决三臂构造（`tools/analysis/v3_6/probe_oracle_write_verdict.py`）

三臂共享同一冻结管线：前端（`_front_end`，`:167-176`）→ WriteHead 门（k/v/alpha/beta）→ 状态/读出替换 → `decode_direct`（`:251-258`：`decoder_in(v_rows) + chunk_pos → decoder`，逐段独立、切分精确）。

- **A1 trained 臂**——状态：`trained_states`（`:178-197`）：逐段复现 KDAStateMachine._forward_torch 的 delta 递推（`S = α·S − β·k(kᵀS) + β·k vᵀ`，`:192-195`；padding 行为恒等步，停在 n_real 精确），输出每段吃完 chunk i 后的 S_i（B,n,H,hk,hv）。读出：`read_trained`（`:209-218`）：固定 readout_query `q`（nq,H,hk）einsum 读出 → reshape → `sm.realign(read).mean(dim=2)`（nq 均值），与模型 `_forward_torch`+`_slm_store_rows` 的 v_rows 形态一致。
- **A2 oracle 写入臂**——状态：`oracle_states`（`:200-206`）：`S_i = Σ_{j≤i} k_j v_jᵀ`，即 `outer = einsum("bchk,bchv->bchkv", k, v).cumsum(dim=1)`——**无衰减、无 delta 擦除的纯累计叠加**；键值来自 c 格自己训好的 WriteHead（不是另造的 oracle 键值）。读出仍走 trained 链。
- **A3 ridge 读出臂**——状态用 trained S_i；读出换闭式岭回归：`ridge_unmix`（`:221-241`）：对每段 i、每头 h，`K = k[0,:i+1,h]`（WriteHead 行已单位范，`:234` 注释），`A = K Kᵀ + λI`，`V̂ = solve(A, K S_i)`，取回本段行 `V̂[-1]`；H 头拼接后经 `read_via_realign`（`:244-248`：`realign(reads.unsqueeze(2)).mean(dim=2)`）进 decoder。λ ∈ {1e-4, 1e-2, 1} 三档（臂矩阵行 `score(f"A3_ridge_trained_l{lam}")`，`:381-385`）。A4 = oracle 态 × 同一 ridge 读出（2×2 非对角元）。
- **A6 "内容向量保留 82%" 探针的输入→输出映射**（`byte_probe`，`:266-290`）：
  - 输入 X：该段**写值向量 v_i**（H·hv = 4×256 = 1024 维；上限对照为 memory 行 m_i，512 维）；输出 Y：该段 slot s（s=0..3）的**字节 id**（one-hot 258 类，`:278`）。
  - 映射：one-vs-all 岭回归闭式解 `W = solve(XᵀX + λI, XᵀY₁)`，λ=1.0，特征尾接常数 1 列（bias，`:277`）；**2-fold**：固定种子 0 的 randperm 前后半互训互测（`:279-287`），报两折均值 acc 与 majority 基线（`:288-289`）；n<40 的 slot 跳过（`:275-276`）。
  - 读数（SUMMARY.txt）：v→slot0 acc 0.6185 vs majority 0.2138；m→slot0 0.7096。"保留 82%" = slot0 上 (0.6185−0.2138)/(0.7096−0.2138) ≈ 0.816（本档案按 SUMMARY 数字复算；登记行原文"保留 memory 行 82% 线性信息增量"）。
  - 纯代数零训练（`:60`、`":269"` docstring"Closed-form algebra only"）。

### 2.2 配置卡二：E83 fork 1 四评测臂接线（`tools/train/v3_6/retrain_readout_chain.py`）

四臂 = {natural, oracle} × {full, stateonly}，由 `evaluate_chain`（`:327-336`）双重循环产出，每臂 = `_eval_acc`（`:296-324`）一次 16 窗（eval seed 1042）补全形态 byte_acc（CLEAN 累积网格目标，`make_cumulative_retention_targets`，`:315-317`）：

- **条件来源（状态侧）**：`_states_for`（`:223-241`）——natural 臂 = `trained_states`（KDA delta 递推）；oracle 臂 = `oracle_states`（纯累计叠加）；**eval 时 lam=None**（`:313` 调用不传 lam），即评测用纯累计 oracle 态，μ 课程混合只在训练步（`train_step:273` 抽档）。
- **条件来源（存储两侧）**：`_chain_logits`（`:244-257`）——c 格 K 侧 `k_rows = index[:, :n_real]`（summarizer 直通 index 行，`:234`）；**c 格 v=state 时 store 的 V 侧 = 状态读出行**：固定 readout_query 读出 S → `sm.realign(read).mean(dim=2)` 得 v_rows（`:250-253`，梯度从 realign 起）；`backbone(k_rows, v_rows, mask, pos)` → `cond = backbone_out + pos` → decoder（`:255-257`）。
- **full 臂**：store 原样（工程上限）。
- **stateonly 臂**：`_eval_acc` 把 `model.backbone.k_block_eval` 置 True（`:305-307`），finally 复原（`:322-323`）。其机制在 `flued/v36/model.py:1370-1374`：**把对齐后的 K 行整体置零**（`k_flat = torch.zeros_like(k_flat)`），block-1 cross-attention 退化为均匀注意力——注意力键不再携带任何 index 内容。
- **审计问题："状态独存"臂里内容旁路（V 直读通道）被遮蔽了还是还在？**——**还在，两处**：
  1. store 的 **V 侧完全不动**：`k_block_eval` 只零化 `k_flat`，`store_v = align_v(v_rows)`（`model.py:1354`）原样进入注意力 value（`:1376`）。c 格上这个 V 侧本来就是状态读出行（设计内——该臂要测的就是"只留状态读出行承载内容"，`retrain_readout_chain.py:14-17` 护栏一 docstring）。
  2. **种子通道不被动**：`model.py:1359-1362` 注释明言 "pos-injection/k-block below touch attention keys only, never the seed"。对象 2 是 K-seed 格（seed_source=k），种子 = `align_k(index 行)`（`:1362`）——**stateonly 臂下 index 内容仍经种子进入隐藏态**（复训器 docstring `:17-18` 同样登记："K-seed 格的种子通道按构造保留 index 内容，消融只作用于注意力键"）。对象 1（v371，seed_source=v）种子 = align_v(v_rows)，与 V 侧同源。
  - 口径后果：对象 2 的 stateonly 不是"纯状态"条件（种子携带 index 直通内容）；E83 四臂全同 0.2999 的"K 消融无差异"读数应在此口径下引用。
- **入口守卫**：`:383-389`——v_row_source≠"state" 或 k_row_source≠"index" 的 ckpt 直接 ValueError（fork 1 护栏一只定义在 c 格）。

### 2.3 配置卡三：E85 fork 2 首臂（m=4 多视角训练格）

- **基座**：`configs/canonical_v37.json`（v37.2-20260817，a 格锚）+ 覆盖：`k_row_source=state`（b 格）、`to_k_center=true`、`readout_views=4`、`verify_topl=0`、`cloze_prob=0.3/cloze_weight=0.3`、ctx 4096（seq 4096/stride 2048/batch 1/max_chunks 1024）、20K 步。全部字段值见 §1-E85 配置段（resolved_config.json 全录）。
- **多视角机制**（代码层）：`_slm_store_rows(with_views=True)`（`flued/v36/model.py:1963-1968`）在 k_row_source=state 时额外产出 `k_store = state_machine_k.forward_views(gates_k, chunk_mask)`（B,C,m,d_pack）；`_forward_slm:2000-2005` 把 k_store/v_store 喂给主干；`SLMBackbone.forward:1348-1351` 检测 4 维输入路由进 `_forward_views`（`:1398-1450`）：每段 m 条测量行进 store，align_k/align_v/realign m 路**共享**（零新参数——params 47,970,472 与 m=1 手术 b 格逐位相同，两 run summary.json 互证），种子 = view-0 K 行 / view 均值 V 行（`:1424`）；查询位置仍逐段，位置 i 见 chunks 0..i 的全部视角（因果掩码 `:1437-1445`）；direct/predict 路径仍用单条 trained-readout 行、位不变（`:1954-1958` docstring）。
- **训练曲线**：逐千步表（loss/direct_acc/backbone_acc/cloze_byte_acc/key_mu_k/state_norm）见 §1-E85——爬坡形态要点：codec 双指标 1K–16K 单调爬（direct 0.2973→0.7251），17K–18K 小幅回落（0.7095→0.6995）后收 0.7265；key_mu_k 全程在 0.54–0.98 区间震荡无趋势（终态 train 0.7465 / eval 0.7309，暖 buffer 口径下仍居塌区上沿）；state_norm 3K 起破 10、7K 峰值 52.29 后回落 14–29 震荡；cloze_byte_acc 全程 ≤0.09 贴地。
- **判负读数**：终评 codec 四指标全线让位 ~4pp（§1-E85 对照表）；档案馆 D=64 hit@1/hit@5e 归零（report JSON `k_side[0].levels."64"`：hit1 0.0、hit5 0.0、hit5_entry 0.0，rand1 0.0014）。

---

## 3. 模型接线说明：种子路径与 `--k-row-source` / `--v-row-source`

（全部行号以工作区当前 `flued/v36/model.py` 为准；任务书原估"forward ≈:1140-1180、_slm_store_rows ≈:1666"已漂移，实际为 `class SLMBackbone` :1241、`forward` :1335-1396、`_slm_store_rows` :1944-1987。）

### 3.1 主干"拿状态当种子"过不过 realign？——**不过**

- 种子构造（`SLMBackbone.forward:1352-1363`）：`store_v = align_v(v_rows)`（:1354）、`k_flat = align_k(k_rows)`（:1355），`seed = k_flat if seed_source=="k" else store_v`（:1362），`h = seed + pos`（:1363）。
- `align_k`/`align_v` 是**无 bias 单层线性**（`nn.Linear(k_dim|v_dim, d_backbone, bias=False)`，`:1283-1284`），docstring 明言"PURE dimensional alignments … NOT content parsers"（`:1252-1254`）。**realign 不出现在种子路径上**。
- realign 出现的位置：仅状态机读出内部（`KDAStateMachine` 各 forward 形态，如 `:782`、`:899`、`:968`、`:992`——固定 readout_query 读出后 `self.realign(read)`）。当通道源为 state 时，行在 `_slm_store_rows` 生成阶段已经过了这一次 realign：k=state → `write_head_k(index)` → `state_machine_k` → `package_k.mean(dim=2)`（`:1963-1966`）；v=state → `write_head(memory)` → `state_machine` → `package_v.mean(dim=2)`（`:1972-1975`）。
- 因此精确表述：**种子 = align_k(行) 或 align_v(行) + chunk_pos**；若该行来自 state 通道，它在行生成时已过一次 realign（状态机读出环节），种子拼接环节本身不再过 realign，只过 align_k/align_v 纯维对齐。
- fork 2 多视角路径同理：种子 = `align_k(k_rows[:,:,0])`（K-seed）或 `align_v(v_rows.mean(dim=2))`（V-seed），`:1424`。
- 附带口径：`k_pos_inject` 与 `k_block_eval` 只作用于注意力键 `k_flat`，**从不碰种子**（`:1359-1361` 注释；置零在 `:1370-1374`）。

### 3.2 `--k-row-source` / `--v-row-source` 语义与合法组合

- **CLI 定义**（`tools/train/v3_6/train_v36.py`）：`--k-row-source` choices=["memory","state","index"] 默认 memory（`:295-302`，help：memory=状态前 memory 行；state=逐段状态读出（内容）经专用投影；index=summarizer index 行，仅 v3.7 slm 模式）；`--v-row-source` choices=["memory","state"] 默认 memory（`:304-309`）。
- **slm 模式合法域**（`model.py:1270-1278`）：k ∈ {index, state}——`memory` 对 K 通道**非法**（"the memory row is the V standard"，`:1272-1276`；模型级守卫重复于 `:1841-1845`）；v ∈ {memory, state}（`:1277-1278`）。由此定义 S39 四格：a=(index,memory)、b=(state,memory)、c=(index,state)、d=(state,state)（canonical_v37.json `usage_note` 字段同述）。
- **配套守卫**（全部响亮报错，不静默回退）：
  - `seed_source ∈ {v, k}`（`:1317-1319`）：v = 种子取 align_v(V 行)（consensus §1.3 默认旧口径）；k = 种子取 align_k(index/K 行)，K 内容经种子进深层自注意力（v37.2 默认，`train_v36.py:329-336` help）。
  - `k_pos_inject` 仅在 k=index 且 v=memory 合法（a+pos 单变量臂，`:1320-1331`；CLI help `train_v36.py:310-319`）。
  - slm 还要求 summarizer_type="dit"（`:1836-1840`）、per_chunk_readout=True（`:1846-1847`）、backbone_readout="per_chunk"（`:1848-1851`）、prefix_task=False（`:1852-1853`）；与 codec_final/paged/draft 组合一律报错（canonical usage_note）。
  - 旧 xattn 路径：k/v_row_source ∈ {memory, state}，state 对 paged_xattn 未定义（`:1091-1096`）；k_pos_inject 要求双 memory（`:1113` 一带）。
- **通道落线**（`_slm_store_rows:1944-1987`）：summarizer 直产 (memory, index)（`:1959`）；k=state 才创建 K 通道 WriteHead+状态机对、v=state 才创建 V 通道对（**a 格两者都不创建**，`:1876-1881` 条件创建）；v=memory 时另建 `decoder_in_mem` 细粒度对齐（`:1885-1886`），direct 条件随 V 源走（`_forward_slm:2007-2008`：`dec_in = decoder_in if v==state else decoder_in_mem`；`cond_direct = dec_in(v_rows)+pos`）。

---

## 4. 复训器加固配方改动清单（`tools/train/v3_6/retrain_readout_chain.py`，2026-08-19 用户裁定四项，docstring `:31-37`）

| 项 | 内容 | 代码行号 |
|---|---|---|
| ① 梯度裁剪 | `--grad-clip` 默认 **1.0**（`:357`）；`clip_grad_norm_` 作用于全部 requires_grad 参数（`:286`），日志记录 pre-clip grad_norm（`:455`） | :286, :357, :455 |
| ② NaN 护栏 | loss 非有限 → 跳步、指标不前进（`:279-284`）；grad 非有限（有限 loss 也可能产出非有限梯度）→ zero_grad 跳步（`:287-291`）；`NanSkipTracker`（`:91-111`）：**连续** `--nan-abort-after`（默认 **10**，`:360-361`）次跳步 → 响亮退出（`SystemExit(1)`，写 abort 行进日志，**不覆盖**最近 resume 状态，`:445-452`）；成功步重置连续计数（`:107-108`）；跳步永不推进指标（`:442-444`，AGENTS.md 陷阱 3） | :91-111, :279-291, :360-361, :442-452 |
| ③ LR 日程 | `lr_at`（`:79-88`）：`--warmup-steps`（默认 **200**，`:358-359`）线性 0→base_lr，随后**余弦衰减到 0**（step=total_steps 处恰为 0）；对 step 无状态 → resume 后落在同一 lr 轨迹（`:82-83`）；应用点 `:437-439`。存证：加固版 stdout.log 首行 lr 5e-06@1 → 0.001@200 → 末行 lr 0.0@20000 | :79-88, :358-359, :437-439 |
| ④ resume 结构 | `save_retrain_state`（`:128-147`）：modules（realign/decoder_in/decoder 剔 byte_lookup 行，±backbone，`:114-125`）+ optimizer + step + **全部 RNG 流**（mix_rng/torch/cuda/_MASK_GENERATOR，`:137-140`）+ nan 计数 + eval 历史 + args；`load_retrain_state`（`:150-177`）：冻结面不一致即响亮 ValueError（`:158-162`）；数据流确定性重建后按 step 快进（`:420-421`）；`--resume`/`--resume-path`（`:364-366`）；保存节奏 `--save-every` 默认 1000（`:362-363`、`:476-477`），落 `<out-dir>/retrain_state_latest.pt` | :114-177, :362-366, :420-421, :476-477 |

关联修正（先于加固、同属 E83 教训链）：`--oracle-frac-end` 默认 0.1→**0.3**（"修正一 2026-08-19"，`:347`  help 原文）。验证存证：E86 加固重跑全程 nan_skips=0、E87 40K 全程 nan_skips=0（两 run stdout.log 末行）。

---

## 5. 历史档案

### 5.1 E66 / E64 K-block 探针零漂移原始测量

- E64（登记 `docs/CURRENT_STATE.md:133`；探针 `outputs/probes/v37_kblock_a_im_20260817.log`、`v37_kblock_b_sm_20260817.log`）——eval 时 K 通道键清零（`--k-block-eval`）重测 V-seed a/b 格：
  - a 格（log 原值）：direct_acc 0.7923 / backbone_acc 0.7466 / masked 0.1323 / unmasked 0.7794 / direct_ppl 2.1411 / backbone_ppl 2.6421 / predict_cos 0.5619（对照登记原值 0.7923/0.7468/0.1341/2.141——漂移 ≤0.2pp）。
  - b 格（log 原值）：direct_acc 0.7780 / backbone_acc 0.7338 / masked 0.1371 / unmasked 0.7657 / direct_ppl 2.2725 / backbone_ppl 2.7887 / state_norm 254.80（对照 0.7780/0.7337/0.1371/2.273）。
- E66（登记 `:135`；探针 `outputs/probes/v37ks_a_kblock_20260817.log`）——K-seed a 格（v37ks_a_im_v371_20k_ctx4096_20260817）键清零重测：direct_acc 0.8063 / backbone_acc 0.7568 / masked 0.1220 / unmasked 0.7907 / direct_ppl 2.0116 / backbone_ppl 2.5157 / predict_cos 0.3406 / state_norm 0.0（a 格无状态机）。对照本格无屏蔽终评（登记行）：direct_ppl 逐位相同（2.012）、backbone_ppl 2.5157 vs 2.5136、masked 0.1220 vs 0.1235——**第二次零漂移**（漂移 ≤0.2pp）。
- 判读（登记行）：V-seed 下索引通道装饰化（K 仅出现于 block-1 Q·K，被路由成均匀注意力）；K-seed 使 K 内容经种子进自注意力，block-1 的 K/V 库检索依旧无人用；K-seed 本身无害且略优（v37.2 默认种子的依据）。

### 5.2 v37.2 canonical 配置关键字段（`configs/canonical_v37.json` 原值）

canonical_version = `v37.2-20260817`；backbone_mode=slm；**k_row_source=index、v_row_source=memory、seed_source=k**（a 格锚 + K 种子）；summarizer_type=dit（slots 4、hidden 1024、dit_layers 2）、d_mem 512；kda_heads 4、head_k 128、head_v 256、write_hidden 1024、kda_tau_max 256.0；readout_queries 1、d_pack 1536；backbone d 384 / layers 3 / nhead 8 / ffn 1024；decoder hidden 1024 / layers 3；max_chunks 64、max_span 64、bytes_per_chunk 16；tau_cut 0.94、tau_trans 0.75、boundary dynamic（temperature 0.15、bridge_gradient_scale 0.1）；mask mixed：prob 0.05、span 1-8、char_frac 0.4、char_span_max 3；predict latent（weight 1.0、latent_weight 0.1）；lr 2e-4、wd 0.01、fused_adamw、warmup 200、grad_clip 1.0；max_steps 20000、seq_len 512（配置文件内占位口径；正式 run 一律显式覆盖，如 4096 线）、batch_size 8；seed 42、eval_mask_seed 1042；amp true；**init_checkpoint = `K:\FLUED_archive\s0pp_pro_v4_sft_20260805\latest.pt`**、freeze_prefixes = `byte_lookup,encoder_blocks,segmentor_blocks,segmentor_head`；per_chunk_readout true；kda_impl fla；cumulative_mask_retention true。evidence_base / supersedes / usage_note 字段全文见 JSON（v37.2 裁定：默认种子切 K——E66 K-seed a 格略优且无害；E64/E66 K-block 双次零漂移证 V-seed 下索引通道装饰化）。

### 5.3 K-seed 把 index 行 μ 从 0.93 打到 0.17 的实验记录

出处：`outputs/key_collapse_survey_20260818/key_collapse_survey.json` `results[]`（SUMMARY.txt 因子表同值）：

| 格 | run（V-seed → K-seed） | index 行 μ（V-seed） | index 行 μ（K-seed） | seedΔ |
|---|---|---|---|---|
| a | v37_a_im_v371 → v37ks_a_im_v371 | 0.9325±0.0501（PR/n 0.0068） | 0.1736±0.0204（PR/n 0.1204） | **−0.7589** |
| b | v37_b_sm_v371 → v37ks_b_sm_v371 | 0.8583±0.0593 | 0.1251±0.0140 | −0.7332 |
| d | v37_d_ss_v371 → v37ks_d_ss_v371 | 0.7923±0.0423 | 0.1699±0.0246 | −0.6224 |
| c | v37_c_is_v371 → v37ks_c_is_v371 | 0.8847±0.0696 | 0.1569±0.0414 | （SUMMARY 未列此行分解；JSON 原值如上） |

K-seed + cloze 世代 a 格 index 行 0.1867±0.0205（clozeΔ +0.0131——压力不再动几何）。注意对照：**summarizer index 行被 K-seed 修健康后，WriteHead 键照塌**（b 格 K 键 0.9199、c 格 V 键 0.9578）——E74"压塌定位在 WriteHead.to_k 自身、与输入无关"的支柱数据。

---

## 6. 复训 run 逐步指标曲线（全部出自各 run `train_log.jsonl` eval 记录；eval 每 200 步一次、16 窗、seed 1042；loss 列为该步前窗口训练损失均值）

> 任务书称"五条复训 run"但实列 8 个 run-id（首跑×2、μ 课程×2、fork 1×2、加固×1、40K×1）——本档案 8 条全收。地板常量 0.6185（E73-A6 slot0 线性探针口径）为各 run 内嵌参照；`plateau_acc` = 末 3 次 eval natural full/direct 臂均值（`retrain_readout_chain.py:467`）。

### 6.1 首跑·对象 1（未手术 c 格）`retrain_readout_c_v371_20260818`（5K 步，direct 形态）

| step | loss | direct_acc_natural | direct_acc_oracle |
|---|---|---|---|
| 1000 | 4.999 | 0.0537 | 0.0406 |
| 2000 | 4.951 | 0.0630 | 0.0468 |
| 3000 | 4.645 | 0.0997 | 0.0603 |
| 4000 | 4.397 | 0.1248 | 0.0594 |
| 5000 | 4.256 | 0.1641 | 0.0621 |

### 6.2 首跑·对象 2（手术 c 格）`retrain_readout_c_tokcenter_20260818`（5K 步，direct 形态）

| step | loss | direct_acc_natural | direct_acc_oracle |
|---|---|---|---|
| 1000 | 4.861 | 0.0655 | 0.0564 |
| 2000 | 4.769 | 0.0937 | 0.0606 |
| 3000 | 4.561 | 0.1191 | 0.0620 |
| 4000 | 4.257 | 0.1670 | 0.0644 |
| 5000 | 4.125 | 0.2042 | 0.0613 |

### 6.3 μ 课程·对象 1 `retrain_readout_c_v371_mucurr_20260818`（20K 步，direct 形态）

| step | loss | natural | oracle | | step | loss | natural | oracle |
|---|---|---|---|---|---|---|---|---|
| 1000 | 4.921 | 0.0598 | 0.0553 | | 11000 | 4.505 | 0.1255 | 0.0697 |
| 2000 | 4.885 | 0.0716 | 0.0590 | | 12000 | 4.504 | 0.1342 | 0.0691 |
| 3000 | 4.825 | 0.0717 | 0.0614 | | 13000 | 4.514 | 0.1426 | 0.0683 |
| 4000 | 4.834 | 0.0777 | 0.0642 | | 14000 | 4.399 | 0.1488 | 0.0694 |
| 5000 | 4.728 | 0.0803 | 0.0631 | | 15000 | 4.317 | 0.1582 | 0.0693 |
| 6000 | 4.734 | 0.0921 | 0.0649 | | 16000 | 4.380 | 0.1680 | 0.0698 |
| 7000 | 4.662 | 0.0967 | 0.0669 | | 17000 | 4.360 | 0.1715 | 0.0696 |
| 8000 | 4.649 | 0.1034 | 0.0679 | | 18000 | 4.268 | 0.1835 | 0.0697 |
| 9000 | 4.630 | 0.1060 | 0.0669 | | 19000 | 4.314 | 0.1916 | 0.0702 |
| 10000 | 4.575 | 0.1119 | 0.0685 | | 20000 | 4.243 | 0.1898 | 0.0702 |

终评 plateau 0.1916（below_floor）。

### 6.4 μ 课程·对象 2 `retrain_readout_c_tokcenter_mucurr_20260818`（20K 步，direct 形态）

| step | loss | natural | oracle | | step | loss | natural | oracle |
|---|---|---|---|---|---|---|---|---|
| 1000 | 5.062 | 0.0500 | 0.0409 | | 11000 | 4.593 | 0.0999 | 0.0587 |
| 2000 | 5.066 | 0.0504 | 0.0410 | | 12000 | 4.606 | 0.1063 | 0.0595 |
| 3000 | 4.956 | 0.0537 | 0.0409 | | 13000 | 4.580 | 0.1149 | 0.0616 |
| 4000 | 4.879 | 0.0552 | 0.0409 | | 14000 | 4.452 | 0.1215 | 0.0611 |
| 5000 | 4.915 | 0.0580 | 0.0407 | | 15000 | 4.393 | 0.1322 | 0.0615 |
| 6000 | 4.946 | 0.0589 | 0.0410 | | 16000 | 4.426 | 0.1466 | 0.0638 |
| 7000 | 4.896 | 0.0584 | 0.0409 | | 17000 | 4.413 | 0.1567 | 0.0640 |
| 8000 | 4.872 | 0.0596 | 0.0409 | | 18000 | 4.316 | 0.1640 | 0.0644 |
| 9000 | 4.875 | 0.0610 | 0.0410 | | 19000 | 4.360 | 0.1771 | 0.0644 |
| 10000 | 4.673 | 0.0937 | 0.0559 | | 20000 | 4.258 | 0.1837 | 0.0645 |

终评 plateau 0.1807（below_floor）。注意 1K–9K 近平台（0.050–0.061）、10K 后才起步——μ 课程版对象 2 的爬坡比对象 1 晚约 9K 步。

### 6.5 fork 1·对象 1（未手术）`retrain_readout_c_v371_completion_ubb_20260819`（20K 步，补全形态，加固前）

| step | loss | nat_full | nat_stateonly | orc_full | orc_stateonly |
|---|---|---|---|---|---|
| 1000 | 4.842 | 0.0633 | 0.0638 | 0.0639 | 0.0639 |
| 2000 | 4.797 | 0.0674 | 0.0672 | 0.0673 | 0.0673 |
| 3000 | 4.752 | 0.0675 | 0.0675 | 0.0675 | 0.0675 |
| 4000 | 4.776 | 0.0680 | 0.0677 | 0.0677 | 0.0677 |
| 5000 | 4.707 | 0.0680 | 0.0675 | 0.0676 | 0.0676 |
| 6000 | 4.737 | 0.0683 | 0.0682 | 0.0682 | 0.0682 |
| 7000 | 4.677 | 0.0680 | 0.0676 | 0.0677 | 0.0676 |
| 8000 | 4.673 | 0.0689 | 0.0682 | 0.0682 | 0.0682 |
| 9000 | 4.695 | 0.0678 | 0.0674 | 0.0674 | 0.0674 |
| 10000 | 4.653 | 0.0689 | 0.0685 | 0.0685 | 0.0685 |
| 11000 | 4.657 | 0.0685 | 0.0682 | 0.0682 | 0.0682 |
| 12000 | 4.694 | 0.0681 | 0.0678 | 0.0678 | 0.0678 |
| 13000–20000 | **NaN** | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

train loss 首个 NaN 在 **step 12300**（train_log.jsonl 训练记录，每 50 步一条；12.3K–20K 共 155 条 NaN-loss），eval 自 13K 起归零——发散前 12K 步一直贴在 0.068 平台。

### 6.6 fork 1·对象 2（手术）`retrain_readout_c_tokcenter_completion_ubb_20260819`（20K 步，补全形态，加固前）

| step | loss | nat_full | nat_stateonly | orc_full | orc_stateonly |
|---|---|---|---|---|---|
| 1000 | 3.962 | 0.2425 | 0.2426 | 0.2443 | 0.2444 |
| 2000 | 3.874 | 0.2700 | 0.2701 | 0.2699 | 0.2700 |
| 3000 | 3.859 | 0.2709 | 0.2709 | 0.2710 | 0.2709 |
| 4000 | 3.747 | 0.2809 | 0.2809 | 0.2810 | 0.2810 |
| 5000 | 3.784 | 0.2791 | 0.2791 | 0.2790 | 0.2790 |
| 6000 | 3.821 | 0.2864 | 0.2864 | 0.2864 | 0.2864 |
| 7000 | 3.731 | 0.2859 | 0.2859 | 0.2859 | 0.2859 |
| 8000 | 3.761 | 0.2860 | 0.2860 | 0.2860 | 0.2860 |
| 9000 | 3.721 | 0.2894 | 0.2894 | 0.2894 | 0.2894 |
| 10000 | 3.715 | 0.2922 | 0.2922 | 0.2922 | 0.2922 |
| 11000 | 3.658 | 0.2946 | 0.2946 | 0.2946 | 0.2946 |
| 12000 | 3.713 | 0.2935 | 0.2935 | 0.2935 | 0.2935 |
| 13000 | 3.758 | 0.2960 | 0.2960 | 0.2960 | 0.2960 |
| 14000 | 3.607 | 0.2975 | 0.2974 | 0.2975 | 0.2975 |
| 15000 | 3.656 | 0.2956 | 0.2956 | 0.2956 | 0.2956 |
| 16000 | 3.703 | 0.2978 | 0.2978 | 0.2978 | 0.2978 |
| 17000 | 3.687 | 0.2977 | 0.2977 | 0.2977 | 0.2977 |
| 18000 | 3.618 | 0.2997 | 0.2997 | 0.2997 | 0.2997 |
| 19000 | 3.740 | 0.3002 | 0.3002 | 0.3002 | 0.3002 |
| 20000 | 3.628 | 0.2999 | 0.2999 | 0.2999 | 0.2999 |

终评 plateau_acc 0.300（below_floor）。爬坡形态：1K 即 0.24（起步远高于对象 1 的 0.06），4K 破 0.28 后进入缓坡，全程四臂几乎逐位相同。

### 6.7 加固重跑（未手术对象）`retrain_readout_c_v371_completion_ubb_hardened_20260819`（20K 步，补全形态，加固版）

| step | loss | nat_full | nat_stateonly | orc_full | orc_stateonly |
|---|---|---|---|---|---|
| 1000 | 4.807 | 0.0680 | 0.0679 | 0.0675 | 0.0675 |
| 2000 | 4.814 | 0.0671 | 0.0669 | 0.0669 | 0.0669 |
| 3000 | 4.748 | 0.0682 | 0.0683 | 0.0683 | 0.0683 |
| 4000 | 4.773 | 0.0683 | 0.0680 | 0.0680 | 0.0680 |
| 5000 | 4.710 | 0.0678 | 0.0679 | 0.0679 | 0.0679 |
| 6000 | 4.746 | 0.0681 | 0.0679 | 0.0679 | 0.0679 |
| 7000 | 4.675 | 0.0687 | 0.0685 | 0.0685 | 0.0685 |
| 8000 | 4.674 | 0.0684 | 0.0681 | 0.0681 | 0.0681 |
| 9000 | 4.692 | 0.0686 | 0.0682 | 0.0682 | 0.0682 |
| 10000 | 4.654 | 0.0690 | 0.0686 | 0.0686 | 0.0686 |
| 11000 | 4.660 | 0.0697 | 0.0691 | 0.0689 | 0.0689 |
| 12000 | 4.695 | 0.0695 | 0.0692 | 0.0690 | 0.0690 |
| 13000 | 4.695 | 0.0696 | 0.0696 | 0.0686 | 0.0686 |
| 14000 | 4.634 | 0.0706 | 0.0704 | 0.0690 | 0.0690 |
| 15000 | 4.606 | 0.0713 | 0.0708 | 0.0690 | 0.0691 |
| 16000 | 4.653 | 0.0712 | 0.0710 | 0.0686 | 0.0687 |
| 17000 | 4.637 | 0.0719 | 0.0711 | 0.0688 | 0.0690 |
| 18000 | 4.612 | 0.0720 | 0.0712 | 0.0689 | 0.0691 |
| 19000 | 4.670 | 0.0721 | 0.0714 | 0.0688 | 0.0688 |
| 20000 | 4.597 | 0.0722 | 0.0715 | 0.0687 | 0.0688 |

全程 nan_skips=0（stdout.log 末行）；平安通过 12.3K 历史发散点。**爬坡形状**：1K–13K 贴 0.068–0.070 长平台（与 6.5 发散前同区），14K 起以 ~0.0005/K 步的斜率缓慢爬坡至 0.0722 未走平——与 6.6 手术版"1K 即 0.24、4K 破 0.28"的形状对比即"几何健康度→可训练性"的曲线级证据：同预算同配方，饱和上限 0.0722 vs 0.300（4.2×）。

### 6.8 40K 延长（手术对象）`retrain_readout_c_tokcenter_40k_20260819`（补全形态，加固版）

| step | loss | nat_full | | step | loss | nat_full |
|---|---|---|---|---|---|---|
| 1000 | 3.876 | 0.2605 | | 21000 | 3.610 | 0.3079 |
| 2000 | 3.871 | 0.2704 | | 22000 | 3.611 | 0.3092 |
| 3000 | 3.838 | 0.2760 | | 23000 | 3.626 | 0.3096 |
| 4000 | 3.745 | 0.2812 | | 24000 | 3.592 | 0.3109 |
| 5000 | 3.780 | 0.2812 | | 25000 | 3.666 | 0.3121 |
| 6000 | 3.823 | 0.2867 | | 26000 | 3.539 | 0.3122 |
| 7000 | 3.720 | 0.2887 | | 27000 | 3.531 | 0.3141 |
| 8000 | 3.755 | 0.2873 | | 28000 | 3.588 | 0.3146 |
| 9000 | 3.708 | 0.2921 | | 29000 | 3.715 | 0.3145 |
| 10000 | 3.703 | 0.2958 | | 30000 | 3.614 | 0.3155 |
| 11000 | 3.649 | 0.2956 | | 31000 | 3.544 | 0.3160 |
| 12000 | 3.700 | 0.2972 | | 32000 | 3.581 | 0.3166 |
| 13000 | 3.742 | 0.2989 | | 33000 | 3.623 | 0.3172 |
| 14000 | 3.592 | 0.2996 | | 34000 | 3.602 | 0.3171 |
| 15000 | 3.643 | 0.3012 | | 35000 | 3.527 | 0.3176 |
| 16000 | 3.685 | 0.3025 | | 36000 | 3.609 | 0.3182 |
| 17000 | 3.667 | 0.3033 | | 37000 | 3.613 | 0.3181 |
| 18000 | 3.597 | 0.3050 | | 38000 | 3.699 | 0.3183 |
| 19000 | 3.721 | 0.3059 | | 39000 | 3.611 | 0.3185 |
| 20000 | 3.603 | 0.3075 | | 40000 | 3.579 | 0.3185 |

四臂终评逐位相同（0.3185）；39K–40K 逐位走平（plateau 0.3185）；全程 nan_skips=0；20K 处读数 0.3075 与 E83 同对象 20K 读数 0.2999 的差 = 加固版（warmup+cosine）配方差异（本 run 与 6.6 非同配方延续，比较时注意）。

---

## 7. 对账中发现的不一致与悬空清单

**文档间/文档与数据不一致**：
1. **E83 NaN 时点两处不一致**：E83 登记行（`docs/CURRENT_STATE.md:152`）写"15K 处 loss NaN 发散归零"；E86 登记行（`:155`）写"12.4K NaN 发散点"；train_log.jsonl 实测首个 NaN-loss 在 **step 12300**（12.3K）。以日志为准。
2. **E80 起点读数口径**：登记行（`:149`）"0.134→0.164 / 0.176→0.204"的起点对应 train_log ~4.4K 步处读数，非首评（首评 step 200 = 0.0513 / 0.0303）。登记行选取的是后段区间。
3. **E77 退火终点**：登记行（`:146`）"余弦退火 0.8→0.1"为复训器建成时点口径；现行脚本默认 0.3（`retrain_readout_chain.py:347` 修正一），E81 起各 run pt args 均为 0.3（E80 首跑 args 存证 0.1）。
4. **E85 探针报告落盘目录跨日期**：报告在 `outputs/s39_addressing_probe_v37_20260817/`（0817 目录），探针 log 在 `outputs/s39_addressing_probe_v37_20260818/run_views4_b.log`，run 本身是 0819——引用需以 log 末行路径为准；登记行"report views4"无路径。
5. **任务书行号漂移**：任务书所给 `SLMBackbone.forward ≈ model.py:1140-1180`、`_slm_store_rows ≈ :1666` 与当前工作区不符（实际 :1335-1396 / :1944-1987）；本档案一律以实测行号为准。
6. **"状态独存"臂语义**：E83 登记行"K 消融无差异（K 装饰性再互证）"——在 K-seed 格（对象 2）上 k_block_eval 只置零注意力键、种子通道仍携带 index 内容（`retrain_readout_chain.py:17-18`、`model.py:1359-1362`），该互证应在此口径下引用（详见 §2.2）。
7. **"五条复训 run"**：任务书文字与所列 run-id 数量（8）不符；本档案按 8 条收录。

**悬空（未落盘/未找到）**：
- E80–E83、E86、E87 全部复训 run 的**命令行原文**：复训器不落 resolved_config.json，docs/ 内也无 launcher 记录；本档案以 `retrained_readout.pt` 内嵌 `args` 字段还原（等效参数已列入各页）。其中 E83 两条 run（completion_ubb）连 stdout.log 都未保存，参数量首行（14,947,335/94 tensors）由同配方 E86/E87 的 stdout.log 旁证。
- E75 登记行"W_to_k SVD 有效秩 361–374/512"：SUMMARY.txt 未载，应在 `layerwise_decomposition.json` 内（登记行 `:144` 为唯一文字出处；本档案未逐字段展开该 JSON）。
- E73 A0/A1 逐行字节恢复率 10 分位桶曲线：在 `oracle_write_verdict.json`（本档案引 SUMMARY 聚合值）。

---

*第一部分完。编制：Kimi Code（只读对账，未改动任何被审文件）；编制日期 2026-08-19。*
