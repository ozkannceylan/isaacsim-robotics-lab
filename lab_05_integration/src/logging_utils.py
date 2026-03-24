"""Logging and serialization helpers for Lab 05 integration."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


def write_summary(summary: dict[str, Any], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2), encoding='utf-8')
    return path


def write_scoreboard_csv(summary: dict[str, Any], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=['name', 'status', 'score', 'passed'])
        writer.writeheader()
        for row in summary.get('subsystems', []):
            writer.writerow(
                {
                    'name': row['name'],
                    'status': row['status'],
                    'score': row['score'],
                    'passed': row['passed'],
                }
            )

    return path
