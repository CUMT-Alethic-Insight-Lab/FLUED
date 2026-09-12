# Kimi-Linear-48B-A3B-Base 双卡部署 README（kimi122 复证臂）

> 施工：agent，2026-09-12。repo canonical 路径 `tools/analysis/v3_6/`；
> 实例副本 `/root/kimi_linear_deploy/code/`（部署快照，**以 repo 为准**）。
> 上游跨架构仪器：`tools/analysis/cross_arch/probe_e122_deltanet_book.py`（行为侧，
> DeltaNet 臂 500 窗 contrast 0.281 nat CI 不含 0）+ `probe_deltanet_state_readout.py`
> （表示侧）。本臂移植到工业级 SOTA 混合线性注意力 Kimi-Linear-48B-A3B-Base。

## 1. 实例事实（2026-09-12 盘点，卡B 克隆机 15970）

| 项 | 值 |
|---|---|
| CPU / RAM | 208 核 / 1007G |
| 根 overlay | 30G（仅用 864M，**易失**，重置即清） |
| 数据盘 `/root/autodl-tmp` | `/dev/md0` xfs，**170G 配额，41G 已用，130G 可用** |
| `/autodl-pub` | 7.3T NFS，**只读**（touch 实测 Read-only file system） |
| GPU | 无卡模式（nvidia-smi Permission denied），一切 GPU 计算待换卡 |
| Python | `/root/miniconda3` base = 3.12.3，pip 26.1.2（**不在 PATH，用全路径**） |
| 工具链 | git 2.34.1、curl、wget、rsync ✓；conda env 仅 base |

### 存储选项清单（98G 权重落位）

1. **`/root/autodl-tmp`（推荐，唯一可行）**：130G 可用 ≥ 110G 决策阈值 ✓；
   磁盘写速实测 498 MB/s；落位 98.25G 后余 ~32G——**紧**。若语料（corpus_v3.txt
   23G）也须同机共存，建议：① AutoDL 控制台扩容数据盘（用户操作），或
   ② 清理旧 checkpoints（19G，见 §2）——**先报后批，agent 不擅自删**。
2. 根 overlay `/`：30G 且重置即清 → 否。
3. `/autodl-pub`：只读 NFS → 否。
4. lsblk 其余：sda2 893G = 宿主盘（容器内不可挂、不该碰）；nbd1 531G / nbd2 181G
   未附加到本实例 → 无其他用户可写大容量。

## 2. 残留报告（只报不删）

克隆机 `/root/autodl-tmp` **不是空机**（与"全新起"预期不符，实测如此）：
`FLUED/` repo 64M、`checkpoints/` 19G（`v37ks_a_im_v373_scale3x_20k_ctx4096_20260911`
三种子 + `_smoke_scale3x_500`，最新 mtime 2026-09-12 08:00）、`corpus/corpus_v3.txt`
23G（VERIFIED.sha256 在）、gate2_scale3x 日志/输出 224M、git bundle 两个。全部
**未动**。处置权在用户：确认废弃后可整目录清理，回收 ~19.2G。

## 3. 测速记录与下载决策（2026-09-12）

| 通道 | 100MB 采样 | 结论 |
|---|---|---|
| hf-mirror.com | **2.91 MB/s** | < 20MB/s 阈值 |
| modelscope.cn | 4.28 MB/s | 同样不达标（备选参考） |
| 数据盘写速 | 498 MB/s | 磁盘不是瓶颈，网络是 |

**决策（按既定规则）**：不满足「≥110G 且 ≥20MB/s」双条件中的速度项 → **云端全量
下载不起**。权重获取主路径：本地 L: 下载（已在跑，agent-203 侧）完成后**上传实例**
（AutoDL 网盘中转或直传）。若要云端直下：`outputs/_kimi_linear_download/dl_kimi_linear_base.sh`
模板改 `DIR="/root/autodl-tmp/models/Kimi-Linear-48B-A3B-Base"` 后 `setsid nohup`
夜间跑（断点续传 + sha256 校验内建）——**待用户批准再启**。

## 4. 环境安装（无卡即可全做）

```bash
# 一键（幂等；走清华 PyPI 镜像更快）
bash /root/kimi_linear_deploy/code/install_kimi_linear_env.sh
# 或手动：
/root/miniconda3/bin/pip install -U pip
/root/miniconda3/bin/pip install -U "transformers>=4.57.0,<5" "fla-core>=0.4.0" \
    tiktoken einops packaging accelerate
# 可选（MLA 原生后端；缺席自动 SDPA shim，仪器双臂同后端不受影响）：
/root/miniconda3/bin/pip install flash-attn --no-build-isolation
```

`requirements_kimi_linear.txt` 为 pinned 清单。**transformers 必须 <5**（v5 的
`_tied_weights_keys` dict 化与远码/fla 组合有已知的雷，DeltaNet 臂 2026-09 实证）。

## 5. 模型事实速查（ref/ 已读码验证，git blob sha1 对上 HF MANIFEST）

- 层结构：27 层 = **20 KDA + 7 MLA**（3:1）。KDA 层类 `KimiDeltaAttention`
  （modeling_kimi.py 内定义，fla.ops.kda 核）；MLA 类 `KimiMLAAttention`。
  1 基 kda_layers = {1,2,3,5,6,7,9,10,11,13,14,15,17,18,19,21,22,23,25,26}，
  `config.is_kda_layer(i)` 按 i+1 查表（**0 基层号 = 表值 −1**）。
- 线性状态：`KimiDynamicCache.recurrent_states[layer_idx]`，形状
  `[B=1, H=32, K=128, V=128]`（无 GVA），每边界 524288 维；由
  `fla.ops.kda.chunk_kda(output_final_state=True)` 写出。conv 状态另存
  `conv_states[layer_idx]`（kernel=4）。
- 递推式（fla/ops/kda/naive.py 同式，读出仪器独立 fp32 重算 + 终态对拍哨兵）：
  `S ← S·exp(g_t)（K 维 fine-grained 门控）; S += (βk_t) ⊗ (v_t − k_tᵀS)`；
  q,k 进核前逐 token L2。
- tokenizer：`TikTokenTokenizer`（tiktoken.model，词表 163840）；**`__call__`
  不前置 BOS**（未覆写 build_inputs_with_special_tokens）——窗 = 裸 token 序列。
- 版本：transformers ≥4.56（config 以 4.57.0 构建）、torch ≥2.6、fla-core ≥0.4.0、
  tiktoken、einops、packaging。

### 已知坑（每条都有对应工程处置）

1. **modeling_kimi 强制 `_attn_implementation="flash_attention_2"`**（`__init__`
   无条件覆盖，警告后照写）→ 无 flash-attn 环境首前向即炸。处置：
   `kload.install_kimi_mla_sdpa_shim()` 把注册表条目换成 SDPA 等价实现
   （4D additive causal mask 直接作 attn_mask，数学等价；进程内，不改文件）。
   fingerprint 记实际后端，双臂同后端。
2. transformers v5 `_tied_weights_keys` dict 化雷 → pin `<5`。
3. fla chunk 约束：序列长须为 64 的倍数 → 所有仪器 `--max-tokens` 强制校验。
4. 双卡聚合：`device_map="auto"`（accelerate），98G BF16 拆两卡；
   `--max-memory 0:70GiB,1:70GiB` 可约束。

## 6. 三件仪器（+ 手术件）用法

权重落位 `/root/autodl-tmp/models/Kimi-Linear-48B-A3B-Base/` 后：

```bash
REPO=/root/autodl-tmp/FLUED          # 或部署快照 code/ 目录
MODEL=/root/autodl-tmp/models/Kimi-Linear-48B-A3B-Base
CORP=/root/autodl-tmp/corpus/corpus_v3.txt

# ① 必要性账（输入侧遮蔽 + 簇级同体半分对照；行为侧）
python $REPO/tools/analysis/v3_6/probe_kimi_linear_book.py \
  --model-path $MODEL --corpus $CORP --n-windows 40 --device cuda \
  --max-memory 0:70GiB,1:70GiB --out-dir /root/autodl-tmp/outputs/kimi_book_smoke

# ② 闭式读出（KDA 边界态 ridge 探针；表示侧；全 20 层单 pass ≈27G CPU RAM）
python $REPO/tools/analysis/v3_6/probe_kimi_linear_state_readout.py \
  --model-path $MODEL --corpus $CORP --n-windows 40 --device cuda \
  --max-memory 0:70GiB,1:70GiB --out-dir /root/autodl-tmp/outputs/kimi_readout_smoke

# ③ KDA 状态置零解离（局部/长程；手术级）
python $REPO/tools/analysis/v3_6/probe_kimi_linear_state_surgery.py \
  --model-path $MODEL --corpus $CORP --n-windows 40 --device cuda \
  --max-memory 0:70GiB,1:70GiB --out-dir /root/autodl-tmp/outputs/kimi_surgery_smoke
```

长作业一律 `setsid nohup … &`。判词纪律：体制判词一律「同机同 env 内成立」
（AGENTS 坑 11/12）；跨模型只比方向不比绝对值。

## 7. 无卡阶段检查单（本次已完成）

- [x] 四仪器模块 + 部署件 scp 到 `/root/kimi_linear_deploy/{code,ref}/`
- [x] 远端 `python -m py_compile` 语法级冒烟全绿
- [ ] 装依赖（§4，无卡可做）
- [ ] 等权重落位（§3 决策）→ 换卡后先 `--n-windows 2 --device cpu`（小窗）或
      直接 GPU 冒烟 `--n-windows 2`，再开 40 窗

## 8. ref/ 清单（git blob sha1，HF MANIFEST 对上）

| 文件 | sha1 |
|---|---|
| config.json | 912298398b14894fa1bb5e858e3d788e060204c0 |
| configuration_kimi.py | 2d66544ae84b3c22b5ec88da2ef3843089198ddd |
| modeling_kimi.py | 4f296a216c45d2569392eab34b3ac54018e46eec |
| tokenization_kimi.py | 4ed6d54161322844166fd114ec77d5e07202c2c0 |
| tokenizer_config.json | 8bfc1efdf0d93e143c98d7bf1199f4aad326c10b |
| special_tokens_map.json | f5b5c7742464f515c7d3c42d70fa7f18f080207b |
| generation_config.json | df17c871d59dbbbcaf3dd50b9df2e5c840e5ab88 |
