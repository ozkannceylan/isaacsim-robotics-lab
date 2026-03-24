"""Operations pipeline orchestration for Lab 06."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from lab_05_integration.src.config_loader import load_config as load_lab_05_config
from lab_05_integration.src.integration_pipeline import run_integration_pipeline
from lab_05_integration.src.integration_setup import initialize_integration

from .models import OperationsContext
from .report_builder import build_operations_report


def run_operations_pipeline(context: OperationsContext, project_root: Path | None = None) -> dict[str, Any]:
    root = project_root or Path.cwd()
    lab_05_config = load_lab_05_config(context.lab_05_config_path)
    lab_05_context = initialize_integration(lab_05_config, root)
    mission_summary = run_integration_pipeline(lab_05_context, project_root=root)
    report = build_operations_report(context, mission_summary)
    report['mission_summary'] = mission_summary
    return report
