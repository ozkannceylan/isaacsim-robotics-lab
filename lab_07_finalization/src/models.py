"""Typed models for Lab 07 finalization."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RunConfig:
    seed: int = 0
    audit_name: str = 'repo_audit.csv'


@dataclass(frozen=True)
class ThresholdConfig:
    minimum_final_score: float
    minimum_repo_completeness: float


@dataclass(frozen=True)
class InputConfig:
    release_manifest: str
    lab_06_config: str


@dataclass(frozen=True)
class Lab7Config:
    run: RunConfig
    thresholds: ThresholdConfig
    inputs: InputConfig


@dataclass(frozen=True)
class FinalizationContext:
    seed: int
    audit_output_path: Path
    manifest_path: Path
    release_name: str
    lab_06_config_path: Path
    thresholds: ThresholdConfig
    required_paths: tuple[str, ...]
