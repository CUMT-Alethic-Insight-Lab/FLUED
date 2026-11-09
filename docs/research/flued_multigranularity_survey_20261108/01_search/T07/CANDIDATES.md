# T07 首轮候选：效用学习、反事实控制、预算、校准与训练动力学

日期：2026-11-08。范围：发现／摘要初筛，不是全文综述。

## 计数与阅读口径

- **55 个去重作品，55 个身份及摘要／官方介绍已核验；30 项标记「精读优先」；全文精读 0，代码核验 0。**
- 全部通过公开原始来源核验：arXiv 摘要页及官方 Atom 元数据、PMLR、NeurIPS proceedings、ACL Anthology。实际查询与抓取批次见 `SEARCH_LOG.md`。Atom 用于补齐标题、作者、版本及正式版关联，不能算全文阅读。
- `A` = 已读摘要／官方介绍；`M` = 官方元数据补核。所有候选均为 A，arXiv 条目同时 M。作者只写首作者等，完整名单可循原始来源；没有可靠返回的作者明确留待核。
- 下文「支持」指值得追查的机制依据，「反例」指能限制某种设计推断的潜力，**不代表已对 FLUED 得出结论**。所有经验数字、证明强度均须下一轮回原文定位后才能用于综合稿。
- 年份优先列首次公开年；正式发表或修订另列，不把预印本、正式版、同一 ID 的版本计成不同作品。未经核验的正式会议信息不补猜。
- 全文链接是**入口**，不是已经抓取或精读的证据。新近作品仅核验其存在和作者摘要主张，不背书其有效性或成熟度。

## 本专题用语边界

主动特征获取（Active Feature Acquisition，AFA）：每个样本按成本逐步选择获取哪些尚未观察的输入。计算价值（Value of Computation，VOC）：执行额外计算相对于立即决策的预期净收益。非短视效用：把当前动作对未来可用动作及最终结果的影响一并计入，而非仅测一步改善。离策略评估（Off-policy Evaluation，OPE）：用一种策略产生的数据估计另一策略的回报。双重稳健估计：组合回报模型与行为策略模型来控制偏差和方差，但仍须检查识别、支持覆盖等条件。自适应次模性：随已观察信息增加，动作的条件边际收益满足递减的结构条件；不是所有信息增益都具有该性质。部分信息分解（Partial Information Decomposition，PID）：把多源信息区分为冗余、独有和协同成分。机制形成：训练期间实现某行为的内部计算结构逐步建立，与收官点的使用证据不同。

CBIU 仅为内部线索，本轮不对外查询该内部词，也不假定存在同名成熟公共文献。以下收集的是可公开核验的相关机制。

## A. 信息／计算价值、互补与主动获取（14）

### T07-001 — Learning to select computations — 精读优先
- 作者／年份／版本：Frederick Callaway 等；2017 首发，UAI 2018；arXiv v3（2018）。稳定 ID：`1711.06892`。[原始摘要](https://arxiv.org/abs/1711.06892)；[全文入口](https://arxiv.org/pdf/1711.06892v3)。深度：A+M。
- 摘要机制：Bayesian metalevel policy search 用短视信息价值与完美信息价值之间的界，学习近似最优的计算选择；覆盖停止、竞争选项间分配和规划，并计入元控制开销。
- 支持／反例潜力：支持学习「是否再算」而不是按熵直接分配；也提醒控制器本身可能比被节省的计算更贵。
- **精读问题**：界的成立条件是什么？需多少模拟／标签来学习价值？各计算动作间的互补如何通过策略表达，是否有短视贪心失败例？

### T07-002 — Rational Metareasoning for Large Language Models
- 作者／年份／版本：C. Nicolò De Sabbata 等；2024 首发，v3（2025-06-23）。ID：`2410.05563`。[摘要](https://arxiv.org/abs/2410.05563)；[全文](https://arxiv.org/pdf/2410.05563v3)。A+M。
- 摘要机制：把计算价值式的多余推理惩罚加入奖励，用 Expert Iteration 学习何时生成中间推理。
- 支持／反例潜力：支持选择性计算可经训练形成；仅减少生成 token 不等于减少实际延迟或证明来源读取效用。
- 下一步：核查奖励、无推理反事实标签的生成成本及多任务／难度迁移；正式会议信息待官网追认。

### T07-003 — Adaptive Submodularity: Theory and Applications in Active Learning and Stochastic Optimization — 精读优先
- 作者／年份／版本：Daniel Golovin、Andreas Krause；2010 首发；v5（2017）。ID：`1003.3967`。[摘要](https://arxiv.org/abs/1003.3967)；[全文](https://arxiv.org/pdf/1003.3967v5)。A+M。
- 摘要机制：在自适应次模条件下，为自适应贪心提供最大化／覆盖近似保证。
- 支持／反例潜力：支持有条件的贪心，不支持任意动作效用相加。**官方元数据特别说明 v5 修复 Theorem 13 证明缺陷，改为附加强自适应次模条件下的较弱保证**；旧版结论不可直接搬用。
- **精读问题**：分别抄清单调性、条件独立、预算和覆盖条件；组合证据 XOR 式互补是否破坏条件？版本修订影响哪些可引用定理？

### T07-004 — Understanding Global Feature Contributions With Additive Importance Measures — 精读优先
- 作者／年份／版本：Ian Covert、Scott Lundberg、Su-In Lee；NeurIPS 2020，v2。ID：`2004.00668`。[摘要](https://arxiv.org/abs/2004.00668)；[全文](https://arxiv.org/pdf/2004.00668v2)。A+M。
- 摘要机制：SAGE 以预测能力的 Shapley 分配量化全局特征贡献，明确考虑特征交互。
- 支持／反例潜力：可提供互补／冗余下的贡献仪器；**归因结果可加不等于真实动作效用可加**，也不是顺序策略的 Q 值。
- **精读问题**：缺失特征怎样边缘化？条件依赖与分布外遮蔽如何影响贡献？估计一个动作组需多少模型调用，能否承受训练标签预算？

### T07-005 — Dynamic Feature Acquisition with Arbitrary Conditional Flows
- 作者／年份／版本：Yang Li、Junier B. Oliva；2020 首发，v2（2021）。ID：`2006.07701`。[摘要](https://arxiv.org/abs/2006.07701)；[全文](https://arxiv.org/pdf/2006.07701v2)。A+M。
- 摘要机制：任意条件流估计条件分布，以条件互信息选下一特征，并学习贝叶斯网络加速。
- 支持／反例潜力：支持查询条件获取；信息增益不自动等价于下游损失改善，且条件生成器本身昂贵。
- 下一步：核查获取规则是否短视、生成器误差与训练完整数据要求、真实计算成本。

### T07-006 — Reinforcement Learning with Efficient Active Feature Acquisition
- 作者／年份／版本：Haiyan Yin 等；2020，v1。ID：`2011.00825`。[摘要](https://arxiv.org/abs/2011.00825)；[全文](https://arxiv.org/pdf/2011.00825v1)。A+M。注意摘要页提交者拼写不作为作者，作者以 Atom 为准。
- 摘要机制：模型式强化学习联合主动获取策略与顺序变分表示，在部分可见状态下兼顾任务奖励和测量成本。
- 支持／反例潜力：观测动作会改变后续控制，较静态输入遮蔽更接近闭环获取；机器人／医疗模拟不能直接证明语言任务适用。
- 下一步：核查观测与环境动作时间尺度、获取成本定义、模型偏差和样本成本。

### T07-007 — Evaluation of Active Feature Acquisition Methods for Static Feature Settings — 精读优先
- 作者／年份／版本：Henrik von Kleist 等；2023，v2。ID：`2312.03619`。[摘要](https://arxiv.org/abs/2312.03619)；[全文](https://arxiv.org/pdf/2312.03619v2)。A+M。
- 摘要机制：部署主动获取策略会改变缺失分布；提出半离线评估，在静态特征设置中构造 IPW、直接法及双重强化学习估计。
- 支持／反例潜力：直接反驳「在历史已观察样本上量 on/off 就等价于部署效用」；MAR、MNAR 的可识别前提必须区分。
- **精读问题**：何时允许重排获取顺序？观测动作是否影响真实特征值？各估计量的支持覆盖、缺失机制与额外模型假设分别是什么？

### T07-008 — BRiG-AFA: Bellman Risk-to-Go Learning for Non-Myopic Active Feature Acquisition — 精读优先
- 作者／年份／版本：Jiaorong Feng、Qian Li、Ying Li；2026-08-03，v1。ID：`2608.02305`。[摘要](https://arxiv.org/abs/2608.02305)；[全文](https://arxiv.org/pdf/2608.02305v1)。A+M；新近预印本。
- 摘要机制：按剩余预算分别学习候选条件的终局风险函数，以 Bellman 目标向后拟合；当前无即时收益的上下文特征可因后续动作而有价值。
- 支持／反例潜力：非常贴近「先获取线索才知道去哪里」的互补效用；作者摘要主动承认小预算上的混合结果及尚缺全面先进方法比较。
- **精读问题**：目标是否使用未获取值而造成标签泄漏？每个预算／候选的全信息监督要多少调用？原始风险到部署策略的误差传播如何界定？

### T07-009 — Learning to Acquire Information
- 作者／年份／版本：Yewen Pu、Leslie Pack Kaelbling、Armando Solar-Lezama；UAI 2017。ID：`pmlr-r15-pu17a`。[官方摘要](https://proceedings.mlr.press/r15/pu17a.html)；[全文](https://raw.githubusercontent.com/mlresearch/r15/main/assets/pu17a/pu17a.pdf)。A。
- 摘要机制：在统一观测熵假设下，直接从历史观测预测下一观测结果，绕开复杂隐假设空间，只用观测数据学习查询。
- 支持／反例潜力：支持降低标签要求；关键熵假设限制了把最大观测熵当成普遍任务效用的推断。
- 下一步：追查假设失败时的反例及与任务标签无关的查询是否仍改善决策。PMLR 2026-10 重刊不是新作品。

### T07-010 — Learning to Maximize Mutual Information for Dynamic Feature Selection — 精读优先
- 作者／年份／版本：Ian Covert 等；ICML 2023，v2。ID：`2301.00557`。[摘要](https://arxiv.org/abs/2301.00557)；[全文](https://arxiv.org/pdf/2301.00557v2)。A+M。
- 摘要机制：以摊销优化学习条件互信息贪心策略，训练最优时恢复贪心，无需直接求解通用强化学习。
- 支持／反例潜力：应作为简单强对照；恢复贪心不是恢复最优非短视策略，互补动作可能使一步收益失灵。
- **精读问题**：最优训练结论所需数据、损失和模型容量条件是什么？估计互信息的教师信号从何而来？与 T07-008、011 在非短视考场上怎样比较？

### T07-011 — AFABench: A Generic Framework for Benchmarking Active Feature Acquisition — 精读优先
- 作者／年份／版本：Valter Schütz 等；2025 首发，v3（2026-02-22）。ID：`2508.14734`。[摘要](https://arxiv.org/abs/2508.14734)；[全文](https://arxiv.org/pdf/2508.14734v3)。A+M。
- 摘要机制：统一静态、短视与强化学习主动获取方法；引入 CUBE-NM 合成数据专门暴露短视选择的局限。
- 支持／反例潜力：可找到互补动作的最低成本诊断任务；新方法应先战胜静态／简单获取，不因“可学习”即胜出。
- **精读问题**：基准是否公平计入训练和调参成本？哪些非短视方法反而输给静态／贪心？预算／特征成本是否异质？需定位真实表格，不引用检索片段的排名。

### T07-012 — Non-Myopic Active Feature Acquisition via Pathwise Policy Gradients — 精读优先
- 作者／年份／版本：Linus Aronsson、Morteza Haghir Chehreghani；2026，v2（2026-09-29）。ID：`2605.05511`。[摘要](https://arxiv.org/abs/2605.05511)；[全文](https://arxiv.org/pdf/2605.05511v2)。A+M；预印本。
- 摘要机制：整条获取轨迹上的连续松弛／路径梯度；前向离散动作、反向软松弛，并按阶段锐化温度。
- 支持／反例潜力：覆盖动作改变后续策略、训练与部署离散化不一致；不能把降低梯度方差误写成无偏或普遍更优。
- **精读问题**：直通梯度偏差如何分析？温度课程是否关系到机制形成？全轨迹监督、存储和反向传播成本与离策略学习相比如何？

### T07-013 — The Lagrangian Structure of Cost-Penalized Active Feature Acquisition — 精读优先
- 作者／年份／版本：Joseph Bingham；2026-10-15，v1。ID：`2610.21919`。[摘要](https://arxiv.org/abs/2610.21919)；[全文](https://arxiv.org/pdf/2610.21919v1)。A+M；预印本，理论未复核。
- 摘要机制：区分期望成本的拉格朗日松弛与硬预算策略，分解预算松弛差和贪心次优差；明确声称即使联合高斯，目标互信息也不一定次模。
- 支持／反例潜力：直接限制“信息增益−固定成本”启发式的保证；摘要承认大临床任务上次优差不可计算，诊断不是数值保证。
- **精读问题**：次模比率界是否逐历史成立？硬／软预算和随机化差怎样定义？证书需要求解何种最优问题，计算困难是否仅被转移？

### T07-014 — Active Feature Acquisition With Incomplete Training Data — 精读优先
- 作者／年份／版本：Reza Rezvan 等；2026-09-26，v1。ID：`2609.32325`。[摘要](https://arxiv.org/abs/2609.32325)；[全文](https://arxiv.org/pdf/2609.32325v1)。A+M；预印本。
- 摘要机制：训练数据不完整时，一步动作价值在 MCAR 条件下不变，多步价值可降低；过滤与生成恢复分别涉及维度／预算上的指数样本规模。
- 支持／反例潜力：指出非短视效用学习可能比短视方法更依赖昂贵完整训练标签；不能只报部署时少读。
- **精读问题**：MCAR 下“不变”的估计对象是什么？指数结论的上下界、分布及可达性条件？语言中缺少完整反事实轨迹时哪种恢复误差最危险？

## B. 反事实评估、信用分配与预算（6）

### T07-015 — Doubly Robust Policy Evaluation and Learning
- 作者／年份／版本：Miroslav Dudik、John Langford、Lihong Li；ICML 2011，v2。ID：`1103.4601`。[摘要](https://arxiv.org/abs/1103.4601)；[全文](https://arxiv.org/pdf/1103.4601v2)。A+M。
- 摘要机制：情境赌博机中结合奖励模型和历史策略模型，缓解偏差／方差。
- 支持／反例潜力：提供单步动作效用学习基线；不自动处理动作影响后续状态与策略。
- 下一步：核查倾向概率、动作支持覆盖与有限样本误差，不能将双重稳健理解为无需探索。

### T07-016 — Doubly Robust Off-policy Value Evaluation for Reinforcement Learning — 精读优先
- 作者／年份／版本：Nan Jiang、Lihong Li；2015 预印本／ICML 2016。ID：`pmlr-v48-jiang16`，关联 `1511.03722`。[官方摘要](https://proceedings.mlr.press/v48/jiang16.html)；[全文](https://proceedings.mlr.press/v48/jiang16.pdf)。A；预印本和正式版同计一项。
- 摘要机制：把双重稳健从单步推广到顺序决策，研究内在困难及部分场景下的下界匹配。
- 支持／反例潜力：on/off 导致后续策略变化，应估计轨迹回报而非仅终层遮蔽差；仍依赖历史轨迹可覆盖新策略。
- **精读问题**：无偏性所需哪些已知量？长轨迹方差怎样增长？固定后续动作的干预与按新状态继续策略的总效应是否被区分？

### T07-017 — Counterfactual Risk Minimization: Learning from Logged Bandit Feedback
- 作者／年份／版本：Adith Swaminathan、Thorsten Joachims；2015，v2。ID：`1502.02362`。[摘要](https://arxiv.org/abs/1502.02362)；[全文](https://arxiv.org/pdf/1502.02362v2)。A+M。
- 摘要机制：倾向评分与方差敏感泛化界导出反事实风险最小化和 POEM。
- 支持／反例潜力：可追查效用标签来自旧控制器时的选择偏差；不是新策略未知动作的免费标签来源。
- 下一步：核查裁剪、方差正则与有效样本量；与 T07-016 区分单步／顺序口径。

### T07-018 — CANDOR: Counterfactual ANnotated DOubly Robust Off-Policy Evaluation — 精读优先
- 作者／年份／版本：Aishwarya Mandyam 等；2024 首发，v2（2026-05-27）；官方元数据称 CHIL 2026，正式页面待追。[摘要](https://arxiv.org/abs/2412.08052)；[全文](https://arxiv.org/pdf/2412.08052v2)。ID：`2412.08052`。A+M。
- 摘要机制：用专家反事实注释扩充覆盖，但不准确注释可比无注释更差；比较将注释放入不同双重稳健部件的方法。
- 支持／反例潜力：强反例于“造更多反事实标签必然更好”；专家／教师标签偏差与方差须分开成本化。
- **精读问题**：注释依赖何种可识别前提？为何仅放奖励模型部件更稳健？同样预算应用于真随机探索、合成标签或专家注释，收益如何比较？

### T07-019 — Bandits with Knapsacks
- 作者／年份／版本：Ashwinkumar Badanidiyuru、Robert Kleinberg、Aleksandrs Slivkins；FOCS 2013；扩展 v8（2017）。ID：`1305.2545`，DOI `10.1109/FOCS.2013.30`。[摘要](https://arxiv.org/abs/1305.2545)；[全文](https://arxiv.org/pdf/1305.2545v8)。A+M。
- 摘要机制：多个资源预算下同时学习收益与消耗，平衡探索或原始—对偶更新；最优动态策略可强于最佳固定动作。
- 支持／反例潜力：预算不必只是一项固定惩罚；但跨轮资源预算与单次输入的读预算不同。
- 下一步：核查独立同分布收益／消耗假设、耗尽规则及与多步观测状态相容性。

### T07-020 — Constrained Policy Optimization — 精读优先
- 作者／年份／版本：Joshua Achiam、David Held、Aviv Tamar、Pieter Abbeel；ICML 2017。ID：`pmlr-v70-achiam17a`。[官方摘要](https://proceedings.mlr.press/v70/achiam17a.html)；[全文](https://proceedings.mlr.press/v70/achiam17a/achiam17a.pdf)。A。
- 摘要机制：策略优化显式约束行为成本，通过策略差异界给出每次迭代近似满足约束的保证。
- 支持／反例潜力：把收益与预算分开比固定罚项更可解释；期望成本保证不等于逐样本硬上限。
- **精读问题**：保证是精确策略搜索还是采样近似？约束沿训练全程成立到何种程度？多个成本量纲、控制器开销和尾延迟如何纳入？

## C. 校准、选择性预测与决策风险（6）

### T07-021 — On Calibration of Modern Neural Networks
- 作者／年份／版本：Chuan Guo、Geoff Pleiss、Yu Sun、Kilian Q. Weinberger；ICML 2017。ID：`pmlr-v70-guo17a`。[摘要](https://proceedings.mlr.press/v70/guo17a.html)；[全文](https://proceedings.mlr.press/v70/guo17a/guo17a.pdf)。A。
- 摘要机制：现代神经网络概率失校准；温度缩放在所测分类设置中有效。
- 支持／反例潜力：原始置信度不应直接当获取价值；分类校准并不校准“再读一次能提高多少”。
- 下一步：区分正确率校准、动作优势校准与预算阈值校准；保留独立校准集成本。

### T07-022 — Can You Trust Your Model's Uncertainty? Evaluating Predictive Uncertainty Under Dataset Shift — 精读优先
- 作者／年份／版本：Yaniv Ovadia 等；NeurIPS 2019，v2。ID：`1906.02530`。[摘要](https://arxiv.org/abs/1906.02530)；[全文](https://arxiv.org/pdf/1906.02530v2)。A+M。
- 摘要机制：大规模比较分布偏移下预测不确定性，发现传统事后校准及多种方法不足，一些模型平均方法表现较强。
- 支持／反例潜力：直接限制“校准一次就能安全控制所有新查询”；没有证明集成方法在本任务普遍最好。
- **精读问题**：偏移类型、强度及风险指标是什么？控制器改变被读样本分布是否属于所测偏移？获取后再校准的额外成本怎样量化？

### T07-023 — SelectiveNet: A Deep Neural Network with an Integrated Reject Option
- 作者／年份／版本：Yonatan Geifman、Ran El-Yaniv；ICML 2019。ID：`pmlr-v97-geifman19a`。[摘要](https://proceedings.mlr.press/v97/geifman19a.html)；[全文](https://proceedings.mlr.press/v97/geifman19a/geifman19a.pdf)。A。
- 摘要机制：联合学习预测和拒答，而不是固定模型置信度阈值，优化风险—覆盖权衡。
- 支持／反例潜力：停止／拒答可作为学习动作；低风险若来自几乎全拒答并非有效节省。
- 下一步：核查覆盖约束和训练目标是否适合“回退原文”而非完全拒答。

### T07-024 — Conformal Risk Control — 精读优先
- 作者／年份／版本：Anastasios N. Angelopoulos 等；2022 首发，v4（2025-06-13）。ID：`2208.02814`。[摘要](https://arxiv.org/abs/2208.02814)；[全文](https://arxiv.org/pdf/2208.02814v4)。A+M；正式 ICLR 2024 入口待追认，不另计。
- 摘要机制：推广共形预测至任意单调损失的期望控制，另有分布偏移、分位风险等扩展。
- 支持／反例潜力：可为停止阈值提供有限样本约束框架；**读取更多不保证实际任务损失单调**，不能直接套定理。
- **精读问题**：交换性、损失有界和单调条件的精确定义？风险是总体期望还是选择后子群？同一校准集反复选策略会怎样？

### T07-025 — Selective Conformal Risk Control
- 作者／年份／版本：Yunpeng Xu、Wenge Guo、Zhi Wei；2025-12-14 首发，v2（2026-04-27）。ID：`2512.12844`。[摘要](https://arxiv.org/abs/2512.12844)；[全文](https://arxiv.org/pdf/2512.12844v2)。A+M；预印本。
- 摘要机制：先选择可信样本再做风险控制；联合校准和测试样本的方法与仅校准集方法分别给出不同保证。
- 支持／反例潜力：选择性读取／停止后的校准不是普通总体校准；两数据集证据不构成语言顺序访问保证。
- 下一步：比较精确有限样本保证与 PAC 型保证，是否允许在线多步策略改变所选子集。

### T07-026 — Conformal Selective Prediction with General Risk Control — 精读优先
- 作者／年份／版本：Tian Bai、Ying Jin；2026-03-25，v1。ID：`2603.24704`。[摘要](https://arxiv.org/abs/2603.24704)；[全文](https://arxiv.org/pdf/2603.24704v1)。A+M；预印本。
- 摘要机制：SCoRE 用广义 e-values 构造信任／拒绝决策，控制被信任样本上的一般有界连续风险。
- 支持／反例潜力：比单纯正确率校准更接近动作依赖风险；摘要的分布偏移扩展不可理解为任意策略漂移免疫。
- **精读问题**：两类风险保证究竟控制何种随机比率／期望？如何处理多次自适应查看与动作选择？需要多少独立标签，能否用于优势而非预测风险？

## D. 多任务梯度与辅助训练（5）

### T07-027 — GradNorm: Gradient Normalization for Adaptive Loss Balancing in Deep Multitask Networks
- 作者／年份／版本：Zhao Chen 等；ICML 2018。ID：`pmlr-v80-chen18a`。[摘要](https://proceedings.mlr.press/v80/chen18a.html)；[全文](https://proceedings.mlr.press/v80/chen18a/chen18a.pdf)。A。
- 摘要机制：动态调整任务梯度幅值，平衡多任务训练速率。
- 支持／反例潜力：辅助重建与终任务信号尺度可能失衡；幅度平衡不意味着梯度方向一致或新路径真正被消费。
- 下一步：核查训练速率基准、额外反向成本和某任务权重消失的可能性。

### T07-028 — Gradient Surgery for Multi-Task Learning — 精读优先
- 作者／年份／版本：Tianhe Yu 等；NeurIPS 2020，v4。ID：`2001.06782`。[摘要](https://arxiv.org/abs/2001.06782)；[全文](https://arxiv.org/pdf/2001.06782v4)。A+M。
- 摘要机制：PCGrad 在任务梯度冲突时投影，缓解特定优化景观中的有害干扰。
- 支持／反例潜力：可作多损失冲突对照；单步余弦为正或投影后不冲突都不是整个训练史的因果贡献证据。
- **精读问题**：三种有害条件各是什么？投影顺序、随机梯度噪声、参数分块和多次反向成本？是否存在改善平均指标却让目标机制旁路更严重的可能？

### T07-029 — Conflict-Averse Gradient Descent for Multi-task Learning
- 作者／年份／版本：作者名单本轮原始页面抽取未返回，留待核；NeurIPS 2021。稳定 ID：NeurIPS `9d27fdf2477ffbff837d73ef7ae23db9`。[官方摘要](https://proceedings.neurips.cc/paper/2021/hash/9d27fdf2477ffbff837d73ef7ae23db9-Abstract.html)；[全文](https://proceedings.neurips.cc/paper/2021/file/9d27fdf2477ffbff837d73ef7ae23db9-Paper.pdf)。A；检索关联 arXiv `2110.14048`，未另计。
- 摘要机制：以最差任务局部改善正则化平均损失更新，连接普通梯度下降及多目标方法，并声称收敛保证。
- 支持／反例潜力：可明确“平均目标最优”与“每个任务最好”不是一回事；不是机制形成保证。
- 下一步：追正式作者信息、定理的光滑性和步长条件、各任务尾部表现与求解开销。

### T07-030 — Multi-Task Learning as a Bargaining Game
- 作者／年份／版本：Aviv Navon 等；ICML 2022。ID：`pmlr-v162-navon22a`，关联 `2202.01017`。[官方摘要](https://proceedings.mlr.press/v162/navon22a.html)；[全文](https://proceedings.mlr.press/v162/navon22a/navon22a.pdf)。A。
- 摘要机制：把任务梯度组合建模为议价，特定假设下使用唯一 Nash 议价解，并推导收敛性质。
- 支持／反例潜力：提供区别于简单余弦／幅度的优化对照；议价公平性不等于目标信息被真正使用。
- 下一步：检查存在共同改善方向的条件、退化情形及与原始损失尺度的关系。

### T07-031 — Adapting Auxiliary Losses Using Gradient Similarity — 精读优先
- 作者／年份／版本：Yunshu Du 等；2018 首发，v2（2020）。ID：`1812.02224`。[摘要](https://arxiv.org/abs/1812.02224)；[全文](https://arxiv.org/pdf/1812.02224v2)。A+M。
- 摘要机制：用主／辅任务梯度余弦动态赋权，探测辅助损失何时开始有害，并给出主任务临界点收敛结论。
- 支持／反例潜力：与“辅助训练有帮助还是旁路”直接相关；收官正余弦不能倒推出早期路径未被压制。
- **精读问题**：连续训练的辅助梯度可见性怎样记录？零梯度／低余弦是否意味着机制无用还是尚未形成？定理是否只保主任务不保辅助语义？

## E. 捷径、梯度饥饿和机制形成（7）

### T07-032 — The Pitfalls of Simplicity Bias in Neural Networks
- 作者／年份／版本：Harshay Shah 等；NeurIPS 2020，v2。ID：`2006.07710`。[摘要](https://arxiv.org/abs/2006.07710)；[全文](https://arxiv.org/pdf/2006.07710v2)。A+M。
- 摘要机制：在可控多特征数据中，训练可极端依赖最简单特征、忽略更复杂预测特征；甚至损害同分布泛化，常用集成／对抗方法可能不足。
- 支持／反例潜力：弱使用不能直接判定复杂信息无价值；需要把数据可预测性与训练偏好分离。
- 下一步：核查“简单”的定义和可迁移范围，不把图像或合成特征定理当作所有压缩通路结论。

### T07-033 — Gradient Starvation: A Learning Proclivity in Neural Networks — 精读优先
- 作者／年份／版本：Mohammad Pezeshki 等；2020 首发／NeurIPS 2021，v4。ID：`2011.09468`。[摘要](https://arxiv.org/abs/2011.09468)；[全文](https://arxiv.org/pdf/2011.09468v4)。A+M。
- 摘要机制：交叉熵可只捕获一部分有效预测特征，其他有效特征无法被发现；动力系统分析给出出现条件与解耦正则方法。
- 支持／反例潜力：是“较容易旁路先收敛，从而饿死新信息通道”的机制候选；不是任意未使用通路都必然受饥饿。
- **精读问题**：统计结构和参数化前提是什么？饥饿发生在表示学习还是读出？哪些训练史干预能分开“没学会”和“学会但不使用”？

### T07-034 — Complexity Matters: Dynamics of Feature Learning in the Presence of Spurious Correlations — 精读优先
- 作者／年份／版本：GuanWen Qiu、Da Kuang、Surbhi Goel；2024，v3。ID：`2403.03375`。[摘要](https://arxiv.org/abs/2403.03375)；[全文](https://arxiv.org/pdf/2403.03375v3)。A+M。官方元数据称 ICML 2024 正式题名为 **Complexity Matters: Feature Learning in the Presence of Spurious Correlations**，同一作品不重计。
- 摘要机制：控制核心／伪特征的复杂度和相关性，发现学习阶段未必可分，核心学会后伪特征也未必被遗忘。
- 支持／反例潜力：反驳“只看训练早晚就知道是捷径还是核心机制”；“后期学会核心”也不说明旁路已消失。
- **精读问题**：哪些去偏方法依赖阶段可分而失效？可观测的特征进度量是什么？一层 ReLU 的 XOR 分析可以外推到何种范围？

### T07-035 — Grokking: Generalization Beyond Overfitting on Small Algorithmic Datasets
- 作者／年份／版本：Alethea Power 等；2022，v1。ID：`2201.02177`。[摘要](https://arxiv.org/abs/2201.02177)；[全文](https://arxiv.org/pdf/2201.02177v1)。A+M。
- 摘要机制：小算法数据上，泛化可远晚于训练过拟合出现，数据规模影响所需优化时间。
- 支持／反例潜力：短跑未形成机制不等于机制不可能；但不能据此无限延长训练或承诺自然语言必会出现同样转折。
- 下一步：与进度量及因果形成实验联合读，明确何种证据才能合理增加训练预算。

### T07-036 — Progress measures for grokking via mechanistic interpretability — 精读优先
- 作者／年份／版本：Neel Nanda 等；2023，v3。ID：`2301.05217`。[摘要](https://arxiv.org/abs/2301.05217)；[全文](https://arxiv.org/pdf/2301.05217v3)。A+M。
- 摘要机制：在模加小 Transformer 中还原 Fourier 算法，定义连续进度量，区分记忆、回路形成和清理。
- 支持／反例潜力：准确率突变可能掩盖内部机制逐渐形成；终点梯度或终点消融不能代表训练全史。
- **精读问题**：哪些进度量预测后续行为而非事后拟合？消融是否检验必要性／充分性？如何避免对某一人工算法回路的专属指标过拟合？

### T07-037 — What needs to go right for an induction head? A mechanistic study of in-context learning circuits and their formation — 精读优先
- 作者／年份／版本：Aaditya K. Singh 等；2024，v1。ID：`2404.07129`。[摘要](https://arxiv.org/abs/2404.07129)；[全文](https://arxiv.org/pdf/2404.07129v1)。A+M。
- 摘要机制：在合成训练中持续钳制部分激活，分解驱动归纳头形成的三个子回路；研究形成时间与数据依赖。
- 支持／反例潜力：**持续训练干预**不同于收官点遮蔽，是训练形成因果证据的重要入口。摘要称头的加性不能外推为任意获取动作效用加性。
- **精读问题**：钳制如何影响其余网络补偿？控制是否匹配训练预算和激活分布？形成因果、当下消费因果及部署总策略效应分别如何测量？

### T07-038 — On the Emergence of Induction Heads for In-Context Learning
- 作者／年份／版本：Tiberiu Musat 等；2025-11-02 首发，v2（2026-01-08）。ID：`2511.01033`。[摘要](https://arxiv.org/abs/2511.01033)；[全文](https://arxiv.org/pdf/2511.01033v2)。A+M；预印本。
- 摘要机制：最小任务及修改架构下，训练受限于低维子空间，推导归纳头形成时间随上下文长度的二次渐近关系。
- 支持／反例潜力：提供可核查形成时间理论；结论仅针对特定改造模型，不能作长窗真实训练的普遍复杂度定理。
- 下一步：核查结构约束、学习率、初始化、数据分布及与 T07-037 的差异。

## F. 最邻近的查询访问／来源回访及相反结果（11）

### T07-039 — DynaKRAG: A Unified Framework for Learnable Evidence Control in Multi-Hop Retrieval-Augmented Generation — 精读优先
- 作者／年份／版本：Chenyu Zhou 等；2026，v2（2026-08-22）。ID：`2607.06507`。[摘要](https://arxiv.org/abs/2607.06507)；[全文](https://arxiv.org/pdf/2607.06507v2)。A+M；预印本。
- 摘要机制：共享状态条件策略控制继续／作答及证据动作，用相对立即作答的优势评分选择动作；动作更新状态并可启用新动作，终局再压缩证据。
- 支持／反例潜力：本轮**学习型证据动作效用**最近邻；不是已确认的多粒度来源回访组合，其摘要未证明可追溯下钻和动作互补估计。
- **精读问题**：优势标签是固定后续策略还是重新滚动？训练标签花费多少模型／检索调用？无效动作屏蔽是否泄漏答案？是否真的学习多步互补而非单步排序？

### T07-040 — Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection
- 作者／年份／版本：Akari Asai 等；2023，v1。ID：`2310.11511`。[摘要](https://arxiv.org/abs/2310.11511)；[全文](https://arxiv.org/pdf/2310.11511v1)。A+M。
- 摘要机制：学习检索／反思特殊 token，按需取段并评估证据和生成，推理期可调控制。
- 支持／反例潜力：直接说明“按需检索／自评”已有学习机制；反思标签不等于动作反事实净收益标签。
- 下一步：核查标签生成器、来源成本、阈值与引用评价；正式版入口待跨专题目录去重。

### T07-041 — Active Retrieval Augmented Generation
- 作者／年份／版本：Zhengbao Jiang 等；EMNLP 2023，v2。ID：`2305.06983`。[摘要](https://arxiv.org/abs/2305.06983)；[全文](https://arxiv.org/pdf/2305.06983v2)。A+M。FLARE 是文内方法，不另计作品。
- 摘要机制：预测下一句，用预测内容查询；遇低置信 token 则检索并重新生成。
- 支持／反例潜力：提供无需复杂价值学习的主动访问对照；低置信不代表原文值得读，也可能使错误预测引导错误查询。
- 下一步：核查触发指标、重新生成成本及检索失败后的停止／回退规则。

### T07-042 — Adaptive-RAG: Learning to Adapt Retrieval-Augmented Large Language Models through Question Complexity
- 作者／年份／版本：Soyeong Jeong 等；NAACL 2024，v2。ID：`2403.14403`。[摘要](https://arxiv.org/abs/2403.14403)；[全文](https://arxiv.org/pdf/2403.14403v2)。A+M。
- 摘要机制：用模型实际答题结果和数据集归纳偏置构造复杂度标签，在无检索／单步／迭代检索之间路由。
- 支持／反例潜力：结果驱动的效用监督近邻；以数据集身份或难度捷径预测路由的风险值得查，不把“复杂度”当真实因果机制。
- 下一步：列清每条标签需跑几种策略、是否同源评估、分布迁移是否失效。

### T07-043 — Sufficient Context: A New Lens on Retrieval Augmented Generation Systems — 精读优先
- 作者／年份／版本：Hailey Joren 等；2024-11-09 首发，v3（2025-04-23）。ID：`2411.06037`。[摘要](https://arxiv.org/abs/2411.06037)；[全文](https://arxiv.org/pdf/2411.06037v3)。A+M。
- 摘要机制：区分上下文是否充分、模型是否会用；即便不充分的上下文也可能有用，提出结合充分性信号的选择性生成。
- 支持／反例潜力：**信息存在、信息充分、被读取、被有效消费、最终答对不是同一个量**；可为效用标签的混杂分层。
- **精读问题**：自动充分性标注是否看见参考答案？标签误差怎样改变结论？如何构造相同来源、不同充分性和可消费性的同卷反事实比较？

### T07-044 — Adaptive Retrieval Without Self-Knowledge? Bringing Uncertainty Back Home
- 作者／年份／版本：Viktor Moskvoretskii 等；ACL 2025。ID：`2025.acl-long.319`，DOI `10.18653/v1/2025.acl-long.319`。[官方摘要](https://aclanthology.org/2025.acl-long.319/)；[全文](https://aclanthology.org/2025.acl-long.319.pdf)。A。
- 摘要机制：比较 35 种主动检索方法／不确定性方法、6 数据集、10 指标；摘要称简单不确定性技术常有较好效率与自知识表现、问答质量相当。
- 支持／反例潜力：本轮最直接的复杂主动访问**相反结果**，防止只收集复杂控制器的正例；并非说明所有价值学习都无用。
- 下一步：全文核查公平输入、检索器、阈值校准、训练成本与“自知识”评价是否可靠；适合与 T07-039 联合精读，暂不占 30 项主优先额度。

### T07-045 — RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval
- 作者／年份／版本：Parth Sarthi 等；2024，v1。ID：`2401.18059`。[摘要](https://arxiv.org/abs/2401.18059)；[全文](https://arxiv.org/pdf/2401.18059v1)。A+M。
- 摘要机制：递归嵌入、聚类、摘要构建多层树，从不同抽象层取信息。
- 支持／反例潜力：多粒度表示／检索是明确已有机制；摘要不等于已经验证按动作效用逐层下钻或原始来源回访。
- 下一步：与 T03/T04 去重，核查扁平展开取树节点和真正递归访问的区别，计算建树／更新成本。

### T07-046 — ArchRAG: Attributed Community-based Hierarchical Retrieval-Augmented Generation
- 作者／年份／版本：Shu Wang 等；2025 首发，v4（2026-05-11）；官方元数据关联 AAAI 2026，DOI `10.1609/aaai.v40i19.38619`。ID：`2502.09891`。[摘要](https://arxiv.org/abs/2502.09891)；[全文](https://arxiv.org/pdf/2502.09891v4)。A+M。
- 摘要机制：属性社区、LLM 层级聚类与层级索引，减少在线 token 成本并提高相关信息识别。
- 支持／反例潜力：多粒度／图索引和成本结合的近邻；建图、摘要成本与训练型动作价值是否存在须分开。
- 下一步：与 T03/T04 去重，检查原文映射完整性、跨层选择监督及证据被压缩后能否回到来源。

### T07-047 — A Human-Inspired Reading Agent with Gist Memory of Very Long Contexts — 精读优先
- 作者／年份／版本：Kuang-Huei Lee 等；2024，v3。ID：`2402.09727`。[摘要](https://arxiv.org/abs/2402.09727)；[全文](https://arxiv.org/pdf/2402.09727v3)。A+M。ReadAgent 是方法名。
- 摘要机制：模型划分记忆片段、压成梗概，再按任务需要主动回看原始段落；无需新架构的提示系统。
- 支持／反例潜力：本轮**压缩表示＋按需原始来源回访**最明确的已有组合。不能再把该组合本身写成空白；缺口可能在学得效用、粒度控制、完整成本与训练形成上。
- **精读问题**：梗概到原文的地址是否无损保存？一次／顺序回看和读取预算怎样比较？无回访、随机回访、全回访对照是否同算力？摘要制作和反复读写是否计入？

### T07-048 — Recursive Language Models — 精读优先
- 作者／年份／版本：Alex L. Zhang、Tim Kraska、Omar Khattab；2025-12-31 首发，v3（2026-05-11）。ID：`2512.24601`。[摘要](https://arxiv.org/abs/2512.24601)；[全文](https://arxiv.org/pdf/2512.24601v3)。A+M；新近公开作品。
- 摘要机制：把长提示作为外部环境，模型通过程序检查、切分并递归调用自身处理片段；摘要另报小规模后训练模型。
- 支持／反例潜力：程序化可变粒度原始片段访问的近邻；**不据摘要背书所报新模型或性能**，递归访问不自动具有成本最优动作效用。
- **精读问题**：源码定位和访问范围是否完整可追溯？后训练信号如何获得？工具调用、环境、子调用与失败重试成本是否齐全？不同版本是否新增训练结果，不能把 v3 内容倒填为 2025 首发结论。

### T07-049 — Shortcut Learning in Deep Neural Networks
- 作者／年份／版本：Robert Geirhos 等；2020 首发，v5（2023）；官方元数据关联 Nature Machine Intelligence，DOI `10.1038/s42256-020-00257-z`。ID：`2004.07780`。[摘要](https://arxiv.org/abs/2004.07780)；[全文](https://arxiv.org/pdf/2004.07780v5)。A+M。
- 摘要机制：综述／观点文，把标准基准有效而难测试条件失败的决策规则归为捷径，讨论解释与评价改进。
- 支持／反例潜力：为读控制器利用任务身份、位置或格式代替信息效用提供检查框架；不是针对某条具体路径的实验证据。
- 下一步：回溯文内具体失败任务，不把观点文当作训练动力学定理。

## G. 交互分解、反事实基线、标签成本与决策校准补充（6）

### T07-050 — Nonnegative Decomposition of Multivariate Information — 精读优先
- 作者／年份／版本：Paul L. Williams、Randall D. Beer；2010，v1。ID：`1004.2515`。[摘要](https://arxiv.org/abs/1004.2515)；[全文](https://arxiv.org/pdf/1004.2515v1)。A+M。
- 摘要机制：用冗余格和部分信息原子区分多源冗余及协同，解释交互信息负值中的混合含义。
- 支持／反例潜力：理论上直接提醒多源贡献不能只加单源分数；这是一种分解定义，不是行动价值或唯一公认协同度量。
- **精读问题**：该冗余定义有哪些已知反例？应追查后续修订／替代定义。能否构造最小 XOR 与重复来源任务，检验某效用仪器漏掉协同或重复计功？

### T07-051 — Counterfactual Multi-Agent Policy Gradients — 精读优先
- 作者／年份／版本：Jakob Foerster 等；2017 首发，v3（2024-12-11）。ID：`1705.08926`。[摘要](https://arxiv.org/abs/1705.08926)；[全文](https://arxiv.org/pdf/1705.08926v3)。A+M。
- 摘要机制：集中式 Q 评论器、分散策略；通过边缘化单个代理动作且固定其他代理动作构造反事实基线。
- 支持／反例潜力：可借鉴低成本信用分配；**固定其他动作的基线并不等于撤掉一个读取动作后允许后续策略适应的总效用**。
- **精读问题**：反事实基线究竟是方差缩减还是已识别的因果量？多动作联合删除／替换是否会改变排名？一步算完基线是否以训练一个昂贵 Q 模型为代价？

### T07-052 — Decision-Making Under Selective Labels: Optimal Finite-Domain Policies and Beyond
- 作者／年份／版本：Dennis Wei；ICML 2021。ID：`pmlr-v139-wei21a`。[摘要](https://proceedings.mlr.press/v139/wei21a.html)；[全文](https://proceedings.mlr.press/v139/wei21a/wei21a.pdf)。A。
- 摘要机制：某类决策下看不到结果标签；在线平衡取标签的成本与未来效用，有限域最优阈值随已收标签变化。
- 支持／反例潜力：拒读／停止动作会让未选动作长期缺标签，控制器可能自我确认；标签获取本身也是有成本的策略。
- 下一步：区分标签选择与输入特征选择，追查探索成本是否可映射到反事实读取试验。

### T07-053 — Calibrating Predictions to Decisions: A Novel Approach to Multi-Class Calibration — 精读优先
- 作者／年份／版本：Shengjia Zhao 等；2021，v1。ID：`2107.05719`。[摘要](https://arxiv.org/abs/2107.05719)；[全文](https://arxiv.org/pdf/2107.05719v1)。A+M。
- 摘要机制：针对有限下游动作集合而非完整类别分布做决策校准，可降低样本复杂度并改善实际决策。
- 支持／反例潜力：校准对象应是会改变读取／停止选择的差异，而不只是语言模型总体概率。
- **精读问题**：动作数、类别数、损失函数及最佳响应条件是什么？每个样本／历史拥有不同可用地址时是否仍适用？需多少独立动作结果标签？

### T07-054 — Dimension-Free Decision Calibration for Nonlinear Loss Functions — 精读优先
- 作者／年份／版本：Jingwu Tang、Jiayun Wu、Zhiwei Steven Wu、Jiahao Zhang；2025-04-22，v1。ID：`2504.15615`。[摘要](https://arxiv.org/abs/2504.15615)；[全文](https://arxiv.org/pdf/2504.15615v1)。A+M；预印本。
- 摘要机制：非线性损失下，标准确定性最佳响应的校准验证仍有维度相关下界；平滑最佳响应和有界范数函数类允许无维度依赖方案。
- 支持／反例潜力：直接限制把有限动作的线性决策校准无条件套到复杂组合效用；平滑化不是免费化解。
- **精读问题**：无维度依赖藏在哪些范数、平滑参数和动作数中？硬预算／离散停止与平滑响应是否冲突？该损失类能否表示动作互补？

### T07-055 — Graph Coloring for Multi-Task Learning
- 作者／年份／版本：Santosh Patapati、Ian Noronha；2025 首发，v5（2026-06-29）；官方元数据称 ECCV 2026。ID：`2509.16959`。[摘要](https://arxiv.org/abs/2509.16959)；[全文](https://arxiv.org/pdf/2509.16959v5)。A+M。
- 摘要机制：按梯度干扰图着色，将兼容任务分组，训练中重算分组并轮流激活；声称能改进底层多任务优化器。
- 支持／反例潜力：近期从单次梯度修改转向时间调度；仍是作者摘要主张，不背书通用改善或“每批兼容即全程无害”。
- 下一步：核查任务分组随训练的变化、估计噪声、组调度公平性和完整存储／时间开销；与训练史机制测量相接。

## 版本去重与待认领边界

1. T07-016 的 `1511.03722`／PMLR ICML 2016，T07-030 的 `2202.01017`／PMLR ICML 2022，均为一项。
2. FLARE、ReadAgent、SAGE、PCGrad、BRiG-AFA 等方法名不另增作品。正式题名更改见 T07-034；PMLR 重刊日期纠正见 T07-009。
3. T07-003 的 v5 证明修订、T07-048 的 v1→v3 后训练内容、T07-018 的 2026 版本都应全文逐版核查；本轮仅依据官方元数据登记差异线索。
4. T07-045／046／047／048 与 T03、T04、T06 高度交叉；T07 保留“效用、标签、干预及成本”问题，统一目录应按稳定 ID 合并，不因专题不同重复计数。
5. 「多粒度＋保留可回访来源」已有明确近邻 T07-047，另有 T07-045／046／048 的不同实现；「状态条件动作优势＋停止」已有 T07-039。**这不证明已有作品把两组机制按同一可训练接口完整合并；也不允许反过来宣称本组合全新。**
6. 不在 55 项中的待追线索、失败与排除项见 `SEARCH_LOG.md` 和 `HANDOFF.md`，不得计入已确认候选。
