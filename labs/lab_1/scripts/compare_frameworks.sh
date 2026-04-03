#!/usr/bin/env bash
# =============================================================================
# compare_frameworks.sh - Compare RL Games vs SKRL on the same task
#
# Trains the same environment with both frameworks and records metrics.
#
# Usage:
#   bash compare_frameworks.sh                       # CartPole default
#   bash compare_frameworks.sh --task Isaac-Ant-v0   # Ant comparison
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_DIR="$(dirname "$SCRIPT_DIR")"
RESULTS_FILE="$LAB_DIR/src/framework_comparison.csv"
TASK="Isaac-Cartpole-v0"
NUM_ENVS=2048
ITERATIONS=300
ISAACLAB_DIR="${ISAACLAB_DIR:-$HOME/IsaacLab}"

# Parse args
while [[ $# -gt 0 ]]; do
    case "$1" in
        --task)         TASK="$2"; shift 2 ;;
        --num_envs)     NUM_ENVS="$2"; shift 2 ;;
        --iterations)   ITERATIONS="$2"; shift 2 ;;
        *)              shift ;;
    esac
done

FRAMEWORKS=("rl_games" "skrl")

echo "=== Framework Comparison ==="
echo "  Task:       $TASK"
echo "  num_envs:   $NUM_ENVS"
echo "  Iterations: $ITERATIONS"
echo "  Frameworks: ${FRAMEWORKS[*]}"
echo ""

# CSV header
echo "framework,task,num_envs,iterations,wall_time_sec" > "$RESULTS_FILE"

for FW in "${FRAMEWORKS[@]}"; do
    TRAIN_SCRIPT="$ISAACLAB_DIR/source/standalone/workflows/${FW}/train.py"

    if [[ ! -f "$TRAIN_SCRIPT" ]]; then
        echo "  SKIP: $FW (script not found: $TRAIN_SCRIPT)"
        continue
    fi

    echo "--- Training with $FW ---"
    START_TIME=$(date +%s.%N)

    python "$TRAIN_SCRIPT" \
        --task "$TASK" \
        --num_envs "$NUM_ENVS" \
        --max_iterations "$ITERATIONS" \
        --headless \
        2>&1 | tail -5

    END_TIME=$(date +%s.%N)
    ELAPSED=$(echo "$END_TIME - $START_TIME" | bc)

    echo "  $FW: wall_time=${ELAPSED}s"
    echo "$FW,$TASK,$NUM_ENVS,$ITERATIONS,$ELAPSED" >> "$RESULTS_FILE"
    echo ""
done

echo "=== Comparison Complete ==="
echo "Results saved to: $RESULTS_FILE"
echo ""
cat "$RESULTS_FILE"
