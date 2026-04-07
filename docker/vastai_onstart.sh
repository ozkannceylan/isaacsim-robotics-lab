#!/usr/bin/env bash
# =============================================================================
# vastai_onstart.sh — Runs on every Vast.ai instance boot
#
# This script is executed automatically when a Vast.ai instance starts.
# It clones/pulls the project repo and sets up symlinks to the persistent
# /data volume so training artifacts survive instance destruction.
#
# Vast.ai on-start script config:
#   bash /opt/vastai_onstart.sh
# =============================================================================
set -euo pipefail

LOG="/data/onstart.log"
echo "=== on-start: $(date -u '+%Y-%m-%d %H:%M:%S UTC') ===" | tee -a "$LOG"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
PROJECT_REPO="https://github.com/ozkannceylan/isaacsim-robotics-lab.git"
PROJECT_DIR="/workspace/isaacsim-robotics-lab"
DATA_DIR="/data"

# ---------------------------------------------------------------------------
# Activate conda
# ---------------------------------------------------------------------------
source /opt/conda/etc/profile.d/conda.sh
conda activate isaaclab

# ---------------------------------------------------------------------------
# Isaac Lab environment defaults (persist across all SSH sessions)
# ---------------------------------------------------------------------------
cat > /etc/profile.d/isaaclab_env.sh << 'ENVEOF'
export HEADLESS=1
export LIVESTREAM=2
ENVEOF
chmod +x /etc/profile.d/isaaclab_env.sh
export HEADLESS=1
export LIVESTREAM=2
echo "[OK]   Set HEADLESS=1, LIVESTREAM=2 (WebRTC)" | tee -a "$LOG"

# ---------------------------------------------------------------------------
# Repair Isaac Lab core package if only namespace packages are present
#
# Some images end up with isaaclab sub-packages installed but not the core
# editable package. In that case `isaaclab` resolves as a namespace package,
# which breaks runtime inspection in AppLauncher-driven flows.
# ---------------------------------------------------------------------------
echo "[INFO] Verifying Isaac Lab core package..." | tee -a "$LOG"
if python -c "from isaaclab.app import AppLauncher" >/dev/null 2>&1; then
    echo "[OK]   isaaclab.app import works." | tee -a "$LOG"
else
    echo "[WARN] isaaclab.app import failed. Reinstalling core package..." | tee -a "$LOG"
    if [[ -d "/opt/IsaacLab/source/isaaclab" ]]; then
        cd /opt/IsaacLab/source/isaaclab
        pip install --no-cache-dir -e . --no-build-isolation 2>&1 | tee -a "$LOG"
        cd - >/dev/null
        if python -c "from isaaclab.app import AppLauncher" >/dev/null 2>&1; then
            echo "[OK]   isaaclab core package repaired." | tee -a "$LOG"
        else
            echo "[WARN] isaaclab.app import still failing after repair." | tee -a "$LOG"
        fi
    else
        echo "[WARN] /opt/IsaacLab/source/isaaclab not found; cannot repair core package." | tee -a "$LOG"
    fi
fi

# ---------------------------------------------------------------------------
# Clone or pull project repo
# ---------------------------------------------------------------------------
if [[ -d "$PROJECT_DIR/.git" ]]; then
    echo "[INFO] Project repo exists, pulling latest..." | tee -a "$LOG"
    cd "$PROJECT_DIR"
    git pull --ff-only 2>&1 | tee -a "$LOG" || echo "[WARN] git pull failed (may have local changes)" | tee -a "$LOG"
else
    echo "[INFO] Cloning project repo..." | tee -a "$LOG"
    git clone "$PROJECT_REPO" "$PROJECT_DIR" 2>&1 | tee -a "$LOG"
fi

cd "$PROJECT_DIR"

# ---------------------------------------------------------------------------
# Persistent volume symlinks
#
# /data is a Vast.ai persistent volume that survives instance restarts.
# Symlink training outputs there so they aren't lost.
# ---------------------------------------------------------------------------
echo "[INFO] Setting up persistent volume symlinks..." | tee -a "$LOG"

mkdir -p "$DATA_DIR/outputs" "$DATA_DIR/checkpoints" "$DATA_DIR/logs"

# Create symlinks only if they don't already exist
for dir in outputs checkpoints logs; do
    target="$PROJECT_DIR/$dir"
    if [[ -L "$target" ]]; then
        echo "[OK]   $dir -> $(readlink "$target")" | tee -a "$LOG"
    elif [[ -d "$target" ]]; then
        echo "[WARN] $dir is a real directory, moving contents to /data and symlinking..." | tee -a "$LOG"
        cp -rn "$target/"* "$DATA_DIR/$dir/" 2>/dev/null || true
        rm -rf "$target"
        ln -s "$DATA_DIR/$dir" "$target"
        echo "[OK]   $dir -> $DATA_DIR/$dir" | tee -a "$LOG"
    else
        ln -s "$DATA_DIR/$dir" "$target"
        echo "[OK]   $dir -> $DATA_DIR/$dir" | tee -a "$LOG"
    fi
done

# ---------------------------------------------------------------------------
# Quick sanity check
# ---------------------------------------------------------------------------
echo "" | tee -a "$LOG"
echo "[INFO] Quick sanity check..." | tee -a "$LOG"

GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null | head -1 || echo "UNKNOWN")
PYTHON_VER=$(python --version 2>&1)
TORCH_CUDA=$(python -c "import torch; print(torch.cuda.is_available())" 2>/dev/null || echo "False")

echo "  GPU:          $GPU_NAME" | tee -a "$LOG"
echo "  Python:       $PYTHON_VER" | tee -a "$LOG"
echo "  CUDA (torch): $TORCH_CUDA" | tee -a "$LOG"

if [[ "$TORCH_CUDA" == "True" ]]; then
    echo "[OK]   Instance ready for Isaac Lab development." | tee -a "$LOG"
else
    echo "[WARN] CUDA not available via PyTorch. Check GPU and driver." | tee -a "$LOG"
fi

echo "=== on-start complete: $(date -u '+%Y-%m-%d %H:%M:%S UTC') ===" | tee -a "$LOG"
