# I3 · 排序字段与方向：定版复核

日期：2026-11-06。正式数据为 `design-lab/case-content/inference/export-sort-direction.json`，历史审阅位于论文仓库 `notes/cases/inference/export-sort-direction.md`。

## 实际复核范围

读取本案七方法 m4 完整思考与调用，逐项比对展示调用、推理节选、所有标注及中文描述。原始任务与 `task.json.question` 完全一致。工具定义确实把 `sortBy` 的描述写成排序字段，但 `enum` 只有 `ASC`、`DESC`，没有独立 `sortDirection` 参数。摘要承认这一可见歧义，不能扩大成真实 AWS API 的普遍规则。

| 方法 | 确认的取舍 |
| --- | --- |
| SteerDistill | 完整思考先疑惑再明确以枚举值为准；调用 `sortBy="DESC"`。保留决断句与参数蓝标，未只截正确调用掩盖未解决的矛盾。 |
| BF16 | 同样选择 `DESC` 并正确调用，保持蓝色。原文 `sosortBy` 拼写粘连来自源记录，不擅自润色引文。 |
| On-Policy QAD | 反复讨论后仍决定字段名；调用 `LastUpdatedDateTime`。所选推理红标与实际参数对应。合法默认 `filterOperator="EQ"` 不作为错误重点。 |
| GPTQ | 思考明确看到枚举只有方向，最后调用却填字段名并加 schema 中没有的 `sortDirection`。保留原推理无标，两个动作红标正确；不把该思考伪装成明确支持错误调用。 |
| EfficientQAT | 猜测可把字段和方向拼成 `_DESC`，实际也这样调用；两处红标一致。 |
| BitDistiller | 最后仍主张字段名，调用确实填字段名。思考提到额外方向字段，实际调用没有该字段；展示未增添该参数，也未误标合法的 `filterOperator`。 |
| QeRL | 思考尝试用点号拼接，实际调用 `LastUpdatedDateTime.DESC`，保留该局部红标。 |

七个调用与源 arguments 严格一致，仅去掉共同 MCP 前缀；七段推理都是源 m4 连续子串。所有方法都有原始轨迹入口，BF16 成功没有被改成失败。Mock 返回不入页，页面不声称已取得真实排序结果。中文任务背景和各分支一句话描述足够清楚，无必要扩写。

## 本轮处置

**未改 JSON。** 不新建标注、不重写原文，不为“优化”增加冗余结论。原始任务、raw、catalog、shared 均未改。4 案联合完整性检查通过，本案 7 个动作与 7 段推理另做 source 对照。浏览器验收由 root 负责。
