# Figure generation

Plot the paper's numerical summaries using the inputs in
[`results/`](../results/README.md). Run commands from the repository root.

## Generate figures

```bash
python -m pip install -r requirements/figures.txt
python scripts/figures/plot_results.py --data results/data --output /tmp/steerdistill-figures
```

The command creates seven PDF/PNG figure pairs, a model-comparison SVG, chart
JSON, and a manifest recording input hashes and the Matplotlib version.
The plots use layouts suited to inspecting the included data.

## Check inputs

```bash
python -B -m unittest discover -s tests -p test_experiment_data.py -v
```

These CPU checks cover dimensions, hashes, averages, and numeric bounds.
Tables retain the paper's displayed precision; efficiency coordinates are
decoded plot summaries. See [provenance](../results/README.md#provenance)
for their measurement scope. Write generated figures outside the source tree.
