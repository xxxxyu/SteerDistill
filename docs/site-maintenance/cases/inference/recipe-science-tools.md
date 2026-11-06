# I2 · 连续科学查询：定版复核

日期：2026-11-06。正式数据为 `design-lab/case-content/inference/recipe-science-tools.json`。早期完整取舍记录保留在论文仓库 `notes/cases/inference/recipe-science-tools.md`。

## 范围与事实核验

本案展示同一个用户请求中的两次科学查询，不是两个用户轮次。逐项检查七方法的 m6/m8 调用、其完整思考，以及所选推理来源：BF16/Ours 取 m8；其他五方法 m6/m8 没有实质思考，保留的句子来自更早 m4 的完整计划。没有把行动后的解释放到行动前。

原始任务完整匹配 `task.json.question`。工具定义确认 `method_used` 可省略，默认 `default` 对应 most accepted method；这不是因少填参数而失败。十四个展示工具名与实参逐一匹配源记录，保留所有真实误拼，未通过去前缀操作修好错误工具名。返回是 Mock，继续不展示为真实检索结果。

| 方法 | 调用与标注审查 |
| --- | --- |
| BF16、SteerDistill | 两次都使用 `science_history.get_discovery_details`；第二次蓝标强调接口保持，第一次留白避免重复强调。 |
| GPTQ | 第一次接口正确，第二次改成 `m-core-mcp-tool-science-history-get-discovery-details`；第二次红标匹配实际错误。 |
| On-Policy QAD | 第一次接口正确，第二次变成 `m/dataTables`；保留局部红标。 |
| QeRL | 第一次正确，第二次变成 `m_c_p_tool_science_history_get_discovery_details`；不把错误改写成规范名。 |
| EfficientQAT、BitDistiller | 两次均多写 `sc`，标出 `scscience_history`；其余参数不多标。 |

GPTQ/QAD/QeRL 的对比框中性、仅第二个错误名称红标，是既有混合事件设计：没有因为最后一步错误就把第一个正确调用染红。三者的计划推理仍说复用同一工具；节选保留无标状态，不捏造“计划选择了错误工具”的因果。BF16/Ours 真实正确保留蓝色。全任务分数与局部接口判断一致，但页面继续只解释所选接口片段。

## 本轮处置

**未改 JSON。** 任务、两次调用及可选推理足以说明差异；不额外追加科普、数据来源标签或成功声明。七方法共 14 个调用、7 段推理逐一核验来源；标题、中文说明、语气与其余案例协调。原始任务、source 路径、raw、catalog 和共享组件均未改动。完整性检查通过；不含浏览器验收，由 root 统一完成。
