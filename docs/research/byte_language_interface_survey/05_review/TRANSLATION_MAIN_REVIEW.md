# 主体三份译稿的独立双语审查

审查日期：2026-11-09。范围仅为最终主体三份英文与三份中文，以及 `TRANSLATION_NOTES_MAIN.md`。本报告不是译文摘要、清单译稿审查、英文科学性重审或原论文复现。

## 1. 结论与处理优先级

**结构完整性通过；技术忠实度有条件通过，建议先修复 4 项 P1，再处理 7 项 P2。未发现 P0。**

- **P0：0 项。** 未发现整节／整表／整道开放问题缺失、主要数值颠倒、复制上界假设被整体删除，或把 MtPC／TokSuite 未决事项直接裁定为已实测软件错误。
- **P1：4 项。** 当前未完成块被误称为局部块；摘要把已采样条件关系译成“样本内块”；两处把“可以消除未知符号而仍发生失败”收紧为“不能阻止”；parity 被系统译为“公平性”，混入原文刻意分开的规范性结论。
- **P2：7 项。** 概率质量用语、倍数减速表达、lemma／token 混淆、多峰性／多模态歧义、语言集合被称“人群”、abridgment 被译成“缩写”，以及少量命令式／防御性直译。

这是**完整译稿的局部修订意见**，不是要求重译或用摘要替换正文。八轴机制、两附录、八表、十五问题及关键来源限定均有对应。未发现一整段实质论证无中文对应；这不等于每句技术意义已经无误。译者说明第 89、100 行的零省略／条件全保留表述，应在修复下列局部失真后再作最终确认，不能以块数相同替代语义审查。

优先级定义：P0＝阻断发布的整体遗漏或重大结论／数学破坏；P1＝可改变机制、条件或结论含义，建议发布前修复；P2＝歧义、术语和行文修订，不改变总体证据方向。下面共 11 个修订单元；一个单元可能涉及多处同类实例，不把重复出现另算问题。

## 2. 独立性、输入快照与方法

遵循 [PLAN](../PLAN.md) 的完整翻译要求、证据状态区分和只读边界。完整逐段阅读三对文件，共 1,056 行英文和 1,056 行中文，另读主体翻译说明与 [CLAIM_RULES](CLAIM_RULES.md)。正文、摘要、问题单都独立检查，不以摘要替代长文。下文登记 **60 组成对实质段落／论证段**，跨越八轴，并另外列出数学和关键数字核对。

没有读取或修改项目外文件；没有网络上传、子代理、训练、安装、提交或推送；没有修改英文、译者文件、术语表或其他审稿文件。唯一写入为本报告。术语修订是对原文已有概念的译法建议，不新增研究概念。

### 2.1 文件代号与行号

以下代号只为使审查表可读；每个行号都指本次快照中的实际文件行，不是 PDF 行号。三对文件行号恰好对应。

| 代号 | 英文路径 | 中文路径 |
|---|---|---|
| S | `docs/research/byte_language_interface_survey/04_synthesis/SURVEY_EN.md` | `docs/research/byte_language_interface_survey/06_translation/SURVEY_ZH.md` |
| E | `docs/research/byte_language_interface_survey/04_synthesis/EXECUTIVE_SUMMARY_EN.md` | `docs/research/byte_language_interface_survey/06_translation/EXECUTIVE_SUMMARY_ZH.md` |
| Q | `docs/research/byte_language_interface_survey/04_synthesis/OPEN_QUESTIONS_EN.md` | `docs/research/byte_language_interface_survey/06_translation/OPEN_QUESTIONS_ZH.md` |

### 2.2 SHA256

| 文件 | 英文 SHA256 | 中文 SHA256 |
|---|---|---|
| S | `45cbcf639e1d5f598f823619313190ef8c2d64725ee5df95517fb754cb55e685` | `dce207d8efe6df6d093bb37678c526e84f46faa771f7cc138823846699a71e73` |
| E | `14317c35e9b1318b26e0d6218c7dc6c7eb5d02d619f20de5d5f530bf7633903b` | `fe448c866153296765d3711fb1022aba92b1fb579ac8ff039b31362afc2f4835` |
| Q | `814b75b0c01da61a3df072d7d047d79c982a6495b869d1d7f79b7e46870691e0` | `17b9170a343d86af73a2bdf2d6eb10498a88449853bbd4b64d5cfa1ab8c71415` |

主体翻译说明 SHA256：`a4874b63eafe52d65800ae27fcbc327408eca985a7fe4c5db7e9766f481ede00`。英文哈希与说明中的底本快照相同。

## 3. 全结构核对：不是只有标题计数

| 检查对象 | 英／中实计 | 结果 |
|---|---|---|
| S 行数／标题／空行分隔块 | 810／97／345，各自相等 | 标题所在行、级别、空行位置也逐项相同 |
| S 主节 | 1–16，顺序相同 | `s01`–`s16` 全保留；不是把目录项当正文节 |
| S 附录 | A、B | `appendix-a`、`appendix-b`，及 A.1–A.4 全保留 |
| S 表 1–8 | 8 个表块、91 行（含表头／分隔行） | 各表行数依次 14、12、8、9、12、11、14、11；逐行列数一致 |
| S 显示公式 | 1 块 | BPB 两行等式逐字符相同；行内数学另行人工核对 |
| E 行数／标题／块 | 79／11／40，各自相等 | 总标题加十个编号节；没有用 E 代替 S |
| Q 行数／标题／块 | 167／21／73，各自相等 | 五个大节、十五个 OQ 小节、一个总标题 |
| Q 开放问题 | OQ-01–OQ-15，全部有实质内容 | `oq01`–`oq15` 显式锚点顺序不变；研究比较 01–07、薄弱结果 08–11、规格核销 12–15 未互换 |
| Q 优先级表 | 1 表、6 行 | 行列次序与英文相同 |
| 总标题／块 | 129／458，各自相等 | 没有缺失的结构块 |
| Markdown 链接 | S 208、E 15、Q 28 | 共 251；9 外链和 242 本地链接目标均保留并核验 |
| 链接重定位 | 三译文间导航改中文，其他指回原材料 | 将这三种预期导航替换正规化后，全部链接目标及出现顺序一致；本地文件／锚点无缺失 |
| BIW／BIP 引用 | 每对文件有序出现序列相同 | 不是只比集合；重复引用也保留 |

独立只读 Python 检查以当前文件直接计算，不复用译者给出的结论。数字检查先枚举各行差异，再人工检查数值归属和比较方向；另比较全文件数字多重集。仅正规化 `Ninety-two`→`92`、`38 billion`→`380 亿` 后，E、Q 全等，S 只少一个重复模型名 `CharT5` 的末尾 `5`（第 173 行中文省重复主语，模型身份明确），不是丢失数值。数字换序如 PTB 参数／困惑度、TPU 型号／减速、训练字节／参数等均已回看其语义归属，不能由多重集相同直接宣布通过。

首版临时检查的正则转义报错，修正后检查完成；未产生脚本、日志或中间文件。其后显示公式检查曾有 Python 转义写法警告，不影响公式比较结果。纯 Markdown 审查未运行 pytest 或训练，不把文档检查当论文实验认证。

## 4. P1：建议发布前修复

引号内均为指定行的连续原文片段，不是审查者回译。

### P1-01：partial patch 被误换成 local patch

位置：`docs/research/byte_language_interface_survey/04_synthesis/SURVEY_EN.md:335` ↔ `docs/research/byte_language_interface_survey/06_translation/SURVEY_ZH.md:335`。

- EN：`Scratchpad Patching pools only the observed partial patch, runs the trunk, broadcasts the result, and overwrites transient state rather than committing another persistent patch.`
- ZH：`Scratchpad Patching 只池化已观察的局部块，运行主干、广播结果并覆盖临时状态，而非提交新的持久块。`
- 问题：此处关键是**尚未完成的当前块中，已经观察到的部分**，不是泛指“局部块”。partial→局部使刷新时机及因果可用性这一核心机制不再明确。Q:47 的“已观察的未完成块”译法正确，说明并非整个机制被遗漏。
- 最小修订：仅把 `只池化已观察的局部块` 改为 `仅池化当前未完成块中已观察到的部分`，保留其余句子。

### P1-02：sampled within-block conditionals 被译成“样本内块条件分布”

位置：`docs/research/byte_language_interface_survey/04_synthesis/EXECUTIVE_SUMMARY_EN.md:43` ↔ `docs/research/byte_language_interface_survey/06_translation/EXECUTIVE_SUMMARY_ZH.md:43`。

- EN：`Independent future heads provide parallel proposals, not sampled within-block conditionals.`
- ZH：`独立未来头提供并行提议，不是样本内块条件分布；`
- 问题：sampled 不是“样本内”。原文及 S:367 的区别是：未来偏移头不以此前已采样的块内字节为条件，不能因此构成局部自回归联合分布。中文引入了不存在的“样本内块”对象。S:367 本身保留了正确区别，摘要也须能独立读懂。
- 最小修订：`独立未来头提供并行提议，并非以块内先前已采样字节为条件的预测；`。

### P1-03：有失败反例，不等于“不能阻止”任何失败

位置：E:59 和 Q:94；S:577 的“不能可靠阻止”保留得较好。

- EN E:59：`Byte fallback can remove unknowns without preventing translation collapse.`
- ZH E:59：`字节回退可移除未知符号，却不能阻止翻译崩溃。`
- EN Q:94：`Byte fallback can remove unknowns without preventing translation collapse.`
- ZH Q:94：`字节回退可去掉未知符号，却不能阻止翻译崩溃。`
- 问题：英文的 can ... without 是可发生的组合／对“覆盖足以保证成功”的反例；中文无模态的“不能阻止”容易变成机制普遍无效的断言。本文证据不支持取消这层可能性。
- 最小修订：两处均改为 `字节回退即使消除了未知符号，仍可能出现翻译崩溃。`，或 `字节回退可消除未知符号，却不保证避免翻译崩溃。`。

### P1-04：parity 与 fairness 不应合并为同一个“公平性”

主要位置：S:5、559、587、722；E:59 首次只写 TP／IP 也应补清楚对象。

- EN S:559：`Length parity is a resource diagnostic, not task fairness itself.`
- ZH S:559：`长度公平性是资源诊断，不是任务公平本身。`
- EN S:587：`The dialect study defines tokenization parity as a language/English length ratio and information parity as an English/language total-NLL ratio.`
- ZH S:587：`方言研究把分词公平性（TP）定义为某语言／英语长度比，信息公平性（IP）定义为英语／某语言总 NLL 比。`
- 问题：原文分开**长度／信息比率或均衡程度**与规范性的任务公平。译文反复以“公平性”命名前者，虽后接“不是公平本身”的限定，却形成同词反复、削弱关键区分。没有改掉任何相关系数或制造 TP／IP 正负号冲突，但术语会诱导过度解释。
- 最小修订：S:587 改为 `方言研究将分词长度比（TP）定义为某语言／英语长度比，将信息比（IP）定义为英语／某语言总 NLL 比。`；S:559 用 `长度均衡程度是资源诊断，不等于任务公平。`；S:5 的 `位置公平性` 用 `位置消耗的均衡程度`，S:722 相应 `公平` 用 `长度均衡程度`。E:59 首次写 `方言分词长度比（TP）与信息比（IP）的关联`。定义与比值方向不动。

## 5. P2：最小术语与行文修订

### P2-01：probability mass 不能让读者误解为预测质量

位置：S:387 和 Q:127。

- EN S:387：`Accepted mass is min(p,q); the normalized positive residual (p−q)+ restores missing target mass after rejection.`
- ZH S:387：`接受质量为 min(p,q)；拒绝后归一化正残差 (p−q)+ 补回目标缺失质量。`
- EN Q:127：`Accepted mass is min(p,q)=(.5,.1), with rejection probability .4.`
- ZH Q:127：`接受质量 min(p,q)=(.5,.1)，拒绝概率 .4。`
- 问题：公式未错，但“接受质量”尤其在邻近任务质量／接受量讨论中像 quality；mass 应明确是概率质量。
- 最小修订：`被接受的概率质量为 min(p,q)`；`补回目标分布缺失的概率质量`。Q 同步。不改接受比、归一化残差或反例数值。

### P2-02：减速倍数写成耗时比，避免“两倍慢”的歧义

位置：S:171、672、675。

- EN S:675：`Dynamic implementation can train about twice as slowly as isotropic control`
- ZH S:675：`动态实现训练可能约为各向同性对照的两倍慢`
- EN S:171：`Table 10 reports 6.4–9.5× slower **XNLI** inference across the reported sizes on **TPUv3-32**; its XSum measurements instead use TPUv3-128.`
- ZH S:171：`Table 10 在 **TPUv3-32** 上报告，各尺寸 **XNLI** 推理慢 6.4–9.5×；XSum 则用 TPUv3-128。`
- 最小修订：S:675 用 `动态实现的训练耗时可能约为各向同性对照的两倍`；S:171 用 `各报告尺寸的 XNLI 推理耗时约为 mT5 的 6.4–9.5 倍`，保留硬件与 XSum 区分；表 6 同步。这里未发现倍率数字抄错，建议只消除中文读法歧义。

### P2-03：lemma 不是本文的 token／词元

位置：S:611、744。

- EN S:744：`Rare forms, held-out lemmas, direction, annotation and clean controls`
- ZH S:744：`稀有形式、留出词元、方向、标注及干净对照`
- EN S:611：`while similarity and lemma filtering lower trained-model scores`
- ZH S:611：`相似性与词元还原过滤降低训练模型分数`
- 问题：本文已用“词元”表示 token；held-out lemmas 是留出的词汇基本形，不是留出分词单元。中文也通常把 lemmatization 称词形还原，而非词元还原。
- 最小修订：S:744 用 `留出的词汇基本形（lemma）`；S:611 用 `相似性与词形还原过滤`。不改变筛选后的分数或训练／探针边界。

### P2-04：完整序列蒸馏中的 multimodal 是多峰目标，不是多种输入模态

位置：S:716。

- EN：`the fifth can reduce multimodal target variation.`
- ZH：`第五种可减少多模态目标变化。`
- 问题：上下文是完整教师序列减少候选目标的多峰／多解变异，不是图像、文字等输入模态。“多模态”在概率语境并非绝对不能用，但本综述兼有视觉相邻证据，此处易误读。
- 最小修订：`第五种可减少目标分布多峰性带来的变异。`，保留 can 的非必然性。

### P2-05：MYTE 的 population 应落在评估语言集合上

位置：S:567、E:57、Q:141、145。

- EN S:567：`The tables' population/aggregation relationship is unreconciled;`
- ZH S:567：`两表人群／聚合关系尚未协调；`
- EN Q:141：`How do MYTE's reported evaluated populations and aggregates relate?`
- ZH Q:141：`MYTE 报告的评估人群与聚合之间是什么关系？`
- 问题：此处要核销的是语言集合、运行与聚合权重，不是人的受试群体；中文把泛统计 population 机械译为“人群”。相关语言列和数字都正确，不构成新的结果错误。
- 最小修订：S/E 用 `评估语言集合／聚合口径`；Q 标题用 `MYTE 报告的评估语言集合与聚合结果之间是什么关系？`，Q:145 同步。一般用户公平语境的“人群”不必全局替换。

### P2-06：abridgment 应译为删节稿，不是缩写

位置：S:806。

- EN：`A complete translation should preserve their order and meaning, rather than replace the body with an abridgment.`
- ZH：`完整翻译须保留次序与含义，不能用缩写替代正文。`
- 最小修订：`完整翻译须保留次序与含义，不能用删节稿替代正文。`。当前交付结构并没有真的删节；这是附录中的交付约定词义错误。

### P2-07：局部防御性直译可收敛成直接、带条件的中文

不建议删除整段限制；下列限制各自有科学作用，只改语气和句法。

- S:567 EN：`A single reconciled MT ranking cannot be fabricated from them.`
- S:567 ZH：`不能捏造单一已协调 MT 排名`。
- 最小修订：`在这些差异厘清前，无法给出统一的机器翻译排名。` 保留未决状态及不合并两表的条件，不把“捏造”作为对读者的防御性指令。
- Q:129 EN：`Timings are not invalidated by association`。
- Q:129 ZH：`计时不因关联而失效`。
- 最小修订：`这一保证未核实，并不使已报告的计时结果失效。` 保留精确性／速度的分离，去掉无明确中文所指的“关联”。

总体行文虽偏紧、常有“不是……”“不能……”结构，但多数承载原文的必要区分，不能为降低防御感而删除。尤其不得删掉 ByT5 的工件／运行边界、H-Net 的参数与近似预算、复制界的状态唯一通路或 MtPC／TokSuite 的开放状态。

## 6. 六十组成对实质抽检登记

每行的 S/E/Q 对应 §2.1 的两个完整路径；两侧行号相同。摘录为原行中的连续文字，略去的其余句子也已阅读；本表不是用零散名词冒充段落抽查。“通过”指该行列出的核心语义和所在论证条件保留，不取代 §4–5 的局部修订。数学全文及额外关键数值另见 §7。

| # | 对应行／轴 | 英文原文摘录 | 中文原文摘录 | 结论 |
|---|---|---|---|---|
| 01 | S:33，四接口 | `It need not change all of them.` | `并不必同时改变所有连接。` | 字节接口不必覆盖全部环节，通过 |
| 02 | S:41，证据计数 | `not 296 independent scientific problems or successful experiments` | `不等于 296 个独立科学问题或成功实验` | 141／137／296／92 及 FULL 界限通过 |
| 03 | S:56，byte／code point／character | `surrogate code points are not Unicode scalar values and cannot occur in legal UTF-8.` | `代理码点不是 Unicode 标量值，不能出现在合法 UTF-8 中。` | 八位、1–4 字节、码点／标量／字素／受限字符分开，通过 |
| 04 | S:58，规范等价 | `A complete valid scalar can be the wrong scalar.` | `一个完整合法标量也可能是错误标量；` | 合法、正确和原字节保留分开，通过 |
| 05 | S:91，上下文 | `A context of 1,024 model symbols is not a context of 1,024 bytes, scalars, graphemes, or words.` | `1,024 个模型符号的上下文，不等于 1,024 字节、标量、字素或词。` | 原文量／内部距离通过 |
| 06 | S:102，历史压缩 | `Wikipedia was 1.60 versus 1.51 bits per transformed character.` | `Wikipedia 上是每个变换后字符 1.60 对 1.51 比特。` | PAQ 胜负与变换后字符单位通过 |
| 07 | S:108，梯度与状态 | `A short gradient horizon therefore need not imply equally short forward history` | `因此，短梯度跨度不必意味着同样短的前向历史` | 49／10,000／205／100 字节归属通过 |
| 08 | S:122，组合与预算 | `Its often-cited approximately 60% saving uses a different published 52M comparator, not that 20M baseline.` | `常被引用的约 60% 参数节省，参照的是另一已发表的 52M 模型，不是这个 20M 基线。` | 19M/20M/52M，78.9/85.4/84.6/92.6，吞吐通过 |
| 09 | S:124，ELMo 共享 | `while directional LSTMs remain separate.` | `方向性 LSTM 则保持独立。` | 方向间共享不冒充输入输出绑定；PARTIAL 保留 |
| 10 | S:130，字节 BPE | `The LM predicts 50,257 merged symbols, and its context is 1,024 model tokens.` | `LM 预测 50,257 个合并符号，上下文为 1,024 模型词元。` | 不改成逐字节生成，通过 |
| 11 | S:151，ByteNet | `Table/prose result discrepancies in arXiv:1610.10099v2 remain source-reporting issues rather than evidence that dilation failed` | `arXiv:1610.10099v2 表格与正文的结果差异，仍属于来源报告差异，不是膨胀机制失败的证据` | 源／目标可见性和报告差异通过 |
| 12 | S:157，SDD | `Group boundaries cannot automatically compensate for a weaker recovery interface` | `组边界不能自动弥补更弱的恢复接口` | 16.56/19.46/19.98 与 28.62/27.49/27.27 对照通过 |
| 13 | S:171，ByT5 | `The corresponding grapheme-to-phoneme word error rates are 15.4% versus 43.5%, a different error unit.` | `相应字素到音素的词错误率为 15.4% 对 43.5%，是另一种误差单位。` | CER/PER/词错误率和三种 TPU 通过；倍数行文见 P2-02 |
| 14 | S:173，CharT5 | `It is neither an unrestricted code-point-only model nor a pure byte-step model.` | `它既不是不受限的纯码点模型，也不是纯逐字节模型。` | 47,198、回退、1.23B、36/12、1,376、11% 及三任务近对照通过 |
| 15 | S:181，CANINE | `Bucket collisions mean this is not exact original-code-point probability.` | `桶碰撞意味着这不是精确原码点概率。` | 子词监督／部署无分词器分开，通过 |
| 16 | S:208，稀疏计算 | `The table supplies no time unit.` | `表头未给时间单位。` | 1.00/.99/1.13 与 1.31/.55/.35 不擅加秒；音频／语言分开 |
| 17 | S:210，Reformer | `None of these reduces the number of text positions.` | `三者都不减少文本位置。` | 连接、激活、执行分块及 QK 共享通过 |
| 18 | S:218，Transformer-XL | `compare reuse with uncached full-window recomputation.` | `比较的是复用与无缓存的整窗重计算。` | 800→363×、3,800→1,874× 对应正确，不升级服务加速 |
| 19 | S:228，ACT | `The reported errors are training-set errors and fairly similar with and without ACT` | `所报错误是训练集错误，ACT 与非 ACT 颇接近` | 字节内转移、近似梯度、非墙钟通过 |
| 20 | S:254，聚合算子 | `a mean loses order unless its members are contextualized or position-coded` | `均值若成员未经上下文化或位置编码则丢失顺序` | 边界／内容／计算压力三分通过 |
| 21 | S:262，SpaceByte | `The preferred policy changes by domain` | `偏好策略随领域变化` | PG-19 与 arXiv 三个 BPB 不换顺序，非单因素比较 |
| 22 | S:270，MANTa | `This is a differentiable membership approximation, not exact marginalization over every discrete segmentation.` | `这是可微成员关系近似，不是对所有离散分段的精确边缘化。` | 四分之一上限和无瓶颈退化通过 |
| 23 | S:280，H-Net 主预算 | `so this is not equal-parameter evidence.` | `所以不是等参数证据。` | 四系统准确率／GFLOPs、1.3B/1.6B、文本近似匹配通过 |
| 24 | S:282，H-Net 跨域 | `making dynamic and space nearly tied on code.` | `动态与空格在代码上近乎持平。` | 中文／代码两组数字与领域预算通过 |
| 25 | S:284，策略梯度 | `Discounting deliberately introduces bias` | `折扣有意引入偏差` | Jensen 下界、1.280/1.299/1.386 及非答案准确率通过 |
| 26 | S:290，熵与置信度 | `Entropy is uncertainty over possible next bytes before the actual byte is observed.` | `熵是观察实际字节前对可能下一字节的不确定性。` | 观察前分布／已观察标签、停止梯度、100M/512 分开 |
| 27 | S:292，BLT | `but the space arm comes from an earlier version without cross-attention.` | `但空格分支来自无交叉注意力的早期版本。` | 七赢四、4T/4.5T/6T、68.9/67.2/67.4 归属通过 |
| 28 | S:296，效用信号 | `The signal can improve a tightly controlled intermediate event without solving the whole task` | `信号可以改善严格控制的中间事件，却未解决完整任务` | 19.0→67.1、67.8、4.8/51.4、自由约2% 通过 |
| 29 | S:317，Hourglass | `but the shifted-input residual can still transmit the immediately previous symbol` | `但移位输入残差仍能传递紧邻前一符号` | k−1 移位、缩短分支与残差分开，不造独立性／泄漏结论 |
| 30 | S:329，前缀稳定 | `This refutes universal prefix stability, not an actual leak-rate measurement for the Llama tokenizer in byte-simulation experiments.` | `这反驳普遍前缀稳定性，不是字节模拟实验中 Llama 分词器实际泄漏率的测量。` | bc/ab 反例与实测边界通过 |
| 31 | S:335，瞬态刷新 | `pools only the observed partial patch` | `只池化已观察的局部块` | P1-01；其余提交／丢弃依赖路径保留 |
| 32 | S:367，未来头 | `Earlier hidden slots are not earlier sampled byte identities.` | `先前隐藏槽位不是先前采样字节身份；` | 主文通过；摘要同义表达有 P1-02 |
| 33 | S:375，MtPC 资源 | `Higher rank improves acceptance and loses throughput.` | `高秩增加接受、降低吞吐；` | 730M/21M、三接受量／吞吐、batch-one／排除预填充通过 |
| 34 | S:377，MtPC 保证 | `this is not a measured released-code bug and does not invalidate throughput.` | `这不是测得的发布代码缺陷，也不使吞吐结果失效。` | 算法规格／解释反例／实际软件未知三层保留 |
| 35 | S:387，随机校正 | `Temperature and top-p transformations must be included inside the actual p and q used by the ratio.` | `温度和 top-p 变换必须计入比值所用实际 p、q。` | 接受比／残差／可选奖励正确；mass 译法见 P2-01 |
| 36 | S:398，概率事件 | `the denominator does not make their numerators identical.` | `分母相同不使分子相同。` | 链／路径／字符串／前缀／标记／去噪六对象保留 |
| 37 | S:400–407，BPB | `N is not padded array length.` | `N 不是填充数组长度。` | 显示公式相同；EOS、提示、窗口、总量加权条件通过 |
| 38 | S:409，转换 | `word perplexity is 2 raised to BPB times their ratio.` | `词困惑度为 2 的“BPB 乘二者比率”次方。` | 826,189/159,658 方向、处理语料与 UNK 限制通过 |
| 39 | S:421，Exact Byte | `masking and renormalizing that mass changes the original distribution.` | `掩蔽并重新归一化会改变原分布。` | 规范支持集精确性未扩为任意神经模型路径边缘化 |
| 40 | S:437，TokSuite | `the actual run-to-log-to-Figure 6 transformation remains unknown.` | `实际运行→日志→Figure 6 变换仍未知。` | 错文字不推成运行错误；独立排序／同文本对照／Gemma40例保留 |
| 41 | S:460，绑定算术 | `the saving is 524,288 parameters.` | `节省 524,288 参数。` | Vd 与偏置／桥接排除正确，分析核算不冒充实测 |
| 42 | S:468，ByT5 共享 | `Encoder/decoder input shared; decoder input/output unshared` | `编码器／解码器输入共享；解码器输入／输出不共享` | XNLI 百万步初始化、可变 gin／固定 Mesh、运行依赖／别名未知全保留 |
| 43 | S:485–491，读出几何 | `Learned scales or hidden norms change the bound.` | `可学习尺度或隐藏范数会改变上界。` | 点积、行归一化、完整余弦、2.8% 上界及秩方向通过 |
| 44 | S:497，独热负对照 | `The study identifies a training-recipe interaction, not intrinsic embedding-free superiority.` | `研究揭示训练配方交互，而非无嵌入内在优越性。` | 整词元抹除／逐元素 dropout、译入英语差 .45 BLEU 通过 |
| 45 | S:532，转换 | `The severe failure belongs to that configuration` | `严重失败属于该配置` | 等20B、70.7/31.2、73.6/46.7；不推广至 Bolmo 全路线 |
| 46 | S:542，外推 | `not an observed four-point maximum-checkpoint gain.` | `不是观察到的最大检查点提高四点。` | 44.6/44.4、30.94%、1.8×10^21、额外教师成本通过 |
| 47 | S:565，MYTE 长度 | `not an absolute length increase for Santali` | `不是桑塔利语绝对长度增加` | 305→145、131→109、365→365、2.80→3.35 全保留 |
| 48 | S:567–569，MYTE 修正 | `not target-language bytes.` | `不是目标语言字节。` | Table 4/8 两模型／两列／不同符号、+1 分母和聚合未决保留 |
| 49 | S:587–589，方言 | `it does not unambiguously contradict the negative TP column.` | `不构成与负 TP 列无歧义的矛盾。` | 相关系数／IP 指代通过；parity 术语见 P1-04 |
| 50 | S:603–605，Unicode | `Invalid-byte-ignore decoding can hide failures by dropping bytes` | `忽略非法字节的解码可通过丢字节隐藏失败` | 96.21/50.47、部分进展／完整合法／预期标量分开 |
| 51 | S:613–615，字符技能 | `the onset threshold is above **0.5%**, not 50% mastery` | `起效阈值是超过 **0.5%**，不是 50% 掌握` | 低阈值非掌握；四类CharBench均值通过 |
| 52 | S:623，复制界 | `Each retained state determines at most one correct answer` | `每个保留状态最多决定一个正确答案` | 完整假设、上界和 b 不等式均通过，详 §7 |
| 53 | S:640–644，缩放 | `This fitted N is not whole-resident parameter storage` | `拟合 N 不是全部驻留参数存储` | 两论文各自 N／FLOP 口径、3:1 混合主干、前沿反转保留 |
| 54 | S:650–656，文本接触与代理 | `Retention and repetition must be counted after packing and filtering` | `保留和重复须在装箱过滤后计数` | 30.4–43.5%、四分词器文本对照、压缩／质量负例通过 |
| 55 | S:731–753，评估设计 | `A strong frontier point does not isolate why it wins` | `强前沿点不隔离胜因` | 三设计、统计单位／地板／最差群通过；表8 lemma 见 P2-03 |
| 56 | S:779–810，两附录 | `A version, alias, appendix, or repeated citation does not become another entity.` | `版本、别名、附录或重复引用不另成实体。` | 计数／阅读状态／引用链／术语约定实质保留；abridgment 见 P2-06 |
| 57 | E:43、59–65，摘要独立阅读 | `not sampled within-block conditionals.` | `不是样本内块条件分布；` | P1-02、03；摘要其余事件／复制限制未删 |
| 58 | Q:94–98，复制评估 | `arms permitting replay or external access require their own storage, access, and pass budgets` | `允许重读或外部访问的分支需自行列存储、访问和遍数预算` | 不能滥用状态唯一通路界；覆盖句的模态见 P1-03 |
| 59 | Q:125–129，MtPC 反例 | `This is an analyst counterexample to the specified discard-and-ordinary-restart interpretation, not released-code execution.` | `这是分析者针对指定“丢弃后普通重启”解释的反例，不是执行发布代码。` | (.5,.5)/(.9,.1)、.4残差、(.7,.3) 及实际分支未知保留 |
| 60 | Q:134–156，三个规格核销项 | `Wrong explanatory wording does not prove the figure executed that formula` | `说明文字错误不证明图执行该公式` | TokSuite图未知、MYTE行列已纠正但聚合未决、实际边界未测泄漏，分别保留 |

## 7. 数学、关键数值及敏感修正的专门核对

### 7.1 全部主要数学关系

以下为所核对的原式／论证，不是建议添加到译文的新推导。

1. **单位、字母表与状态量。** S:56 的八位字节、UTF-8 1–4 字节、码点／标量／字素区别；S:346 的平坦 k 字节头 `256^k` 种结果，未误写为 `256k`。S:270 的 Bernoulli 前沿、Poisson-binomial 累积块索引与截断高斯近似，未改成精确离散分段边缘化。
2. **学习目标。** S:284 的期望条件对数似然、Jensen 下界、得分函数与折扣偏差，仍是原有主张而非无条件无偏保证；S:290 的观察前熵与 `1−已观察下一字节概率`、停止梯度区分保留；S:278 的比例损失不等于逐样本硬配额。没有把这些目标互译成“语义边界”。
3. **因果索引。** S:315 的全局移一整块／局部移一字节，S:317 的额外 `k−1`，S:329 的 `[ab]` 对 `[a,bc]`，符号与先后关系均在。Hourglass 译文保留 shifted residual 的前一符号通路，没有恢复已纠正的“组内完全独立”说法。
4. **BPB。** S:402–405 的显示式逐字符一致：

   ```text
   S_bits/original_byte = L/(B ln 2) = CE_mean_nats × N/(B ln 2).
   ```

   L 是自然对数损失总和，N 是有效标签数，B 是对应原文字节数。S:407、E:65、Q:134–138 保留 bit 日志不再除 ln2、不是填充长度、提示／EOS／重叠／加权条件。没有把路径换分母当成完成字符串边缘化。
5. **lm1b 重表达。** S:409 的 `2^(BPB × 826189/159658)` 方向正确，826,189 是字节事件、159,658 是词事件；同一处理语料、换行／EOS 约定、不能恢复 UNK 都未删。中文用了文字式而非新增显示公式，但数学关系完整。
6. **随机接受与残差。** S:387 的 `min(1,p(x)/q(x))`、接受概率质量 `min(p,q)`、拒绝后归一化 `(p−q)+`、全部接受可选 target bonus 均保留。Q:127 的 `p=(.5,.5)`、`q=(.9,.1)`、接受质量 `(.5,.1)`、拒绝 `.4`、正确贡献 `(0,.4)` 与错误重启贡献 `.4p=(.2,.2)` 导致 `(.7,.3)`，逐项一致。只是 mass 的中文应修，见 P2-01。
7. **参数算术和头几何。** S:460 的两表与一表之差 `Vd`，`256×2048=524288` 正确。S:485 的 `wᵢᵀh`、`wᵢᵀh/||wᵢ||`、`s·wᵢᵀh/(||wᵢ||||h||)` 均保留；行归一化保留隐藏幅值、完整余弦移除该通道的方向未反。
8. **置信度上界与秩条件。** S:489 的未缩放 logit `[−1,1]`、`e²/(e²+V−1)`、V=256 约 2.8% 正确（独立算术约 0.0281607）。S:491 的满行秩 `d≥V` 与 `ZᵀZ=I_d` 需要 `V≥d` 没有对调；“代数可达”不变成“能训练成功”。
9. **集合反例。** S:548 的 `aaaa`／`aaaaa` 同有 `{_aa, aaa, aa_}`，二值不重复三元组而非计数多重集，未暗改成实际发布软件碰撞。
10. **状态唯一通路的复制界。** S:623 完整保留：均匀长度 L、D 符号输入；读完才开始确定性输出；所有输入相关影响只经有限可区分保留状态 S；未计源重读、外存、提前输出及旁路排除。式为：

    ```text
    success ≤ min(1, |S|/D^L)
    b = log₂|S|
    success ≥ 1−ε  ⇒  b ≥ L log₂D + log₂(1−ε),  0≤ε<1.
    ```

    负的 `log₂(1−ε)` 没有被误改正号或删除。E:61 与 Q:94–96 也保留“读入完成后／所有通路计数”，未推广至边读边回显或自然语言不可能定理；允许重读／缓存的臂须另列其资源预算。中文 S:623 的“D 个符号上的均匀长度 L 输入”略压缩，结合上下文及 Q:94 含义明确；若顺手润色，可写“在大小为 D 的字母表上均匀抽取的长度 L 字符串”，不另列阻断问题。
11. **时耗换算。** S:674 的 132→93 秒，减少 `39/132≈29.545%`、速率比 `132/93≈1.41935`，与 29.5%／1.42× 相符。没有把减少 29.5% 译成“快 29.5 倍”。H-Net／ByT5 减速数字也未换值，但表达建议改成耗时比。

### 7.2 关键比较与更正边界

下列不仅核对数字存在，也核对模型顺序、指标、单位、硬件、适用预算及结论强度。没有发现未解释的数值丢失或顺序翻转。

| 位置 | 核对内容 | 结论 |
|---|---|---|
| S:110、114、122 | 静态／动态1.67→1.33；38 billion→380亿；19M/20M对照与52M的60%节省；78.9/84.6/92.6；1500/3000词每秒 | 数值、条件及单位正确 |
| S:149、155、157、163 | 芬兰13.10/13.98；老挝9.2/5.9/6.4/6.5；SDD两组BLEU；CharacterBERT55/26.5小时 | 负例未消失，非普遍细输入胜出 |
| S:171、173；表6 | ByT5 CER10.5/18.1、PER1.8/6.7、形态89.7/75.7、G2P词错误15.4/43.5；4.1字节；TPUv3-64训练约.75×、TPUv3-32 XNLI6.4–9.5×、XSum128；CharT5三任务79.0/79.7、87.6/87.7、11.2/11.5 | 指标和硬件不互换；见P2-02的中文倍数措辞 |
| S:183、185、191 | CANINE127M→167M、74.0→86.7、mBERT87.8；SELECTP+2.8/MINSPAN+5.7；6400/9000/900；Perceiver81.0/71.5、201M/20M、109B/113B | 容量、吞吐及不同消融角色保留 |
| S:202、208、218、220、272 | 1.06、.874→23.0；稀疏三质量／时间；XL363×/1874×及对应长度；3072槽.97/4096槽1.00；MANTa2.61/9.06/1.13秒与16V100 | 未升级成质量匹配的因果服务结论 |
| S:262、280–284；E:35；Q:29 | SpaceByte两领域三分数；H-Net BPE55.5/.69、space57.1/.70、one-stage56.2/.72、two-stage58.2/.69；1.3B/1.6B、8192字节/1792GPT-2词元；中文59.9/62.9/66.3、代码.3376/.3163/.3161；策略1.280/1.299/1.386 | H-Net正结果充分保留，预算近似和非边界单因素归因也保留 |
| S:292–298 | BLT七项赢四、约4T/4.5T/6T、ARC68.9/67.2/67.4、旧空格无交叉注意力；SOMBRERO .6701/.6571/.6578/.6568、5×/1.95/839B；效用中间值与自由生成反差 | 不把系统比较当熵唯一优势或独立重复验证 |
| S:304、323、337、369、375、383；表6 | MrT5删除50%、44.29→29.99ms与EM/F1下降；.04/25.49；scratch48→54.2与5.7×→2.9×；LCA210.42→164.18、τ=.75、另2.1–2.3×无缓存；MtPC三接受量及吞吐；3.3×在k=8非k=10 | 更高接受／可见性合法不被误写成充分质量或更快 |
| S:429、456、458、481、487、497 | +2.88nats≈17.8倍且非逐词保证；66M/78.4→51M/74.3；77.7/74.7/73.9/73.2；70%、35.71→36.64；29.3/29.9/29.7；.45BLEU | 观察、背景理论、配方依赖均在 |
| S:468，表5 | ByT5 encoder/decoder输入共享但decoder输入/输出不共享；Large XNLI可变gin、百万步初始化、Mesh4758510固定定义 | 没有外推所有尺寸／移植，没有冒充运行张量别名核验 |
| S:512、530–542 | 1.062/1.158/2.482/1.068、235M/219M；43.1B+172.9B转换；等20B两任务；512类；GSM/MMLU任务反转；60.50/39.06、66.31/25.43；10.4秒每100–150字节四3090、两天；44.6/44.4非四点、30.94% | 目标／适配／教师成本和观察／外推分开 |
| S:557、563、565–571 | 掸语3.94/1.42、粤语.87/.31；189/204、1.4900/1.4854；MYTE长度／相对比；MAGNET44.62/44.61/41.06、印地29.18→21.23、泰卢固68.63→53.90 | 长度／覆盖不升级成任务公平 |
| S:567–569；E:57；Q:143–147 | **Table8 MyT5低资源/总体21.1/21.8；ByT5 21.9/23.1**；Table4低资源20.4/20.1反向；十五列/十四名称、Maltese/Shona/Marathi；平行英语字节+1非目标BPB、250K步非同预算 | 已纠正的行列没有复发；未擅自解决语言集合／聚合矛盾 |
| S:587–589 | TP Phi+.638、mBERT+.4836、Llama−.380；IP Phi−.413/Llama+.268 | 译文未制造确定TP正文矛盾，亦未增显著性；但术语需P1-04 |
| S:581、595–615 | XTREME14.6/37.6、37.5/21.8与70/39不同口径；自然噪声两组退化与混合四分数；96.21/50.47；拼写32.9→16.5、93.5、1000后差<.01；**0.5%非50%**；CharBench77.34/47.96/43.64/32.37 | 可恢复／可用、合法／预期、监督低阈值／掌握均分开 |
| S:640–656、680 | 988/320、50M–6.7B、4B–1.1T、5×10^18–2×10^21；3.69→3.33；3.3B长度4的74.1对6.7B长度8的68.2；3:1混合主干和N排除；30.4–43.5%；四分词器104.86B/114.89B/100.23B/169.80B；τ .33/−.07/.87；PathPiece1.26B44%对BPE1.49B50%；Bolmo125/150与6.6 | 参数、估计计算、保留文本、吞吐前沿没有混成一个公平预算 |
| S:779–789 | 136+1+3+1=141；137研究文献非原生模型数；283+3+10=296；两种不同506关系；92=30+62、62=60+2；233+4+53+3+2+1=296 | 两附录的计数／证据状态没有删减或抬高阅读信用 |

## 8. 建议核销方式与本次未做事项

1. 译者按 §4 修复四项 P1，按 §5 逐项接受或说明 P2；不需改英文底本或再做论文训练。
2. 修后重新检查 16 节／两附录／8 表／15 问题、同序链接／标识符，以及本报告点名的对应句。若保持单行对应很好；若为中文自然分段调整行数，应保留段落映射而非追求机械同长度。
3. 更新主体翻译说明中的最终哈希与自检描述，不能继续用本报告记录的旧中文哈希代表修订版。
4. 本报告**没有执行这些译文修订**；也未核销 MtPC实际优化封装、TokSuite实际Figure6流水线、MYTE聚合或实际离线边界前缀稳定性。这些是原英文明确保留的开放事项，中文多数忠实保留，不是本次译审要替作者解决的缺口。
5. 未审查完整清单、分类译稿或其他翻译团队的产物；本报告不为那些文件背书。未新增 FULL 阅读或实验信用。

最终判断：可以确认这是真正的完整主体翻译，而不是摘要替代；科学骨架和关键更正总体忠实。当前不宜宣称“所有实质条件逐句无误”；修完四项 P1 后即可进行局部复核，无须推倒重来。

## 9. 交付前复核记录

- 内联只读 Python：60 行抽检编号恰为 01–60；逐一将表中英文／中文引文与所标原文件行范围作子串核验，**120 个引文全部匹配，0 处错引**；P1／P2 标题实计 4／7。
- 再算六份终稿和主体说明的 SHA256：**七个输入均与 §2.2 快照相同**，审查未改动底本或译稿。
- 报告 UTF-8 无替换字符、无尾随空白。`git status --short` 与进入任务时同为既有未跟踪目录／bundle 列表；定向 `git status --short --untracked-files=all -- docs/research/byte_language_interface_survey/05_review/TRANSLATION_MAIN_REVIEW.md` 确认新增的指定报告。未生成需要清理的脚本或测试输出；其余既有未跟踪文件原样保留。
