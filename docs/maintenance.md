# Website maintenance

Build and serve the research website from the files in this branch. The source map below identifies
the templates, presentation data, and records used by each page.

## Source map

| Change | Source |
| --- | --- |
| Shared shell and four generated HTML pages | `site/templates/`, `scripts/build-pages.mjs` |
| Fonts, theme, navigation and page layouts | `site/` |
| Chinese article and four embedded cases | `design-lab/main-article.zh.json`, `design-lab/article-content/` |
| Formal case catalogue and Chinese case content | `design-lab/case-content/catalog.json`, its three kind directories |
| English case overlays | `design-lab/case-content/en/` |
| Case/record components and exact-span checks | `design-lab/case-shared/` |
| Published case evidence and downloads | `data/case-library/` |
| Homepage result chart and downloadable table | `experiments/data/` |
| GUI task replays, reviewed annotations and screenshots | `demos/`, `scripts/build-demo.py` |

Edit templates, then regenerate HTML; do not edit generated HTML directly. `python3
scripts/build-case-locales.py` regenerates the English catalogue. An English overlay's
`sourceSha256` binds it to the reviewed Chinese JSON. When changing a source list, remap its
translated indices. Review translations before updating the hash. Keep original task/action/guidance
evidence intact, except for declared privacy redactions applied consistently to every copy.

Case authoring and renderer contracts remain in [case content](../design-lab/case-content/README.md)
and [shared components](../design-lab/case-shared/README.md).

## Case evidence and privacy

Only evidence supporting registered cases is published. Do not import whole experiment directories.
Keep stable case/source IDs, all primary records, and files referenced by displayed evidence.
Exclude nested import ZIPs, SQLite dumps, transport/tokenization logs, local runtime code, and stale
checksums.

Replace experiment host/user roots with `/redacted` before publishing any raw record. Simulated
benchmark paths such as `/alex`, `/workspace`, `/home/user`, and task-provided mock account fields
are evidence, not paths on a researcher's machine. Preserve them. The task replays use simulated app
state and test identities; review new screenshots as well as text for actual personal data. Never
use model-generated success claims as a substitute for recorded outcomes.

For a new or changed case, update its `manifest.json` inventory, byte sizes and SHA-256 values to
match the sanitized public files, then run:

```bash
python3 scripts/case-library.py --package
python3 scripts/case-library.py --check
```

The ZIP contains those exact public bytes and its manifest. This manifest verifies the distributed
sanitized copy; it does not claim byte identity with private experiment originals. Do not add
historical manifests describing removed files. The checker rejects source links outside the case's
own root.

## GUI replays

Run `python3 scripts/build-demo.py` after editing source records or reviewed annotations. The four
tasks contain 172 decisions in total: WPS 13, Slack 52, WhatsApp 70, and Google News 37. A decision
is one recorded model response with its thought, action, executed coordinates, and timing fields.
The 184 PNGs are one screenshot per decision plus a final screen for each of the 12 task/model runs.
The release cleanup preserves the original bytes of all 172 decisions and 184 screenshots; only
experiment paths in provenance metadata are redacted.

Measured step endpoints and inference/execution durations determine replay timing; phase placement
within each step is reconstructed. The screenshot sequence is not continuous video and has no
measured token-level timing. Selection is post hoc, not evidence of aggregate speed or a
matched-training ablation. Model-lineage information in `demos/*/source.json` awaits updated author
evidence; do not infer lineage from a redacted model-storage path.

## Validation

```bash
python3 scripts/check-release.py
```

This runs generated-page/locale freshness checks, all existing Node tests, case annotation/link
checks, ZIP/hash verification, and text/archive privacy checks. Check the homepage, article, a
training/inference/recovery case and raw reader in a browser at both root and `/SteerDistill/`
hosting, in both languages, on desktop and narrow screens. Inspect themes, method selection,
language switching, replay controls, and source downloads after layout changes.

The global language choice is preserved between entries. Homepage defaults to English; article and
cases default to Chinese. The article body remains Chinese. Legacy ablation URLs are aliases for the
current guidance-comparison section; they do not require keeping withdrawn case configurations or
raw banks.

## GitHub Pages deployment

The code branch `codex/arxiv-code-release` is the repository default. GitHub Pages serves `/` from
`codex/case-expansion-20261104`. Push changes to the website branch after running the publication
checks.

Existing development history is retained for now. Before the public announcement, consolidate the
release into a clean commit as agreed with the project owner.

## Release TODOs

- TODO: Add the public arXiv URL in `site/templates/home.html` and rebuild the pages.
- TODO: Add checkpoint download links in the same resource navigation.
- TODO: Reconcile GUI model-lineage metadata with the updated author evidence.
