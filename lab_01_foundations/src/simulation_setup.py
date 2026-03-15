"""Simulation setup stubs for Lab 01 foundations."""

from __future__ import annotations

from pathlib import Path

from .models import LabConfig, SimulationContext


class SetupError(RuntimeError):
    """Raised when simulation setup cannot be completed."""


def initialize_simulation(config: LabConfig, project_root: Path) -> SimulationContext:
    """Build a minimal simulation context from config and model paths."""
    robot_path = project_root / config.models.robot
    environment_path = project_root / config.models.environment

    for path in (robot_path, environment_path):
        if not path.exists():
            raise SetupError(f"Model asset not found: {path}")

    return SimulationContext(
        robot_model_path=robot_path,
        environment_model_path=environment_path,
        time_step=config.simulation.time_step,
        max_steps=config.run.max_steps,
        seed=config.run.seed,
    )
