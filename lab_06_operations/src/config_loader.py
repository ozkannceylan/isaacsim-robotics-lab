"""Configuration loading and validation for Lab 06 operations."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import InputConfig, Lab6Config, RunConfig, ThresholdConfig


class ConfigError(ValueError):
    """Raised when Lab 6 config parsing or validation fails."""


def load_config(config_path: str | Path) -> Lab6Config:
    path = Path(config_path)
    if not path.exists():
        raise ConfigError(f'Config file not found: {path}')
    if path.suffix.lower() != '.json':
        raise ConfigError('Lab 6 config must use .json extension')

    data = json.loads(path.read_text(encoding='utf-8'))
    return validate_config(data)


def validate_config(config: dict[str, Any]) -> Lab6Config:
    required = ['run', 'thresholds', 'inputs']
    missing = [key for key in required if key not in config]
    if missing:
        raise ConfigError(f"Missing required config section(s): {', '.join(missing)}")

    run_data = config['run']
    threshold_data = config['thresholds']
    inputs_data = config['inputs']

    thresholds = ThresholdConfig(
        minimum_release_score=float(threshold_data['minimum_release_score']),
        maximum_open_risk=int(threshold_data['maximum_open_risk']),
        require_success_status=bool(threshold_data['require_success_status']),
    )
    if not 0.0 <= thresholds.minimum_release_score <= 1.0:
        raise ConfigError('thresholds.minimum_release_score must be between 0 and 1')
    if thresholds.maximum_open_risk < 0:
        raise ConfigError('thresholds.maximum_open_risk must be >= 0')

    required_inputs = ['operations_manifest', 'lab_05_config']
    missing_inputs = [key for key in required_inputs if key not in inputs_data]
    if missing_inputs:
        raise ConfigError(f"Missing required input path(s): {', '.join(missing_inputs)}")

    inputs = InputConfig(
        operations_manifest=str(inputs_data['operations_manifest']),
        lab_05_config=str(inputs_data['lab_05_config']),
    )
    run = RunConfig(
        seed=int(run_data.get('seed', 0)),
        checklist_name=str(run_data.get('checklist_name', 'deployment_checklist.csv')),
    )
    if not run.checklist_name.endswith('.csv'):
        raise ConfigError('run.checklist_name must end with .csv')

    return Lab6Config(run=run, thresholds=thresholds, inputs=inputs)
