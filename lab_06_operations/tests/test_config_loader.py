import unittest

from lab_06_operations.src.config_loader import ConfigError, load_config, validate_config


class TestConfigLoader(unittest.TestCase):
    def test_load_default_config(self) -> None:
        config = load_config('lab_06_operations/configs/default.json')
        self.assertEqual(config.run.seed, 19)
        self.assertEqual(config.thresholds.maximum_open_risk, 1)

    def test_invalid_thresholds_raise(self) -> None:
        with self.assertRaises(ConfigError):
            validate_config(
                {
                    'run': {'seed': 0, 'checklist_name': 'ops.csv'},
                    'thresholds': {
                        'minimum_release_score': 1.5,
                        'maximum_open_risk': 1,
                        'require_success_status': True,
                    },
                    'inputs': {
                        'operations_manifest': 'manifest.json',
                        'lab_05_config': 'lab5.json',
                    },
                }
            )


if __name__ == '__main__':
    unittest.main()
