#!/usr/bin/env bash
# =============================================================================
# train_ant.sh - Train Ant locomotion with Isaac Lab
#
# Usage:
#   bash train_ant.sh                               # defaults: rl_games, 2048 envs
#   bash train_ant.sh --num_envs 4096               # custom env count
#   bash train_ant.sh --framework skrl              # use SKRL
#   bash train_ant.sh --max_iterations 1000         # longer training
# =============================================================================
set -euo pipefail

# Defaults
FRAMEWORK="rl_games"
NUM_ENVS=2048
MAX_ITERATIONS=1000
HEADLESS="--headless"
EXTRA_ARGS=""
TASK="Isaac-Ant-v0"

# Parse args
while [[ $# -gt 0 ]]; do
    case "$1" in
        --framework)    FRAMEWORK="$2"; shift 2 ;;
        --num_envs)     NUM_ENVS="$2"; shift 2 ;;
        --max_iterations) MAX_ITERATIONS="$2"; shift 2 ;;
        --gui)          HEADLESS=""; shift ;;
        --task)         TASK="$2"; shift 2 ;;
        *)              EXTRA_ARGS="$EXTRA_ARGS $1"; shift ;;
    esac
done

ISAACLAB_DIR="${ISAACLAB_DIR:-$HOME/IsaacLab}"
SCRIPT_DIR="$ISAACLAB_DIR/source/standalone/workflows/${FRAMEWORK}"

case "$FRAMEWORK" in
    rl_games)  TRAIN_SCRIPT="$SCRIPT_DIR/train.py" ;;
    skrl)      TRAIN_SCRIPT="$SCRIPT_DIR/train.py" ;;
    *)         echo "Unknown framework: $FRAMEWORK"; exit 1 ;;
esac

if [[ ! -f "$TRAIN_SCRIPT" ]]; then
    echo "Training script not found: $TRAIN_SCRIPT"
    exit 1
fi

echo "=== Ant Locomotion Training ==="
echo "  Framework:      $FRAMEWORK"
echo "  Task:           $TASK"
echo "  num_envs:       $NUM_ENVS"
echo "  max_iterations: $MAX_ITERATIONS"
echo "  Mode:           $([ -n "$HEADLESS" ] && echo 'headless' || echo 'GUI')"
echo ""

python "$TRAIN_SCRIPT" \
    --task "$TASK" \
    --num_envs "$NUM_ENVS" \
    --max_iterations "$MAX_ITERATIONS" \
    $HEADLESS \
    $EXTRA_ARGS
