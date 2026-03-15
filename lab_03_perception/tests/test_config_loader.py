import unittest

from lab_03_perception.src.config_loader import ConfigError, load_config, validate_config
from lab_03_perception.src.models import Lab3Config


class TestConfigLoader(unittest.TestCase):
    def test_load_default(self) -> None:
        config = load_config("lab_03_perception/configs/default.json")
        self.assertIsInstance(config, Lab3Config)
        self.assertEqual(config.run.num_frames, 20)

    def test_invalid_noise_level(self) -> None:
        with self.assertRaises(ConfigError):
            validate_config(
                {
                    "run": {"num_frames": 10, "seed": 1},
                    "sensor": {"width": 32, "height": 24, "noise_level": 2.0},
                    "models": {"camera_model_file": "lab_03_perception/models/camera.json"},
                }
            )


if __name__ == "__main__":
    unittest.main()
