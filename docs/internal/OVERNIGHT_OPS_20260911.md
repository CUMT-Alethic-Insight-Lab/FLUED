# OVERNIGHT OPS 2026-09-11/12（夜班操作手册）

> 用途：cron 触发时按指引用节执行。用户已授权先斩后奏（09-12 晚续期：**有效期至 09-13 中午**）。
> 自主权边界：判词裁定（密度闸门掉线、DeltaNet 分支定性）一律停下等用户。
> **09-12 注**：§B/§C/§D 为 09-11 夜旧机（47807/42166 已失效）历史记录；卡A 内容已克隆至新双卡机 A79（15970），语料/150M 三 seed 基座已在数据盘验证副本。今晚现役链 = §A + §H。

## §A E124 收官+四列点火（cron :13）

1. ssh -i ~/.ssh/flued_partner_ed25519 -p 60222 root@106.15.75.26：`ps -p 37725 -o pid,etime --no-headers` + `wc -l < /workspace/outputs/e124_mask_log_seed42.jsonl`。未到 10000 → 简报一句结束。
2. 到 10000 → scp 拉回 `/workspace/outputs/e124_mask_log_seed42.jsonl` → 本地 `outputs/e124_mask_log_seed42.jsonl`（串行重试）。
3. sha256 登记 + 末窗字段审计（cand_mode=random / cand_seed=20260911 / candidates / hw 含 4090）。
4. **密度闸门**：python 读本地 jsonl，逐窗 sum 被遮 chunk 字节数取均值。≥54.8 → 进 5；<54.8 → 停下报用户（剂量重裁是用户权）。
5. 四列串行点火（先 `nvidia-smi` + 进程查重）：写 outputs/_e124_ignite_4cols.sh，逐列：
   `PYTHONUTF8=1 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 "C:/Users/74090/Miniconda3/envs/kda-kernels/python.exe" -X utf8 tools/train/v3_6/train_v36_s1.py --config configs/v3_7_e124_<COL>.json`
   顺序 comb → gate → demand → cont；Bash run_in_background + disable_timeout 起脚本；列间确认上列 latest.pt + train_log 收官行。
6. 换岗：本 cron 改监控四列（train_log 尾 + 零 NaN + acc 水位 + 进程/GPU）；NaN/回落>2pp/进程死才报用户。
7. 异常：进程死且行数<10000 → 查 /workspace/outputs/e124_mask_log_seed42.log 尾部，坑9纪律重跑（从 0），报用户。
8. 四列收官 → 跑五仪表判读雏形（RD 曲线/k_rows 置乱/位置先验/遮蔽位读出/定向消融），读数原样报用户，判词留白。

## §B 卡A语料（cron :53）

1. ssh -p 47807：stat 大小（目标 23777636695）+ grep DD_EXIT corpus_transfer2.log + dd 进程。在传→简报。
2. 完成 → 卡A sha256sum 全量 + 4090（-p 60222）sha256 /workspace/corpus/corpus_v3.txt；一致 → 写 `VERIFIED.sha256`（150M 链要看）+ 删卡A /root/.ssh/tmp_pull_key；查卡B（-p 42166）：未完→留 4090 授权与本地 ~/.ssh/tmp_h800_pull_key*，删本 cron；也完→三侧销毁（4090 authorized_keys 删 tmp-h800-pull-20260911 行 + 本地私钥删）+删卡B cron，报收官。
3. 死且不足：truncate 1MiB 边界 + dd skip=seek 重续（授权被误撤先重新授权回 4090）。

## §C 卡B语料（cron :57）

同 §B 流程，端口 42166、日志 corpus_transfer.log、对侧查 47807。卡B收官报「卡B全量就绪」。

## §D 卡A 150M 链（cron :31）——监控相位（09-11 23:59 换岗）

状态：seed42 收官（dacc 0.3517）；seed1 收官（20000 步，loss 5.04，dacc 0.3367，零 NaN，~04:57）；**seed2 已点火（pid 27271，~05:33，ETA ~07:55）**。三 seed 收官后链完。

每轮：
1. ssh -p 47807：`tail -1 /root/autodl-tmp/checkpoints/v37ks_a_im_v373_scale3x_20k_ctx4096_20260911_s2/train_log.jsonl`（nan_skips=0 且 loss 降）+ `ps -p 27271`。健在→简报一句。
2. seed2 收官（进程退+_s2/summary.json 在）→ 三 seed 齐，读数原样报用户（判词留白），本链完。
3. 异常：NaN/loss 爆炸（predict_loss 上千=4x@2e-4 前科形态）/进程死且步数<20000 → 停下报用户，不硬修。
4. 三 seed 全收官→读数原样报用户（codec/direct_acc/predict_cos 七碑），判词留白。

（历史：第 1-5 步已执行——VERIFIED 核验、bundle 同步卡A repo 至 fa1554f、remote 配置三枚、bpe tokenizer 补传 sha256 对拍、冒烟与点火。）

## §E 卡B 复证臂队列（无 cron，subagent 线）

- 500 窗必要性账：已收官（见 changelog 09-11 晚四）。
- 正对照 transformer-340M：已收官强阳 +0.3331（晚五）。
- 闭式读出探针 500 窗：已收官（晚五，24/24 层均匀显著）。
- 卡B 之后无排队任务 → 早晨报用户时建议关机省钱（余额跑道见 §G）。

## §F 纪律速查

- 删除先报后批；凭证不落盘不落册；setsid nohup 起长作业；串行 scp；同臂锁单机。
- GitHub 断连：push 失败挂兜底 cron（推成自删）。
- 证据表编辑后核 `grep -c "^| E[0-9]* |" docs/CURRENT_STATE.md` = 123。

## §G 预算账（2026-09-11 21:02 快照）

- AutoDL：余额 ¥204.73，双卡烧速 ¥13.96/h → 跑道至 ~09-12 11:40。
- 卡A 计划：~23:30 点火 seed42（2-4h）→ seed1 → seed2 串行；seed2 可能撞上余额见底（ckpt_every=1000 兜底，损失可控）。
- 卡B：agent-203 冒烟后无任务 → 建议用户早上下手动关机（省 ~¥7/h 延卡A跑道）；我无法远程关停计费。
- Kimi Code 额度：7 天 49.53%（09-13 夜重置）——cron 提示词已瘦身，subagent 优先于主会话长操作。

## §H 15970 挂双卡 + Kimi Linear 复证臂链（cron :47，09-12 夜新增）

背景：A79 机（实例 56e9nt826x-29a8cae7，当前**无卡模式**运行中）数据盘在收 98G 权重（本地任务 bash-wlrbwa52，日志 `outputs/_kimi_linear_download/ul.log`，成功标志 `KIMI_LINEAR_BASE_UPLOAD_VERIFIED`）。**上传未完绝不关机**（scp 断点续传但白烧时间）。

状态机（每轮推进一格，逐格验证）：

1. **等上传**：`tail -5 outputs/_kimi_linear_download/ul.log`。无 VERIFIED → 简报一句结束。
2. **挂卡**（webbridge，daemon http://127.0.0.1:10086，session=`autodl-gpu-attach`，Windows 下请求体一律写临时 json 文件用 `curl.exe --data-binary` 发，非 ASCII 禁内联）：
   a. find_tab url=https://www.autodl.com/console/instance/list（不在则 navigate newTab:true）→ snapshot。
   b. 找 A79机/56e9nt826x 行的「关机」按钮（09-12 21:40 快照为 @e22，**以实时快照为准**）→ click → 确认弹窗点确认 → 轮询 snapshot 至状态「已关机」（1-3 min）。
   c. 点该行「开机」（普通开机=带卡；**绝不点 更多→无卡模式开机**）→ 轮询至「运行中」且无「无卡模式」标（3-8 min）。
   d. snapshot 读该行新 SSH 登录指令（**端口重启后可能变**）→ 用新端口探活：`ssh -o BatchMode=yes -o ConnectTimeout=15 -p <PORT> root@connect.westd.seetacloud.com "hostname; nvidia-smi -L"`（key auth 已装）。盼：2× RTX PRO 6000。
3. **冒烟**：ssh 进 `/root/kimi_linear_deploy`，按其 README/脚本跑装载+前向+哨兵首验（transformers 4.57.x 环境在机；权重 `/root/autodl-tmp/models/Kimi-Linear-48B-A3B-Base/`；双卡 device_map）。冒烟任何一灯不绿 → 停下报用户，不硬修。
4. **点火必要性账**：冒烟全绿 → setsid nohup 起三探针第一发（必要性账，复证臂最高优先），产物落数据盘（系统盘只有 30G），登记 pid+log 路径。
5. 换岗：本 cron 此后转监控探针（log 尾+进程+显存）；探针收官 → 读数原样报用户（判词留白）→ **关机回无卡模式**（webbridge 同法）→ 删本 cron。
6. 余额纪律：挂卡后烧 ¥13.97/h；若探针无法过夜跑（如冒烟红灯待修），**当晚关机回无卡模式**，不空烧。

预算快照（09-12 21:40 估）：余额 ~¥190；挂卡 9h ≈ ¥126，明早余 ~¥60+，够烧到 09-13 午。
