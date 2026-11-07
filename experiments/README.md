# Website chart inputs

This directory contains only the two numerical files used by the homepage:

- [benchmark_results.csv](data/benchmark_results.csv): the paper's 33 model/precision/method rows, also offered as a download.
- [results-chart.json](data/results-chart.json): the W4A16/BF16 chart projection.

Scores are percentages. The average is the unweighted mean of the five
benchmark scores. `Ours` is SteerDistill. These are displayed paper summaries,
not raw runs or per-seed outcomes. The website needs no plotting or training
code to read them.
