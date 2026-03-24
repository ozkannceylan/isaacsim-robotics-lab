# Lab 03: RL Arm Control

## Objectives

- Transition from Direct to Manager-Based workflow
- Design a reach + grasp RL task for a 6-DOF manipulator
- Implement structured observation, action, and reward managers
- Train an RL agent to reach a target pose and grasp an object
- Understand contact-rich physics: grasp stability, condim, solver params

## Prerequisites

- Lab 02 complete (custom RL env, PPO training pipeline)
- Understanding of task-space vs joint-space control
- Basic grasp mechanics (antipodal grasps, force closure)

## Capstone Demo

Two trained policies:
1. **Reach:** Franka Panda reaches arbitrary 3D target positions (success > 90%)
2. **Grasp:** Franka Panda picks up a cube from a table (success > 70%)

Both policies trained headless on local RTX 4050 with ≤64 envs.

## Theory

### Manager-Based Workflow
- **ObservationManager** — defines observation groups (policy, critic, privileged)
- **ActionManager** — maps RL actions to sim commands (joint pos, joint vel, IK)
- **RewardManager** — weighted sum of reward terms, each a separate function
- **TerminationManager** — multiple termination conditions, each with time_out flag
- **CurriculumManager** — modify reward weights or env params during training
- **EventManager** — domain randomization events (startup, reset, interval)

### Action Spaces for Manipulation
- **Joint position delta** — action = Δq, applied as q_target = q_current + Δq
- **Joint velocity** — action = q_dot, applied directly
- **IK-based** — action = (Δx, Δy, Δz, Δroll, Δpitch, Δyaw) in task space, IK solver computes joints
- **This lab uses joint position delta** for reach, IK-based for grasp

### Reward Design for Manipulation
- **Distance reward** — negative L2 distance to target (dense)
- **Orientation reward** — alignment between gripper and target orientation
- **Grasp reward** — contact force between fingers and object
- **Lift reward** — object height above table (sparse but critical)
- **Action penalty** — smooth actions preferred

## Architecture

```
lab_03_arm_control/
├── __init__.py
├── reach/
│   ├── __init__.py                    # gym.register for reach task
│   ├── reach_env_cfg.py               # ManagerBasedRLEnvCfg
│   │   ├── ReachSceneCfg              # Franka + table + target marker
│   │   ├── ObservationsCfg            # Joint pos/vel + target pos
│   │   ├── ActionsCfg                 # Joint position delta
│   │   ├── RewardsCfg                 # Distance + action penalty
│   │   ├── TerminationsCfg            # Success + timeout + out-of-bounds
│   │   └── CurriculumCfg             # Target distance range expansion
│   └── mdp/                           # Custom MDP terms
│       ├── observations.py
│       ├── rewards.py
│       └── terminations.py
├── grasp/
│   ├── __init__.py                    # gym.register for grasp task
│   ├── grasp_env_cfg.py               # ManagerBasedRLEnvCfg
│   │   ├── GraspSceneCfg             # Franka + table + cube
│   │   ├── ObservationsCfg            # Joint state + cube pose + contact
│   │   ├── ActionsCfg                 # IK delta + gripper binary
│   │   ├── RewardsCfg                 # Approach + grasp + lift
│   │   └── TerminationsCfg
│   └── mdp/
│       ├── observations.py
│       ├── rewards.py
│       └── terminations.py
└── agents/
    └── skrl_ppo_cfg.py
```

## Implementation Notes for Claude Code

### Phase 1: Reach Task (Manager-Based)
- Scene: Franka Panda on table + visual target sphere
- Observation group "policy": `[joint_pos_rel, joint_vel, target_pos_body]` (dim ~15)
- Action: `JointPositionActionCfg` with delta mode, 7 DOF
- Rewards:
  - `reaching_target`: `-distance * 1.0` (dense)
  - `action_rate`: `-action_diff^2 * 0.01`
  - `success_bonus`: `+5.0` when distance < 0.02
- Termination: `time_out` at 200 steps, `success` when distance < 0.02
- Target randomized in hemisphere in front of robot

### Phase 2: Grasp Task
- Scene: Franka Panda + table + cube (5cm, 100g)
- Observation: joint state + cube pose + relative cube-to-gripper vector
- Action: IK delta (6D) + gripper open/close (1D binary threshold)
- Reward phases:
  1. **Approach** — decrease gripper-to-cube distance
  2. **Align** — gripper orientation reward (fingers parallel to cube face)
  3. **Grasp** — contact force between both fingers and cube
  4. **Lift** — cube height above initial position
- Use `condim=3` for friction contacts, tune `solref` for grasp stability

### Phase 3: Physics Tuning
- PhysX solver: `num_position_iterations=8, num_velocity_iterations=2`
- Contact: `contact_offset=0.02, rest_offset=0.001`
- Cube: `static_friction=1.0, dynamic_friction=0.8`
- If cube slips: increase friction, decrease solver dt, increase substeps

### Critical Constraints
- Manager-based env: rewards/obs/terms are SEPARATE functions, not one monolith
- Each reward term receives `(env, **kwargs)` and returns `(num_envs,)` tensor
- IK solver must run on GPU — use Isaac Lab's built-in `DifferentialIKController`
- Gripper action: threshold continuous output → binary open/close
- Cube spawning: randomize position on table within reachable workspace

## Success Criteria

| Metric | Target |
|--------|--------|
| Reach: success rate > 90% (distance < 2cm) | Pass |
| Reach: mean episode reward > 150 | Pass |
| Grasp: success rate > 70% (cube lifted > 5cm) | Pass |
| Grasp: stable hold for 30+ steps after lift | Pass |
| Both tasks train on local RTX 4050 (64 envs, headless) | Pass |
| VRAM usage during training | < 5.5 GB |
| Training time: Reach < 30 min, Grasp < 90 min | Pass |

## References

- [Isaac Lab — Manager-Based RL Env Tutorial](https://isaac-sim.github.io/IsaacLab/main/source/tutorials/03_envs/create_manager_rl_env.html)
- [Isaac Lab — Franka Reach Example](https://isaac-sim.github.io/IsaacLab/main/source/overview/environments.html)
- [Isaac Lab — Differential IK Controller](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.controllers.html)
- [PhysX Contact Parameters](https://docs.isaacsim.omniverse.nvidia.com/latest/reference_material/physics_settings.html)
