# 009 提取指定句子并写入文件

未指导学生恢复了文件不存在错误，但写入错误句段。新的指导要求先建文件、再追加第二个匹配句子，没有提供答案句子。学生从原上下文中识别正确句子，执行touch和echo，局部与最终验收通过。

本次teacher仅接收当前上下文、失败首步和参考首步证据；不接收前次完整续跑的终局评分、参考答案或后续结果反馈。

- 任务及工具定义：`task.json`
- 未指导学生：`before/trajectory.json`
- 参考轨迹：`reference/trajectory.json`
- 新指导后轨迹与推理：`after/trajectory.json`、`after/cot_and_actions.txt`
- Teacher原始输入与分析：`steering/request.json`、`steering/analysis.json`
- 实际steering prompt：`steering/raw_steering_prompt.txt`
- 局部验收：`reference/local_gate.json`、`after/local_gate.json`
- 最终验收：`after/score.json`
