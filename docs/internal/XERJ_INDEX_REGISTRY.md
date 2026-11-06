# XERJ 本地索引登记册（2026-10-31 建立）

> AGENTS.md「可选代码检索：XERJ」节的使用前检查②所指登记：本项目语料与查询入口。
> 本文件含本机盘符路径与运维命令，属本地运维记录（docs/internal/），不入匿名镜像。

## 节点（本机，loopback-only）

- 启动：`XERJ_DISABLE_FEEDBACK=true xerj --data-dir ~/xerj-data`（后台常驻；本次 PID 38024）
- ES 端点：`http://localhost:9200`（Elasticsearch wire-compatible）；UI：`http://localhost:8080`
- 绑定默认 127.0.0.1，不出网；TLS/API-key 鉴权默认开启
- API key：`~/xerj-data/admin.key`（repo 外文件；引用路径即可，**永不打印/入册/入 commit**）
- 纪律：一切 xerj 调用带 `XERJ_DISABLE_FEEDBACK=true`（AGENTS.md 边界条款禁自动 field report）；
  纯本地 BM25+keyword（`--no-semantic`，未启用任何嵌入模型/外部服务）
- 同机另有他人节点（PID 40816，端口 9320-9322，data 在他项目树下）——**互不混写**，
  本项目一切读写走 9200。

## 语料（7 前缀，源版本 git `c99864c`，建账 2026-10-31）

| 前缀（索引模式） | 源目录 | 覆盖 | 记录数 | 排除 |
|---|---|---|---|---|
| `flued-*` | `flued/` | 25 文件 | 448 | __pycache__（内建） |
| `tools-*` | `tools/` | 290 文件 | 3846 | `tools/.xerjignore`：data/evacuator/（166M 备份）、baselines/bpe_baseline_standalone/checkpoints/（3.4G 权重） |
| `tests-*` | `tests/` | 78 文件 | 1375 | __pycache__；1 fixture 判 junk（正常） |
| `configs-*` | `configs/` | 79 文件 | 193 | — |
| `docs-*` | `docs/` | 130 文件 | 1439 | —（audit docx/pdf 在本地索引内，仍不入镜像） |
| `experiments-*` | `experiments/` | 6 文件 | 64 | — |
| `flashkda-*` | `FlashKDA/` | 25 文件 | 184 | `FlashKDA/.xerjignore`：/cutlass/（vendored 82M）、/build/、/flash_kda.egg-info/ |

**不入索引**：checkpoints/、outputs/、results/、.git、语料盘（P:/F: 全部世代）——
模型权重、运行日志、曲线产物、语料按纪律一概排除。repo 根散件（README/AGENTS.md/pyproject）未编目，直接读。

## 查询入口与字段图

- 入口：`POST http://localhost:9200/<模式>/_search`（多索引用**逗号列表** `flued-*,docs-*`，勿用 alias）；
  header `Authorization: ApiKey $XERJ_API_KEY`。
- 字段图（代码为**符号级**记录）：
  - `body`：prose/文档正文（docs/configs 等）
  - `code`：符号签名行；`impl`：符号全文；`name`/`kind`：符号名与类别
  - `path`（文件名）/`ax_path`（repo 相对路径）/`start_line`-`end_line`/`line`
- **标识符检索用 `match` / `query_string`，勿用跨标点的 `match_phrase`**——
  code 分析器切 snake_case 且标点处有位置间隙（实测："diag_eye" phrase 0 命中、
  match 13 命中，top 命中 v36/model.py forward:1766-1891）。
- 册览：`xerj autoindex map --url http://localhost:9200`（子节：`--dataset <slug>`）。

## 维护

- 维护者=主会话 AI；其他会话/agent 默认只读查询。
- 重索引（源码变更后）：`XERJ_DISABLE_FEEDBACK=true xerj autoindex <目录> --url http://localhost:9200 --prefix <前缀> --no-semantic --no-graph --code-analyzer code`
  （幂等；大改后加 `--fresh`）。合并/切版本后由维护者增量更新。
- 排除契约：`tools/.xerjignore`、`FlashKDA/.xerjignore`（未 commit，随登记册同批处置）。
- 多 agent 共用：只传本册路径+前缀清单，不转发检索原文。
