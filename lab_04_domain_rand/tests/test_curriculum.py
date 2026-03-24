import unittest

from lab_04_domain_rand.config_loader import load_config
from lab_04_domain_rand.robust_grasp.training import train_domain_randomized_policy


class TestCurriculum(unittest.TestCase):
    def test_adr_widens_ranges_beyond_2x(self) -> None:
        config = load_config("lab_04_domain_rand/configs/local.yaml")
        training = train_domain_randomized_policy(config)
        self.assertGreaterEqual(training.max_range_scale, 2.0)


if __name__ == "__main__":
    unittest.main()
