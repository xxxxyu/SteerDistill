# Lock doors · 独立编辑证据记录

## 选择与比较范围

选择为紧凑 ablation 案例：用户已经要求检查并锁好所有车门，状态查询显示四门未锁；具体分歧是执行锁门，还是把明确的执行请求重新解释为查询并询问许可。Teacher 结构化指导分支把未锁状态接到实际锁门；选中的 Student 结构化和 Teacher 自由文本分支虽然都收到正确的锁门指导，agent 仍将请求缩减为状态确认。默认展示 Teacher 结构化与 Student 结构化失败分支。GPT 结构化成功分支保留在选择器中。完整候选重筛、其他成功试次与比较范围见 [reselection-51-27.md](reselection-51-27.md)；正文直接解释这几条轨迹的行为差异。

正文数据：[lock-doors.json](../../../../design-lab/case-content/ablation/lock-doors.json)。原始包根目录：[multi_turn_base_51](../../../../data/cases/ablation_case/reviewed-20261105/main/multi_turn_base_51/)，以下路径均相对此目录。

| 方法 | 选定路径 | 首个 actor 请求 seed | 结果 |
|---|---|---|---|
| Teacher 结构化指导 | `trial-history/teacher_structured/001` | 71782829 | 锁门，0 扇未锁 |
| Student 结构化指导 | `trial-history/student_structured/008` | 71782836 | 没有新增调用，4 扇未锁 |
| Teacher 自由文本指导 | `trial-history/teacher_freeform/003` | 71782829 | 没有新增调用，4 扇未锁 |
| GPT 结构化指导 | `trial-history/external_structured/003` | 71782829 | 锁门，0 扇未锁 |
| 无指导 | `unguided` 原始轨迹 | 71782828（turn-002） | 没有新增调用，4 扇未锁 |

四个 guided 分支的 `restore.json` 的 state/context digest 相同；`replayed=2`，恢复 list_tools 和 displayCarStatus 后的状态。实际请求去掉系统消息末尾的 `Local steering for this response only:` 指导后，role/content 与 anchor 一致；传输请求不含原轨迹的 reasoning/tool_calls 等附加字段。guided 第一请求有指导，成功分支第二请求中系统消息已还原，无持续注入；Teacher 自由文本与 Student 结构化直接结束，没有第二请求。Teacher/Freeform/GPT 所选首请求 seed 为 71782829，Student 为 71782836；保留不同 seed 的来源，不称作完全受控的整体因果估计。

`unguided/trajectory.json.messages[:6]` 与 `context/anchor-context.json` 逐字段相等，`unguided/turn-002/pre-context.json` 也与 anchor 相等。其 `restore.json` 记录的是原始运行开始（`replayed=0`），因此该文件的 context digest 不应误认为断点 digest。正文展示它的 message 6，只比较查询之后的续行，不把原始发现工具/查询的前缀再算作分支动作。无指导是原始失败轨迹，不是与四个 guided 分支同 seed 的重跑。

本次验证范围为 `goal_turn=0`（锁门请求），不是整个四轮任务。原始任务折叠保留 `context/task.json.question` 的四条用户请求及原顺序；后续启动引擎、胎压、消息任务没有在本页声称完成。harness 说明不混进用户原文。

## 指导来源与完整阅读

全部正文指导直接取选定试次 `turn-000/request.json.messages[0].content` 的实际注入后缀，不取目录表面上默认的指导文件。

- Teacher structured/001 实际指导是带 `remainingUnlockedDoors=4` 与 `=0` 的四字段版本。`methods/teacher_structured/guidance/guidance.json` 是另一版本（含 `ground truth` 的 recovery_check），未用于正文。完整所选指导要求锁门并在执行后确认 doorStatus；agent 使用锁门返回确认，没有再次 displayCarStatus。所选版本的独立 advisor 生成响应未在此包找到；不展示其他版本的 advisor 推理冒充来源。
- Student structured/008 实际指导与 `methods/student_structured/guidance/guidance.json.text` 完全相同，四字段明确由未锁到锁定。actor 完整 reasoning 识别可用锁门工具与未锁状态，但称“用户的首要需求是验证当前状态而非立即锁定”，把锁门留待后续。完整回复报告四门未锁并询问是否锁门；其 summary 也明确把锁门称为下一步。没有新调用、没有下一条请求。指导本身正确，不能将失败解释为 Student 指导有事实错误。
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
| 两个成功分支锁门调用/返回 | 相应 `trajectory.json` messages 6/7；`execution.json[2]` | 展示原 mcp_tool_lockDoors 名称、全部门名、unlock 值；解开 call_tool 包装，不改变参数；返回两字段完整 |
| 成功最终回复（仅记录） | 相应 `trajectory.json.messages[8].content` | 完整审阅与状态相符；重复确认和礼貌结尾不占正文动作框 |
| Student structured 最终回复 | `trial-history/student_structured/008/trajectory.json.messages[6].content` | 去除 think 与显示用 `**`，正文取 `<summary>` 之前的原文连续段落并设置 `event.excerpt:true`；原始 summary 及全部字节仍在完整记录，不合成改写或声称执行过锁门 |
| Teacher freeform 最终回复 | `trial-history/teacher_freeform/003/trajectory.json.messages[6].content` | 去除 think；去除显示用 `**`，保留两项建议和确认问题，不只截取一句 |
| Unguided 最终回复 | `unguided/trajectory.json.messages[6].content` | 同上，保留其完整状态报告、建议和确认问题 |
| 各分支可展开 reasoning | 各 `trajectory.json.messages[6].reasoning` | 原文节选；Student 取原文连续句，展示错误的 verify-first 判断；Teacher freeform 仅保留“然而”开头的错误解释段；此前相反陈述已审阅，完整顺序在记录中 |
| 指导字段/节选 | 各选定 `turn-000/request.json.messages[0].content` 注入后缀 | JSON 指导解码为四原始字段；freeform 完整字段原文保留，节选仅去首尾空白；不修复大小写或调用格式 |
| 最终四门状态、未锁数 | 各 `execution.json` 最后一项 `.after.VehicleControlAPI.attributes.{doorStatus,remainingUnlockedDoors}` | 两个成功路径最后是 lockDoors；三个失败路径最后仍是前缀的 displayCarStatus。逐个确认四门值，无新增调用导致状态保持 |
| 锁门请求验证通过/未通过（仅记录） | 各 `score.json.{passed,official_state,official_response,goal_turn}` | 明确仅锁门请求。失败检查实际对比四门 unlocked vs locked、4 vs 0，并缺少锁门返回；不是格式性失败 |

`context/reference-alignment.json` 提供 exact_state_replay 与目标全状态，`teacher-reference/replayed-trajectory.json`/execution 可查参考 lineage。所选 guided `local-comparison.json` 在 continuation 前比较状态和返回：Teacher/GPT 结构化 true/true，Student 结构化与 freeform false/false；其 actual_state 与执行记录一致。记录中的任务验证来自 score，未将指导 recovery_check 与局部检查/任务检查混为一项，也不声称本页展示模型训练后的表现。

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
| Student structured 回复 | `Would you like me to lock them now?` 红 | 再次请求已经存在的授权，是具体停点；未锁状态报告本身属实不标红；重复 summary 不放入正文，原始完整内容保留在记录 |
| Student structured reasoning | `但用户的首要需求是验证当前状态而非立即锁定` 红 | 错误收缩任务目标，归属 agent；同句可用工具名称保留未标，其他推理全文已审阅留在记录 |
| Student structured guidance | `Call mcp_tool_lockDoors with unlock=False` 蓝 | 正确指导原文保留；不能因 actor 失败把指导染红；其余字段不另标 |
| Student structured result | `未锁车门：4` 红 | 最后执行状态仍四门未锁；其余状态值保留不重复标 |
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

成功分支最终回复在正文删除、保留原记录。所有最终回复的完整 reasoning 亦已审阅但未全部重印：Teacher 成功后复述正确返回，GPT 为空白；Student 只有一条失败回复，完整 reasoning 不含执行或自我纠正；没有被隐藏的错误调用或相反指令。方法描述、标题、摘要不额外标注；结果仅呈现车门状态，任务验证留在记录中；不从成功/失败分数自动推导全文颜色。

## 完整记录与验证

manifest 收录本目标原始目录全部 1,631 个文件，直接链接现有文件、不复制原始字节。主目录只置顶五条选定轨迹、五份 score、四份实际指导注入请求（14 项）；其他试次、同方法默认样本、生成请求/响应、transport、参考与 context 均 secondary。源 ID 使用目标内相对路径，URL 使用站点相对路径；源文件内原机器路径保持原样。

预览：`design-lab/paper-cases.html?group=ablation&case=lock-doors`。
记录：`design-lab/case-records.html?group=ablation&case=lock-doors&source=trial-history%2Fteacher_structured%2F001%2Ftrajectory.json&message=6`。

- 已逐方法核对实际指导后缀、全部相关 actor 推理与调用、最终状态四门/计数、锁门请求 score 和局部对齐报告。
- 原始用户问题逐字段复制，无 harness 前缀。直接源对齐脚本通过：五个分支前缀、实际指导、调用及返回、最终回复、推理子串、用户原文、guided seed、指导移除逐项断言。
- 共享 integrity checker 已通过：1 case、21 个精确 span、1,631 个现存源 URL；语义审阅与机械偏移检查分别完成。
- 浏览器宽/窄屏、折叠、选择器、记录 reader 与下载由集成 owner 进行，本文不声称已完成。
- 本轮仅修改 lock-doors JSON、此 ledger 与独立重筛 audit；不修改 catalog/共享组件或 rename 案例，不提交 commit。
- 2026-11-05 重筛：保留经过完整复核的 Teacher structured/001 和 External structured/003；Student 改为有明确意图误读的失败 /008；Freeform /003 保持。成功 /000 等试次仍在完整记录中，原主目录三项迁为 secondary，Student /008 的轨迹、score、注入请求升为 primary。


- 浏览器复核后仅调整 Student /008 回复显示：保留 `<summary>` 前的原文段落，显式标为节选，避免将 transport 式标签作为正文；确认问题及其红色区间不变。
