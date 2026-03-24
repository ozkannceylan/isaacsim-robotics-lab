"""Deterministic randomization-event sampling for Lab 04."""

from __future__ import annotations

import random

from lab_04_domain_rand.models import EpisodeDomainParams, EvaluationScenarioCfg
from lab_04_domain_rand.robust_grasp.robust_grasp_env_cfg import RobustGraspEnvCfg


def sample_episode_batch(
    cfg: RobustGraspEnvCfg,
    episode_index: int,
    env_count: int,
    range_scale: float,
    eval_override: EvaluationScenarioCfg | None = None,
) -> tuple[EpisodeDomainParams, ...]:
    """Sample a deterministic batch of randomized episode parameters."""
    physics = cfg.physics_randomization
    noise = cfg.observation_noise
    geometry = cfg.geometry_randomization
    perturbation = cfg.external_perturbation

    mass_range = physics.mass_kg_range.scaled_about_center(range_scale)
    friction_range = physics.friction_range.scaled_about_center(range_scale)
    damping_range = physics.joint_damping_scale_range.scaled_about_center(range_scale)
    stiffness_range = physics.actuator_stiffness_scale_range.scaled_about_center(range_scale)
    size_range = geometry.size_m_range.scaled_about_center(range_scale)
    force_range = perturbation.force_n_range.scaled_about_center(range_scale)

    object_types = eval_override.allowed_object_types if eval_override is not None else geometry.object_types
    samples: list[EpisodeDomainParams] = []
    for env_index in range(env_count):
        rng = random.Random(cfg.training.seed + (episode_index * 10_003) + env_index)
        params = EpisodeDomainParams(
            mass_kg=rng.uniform(mass_range.min_value, mass_range.max_value),
            friction=rng.uniform(friction_range.min_value, friction_range.max_value),
            joint_damping_scale=rng.uniform(damping_range.min_value, damping_range.max_value),
            actuator_stiffness_scale=rng.uniform(stiffness_range.min_value, stiffness_range.max_value),
            object_type=object_types[rng.randrange(len(object_types))],
            object_size_m=rng.uniform(size_range.min_value, size_range.max_value),
            joint_pos_noise_std=noise.joint_pos_std_rad,
            joint_vel_noise_std=noise.joint_vel_std_rad_s,
            object_pose_noise_std=noise.object_pose_std_m,
            external_force_n=rng.uniform(force_range.min_value, force_range.max_value),
        )
        if eval_override is not None:
            params = apply_evaluation_override(params, eval_override)
        samples.append(params)
    return tuple(samples)


def apply_evaluation_override(
    params: EpisodeDomainParams,
    override: EvaluationScenarioCfg,
) -> EpisodeDomainParams:
    """Apply a fixed evaluation override to sampled episode parameters."""
    friction = override.friction_override if override.friction_override is not None else params.friction
    return EpisodeDomainParams(
        mass_kg=params.mass_kg * override.mass_multiplier,
        friction=friction,
        joint_damping_scale=params.joint_damping_scale,
        actuator_stiffness_scale=params.actuator_stiffness_scale,
        object_type=params.object_type,
        object_size_m=params.object_size_m,
        joint_pos_noise_std=params.joint_pos_noise_std * override.observation_noise_scale,
        joint_vel_noise_std=params.joint_vel_noise_std * override.observation_noise_scale,
        object_pose_noise_std=params.object_pose_noise_std * override.observation_noise_scale,
        external_force_n=params.external_force_n * override.external_force_scale,
    )
