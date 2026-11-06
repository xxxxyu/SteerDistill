# 九例训练 ZIP 更新复核 · 2026-11-06 11:52 版

## 结论

本次有实质进展：**base37 可从有条件候选升级为可制作训练案例**；banking_6_2 新补的事后 reference 数据库对照真实有效，内容正确性证据已补强，但历史运行 gate 未改变。其他七例没有新增实质运行证据，选材结论不变。本轮只审核，未修改网站、远端或运行模型。

## 版本和增量

- 来源：`nx:/mnt/genming/training-case-supervision-20261106/packages/training_steering_9_cases_20261106.zip`。
- 远端修改时间：2026-11-06 11:52:36 +08:00；大小5,632,413 bytes。
- 远端/本地 SHA-256：`c0b7ddc716fa8e9945dca5b48b1f2dd73c56445733ec297ec0931c9ebd8ea36d`。
- 包内1111项checksums全部通过。与[11:31版](training-package-refresh-20261106-1131.md)逐文件比较，新增13、修改34、删除12。新增/删除主要是base37的Teacher及3轮student transport记录替换；另新增banking的 `reference_state_comparison.json`。
- base37的before/reference不变，重新生成steering及after；banking没有重采样。其余案例实际运行材料不变。
- 总 `local_verification_index.scope` 仍写“no new inference”，与本次base37实际新响应冲突；以实际请求、响应、选中来源和修复脚本为准。`case37_protocol_repaired:true` 本身不作为验收证据。

## base37：已解决旧反馈问题

包内位置：`cases/009_multi_turn_base_37/`。新来源 `nx:/mnt/genming/training-case-protocol-repair-20261106/multi_turn_base_37/{steering,after}/attempt-0`；参考仍来自 `new-ablation-pipeline-batch2-20261105/.../reference/attempt-0`。

### 实际请求和运行顺序

1. 完整读取新 `steering/request.json`。user payload只包含task、context、failed_response、failed_execution、current_state、reference_first_response、reference_first_execution和空 `feedback: []`。context逐项等于原before的前20条消息；失败思考/动作与原始响应一致（轨迹把思考合并为think区，API响应则分字段）。
2. 没有携带旧attempt-1的终局失败、完整续跑或ground-truth反馈。参考首步思考本身含正确句子，属于提供的reference材料；不将它误报成终局答案泄漏。
3. 检查远端 `case-rerun-20261103/repair_case37_protocol.py`：只追加local gate失败的状态反馈；一旦local gate通过就break，不以终局失败触发新指导。运行日志确认为attempt0、local=true、qualified=true。
4. 检查其调用的 `bfcl_training10.py:rollout`：首响应执行后先比较实际环境状态与reference首步状态，并检查执行有效性；失败就返回。gate通过后才进入下一次生成。指导仅传给turn0。
5. actual/target/reference三者一致：首步 `touch("1.txt")` 新建空文件，是有意义的写状态核验。原始after turn001/002请求的system均撤去指导。
6. 下一步 `echo` 写入 `However, a server error was detected in the final testing phase.`；末态与任务核验通过。四段新Teacher/student reasoning均与实际API response reasoning逐字一致（仅去首尾空白）。

### 内容与展示判断

- 无指导先向不存在的1.txt写入 `resolving the server error.`，报错后会补建，但再次写入同一错误片段。不能呈现为始终不会建文件。
- 新Teacher分析识别正确目标句，最终指导要求先touch、再写第二个匹配句；指导没有直接写出目标句全文。
- student首轮曾混淆全文第二句与第二个匹配句，但随后明确重数，得出正确句子。下一轮在无system指导下正确写入；这是有记录的自我更正，不是仅凭正确调用推断反思。
- 结束思考仍有“五次提及”“用户确认成功”的不精确回顾；最终文件名、写入句子与实际结果一致。这些背景回顾不影响本例的核心修正，不概括为“所有思考无误”。
- 推荐展示范围：已知文件行数为1、用户要求取第二个匹配句 → 无指导错误写入及补建后的错误内容 → 有指导先建文件、局部接受 → 撤去指导后正确写入。原始三轮请求保留折叠。
- 局部核验只接受新建空文件，**不提前证明后续句子选择正确**。后续写入由实际末态和终局记录支持。不要把两个检查合并，也不要声称Teacher明确指出了漏数的具体句子。

## banking_6_2：事后核对已补实，运行 gate 未变

包内 `cases/003_banking_6_2/reference_state_comparison.json` 比较了实际保存的before/reference/after `local_state.db`，不是仅增加通过标签。

- 独立核验3份数据库哈希，并重新执行cards/card_controls联表查询。目标card5均属account3、virtual、USD2000、active；before `international_allowed=1`，reference/after均为0；国家集合均为CA/US。
- 重算投影与报告完全一致。进一步遍历reference/after所有表，在忽略created_at/updated_at及card_controls.id后，没有其他差异表。
- 旧“缺乏明确reference状态对照材料”的问题已补齐。这个比较支持修正后的业务配置与reference一致，不应继续称作“没有做任何reference比较”。
- 但所有模型请求/响应、运行中的local_gate与续跑均字节不变。新增文件是对旧数据库的事后比较，不证明该reference比较曾参与当时的接受/拒绝。原先指导复用及本次before触发关系也未重建。
- 因而它可支持“有指导修正、事后与reference核验一致”的观察；若作为现有完整训练闭环模板，仍应补接入reference核验的运行记录。内容价值仍高，列下一优先候选，不通过改名或隐藏流程差异直接上线。

## 建议

1. 新增base37训练案例，不替换T1/T2；制作时突出创建前提与后续正确写入，避免扩大指导内容的因果解释。
2. banking_6_2保留为下一优先项。行为/数据库内容已可用，剩余工作是运行协议闭环。
3. 其余七例不因本次包更新时间自动重评为可用。A6维持现有消融；其余沿用[前轮审核](latest-cases-review-20261106.md)。

本轮记录已完成，未加入页面、未推送或发布。

## 后续决定：纳入 T3 / T4

用户确认可以使用后来补齐的状态比较，要求重点排除错轮次。进一步检查运行脚本、完整三分支轨迹和数据库，确认 banking 的 local_state 在唯一一次工具操作后立即保存；后续只有最终回复，没有其他调用，且各分支 local_state 与自己的 final.db 字节一致。因而状态比较没有错轮次。按实际配置及参考对照展示为 T3，保留比较文件的真实生成来源，不将补充比较写成当时控制续跑的 gate。base37 同时纳入 T4。具体整合见 [训练案例新增记录](training-additions-20261106.md)。此前建议保留为审核历史，不再作为当前纳入决定。
