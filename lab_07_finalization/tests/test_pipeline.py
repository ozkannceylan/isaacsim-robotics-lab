import json
import tempfile
import unittest
from pathlib import Path

from lab_07_finalization.src.config_loader import load_config
from lab_07_finalization.src.finalization_setup import initialize_finalization
from lab_07_finalization.src.logging_utils import write_audit_csv, write_summary
from lab_07_finalization.src.release_report import build_release_report
from lab_07_finalization.src.repo_audit import run_repo_audit
from lab_06_operations.src.config_loader import load_config as load_lab_06_config
from lab_06_operations.src.operations_pipeline import run_operations_pipeline
from lab_06_operations.src.operations_setup import initialize_operations


class TestPipeline(unittest.TestCase):
    def test_end_to_end(self) -> None:
        config = load_config('lab_07_finalization/configs/dev.json')
        context = initialize_finalization(config, Path.cwd())
        lab_06_config = load_lab_06_config(context.lab_06_config_path)
        lab_06_context = initialize_operations(lab_06_config, Path.cwd())
        operations_summary = run_operations_pipeline(lab_06_context, project_root=Path.cwd())
        audit_summary = run_repo_audit(context, project_root=Path.cwd())
        summary = build_release_report(context, operations_summary, audit_summary)

        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            summary_path = write_summary(summary, tmpdir / 'summary.json')
            audit_path = write_audit_csv(summary, tmpdir / 'audit.csv')

            payload = json.loads(summary_path.read_text(encoding='utf-8'))
            self.assertIn(payload['status'], {'final_ready', 'needs_follow_up'})
            self.assertTrue(audit_path.exists())


if __name__ == '__main__':
    unittest.main()
