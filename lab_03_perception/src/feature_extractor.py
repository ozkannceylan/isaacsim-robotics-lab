"""Feature extraction for synthetic sensor frames."""

from __future__ import annotations

from typing import Any

from .models import FrameSample


def extract_features(samples: list[FrameSample]) -> dict[str, Any]:
    if not samples:
        return {
            "status": "empty",
            "num_frames": 0,
            "avg_mean_intensity": 0.0,
            "avg_variance": 0.0,
            "frame_features": [],
        }

    avg_mean = sum(s.mean_intensity for s in samples) / len(samples)
    avg_var = sum(s.variance for s in samples) / len(samples)

    frame_rows = [
        {
            "frame_index": s.frame_index,
            "mean_intensity": s.mean_intensity,
            "variance": s.variance,
        }
        for s in samples
    ]

    return {
        "status": "success",
        "num_frames": len(samples),
        "avg_mean_intensity": round(avg_mean, 6),
        "avg_variance": round(avg_var, 6),
        "frame_features": frame_rows,
    }
