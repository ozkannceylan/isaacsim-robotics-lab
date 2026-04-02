# Lab 0: Architecture

## System Overview

Lab 0 establishes the cloud development environment. No application code is written; the deliverables are infrastructure scripts and validation.

## What Runs Where

```
┌─────────────────────────────┐     ┌──────────────────────────────────┐
│  Local Machine              │     │  Vast.ai Instance (RTX 4090)     │
│                             │     │                                  │
│  - Code editing (VS Code)   │ SSH │  - Isaac Sim 5.1 (PhysX GPU)    │
│  - Git operations           │────>│  - Isaac Lab 2.3.x              │
│  - Documentation            │     │  - PyTorch 2.7 + CUDA 12.8     │
│  - ROS2 node dev (later)    │     │  - Conda env: isaaclab          │
│  - VNC viewer               │ VNC │  - TurboVNC + VirtualGL         │
│                             │<────│  - Training / rendering         │
└─────────────────────────────┘     └──────────────────────────────────┘
            │                                      │
            │         git push / pull              │
            └──────────────┐  ┌────────────────────┘
                           v  v
                    ┌──────────────┐
                    │   GitHub     │
                    │ (source of   │
                    │   truth)     │
                    └──────────────┘
```

## Software Stack on Instance

```
┌──────────────────────────────────────┐
│  RL Frameworks (rl_games, skrl)      │  <- installed by isaaclab.sh -i
├──────────────────────────────────────┤
│  Isaac Lab 2.3.x                     │  <- ~/IsaacLab (from source)
├──────────────────────────────────────┤
│  Isaac Sim 5.1.0                     │  <- pip install from NVIDIA PyPI
├──────────────────────────────────────┤
│  PyTorch 2.7.0 + CUDA 12.8          │  <- pip install
├──────────────────────────────────────┤
│  Python 3.11 (Conda: isaaclab)       │  <- Miniconda
├──────────────────────────────────────┤
│  NVIDIA Driver + CUDA Toolkit        │  <- Pre-installed on Vast.ai
├──────────────────────────────────────┤
│  Ubuntu 22.04                        │  <- Vast.ai base image
└──────────────────────────────────────┘
```

## Port Forwarding

| Service | Remote Port | Local Tunnel | Purpose |
|---------|-------------|--------------|---------|
| SSH | Varies (Vast.ai assigned) | Direct | Shell access |
| VNC | 5901 | `ssh -L 5901:localhost:5901` | Desktop GUI |
| noVNC | 6080 | `ssh -L 6080:localhost:6080` | Browser GUI |
| TensorBoard | 6006 | `ssh -L 6006:localhost:6006` | Training viz |

## Data Flow

1. **Code changes:** Local -> git push -> GitHub -> git pull on instance
2. **Training results:** Instance -> git push -> GitHub -> git pull on local
3. **Large artifacts** (videos, checkpoints): scp from instance to local
4. **Never rely on Vast.ai disk:** Always push/download before stopping instance

## Key Directories on Instance

| Path | Purpose |
|------|---------|
| `~/miniconda3/` | Conda installation |
| `~/IsaacLab/` | Isaac Lab source (v2.3.0 tag) |
| `~/projects/isaacsim-robotics-lab/` | This project repo |
| `~/setup_instance.log` | Setup script log |

## Cloud Cost Model

- RTX 4090 on Vast.ai: ~$0.25-0.40/hr
- Target budget: $15-20/month
- Lab 0 estimated cost: $1-2 (3-5 hours for initial setup + validation)
- Mitigation: idle auto-shutdown, headless-first workflow, local code editing
