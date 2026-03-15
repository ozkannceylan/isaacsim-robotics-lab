"""Trajectory helpers for Lab 01 foundations."""

from __future__ import annotations

import math
from typing import Sequence


def compute_capture_steps(step_count: int, frame_count: int) -> tuple[int, ...]:
    """Spread frame captures evenly across the simulation horizon."""
    return tuple(((index + 1) * step_count // frame_count) - 1 for index in range(frame_count))


def generate_joint_targets(
    base_positions: Sequence[float],
    amplitudes_rad: Sequence[float],
    phase_offsets_rad: Sequence[float],
    frequency_hz: float,
    time_s: float,
) -> tuple[float, ...]:
    """Generate a sine trajectory for each joint."""
    phase = 2.0 * math.pi * frequency_hz * time_s
    return tuple(
        float(base + amplitude * math.sin(phase + offset))
        for base, amplitude, offset in zip(base_positions, amplitudes_rad, phase_offsets_rad, strict=True)
    )


def generate_joint_velocities(
    amplitudes_rad: Sequence[float],
    phase_offsets_rad: Sequence[float],
    frequency_hz: float,
    time_s: float,
) -> tuple[float, ...]:
    """Compute analytical joint velocities for the sine trajectory."""
    omega = 2.0 * math.pi * frequency_hz
    phase = omega * time_s
    return tuple(
        float(amplitude * omega * math.cos(phase + offset))
        for amplitude, offset in zip(amplitudes_rad, phase_offsets_rad, strict=True)
    )
