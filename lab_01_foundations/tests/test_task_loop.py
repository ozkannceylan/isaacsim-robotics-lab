import unittest
from pathlib import Path

from lab_01_foundations.src.models import SimulationContext
from lab_01_foundations.src.task_loop import run_task_loop


class TestTaskLoop(unittest.TestCase):
    def test_run_task_loop_returns_expected_fields(self) -> None:
        context = SimulationContext(
            robot_model_path=Path("lab_01_foundations/models/robot.usd"),
            environment_model_path=Path("lab_01_foundations/models/environment.usd"),
            max_steps=10,
            time_step=0.1,
            seed=1,
        )
        summary = run_task_loop(context)
        self.assertEqual(summary["status"], "success")
        self.assertEqual(summary["steps_executed"], 10)
        self.assertEqual(summary["simulated_time"], 1.0)
        self.assertEqual(summary["seed"], 1)

    def test_trajectory_collection(self) -> None:
        context = SimulationContext(
            robot_model_path=Path("lab_01_foundations/models/robot.usd"),
            environment_model_path=Path("lab_01_foundations/models/environment.usd"),
            max_steps=5,
            time_step=0.1,
            seed=2,
        )
        summary = run_task_loop(context, collect_trajectory=True)
        self.assertEqual(len(summary["trajectory"]), 5)


if __name__ == "__main__":
    unittest.main()
