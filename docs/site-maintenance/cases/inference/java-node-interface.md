# I1 · Java 工具名大小写：定版复核

日期：2026-11-06。本轮独立复核现有案例，不重建选例。早期逐段证据表位于论文仓库 `notes/cases/inference/java-node-interface.md`；正式展示数据为 `design-lab/case-content/inference/java-node-interface.json`。

## 复核范围与结论

检查七个方法的任务、工具定义、展示动作、推理、标注、记录入口与 archived score。原始任务与 `task.json.question` 一致。逐一读取每个方法 m4 的完整调用前思考和结构化调用；七段推理节选均是该消息的连续原文，七个展示调用与源调用一致，仅省略共同 `mcp_tool_` 前缀并解码参数 JSON。实际核验的是生成的接口调用，不将 Mock 返回当成真实 Elasticsearch 执行。

| 方法 | 本轮确认的行为和视觉语义 |
| --- | --- |
| BF16、SteerDistill | `NodeIdConverter.format` / `toAppendTo` 均匹配定义；动作蓝标正确。推理节选用于解释绑定，无需另加标记。 |
| GPTQ、EfficientQAT、BitDistiller、QeRL | 思考中工具名正确，实际调用变成 `Nodeidconverter.format`。保留推理正确拼写的蓝标、调用错误拼写的红标；不能把整段推理染红。 |
| On-Policy QAD | 思考正确写出工具名和 `toAppendTo`，动作同时误写 `Nodeidconverter` 与 `toappendto`。两处独立红标及对应正确推理蓝标均必要。 |

全方法 score 中 BF16/Ours 通过，其余未通过，与所展示接口差异相符。页面没有把生成调用扩写为真实节点 ID 写入成功，也没有隐藏一个实际正确的 baseline 调用。中文摘要、各方法差异说明直接、易读，不需要补说明或免责声明。

## 本轮处置

**未改 JSON。** 保留既有七方法、默认 Ours/QAD、单轮展示、全部原文及标注。未修改 raw、共享组件或 catalog。已检查 7 个动作和 7 段完整来源消息中的推理；无新增浏览器审查，视觉验收由 root 统一完成。

四案联合完整性检查通过：4 configs、56 个精确标注、212 个来源 URL。独立对照脚本另核验了本案全部调用名、参数和推理原文，不以 span 匹配代替上表语义审查。
