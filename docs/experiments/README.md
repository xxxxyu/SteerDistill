# Paper results

The included [numerical results](../../results/README.md) cover main scores,
ablations, training settings, additional metrics, trajectory statistics, and
efficiency curves.

## Metrics

The main average is the unweighted mean of BFCL V4 Overall, tau2-Bench Pass@1,
WebShop SR, ALFWorld SR, and Search QA's seven-dataset mean EM. Scores are
percentages. W4A16 covers all three models; W2A16 and W4A8 cover Qwen3-8B.

The training-efficiency comparison uses Qwen3-8B on tau2-Bench: SteerDistill
reaches 31.68% at 32 GPUh, versus QeRL's 29.84% at 96 GPUh. This is the
67% GPU-hour reduction reported in the paper.

## Inspect and plot

Run from the repository root:

```bash
python -m pip install -r requirements/figures.txt
python scripts/figures/plot_results.py --data results/data --output /tmp/steerdistill-figures
```

The efficiency files record displayed means, uncertainty bands, and marker
coordinates. Training bands show the standard deviation across four evaluations
per checkpoint. See [numerical provenance](../../results/README.md#provenance)
for units and extraction details.

## Reproduce the runs

Follow [training](../training/README.md) and [evaluation](../evaluation/README.md)
with the matching post-RL checkpoints, task data, external revisions, and
benchmark settings. Choose the matching model and task group in
[checkpoint setup](../benchmarks.md#checkpoints).
