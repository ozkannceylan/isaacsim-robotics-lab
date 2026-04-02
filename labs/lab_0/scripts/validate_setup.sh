#!/usr/bin/env bash
# =============================================================================
# validate_setup.sh - Validate Isaac Sim + Isaac Lab Installation
#
# Usage: conda activate isaaclab && bash validate_setup.sh
#
# Runs a series of checks to verify the Vast.ai instance is correctly
# configured for Isaac Sim 5.1 + Isaac Lab development.
# =============================================================================
set -euo pipefail

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PASS_COUNT=0
FAIL_COUNT=0
WARN_COUNT=0

pass() { echo -e "  ${GREEN}PASS${NC}  $*"; ((PASS_COUNT++)); }
fail() { echo -e "  ${RED}FAIL${NC}  $*"; ((FAIL_COUNT++)); }
warn() { echo -e "  ${YELLOW}WARN${NC}  $*"; ((WARN_COUNT++)); }

# ---------------------------------------------------------------------------
# Check 1: nvidia-smi
# ---------------------------------------------------------------------------
echo ""
echo "=== Check 1: GPU Detection ==="

if command -v nvidia-smi &>/dev/null; then
    GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null | head -1)
    DRIVER_VER=$(nvidia-smi --query-gpu=driver_version --format=csv,noheader 2>/dev/null | head -1)
    VRAM=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader 2>/dev/null | head -1)

    if echo "$GPU_NAME" | grep -qi "RTX 4090"; then
        pass "GPU: $GPU_NAME ($VRAM)"
    elif echo "$GPU_NAME" | grep -qi "RTX"; then
        warn "GPU: $GPU_NAME (expected RTX 4090, but RTX should work)"
    else
        fail "GPU: $GPU_NAME (RTX with RT Cores required for Isaac Sim)"
    fi
    pass "Driver: $DRIVER_VER"
else
    fail "nvidia-smi not found"
fi

# ---------------------------------------------------------------------------
# Check 2: Conda environment
# ---------------------------------------------------------------------------
echo ""
echo "=== Check 2: Conda Environment ==="

if [[ -n "${CONDA_DEFAULT_ENV:-}" ]] && [[ "$CONDA_DEFAULT_ENV" == "isaaclab" ]]; then
    pass "Conda env: $CONDA_DEFAULT_ENV"
else
    fail "Conda env: '${CONDA_DEFAULT_ENV:-not activated}' (expected 'isaaclab')"
    echo "       Run: conda activate isaaclab"
fi

PYTHON_VER=$(python --version 2>&1 || echo "not found")
if echo "$PYTHON_VER" | grep -q "3.11"; then
    pass "Python: $PYTHON_VER"
else
    fail "Python: $PYTHON_VER (expected 3.11.x)"
fi

# ---------------------------------------------------------------------------
# Check 3: Isaac Sim import
# ---------------------------------------------------------------------------
echo ""
echo "=== Check 3: Isaac Sim ==="

ISAACSIM_VER=$(python -c "import isaacsim; print(isaacsim.__version__)" 2>/dev/null || echo "IMPORT_FAILED")
if [[ "$ISAACSIM_VER" == "IMPORT_FAILED" ]]; then
    fail "Isaac Sim: import failed"
else
    pass "Isaac Sim: $ISAACSIM_VER"
fi

# ---------------------------------------------------------------------------
# Check 4: Isaac Lab import
# ---------------------------------------------------------------------------
echo ""
echo "=== Check 4: Isaac Lab ==="

ISAACLAB_OK=$(python -c "import isaaclab; print('OK')" 2>/dev/null || echo "IMPORT_FAILED")
if [[ "$ISAACLAB_OK" == "OK" ]]; then
    pass "Isaac Lab: importable"
else
    fail "Isaac Lab: import failed"
fi

# ---------------------------------------------------------------------------
# Check 5: PyTorch + CUDA
# ---------------------------------------------------------------------------
echo ""
echo "=== Check 5: PyTorch ==="

TORCH_VER=$(python -c "import torch; print(torch.__version__)" 2>/dev/null || echo "IMPORT_FAILED")
if [[ "$TORCH_VER" == "IMPORT_FAILED" ]]; then
    fail "PyTorch: import failed"
else
    pass "PyTorch: $TORCH_VER"
fi

CUDA_AVAIL=$(python -c "import torch; print(torch.cuda.is_available())" 2>/dev/null || echo "False")
TORCH_CUDA=$(python -c "import torch; print(torch.version.cuda)" 2>/dev/null || echo "N/A")
if [[ "$CUDA_AVAIL" == "True" ]]; then
    pass "CUDA available: True (CUDA $TORCH_CUDA)"
else
    fail "CUDA available: False"
fi

GPU_COUNT=$(python -c "import torch; print(torch.cuda.device_count())" 2>/dev/null || echo "0")
GPU_TORCH_NAME=$(python -c "import torch; print(torch.cuda.get_device_name(0))" 2>/dev/null || echo "N/A")
pass "PyTorch GPU: $GPU_TORCH_NAME (devices: $GPU_COUNT)"

# ---------------------------------------------------------------------------
# Check 6: Isaac Sim headless smoke test
# ---------------------------------------------------------------------------
echo ""
echo "=== Check 6: Isaac Sim Headless Smoke Test ==="

SMOKE_RESULT=$(timeout 120 python -c "
from isaacsim import SimulationApp
app = SimulationApp({'headless': True})
print('HEADLESS_OK')
app.close()
" 2>/dev/null || echo "SMOKE_FAILED")

if echo "$SMOKE_RESULT" | grep -q "HEADLESS_OK"; then
    pass "Isaac Sim headless: OK"
else
    fail "Isaac Sim headless: failed (may need longer timeout on first run)"
    echo "       First run compiles shaders and downloads assets (~10GB)."
    echo "       Try running manually: python -c \"from isaacsim import SimulationApp; app = SimulationApp({'headless': True}); app.close()\""
fi

# ---------------------------------------------------------------------------
# Check 7: RL frameworks
# ---------------------------------------------------------------------------
echo ""
echo "=== Check 7: RL Frameworks ==="

RLGAMES_VER=$(python -c "import rl_games; print(rl_games.__version__ if hasattr(rl_games, '__version__') else 'installed')" 2>/dev/null || echo "IMPORT_FAILED")
if [[ "$RLGAMES_VER" == "IMPORT_FAILED" ]]; then
    warn "RL Games: not found (optional, installed by Isaac Lab)"
else
    pass "RL Games: $RLGAMES_VER"
fi

SKRL_VER=$(python -c "import skrl; print(skrl.__version__)" 2>/dev/null || echo "IMPORT_FAILED")
if [[ "$SKRL_VER" == "IMPORT_FAILED" ]]; then
    warn "SKRL: not found (optional)"
else
    pass "SKRL: $SKRL_VER"
fi

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
echo ""
echo "========================================"
echo " Validation Summary"
echo "========================================"
echo -e "  ${GREEN}PASS:${NC} $PASS_COUNT"
echo -e "  ${RED}FAIL:${NC} $FAIL_COUNT"
echo -e "  ${YELLOW}WARN:${NC} $WARN_COUNT"
echo ""

if (( FAIL_COUNT == 0 )); then
    echo -e "  ${GREEN}All critical checks passed!${NC}"
    echo "  Ready for Isaac Lab development."
else
    echo -e "  ${RED}$FAIL_COUNT check(s) failed. Review above and fix before proceeding.${NC}"
fi
echo ""
