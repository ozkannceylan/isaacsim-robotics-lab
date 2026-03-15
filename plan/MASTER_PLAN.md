# Isaac Sim Robotics Lab — Master Plan

> **Goal:** GPU-accelerated robotics curriculum from RL fundamentals to VLA-controlled humanoid manipulation  
> **Stack:** Isaac Sim · Isaac Lab · RSL-RL / SKRL · Python  
> **Author:** M. Ozkan Ceylan  
> **Infra:** Local (Ubuntu 24, RTX 4050 6GB) + Lambda Labs (A10/A100 on demand)

---

## Vision

A structured, hands-on lab series that builds Isaac Sim and Isaac Lab competency from scratch. Each lab produces a trained policy, rigorous documentation, and a blog post. The series begins with simulation fundamentals and ends with a VLA-controlled humanoid performing manipulation tasks from natural language commands.

The key differentiator from the companion MuJoCo lab: here we learn to **scale** — GPU-parallel environments, domain randomization, sim-to-real transfer, and the NVIDIA robotics ecosystem.

```
Lab 1          Lab 2          Lab 3          Lab 4
Isaac Sim   →  RL Env      →  RL Arm      →  Domain Rand
Foundations    Design          Control        & Sim2Real
                                                │
Lab 7          Lab 6          Lab 5          ◄──┘
VLA          ← Whole-Body  ← Locomotion
Pipeline       Loco-Manip     (G1 Biped)
```

---

## Lab Summary

| Lab | Title | Capstone Demo | Infra |
|-----|-------|---------------|-------|
| 1 | Isaac Sim Foundations | Spawn UR5e, apply joint commands, render camera | Local |
| 2 | RL Environment Design | Train Cartpole PPO from scratch in Isaac Lab | Local |
| 3 | RL Arm Control | RL-trained reach + grasp with Franka/UR5e | Local |
| 4 | Domain Randomization & Sim2Real | Robust grasp policy surviving visual/physics perturbation | Local (borderline) |
| 5 | Bipedal Locomotion | G1 walking on flat + rough terrain via RL | Lambda Labs |
| 6 | Whole-Body Loco-Manipulation | G1 walks to object, picks it up, carries it | Lambda Labs |
| 7 | VLA Integration | "Pick up the red cup" — language-to-action via synthetic data | Lambda Labs |

---

## Progression Logic

```
SIMULATION LITERACY (Lab 1)
  Understand Isaac Sim/Lab APIs, USD, PhysX, asset pipeline.
      │
      ▼
RL FUNDAMENTALS (Lab 2)
  Build a vectorized env from scratch. Observation, action, reward design.
      │
      ▼
MANIPULATION (Lab 3)
  Apply RL to real robotics: reach, grasp, contact-rich tasks.
      │
      ▼
ROBUSTNESS (Lab 4)
  Domain randomization, visual perturbation, physics randomization.
  The bridge from sim to real.
      │
      ▼
LOCOMOTION (Lab 5)
  Floating-base paradigm shift. Bipedal walking via RL.
      │
      ▼
INTEGRATION (Labs 6-7)
  Locomotion + manipulation + perception + language.
```

---

## Platform & Infra Strategy

### Compute Tiers

| Tier | GPU | VRAM | Use For |
|------|-----|------|---------|
| Local | RTX 4050 Laptop | 6 GB | Labs 1-3 (headless, ≤64 envs) |
| Local Stretch | RTX 4050 | 6 GB | Lab 4 (headless, tight VRAM, ≤128 envs) |
| Cloud | Lambda Labs A10G | 24 GB | Labs 5-6 (512+ envs, G1 model) |
| Cloud Heavy | Lambda Labs A100 | 40/80 GB | Lab 7 (VLA training + rendering) |

### Seamless Local ↔ Cloud Workflow

The repo is designed so the same codebase runs on both local and Lambda Labs without modification:

1. **Single conda env spec** — `environment.yml` pins Isaac Sim + Isaac Lab + PyTorch versions
2. **Config-driven num_envs** — each lab has `config/local.yaml` and `config/cloud.yaml`
3. **Git-based sync** — push from local, pull on Lambda instance
4. **Checkpoint portability** — all checkpoints save to `outputs/` with relative paths
5. **Docker fallback** — `Dockerfile` provided for Lambda Labs reproducibility
6. **Setup script** — `scripts/setup_lambda.sh` handles NGC login, conda env, pip install in one shot

### Key Constraints

- **Always headless on local** — GUI eats 1-2 GB VRAM you cannot afford
- **DLSS Performance mode** — default on, reduces rendering VRAM
- **Texture streaming budget** — reduce to 30% on local (default 60%)
- **No camera sensors on local** — defer rendering-heavy tasks to cloud
- **Isaac Sim 5.x + Python 3.11** — pin this across all environments

---

## Robot Progression

| Labs | Robot | Source | Rationale |
|------|-------|--------|-----------|
| 1-2 | Cartpole (built-in) | Isaac Lab examples | Minimal complexity, learn APIs |
| 3-4 | Franka Panda / UR5e | Isaac Lab assets | Industry-standard manipulator, rich contact physics |
| 5-7 | Unitree G1 | Isaac Lab / Menagerie | Full humanoid with Dex3 hands, ecosystem support |

---

## Repo Structure

```
isaacsim-robotics-lab/
├── MASTER_PLAN.md                    # This file
├── CLAUDE.md                         # Agentic coding context for Claude Code
├── README.md                         # Public-facing repo overview
├── environment.yml                   # Conda env spec (Isaac Sim + Lab + deps)
├── Dockerfile                        # Lambda Labs / cloud reproducibility
├── pyproject.toml                    # Project metadata + editable install
├── setup.py                          # Isaac Lab extension setup
│
├── scripts/
│   ├── setup_local.sh                # Local Ubuntu 24 bootstrap
│   ├── setup_lambda.sh               # Lambda Labs one-shot setup
│   └── common.sh                     # Shared env vars and helpers
│
├── config/
│   ├── local.yaml                    # Local hardware profile (num_envs, headless, etc.)
│   └── cloud.yaml                    # Cloud hardware profile
│
├── source/
│   └── isaacsim_robotics_lab/        # Isaac Lab extension (installed via pip -e)
│       ├── __init__.py
│       ├── tasks/
│       │   ├── direct/               # Direct workflow tasks
│       │   │   ├── lab_01_foundations/
│       │   │   ├── lab_02_rl_env/
│       │   │   ├── lab_03_arm_control/
│       │   │   ├── lab_04_domain_rand/
│       │   │   ├── lab_05_locomotion/
│       │   │   ├── lab_06_loco_manip/
│       │   │   └── lab_07_vla/
│       │   └── manager_based/        # Manager-based tasks (Labs 3+)
│       │       └── ...
│       ├── robots/                   # Robot configs (ArticulationCfg)
│       │   ├── ur5e.py
│       │   ├── franka.py
│       │   └── g1.py
│       ├── rewards/                  # Shared reward terms
│       ├── observations/             # Shared observation terms
│       └── utils/                    # Shared helpers
│
├── docs/
│   ├── lab_01_foundations.md
│   ├── lab_02_rl_env.md
│   ├── ...
│   └── lab_07_vla.md
│
├── blog/
│   ├── lab_01_isaac_sim_foundations.md
│   └── ...
│
├── outputs/                          # Training outputs (gitignored)
│   ├── lab_01/
│   ├── lab_02/
│   └── ...
│
└── tests/
    ├── test_lab_01.py
    └── ...
```

---

## Deliverables Per Lab

Each lab produces four artifacts:

1. **Task Code** — Isaac Lab environment + training config under `source/`
2. **Trained Policy** — Checkpoint + TensorBoard logs under `outputs/`
3. **Documentation** — Technical writeup in `docs/lab_XX.md`
4. **Blog Post** — Public-facing article in `blog/`

---

## Documentation Template

Every `docs/lab_XX.md`:

```
# Lab XX: [Title]

## Objectives
## Prerequisites (prior labs, concepts)
## Theory (RL formulation, reward design rationale)
## Architecture (env structure, observation/action spaces, manager hierarchy)
## Implementation Notes (key design decisions for Claude Code)
## Training Results (reward curves, success rates, num_envs scaling)
## Lessons Learned
## References
```

Every blog post:

```
# [Title]

## Context (why this matters for robotics)
## The Approach (Isaac Lab specifics)
## Key Insight
## Results (videos, plots)
## What's Next
```

---

## Timeline Estimate

| Phase | Labs | Duration | Infra | Notes |
|-------|------|----------|-------|-------|
| Foundations | 1-2 | ~1 week | Local | API fluency, RL pipeline |
| Manipulation | 3-4 | ~2 weeks | Local | Contact physics, domain rand |
| Locomotion | 5-6 | ~3 weeks | Lambda Labs | Paradigm shift to floating base |
| VLA | 7 | ~2 weeks | Lambda Labs | Builds on humanoid_vla experience |

**Total: ~8 weeks** (part-time, alongside job search)

---

## Risk Register

| Risk | Impact | Mitigation |
|------|--------|------------|
| RTX 4050 VRAM insufficient for Lab 4 | Blocked locally | Reduce num_envs to 32; move to Lambda early |
| Isaac Sim version incompatibility | Broken pipeline | Pin exact versions in environment.yml |
| Lambda Labs GPU availability | Training delays | Book A10G (cheaper, more available); A100 only for Lab 7 |
| G1 model complexity (Labs 5-6) | Slow convergence | Start with Anymal-C quadruped as stepping stone |
| VLA synthetic data quality (Lab 7) | Poor policy transfer | Use Isaac Sim Replicator for structured data generation |
| Scope creep | Schedule slip | Hard-scoped capstone demo per lab — ship when demo works |

---

## Key Decisions

1. **Direct workflow first, Manager-based later** — Labs 1-2 use Direct for understanding; Labs 3+ transition to Manager-based for modularity
2. **SKRL as primary RL library** — Good Isaac Lab integration, supports PPO/SAC/TD3, clean API
3. **RSL-RL for locomotion** — Labs 5-6 use RSL-RL (industry standard for legged robots)
4. **No GUI rendering on local** — All local work is headless; visual verification via Lambda Labs livestream
5. **Separate robot configs** — Reusable `ArticulationCfg` files, not embedded in task code
