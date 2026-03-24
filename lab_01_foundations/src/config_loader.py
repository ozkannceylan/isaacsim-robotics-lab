"""Configuration loading and validation utilities for Lab 01."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import LabConfig, ModelConfig, RunConfig, SimulationConfig


class ConfigError(ValueError):
    """Raised when config parsing or validation fails."""


def load_config(config_path: str | Path) -> LabConfig:
    """Load a JSON/YAML config file and validate required keys."""
    path = Path(config_path)
    if not path.exists():
        raise ConfigError(f"Config file not found: {path}")

    if path.suffix.lower() not in {".json", ".yaml", ".yml"}:
        raise ConfigError("Config must use .json, .yaml, or .yml extension")

    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
    else:
        try:
            import yaml  # type: ignore
        except ImportError as exc:
            raise ConfigError(
                "YAML config requested but PyYAML is not installed. "
                "Use JSON config or install pyyaml."
            ) from exc
        data = yaml.safe_load(path.read_text(encoding="utf-8"))

    return validate_config(data)


def validate_config(config: dict[str, Any]) -> LabConfig:
    """Validate config contract and return typed config object."""
    required_top_level = ["run", "models", "simulation"]
    missing = [key for key in required_top_level if key not in config]
    if missing:
        raise ConfigError(f"Missing required config section(s): {', '.join(missing)}")

    run_data = config["run"]
    sim_data = config["simulation"]
    models_data = config["models"]

    for model_key in ("robot", "environment"):
        if model_key not in models_data:
            raise ConfigError(f"Missing required model path: models.{model_key}")

    run = RunConfig(
        max_steps=int(run_data.get("max_steps", 100)),
        seed=int(run_data.get("seed", 0)),
    )
    if run.max_steps <= 0:
        raise ConfigError("run.max_steps must be > 0")

    simulation = SimulationConfig(time_step=float(sim_data.get("time_step", 0.01)))
    if simulation.time_step <= 0:
        raise ConfigError("simulation.time_step must be > 0")

    models = ModelConfig(
        robot=str(models_data["robot"]),
        environment=str(models_data["environment"]),
    )

    return LabConfig(run=run, simulation=simulation, models=models)
