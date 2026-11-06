# 2026-11-06 新消融交付核验

## 结论

新交付补齐了若干原始记录、重放核验及 A5 的 GPT 分支，但没有修复 A5、A2、A3 原先的指导—结果因果缺口。不能因目录更新或重新选中失败 seed 就撤回 [上一轮审查](../../ablation-causal-review-20261105.md) 的结论。

额外扫描新 pipeline 后，**`multi_turn_base_110` 工单认证是最值得优先复核的新增候选**：结构化指导要求先认证，自由文本却输出“工单已经创建”的回执；实际分支分别创建成功、未创建却报告成功。两支起点及 seed 相同，且有完整非空执行思考。这比“相同正确指导，一成一败”更符合本次标准。仍应把主对照限定为 Teacher structured / Teacher freeform；Student structured 也成功，GPT 的失败与其正确指导相矛盾，不适合混作同一机制优势。

Marketplace 查询属于次级的**局部信息补全**候选；其他方法最终也完成任务，且 Teacher 分析有摇摆，不建议优先放入当前强调明确成败的消融精选。其余新项暂不加入。

本次只读核查。没有更改网站数据、运行实验或发布页面。

## 来源与核查方式

服务器别名 `neogpu-a100-nx-1`，远端根目录：

- `/mnt/genming/ablation-evidence-delivery-20261105`：README、`selected-branches.json`、site-comparison 与重放报告；不是独立的新实验根。
- `/mnt/genming/ablation-fixed-checkpoint-rollouts-20261105`：delivery 的 `fixed-evidence` 指向这里。
- `/mnt/genming/ablation-complete-branches-20261105`：delivery 的 `previous-evidence` 指向这里，补充方法与 seed 在这里。
- `/mnt/genming/new-ablation-pipeline-20261105`、`new-ablation-pipeline-batch2-20261105`、`new-ablation-pipeline-batch3-20261106`。

逐项读取实际注入指导、checkpoint、执行思考、工具调用、返回与状态；没有把 selection/review 的 qualified 字段作为结论。Marketplace/menu 还读取两阶段解码的 thinking 响应和 action 请求，避免把最终 action 响应的空 reasoning 误判为没有思考。

10-case delivery 含 50 个已选择分支，7 个整项结果对照、3 个 local-only 对照。README 明示这些是 outcome-selected、可能混合 seed 的例子，不能当作配对统计。离线 replay 能验证存档动作与状态，不会修复指导本身的错误或创造因果证据。

临时读取快照在本机 `/tmp/ablation-latest-audit-20261106/`，仅作本次审计缓存，不是长期证据源；重建时以以上远端树及分支路径为准。

## 最优新增候选：110，先登录工单系统再创建

路径：`new-ablation-pipeline-20261105/ablations/cases/multi_turn_base_110/`。

| 分支 | 实际指导 | 实际后续与结果 | 展示价值 |
| --- | --- | --- | --- |
| Teacher structured | 未认证则先 `ticket_login`，再创建；核验 `TicketAPI.current_user` | login → create，队列中出现正确优先级和描述的工单 | 主分支 |
| Teacher freeform | 回答“support ticket … has been successfully created”，没有给出认证指令 | create 返回未认证 → login 成功 → 未重试 create 就报告完成；最终队列为空 | 最有价值的失败对照 |
| Student structured | 同样明确先认证再创建 | login → create，成功 | 应如实保留成功，不能标成失败 |
| GPT structured | 明确先认证，且禁止把凭据放进工单描述 | login → create，但把凭据写进描述；任务检查失败 | 指导正确却未遵守，不作为指导内容优劣主证据 |

### 已核实的起点与因果

- Ours：`source-training-case/after/attempt-0`；freeform：`variants/teacher_freeform/student`。
- 两支 `restore.json` 的 context hash 都是 `602ab2e2b7bdab5b62e77e794eb85a05b809c2cdab7f3bb8cebaca5f9d24f43a`；state hash 都是 `bd2614f3c9e94df8536d7be5c5fbb86ca981f496d2f4ce5c0d0d10a192c4b139`。
- 两支首个 actor 请求都是 seed `71785000`、temperature `0.6`；差异确实进入首条 system 的 `Local steering for this response only`。
- 初始 `TicketAPI.current_user=null`、`ticket_queue=[]`。交易会话 `TradingBot.authenticated=true`，不代表独立工单会话已经认证。通用 system 中的 “already logged in” 应在解读时结合具体环境区分，不能隐去两个会话。
- Freeform 指导生成 prompt 明确要求“free-form procedural guidance”，并禁止冒充 student 或返回替代工具调用；模型真实生成了成功回执。不是作者人为把正确指导改成错误描述。
- Freeform 最后思考承认之前 create 失败，却说 “No further actions are needed … The user's request has been fulfilled”；执行记录只有失败 create 和成功 login，最终 ticket_counter=0。成功报告与真实状态的脱节可直接展示。
- Ours 三次响应的 reasoning 均非空、finish=stop；登录后思考明确转向 create，调用和最终状态正确。

### 需要保留的限定

Ours 的 advisor analysis 开头把“描述中包含凭据”与“未登录”混说，随后明确定位为 skipped login；最终四字段指导正确。若要求连指导模型完整思考的每句因果措辞都完全无瑕，这一点仍需由主审判断。正文应展示实际注入的四字段，并保留完整原始分析可查，不能把前句改写成模型原话。

当前足以作为下一步重点候选，但不应扩写成“GPT/Student 都不如 Teacher”或从一例推出格式的总体效果。该目录 outcome 只列四种有指导设置；制作时还需直接使用同 checkpoint 的真实无指导记录，不能自行编造第五支。

## A5 新增 GPT：数据缺口已补，机制缺口未补

新增分支：`ablation-complete-branches-20261105/cases/multi_turn_base_12/supplement/external_structured/seed-71782927`。

- 实际指导正确：当前目录 `/alex`，目标 `/alex/Documents`；先 `cd Documents`，不要直接 `touch`；核验目录切换，后续再执行任务。
- GPT 与已选 Ours 首次请求 `messages[1:]` 完全相同，均为 seed `71782927`；Ours 保存的 context/state hash 分别以 `6d8f432f`、`69828459` 开头。
- GPT actor 思考明确知道 find 不等于改变当前目录，并据指导先 cd；随后 touch `summary.txt`，完整任务通过，最终回答与结果一致。
- 因而“没有 GPT 例子”已过期，可补成成功分支；但 Teacher/Student 的行动规则仍相同，旧失败选择并未变成可解释的指导差异。**补齐分支不等于恢复 A5 的消融主例资格。**

## 10-case delivery 逐项取舍

| 数据 ID | 复核结果 | 优先级 / 建议 |
| --- | --- | --- |
| 51，锁车（A2） | 指导语义相同的旧问题仍在；新重放没有补出关键内容差异 | 不恢复机制优势推荐 |
| 12，目录创建（A5） | GPT 新补成功且指导正确；Teacher/Student 同指导问题仍在 | 可补资料，不能以此重推主例 |
| 61，加油 7 单位 | Ours 的完整推理存在未解释的错误/摇摆，不能只看正确动作与通过标签 | 暂不加入 |
| 74，38L 单位换算（A3） | 正确同义指导执行结果不同，原先 seed/执行服从问题未解决 | 不恢复机制优势推荐 |
| 180，人民币预算转美元 | Ours 正确换算后写入约 2857.14 USD；其他指导也明确要求先换算，失败 actor 却无视。GPT/Student 的初始预算描述另有错位 | 不是清楚的指导内容优势；暂缓 |
| 36，复制后改名 | Student 没给明确 cd 前提，实际停止；但 Teacher 完整分析把源文件查找失败与目标路径问题混淆，且推演状态与已保存 checkpoint 不完全一致 | 低优先备选，未达完整 Ours 干净标准；题材也与已移除重命名例重复 |
| 27，workspace 改名 | 旧交付仍不能靠选中失败解决同义正确指导问题；用户已移除 | 不自动重加；11-06 nonempty-thinking 由主审另记 |
| R02A，archive 改名 | Teacher 分析有错误，其他分支后续恢复成功 | 不加入当前消融精选 |
| Marketplace SKU 查询 | Teacher/GPT 给出正确 supplier 3；其他指导沿用 supplier 2 或笼统 fallback，第一步分别命中/空。最终全部完成 | 次级局部纠正候选，详见下文 |
| Menu 查询 | 指导已给正确 partial keyword/slug，失败执行仍用展示名；初始状态已满足终局目标；若干所谓 thinking 只有标记 | 不加入 |

### Marketplace：可辨认的局部信息差异，但不是终局失败

路径：`ablation-complete-branches-20261105/cases/b2b_ecommerce_marketplace_1_1-f40c9131dfa4-aligned/`，实际 selected 分支在 `supplement/<role>/seed-42`。

共享前缀列出 company 2 为 supplier，但用户在该公司的角色是 buyer_contact；目标商品实际所属 supplier 3。Teacher/GPT 最终指导明确给 3；Student 指导仍围绕 2，freeform 让后续再广搜。Teacher actor 的完整思考先打算试 2，随后明确写出 “the steering says … supplier_id=3 … I will follow”，最终查询 3 命中。其他分支先查 2 返回空，再搜索并完成。

这是可解释的局部信息修正，不应因最终都成功就认定毫无价值。不过它主要说明正确状态信息进入指导，而非当前网站希望突出的终局成败。Teacher advisor analysis 对 2/3 的推理有反复，正确 ID 来自已验证参考；需要完整披露其输入来源，不能包装成 agent 仅从自身前缀推得 3。

该 AWM 分支采用 two-phase generation：`turn-000/thinking/native-generation/response.json` 保存思考，随后 `action/request.json` 通过 assistant reasoning continuation 传给动作阶段。不能只读 action response 的空 reasoning 就说“未保存思考”，也不能把它描述为单次原生 API 自动返回的完整 reasoning。核查两份文件内容相互对应。

## 其他新 pipeline 清点

| 批次 | task 数 | 进入 ablation 的 case | 有失败对照的自动候选 |
| --- | --- | --- | --- |
| new-ablation-pipeline-20261105 | 48 | 110、192、188 | 110 |
| new-ablation-pipeline-batch2-20261105 | 48 | 37、92 | 37 |
| new-ablation-pipeline-batch3-20261106 | 25 | 未生成 ablation 结果 | 无 |

这里按实际 outcome 的 `ablation` 字段清点，不是 `ablations`。192、188、92 没有失败 control，未扩展为精选。

37 要把“包含 server error 的第二个句子”写入 `1.txt`。Student 指导遗漏先建文件，确实先 echo 报错；但终局的错句还涉及把 “No server error occurred …” 错判为不包含该短语。Teacher 自由文本实际上已经给出正确 touch + 正确句子的工具调用，执行仍写错。Ours advisor 对旧失败内容的叙述也与实际引用不稳定。多个问题混杂，不能把全部成败归结为指导结构，优先级低于 110，暂不推荐。

## 旧 01 / 02 / 03 遗留问题

本次 10-case delivery 与三个 new-ablation-pipeline outcome 中，**未找到旧 01 定价、02 时间范围、03 同日预约的修复版消融**。不能以“fixed checkpoint”目录名视为这些语义问题已修复。

03 另有训练新包，但并非消融修复证据。训练审查代理实际读取了 `training-clinic-corrected-retries-20261106/seed-101/cases/...004_booking_and_scheduling_11_4/after/final.db`：BK-20 booked_at 为 `2026-11-05 16:34:52.228088`，SL-3004 就诊时间仍在 `2026-02-03`，same-day flag 仍为 1；system 未提供冻结日期说明。新对照改成了重复建 slot / 复用 slot，不解决原来的同日字段语义矛盾。此处是协作复核记录，精确来源以训练审查报告为准。

旧 01/02 在上述新消融范围未找到新版，故只能维持“未看到解决证据”，不推断整个服务器不存在其他版本。

## 下一步建议

1. 优先独立复核 110，决定是否接受其主对照及完整 advisor analysis 的措辞瑕疵；接受后再制作页面，不先改现有案例。
2. A5 的 GPT 可作为原始记录补全，但不把它当作 A5 原有因果问题已解决。
3. Marketplace 留研究备选；37、36、180 不抢在干净例子之前上线。
4. A2/A3/A5 继续沿用上一轮机制展示暂停结论；01/02/03 等待真正对齐环境语义的重新生成数据。
