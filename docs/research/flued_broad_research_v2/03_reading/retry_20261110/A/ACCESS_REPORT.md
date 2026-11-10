# A组原文重试获取报告

日期：2026-11-10（Asia/Shanghai）。范围仅为 ACCESS_HANDOFF 表01–06，即 BR-R2-T01..T06，占17篇待获取官方原文中的6篇。**本轮新增真实官方原文0/6，新增公开预印本0，新增全文阅读0。** 不是恢复整个研究任务，也不是17篇的合并成功率。

交接清单：[manifest.json](manifest.json)。本目录仅有该清单与本报告，没有PDF、派生正文或错误页伪装成的PDF。terra 应读该清单了解阻塞；**本组没有新取得的原文可交付其阅读**。原有三个公开版本已由先前读者完成版本限定的 FULL（全文阅读）卡，本轮不重复认领。

## 依据和边界

先读 `05_review/ACCESS_HANDOFF.md` 与 `ACCESS_DIAGNOSTIC.md`；六篇标题、论坛、内容引用PDF链接直接取自 `05_review/source_staging/R3_manifest.json`，不猜作者、不反推匿名身份。官方元数据仍标为2026-11-09快照；未取得新状态，不推断录用、撤稿或修订历史。note version 2 不是PDF第二版。

`03_reading/_provided/` 实际不存在，因此无用户合法提供文件可核验，未创建该目录。

工具检查确认已有 `/mingw64/bin/curl`、Python、`pdftotext`；`pdfinfo` 不可用，未安装软件。首个本地凭证脚本因引号转义语法错误未发出HTTP请求；改正后仅有下表所记的一次官方内容PDF请求。整理清单时另一次过长内联脚本在解析阶段失败，随后拆分写入成功，没有额外网络请求或临时文件。

## 先行代表请求：官方访问未恢复

| 实际请求 | 观察 | 处理 |
|---|---|---|
| FetchURL `https://openreview.net/forum?id=FXLPTx7osi` | `Complete the check below to continue to OpenReview`；要求完成验证或登录；工具不提供数值HTTP状态 | 只读返回页，不互动验证、不登录 |
| 已有curl GET `https://openreview.net/pdf/009f6f39ae30a457c722ce02faa53ee551f4b3b2.pdf` | 2026-11-10 03:10:55.345546至03:10:56.013220 UTC；curl退出0但HTTP403；TLS验证结果0；proxy_used=0；无跳转；12,692字节 `text/html`，不是PDF | 不保留错误页。渲染文字为 `Error 403 / Access to this page is restricted. Please check that you are logged in to OpenReview and try again.` |
| 精确标题查询返回的官方定位链接，经FetchURL `https://openreview.net/pdf?id=FXLPTx7osi` | 同一验证页，不是PDF正文；数值HTTP状态未暴露 | 到此停止同类官方路径探测 |

403正文SHA256：`a2d811e0d24af89d9bd4b19cc9e8fbc474c67ef3827648550a6560eca2a5e332`，仅为失败响应凭证，不是论文哈希。`%PDF-` 与尾部 `%%EOF` 均不成立。curl成功退出不等于获取成功。通用403不能单独区分每篇论文权限与验证层原因；论坛/定位链接明确要求验证，足以触发本轮同类路径停试规则。

**本轮没有逐篇重发T02–T06的官方PDF，也未重试官方API。** 每篇未试原因在下表和清单单独登记，不能把代表403冒称为其各自的新HTTP实测。此前六篇逐篇403仅引用旧ACCESS_HANDOFF/P17记录。没有降低TLS或吊销检查、改代理、轮换身份、绕过验证码/登录墙。

## 逐篇去向与缺口

| 编号 | 精确官方标题 / 论坛 | 本轮实际动作或未试原因 | 结果与剩余缺口 |
|---|---|---|---|
| T01 | Tokenization with Formal Guarantees: From Optimal Compression to Provable Bounds / `FXLPTx7osi` | 官方代表PDF、论坛及定位链接实际尝试；普通公开精确完整标题查询 | 官方403/验证；查询返回同一官方定位链接与第三方主题索引，未建立合法独立全文 |
| T02 | Stochasticity in Tokenization Improves Robustness / `rIRkUxOleG` | 官方同类路径因代表验证墙停止；已有2604.16037v1只读核验，不重复下载 | 官方正文未取得。公开标题用Tokenisation而非Tokenization；全文版本相等性、官方附件仍未知 |
| T03 | Online Tokenization with Optimal Delay in Near Linear Time / `8D7l5sK3YT` | 官方同类路径停试；已有2610.19139v1只读核验，不重复下载 | 官方正文未取得。公开标题是Linear Time，官方是Near Linear Time；不能强行当作同版 |
| T04 | Tokenization Invariance Is Learned Late and Broken at the Head / `63kZK7oyd6` | 官方同类路径停试；普通公开精确完整标题查询；FetchURL与内置浏览器检查第三方标题命中页 | 仅索引/聚合页；未取得合法替代全文 |
| T05 | Cross-Tokenizer On-Policy Distillation via Byte-Prefix Marginalization / `Mm5OLOPLT0` | 官方同类路径停试；已有2607.22334v1只读核验，不重复下载 | 同标题不证明官方稿与公开v1逐页一致；官方附件与修订关系未知 |
| T06 | B-Net: Learning Where to Compress in Byte-Level Language Models / `fMymbXoq9T` | 官方同类路径停试；普通公开精确完整标题查询；第三方主题索引FetchURL网络失败后普通curl重试一次 | 索引HTML可取但未发现OpenReview/arXiv链接，非论文；未取得替代全文 |

六篇精确官方PDF URL、原论坛、旧元数据快照、本轮尝试/未试原因都在清单逐项保存。T02/T03/T05已有合法公开版本，故没有浪费流量重下v1，也没有把公开版命名成官方稿。

### 普通公开替代来源检查

三个WebSearch查询均为表中T01/T04/T06完整标题加双引号，未使用作者名；完整查询和相关结果URL见清单。负面结果只代表本轮有界检索未找到，不证明合法公开副本不存在。

- T01：结果包括 `https://openreview.net/pdf?id=FXLPTx7osi` 与 `https://dag.snu.ac.kr/paper_search/links?label=task&norm=tokenization`。前者实际FetchURL仍是验证页；第三方主题索引不是独立论文，不将搜索摘要算全文。
- T04：结果包括同一SNU主题索引与 `https://acceptodds.com/papers/iclr2027-26364`。FetchURL只返回标题、站点名和社交链接。内置浏览器文档元素检查只有社交链接、通用元素、站点安全版按钮、邮件链接，未出现论文下载来源；未按按钮。站点预测不作为录用或学术证据。仅关闭本轮新建页，其他157页未动；大量标签会使侧栏拥挤，但未为整理标签更改用户状态。
- T06：结果仅相应主题/指标索引及不相干论文。实际访问 `https://dag.snu.ac.kr/paper_search/links?label=method&norm=tokenizer` 时FetchURL报告网络错误；一次正常curl重试于03:13:33.698412 UTC结束，退出0、HTTP200、TLS0、proxy_used=0、11,525字节HTML，无OpenReview/arXiv href。该索引不当作原文，未保存。另一个指标索引没有再请求，因为没有独立全文线索。

## 已有公开版的只读复核：不是新获取

原文件未复制、未修改；解析输出仅留内存。三个PDF的SHA256均与ACCESS_HANDOFF完全相同，均有 `%PDF-`、末尾2KB内 `%%EOF`，已有 `pdftotext -layout -enc UTF-8 <path> -` 均退出0。首页面内空白规范化后的公开版标题均匹配，且有Abstract标记。**这不等于官方摘要对照、不等于读完全文。** 页数依据成功文本提取的换页符统计，未使用不存在的pdfinfo作独立页树校验。

| 公开版本 | 原有项目相对路径（以研究根目录为基准） | 字节 / 文本解析页数 | SHA256 |
|---|---|---|---|
| T02 arXiv2604.16037v1 | `05_review/source_staging/R3_BR-R2-T02__2604.16037v1.pdf` | 705191 / 37 | `cad655df35b4027b157bf5ee1482eb72e9ef490364933b48606b42db1ff13977` |
| T03 arXiv2610.19139v1 | `03_reading/V17/sources/BR-R2-T03__2610.19139v1.pdf` | 1181161 / 58 | `86a4690df7f6a2a38243e157eac56b094047dc01ea155bd12e74212187078ce9` |
| T05 arXiv2607.22334v1 | `03_reading/V17/sources/BR-R2-T05__2607.22334v1.pdf` | 1283527 / 28 | `341d34838d7c76b9ae9449f0ab169cf8d20822be0012297413aaff220b73a949` |

T03解析器有 `Mismatch between font type and embedded font file` 警告，退出码仍为0；该警告已保留，不据此宣称数学符号或复杂表格提取无损。完整阅读仍应以原PDF为准。本轮未读取这些PDF全部内容作科学判断，亦未将作者信息输出或与匿名稿链接。

## 对“读完后判断报告需否补充”的交接

本轮未获得官方原文，不能完成这六篇官方稿的全文阅读、两版全量比较或据此裁定报告“需要/不需要”科学补充。特别是T03标题差异、三份预印本与官方稿的正文差异、六篇的表图/附录/独立补充材料仍未核定。不能用索引摘要、站点预测或原有预印本的FULL状态来抹平这些缺口。

因此仅能登记**访问限制未解除**；不能宣布报告的科学综述无需补充，也不能凭新摘要添加结果判词。旧卡、旧报告和证据注册表均未修改。terra读取本目录清单后可复用原有版本限定卡，但本轮没有待其阅读的新源文件；合法公开访问恢复或用户提供合法官方PDF后，仍须做签名/解析/页数/标题摘要匹配、版本边界与完整性验证，再安排正文阅读和报告补充判断。

## 文件与核验

仅写 `03_reading/retry_20261110/A/manifest.json`、`03_reading/retry_20261110/A/ACCESS_REPORT.md`。没有安装、运行论文代码、提交训练、提交Git、派生代理或写共享文档。无临时下载文件遗留。三个旧PDF只读哈希/解析检查通过，清单JSON结构及六条唯一记录/来源匹配检查通过；项目软件构建和测试不适用于本次获取凭证任务。最终Git状态仅显示原已存在的整棵研究目录等未跟踪项，其他会话的文件未清理或改动。
