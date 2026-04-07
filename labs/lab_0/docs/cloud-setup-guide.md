# Cloud GPU Setup Guide for Isaac Sim + Isaac Lab

A complete guide to deploying NVIDIA Isaac Sim 5.1 and Isaac Lab 2.3.0 on cloud GPU instances. Covers the Docker-based pipeline, Vast.ai configuration, validation, training, and cost management.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Docker Image](#docker-image)
- [Vast.ai Deployment](#vastai-deployment)
- [Other Cloud Providers](#other-cloud-providers)
- [On-Start Script](#on-start-script)
- [Validation](#validation)
- [Training Your First Agent](#training-your-first-agent)
- [Video Recording](#video-recording)
- [Data Persistence and Backup](#data-persistence-and-backup)
- [Cost Management](#cost-management)
- [Troubleshooting](#troubleshooting)
- [Known Issues](#known-issues)
- [Appendix: Version Matrix](#appendix-version-matrix)

---

## Overview

Isaac Sim requires an NVIDIA RTX GPU with RT Cores for rendering. Since most local machines don't have this hardware, we use cloud GPU instances. This project uses a custom Docker image that bundles the entire stack:

```
Docker Image (ozkanceylan/isaacsim-robotics-lab:latest)
├── NVIDIA CUDA 12.8 Runtime (Ubuntu 22.04)
├── Miniconda + Python 3.11 (env: isaaclab)
├── Isaac Sim 5.1.0 (pip install from NVIDIA PyPI)
├── Isaac Lab 2.3.0 (source install at /opt/IsaacLab)
├── PyTorch 2.7.0+cu128
├── RL Games, SKRL (RL frameworks)
├── TensorBoard, pytest, matplotlib
└── On-start script at /opt/vastai_onstart.sh
```

Project code is **not** baked into the image. It's cloned from GitHub on every boot via the on-start script, ensuring you always have the latest version.

---

## Prerequisites

### Cloud Account

- **Vast.ai:** Create an account at [vast.ai](https://vast.ai), add billing (credit card or crypto). Minimum $5 credit recommended.
- **Other providers:** Any provider with NVIDIA RTX GPUs and Docker support (Lambda, RunPod, GCP, etc.).

### Local Machine

- SSH client (built into macOS/Linux, use Git Bash or WSL on Windows)
- Git
- VNC viewer (optional, for GUI access) — [TigerVNC](https://tigervnc.org/) or [RealVNC](https://www.realvnc.com/)
- Code editor (VS Code recommended)

### GPU Requirements

Isaac Sim requires NVIDIA GPUs with **RT Cores** for ray-traced rendering:

| GPU | RT Cores | VRAM | Supported |
|-----|----------|------|-----------|
| RTX 4090 | Yes | 24 GB | Yes (recommended) |
| RTX 5090 | Yes | 32 GB | Yes (tested) |
| RTX A6000 | Yes | 48 GB | Yes |
| RTX 3090 | Yes | 24 GB | Yes (older driver) |
| A100 | No | 40/80 GB | **No** |
| H100 | No | 80 GB | **No** |
| T4 | Yes (limited) | 16 GB | Partial (low VRAM) |

---

## Docker Image

### Image Details

- **Docker Hub:** `ozkanceylan/isaacsim-robotics-lab:latest`
- **Base:** `nvidia/cuda:12.8.0-devel-ubuntu22.04`
- **Size:** ~15 GB (compressed ~8 GB on Docker Hub)
- **Dockerfile:** `docker/Dockerfile` in the project repository

### Building the Image Locally

If you need to customize or rebuild the image:

```bash
cd docker/
bash build_and_push.sh              # defaults to ozkanceylan/isaacsim-robotics-lab:latest
bash build_and_push.sh myuser       # custom Docker Hub user
bash build_and_push.sh myuser v2    # custom tag
```

The build process:
1. Installs system dependencies (git, curl, VNC tools, Vulkan, etc.)
2. Sets up Miniconda with Python 3.11
3. Installs Isaac Sim 5.1.0 from NVIDIA PyPI
4. Clones Isaac Lab 2.3.0 from source and runs the installer
5. Installs the `isaaclab` core package (fix for import issue)
6. Pre-accepts the NVIDIA Omniverse EULA
7. Installs PyTorch 2.7.0 with CUDA 12.8 support
8. Copies the on-start script to `/opt/vastai_onstart.sh`

Build time: ~30-45 minutes (depends on network speed).

### What the Image Does NOT Include

- Project source code (cloned at runtime)
- Training checkpoints or logs
- User SSH keys or credentials
- VNC server configuration (can be added separately)

---

## Vast.ai Deployment

### Step 1: Use the Pre-Built Template

The easiest way to get started on Vast.ai:

1. Open the template: [Isaac Sim Template on Vast.ai](https://cloud.vast.ai/?ref_id=460420&creator_id=460420&name=isaacsim)
   - Template hash: `e2b4bc434edeb622c212f9966e532815`
2. The template pre-configures:
   - Docker image: `ozkanceylan/isaacsim-robotics-lab:latest`
   - On-start script
   - Recommended resource allocations

### Step 2: Select an Instance

Filter criteria:

| Criterion | Minimum | Recommended |
|-----------|---------|-------------|
| GPU | RTX 4090 (24 GB) | RTX 5090 (32 GB) |
| RAM | 32 GB | 64 GB |
| Disk | 50 GB | 100 GB |
| Upload speed | 100 Mbps | 500 Mbps+ |
| Reliability | >95% | >99% |
| Location | Any | EU (lower latency from Europe) |

### Step 3: Configure the Instance

- **Docker image:** `ozkanceylan/isaacsim-robotics-lab:latest`
- **On-start script:**
  ```
  bash /opt/vastai_onstart.sh
  ```
- **Disk allocation:** At least 50 GB (Isaac Sim assets are large)
- **Persistent storage:** Enable `/data` volume if available (for training artifacts)

### Step 4: Launch and Connect

```bash
# SSH into the instance (port and IP from Vast.ai dashboard)
ssh -p <port> root@<host>

# Verify GPU
nvidia-smi

# The conda environment is auto-activated
python -c "import torch; print(torch.cuda.is_available())"  # Should print True

# Project repo is at:
cd /workspace/isaacsim-robotics-lab
```

### Step 5: Set Idle Auto-Shutdown

On the Vast.ai dashboard, set the idle timeout to 30 minutes to avoid unnecessary charges.

---

## Other Cloud Providers

### Generic Docker Deployment

For any cloud provider with Docker + NVIDIA GPU support:

```bash
# Pull the image
docker pull ozkanceylan/isaacsim-robotics-lab:latest

# Run with GPU access and persistent storage
docker run -it --gpus all \
  --shm-size=8g \
  -v /host/data:/data \
  -p 6006:6006 \
  -p 6080:6080 \
  ozkanceylan/isaacsim-robotics-lab:latest

# Inside the container
conda activate isaaclab
git clone https://github.com/ozkannceylan/isaacsim-robotics-lab.git /workspace/isaacsim-robotics-lab
cd /workspace/isaacsim-robotics-lab
bash labs/lab_0/scripts/validate_setup.sh
```

### Lambda Cloud

Lambda instances come with NVIDIA drivers pre-installed:

```bash
# SSH in, then:
docker pull ozkanceylan/isaacsim-robotics-lab:latest
docker run -it --gpus all -v /home/ubuntu/data:/data ozkanceylan/isaacsim-robotics-lab:latest
```

### RunPod

Use the Docker image directly as the RunPod template image, or:

```bash
# In a RunPod terminal
docker pull ozkanceylan/isaacsim-robotics-lab:latest
docker run -it --gpus all -v /workspace:/data ozkanceylan/isaacsim-robotics-lab:latest
```

---

## On-Start Script

The on-start script (`docker/vastai_onstart.sh`, copied to `/opt/vastai_onstart.sh` in the image) runs automatically on every Vast.ai instance boot. It handles:

1. **Conda activation:** Activates the `isaaclab` environment
2. **Project clone/pull:** Clones from GitHub (or pulls latest if already cloned)
3. **Persistent symlinks:** Creates symlinks from `outputs/`, `checkpoints/`, `logs/` to `/data/` volume
4. **Sanity check:** Verifies GPU, Python, and CUDA availability

Logs are written to `/data/onstart.log`.

### Customization

To add your own startup steps, create a script at `docker/user_onstart.sh` and call it at the end of `vastai_onstart.sh`.

---

## Validation

### Full Validation Suite

```bash
conda activate isaaclab
cd /workspace/isaacsim-robotics-lab
bash labs/lab_0/scripts/validate_setup.sh
```

The validation script checks:

| # | Check | What It Verifies |
|---|-------|-----------------|
| 1 | GPU Detection | RTX GPU with RT Cores, driver version |
| 2 | Python Environment | Python 3.11, conda env or Docker |
| 3 | Isaac Sim | `import isaacsim` succeeds |
| 4 | Isaac Lab | `from isaaclab.app import AppLauncher` succeeds |
| 5 | PyTorch | PyTorch version, CUDA availability |
| 6 | Headless Smoke Test | Isaac Sim runs headless without errors |
| 7 | RL Frameworks | RL Games and SKRL importable |

### Manual Quick Checks

```bash
# GPU
nvidia-smi

# Python + CUDA
python -c "import torch; print(f'PyTorch {torch.__version__}, CUDA: {torch.cuda.is_available()}, GPU: {torch.cuda.get_device_name(0)}')"

# Isaac Sim
python -c "import isaacsim; print('Isaac Sim OK')"

# Isaac Lab
python -c "from isaaclab.app import AppLauncher; print('Isaac Lab OK')"
```

### First-Run Considerations

On the very first run after creating an instance:
- **Shader compilation:** Isaac Sim compiles GPU shaders on first launch (2-5 min)
- **Asset download:** Some assets are fetched from AWS S3 on first use (~10 GB)
- **EULA:** Already pre-accepted in the Docker image

Subsequent runs are much faster (10-30 seconds startup).

---

## Training Your First Agent

### CartPole (Smoke Test)

```bash
# Quick test: 50 iterations, ~20 seconds
bash /opt/IsaacLab/isaaclab.sh -p \
  /opt/IsaacLab/scripts/reinforcement_learning/rl_games/train.py \
  --task Isaac-Cartpole-v0 --headless --num_envs 512 --max_iterations 50
```

### CartPole (Full Training)

```bash
# Full training: 300 iterations, ~2 minutes
bash /opt/IsaacLab/isaaclab.sh -p \
  /opt/IsaacLab/scripts/reinforcement_learning/rl_games/train.py \
  --task Isaac-Cartpole-v0 --headless --num_envs 2048 --max_iterations 300
```

### Ant Locomotion

```bash
bash /opt/IsaacLab/isaaclab.sh -p \
  /opt/IsaacLab/scripts/reinforcement_learning/rl_games/train.py \
  --task Isaac-Ant-v0 --headless --num_envs 2048 --max_iterations 500
```

### Understanding CartPole Rewards

The default CartPole reward config uses penalty terms:
- Alive bonus: +1.0
- Angle penalty: -1.0
- Cart velocity penalty: -0.01
- Pole velocity penalty: -0.005
- Termination penalty: -2.0

**Negative total rewards are normal.** The agent improves from ~-1.80 toward 0. Near-zero is the goal. Check individual reward components in TensorBoard for details.

### `num_envs` Constraints

The RL Games default config for CartPole has:
- `minibatch_size: 8192`
- `horizon_length: 16`
- `batch_size = num_envs * horizon_length`

Therefore: `num_envs >= 512` (because 512 * 16 = 8192 = minibatch_size).

Using fewer environments will cause an `AssertionError`.

---

## Video Recording

### Record a Trained Policy

```bash
# After training, play back with video recording
bash /opt/IsaacLab/isaaclab.sh -p \
  /opt/IsaacLab/scripts/reinforcement_learning/rl_games/play.py \
  --task Isaac-Cartpole-v0 --headless --num_envs 4 \
  --video --video_length 200
```

Videos are saved to the training log directory under `videos/play/`.

### Custom Recording Scripts

The project includes custom recording scripts in `labs/lab_0/scripts/`:

```bash
# Single environment demo with sinusoidal control
bash /opt/IsaacLab/isaaclab.sh -p labs/lab_0/scripts/record_demo.py --headless --enable_cameras

# 16 parallel environments with random actions
bash /opt/IsaacLab/isaaclab.sh -p labs/lab_0/scripts/multi_env_demo.py --headless --enable_cameras
```

> **Key flag:** `--enable_cameras` is required for headless video recording. It enables Omniverse Replicator for offscreen rendering.

---

## Data Persistence and Backup

### Persistent Volume (`/data/`)

Vast.ai provides a persistent `/data` volume that survives instance restarts. The on-start script creates symlinks:

```
/workspace/isaacsim-robotics-lab/outputs/     -> /data/outputs/
/workspace/isaacsim-robotics-lab/checkpoints/ -> /data/checkpoints/
/workspace/isaacsim-robotics-lab/logs/        -> /data/logs/
```

### Backup Strategy

```bash
# Always push code changes before stopping an instance
cd /workspace/isaacsim-robotics-lab
git add -A && git commit -m "checkpoint: <description>" && git push

# Download large artifacts (videos, checkpoints) to local
scp -P <port> root@<host>:/data/checkpoints/model.pth ./local_backups/
scp -P <port> root@<host>:/workspace/isaacsim-robotics-lab/labs/lab_0/media/*.mp4 ./
```

### Data Flow

```
Local Machine (code editing, docs)
       │  git push
       v
    GitHub (source of truth)
       │  git pull (via on-start script)
       v
Cloud Instance (training, rendering)
       │  /data volume (persists across restarts)
       │  scp / git push (for code changes)
       v
Local Machine (analysis, portfolio)
```

---

## Cost Management

### Pricing (April 2026)

| GPU | Vast.ai Spot | Vast.ai On-Demand |
|-----|-------------|-------------------|
| RTX 4090 | $0.20-0.30/hr | $0.35-0.45/hr |
| RTX 5090 | $0.35-0.50/hr | $0.50-0.65/hr |

### Budget Tips

1. **Set idle auto-shutdown** to 30 minutes on the Vast.ai dashboard
2. **Use headless mode** (`--headless`) for all training — no display overhead
3. **Develop locally:** Write code, configs, and documentation on your local machine. Only SSH to the instance for execution
4. **Batch work:** Plan your cloud sessions. Start instance, run all experiments, push results, stop instance
5. **Monitor costs:** Vast.ai shows running cost in real-time on the dashboard

### Estimated Cost per Lab

| Lab | Estimated Hours | Estimated Cost |
|-----|----------------|---------------|
| Lab 0: Setup & Validation | 2-4 hrs | $1-2 |
| Lab 1: RL Fundamentals | 8-12 hrs | $3-5 |
| Lab 2: Custom Tasks | 10-15 hrs | $4-6 |
| Lab 3: Sensors & SynData | 8-12 hrs | $3-5 |
| Lab 4: Sim-to-Real | 10-15 hrs | $4-6 |
| **Total** | **38-58 hrs** | **$15-24** |

---

## Troubleshooting

### Isaac Sim Import Fails

```
ModuleNotFoundError: No module named 'isaaclab.app'
```

The Isaac Lab installer sometimes misses the core package:

```bash
cd /opt/IsaacLab/source/isaaclab
pip install -e . --no-build-isolation
```

### EULA Hangs on Import

```
import isaacsim  # hangs waiting for input
```

Pre-accept the EULA:

```bash
echo 'Y' | python -c "import isaacsim"
```

### Vulkan Driver Error (RTX 5090)

```
vkCreateInstance failed. Vulkan 1.1 is not supported
```

This occurs because RTX 5090 exposes Vulkan 1.4 but Ubuntu 22.04 has Vulkan loader 1.3. **This does not affect headless training or video recording.** Safe to ignore.

### Batch Size Assertion Error

```
AssertionError: self.batch_size % self.minibatch_size == 0
```

Increase `num_envs`. For CartPole with default RL Games config: `num_envs >= 512`.

### Out of Memory (OOM)

```
CUDA out of memory
```

Reduce `num_envs`. Monitor VRAM with:

```bash
watch -n 1 nvidia-smi
```

### Scripts Fail with `invalid option name`

```
set: pipefail: invalid option name
```

Windows line endings (`\r\n`) in shell scripts. Fix:

```bash
sed -i 's/\r$//' labs/lab_0/scripts/*.sh
```

Or configure git to handle this automatically:

```bash
git config core.autocrlf input
```

### Isaac Sim Slow First Launch

Normal. First launch compiles shaders and may download up to 10 GB of assets from AWS S3. Allow 5-10 minutes. Subsequent launches take 10-30 seconds.

### `isaaclab` Command Not Found

The Docker image doesn't add `isaaclab.sh` to PATH. Use the full path:

```bash
bash /opt/IsaacLab/isaaclab.sh -p <your_script.py>
```

---

## Known Issues

| Issue | Status | Workaround |
|-------|--------|------------|
| Vulkan 1.4 ICD vs 1.3 loader on RTX 5090 | Open (upstream) | Headless mode works fine |
| Isaac Sim captures stdout | By design | Use file markers or exit codes for detection |
| Isaac Lab 3.0 Beta breaking changes | Avoid | Stay on v2.3.0 |
| NumPy 2.x incompatibility | Occasional | `pip install "numpy<2"` |

---

## Appendix: Version Matrix

Validated on April 7, 2026, on an RTX 5090 instance:

| Component | Version |
|-----------|---------|
| GPU | NVIDIA GeForce RTX 5090 |
| VRAM | 32 GB |
| NVIDIA Driver | 570.144 |
| CUDA | 12.8 |
| Python | 3.11.15 |
| PyTorch | 2.7.0+cu128 |
| Isaac Sim | 5.1 |
| Isaac Lab | 2.3.0 |
| RL Games | Bundled |
| SKRL | Bundled |
| TensorBoard | Latest |
| imageio | 2.37.0 |
| OpenCV | 4.11.0 |
| MoviePy | 2.1.2 |
| Gymnasium | 1.2.0 |
| OS | Ubuntu 22.04 (Docker) |
