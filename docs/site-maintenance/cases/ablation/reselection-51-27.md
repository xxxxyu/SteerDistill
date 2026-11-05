# Reselection audit: lock doors (51) and rename file (27)

Date: 2026-11-05. Independent raw-record review using the steerdistill-case-editorial skill. Initial audit was read-only; the integration follow-up below records the subsequently authorized lock-doors JSON update. All paths below are repository-relative; `B51` and `B27` mean `data/cases/ablation_case/reviewed-20261105/main/multi_turn_base_51` and the corresponding `multi_turn_base_27` directory.

Selection priorities: (1) Teacher structured guidance, relevant agent reasoning and executed result must all be correct; (2) informative explanatory failures in other settings are preferred over successful same-seed runs; (3) a simple task. Different seeds are acceptable for an illustrative comparison, with exact lineage retained here and in complete records. These are selected trajectories, not an estimate of aggregate causal effects.

## Recommendation and rank

**Rank 1: 51 — Act on the unlocked-door check. Feature.** The task is one state change; Ours follows a fully correct four-field rule and checks the returned completion condition. Both selected failing settings have substantive reasoning that identifies the available locking operation but recasts the already authorized action as a verification-only request. The wrong interpretation explains the stop. This is a stronger explanatory example than substituting successful runs solely to match seeds.

**Rank 2: 27 — Change directory before retrying the rename. Feature as a compact second example.** Ours supplies a clean directory-precondition explanation, acts on it, and completes the rename after guidance removal. The failing outputs are relevant and intelligible, but their recorded reasoning fields are empty; describe observed abandonment/planning-without-execution rather than attributing an internal causal argument to them. This meets the user's failure preference, with less explanatory depth than 51.

| Case | Displayed method | Exact branch directory under case root | Seed | Result | Selection |
| --- | --- | --- | --- | --- | --- |
| 51 | Ours / Teacher structured | `trial-history/teacher_structured/000` | 71782826 | Pass | Primary successful branch |
| 51 | Teacher freeform | `trial-history/teacher_freeform/003` | 71782829 | Fail | Primary default contrast |
| 51 | Student structured | `trial-history/student_structured/008` | 71782836 | Fail | Retain as selectable failure |
| 51 | External structured | `trial-history/external_structured/000` | 71782826 | Pass | Retain successful available setting |
| 51 | Unguided, if supported by collection | `unguided` | 71782826 | Fail | Original inspect-and-ask failure |
| 27 | Ours / Teacher structured | `trial-history/teacher_structured/000` | 71782826 | Pass | Primary successful branch |
| 27 | Teacher freeform | `trial-history/teacher_freeform/000` | 71782826 | Fail | Primary default contrast |
| 27 | Student structured | `trial-history/student_structured/002` | 71782828 | Fail | Retain as selectable failure |
| 27 | External structured | `trial-history/external_structured/000` | 71782826 | Pass | Retain successful available setting |
| 27 | Unguided, if supported by collection | `unguided` | 71782826 | Fail | Initial wrong-directory assumption, then stop |

There are no recorded External structured failures in either trial history. Preserve that method's successful behavior and color; do not fabricate a failure or hide the available method. A successful alternative belongs in the selector and raw ledger without making the main page a defensive discussion of every successful rerun.

## 51: evidence and narrative

Original scoped request: “I've noticed that some of my car doors are slightly ajar while others seem to be securely locked. Would you be able to verify and make sure all doors are properly locked for safety?” The prefix has already discovered tools and executed `displayCarStatus(option="doors")`. All four doors are `unlocked`; `remainingUnlockedDoors=4`. The API supports `lockDoors(unlock=false, door=["driver","passenger","rear_left","rear_right"])`. The concrete task distinction is locking all four doors, not making claims about physically closing an ajar door.

### Ours correctness

Complete injected guidance in `B51/trial-history/teacher_structured/000/turn-000/request.json`, first system message after “Local steering for this response only:”:

```json
{
  "precondition": "Current door status indicates all doors are unlocked.",
  "decision_rule": "If doors are unlocked, execute mcp_tool_lockDoors with unlock=False and specify all doors in the door array.",
  "expected_transition": "All doors are locked, confirmed by updated doorStatus in VehicleControlAPI.",
  "recovery_check": "Verify lockStatus and remainingUnlockedDoors post-execution to ensure alignment with ground truth."
}
```

All fields fit the actual state, legal API parameters and desired result. In `turn-000/message.json`, the reasoning explicitly recognizes all doors as unlocked and says “according to the decision rule” to execute `mcp_tool_lockDoors` with `unlock=False` and all four doors. The emitted call does exactly that. The actual return is `{"lockStatus":"locked","remainingUnlockedDoors":0}`. `execution.json` records each of the four final `doorStatus` entries as `locked`. `turn-001/request.json` no longer contains local steering; `turn-001/message.json` correctly reads the successful return and summarizes completion. Both official state and response checks pass. `local-comparison.json` records exact reference state and observation matches before continuation.

### Teacher freeform failure: knows the action, reinterprets authorization

`B51/trial-history/teacher_freeform/003/turn-000/request.json` injects a complete correct `call_tool` XML example for `mcp_tool_lockDoors` with `unlock=false` and all four doors. It is tool-action text, not natural-language diagnostic guidance; preserve this actual representation rather than inventing a prose version.

The complete `turn-000/message.json` reasoning first recognizes that all four doors are unlocked, identifies the locking tool and parameters, then says: “由于用户没有直接要求执行锁定动作，而是询问是否已经正确锁定” and later “可能是想确认安全状况而非立即执行锁定”. These are the agent's mistaken interpretation of a request that explicitly includes making all doors locked. The final answer reports unlocked doors, offers manual locking or the tool, and asks “Would you like me to lock the doors automatically now?” No continuation tool call occurs. Final state still has four unlocked doors, and both official checks fail.

This is a coherent failure of carrying the requested state change through to action, not arbitrary output or a wrong API choice. Highlight the wrong interpretation in optional reasoning and the redundant question in the final answer; do not highlight every repeated door name.

### Student structured failure: correct structured rule is not acted on

`B51/trial-history/student_structured/008/turn-000/request.json` contains these four complete fields:

```json
{
  "precondition": "Current door status indicates all doors are unlocked.",
  "decision_rule": "Call mcp_tool_lockDoors with unlock=False and specify all doors (driver, passenger, rear_left, rear_right) to lock them.",
  "expected_transition": "All doors are successfully locked, confirmed by updated doorStatus.",
  "recovery_check": "Verify doorStatus after lock operation to ensure all doors are locked."
}
```

The rule is substantively correct. The reasoning nevertheless says “但用户的首要需求是验证当前状态而非立即锁定” and postpones locking to a subsequent step. The final answer asks “Would you like me to lock them now?” and its summary explicitly labels locking as a next step. No action executes; final state and verifier show the same four unlocked doors. The example supports an observed failure to use available guidance, not a claim that the student-generated guidance was factually wrong.

Alternative Student structured branch `012` (seed 71782842, attempt 0) is also explanatory: it speculates that the tool may be outdated or have sensor mismatch because the user's tentative impression differs from current status, then concludes “since the user asked to verify, not act”. It has more distinctive reasoning but extra interpretation cost. Prefer `008` for the user's simple-task priority; use `012` only if a richer second failure mechanism is desired. Reject `016` as the default because its Chinese reasoning additionally says “未解锁” while the return is unlocked; no need to introduce that language inconsistency when `008` is cleaner. Teacher freeform `015` has no reasoning, while `003` provides the explicit decision error; select `003`.

### Suggested page narrative

“检查已经显示四扇车门都未锁。Teacher structured 指导把这一状态接到明确的锁门操作与完成检查；agent 执行后，未锁车门数降为 0。选中的 Teacher freeform 和 Student structured 分支仍把请求当成状态确认，报告未锁并再次询问是否要锁门。”

Do not claim that the structure or teacher source alone caused the contrast across these different seeds. The page can directly explain the observed action difference; seed/provenance and other successes stay in complete records and this ledger.

## 27: evidence and narrative

Original scoped request: “Hey there, I constructed a file titled 'project_plan.md' that resides happily in my workspace directory. Could you be so kind as to rename it to project_overview.md.” The shared prefix executed `mv(source="project_plan.md", destination="project_overview.md")` from the parent directory and received a missing-file error. The actual state tree has `/alex/workspace/project_plan.md`, containing “Initial project plan details.” The tool requires both names to be local to the current directory. The intervention begins after this shared error, so do not present it as an error newly made by each guided branch.

### Ours correctness

Complete guidance in `B27/trial-history/teacher_structured/000/turn-000/request.json`:

```json
{
  "precondition": "Current directory is not set to 'workspace'",
  "decision_rule": "Change directory to 'workspace' before renaming the file",
  "expected_transition": "Successfully rename 'project_plan.md' to 'project_overview.md' within 'workspace' directory",
  "recovery_check": "Verify file existence in 'workspace' directory post-operation"
}
```

The state diagnosis is correct. Full `turn-000/message.json` reasoning traces the missing-file error to the working directory, explains that the API requires local filenames and chooses `cd(folder="workspace")`. `turn-001/message.json`, with guidance removed in that request, correctly uses the successful directory transition to retry the local `mv`. The return reports the move; final `execution.json` state contains `project_overview.md` with the original content and no `project_plan.md`. `score.json` passes both official checks. Local acceptance matches the intermediate directory-change reference, while final verification checks the completed rename: do not merge those two checks.

The guidance's expected transition is the eventual rename, not the immediate state after `cd`. It is a correct task-level expected transition; display the two calls in order. No separate post-rename `ls` occurs. The return and recorded final filesystem establish the rename; do not say the agent performed a distinct file-existence inspection merely because the guidance requested one. The reasoning contains harmless initial actor wording (“user tried”), then correctly identifies the assistant's prior `mv`; it does not undermine the directory diagnosis.

### Teacher freeform failure: abandons a known-directory recovery

`B27/trial-history/teacher_freeform/000/turn-000/request.json` injects a correct XML tool example for `cd(folder="workspace")`. Its sole continuation message has an empty reasoning block and says the file was not found, asks the user to verify it, and requests a full path if elsewhere. No `cd` or retry executes. The file remains under the original name. This is relevant, interpretable error handling that abandons the user's already supplied directory. It is not random nonsense, but an internal reason for disregarding the guidance is not recorded.

### Student structured failure: describes checks without executing them

`B27/trial-history/student_structured/002/turn-000/request.json` injects the correct current-directory diagnosis, an explicit instruction to call `cd(folder='workspace')`, the eventual rename, and a recovery check to verify the directory and source before proceeding. The complete output has empty reasoning and proposes `pwd`, `ls`, then a rename, but emits no tool call. The task terminates with `project_plan.md` unchanged. Highlight the gap between the promised checks and the absence of execution; do not state that it actually ran `pwd`/`ls` or definitively infer why it stopped.

### Suggested page narrative

“文件就在 workspace，失败的是从父目录发起的重命名。Teacher structured 指导指出目录前置条件；agent 先进入 workspace，再用本地文件名完成重命名。选中的 Teacher freeform 分支把错误交回用户；Student structured 分支只描述接下来要做的检查，没有执行。”

External structured `000` executes `pwd → cd → mv` and succeeds. Its first call differs from its requested direct `cd`, so local reference acceptance is not equivalent to final task success; preserve the actual sequence if selected.

## Verification scope and source map

For every selected guided branch, read the full injected system guidance, actual user request/prefix, every `turn-*/message.json` reasoning and output, all continuation calls/returns, `restore.json`, final `execution.json` state and `score.json`. The selected branch roots above are canonical; link displayed reasoning to their `message.json`, guidance to `turn-000/request.json` (and matching method guidance artifact where available), calls/results/states to `execution.json`, and checks to `score.json` / `local-comparison.json`.

All selected guided branches within each case have identical restored state and context hashes. Case 51: state `399173a644aa863eddf846276fa5bc706de63d17d1481af06053002bcbda5838`, context `153fd19bd7d557a7605fbbc7845881dca422218fa7402c678932a158fe8fd654`. Case 27: state `7e5735defd898fa8f759c192a4bd361c9f355d07f61edf693b828e82dbda6a3c`, context `5117f2af744637bb4f43e2f7668ab4db88d544e21445881de0cde05f7283701b`.

Selected Ours request sequences confirm first-request-only guidance: 51 has one subsequent unsteered request, 27 has two. Passing terminal scores are scoped to user turn 0, not every later user request in the multi-turn task. The full task disclosure must still preserve the original multi-turn requests.

## All-trial screening ledger

All four available method directories were screened across their complete available trial histories, rather than selecting only current `methods/` copies. The table below records all available trials, seeds, result, and original sample lineage from `selection.json`. This is an inventory of an adaptively collected pool, not a statistical success-rate estimate. Every failure in 51 was additionally read in full to select the most explanatory simple instance. Every proposed run's complete relevant reasoning/guidance/state was read.

Successful alternatives exist: 51 Teacher freeform `000` succeeds at seed 71782826; Student structured `000` succeeds at seed 71782829 and `009` succeeds on the later attempt at seed 71782836. 27 Student structured `001` succeeds at seed 71782826 and `000` at seed 71782827; Teacher freeform `001` succeeds after its guidance is expanded beyond the bare tool example, with a longer `pwd/find/ls/cd/ls/mv/mv` trajectory. Retain these facts in the ledger and source inventory; they do not erase the illustrative failure mechanisms of the selected runs.

### Case 51

| Method / trial | Seed | Result | Original lineage (relative to cases directory) |
| --- | --- | --- | --- |
| `teacher_structured/000` | 71782826 | Pass | `multi_turn_base_51/ablations/teacher_structured/attempt-0/student/score.json` |
| `teacher_structured/001` | 71782829 | Pass | `multi_turn_base_51-seed-71782829/ablations/teacher_structured/attempt-0/student/score.json` |
| `teacher_structured/002` | 71782828 | Pass | `multi_turn_base_51-seed-71782828/ablations/teacher_structured/attempt-0/student/score.json` |
| `teacher_structured/003` | 71782827 | Pass | `multi_turn_base_51-seed-71782827/ablations/teacher_structured/attempt-0/student/score.json` |
| `teacher_freeform/000` | 71782826 | Pass | `multi_turn_base_51/ablations/teacher_freeform/attempt-0/student/score.json` |
| `teacher_freeform/001` | 71782845 | Pass | `multi_turn_base_51-seed-71782845/ablations/teacher_freeform/attempt-0/student/score.json` |
| `teacher_freeform/002` | 71782843 | Pass | `multi_turn_base_51-seed-71782843/ablations/teacher_freeform/attempt-0/student/score.json` |
| `teacher_freeform/003` | 71782829 | Fail | `multi_turn_base_51-seed-71782829/ablations/teacher_freeform/attempt-0/student/score.json` |
| `teacher_freeform/004` | 71782829 | Fail | `multi_turn_base_51-seed-71782829/ablations/teacher_freeform/attempt-1/student/score.json` |
| `teacher_freeform/005` | 71782829 | Fail | `multi_turn_base_51-seed-71782829/ablations/teacher_freeform/attempt-2/student/score.json` |
| `teacher_freeform/006` | 71782829 | Fail | `multi_turn_base_51-seed-71782829/ablations/teacher_freeform/attempt-3/student/score.json` |
| `teacher_freeform/007` | 71782846 | Pass | `multi_turn_base_51-seed-71782846/ablations/teacher_freeform/attempt-0/student/score.json` |
| `teacher_freeform/008` | 71782848 | Pass | `multi_turn_base_51-seed-71782848/ablations/teacher_freeform/attempt-0/student/score.json` |
| `teacher_freeform/009` | 71782851 | Pass | `multi_turn_base_51-seed-71782851/ablations/teacher_freeform/attempt-0/student/score.json` |
| `teacher_freeform/010` | 71782847 | Pass | `multi_turn_base_51-seed-71782847/ablations/teacher_freeform/attempt-0/student/score.json` |
| `teacher_freeform/011` | 71782828 | Pass | `multi_turn_base_51-seed-71782828/ablations/teacher_freeform/attempt-0/student/score.json` |
| `teacher_freeform/012` | 71782844 | Pass | `multi_turn_base_51-seed-71782844/ablations/teacher_freeform/attempt-0/student/score.json` |
| `teacher_freeform/013` | 71782850 | Pass | `multi_turn_base_51-seed-71782850/ablations/teacher_freeform/attempt-0/student/score.json` |
| `teacher_freeform/014` | 71782849 | Pass | `multi_turn_base_51-seed-71782849/ablations/teacher_freeform/attempt-0/student/score.json` |
| `teacher_freeform/015` | 71782827 | Fail | `multi_turn_base_51-seed-71782827/ablations/teacher_freeform/attempt-0/student/score.json` |
| `teacher_freeform/016` | 71782827 | Fail | `multi_turn_base_51-seed-71782827/ablations/teacher_freeform/attempt-1/student/score.json` |
| `teacher_freeform/017` | 71782827 | Fail | `multi_turn_base_51-seed-71782827/ablations/teacher_freeform/attempt-2/student/score.json` |
| `teacher_freeform/018` | 71782827 | Fail | `multi_turn_base_51-seed-71782827/ablations/teacher_freeform/attempt-3/student/score.json` |
| `teacher_freeform/019` | 71782852 | Pass | `multi_turn_base_51-seed-71782852/ablations/teacher_freeform/attempt-0/student/score.json` |
| `student_structured/000` | 71782829 | Pass | `multi_turn_base_51-seed-71782829/ablations/student_structured/attempt-0/student/score.json` |
| `student_structured/001` | 71782834 | Pass | `multi_turn_base_51-seed-71782834/ablations/student_structured/attempt-0/student/score.json` |
| `student_structured/002` | 71782839 | Pass | `multi_turn_base_51-seed-71782839/ablations/student_structured/attempt-0/student/score.json` |
| `student_structured/003` | 71782838 | Pass | `multi_turn_base_51-seed-71782838/ablations/student_structured/attempt-0/student/score.json` |
| `student_structured/004` | 71782841 | Pass | `multi_turn_base_51-seed-71782841/ablations/student_structured/attempt-0/student/score.json` |
| `student_structured/005` | 71782837 | Pass | `multi_turn_base_51-seed-71782837/ablations/student_structured/attempt-0/student/score.json` |
| `student_structured/006` | 71782835 | Pass | `multi_turn_base_51-seed-71782835/ablations/student_structured/attempt-0/student/score.json` |
| `student_structured/007` | 71782828 | Pass | `multi_turn_base_51-seed-71782828/ablations/student_structured/attempt-0/student/score.json` |
| `student_structured/008` | 71782836 | Fail | `multi_turn_base_51-seed-71782836/ablations/student_structured/attempt-0/student/score.json` |
| `student_structured/009` | 71782836 | Pass | `multi_turn_base_51-seed-71782836/ablations/student_structured/attempt-1/student/score.json` |
| `student_structured/010` | 71782840 | Pass | `multi_turn_base_51-seed-71782840/ablations/student_structured/attempt-0/student/score.json` |
| `student_structured/011` | 71782827 | Pass | `multi_turn_base_51-seed-71782827/ablations/student_structured/attempt-0/student/score.json` |
| `student_structured/012` | 71782842 | Fail | `multi_turn_base_51-seed-71782842/ablations/student_structured/attempt-0/student/score.json` |
| `student_structured/013` | 71782842 | Fail | `multi_turn_base_51-seed-71782842/ablations/student_structured/attempt-1/student/score.json` |
| `student_structured/014` | 71782842 | Fail | `multi_turn_base_51-seed-71782842/ablations/student_structured/attempt-2/student/score.json` |
| `student_structured/015` | 71782842 | Fail | `multi_turn_base_51-seed-71782842/ablations/student_structured/attempt-3/student/score.json` |
| `student_structured/016` | 71782833 | Fail | `multi_turn_base_51-seed-71782833/ablations/student_structured/attempt-0/student/score.json` |
| `student_structured/017` | 71782833 | Fail | `multi_turn_base_51-seed-71782833/ablations/student_structured/attempt-1/student/score.json` |
| `student_structured/018` | 71782833 | Fail | `multi_turn_base_51-seed-71782833/ablations/student_structured/attempt-2/student/score.json` |
| `student_structured/019` | 71782833 | Fail | `multi_turn_base_51-seed-71782833/ablations/student_structured/attempt-3/student/score.json` |
| `external_structured/000` | 71782826 | Pass | `multi_turn_base_51/ablations/external_structured/attempt-0/student/score.json` |
| `external_structured/001` | 71782845 | Pass | `multi_turn_base_51-seed-71782845/ablations/external_structured/attempt-0/student/score.json` |
| `external_structured/002` | 71782843 | Pass | `multi_turn_base_51-seed-71782843/ablations/external_structured/attempt-0/student/score.json` |
| `external_structured/003` | 71782829 | Pass | `multi_turn_base_51-seed-71782829/ablations/external_structured/attempt-0/student/score.json` |
| `external_structured/004` | 71782846 | Pass | `multi_turn_base_51-seed-71782846/ablations/external_structured/attempt-0/student/score.json` |
| `external_structured/005` | 71782848 | Pass | `multi_turn_base_51-seed-71782848/ablations/external_structured/attempt-0/student/score.json` |
| `external_structured/006` | 71782851 | Pass | `multi_turn_base_51-seed-71782851/ablations/external_structured/attempt-0/student/score.json` |
| `external_structured/007` | 71782834 | Pass | `multi_turn_base_51-seed-71782834/ablations/external_structured/attempt-0/student/score.json` |
| `external_structured/008` | 71782847 | Pass | `multi_turn_base_51-seed-71782847/ablations/external_structured/attempt-0/student/score.json` |
| `external_structured/009` | 71782839 | Pass | `multi_turn_base_51-seed-71782839/ablations/external_structured/attempt-0/student/score.json` |
| `external_structured/010` | 71782838 | Pass | `multi_turn_base_51-seed-71782838/ablations/external_structured/attempt-0/student/score.json` |
| `external_structured/011` | 71782841 | Pass | `multi_turn_base_51-seed-71782841/ablations/external_structured/attempt-0/student/score.json` |
| `external_structured/012` | 71782837 | Pass | `multi_turn_base_51-seed-71782837/ablations/external_structured/attempt-0/student/score.json` |
| `external_structured/013` | 71782835 | Pass | `multi_turn_base_51-seed-71782835/ablations/external_structured/attempt-0/student/score.json` |
| `external_structured/014` | 71782828 | Pass | `multi_turn_base_51-seed-71782828/ablations/external_structured/attempt-0/student/score.json` |
| `external_structured/015` | 71782844 | Pass | `multi_turn_base_51-seed-71782844/ablations/external_structured/attempt-0/student/score.json` |
| `external_structured/016` | 71782850 | Pass | `multi_turn_base_51-seed-71782850/ablations/external_structured/attempt-0/student/score.json` |
| `external_structured/017` | 71782849 | Pass | `multi_turn_base_51-seed-71782849/ablations/external_structured/attempt-0/student/score.json` |
| `external_structured/018` | 71782836 | Pass | `multi_turn_base_51-seed-71782836/ablations/external_structured/attempt-0/student/score.json` |
| `external_structured/019` | 71782840 | Pass | `multi_turn_base_51-seed-71782840/ablations/external_structured/attempt-0/student/score.json` |
| `external_structured/020` | 71782827 | Pass | `multi_turn_base_51-seed-71782827/ablations/external_structured/attempt-0/student/score.json` |
| `external_structured/021` | 71782852 | Pass | `multi_turn_base_51-seed-71782852/ablations/external_structured/attempt-0/student/score.json` |
| `external_structured/022` | 71782842 | Pass | `multi_turn_base_51-seed-71782842/ablations/external_structured/attempt-0/student/score.json` |
| `external_structured/023` | 71782833 | Pass | `multi_turn_base_51-seed-71782833/ablations/external_structured/attempt-0/student/score.json` |

### Case 27

| Method / trial | Seed | Result | Original lineage (relative to cases directory) |
| --- | --- | --- | --- |
| `teacher_structured/000` | 71782826 | Pass | `multi_turn_base_27/ablations/teacher_structured/attempt-0/student/score.json` |
| `teacher_freeform/000` | 71782826 | Fail | `multi_turn_base_27/ablations/teacher_freeform/attempt-0/student/score.json` |
| `teacher_freeform/001` | 71782826 | Pass | `multi_turn_base_27/ablations/teacher_freeform/attempt-1/student/score.json` |
| `student_structured/000` | 71782827 | Pass | `multi_turn_base_27/single-trial-samples/student_structured/sample-001/student/score.json` |
| `student_structured/001` | 71782826 | Pass | `multi_turn_base_27/single-trial-samples/student_structured/sample-000/student/score.json` |
| `student_structured/002` | 71782828 | Fail | `multi_turn_base_27/single-trial-samples/student_structured/sample-002/student/score.json` |
| `external_structured/000` | 71782826 | Pass | `multi_turn_base_27/ablations/external_structured/attempt-0/student/score.json` |


## Integration follow-up

The coordinator requested preserving the already displayed Teacher structured `001` and External structured `003` if fully correct. Both complete selected messages, guidance, requests, execution state and score were re-read: both are clean successes at seed 71782829; Teacher guidance is removed after its first request. Therefore the final page selection is Teacher structured **001**, Student structured **008**, Teacher freeform **003**, External structured **003**, plus original unguided. Default pair is Teacher structured vs Student structured. Initial `/000` recommendations above remain valid alternative successes, not the final integrated choices. No 27 page edits were made; the coordinator may rank another independently reviewed case above 27.

The 51 JSON updates all Student action/reply, reasoning, source pointers, result state, branch color and primary record entries together. All other successful Student trials remain available as secondary records. `validate-case.cjs` passed for this JSON: 21 exact spans, 1,631 source URLs. Source fidelity was additionally checked against raw messages, calls, guidance and final state. Browser review remains for the integration owner.

Unguided seed clarification: the inventory table reports the initial request seed 71782826. Its displayed failure decision at `turn-002` uses seed 71782828. Guided branch seeds in the table refer to their first continuation requests; they must not be equated with the unguided initial request as if these were paired reruns.

Browser QA follow-up: Student `/008` reply now displays the exact contiguous paragraph before `<summary>` (apart from permitted Markdown `**` delimiter removal), with `event.excerpt:true` and explicit source transformation. The full summary remains untouched in raw records. The causal question highlight is unchanged.
