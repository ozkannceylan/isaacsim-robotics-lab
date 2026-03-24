import unittest
from pathlib import Path

from lab_07_finalization.src.models import FinalizationContext, ThresholdConfig
from lab_07_finalization.src.release_report import build_release_report


class TestReleaseReport(unittest.TestCase):
    def test_build_release_report(self) -> None:
        context = FinalizationContext(
            seed=0,
            audit_output_path=Path('lab_07_finalization/data/repo_audit.csv'),
            manifest_path=Path('lab_07_finalization/models/release_manifest.json'),
            release_name='final_release',
            lab_06_config_path=Path('lab_06_operations/configs/default.json'),
            thresholds=ThresholdConfig(minimum_final_score=0.8, minimum_repo_completeness=1.0),
            required_paths=('README.md', 'lab_01_foundations'),
        )
        operations_summary = {'status': 'ready', 'overall_score': 0.9}
        audit_summary = {
            'repo_completeness': 1.0,
            'audit_rows': [{'path': 'README.md', 'exists': True, 'type': 'file'}],
        }

        report = build_release_report(context, operations_summary, audit_summary)
        self.assertEqual(report['status'], 'final_ready')
        self.assertEqual(report['recommended_next_step'], 'tag_release')


if __name__ == '__main__':
    unittest.main()
