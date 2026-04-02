# IsaacSim Robotics Lab - Project Plan

## Purpose

A hands-on learning curriculum for mastering NVIDIA Isaac Sim and Isaac Lab. The goal is to build deep, demonstrable expertise in the NVIDIA robotics simulation ecosystem, from scene composition to sim-to-real RL policy transfer.

This project complements (does not duplicate) the existing `mujoco-robotics-lab`, which covers foundational robotics concepts (kinematics, dynamics, motion planning). This lab focuses exclusively on what Isaac Sim/Lab uniquely offers: GPU-accelerated parallel environments, RTX sensor simulation, domain randomization, synthetic data generation, and NVIDIA-ecosystem integrations.

## Target Platform

- **Robot:** Unitree G1 humanoid (consistent with humanoid_vla portfolio project)
- **Simulator:** Isaac Sim 5.1 + Isaac Lab 2.3.0 (stable release)
- **Compute:** Vast.ai cloud GPU (RTX 4090, 24GB VRAM)
- **Access:** SSH + VNC/noVNC for GUI, headless mode for RL training
- **OS:** Ubuntu 22.04 (NGC container base)

## Why Isaac Lab 2.3.0 (not 3.0 Beta)

Isaac Lab 3.0 Beta introduces a ground-up architectural overhaul (multi-backend physics, kit-less mode, Warp-native pipelines). While promising, the develop branch has breaking changes and is not production-ready. Version 2.3.0 on Isaac Sim 5.1 is the latest stable release with full documentation, community support, and proven workflows. The curriculum can be upgraded to 3.0 once it stabilizes.

## Why Vast.ai (not Lambda Labs)

Isaac Sim requires RT Core-capable GPUs for full rendering (RTX cameras, ray-traced sensors). Data center GPUs like A100/H100 lack RT Cores and are explicitly unsupported by Isaac Sim. Lambda Labs only offers A100/H100 instances. Vast.ai provides RTX 4090 (24GB VRAM, RT Cores) at ~$0.30/hr, which supports both GUI rendering and headless RL training.

## Curriculum Structure

5 focused labs, each building on the previous. Estimated total cloud hours: 40-60 hours (~$12-18 at Vast.ai rates).

| Lab | Title | Mode | Est. Hours |
|-----|-------|------|------------|
| 0 | Cloud Setup and Validation | GUI | 3-4 |
| 1 | Isaac Lab RL Fundamentals | Headless + GUI | 8-10 |
| 2 | Custom Task and Reward Engineering | Headless + GUI | 10-12 |
| 3 | Sensor Simulation and Synthetic Data | GUI (RTX) | 8-10 |
| 4 | Sim-to-Real Pipeline | Both | 10-12 |

## Relationship to Other Projects

- **mujoco-robotics-lab:** Foundational robotics (kinematics, dynamics, control). Concepts transfer but code does not.
- **humanoid_vla:** Portfolio flagship. Lab 4 connects Isaac Lab policy training back to the G1 + ROS2 deployment pipeline established there.
- **Portfolio website (ozkanceylan.dev):** Each completed lab produces a blog-ready writeup with visuals and metrics.

## Repository Structure

```
isaacsim-robotics-lab/
  plan/
    README.md              # This file
    lab-0-cloud-setup.md
    lab-1-rl-fundamentals.md
    lab-2-custom-tasks.md
    lab-3-sensors-syndata.md
    lab-4-sim-to-real.md
    cloud-setup-guide.md   # Vast.ai + NGC practical setup
  labs/
    lab_0/
    lab_1/
    lab_2/
    lab_3/
    lab_4/
  configs/
  docs/
  CLAUDE.md                # Claude Code rules and context
```
