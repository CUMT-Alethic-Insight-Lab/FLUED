#!/bin/bash
# R3 丙臂判决账编排（500 窗×4 块+池化；同卷构成：种子 424242 选择链 / 424243 池化，
# 与 R2 母列收官同窗集同选择链同计分位；仪器本体零口径改动，仅启动器装载/计划注入）。
# 5080 本地 env：kda-kernels python（-X utf8），GPU 串行逐块。
set -e
PY=C:/Users/74090/Miniconda3/envs/kda-kernels/python.exe
MODEL=outputs/r3_transplant_vtile_20260914/main20k_vtile/latest
CORPUS=P:/FLUED_corpus/corpus_v3/corpus_v3.txt
OUT=outputs/r3_transplant_vtile_20260914
for b in 0 1 2 3; do
  s=$((b*500))
  echo "[verdict] block $b start-window $s $(date +%H:%M:%S)"
  OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 $PY -X utf8 \
    tools/baselines/deltanet_r2/probe_r3_vtile_book.py \
    --model-path $MODEL --corpus $CORPUS --n-windows 500 --start-window $s \
    --seed 424242 --device cuda --out-dir $OUT/verdict_b$b > $OUT/verdict_b$b.log 2>&1
  echo "[verdict] block $b done $(date +%H:%M:%S)"
done
$PY -X utf8 tools/baselines/deltanet_r2/pool_necessity_blocks.py \
  --blocks $OUT/verdict_b0 $OUT/verdict_b1 $OUT/verdict_b2 $OUT/verdict_b3 \
  --out $OUT/necessity_pooled_seen.json > $OUT/pool.log 2>&1
echo "[verdict] pooled -> $OUT/necessity_pooled_seen.json"
