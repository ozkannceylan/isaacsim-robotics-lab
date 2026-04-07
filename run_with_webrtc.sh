#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ISAACLAB_DIR="${ISAACLAB_DIR:-/opt/IsaacLab}"
TARGET_SCRIPT="${ISAACLAB_WEBRTC_TARGET:-$ROOT_DIR/labs/lab_1/scripts/train_cartpole.sh}"
LIVESTREAM_MODE="${ISAACLAB_LIVESTREAM:-2}"

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

export HEADLESS=1
export ISAACLAB_LIVESTREAM="$LIVESTREAM_MODE"

echo "=== Isaac Lab WebRTC Launch ==="
echo "  Target:      $TARGET_SCRIPT"
echo "  Headless:    1"
echo "  Livestream:  $LIVESTREAM_MODE"
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
