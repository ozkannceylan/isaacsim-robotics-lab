"""Config loader for Lab 3 perception."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import Lab3Config, ModelConfig, RunConfig, SensorConfig


class ConfigError(ValueError):
    """Raised on invalid config."""


def load_config(config_path: str | Path) -> Lab3Config:
    path = Path(config_path)
    if not path.exists():
        raise ConfigError(f"Config not found: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    return validate_config(data)


def validate_config(config: dict[str, Any]) -> Lab3Config:
    for key in ("run", "sensor", "models"):
        if key not in config:
            raise ConfigError(f"Missing required section: {key}")

    run = RunConfig(
        num_frames=int(config["run"].get("num_frames", 20)),
        seed=int(config["run"].get("seed", 0)),
    )
    sensor = SensorConfig(
        width=int(config["sensor"].get("width", 64)),
        height=int(config["sensor"].get("height", 48)),
        noise_level=float(config["sensor"].get("noise_level", 0.05)),
    )
    model = ModelConfig(
        camera_model_file=str(config["models"].get("camera_model_file", "lab_03_perception/models/camera.json"))
    )

    if run.num_frames <= 0:
        raise ConfigError("run.num_frames must be > 0")
    if sensor.width <= 0 or sensor.height <= 0:
        raise ConfigError("sensor.width and sensor.height must be > 0")
    if not (0.0 <= sensor.noise_level <= 1.0):
        raise ConfigError("sensor.noise_level must be between 0.0 and 1.0")

    return Lab3Config(run=run, sensor=sensor, models=model)
