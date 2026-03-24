"""Perception context setup."""

from __future__ import annotations

from pathlib import Path

from .models import Lab3Config, PerceptionContext


class SetupError(RuntimeError):
    """Raised when setup fails."""


def initialize_perception(config: Lab3Config, project_root: Path) -> PerceptionContext:
    camera_model_path = project_root / config.models.camera_model_file
    if not camera_model_path.exists():
        raise SetupError(f"Camera model not found: {camera_model_path}")

    return PerceptionContext(
        camera_model_path=camera_model_path,
        num_frames=config.run.num_frames,
        seed=config.run.seed,
        width=config.sensor.width,
        height=config.sensor.height,
        noise_level=config.sensor.noise_level,
    )
