"""Typed runtime models for Lab 01 artifact generation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class JointStateRecord:
    """Single-step joint command and state sample."""

    step: int
    sim_time_s: float
    joint_targets_rad: tuple[float, ...]
    joint_positions_rad: tuple[float, ...]
    joint_velocities_rad_s: tuple[float, ...]


@dataclass(frozen=True)
class CapturedFrame:
    """Captured RGB frame encoded as packed 8-bit RGB bytes."""

    frame_index: int
    step: int
    width: int
    height: int
    rgb_bytes: bytes


@dataclass(frozen=True)
class LabRunResult:
    """Complete artifact payload for a Lab 01 execution."""

    runtime_name: str
    joint_names: tuple[str, ...]
    joint_state_records: tuple[JointStateRecord, ...]
    captured_frames: tuple[CapturedFrame, ...]
    metadata: Mapping[str, object]
