import json
import tempfile
import unittest
from pathlib import Path

from lab_06_operations.src.config_loader import load_config
from lab_06_operations.src.logging_utils import write_checklist_csv, write_summary
from lab_06_operations.src.operations_pipeline import run_operations_pipeline
from lab_06_operations.src.operations_setup import initialize_operations


class TestPipeline(unittest.TestCase):
    def test_end_to_end(self) -> None:
        config = load_config('lab_06_operations/configs/dev.json')
        context = initialize_operations(config, Path.cwd())
        summary = run_operations_pipeline(context, project_root=Path.cwd())

        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            summary_path = write_summary(summary, tmpdir / 'summary.json')
            checklist_path = write_checklist_csv(summary, tmpdir / 'checklist.csv')

            payload = json.loads(summary_path.read_text(encoding='utf-8'))
            self.assertIn(payload['status'], {'ready', 'hold'})
            self.assertTrue(checklist_path.exists())


if __name__ == '__main__':
    unittest.main()
