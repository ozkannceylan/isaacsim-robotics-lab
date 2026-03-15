"""Simulation and output configuration dataclasses for Lab 01 foundations."""

from __future__ import annotations

from dataclasses import dataclass

from .scene_cfg import FoundationsSceneCfg


@dataclass(frozen=True)
class RuntimeCfg:
    """Simulation execution parameters."""

    headless: bool
    device: str
    physics_dt: float
    render_interval: int
    step_count: int
    seed: int


@dataclass(frozen=True)
class OutputCfg:
    """Artifact output locations."""

    root_dir: str
    summary_filename: str
    joint_state_filename: str
    frames_dirname: str


@dataclass(frozen=True)
class Lab01Config:
    """Full Lab 01 runtime configuration."""

    runtime: RuntimeCfg
    output: OutputCfg
    scene: FoundationsSceneCfg
