# 九例训练 ZIP 更新复核 · 2026-11-06 11:31 版

## 结论

本次是参考证据整理，不是新一批运行。没有新增可直接加入正式训练分类的案例；原先选材结论保持。已展示的 T2 来自另一个 long-context 包，不在此 ZIP 中；工单110保留为现有 A6，不重复包装为新的训练成功/失败对照。

## 文件版本与差异

- 来源：`nx:/mnt/genming/training-case-supervision-20261106/packages/training_steering_9_cases_20261106.zip`。
- 远端修改时间：2026-11-06 11:31:04 +08:00；大小 5,634,631 bytes。
- 本次本地与远端 SHA-256 一致：`1b92292ed4babf6493a57094fdce7f5995d7228258804db749c32601201b8670`。
- 上轮审查版本 SHA-256：`d0bac56a8987fb5657284be68d9f3bd1963def20f458e742185c53d62f0dbd3b`。
- ZIP 共1111个文件，`checksums.json` 中1110项全部通过校验。
- 与上轮解包目录逐文件比较：新增6个文件，修改11个文件，删除0个。新增的是总 `local_verification_index.json` 和110/188/192/92/37的 `reference/local_gate.json`；修改的是这五例的 SUMMARY/selection及总checksums。
- 所有 before/reference/after 轨迹、模型请求/响应、指导、环境执行、原有 student local gate、数据库及终局核验均字节一致。前四个业务案例全部不变。

新增索引明确记录：`Evidence consolidation from existing execution records; no new inference or environment replay.` 五个参考gate均标记 `compiled_from_saved_records: true`，编译时间为03:31:02 UTC。不能把新文件落盘时间当成运行时核验发生时间。

## 新增汇总逐项核查

五例均核实：引用文件SHA-256正确；汇总before/actual状态等于实际reference首步执行前后状态；reference首步post state等于原after gate的target state；guided actual等于target；`outcome.reference.valid_first_step`原记录为true。

| 案例 | Reference首步 | 状态变化 | 新汇总解决的问题 |
| --- | --- | --- | --- |
| 110 | ticket_login | 有 | 便于直接找到参考首步与student目标的映射；原先已可从执行记录核实 |
| 188 | retrieve_invoice | 无 | 只汇总状态相同，仍无读取结果比较 |
| 192 | retrieve_invoice | 无 | 同上；不修复执行思考中的工具名矛盾 |
| 92 | displayCarStatus | 无 | 同上；不验证实际读到的油量 |
| 37 | touch | 有 | 补齐新建空文件的参考说明；不改变指导吸收终局答案反馈的来源 |

原student gate仍明确是 `Successful tool execution and reference state equality; no action-string or response-string gate`。新reference汇总没有新增observation比较，也没有修改历史接受/续跑流程。状态写入的证据仍有意义；读取动作的已知缺口仍存在。

## 当前选材与后续优先级

1. **银行卡国家限制 banking_6_2：最值得补证据。** 修正规则和开关语义清楚，但业务gate仍为既有谓词/任务核验，未接reference局部比较；本次无变化。仍暂缓正式训练页。
2. **指定句子写入 base37：保留有条件候选。** 最终思考、指导与写入可读，但选中重试使用前次完整续跑的终局GT句子。不是本次修复，也不能靠新增参考gate变成仅局部反馈的闭环例。
3. **按余量加油 base92：暂缓。** 读信息核验和Teacher分析失实两项均未改变，且网站已有加油恢复案例，增量价值有限。
4. **工单 base110：保留已有A6，不新增训练页。** 无指导其实自行登录并重试建单，终局差异在描述字段；指导主要解决登录前提。新汇总不改变这个选材问题。
5. **发票188/192：继续跳过。** 原相关思考矛盾及只读gate缺口均未变。
6. **资产、酒店、预约：继续跳过。** 初态重复借出/日期、价格来源、同日预约日期语义等旧问题未更新。

本轮复核以字节差异为范围，继承上轮对完全相同轨迹的逐条语义审查，不声称再次生成或修复它们。详见[上轮总审核](latest-cases-review-20261106.md)、[业务候选](cases/training/latest-core-audit-20261106.md)和[BFCL候选](cases/training/latest-new-audit-20261106.md)。网站展示、原始数据及远端均未修改，未重跑或发布。
