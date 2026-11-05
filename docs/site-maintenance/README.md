# Site maintenance

This repository is a static publication tree. GitHub Pages serves the root at https://xxxxyu.github.io/SteerDistill/. The 2026-11-02 revision separates the English project landing from the Chinese research article while retaining continuous scrolling between them. All four entry pages share the navigation, theme and typography.

## Four entry pages, one shell

| Entry | Purpose | Language |
| --- | --- | --- |
| `index.html` | Paper identity, benchmark overview, TL;DR and concept animation | English |
| `article.html` | Independent research blog post, Xiangyu Li byline, contents and notes | Chinese |
| `design-lab/paper-cases.html` | Nineteen full cases (A2–A4 pending user review) | Chinese |
| `design-lab/case-records.html` | Original trajectories and record navigation | Chinese |

The navigation labels are shared and deliberately Chinese: SteerDistill / 研究文章 / 案例分析 / theme. A bilingual interface is deferred until the content is settled.

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
| Homepage task video placeholders and provenance | `demos/`, `docs/site-maintenance/demo-sources.json` |
| Original records / benchmark figures and inputs | `data/`, `experiments/` |

Run `node scripts/build-pages.mjs` after editing templates or article metadata. It generates all four HTML entry pages with one header and shared asset declarations. No framework server or package installation is required; commit generated pages together with their sources. `node scripts/build-pages.mjs --check` detects stale output. Do not edit generated HTML directly.

## Reading behavior

The homepage progressively renders the same article component below its task demonstration section. Scrolling remains entirely native: no wheel interception, artificial scroll thresholds or forced document reload. Crossing into the article updates the URL to `article.html`, the title and active navigation using `replaceState`; scrolling back restores the homepage address. Passive scrolling does not create history entries. Explicit links retain normal browser navigation. Reloading or sharing the article URL opens the independent post without the landing page.

The article uses a symmetric 1080px grid: 172px contents, 28px gap, 680px reading column, 28px gap, 172px contextual notes. All case embeds, figures and resource links share the 680px reading measure. Below 1160px, both rails collapse together: contents becomes a disclosure and notes move to the endnote list; the reading column stays centered. The post ends with its resource links, without a duplicated site footer. Each footnote is authored once alongside its paragraph and rendered consistently in either view. Six short section labels come from the same chapter data as the headings.

Article metadata uses `post.title` for the document title and optional `post.titleLines` for intentional heading line breaks. `post.author`, `post.date`, `post.intro` belong to the blog, not the paper author block. A paragraph can provide `note: { id, text }`; the renderer generates stable references, notes and return links. Chapter `id` values remain stable for external links.

Old `design-lab/p2.html` links still redirect to the root. Homepage links with existing article section hashes redirect to the independent post. All assets resolve through `SitePaths.url()` and support the GitHub project prefix. Raw task paths are never rewritten.

## Homepage demonstrations

The two temporary videos are restored byte-for-byte from `ustccuigm/bitdistill` gh-pages, not new benchmark evidence. They show the task-adapted SteerDistill checkpoint on BestBuy tasks 47 and 52. The original comparison used different training budgets; do not turn these placeholders into a benchmark claim. The source commit, original paths and blob hashes are recorded in `demo-sources.json`. Replace the video sources, posters, accessible names and task captions together in `site/templates/home.html` when the final demos are ready. The player uses native controls and `preload="none"`, without autoplay.

The hero uses Libre’s real 700 variable-font weight through a home-only font alias, an italic Source Serif paper title and a tinted TL;DR panel. The method link lives in the TL;DR. The compact SVG uses 48px decision slots on a 60px grid; the guidance speech bubble spans two slots, with the paper’s prompt symbol G changing to G′ after feedback. It never reuses the red failed-decision style. The bars do not encode measured latency or action counts.

`design-lab/p2-concept.js` drives all SVG marks with one 17-second Web Animations clock. Its named tracks describe individual decision reveals, guidance, an unsuccessful local student retry, failed local verification, feedback, refined guidance, the successful local retry, acceptance and sequential distillation. Both attempts reuse one rectangle position: they do not depict a multi-turn rollout. Labels and baseline rules belong to the same timed units as their associated marks; no diagram labels stay on an otherwise empty frame. Visible terminology follows the paper: Behavioral divergence / Student retry / Local verify / Distill / Act without guidance. Arrowheads follow their connecting strokes. Completed marks hold briefly, fade together, then restart. Pause/resume, offscreen suspension and page visibility retain a common instant; reduced motion shows the complete accepted route. The controller has no independent looping CSS animations. Keep the causal ordering and `data-motion` names synchronized when changing the SVG; verify a complete cycle visually and run `node --test scripts/concept-motion.test.cjs`.

The benchmark follows directly beneath the hero; precision stays in the setting controls rather than a duplicate header label.

## Case editing and verification

The [2026-11-04 review batch](case-batch-20261104.md) adds R3–R5 using the existing sequence template; the user has accepted all three and confirmed deferral of the ten training packages. The public release has not yet been updated. The subsequent [ablation review](ablation-review-20261104.md) defers upstream 01/03 and updates A1 (upstream 02) with attributed guidance-generation analysis; that update awaits user review.

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
