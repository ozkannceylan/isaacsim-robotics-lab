import unittest

from lab_01_foundations.src.config_loader import ConfigError, load_config, validate_config
from lab_01_foundations.src.models import LabConfig


class TestConfigLoader(unittest.TestCase):
    def test_load_default_config_success(self) -> None:
        config = load_config("lab_01_foundations/configs/default.json")
        self.assertIsInstance(config, LabConfig)
        self.assertEqual(config.run.max_steps, 100)
        self.assertEqual(config.run.seed, 42)

    def test_missing_config_raises(self) -> None:
        with self.assertRaises(ConfigError):
            load_config("lab_01_foundations/configs/does_not_exist.json")

    def test_invalid_max_steps_raises(self) -> None:
        with self.assertRaises(ConfigError):
            validate_config(
                {
                    "run": {"max_steps": 0},
                    "simulation": {"time_step": 0.01},
                    "models": {
                        "robot": "lab_01_foundations/models/robot.usd",
                        "environment": "lab_01_foundations/models/environment.usd",
                    },
                }
            )


if __name__ == "__main__":
    unittest.main()
