"""Configuration loading and validation for Lab 05 integration."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import InputConfig, Lab5Config, RunConfig, ThresholdConfig


class ConfigError(ValueError):
    """Raised when config parsing or validation fails."""


def load_config(config_path: str | Path) -> Lab5Config:
    path = Path(config_path)
    if not path.exists():
        raise ConfigError(f"Config file not found: {path}")
    if path.suffix.lower() != ".json":
        raise ConfigError("Lab 5 config must use .json extension")

    data = json.loads(path.read_text(encoding="utf-8"))
    return validate_config(data)


def validate_config(config: dict[str, Any]) -> Lab5Config:
    required = ["run", "thresholds", "inputs"]
    missing = [key for key in required if key not in config]
    if missing:
        raise ConfigError(f"Missing required config section(s): {', '.join(missing)}")

    run_data = config["run"]
    threshold_data = config["thresholds"]
    inputs_data = config["inputs"]

    thresholds = ThresholdConfig(
        max_foundation_energy=float(threshold_data["max_foundation_energy"]),
        max_navigation_steps=int(threshold_data["max_navigation_steps"]),
        min_perception_mean_intensity=float(threshold_data["min_perception_mean_intensity"]),
        min_overall_score=float(threshold_data["min_overall_score"]),
    )
    if thresholds.max_foundation_energy <= 0:
        raise ConfigError("thresholds.max_foundation_energy must be > 0")
    if thresholds.max_navigation_steps <= 0:
        raise ConfigError("thresholds.max_navigation_steps must be > 0")
    if not 0.0 <= thresholds.min_perception_mean_intensity <= 1.0:
        raise ConfigError("thresholds.min_perception_mean_intensity must be between 0 and 1")
    if not 0.0 <= thresholds.min_overall_score <= 1.0:
        raise ConfigError("thresholds.min_overall_score must be between 0 and 1")

    required_inputs = ["integration_manifest", "lab_01_config", "lab_02_config", "lab_03_config"]
    missing_inputs = [key for key in required_inputs if key not in inputs_data]
    if missing_inputs:
        raise ConfigError(f"Missing required input path(s): {', '.join(missing_inputs)}")

    inputs = InputConfig(
        integration_manifest=str(inputs_data["integration_manifest"]),
        lab_01_config=str(inputs_data["lab_01_config"]),
        lab_02_config=str(inputs_data["lab_02_config"]),
        lab_03_config=str(inputs_data["lab_03_config"]),
    )
    run = RunConfig(
        seed=int(run_data.get("seed", 0)),
        scoreboard_name=str(run_data.get("scoreboard_name", "subsystem_scoreboard.csv")),
    )
    if not run.scoreboard_name.endswith('.csv'):
        raise ConfigError("run.scoreboard_name must end with .csv")

    return Lab5Config(run=run, thresholds=thresholds, inputs=inputs)
