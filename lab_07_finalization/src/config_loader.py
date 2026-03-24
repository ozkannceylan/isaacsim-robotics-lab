"""Configuration loading and validation for Lab 07 finalization."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import InputConfig, Lab7Config, RunConfig, ThresholdConfig


class ConfigError(ValueError):
    """Raised when Lab 7 config parsing or validation fails."""


def load_config(config_path: str | Path) -> Lab7Config:
    path = Path(config_path)
    if not path.exists():
        raise ConfigError(f'Config file not found: {path}')
    if path.suffix.lower() != '.json':
        raise ConfigError('Lab 7 config must use .json extension')

    data = json.loads(path.read_text(encoding='utf-8'))
    return validate_config(data)


def validate_config(config: dict[str, Any]) -> Lab7Config:
    required = ['run', 'thresholds', 'inputs']
    missing = [key for key in required if key not in config]
    if missing:
        raise ConfigError(f"Missing required config section(s): {', '.join(missing)}")

    run_data = config['run']
    threshold_data = config['thresholds']
    inputs_data = config['inputs']

    thresholds = ThresholdConfig(
        minimum_final_score=float(threshold_data['minimum_final_score']),
        minimum_repo_completeness=float(threshold_data['minimum_repo_completeness']),
    )
    if not 0.0 <= thresholds.minimum_final_score <= 1.0:
        raise ConfigError('thresholds.minimum_final_score must be between 0 and 1')
    if not 0.0 <= thresholds.minimum_repo_completeness <= 1.0:
        raise ConfigError('thresholds.minimum_repo_completeness must be between 0 and 1')

    required_inputs = ['release_manifest', 'lab_06_config']
    missing_inputs = [key for key in required_inputs if key not in inputs_data]
    if missing_inputs:
        raise ConfigError(f"Missing required input path(s): {', '.join(missing_inputs)}")

    inputs = InputConfig(
        release_manifest=str(inputs_data['release_manifest']),
        lab_06_config=str(inputs_data['lab_06_config']),
    )
    run = RunConfig(
        seed=int(run_data.get('seed', 0)),
        audit_name=str(run_data.get('audit_name', 'repo_audit.csv')),
    )
    if not run.audit_name.endswith('.csv'):
        raise ConfigError('run.audit_name must end with .csv')

    return Lab7Config(run=run, thresholds=thresholds, inputs=inputs)
