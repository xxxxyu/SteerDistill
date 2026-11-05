# 换算出加仑数后，还要执行加油 · 证据账本

## 选择与范围

选择为一个聚焦的 ablation 比较案例。可读的信息是：换算返回给出了正确的数值，但补加燃油还需要一次改变环境状态的调用。所选 Teacher 结构化指导、Student 结构化指导和 GPT 结构化指导均使 agent 执行 `mcp_tool_fillFuelTank(fuelAmount=10.04)`；Teacher 自由文本指导给出了相同调用，agent 却直接回复完成。原始无指导运行也停在数值确认。本例不把成功写成 Teacher 独有能力，不把一组经过选择的运行写成总体成功率或等预算格式实验。

作者独立阅读本例原始指导、生成分析、执行推理、调用与状态；未读取本例旧页面或旧 editorial JSON。接受的 `sales-order-pricing.json` 仅用于结构参照。按任务指定，仅产出本 JSON 和本账本。

所有原始路径以下述目录 `B` 为根：

`data/cases/ablation_case/reviewed-20261105/main/multi_turn_base_74/`

[原始任务](../../../../data/cases/ablation_case/reviewed-20261105/main/multi_turn_base_74/context/task.json)有两轮：先加油，再启动发动机并汇报状态。页面折叠框保留两轮完整原文；操作和验证明确限于第一轮，未把第一轮通过写成整个多轮任务完成。

## 运行身份与对应关系

| 页面方法 | 所选运行（相对 B） | 指导 | 第一轮结果 |
| --- | --- | --- | --- |
| Teacher 结构化指导 | `trial-history/trials/teacher_structured/guide-1/seed-71782927/` | `trial-history/guidance/teacher_structured/attempt-1/` | 通过 |
| Teacher 自由文本指导 | `trial-history/trials/teacher_freeform/guide-0/seed-71782927/` | `trial-history/guidance/teacher_freeform/attempt-0/` | 未通过 |
| Student 结构化指导 | `trial-history/trials/student_structured/guide-0/seed-71782927/` | `trial-history/guidance/student_structured/attempt-0/` | 通过 |
| GPT 结构化指导 | `trial-history/trials/external_structured/guide-0/seed-71782927/` | `trial-history/guidance/external_structured/attempt-0/` | 通过 |
| 无指导 | `unguided/` | 无 | 未通过 |

四个所选 guided `restore.json` 均为 `verified=true`，状态哈希为 `d3c68590caee17e444b92be8b67f776e5f05347fbbe8ceb4acb15bb0f471551e`，上下文哈希为 `146341f5935222904f318eb3eaa0b86bc57d56416d475e2c856b8a6f61f9557d`。逐项比较确认：四个 guided 轨迹及原始无指导轨迹的 messages[0:6] 均与 `context/anchor-context.json` 完全相等。无指导原始轨迹为 7 条消息，页面显示的对应后缀恰为 message 6，而非另一轮或另一状态的失败。

原始无指导执行的最后一项是 `liter_to_gallon(liter=38)`，返回 `gallon=10.038536`；前后 `VehicleControlAPI.attributes.fuelLevel` 均为 10.0。三个成功分支在同一前缀后增加了 `fillFuelTank`，从 10.0 增至 20.04。所选失败自由文本分支未增加任何调用。

实际 `turn-000/request.json` 的 system 内容包含对应 `guidance.json.text`，并标明 `Local steering for this response only:`。其非 system 消息的 role/content 与 anchor 相同；请求序列化省略了冗余 reasoning/tool_calls/tool_call_id 字段，不能把完整请求对象说成逐字相等。三个成功分支 `turn-001/request.json` 已移除指导，继续生成最终回复。失败自由文本分支第一条输出即结束。本页是指导变体的同起点续行比较，不称为训练后模型效果。

### 保留的 refinement 历史

Teacher structured 的 guide-0 已明确给出 `Call mcp_tool_fillFuelTank with fuelAmount=10.04`，但三个 seeds 的 `score.json.passed` 均为 false：71782927 和 71782928 询问是否继续加油，71782929 无调用却称已加油。guide-1 的生成请求包含这些失败的实际 first execution、local comparison、native verification 反馈；其指导改为四字段中强调当前状态、执行补油及 20.04 的结果。所选 guide-1 seed 71782927 成功。

因此不能仅据本例将差异归因于结构化格式本身、声称各方法同等搜索预算，或把 guide-1 写成首次尝试。所有 guide-0、guide-1、其他 seeds、生成请求/响应均保留在完整记录的次级来源选择器。默认页面只比较指定运行。

`context/reference-alignment.json` 的 `exact_state_replay=true`；参考为受 verifier assistance 的固定成功 suffix。`reference_verifier_assistance=true`、`not_unguided_teacher_performance=true`，不能将此参考当无指导 Teacher 性能。实际无指导选项来自 `unguided/`。

## 原文与状态映射

| 展示项 | 原始位置及意义 |
| --- | --- |
| 标题及任务摘要 | `context/task.json.question[0]`；函数 `fillFuelTank.parameters.properties.fuelAmount.description` 明确是新增油量；anchor message 5、`context/prefix-execution.json` 的最后一项给出换算结果与当前 10.0。 |
| 折叠的完整原始任务 | `context/task.json.question` 原样复制，保留第二轮和原顺序；未把 harness 内容混入用户请求。 |
| 成功调用及返回 | 每个成功运行 `trajectory.json.messages[6]` 的 wrapper `call_tool` 内层函数与参数，以及 message 7 的嵌套 text 返回；`execution.json[2]` 交叉核对。页面展示实际内层名称 `mcp_tool_fillFuelTank`，没有改动大小写或参数。 |
| 成功最终回复（仅记录） | 同一 `trajectory.json.messages[8].content`；完成确认已核对，页面省略重复回复，原文保留在记录。 |
| 自由文本、无指导回复 | 各自 `trajectory.json.messages[6].content`，同样仅去除 think wrapper 与 `**`。无指导不伪造指导文本。 |
| 可选执行推理 | 每个分支 `trajectory.json.messages[6].reasoning` 的连续原文节选；与决策发生顺序一致。 |
| 指导框 | 相应 `guidance.json.text`。结构化值 JSON 解码为四个原始字段；freeform 为原样 XML 调用文本，不替其改写成自然语言建议。节选只 trim 两端空白。 |
| 成功油量结果 | `execution.json[2].before/after.VehicleControlAPI.attributes.fuelLevel`，10.0 → 20.04；`arguments.fuelAmount=10.04`。 |
| 两个失败油量结果 | 各自 `execution.json[1].after.VehicleControlAPI.attributes.fuelLevel=10.0`；完整 execution 仅 list_tools 与 liter_to_gallon。 |
| 第一轮任务验证（仅记录） | 各自 `score.json` 的 `goal_turn=0`、`official_state`、`official_response`、`passed`。失败 predicate 同时显示 fuelLevel 10.0 对 20.04，且缺少 `{'fuelLevel':20.04}` 返回，正对应漏加油，不只是格式差异。 |
| guided 局部核对（仅记录） | 每个运行 `local-comparison.json.checked_before_continuation`、`exact_reference_state`、`exact_reference_observation`；三个成功均 true/true，自由文本 false/false。与指导中的 recovery_check 是不同证据。 |

JSON 的每个展示事件、推理与结果含 site-relative `source.file`、message / executionIndex / field 定位。记录清单覆盖 B 下全部 414 个已有文件，不复制数据包；18 个主要来源为五种方法轨迹、四种指导、五种第一轮验证、四种局部比较，其余在次级选择器保留，包括 refinement 历史和参考来源。

## 完整推理及指导审阅

- Teacher 结构化：完整 attempt-1 生成分析准确区分转换与实际加油，四字段与状态一致。执行前推理正确选择 10.04；执行后 message 8 对总油量 20.04 一度疑惑，猜测先前油量和容量，但未追加错误操作，最终明确报告加入 10.04、总量 20.04。页面只称执行成功，不称已形成完备环境理解或发生自我纠错。post-result 推理完整保留在 records，未将它冒充调用前决策。
- Teacher 自由文本：完整生成分析也准确指出漏执行；最终指导却是 XML 调用文本。执行 agent 的完整 message 6 只讨论取两位小数，最后认为格式化确认即可完成，输出错误的已加油陈述。这里失败不是指导缺少正确工具名；页面描述保留这一点。
- Student 结构化：完整生成分析、四字段及执行前推理正确要求加油。message 8 对 20.04 产生短暂疑惑，随后说明用户未要求空箱、关键是新增 10.04；最终报告正确。页面不夸大为无困惑的理解。
- GPT 结构化：完整四字段要求使用已有转换值，不重复转换、不在调用前结束。生成 response 的 reasoning_content 仅 `**Correcting JSON fuel output**`，没有更多可审阅分析。执行两条 reasoning 均与调用和结果一致。
- 无指导：完整 message 6 reasoning 将用户意图解释成理解单位、确认格式，舍弃实际状态变化；故展示末段意图判断。prefix messages 2/4 曾有 9.998536 等错误心算，但真实转换返回 10.038536 已覆盖这一数值错误，各分支共享同一前缀。失败关键是漏操作，不归因为换算数值错误。

## 逐段标注审阅

蓝色表示本地正确的动作/要求或实际状态变化；砖红表示将数值确认当作任务完成的决策或未改变的状态。指导有正确的操作要求时仍用蓝色，即使该分支执行失败。以下为逐个保留选择，而非按函数名或方法自动高亮。

| 方法 / 位置 | 保留的精确 span | 必要性及颜色 |
| --- | --- | --- |
| Teacher 结构化 / action 0 args | `fuelAmount=10.04` | 蓝色；将四舍五入后的换算量作为新增油量，函数名使用既有普通蓝色语法样式。 |
| Teacher 结构化 / reasoning | `I should use this tool with the rounded 10.04 gallons.` | 蓝色；从格式化转向使用加油工具。 |
| Teacher 结构化 / guidance | `Execute fuel refill using the converted gallon value` | 蓝色；即时操作要求，而非换算或宣告完成。 |
| Teacher 结构化 / result 0 | `10.0 → 20.04` | 蓝色；状态实际变化。 |
| Teacher 自由文本 / reply | `The fuel tank has been filled` | 砖红；明确陈述完成，但无实际加油调用。 |
| Teacher 自由文本 / reasoning | `The task is complete once the converted value is properly formatted and confirmed.` | 砖红；将完成条件缩成格式确认，解释为什么未调用。 |
| Teacher 自由文本 / guidance | `mcp_tool_fillFuelTank` | 蓝色；指导中确实有正确加油工具，不能把失败误讲为无操作提示。XML 参数保留但不另作重复标记。 |
| Teacher 自由文本 / result 0 | `仍为 10.0` | 砖红；状态未改变。 |
| Student 结构化 / action 0 args | `fuelAmount=10.04` | 蓝色；独立核对该运行确有同一正确新增油量，函数名不另加背景标记。 |
| Student 结构化 / reasoning | `The tool requires the fuelAmount in gallons, so I'll input 10.04.` | 蓝色；明确把换算值作为动作输入。 |
| Student 结构化 / guidance | `Call mcp_tool_fillFuelTank with fuelAmount=10.04` | 蓝色；精确操作要求，余下说明不重复突出。 |
| Student 结构化 / result 0 | `10.0 → 20.04` | 蓝色；该运行的实际补加状态。 |
| GPT 结构化 / action 0 args | `fuelAmount=10.04` | 蓝色；独立核对该运行输入正确新增油量，函数名不另加背景标记。 |
| GPT 结构化 / reasoning | `The next step would be to call the mcp_tool_fillFuelTank with fuelAmount set to 10.04 gallons.` | 蓝色；决策直接落在下一工具操作。 |
| GPT 结构化 / guidance | `do not repeat the conversion or claim completion before this call succeeds.` | 蓝色；把完成与调用成功绑定，补足本例关键判断。 |
| GPT 结构化 / result 0 | `10.0 → 20.04` | 蓝色；此分支状态变化。 |
| 无指导 / reply | `Done.` | 砖红；在尚未执行补加燃油时结束当前任务。后文确实只说确认了数值，未把它改写成更强的已加油谎称。 |
| 无指导 / reasoning | `confirming the calculation and formatting correctly is key here.` | 砖红；误把用户要执行的操作缩成数值说明。 |
| 无指导 / result 0 | `仍为 10.0` | 砖红；对应原始状态未改变。 |

逐段无标记决定：

- 三个成功分支 action return `fuelLevel=20.04` 均已核对，保持无独立 span，因为动作与下面状态结果已经承担重点；不按返回格式自动标记。
- 三个成功分支最终回复已完整审阅，主页面省略；它们准确重复补加与总量，不引入新的因果信息，完整记录仍可查看。
- Teacher 自由文本回复的 38 liters、10.04 gallons 与精度说明正确，保留普通文字，不能染成错误数值；无指导的未来语态 `will be filled` 和“confirmed the fuel amount”亦保持未标记，避免把弱表述夸大成已执行陈述。
- 五段选中 reasoning 的其余文本均逐段审阅；换算、四舍五入与复述目标是背景，未追加标记。未将工具返回后写的解释前置。
- 四段指导节选的其余内容，以及完整原文的全部未选字段保持未标记；没有每字段必标的规则。完整四字段保留原值，freeform 保留原始转义和调用格式。
- 各分支局部比较和任务验证已核对，仅保留在记录中；主结果只显示油量状态，避免重复表达成功/失败。
- 原始任务、方法描述及摘要无高亮。guide-0 历史和其他 seeds 不挤入主比较，也不隐去原始来源。

## 验证与交接

已完成：

1. 对原始无指导与四个 guided 的 anchor 前缀逐对象相等检查；工具参数、返回和前后状态交叉核对；查看各运行完整相关推理和指导生成分析。
2. 检查实际首请求指导注入与成功分支下一请求移除；核对所选 guide-1 refinement 请求以及 guide-0 三个失败结果。
3. 原文对齐脚本逐项断言完整 question、五种方法调用/回复/推理/结果状态及四种完整 guidance 原文匹配；通过。
4. `node design-lab/case-shared/validate-case.cjs design-lab/case-content/ablation/convert-then-refuel.json` 通过：19 个精确 UTF-16 spans，414 个存在的来源 URL。此检查不替代上述语义审阅。

待集成负责人完成：桌面/窄屏、五种方法切换、折叠、来源读者和下载的浏览器 QA；未声称已视觉验收。集成负责人已告知共享读者增加 guidance.json 的 `text` envelope 解析；无指导 `guidance:null` 的呈现由负责人处理。作者未修改渲染器或 catalog。

未注册预览：

- `design-lab/paper-cases.html?group=ablation&case=convert-then-refuel`
- `design-lab/case-records.html?group=ablation&case=convert-then-refuel&source=teacher_structured-trajectory&message=6`

无需重新运行实验，未提交 commit。技术核对与用户最终接受分开。
