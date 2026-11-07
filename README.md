# SteerDistill

**Quantizing LLM Agents via Closed-Loop Teacher Steering**

[Website and cases](https://xxxxyu.github.io/SteerDistill/) · [Quickstart](#quickstart-qwen3-8b-on-bfcl-v4) · [Training](docs/training/README.md) · [Evaluation](docs/evaluation/README.md) · [For agents](#for-agents)

Low-bit agents can overlook task requirements and environment conditions even
when their responses look plausible. SteerDistill constructs corrections in
the student's own failure contexts, then teaches the student to use them:

1. **Revise with closed-loop teacher steering.** Restore the pre-error state,
   let the frozen student retry with teacher guidance, and use execution
   feedback to refine that guidance until the correction passes local verification.
2. **Internalize without guidance.** Train the learner without steering prompts:
   match the steered student at corrected turns and the BF16 teacher elsewhere.

The trained quantized student acts independently at inference time. Accepted
local corrections remain useful for training even when the task is not solved.

## Main results

Five-benchmark average scores from the paper (percent; higher is better):

| Model | BF16 | Strongest quantized baseline (QeRL, W4A16) | SteerDistill W4A16 |
| --- | ---: | ---: | ---: |
| Qwen3-8B | 53.54 | 51.00 | **53.18** |
| Qwen3.5-4B | 61.68 | 59.24 | **60.95** |
| Gemma 4 12B-it | 65.13 | 62.64 | **64.31** |

SteerDistill improves on the strongest W4A16 baseline by 1.67–2.18 points
and stays within one point of BF16. On Qwen3-8B / tau2-Bench, the paper's
intermediate-checkpoint comparison achieves a 1.84-point higher success rate
than QeRL using 67% fewer training GPU hours (32 vs. 96 GPUh).
See the [full results and evidence scope](docs/experiments/README.md).

This repository starts from benchmark-specific, post-RL BF16 checkpoints and
provides data preparation, clipping calibration, quantized model export,
online distillation, and benchmark evaluation. Supply your own post-RL
checkpoints; model weights and benchmark data are downloaded separately.
**Checkpoint downloads are planned; links will be added for the public release.**
Until then, running the method requires your own compatible post-RL checkpoints.
The repository covers the low-bit stage; it does not include the preceding
GRPO training or implementations of all comparison baselines.

## Models and benchmarks

**Models and training guides:**

- [Qwen3-8B](docs/training/README.md#qwen3-8b)
- [Qwen3.5-4B](docs/training/README.md#qwen35-4b)
- [Gemma 4 12B-it](docs/training/README.md#gemma-4-12b-it)

**Benchmarks:** BFCL V4, tau2-Bench, WebShop, ALFWorld, and Search QA.

W4A16 is the paper's setting for all three models. Qwen3-8B additionally has
W2A16 and W4A8 results; the additional runtime's numerical and performance
scope is explained in the [precision guide](docs/training/precision.md).

All model families use the shared quantization and training pipeline. For each
model, BFCL V4 and tau2-Bench share one post-RL checkpoint and training run;
the other benchmarks use separate checkpoints. See [benchmark setup](docs/benchmarks.md)
for model keys, downloads, data formats, and evaluation protocols.

## Requirements

- Linux, Bash, and NVIDIA GPUs; the default distributed training setup uses
  eight A100 80GB GPUs.
- Python 3.10 for training; separate inference and benchmark environments.
  The external tool-use adapter uses Python 3.12.
- The training dependencies in [requirements/training.lock](requirements/training.lock).
- A vLLM build supporting the selected model architecture and quantized kernels.

The environment versions, CUDA toolkit configuration, and external source
revisions are listed in [reproducibility.md](docs/reproducibility.md).

## Getting started

### Install the training package

```bash
git clone https://github.com/xxxxyu/SteerDistill.git
cd SteerDistill

python3.10 -m venv .venv
.venv/bin/python -m pip install torch==2.7.1 --index-url https://download.pytorch.org/whl/cu126
.venv/bin/python -m pip install -r requirements/training.lock
.venv/bin/python -m pip install --no-deps -e .
```

Prepare the inference, benchmark, and tool-adapter environments using
[the environment guide](docs/reproducibility.md), then configure their paths.

### Configure once

```bash
cp configs/local.example.env configs/local.env
chmod 600 configs/local.env
```

Set environment, checkpoint, data, GPU, and private API settings in
`configs/local.env`. Launchers load this Git-ignored file automatically;
no manual `export` is required. The default route is Qwen3-8B with BFCL V4.
See [local configuration](docs/benchmarks.md#local-configuration) for overrides
and [checkpoint paths](docs/benchmarks.md#checkpoints) for each model.

### Check prerequisites

```bash
bash scripts/validate/preflight.sh
```

### Quickstart: Qwen3-8B on BFCL V4

After installation, prepare the [tool-use training inputs](docs/benchmarks.md#tool-use-training)
and set `QWEN3_8B_TOOL_USE_MODEL` in `configs/local.env` to your post-RL BF16
checkpoint. Configure `SERPAPI_API_KEY` for BFCL web-search evaluation.
Then run the complete route:

```bash
bash scripts/run/run_benchmark.sh full --model qwen3_8b --benchmark bfcl_v4
```

This runs prerequisite checks, calibration-data preprocessing, clipping,
quantized student export, online teacher-steered training, and BFCL V4
evaluation. Evaluation uses the latest completed student checkpoint without
teacher guidance. Artifacts are written under
`$STEER_ASSET_ROOT/runs/qwen3_8b/bfcl_v4/`; see [training outputs](docs/training/README.md#outputs).

## Workflow guides

| Guide | Contents |
| --- | --- |
| [Data preparation](docs/data/README.md) | Benchmark training inputs and calibration preprocessing |
| [Quantization and training](docs/training/README.md) | Separate commands for all three models, shared tool-use training, and training outputs |
| [Evaluation](docs/evaluation/README.md) | All five benchmarks, runtime prerequisites, and checkpoint selection |
| [Experiment data and figures](docs/experiments/README.md) | Self-contained paper result tables, their provenance, and plotting commands |

## For agents

Start with [the agent guide](docs/agents.md) for the paper-to-code map,
configuration rules, expected artifacts, and a minimal run sequence. Use
[environment setup](docs/reproducibility.md) and [model/data setup](docs/benchmarks.md)
before launching a GPU job. These guides describe the supported public routes;
internal names such as `skill` refer to stored steering prompts, not an
additional retrieval system required at inference.

## Acknowledgments and license

We thank the authors of BitDistiller, the benchmark environments, and the
inference libraries used by this project. Attribution and component terms are
listed in [third-party notices](docs/third_party_notices.md).
SteerDistill is distributed under the [MIT License](LICENSE), with the retained
Apache-2.0 terms for incorporated GPTQ-triton material. Model and dataset
licenses remain with their respective providers. Citation metadata is in
[CITATION.cff](CITATION.cff); the arXiv identifier will be added when available.
