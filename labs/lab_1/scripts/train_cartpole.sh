#!/usr/bin/env bash
# =============================================================================
# train_cartpole.sh - Train CartPole with Isaac Lab
#
# Usage:
#   bash train_cartpole.sh                          # defaults: rl_games, 2048 envs, 300 iters
#   bash train_cartpole.sh --num_envs 4096          # custom env count
#   bash train_cartpole.sh --framework skrl         # use SKRL instead
#   bash train_cartpole.sh --gui                    # with GUI (slower)
#   bash train_cartpole.sh --max_iterations 500     # more training
# =============================================================================
set -euo pipefail

# Defaults
FRAMEWORK="rl_games"
NUM_ENVS=2048
MAX_ITERATIONS=300
HEADLESS="--headless"
EXTRA_ARGS=""
TASK="Isaac-Cartpole-v0"

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

# Resolve training script
case "$FRAMEWORK" in
    rl_games)
        TRAIN_SCRIPT="$SCRIPT_DIR/train.py"
        ;;
    skrl)
        TRAIN_SCRIPT="$SCRIPT_DIR/train.py"
        ;;
    *)
        echo "Unknown framework: $FRAMEWORK (supported: rl_games, skrl)"
        exit 1
        ;;
esac

if [[ ! -f "$TRAIN_SCRIPT" ]]; then
    echo "Training script not found: $TRAIN_SCRIPT"
    echo "Is ISAACLAB_DIR set correctly? Current: $ISAACLAB_DIR"
    exit 1
fi

echo "=== CartPole Training ==="
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
