# Formal case author contract · schemaVersion 1

Authors write exactly one `case-content/<kind>/<slug>.json` and one editorial ledger under `docs/site-maintenance/cases/<kind>/<slug>.md`. Kinds are `training`, `inference`, `recovery`, `ablation`. Do not change the registry, readers, shared assets or another author's case. An integration owner registers accepted JSON in `catalog.json`; loading a case never generates or rewrites its content.

The single maintained component source is `design-lab/case-shared/`. Read the editorial SKILL and `case-shared/README.md`; follow the selection gate and review raw data before authoring. Existing case JSON is a composition reference, not evidence for a different task.

```json
{
  "schemaVersion": 1,
  "id": "my-case-slug",
  "kind": "inference",
  "title": "Concrete case title",
  "summary": "Task and material environment condition.",
  "template": "comparison",
  "originalTask": {"question": [[{"role": "user", "content": "Full verbatim user request"}]]},
  "presentation": {},
  "records": {
    "defaultSource": "ours",
    "defaultMessage": 4,
    "sources": [{"id": "ours", "label": "SteerDistill · 轨迹", "url": "data/cases/example/Ours/trajectory.json", "primary": true, "format": "auto"}]
  }
}
```

All `url` / external-download `href` values are site-relative (`data/cases/...`, without a leading slash), or portable HTTPS URLs when needed. `SitePaths.url()` resolves these resource paths relative to the deployed site, including its project prefix. Do not rewrite filesystem paths inside raw records. Raw bytes stay in their original location; do not duplicate archives. IDs/slugs must be stable `[a-z0-9_-]+`. `title`/`summary` belong in the envelope only; no machine provenance or protocol boilerplate in the task summary.

## Titles and explicit case codes

Use a full `title` that identifies the task and its key decision, without a final period, Chinese full stop, question mark or exclamation mark. Keep the title in the case JSON and matching catalog entry identical; do not include the case code in that text.

For each accepted entry, the integration owner adds a fixed `code` and a separate `indexTitle` to `catalog.json`. Prefixes are `T` (training), `I` (inference), `R` (recovery) and `A` (ablation), followed by a positive integer. Assign the next unused number in the category; never derive it from display order or recycle a withdrawn code. Existing entries are renumbered only when the user explicitly requests a reorganization; record that mapping in the integration notes. Unregistered author previews need no code.

Catalog groups may define ordered `sections: [{id, label}]` for reading subgroups. Each registered case in that group sets `section` to one declared ID. Keep case entries in the intended reading order; the shared adapter supplies the subgroup layout. This classification is editorial data, not inferred from task IDs or keywords.

`indexTitle` is a short subject label, manually chosen to fit one sidebar line with its code (at most eight characters; prefer four to six Chinese characters). It has no final sentence punctuation. The shared sidebar displays `I1 · 工具名大小写`, while the case heading displays the same code followed by the full title. Do not hide an overlong index with an ellipsis or put identifiers into the task summary. Check the actual sidebar fit when integrating a case.

## Templates

`template: "training"`: `presentation` is the data portion of `CaseTemplates.training`: `branches`, optional `guidance:{title,fields,checks,takeaway}`. `branches[]` contains `{title,summary,tone,events,reasoning?}`. `guidance` is one row-based full-width box and optional execution checks. The shell supplies envelope title/summary/originalTask and records footer.

`template: "sequence"`: `presentation` is the data portion of `CaseTemplates.sequence`: `steps`, optional `sequenceTitle`, `reference`, `result`, `compact`. Preserve accepted recovery composition using `reference:{position:"before",compact:true,...}` when appropriate. These are layout options, not evidence claims.

`template: "comparison"`: `presentation` contains:

- `methods[]`: `{id,name,heading?,description?,turns:[eventArrays],tones:[tonePerTurn],reasoning:[{text,highlights,source}?],outcomes:[string?],record:{sourceId,message}}`.
- `turns[]`: `{label,title?,summary?,showOutcome?}`. If `showOutcome` is true, the generic loader reads that turn's `method.outcomes[index]`; no callbacks in JSON.
- `defaultPair:[leftId,rightId]`, optional `selectionLabels:[leftLabel,rightLabel]`.
- Reserve each branch heading for its method/intervention name (`heading` may be omitted to use `name`); put observed behavior in `description`. Do not insert a full-width schema/protocol explanation between paired headings and action frames. Material common tool constraints belong in the task background.
- Retain all available inference methods. Selections update actions, reasoning, observed results and records together. Branch color reflects local behavior, not full-task score.
- Optional `details:{guidanceTitle,guidanceLabel,resultTitle}` enables the accepted ablation continuation. Each method then supplies `guidanceExcerpt`, `guidanceHighlights`, `guidance` (four original fields, or `{guidance: "freeform text"}`), and `resultLines:[{text,highlights,source}]`. This uses the existing fields/highlight components; do not invent a renderer.

All event arrays use **display-ready** EvidenceUI strings:

```json
{"type":"action","name":"lookup","args":"key=\"value\"","result":"found=true","highlights":{"args":[{"start":5,"end":10,"text":"value"}]},"source":{"file":".../trajectory.json","message":4,"returnMessage":5}}
```

Fix the illustrative span offsets to your literal text; spans use JavaScript UTF-16 indices. Replies use `{type:"reply",text,highlights:{text:[]},source}`. Reasoning uses `{text,highlights,source}`. Spans may include explicit `tone:"before"|"after"`; otherwise they inherit the frame. Every occurrence must be manually reviewed in the ledger, including deliberate no-mark decisions. Do not send raw argument objects for the renderer to format, choose highlights or infer correctness. Mark omissions as excerpts and preserve event order.

## Shared record reader manifest

`sources[]` is the full inventory; set `primary:true` on the few default sidebar sources (usually each method's trajectory, guidance, verifier). Other files stay available through the secondary source picker. Each entry is `{id,label,url,primary?,format?,messagePath?,tone?}`.

- `format:"auto"` recognizes `messages`, `trajectory`, response `choices[].message`, arrays, and single JSON objects. `messagePath` is an optional dot-separated path to an explicit message array.
- `format:"guidance"` displays original structured guidance in shared fields, or freeform text unchanged.
- `format:"text"` keeps text readable; `format:"sqlite"` is download-only binary.
- `tone` is optional and editorial, never inferred from method identity. Do not mark an entire trajectory blue when it contains a meaningful error; use neutral manifest tone and case excerpts for local annotations.
- `records.defaultSource/defaultMessage` and each comparison method's `record` provide stable deep links. The reader supports exact raw-file mode and current-source download. Full file inventories do not replace the focused source → message reader.
- Optional `records.download:{href,label}` can link an existing complete archive; no new archive is required.

## Reference configs (accepted content, migrated without new conclusions)

- `training/directory-navigation.json`
- `inference/watchlist-disambiguation.json`
- `recovery/fuel-capacity.json`
- `ablation/sales-order-pricing.json`

Formal page: `design-lab/paper-cases.html?group=<kind>&case=<slug>`.
Record reader: `design-lab/case-records.html?group=<kind>&case=<slug>&source=<sourceId>&message=<zeroBasedIndex>`.

The ledger must map claims/excerpts/results to raw files and message/field/DB predicates, describe protocol limits, and record every retained/unmarked passage decision and validation. New pages require source validation and coordinator browser acceptance before catalog integration.

## Local validation and unregistered previews

Run the read-only integrity checker before handoff:

```sh
node design-lab/case-shared/validate-case.cjs design-lab/case-content/inference/my-case-slug.json
```

With no file argument it checks all registered cases. It verifies shape, turn alignment, display strings, exact span boundaries/text, source-file existence, registry ID/code collisions, category code prefixes and title/index consistency. It does not choose or repair annotations, prove raw-source fidelity, or replace the ledger review.

An explicit safe `group`/`case` URL can load an unregistered JSON at its prescribed path for coordinator preview. This adds nothing to `catalog.json`; only reviewed entries belong in the saved registry. Old directory-task and reference aliases are recorded in the registry for backwards-compatible links.


Withdrawn cases are listed in the catalog group's `retiredCases`; they are no longer available as formal unregistered previews. Preserve their raw data; historical presentation files remain in the pre-publication archive. This keeps withdrawal distinct from an author preview awaiting review.

For a tool return whose meaning differs from its frame, set its manually reviewed `returnTone` to `before`, `after` or `neutral`. Omission or an empty string inherits the frame. For example, a returned price can be valid for the requested date even when the agent selected the wrong date. This is an evidence decision, not a method-wide formatting rule.
