"""YAML configuration loading for Lab 04."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

import yaml

from .robust_grasp.robust_grasp_env_cfg import (
    CurriculumCfg,
    EvaluationCfg,
    ExternalPerturbationCfg,
    GeometryRandomizationCfg,
    ObservationNoiseCfg,
    PhysicsRandomizationCfg,
    RangeCfg,
    RobustGraspEnvCfg,
    TrainingCfg,
)


class ConfigError(ValueError):
    """Raised when the Lab 04 config is invalid."""


def load_config(config_path: str | Path) -> RobustGraspEnvCfg:
    """Load and validate the Lab 04 config."""
    path = Path(config_path)
    if not path.exists():
        raise ConfigError(f"Config not found: {path}")
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ConfigError("Top-level config payload must be a mapping")
    return validate_config(payload)


def validate_config(payload: dict[str, Any]) -> RobustGraspEnvCfg:
    """Validate the raw config payload."""
    training_data = _require_mapping(payload, "training")
    physics_data = _require_mapping(payload, "physics_randomization")
    noise_data = _require_mapping(payload, "observation_noise")
    geometry_data = _require_mapping(payload, "geometry_randomization")
    perturbation_data = _require_mapping(payload, "external_perturbation")
    curriculum_data = _require_mapping(payload, "curriculum")
    evaluation_data = _require_mapping(payload, "evaluation")

    cfg = RobustGraspEnvCfg(
        training=TrainingCfg(
            headless=bool(training_data.get("headless", True)),
            device=str(training_data.get("device", "cuda:0")),
            num_envs=int(training_data.get("num_envs", 32)),
            num_training_episodes=int(training_data.get("num_training_episodes", 600)),
            max_episode_steps=int(training_data.get("max_episode_steps", 200)),
            seed=int(training_data.get("seed", 42)),
            output_dir=str(training_data.get("output_dir", "outputs/lab_04")),
            vanilla_range_scale=float(training_data.get("vanilla_range_scale", 0.2)),
        ),
        physics_randomization=PhysicsRandomizationCfg(
            mass_kg_range=_as_range_cfg(physics_data["mass_kg_range"], "physics_randomization.mass_kg_range"),
            friction_range=_as_range_cfg(physics_data["friction_range"], "physics_randomization.friction_range"),
            joint_damping_scale_range=_as_range_cfg(
                physics_data["joint_damping_scale_range"], "physics_randomization.joint_damping_scale_range"
            ),
            actuator_stiffness_scale_range=_as_range_cfg(
                physics_data["actuator_stiffness_scale_range"],
                "physics_randomization.actuator_stiffness_scale_range",
            ),
        ),
        observation_noise=ObservationNoiseCfg(
            joint_pos_std_rad=float(noise_data.get("joint_pos_std_rad", 0.01)),
            joint_vel_std_rad_s=float(noise_data.get("joint_vel_std_rad_s", 0.05)),
            object_pose_std_m=float(noise_data.get("object_pose_std_m", 0.005)),
        ),
        geometry_randomization=GeometryRandomizationCfg(
            object_types=_as_string_tuple(geometry_data["object_types"], "geometry_randomization.object_types"),
            size_m_range=_as_range_cfg(geometry_data["size_m_range"], "geometry_randomization.size_m_range"),
        ),
        external_perturbation=ExternalPerturbationCfg(
            interval_steps=int(perturbation_data.get("interval_steps", 50)),
            force_n_range=_as_range_cfg(perturbation_data["force_n_range"], "external_perturbation.force_n_range"),
        ),
        curriculum=CurriculumCfg(
            success_window=int(curriculum_data.get("success_window", 100)),
            widen_threshold=float(curriculum_data.get("widen_threshold", 0.8)),
            narrow_threshold=float(curriculum_data.get("narrow_threshold", 0.5)),
            adjust_factor=float(curriculum_data.get("adjust_factor", 0.1)),
            min_scale=float(curriculum_data.get("min_scale", 0.6)),
            max_scale=float(curriculum_data.get("max_scale", 2.8)),
        ),
        evaluation=EvaluationCfg(
            episodes_per_config=int(evaluation_data.get("episodes_per_config", 100)),
            chart_filename=str(evaluation_data.get("chart_filename", "robustness_comparison.svg")),
            dr_policy_name=str(evaluation_data.get("dr_policy_name", "domain_randomized")),
            vanilla_policy_name=str(evaluation_data.get("vanilla_policy_name", "vanilla_lab03")),
        ),
    )
    _validate_lab04_config(cfg)
    return cfg


def _validate_lab04_config(cfg: RobustGraspEnvCfg) -> None:
    if not cfg.training.headless:
        raise ConfigError("Lab 04 must use headless mode on the local profile")
    if cfg.training.num_envs <= 0 or cfg.training.num_envs > 64:
        raise ConfigError("training.num_envs must be between 1 and 64 for the local profile")
    if cfg.training.num_training_episodes < cfg.curriculum.success_window:
        raise ConfigError("training.num_training_episodes must cover at least one curriculum window")
    if cfg.external_perturbation.interval_steps <= 0:
        raise ConfigError("external_perturbation.interval_steps must be > 0")
    if len(cfg.geometry_randomization.object_types) < 2:
        raise ConfigError("geometry_randomization.object_types must contain at least two object types")
    if cfg.evaluation.episodes_per_config <= 0:
        raise ConfigError("evaluation.episodes_per_config must be > 0")


def _require_mapping(payload: dict[str, Any], key: str) -> dict[str, Any]:
    value = payload.get(key)
    if not isinstance(value, dict):
        raise ConfigError(f"Missing required mapping: {key}")
    return value


def _as_range_cfg(raw: Sequence[Any], field_name: str) -> RangeCfg:
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)) or len(raw) != 2:
        raise ConfigError(f"{field_name} must be a sequence with exactly two values")
    min_value = float(raw[0])
    max_value = float(raw[1])
    if min_value >= max_value:
        raise ConfigError(f"{field_name} must have min < max")
    return RangeCfg(min_value=min_value, max_value=max_value)


def _as_string_tuple(raw: Sequence[Any], field_name: str) -> tuple[str, ...]:
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)) or len(raw) == 0:
        raise ConfigError(f"{field_name} must be a non-empty sequence")
    return tuple(str(value) for value in raw)
