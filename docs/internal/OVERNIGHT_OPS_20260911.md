# OVERNIGHT OPS 2026-09-11（夜班操作手册）

> 用途：cron 触发时按指引用节执行。用户已授权先斩后奏（有效期至 09-12 中午）。
> 自主权边界：判词裁定（密度闸门掉线、DeltaNet 分支定性）一律停下等用户。

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
