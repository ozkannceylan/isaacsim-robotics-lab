import json
import tempfile
import unittest
from pathlib import Path

from lab_01_foundations.src.config_loader import load_config
from lab_01_foundations.src.logging_utils import write_run_summary, write_trajectory_csv
from lab_01_foundations.src.simulation_setup import initialize_simulation
from lab_01_foundations.src.task_loop import run_task_loop


class TestPipeline(unittest.TestCase):
    def test_end_to_end_outputs(self) -> None:
        config = load_config("lab_01_foundations/configs/dev.json")
        context = initialize_simulation(config, project_root=Path.cwd())
        summary = run_task_loop(context, collect_trajectory=True)

        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            summary_path = write_run_summary(summary, tmpdir / "summary.json")
            traj_path = write_trajectory_csv(summary, tmpdir / "trajectory.csv")

            data = json.loads(summary_path.read_text(encoding="utf-8"))
            self.assertEqual(data["status"], "success")
            self.assertEqual(data["steps_executed"], 25)
            self.assertTrue(traj_path.exists())


if __name__ == "__main__":
    unittest.main()
