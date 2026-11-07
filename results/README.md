# Numerical results

Seven CSV files contain the paper's numerical summaries; `manifest.json`
records their hashes and dimensions.

## Files

| Input | Contents |
| --- | --- |
| `data/benchmark_results.csv` | Main table: 33 model / precision / method rows; five metrics and their mean |
| `data/ablations.csv` | BFCL V4 ablations (Q1–Q5), including category scores |
| `data/training_settings.csv` | Current paper's epochs, learning rate and complete-trajectory batch size |
| `data/additional_metrics.csv` | tau2 Pass@4, WebShop Task Score, and seven Search QA datasets |
| `data/inference_statistics.csv` | Tokens, steps and tool calls, averaged over each method's successful tasks |
| `data/training_efficiency.csv` | Displayed GPU-hour curves and uncertainty bands |
| `data/inference_efficiency.csv` | Displayed token / Pass@1 coordinates for Qwen3-8B |

## Units

Tabular values are checked against manuscript revision `6cda9cd` (2026-11-07).
Scores are percentages. Token counts convert the paper's K units to thousands.
`Ours` is SteerDistill; labels in CSVs are identifiers retained for plotting.

## Provenance

The efficiency CSVs were decoded from vector coordinates in the October 16
paper snapshot (SHA-256 `0105ebb9e4df6877c7d97cebade0d4f584ea8dd999c499ec4a1f602482e502bf`).
Their decimal places reflect coordinate-decoding precision. They summarize
plotted results across evaluations. Training bands are the displayed mean
plus/minus one standard deviation across four evaluations per checkpoint.
The source snapshot's additional-efficiency caption said Pass@4 while its
axis said Pass@1; these coordinates follow the axis and the current manuscript.

## Plot and validate

See [figure generation](../docs/figures.md). `manifest.json` records file hashes
and expected dimensions; the local data tests verify these without a GPU.
