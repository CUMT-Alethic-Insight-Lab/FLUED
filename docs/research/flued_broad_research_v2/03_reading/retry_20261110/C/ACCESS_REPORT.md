# C组：六篇官方原文有界重试

日期：2026-11-10（Asia/Shanghai）。范围仅为 `ACCESS_HANDOFF.md` 表12–17，V02、V04、V13、V14、V22、V25；属于17篇总任务中的6篇，不代表其余11篇的本轮结果。

## 结果与交接

- **新取得官方原文0/6，另获公开预印本0，新增完整阅读0。** 六个确切官方PDF地址本轮各请求一次，均为HTTP403 HTML错误页，不是PDF。
- 先读 `05_review/ACCESS_HANDOFF.md` 和 `ACCESS_DIAGNOSTIC.md`，并核对 `05_review/source_staging/R3_manifest.json` 中这六条官方标题、论坛ID、PDF内容引用；未猜测稿件或作者身份。
- 完整机器凭证：[manifest.json](manifest.json)。terra需要核对此清单的阻塞和缺口，**本组没有待全文阅读的新PDF/text**。`summary.terra_new_fulltext_queue` 是空数组。
- 本轮不能完成“读完六篇后判断科学报告是否需补充”：真实原文仍未取得，正文、对照、表图、附录均未阅读。没有基于新全文的科学补充依据，也不能据此宣布“不需补充”。既有报告的来源/版本限制应继续保留；旧卡、旧报告、注册表均未改。

## 代表检查与停止边界

先以FetchURL访问：

1. `https://openreview.net/forum?id=UUldzWxIL4`
2. `https://openreview.net/pdf/9c64cd9b8b1bba44c1ff65945bd6c1a02ed98a9d.pdf`

两者提取文本均为“Complete the check below to continue to OpenReview / Please complete the verification above / Sign in to skip this check”。FetchURL未提供HTTP状态，不能把它编造成HTTP200或403。未操作验证码或登录入口。

随后使用已存在的 `/mingw64/bin/curl`，依照访问诊断中正常可用方式，对**六个不同的确切官方内容引用各做一次GET**。不重复同一403请求，不尝试其他PDF形状、登录、challenge端点或身份切换。此举只为逐篇形成实际凭证，不是宣称验证墙恢复。其余论坛/locator/direct-note/API没有逐篇重探，原因是代表页面明确验证要求，且各自PDF已经返回一致拒绝。

所有curl请求保持默认信任、证书/吊销验证及代理设置，限制HTTPS和HTTPS重定向，连接上限15秒、总时限60秒；未使用`--fail`，以便在内存检查错误响应。因此curl退出0仅代表完成HTTP交换，**不等于下载成功**。无TLS/代理规避、软件安装、论文代码执行或训练。

## 六篇官方请求逐项结果

下列每条均为本轮实际GET，不是沿用昨日尝试：

|表行 / ID|确切官方标题 / 论坛|确切官方PDF|结果|
|---|---|---|---|
|12 / V02|Linear Attention lacks Incentive for Associative Recall, not Capacity；[UUldzWxIL4](https://openreview.net/forum?id=UUldzWxIL4)|https://openreview.net/pdf/9c64cd9b8b1bba44c1ff65945bd6c1a02ed98a9d.pdf|HTTP403；HTML；未取得|
|13 / V04|SDG: State-Dependent Gating at Chunk Boundaries for Linear Attention；[lYWcLB1rAh](https://openreview.net/forum?id=lYWcLB1rAh)|https://openreview.net/pdf/a6be3de5a7a112d8d9971f44d46409d02e29d0aa.pdf|HTTP403；HTML；未取得|
|14 / V13|Cross-Model Stitching Transfers Answers, Not Computation；[98Rbm5C5Bl](https://openreview.net/forum?id=98Rbm5C5Bl)|https://openreview.net/pdf/292012e3cebcb326c132293eb93d41f533bf95d3.pdf|HTTP403；HTML；未取得|
|15 / V14|Receiver State Shapes Functional Compatibility: Internal Message Adaptation for Model Stitching；[2M4nt7AFuD](https://openreview.net/forum?id=2M4nt7AFuD)|https://openreview.net/pdf/b167a621df8f120088cda7baa7cccfcbfd226cd7.pdf|HTTP403；HTML；未取得|
|16 / V22|When Routing Must Be Right: Irreversible Lock-In in Attention Routing；[9vT48Lms48](https://openreview.net/forum?id=9vT48Lms48)|https://openreview.net/pdf/4b049a14ede5c22389997afeb1b72a99e81a7de5.pdf|HTTP403；HTML；未取得|
|17 / V25|Understanding the Predictive-State Bottlenecks of Transformer Models；[58JxyfvZJj](https://openreview.net/forum?id=58JxyfvZJj)|https://openreview.net/pdf/3df135438f55aa7adaea9da322f21607da69a080.pdf|HTTP403；HTML；未取得|

六次均curl退出0、`ssl_verify_result=0`、`proxy_used=0`、重定向0，`content_type=text/html`，响应12,692字节，标题`Error 403 | OpenReview`，可见错误为“Access to this page is restricted. Please check that you are logged in to OpenReview and try again.”。每次请求的UTC时间、确切请求/最终地址和错误响应SHA256分别记录在manifest的`papers[].attempts[]`；六个错误页SHA256均为：

`a2d811e0d24af89d9bd4b19cc9e8fbc474c67ef3827648550a6560eca2a5e332`

这是**HTML错误体哈希，不是原文PDF哈希**。没有保存错误页假扮PDF；不能从通用403确定每篇的具体访问控制原因，验证层与稿件权限原因尚未区分。

## 合法公开替代版检索

- 内置浏览器按V02完整标题加引号检索，`browser.create_tab(query)`返回`NAVIGATION_FAILED / ERR_CONNECTION_CLOSED`。恢复该已创建标签的控制后，做一次普通网络重试，仍为同一错误。中间一次`TAB_NOT_ACTIVE`是控制操作失败，没有发出检索请求，不计第三次网络尝试。未换代理、身份或浏览器。其余五篇不在同一已坏的浏览器搜索线路连续重试。
- 六篇分别通过**官方arXiv公开API**按完整精确标题查询，`start=0&max_results=5`；每次curl退出0、HTTP200、TLS验证0、`proxy_used=0`，XML解析成功，`totalResults=0`且条目为空。完整查询URL、参数、UTC日期及响应SHA256见`public_searches`。这是六个实际独立查询，不是将一个失败推广成六个阴性结果。
- 该有界零命中不能证明其他合法公开副本不存在，亦未遍历作者网站。未反推匿名作者，未用近题旧论文替代，未把搜索结果或摘要当正文。
- 已有三份T02/T03/T05预印本均不属于本C组，未重下载、复制或计作新增官方原文。官方版与公开预印本取得数分别为0和0。

## 文件完整性、版本与阅读缺口

- `03_reading/_provided/` 在检查时不存在，没有可核验的合法用户文件；没有自行创建它。
- 六个收到的响应均无`%PDF-`签名，也无末尾`%%EOF`，在PDF入口前即被拒绝。因此没有可运行的PDF解析对象、页数、第一页标题或PDF摘要，manifest对应字段为null/未运行，**不是通过验证**。现有`pdftotext`已经确认可定位，`pdfinfo`不在PATH；没有安装替代工具，因为根本未取得PDF。
- 官方标题/URL只匹配昨日R3元数据快照；本轮未取得新的官方正文、状态或决议。`note_version=2`不解释为PDF稿件v2，不推断录用或稿件修订关系。
- 全文、图表、证明、附录、独立补充文件及任何公开版/官方版等同性仍未知。没有FULL（完整阅读并检查决定性图表/附录）声明；没有新全文可供判断报告是否需实质补充。

## 本次落盘与校验

只在`docs/research/flued_broad_research_v2/03_reading/retry_20261110/C/`新增：

1. `manifest.json`：六条元数据快照、六次官方PDF响应凭证、六次arXiv查询、代表FetchURL与浏览器失败、验证缺口和terra队列。
2. `ACCESS_REPORT.md`：本报告。

没有新增PDF/text，因为没有取得真实全文；原始错误体仅内存检查，无临时/partial文件。校验包括JSON解析、六个唯一ID及12–17行号、标题/论坛/URL对只读R3源的一致性、六次403非PDF和六次arXiv200零条目的计数、输出目录仅这两个文件、严格UTF-8与尾随空白检查，以及Git状态。源码构建、软件测试不适用于本次访问凭证交付；未运行。未提交、更改系统设置、派生代理或修改任何旧卡/旧报告。
