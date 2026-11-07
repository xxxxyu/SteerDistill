# Figure generation

All inputs are included in [`results/`](../results/README.md). From this checkout:

```bash
python -m pip install -r requirements/figures.txt
python scripts/figures/plot_results.py --data results/data --output /tmp/steerdistill-figures
```

This produces seven PDF/PNG figure pairs, a model-comparison SVG, chart JSON,
and a manifest recording input hashes and the Matplotlib version. These plots
are alternate renderings of the paper's numerical summaries. They do not
regenerate individual training runs, seed outcomes, or exact paper layouts.

```bash
python -B -m unittest discover -s tests -p test_experiment_data.py -v
```

The data checks run against this checkout and require no model or GPU. Result
tables use the paper's displayed precision; efficiency coordinates are decoded
plot summaries. See [results provenance](../results/README.md) before interpreting
their extra decimal places. Keep generated figures outside the source tree.
