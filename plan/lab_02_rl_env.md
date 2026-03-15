# Lab 02: RL Environment Design

## Objectives

- Understand Isaac Lab's environment abstraction: Direct vs Manager-based workflows
- Build a custom RL environment from scratch (not just run examples)
- Design observation space, action space, reward function, and termination criteria
- Train a PPO agent via SKRL on the custom environment
- Analyze training with TensorBoard: reward curves, episode length, value loss

## Prerequisites

- Lab 01 complete (Isaac Sim + Lab installed, API familiarity)
- Reinforcement learning fundamentals (MDP, policy gradient, PPO)
- Understanding of gymnasium API (obs, action, reward, done, info)

## Capstone Demo

A custom Cartpole-v2 environment with:
1. Modified physics (heavier pole, friction, wind disturbance)
2. Custom reward shaping (not just binary alive/dead)
3. Curriculum: pole starts near vertical, gradually increases initial angle range
4. Trained PPO agent balancing for 1000+ steps consistently
5. TensorBoard dashboard showing learning progression

## Theory

### Isaac Lab Environment Types

**Direct Workflow:**
- Single Python class inherits from `DirectRLEnv`
- All logic (obs, rewards, resets) in one file
- Best for: simple tasks, learning the system, full control

**Manager-Based Workflow:**
- Modular: separate `ObservationManager`, `RewardManager`, `TerminationManager`, `CurriculumManager`
- Config-driven: swap components via `ManagerBasedRLEnvCfg`
- Best for: complex tasks, reusability, research iteration

**This lab uses Direct workflow** to understand everything from first principles.

### Vectorized Environment Design
- Isaac Lab runs N copies of the environment in parallel on GPU
- Observations are tensors of shape `(num_envs, obs_dim)`
- Actions are tensors of shape `(num_envs, act_dim)`
- Resets happen per-env (selective reset), not global
- Key: no Python loops over environments — everything is batched tensor ops

### Reward Engineering
- Dense vs sparse rewards
- Reward scaling and normalization
- Common pitfalls: reward hacking, local optima, reward explosion
- This lab implements: alive bonus + angle penalty + velocity penalty + energy penalty

## Architecture

```
lab_02_rl_env/
├── __init__.py                      # gym.register() call
├── cartpole_v2_env.py               # DirectRLEnv subclass
│   ├── __init__()                   # Scene setup, spaces
│   ├── _setup_scene()               # Spawn cartpole articulation
│   ├── _pre_physics_step()          # Apply actions to sim
│   ├── _get_observations()          # Build obs tensor
│   ├── _get_rewards()               # Compute reward tensor
│   ├── _get_dones()                 # Termination conditions
│   ├── _reset_idx()                 # Per-env selective reset
│   └── _apply_curriculum()          # Increase difficulty over time
├── cartpole_v2_env_cfg.py           # Environment configuration
│   ├── CartpoleV2SceneCfg           # Scene: cartpole + ground
│   ├── CartpoleV2EnvCfg             # Env params: obs/act dims, reward weights
│   └── PPORunnerCfg                 # Training hyperparameters
└── agents/
    └── skrl_ppo_cfg.py              # SKRL PPO agent config
```

## Implementation Notes for Claude Code

### Phase 1: Direct Env Scaffold
- Subclass `DirectRLEnv`
- Define `cfg: CartpoleV2EnvCfg` dataclass with all parameters
- Implement `_setup_scene()`: spawn cartpole articulation from Isaac Lab built-in asset
- Register via `gym.register(id="IsaacLab-CartpoleV2-Direct-v0", entry_point=...)`

### Phase 2: Observation & Action Space
- **Observations (dim=6):**
  - Cart position, cart velocity
  - Pole angle (sin, cos), pole angular velocity
  - Applied force (previous action)
- **Actions (dim=1):**
  - Continuous force on cart joint, clipped to [-10, 10] N
- All as PyTorch tensors on GPU, shape `(num_envs, dim)`

### Phase 3: Reward Function
```
reward = (
    w_alive * alive_bonus           # +1.0 per step while pole is up
  + w_angle * angle_penalty         # -1.0 * (angle / max_angle)^2
  + w_cart  * cart_penalty           # -0.5 * (cart_pos / max_cart)^2
  + w_vel   * velocity_penalty       # -0.1 * pole_angular_vel^2
  + w_energy * energy_penalty        # -0.01 * action^2
)
```
- All weights configurable via `CartpoleV2EnvCfg`
- Reward computed as batched tensor ops (no loops)

### Phase 4: Termination & Reset
- **Termination conditions:**
  - Pole angle > 0.4 rad (~23 degrees)
  - Cart position > 2.5 m from center
  - Episode length > 1000 steps (truncation)
- **Reset:**
  - `_reset_idx(env_ids)` receives tensor of env indices that need reset
  - Randomize initial cart position: uniform(-0.5, 0.5)
  - Randomize initial pole angle: uniform(-0.1, 0.1) (curriculum will widen this)

### Phase 5: Curriculum
- After mean reward > threshold, increase initial angle range
- Stage 1: uniform(-0.1, 0.1) → Stage 2: (-0.2, 0.2) → Stage 3: (-0.3, 0.3)
- Log curriculum stage to TensorBoard

### Phase 6: Training
- Use SKRL PPO with default hyperparameters
- Train headless: `isaaclab -p scripts/train.py --task IsaacLab-CartpoleV2-Direct-v0 --headless --num_envs 64`
- Local: 64 envs, ~2000 iterations
- Log to TensorBoard in `outputs/lab_02/`

### Critical Constraints
- Every method receives/returns tensors on `self.device` — never move to CPU
- `_reset_idx()` must ONLY reset the envs in `env_ids`, not all envs
- Reward tensor must be shape `(num_envs,)` not `(num_envs, 1)`
- Observation tensor shape must match `self.cfg.observation_space`
- gym.register must be called in `__init__.py` at import time

## Success Criteria

| Metric | Target |
|--------|--------|
| Custom env registered and loads without errors | Pass |
| PPO trains and reward curve trends upward | Pass |
| Mean reward > 800 after 1500 iterations (64 envs) | Pass |
| Curriculum progresses through all 3 stages | Pass |
| TensorBoard shows reward, episode length, curriculum stage | Pass |
| No CPU-GPU data transfers in hot loop | Pass |

## References

- [Isaac Lab — Creating Direct RL Env](https://isaac-sim.github.io/IsaacLab/main/source/tutorials/03_envs/create_direct_rl_env.html)
- [Isaac Lab — Creating Manager-Based RL Env](https://isaac-sim.github.io/IsaacLab/main/source/tutorials/03_envs/create_manager_rl_env.html)
- [Isaac Lab — Training with RL Agent](https://isaac-sim.github.io/IsaacLab/main/source/tutorials/03_envs/run_rl_training.html)
- [SKRL Documentation](https://skrl.readthedocs.io/)
