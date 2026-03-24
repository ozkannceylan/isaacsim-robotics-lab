"""SKRL PPO configuration scaffold for Lab 04."""

from __future__ import annotations

from dataclasses import dataclass

from lab_04_domain_rand.robust_grasp.robust_grasp_env_cfg import TrainingCfg


@dataclass(frozen=True)
class SkrlPpoCfg:
    """Compact PPO config matching the local-headless Lab 04 profile."""

    learning_rate: float
    rollout_length: int
    minibatches: int
    epochs: int
    gamma: float
    gae_lambda: float
    clip_range: float
    headless: bool
    num_envs: int


def build_local_ppo_cfg(training: TrainingCfg) -> SkrlPpoCfg:
    """Return a reproducible PPO config for the local training profile."""
    return SkrlPpoCfg(
        learning_rate=3.0e-4,
        rollout_length=64,
        minibatches=4,
        epochs=5,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        headless=training.headless,
        num_envs=training.num_envs,
    )
