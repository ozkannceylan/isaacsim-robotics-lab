# Lab 1: Isaac Lab RL Fundamentals

## Objective

Master Isaac Lab's core abstractions by training RL policies on built-in environments. Understand GPU-parallelized simulation, the manager-based workflow, and how Isaac Lab differs from standard Gymnasium-style RL.

## Why This Lab Exists

Isaac Lab's architecture is fundamentally different from MuJoCo/Gymnasium. Environments run thousands of parallel instances on GPU. Observations, actions, and rewards are batched tensors. Understanding this paradigm shift is essential before building custom tasks.

## Prerequisites

- Lab 0 complete (working cloud setup)
- Familiarity with RL concepts (policy gradient, PPO) from mujoco-robotics-lab
- Basic PyTorch tensor operations

## Deliverables

1. Trained CartPole policy with training curves (tensorboard)
2. Trained Ant locomotion policy with video recording
3. Comparison document: Isaac Lab vs MuJoCo Gymnasium workflow
4. Code demonstrating key Isaac Lab abstractions

## Tasks

### 1.1 Isaac Lab Architecture Deep Dive

Study and document the following core concepts (no coding, just understanding):

- **Scene composition:** How USD scenes, assets, and sensors are organized
- **Manager-based vs Direct workflow:** When to use each, tradeoffs
- **InteractiveScene:** The container for all simulation entities
- **ObservationManager, ActionManager, RewardManager, TerminationManager:** The four pillars
- **GPU parallelism:** How `num_envs` works, tensor batching, no Python loops

Produce a concept map or architecture diagram.

### 1.2 CartPole: Hello World

Train CartPole using Isaac Lab's built-in environment:

- Run with default config, observe training
- Experiment with `num_envs` (64, 256, 1024, 4096) and measure throughput (steps/sec)
- Plot training curves for different `num_envs` settings
- Compare wall-clock time vs MuJoCo CartPole (from mujoco-robotics-lab)

Key insight to capture: GPU parallelism gives N-fold speedup, but with diminishing returns as N exceeds GPU capacity.

### 1.3 Ant Locomotion

Train the Ant quadruped environment:

- Default config, train to convergence
- Record evaluation video (Isaac Lab's video wrapper)
- Inspect reward components: forward velocity, energy penalty, alive bonus
- Experiment with reward weight modifications and document effects

### 1.4 RL Framework Integration

Isaac Lab supports multiple RL frameworks. Test at least two:

- **RL Games:** Default, NVIDIA-maintained, fastest
- **SKRL:** More Pythonic, easier to customize
- **RSL-RL / Stable Baselines:** Optional comparison

Document: which framework for which use case, performance differences.

### 1.5 Headless vs GUI Training

- Train headless (faster, production mode)
- Train with GUI (visualization, debugging mode)
- Measure FPS difference
- Learn to toggle rendering mid-training for spot-checking

### 1.6 Logging and Experiment Tracking

- TensorBoard integration: training curves, reward components
- Checkpoint saving/loading
- Evaluation and video recording pipeline
- Organize outputs for portfolio documentation

## Key Concepts to Internalize

| Concept | MuJoCo/Gym Equivalent | Isaac Lab Approach |
|---------|----------------------|-------------------|
| Environment step | `env.step(action)` | Batched tensor operations on GPU |
| Observation | NumPy array | GPU tensor (no CPU transfer) |
| Parallelism | `SubprocVecEnv` (CPU) | Single GPU, thousands of envs |
| Scene setup | XML/MJCF | USD + Python API |
| Reward | Single scalar | RewardManager with weighted terms |
| Reset | `env.reset()` | Auto-reset per-env on termination |

## Success Criteria

- CartPole converges in <5 minutes wall-clock
- Ant walks forward stably after training
- Can articulate the architectural differences between Isaac Lab and MuJoCo workflows
- Training curves and videos captured for portfolio

## Estimated Cloud Cost

8-10 hours at ~$0.30/hr = ~$2.40-3.00
