# Lab 2: Custom Task and Reward Engineering

## Objective

Design and implement a custom manipulation task for the Unitree G1 humanoid using Isaac Lab's manager-based workflow. This is the core skill: defining tasks, shaping rewards, and configuring domain randomization from scratch.

## Why This Lab Exists

Built-in environments teach you how Isaac Lab works. Real-world value comes from creating your own tasks. This lab bridges the gap between "I can run examples" and "I can build custom robotics research environments." It also directly feeds the NEURA Robotics interview narrative.

## Prerequisites

- Lab 1 complete (Isaac Lab fundamentals understood)
- Understanding of reward shaping from mujoco-robotics-lab
- Unitree G1 URDF/USD model available (from humanoid_vla project)

## Deliverables

1. Custom G1 reach task: train the G1 to reach a target position with its hand
2. Custom G1 pick-and-place task: grasp and move an object
3. Domain randomization config: friction, mass, initial pose variations
4. Reward ablation study: document which reward terms matter most
5. Reusable task template for future custom environments

## Tasks

### 2.1 Unitree G1 Asset Integration

Import the G1 into Isaac Lab:

- Convert URDF to USD (if not already available in Isaac Lab's asset library)
- Verify joint limits, collision meshes, and visual meshes
- Spawn G1 in a basic scene, verify articulation works
- Compare with Isaac Lab's built-in humanoid assets for reference

### 2.2 Manager-Based Environment Scaffold

Build a custom environment using the manager-based workflow:

- Define `SceneCfg`: G1 robot + ground plane + target marker
- Define `ObservationsCfg`: joint positions, joint velocities, end-effector pose, target position
- Define `ActionsCfg`: joint position targets (start simple)
- Define `RewardsCfg`: distance-to-target, energy penalty, alive bonus
- Define `TerminationsCfg`: timeout, fall detection, success threshold

Document the full config structure as a reference template.

### 2.3 Reach Task

Train G1 to reach a random target position with its right hand:

- Target: random 3D position within workspace
- Reward: negative L2 distance to target + bonus on reach + energy penalty
- Start with 256 parallel envs, scale to 2048
- Train with RL Games PPO, tune hyperparameters
- Record success rate over training

### 2.4 Pick-and-Place Task (Progressive Complexity)

Extend the reach task to include object interaction:

**Phase A: Approach**
- Spawn a cube on a table
- Reward for approaching the cube

**Phase B: Grasp**
- Add surface gripper or contact-based grasping
- Reward for successful grasp (object lifted)

**Phase C: Transport**
- Add target placement zone
- Reward for placing object at target

Use curriculum learning or reward scheduling to train phases progressively.

### 2.5 Domain Randomization

Add randomization to make policies robust:

- Physics: friction coefficients, object mass, joint damping
- Visual: lighting changes, object color (for sensor-based tasks in Lab 3)
- Initial conditions: starting joint configuration, object spawn position
- Measure policy robustness: train with/without randomization, evaluate on perturbed conditions

Document the randomization config and its effect on policy generalization.

### 2.6 Reward Engineering Study

Systematic ablation of reward components:

- Train with each reward term individually
- Train with all terms, then remove one at a time
- Document which terms are essential vs nice-to-have
- Visualize reward component contributions over training

This analysis is excellent interview and blog content.

## Architecture Decisions to Document

- Why manager-based over direct workflow for this task
- How observation space design affects learning speed
- Action space choice: joint positions vs joint velocities vs torques
- Reset strategy: full reset vs partial reset on termination

## Success Criteria

- G1 reaches random targets with >80% success rate
- Pick-and-place achieves >50% success rate (this is hard, partial credit expected)
- Domain randomization measurably improves generalization
- All configs are clean, documented, and reusable

## Estimated Cloud Cost

10-12 hours at ~$0.30/hr = ~$3.00-3.60
