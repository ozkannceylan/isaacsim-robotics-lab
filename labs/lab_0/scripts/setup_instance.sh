#!/usr/bin/env bash
# =============================================================================
# setup_instance.sh - Automated Vast.ai Instance Setup for Isaac Sim + Isaac Lab
#
# Usage: bash setup_instance.sh
#
# This script automates the full setup of a Vast.ai RTX 4090 instance:
#   1. Checks GPU, CUDA, and disk prerequisites
#   2. Installs Miniconda (if not present)
#   3. Creates a conda environment (isaaclab, Python 3.11)
#   4. Installs Isaac Sim 5.1.0 via pip
#   5. Installs Isaac Lab 2.3.x from source
#   6. Installs PyTorch 2.7.0 with CUDA 12.8
#   7. Clones the isaacsim-robotics-lab project repo
#
# Idempotent: safe to run multiple times.
# Estimated time: ~15-20 minutes on good connection.
# =============================================================================
set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
CONDA_DIR="$HOME/miniconda3"
CONDA_ENV_NAME="isaaclab"
PYTHON_VERSION="3.11"
ISAAC_SIM_VERSION="5.1.0"
ISAAC_LAB_TAG="v2.3.0"
ISAAC_LAB_DIR="$HOME/IsaacLab"
PYTORCH_VERSION="2.7.0"
TORCHVISION_VERSION="0.22.0"
PROJECT_REPO="https://github.com/ozkannceylan/isaacsim-robotics-lab.git"
PROJECT_DIR="$HOME/projects/isaacsim-robotics-lab"
LOG_FILE="$HOME/setup_instance.log"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

log()  { echo -e "${CYAN}[INFO]${NC}  $*" | tee -a "$LOG_FILE"; }
ok()   { echo -e "${GREEN}[OK]${NC}    $*" | tee -a "$LOG_FILE"; }
warn() { echo -e "${YELLOW}[WARN]${NC}  $*" | tee -a "$LOG_FILE"; }
fail() { echo -e "${RED}[FAIL]${NC}  $*" | tee -a "$LOG_FILE"; exit 1; }

separator() {
    echo "" | tee -a "$LOG_FILE"
    echo "========================================" | tee -a "$LOG_FILE"
    echo " $1" | tee -a "$LOG_FILE"
    echo "========================================" | tee -a "$LOG_FILE"
}

# Start log
echo "=== Setup started: $(date -u '+%Y-%m-%d %H:%M:%S UTC') ===" > "$LOG_FILE"

# ---------------------------------------------------------------------------
# Step 1: Check prerequisites
# ---------------------------------------------------------------------------
separator "Step 1: Checking prerequisites"

# GPU check
if ! command -v nvidia-smi &>/dev/null; then
    fail "nvidia-smi not found. Is the NVIDIA driver installed?"
fi

GPU_INFO=$(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || true)
if [[ -z "$GPU_INFO" ]]; then
    fail "nvidia-smi returned no GPU info."
fi

if echo "$GPU_INFO" | grep -qi "RTX"; then
    ok "GPU detected: $GPU_INFO"
else
    warn "GPU detected: $GPU_INFO (not RTX - Isaac Sim rendering may not work)"
fi

DRIVER_VERSION=$(nvidia-smi --query-gpu=driver_version --format=csv,noheader 2>/dev/null | head -1)
ok "NVIDIA driver: $DRIVER_VERSION"

# CUDA check
CUDA_VERSION=$(nvidia-smi | grep -oP 'CUDA Version: \K[0-9.]+' || true)
if [[ -z "$CUDA_VERSION" ]]; then
    warn "Could not determine CUDA version from nvidia-smi."
elif [[ "$CUDA_VERSION" == 12.* ]]; then
    ok "CUDA version: $CUDA_VERSION"
else
    warn "CUDA version: $CUDA_VERSION (expected 12.x)"
fi

# Disk space check
FREE_GB=$(df -BG --output=avail "$HOME" | tail -1 | tr -dc '0-9')
if (( FREE_GB < 50 )); then
    warn "Only ${FREE_GB}GB free disk space. Isaac Sim needs ~50GB+. Consider freeing space."
else
    ok "Disk space: ${FREE_GB}GB free"
fi

# ---------------------------------------------------------------------------
# Step 2: Install Miniconda
# ---------------------------------------------------------------------------
separator "Step 2: Installing Miniconda"

if [[ -d "$CONDA_DIR" ]] && [[ -f "$CONDA_DIR/bin/conda" ]]; then
    ok "Miniconda already installed at $CONDA_DIR"
else
    log "Downloading Miniconda installer..."
    MINICONDA_INSTALLER="/tmp/miniconda_installer.sh"
    curl -fsSL https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o "$MINICONDA_INSTALLER"
    log "Installing Miniconda to $CONDA_DIR..."
    bash "$MINICONDA_INSTALLER" -b -p "$CONDA_DIR" 2>&1 | tee -a "$LOG_FILE"
    rm -f "$MINICONDA_INSTALLER"
    ok "Miniconda installed"
fi

# Initialize conda for this script
# shellcheck disable=SC1091
source "$CONDA_DIR/etc/profile.d/conda.sh"

# Initialize conda for bash (idempotent)
if ! grep -q "conda initialize" "$HOME/.bashrc" 2>/dev/null; then
    log "Initializing conda for bash..."
    "$CONDA_DIR/bin/conda" init bash 2>&1 | tee -a "$LOG_FILE"
    ok "Conda initialized for bash"
else
    ok "Conda already initialized for bash"
fi

# ---------------------------------------------------------------------------
# Step 3: Create conda environment
# ---------------------------------------------------------------------------
separator "Step 3: Creating conda environment '$CONDA_ENV_NAME'"

if conda env list | grep -q "^${CONDA_ENV_NAME} "; then
    ok "Conda env '$CONDA_ENV_NAME' already exists"
else
    log "Creating conda env with Python $PYTHON_VERSION..."
    conda create -n "$CONDA_ENV_NAME" python="$PYTHON_VERSION" -y 2>&1 | tee -a "$LOG_FILE"
    ok "Conda env '$CONDA_ENV_NAME' created"
fi

conda activate "$CONDA_ENV_NAME"
PYTHON_VER=$(python --version 2>&1)
ok "Active environment: $CONDA_ENV_NAME ($PYTHON_VER)"

# ---------------------------------------------------------------------------
# Step 4: Install Isaac Sim 5.1 via pip
# ---------------------------------------------------------------------------
separator "Step 4: Installing Isaac Sim $ISAAC_SIM_VERSION"

if python -c "import isaacsim; print(isaacsim.__version__)" 2>/dev/null | grep -q "$ISAAC_SIM_VERSION"; then
    ok "Isaac Sim $ISAAC_SIM_VERSION already installed"
else
    log "Installing Isaac Sim $ISAAC_SIM_VERSION (this may take several minutes)..."
    pip install "isaacsim[all,extscache]==$ISAAC_SIM_VERSION" \
        --extra-index-url https://pypi.nvidia.com \
        2>&1 | tee -a "$LOG_FILE"
    ok "Isaac Sim $ISAAC_SIM_VERSION installed"
fi

# ---------------------------------------------------------------------------
# Step 5: Install Isaac Lab from source
# ---------------------------------------------------------------------------
separator "Step 5: Installing Isaac Lab ($ISAAC_LAB_TAG)"

if [[ -d "$ISAAC_LAB_DIR" ]]; then
    ok "Isaac Lab directory already exists at $ISAAC_LAB_DIR"
    cd "$ISAAC_LAB_DIR"
    CURRENT_TAG=$(git describe --tags --exact-match 2>/dev/null || echo "unknown")
    if [[ "$CURRENT_TAG" == "$ISAAC_LAB_TAG" ]]; then
        ok "Already on tag $ISAAC_LAB_TAG"
    else
        warn "Isaac Lab is on '$CURRENT_TAG', expected '$ISAAC_LAB_TAG'. Re-cloning..."
        cd "$HOME"
        rm -rf "$ISAAC_LAB_DIR"
        git clone --depth 1 --branch "$ISAAC_LAB_TAG" \
            https://github.com/isaac-sim/IsaacLab.git "$ISAAC_LAB_DIR" \
            2>&1 | tee -a "$LOG_FILE"
    fi
else
    log "Cloning Isaac Lab $ISAAC_LAB_TAG..."
    git clone --depth 1 --branch "$ISAAC_LAB_TAG" \
        https://github.com/isaac-sim/IsaacLab.git "$ISAAC_LAB_DIR" \
        2>&1 | tee -a "$LOG_FILE"
fi

cd "$ISAAC_LAB_DIR"
if python -c "import isaaclab" 2>/dev/null; then
    ok "Isaac Lab already importable"
else
    log "Running Isaac Lab installer (installs all RL frameworks)..."
    ./isaaclab.sh -i 2>&1 | tee -a "$LOG_FILE"
    ok "Isaac Lab installed"
fi

# ---------------------------------------------------------------------------
# Step 6: Install PyTorch
# ---------------------------------------------------------------------------
separator "Step 6: Installing PyTorch $PYTORCH_VERSION"

CURRENT_TORCH=$(python -c "import torch; print(torch.__version__)" 2>/dev/null || echo "none")
if [[ "$CURRENT_TORCH" == "$PYTORCH_VERSION"* ]]; then
    ok "PyTorch $CURRENT_TORCH already installed"
else
    log "Installing PyTorch $PYTORCH_VERSION with CUDA 12.8..."
    pip install "torch==$PYTORCH_VERSION" "torchvision==$TORCHVISION_VERSION" \
        --index-url https://download.pytorch.org/whl/cu128 \
        2>&1 | tee -a "$LOG_FILE"
    ok "PyTorch installed"
fi

# ---------------------------------------------------------------------------
# Step 7: Clone project repository
# ---------------------------------------------------------------------------
separator "Step 7: Cloning project repository"

if [[ -d "$PROJECT_DIR" ]]; then
    ok "Project repo already exists at $PROJECT_DIR"
    cd "$PROJECT_DIR"
    git pull --ff-only 2>&1 | tee -a "$LOG_FILE" || warn "git pull failed (may have local changes)"
else
    log "Cloning $PROJECT_REPO..."
    mkdir -p "$(dirname "$PROJECT_DIR")"
    git clone "$PROJECT_REPO" "$PROJECT_DIR" 2>&1 | tee -a "$LOG_FILE"
    ok "Project cloned to $PROJECT_DIR"
fi

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
separator "Setup Complete"

echo "" | tee -a "$LOG_FILE"
echo "  GPU:          $GPU_INFO" | tee -a "$LOG_FILE"
echo "  Driver:       $DRIVER_VERSION" | tee -a "$LOG_FILE"
echo "  CUDA:         $CUDA_VERSION" | tee -a "$LOG_FILE"
echo "  Conda env:    $CONDA_ENV_NAME" | tee -a "$LOG_FILE"
echo "  Python:       $(python --version 2>&1)" | tee -a "$LOG_FILE"

ISAACSIM_VER=$(python -c "import isaacsim; print(isaacsim.__version__)" 2>/dev/null || echo "check manually")
TORCH_VER=$(python -c "import torch; print(torch.__version__)" 2>/dev/null || echo "check manually")
TORCH_CUDA=$(python -c "import torch; print(torch.version.cuda)" 2>/dev/null || echo "N/A")

echo "  Isaac Sim:    $ISAACSIM_VER" | tee -a "$LOG_FILE"
echo "  Isaac Lab:    $ISAAC_LAB_DIR ($ISAAC_LAB_TAG)" | tee -a "$LOG_FILE"
echo "  PyTorch:      $TORCH_VER (CUDA $TORCH_CUDA)" | tee -a "$LOG_FILE"
echo "  Disk free:    ${FREE_GB}GB" | tee -a "$LOG_FILE"
echo "  Project:      $PROJECT_DIR" | tee -a "$LOG_FILE"
echo "  Log:          $LOG_FILE" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

ok "Next step: run validate_setup.sh to verify everything works."
echo "  conda activate $CONDA_ENV_NAME" | tee -a "$LOG_FILE"
echo "  bash $PROJECT_DIR/labs/lab_0/scripts/validate_setup.sh" | tee -a "$LOG_FILE"

echo "" | tee -a "$LOG_FILE"
echo "=== Setup finished: $(date -u '+%Y-%m-%d %H:%M:%S UTC') ===" | tee -a "$LOG_FILE"
