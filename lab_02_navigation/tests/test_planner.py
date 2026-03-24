import unittest
from pathlib import Path

from lab_02_navigation.src.models import NavigationContext
from lab_02_navigation.src.planner import run_planner


class TestPlanner(unittest.TestCase):
    def test_reaches_goal(self) -> None:
        context = NavigationContext(
            map_file_path=Path("lab_02_navigation/models/map.json"),
            step_size=1.0,
            max_steps=30,
            seed=1,
            start=(0.0, 0.0),
            goal=(3.0, 4.0),
        )
        summary = run_planner(context, collect_path=True)
        self.assertEqual(summary["status"], "success")
        self.assertEqual(summary["final_position"], (3.0, 4.0))
        self.assertGreater(len(summary["waypoints"]), 0)


if __name__ == "__main__":
    unittest.main()
