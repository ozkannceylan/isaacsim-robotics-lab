#!/usr/bin/env bash
# =============================================================================
# benchmark_num_envs.sh - Benchmark throughput across different num_envs
#
# Trains CartPole for a fixed number of iterations with varying num_envs
# and records steps/sec for each. Results are saved to a CSV file.
#
# Usage:
#   bash benchmark_num_envs.sh                      # default sweep
#   bash benchmark_num_envs.sh --iterations 100     # fewer iterations per run
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_DIR="$(dirname "$SCRIPT_DIR")"
RESULTS_FILE="$LAB_DIR/src/benchmark_results.csv"
ITERATIONS=100
TASK="Isaac-Cartpole-v0"
FRAMEWORK="rl_games"
ISAACLAB_DIR="${ISAACLAB_DIR:-$HOME/IsaacLab}"

# Parse args
while [[ $# -gt 0 ]]; do
    case "$1" in
        --iterations)   ITERATIONS="$2"; shift 2 ;;
        --task)         TASK="$2"; shift 2 ;;
        --framework)    FRAMEWORK="$2"; shift 2 ;;
        *)              shift ;;
    esac
done

TRAIN_SCRIPT="$ISAACLAB_DIR/source/standalone/workflows/${FRAMEWORK}/train.py"

if [[ ! -f "$TRAIN_SCRIPT" ]]; then
    echo "Training script not found: $TRAIN_SCRIPT"
    exit 1
fi

# num_envs values to test
ENV_COUNTS=(64 256 1024 2048 4096 8192)

echo "=== num_envs Throughput Benchmark ==="
echo "  Task:       $TASK"
echo "  Framework:  $FRAMEWORK"
echo "  Iterations: $ITERATIONS per run"
echo "  Sweep:      ${ENV_COUNTS[*]}"
echo ""

# CSV header
echo "num_envs,wall_time_sec,iterations,task,framework" > "$RESULTS_FILE"

for N in "${ENV_COUNTS[@]}"; do
    echo "--- Running num_envs=$N ---"
    START_TIME=$(date +%s.%N)

    # Run training, capture output
    python "$TRAIN_SCRIPT" \
        --task "$TASK" \
        --num_envs "$N" \
        --max_iterations "$ITERATIONS" \
        --headless \
        2>&1 | tail -5

    END_TIME=$(date +%s.%N)
    ELAPSED=$(echo "$END_TIME - $START_TIME" | bc)

    echo "  num_envs=$N  wall_time=${ELAPSED}s"
    echo "$N,$ELAPSED,$ITERATIONS,$TASK,$FRAMEWORK" >> "$RESULTS_FILE"
    echo ""
done

echo "=== Benchmark Complete ==="
echo "Results saved to: $RESULTS_FILE"
echo ""
cat "$RESULTS_FILE"
