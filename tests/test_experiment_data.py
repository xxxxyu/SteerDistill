"""CPU-only checks for the organized experiment data."""
import csv
import json
import hashlib
import math
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1] / "results"
METHODS = {"BF16", "Ours", "GPTQ", "EfficientQAT", "BitDistiller", "On-Policy QAD", "QeRL"}


def rows(name):
    with (ROOT / "data" / name).open(newline="") as stream:
        return list(csv.DictReader(stream))


class ExperimentDataTest(unittest.TestCase):
    def test_manifest_dimensions_and_finite_values(self):
        manifest = json.loads((ROOT / "manifest.json").read_text())
        for name, expected in manifest["sha256"].items():
            self.assertEqual(hashlib.sha256((ROOT / "data" / name).read_bytes()).hexdigest(), expected, name)
        for name, specification in {**manifest["tables"], **manifest["figures"]}.items():
            data = rows(name)
            self.assertEqual(len(data), specification["rows"], name)
            for row in data:
                self.assertNotIn(None, row)
                for value in row.values():
                    try:
                        number = float(value)
                    except ValueError:
                        continue
                    self.assertTrue(math.isfinite(number), name)

    def test_benchmark_coverage_and_averages(self):
        data = rows("benchmark_results.csv")
        keys = {(r["model"], r["precision"], r["method"]) for r in data}
        self.assertEqual(len(keys), 33)
        for model in ("Qwen3-8B", "Qwen3.5-4B", "Gemma 4 12B-it"):
            self.assertEqual({r["method"] for r in data if r["model"] == model and r["precision"] in ("BF16", "W4A16")}, METHODS)
        for row in data:
            values = [float(row[k]) for k in ("bfcl_v4", "tau2_bench", "webshop", "alfworld", "search_qa")]
            self.assertTrue(all(0 <= value <= 100 for value in values))
            self.assertLessEqual(abs(sum(values)/5 - float(row["average"])), .0051)

    def test_training_curves_and_bands(self):
        data = rows("training_efficiency.csv")
        for method in ("On-Policy QAD", "QeRL", "Ours"):
            selected = [r for r in data if r["method"] == method]
            hours = [int(r["gpu_hours"]) for r in selected]
            self.assertEqual(hours, [0, 8, 16, 24, 32, 40, 48, 64, 80, 96, 112])
            for row in selected:
                self.assertLessEqual(float(row["lower"]), float(row["mean"]))
                self.assertLessEqual(float(row["mean"]), float(row["upper"]))
                self.assertAlmostEqual(float(row["lower"])+float(row["upper"]), 2*float(row["mean"]), places=3)

    def test_scatter_dimensions(self):
        scatter = rows("inference_efficiency.csv")
        for precision in ("W4A16", "W2A16", "W4A8"):
            selected = [r for r in scatter if r["precision"] == precision]
            self.assertEqual({r["method"] for r in selected}, METHODS)
            self.assertEqual(len(selected), 7)
            self.assertTrue(all(float(r["output_tokens"]) > 0 and 0 <= float(r["pass_at_1"]) <= 100 for r in selected))


if __name__ == "__main__":
    unittest.main()
