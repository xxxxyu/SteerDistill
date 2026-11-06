# SteerDistill

Research website for **SteerDistill: Quantizing LLM Agents via Closed-Loop Teacher Steering**.

- Website: https://xxxxyu.github.io/SteerDistill/
- English project homepage: `index.html`
- Chinese research article: `article.html`
- Full cases: `design-lab/paper-cases.html`
- Raw-record reader: `design-lab/case-records.html`

This is a static site with local fonts. A small Node script generates the four entry pages from shared templates; hosting needs no build server. To preview:

```sh
node scripts/build-pages.mjs
python3 -m http.server 18775
```

Open `http://localhost:18775/`. The release source branch is `codex/steerdistill-site` in `xxxxyu/SteerDistill`; GitHub Pages publishes the repository root. Links and data requests also support the `/SteerDistill/` project prefix; the former `design-lab/p2.html` entry redirects to the homepage.

The collection currently includes 19 reviewed cases: 5 training corrections (including guidance comparisons), 9 inference comparisons, and 5 autonomous recoveries. The research article presents four concise examples; full case pages retain method comparisons, reasoning, guidance, and links to original records. Archived raw data is preserved for future case review and expansion.

See [site maintenance](docs/site-maintenance/README.md) for the source map, validation, and editorial interfaces. This repository contains the website only. Training and evaluation implementation is maintained in [ustccuigm/bitdistill](https://github.com/ustccuigm/bitdistill).

Code is distributed under the [MIT license](LICENSE). Visual reference and font licenses are listed in [third-party notices](THIRD-PARTY-NOTICES.txt).

Published case sources, hashes, and per-case downloads are indexed in [the case library](data/case-library/README.md). Run `python3 scripts/case-library.py --check` to verify the source inventory and archives.
