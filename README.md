# SteerDistill website

Research website for **SteerDistill: Quantizing LLM Agents via Closed-Loop Teacher Steering**.

[Website](https://xxxxyu.github.io/SteerDistill/) · [Project code](https://github.com/xxxxyu/SteerDistill)

This checkout serves the website only. It includes the bilingual homepage,
four interactive GUI task replays, the Chinese research article, and 19
reviewed bilingual cases: 5 training corrections/guidance comparisons, 9
inference comparisons, and 5 autonomous recoveries. Each case links to its
sanitized source records and a self-contained ZIP download.

## Preview and maintain

Use Node.js 20+ and Python 3.10+. No package installation or framework server is needed.

```bash
node scripts/build-pages.mjs
python3 -m http.server 18775
```

Open [the local preview](http://localhost:18775/). The four maintained entry points are:

- `index.html?lang=en` / `index.html?lang=zh`: homepage, results, and GUI replays.
- `article.html`: Chinese article, also reached by scrolling below the homepage.
- `design-lab/paper-cases.html?lang=en` / `?lang=zh`: full case collection.
- `design-lab/case-records.html`: source reader linked from each case.

The current development branch is `codex/case-expansion-20261104`. GitHub Pages
can serve this checkout's root under `/SteerDistill/`; hosting needs no build
server. The former `design-lab/p2.html` URL redirects to the homepage.

Run `python3 scripts/check-release.py` before publication. See
[maintenance](docs/maintenance.md) for the source map, build commands, and
verification scope, and [case evidence](data/case-library/README.md) for the
sanitization policy. All assets required by the pages are in this checkout.
Unselected experiments and candidate case banks are excluded.

Paper and checkpoint URLs will be added when available.

Code is distributed under the [MIT license](LICENSE). Layout references and
font licenses are listed in [third-party notices](THIRD-PARTY-NOTICES.txt).
