"""Operations setup for Lab 06."""

from __future__ import annotations

import json
from pathlib import Path

from .models import Lab6Config, OperationsContext


class SetupError(RuntimeError):
    """Raised when operations setup cannot be completed."""


def initialize_operations(config: Lab6Config, project_root: Path) -> OperationsContext:
    manifest_path = project_root / config.inputs.operations_manifest
    lab_05_config_path = project_root / config.inputs.lab_05_config

    for path in (manifest_path, lab_05_config_path):
        if not path.exists():
            raise SetupError(f'Required operations asset not found: {path}')

    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))

    return OperationsContext(
        seed=config.run.seed,
        checklist_output_path=project_root / 'lab_06_operations/data' / config.run.checklist_name,
        manifest_path=manifest_path,
        deployment_target=str(manifest.get('deployment_target', 'unknown_target')),
        lab_05_config_path=lab_05_config_path,
        thresholds=config.thresholds,
        required_checks=tuple(manifest.get('required_checks', [])),
        recommended_actions=tuple(manifest.get('recommended_actions', [])),
    )
