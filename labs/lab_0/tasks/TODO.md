# Lab 0: TODO

## Current Focus

Phase 6 - Documentation and Evidence (final phase)

## Blockers

None

---

## Phase 1: Instance Selection and SSH Setup
- [x] Select RTX instance on Vast.ai (RTX 5090 32GB, EU)
- [x] Configure SSH key authentication
- [x] Verify SSH connection (ssh -p 20295 root@213.224.31.105)
- [x] Set idle auto-shutdown timeout
- [x] Verify nvidia-smi shows RTX 5090, Driver 570.144, CUDA 12.8

## Phase 2: Docker-Based Setup (replaces old setup_instance.sh)
- [x] Docker image built and pushed: ozkanceylan/isaacsim-robotics-lab:latest
- [x] Repo auto-cloned to /workspace/isaacsim-robotics-lab via vastai_onstart.sh
- [x] Isaac Sim import OK (EULA pre-accepted in Docker image)
- [x] Isaac Lab 2.3.0 import OK (core package installed in Docker image)
- [x] Python 3.11.15 system-wide (no conda needed)

## Phase 3: Validation Checks
- [x] nvidia-smi: RTX 5090, 32GB VRAM, Driver 570.144, CUDA 12.8
- [x] PyTorch 2.7.0+cu128, CUDA available
- [x] Isaac Sim import OK
- [x] Isaac Lab 2.3.0 import OK
- [x] Repo cloned at /workspace/isaacsim-robotics-lab
- [x] Disk space: 182G free (root), 3.1T free (data)

## Phase 4: VNC Setup (Optional — skipped)
- [ ] Not needed for headless workflow
- [ ] Vulkan 1.4 ICD vs 1.3 loader mismatch blocks GUI on RTX 5090

## Phase 5: First Isaac Lab Training + Video Recording
- [x] CartPole headless training: 512 envs, 50 iterations, ~17s wall clock
- [x] Rewards improving: -1.80 → -1.57 (expected negative with default config)
- [x] GPU utilization confirmed via nvidia-smi
- [x] Checkpoint saved: /root/logs/rl_games/cartpole/2026-04-07_10-51-51/nn/cartpole.pth
- [x] Video: trained policy rollout (cartpole_trained.mp4, 282KB)
- [x] Video: standalone demo with sinusoidal control (demo.mp4, 197KB)
- [x] Video: 16 parallel envs with random actions (multi_env_demo.mp4, 333KB)

## Phase 6: Documentation and Evidence
- [x] LESSONS.md updated with validated versions, working commands, insights
- [x] TODO.md updated with completed items
- [ ] nvidia-smi screenshot → media/
- [x] Write English documentation (docs/cloud-setup-guide.md)
- [x] Write Turkish documentation (docs-turkish/cloud-setup-guide.md)
- [x] Write Lab 0 README.md (quick-start guide)
- [ ] Git commit all results
- [ ] Git push
