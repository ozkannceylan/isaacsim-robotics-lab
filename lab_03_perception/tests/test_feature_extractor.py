import unittest
from pathlib import Path

from lab_03_perception.src.feature_extractor import extract_features
from lab_03_perception.src.models import FrameSample, PerceptionContext
from lab_03_perception.src.sensor_sim import generate_sensor_frames


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

    def test_fixed_seed_produces_stable_features(self) -> None:
        context = PerceptionContext(
            camera_model_path=Path("lab_03_perception/models/camera.json"),
            num_frames=10,
            seed=7,
            width=32,
            height=24,
            noise_level=0.02,
        )
        first = extract_features(generate_sensor_frames(context))
        second = extract_features(generate_sensor_frames(context))
        self.assertEqual(first["frame_features"], second["frame_features"])
        self.assertEqual(first["avg_mean_intensity"], second["avg_mean_intensity"])
        self.assertEqual(first["avg_variance"], second["avg_variance"])


if __name__ == "__main__":
    unittest.main()
