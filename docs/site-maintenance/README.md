# Site maintenance

The repository root is the static publication tree for https://xxxxyu.github.io/SteerDistill/.

## Source map

| Purpose | Maintained source |
| --- | --- |
| Homepage and accepted hero | `index.html` |
| Chinese article and hero labels | `design-lab/main-article.zh.json` |
| Article composition | `design-lab/main-article.js` and `.css` |
| Four inline cases | `design-lab/article-content/cases.zh.json` |
| Full cases and registry | `design-lab/case-content/` |
| Case reader and raw record reader | `design-lab/paper-cases.html`, `design-lab/case-records.html` |
| Shared evidence, layout, sidebar, URL handling | `design-lab/case-shared/` |
| Original records and expansion pool | `data/` |
| Benchmark chart inputs and figures | `experiments/` |

The accepted presentation uses a 1080px page, 710px article text, and 850px inline evidence. Inline method rails share title/body heights across all methods; scrolling does not move following prose. Detailed reasoning and original guidance stay in the full case pages. Keep article excerpts concise rather than reproducing the complete case interface.

## Editing and verification

Read the [case author contract](../../design-lab/case-content/README.md) and [shared interfaces](../../design-lab/case-shared/README.md). Review each method, action, and reasoning excerpt against original records. Highlights are explicit, individually reviewed spans; the renderer does not choose them. Add case-specific editorial ledgers under `cases/<kind>/` when extending the collection.

Run from the repository root:

```sh
node design-lab/case-shared/validate-case.cjs
node --test design-lab/case-shared/tests/*.cjs
python3 -m http.server 18775
```

Check desktop and narrow screens, light/dark themes, all five benchmark settings, method navigation, original-record links, and browser Back/Forward. With inline rails, check following-section document coordinates before/after changing methods. Check both root hosting and a `/SteerDistill/` URL prefix.

Resource URLs in presentation JSON are site-relative, without a leading slash. `SitePaths.url()` resolves them from the shared script location, preserving GitHub Pages project prefixes. Do not apply URL rewriting to raw task content or filesystem paths. Keep local font names stable for browser caching; bump script/style query versions when shipping changes.

## Publication cleanup

The accepted Chinese homepage is the root entry. `design-lab/p2.html` redirects while preserving its query/hash. Former layout studies, candidate preview pages, demos, and temporary screenshots were removed after a complete external archive was made. [The cleanup manifest](cleanup-manifest.json) records that operation. All original `data/` bytes remain available, including unselected cases for later review. The three appendix candidates are retained as [editorial records](appendix-candidates.md), not separate public trial interfaces.

The original local archive is external to this repository; its portable location hint appears in the manifest. No unpublished manuscript notes are included in this publication tree. Preserve the root MIT license, OxyGen notice/license, and font licenses when distributing the site.
