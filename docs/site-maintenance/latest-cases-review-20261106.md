# nx 最新 training / ablation 数据复核 · 2026-11-06

最新更新：[11:52 版九例训练 ZIP 复核](training-package-refresh-20261106-1152.md)。base37重新生成指导与续跑，解决旧终局反馈问题，可制作训练案例；banking补齐事后reference数据库对照，运行gate仍待接入。此前[11:31版](training-package-refresh-20261106-1131.md)只有参考gate汇总，结论仅适用于该历史版本。

只读审查截至本轮的已落盘记录；没有运行模型、修改远端数据或修改网站。三位独立审查者分工检查业务训练、新 BFCL 训练、消融交付与新增流水线，协调者核验优先候选及共同协议。

## 最新来源

原发布目录 `training-local-site-20261104/data/cases/` 尚未同步本轮新增材料。最新证据主要位于 nx `/mnt/genming/` 下：

- `training-case-supervision-20261106/packages/training_steering_9_cases_20261106.zip`：4 个业务 + 5 个 BFCL 训练案例。
- `training-bfcl-long-context-search-20261106/`：随后补出的长上下文训练及对应消融。
- `ablation-evidence-delivery-20261105/`：10 个五分支消融执行对照，链接 `ablation-fixed-checkpoint-rollouts-20261105/` 和 `ablation-complete-branches-20261105/`。
- `new-ablation-pipeline-20261105/`、`new-ablation-pipeline-batch2-20261105/`、`new-ablation-pipeline-batch3-20261106/`：未全部进入上述交付目录的新数据。
- `ablation-nonempty-thinking-20261106/`：重命名 27 的非空推理补采样仍在进行。

训练 ZIP SHA-256：`d0bac56a8987fb5657284be68d9f3bd1963def20f458e742185c53d62f0dbd3b`。包内 **1104 个文件全部通过 checksums 校验**。这只证明传输/打包一致，语义与协议另外检查。

## 之前的问题是否解决

| 问题 | 本轮发现 | 状态 |
| --- | --- | --- |
| A5 缺 GPT 分支 | 新增 `ablation-complete-branches-20261105/cases/multi_turn_base_12/supplement/external_structured/seed-71782927`，有指导与成功执行 | 已补齐，不再沿用“没有现成 GPT”结论 |
| A5/A2/A3 指导相近却结果不同 | 扩充运行与分支，不等于产生新的可解释指导差异；原先的语义相同/正确指导下执行波动问题仍在 | 未解决，不恢复旧优势叙事 |
| 训练 student 思考为空 | 新业务数据确有实际模型生成思考，再以同模型延续动作；before/reference/after 均可溯源 | 已改善，是两阶段新采样，不是补写旧日志 |
| 指导一直留在续跑中 | 新选业务/BFCL 首轮指导、之后撤去的请求记录可核实 | 已改善 |
| 业务训练只用 SQL/终局判据作为局部接受 | `effective-local-acceptance` 仍未读取 reference 状态/返回；资产是 SQL，银行是 native task verifier | 未解决 |
| 新 BFCL 局部参考比较 | 有执行成功与 reference state equality，并在继续前检查 | 写状态动作有实质进展；读取动作还缺返回信息比较 |
| 旧订单提交、转账关联优先候选 | 订单的新参考失败/最新尝试未完成；转账新思考完整但仍 SQL gate | 尚未补齐此前要求 |
| 预约同日语义 | 新训练 BK-20 创建于 2026-11-05，就诊仍是 2026-02-03，标志为1；没有日期一致性修复 | 未解决 |
| 酒店与资产旧问题 | 酒店210价格仍无独立来源；资产仍有重复未归还记录和过去截止日 | 未解决 |

业务两阶段解码的实证：原始 thinking completion 的内容与 `reasoning.txt`/hash 一致，action 请求逐字接续该 reasoning；同一标准模板，无人工思考补写。它设置了最小 thinking 长度并重新采样，需与旧 temperature0 记录区分。细节见 [业务训练审核](cases/training/latest-core-audit-20261106.md)。

## 值得优先考虑的案例

### 训练

1. **长上下文50：工具列表编号不能成为工具名。** `training-bfcl-long-context-search-20261106/training/cases/multi_turn_long_context_50/`。before 反复调用 `mcp_tool_16_lockDoors` / `mcp_tool_20_setHeadlights`；指导明确实际工具名，after 使用正确名字解锁，局部状态与参考相同，通过后撤去指导，再打开车灯。动作与推理相符。信息偏接口纠错，展示时明确编号混入工具名，避免变成无意义的拼写差异。该例的来源/格式消融各对照都成功，不要同时包装为消融优势。
2. **国际交易限制 banking_6_2：填白名单还要启用限制。** 指导把错误的 `international_allowed=1` 改成0，before/after 推理、调用、数据库一致；工具 schema 明确0表示 enforce allowed countries。内容最强、阅读成本低，但业务局部 gate 未接 reference。作为下一项补验证的优先素材，不通过改名掩盖这一缺口。
3. **base37：创建文件后写入第二个匹配句。** 最终指导、创建动作和写入内容正确，after 的计数混乱有真实后续修正。首个 touch 是有意义的写状态匹配。该指导来自 attempt2，实际反馈含较早完整续跑的终局错误内容，不是只根据首轮局部拒绝改写；应保留这条来源差异。比前两例叙事成本高，列后备。

base92 的“读余量后补足”动作易懂，但接受的是读取后的不变状态、未比较返回；Teacher 分析还有不准确的过程复述。188/192 发票例的推理仍有矛盾，110 训练 before 后来已自行登录、全局失败另有描述字段问题。酒店、预约、资产不因新包标签而升为可用主例。详见 [新训练审核](cases/training/latest-new-audit-20261106.md)。

### 消融

**首选：base110「先登录工单系统，再创建工单」。**

来源 `new-ablation-pipeline-20261105/ablations/cases/multi_turn_base_110/`。比较 `source-training-case/after/attempt-0` 与 `variants/teacher_freeform/student`：

- Ours 四字段明确未认证时先 `ticket_login`，成功后再建工单。实际顺序 login → create，最终工单队列有1条；完整执行思考先厘清认证前提，再执行，两步一致。
- Teacher 自由文本输出的是“工单已成功创建”的完成回执，没有给修正过程。对应 agent 直接 create 得到未认证错误，随后 login，却不重试 create 就宣布完成；最终队列为空。
- 两条首次执行的上下文/初态 hash、seed 71785000 和 temperature0.6 一致，不是换失败 seed 形成的对照。实际请求分别注入上述完整指导。
- 这次能指明指导的具体问题：把需要修正的行动过程写成已经完成的结果。不是“相同正确指导一成一败”。但不将单例扩大为所有自由文本必然如此。
- Student 结构化同样成功，如实保留；GPT 也正确指出登录前提，不能把它的其他描述问题硬塞成该前提的失败对照。区分交易会话已经登录与独立工单会话未登录。

协调者已独立阅读上述两条完整关键思考、指导和调用序列。推荐制作时只展示工单请求，不复述前五轮交易背景。旧训练 before 与本例自由文本 continuation 不是同一个分支，不能混用。

**次级候选：marketplace 商品所属供应商。** Ours 指导指出账号公司2并非商品供应商3，首轮正确查询3；Student 指导主要复述失败，把纠正建议放在核验字段，实际仍查询2。存在局部信息差，但自由文本已正确要求跨供应商搜索，不能把它的重复查询说成指导没有纠正。五分支最终均成功，只能围绕首次局部修正展示，价值弱于110。完整思考在两阶段 sidecar，不因普通 response.reasoning 为空误报缺失。

其他新补的换汇180、重命名36、菜单查询及旧三例未形成同样清楚、干净的指导差异故事。详见 [最新消融审核](cases/ablation/latest-delivery-audit-20261106.md)。

## 仍运行的补采样

截至 **2026-11-06 10:51（Asia/Shanghai）**，`ablation-nonempty-thinking-20261106/result.json` 仍为 completed=false，只选中 Teacher freeform seed71840078，Student 仍在采样。该 freeform 失败确实补齐了非空思考；原指导为字面的 cd 工具调用，actor 将它当成“之前调用过 cd”，最终没有完成重命名。这比空白思考多了一个格式误读线索，但尚无完整配套对照，用户已经移除27，不建议因此重加。新采样仍以找到失败为停止条件，不把采样次数当随机失败率。

快照 result SHA-256：`0b02d2b13788d98c63b7f05c59ec63c2712d97fc3361a6892cc8b00e5839af2d`。这只是审查时点，不承诺后续任务状态。

## 下一步建议

先审阅/制作 **消融110** 与 **训练长上下文50**；同时优先补国际交易限制的 reference 局部验证，再考虑加入完整训练模板。其余不按包数量扩展。A5新增GPT资料可保留，但它不改变该例原有因果问题。本轮网站、目录、正文和原始数据均未修改，未发布。
