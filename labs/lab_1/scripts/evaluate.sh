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
HEADLESS="--headless"
VIDEO_ARGS=""
NUM_ENVS=64
ISAACLAB_DIR="${ISAACLAB_DIR:-$HOME/IsaacLab}"

# Parse args
while [[ $# -gt 0 ]]; do
    case "$1" in
        --framework)    FRAMEWORK="$2"; shift 2 ;;
        --task)         TASK="$2"; shift 2 ;;
        --checkpoint)   CHECKPOINT="$2"; shift 2 ;;
        --num_envs)     NUM_ENVS="$2"; shift 2 ;;
        --gui)          HEADLESS=""; shift ;;
        --video)        VIDEO_ARGS="--video --video_length 300 --video_interval 100"; shift ;;
        *)              shift ;;
    esac
done

if [[ -z "$TASK" ]] || [[ -z "$CHECKPOINT" ]]; then
    echo "Usage: evaluate.sh --task <task> --checkpoint <path> [--video] [--gui]"
    exit 1
fi

PLAY_SCRIPT="$ISAACLAB_DIR/source/standalone/workflows/${FRAMEWORK}/play.py"

if [[ ! -f "$PLAY_SCRIPT" ]]; then
    echo "Play script not found: $PLAY_SCRIPT"
    exit 1
fi

echo "=== Evaluation ==="
echo "  Framework:  $FRAMEWORK"
echo "  Task:       $TASK"
echo "  Checkpoint: $CHECKPOINT"
echo "  num_envs:   $NUM_ENVS"
echo "  Mode:       $([ -n "$HEADLESS" ] && echo 'headless' || echo 'GUI')"
echo "  Video:      $([ -n "$VIDEO_ARGS" ] && echo 'yes' || echo 'no')"
echo ""

# shellcheck disable=SC2086
python "$PLAY_SCRIPT" \
    --task "$TASK" \
    --num_envs "$NUM_ENVS" \
    --checkpoint "$CHECKPOINT" \
    $HEADLESS \
    $VIDEO_ARGS
