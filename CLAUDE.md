# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Read and follow: /home/ozkan/Documents/MyProjects/_meta/workflow-rules.md

## Goal

Build portfolio-ready expertise in NVIDIA Isaac Sim and Isaac Lab through a structured 5-lab curriculum. Focus areas: GPU-accelerated RL, RTX sensor simulation, synthetic data generation, and sim-to-real transfer with the Unitree G1 humanoid.

This project complements `mujoco-robotics-lab` (foundational robotics: kinematics, dynamics, motion planning). It does NOT duplicate those concepts. Instead it focuses on what Isaac Sim/Lab uniquely offers: GPU-parallel environments, RTX sensors, domain randomization, Replicator, and NVIDIA-ecosystem integrations.

## Context

- Engineer has a mechatronics background with a master's in RL for mobile robotics
- MuJoCo labs 1-5 are complete (FK, IK, dynamics, motion planning, grasping)
- humanoid_vla project (Unitree G1, ACT imitation learning, ROS2) is the portfolio flagship
- Active job search targeting humanoid robotics and AI engineering roles (NEURA Robotics interview in progress)
- All labs run on Vast.ai cloud GPU (RTX 4090, 24GB VRAM), NOT local machine

---

## Common Commands

### Cloud setup (Vast.ai)

```bash
# SSH into Vast.ai instance
ssh -p <port> root@<vast-ip>

# Verify GPU
nvidia-smi  # Expect: RTX 4090, driver 535+

# One-time setup (run from the repo on the instance):
bash labs/lab_0/scripts/setup_instance.sh
```

### Isaac Lab (pip-based install)

```bash
conda activate isaaclab

# Headless training (no GUI, fastest)
python source/standalone/workflows/rl_games/train.py --task Isaac-Cartpole-v0 --headless --num_envs 2048

# GUI training (for visual debugging)
python source/standalone/workflows/rl_games/train.py --task Isaac-Cartpole-v0 --num_envs 256

# Evaluate trained policy
python source/standalone/workflows/rl_games/play.py --task Isaac-Cartpole-v0 --checkpoint <path>
```

### Run tests

```bash
# All tests for a specific lab
pytest labs/lab_0/tests/
pytest labs/lab_1/tests/

# Single test file
pytest labs/lab_2/tests/test_custom_env.py -v

# All tests across the project
pytest labs/*/tests/
```

### Record video

```bash
# Isaac Lab built-in video wrapper
python <script>.py --video --video_length 200 --video_interval 1000
```

---

## Architecture Principle

```
Isaac Sim  = physics engine + RTX renderer + USD scene graph
Isaac Lab  = RL framework layer (environments, managers, wrappers)
Pinocchio  = analytical robotics (FK, Jacobian, dynamics) when needed
ROS2       = deployment bridge (sim-to-real)
```

- Use Isaac Lab's manager-based workflow for all new environments
- Use Isaac Sim's native physics (PhysX) for simulation, NOT MuJoCo
- Use Pinocchio only when you need analytical quantities Isaac Lab doesn't provide (rare)
- GPU tensors stay on GPU. Avoid CPU transfers in the training loop.

## Key Architectural Difference from MuJoCo Labs

| Aspect | MuJoCo Labs | Isaac Sim Labs |
|--------|-------------|----------------|
| Physics | MuJoCo (CPU) | PhysX (GPU) |
| Parallelism | Single env or SubprocVecEnv | Thousands of envs on one GPU |
| Observations | NumPy arrays | GPU tensors (torch) |
| Scene format | MJCF XML | USD (Universal Scene Description) |
| Rendering | MuJoCo native | RTX ray-tracing |
| Analytical tools | Pinocchio (heavy use) | Isaac Lab built-in + Pinocchio (light use) |
| Deployment | Custom scripts | ROS2 bridge, ONNX export |

---

## Platform

- **Target robot:** Unitree G1 humanoid
- **Simulator:** Isaac Sim 5.1 + Isaac Lab 2.3.x
- **Compute:** Vast.ai RTX 4090 (24GB VRAM)
- **OS:** Ubuntu 22.04 (NGC container)
- **Python:** 3.11
- **RL frameworks:** RL Games (primary), SKRL (secondary)
- **Local machine:** Used only for code editing, git, ROS2 node development. No Isaac Sim locally (GPU insufficient).

---

## Repository Structure

```
isaacsim-robotics-lab/
  plan/
    README.md
    lab-0-cloud-setup.md
    lab-1-rl-fundamentals.md
    lab-2-custom-tasks.md
    lab-3-sensors-syndata.md
    lab-4-sim-to-real.md
    cloud-setup-guide.md
  labs/
    lab_0/
      tasks/        # PLAN.md, ARCHITECTURE.md, TODO.md, LESSONS.md
      src/
      scripts/      # setup_instance.sh, validate_setup.sh, setup_vnc.sh
      docs/
      docs-turkish/
      media/
      tests/
    lab_1/
    lab_2/
    lab_3/
    lab_4/
  configs/          # Shared Isaac Lab configs, domain randomization presets
  tools/            # Utility scripts (video, benchmarking, cost tracking)
  docs/             # Project-level documentation
  CLAUDE.md
```

---

## Per-Lab Workflow

**Mandatory for every new lab. Follow in order.**

1. **Read the lab plan**: `plan/lab-N-<name>.md` fully before anything else
2. **Create lab folder** with `tasks/`, `src/`, `docs/`, `docs-turkish/`, `media/`, `tests/`
3. **Write `tasks/PLAN.md`**: Break lab plan into phased implementation steps
4. **Write `tasks/ARCHITECTURE.md`**: Module map, data flow, key interfaces, Isaac Lab configs, cloud requirements
5. **Create `tasks/TODO.md`**: Generated from PLAN.md, updated after every step. Must have "Current Focus" and "Blockers" sections
6. **Maintain `tasks/LESSONS.md`**: Live journal of bugs/fixes/insights with Symptom/Root cause/Fix/Takeaway format

## Execution Rules

1. **Read lab plan -> Write PLAN -> Write ARCHITECTURE -> Create TODO -> Then code.** Never skip steps.
2. **Update TODO.md after every completed step.**
3. **Log bugs in LESSONS.md immediately.** Cloud GPU debugging is expensive; don't repeat mistakes.
4. **One phase at a time.** Complete all steps in Phase N before starting Phase N+1.
5. **Tests before moving on.** Each phase should have passing tests before the next phase begins.
6. **Minimize cloud GPU time.** Write and test code logic locally where possible. Use cloud only for Isaac Sim execution.
7. **When resuming a lab**, read `tasks/TODO.md` first to find exactly where you left off.
8. **ONE milestone per session.** Do NOT proceed to next milestone until gate criteria are met.
9. **Every milestone ends with evidence:** screenshot, video (media/mN_*.mp4), training curve, or metrics table.

---

## Isaac Lab Specific Patterns

### Manager-Based Environment Template

```python
from isaaclab.envs import ManagerBasedRLEnvCfg
from isaaclab.managers import (
    ObservationGroupCfg, ObservationTermCfg,
    RewardTermCfg, TerminationTermCfg,
    SceneEntityCfg,
)

@configclass
class MyEnvCfg(ManagerBasedRLEnvCfg):
    scene: MySceneCfg = MySceneCfg(num_envs=2048)
    observations: ObservationsCfg = ObservationsCfg()
    actions: ActionsCfg = ActionsCfg()
    rewards: RewardsCfg = RewardsCfg()
    terminations: TerminationsCfg = TerminationsCfg()
```

### GPU Tensor Pattern (No CPU Transfers)

```python
# CORRECT: everything stays on GPU
obs = env.obs_buf          # torch.Tensor on GPU
action = policy(obs)       # inference on GPU
env.step(action)           # physics on GPU

# WRONG: unnecessary CPU transfer
obs_np = env.obs_buf.cpu().numpy()  # kills performance
```

### Domain Randomization Config

```python
from isaaclab.managers import RandomizationTermCfg

randomization = {
    "object_mass": RandomizationTermCfg(
        func=randomize_rigid_body_mass,
        params={"mass_range": (0.1, 2.0)},
    ),
    "friction": RandomizationTermCfg(
        func=randomize_physics_material,
        params={"friction_range": (0.4, 1.2)},
    ),
}
```

### Policy Export

```python
# ONNX export for deployment
import torch
dummy_input = torch.randn(1, obs_dim).cuda()
torch.onnx.export(policy, dummy_input, "policy.onnx")

# Verify
import onnxruntime as ort
session = ort.InferenceSession("policy.onnx")
```

---

## Cloud GPU Cost Discipline

- **Target budget:** $15-20/month total
- **Track every session:** Log start time, end time, cost in a running file
- **Auto-shutdown:** Always set idle timeout before starting work
- **Headless first:** Use GUI only when visual inspection is necessary
- **Local development:** Write configs, tests, documentation locally. Cloud is for execution only.
- **Push before stop:** Always git push results before stopping a Vast.ai instance

## File Sync Strategy

```
Local (code editing, git, docs)
  |  git push
  v
GitHub (source of truth)
  |  git pull
  v
Vast.ai Instance (execution, training)
  |  scp / git push
  v
Local (analysis, portfolio writing)
```

Never rely on Vast.ai disk persistence for critical data. Always push to GitHub or download artifacts.

---

## Tech Stack

- **Python 3.11**
- **Isaac Sim 5.1** (PhysX GPU, RTX rendering, USD)
- **Isaac Lab 2.3.x** (manager-based RL environments, from source v2.3.0 tag)
- **PyTorch** (policy networks, GPU tensors)
- **RL Games** (primary RL framework, NVIDIA-maintained)
- **SKRL** (secondary, more Pythonic)
- **NVIDIA Replicator** (synthetic data generation)
- **ROS2 Humble** (sim-to-real bridge, Lab 4)
- **ONNX Runtime** (policy deployment)
- **TensorBoard** (training visualization)
- **Pinocchio** (analytical robotics, used sparingly)

## Code Standards

- Every function: docstring + type hints
- Comments in English
- Test files in `labs/lab_N/tests/` with naming `test_{module}.py`
- Use `pathlib.Path` for all file paths
- No hardcoded absolute paths
- Documentation: always write both English (`docs/`) and Turkish (`docs-turkish/`)
- Isaac Lab configs: use `@configclass` decorator, follow Isaac Lab naming conventions
- Tensor operations: keep on GPU, use PyTorch ops not NumPy

---

## Known Issues + Solutions

### Isaac Sim first launch is slow
First launch downloads ~10GB of assets and compiles shaders. Subsequent launches are faster (10-30s). Be patient on first run.

### RT Core requirement
Isaac Sim rendering requires RTX GPUs with RT Cores. A100/H100 are NOT supported. Always use RTX 4090 on Vast.ai.

### Isaac Lab version compatibility
Isaac Lab 2.3.0 requires Isaac Sim 5.1. Version mismatches cause silent failures. Always verify:
```python
import isaacsim
print(isaacsim.__version__)  # Must match expected version
```

### NumPy 2.x incompatibility
Isaac Lab may require NumPy 1.x. If you see NumPy errors:
```bash
pip install --force-reinstall "numpy<2"
```

### VNC black screen on Vast.ai
Install VirtualGL and use `vglrun` prefix for GPU-accelerated rendering through VNC.

### num_envs and VRAM
RTX 4090 has 24GB VRAM. Approximate limits:
- Simple envs (CartPole): up to 8192 envs
- Medium envs (Ant): up to 4096 envs
- Complex envs (G1 humanoid): up to 1024-2048 envs (depends on observation/action space)
Monitor with `nvidia-smi` during training. OOM = reduce num_envs.

### Headless mode requires explicit flag
Without `--headless`, Isaac Sim tries to open a GUI window. On cloud without display, this crashes.

### USD asset paths
Isaac Lab assets are hosted on AWS S3. First load per asset may take minutes depending on network. Assets are cached locally after first download.

### Isaac Lab 3.0 Beta is NOT stable
Do not upgrade to 3.0 Beta. It has breaking changes and is under active development. Stay on 2.3.0.

---

## Lab Progress

- [ ] Lab 0: Cloud Setup and Validation (Vast.ai + NGC + Isaac Sim)
- [ ] Lab 1: Isaac Lab RL Fundamentals (CartPole, Ant, framework comparison)
- [ ] Lab 2: Custom Task and Reward Engineering (G1 reach, pick-and-place, domain randomization)
- [ ] Lab 3: Sensor Simulation and Synthetic Data (RTX cameras, LiDAR, Replicator)
- [ ] Lab 4: Sim-to-Real Pipeline (ONNX export, ROS2 bridge, capstone)

Target robot transitions: Labs 0-1 use built-in assets. Labs 2-4 use Unitree G1 humanoid.

---

## Debugging Checklist

When Isaac Lab training fails or produces bad results:
1. Check `num_envs` vs VRAM (nvidia-smi)
2. Verify headless flag if on cloud
3. Check Isaac Sim + Isaac Lab version compatibility
4. Inspect reward components individually (TensorBoard)
5. Reduce num_envs to 64 and run with GUI for visual debugging
6. Check observation space: are all values normalized / in reasonable range?
7. Verify action space bounds match robot joint limits
8. Check termination conditions: too aggressive = no learning, too lenient = bad behavior

## Session Start Protocol

1. Read this CLAUDE.md
2. Read the lab plan: `plan/lab-N-<name>.md`
3. Check `labs/lab_N/tasks/TODO.md` for current state
4. Check `labs/lab_N/tasks/LESSONS.md` for known issues
5. Resume from "Current Focus" in TODO.md
6. If on cloud: verify GPU with `nvidia-smi`, check disk space with `df -h`