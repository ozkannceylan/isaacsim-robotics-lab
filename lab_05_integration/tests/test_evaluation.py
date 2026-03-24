import unittest
from pathlib import Path

from lab_05_integration.src.evaluation import build_mission_summary, evaluate_subsystems
from lab_05_integration.src.models import IntegrationContext, ThresholdConfig


class TestEvaluation(unittest.TestCase):
    def test_evaluate_subsystems(self) -> None:
        context = IntegrationContext(
            seed=0,
            scoreboard_output_path=Path('lab_05_integration/data/subsystem_scoreboard.csv'),
            manifest_path=Path('lab_05_integration/models/integration_manifest.json'),
            mission_name='test_mission',
            lab_01_config_path=Path('lab_01_foundations/configs/default.json'),
            lab_02_config_path=Path('lab_02_navigation/configs/default.json'),
            lab_03_config_path=Path('lab_03_perception/configs/default.json'),
            thresholds=ThresholdConfig(
                max_foundation_energy=50.0,
                max_navigation_steps=10,
                min_perception_mean_intensity=0.4,
                min_overall_score=0.8,
            ),
        )
        metrics = {
            'lab_01_foundations': {'status': 'success', 'energy_used': 25.0, 'steps_executed': 100},
            'lab_02_navigation': {'status': 'success', 'steps_executed': 5, 'path_length': 5.0},
            'lab_03_perception': {'status': 'success', 'num_frames': 20, 'avg_mean_intensity': 0.5},
        }

        subsystems = evaluate_subsystems(context, metrics)
        summary = build_mission_summary(context, subsystems)

        self.assertEqual(len(subsystems), 3)
        self.assertEqual(summary['status'], 'success')
        self.assertGreaterEqual(summary['overall_score'], 0.8)


if __name__ == '__main__':
    unittest.main()
