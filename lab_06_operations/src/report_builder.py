"""Deployment readiness reporting for Lab 06."""

from __future__ import annotations

from typing import Any

from .models import OperationsContext


def build_operations_report(context: OperationsContext, mission_summary: dict[str, Any]) -> dict[str, Any]:
    overall_score = float(mission_summary['overall_score'])
    status_success = mission_summary['status'] == 'success'
    open_risks = sum(1 for subsystem in mission_summary['subsystems'] if not subsystem['passed'])
    readiness_pass = overall_score >= context.thresholds.minimum_release_score and open_risks <= context.thresholds.maximum_open_risk
    if context.thresholds.require_success_status:
        readiness_pass = readiness_pass and status_success

    risk_level = 'low' if open_risks == 0 else 'medium' if open_risks <= context.thresholds.maximum_open_risk else 'high'
    checklist = []
    for check_name in context.required_checks:
        if check_name == 'integration_status':
            passed = status_success
            observed = mission_summary['status']
        elif check_name == 'overall_score':
            passed = overall_score >= context.thresholds.minimum_release_score
            observed = round(overall_score, 6)
        else:
            passed = all(subsystem['status'] == 'success' for subsystem in mission_summary['subsystems'])
            observed = 'consistent' if passed else 'mixed'
        checklist.append({'check': check_name, 'passed': passed, 'observed': observed})

    return {
        'status': 'ready' if readiness_pass else 'hold',
        'deployment_target': context.deployment_target,
        'overall_score': round(overall_score, 6),
        'risk_level': risk_level,
        'open_risks': open_risks,
        'recommended_actions': list(context.recommended_actions),
        'checklist': checklist,
    }
