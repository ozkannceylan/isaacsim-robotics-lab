import unittest

from lab_07_finalization.src.config_loader import ConfigError, load_config, validate_config


class TestConfigLoader(unittest.TestCase):
    def test_load_default_config(self) -> None:
        config = load_config('lab_07_finalization/configs/default.json')
        self.assertEqual(config.run.seed, 23)
        self.assertEqual(config.thresholds.minimum_final_score, 0.85)

    def test_invalid_thresholds_raise(self) -> None:
        with self.assertRaises(ConfigError):
            validate_config(
                {
                    'run': {'seed': 0, 'audit_name': 'audit.csv'},
                    'thresholds': {
                        'minimum_final_score': 1.1,
                        'minimum_repo_completeness': 1.0,
                    },
                    'inputs': {
                        'release_manifest': 'release.json',
                        'lab_06_config': 'lab6.json',
                    },
                }
            )


if __name__ == '__main__':
    unittest.main()
