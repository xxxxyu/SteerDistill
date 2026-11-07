# Paper results

[Project overview](../../README.md) · [Numerical inputs](../../results/README.md)

This checkout includes the paper's main scores, ablations, training settings,
additional metrics, trajectory statistics, and displayed efficiency coordinates.
They can be inspected and plotted without fetching another branch:

```bash
python -m pip install -r requirements/figures.txt
python scripts/figures/plot_results.py --data results/data --output /tmp/steerdistill-figures
```

The headline average is the unweighted mean of BFCL V4 Overall, tau2-Bench
Pass@1, WebShop SR, ALFWorld SR, and Search QA's seven-dataset mean EM.
All scores are percentages. W4A16 covers the three models; W2A16 and W4A8
cover Qwen3-8B. The 67% GPU-hour reduction compares a 32-GPUh SteerDistill
checkpoint with QeRL at 96 GPUh on Qwen3-8B / tau2-Bench; it does not imply
that every final score is obtained at 32 GPUh.

The efficiency files contain displayed means, bands, and marker coordinates,
not per-seed or per-task runs. The training bands represent four evaluations
per checkpoint. Raw benchmark datasets, checkpoints, and unpublished experiment
archives are not bundled. The website presents selected qualitative cases;
those examples do not estimate benchmark success rates.

To run the method, follow [training](../training/README.md) and
[evaluation](../evaluation/README.md). Exact score reproduction also requires
the matching post-RL checkpoints, data, external revisions, and evaluation
settings. Checkpoint download links are pending the public release.
