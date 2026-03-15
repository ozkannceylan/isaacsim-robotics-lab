import json
import tempfile
import unittest
from csv import DictReader
from pathlib import Path

from lab_01_foundations.src.foundations_standalone import main


class TestPipeline(unittest.TestCase):
    def test_mock_runtime_writes_expected_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            exit_code = main(
                [
                    "--mock-runtime",
                    "--config",
                    "lab_01_foundations/configs/mock.yaml",
                    "--output-dir",
                    str(tmpdir),
                ]
            )
            self.assertEqual(exit_code, 0)

            summary_path = tmpdir / "run_summary.json"
            csv_path = tmpdir / "joint_states.csv"
            frames = sorted((tmpdir / "frames").glob("*.png"))
            data = json.loads(summary_path.read_text(encoding="utf-8"))
            self.assertEqual(data["status"], "success")
            self.assertEqual(data["runtime_name"], "mock")
            self.assertEqual(data["step_count"], 30)
            self.assertEqual(data["captured_frame_count"], 3)
            self.assertEqual(len(frames), 3)
            self.assertEqual(frames[0].read_bytes()[:8], b"\x89PNG\r\n\x1a\n")

            with csv_path.open("r", encoding="utf-8", newline="") as handle:
                rows = list(DictReader(handle))
            self.assertEqual(len(rows), 30)


if __name__ == "__main__":
    unittest.main()
