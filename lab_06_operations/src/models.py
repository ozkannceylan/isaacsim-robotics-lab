"""Typed models for Lab 06 operations."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RunConfig:
    seed: int = 0
    checklist_name: str = 'deployment_checklist.csv'


@dataclass(frozen=True)
class ThresholdConfig:
    minimum_release_score: float
    maximum_open_risk: int
    require_success_status: bool


@dataclass(frozen=True)
class InputConfig:
    operations_manifest: str
    lab_05_config: str


@dataclass(frozen=True)
class Lab6Config:
    run: RunConfig
    thresholds: ThresholdConfig
    inputs: InputConfig


@dataclass(frozen=True)
class OperationsContext:
    seed: int
    checklist_output_path: Path
    manifest_path: Path
    deployment_target: str
    lab_05_config_path: Path
    thresholds: ThresholdConfig
    required_checks: tuple[str, ...]
    recommended_actions: tuple[str, ...]
