# Lock doors · 独立编辑证据记录

## 选择与比较范围

选择为紧凑 ablation 案例：用户已经要求检查并锁好所有车门，状态查询显示四门未锁；具体分歧是执行锁门，还是把明确的执行请求重新解释为查询并询问许可。三个结构化指导分支实际锁门，Teacher 自由文本指导虽给出正确调用，agent 仍停在确认问题。原始无指导分支也停在确认问题。这不是 Teacher 独有成功案例，也不以一组试次推导指导形式的总体因果效应。

正文数据：[lock-doors.json](../../../../design-lab/case-content/ablation/lock-doors.json)。原始包根目录：[multi_turn_base_51](../../../../data/cases/ablation_case/reviewed-20261105/main/multi_turn_base_51/)，以下路径均相对此目录。

| 方法 | 选定路径 | 首个 actor 请求 seed | 结果 |
|---|---|---|---|
| Teacher 结构化指导 | `trial-history/teacher_structured/001` | 71782829 | 锁门，0 扇未锁 |
| Student 结构化指导 | `trial-history/student_structured/000` | 71782829 | 锁门，0 扇未锁 |
| Teacher 自由文本指导 | `trial-history/teacher_freeform/003` | 71782829 | 没有新增调用，4 扇未锁 |
| GPT 结构化指导 | `trial-history/external_structured/003` | 71782829 | 锁门，0 扇未锁 |
| 无指导 | `unguided` 原始轨迹 | 71782828（turn-002） | 没有新增调用，4 扇未锁 |

四个 guided 分支的 `restore.json` 的 state/context digest 相同；`replayed=2`，恢复 list_tools 和 displayCarStatus 后的状态。实际请求去掉系统消息末尾的 `Local steering for this response only:` 指导后，role/content 与 anchor 一致；传输请求不含原轨迹的 reasoning/tool_calls 等附加字段。guided 第一请求有指导，成功分支第二请求中系统消息已还原，无持续注入；Teacher 自由文本直接结束，没有第二请求。

`unguided/trajectory.json.messages[:6]` 与 `context/anchor-context.json` 逐字段相等，`unguided/turn-002/pre-context.json` 也与 anchor 相等。其 `restore.json` 记录的是原始运行开始（`replayed=0`），因此该文件的 context digest 不应误认为断点 digest。正文展示它的 message 6，只比较查询之后的续行，不把原始发现工具/查询的前缀再算作分支动作。无指导是原始失败轨迹，不是与四个 guided 分支同 seed 的重跑。

本次验证范围为 `goal_turn=0`（锁门请求），不是整个四轮任务。原始任务折叠保留 `context/task.json.question` 的四条用户请求及原顺序；后续启动引擎、胎压、消息任务没有在本页声称完成。harness 说明不混进用户原文。

## 指导来源与完整阅读

全部正文指导直接取选定试次 `turn-000/request.json.messages[0].content` 的实际注入后缀，不取目录表面上默认的指导文件。

- Teacher structured/001 实际指导是带 `remainingUnlockedDoors=4` 与 `=0` 的四字段版本。`methods/teacher_structured/guidance/guidance.json` 是另一版本（含 `ground truth` 的 recovery_check），未用于正文。完整所选指导要求锁门并在执行后确认 doorStatus；agent 使用锁门返回确认，没有再次 displayCarStatus。所选版本的独立 advisor 生成响应未在此包找到；不展示其他版本的 advisor 推理冒充来源。
- Student structured/000 实际指导与 `methods/student_structured/guidance/guidance.json.text` 完全相同。完整 advisor reasoning 和四字段 guidance 均已读：明确由未锁到锁定，无相反的未解决指令。actor 完整首段 reasoning 反复权衡再次查询和直接完成，最后执行锁门；下一条完整 reasoning 依据返回结束。正文只说明实际锁门，不把 recovery_check 文字写成已执行动作。
- Teacher freeform/003 实际指导与 `methods/teacher_freeform/guidance/guidance.json.text` 完全相同，内容就是一个正确 `mcp_tool_lockDoors` XML 调用，不是错误的“请求确认”建议。完整 advisor reasoning 也明确要求立即锁门；其最终调用是给 actor 的指导文本，不能当作 actor 执行。actor 完整 reasoning 先承认用户希望确保锁定，又改称用户没有直接要求执行；无后续纠正。推理节选显示错误解释段；前面的相反陈述已审阅，完整顺序留在记录中，不称自省/恢复。
- External structured/003 实际四字段指导从请求还原。指出原失败问了多余许可、要求立即锁门、以返回确认。此包无 `methods/external_structured` 生成目录；不编造 advisor 推理。actor 首条完整 reasoning 正确理解锁定和四门参数，第二条 reasoning 仅空白。
- Unguided 没有注入指导。`guidance:null` 由共享组件显示缺席状态；不合成伪指导。完整失败 reasoning 已读：把任务缩减为报告状态，最终询问许可。

已独立读完所有被选 actor 的完整 reasoning、调用与最终回复（guided trajectory messages 6–8 或 6；unguided message 6），以及共同前缀 messages 2、4 的 reasoning。首条前缀发现工具；第二条前缀选择查状态并偏重“verification”，没有改变四门。前缀在任务背景概述，不呈现为某分支独有行为。

## 主张、引用与状态映射

| 页面内容 | 原始定位 | 编辑处理 |
|---|---|---|
| 标题/摘要的锁门请求 | `context/task.json.question[0][0].content` | 中文压缩，未把“ajar”断言为工具检测到的机械开门状态 |
| 查询返回四门未锁 | `context/anchor-context.json[5]` 的嵌套 tool text；`context/prefix-execution.json[1].response.doorStatus` | 列出四门；没有称“有些已锁” |
| unlock=false 表示锁定 | `context/task.json.function` 中 lockDoors.parameters.properties.unlock.description；anchor[3] 工具目录 | 简述共同约束 |
| 三个成功分支锁门调用/返回 | 相应 `trajectory.json` messages 6/7；`execution.json[2]` | 展示原 mcp_tool_lockDoors 名称、全部门名、unlock 值；解开 call_tool 包装，不改变参数；返回两字段完整 |
| 成功最终回复（仅记录） | 相应 `trajectory.json.messages[8].content` | 完整审阅与状态相符；重复确认和礼貌结尾不占正文动作框 |
| Teacher freeform 最终回复 | `trial-history/teacher_freeform/003/trajectory.json.messages[6].content` | 去除 think；去除显示用 `**`，保留两项建议和确认问题，不只截取一句 |
| Unguided 最终回复 | `unguided/trajectory.json.messages[6].content` | 同上，保留其完整状态报告、建议和确认问题 |
| 各分支可展开 reasoning | 各 `trajectory.json.messages[6].reasoning` | 原文节选；Student 两段之间 `[…]` 明示删节；Teacher freeform 仅保留“然而”开头的错误解释段；此前相反陈述已审阅，完整顺序在记录中 |
| 指导字段/节选 | 各选定 `turn-000/request.json.messages[0].content` 注入后缀 | JSON 指导解码为四原始字段；freeform 完整字段原文保留，节选仅去首尾空白；不修复大小写或调用格式 |
| 最终四门状态、未锁数 | 各 `execution.json` 最后一项 `.after.VehicleControlAPI.attributes.{doorStatus,remainingUnlockedDoors}` | 三个成功路径最后是 lockDoors；两个失败路径最后仍是前缀的 displayCarStatus。逐个确认四门值，无新增调用导致状态保持 |
| 锁门请求验证通过/未通过（仅记录） | 各 `score.json.{passed,official_state,official_response,goal_turn}` | 明确仅锁门请求。失败检查实际对比四门 unlocked vs locked、4 vs 0，并缺少锁门返回；不是格式性失败 |

`context/reference-alignment.json` 提供 exact_state_replay 与目标全状态，`teacher-reference/replayed-trajectory.json`/execution 可查参考 lineage。所选 guided `local-comparison.json` 在 continuation 前比较状态和返回：三个结构化 true/true，freeform false/false；其 actual_state 与执行记录一致。记录中的任务验证来自 score，未将指导 recovery_check 与局部检查/任务检查混为一项，也不声称本页展示模型训练后的表现。

## 每处标注的人工语义审阅

以下不是自动差异高亮。每个区间都已对照上述源事件阅读，最终 JSON 存显式 UTF-16 start/end/text。蓝色 `after` 表示本任务所需动作/达到目标的状态，红色 `before` 表示停在报告/重复许可造成任务未完成。指导中的蓝色正确动作可与同方法红色失败行动共存。

| 方法/段落 | 保留标注 | 原因及不标注范围 |
|---|---|---|
| Teacher structured 操作 args | `unlock=false` 蓝 | 实际改变状态的方向；完整四门数组必要但不另标，函数名仅常规语法色 |
| Teacher structured 返回 | `remainingUnlockedDoors=0` 蓝 | 直接验证锁门效果；lockStatus 保留但不重复标 |
| Teacher structured 回复（仅记录） | 无 | 返回已承担效果证据，重复确认未选入正文 |
| Teacher structured reasoning | `The next step is to lock all doors.` 蓝 | 将发现未锁转换为实际动作；前文观察不标 |
| Teacher structured guidance | `Call mcp_tool_lockDoors with unlock=false` 蓝 | 选择动作与锁定方向；后续 all doors 保留但不重复强调；完整字段不加额外自动标注 |
| Teacher structured result | `未锁车门：0` 蓝 | 对应实际最终属性；四门 locked 不重复标，验证只留在记录中 |
| Student structured 操作 args | `unlock=false` 蓝 | 本分支独立确认为实际锁门，未因方法名改色；四门数组不另标 |
| Student structured 返回 | `remainingUnlockedDoors=0` 蓝 | 实际成功返回；lockStatus 不重复标 |
| Student structured 回复（仅记录） | 无 | 声称完成与状态一致，重复确认未选入正文 |
| Student structured reasoning | `So, the next step is to lock them.` 蓝 | 明确下一动作；第二段关于直接完成的节选不标，保留对复查的权衡，未再次查询的事实留在本 ledger |
| Student structured guidance | `Call mcp_tool_lockDoors with unlock=False` 蓝 | 原文 Python 式 False 保留；其意图正确，不能无声修成 false；四门清单和其他字段不标 |
| Student structured result | `未锁车门：0` 蓝 | 最终状态已核实；四门值不重复标，验证只留在记录中 |
| Teacher freeform 回复 | `Would you like me to lock the doors automatically now?` 红 | 这句话具体体现把已请求的动作留待再次确认；两条建议保留未标，含正确工具名不等于执行 |
| Teacher freeform reasoning | `由于用户没有直接要求执行锁定动作，而是询问是否已经正确锁定` 红 | 错误解释明确归属 agent；之前承认用户目标的段落已审阅，留在记录中；没有将相反陈述合成“自我纠正” |
| Teacher freeform guidance | `mcp_tool_lockDoors` 蓝 | advisor 的实际正确动作，和 actor 不执行形成差异；XML/args 保留未标，避免把整段当失败 |
| Teacher freeform result | `未锁车门：4` 红 | 实际未完成；其余状态不重复标，验证只留在记录中 |
| GPT structured 操作 args | `unlock=false` 蓝 | 本分支实际执行锁门；四门清单必要但不重复标 |
| GPT structured 返回 | `remainingUnlockedDoors=0` 蓝 | 成功状态证据；lockStatus 未重复标 |
| GPT structured 回复（仅记录） | 无 | 确认与状态相符，重复确认未选入正文 |
| GPT structured reasoning | `Since the user wants to lock them, unlock should be false.` 蓝 | 把用户意图落实到正确布尔方向；同段其他参数说明不标 |
| GPT structured guidance | `Call \`mcp_tool_lockDoors\` now` 蓝 | 明确要求当下执行；此前 permission 解释和后面的完整参数保留未标 |
| GPT structured result | `未锁车门：0` 蓝 | 独立核实最终属性；四门值不另标，验证只留在记录中 |
| 无指导 回复 | `Would you like me to proceed with locking the doors now?` 红 | 原始失败决策具体停点；报告四门未锁是事实所以不红色标记该事实 |
| 无指导 reasoning | `But the immediate step is to report the current status.` 红 | 把需要执行的目标收缩为报告；其余上下文保留不标 |
| 无指导 result | `未锁车门：4` 红 | 依据原始最后状态与 score；没有无指导伪指导标注 |

成功分支最终回复在正文删除、保留原记录。所有最终回复的完整 reasoning 亦已审阅但未全部重印：Teacher/Student 成功后复述正确返回，GPT 为空白；没有被隐藏的错误调用或相反指令。方法描述、标题、摘要不额外标注；结果仅呈现车门状态，任务验证留在记录中；不从成功/失败分数自动推导全文颜色。

## 完整记录与验证

manifest 收录本目标原始目录全部 1,631 个文件，直接链接现有文件、不复制原始字节。主目录只置顶五条选定轨迹、五份 score、四份实际指导注入请求（14 项）；其他试次、同方法默认样本、生成请求/响应、transport、参考与 context 均 secondary。源 ID 使用目标内相对路径，URL 使用站点相对路径；源文件内原机器路径保持原样。

预览：`design-lab/paper-cases.html?group=ablation&case=lock-doors`。
记录：`design-lab/case-records.html?group=ablation&case=lock-doors&source=trial-history%2Fteacher_structured%2F001%2Ftrajectory.json&message=6`。

- 已逐方法核对实际指导后缀、全部相关 actor 推理与调用、最终状态四门/计数、锁门请求 score 和局部对齐报告。
- 原始用户问题逐字段复制，无 harness 前缀。直接源对齐脚本通过：五个分支前缀、实际指导、调用及返回、最终回复、推理子串、用户原文、guided seed、指导移除逐项断言。
- 共享 integrity checker 已通过：1 case、22 个精确 span、1,631 个现存源 URL；语义审阅与机械偏移检查分别完成。
- 浏览器宽/窄屏、折叠、选择器、记录 reader 与下载由集成 owner 进行，本文不声称已完成。
- 本 author 只新增 JSON 和本 ledger；不修改 catalog/共享组件，不提交 commit。

