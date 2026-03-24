import unittest
from pathlib import Path

from lab_06_operations.src.models import OperationsContext, ThresholdConfig
from lab_06_operations.src.report_builder import build_operations_report


class TestReportBuilder(unittest.TestCase):
    def test_build_operations_report(self) -> None:
        context = OperationsContext(
            seed=0,
            checklist_output_path=Path('lab_06_operations/data/deployment_checklist.csv'),
            manifest_path=Path('lab_06_operations/models/operations_manifest.json'),
            deployment_target='staging_bundle',
            lab_05_config_path=Path('lab_05_integration/configs/default.json'),
            thresholds=ThresholdConfig(
                minimum_release_score=0.8,
                maximum_open_risk=1,
                require_success_status=True,
            ),
            required_checks=('integration_status', 'overall_score', 'subsystem_consistency'),
            recommended_actions=('publish_summary', 'archive_scoreboard'),
        )
        mission_summary = {
            'status': 'success',
            'overall_score': 0.9,
            'subsystems': [
                {'status': 'success', 'passed': True},
                {'status': 'success', 'passed': True},
            ],
        }

        report = build_operations_report(context, mission_summary)
        self.assertEqual(report['status'], 'ready')
        self.assertEqual(len(report['checklist']), 3)


if __name__ == '__main__':
    unittest.main()
