import unittest

from lab_01_foundations.src.config_loader import ConfigError, apply_output_dir, load_config, validate_config


class TestConfigLoader(unittest.TestCase):
    def test_load_local_config_matches_plan_targets(self) -> None:
        config = load_config("lab_01_foundations/configs/local.yaml")
        self.assertEqual(config.runtime.step_count, 300)
        self.assertEqual(config.scene.camera.frame_count, 30)
        self.assertEqual(config.scene.camera.width, 640)
        self.assertEqual(config.scene.camera.height, 480)
        self.assertEqual(len(config.scene.robot.joint_names), 6)
        self.assertTrue(config.runtime.headless)

    def test_missing_config_raises(self) -> None:
        with self.assertRaises(ConfigError):
            load_config("lab_01_foundations/configs/does_not_exist.yaml")

    def test_invalid_frame_count_raises(self) -> None:
        with self.assertRaises(ConfigError):
            validate_config(
                {
                    "runtime": {"headless": True, "physics_dt": 0.01, "render_interval": 1, "step_count": 2},
                    "output": {"root_dir": "tmp"},
                    "scene": {
                        "environment": {"usd_path": "warehouse.usd", "prim_path": "/World/Warehouse"},
                        "robot": {
                            "usd_path": "ur5e.usd",
                            "prim_path": "/World/Robot",
                            "base_position": [0.0, 0.0, 0.0],
                            "base_orientation": [1.0, 0.0, 0.0, 0.0],
                            "joint_names": ["a", "b", "c", "d", "e", "f"],
                            "joint_amplitudes_rad": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
                            "joint_phase_offsets_rad": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                            "trajectory_frequency_hz": 0.25,
                        },
                        "table": {
                            "prim_path": "/World/Table",
                            "position": [0.0, 0.0, 0.0],
                            "size": [1.0, 1.0, 1.0],
                            "color": [0.5, 0.5, 0.5],
                        },
                        "camera": {
                            "prim_path": "/World/Camera",
                            "position": [0.0, 0.0, 1.0],
                            "orientation": [1.0, 0.0, 0.0, 0.0],
                            "convention": "world",
                            "width": 64,
                            "height": 48,
                            "frame_count": 3,
                        },
                    },
                }
            )

    def test_apply_output_dir_returns_updated_copy(self) -> None:
        config = load_config("lab_01_foundations/configs/mock.yaml")
        updated = apply_output_dir(config, "/tmp/lab_01_test")
        self.assertNotEqual(updated.output.root_dir, config.output.root_dir)
        self.assertEqual(updated.output.root_dir, "/tmp/lab_01_test")


if __name__ == "__main__":
    unittest.main()
