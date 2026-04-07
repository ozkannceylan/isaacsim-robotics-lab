#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ISAACLAB_DIR="${ISAACLAB_DIR:-/opt/IsaacLab}"
TARGET_SCRIPT="${ISAACLAB_WEBRTC_TARGET:-$ROOT_DIR/labs/lab_1/scripts/train_cartpole.sh}"
LIVESTREAM_MODE="${LIVESTREAM:-2}"
CONDA_SH="${CONDA_SH:-/opt/conda/etc/profile.d/conda.sh}"
CONDA_ENV_NAME="${CONDA_ENV_NAME:-isaaclab}"

if [[ $# -gt 0 && "$1" != -* ]]; then
    CANDIDATE="$1"
    if [[ "$CANDIDATE" != /* ]]; then
        CANDIDATE="$ROOT_DIR/$CANDIDATE"
    fi

    if [[ -f "$CANDIDATE" ]]; then
        TARGET_SCRIPT="$CANDIDATE"
        shift
    fi
fi

if [[ ! -f "$TARGET_SCRIPT" ]]; then
    echo "Launch target not found: $TARGET_SCRIPT" >&2
    echo "Usage: ./run_with_webrtc.sh [path/to/script.{sh,py}] [script args...]" >&2
    exit 1
fi

# Ensure the Isaac Lab conda environment is active before invoking Python.
if [[ -f "$CONDA_SH" ]]; then
    # shellcheck disable=SC1090
    source "$CONDA_SH"
    conda activate "$CONDA_ENV_NAME"
fi

# Repair Isaac Lab core package if only namespace packages are present.
if ! python -c "from isaaclab.app import AppLauncher" >/dev/null 2>&1; then
    echo "[WARN] isaaclab.app import failed. Reinstalling core package..."
    if [[ -d "$ISAACLAB_DIR/source/isaaclab" ]]; then
        (
            cd "$ISAACLAB_DIR/source/isaaclab"
            pip install --no-cache-dir -e . --no-build-isolation
        )
    else
        echo "[ERROR] Isaac Lab source not found at $ISAACLAB_DIR/source/isaaclab" >&2
        exit 1
    fi
fi

export HEADLESS=1
export LIVESTREAM="$LIVESTREAM_MODE"

echo "=== Isaac Lab WebRTC Launch ==="
echo "  Target:      $TARGET_SCRIPT"
echo "  Headless:    1"
echo "  Livestream:  $LIVESTREAM_MODE"
echo ""
echo "  Streaming ports (once app starts):"
echo "    HTTP API / health:  http://localhost:8011/v1/streaming/ready"
echo "    WebRTC server:      ws://localhost:49100"
echo "    API docs (Swagger): http://localhost:8011/docs"
echo ""
echo "  Connect with NVIDIA Kit Remote client, or SSH-tunnel both ports:"
echo "    ssh -L 8011:localhost:8011 -L 49100:localhost:49100 root@<host> -p <port>"
echo ""

case "$TARGET_SCRIPT" in
    *.sh)
        exec bash "$TARGET_SCRIPT" --livestream "$LIVESTREAM_MODE" "$@"
        ;;
    *.py)
        exec bash "$ISAACLAB_DIR/isaaclab.sh" -p "$TARGET_SCRIPT" --livestream "$LIVESTREAM_MODE" "$@"
        ;;
    *)
        echo "Unsupported target type: $TARGET_SCRIPT" >&2
        echo "Expected a .sh wrapper or an Isaac Lab .py entrypoint." >&2
        exit 1
        ;;
esac
