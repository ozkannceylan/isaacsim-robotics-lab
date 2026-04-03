# Isaac Lab vs MuJoCo/Gymnasium: Workflow Comparison

## Overview

This document compares the RL workflow between Isaac Lab (GPU-parallelized, manager-based) and MuJoCo/Gymnasium (CPU, single-env or vectorized). Based on hands-on experience from both `mujoco-robotics-lab` and this Isaac Sim lab.

## Architecture Comparison

| Aspect | MuJoCo / Gymnasium | Isaac Lab |
|--------|-------------------|-----------|
| Physics engine | MuJoCo (CPU) | PhysX 5 (GPU) |
| Parallelism | `SubprocVecEnv` (multi-process) | Single GPU, thousands of envs |
| Observation format | NumPy arrays | PyTorch GPU tensors |
| Action format | NumPy arrays | PyTorch GPU tensors |
| Scene description | MJCF XML | USD (Universal Scene Description) |
| Rendering | MuJoCo native (CPU/GL) | RTX ray-tracing (GPU) |
| Environment structure | `gymnasium.Env` subclass | `ManagerBasedRLEnv` with config |
| Reward definition | Manual in `step()` | `RewardManager` with weighted terms |
| Observation definition | Manual in `_get_obs()` | `ObservationManager` with terms |
| Reset logic | Manual in `reset()` | Auto-reset per-env on termination |
| RL framework | Stable Baselines3 (typical) | RL Games, SKRL, RSL-RL |

## Key Paradigm Differences

### 1. No Python Loops Over Environments

**MuJoCo:** Even with `SubprocVecEnv`, each env runs in its own process. Python overhead per env.

**Isaac Lab:** All envs share one PhysX simulation on GPU. Operations are batched tensor ops — no Python loop over individual envs.

### 2. Manager-Based Decomposition

**MuJoCo:** Observations, rewards, and terminations are computed in a single `step()` method.

**Isaac Lab:** Each concern is a separate Manager with independently configurable Terms:
- `ObservationManager` — each term is a function returning a tensor
- `RewardManager` — each term has a weight, computed in parallel
- `TerminationManager` — each term returns a boolean mask

This makes reward engineering much more modular and easier to experiment with.

### 3. Configuration-Driven Design

**MuJoCo:** Environment behavior is defined in Python class methods.

**Isaac Lab:** Behavior is defined in `@configclass` dataclasses. The same env code works with different configs — changing rewards, observations, or actions without modifying the environment class.

### 4. GPU Tensor Pipeline

**MuJoCo:**
```python
obs = env.reset()           # NumPy array
action = policy(obs)        # CPU inference (or GPU → CPU → GPU)
obs, reward, done, info = env.step(action)  # CPU physics
```

**Isaac Lab:**
```python
obs = env.obs_buf            # GPU tensor, never leaves GPU
action = policy(obs)         # GPU inference
env.step(action)             # GPU physics
```

Zero CPU transfers in the hot loop.

## Performance Comparison

*Fill in with actual benchmark data after running experiments.*

| Metric | MuJoCo CartPole | Isaac Lab CartPole |
|--------|----------------|-------------------|
| Steps/sec (1 env) | | |
| Steps/sec (256 envs) | | |
| Steps/sec (2048 envs) | N/A | |
| Wall-clock to convergence | | |
| GPU memory usage | None | |

## When to Use Which

| Use Case | Recommended |
|----------|-------------|
| Quick prototyping, simple envs | MuJoCo/Gymnasium |
| Large-scale RL training | Isaac Lab |
| Photorealistic rendering | Isaac Lab (RTX) |
| Custom analytical robotics (FK, IK, dynamics) | MuJoCo + Pinocchio |
| Domain randomization at scale | Isaac Lab |
| Sim-to-real with sensor simulation | Isaac Lab |
| Education and learning RL basics | MuJoCo/Gymnasium |

## RL Framework Comparison (Isaac Lab)

*Fill in after running compare_frameworks.sh.*

| Framework | Steps/sec | API Style | Best For |
|-----------|-----------|-----------|----------|
| RL Games | | YAML config | Production training, speed |
| SKRL | | Python API | Customization, research |
