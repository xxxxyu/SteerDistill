# Site maintenance

This repository is a static publication tree. GitHub Pages serves the root at https://xxxxyu.github.io/SteerDistill/. The 2026-11-02 revision separates the English project landing from the Chinese research article while retaining continuous scrolling between them. All four entry pages share the navigation, theme and typography.

## Four entry pages, one shell

| Entry | Purpose | Language |
| --- | --- | --- |
| `index.html` | Paper identity, benchmark overview, TL;DR and concept animation | English |
| `article.html` | Independent research blog post, Xiangyu Li byline, contents and notes | Chinese |
| `design-lab/paper-cases.html` | Nineteen listed full cases: 5 training, 9 inference, 5 recovery | Chinese |
| `design-lab/case-records.html` | Original trajectories and record navigation | Chinese |

The navigation labels are shared and deliberately Chinese: SteerDistill / 研究文章 / 案例分析 / theme. A bilingual interface is deferred until the content is settled.

Current release review: [2026-11-06 case finalization](case-finalization-20261106.md). The collection has three groups. Training contains 修正过程 (T1–T4) and 指导对照 (T5, formerly A6/A1). Old ablation URLs remain compatible. Current raw records and per-case downloads are indexed in [the case library](../../data/case-library/README.md).

Earlier audits keep their historical numbering; consult the finalization mapping rather than interpreting old A1 references as the current ticket case.

### Sources and ownership

| Change | Edit |
| --- | --- |
| Navigation markup, labels and destinations | `site/templates/header.html` |
| Fonts, paper colors, theme palette, global navigation geometry | `site/site.css` |
| Initial theme and interaction | `site/theme-init.js`, `site/site.js` |
| Homepage paper identity and overview content | `site/templates/home.html` |
| Homepage composition | `site/home.css` |
| Benchmark rendering / concept animation | `design-lab/press.js`, `design-lab/p2-concept.js` |
| Article title, author, sections, paragraphs and footnotes | `design-lab/main-article.zh.json` |
| Article renderer and instructional diagrams | `design-lab/main-article.js`, `design-lab/main-article.css` |
| Blog layout, reading navigation and responsive notes | `site/article.css`, `site/reading.js` |
| Continuous homepage-to-article reading | `site/home.js` |
| Case/record body templates | `site/templates/paper-cases.html`, `site/templates/case-records.html` |
| Approved inline case excerpts | `design-lab/article-content/cases.zh.json` |
| Full cases and registry | `design-lab/case-content/` |
| Shared evidence, case layout, sidebar, URL resolution | `design-lab/case-shared/` |
| Interactive task gallery, replay data and timing | `demos/catalog.json`, `demos/{wps,slack,whatsapp,news}/`, `scripts/build-demo.py`, `site/demo-gallery.js`, `site/demo-timing.js`, `site/demo-replay.js`, `site/demo-replay.css` |
| Original records / benchmark figures and inputs | `data/`, `experiments/` |

Run `node scripts/build-pages.mjs` after editing templates or article metadata. It generates all four HTML entry pages with one header and shared asset declarations. No framework server or package installation is required; commit generated pages together with their sources. `node scripts/build-pages.mjs --check` detects stale output. Do not edit generated HTML directly.

## Reading behavior

The homepage progressively renders the same article component below its task demonstration section. Scrolling remains entirely native: no wheel interception, artificial scroll thresholds or forced document reload. Crossing into the article updates the URL to `article.html`, the title and active navigation using `replaceState`; scrolling back restores the homepage address. Passive scrolling does not create history entries. Explicit links retain normal browser navigation. Reloading or sharing the article URL opens the independent post without the landing page.

The article uses a symmetric 1080px grid: 172px contents, 28px gap, 680px reading column, 28px gap, 172px contextual notes. All case embeds, figures and resource links share the 680px reading measure. Below 1160px, both rails collapse together: contents becomes a disclosure and notes move to the endnote list; the reading column stays centered. The post ends with its resource links, without a duplicated site footer. Each footnote is authored once alongside its paragraph and rendered consistently in either view. Six short section labels come from the same chapter data as the headings.

Article metadata uses `post.title` for the document title and optional `post.titleLines` for intentional heading line breaks. `post.author`, `post.date`, `post.intro` belong to the blog, not the paper author block. A paragraph can provide `note: { id, text }`; the renderer generates stable references, notes and return links. Chapter `id` values remain stable for external links.

Old `design-lab/p2.html` links still redirect to the root. Homepage links with existing article section hashes redirect to the independent post. All assets resolve through `SitePaths.url()` and support the GitHub project prefix. Raw task paths are never rewritten.

## Homepage demonstrations

The homepage offers four tasks from `SteerDistill-FourTasks-FullTrajectories-And-Media.zip`: WPS document search, Slack image sharing, WhatsApp poll creation and Google News article reading. `demos/catalog.json` defines their order, task descriptions and data paths. Unchanged records and screenshots for BF16, SteerDistill and On-Policy QAD live in each `demos/{task}/raw/`; package hashes and source conditions are recorded in each `source.json`. Previous BestBuy video provenance remains in `demo-sources.json`, but those placeholders are no longer shown.

Run `python3 scripts/build-demo.py` to regenerate all four `replay.json` files. The builder retains all 172 decisions and original thought/action strings (WPS 13, Slack 52, WhatsApp 70, Google News 37). Individually reviewed highlights and reasons, including deliberately unmarked steps, live in each `editorial.json`; the builder only validates exact text matches and converts them to offsets. Add future tasks through the catalogue, original records and editorial data rather than separate player implementations.

`DemoReplay.mount()` owns a task's clock, method rail and screen viewer. `demo-gallery.js` owns the task tabs and panel lifecycle. Tasks use an open four-column editorial index (two columns on narrow screens), with the app name above a short task title. The task description sits directly below the index; methods use the lighter horizontal `ArticleCaseRail.mount()` interface shared with the article (`language: 'en'`, optional `detail` text for precision). Method order is BF16, SteerDistill W4A16, On-Policy QAD W4A16, initially showing the first two. Task selection pauses the outgoing replay and preserves its local positions, shared clock and method selection. Only the selected task loads initially; its screenshots are decoded before playback. Direct links use `?demo=wps|slack|whatsapp|news#demo`. Tabs support arrow keys, Home and End. No autoplay.

The global control drives all methods in the current task. Each method timeline and Previous/Next control can inspect a paused local position without changing the shared clock or other methods. During playback, other methods continue while the inspected method stays paused. Explicit global seek or Play resynchronizes all methods; each playhead stops at its own run end. Horizontal method navigation does not change time or card height. Thinking and action remain visible together through shared `EvidenceUI.frame`, `highlightedText` and `action` components; long output scrolls within its frame. The previous output remains visible while the next decision is being generated, labelled with its source step. Screen enlargement pauses playback. Tap and swipe overlays use executed screenshot coordinates. Precision labels were verified against checkpoint AWQ configs in `demos/wps/precision-source.json`. Inference, execution and overhead use blue, brick red and warm gray; the area after a run finishes is unfilled paper.

**Timing contract:** per-step elapsed endpoints, inference duration and environment duration are measured. Internal phase placement is reconstructed as overhead → inference → execution; the source does not contain exact phase start timestamps or token-level timestamps. Do not label the slowed source MP4 duration as execution time, stream invented token timings, stretch shorter runs to align their steps, or add waiting time to a completed run. Executed screenshot coordinates, rather than normalized model coordinates, drive click markers. The entire replay is a screenshot sequence, not continuous captured video.

Editorial observations retained in the replay:

- WPS: BF16/SteerDistill each complete in five decisions. Inference: 3.4313/2.2459 s; execution: 2.2786/2.2804 s; total: 7.0462/5.8493 s. SteerDistill starts with a welcome toast; both can access search. QAD types without focusing search and stops after three decisions. Its initial intention to search is correct and is not marked as a failure.
- Slack: both successful runs upload twice; all 11 decisions and the duplicate image remain visible. QAD repeatedly taps outside the attachment target and reaches the 30-action limit. Highlights focus on the first miss and the unsupported repetition, not every repeated sentence.
- WhatsApp: BF16 first explores the wrong menu, then switches to the attachment menu; SteerDistill takes the direct path. QAD never focuses the name field and cannot advance. SteerDistill's verification-code steps are taps; the environment fills the code. Do not describe those taps as typing the code from its thought.
- Google News: both successful runs visit three Sports articles. BF16's final recap names two stories it did not visit; those statements are marked red despite evaluator success. SteerDistill uses related stories after a Back tap leaves the article open. QAD ends as infeasible immediately. Preserve the distinction between evaluator success and correctness of the closing summary.

The source's older QAD training lineage differs from BF16/SteerDistill: these selected runs are behavioral examples, not matched-training ablations or aggregate speed claims. These conditions remain in the source files rather than the replay UI. The gallery ends with two sentences covering the base model, ScaleWoB, BF16-to-W4A16 initialization, training on eight A100 GPUs (author-confirmed) and inference on one A100. The model/environment sentence and hardware sentence occupy separate lines at full gallery width; ScaleWoB links to its project site. GRPO is not asserted for the Brownie checkpoint: its training recipe has not been verified. The final homepage wording was supplied by the author: both SteerDistill and On-Policy QAD W4A16 initialize from the post-trained BF16 checkpoint. This differs from the archived demo provenance, which identifies an older Qwen3-VL origin for QAD; the original records remain unchanged and do not independently establish the shared initialization. No demo data-download or source-record interface is exposed in the UI. Model identity and inference/total time share a compact header; completion status appears beside the step number.

Validation: `node --test scripts/demo-replay.test.cjs scripts/site.test.cjs scripts/concept-motion.test.cjs`. Tests compare every generated step with original records, validate highlights and timing boundaries, and check independent/shared seeking. Browser acceptance covers four-task switching, retained clocks and method selections, paused background playback, unique IDs, swipe markers, direct links, rapid switching, keyboard navigation, dark theme and narrow layouts. The WPS baseline additionally covers magnification and playback controls at 1366/1024/768/390px widths.

The hero uses Libre’s real 700 variable-font weight through a home-only font alias, an italic Source Serif paper title and a tinted TL;DR panel. The method link lives in the TL;DR. The compact SVG uses 48px decision slots on a 60px grid; the guidance speech bubble spans two slots, with the paper’s prompt symbol G changing to G′ after feedback. It never reuses the red failed-decision style. The bars do not encode measured latency or action counts.

`design-lab/p2-concept.js` drives all SVG marks with one 17-second Web Animations clock. Its named tracks describe individual decision reveals, guidance, an unsuccessful local student retry, failed local verification, feedback, refined guidance, the successful local retry, acceptance and sequential distillation. Both attempts reuse one rectangle position: they do not depict a multi-turn rollout. Labels and baseline rules belong to the same timed units as their associated marks; no diagram labels stay on an otherwise empty frame. Visible terminology follows the paper: Behavioral divergence / Student retry / Local verify / Distill / Act without guidance. Arrowheads follow their connecting strokes. Completed marks hold briefly, fade together, then restart. Pause/resume, offscreen suspension and page visibility retain a common instant; reduced motion shows the complete accepted route. The controller has no independent looping CSS animations. Keep the causal ordering and `data-motion` names synchronized when changing the SVG; verify a complete cycle visually and run `node --test scripts/concept-motion.test.cjs`.

The benchmark follows directly beneath the hero; precision stays in the setting controls rather than a duplicate header label.

## Case editing and verification

The [2026-11-04 review batch](case-batch-20261104.md) adds the user-accepted R3–R5 using the existing sequence template. The [latest evidence audit](latest-cases-review-20261106.md) selected the tool-name training case and ticket-login ablation from newer data (then T2 and A6); earlier training packages remain deferred. The prior [ablation review](ablation-review-20261104.md) is historical: its A1 selection is now withdrawn. These local updates have not been published.

Read the [case author contract](../../design-lab/case-content/README.md) and [shared interfaces](../../design-lab/case-shared/README.md). Highlights remain explicit, individually reviewed spans.

```sh
node scripts/build-pages.mjs --check
node --test scripts/site.test.cjs scripts/concept-motion.test.cjs
node design-lab/case-shared/validate-case.cjs
node --test design-lab/case-shared/tests/*.cjs
python3 -m http.server 18775
```

Check root and `/SteerDistill/` hosting, five benchmark settings, scroll continuation in both directions, standalone article/deep links, theme persistence, narrow-screen contents and notes, and case/record links. Verify equal-height rails after method changes. Use local preview while reviewing new layout revisions; the published branch remains `codex/steerdistill-site`.

## Prior cleanup and retained evidence

Former layout studies, demos and temporary screenshots were archived outside the repository before removal. [The cleanup manifest](cleanup-manifest.json) records that operation. Original `data/` bytes remain available, including unselected cases. Three appendix candidates are retained as [editorial records](appendix-candidates.md).

No unpublished manuscript notes are included here. Preserve the MIT license, OxyGen notice/license and font licenses. Research decisions and the manuscript fact map are maintained in the private paper repository, separately from this public site.


## Bilingual case editorial

The 19 accepted cases and their record reader support `?lang=zh` and `?lang=en`. Chinese remains the default until a reader selects English; the header toggle saves the choice and keeps the current case, method pair, source, message, raw/readable mode and URL fragment. Sidebar and record links carry the selected language. The homepage also supports both languages; the article body remains Chinese.

Chinese case JSON remains the source of truth. English editorial overlays live in `design-lab/case-content/en/{kind}/{id}.json`; they replace explicit JSON-pointer paths after the original data is loaded. They do not translate arbitrary DOM text. `case-locale.js` owns case-specific interface labels and applies the overlays without mutating the cached Chinese data; `site/locale.js` owns the global language preference and navigation. The shared evidence, comparison, training, sequence and record components render both versions.

Translate titles, summaries, editorial explanations/results, frame labels, source display labels and UI. Keep original task turns, actual model reasoning/replies, tool calls and returns, Teacher guidance and source files verbatim. Some evidence fields also contain editor-added chronology headings or “excerpt” markers: only these annotations are translated. Their boundaries are recorded in `mixedFieldNotes`; highlights move with the same source passages. No original response is translated, corrected or paraphrased for the English view.

Each overlay has a short English `indexTitle`, a `preserved` ledger, and a `sourceSha256` tied to the reviewed Chinese case file. The build/check rejects a stale translation until it is reviewed and its source hash updated. Build the English catalogue with `python3 scripts/build-case-locales.py`; `--check` verifies it is current. Regenerate shared HTML with `node scripts/build-pages.mjs` after shell changes. When changing accepted Chinese editorial content, review the corresponding overlay; invalid paths fail visibly rather than falling back to a partially translated case.

Checks: `node --test scripts/case-locales.test.cjs design-lab/case-shared/tests/*.cjs scripts/site.test.cjs`. The locale tests compare source payloads, metadata, action names/arguments, guidance and annotated excerpts, validate all English highlights, and confirm numbering/routes remain unchanged. Browser review covers all 19 English cases and all 68 comparison-method selections, language toggling with selected methods and raw source state retained, Chinese regression, source downloads, desktop/narrow layouts and the record reader. English uses the existing layout; only the requested language toggle is new.


### Task scope and header review

All 19 case pages now use an explicit `taskTurns` selection, shared by both languages. Complete requests stay in `originalTask` and the raw record files. Scope decisions are recorded in the [author contract](../../design-lab/case-content/README.md#task-disclosure-scope); only unrelated user turns are hidden on the focused page. T1 now shows only the request to read the file. T5 shows the support-ticket request; I7 keeps the removal, clarification and list-check turns. T2 keeps the earlier requests needed to interpret its output filename and target sentence.

Frame headers use one content-type/context interface across action comparisons, reasoning, guidance and verification. The same type, weight, padding and paper-colored header apply in both languages; red/blue continues to encode evidence meaning in the top rule and content. Paired header rows align even when translated context wraps. No raw call, reply, guidance, task message or result was rewritten.

Checks include `scripts/case-task-scope.test.cjs`, the bilingual fidelity suite and browser inspection of both locales for all 19 cases, including paired-header alignment and narrow-screen layout.


## Site language and homepage translation

All four maintained entry points load `site/locale.js`. The header owns a single language switch. An explicit `?lang=zh|en` takes precedence over the saved `steerdistill-language` preference; the older case-only preference is accepted on migration. With no preference, the homepage starts in English and the article/case entries in Chinese. Internal page links preserve the selection, including the continuous homepage-to-article transition. Record source/message/mode and case method selections survive a language change.

`site/home-locale.js` translates only explicitly selected homepage prose, replay controls, task summaries and editorial step titles. Paper identity, benchmark/method names and diagram terminology remain English. Demo thoughts, actions, screenshots and timings remain in the original data. `case-locale.js` delegates language/navigation to the shared locale and applies only the reviewed case overlays. The article surface remains `lang="zh-CN"`; changing the global language affects its shell and destination links, not the post or its embedded cases.

Run `node --test scripts/site-locales.test.cjs scripts/case-locales.test.cjs scripts/demo-replay.test.cjs` after changing localization. Rebuild the four entries with `node scripts/build-pages.mjs`. Translation coverage tests check every recorded demo step title; source-fidelity tests are separate from editorial review.


## Follow-up TODOs

- Revise and finalize the research article content. Keep the current Chinese body and embedded examples for this release; translate the article after its content is approved. This is deliberately deferred, not a blocker for publishing the reviewed homepage, demos and case collection.
- Add the homepage Paper / arXiv link when a public manuscript URL or approved PDF is available.
