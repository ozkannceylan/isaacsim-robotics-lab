import unittest

from lab_04_domain_rand.config_loader import load_config
from lab_04_domain_rand.robust_grasp.mdp.events import sample_episode_batch


class TestEvents(unittest.TestCase):
    def test_sampling_is_deterministic(self) -> None:
        config = load_config("lab_04_domain_rand/configs/local.yaml")
        first = sample_episode_batch(config, episode_index=3, env_count=4, range_scale=1.0)
        second = sample_episode_batch(config, episode_index=3, env_count=4, range_scale=1.0)
        self.assertEqual(first, second)

    def test_samples_stay_in_range(self) -> None:
        config = load_config("lab_04_domain_rand/configs/local.yaml")
        batch = sample_episode_batch(config, episode_index=0, env_count=8, range_scale=1.0)
        for params in batch:
            self.assertGreaterEqual(params.mass_kg, 0.05)
            self.assertLessEqual(params.mass_kg, 0.3)
            self.assertIn(params.object_type, config.geometry_randomization.object_types)


if __name__ == "__main__":
    unittest.main()
