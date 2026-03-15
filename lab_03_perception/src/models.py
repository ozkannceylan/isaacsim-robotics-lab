"""Typed models for Lab 3 perception."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RunConfig:
    num_frames: int = 20
    seed: int = 0


@dataclass(frozen=True)
class SensorConfig:
    width: int = 64
    height: int = 48
    noise_level: float = 0.05


@dataclass(frozen=True)
class ModelConfig:
    camera_model_file: str = "lab_03_perception/models/camera.json"


@dataclass(frozen=True)
class Lab3Config:
    run: RunConfig
    sensor: SensorConfig
    models: ModelConfig


@dataclass(frozen=True)
class PerceptionContext:
    camera_model_path: Path
    num_frames: int
    seed: int
    width: int
    height: int
    noise_level: float


@dataclass(frozen=True)
class FrameSample:
    frame_index: int
    mean_intensity: float
    variance: float
