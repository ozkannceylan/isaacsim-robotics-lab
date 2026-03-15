# CLAUDE.md — Isaac Sim Robotics Lab

> Context file for Claude Code. Read this before every coding session.

## Project Overview

This is a structured robotics curriculum built on NVIDIA Isaac Sim and Isaac Lab. The repo contains 7 labs progressing from simulation fundamentals to VLA-controlled humanoid manipulation. All code runs headless on Ubuntu 24.

**Read `MASTER_PLAN.md` for full project scope and architecture.**
**Read `docs/lab_XX_*.md` for the specific lab you are working on.**

## Critical Rules

### 1. Always Read the Lab Plan First
Before writing ANY code for a lab, read `docs/lab_XX_*.md` completely. The architecture, file structure, and implementation notes are defined there. Do not deviate from the specified architecture without explicit approval.

### 2. Isaac Lab Conventions
- All environments must be registered via `gym.register()` in `__init__.py`
- Use `isaaclab -p script.py` to run scripts, NOT bare `python`
- All training runs with `--headless` flag (no GUI on local machine)
- Follow Isaac Lab's Direct or Manager-Based workflow as specified per lab
- Pin to Isaac Sim 5.x + Python 3.11

### 3. GPU Memory Awareness
- Local machine: RTX 4050 with 6 GB VRAM
- ALWAYS use headless mode locally
- Default `num_envs=64` for local, `num_envs=512` for cloud
- Load configs from `config/local.yaml` or `config/cloud.yaml`
- If VRAM errors occur: reduce num_envs by half, disable camera sensors
- NEVER enable GUI rendering on local machine

### 4. Tensor Operations Only
- No Python loops over environments in the sim loop
- All observation, reward, and termination computation must be batched PyTorch tensor ops
- All data stays on GPU (`self.device`) — never `.cpu()` in the hot loop
- Reward tensors: shape `(num_envs,)` not `(num_envs, 1)`
- Use `torch.where()` instead of if/else for per-env logic

### 5. Code Style
- Type hints on all function signatures
- Docstrings on all classes and public methods (NumPy style)
- Config dataclasses for all parameters (no magic numbers in code)
- Snake_case for files and variables, PascalCase for classes
- Max 200 lines per file — split into modules early

### 6. File Structure Discipline
- Task code goes in `source/isaacsim_robotics_lab/tasks/`
- Robot configs go in `source/isaacsim_robotics_lab/robots/`
- Shared reward/obs terms go in `source/isaacsim_robotics_lab/rewards/` and `observations/`
- Training outputs go in `outputs/lab_XX/` (gitignored)
- Tests go in `tests/`

### 7. Testing
- Every lab must have at least one test in `tests/`
- Test that env creates, steps, and resets without error
- Test with `num_envs=4` and `max_steps=10` (fast smoke test)
- Run: `isaaclab -p -m pytest tests/test_lab_XX.py -v`

### 8. Checkpoint & Reproducibility
- Set random seed in training config
- Save checkpoints every 500 iterations to `outputs/lab_XX/checkpoints/`
- TensorBoard logs to `outputs/lab_XX/logs/`
- All hyperparameters in config files, never hardcoded

## Environment Setup

### Local (Ubuntu 24, RTX 4050)
```bash
# One-time setup
conda create -n isaaclab python=3.11
conda activate isaaclab
pip install torch==2.7.0 torchvision==0.22.0 --index-url https://download.pytorch.org/whl/cu128
pip install isaacsim[all,extscache] --extra-index-url https://pypi.nvidia.com
git clone https://github.com/isaac-sim/IsaacLab.git
cd IsaacLab && pip install -e .
cd .. && pip install -e source/isaacsim_robotics_lab
```

### Lambda Labs (A10G/A100)
```bash
# Run the setup script (handles everything)
bash scripts/setup_lambda.sh
```

## Common Patterns

### Launching a standalone script
```python
from isaaclab.app import AppLauncher
parser = argparse.ArgumentParser()
AppLauncher.add_app_launcher_args(parser)
args = parser.parse_args()
app_launcher = AppLauncher(args)
simulation_app = app_launcher.app
# ... your code ...
simulation_app.close()
```

### Creating a Direct RL Environment
```python
class MyEnv(DirectRLEnv):
    cfg: MyEnvCfg
    
    def __init__(self, cfg, render_mode=None, **kwargs):
        super().__init__(cfg, render_mode, **kwargs)
    
    def _setup_scene(self):
        # Spawn assets, configure physics
        ...
    
    def _pre_physics_step(self, actions):
        # Apply actions to simulation
        ...
    
    def _get_observations(self):
        # Return dict with "policy" key
        return {"policy": obs_tensor}
    
    def _get_rewards(self):
        # Return (num_envs,) tensor
        return reward_tensor
    
    def _get_dones(self):
        # Return (terminated, truncated) tuple of (num_envs,) bool tensors
        return terminated, truncated
    
    def _reset_idx(self, env_ids):
        # Reset only the envs in env_ids
        super()._reset_idx(env_ids)
        ...
```

### Training with SKRL
```bash
isaaclab -p scripts/reinforcement_learning/skrl/train.py \
    --task IsaacLab-MyTask-Direct-v0 \
    --headless \
    --num_envs 64
```

### Training with RSL-RL (locomotion)
```bash
isaaclab -p scripts/reinforcement_learning/rsl_rl/train.py \
    --task IsaacLab-MyTask-Direct-v0 \
    --headless \
    --num_envs 512
```

## Debugging Checklist

If something doesn't work:
1. **VRAM error?** → Reduce num_envs, ensure --headless, check for camera sensors
2. **Env won't load?** → Check gym.register in __init__.py, verify pip install -e
3. **Reward is NaN?** → Check for division by zero, clamp distances
4. **Policy doesn't learn?** → Check observation normalization, reward scale, action space bounds
5. **Isaac Sim crash?** → Check driver version (535+), check Python version (3.11)
6. **Assets won't load?** → First run downloads from NVIDIA servers (10+ min), check internet

## Project Status Tracking

Update this section as labs are completed:

| Lab | Status | Notes |
|-----|--------|-------|
| 01 | STARTED | |
| 02 | STARTED | |
| 03 | STARTED | |
| 04 | NOT STARTED | |
| 05 | NOT STARTED | Requires Lambda Labs |
| 06 | NOT STARTED | Requires Lambda Labs |
| 07 | NOT STARTED | Requires Lambda Labs |

## References

- [Isaac Lab Documentation](https://isaac-sim.github.io/IsaacLab/main/)
- [Isaac Sim Documentation](https://docs.isaacsim.omniverse.nvidia.com/)
- [SKRL Documentation](https://skrl.readthedocs.io/)
- [RSL-RL Repository](https://github.com/leggedrobotics/rsl_rl)