#!/usr/bin/env bash
# =============================================================================
# evaluate.sh - Evaluate a trained policy and optionally record video
#
# Usage:
#   bash evaluate.sh --task Isaac-Cartpole-v0 --checkpoint <path>
#   bash evaluate.sh --task Isaac-Ant-v0 --checkpoint <path> --video
#   bash evaluate.sh --task Isaac-Ant-v0 --checkpoint <path> --gui
# =============================================================================
set -euo pipefail

FRAMEWORK="rl_games"
TASK=""
CHECKPOINT=""
VIDEO_ARGS=""
NUM_ENVS=64
ISAACLAB_DIR="${ISAACLAB_DIR:-/opt/IsaacLab}"

# Isaac Lab reads HEADLESS env var (int). Only pass --headless CLI flag if env var is NOT set.
if [[ -z "${HEADLESS:-}" ]]; then
    HEADLESS_FLAG="--headless"
else
    HEADLESS_FLAG=""
fi

# Parse args
while [[ $# -gt 0 ]]; do
    case "$1" in
        --framework)    FRAMEWORK="$2"; shift 2 ;;
        --task)         TASK="$2"; shift 2 ;;
        --checkpoint)   CHECKPOINT="$2"; shift 2 ;;
        --num_envs)     NUM_ENVS="$2"; shift 2 ;;
        --gui)          HEADLESS_FLAG=""; export HEADLESS=0; shift ;;
        --video)        VIDEO_ARGS="--video --video_length 300 --video_interval 100"; shift ;;
        *)              shift ;;
    esac
done

if [[ -z "$TASK" ]] || [[ -z "$CHECKPOINT" ]]; then
    echo "Usage: evaluate.sh --task <task> --checkpoint <path> [--video] [--gui]"
    exit 1
fi

PLAY_SCRIPT="$ISAACLAB_DIR/scripts/reinforcement_learning/${FRAMEWORK}/play.py"

if [[ ! -f "$PLAY_SCRIPT" ]]; then
    echo "Play script not found: $PLAY_SCRIPT"
    exit 1
fi

echo "=== Evaluation ==="
echo "  Framework:  $FRAMEWORK"
echo "  Task:       $TASK"
echo "  Checkpoint: $CHECKPOINT"
echo "  num_envs:   $NUM_ENVS"
echo "  Mode:       $([ -n "$HEADLESS_FLAG" ] && echo 'headless' || echo 'GUI (HEADLESS env='${HEADLESS:-unset}')')"
echo "  Video:      $([ -n "$VIDEO_ARGS" ] && echo 'yes' || echo 'no')"
echo ""

# shellcheck disable=SC2086
bash "$ISAACLAB_DIR/isaaclab.sh" -p "$PLAY_SCRIPT" \
    --task "$TASK" \
    --num_envs "$NUM_ENVS" \
    --checkpoint "$CHECKPOINT" \
    $HEADLESS_FLAG \
    $VIDEO_ARGS
