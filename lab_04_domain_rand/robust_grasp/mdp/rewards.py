"""Episode scoring and reward estimation for Lab 04."""

from __future__ import annotations

from typing import Mapping

from lab_04_domain_rand.models import EpisodeDomainParams, PolicyProfile


def evaluate_episode(
    policy: PolicyProfile,
    params: EpisodeDomainParams,
    noisy_observation: Mapping[str, float],
    max_episode_steps: int,
) -> tuple[bool, float]:
    """Compute a deterministic success flag and reward for one episode."""
    type_bonus = 0.15 if params.object_type in policy.supported_object_types else -0.7
    score = 2.35 + type_bonus
    score -= 0.9 * abs(params.mass_kg - 0.175) / policy.mass_tolerance_kg
    score -= 0.95 * abs(params.friction - 0.8) / policy.friction_tolerance
    score -= 0.2 * abs(params.joint_damping_scale - 1.0) / policy.joint_damping_tolerance
    score -= 0.15 * abs(params.actuator_stiffness_scale - 1.0) / policy.actuator_stiffness_tolerance
    score -= 0.7 * abs(params.object_size_m - 0.055) / policy.size_tolerance_m
    score -= 0.55 * params.external_force_n / policy.external_force_tolerance_n
    score -= 0.45 * abs(float(noisy_observation["joint_pos_noise"])) / policy.joint_pos_noise_tolerance
    score -= 0.3 * abs(float(noisy_observation["joint_vel_noise"])) / policy.joint_vel_noise_tolerance
    score -= 0.5 * abs(float(noisy_observation["object_pose_noise"])) / policy.object_pose_noise_tolerance

    reward = 1.2 + score - (max_episode_steps * 0.001)
    return score > 0.0, round(reward, 6)
