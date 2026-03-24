import unittest

from lab_05_integration.src.config_loader import ConfigError, load_config, validate_config


class TestConfigLoader(unittest.TestCase):
    def test_load_default_config(self) -> None:
        config = load_config('lab_05_integration/configs/default.json')
        self.assertEqual(config.run.seed, 11)
        self.assertEqual(config.thresholds.max_navigation_steps, 6)

    def test_invalid_thresholds_raise(self) -> None:
        with self.assertRaises(ConfigError):
            validate_config(
                {
                    'run': {'seed': 0, 'scoreboard_name': 'scores.csv'},
                    'thresholds': {
                        'max_foundation_energy': 0,
                        'max_navigation_steps': 5,
                        'min_perception_mean_intensity': 0.5,
                        'min_overall_score': 0.8,
                    },
                    'inputs': {
                        'integration_manifest': 'manifest.json',
                        'lab_01_config': 'a.json',
                        'lab_02_config': 'b.json',
                        'lab_03_config': 'c.json',
                    },
                }
            )


if __name__ == '__main__':
    unittest.main()
