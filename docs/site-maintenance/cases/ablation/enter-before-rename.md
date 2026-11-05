# 重命名文件前，先进入文件所在目录

## Selection and scope

Selected as a focused ablation comparison. The informative unit is the continuation after a failed local rename: structured Teacher guidance leads to `cd` then `mv`; the selected freeform Teacher guidance contains the correct `cd` call, but the executing agent instead ends with a request for a path. Student structured guidance also produces `cd` then `mv`. GPT structured guidance produces an extra `pwd` diagnosis, then the same successful directory change and rename. These are observed continuations under different guidance, not post-training model comparisons or an estimate of a format effect across trials.

The current request is user turn 0, renaming `workspace/project_plan.md` to `project_overview.md`. Later ticket requests are preserved verbatim in the closed original-task disclosure but are not executed or scored in this comparison. All selected execution entries have `user_turn: 0`; all selected scores have `goal_turn: 0`. No later-turn result is used as evidence.

Raw package: [`data/cases/ablation_case/reviewed-20261105/main/multi_turn_base_27/`](../../../../data/cases/ablation_case/reviewed-20261105/main/multi_turn_base_27/). All source paths below are relative to this package. No old target editorial page, catalog description, or target screenshot was consulted. The accepted `sales-order-pricing.json` supplied only composition and shared-interface conventions.

## Chosen runs and anchor

| Method | Selected run | Displayed trajectory messages (zero-based) | Current-request outcome |
| --- | --- | --- | --- |
| Teacher 结构化指导 | `trial-history/teacher_structured/000` | 6–9: `cd`, `mv` | Passed state and execution-response checks |
| Student 结构化指导 | `trial-history/student_structured/001` | 6–9: `cd`, `mv` | Passed both checks |
| Teacher 自由文本指导 | `trial-history/teacher_freeform/000` | 6: final reply | Failed both checks |
| GPT 结构化指导 | `trial-history/external_structured/000` | 6–11: `pwd`, `cd`, `mv` | Passed both checks |
| 无指导 | `unguided` | 6: final reply | Failed both checks |

All four selected guided `context.json` files and their `trajectory.json.messages[0:6]` exactly equal `context/anchor-context.json`. Each selected restore receipt has `verified: true`, `replayed: 2`, state SHA `7e5735defd898fa8f759c192a4bd361c9f355d07f61edf693b828e82dbda6a3c`, and context SHA `5117f2af744637bb4f43e2f7668ab4db88d544e21445881de0cde05f7283701b`.

The unguided run requires separate interpretation: its restore receipt starts before tool discovery (`replayed: 0`) and therefore has a different context SHA. Its state SHA equals the guided restored state SHA. More decisively, its actual first six trajectory messages exactly reproduce the six-message anchor, including tool discovery, the failed `mv`, and the error return. The displayed message 6 is therefore the unguided continuation at that same observed boundary, not an unrelated initial decision. No guidance marker appears in any unguided request.

The common failed call is trajectory message 4, with error return at message 5; `execution.json[1]` records the unchanged file tree. The root directory is `alex` and `workspace` contains `project_plan.md` with content `Initial project plan details.`. GPT's subsequent `pwd` returns `/alex`, directly confirming the parent-directory interpretation. The tool schema in the anchor's tool-list message requires local source and destination names for `mv`; `cd` changes one directory level. This supports the task summary.

## Guidance and continuation protocol

For all four guided methods the authoritative displayed guidance is the exact suffix of `turn-000/request.json.messages[0].content` after `Local steering for this response only:\n`. Structured JSON is parsed into its original four fields; freeform XML is retained as a `guidance` string. The excerpt trims outer whitespace only for freeform display. No wording or escaping within the guidance is repaired.

The first request contains the guidance suffix. Every available subsequent request has the original system message without that suffix. Earlier generated reasoning remains in the conversation as ordinary assistant history. This is one-response guidance injection with continued execution. The freeform run immediately ends and has no subsequent request.

| Method | Full guidance review and relevant qualification |
| --- | --- |
| Teacher structured | Correctly identifies the missing directory change. `decision_rule` says to change to workspace before renaming. `expected_transition` names the eventual rename, whereas the local reference target is only the directory change. `recovery_check` proposes a post-operation file check; no `ls` or other separate existence check is executed. The page claims the recorded rename and verifier result, not execution of every guidance field. |
| Student structured | Correctly specifies `mcp_tool_cd(folder='workspace')` before renaming. Its recovery check also asks to confirm the old file exists before proceeding; the actual path is `cd` then `mv`, without a separate existence query. Guidance reuse provenance is in `methods/student_structured/guidance/provenance.json`; no new advisor reasoning artifact is present in this package. |
| Teacher freeform | Actual final guidance is a `<tool_call>` block for `mcp_tool_cd` with `folder: workspace`, not a vague paragraph or an erroneous action. The guidance-generation reasoning accurately diagnoses the directory dependency. The executing agent's message 6 has only whitespace reasoning and no tool call, so no decision rationale is invented for its failure to follow the suggestion. |
| GPT structured | Correctly asks not to stop or request a path, and to call `cd` once before attempting the rename. The executing agent first calls `pwd`, which differs from that specific instruction and the local reference observation. It then calls `cd` and `mv` and passes the current-request checks. The page describes this successful diagnostic continuation. No standalone external guidance-generation file is available; the actual selected request is the direct source. |
| Unguided | No guidance exists. The JSON omits all guidance and advisor-analysis properties for this method. The shared adapter supplies the absence label. |

`context/reference-alignment.json` reports a verified exact replay and successful reference, with local target response `current_working_directory: workspace`. The selected structured Teacher and Student local-comparison receipts report both `exact_reference_state` and `exact_reference_observation` true. Freeform and GPT report state true but observation false. The serialized state does not expose working-directory identity; the observation is therefore material to this local comparison. In particular, GPT's `pwd` response `/alex` is not the reference `cd` observation. This local mismatch does not imply failure of the later continuation, whose score passes. These receipts remain in complete records; the main result row concerns the actual final file.

## Claim and excerpt map

Display JSON: [`design-lab/case-content/ablation/enter-before-rename.json`](../../../../design-lab/case-content/ablation/enter-before-rename.json).

- Original task: exact `context/task.json.question`, all three ordered user requests. Harness instructions are not merged into this disclosure.
- Method descriptions: selected trajectory messages starting at 6, with the aligned `execution.json` entries below. The common failed prefix is summarized once rather than repeated in each branch.
- Teacher structured actions: `trajectory.messages[6..9]`, `execution[2..3]`. Student actions use the same indices in its own selected run. GPT actions: `trajectory.messages[6..11]`, `execution[2..4]`. Function names preserve `mcp_tool_*` from the actual model calls; arguments and returns are displayed as `key=value` strings sourced from the aligned execution records. Only the transport wrapper and duplicated `<think>` content are omitted.
- Teacher freeform reply and unguided reply: each selected `trajectory.messages[6].content`, removing its empty `<think>` wrapper and trimming outer whitespace. The replies differ and are independently retained verbatim.
- Agent reasoning excerpts: each successful branch's `trajectory.messages[6].reasoning`, before its first continuation action. The display retains a single contiguous paragraph per branch. No later reflection is presented as the earlier decision.
- Teacher advisor analysis reviewed but omitted from the main display: `methods/teacher_structured/guidance/response.json` and `methods/teacher_freeform/guidance/response.json`, `choices[0].message.reasoning`, first paragraph. Complete advisor reasoning was read for both. Its paragraphs elaborate the same correct directory diagnosis and add no material contradiction or new decision beyond the guidance, so they remain in complete records.
- Final filename and preserved content: each selected `execution.json` last entry's `after.GorillaFileSystem.attributes.root.attributes.contents.workspace.attributes.contents`. Successful runs contain only `project_overview.md` with the original file content; failed branches retain `project_plan.md` with that content. Successful execution indices are Teacher 3, Student 3, GPT 4; failed branches end at index 1.
- Current-request checks (records and claim validation, not a separate main-page result row): each selected `score.json`, `goal_turn`, `official_state.valid`, `official_response.valid`. Both flags pass in the three successful runs and fail in freeform/unguided. `semantic_errors: []` in freeform is not treated as success.

## Individual annotation review

Blue marks indicate a supported directory diagnosis, prerequisite action, valid guidance, or completed rename. Red marks indicate stopping with the rename unresolved, not a failed transport. Correct freeform guidance is blue even though its execution branch is red. Repeated filenames and function names are not automatically marked. Every retained span was chosen for its role below; offsets merely validate those choices.

| Passage | Retained mark and reason | Deliberately unmarked material |
| --- | --- | --- |
| Teacher structured action at message 6 | Argument `"workspace"`, blue: the missing directory prerequisite is the decisive change. | Function name and directory-return value repeat the same action; no second mark is needed. |
| Teacher structured action at message 8 | Returned `'project_plan.md' moved to 'project_overview.md'`, blue: actual completion after entering the directory. | Both filename arguments are shared task parameters. |
| Student structured action at message 6 | Argument `"workspace"`, blue: this independently chosen run applies the same prerequisite. | Function name and return remain readable without duplicate emphasis. |
| Student structured action at message 8 | Returned rename statement, blue: confirms this run also completes. | Source/destination arguments add no different decision. |
| GPT action at message 6 | Returned `"/alex"`, blue: the extra diagnosis identifies the parent directory; it is not an execution error. | `pwd` name is not colored as failure merely because the local-reference observation differs. |
| GPT action at message 8 | Argument `"workspace"`, blue: the observed diagnostic result leads to the necessary navigation. | Return repeats the action. |
| GPT action at message 10 | Returned rename statement, blue: confirms successful completion despite the first-step local mismatch. | Filename arguments and empty reasoning are unmarked. |
| Teacher freeform reply at message 6 | `provide the full path`, red: the agent stops and requests information despite the known workspace location and correct suggested call. | The factual report that the old call did not find a local file is not itself marked as false. Other reply wording is retained without emphasis. |
| Unguided reply at message 6 | `provide the full path`, red: this independently reviewed reply likewise stops at the directory error. | Other text is retained; no reasoning is supplied because its field is whitespace. |
| Teacher structured guidance | Entire decision rule, blue: a short explicit ordering dependency. | Preconditions, expected transition, and recovery instruction are kept in full guidance without additional marks. |
| Student structured guidance | `Call mcp_tool_cd with folder='workspace'`, blue: the concrete prerequisite action. | Remaining rule explains the same ordering; full fields are unmarked. |
| Teacher freeform guidance | `mcp_tool_cd`, blue: the suggested tool is correct even though it is not executed. | XML syntax and escaped JSON remain unchanged; no red mark falsely labels guidance as incorrect. |
| GPT structured guidance | `defer the rename until that directory change succeeds.`, blue: the dependency that the eventual execution respects. | The one-call instruction and request-not-to-stop remain visible without implying they were exactly followed at the first step. |
| Teacher agent reasoning at message 6 | `mcp_tool_cd with folder="workspace"`, blue: the agent explicitly chooses the prerequisite before acting. | Surrounding prediction is unmarked. Complete reasoning acknowledges the earlier direct-move error; later message 8 reasons from the actual successful `cd` return and is retained in records rather than duplicated. Message 10 has whitespace reasoning. |
| Student agent reasoning at message 6 | `first step: cd to workspace. Then mv the file.`, blue: explicit corrected action order. | Earlier reasoning repeats that diagnosis; messages 8 and 10 have whitespace reasoning and are not invented. |
| GPT agent reasoning at message 6 | `use mcp_tool_pwd to check the current directory`, blue: accurately explains the actual extra diagnostic action. | Full reasoning was reviewed, including repeated `pwd→cd→mv` plans. Message 8 uses the returned `/alex` to choose workspace; message 10 is empty; message 12 summarizes successful execution. Those are not spliced into the first-step excerpt. |
| Teacher structured advisor analysis | No displayed excerpt or marks: the correct diagnosis repeats the guidance. | Complete reasoning inspected and consistent; retained in records. |
| Teacher freeform advisor analysis | No displayed excerpt or marks: this correct diagnosis does not explain why the executing agent ignored it. | Complete reasoning inspected and retained in records; no executing-agent rationale is inferred from it. |
| Teacher final-state result | `project_overview.md`, blue: task-relevant final filename. | Preserved file-content claim needs no further mark. |
| Student final-state result | `project_overview.md`, blue: independently checked successful state. | Other state-summary wording unmarked. |
| GPT final-state result | `project_overview.md`, blue: later completion is distinct from the local first-step mismatch. | Other state-summary wording unmarked. |
| Freeform final-state result | `project_plan.md`, red: the unchanged old filename establishes the unresolved request. | Other state-summary wording unmarked. |
| Unguided final-state result | `project_plan.md`, red: independently verified unchanged file. | Other state-summary wording unmarked. |

No available relevant reasoning or guidance contradicts the displayed directory diagnosis. The freeform agent and unguided agent have no substantive continuation reasoning to display. The JSON therefore omits their reasoning entries rather than adding a paraphrased rationale.

## Records and validation

The manifest contains all 402 files in the raw package, including unselected trials, provenance, transport requests/responses, and comparison receipts. No raw files were rewritten or copied. Selected trajectories, first guided requests, and current-request scores form the primary source list; other sources remain in the secondary picker. Stable method record links open the selected continuation at trajectory message 6. No source is assigned a global success/failure tone.

Performed:

- Read the author contract, shared-component README, accepted ablation composition, editorial skill, and review rubric.
- Reviewed complete selected guidance and all relevant executing-agent reasoning, including empty fields and post-action reasoning. Independently inspected generated Teacher advisor analyses where available.
- Verified all selected context/prefix equalities, unguided prefix equality, restore states, current-request scope, and one-response guidance injection/removal from actual request files.
- Compared final file names and unchanged contents directly in execution states against the current-request verifier results.
- Direct source-alignment assertions passed for verbatim original tasks, actual tool names and displayed arguments/returns, reply-wrapper cleanup, contiguous reasoning excerpts, complete injected guidance, final-state predicates, and the exact 402-file inventory. This supplements the manual relevance/color review above.
- `node design-lab/case-shared/validate-case.cjs design-lab/case-content/ablation/enter-before-rename.json`: PASS, 21 exact spans and 402 source URLs.

Pending coordinator acceptance: desktop/narrow browser layout, paired selection, original-task/reasoning folding, source readable/raw/download behavior, and catalog registration. The shared reader originally recognized a different system-guidance delimiter; the coordinator was notified to support the actual `Local steering for this response only:` marker. No shared code or catalog was changed by this author.

Preview: `design-lab/paper-cases.html?group=ablation&case=enter-before-rename`.

Records: `design-lab/case-records.html?group=ablation&case=enter-before-rename&source=trial-history/teacher_structured/000/trajectory.json&message=6`.
