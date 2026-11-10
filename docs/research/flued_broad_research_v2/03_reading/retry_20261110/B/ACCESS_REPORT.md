# B组：17篇原文重试中的07–11（2026-11-10）

## 结果与交接

**本组5篇：新增取得官方原文0/5，新增合法公开预印本0/5，新增全文阅读0篇。** 这是17篇任务中的B组结果，不代表其他12篇。没有可交terra立即阅读的新PDF；本组确切交接清单为[manifest.json](manifest.json)。原文获取仍未完成，不能据此判断科学报告“不需补充”。必须取得并核验真实正文后，再由terra阅读并判断补充点。

仅新建本目录中的`manifest.json`和本报告；没有改动旧卡、旧报告、05_review材料、共享注册表或生产代码。未恢复完整goal，没有安装软件、运行论文代码、提交训练、派生代理或提交Git。三篇已存在的其他预印本未下载、未复制、未计作新原文。

## 先决核对

- 先读`05_review/ACCESS_HANDOFF.md`及`05_review/ACCESS_DIAGNOSTIC.md`；标题、论坛与PDF引用逐项来自既有`05_review/source_staging/R3_manifest.json`，不猜ID或作者。
- 检查用户文件目录`03_reading/_provided/`：本次不存在，无可核验的用户供应文件；不预设已有文件。
- `which curl`找到既有`/mingw64/bin/curl`；Python环境已有`pypdf`和`fitz`。没有安装或更新任何依赖。
- 全程普通公开HTTPS，保留证书验证与既有网络默认，不导入会话、凭据，不修改代理、信任或身份，不解验证码、不绕登录墙。官方元数据是2026-11-09历史快照，未冒充今日状态或接收决定；note version 2不代表PDF第二版。

## 当前代表官方路径：没有恢复

首先用FetchURL分别请求V11论坛和精确PDF引用：

- `https://openreview.net/forum?id=xzOnjQHMr9`
- `https://openreview.net/pdf/88de0a6529e8f9fe919aa650e754de9ca6b897a5.pdf`

两者均提取到“Complete the check below to continue to OpenReview / Please complete the verification above / Sign in to skip this check”。FetchURL没有暴露HTTP码，不能把它的工具成功当作PDF成功。

另按既有诊断推荐，用正常curl对**同一代表PDF**进行一次客户端接入核对，而非验证交互：UTC `2026-11-10T03:10:38.209759+00:00`，curl exit **0**，HTTP **403**，`text/html`，**12,692字节**，`ssl_verify_result=0`，`proxy_used=0`，无重定向。正文是“Error 403 / Access to this page is restricted. Please check that you are logged in to OpenReview and try again”。既无`%PDF-`，也无尾部`%%EOF`；没有保存伪PDF。该HTML响应SHA-256为`a2d811e0d24af89d9bd4b19cc9e8fbc474c67ef3827648550a6560eca2a5e332`，**这是错误页响应哈希，不是论文哈希**。

明确当前同类验证/受限响应后停止官方同类重试。没有逐篇重复其他四个PDF、论坛或direct-note API，更没有将V11的403虚报为其他四篇的今日实测HTTP码。它们各自的未试原因均写入清单。过去V24的`ChallengeRequiredError`仍只是既有记录，本次不声称又取得了它。

## 五篇逐项结果

| 清单号 / key | 确切官方标题 | 论坛 | 今日官方正文动作 | 今日合法副本检索 | 取得 |
|---|---|---|---|---|---|
|07 / V11|LoopLA: Causal State Refinement for Looped Linear Attention|[xzOnjQHMr9](https://openreview.net/forum?id=xzOnjQHMr9)|代表论坛/PDF FetchURL验证页；精确PDF curl403 HTML|内置浏览器精确标题检索失败，一次普通重载；另作Bing与Google精确标题FetchURL检索|0|
|08 / V16|Farsighted Correction of Shortcut Learning: From Dynamic Starvation to Confidence-Gap Optimization|[JrKJaRbQpz](https://openreview.net/forum?id=JrKJaRbQpz)|未个别重复：V11当前同类验证/受限已触发停止规则|内置浏览器精确标题检索实际失败；另作Bing与Google精确标题FetchURL检索|0|
|09 / V20|Exact Finite-Query KV Cache Compilation|[OQhOBMNVeN](https://openreview.net/forum?id=OQhOBMNVeN)|未个别重复：同上|Bing与Google精确标题FetchURL检索；浏览器已连续关闭连接，不再逐项重试|0|
|10 / V21|Where You Put Attention Matters More Than How Much You Use: Attention Placement in Hybrid Sequence Models|[0fPxp7a50O](https://openreview.net/forum?id=0fPxp7a50O)|未个别重复：同上|Bing与Google精确标题FetchURL检索；浏览器未个别请求原因同上|0|
|11 / V24|Predictive State Has a Scope|[uILf1c6VDo](https://openreview.net/forum?id=uILf1c6VDo)|未个别重复：同上；没有重复已知验证API|Bing与Google精确标题FetchURL检索；浏览器未个别请求原因同上|0|

五个精确PDF URL、论坛、历史官方元数据和逐篇检索URL全部保留在`manifest.json`的`entries`，不是只给关键词让后续人猜路径。

## 检索接入局限：不能解释成“没有公开副本”

按当前浏览器指示先使用Kimi Code Desktop内置浏览器：V11精确标题新建检索页得到`NAVIGATION_FAILED / ERR_CONNECTION_CLOSED`；一次普通重载后等待25秒超时，后续状态仍为`ERR_CONNECTION_CLOSED`。V16第一次控制动作因`TAB_NOT_ACTIVE`被拒绝，未发出搜索请求；选回本组页后实际精确检索仍是`ERR_CONNECTION_CLOSED`。没有把控制错误算作网络请求。其余三篇不继续在同样坏的浏览器通道重复，避免无止境重试；未使用用户Chrome/Edge会话。

随后五篇各用普通公开精确标题URL取得Bing页面，但结果与请求严重不对应：

- V11返回小米股票结果（显示44,700条）；
- V16返回Windows求助结果（About 50 results）；
- V20返回`exact`词典/商业软件结果（107,000条）；
- V21返回`where`词典/公司结果（769,000条）；
- V24返回`predictive`词典/咨询结果（31,800条）。

这些返回不能确证引号查询得到忠实执行，也不是合格的“零命中”，不能证明合法副本不存在。没有跟随无关结果、反推匿名身份或错配其他论文。再对五个完整标题各作一次普通Google公开检索FetchURL请求，均为`Failed to fetch URL due to network error: fetch failed`，没有可用结果；工具没有暴露HTTP码。未将连接错误写成403/404。已有浏览器普通重试及两种公开页面接入记录后停止，不再改代理、证书或身份试探。

## 完整性、版本及阅读状态

真实PDF为0，因此页数、PDF哈希、解析成功、首页标题/摘要与官方元数据逐项匹配均**不可核验**；清单使用`null`/明确不适用，而非伪造通过。原文正文、图表、参考文献、附录、独立补充材料及版本关系仍缺失。正文未取得，没有做正文科学裁定、摘要代全文或“FULL”阅读声明。匿名记录保持匿名，既有公开预印本与官方投稿版严格分开。

本次没有新正文证据，**报告是否应补充仍待定**，不能因为阻塞就宣布五种机制不重要或报告无需增补。terra应先读取本组`manifest.json`的`terra_handoff`和逐篇条目：当前`ready_to_read_pdf_paths=[]`；取得合法文件后再做签名、EOF、解析、页数、标题/摘要及版本核对，之后才进入实际阅读与补充判断。

## 本目录交付核对

最终运行Python标准库校验：JSON可解析；恰好五个指定key且不重复；五组标题、论坛和精确PDF引用与历史官方清单一致；每篇两次公开检索的查询等于带引号的完整标题；三个成功/阅读计数均为0；PDF/text路径及页数为空；目录只有本报告与manifest，无`.part`、伪PDF、脚本或日志。文本严格UTF-8，无行尾空白。检查了Git状态，不删除并发任务或此前已有的未跟踪文件。此为资料接入交付，不涉及软件构建/训练或项目测试；没有以编译替代原文获取验证。
