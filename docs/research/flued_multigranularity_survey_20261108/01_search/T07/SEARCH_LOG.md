# T07 实际检索日志

日期：2026-11-08（Asia/Shanghai）。执行范围仅本目录。遵守上层 PLAN：公开机制词检索，不上传内部文档；不训练、不提交、不改源码／证据表、不派生代理。

## 1. 方法与真实计数

- 平台：`WebSearch` 广域／定向检索；`FetchURL` 读取公开原始摘要、会议页面及 arXiv 官方 Atom 元数据。没有使用学术数据源插件、没有调用付费资源或用户登录会话。
- 实际 **43 次 WebSearch：39 次返回结果，4 次 HTTP 429**。查询返回多项结果不等于确认多篇作品。
- 实际 **61 次 FetchURL：56 次作品／会议摘要页读取，5 次官方 Atom 批量元数据补核**。全部成功返回文本。56 个作品页面中 **55 个进入候选，1 个错误身份排除**。
- **55 个去重有效候选，30 个精读优先；全文部分阅读 0、全文精读 0、代码核验 0。** 未将搜索片段、返回长页面或摘要页面出现 PDF 链接视作全文阅读。
- 另保留 **7 个仅发现、身份／摘要未完整核验的追查入口**（第 5 节），不计入 55。一个错误 ID 排除，以及一项未定位到的记忆线索，另记而不凑数。
- 没有使用浏览器 GUI；本轮依用户要求主要通过 WebSearch＋FetchURL 读取公共页面。没有遇到需要绕过的登录／访问拒绝。
- 检索记忆只作入口：直接尝试的已知题名／ID 必须经过原始摘要和元数据核对；错误映射 `2202.01093` 已排除，未静默改造成另一个“命中”。

## 2. 批次与实际检索式

以下每行就是实际传给 WebSearch 的 `query`。候选编号只表关联发现，不声称该次查询完成身份／摘要核验；确认由第 3 节 FetchURL 完成。日期均 2026-11-08。

### B1：计算价值、反事实获取与近期检索控制（Q01–Q03）

| 编号 | 实际查询 | 结果／用途 |
|---|---|---|
| Q01 | `"value of computation" "metareasoning" reinforcement learning` | T07-001、002；另发现机器人计算预算近期线索 U1。 |
| Q02 | `"counterfactual" "feature acquisition" reinforcement learning information acquisition` | T07-006、007；时变评估 U3、传感选择 U2 待核。 |
| Q03 | `"adaptive retrieval" "utility" "reinforcement" RAG 2025 2026` | 发现 T07-039；不采用博客／聚合列表中的效能背书。 |

### B2：互补、归因、离策略、多任务和捷径（Q04–Q09）

| 编号 | 实际查询 | 结果／用途 |
|---|---|---|
| Q04 | `"adaptive submodularity" "information gain" "complementarity"` | 初次结果噪声大，出现 T07-013 线索；后续改写为准确题名 Q12。 |
| Q05 | `"SAGE" "Shapley" "feature importance" Covert 2020` | T07-004；条件特征重要性仅作后续扩展，不新增候选。 |
| Q06 | `"Doubly Robust Policy Evaluation" "Counterfactual" sequential decision` | T07-018 及分布型离策略评估 U4；定向追查 Q28／29。 |
| Q07 | `"PCGrad" "CAGrad" "Nash-MTL" "GradNorm"` | 返回引用／对照表较多；不采纳中文博客声称的百分比，改找原始作品。 |
| Q08 | `"shortcut learning" "gradient starvation" "grokking" neural networks` | T07-033、034；与简单偏好、训练机制形成关联。 |
| Q09 | `"calibration" "selective prediction" "conformal risk control" neural networks` | T07-025、026；回溯基础共形风险文献。 |

### B3：AFA、次模保证、预算和梯度原始工作（Q10–Q15）

| 编号 | 实际查询 | 结果／用途 |
|---|---|---|
| Q10 | `"Learning to acquire information" "active feature acquisition"` | T07-005、008；准确题名后追 Q16。 |
| Q11 | `"Efficient Feature Selection via" "conditional" "information" acquisition` | 没找到足够可信对应工作；返回医疗时序二手介绍，不纳候选。 |
| Q12 | `"Adaptive Submodularity: Theory and Applications"` | T07-003；另发现 Adaptive Sequence Submodularity U5。 |
| Q13 | `"Counterfactual Risk Minimization" "Doubly Robust Policy Evaluation"` | T07-017；仍需原始摘要核验。 |
| Q14 | `"Bandits with Knapsacks" "Constrained Policy Optimization"` | 返回引用多，后续直接读官方页 T07-020，并以 Q30 定位 T07-019。 |
| Q15 | `"Gradient Surgery for Multi-Task Learning" "Conflict-Averse"` | T07-028、029，定向取得 NeurIPS 官方摘要。 |

### B4：获取学习、非短视基准、多粒度最近邻（Q16–Q21）

| 编号 | 实际查询 | 结果／用途 |
|---|---|---|
| Q16 | `"site:proceedings.mlr.press" "Learning to Acquire Information"` | T07-009，确认 2017 作品被 2026 重刊，不是近期新方法。 |
| Q17 | `"Efficient and Adaptive" "Feature Acquisition" Covert` | 发现 T07-012；与原本记忆线索不同，不冒充准确题名命中。 |
| Q18 | `"Budgeted" "Feature Acquisition" "JAFA"` | T07-011、013、014；JAFA 原始工作本轮未独立核验，不计。 |
| Q19 | `"Self-RAG" "Adaptive-RAG" "FLARE" retrieval` | T07-040、041、042、044 的公共谱系。 |
| Q20 | `"Sufficient Context" "Retrieval Augmented Generation"` | T07-043；搜索结果存在错乱日期，以摘要页与元数据日期为准。 |
| Q21 | `"Hierarchical" "retrieval" "reinforcement learning" "2026" granular` | T07-046；Deep GraphRAG U6、EventMemAgent U7 待核。 |

### B5：强简单对照、来源回访、形成机制（Q22–Q29）

| 编号 | 实际查询 | 结果／用途 |
|---|---|---|
| Q22 | `"Efficient Dynamic Feature Selection" Covert` | 实际定位到 T07-010，正式题名是 Learning to Maximize Mutual Information for Dynamic Feature Selection。 |
| Q23 | `"ReadAgent" "gists"` | T07-047；不采用第三方 FractalAgent 仓库对既有工作的自述作为证据。 |
| Q24 | `"Recursive Language Models" arxiv` | T07-048；新近模型相关声称仅作作者摘要主张，后读原始摘要／元数据。 |
| Q25 | `"Multi-Task Learning as a Bargaining Game" "multi-task" weighting enough` | T07-030；“好权重是否足够”未在此查询中得到准确作品。 |
| Q26 | `"On the Pitfalls of Simplicity Bias" "Learning and Generalization"` | 实际题名 T07-032，没有 On the 前缀。 |
| Q27 | `"Using Auxiliary Tasks" "Gradient Similarity"` | 实际题名 T07-031，非查询记忆中的题名。 |
| Q28 | `"Doubly Robust Policy Evaluation and Learning"` | T07-015；官方摘要核验。 |
| Q29 | `"Doubly Robust Off-policy Value Evaluation for Reinforcement Learning"` | T07-016，预印本／ICML 正式版关联为一作品。 |

### B6：预算、校准、多任务、机制形成；发生限流（Q30–Q37）

| 编号 | 实际查询 | 结果／用途 |
|---|---|---|
| Q30 | `"Bandits with Knapsacks" arxiv Badanidiyuru` | T07-019 的 arXiv ID 和 FOCS 版本关联。 |
| Q31 | `"On Calibration of Modern Neural Networks"` | **HTTP 429**；未重试相同查询，后用 FetchURL 读 PMLR 原始页 T07-021。 |
| Q32 | `"Can You Trust Your Model's Uncertainty"` | **HTTP 429**；先直接读原始摘要，稍后改写 Q39 一次补定位。 |
| Q33 | `"SelectiveNet" "Conformal Risk Control"` | 返回原始工作的引用和部分低可信应用，不以应用文章替代基础文献核验；直接读 T07-023、024。 |
| Q34 | `"GradNorm: Gradient Normalization"` | **HTTP 429**；改读已知 PMLR 官方入口 T07-027 并核验题名／作者。 |
| Q35 | `"Multi-Task Learning" "Just a Good Task Weighting"` | **HTTP 429**；后 Q38 一次重试仍未准确定位，记为未解决线索。 |
| Q36 | `"In-context Learning and Induction Heads" "Progress measures"` | T07-036、037、038；旧归纳头文章在此返回，未额外纳入重复背景。 |
| Q37 | `"Grokking: Generalization Beyond Overfitting"` | T07-035。 |

限流应对：不无限重试；穿插原始摘要读取和已有结果核验。4 次 429 中两项由不同查询补追（Q39／Q38），另两项直接读公开 PMLR 官方入口；没有通过账号、代理或私有接口绕过访问拒绝。

### B7：互补分解、信用分配、标签与决策校准（Q38–Q43）

| 编号 | 实际查询 | 结果／用途 |
|---|---|---|
| Q38 | `"Multi-Task Learning" "Just a Good Task Weighting"` | 返回成功但没有准确定位该记忆线索；停止重试，不计候选。 |
| Q39 | `"Can You Trust Your Model's Uncertainty" "1906.02530"` | 搜索结果多为二手引用；身份／摘要最终由 arXiv 官方页面和 Atom 确认 T07-022。 |
| Q40 | `"Nonnegative Decomposition of Multivariate Information"` | 返回后续文章中的原始工作引用；直接原始摘要和 Atom 确认 T07-050。 |
| Q41 | `"Counterfactual Multi-Agent Policy Gradients"` | T07-051；不把固定其余动作的基线理解成动态策略总效用。 |
| Q42 | `"Selective Labels" "Learning" "Decisions"` | T07-052，标签选择／探索成本。 |
| Q43 | `"On Calibration" "decision" "Decision Calibration"` | T07-053、054；标题、作者、摘要再由原始页核验。 |

## 3. 原始摘要读取清单（56 次）

所有以下 URL 均实际调用 FetchURL，返回摘要／官方介绍；候选编号可与 `CANDIDATES.md` 一一对照。除 X1 外均进候选。这里只记录真实请求 URL，不把后续 PDF 入口点击虚构为已执行。

### F1（8）

- T07-001 https://arxiv.org/abs/1711.06892
- T07-002 https://arxiv.org/abs/2410.05563
- T07-003 https://arxiv.org/abs/1003.3967
- T07-004 https://arxiv.org/abs/2004.00668
- T07-005 https://arxiv.org/abs/2006.07701
- T07-006 https://arxiv.org/abs/2011.00825
- T07-007 https://arxiv.org/abs/2312.03619
- T07-008 https://arxiv.org/abs/2608.02305

### F2（10）

- T07-009 https://proceedings.mlr.press/r15/pu17a.html
- T07-010 https://arxiv.org/abs/2301.00557
- T07-011 https://arxiv.org/abs/2508.14734
- T07-012 https://arxiv.org/abs/2605.05511
- T07-013 https://arxiv.org/abs/2610.21919
- T07-014 https://arxiv.org/abs/2609.32325
- T07-015 https://arxiv.org/abs/1103.4601
- T07-016 https://proceedings.mlr.press/v48/jiang16.html
- T07-017 https://arxiv.org/abs/1502.02362
- T07-018 https://arxiv.org/abs/2412.08052

### F3（10）

- T07-019 https://arxiv.org/abs/1305.2545
- T07-020 https://proceedings.mlr.press/v70/achiam17a.html
- T07-021 https://proceedings.mlr.press/v70/guo17a.html
- T07-022 https://arxiv.org/abs/1906.02530
- T07-023 https://proceedings.mlr.press/v97/geifman19a.html
- T07-024 https://arxiv.org/abs/2208.02814
- T07-025 https://arxiv.org/abs/2512.12844
- T07-026 https://arxiv.org/abs/2603.24704
- T07-027 https://proceedings.mlr.press/v80/chen18a.html
- T07-028 https://arxiv.org/abs/2001.06782

### F4（10）

- T07-029 https://proceedings.neurips.cc/paper/2021/hash/9d27fdf2477ffbff837d73ef7ae23db9-Abstract.html
- T07-030 https://proceedings.mlr.press/v162/navon22a.html
- T07-031 https://arxiv.org/abs/1812.02224
- T07-032 https://arxiv.org/abs/2006.07710
- T07-033 https://arxiv.org/abs/2011.09468
- T07-034 https://arxiv.org/abs/2403.03375
- T07-035 https://arxiv.org/abs/2201.02177
- T07-036 https://arxiv.org/abs/2301.05217
- T07-037 https://arxiv.org/abs/2404.07129
- T07-038 https://arxiv.org/abs/2511.01033

### F5（12）

- T07-039 https://arxiv.org/abs/2607.06507
- T07-040 https://arxiv.org/abs/2310.11511
- T07-041 https://arxiv.org/abs/2305.06983
- T07-042 https://arxiv.org/abs/2403.14403
- T07-043 https://arxiv.org/abs/2411.06037
- T07-044 https://aclanthology.org/2025.acl-long.319/
- T07-045 https://arxiv.org/abs/2401.18059
- T07-046 https://arxiv.org/abs/2502.09891
- T07-047 https://arxiv.org/abs/2402.09727
- T07-048 https://arxiv.org/abs/2512.24601
- T07-049 https://arxiv.org/abs/2004.07780
- **X1 排除** https://arxiv.org/abs/2202.01093 ：原本作为多任务权重记忆入口试取，实际为 IXPE X 射线偏振探测数据加权研究；作者及摘要完全不符，不进入候选。

### F6（6）

- T07-050 https://arxiv.org/abs/1004.2515
- T07-051 https://arxiv.org/abs/1705.08926
- T07-052 https://proceedings.mlr.press/v139/wei21a.html
- T07-053 https://arxiv.org/abs/2107.05719
- T07-054 https://arxiv.org/abs/2504.15615
- T07-055 https://arxiv.org/abs/2509.16959

## 4. 官方元数据补核（5 次 FetchURL，45 条 arXiv 记录）

摘要页正文抽取经常省略题名／作者，**没有把提交者当成作者**。通过 FetchURL 读取 arXiv 官方公开 Atom 记录，核对题名、作者、首次日期、更新版、comment、journal_ref 与 DOI；未使用插件型学术数据源。

- M1：8 条，补核 T07-001–008。
  https://export.arxiv.org/api/query?id_list=1711.06892,2410.05563,1003.3967,2004.00668,2006.07701,2011.00825,2312.03619,2608.02305
- M2：10 条。
  https://export.arxiv.org/api/query?id_list=2301.00557,2508.14734,2605.05511,2610.21919,2609.32325,1103.4601,1502.02362,2412.08052,1305.2545,1906.02530&max_results=10
- M3：10 条。
  https://export.arxiv.org/api/query?id_list=2208.02814,2512.12844,2603.24704,2001.06782,1812.02224,2006.07710,2011.09468,2403.03375,2201.02177,2301.05217&max_results=10
- M4：10 条。
  https://export.arxiv.org/api/query?id_list=2404.07129,2511.01033,2607.06507,2310.11511,2305.06983,2403.14403,2411.06037,2401.18059,2502.09891,2402.09727&max_results=10
- M5：7 条。
  https://export.arxiv.org/api/query?id_list=2512.24601,2004.07780,1004.2515,1705.08926,2107.05719,2504.15615,2509.16959&max_results=10

其余 10 项的元数据／题名由 PMLR 8 项、ACL 1 项、NeurIPS 1 项官方页确认。T07-029 作者名单未随正文抽取返回，明确留待下一轮核对，不影响稳定 ID、题名、年份和摘要已确认。

重要核验收获：T07-003 v5 明示证明缺陷修订；T07-034 预印本／正式版异名；T07-009 的 2026 日期只是重刊；T07-048 v3 可能含首发不存在的后训练内容。以上均不是第二篇作品。

## 5. 仅发现、待核验追查入口（7；均不计入 55）

| ID | 实际发现入口 | 已知深度与下一步 |
|---|---|---|
| U1 | Learning Robot Metareasoning: Adaptive Computation Budgets for Real-Time Control；https://arxiv.org/html/2610.23662v1 | Q01 搜索片段，未 Fetch；核对计算预算是否实际执行成本、semi-MDP 假设，不能背书新方法。 |
| U2 | Uncertainty-Guided Counterfactual Sensor Selection and Safety-Gated Recognition for Autonomous Sensing Agents in IoT Systems；https://arxiv.org/html/2610.35344v1 | Q02 搜索片段，未核身份／摘要；关注固定识别模型受控响应与自然反事实效应的区分。 |
| U3 | Evaluation of Active Feature Acquisition Methods for Time-…；http://jmlr.org/papers/volume26/23-1635/23-1635.pdf | Q02 标题被截断，只知道 2025 JMLR 线索；不得补全题名。追 T07-007 的 companion paper 并核对是否时变特征、测量反过来影响状态。 |
| U4 | Doubly-Robust Estimation of Counterfactual Policy Mean Embeddings；https://neurips.cc/virtual/2025/poster/120338 | Q06／Q13 官方搜索介绍，尚未 Fetch；分布型 OPE，可能补齐尾部／多损失效用，不只均值。 |
| U5 | Adaptive Sequence Submodularity；https://arxiv.org/html/1902.05981v2 | Q12 搜索片段，未读摘要；追动作顺序与集合模型的差异，判断是否允许改变后续策略。 |
| U6 | Deep GraphRAG: A Balanced Approach to Hierarchical Retrieval and Adaptive Integration；https://arxiv.org/html/2601.11144v3 | Q21 搜索结果，未核；需先确认身份、摘要和来源回访，再讨论邻近程度。 |
| U7 | EventMemAgent: Hierarchical Event-Centric Memory…；https://media.eventhosts.cc/Conferences/ECCV2026/pdfs/11561.pdf | Q21 搜索结果题名截断，未核身份／摘要；多粒度工具＋强化学习线索，正式题名、作者、论文状态均待核。 |

额外未定位线索：记忆中的 “Just a Good Task Weighting” 未通过 Q25、Q35、Q38 定位为可确认作品；错误 ID X1 不补猜、不计数。若后续重新定位，先准确搜索题名，再官方核验。

## 6. 最近 12 个月实际覆盖与局限

窗口采用 **2025-11-08 至 2026-11-08**，区分首发和旧工作修订，不能混成“13 篇全新成果”。

- 窗口内首发 **8**：T07-008、012、013、014、025、026、039、048。
- 旧作品在窗口内修订 **5**：T07-011、018、038、046、055。T07-038 首发 2025-11-02，距窗口边界差 6 天，**仅修订计入近期覆盖**。
- 其余仅搜索发现的 2026 线索 U1、U2、U6、U7 不计确认覆盖。T07-009 重刊不计近期方法发展。
- 近期方向初筛：非短视获取的监督风险回归／路径梯度，完整训练数据假设的显式研究，选择后风险保证，状态条件证据控制，以及程序化可变片段访问。均需精读后才能判断证据强弱。

检索局限：理论基础检索主要经机器学习与信息论公开文献，尚未系统覆盖经济学信息设计、因果推断中的动态治疗策略、非平稳预算和所有 2026 新工作。55 项只是可追溯首批，不声称全域覆盖或达到阶段收束条件。
