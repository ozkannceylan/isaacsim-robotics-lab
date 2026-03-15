"""Typed models for Lab 2 navigation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RunConfig:
    max_steps: int = 200
    seed: int = 0


@dataclass(frozen=True)
class PlannerConfig:
    step_size: float = 1.0


@dataclass(frozen=True)
class ModelConfig:
    map_file: str = "lab_02_navigation/models/map.json"


@dataclass(frozen=True)
class Lab2Config:
    run: RunConfig
    planner: PlannerConfig
    models: ModelConfig
    start: tuple[float, float]
    goal: tuple[float, float]


@dataclass(frozen=True)
class NavigationContext:
    map_file_path: Path
    step_size: float
    max_steps: int
    seed: int
    start: tuple[float, float]
    goal: tuple[float, float]
