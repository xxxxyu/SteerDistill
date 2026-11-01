# SteerDistill

Research website for **SteerDistill: Quantizing LLM Agents via Closed-Loop Teacher Steering**.

- Website: https://xxxxyu.github.io/SteerDistill/
- Homepage: `index.html`
- Full cases: `design-lab/paper-cases.html`
- Raw-record reader: `design-lab/case-records.html`

This is a static site with local fonts and no build step. To preview:

```sh
python3 -m http.server 18775
```

Open `http://localhost:18775/`. The release source branch is `codex/steerdistill-site` in `xxxxyu/SteerDistill`; GitHub Pages publishes the repository root. Links and data requests also support the `/SteerDistill/` project prefix; the former `design-lab/p2.html` entry redirects to the homepage.

The collection currently includes 13 reviewed cases across training, inference, recovery, and guidance ablations. The homepage presents four concise examples; full case pages retain method comparisons, reasoning, guidance, and links to original records. Archived raw data is preserved for future case review and expansion.

See [site maintenance](docs/site-maintenance/README.md) for the source map, validation, and editorial interfaces. This repository contains the website only. Training and evaluation implementation is maintained in [ustccuigm/bitdistill](https://github.com/ustccuigm/bitdistill).

Code is distributed under the [MIT license](LICENSE). Visual reference and font licenses are listed in [third-party notices](THIRD-PARTY-NOTICES.txt).
