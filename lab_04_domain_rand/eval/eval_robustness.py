"""Robustness evaluation for Lab 04."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import yaml

from lab_04_domain_rand.models import EvaluationResult, EvaluationScenarioCfg, PolicyProfile
from lab_04_domain_rand.robust_grasp.mdp.events import sample_episode_batch
from lab_04_domain_rand.robust_grasp.mdp.observations import add_observation_noise, build_clean_observation
from lab_04_domain_rand.robust_grasp.mdp.rewards import evaluate_episode
from lab_04_domain_rand.robust_grasp.robust_grasp_env_cfg import RobustGraspEnvCfg


def load_evaluation_configs(config_dir: str | Path) -> tuple[EvaluationScenarioCfg, ...]:
    """Load evaluation scenario overrides from YAML files."""
    config_path = Path(config_dir)
    configs: list[EvaluationScenarioCfg] = []
    for path in sorted(config_path.glob("*.yaml")):
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        configs.append(
            EvaluationScenarioCfg(
                name=str(payload["name"]),
                mass_multiplier=float(payload.get("mass_multiplier", 1.0)),
                friction_override=_optional_float(payload.get("friction_override")),
                observation_noise_scale=float(payload.get("observation_noise_scale", 1.0)),
                external_force_scale=float(payload.get("external_force_scale", 1.0)),
                allowed_object_types=tuple(str(value) for value in payload.get("allowed_object_types", ("cube",))),
            )
        )
    return tuple(configs)


def evaluate_policies(
    cfg: RobustGraspEnvCfg,
    dr_policy: PolicyProfile,
    vanilla_policy: PolicyProfile,
    eval_configs: Iterable[EvaluationScenarioCfg],
) -> tuple[EvaluationResult, ...]:
    """Evaluate the DR and vanilla policies on each fixed evaluation config."""
    results: list[EvaluationResult] = []
    for config_index, eval_cfg in enumerate(eval_configs):
        dr_successes = 0
        vanilla_successes = 0
        dr_reward_sum = 0.0
        vanilla_reward_sum = 0.0

        batch = sample_episode_batch(
            cfg,
            episode_index=10_000 + config_index,
            env_count=cfg.evaluation.episodes_per_config,
            range_scale=1.0,
            eval_override=eval_cfg,
        )
        for env_index, params in enumerate(batch):
            seed_token = cfg.training.seed + (config_index * 1000) + env_index
            noisy = add_observation_noise(build_clean_observation(params), params, seed_token)
            dr_success, dr_reward = evaluate_episode(dr_policy, params, noisy, cfg.training.max_episode_steps)
            vanilla_success, vanilla_reward = evaluate_episode(
                vanilla_policy, params, noisy, cfg.training.max_episode_steps
            )
            dr_successes += int(dr_success)
            vanilla_successes += int(vanilla_success)
            dr_reward_sum += dr_reward
            vanilla_reward_sum += vanilla_reward

        episode_count = cfg.evaluation.episodes_per_config
        results.append(
            EvaluationResult(
                config_name=eval_cfg.name,
                dr_success_rate=round(dr_successes / episode_count, 6),
                vanilla_success_rate=round(vanilla_successes / episode_count, 6),
                dr_mean_reward=round(dr_reward_sum / episode_count, 6),
                vanilla_mean_reward=round(vanilla_reward_sum / episode_count, 6),
            )
        )
    return tuple(results)


def _optional_float(value: object) -> float | None:
    return None if value is None else float(value)
