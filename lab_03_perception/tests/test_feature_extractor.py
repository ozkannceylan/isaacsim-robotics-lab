import unittest

from lab_03_perception.src.feature_extractor import extract_features
from lab_03_perception.src.models import FrameSample


class TestFeatureExtractor(unittest.TestCase):
    def test_extract_features_non_empty(self) -> None:
        samples = [
            FrameSample(frame_index=0, mean_intensity=0.4, variance=0.01),
            FrameSample(frame_index=1, mean_intensity=0.6, variance=0.03),
        ]
        summary = extract_features(samples)
        self.assertEqual(summary["status"], "success")
        self.assertEqual(summary["num_frames"], 2)
        self.assertAlmostEqual(summary["avg_mean_intensity"], 0.5)


if __name__ == "__main__":
    unittest.main()
