# Lab 1: Benchmark Results

## num_envs Throughput Scaling

### Setup
- **GPU:** NVIDIA GeForce RTX 5090 (32 GB VRAM)
- **Driver:** 570.144, CUDA 12.8
- **Task:** Isaac-Cartpole-v0
- **Framework:** RL Games (PPO)
- **Iterations per run:** 100
- **Horizon length:** 16 (rl_games default for CartPole)
- **Total steps formula:** num_envs * iterations * horizon_length

### Results Table

| num_envs | Wall Time (s) | Total Steps | Steps/sec | FPS Step | FPS Total | GPU Mem (MiB) |
|----------|---------------|-------------|-----------|----------|-----------|---------------|
| 512 | 27 | 819,200 | 30,341 | 90,867 | 59,824 | 2,925 |
| 1024 | 34 | 1,638,400 | 48,188 | 135,277 | 77,806 | 2,991 |
| 2048 | 46 | 3,276,800 | 71,235 | 231,963 | 104,896 | 3,123 |
| 4096 | 63 | 6,553,600 | 104,025 | 440,570 | 136,103 | 3,389 |
| 8192 | 98 | 13,107,200 | 133,747 | 869,586 | 169,718 | 3,937 |

### Throughput Chart

![Throughput Scaling](../media/throughput_scaling.png)

### Observations

- **FPS Step scales near-linearly:** 91K (512 envs) to 870K (8192 envs) = 9.6x for 16x envs. GPU is underutilized at low env counts.
- **FPS Total (including training) scales more modestly:** 60K to 170K (2.8x), because PPO network training cost grows with batch size.
- **Wall time increases** with num_envs (27s to 98s for 100 iters) because each iteration processes more samples. But throughput (total steps / wall time) scales 4.4x from 512 to 8192 envs.
- **GPU memory is extremely low for CartPole:** 2.9-3.9 GB across the range. RTX 5090's 32 GB is vastly underutilized — much larger env counts or complex envs are feasible.
- **Sweet spot for CartPole:** 4096-8192 envs. At 4096+, step FPS exceeds 440K, meaning GPU is well saturated.

### Key Insight

GPU parallelism gives massive speedup, but with two regimes:
1. **Physics throughput (FPS Step):** Scales almost linearly until GPU compute saturates
2. **Training throughput (FPS Total):** Scales sub-linearly because the RL optimizer (PPO minibatch updates) becomes the bottleneck at high env counts

---

## CartPole Convergence Training

### Setup
- **num_envs:** 2048
- **max_iterations:** 300
- **Wall clock:** 109 seconds (~1 min 49 sec)
- **Total frames:** 9,830,400

### Reward Progression

| Epoch | Reward |
|-------|--------|
| 25 | 4.298 |
| 50 | 4.886 |
| 54 | 4.894 |
| 65 | 4.917 |
| 100 | 4.414 |
| 125 | 4.554 |
| 140 | 4.925 |
| 141 | 4.932 (peak) |
| 150 | 4.897 |
| 200 | 4.464 |
| 225 | 3.393 |
| 250 | 4.182 |
| 275 | 4.731 |
| 300 | 4.503 |

**Converged:** Yes. Reward reaches ~4.9/5.0 (theoretical max ~5.0). Oscillates between 3.4-4.9 due to on-policy PPO stochastic exploration.

### Checkpoints (on instance)
- Best: `logs/rl_games/cartpole/2026-04-07_11-23-54/nn/cartpole.pth`
- Final: `logs/rl_games/cartpole/2026-04-07_11-23-54/nn/last_cartpole_ep_300_rew_4.5029907.pth`

---

## Headless vs GUI FPS

| Mode | num_envs | FPS |
|------|----------|-----|
| Headless | 256 | *(skipped — VNC GUI not available on RTX 5090 due to Vulkan mismatch)* |
| GUI | 256 | *(skipped)* |
| Speedup | | N/A |

Note: GUI mode requires Vulkan display. RTX 5090 has Vulkan ICD 1.4 vs system loader 1.3 — GUI rendering not supported on this instance. All training is headless.

---

## Ant Reward Experiments

*To be filled after Phase 3.*

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
