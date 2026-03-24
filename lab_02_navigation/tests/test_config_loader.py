import unittest

from lab_02_navigation.src.config_loader import ConfigError, load_config, validate_config
from lab_02_navigation.src.models import Lab2Config


class TestConfigLoader(unittest.TestCase):
    def test_load_default(self) -> None:
        config = load_config("lab_02_navigation/configs/default.json")
        self.assertIsInstance(config, Lab2Config)
        self.assertEqual(config.run.max_steps, 200)

    def test_invalid_steps(self) -> None:
        with self.assertRaises(ConfigError):
            validate_config({
                "run": {"max_steps": 0},
                "planner": {"step_size": 1.0},
                "models": {"map_file": "lab_02_navigation/models/map.json"},
                "start": [0, 0],
                "goal": [1, 1]
            })


if __name__ == "__main__":
    unittest.main()
