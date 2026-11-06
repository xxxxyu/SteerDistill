# 2026-11-06 新训练案例原始证据核查（新增候选分组）

本报告覆盖 selected-training-data 九例中的酒店、预约与五个 BFCL 案例，以及 long-context 新搜索中的两例。资产与银行卡案例由并行报告覆盖。只读核查原始 before/reference/steering/after、完整相关 reasoning、局部 gate 和未指导续跑；未修改网站、未重跑模型。

## 结论与优先级

| 顺位 | 案例 | 实际差异及阅读价值 | 判定 |
| --- | --- | --- | --- |
| 1 | `multi_turn_long_context_50` 解锁后开灯 | 无指导把工具目录序号拼进工具名，反复调用失败；正确指导明确 `lockDoors` 与 `setHeadlights`，先解锁四扇门，通过与 reference 相同的写状态检查，再移除指导开灯。完整相关 reasoning 与实际动作一致。任务短、动作因果清楚 | **可制作训练候选**。局部写状态闭环已成立；不是消融优势案例（该轮其他设置也都成功）。研究信息偏工具寻址，优先级低于有实质策略修正的案例，但证据较干净 |
| 2 | `multi_turn_base_37` 先建文件，再写第二个匹配句 | 原 before 向不存在的文件写错误片段，随后建文件但仍写错。最终选中 retry 明确辨认第二个匹配句，先 `touch`，局部与 reference 空文件状态一致；撤除指导后写入正确句子，终局通过。reasoning 中的句子计数混淆有明确自我更正 | **有条件候选**。最终指导正确、动作可读；但选中 attempt-2 吸收了前次完整续跑的终局 GT 反馈，不能说它仅靠局部核验自动找到了句子错误。可作为最终修正行为例，是否作为论文同协议训练闭环例需确认下面的反馈来源 |
| 3 | `multi_turn_base_92` 补足油量 | before 加 50 升导致超过油箱容量；after 明确解决 fuelAmount 是增量的疑惑，查得 10.5 后加 39.5 达到 50。因果清楚，完整 student reasoning 中有明确更正 | **暂缓**。局部步是只读查询，仅检查状态不变，没有核验读出的 10.5；Teacher analysis 又叙述了不存在的补油后行程核验。不能靠正确调用遮住指导依据问题 |
| 4 | `multi_turn_base_110` 登录后提交工单 | before 首次未登录，但会自行登录重试；真正终局失败在把用户名和密码混入工单描述。after 首先登录，移除指导后提交干净描述 | **不优先**。指导主要修复登录前提，不能把终局失败全部归因于缺少登录；请求原文引号不闭合，描述边界也不够干净。局部登录写状态证据可留作备选 |
| 5 | `multi_turn_base_188` 查询发票 | before 工具名/参数错后改成用 insurance_id 查询，不存在；after 用 latest_reservation 正确读取发票，再加保险费 | **跳过**。after reasoning 称上下文未提 insurance_id，实际前文已有；读操作 gate 未核验返回。理解上下文的代价较高 |
| 6 | `multi_turn_base_192` 发票接口名 | before 反复拼错 `retrieive_invoice`；after 调用正确的 `retrieve_invoice` | **跳过**。after reasoning 仍先声称工具名为另一错误拼写 `retriebe_invoice`，没有明确更正该说法；仅正确调用不足以构成高标准正例。且是只读空状态 gate |
| 7 | `multi_turn_long_context_163` 十一月机票 | after 首次就按 11 月 16 日查价订票；before 先错用日期和机场形式，但其完整 reasoning 已明确反思并改为 11 月 16 日，最后订对了 | **跳过**。不能写成 before 最终订错日期；差异更多在早期查询及预期回复。任务日期措辞本身曲折，与既有十一月案例重合 |
| — | `booking_2_2` 酒店预算 | before 把 under 220 写成 220；after 写成 210 并补 Downtown Seattle Hotel | **旧问题未解决，跳过**。原始任务及先前工具返回没有 210 的价格来源，也没有查询得来的酒店；指导直接指定它。通过预算 SQL 不能证明虚构的酒店及价格是正确决策 |
| — | `booking_and_scheduling_11_4` 同日预约 | 新 before 因列表漏显示 08:00 而补建重复时段；after 直接订已有 08:45 时段。Teacher 指导却仍主要强调 same-day 标记 | **旧问题未解决，跳过**。执行日期与预约日期仍不一致，且当前失败机制已不是缺 same-day 标记；指导与新 failure 的对应不清楚 |

## 局部 gate 与续跑：本次真正改善了什么

五个 selected BFCL 及两个 long-context 的 `after/local_gate.json` 都记录 `checked_before_continuation: true`、`execution_valid: true`、与 reference 相同的 `actual_state` / `target_state`。criterion 明确写为：`Successful tool execution and reference state equality; no action-string or response-string gate`。after 首个请求附指导，后续请求恢复基础 system；不是每步持续注入指导。

这对 **解锁、touch、登录等写状态动作**有实质意义，不应因没有逐字对齐返回而全部否决。long50 的门锁状态改变，以及 base37 的新建空文件，都有实际 reference 状态目标。相反，base92 的查油量、188/192 的发票查询、long163 的查航班费用都是只读动作，执行前后状态不变。它们必须另外比较读返回的有效信息；现有 gate 未完成这一点，不能称为已落实论文的只读局部核验。

酒店采用自定义 SQL 谓词，预约采用本地 native task completion，不能等同于 reference 状态/信息匹配。业务 after/reference 的用户和工具前缀相同；request 里的最后一个空 assistant 项 `reasoning` 不同，可能是生成后的保存形式，不据此断言锚点不同。

## base37：正确最终指导与反馈来源须分开

`selection.json` 指向 `steering/attempt-2`、`after/attempt-2`。`outcome.json` 记录：attempt-0 被 local gate 拒绝；attempt-1 局部 touch 被接受，但后续写成第一句 `No server error occurred during the initial phase.`，终局 state checker 失败；attempt-2 成功。

选中 `steering/request.json` 的 user payload **实际带有**前两次反馈，包括 attempt-1 的完整终局状态与 ground truth 正确句 `However, a server error was detected in the final testing phase.`。因此 Teacher analysis 提到前次写入 `No server error...` 有真实来源，并非凭空误诊；但不是原始 before（原始 before 写的是 `resolving the server error.`）。

这是一条有效的“有反馈后生成正确指导”记录，但反馈越过了局部 touch，包含完整续跑后的终局答案。不能将终局失败驱动的新重试包装成只在局部参考状态不匹配时继续重试。该差异属于训练协议/采集流程核对，不能靠页面上省略说明解决。若最终只选一个最少额外解释的新增训练案例，先选 long50。

## 预约与酒店旧问题的具体证据

- 预约 `after/final.db` 的 BK20：`booked_at = 2026-11-05 16:34:52.228088`，`appointment_slot_id = SL3004`；SL3004 是 `2026-02-03 08:45`，仍写 `is_same_day_booking = 1`。请求中没有冻结时钟。same-day 的日期语义未修复。
- 预约初始数据库已有四个 15 分钟时段且容量为 3；列表只显示后面三个，遗漏 08:00。新 before 据此新建重复 SLOT25。它也设了 same-day 标记，因而不能沿用旧版“漏标记导致失败”的因果解说。after 指导称已找到正确 SL3004，主要强调标记，未解释这个列表/重复时段问题。
- 酒店 after 和 guidance 将 `<220` 改写成确定的 210，酒店名也直接构造。可以把这视为人工录入草稿记录，但不适合在当前“模型找回正确执行”的案例中把它描绘为有事实依据的酒店选择。

## 来源与复核路径

远端均在 `nx:/mnt/genming/`：

- 九例总索引：`training-case-supervision-20261106/selected-training-data.json`；交付包 `training_steering_9_cases_20261106`。本报告核查包中 `cases/002_booking_2_2`、`004_booking_and_scheduling_11_4`、`005_multi_turn_base_110`、`006_multi_turn_base_188`、`007_multi_turn_base_192`、`008_multi_turn_base_92`、`009_multi_turn_base_37`。
- 酒店源：`training-reference-retries-20261106/seed-101/cases/booking_2_2`；预约源：`training-clinic-corrected-retries-20261106/seed-101/cases/booking_and_scheduling_11_4`。
- 110/188/192：`new-ablation-pipeline-20261105/training/cases/`；92/37：`new-ablation-pipeline-batch2-20261105/training/cases/`。各例 selected sources 保留具体 attempt。
- 新长上下文：`training-bfcl-long-context-search-20261106/progress.json`；48 个完成条目中自动 training 候选只有 50、163，ablation 候选均否；另有 2 个 JSON 错误。实际核查 `training/cases/multi_turn_long_context_50` 与 `163` 的 before、选中 reference / steering / after 和 gate。50 使用 reference attempt-1、steering/after attempt-0；163 使用 reference attempt-2、steering/after attempt-0。

本报告只给证据与选材结论；尚未制作页面，也不把自动 qualified 或手写 audit 标签当成原始正确性的证据。
