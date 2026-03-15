"""Config loader for Lab 2 navigation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import Lab2Config, ModelConfig, PlannerConfig, RunConfig


class ConfigError(ValueError):
    pass


def load_config(config_path: str | Path) -> Lab2Config:
    path = Path(config_path)
    if not path.exists():
        raise ConfigError(f"Config not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    return validate_config(data)


def validate_config(config: dict[str, Any]) -> Lab2Config:
    for key in ("run", "planner", "models", "start", "goal"):
        if key not in config:
            raise ConfigError(f"Missing required section: {key}")

    run = RunConfig(max_steps=int(config["run"].get("max_steps", 200)), seed=int(config["run"].get("seed", 0)))
    planner = PlannerConfig(step_size=float(config["planner"].get("step_size", 1.0)))
    models = ModelConfig(map_file=str(config["models"].get("map_file", "lab_02_navigation/models/map.json")))

    if run.max_steps <= 0:
        raise ConfigError("run.max_steps must be > 0")
    if planner.step_size <= 0:
        raise ConfigError("planner.step_size must be > 0")

    start = tuple(config["start"])
    goal = tuple(config["goal"])
    if len(start) != 2 or len(goal) != 2:
        raise ConfigError("start and goal must have 2 values")

    return Lab2Config(run=run, planner=planner, models=models, start=(float(start[0]), float(start[1])), goal=(float(goal[0]), float(goal[1])))
