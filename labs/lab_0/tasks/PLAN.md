# Lab 0: Cloud Setup and Validation - Implementation Plan

## Overview

Deploy Isaac Sim 5.1 + Isaac Lab 2.3.x on a Vast.ai RTX 4090 instance. Validate GPU rendering, headless mode, and remote GUI access. Produce a reproducible setup that can be re-deployed in <30 minutes.

## Version Matrix

| Component | Version | Install Method |
|-----------|---------|----------------|
| Isaac Sim | 5.1.0 | pip (NVIDIA PyPI) |
| Isaac Lab | 2.3.x (v2.3.0 tag) | Source (git clone + isaaclab.sh) |
| Python | 3.11 | Conda |
| PyTorch | 2.7.0 | pip (cu128) |
| CUDA | 12.x | Pre-installed on Vast.ai |
| OS | Ubuntu 22.04 | Vast.ai base image |

---

## Phase 1: Instance Selection and SSH Setup

**Steps:**
1. Log into Vast.ai, filter for RTX 4090 instances
2. Select instance: 24GB VRAM, 32GB+ RAM, 50GB+ disk, Ubuntu 22.04
3. Prefer EU-based instances (lower latency from Berlin)
4. Look for reliability score >95%
5. Set up SSH key authentication
6. Verify SSH connection: `ssh -p <port> root@<vast-ip>`
7. Set idle auto-shutdown timeout (e.g., 30 min)

**Gate:** SSH connection established, nvidia-smi shows RTX 4090.

---

## Phase 2: Run setup_instance.sh

**Steps:**
1. Clone this repo on the instance (or scp the script)
2. Run: `bash labs/lab_0/scripts/setup_instance.sh`
3. Monitor the log for errors
4. Source bashrc to pick up conda: `source ~/.bashrc`
5. Activate env: `conda activate isaaclab`

**Gate:** Script completes without errors. Log saved to ~/setup_instance.log.

---

## Phase 3: Run validate_setup.sh

**Steps:**
1. Activate conda env: `conda activate isaaclab`
2. Run: `bash labs/lab_0/scripts/validate_setup.sh`
3. All critical checks should pass
4. If Isaac Sim headless test fails on first run, wait for shader compilation (~5-10 min), then retry

**Gate:** All PASS, zero FAIL in validation summary.

---

## Phase 4: VNC Setup (Optional)

**Steps:**
1. Run: `sudo bash labs/lab_0/scripts/setup_vnc.sh --novnc`
2. Set up SSH tunnel from local machine
3. Connect via VNC viewer or browser (noVNC)
4. Verify desktop renders
5. Test GPU rendering: `vglrun glxgears`

**Gate:** VNC desktop visible, GPU-accelerated rendering works.

---

## Phase 5: First Isaac Lab Training

**Steps:**
1. Navigate to Isaac Lab directory: `cd ~/IsaacLab`
2. Run CartPole headless training (smoke test):
   ```bash
   python source/standalone/workflows/rl_games/train.py \
       --task Isaac-Cartpole-v0 --headless --num_envs 2048 \
       --max_iterations 100
   ```
3. Verify training produces output (rewards improving)
4. Check GPU utilization during training: `nvidia-smi`
5. Save training curve screenshot to `labs/lab_0/media/`

**Gate:** CartPole training runs without errors. Reward trend visible.

---

## Phase 6: Documentation and Evidence

**Steps:**
1. Capture evidence for each phase:
   - Screenshot of nvidia-smi output
   - validate_setup.sh output (copy to docs/)
   - CartPole training curve (TensorBoard screenshot or terminal output)
   - VNC desktop screenshot (if applicable)
2. Update TODO.md: mark all phases complete
3. Update LESSONS.md with any issues encountered
4. Write English docs (docs/) and Turkish docs (docs-turkish/)
5. Git push all results

**Gate:** All evidence files in media/. Docs written. Git pushed.
