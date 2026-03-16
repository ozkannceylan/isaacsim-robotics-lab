"""Shared runtime models for Lab 04."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EpisodeDomainParams:
    """Randomized parameters for a single grasp episode."""

    mass_kg: float
    friction: float
    joint_damping_scale: float
    actuator_stiffness_scale: float
    object_type: str
    object_size_m: float
    joint_pos_noise_std: float
    joint_vel_noise_std: float
    object_pose_noise_std: float
    external_force_n: float


@dataclass(frozen=True)
class PolicyProfile:
    """Capability profile used by the deterministic trainer and evaluator."""

    name: str
    supported_object_types: tuple[str, ...]
    mass_tolerance_kg: float
    friction_tolerance: float
    joint_damping_tolerance: float
    actuator_stiffness_tolerance: float
    size_tolerance_m: float
    joint_pos_noise_tolerance: float
    joint_vel_noise_tolerance: float
    object_pose_noise_tolerance: float
    external_force_tolerance_n: float


@dataclass(frozen=True)
class CurriculumSnapshot:
    """Single ADR state snapshot."""

    episode_index: int
    range_scale: float
    rolling_success_rate: float


@dataclass(frozen=True)
class TrainingResult:
    """Training output for one policy profile."""

    policy_profile: PolicyProfile
    curriculum_history: tuple[CurriculumSnapshot, ...]
    mean_success_rate: float
    max_range_scale: float


@dataclass(frozen=True)
class EvaluationScenarioCfg:
    """Evaluation configuration override loaded from YAML."""

    name: str
    mass_multiplier: float
    friction_override: float | None
    observation_noise_scale: float
    external_force_scale: float
    allowed_object_types: tuple[str, ...]


@dataclass(frozen=True)
class EvaluationResult:
    """Aggregated policy comparison for a single evaluation config."""

    config_name: str
    dr_success_rate: float
    vanilla_success_rate: float
    dr_mean_reward: float
    vanilla_mean_reward: float
