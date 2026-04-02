# Lab 0: Cloud Setup and Validation

## Objective

Deploy Isaac Sim 5.1 + Isaac Lab 2.3.0 on a Vast.ai RTX 4090 instance. Validate GPU rendering, headless mode, and remote GUI access. Document the full setup as a reproducible guide.

## Why This Lab Exists

Cloud GPU setup for Isaac Sim is non-trivial. The NGC container needs RT Core validation, display forwarding for GUI mode, and correct driver versions. Getting this right before any robotics work saves hours of debugging later. The resulting setup guide is itself a valuable portfolio artifact.

## Prerequisites

- Vast.ai account with billing configured
- NGC account (free, for container access)
- SSH client + VNC viewer on local machine
- Basic Docker/container knowledge

## Deliverables

1. Working Isaac Sim GUI accessible via VNC from local machine
2. Headless script execution confirmed (no display required)
3. `cloud-setup-guide.md` with step-by-step instructions
4. Screenshot/recording of Isaac Sim running on Vast.ai

## Tasks

### 0.1 Vast.ai Instance Selection

Select an RTX 4090 instance with the following minimum specs:
- GPU: RTX 4090 (24GB VRAM)
- RAM: 32GB+
- Disk: 50GB+ (Isaac Sim assets are large)
- OS: Ubuntu 22.04 compatible
- Docker: Pre-installed

Filter for instances with good reliability scores (>95% uptime). Prefer EU-based instances for lower latency from Berlin.

### 0.2 NGC Container Setup

Pull and configure the official Isaac Sim container:
- Container: `nvcr.io/nvidia/isaac-sim:4.5.0` (or latest compatible with Isaac Lab 2.3.0)
- Verify RT Core detection inside container
- Validate NVIDIA driver version compatibility

### 0.3 GUI Access Setup

Configure remote desktop access for visual debugging and scene inspection:
- Option A: VNC server (TurboVNC + VirtualGL) inside container
- Option B: noVNC for browser-based access (no client install)
- Test rendering performance, ensure acceptable frame rates

### 0.4 Isaac Lab Installation

Install Isaac Lab 2.3.0 inside the running container:
- pip-based installation (recommended for cloud)
- Verify all extensions load correctly
- Run the compatibility checker script

### 0.5 Validation Checks

Run these validation scripts and document results:

| Check | Command | Expected Result |
|-------|---------|-----------------|
| GPU detection | `nvidia-smi` | RTX 4090, driver 535+ |
| RT Core test | Isaac Sim RTX rendering | Ray-traced output |
| Headless mode | `python -m isaacsim.app ...` | Runs without display |
| Isaac Lab import | `import isaaclab` | No errors |
| Sample env | Cartpole-v0 training (100 steps) | Converges |

### 0.6 Persistence and Cost Management

- Document snapshot/save strategy for Vast.ai (avoid re-setup on each session)
- Set up auto-shutdown script to prevent idle billing
- Calculate actual cost per session for budget tracking

## Success Criteria

- Isaac Sim GUI renders correctly via remote access
- Headless RL training runs without errors
- Total setup time documented (target: <2 hours for repeat setup)
- cloud-setup-guide.md is complete and tested

## Estimated Cloud Cost

3-4 hours at ~$0.30/hr = ~$1.00-1.20

## Notes

- Isaac Sim first launch downloads ~10GB of assets. Factor this into initial setup time.
- If VNC performance is poor, prioritize headless workflow and use GUI only for scene inspection.
- Consider creating a Vast.ai template for quick re-deployment.
