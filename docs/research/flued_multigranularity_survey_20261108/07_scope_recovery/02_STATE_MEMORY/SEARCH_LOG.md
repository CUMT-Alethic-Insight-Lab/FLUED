# 02_STATE_MEMORY｜公开检索与去重记录

2026-11-08｜sol。只发送公开机制词、公开题名/编号；未发送内部实验、文件正文或项目未公开数字。使用WebSearch、FetchURL及Kimi内置浏览器；未调用数据源、付费接口或外部登录会话。

## 1. 实际查询：8次，不按命中数凑篇数

| 次序 | WebSearch原样查询 | 判别目的 | 实际有用命中与处理 |
|---|---|---|---|
| Q1 | `fast weight programmers delta rule memory capacity correlated keys interference 1992 2021` | 经典加性外积与纠错写入的区别 | W0199，PMLR正式页核作者/题名/摘要；已入未读，不算新增。2508.08435仅为背景综述线索，未核全文、未纳候选 |
| Q2 | `linear recurrent memory capacity learnability associative recall out of distribution query Mamba 2025 2026` | 容量与可学性、长期干扰分离 | Anatomy 2609.16183；官方摘要及§1–6抽读后纳新候选。JRT 2407.05483仅线索，因涉及再读输入的权限，不作为本轮纯状态替代路线主要证据 |
| Q3 | `MIRAS Titans memory retention forgetting gradient surprise 2504.13173` | 遗忘/保持是否只有单一衰减门 | MIRAS原文入口和Google Research官方介绍；仅采用原始arXiv摘要/元数据，未拿博客替代原文；新增候选 |
| Q4 | `associative recall recurrent models unseen keys out of distribution queries "2025" "2026"` | 未见键/查询泛化是否有独立证据 | 重复命中Anatomy；去重不加篇。结果稀疏，没有因此宣称OOD领域为空白 |
| Q5 | `"linear attention" "stability" "delta" "2026" memory` | 稳定写入、主动擦除与遗忘分离 | EDA 2606.26560，后取官方摘要；新增候选。其他仅搜索摘要或二手资料不计原文证据 |
| Q6 | `"HiPPO" "Recurrent Memory" polynomial projections 2020` | 不保存原文的经典时间统计保持路线 | HiPPO 2008.07669，官方摘要/元数据核验；新增候选。现代博客仅导航，不采用其定理解释 |
| Q7 | `"Revisiting Associative Recall in Modern Recurrent Models"` | 有限状态失败是否含学习率/优化混杂 | W0088；重取v2官方摘要，确认主张范围为学习率、宽深与组件；已入未读 |
| Q8 | `"delta rule" "residual" "forgetting" "correlated" memory capacity` | 原特征、误差修正及值侧几何的区别 | W0203 Dual DeltaNet；重取v1官方摘要，已入未读。搜索提及预条件/不确定性路线，但未核对应原文，保持未知，不扩候选数量 |

检索覆盖经典（2020/2021）、反例/优化纠偏（2025/2026）、最新进展（2026-10-28），不是按日期扫描到所有2026论文。未系统检索经典突触模型、终身权重学习、全部状态空间变体或有限精度数值分析；这些不在本轮已覆盖声明内。

## 2. 实际访问：FetchURL 13次尝试

| 序号 | 准确URL／版本 | 结果与实际采用范围 |
|---|---|---|
| F1 | https://proceedings.mlr.press/v139/schlag21a.html | 成功；正式书目、作者、摘要。没有把关联PDF视为已读 |
| F2 | https://arxiv.org/html/2609.16183v1 | 网络terminated，工具报告约376秒；不是403、登录墙或原文不存在 |
| F3 | https://arxiv.org/abs/2504.13173 | 成功；摘要、提交史，原文正文未读 |
| F4 | https://arxiv.org/abs/2008.07669 | 成功；摘要、v1/v2提交史，原文正文未读 |
| F5 | https://arxiv.org/abs/2606.26560 | 成功；作者栏、摘要、v1提交史，原文正文未读 |
| F6 | https://arxiv.org/abs/2508.19029v2 | 成功；摘要、v2 2025-10-10，非全文 |
| F7 | https://arxiv.org/abs/2610.19709v1 | 成功；摘要、v1 2026-10-14，非全文 |
| F8 | https://arxiv.org/abs/2610.38578v1 | 成功；摘要、v1 2026-10-28，非全文 |
| F9 | https://arxiv.org/abs/2412.06464v3 | 成功；摘要、v3 2025-03-06，非全文 |
| F10 | https://arxiv.org/abs/2312.04927v1 | 成功；摘要、v1 2023-12-08，非全文 |
| F11 | https://arxiv.org/abs/2407.04620v4 | 成功；作者栏、摘要、v4 2025-08-31，非全文 |
| F12 | https://arxiv.org/abs/2501.00663v1 | 成功；摘要、v1 2024-12-31，非全文；不按编号误写首发为2025 |
| F13 | https://arxiv.org/abs/2605.22791v1 | 成功；摘要、v1 2026-05-21，非全文 |

12次成功，1次失败。失败后对同一官方HTML用内置浏览器重试一次成功，没有绕过拒绝或更换非法来源。另浏览器访问3个官方摘要页：`2609.16183`、`2504.13173v1`、`2008.07669v2`，用DOM文本核作者、完整题名、版本；随后读取Anatomy同版正文§1–6（2页连续DOM快照，非全部论文）。中间一次分页参数组合错误已按工具提示更正，不是网络失败，不加作品/查询数。没有打开用户要求观看的网页，后台检索页不切前台；只创建一个研究页并在结束时关闭。

### 正文抽样得到的有区分力信息

- Anatomy §3.2固定递推状态1024个元素；这不是把所有模型参数或每步计算全匹配。
- §3.3把条目数、干扰间隔和重复键诱饵分开；重复键题以首次绑定为真值，不能误当“应覆盖为最新值”的更新任务。
- §4.2明确卷积效应随学习率调优而变化；原始大差值不等架构类普遍优势。
- §5–6在同架构改变课程，报告从失败到可成功；这只能排除该任务/长度下的架构绝对不可能，不证明自然语言消费或所有长程问题已解决。
- §6提到伴随大模型转换工作的未见符号失败，但这里只是作者转述；伴随论文未直接核验，故未作为第五个新增作品或独立OOD证据。
- §7以后和附录未读。本次不是新增FULL，不修改原READING_STATUS。

## 3. 与CATALOG精确去重

对`02_catalog/CATALOG.md`同时搜索稳定编号及题名/别名：`2606.26560|2609.16183|2504.13173|2008.07669|Erase-then|Anatomy of Associative|It.s All Connected|Optimal Polynomial`，零命中。故仅正式提名下列**4个目录外作品**，不擅自分配W-ID。

| 本地引用号 | 核验身份与固定版本 | 证明为何不是已有同作 | 本轮阅读等级 |
|---|---|---|---|
| N02-1 | *It's All Connected: A Journey Through Test-Time Memorization, Attentional Bias, Retention, and Online Optimization*；Ali Behrouz、Meisam Razaviyayn、Peilin Zhong、Vahab Mirrokni；2504.13173v1，2025-04-17 | MIRAS不是W0234 Titans或W0217 Atlas；机制框架相关，稳定编号与题名不同 | 官方摘要/身份核验；未读正文 |
| N02-2 | *HiPPO: Recurrent Memory with Optimal Polynomial Projections*；Albert Gu、Tri Dao、Stefano Ermon、Atri Rudra、Christopher Ré；2008.07669v2，2020-10-23 | 不是W0238 Mamba、W0239对偶报告，也不是外部HippoRAG | 官方摘要/身份核验；未读正文 |
| N02-3 | *Anatomy of Associative Recall in Fixed-State Recurrences: A Matched-State Decomposition, an Interference Wall, and a Curriculum That Breaks It*；Julian Boesch、Andrew Wee；2609.16183v1，2026-09-14 | 不是W0088 Revisiting；它引用并针对学习率/卷积差异追加固定状态分解 | 官方摘要＋§1–6抽读；未全文 |
| N02-4 | *Erase-then-Delta Attention: Decoupling Erase and Write Addresses in Delta-Rule Linear Attention*；Xiao Li、Chengruidong Zhang、Hao Luo等；2606.26560v1，2026-06-25 | W0202 GDN-2解耦擦写门强度；EDA另学擦除方向；W0203是值侧重组，三者不能因“decoupling”统并 | 官方作者/摘要/版本核验；未读正文 |

**已入但漏读**：W0199、W0060、W0088、W0201、W0202、W0203、W0213、W0234、W0242；本轮重取它们的公开入口，不增加作品数或FULL数。

**已读且已有综合，不冒称漏综合**：W0229在旧01 §4；W0204/W0214/W0210/W0208在旧01 §3–4和G5；W0237/W0207已有残差/缓存区分。新缺口是它们尚未串成完整状态写忘与可学使用链，而非旧报告从未提过这些作品。

**未采用线索**：2508.08435背景综述、2407.05483再读路线、搜索结果中的匿名OpenReview稿和二手新闻。没有核全文/身份的检索命中不计为本轮4个正式新增候选；该数量也不是全部搜索结果中的陌生标题数量。

## 4. 文件与计数核验

- 脚本按目录W行重计543实体；230卡链接全部落盘，状态声明219 FULL/11 PARTIAL；核心W0199–W0247为49条、11 FULL/38未读。只是链接/文本声明核验。
- 人工实读样本12卡的路径及范围详见[COVERAGE_AUDIT](COVERAGE_AUDIT.md)，其中W0050保留PARTIAL。
- 写后Python静态检查通过：三文件UTF-8且非空，26个文档内相对链接全部存在；队列编号连续1–12。目录外正式提名4篇由上述编号/题名去重核定。git状态与起始相同，整个调研目录原本未跟踪；未运行训练或pytest（文献审计无代码变更）。研究浏览器页已关闭，其他代理/用户页面未动。
- 只写`07_scope_recovery/02_STATE_MEMORY/`三文件；没有临时下载、脚本文件、日志、构建或测试产物。其他并行代理文件不归本代理修改或清理。
