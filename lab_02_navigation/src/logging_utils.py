"""Artifact writers for Lab 2 outputs."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


def write_summary(summary: dict[str, Any], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = dict(summary)
    payload.pop("waypoints", None)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def write_path_csv(summary: dict[str, Any], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["x", "y"])
        writer.writeheader()
        for wp in summary.get("waypoints", []):
            writer.writerow(wp)
    return path
