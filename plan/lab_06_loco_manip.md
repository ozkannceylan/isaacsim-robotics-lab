# Lab 06: Whole-Body Loco-Manipulation

## Objectives

- Unlock G1's upper body: combine locomotion with arm manipulation
- Train a whole-body controller: walk + reach + grasp simultaneously
- Use hierarchical policy architecture: locomotion base + manipulation head
- Implement task-space commands for the hand while walking

## Prerequisites

- Lab 05 complete (G1 walking policy on flat + rough terrain)
- Lab 03 concepts (manipulation, grasp rewards)
- Understanding of hierarchical RL / task decomposition

## Capstone Demo

Unitree G1:
1. Receives command: "walk to position (2, 0) and pick up the cube"
2. Walks to the approximate location
3. Reaches for the cube on a table
4. Grasps and lifts the cube
5. Walks back to origin while carrying the cube

## Theory

### The Integration Challenge
- Locomotion policy controls legs (12 DOF) — trained in Lab 05
- Manipulation needs arms + hands (12+ DOF per arm, 6+ DOF per Dex3 hand)
- Naive approach: one policy controls everything (~40+ DOF) — high-dimensional, hard to train
- Better approach: hierarchical decomposition

### Hierarchical Policy Architecture
```
High-Level Planner
    ├── Walk-to-target command (vx, vy, yaw_rate)
    │       ↓
    │   Locomotion Policy (Lab 05, frozen or fine-tuned)
    │       → Leg joint targets (12 DOF)
    │
    └── Reach-and-grasp command (target_pos, grasp_flag)
            ↓
        Manipulation Policy (trained here)
            → Arm + hand joint targets (12-18 DOF)
```

### Approaches to Whole-Body Control
1. **Frozen legs, train arms** — simplest, legs use Lab 05 policy frozen, only arm policy trained
2. **Joint fine-tuning** — load Lab 05 policy, fine-tune all joints together with manipulation reward
3. **HOVER-style** — NVIDIA's neural whole-body controller approach

**This lab uses approach 1 first (frozen legs), then approach 2 (fine-tuning) as stretch goal.**

## Architecture

```
lab_06_loco_manip/
├── __init__.py
├── walk_and_grasp/
│   ├── __init__.py
│   ├── walk_grasp_env_cfg.py
│   │   ├── WalkGraspSceneCfg         # G1 (full body) + table + cube
│   │   ├── ObservationsCfg            # Proprioception + object pose + commands
│   │   ├── ActionsCfg                 # Arm joints + gripper (legs from frozen policy)
│   │   ├── RewardsCfg
│   │   │   ├── walk_to_target         # Base position tracking
│   │   │   ├── reach_object           # Hand-to-object distance
│   │   │   ├── grasp_reward           # Contact + lift
│   │   │   ├── carry_stability        # Object doesn't drop while walking
│   │   │   └── locomotion_quality     # Don't degrade walking
│   │   ├── TerminationsCfg
│   │   └── EventsCfg                  # Object position randomization
│   └── mdp/
│       ├── observations.py
│       ├── rewards.py
│       ├── actions.py                 # Custom action term: frozen legs + trained arms
│       └── commands.py                # Walk-to-target + grasp commands
├── policies/
│   └── frozen_locomotion.py           # Wrapper to load Lab 05 checkpoint
└── agents/
    └── rsl_rl_ppo_cfg.py
```

## Implementation Notes for Claude Code

### Phase 1: Full-Body G1 Setup
- Unlock all G1 joints: legs (12) + torso (1-3) + arms (12-14) + hands (variable)
- Simplify hands initially: 1 DOF per hand (open/close) instead of full Dex3
- Total active DOF: ~28
- Create `robots/g1_full.py` with all joint groups configured

### Phase 2: Frozen Locomotion Base
- Load Lab 05 checkpoint
- Freeze leg policy: at each step, run Lab 05 policy on leg observation subset → leg targets
- Only train arm/hand policy
- This significantly reduces training complexity

### Phase 3: Arm Manipulation on Walking Robot
- Observation for arm policy:
  - Arm joint positions/velocities (~14)
  - Object pose relative to hand (~6)
  - Gripper state (1)
  - Base velocity (for compensation) (3)
  - Walk command / base target (3)
- Action for arm policy:
  - Arm joint position deltas (6-7 per arm)
  - Gripper open/close (1 per hand)

### Phase 4: Task Sequencing
- The env needs a state machine for the multi-phase task:
  1. **Navigate** — walk toward table (locomotion reward dominant)
  2. **Approach** — slow down near table, extend arm (manipulation reward ramps up)
  3. **Grasp** — stop walking, execute grasp (locomotion reward = stay still)
  4. **Carry** — walk to return point while holding object
- Implement via `CurriculumManager` or explicit phase tracking in env

### Phase 5: Reward Design
```
# Phase-dependent reward weighting
if phase == NAVIGATE:
    reward = 1.0 * walk_to_target + 0.1 * reach_object
elif phase == APPROACH:
    reward = 0.5 * walk_to_target + 1.0 * reach_object
elif phase == GRASP:
    reward = 0.1 * stay_still + 2.0 * grasp_reward
elif phase == CARRY:
    reward = 1.0 * walk_to_origin + 2.0 * carry_stability
```

### Phase 6: Fine-Tuning (Stretch Goal)
- Unfreeze leg policy, add small learning rate for legs
- Allow legs to adapt their gait for carrying load
- Risk: catastrophic forgetting of walking skill
- Mitigation: KL penalty between fine-tuned and original leg policy

### Training Config (Lambda Labs)
- 256-512 envs (whole-body is more memory-intensive)
- Train arm policy: 2-3M steps
- Fine-tuning (if attempted): 500K additional steps with low LR
- A10G should suffice; A100 if 512 envs + full Dex3 hands

### Critical Constraints
- **CLOUD ONLY** — full G1 model with objects is heavy
- Frozen locomotion policy must be loaded as a separate network, not part of training graph
- State machine phases need to be tracked per-env independently
- Object must not clip through robot during carry — tune contact params
- Walking gait should be reasonably maintained while arm is moving — add locomotion quality reward

## Success Criteria

| Metric | Target |
|--------|--------|
| G1 walks to target position (within 0.5m) | Pass |
| G1 reaches and grasps cube on table | > 60% success |
| G1 carries cube back to origin without dropping | > 40% success |
| Walking gait quality maintained during manipulation | Qualitative |
| Full pipeline in single episode (walk → grasp → carry) | > 30% success |
| Training on Lambda Labs A10G | < 6 hours |

## References

- [HOVER — Neural Whole-Body Controller for Humanoids](https://github.com/NVlabs/HOVER)
- [Isaac Lab — Humanoid Environments](https://isaac-sim.github.io/IsaacLab/main/source/overview/environments.html)
- [Ha et al. — Learning Agile Robotic Locomotion Skills by Imitating Animals (2020)](https://arxiv.org/abs/2004.00784)
- [Cheng et al. — Expressive Whole-Body Control for Humanoid Robots (2024)](https://arxiv.org/abs/2402.16796)
