"""Finalization setup for Lab 07."""

from __future__ import annotations

import json
from pathlib import Path

from .models import FinalizationContext, Lab7Config


class SetupError(RuntimeError):
    """Raised when finalization setup cannot be completed."""


def initialize_finalization(config: Lab7Config, project_root: Path) -> FinalizationContext:
    manifest_path = project_root / config.inputs.release_manifest
    lab_06_config_path = project_root / config.inputs.lab_06_config

    for path in (manifest_path, lab_06_config_path):
        if not path.exists():
            raise SetupError(f'Required finalization asset not found: {path}')

    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))

    return FinalizationContext(
        seed=config.run.seed,
        audit_output_path=project_root / 'lab_07_finalization/data' / config.run.audit_name,
        manifest_path=manifest_path,
        release_name=str(manifest.get('release_name', 'repo_release')),
        lab_06_config_path=lab_06_config_path,
        thresholds=config.thresholds,
        required_paths=tuple(manifest.get('required_paths', [])),
    )
