"""Deterministic synthetic sensor simulation."""

from __future__ import annotations

import random

from .models import FrameSample, PerceptionContext


def generate_sensor_frames(context: PerceptionContext) -> list[FrameSample]:
    rng = random.Random(context.seed)
    samples: list[FrameSample] = []

    pixel_count = context.width * context.height
    for frame_idx in range(context.num_frames):
        base = 0.35 + 0.3 * ((frame_idx % 10) / 9)
        noise = rng.uniform(-context.noise_level, context.noise_level)
        mean_intensity = min(1.0, max(0.0, base + noise))
        variance = abs(rng.uniform(0.0, context.noise_level)) * (1.0 + (pixel_count / 5000))
        samples.append(
            FrameSample(
                frame_index=frame_idx,
                mean_intensity=round(mean_intensity, 6),
                variance=round(variance, 6),
            )
        )

    return samples
