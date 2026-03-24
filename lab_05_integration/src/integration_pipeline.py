"""Cross-lab orchestration for Lab 05 integration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from lab_01_foundations.src.config_loader import load_config as load_lab_01_config
from lab_01_foundations.src.simulation_setup import initialize_simulation
from lab_01_foundations.src.task_loop import run_task_loop
from lab_02_navigation.src.config_loader import load_config as load_lab_02_config
from lab_02_navigation.src.navigation_setup import initialize_navigation
from lab_02_navigation.src.planner import run_planner
from lab_03_perception.src.config_loader import load_config as load_lab_03_config
from lab_03_perception.src.feature_extractor import extract_features
from lab_03_perception.src.perception_setup import initialize_perception
from lab_03_perception.src.sensor_sim import generate_sensor_frames

from .evaluation import build_mission_summary, evaluate_subsystems
from .models import IntegrationContext


def run_integration_pipeline(context: IntegrationContext, project_root: Path | None = None) -> dict[str, Any]:
    root = project_root or Path.cwd()

    foundations_config = load_lab_01_config(context.lab_01_config_path)
    foundations_context = initialize_simulation(foundations_config, root)
    foundation_metrics = run_task_loop(foundations_context, collect_trajectory=False)

    navigation_config = load_lab_02_config(context.lab_02_config_path)
    navigation_context = initialize_navigation(navigation_config, root)
    navigation_metrics = run_planner(navigation_context, collect_path=False)

    perception_config = load_lab_03_config(context.lab_03_config_path)
    perception_context = initialize_perception(perception_config, root)
    perception_samples = generate_sensor_frames(perception_context)
    perception_metrics = extract_features(perception_samples)

    metrics = {
        "lab_01_foundations": foundation_metrics,
        "lab_02_navigation": navigation_metrics,
        "lab_03_perception": perception_metrics,
    }
    subsystem_results = evaluate_subsystems(context, metrics)
    summary = build_mission_summary(context, subsystem_results)
    summary["integrated_metrics"] = {
        "foundation_energy": foundation_metrics["energy_used"],
        "navigation_steps": navigation_metrics["steps_executed"],
        "perception_frames": perception_metrics["num_frames"],
    }
    return summary
