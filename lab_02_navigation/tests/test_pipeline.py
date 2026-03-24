import json
import tempfile
import unittest
from pathlib import Path

from lab_02_navigation.src.config_loader import load_config
from lab_02_navigation.src.logging_utils import write_path_csv, write_summary
from lab_02_navigation.src.navigation_setup import initialize_navigation
from lab_02_navigation.src.planner import run_planner


class TestPipeline(unittest.TestCase):
    def test_end_to_end(self) -> None:
        cfg = load_config("lab_02_navigation/configs/dev.json")
        ctx = initialize_navigation(cfg, Path.cwd())
        summary = run_planner(ctx, collect_path=True)

        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            summary_path = write_summary(summary, tmpdir / "summary.json")
            path_path = write_path_csv(summary, tmpdir / "path.csv")

            data = json.loads(summary_path.read_text(encoding="utf-8"))
            self.assertIn(data["status"], {"success", "incomplete"})
            self.assertTrue(path_path.exists())


if __name__ == "__main__":
    unittest.main()
