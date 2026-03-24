"""Integration setup for Lab 05."""

from __future__ import annotations

import json
from pathlib import Path

from .models import IntegrationContext, Lab5Config


class SetupError(RuntimeError):
    """Raised when integration setup cannot be completed."""


def initialize_integration(config: Lab5Config, project_root: Path) -> IntegrationContext:
    manifest_path = project_root / config.inputs.integration_manifest
    lab_01_config_path = project_root / config.inputs.lab_01_config
    lab_02_config_path = project_root / config.inputs.lab_02_config
    lab_03_config_path = project_root / config.inputs.lab_03_config

    for path in (manifest_path, lab_01_config_path, lab_02_config_path, lab_03_config_path):
        if not path.exists():
            raise SetupError(f"Required integration asset not found: {path}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    mission_name = str(manifest.get("mission_name", "integration_mission"))

    return IntegrationContext(
        seed=config.run.seed,
        scoreboard_output_path=project_root / 'lab_05_integration/data' / config.run.scoreboard_name,
        manifest_path=manifest_path,
        mission_name=mission_name,
        lab_01_config_path=lab_01_config_path,
        lab_02_config_path=lab_02_config_path,
        lab_03_config_path=lab_03_config_path,
        thresholds=config.thresholds,
    )
