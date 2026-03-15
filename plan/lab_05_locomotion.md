# Lab 05: Bipedal Locomotion

## Objectives

- Transition from fixed-base manipulation to floating-base locomotion
- Understand the paradigm shift: balance, foot contact, gait generation
- Train G1 humanoid to walk on flat and rough terrain via RL
- Use RSL-RL (industry standard for legged locomotion)
- Run training on Lambda Labs (512+ parallel envs required)

## Prerequisites

- Lab 04 complete (DR, robust policies, Manager-Based workflow)
- Understanding of floating-base dynamics, ZMP, contact scheduling
- Lambda Labs account + SSH access configured
- MuJoCo Lab 7 concepts helpful but not required

## Capstone Demo

Unitree G1 humanoid:
1. Stands up from initial pose and self-balances
2. Walks forward at commanded velocity (0.5 m/s)
3. Turns left/right on command
4. Walks on rough terrain (height field with 2cm perturbations)
5. Recovers from moderate push perturbation

## Theory

### Fixed-Base vs Floating-Base
- Fixed-base: robot bolted to world, only joints move
- Floating-base: robot base is free, 6 DOF added (position + orientation)
- Consequence: all motion must be dynamically balanced, no "cheating" with a fixed anchor
- Under-actuation: you cannot directly control base position — only through contact forces

### Locomotion RL Formulation
- **Observation:** base orientation (projected gravity), base angular velocity, joint positions, joint velocities, previous action, velocity command
- **Action:** target joint positions for all leg joints (PD controller tracks them)
- **Reward:** velocity tracking + orientation stability + gait regularity + energy efficiency

### Reward Terms for Walking (standard formulation)
- `lin_vel_tracking`: reward for matching commanded x/y velocity
- `ang_vel_tracking`: reward for matching commanded yaw rate
- `base_height`: penalty for base too low or too high
- `orientation`: penalty for base tilting (projected gravity deviation)
- `joint_torque`: energy penalty
- `action_rate`: smoothness penalty
- `feet_air_time`: encourage periodic foot lifting (gait emergence)
- `foot_contact_force`: limit impact forces
- `joint_limit`: penalty for approaching joint limits

### Terrain Curriculum
- Start on flat ground
- As performance improves: add height field noise, slopes, steps
- Isaac Lab provides `TerrainImporterCfg` with procedural generation

## Architecture

```
lab_05_locomotion/
├── __init__.py
├── g1_walk/
│   ├── __init__.py
│   ├── g1_walk_env_cfg.py
│   │   ├── G1WalkSceneCfg              # G1 + terrain
│   │   ├── ObservationsCfg              # Proprioception + commands
│   │   ├── ActionsCfg                   # Joint position targets (legs only)
│   │   ├── RewardsCfg                   # Locomotion reward terms
│   │   ├── TerminationsCfg              # Fall detection, timeout
│   │   ├── CurriculumCfg               # Terrain difficulty progression
│   │   ├── EventsCfg                    # Push perturbation, physics rand
│   │   └── CommandsCfg                  # Velocity commands (vx, vy, yaw_rate)
│   └── mdp/
│       ├── observations.py
│       ├── rewards.py                   # Locomotion-specific rewards
│       ├── terminations.py
│       ├── commands.py                  # Velocity command generator
│       └── events.py                    # Push perturbation
├── terrain/
│   ├── terrain_cfg.py                   # Terrain generation configs
│   └── terrain_utils.py                 # Height field generators
└── agents/
    ├── rsl_rl_ppo_cfg.py               # RSL-RL PPO config
    └── rsl_rl_runner_cfg.py            # Runner config (logging, checkpoints)
```

## Implementation Notes for Claude Code

### Phase 0: Lambda Labs Setup
- SSH into Lambda instance
- Run `scripts/setup_lambda.sh` (NGC login, conda env, Isaac Lab install)
- Clone repo, `pip install -e source/isaacsim_robotics_lab`
- Verify: run Lab 02 Cartpole with 512 envs — confirm GPU utilization

### Phase 1: G1 Robot Configuration
- Use Unitree G1 from Isaac Lab assets (`isaaclab.sim.spawners`)
- Create `robots/g1.py` with `ArticulationCfg`:
  - PD controller gains for each joint group (hip, knee, ankle)
  - Joint limits, default pose (standing)
  - Enable self-collision filtering
- Lock upper body joints initially (arms fixed, only legs active)
- Active joints: 12 (6 per leg: hip_yaw, hip_roll, hip_pitch, knee, ankle_pitch, ankle_roll)

### Phase 2: Standing Balance (sub-task)
- Before walking: train standing balance policy
- Simplified reward: only orientation + height + energy
- No velocity command tracking
- 200 step episodes, 512 envs
- This gives a good initialization for walking policy

### Phase 3: Flat Ground Walking
- Velocity command: sample vx from uniform(0, 1.0), vy=0, yaw_rate=0
- Observation (dim ~48):
  - Projected gravity vector (3)
  - Base angular velocity (3)
  - Joint positions relative to default (12)
  - Joint velocities (12)
  - Previous action (12)
  - Velocity command (3)
  - Phase variable (sin/cos of gait clock) (2)
- Action (dim=12): joint position deltas
- PD controller: `stiffness=40, damping=1.0` (tune per joint group)

### Phase 4: Reward Tuning
- Start with standard locomotion rewards from Isaac Lab examples
- Key weights (starting point, will need tuning):
  - `lin_vel_tracking`: 1.0 (primary objective)
  - `ang_vel_tracking`: 0.5
  - `orientation`: -1.0 (keep upright)
  - `base_height`: -1.0 (target height ~0.68m for G1)
  - `action_rate`: -0.01
  - `joint_torque`: -0.0001
  - `feet_air_time`: 0.5 (encourage stepping)
- Use reward shaping: `exp(-distance/sigma)` for tracking rewards

### Phase 5: Terrain Curriculum
- Stage 1: Flat ground (0-500k steps)
- Stage 2: Gentle noise (height_range=0.02m) (500k-1M steps)
- Stage 3: Rougher terrain (height_range=0.05m) (1M-2M steps)
- Use `TerrainImporterCfg` with `terrain_type="generator"`
- Terrain grid: multiple patches per difficulty level, envs placed on appropriate patches

### Phase 6: Push Recovery
- EventManager at `interval`: apply random force to base
- Force: uniform(0, 50) N, random horizontal direction
- Interval: every 200-500 steps (randomized)
- This forces the policy to be dynamically stable, not just statically balanced

### Training Config (Lambda Labs)
- 512-2048 envs (start with 512, scale up if stable)
- PPO: horizon=24 steps, mini_batches=4, learning_rate=1e-3
- Total steps: 2-5M (expect 2-4 hours on A10G)
- Checkpoint every 500 iterations

### Critical Constraints
- **CLOUD ONLY** — 512 envs with G1 model will NOT fit in 6GB VRAM
- RSL-RL requires specific wrapper: use `RslRlVecEnvWrapper` from `isaaclab_rl`
- G1 has 37 DOF total — lock upper body to 12 active leg DOF for this lab
- Fall detection: base height < 0.3m OR base angle > 1.0 rad
- Physics dt=0.005s, policy dt=0.02s (decimation=4)
- Gravity = -9.81 m/s^2 (verify in sim config)

## Success Criteria

| Metric | Target |
|--------|--------|
| G1 stands and self-balances for 1000+ steps | Pass |
| Flat ground: forward velocity tracking error < 0.1 m/s | Pass |
| Flat ground: walks 10m without falling | Pass |
| Rough terrain: walks 5m on 2cm height noise | Pass |
| Push recovery: survives 30N lateral push | Pass |
| Training: 512+ envs on Lambda A10G | Pass |
| Training time | < 4 hours |

## References

- [Isaac Lab — Anymal Locomotion Example](https://isaac-sim.github.io/IsaacLab/main/source/overview/environments.html)
- [Isaac Lab — Unitree G1 Velocity Task](https://github.com/isaac-sim/IsaacLab)
- [RSL-RL Documentation](https://github.com/leggedrobotics/rsl_rl)
- [HOVER — Neural Whole-Body Controller](https://github.com/NVlabs/HOVER)
- [Rudin et al. — Learning to Walk in Minutes (2022)](https://arxiv.org/abs/2109.11978)
