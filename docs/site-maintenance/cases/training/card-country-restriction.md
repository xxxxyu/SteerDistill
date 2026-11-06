# 银行卡国家限制：名单与总开关

## Selection and current authorization

Selected as a compact training-correction example: the unguided agent repeatedly reads the correct switch definition but commits `international_allowed=1`, allowing all international transactions despite also writing `US,CA`. The guided actor uses `0`, which enforces the list. The tool writes, actual card configuration, and saved-reference comparison agree. The page explains configuration correctness, not a real transaction test.

The user explicitly allows a case whose valid state comparison was supplemented later, provided it compares the correct immediate step. This case is therefore not excluded by the earlier blanket requirement that reference comparison must have executed as the runtime gate. This authorization does not change source history: the original runtime check was a native task-completion check; the reference-state report was added later. The page calls the latter “参考对照”, never claims it triggered continuation, and does not turn that distinction into reader-facing disclaimer prose.

## Sources and import

- Authored config: `design-lab/case-content/training/card-country-restriction.json`.
- Shared template/reference: training API; `training/directory-navigation.json` and accepted `training/tool-list-numbering.json` supply composition, not target facts.
- Raw root: `data/case-library/training/card-country-restriction/raw/`. All source paths below are relative to this root.
- Coordinator-provided package: `training_steering_9_cases_20261106/cases/003_banking_6_2`, from the training review package on host alias `neogpu-a100-nx-1`. The actual model source is identified by the preserved `protocol.json` and `supplement-protocol.json`.
- Imported all 129 package files, unchanged. `import-manifest.json` records SHA-256 and byte sizes, checked against the provided package after copying. The manifest is the 130th source. This author did not independently redownload the upstream server package and does not claim a remote-server hash check.
- Unlike an earlier package description, this actual source includes both `initial.db` and `pre_state.db`. They were inspected and preserved.
- Full inventory retains every request, reasoning, response, local database, final database, environment, schema, native verifier/check and later comparison artifact. Primary reader sources are before/after/reference trajectories, original guidance and saved-state reference comparison. Native runtime gate and protocol records are secondary, without default-flow metadata clutter.

## Raw audit and timing

1. All three selected trajectories' first ten messages are exactly equal. The original task is `task.json.task`, also message 1 in `context.json`; the entire original request is preserved in the collapsed task disclosure.
2. Common history has already looked up account 3, created card 5, set a 2000 USD limit and activated it. `initial.db` has no card 5. `pre_state.db` has card 5 with account 3, virtual/2000/USD/active and no `card_controls` row. The source database resolves the initial state rather than relying on the old summary.
3. Each branch has one next operation at trajectory message 10, its return at 11 and a final textual answer at 12 with no tool call. Each branch's `local_state.db` is byte-identical to its own `final.db`.
4. `before` calls `mcp_server_update_card_controls` with `international_allowed=1`, `allowed_countries="US,CA"`, `card_id=5`. It writes a row with integer 1; its returned API representation is Boolean `true`.
5. `reference` and `after` call `mcp_server_create_card_controls` with `international_allowed=0`, same country list and card ID. Both write integer 0, returned as Boolean `false`.
6. Inspected `after/environment.py` CardControlUpdateRequest description (“1 to allow all international, 0 to enforce allowed countries”), plus both create/update implementations. Update also creates a missing row. Thus choosing update is not the failure; the selected switch value is. No tool-name highlight or create-versus-update success claim is used.
7. `after/turn-000/original_request.json` has the exact guidance appended to system content as “Local steering for this response only”. `after/turn-001/original_request.json` omits it and generates only the final explanation. This case does not have another unsteered environment-changing action after the correction.
8. Original `after/local_gate.json` says `native_state_verification: complete` and `checked_before_continuation:true`, with scope requiring task completion immediately after the single response. It is not a runtime reference-state-equality receipt. The coordinator independently checked the runner's snapshot ordering; this author independently confirmed one action then text-only completion and identical local/final bytes.
9. `reference_state_comparison.json` explicitly describes comparison of saved immediate post-action databases, with no new model inference. Independently verified its three source SHA-256 values, queried actual card/account/control fields, and compared every reference/after database table ignoring only `created_at` and `updated_at`. Equality passed even without removing `card_controls.id`. Before differs on the decisive flag.
10. Ran the original `task_verifier.py` against imported `initial.db` and each immediate local database: before returns `others`, reference and after return `complete`. The local Python required postponed type annotations; this was injected in memory only, with no source-file change. The verifier checks new-card identity, account 3, virtual/2000/USD/active and exact country set US/CA with flag 0. No financial transaction was created or tested.

## Complete reasoning and guidance review

Reviewed all selected before/reference/after messages, full turn-000 and turn-001 reasoning, and `steering/analysis.json` final guidance plus full Teacher reasoning.

- Before turn-000 reasoning repeatedly states the actual switch semantics correctly, then chooses 1 anyway. It contains unresolved contradiction, not an explicit correction followed by a corrected call. The excerpt deliberately preserves a correct reading followed by the final wrong choice, in chronological order. Its final response also incorrectly claims the resulting configuration restricts usage to US/CA; no later tool fixes the state.
- Reference turn-000 chooses 0 to enforce the country list; its final summary agrees with the saved state. No conflicting flag choice occurs.
- Guided turn-000 quotes the actual Teacher decision rule, chooses 0 and executes it. Turn-001 accurately summarizes the configured restriction. No wrong intermediate reasoning is hidden.
- Teacher four fields have the correct existing-card precondition, switch value, country list and expected state. The conditional recovery_check is not presented as an extra status-query call. Its reasoning says update updates an existing row without mentioning that this implementation also creates a missing row; that is an incomplete generalization, not the causal distinction. The final create call is supported and correct. The page neither quotes that incomplete generalization nor implies update would have failed.
- The case supports the correction's parameter/configuration meaning. It does not claim superiority from call-name differences, measured behavior of a payment system, or a reference comparison that was not actually performed at runtime.

## Display/source map

| Display | Source | Transformation and purpose |
| --- | --- | --- |
| Title and task summary | `task.json.task`, `context.json` messages 2–9; `after/environment.py` parameter definitions | State the user's desired configuration and relevant flag semantics. No precision/checkpoint/task IDs in prose. |
| Original request | `task.json.task` | Verbatim full request, shared originalTask disclosure. |
| Before call/return | `before/trajectory.json.messages[10/11]`; before execution and local DB | Remove only common `mcp_server_` prefix, preserve actual update function and argument values. Arrange three arguments on two lines. Return excerpt preserves actual Boolean `true` and country string; omit row ID/timestamps. |
| After call/return | `after/trajectory.json.messages[10/11]`; after execution and local DB | Same display transformation, preserve create function, 0 argument and Boolean `false` return. |
| Before optional reasoning | `before/trajectory.json.messages[10].reasoning` | Exact two-line flag definition followed by `…` and the final “I'll set…” sentence. Do not turn internal questioning into claimed self-correction. |
| After optional reasoning | `after/trajectory.json.messages[10].reasoning` | Exact full sentence quoting the actual decision rule. Ordinary single quotes remain ordinary text. |
| Teacher four fields | `steering/raw_steering_prompt.txt` | Parsed object, every field value unchanged. No inserted code formatting for ordinary single quotes. |
| 配置状态 | after local DB: cards id 5 and card_controls card_id 5 | 0/US,CA plus retained active/2000. Card ID stays in trace and records rather than task metadata. |
| 参考对照 | reference/after local DBs and `reference_state_comparison.json` | Same configuration; before still has flag 1. Do not label this runtime acceptance or an executed transaction check. |

All displayed excerpts carry file/message source pointers. Raw bytes and records remain untouched. Returned Boolean types are not silently changed into integers: action parameters use 1/0, returns use true/false, state prose uses saved integer values.

## Individual annotation ledger

| Passage | Kept span and meaning | Reviewed without extra mark |
| --- | --- | --- |
| Before action m10 | Red `international_allowed=1`, the wrong policy switch for the requested restriction | Actual update function left without highlight: it successfully writes the row. Country string is correct and therefore unmarked. |
| Before result m11 | Red `international_allowed: true`, showing that the wrong setting was actually persisted | Country list retained unmarked, not implied to override the switch. No invented error return. |
| After action m10 | Blue `international_allowed=0`, the value enforcing the list | Create function and country string unmarked; do not suggest the function-name change is causal. |
| After result m11 | Blue `international_allowed: false`, observed representation of the corrected switch | Remaining payload retained only as needed for contrast. |
| Before reasoning m10 | Red final `'international_allowed' to 1 and allowed_countries to US,CA` span (actual backtick/double-quote syntax kept), the mistaken commitment after reading the right definition | Preceding correct definition is ordinary prose, not red highlighted. Full contradictory repetition stays in records rather than overwhelming the optional excerpt. |
| After reasoning m10 | Blue `'international_allowed' set to 0 (to restrict)` | Function and country names remain unmarked; the rule is readable without emphasizing every token. |
| Teacher guidance and result fields | No additional background highlights; shared guidance fields and inline code provide hierarchy | No automatic bold agent, metadata badges, quoted-text code conversion or blanket semantic rules. |

Six retained spans, each individually selected for flag choice or persisted configuration. Offset matching validates exact display locations, not semantic importance.

## Validation and coordinator handoff

- All 129 imported files hash-match the supplied package; the three immediate DB hashes also match the later reference report.
- Original task, all displayed arguments/return values and reasoning excerpts checked directly against raw records.
- State SQL, shared prefix, local/final byte equality, full reference/after DB comparison excluding timestamps, and native verifier re-evaluation passed.
- `node design-lab/case-shared/validate-case.cjs design-lab/case-content/training/card-country-restriction.json` passed: 1 config, 6 exact spans, 130 source URLs.
- Suggested index title: `国家限制开关`; coordinator owns T3 registration.
- Pending coordinator browser review: paired action/return wrapping, original-task/reasoning disclosures, guidance row layout, records guidance/reference comparison/SQLite downloads, desktop and narrow screen.
- Unregistered page: `/design-lab/paper-cases.html?group=training&case=card-country-restriction`.
- Record link: `/design-lab/case-records.html?group=training&case=card-country-restriction&source=before%2Ftrajectory.json&message=10`.
- No catalog, shared template/CSS, article files or other case were edited; no commit.

Coordinator editorial pass: title narrowed to 国际交易; guidance heading uses “启用国家限制”; both action frames explicitly label returns as 节选. No call arguments were removed. The entire original task and each contiguous reasoning piece were rechecked for exact raw-string membership; the before excerpt uses an explicit `…` between noncontiguous pieces, and its first two lines are contiguous in the source.
