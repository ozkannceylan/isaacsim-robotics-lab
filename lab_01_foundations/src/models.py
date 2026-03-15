"""Typed models for Lab 01 configuration and runtime state."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RunConfig:
    max_steps: int = 100
    seed: int = 0


@dataclass(frozen=True)
class SimulationConfig:
    time_step: float = 0.01


@dataclass(frozen=True)
class ModelConfig:
    robot: str = "lab_01_foundations/models/robot.usd"
    environment: str = "lab_01_foundations/models/environment.usd"


@dataclass(frozen=True)
class LabConfig:
    run: RunConfig
    simulation: SimulationConfig
    models: ModelConfig


@dataclass(frozen=True)
class SimulationContext:
    robot_model_path: Path
    environment_model_path: Path
    time_step: float
    max_steps: int
    seed: int
