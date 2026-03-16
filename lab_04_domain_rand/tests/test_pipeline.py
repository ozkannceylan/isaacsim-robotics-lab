import json
import tempfile
import unittest
from csv import DictReader
from pathlib import Path

from lab_04_domain_rand.main import main


class TestPipeline(unittest.TestCase):
    def test_end_to_end_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            exit_code = main(
                [
                    "--config",
                    "lab_04_domain_rand/configs/local.yaml",
                    "--eval-config-dir",
                    "lab_04_domain_rand/eval/eval_configs",
                    "--output-dir",
                    str(tmpdir),
                ]
            )
            self.assertEqual(exit_code, 0)

            summary = json.loads((tmpdir / "summary.json").read_text(encoding="utf-8"))
            with (tmpdir / "evaluation_results.csv").open("r", encoding="utf-8", newline="") as handle:
                rows = list(DictReader(handle))

            self.assertEqual(summary["status"], "success")
            self.assertGreaterEqual(summary["dr_training"]["max_range_scale"], 2.0)
            self.assertEqual(len(rows), 4)
            for row in rows:
                self.assertGreater(float(row["dr_success_rate"]), float(row["vanilla_success_rate"]))


if __name__ == "__main__":
    unittest.main()
