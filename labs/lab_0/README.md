# Lab 0: Cloud GPU Setup for Isaac Sim + Isaac Lab

Deploy NVIDIA Isaac Sim 5.1 and Isaac Lab 2.3.0 on a cloud GPU instance in under 10 minutes using a pre-built Docker image. This guide covers Vast.ai (primary) and generic cloud providers.

## Quick Start (Vast.ai)

### Option A: Use the Pre-Built Template (Fastest)

1. Open the [Isaac Sim Vast.ai Template](https://cloud.vast.ai/?ref_id=460420&creator_id=460420&name=isaacsim)
   - Template hash: `e2b4bc434edeb622c212f9966e532815`
2. Select an instance with:
   - **GPU:** RTX 4090 (24 GB) or RTX 5090 (32 GB) — RT Cores required
   - **RAM:** 32 GB+
   - **Disk:** 50 GB+
   - **Reliability:** >95%
3. Set the **on-start script** to:
   ```
   bash /opt/vastai_onstart.sh
   ```
4. Launch the instance
5. SSH in:
   ```bash
   ssh -p <port> root@<host>
   ```
6. You're ready. The conda environment `isaaclab` is auto-activated and the project repo is cloned at `/workspace/isaacsim-robotics-lab`.

### Option B: Manual Docker Image

If the template isn't available or you prefer manual setup:

1. Create a Vast.ai instance with any Ubuntu 22.04 base image
2. SSH in and pull the Docker image:
   ```bash
   docker pull ozkanceylan/isaacsim-robotics-lab:latest
   ```
3. Or use `ozkanceylan/isaacsim-robotics-lab:latest` directly as the Docker image when creating the instance on Vast.ai.

---

## Quick Start (Other Cloud Providers)

Works on any provider with NVIDIA RTX GPUs (Lambda, RunPod, GCP with L4/RTX, etc.).

### Prerequisites

- NVIDIA GPU with **RT Cores** (RTX 4090, RTX 5090, RTX A6000, etc.)
  - A100 and H100 are **NOT supported** — they lack RT Cores
- NVIDIA Driver 535+ installed
- Docker with NVIDIA Container Toolkit (`nvidia-docker`)

### Steps

```bash
# 1. Pull the image
docker pull ozkanceylan/isaacsim-robotics-lab:latest

# 2. Run the container
docker run -it --gpus all \
  -v /path/to/persistent/storage:/data \
  -p 6006:6006 \
  ozkanceylan/isaacsim-robotics-lab:latest

# 3. Inside the container, activate the environment
conda activate isaaclab

# 4. Clone the project
git clone https://github.com/ozkannceylan/isaacsim-robotics-lab.git /workspace/isaacsim-robotics-lab

# 5. Validate the stack
cd /workspace/isaacsim-robotics-lab
bash labs/lab_0/scripts/validate_setup.sh
```

---

## What's in the Docker Image

| Component | Version | Notes |
|-----------|---------|-------|
| Base | `nvidia/cuda:12.8.0-devel-ubuntu22.04` | |
| Python | 3.11 (Conda) | Env name: `isaaclab` |
| Isaac Sim | 5.1.0 | Installed via pip from NVIDIA PyPI |
| Isaac Lab | 2.3.0 | Source install at `/opt/IsaacLab` |
| PyTorch | 2.7.0+cu128 | CUDA 12.8 |
| RL Games | Bundled with Isaac Lab | Primary RL framework |
| SKRL | Bundled with Isaac Lab | Secondary RL framework |
| TensorBoard | Latest | Training visualization |
| pytest | Latest | Testing |

The Docker image does **not** contain project code. Code is cloned at boot via the on-start script, so you always get the latest version from GitHub.

---

## Validate Your Setup

After the instance is running:

```bash
# Run the full validation suite
conda activate isaaclab
bash labs/lab_0/scripts/validate_setup.sh
```

Expected output (all checks should PASS):

```
=== Check 1: GPU Detection ===
  PASS  GPU: NVIDIA GeForce RTX 4090 (24564 MiB)
  PASS  Driver: 535.xxx

=== Check 2: Python Environment ===
  PASS  Conda env: isaaclab
  PASS  Python: Python 3.11.x

=== Check 3: Isaac Sim ===
  PASS  Isaac Sim: OK

=== Check 4: Isaac Lab ===
  PASS  Isaac Lab: importable

=== Check 5: PyTorch ===
  PASS  PyTorch: 2.7.0+cu128
  PASS  CUDA available: True

=== Check 6: Isaac Sim Headless Smoke Test ===
  PASS  Isaac Sim headless: OK

  All critical checks passed!
```

> **Note:** The first run of Check 6 takes 2-5 minutes as Isaac Sim compiles shaders and downloads assets (~10 GB). Subsequent runs are fast (10-30s).

---

## Run Your First Training

```bash
# CartPole — 512 environments, 50 iterations (~20 seconds)
bash /opt/IsaacLab/isaaclab.sh -p \
  /opt/IsaacLab/scripts/reinforcement_learning/rl_games/train.py \
  --task Isaac-Cartpole-v0 --headless --num_envs 512 --max_iterations 50
```

For longer training (recommended 200-500 iterations for convergence):

```bash
bash /opt/IsaacLab/isaaclab.sh -p \
  /opt/IsaacLab/scripts/reinforcement_learning/rl_games/train.py \
  --task Isaac-Cartpole-v0 --headless --num_envs 2048 --max_iterations 300
```

### Record a Video of the Trained Policy

```bash
bash /opt/IsaacLab/isaaclab.sh -p \
  /opt/IsaacLab/scripts/reinforcement_learning/rl_games/play.py \
  --task Isaac-Cartpole-v0 --headless --num_envs 4 \
  --video --video_length 200
```

### Monitor Training with TensorBoard

```bash
# On the instance
tensorboard --logdir /root/logs --port 6006 --bind_all &

# On your local machine (SSH tunnel)
ssh -p <port> -L 6006:localhost:6006 root@<host>
# Then open http://localhost:6006 in your browser
```

---

## Architecture

```
┌────────────────────────────┐     ┌──────────────────────────────────┐
│  Local Machine             │     │  Cloud GPU Instance (RTX 4090)   │
│                            │     │                                  │
│  - Code editing (VS Code)  │ SSH │  Docker: isaacsim-robotics-lab   │
│  - Git operations          │────>│  ├── Isaac Sim 5.1 (PhysX GPU)  │
│  - Documentation           │     │  ├── Isaac Lab 2.3.0             │
│  - Analysis & portfolio    │     │  ├── PyTorch 2.7 + CUDA 12.8    │
│                            │     │  └── Conda env: isaaclab         │
└────────────────────────────┘     └──────────────────────────────────┘
           │                                      │
           │          git push / pull             │
           └──────────────┐  ┌────────────────────┘
                          v  v
                   ┌──────────────┐
                   │    GitHub    │
                   │ (source of  │
                   │   truth)    │
                   └──────────────┘
```

### Data Persistence

Training artifacts are symlinked to `/data/` (Vast.ai persistent volume):

| Path | Purpose |
|------|---------|
| `/data/outputs/` | Training outputs |
| `/data/checkpoints/` | Model checkpoints |
| `/data/logs/` | TensorBoard logs |

These survive instance restarts. **Always push important results to GitHub before destroying the instance.**

### Port Forwarding

| Service | Remote Port | SSH Tunnel | Purpose |
|---------|-------------|------------|---------|
| SSH | Assigned by Vast.ai | Direct | Shell access |
| TensorBoard | 6006 | `-L 6006:localhost:6006` | Training visualization |
| noVNC | 6080 | `-L 6080:localhost:6080` | Browser-based GUI (optional) |

---

## `num_envs` Guidelines

The number of parallel environments depends on your GPU VRAM:

| Environment | RTX 4090 (24 GB) | RTX 5090 (32 GB) |
|-------------|-------------------|-------------------|
| CartPole | Up to 8192 | Up to 8192+ |
| Ant | Up to 4096 | Up to 4096+ |
| Humanoid (G1) | 1024-2048 | 2048-4096 |

> **Important:** CartPole with default RL Games config requires `num_envs >= 512` because `minibatch_size=8192` and `horizon_length=16` (batch_size = num_envs * 16).

Monitor VRAM during training:
```bash
watch -n 1 nvidia-smi
```

---

## Cost Management

| Provider | GPU | Typical Cost | Notes |
|----------|-----|-------------|-------|
| Vast.ai | RTX 4090 | $0.25-0.40/hr | Spot pricing varies |
| Vast.ai | RTX 5090 | $0.40-0.60/hr | More VRAM (32 GB) |

Tips to minimize costs:
- **Set idle auto-shutdown** (30 min) on Vast.ai
- **Headless first:** Only use GUI when visual inspection is needed
- **Local development:** Write code, configs, and docs locally. Cloud is for execution only
- **Push before stop:** Always `git push` before stopping the instance

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: isaaclab.app` | Run: `cd /opt/IsaacLab/source/isaaclab && pip install -e . --no-build-isolation` |
| Isaac Sim hangs on first import | EULA acceptance needed: `echo 'Y' \| python -c "import isaacsim"` |
| `AssertionError: batch_size % minibatch_size` | Increase `num_envs` (min 512 for CartPole) |
| Vulkan ERROR_INCOMPATIBLE_DRIVER | RTX 5090 specific — safe to ignore for headless training |
| Isaac Sim slow on first run | Normal — shader compilation + asset download (~10 GB). Wait 5-10 min |
| `set: pipefail: invalid option name` | Windows line endings. Fix: `sed -i 's/\r$//' script.sh` |
| OOM (Out of Memory) | Reduce `num_envs`. Monitor with `nvidia-smi` |
| `isaaclab` command not found | Use full path: `bash /opt/IsaacLab/isaaclab.sh -p <script>` |

---

## File Structure

```
labs/lab_0/
├── README.md              # This file
├── scripts/
│   └── validate_setup.sh  # Stack validation script
├── tasks/
│   ├── PLAN.md            # Implementation plan
│   ├── ARCHITECTURE.md    # System architecture
│   ├── TODO.md            # Progress tracker
│   └── LESSONS.md         # Bugs, fixes, insights
├── docs/                  # Detailed English documentation
├── docs-turkish/          # Detailed Turkish documentation
├── media/                 # Demo videos and screenshots
│   ├── cartpole_trained.mp4
│   ├── demo.mp4
│   └── multi_env_demo.mp4
├── src/                   # Source code (if any)
└── tests/                 # Test files
```

---

## Validated Stack (April 2026)

Tested and confirmed working on RTX 5090 (32 GB):

| Component | Version |
|-----------|---------|
| GPU | NVIDIA GeForce RTX 5090 (32 GB VRAM) |
| Driver | 570.144 |
| CUDA | 12.8 |
| PyTorch | 2.7.0+cu128 |
| Isaac Sim | 5.1 |
| Isaac Lab | 2.3.0 |
| Python | 3.11.15 |
| OS | Ubuntu 22.04 (Docker) |

---

## Next Steps

After completing Lab 0 setup, proceed to **Lab 1: Isaac Lab RL Fundamentals** — CartPole deep-dive, Ant locomotion, and RL framework comparison (RL Games vs SKRL).
