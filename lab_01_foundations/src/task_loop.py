"""Task-loop baseline implementation for Lab 01 foundations."""

from __future__ import annotations

import random
from typing import Any

from .models import SimulationContext


def run_task_loop(sim_context: SimulationContext, collect_trajectory: bool = False) -> dict[str, Any]:
    """Run a deterministic placeholder loop and return summary metrics."""
    rng = random.Random(sim_context.seed)
    energy = 0.0
    trajectory = []

    for step in range(sim_context.max_steps):
        action = rng.uniform(-1.0, 1.0)
        energy += abs(action)
        if collect_trajectory:
            trajectory.append({"step": step, "action": round(action, 6)})

    simulated_time = sim_context.max_steps * sim_context.time_step
    return {
        "status": "success",
        "steps_executed": sim_context.max_steps,
        "simulated_time": simulated_time,
        "energy_used": round(energy, 6),
        "seed": sim_context.seed,
        "trajectory": trajectory,
    }
