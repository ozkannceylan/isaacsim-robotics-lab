"""Observation helpers for Lab 04."""

from __future__ import annotations

import random
from typing import Mapping

from lab_04_domain_rand.models import EpisodeDomainParams


def build_clean_observation(params: EpisodeDomainParams) -> dict[str, float]:
    """Build a compact clean observation vector summary."""
    return {
        "object_mass_centered": params.mass_kg - 0.175,
        "surface_friction_centered": params.friction - 0.8,
        "damping_centered": params.joint_damping_scale - 1.0,
        "stiffness_centered": params.actuator_stiffness_scale - 1.0,
        "size_centered": params.object_size_m - 0.055,
        "external_force_n": params.external_force_n,
    }


def add_observation_noise(
    clean_observation: Mapping[str, float],
    params: EpisodeDomainParams,
    seed_token: int,
) -> dict[str, float]:
    """Inject deterministic Gaussian-like noise into the observation summary."""
    rng = random.Random(seed_token)
    noisy = dict(clean_observation)
    noisy["joint_pos_noise"] = _gaussian(rng, params.joint_pos_noise_std)
    noisy["joint_vel_noise"] = _gaussian(rng, params.joint_vel_noise_std)
    noisy["object_pose_noise"] = _gaussian(rng, params.object_pose_noise_std)
    noisy["perceived_force_n"] = params.external_force_n + _gaussian(rng, params.object_pose_noise_std * 10.0)
    return noisy


def _gaussian(rng: random.Random, std_dev: float) -> float:
    """Sample a zero-mean Gaussian value."""
    return rng.gauss(0.0, std_dev)
