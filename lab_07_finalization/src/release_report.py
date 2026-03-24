"""Release report assembly for Lab 07 finalization."""

from __future__ import annotations

from typing import Any

from .models import FinalizationContext


def build_release_report(
    context: FinalizationContext,
    operations_summary: dict[str, Any],
    audit_summary: dict[str, Any],
) -> dict[str, Any]:
    operations_ready = operations_summary['status'] == 'ready'
    final_score = (float(operations_summary['overall_score']) + float(audit_summary['repo_completeness'])) / 2
    repo_complete = float(audit_summary['repo_completeness']) >= context.thresholds.minimum_repo_completeness
    final_ready = operations_ready and repo_complete and final_score >= context.thresholds.minimum_final_score

    return {
        'status': 'final_ready' if final_ready else 'needs_follow_up',
        'release_name': context.release_name,
        'final_score': round(final_score, 6),
        'operations_status': operations_summary['status'],
        'repo_completeness': audit_summary['repo_completeness'],
        'audit_rows': audit_summary['audit_rows'],
        'recommended_next_step': 'tag_release' if final_ready else 'resolve_audit_findings',
    }
