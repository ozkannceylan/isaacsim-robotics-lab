"""Repository audit helpers for Lab 07 finalization."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .models import FinalizationContext


def run_repo_audit(context: FinalizationContext, project_root: Path | None = None) -> dict[str, Any]:
    root = project_root or Path.cwd()
    rows = []
    for required_path in context.required_paths:
        target = root / required_path
        rows.append(
            {
                'path': required_path,
                'exists': target.exists(),
                'type': 'dir' if target.is_dir() else 'file' if target.is_file() else 'missing',
            }
        )

    completeness = sum(1 for row in rows if row['exists']) / len(rows) if rows else 1.0
    return {
        'repo_completeness': round(completeness, 6),
        'audit_rows': rows,
    }
