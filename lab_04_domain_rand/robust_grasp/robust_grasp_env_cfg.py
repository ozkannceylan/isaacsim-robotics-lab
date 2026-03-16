"""Typed environment configuration for Lab 04."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RangeCfg:
    """Closed interval randomization range."""

    min_value: float
    max_value: float

    def scaled_about_center(self, scale: float) -> "RangeCfg":
        """Scale the range span around its midpoint."""
        center = (self.min_value + self.max_value) * 0.5
        half_span = (self.max_value - self.min_value) * 0.5 * scale
        return RangeCfg(min_value=center - half_span, max_value=center + half_span)


@dataclass(frozen=True)
class TrainingCfg:
    """Training/runtime settings for the deterministic scaffold."""

    headless: bool
    device: str
    num_envs: int
    num_training_episodes: int
    max_episode_steps: int
    seed: int
    output_dir: str
    vanilla_range_scale: float


@dataclass(frozen=True)
class PhysicsRandomizationCfg:
    """Physics-domain randomization ranges."""

    mass_kg_range: RangeCfg
    friction_range: RangeCfg
    joint_damping_scale_range: RangeCfg
    actuator_stiffness_scale_range: RangeCfg


@dataclass(frozen=True)
class ObservationNoiseCfg:
    """Observation-noise parameters applied after clean observation assembly."""

    joint_pos_std_rad: float
    joint_vel_std_rad_s: float
    object_pose_std_m: float


@dataclass(frozen=True)
class GeometryRandomizationCfg:
    """Object-type and size randomization settings."""

    object_types: tuple[str, ...]
    size_m_range: RangeCfg


@dataclass(frozen=True)
class ExternalPerturbationCfg:
    """Interval-force perturbation settings."""

    interval_steps: int
    force_n_range: RangeCfg


@dataclass(frozen=True)
class CurriculumCfg:
    """Automatic domain-randomization curriculum settings."""

    success_window: int
    widen_threshold: float
    narrow_threshold: float
    adjust_factor: float
    min_scale: float
    max_scale: float


@dataclass(frozen=True)
class EvaluationCfg:
    """Evaluation/report settings."""

    episodes_per_config: int
    chart_filename: str
    dr_policy_name: str
    vanilla_policy_name: str


@dataclass(frozen=True)
class RobustGraspEnvCfg:
    """Top-level Lab 04 config bundle."""

    training: TrainingCfg
    physics_randomization: PhysicsRandomizationCfg
    observation_noise: ObservationNoiseCfg
    geometry_randomization: GeometryRandomizationCfg
    external_perturbation: ExternalPerturbationCfg
    curriculum: CurriculumCfg
    evaluation: EvaluationCfg
