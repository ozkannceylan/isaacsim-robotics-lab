---
name: vastai-validate
description: Validates a Vast.ai GPU instance is correctly configured for Isaac Sim/Lab development. Use when asked to check, validate, or test a Vast.ai instance.
---

# Vast.ai Instance Validation Skill

When validating a Vast.ai instance, run these checks IN ORDER.
Stop at the first failure and report it clearly.

## Check sequence

1. **GPU check**: `nvidia-smi` -- must show GPU with driver loaded
2. **CUDA check**: `python3 -c "import torch; assert torch.cuda.is_available()"`
3. **Isaac Sim check**: `python3 -c "import isaacsim; print(isaacsim.__version__)"`
4. **Isaac Lab check**: `python3 -c "import isaaclab; print(isaaclab.__version__)"`
5. **Repo check**: `ls /workspace/isaacsim-robotics-lab/CLAUDE.md`
6. **Volume check**: `df -h /data && ls -la /data/`
7. **Symlink check**: `ls -la /workspace/isaacsim-robotics-lab/outputs`
8. **Headless test**: Run cartpole for 10 iterations
9. **Output check**: Verify training artifacts created in outputs/

## Important: conda activation

All Python checks must be run inside the isaaclab conda env:
```bash
source /opt/conda/etc/profile.d/conda.sh && conda activate isaaclab && <command>
```

## Output format

Report results as a checklist:
- [x] GPU: RTX 4090, Driver 535.x, CUDA 12.8
- [x] PyTorch 2.7.0+cu128, CUDA available
- [ ] Isaac Sim: FAILED -- import error: <error message>
...

## Common fixes

- "No module named isaacsim": `pip install "isaacsim[all,extscache]==5.1.0" --extra-index-url https://pypi.nvidia.com`
- "CUDA not available": check nvidia-smi, reinstall torch with CUDA
- "/data not mounted": volume not attached, check Vast.ai template
- "Permission denied": run with sudo or check file ownership
- "Shader compilation": first run takes 5-10 min, retry after
- "NumPy 2.x error": `pip install --force-reinstall "numpy<2"`
