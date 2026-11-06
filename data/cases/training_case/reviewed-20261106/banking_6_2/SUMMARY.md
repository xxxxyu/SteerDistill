# 003 银行卡国家限制

未指导学生意识到数值1允许全部国际交易，却仍填写1；指导后设置0并保留US、CA列表，执行请求的国家限制。

任务见 `task.json`；原始上下文与环境记录保留在本目录。

- 未指导学生：`before/trajectory.json`
- Teacher参考：`reference/trajectory.json`
- 指导后学生：`after/trajectory.json`
- Teacher分析与推理：`steering/analysis.json`
- 实际指导内容：`steering/raw_steering_prompt.txt`

各轨迹目录的 `cot_and_actions.txt` 提供完整逐消息阅读版；请求、响应、工具结果与状态验收记录保留在对应目录。消息序号从0开始，见 `selection.json`。

参考对照局部状态已实测：`reference_state_comparison.json`直接比较reference、before和after的局部数据库，覆盖卡片属性、国际交易开关与国家白名单；忽略创建和更新时间。
