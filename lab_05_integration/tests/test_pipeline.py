import json
import tempfile
import unittest
from pathlib import Path

from lab_05_integration.src.config_loader import load_config
from lab_05_integration.src.integration_pipeline import run_integration_pipeline
from lab_05_integration.src.integration_setup import initialize_integration
from lab_05_integration.src.logging_utils import write_scoreboard_csv, write_summary


class TestPipeline(unittest.TestCase):
    def test_end_to_end(self) -> None:
        config = load_config('lab_05_integration/configs/dev.json')
        context = initialize_integration(config, Path.cwd())
        summary = run_integration_pipeline(context, project_root=Path.cwd())

        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            summary_path = write_summary(summary, tmpdir / 'summary.json')
            scoreboard_path = write_scoreboard_csv(summary, tmpdir / 'scoreboard.csv')

            payload = json.loads(summary_path.read_text(encoding='utf-8'))
            self.assertIn(payload['status'], {'success', 'needs_attention'})
            self.assertEqual(len(payload['subsystems']), 3)
            self.assertTrue(scoreboard_path.exists())


if __name__ == '__main__':
    unittest.main()
