# Lab 1: Architecture

## Overview

Lab 1 focuses on using Isaac Lab's built-in environments. No custom envs are created — the goal is to understand the framework before customizing it in Lab 2.

## Isaac Lab Manager-Based Environment

```
┌─────────────────────────────────────────────────────────┐
│  ManagerBasedRLEnv                                       │
│                                                          │
│  ┌──────────────────┐  ┌──────────────────┐             │
│  │ InteractiveScene  │  │  EventManager    │             │
│  │  - Articulations  │  │  - Resets        │             │
│  │  - Rigid Bodies   │  │  - Randomization │             │
│  │  - Sensors        │  └──────────────────┘             │
│  └──────────────────┘                                    │
│                                                          │
│  ┌──────────────────┐  ┌──────────────────┐             │
│  │ ObservationMgr   │  │ ActionManager    │             │
│  │  - Joint pos/vel  │  │  - Joint effort  │             │
│  │  - Base state     │  │  - Joint pos     │             │
│  │  - Sensor data    │  │  - Velocity      │             │
│  └──────────────────┘  └──────────────────┘             │
│                                                          │
│  ┌──────────────────┐  ┌──────────────────┐             │
│  │ RewardManager    │  │ TerminationMgr   │             │
│  │  - Weighted terms │  │  - Time limit    │             │
│  │  - Per-env scalar │  │  - Bad state     │             │
│  │  - GPU tensor     │  │  - Out of bounds │             │
│  └──────────────────┘  └──────────────────┘             │
└─────────────────────────────────────────────────────────┘
```

## Training Pipeline

```
┌────────────┐    ┌───────────────┐    ┌────────────────┐
│ RL Framework│    │  Isaac Lab    │    │  Isaac Sim     │
│ (RL Games / │───>│  Env Wrapper  │───>│  PhysX GPU     │
│  SKRL)      │    │  (batched     │    │  (parallel     │
│             │<───│   tensors)    │<───│   simulation)  │
└────────────┘    └───────────────┘    └────────────────┘
     │                                         │
     v                                         v
┌────────────┐                        ┌────────────────┐
│ TensorBoard│                        │ USD Scene      │
│ Checkpoints│                        │ RTX Rendering  │
└────────────┘                        └────────────────┘
```

## Environments Used

| Environment | Robot | Obs Dim | Act Dim | Reward Components |
|-------------|-------|---------|---------|-------------------|
| Isaac-Cartpole-v0 | CartPole | 4 | 1 | Pole angle, cart position |
| Isaac-Ant-v0 | Ant quadruped | ~60 | 8 | Forward vel, energy, alive |

## Key Files on Instance

| Path | Purpose |
|------|---------|
| `~/IsaacLab/source/isaaclab/isaaclab/envs/` | Environment base classes |
| `~/IsaacLab/source/isaaclab_tasks/isaaclab_tasks/` | Built-in task definitions |
| `~/IsaacLab/source/standalone/workflows/` | Training scripts per RL framework |
| `~/projects/isaacsim-robotics-lab/labs/lab_1/` | Our scripts and results |

## Scripts in This Lab

| Script | Purpose | Runs On |
|--------|---------|---------|
| `scripts/train_cartpole.sh` | Train CartPole with configurable params | Instance |
| `scripts/train_ant.sh` | Train Ant locomotion | Instance |
| `scripts/benchmark_num_envs.sh` | Sweep num_envs and measure throughput | Instance |
| `scripts/compare_frameworks.sh` | Run same task with RL Games and SKRL | Instance |
| `scripts/evaluate.sh` | Load checkpoint, record video | Instance |
| `src/analyze_throughput.py` | Parse logs, generate throughput chart | Local or Instance |
| `src/compare_rewards.py` | Plot reward component comparison | Local or Instance |

## Data Flow

```
Instance: Train → TensorBoard logs + checkpoints + videos
    │
    git push (or scp for large files)
    │
    v
Local: Analyze → Charts, docs, portfolio writeup
```
