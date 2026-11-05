# Reserve re-selection — 2026-11-05

Selection rule: Teacher structured (Ours) must have correct complete guidance, advisor analysis, execution reasoning and result. Prefer a short task with an interpretable baseline failure. Different-seed illustrative failures are allowed if their sources and successful alternatives remain available; do not infer controlled causal effects from those examples.

## Decision

1. **Promote `multi_turn_base_12` (create in Documents)**. It has a simple, visible failure: searching a directory does not change the working directory. Ours identifies that dependency, executes `cd`, then creates the file. Teacher freeform fails at the same initial actor seed. This belongs beside the simple lock/refuel candidates and ahead of the other reserves; it is especially strong if either lock/refuel has unresolved Ours reasoning contradictions. Its default comparison does not depend on selecting a different failed seed. The separate agents auditing lock/refuel own their final relative rank.
2. **Retain appointment booking as a lower-priority reserve**. There is a real missing `is_same_day_booking=1` baseline error. Ours passes the actual database predicate, but actor reasoning is absent, so the requested full-reasoning criterion cannot be established. A time-filter/storage issue complicates the external branch and adds reading cost.
3. **Do not feature R02A for a clean-Ours advantage**. Both baseline branches eventually finish correctly after real local errors. More decisively, Ours advisor analysis misattributes the observed source lookup error to the destination location without resolving that diagnosis. Correct final guidance/calls alone do not meet this selection rule.

## Create in Documents: evidence audit

Site package: `data/cases/ablation_case/reviewed-20261105/reserve/multi_turn_base_12/`.
Original unpacked package hint: `steerdistill-ablation-reviewed-20261105/reviewed-20261105/reserve/multi_turn_base_12/` under the temporary evidence directory. The site's `unguided/` was separately imported from the original discovery run `ablation-bfcl-discovery-20261104/cases/multi_turn_base_12/student/`.

Read the full common prefix, all three selected trajectories, all available advisor final guidance and advisor analysis, the other Student trial, local alignment/check reports, per-turn requests and state/result records. The common prefix is messages 0–5: tool discovery, then `find(path="Documents", name="summary.txt")` returning no matches. The directory is `/alex`; Documents is empty. `touch` explicitly creates in the current directory. No initial file has been created yet.

| Branch | Exact run path relative to package | Observed behavior |
| --- | --- | --- |
| Ours | `methods/teacher_structured/sample/`; original `trial-history/trials/teacher_structured/guide-0/seed-71782927/` | Messages 6–10: recognizes `touch` is local, `cd Documents` → `touch summary.txt` → truthful final. Guidance and advisor analysis both correctly identify the missing directory change. |
| Teacher freeform | `methods/teacher_freeform/sample/`; original `trial-history/trials/teacher_freeform/guide-0/seed-71782927/` | Messages 6–8: reasons “Since the directory is already specified in the path”; calls `touch` in `/alex` and falsely reports the file in Documents. The guidance itself is a correct `cd` tool-call-shaped text, not an executed call. |
| Student structured failure | `methods/student_structured/sample/`; original `trial-history/trials/student_structured/guide-0/seed-71782928/` | Messages 6–12: wrong-location `touch`, explicit recognition, `cd`, second `touch`, final. Target file now exists, but the extra root file remains. Do not call this “never noticed the error” or “target still absent”. |
| Student structured success | `trial-history/trials/student_structured/guide-0/seed-71782927/` | Messages 6–12: `cd`, redundant `find`, `touch`, final; state and response pass. Preserved as secondary full records. |
| Unguided original | `unguided/` | Messages 0–5 exactly equal Ours' prefix; message 6 `touch`, message 8 false Documents completion. Different sampling seed; no steering in any request. This is the original failed run, not a newly matched-seed retry. |

The three selected guided identity files share context hash `6d8f432f36e681c1cd240ae6275137146650cbb88f419acd4b77ce12b399fd97` and restored state hash `698284594f91bc66d0f133a9551186d9626114490a8826d8d7ba0a28dcbaa049`. Ours and Teacher freeform start at seed 71782927; Student failure starts at 71782928. Unguided turn-002 starts at seed 71782828. These identify examples, not estimates of systematic success rates.

Ours lifecycle: `context/reference-alignment.json` verifies a fixed Teacher `cd Documents` transition. `methods/teacher_structured/sample/local-comparison.json` reports matching state and observation, checked before continuation. `turn-000/request.json` appends local steering, whereas turn-001 and turn-002 requests contain none. The latter create the file and finish. `score.json` passes the state and response predicates for **user turn 0 only**. Do not extend that result to the two later user requests stored in `context/task.json`.

The freeform guidance's advisor reasoning correctly diagnoses the missing `cd`; its final guidance is literally a `<tool_call>` wrapper. The subsequent actor does not execute that proposed call. This is a useful observed guidance/execution contrast, not evidence that freeform necessarily fails. Student guidance is also correct; its failed trial demonstrates failure to follow the correct order plus incomplete recovery, while its successful alternative prevents a universal failure claim.

No GPT/external structured branch exists in this package. No such method is invented. The original unguided complete first-request trajectory now exists and is included in the authored preview.

## R02A: why it remains unselected

Archive path: `steerdistill-ablation-reviewed-20261105/reviewed-20261105/local-only/R02A/`.

Full relevant sources: `checkpoint/design.json`, `checkpoint/pre-state.json`, `checkpoint/provenance.json`, `checkpoint/reference-alignment.json`, `guidance/*/{guidance,response}.json`, `trajectories/*/{trajectory,score,local-check}.json`, plus Ours `turn-000/response.json`.

The checkpoint follows a real copy action; the archive copy is newly created, not a protected original from the task's initial state. `checkpoint/design.json` explicitly lists the archive intermediate as mutable, so its rename is not a preservation violation. Ours correctly executes `cd archive` then basename-only `mv`, preserves the original and passes the constructed predicate. Both baselines first attempt path-valued `mv`; they then make additional diagnostic/schema errors, eventually enter archive and succeed.

However, Ours `guidance/teacher_structured/response.json`, `choices[0].message.reasoning` states that using a destination in the wrong location is “probably why the mv failed”, although the observed error is failure to resolve the source name. It also proposes that the source “should be archive/research_notes.txt” immediately after acknowledging the local-name constraint. The final instruction changes directory correctly, but no explicit correction resolves that causal diagnosis. The full shared prefix also contains extended tool-constraint confusion. This fails the clean-Ours analysis requirement, independent of all branches' terminal success. No alternate Ours or failing-terminal baseline trial is present in this package.

## Appointment booking: confirmed real failure, missing reasoning

Archive path: `steerdistill-ablation-reviewed-20261105/verified_20261104/booking_and_scheduling_11_4/`.

Read every variant's full guidance and continuation `*/student/trajectory.json`, Ours raw `turn-000` through `turn-004/response.json`, the original context, `task_verifier.py`, `pre_state.db` and all five final databases. Independently reran the supplied verifier (with postponed annotation evaluation for Python 3.9 compatibility; verifier logic unchanged).

Pre-state already has four slots `SL-3001`–`SL-3004`, all capacity 3, base 2, overbook capable. Ours redundantly updates three listed slots and creates BK-20 on SL-3004 with same-day flag 1. The new booking is linked to Maria Lopez (patient 2), visit type 4, scheduled; rerun result is `complete`. Teacher freeform, Student structured and unguided create BK-20 with flag 0; all rerun results are `others`. This is a substantive semantic omission, not a failure induced solely by choosing another slot ID.

External guidance incorrectly infers the 08:00 slot is missing from the returned list; its execution creates a duplicate SLOT-25. Final DB contains five slots and the verifier fails at slot count. The original slot does exist in `pre_state.db`. Context list omission must be explained before featuring that branch as a reasoning failure: mixed stored datetime strings and API filtering are an additional confound. Do not repeat the earlier “missing original slot” inference.

Ours raw responses contain `reasoning: null`, `reasoning_tokens: 0`. Thus no full actor reasoning audit is possible. Its final guidance is consistent with the observed available list and its action result is correct, but this falls below the user’s explicit clean-guidance/full-reasoning preference. No alternate trial with recorded reasoning is included.

## Deliverables and validation

Authored only a new independent `create-in-target-directory` config and ledger; no registry or shared component edits. See `create-in-target-directory.md` for source/highlight decisions and preview URLs. Schema/span/source validation passes; coordinator desktop/narrow browser review remains pending.

Final author refinement: compact action/state presentation omits redundant truthful final replies and advisor-analysis disclosures, while preserving the raw analysis and full final guidance. Highlights mark only decisive function names or directory argument values. All four result rows cite actual final execution trees. Integrity validation still passes (19 spans, 381 sources).
