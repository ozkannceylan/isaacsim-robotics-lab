import json
import tempfile
import unittest
from csv import DictReader
from pathlib import Path

from lab_03_perception.src.config_loader import load_config
from lab_03_perception.src.feature_extractor import extract_features
from lab_03_perception.src.logging_utils import write_frame_features_csv, write_summary
from lab_03_perception.src.perception_setup import initialize_perception
from lab_03_perception.src.sensor_sim import generate_sensor_frames


class TestPipeline(unittest.TestCase):
    def test_end_to_end(self) -> None:
        config = load_config("lab_03_perception/configs/dev.json")
        context = initialize_perception(config, Path.cwd())
        samples = generate_sensor_frames(context)
        summary = extract_features(samples)

        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            summary_path = write_summary(summary, tmpdir / "summary.json")
            features_path = write_frame_features_csv(summary, tmpdir / "features.csv")

            payload = json.loads(summary_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["status"], "success")
            self.assertEqual(payload["num_frames"], 10)
            self.assertTrue(features_path.exists())
            with features_path.open("r", encoding="utf-8", newline="") as handle:
                rows = list(DictReader(handle))
            self.assertEqual(len(rows), 10)


if __name__ == "__main__":
    unittest.main()
