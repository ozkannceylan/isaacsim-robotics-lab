"""Deterministic waypoint planner for Lab 2."""

from __future__ import annotations

import math
from typing import Any

from .models import NavigationContext


def run_planner(context: NavigationContext, collect_path: bool = False) -> dict[str, Any]:
    x, y = context.start
    gx, gy = context.goal
    waypoints: list[dict[str, float]] = []
    path_length = 0.0

    steps = 0
    while steps < context.max_steps:
        dx = gx - x
        dy = gy - y
        dist = math.hypot(dx, dy)
        if dist <= context.step_size:
            x, y = gx, gy
            path_length += dist
            steps += 1
            if collect_path:
                waypoints.append({"x": round(x, 4), "y": round(y, 4)})
            break

        ux = dx / dist
        uy = dy / dist
        x += ux * context.step_size
        y += uy * context.step_size
        path_length += context.step_size
        steps += 1
        if collect_path:
            waypoints.append({"x": round(x, 4), "y": round(y, 4)})

    success = (x, y) == (gx, gy)
    return {
        "status": "success" if success else "incomplete",
        "steps_executed": steps,
        "path_length": round(path_length, 4),
        "seed": context.seed,
        "map_file": str(context.map_file_path),
        "start": context.start,
        "goal": context.goal,
        "final_position": (round(x, 4), round(y, 4)),
        "waypoints": waypoints,
    }
