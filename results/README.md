# Numerical results

This directory is self-contained: seven CSV inputs and a hash manifest.
It contains paper summaries, not training datasets or raw trajectories.

| Input | Contents |
| --- | --- |
| `data/benchmark_results.csv` | Main table: 33 model / precision / method rows; five metrics and their mean |
| `data/ablations.csv` | BFCL V4 ablations (Q1–Q5), including category scores |
| `data/training_settings.csv` | Current paper's epochs, learning rate and complete-trajectory batch size |
| `data/additional_metrics.csv` | tau2 Pass@4, WebShop Task Score, and seven Search QA datasets |
| `data/inference_statistics.csv` | Tokens, steps and tool calls, averaged over each method's successful tasks |
| `data/training_efficiency.csv` | Displayed GPU-hour curves and uncertainty bands |
| `data/inference_efficiency.csv` | Displayed token / Pass@1 coordinates for Qwen3-8B |

Tabular values are checked against manuscript revision `6cda9cd` (2026-11-07).
Scores are percentages. Token counts convert the paper's K units to thousands.
`Ours` is SteerDistill; labels in CSVs are identifiers retained for plotting.

The efficiency CSVs were decoded from vector coordinates in the October 16
paper snapshot (SHA-256 `0105ebb9e4df6877c7d97cebade0d4f584ea8dd999c499ec4a1f602482e502bf`).
Their decimal places describe the decoding, not additional measurement
precision. They contain plotted summaries; individual seeds and evaluation
runs cannot be recovered from them. Training bands are the displayed mean
plus/minus one standard deviation across four evaluations per checkpoint.
The source snapshot's additional-efficiency caption said Pass@4 while its
axis said Pass@1; these coordinates follow the axis and the current manuscript.

The removed reasoning-prefix experiment and historical candidate case bank are
outside the current paper's result set. The old PDF coordinate extractor was
specific to that snapshot's layout and is not a release tool.

See [figure generation](../docs/figures.md). `manifest.json` records file hashes
and expected dimensions; the local data tests verify these without a GPU.
