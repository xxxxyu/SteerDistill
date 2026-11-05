# Reselection: fuel tasks 74 and 61

Reviewed 2026-11-05 against the priority order: correct Ours guidance, complete relevant reasoning and result; then a baseline failure with an intelligible mechanism; then low task-reading cost. Different actor seeds are allowed for illustrative selection, with lineage retained. Subsequent coordinator instruction authorized updating the existing 74 JSON and ledger; those edits now select the failed GPT branch by default. No catalog or shared component was edited.

## Recommendation

1. **Retain 74 as a focused illustrative comparison**, led by Ours versus Teacher freeform. Select the failed GPT/external structured trial as another available branch. Keep Student structured as a successful branch because all three recorded Student trials succeed. The useful distinction is converting the requested amount versus executing the refill, not an arithmetic error. This case does not require every baseline to fail.
2. **Defer 61 as an Ours advantage feature.** Its baseline failures are usable, but the only passing Ours run has unresolved, repeated reasoning about insufficient information. No alternative clean passing Ours run exists in the supplied trial history. Keep its raw records; do not repair the reasoning by displaying only its final correct call.

74 is a good simple execution illustration, although its final unsteered reasoning is not an exemplary explanation of state addition: it briefly calls 20.04 confusing and speculates about capacity. It nevertheless correctly identifies the refill operation, uses the requested rounded amount, observes success, and accurately reports the added amount and final total. Feature the concrete execution contrast; do not call its entire reasoning flawless or claim it explicitly reconstructs 10.0 + 10.04 after the result. If the acceptance criterion requires every reasoning sentence to be unambiguous and fully grounded, neither supplied task is a pristine showcase; 74 is the materially better candidate.

## Source roots and coverage

Paths below are relative to `reviewed-20261105/main/multi_turn_base_<id>/` in the supplied `steerdistill-ablation-reviewed-20261105` archive. The 74 source is also retained at `data/cases/ablation_case/reviewed-20261105/main/multi_turn_base_74/` where available. External original-run hints are given by their portable run-directory names, not machine-specific mount paths.

Inspected all archived `trial-history/trials/**/score.json`, `all-valid-trials.json`, guidance JSON, and complete trial `turn-*/message.json` reasoning/calls/final responses. Inspected actual execution, restore, identity, local-comparison and first/next request evidence for selected 74 branches and passing 61. `methods/*/sample` are selected copies, not additional independent runs. The candidate decision is based on those records, not prior page prose.

| Case | Method | Archived trials | Passes |
|---|---|---:|---:|
| 74 | Teacher structured | guide-0 seeds 71782927/28/29; guide-1 seed 71782927 | guide-1 seed 71782927 |
| 74 | Student structured | guide-0 seeds 71782927/28/29 | all three |
| 74 | Teacher freeform | guide-0 seed 71782927 | none |
| 74 | GPT/external structured | guide-0 seeds 71782927/28 | seed 71782927 |
| 61 | Teacher structured | guide-0 seeds 71782927/28/29; guide-1 seeds 71782927/28 | guide-1 seed 71782928 |
| 61 | Student structured | guide-0 seed 71782927 | none |
| 61 | Teacher freeform | guide-0 seed 71782927 | none |
| 61 | GPT/external structured | none in supplied trial history | unavailable |

These counts describe the archive, not estimated method success rates.

## 74: exact selection and behavioural cause

Common task: add 38 liters, using a gallon amount rounded to two decimals. Before intervention, the actual converter has returned `10.038536`; current tank state remains `fuelLevel: 10.0`. The documented fill tool adds its argument to the tank. Thus the visible transition is `fillFuelTank(fuelAmount=10.04)` → `fuelLevel:20.04`. The scoped evaluation is user turn 0 (refill), not the later engine-start request included in the complete original task.

| Role | Exact sample directory | Guidance file | Decision |
|---|---|---|---|
| Ours | `trial-history/trials/teacher_structured/guide-1/seed-71782927/` | `trial-history/guidance/teacher_structured/attempt-1/guidance.json` | Retain successful guided refill |
| Teacher freeform | `trial-history/trials/teacher_freeform/guide-0/seed-71782927/` | `trial-history/guidance/teacher_freeform/attempt-0/guidance.json` | Primary failure contrast |
| GPT structured | `trial-history/trials/external_structured/guide-0/seed-71782928/` | `trial-history/guidance/external_structured/attempt-0/guidance.json` | Secondary failed branch; deliberately different seed |
| Student structured | `trial-history/trials/student_structured/guide-0/seed-71782927/` | `trial-history/guidance/student_structured/attempt-0/guidance.json` | Retain successful comparison; no Student failure exists |

Ours guidance states current fuel 10.0, converted amount 10.04, execute refill, expected total 20.04, verify that total. Its complete first reasoning checks rounding and tool argument semantics, then issues the actual fill call. `turn-000/execution.json` and `local-comparison.json` establish the response and state transition; the latter records exact reference state and observation. Its next request has no injected local-steering text; its final response correctly reports adding 10.04 and total 20.04. The post-result uncertainty described above remains in the full record and must not be editorially erased.

The freeform guidance is literally a proposed `call_tool` XML call with `mcp_tool_fillFuelTank` and `fuelAmount:10.04`. The continued agent instead narrows the task to formatting the converter output: “No other tools seem necessary here. The task is complete once the converted value is properly formatted and confirmed.” It then claims the tank has been filled without executing a refill. Its execution history contains the prefix conversion and no fill call; final fuel stays 10.0 and the verifier expects 20.04. This is the clearest failure because the reasoning, missing action and false completion claim agree on one understandable cause.

The failed GPT structured run also computes 10.04 correctly, then decides “Since the task is done” and finishes with “prepared the fuel quantity for refill.” Its guidance explicitly told it not to claim completion before the fill succeeds, so this is **failure to act on supplied guidance**, not incorrect GPT guidance. Its state also stays 10.0. The successful GPT seed 71782927 must remain in complete records; it does not disqualify the illustrative failed seed 71782928.

Student structured guidance correctly gives the same additive transition, and all three runs execute it. Seed 71782927 is the compact representative; its post-result reasoning briefly questions the total then recognizes existing fuel and the requested addition. Do not label a Student branch as failed or use mild verbal uncertainty as a task failure.

### Lineage and source map

74 originates from run directory `ablation-pending-reference-repair-20261105/cases/multi_turn_base_74`. All selected trials share context hash `146341f5935222904f318eb3eaa0b86bc57d56416d475e2c856b8a6f61f9557d` and state hash `d3c68590caee17e444b92be8b67f776e5f05347fbbe8ceb4acb15bb0f471551e` in `identity.json`; their guidance hashes and seeds differ. All selected guidance artifacts use evidence hash `2428e41994d924458ea7ed193e66bc48487b70fa43c8607c78da6239fce0eb12`. Ours uses guidance attempt 1; the other selected branches use attempt 0. Ours attempt 0 fails all three recorded seeds and must remain available in trial history. This is an illustration selected from available trials, not a same-seed four-way stability or necessity claim.

- Task and evaluation scope: `context/task.json`, `context/scope.json`.
- Shared converter result and unchanged tank state: `context/prefix-execution.json`, selected trial `restore.json`.
- Guidance and whether it is actually supplied: guidance paths above; selected trial `turn-000/request.json`, system message suffix “Local steering for this response only”.
- Ours removal on continuation: `teacher_structured/guide-1/seed-71782927/turn-001/request.json` under the trial root; no local steering suffix.
- Full reasoning, calls, and final claims: each selected trial `turn-000/message.json`; Ours and Student also `turn-001/message.json`.
- Verified state and omission: each selected trial `execution.json`, `local-comparison.json`, `score.json`.
- Optional emphasis: highlight freeform’s decision that formatting completes the task, failed GPT’s “Since the task is done”, actual `fuelAmount:10.04`, and returned/unchanged final fuel where relevant. Leave generic conversion arithmetic unmarked because every selected method gets it right. Ours post-result uncertainty stays readable in full reasoning without positive emphasis.

## 61: why no replacement Ours run is clean

The scoped user request is turn 1: add the minimum integer fuel for reaching Rivermist. Restore state has 42.0 gallons; the accepted reference transition is adding 7.0 to reach 49.0. Earlier route and feasibility steps form the fixed prefix. The available distance tool describes kilometers while reasoning calls the reported 980.0 miles; avoid independently endorsing the entire route calculation as a physically verified minimum. The local target state is verified, but the complete reasoning is the deciding quality issue.

The only passing sample is `trial-history/trials/teacher_structured/guide-1/seed-71782928/`, with guidance `trial-history/guidance/teacher_structured/attempt-1/guidance.json`. It is the same run copied to `methods/teacher_structured/sample/`. Guidance correctly supplies 42.0 current, 49.0 required and their 7.0 difference. The actual call adds 7.0 and the result/state reach 49.0; local comparison records exact reference state/observation and scoped official checks pass.

However, complete `turn-000/message.json` repeatedly claims that the required data cannot be obtained, considers unavailable parameters, and concludes that the tools are insufficient. Its closing paragraph says: “But since the tools don't confirm this, the proper response is to point out the limitation. However, following the scenario's context, the correct action is to fill 7.0 units.” It does not explain why that context resolves the preceding objection; it oscillates between advice and action, then emits the correct call. This is a correct state transition with confused justification, not clean full reasoning. The next reasoning infers feasibility from the filled total without a new feasibility call. Do not describe it as an executed feasibility recheck.

The other Ours samples are not cleaner replacements: guide-0 seed 71782927 gives an insufficient-information answer; guide-0 seeds 71782928 and 71782929 compute 7 from ground-truth-labelled guidance but only recommend it; guide-1 seed 71782927 says it will trigger a fill yet emits no call. All four leave fuel at 42.0. The supplied archive therefore has no clean passing alternative.

Strongest baseline if the task is revisited is Student structured `trial-history/trials/student_structured/guide-0/seed-71782927/`: it recognizes 49−42=7 from guidance but stops at recommending fuel, rather than calling the tool. Teacher freeform `trial-history/trials/teacher_freeform/guide-0/seed-71782927/` instead ignores its explicit 7-gallon call guidance and refuses for missing fuel-efficiency data. Both fail with unchanged 42.0. Their failure mechanisms are real, but cannot elevate the passing Ours reasoning into the desired showcase.

61 originates from `ablation-reviewed-semantic-backfill-20261105/cases/multi_turn_base_61`. The passing Ours identity has context hash `b1c0e1ae9baf47b949f14b67d0f929e0137a60a73e5a7ed245510c3d1b5b629d`, state hash `34d05cbd31893df3fa32ef87d77bb17f52371d8c0e907d1a7f8d4bb38c02b690`, and seed 71782928. Preserve the earlier failed trials and distinct guidance attempts. Reconsider only if another recorded Ours trajectory supplies a clear, consistent decision-to-action chain; a new score alone is insufficient.
