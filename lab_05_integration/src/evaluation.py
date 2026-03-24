"""Deterministic evaluation helpers for Lab 05 integration."""

from __future__ import annotations

from typing import Any

from .models import IntegrationContext, SubsystemResult


def evaluate_subsystems(context: IntegrationContext, metrics: dict[str, dict[str, Any]]) -> list[SubsystemResult]:
    foundation = metrics["lab_01_foundations"]
    navigation = metrics["lab_02_navigation"]
    perception = metrics["lab_03_perception"]

    foundation_score = min(1.0, context.thresholds.max_foundation_energy / float(foundation["energy_used"]))
    foundation_passed = float(foundation["energy_used"]) <= context.thresholds.max_foundation_energy

    navigation_score = min(1.0, context.thresholds.max_navigation_steps / int(navigation["steps_executed"]))
    navigation_passed = int(navigation["steps_executed"]) <= context.thresholds.max_navigation_steps

    perception_score = min(1.0, float(perception["avg_mean_intensity"]) / context.thresholds.min_perception_mean_intensity)
    perception_passed = float(perception["avg_mean_intensity"]) >= context.thresholds.min_perception_mean_intensity

    return [
        SubsystemResult(
            name="lab_01_foundations",
            status=str(foundation["status"]),
            score=round(foundation_score, 6),
            passed=foundation_passed,
            details={
                "energy_used": round(float(foundation["energy_used"]), 6),
                "steps_executed": int(foundation["steps_executed"]),
            },
        ),
        SubsystemResult(
            name="lab_02_navigation",
            status=str(navigation["status"]),
            score=round(navigation_score, 6),
            passed=navigation_passed,
            details={
                "steps_executed": int(navigation["steps_executed"]),
                "path_length": round(float(navigation["path_length"]), 6),
            },
        ),
        SubsystemResult(
            name="lab_03_perception",
            status=str(perception["status"]),
            score=round(perception_score, 6),
            passed=perception_passed,
            details={
                "num_frames": int(perception["num_frames"]),
                "avg_mean_intensity": round(float(perception["avg_mean_intensity"]), 6),
            },
        ),
    ]


def build_mission_summary(context: IntegrationContext, subsystem_results: list[SubsystemResult]) -> dict[str, Any]:
    overall_score = sum(result.score for result in subsystem_results) / len(subsystem_results)
    all_passed = all(result.passed and result.status == 'success' for result in subsystem_results)
    mission_passed = all_passed and overall_score >= context.thresholds.min_overall_score

    return {
        "status": "success" if mission_passed else "needs_attention",
        "mission_name": context.mission_name,
        "overall_score": round(overall_score, 6),
        "minimum_required_score": context.thresholds.min_overall_score,
        "subsystems": [
            {
                "name": result.name,
                "status": result.status,
                "score": result.score,
                "passed": result.passed,
                "details": result.details,
            }
            for result in subsystem_results
        ],
    }
