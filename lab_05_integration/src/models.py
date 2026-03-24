"""Typed models for Lab 05 integration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RunConfig:
    seed: int = 0
    scoreboard_name: str = "subsystem_scoreboard.csv"


@dataclass(frozen=True)
class ThresholdConfig:
    max_foundation_energy: float
    max_navigation_steps: int
    min_perception_mean_intensity: float
    min_overall_score: float


@dataclass(frozen=True)
class InputConfig:
    integration_manifest: str
    lab_01_config: str
    lab_02_config: str
    lab_03_config: str


@dataclass(frozen=True)
class Lab5Config:
    run: RunConfig
    thresholds: ThresholdConfig
    inputs: InputConfig


@dataclass(frozen=True)
class IntegrationContext:
    seed: int
    scoreboard_output_path: Path
    manifest_path: Path
    mission_name: str
    lab_01_config_path: Path
    lab_02_config_path: Path
    lab_03_config_path: Path
    thresholds: ThresholdConfig


@dataclass(frozen=True)
class SubsystemResult:
    name: str
    status: str
    score: float
    passed: bool
    details: dict[str, float | int | str]
