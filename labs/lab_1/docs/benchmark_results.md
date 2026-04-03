# Lab 1: Benchmark Results

## num_envs Throughput Scaling

*This document will be filled with actual results after running `benchmark_num_envs.sh` on the Vast.ai instance.*

### Setup
- **GPU:** (fill in after running)
- **Task:** Isaac-Cartpole-v0
- **Framework:** RL Games
- **Iterations per run:** 100

### Results Table

| num_envs | Wall Time (s) | Total Steps | Steps/sec |
|----------|--------------|-------------|-----------|
| 64 | | | |
| 256 | | | |
| 1024 | | | |
| 2048 | | | |
| 4096 | | | |
| 8192 | | | |

### Throughput Chart

![Throughput Scaling](../media/throughput_scaling.png)

### Observations

- (fill after experiment)
- Expected: near-linear scaling up to GPU saturation, then diminishing returns
- Key insight: GPU parallelism gives N-fold speedup, but with diminishing returns

---

## Headless vs GUI FPS

| Mode | num_envs | FPS |
|------|----------|-----|
| Headless | 256 | |
| GUI | 256 | |
| Speedup | | |

---

## Ant Reward Experiments

### Baseline (default config)
- Final reward:
- Episode length:

### Experiment: 2x energy penalty
- Final reward:
- Episode length:
- Observation:

### Experiment: no alive bonus
- Final reward:
- Episode length:
- Observation:

### Experiment: 2x forward velocity weight
- Final reward:
- Episode length:
- Observation:

![Reward Comparison](../media/reward_comparison.png)
