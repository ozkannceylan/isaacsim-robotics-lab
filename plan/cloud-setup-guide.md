# Cloud Setup Guide: Vast.ai + Isaac Sim

Practical reference for deploying Isaac Sim 5.1 and Isaac Lab 2.3.0 on Vast.ai with an RTX 4090 instance.

## Account Setup

### Vast.ai
1. Create account at vast.ai
2. Add billing (credit card or crypto)
3. Load minimum $10 credit to start
4. Generate SSH key pair and upload public key to Vast.ai settings

### NVIDIA NGC
1. Register at ngc.nvidia.com (free)
2. Join NVIDIA Developer Program
3. Generate NGC API key: NGC dashboard > Setup > API Key
4. Save the API key securely (needed for container pulls)

## Instance Selection Criteria

Search Vast.ai marketplace with these filters:

| Parameter | Requirement | Reason |
|-----------|-------------|--------|
| GPU | RTX 4090 | RT Cores for Isaac Sim rendering |
| VRAM | 24GB | Minimum for Isaac Sim + Isaac Lab |
| RAM | 32GB+ | Asset loading, parallel envs |
| Disk | 80GB+ | Isaac Sim container + assets + outputs |
| CUDA | 12.0+ | Isaac Sim 5.1 requirement |
| Reliability | >95% | Avoid interrupted sessions |
| Region | EU preferred | Lower latency from Berlin |
| Docker | Yes | Container-based deployment |

**Cost target:** ~$0.30/hr on-demand. Avoid spot instances for initial setup (interruption risk during long asset downloads).

## Container Deployment

### Option A: NGC Isaac Sim Container (Recommended)

```bash
# On Vast.ai instance
docker login nvcr.io
# Username: $oauthtoken
# Password: <NGC API Key>

# Pull Isaac Sim container (check exact tag for 5.1 compatibility)
docker pull nvcr.io/nvidia/isaac-sim:4.5.0

# Run with GPU access and display forwarding
docker run --gpus all -it --rm \
  --network host \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v ~/isaacsim-data:/root/isaacsim-data \
  nvcr.io/nvidia/isaac-sim:4.5.0
```

### Option B: Pip Installation (Lighter, Isaac Lab focused)

```bash
# Create conda environment
conda create -n isaaclab python=3.10
conda activate isaaclab

# Install Isaac Sim via pip
pip install 'isaacsim[all,extscache]==4.5.0' --extra-index-url https://pypi.nvidia.com

# Install Isaac Lab 2.3.0
git clone --branch v2.3.0 https://github.com/isaac-sim/IsaacLab.git
cd IsaacLab
./isaaclab.sh -i
```

## Remote GUI Access

### VNC Setup (Inside Container or Instance)

```bash
# Install TurboVNC + VirtualGL
apt-get update && apt-get install -y turbovnc virtualgl

# Start VNC server
/opt/TurboVNC/bin/vncserver :1 -geometry 1920x1080 -depth 24

# Note the port (typically 5901)
```

From local machine:
```bash
# SSH tunnel
ssh -L 5901:localhost:5901 root@<vast-ip> -p <port>

# Connect with VNC viewer to localhost:5901
```

### noVNC Setup (Browser-based, no client needed)

```bash
# Install noVNC
apt-get install -y novnc websockify

# Start websockify bridge
websockify --web /usr/share/novnc 6080 localhost:5901 &

# Access via browser: http://localhost:6080/vnc.html
```

## Validation Checklist

Run these checks after setup:

```bash
# 1. GPU detection
nvidia-smi
# Expected: RTX 4090, driver 535+

# 2. CUDA version
nvcc --version
# Expected: CUDA 12.x

# 3. Isaac Sim headless test
cd /isaac-sim  # or wherever installed
python -c "from isaacsim import SimulationApp; app = SimulationApp({'headless': True}); print('Isaac Sim OK'); app.close()"

# 4. Isaac Lab import
python -c "import isaaclab; print('Isaac Lab OK')"

# 5. Quick training test (headless)
python source/standalone/tutorials/00_sim/create_empty.py --headless
```

## Cost Management

### Auto-shutdown Script

```bash
# save as ~/auto_shutdown.sh
#!/bin/bash
# Shut down instance if GPU idle for 30 minutes
IDLE_THRESHOLD=30  # minutes
# Monitor nvidia-smi utilization
# If <5% for IDLE_THRESHOLD, trigger shutdown
```

### Session Workflow

1. Start instance
2. Pull latest code from GitHub
3. Do work (training, development)
4. Push results to GitHub / download outputs
5. Stop instance (do NOT destroy, preserves disk)

### Budget Tracking

| Item | Cost |
|------|------|
| RTX 4090 instance | ~$0.30/hr |
| Storage (persistent) | ~$0.01/GB/hr |
| Data transfer | Usually included |
| **Target monthly budget** | **$15-20** |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No RT-capable GPU" | Verify RTX 4090 detected, check driver version |
| VNC black screen | Install VirtualGL, use `vglrun` prefix |
| Slow asset loading | First launch downloads ~10GB. Be patient. |
| Out of disk space | Increase disk allocation or clean `/tmp` |
| Container exits | Check GPU memory with `nvidia-smi`, may need to reduce `num_envs` |
| Isaac Lab import error | Verify Python 3.10, correct Isaac Sim version |

## File Sync Strategy

Keep code in GitHub, data on persistent disk:

```
GitHub (code, configs, plans)
  |
  v
Vast.ai Instance (runtime, training)
  |
  v
Local Machine (analysis, writing, portfolio)
```

- Push code changes to GitHub before stopping instance
- Download training artifacts (checkpoints, videos, logs) via SCP
- Do not rely on Vast.ai disk persistence for critical data
