"""Artifact writers for Lab 3 perception."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


def write_summary(summary: dict[str, Any], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = dict(summary)
    payload.pop("frame_features", None)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def write_frame_features_csv(summary: dict[str, Any], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["frame_index", "mean_intensity", "variance"])
        writer.writeheader()
        for row in summary.get("frame_features", []):
            writer.writerow(row)
    return path
