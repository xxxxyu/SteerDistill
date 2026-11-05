# Ablation case batch — 2026-11-05

Historical import record. Current selections and defaults are in [the subsequent reselection review](ablation-reselection-20261105.md).

## Scope and acceptance

User requested the first three reviewed candidates and optional unguided outputs for every ablation case. A2–A4 are implemented in the formal collection and ready for user acceptance; they are not yet published. A1 keeps its guided default pair. The article's embedded examples are unchanged.

| Code | Page ID | Raw candidate | Default pair | Readable distinction |
| --- | --- | --- | --- | --- |
| A1 | sales-order-pricing | existing point_2 | Teacher / Student structured | Pricing lookup and stored discounts |
| A2 | lock-doors | multi_turn_base_51 | Teacher structured / freeform | Execute locking versus ask again after finding unlocked doors |
| A3 | convert-then-refuel | multi_turn_base_74 | Teacher structured / freeform | Convert volume versus actually add fuel |
| A4 | enter-before-rename | multi_turn_base_27 | Teacher structured / freeform | Enter workspace and rename versus stop after missing-file error |

All four offer Teacher structured, Student structured, Teacher freeform, GPT structured and unguided. Successful alternatives remain visibly successful. Unguided is supplementary, never a default. The three new unguided suffixes reproduce the documented anchor context; original sampling is retained in records and is not described as a matched-seed experiment.

A1 only has a full original unguided run, not an additional point-2 continuation. The source creates an order dated 2026-01-01; guided continuations begin with an empty order dated 2025-10-23. It is named “无指导 · 原始轨迹”, described from its own start, and left neutral rather than inheriting the guided-date discount judgment. An independent author reviewed this addition separately. See [A1 evidence note](cases/ablation/sales-order-pricing-unguided.md).

## Authoring and root review

Three independent authors read the installed steerdistill-case-editorial skill, the accepted A1 reference, author contract, and raw target records. Each supplied one JSON and evidence/annotation ledger. Root reviewed the source-supported contrast, full selected Teacher guidance/reasoning, displayed excerpts, scope of final states, and actual interface behavior before registration.

- [A2 source and annotation ledger](cases/ablation/lock-doors.md)
- [A3 source and annotation ledger](cases/ablation/convert-then-refuel.md)
- [A4 source and annotation ledger](cases/ablation/enter-before-rename.md)

Review removed duplicate successful final replies, repetitive verifier-status rows and nonessential analyzer passages. Tool calls/results and final state carry the comparison. Reasoning and full guidance remain collapsed. A2's freeform reasoning excerpt preserves the actual mistaken intent interpretation; A3 distinguishes numerical conversion from state change; A4 retains GPT's successful diagnostic continuation without calling it an accepted first local correction.

The selected runs and full trial histories are retained byte-for-byte. Import audit matched all 2,447 source files (33,551,945 bytes); `data/cases/ablation_case/reviewed-20261105/import-manifest.json` records hashes and portable nx source hints. Do not substitute a generic methods/guidance file when a selected trial injected another revision. Missing independent generation responses for A2's selected Teacher/GPT guidance remain absent; actual injected requests are authoritative.

## Shared implementation

No per-case page, CSS or renderer was added. All four use the common comparison interface, record reader, shell and sidebar.

- Absent guidance displays “未提供指导” and creates no empty full-guidance disclosure.
- Reply and reasoning backticks use the existing inline-code renderer while preserving source annotation offsets and ordinary quotes.
- The record reader supports local-steering system suffixes and guidance `{text: ...}` envelopes; raw mode is untouched.
- Tool-response labels resolve reused call IDs in chronological order, preventing a later tool from renaming an earlier return.
- Phone selectors stack below 520px so method names remain readable.
- Shared assets use the refreshed cache version; four entry pages were rebuilt from the common shell.

## Verification

- Source/annotation validator: 19 configs, 266 exact spans, 3,180 source URLs; catalog title/code consistency passes. This supplements, not replaces, per-span editorial review in the ledgers.
- Automated suite: 23 checks passed, including absent-guidance swapping, annotated inline code, existing loading/navigation, shared shell, project-prefix URLs, article embeds and concept animation.
- Browser: all five method choices reviewed on the new cases, including optional unguided; A1's added original branch checked separately. Default pairs remain guided. Original task, reasoning and full-guidance disclosures function correctly.
- Wide and phone layouts inspected; actual phone CSS viewport 400px, document width 380px including scrollbar allowance, no horizontal overflow. Fixed the initially truncated phone method selectors in the shared component and rechecked A1–A4.
- Shared records: source links, injected four-field guidance, guidance envelope, original unguided response, user/tool messages, raw/readable switching, and return to case checked. Reused tool-ID labeling fix confirmed on the original refueling trace.

User acceptance of the new pages is pending. No push or Pages deployment is part of this batch.
