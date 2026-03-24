"""Navigation setup for Lab 2."""

from __future__ import annotations

from pathlib import Path

from .models import Lab2Config, NavigationContext


class SetupError(RuntimeError):
    pass


def initialize_navigation(config: Lab2Config, project_root: Path) -> NavigationContext:
    map_path = project_root / config.models.map_file
    if not map_path.exists():
        raise SetupError(f"Map file missing: {map_path}")

    return NavigationContext(
        map_file_path=map_path,
        step_size=config.planner.step_size,
        max_steps=config.run.max_steps,
        seed=config.run.seed,
        start=config.start,
        goal=config.goal,
    )
