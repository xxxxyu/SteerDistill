# 解锁车门：工具列表序号混入工具名

## Selection and scope

Selected as a focused training-correction example. The initial agent identifies the right operations and first supplies valid arguments, but incorporates the tool-list numbers into both tool names. The resulting calls never reach the actual vehicle tools. A locally guided retry uses the advertised name, unlocks all four doors and matches the fixed successful reference transition; a continuation without the guidance switches on the headlights. This is revision of a frozen student's rollout, not a demonstration of a subsequently trained model.

The causal unit is compact: advertised tool identity → actual name sent → tool error / changed vehicle state. The whole original request has one user turn and is retained in the original-task disclosure. The first two failed calls suffice for the default contrast; the failed retries and final response remain in records and are reflected in the branch summary.

## Files and provenance

- Authored config: `design-lab/case-content/training/tool-list-numbering.json`.
- Accepted composition: `design-lab/case-content/training/directory-navigation.json`; only its shared training composition was reused.
- Raw root (all paths below relative to this root): `data/cases/training_case/reviewed-20261106/multi_turn_long_context_50/`.
- Remote source: host alias `neogpu-a100-nx-1`, `/mnt/genming/training-bfcl-long-context-search-20261106/training/cases/multi_turn_long_context_50/`.
- `import-manifest.json` records source location, per-file sizes and SHA-256 values. All 159 imported files were compared with hashes independently computed on the source server; every hash matched. The manifest is an additional local provenance file. No source bytes were changed; no model was rerun.
- Selected paths independently confirmed through `outcome.json`: `before/`, `reference/attempt-1/`, `steering/attempt-0/`, `after/attempt-0/`. Other saved reference attempts remain in the inventory.
- All 160 files are available through the shared record reader. Primary sources are before/after/reference trajectories, exact four-field guidance, local gate, terminal score. No custom reader or shared interface change was needed.

## Method and lifecycle audit

Read manuscript `tex/method.tex` and `tex/method_implementation.tex` in the sibling manuscript checkout (`ICLR-2027---Quant-OPD`). They distinguish reference alignment, guided local correction, acceptance and continuation without guidance.

1. The shared prefix is `list_tools`, preserved in trajectory messages 0–3. The returned list names `16. mcp_tool_lockDoors` and `20. mcp_tool_setHeadlights`; the index is outside the tool identifier. `before/execution.json[1].before`, `after/attempt-0/execution.json[1].before` and `reference/attempt-1/execution.json[1].before` are equal.
2. `after/attempt-0/turn-000/request.json.messages[0].content` adds `Local steering for this response only:` and the exact `raw_steering_prompt.txt` to the system message. The remaining initial request prefix equals the next request's original four messages.
3. `after/attempt-0/local_gate.json` has `passed`, `execution_valid` and `checked_before_continuation` all true. Its `actual_state` equals `target_state`, the successful reference's first unlock state and the guided first unlock state. All four `doorStatus` values are `unlocked`, `remainingUnlockedDoors=4`; `headLightStatus` is still `off`.
4. `after/attempt-0/turn-001/request.json` and `turn-002/request.json` contain no steering appendix. The former generates the headlights call. `execution.json[2].after` preserves unlocked doors and sets `headLightStatus=on`.
5. `after/attempt-0/score.json` reports passed and both official state/response valid. Before fails and retains locked doors plus lights off.

The local gate's literal criterion is “Successful tool execution and reference state equality; no action-string or response-string gate”. This page therefore describes state matching and execution validity, never a returned-information gate. The Teacher's `recovery_check` is an instruction; the agent does not call a separate `displayCarStatus`. Tool responses and the saved execution state support the displayed status checks. The two execution-result rows follow the actual local-check/continuation boundary rather than pretending that all four guidance fields were individually executed.

## Complete reasoning and guidance review

Reviewed all before trajectory assistant reasoning (messages 2, 4, 6, 8, 10, 12), all selected after reasoning (2, 4, 6, 8), all selected reference reasoning (2, 4, 6, 8), and the complete Teacher `steering/attempt-0/analysis.json` reasoning and final content. The common discovery step is neutral and retained in records.

- Before message 4 explicitly reads `mcp_tool_16 called LockDoors` and `mcp_tool_20 SetHeadlights`. It correctly reasons about unlocking all doors and setting mode on; the error is tool identity, not intent or the first argument set.
- Before message 6 repeatedly attributes the unknown-tool error to registration/access/naming possibilities and still calls the numbered headlights name. Message 8 considers alternate names and argument formats, then retries `16_lockDoors` with unsupported `["all"]`. Message 10 repeats numbered headlights with blank reasoning. Message 12 considers a correct-looking unnumbered headlights name but never executes it; the final answer says the functionality is unavailable. This is not demonstrated self-correction. We do not suppress a successful repair: none exists in the selected before run.
- After message 4 identifies the actual two tool names and correctly handles all doors. Message 6 correctly reads the unlock result and selects `mode="on"`. Message 8 accurately summarizes both completed actions. No contradictory relevant reasoning was found.
- The successful reference first unlocks the same four doors, then lights on; its later recap matches execution.
- Teacher analysis uses past-tense first-person narration of the supplied successful reference; the final precondition correctly says the doors are locked. Its final four fields name the right functions and parameters. The page does not turn this past-tense analysis into a claim that the student had already succeeded, nor invent a more explicit “remove numeric prefixes” instruction than the teacher actually supplied.

## Claim and display mapping

All trajectory indices are zero-based.

| Display | Exact source | Editorial treatment |
| --- | --- | --- |
| Task and original task | `task.json.question[0][0].content` | Full request in collapsed disclosure; Chinese summary retains the two user goals. |
| List items 16 and 20 | `before/trajectory.json.messages[3].content`, decoded `data[0].text` | Summary identifies the numbering/name distinction; no giant tool list in the main flow. |
| Before unlock | `before/trajectory.json` messages 4/5; `before/execution.json[1]` | Unwrap call_tool and strip only the common `mcp_tool_` prefix. Preserve actual wrong `16_`. All actual first-call arguments retained. Decode the tool-error text. |
| Before headlights | Same trajectory messages 6/7; execution entry 2 | Same transformation, retaining wrong `20_`; mode and exact error retained. |
| Before retries still fail | Same trajectory messages 8–12; final execution state | Summary mentions retry failure. The two repeated calls and final apology add little to the compact contrast; available untouched in records. Frame explicitly says 节选. |
| After unlock | `after/attempt-0/trajectory.json` messages 4/5; execution entry 1 | Unwrap call_tool; strip common namespace. Return presents both payload fields without transport wrappers. |
| After headlights | Same trajectory messages 6/7; execution entry 2 | Actual next call and sole returned status field. |
| Both optional reasoning blocks | Respective trajectory message 4 `.reasoning` | Two exact sentences per branch in original order, separated by `…`. Raw `mcp_tool_` remains inside verbatim reasoning. No paraphrase is placed inside quotation text. |
| Four Teacher fields | `steering/attempt-0/raw_steering_prompt.txt` | Parse JSON object only; each field value unchanged, including original ordinary quotation marks and namespace prefixes. No manufactured backticks or highlights. |
| 局部核验 row | `after/attempt-0/local_gate.json`; selected reference execution entry 1 | State match applies at unlock, before lights on; flags inspected rather than inferred from terminal score. |
| 后续执行 row | requests turn-001/002; after execution entries 1/2; after score | Guidance removal and final state separately verified. No extra status-query call claimed. |

All source pointers in actions/reasoning use site-relative files plus actual message/returnMessage indices. Code formatting uses JSON boolean literals and double-quoted string values; it does not change arguments. Returns remove only JSON punctuation/transport packaging, retaining exact payload keys and values.

## Individually reviewed annotation decisions

| Passage | Kept emphasis and reason | Intentionally unmarked |
| --- | --- | --- |
| Before unlock call (m4) | Red `16_`: the list index incorrectly incorporated into the identifier is the decisive error. | Valid `unlock=true` and four door names: they are not the error. Error return already inherits failure colour; no redundant full-return background. |
| Before headlights call (m6) | Red `20_`: same explicit misread causes the second unknown-tool failure. | Correct `mode="on"`; return is red but not background-marked. |
| After unlock call/return (m4/5) | Blue `lockDoors` contrasts the actual advertised name; blue `remainingUnlockedDoors: 4` establishes all doors changed state. | Argument list is unchanged from the first failed attempt, so no argument emphasis. `lockStatus` stays blue return text without another mark. |
| After headlights call/return (m6/7) | Blue `setHeadlights` contrasts the invalid numbered identifier; returned `"on"` supplies the final observed outcome. | Mode argument is ordinary; no need to repeat the result emphasis on it. |
| Before reasoning (m4) | Red `mcp_tool_16 called LockDoors` and `mcp_tool_20 SetHeadlights`: the exact textual misidentification behind the calls. | Lead-in wording stays plain. Full later hypotheses remain accessible; no unsupported claim of a completed reflection or correction. |
| After reasoning (m4) | Blue actual names `mcp_tool_lockDoors` / `mcp_tool_setHeadlights`: the contrast is correctly reading tool identities. | Descriptive “can unlock doors” and setting mode on are relevant context but do not need emphasis. |
| Teacher four fields | No background annotation; preserving the complete supplied rule provides enough emphasis through the shared field layout. | No ordinary single-quoted phrase is rendered as code. |
| Execution checks | Shared inline code for exact state values and the actual continuation call; no custom blanket colour/highlight rule. | Explanatory Chinese stays normal weight, avoiding bold “agent”, badges or tiny provenance notes. |

Ten explicit highlights total. The script used to calculate exact offsets only located the individually selected phrases above; it did not choose tokens or infer importance by rules.

## Validation and handoff

- Source import: 159/159 remote SHA-256 hashes matched.
- Direct assertions passed for restored-state equality across before/reference/after, selected reference/gate/actual state equality, guidance injection and removal, and the unchanged shared prefix.
- The four displayed reasoning sentences were exact substring-checked against their actual reasoning source before authoring; semantic review is recorded separately above.
- `node design-lab/case-shared/validate-case.cjs design-lab/case-content/training/tool-list-numbering.json` passed: 1 config, 10 exact spans, 160 source URLs.
- Browser/layout/record interaction review is pending coordinator QA; this independent author has not claimed visual acceptance or registered the case.
- Unregistered preview: `/design-lab/paper-cases.html?group=training&case=tool-list-numbering`.
- Records: `/design-lab/case-records.html?group=training&case=tool-list-numbering&source=before%2Ftrajectory.json&message=4`.
- Suggested short index title: `工具列表序号`; integration owner assigns code and registry entry.

## Coordinator integration

Registered after source review for local preview. Desktop/narrow interaction and record-reader checks, integration edits and user-review status are recorded in [the batch review](../../case-batch-20261106.md). This supersedes the pending coordinator QA status at author handoff; user acceptance is still pending.
