# 创建工单前，先登录工单系统

## Selection and comparison

Selected as a focused ablation, defaulting to Teacher structured versus Teacher freeform. The information is a concrete missing prerequisite and an unperformed action: the ticketing session is separate from the authenticated trading session. Structured guidance asks the agent to log in first. The freeform output instead announces an already-created ticket; its actor attempts creation without login, logs in after rejection, and then announces completion without retrying creation. Final ticket queue is empty. The page describes these observed instructions and actions rather than asserting a general win rate or that the wrong freeform statement uniquely caused every later decision.

Retain the actual successful Student structured branch. GPT's final instruction is correct, including an explicit prohibition on putting credentials in the ticket description; its actor logs in correctly but later includes credentials in the created ticket. This is an execution/instruction-following difference, **not** evidence that GPT supplied bad login guidance. The real unguided original run also recovers from the authentication error and creates a ticket containing credentials. It is not the freeform branch and must not be described as failing to create a ticket.

The user request has an unmatched opening quote around the description, followed by credentials explicitly identified as “for the ticket login.” The website reports the additional credentials concretely, rather than inflating an exact-description mismatch into a complete task failure or a claim about security. The decisive default comparison does not depend on that ambiguity: the freeform branch creates no ticket at all.

## Source package and provenance

- Imported the complete case, 325 files / 8,344,402 bytes, unchanged from SSH host `neogpu-a100-nx-1`, directory `/mnt/genming/new-ablation-pipeline-20261105/ablations/cases/multi_turn_base_110/`.
- Repository source root: `data/cases/ablation_case/reviewed-20261106/multi_turn_base_110/` (abbreviated `RAW` below).
- `RAW/import-manifest.json` records every raw file SHA256 and size, remote origin and branch audit. An independent remote SHA256 inventory matched all 325 local files. The added import manifest itself is not a raw source file.
- No reruns, remote edits, source rewrites, branch re-selection or synthetic unguided continuation.
- Full-case inventory is available in the shared record reader's secondary picker. Five trajectories, original guides, scores, local gate and task definition are primary sources.

| Method | Directory below RAW | Actor messages | Seed | Outcome |
| --- | --- | --- | --- | --- |
| Teacher structured | `source-training-case/after/attempt-0` | 26–30 | 71785000 | login → create; one correctly described ticket |
| Teacher freeform | `variants/teacher_freeform/student` | 26–30 | 71785000 | rejected create → login → false completion; no ticket |
| Student structured | `variants/student_structured/student` | 26–30 | 71785000 | login → create; one correctly described ticket |
| GPT structured | `variants/external_structured/student` | 26–30 | 71785000 | login → create; credentials also in description |
| Unguided | `source-training-case/before` | 26–32 | 71782826 | rejected create → login → retry create; credentials in description |

Every `restore.json` has the same context hash `602ab2e2b7bdab5b62e77e794eb85a05b809c2cdab7f3bb8cebaca5f9d24f43a` and state hash `bd2614f3c9e94df8536d7be5c5fbb86ca981f496d2f4ce5c0d0d10a192c4b139`. Independently compared each first actor request's role/content prefix against `source-training-case/anchor-context.json`: all messages 1–25 are identical. Request serialization drops the duplicate reasoning/tool-call metadata while preserving content. Every guided request 0 adds its actual guide to the system message; requests 1 onward restore the unaugmented system prompt. Temperature is 0.6. The unguided seed differs, so it is supplementary, not a matched-seed control.

The structured source's `local_gate.json` is a successful execution/reference-state-equality gate before continuation: `TicketAPI.current_user` becomes `user123`, queue remains empty. This is distinct from its final task check and from the Teacher's suggested recovery check. No page text claims the agent ran an extra verification call or that guide fields alone prove acceptance.

## Claim and excerpt map

All message indexes are zero-based in each `trajectory.json`; execution event indexes are zero-based in each `execution.json`.

- Title/summary: `task.json.question[5]`; every restore's `TradingBot.attributes.authenticated=true`, `TicketAPI.attributes.current_user=null`, `ticket_queue=[]`. The summary omits five rounds of trading history; the original-task disclosure preserves all six original user messages verbatim and in order.
- Primary structured calls: messages 26/27 login and return; 28/29 creation and return; execution events 7/8. Full terminal reasoning/reply at 30 was reviewed and matches successful creation.
- Primary freeform calls: messages 26/27 rejected creation, 28/29 login, 30 false final claim; execution events 7/8 and final state. There is no subsequent create event or tool call.
- Student calls: 26/27 login and 28/29 create, execution events 7/8; its terminal message 30 is correct.
- GPT calls: 26/27 login and 28/29 create, execution events 7/8. The latter description includes the login credential sentence. Final message 30 truthfully confirms a ticket exists, so it is omitted rather than colored as false completion.
- Unguided calls: 26/27 rejected create, 28/29 login, 30/31 retry create, execution events 7/8/9. Message 32 confirms creation but does not disclose that credentials are in its stored description; no claim that it failed to recover authentication.
- All execution-result rows derive from the final event's `after.TicketAPI.attributes`: `current_user`, `ticket_queue`, `ticket_counter`, and queue item `description/status/priority`. Scores are supporting records, not the source of behavioral coloring.
- Original guidance: `source-training-case/steering/attempt-0/raw_steering_prompt.txt` for Teacher structured; `variants/{teacher_freeform,student_structured,external_structured}/guidance/raw_steering_prompt.txt` for others. Full fields preserved without translation or correction. Default excerpts are the actual decision rule, except the freeform opening sentence.

## Full reasoning / guidance review and contradictions

Reviewed full guide contents and complete actor reasoning from message 26 to the final answer for every branch, not only displayed quotes.

Teacher structured advisor analysis opens with an imprecise claim that placing credentials in the description led to authentication failure. Later it explicitly locates the skipped login step and prescribes login then creation. The final four fields are correct for this anchor. The page retains the **entire** advisor reasoning in the existing full-guidance disclosure, with the imprecise early causal clause red and its later accurate missing-login diagnosis blue. It does not label this explicit self-reflection or erase the earlier wording. Actor message 26 considers competing possibilities but concludes login then create; message 28 builds the requested description, without the credentials, and actually creates the ticket. This supports the focused prerequisite contrast, not a claim that all advisor analysis was flawless.

Freeform advisor output is an actual completed-ticket message, not a procedural instruction. Its actor message 26 vacillates on credentials and even proposes including them in thought, but the actual failed create call omits them. The page does not substitute that proposed argument for the real call. Message 28 correctly responds to the authentication error. Message 30 falsely treats the task as fulfilled after login; the retained reasoning excerpt is from this point, not from before the first call.

Student structured guide and execution are correct. Message 26 contains uncertain speculation before settling on the proper order; the retained sentence is that explicit decision. Later message 28 and actual arguments exclude credentials. No failure is manufactured for this comparator.

GPT message 26 correctly states the prerequisite. Root requested a second inspection of message 28: it mentions that the user provided a title, description and username/password, then abbreviates the description as “There is an issue ... AAPL...”. It never explicitly reasons that credentials should be included, and contains no corrective reflection that removes them. Therefore, **no fabricated red reasoning span** is added. The wrong description is established by its actual call and stored ticket. Its displayed reasoning remains blue because it genuinely selects login first. Its guide explicitly says not to include credentials and is colored blue accordingly.

Unguided message 26 wrongly reads the login credentials as ticket text; message 28 diagnoses authentication correctly; message 30 correctly retries creation but again says “the user insisted on including it.” The selected message-30 passage preserves both that mistaken reading and the retry decision in order. This makes the recovery visible without implying that retry fixed the description too.

## Per-passage annotation decisions

No token-based selection or inferred comparison diff was used. The following are individual local judgments; words left unmarked were reviewed as part of the full passages above. Blue means a correct local decision/state, red a missing prerequisite, false claim or misplaced credential content. Overall frame colors do not override event-level judgments.

### Teacher structured

- Login event 7 / msg26: blue call name `ticket_login` emphasizes the prerequisite missing in the primary comparison. Arguments are omitted, not highlighted; their literal synthetic credential values add no explanation. Return `success=true` is blue without extra background.
- Create event 8 / msg28: correct call and return blue; only `status="Open"` receives a blue background to show actual creation. Title/priority are neutral syntax within the correct event, with no separate highlight because they do not distinguish these branches.
- Reasoning msg26: mark `first authenticate, then create the ticket.` blue. This is the causal ordering, not a generic confidence statement; remaining exact sentence text is unmarked.
- Guide decision rule: mark `before creating the ticket` blue, foregrounding the prerequisite rather than all four fields.
- Advisor full analysis: mark the exact initial clause `which led to an authentication failure because the ticket creation tool didn't accept credentials.` red; later `the assistant skipped the login step and directly attempted to create the ticket, leading to the error.` blue. Other analysis remains unmarked.
- Results: mark `已登录`, `工单已创建`, `没有写入用户名和密码` blue. These are three distinct observed state/content facts; priority and status wording need no additional mark.

### Teacher freeform

- First creation msg26: red call reflects premature creation. Return's `User not authenticated.` gets red emphasis; the subsequent instruction in the same error message remains unmarked.
- Login msg28: event and return blue despite the red branch frame. No background highlight; the recovery is visible through color and order and should not become a false failure.
- Final reply msg30: only `has been successfully created` red. Keep title/priority unmarked; the error is claiming completion without a created ticket.
- Reasoning msg30: only `The user's request has been fulfilled` red. It explains why execution stops after login; neighboring wording is left intact, not rephrased as a stronger causal claim.
- Freeform guide: only `has been successfully created in your name!` red. This is the central substantive difference from a valid prerequisite instruction.
- Results: `已登录` blue, `工单队列仍为空` red. This distinguishes successful authentication from actual task completion.

### Student structured

- Login msg26: `ticket_login` blue to show the same valid first action as Teacher structured; successful return blue, unmarked.
- Create msg28: blue event; `status="Open"` blue background. Other common args remain unmarked.
- Reasoning msg26: `first log in using the provided credentials, then create the ticket.` blue, recording its correct final choice without coloring the preceding uncertainty.
- Guide: `Always use the ticket login tool first` blue, direct prerequisite support. No criticism of “always” as a generic policy is inferred from this single task.
- Results: `已登录`, `工单已创建`, `没有写入用户名和密码` blue, all checked against stored state.

### GPT structured

- Login msg26: `ticket_login` blue; return blue. The guide and execution get credit for correct authentication.
- Create msg28: event red for the actual wrong description. Highlight only the excerpt `My username is … and password is …` red; title and priority do not need emphasis. Its successful API return is **neutral**, because acceptance does not establish that the contents follow the requested separation.
- Reasoning msg26: `Once logged in, then create the ticket.` blue. Msg28 reviewed but not added/marked as a speculative explanation of credential copying, as detailed above.
- Guide: `do not include the password or other login credentials in the ticket description.` blue, explicitly showing that this mistake is not endorsed by the guide.
- Results: `已登录` and `工单已创建` blue; `包含了登录用户名和密码` red. A single branch therefore has both successful steps and an incorrect stored field.

### Unguided

- First create msg26: red action, `User not authenticated.` red; credential excerpt red because its arguments already contain those details.
- Login msg28: corrective action and return blue, no background. Do not mark it red from the terminal task score.
- Retry create msg30: credential excerpt remains red, accepted return neutral. Preserve this second create event, since omitting it would turn successful recovery into the freeform failure.
- Reasoning msg30: `But the user insisted on including it.` red marks its mistaken reading; remaining text retains the real retry decision without blanket coloring. The source request says the credentials are for login; the page does not embellish this into a general policy assertion.
- No guide or fake guide excerpt. Shared interface renders “未提供指导”.
- Results: `已登录` and `工单已创建` blue; `包含了登录用户名和密码` red, matching GPT's identical content problem without implying identical lineage.

## Display transformations and exact checks

- Call names omit only `mcp_tool_`; execution records already use the suffix tool name. Tool order is unchanged, and all post-anchor calls are represented.
- All action frames are labeled “调用与回复 · 节选”. `ticket_login(…)` omits username/password values. Correct creation shows title and priority plus an ellipsis for the shared description. Credential-bearing creation shows the exact `My username is` / `and password is` / `for the ticket login.` fragments separated by explicit ellipses, omitting the literal credentials and common business description. No masked value is presented as the actual argument. The untouched call remains in records.
- Result excerpts select actual `id`, `status`, `priority` fields; authentication error text is unchanged, wrapper `success` is not mistaken for operation success.
- Final freeform reply and freeform guide opening remove only Markdown `**` delimiters; textual wording is otherwise exact. Full original guidance retains its delimiters.
- All five actor reasoning excerpts and the full advisor analysis were checked character-for-character against their identified source `reasoning` fields. Every marked English reasoning/guidance substring was rechecked in the matching original text (after only the documented freeform bold-delimiter removal). Chinese result spans are editorial state summaries, not quotes.
- UTF-16 offsets are computed from manually chosen literal spans. The shared validator passed: 36 exact spans, 326 source URLs. This validates rendering integrity, separately from the semantic review above.

## Handoff / remaining acceptance

- Case JSON: `design-lab/case-content/ablation/ticket-login-before-create.json`.
- Preview: `/design-lab/paper-cases.html?group=ablation&case=ticket-login-before-create`.
- Records: `/design-lab/case-records.html?group=ablation&case=ticket-login-before-create&source=source-training-case%2Fafter%2Fattempt-0%2Ftrajectory.json&message=26`.
- Uses the maintained comparison template, row-based guidance/results, exact semantic span interface and shared records inventory. No CSS, renderer, catalog, article embed or other case modified.
- Independent author source/editorial checks completed. Coordinator owns desktop/narrow layout, selection/folding and record-reader visual acceptance, followed by catalog integration. User acceptance remains pending.

## Coordinator integration

Registered after source review for local preview. Desktop/narrow interaction and record-reader checks, integration edits and user-review status are recorded in [the batch review](../../case-batch-20261106.md). This supersedes the pending coordinator QA status at author handoff; user acceptance is still pending.

## 2026-11-06 中文编辑与重编号

当前编号 A1（原 A6）。结果标注改为“没有写入用户名和密码”，事实、来源和正向颜色含义不变；其余中文描述按 [统一编辑记录](../../case-copy-renumbering-20261106.md) 更新。
