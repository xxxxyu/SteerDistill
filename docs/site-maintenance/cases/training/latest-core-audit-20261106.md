# 最新训练案例：旧核心候选与两项业务修正复核 · 2026-11-06

只读检查 nx 数据及代码；没有运行模型、修改远端或修改展示页面。使用 steerdistill-case-editorial 标准，区分可读的行为修正与论文 reference-matched local acceptance。

## 结论

- 新包中 **banking_6_2（国际交易限制）** 的行为解释最清楚：前后 student 思考现已真实非空，指导明确纠正开关语义，调用与数据库由 `international_allowed=1` 改为0，白名单保持 US,CA。作为“局部指导修正”素材明显改善。
- **asset_management_2_2（资产借出地点）** 也补齐真实思考，指导—字段—状态对应清楚，但初态已有同资产、同借用人、同项目、未归还记录的问题未解决；降低优先级。
- 两例的旧核心协议缺口 **仍未解决**：执行时 gate 仍为 SQL predicate 或 native terminal verifier；没有用 reference 的实际状态/返回进行局部比较。新 reference 重新生成，steering 则复用旧记录，不能描述为本次 before 触发的新闭环教师修订。
- 原先优先的 **订单提交 b2b_marketplace_1_7** 未找到完成协议修复的新合格版本；**转账关联 banking_6_4** 有11月5日更新的完整行为对照，但 gate 仍为SQL谓词，尚未补上 reference-matched acceptance。

## 入口、运行来源与检查范围

最新交付入口：`nx:/mnt/genming/training-case-supervision-20261106/packages/training_steering_9_cases_20261106.zip`。只读下载并解包检查。

本报告两例对应包内：

- `cases/001_asset_management_2_2/`，原始运行 `training-eight-paired-resampling-20261106/seed-101/cases/asset_management_2_2/`。
- `cases/003_banking_6_2/`，原始运行 `training-eight-paired-resampling-20261106/seed-303/cases/banking_6_2/`。

检查完整 before/reference/after trajectories、Teacher 原始 analysis/reasoning/prompt、各分支首轮及下一轮请求、thinking/action 两阶段原始响应、local_gate、SQLite 初态/终态、tool schema/environment，以及源代码：

- `/mnt/genming/case-rerun-20261103/repeat_original_training_pairs.py`
- `supplement_original_eight_thinking.py`
- `training_strict_original_model.py`

代码链由 repeat 调用 supplement；supplement 导入 strict runner 后替换生成函数，gate 仍调用 strict runner 的 `condition()`。

## 已修复：student 思考不是事后补写

两例所有 before/reference/after 的关键决策及结束回复均有思考原文。`thinking/response.json` 的实际模型输出包含 `reasoning.txt`，SHA-256 与 `thinking_proof.json` 匹配；`action/request.json` 最后一条 assistant reasoning 与该思考逐字相同。它使用同一模型先生成至少16个 thinking tokens，再从该思考继续生成动作；不是把人工思考粘到旧轨迹上。

但这是新的两阶段解码与重采样，**不是恢复旧运行缺失的 thinking**。`supplement-protocol.json` 已记录 `original_generation_not_recovered` 等边界；metadata 原 protocol 的 temperature0/seed42不能拿来描述新输出。当前资产 before/after 为temperature0.6、seed101，交易限制为temperature0.6、seed303；reference 首次运行temperature0，seed对应一致。新包保留同任务、工具和 pre_state。

原始 `turn-000/original_request.json` 非system history逐项等于包内 context；after首轮system确实追加完整local steering，下一轮恢复原system。reference/before两轮都无指导。思考原文中已提到指导的内容会留在后续历史中，不能将“撤去system指导”写成“从未见过指导”。

## 未修复：运行 gate 不比较 reference

`training_strict_original_model.py:58` 的 `condition(case,db,spec)`：

- 当 table 为 `__native_task_verifier__`，运行完整task verifier，以complete为通过；
- 否则查询固定SQL predicate，`bool(rows)`决定通过，并列出相对pre_state的changed_records。

该函数不读取任何reference DB、reference observation或transition。`branch()` 在首响应执行后复制 local_state、调用condition、写local_gate，再决定是否续跑（约113–118行），所以“检查先于续跑”是真实的，但检查内容仍不是reference-matched acceptance。`effective-local-acceptance.json` 只是重述effective predicate，不能当作接入新比较器的证据。

`supplement_original_eight_thinking.py` 对reference也独立检查相同谓词，之后调用before/after。最后的qualified综合reference和after各自通过，不比较两者。不要因after/ref动作恰好相同，把事后人工相符提升为当时自动执行的gate。

## 国际交易限制：建议保留的行为素材

原始任务要求限制 US/CA 以外的国际交易。工具update schema明确：`1 to allow all international, 0 to enforce allowed countries`。

- before轨迹消息10：思考多次正确复述0/1含义，却最终又选择1；调用 `update_card_controls(card_id=5, international_allowed=1, allowed_countries="US,CA")`。实际API支持无旧记录时创建，因此这里不是工具不存在或纯API错误；数据库id5确实保存1。结束回复误称已限制为US/CA，未反思修正。
- Teacher完整指导：明确要求 `international_allowed=0`、allowed_countries=US,CA；分析指出之前误用了1，内容与实际工具定义一致。
- after消息10：明确引用这条指导，调用 `create_card_controls(... international_allowed=0 ...)`；数据库id5保存0。后续无指导消息12准确报告完成。
- reference同样创建0/US,CA，状态与任务一致。前缀卡5已关联账户3、限额2000、active，指导没有更改其他要求。

这是清楚的“纠正开关含义→正确参数→配置状态”实例。展示应写配置限制已设定，不声称真的发起并拦截交易。若要求训练方法正式闭环证据，仍需补正确gate，不能直接加入该类别冒充已完成协议修复。

## 资产借出：字段修正清楚，业务初态仍不干净

- before消息4思考列出资产、用户、项目、due date和note，遗漏location；实际checkout调用也缺 `checkout_location_full_path`，新id3的location FK为NULL。
- 指导明确补地点参数；after思考与调用补入`NYC Office > Media Closet`，新id3的`checkout_location_id=5`。其他任务参数保持一致，source/raw文字未被修饰成更强推理。
- 但pre_state中id1已有相同asset2、user2、project `Q3 Brand Shoot`、同地点、同截止日且`checked_in_at=NULL`。新运行仍创建第二条未归还借出；这个旧业务语义问题未修复。实际checked_out_at又为2026-11-05、用户固定due_date为2025-08-15；不宜扩张成现实有效的借出示范。

推荐继续低优先保留原始证据。若只展示缺location字段的局部记录，行为修正成立；作为高质量完整任务故事，弱于交易控制。

## 原先订单提交/转账候选的更新状态

扫描 nx `/mnt/genming/training*` 中这两个case目录，并核查最新status/outcome：

- 订单：`training-strict-reasoning-20261105/run-seed-{43,44,45}/cases/b2b_marketplace_1_7/outcome.json` 均为 `qualified:false, reason:fresh_reference_not_verified`。更新的 `training-original-candidate-backfill-20261105/seed-46/cases/b2b_marketplace_1_7` 仅到before阶段，没有完整outcome/reference/after可验收。不能把旧订单例自动升为已修复。
- 转账：`training-strict-reasoning-20261105/run-seed-43/cases/banking_6_4/outcome.json` 有完整before/reference/after与非空思考。before新记录payee_id=NULL，after为1，任务对照仍有价值。但local gate为scheduled_transfers表SQL谓词，reference memo="Water and electric bill"而after memo=NULL，仅分别满足谓词；没有状态/返回reference比较。未发现11月6日新选包包含它或另一个完成gate修复的版本。

## 可复核文件指纹

| 包内文件 | SHA-256 |
| --- | --- |
| 001.../after/local_gate.json | `9c4aa9a8322c403de520e32f330df8d525d4e61219bcac663ffbb9e5c685e2fd` |
| 001.../after/turn-000/request.json | `551af0f3a3ab382645128e9cd7a8ea0afeefe382005d6e38a2beaa91975aeeef` |
| 003.../after/local_gate.json | `ed419fd69acc72f8741df0316969bc4c676c8384708614a0ddaea9f4e70afca1` |
| 003.../after/turn-000/request.json | `6771d216d61d2cad043d3757840314198351ec6ced21e51639daeb2eb127a6ce` |
| 003.../steering/raw_steering_prompt.txt | `5990e295d23f934fc033da64a0461ed65542c70f2117b8b0940910156b4e4461` |
