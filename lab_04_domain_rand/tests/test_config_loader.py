import unittest

from lab_04_domain_rand.config_loader import ConfigError, load_config, validate_config


class TestConfigLoader(unittest.TestCase):
    def test_load_local_config(self) -> None:
        config = load_config("lab_04_domain_rand/configs/local.yaml")
        self.assertEqual(config.training.num_envs, 32)
        self.assertEqual(config.evaluation.episodes_per_config, 100)
        self.assertEqual(config.geometry_randomization.object_types, ("cube", "cylinder", "sphere"))

    def test_invalid_num_envs_raises(self) -> None:
        with self.assertRaises(ConfigError):
            validate_config(
                {
                    "training": {"headless": True, "num_envs": 128, "num_training_episodes": 600},
                    "physics_randomization": {
                        "mass_kg_range": [0.05, 0.3],
                        "friction_range": [0.4, 1.2],
                        "joint_damping_scale_range": [0.8, 1.2],
                        "actuator_stiffness_scale_range": [0.9, 1.1],
                    },
                    "observation_noise": {
                        "joint_pos_std_rad": 0.01,
                        "joint_vel_std_rad_s": 0.05,
                        "object_pose_std_m": 0.005,
                    },
                    "geometry_randomization": {"object_types": ["cube", "cylinder"], "size_m_range": [0.03, 0.08]},
                    "external_perturbation": {"interval_steps": 50, "force_n_range": [0.0, 2.0]},
                    "curriculum": {"success_window": 100, "widen_threshold": 0.8, "narrow_threshold": 0.5},
                    "evaluation": {"episodes_per_config": 100},
                }
            )


if __name__ == "__main__":
    unittest.main()
