"""Deterministic training scaffold for Lab 04."""

from __future__ import annotations

from collections import deque
from dataclasses import replace

from lab_04_domain_rand.models import CurriculumSnapshot, PolicyProfile, TrainingResult
from lab_04_domain_rand.robust_grasp.mdp.events import sample_episode_batch
from lab_04_domain_rand.robust_grasp.mdp.observations import add_observation_noise, build_clean_observation
from lab_04_domain_rand.robust_grasp.mdp.rewards import evaluate_episode
from lab_04_domain_rand.robust_grasp.robust_grasp_env_cfg import RobustGraspEnvCfg


def train_vanilla_policy(cfg: RobustGraspEnvCfg) -> TrainingResult:
    """Train the nominal baseline policy profile without ADR."""
    policy = PolicyProfile(
        name=cfg.evaluation.vanilla_policy_name,
        supported_object_types=("cube",),
        mass_tolerance_kg=0.05,
        friction_tolerance=0.22,
        joint_damping_tolerance=0.16,
        actuator_stiffness_tolerance=0.12,
        size_tolerance_m=0.011,
        joint_pos_noise_tolerance=0.005,
        joint_vel_noise_tolerance=0.025,
        object_pose_noise_tolerance=0.003,
        external_force_tolerance_n=0.7,
    )
    success_rates: list[float] = []
    snapshots: list[CurriculumSnapshot] = []
    for episode_index in range(cfg.training.num_training_episodes):
        batch = sample_episode_batch(
            cfg,
            episode_index=episode_index,
            env_count=cfg.training.num_envs,
            range_scale=cfg.training.vanilla_range_scale,
        )
        success_rate = _evaluate_batch(cfg, policy, batch, episode_index)
        success_rates.append(success_rate)
        snapshots.append(
            CurriculumSnapshot(
                episode_index=episode_index,
                range_scale=cfg.training.vanilla_range_scale,
                rolling_success_rate=success_rate,
            )
        )
    return TrainingResult(
        policy_profile=policy,
        curriculum_history=tuple(snapshots),
        mean_success_rate=round(sum(success_rates) / len(success_rates), 6),
        max_range_scale=cfg.training.vanilla_range_scale,
    )


def train_domain_randomized_policy(cfg: RobustGraspEnvCfg) -> TrainingResult:
    """Train the domain-randomized policy with ADR."""
    policy = PolicyProfile(
        name=cfg.evaluation.dr_policy_name,
        supported_object_types=cfg.geometry_randomization.object_types,
        mass_tolerance_kg=0.09,
        friction_tolerance=0.34,
        joint_damping_tolerance=0.2,
        actuator_stiffness_tolerance=0.16,
        size_tolerance_m=0.016,
        joint_pos_noise_tolerance=0.008,
        joint_vel_noise_tolerance=0.04,
        object_pose_noise_tolerance=0.0045,
        external_force_tolerance_n=1.0,
    )
    window = deque(maxlen=cfg.curriculum.success_window)
    snapshots: list[CurriculumSnapshot] = []
    success_rates: list[float] = []
    current_scale = 1.0
    max_scale = current_scale

    for episode_index in range(cfg.training.num_training_episodes):
        batch = sample_episode_batch(cfg, episode_index, cfg.training.num_envs, current_scale)
        success_rate = _evaluate_batch(cfg, policy, batch, episode_index)
        success_rates.append(success_rate)
        window.append(success_rate)
        rolling_success = sum(window) / len(window)
        policy = _improve_policy(policy, current_scale)
        if len(window) == window.maxlen:
            if rolling_success > cfg.curriculum.widen_threshold:
                current_scale = min(cfg.curriculum.max_scale, current_scale * (1.0 + cfg.curriculum.adjust_factor))
            elif rolling_success < cfg.curriculum.narrow_threshold:
                current_scale = max(cfg.curriculum.min_scale, current_scale * (1.0 - cfg.curriculum.adjust_factor))
        max_scale = max(max_scale, current_scale)
        snapshots.append(
            CurriculumSnapshot(
                episode_index=episode_index,
                range_scale=round(current_scale, 6),
                rolling_success_rate=round(rolling_success, 6),
            )
        )

    return TrainingResult(
        policy_profile=policy,
        curriculum_history=tuple(snapshots),
        mean_success_rate=round(sum(success_rates) / len(success_rates), 6),
        max_range_scale=round(max_scale, 6),
    )


def _evaluate_batch(
    cfg: RobustGraspEnvCfg,
    policy: PolicyProfile,
    batch: tuple,
    episode_index: int,
) -> float:
    successes = 0
    for env_index, params in enumerate(batch):
        clean = build_clean_observation(params)
        noisy = add_observation_noise(clean, params, cfg.training.seed + (episode_index * 1_013) + env_index)
        success, _ = evaluate_episode(policy, params, noisy, cfg.training.max_episode_steps)
        successes += int(success)
    return successes / len(batch)


def _improve_policy(policy: PolicyProfile, current_scale: float) -> PolicyProfile:
    gain = 1.0 + (0.008 * current_scale)
    return replace(
        policy,
        mass_tolerance_kg=policy.mass_tolerance_kg * gain,
        friction_tolerance=policy.friction_tolerance * gain,
        joint_damping_tolerance=policy.joint_damping_tolerance * (1.0 + 0.005 * current_scale),
        actuator_stiffness_tolerance=policy.actuator_stiffness_tolerance * (1.0 + 0.004 * current_scale),
        size_tolerance_m=policy.size_tolerance_m * gain,
        joint_pos_noise_tolerance=policy.joint_pos_noise_tolerance * gain,
        joint_vel_noise_tolerance=policy.joint_vel_noise_tolerance * gain,
        object_pose_noise_tolerance=policy.object_pose_noise_tolerance * gain,
        external_force_tolerance_n=policy.external_force_tolerance_n * (1.0 + 0.01 * current_scale),
    )
