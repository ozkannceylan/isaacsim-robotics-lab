"""Logging and result serialization helpers."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


def write_run_summary(summary: dict[str, Any], output_path: str | Path) -> Path:
    """Write run summary JSON output and return resulting path."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    serializable = dict(summary)
    serializable.pop("trajectory", None)
    path.write_text(json.dumps(serializable, indent=2), encoding="utf-8")
    return path


def write_trajectory_csv(summary: dict[str, Any], output_path: str | Path) -> Path:
    """Write trajectory rows to CSV and return path."""
    rows = summary.get("trajectory", [])
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["step", "action"])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    return path
