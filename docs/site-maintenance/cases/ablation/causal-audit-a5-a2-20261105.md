# Guidance-to-outcome audit: A5 and A2 · 2026-11-05

This audit addresses the user's stricter requirement: a branch's mistaken reasoning may explain its failure, but that does not establish that a substantive difference in guidance explains the method contrast. No page/data selection was changed and no model was rerun.

Source abbreviations (repository-relative):

- `B12` = `data/cases/ablation_case/reviewed-20261105/reserve/multi_turn_base_12/`
- `B51` = `data/cases/ablation_case/reviewed-20261105/main/multi_turn_base_51/`

## Decision

Neither A5 Teacher-vs-Student nor A2 Teacher-vs-Student is a clean example of superior guidance content causing better execution. Both selected failing branches receive the correct requested action. Their errors are interpretable, but originate in not following that guidance; archived success alternatives further undermine the selected contrast as a content-quality explanation.

A5 Teacher-vs-freeform supplies a plausible representation hypothesis (a bare proposed tool call versus an explicit precondition/rule/transition), but the freeform already supplies the correct `cd`. The trace does not establish why it was ignored or isolate the recovery-check field. It is weaker than the simple task initially makes it appear. A2 has the same problem, with stronger counterexamples to a content-based reading.

Recommendation: do not feature either as a decisive guidance-source/structure superiority case under the new criterion. A5 could instead illustrate a local guided correction versus the original unguided failure, if that adds value beyond the accepted directory training example. Keep other trials in records. Do not explain the Teacher/Student gap by inventing an executed verification difference.

## A5: the decisive rule is identical

Selected first-request system suffixes:

| Field | Teacher structured | Student structured |
| --- | --- | --- |
| precondition | Current directory is not set to 'Documents' | Current directory is not 'Documents' |
| decision_rule | Navigate to 'Documents' directory before creating the file | Navigate to 'Documents' directory before creating the file |
| expected_transition | Change current working directory to 'Documents' | Change current directory to 'Documents' successfully |
| recovery_check | Verify current directory is 'Documents' before proceeding | Verify 'summary.txt' is created within 'Documents' |

Sources: `B12/methods/{teacher_structured,student_structured}/sample/turn-000/request.json`. The text is actually injected; this is not a mismatch between the displayed and executed guidance.

Teacher message 6 recognizes that touch creates in the current directory and chooses cd; message 8 reads the returned current directory and creates the file. There is no separate pwd or verification-tool call. It is possible that the earlier check wording helps, but the trace does not identify that field as the cause. Student message 6 ignores the identical navigate-before-create rule and touches in /alex. Message 8 explicitly notices the location mistake, then cd and touch create the target while leaving a root copy. Later requests no longer include the local steering suffix. The recovery is visible, but assigning it specifically to the Student recovery_check would be an inference, not a recorded fact.

`local-comparison.json` is a separate reference-state/observation check applied after the first response: Teacher matches cd; the selected Student touch does not. It is not the automatic execution of either natural-language recovery_check. Different check prose must not be drawn as different system verification machinery.

### Same Student guidance, both outcomes

- `B12/trial-history/trials/student_structured/guide-0/seed-71782927/`: success; cd → redundant find → touch.
- `B12/trial-history/trials/student_structured/guide-0/seed-71782928/`: selected failure; touch → cd → touch, extra root file remains.

The two complete first `request.json` objects differ **only in seed**. Their guidance text is byte-identical. Both restored-state and context hashes agree. Thus the Student rule/check combination can produce the successful ordering; the current selected failure does not establish that its check wording causes failure.

Teacher has one saved trial (seed 71782927), Student two (927 success / 928 failure), freeform one (927 failure). These are archive counts, not success-rate estimates. Samples copied under `methods/*/sample` are not extra runs.

### Freeform and unguided

`B12/methods/teacher_freeform/sample/turn-000/request.json` supplies a tool-call-shaped `cd(folder="Documents")` at seed 71782927. Its actor message 6 nevertheless assumes the earlier find path is enough and calls touch; the file is in /alex. Correct action guidance was present. Teacher structured at the same seed makes the dependency explicit and succeeds, but one such contrast cannot separate phrasing, representation and sampling sensitivity or attribute the result to a particular field.

The unguided original at `B12/unguided/trajectory.json` has the same missing directory change and final wrong location. Ours versus unguided is the clearest available *correction* illustration, because the intervention explicitly adds the prerequisite that the original agent overlooked. It does not demonstrate superiority over other correct guidance sources.

## A2: same semantic guidance, opposite results even at the same seed

Selected source paths are `B51/trial-history/<method>/<index>/`:

- Teacher structured /001: seed 71782829; correct lock instruction and locked result.
- Student structured /008: seed 71782836; correct lock instruction, but agent reasons that the user mainly requested status verification and asks again. No lock call.
- Teacher freeform /003: seed 71782829; a correct proposed lock call, but agent again recasts the request as verification-only. No lock call.
- GPT structured /003: seed 71782829; explicitly says the user already requested security and the prior response incorrectly stopped after inspection. Correct lock execution.

The Student directive is `Call mcp_tool_lockDoors with unlock=False and specify all doors (driver, passenger, rear_left, rear_right) to lock them.` Its expected result and recovery check both require all doors locked. Teacher says the same action, with explicit numeric remainingUnlockedDoors values. The differing result is not explained by a missing lock instruction or check. Both Teacher and GPT inspect a successful lock response; no unique check operation separates them from an otherwise identical attempted Student lock. Student fails before any lock/check stage.

### Strong counterexample in the saved records

`B51/trial-history/student_structured/008/turn-000/request.json` fails.
`B51/trial-history/student_structured/009/turn-000/request.json` succeeds.

Both use seed **71782836**, model `case-model`, temperature 0.6, top_p 0.95, top_k 20, repetition_penalty 1.2, and identical messages apart from the guidance suffix's JSON whitespace. Parsing those suffixes gives **identical four-field dictionaries**. After removing just the suffix, the complete request objects compare equal. /008 uses formatted multiline JSON; /009 uses compact JSON. This is evidence of sensitivity to rendering/sampling conditions, not a semantic guidance defect. The recorded pair cannot distinguish deterministic formatting influence from backend variability, so do not claim either one as the sole cause.

Also /000 succeeds at seed 71782829 with the **byte-identical** Student guidance used by /008. That seed matches the currently featured successful Teacher /001. Selecting /008 creates a failure contrast absent from this same-seed alternative.

Reviewed every distinct saved Teacher/Student/freeform injected guidance variant: seven parsed Student dictionaries, two Teacher dictionaries, and five freeform strings. All direct the correct lock operation. Some have minor descriptive imprecision (for example 'some' unlocked) but no saved variant prescribes the failing action of stopping to ask permission. GPT's more explicit authorization explanation is useful content, but is not an Ours-specific advantage and all 24 saved GPT runs pass. Counts remain archival, with retries and different guidance texts; they are not independent balanced evaluation samples.

The actor failure mechanism (misreading authorization) is clear. The guidance-to-method-result mechanism is not. Presenting these as though one source gave wrong or incomplete locking guidance would be misleading.

## Reviewed artifacts

For both cases: complete selected trajectories, first and subsequent request suffixes, state/score reports, local comparison where supplied, and saved first-request guidance variants. For A5: both full Student trajectories and identities, all four unique trial scores. For A2: full selected Teacher /001, Student /008, freeform /003 and GPT /003 reasoning; Student /009 full first reasoning and operation; all distinct Teacher/Student/freeform guidance suffixes; exact request comparison /008 vs /009; score inventory. Source state verifies wrong-location files / unperformed locking, independently of the case's authored descriptions.
