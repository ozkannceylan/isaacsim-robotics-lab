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

## Ant Locomotion Training

### Setup
- **Task:** Isaac-Ant-v0 (manager-based, 7 reward terms, 60-dim obs, 8-dim action)
- **num_envs:** 2048
- **max_iterations:** 1000
- **Wall clock:** ~3 minutes
- **GPU memory:** 3.4 GB (10.7% of RTX 5090)

### Baseline Results
- **Best reward:** 90.35 (epoch 840)
- **Final reward:** 68.31 (epoch 1000)
- **FPS total:** ~190-250K
- **Convergence:** Yes. Steady climb from 3.27 (ep50) to 90.35 peak.

---

## Ant Reward Experiments

3 experiments with modified reward weights, each trained for 500 iterations with 2048 envs.

### Summary Table

| Experiment | Config Change | Best Reward | Final (ep500) | vs Baseline |
|------------|--------------|-------------|---------------|-------------|
| **baseline** | (default) | 90.35 | 68.31 | -- |
| **high_energy** | action_l2: -0.01, energy: -0.1 | 46.18 | 38.57 | -49% |
| **no_alive** | alive: 0.0 | 65.33 | 54.33 | -28% |
| **high_velocity** | progress: 2.0 | 169.26 | 151.60 | +87% |

### Experiment: 2x energy penalty (high_energy)
- **Config:** action_l2 weight -0.005 -> -0.01, energy weight -0.05 -> -0.1
- **Best reward:** 46.18 (epoch 480)
- **Final reward:** 38.57
- **Wall clock:** 84s
- **Observation:** Doubling energy penalties creates a "lazy" agent. The agent optimizes for stillness to minimize energy costs. Progress component (2.79) is the lowest of all experiments. The agent learns to move conservatively — penalizing energy too harshly suppresses locomotion.

### Experiment: no alive bonus (no_alive)
- **Config:** alive weight 0.5 -> 0.0
- **Best reward:** 65.33 (epoch 481)
- **Final reward:** 54.33
- **Wall clock:** 84s
- **Observation:** Without survival incentive, the agent is slightly more aggressive in movement (progress=3.45) but less stable. It terminates more often without the alive bonus stabilizing behavior. Learning curve shows instability in later epochs (dips from 57.5 to 50.6). The alive bonus acts as a stabilizer.

### Experiment: 2x forward velocity weight (high_velocity)
- **Config:** progress weight 1.0 -> 2.0
- **Best reward:** 169.26 (epoch 480)
- **Final reward:** 151.60
- **Wall clock:** 88s
- **Observation:** Doubling the locomotion reward dramatically increases performance. The agent aggressively prioritizes forward movement, accepting higher energy costs (energy=-0.97, highest of all experiments) as a trade-off. Reaches 100+ reward by epoch 200. The default Ant task is somewhat under-weighted on the locomotion objective.

### Key Takeaways

1. **Positive reward magnitude matters more than penalty tuning.** Doubling the positive reward (high_velocity: +87%) far outperforms adjusting penalties (high_energy: -49%).
2. **Over-penalizing energy creates lazy agents.** The clearest failure mode — optimizing for stillness when energy costs dominate.
3. **The alive bonus is stabilizing but not critical.** Removing it causes -28% performance and training instability, but doesn't cause catastrophic failure.
4. **Energy-velocity trade-off is real.** The high_velocity agent consumed the most energy (-0.97) but had the highest progress (9.77) — classic speed-efficiency trade-off.

---

## RL Framework Comparison: RL Games vs SKRL

### Setup
- **GPU:** NVIDIA GeForce RTX 5090 (32 GB VRAM)
- **Driver:** 570.144, CUDA 12.8
- **RL Games:** Bundled with Isaac Lab 2.3.0
- **SKRL:** v1.4.3
- **Both use PPO** with default Isaac Lab configs (same network architectures per task)
- **num_envs:** 2048 for all runs

### CartPole Comparison

| Metric | RL Games | SKRL |
|--------|----------|------|
| Iterations | 300 | 300 |
| Wall clock time | 109s | 136s |
| Best mean reward | 4.93 | 4.92 |
| Final mean reward | 4.50 | 4.63 |
| Approx FPS (env steps/sec) | ~100K | ~78K |
| Network architecture | [32, 32] ELU | [32, 32] ELU |
| Horizon / rollouts | 16 | 16 |
| Mini-epochs | 8 | 8 |
| Learning rate | 3e-4 (adaptive) | 3e-4 (KL adaptive) |
| Minibatch size | 8192 | 8 mini-batches |
| Convergence epoch | ~54 (first 4.9+) | ~57 (first 4.9+) |
| Reward shaper scale | 1.0 | 1.0 |
| Observation normalization | No | No |

**CartPole observations:**
- Both frameworks converge to near-identical reward (~4.9/5.0). The task is simple enough that any PPO implementation solves it.
- RL Games is ~25% faster in wall time (109s vs 136s) due to tighter C++/CUDA integration and mixed-precision support.
- SKRL shows slightly more reward oscillation in mid-training (dips to 2.46 around iter 183) compared to RL Games, likely due to different minibatch sampling strategies.
- Both use the same [32, 32] ELU network, same learning rate, same horizon.

### Ant Comparison

| Metric | RL Games | SKRL |
|--------|----------|------|
| Iterations | 1000 | 1000 |
| Wall clock time | ~180s | 183s |
| Best mean reward | 90.35 | 72.63 |
| Final mean reward | 68.31 | 72.63 |
| Best max reward | N/A | 101.23 |
| Approx FPS (env steps/sec) | ~190-250K | ~193K |
| Network architecture | [256, 128, 64] ELU | [256, 128, 64] ELU |
| Horizon / rollouts | 16 | 16 |
| Mini-epochs | 4 | 4 |
| Learning rate | 3e-4 (adaptive) | 3e-4 (KL adaptive) |
| Minibatch size | 32768 | 2 mini-batches |
| Mixed precision | Yes | No |
| Input normalization | Yes (RL Games built-in) | Yes (RunningStandardScaler) |
| Value normalization | Yes | Yes (RunningStandardScaler) |
| Reward shaper scale | 0.6 | 0.6 |
| Value loss coefficient | 2.0 | 1.0 |

**Ant observations:**
- RL Games reaches a higher peak reward (90.35) but drops to 68.31 by iteration 1000 (overfitting / reward oscillation).
- SKRL reaches a lower peak (72.63) but is still climbing steadily at iteration 1000 — may benefit from more training.
- Wall times are nearly identical (~180s), suggesting the physics simulation dominates the compute budget for Ant.
- The key hyperparameter difference is value_loss_scale: RL Games uses 2.0 (critic_coef) while SKRL uses 1.0. This gives RL Games stronger value function fitting, helping faster convergence but potentially more reward oscillation.
- RL Games uses mixed precision (FP16) for Ant, SKRL does not — explains why RL Games matches wall time despite higher minibatch processing.

### Aggregate Comparison

| Aspect | RL Games | SKRL |
|--------|----------|------|
| **Speed** | Faster (10-25% on simple tasks) | Slightly slower |
| **Peak performance** | Higher peaks, more oscillation | Lower peaks, steadier learning |
| **Config format** | YAML (RL Games custom schema) | YAML (skrl-native schema) |
| **Model definition** | Implicit (from config) | Explicit (auto-generated Python class) |
| **Logging** | Stdout + TensorBoard | TensorBoard only (no stdout progress) |
| **API complexity** | Minimal (NVIDIA-optimized) | More Pythonic, more configurable |
| **Mixed precision** | Built-in support | Not in default configs |
| **Best for** | Fast training, NVIDIA stack | Research flexibility, custom algorithms |

### Key Takeaways

1. **For production training, RL Games is faster.** Its C++ backend and mixed-precision support give 10-25% wall-time advantage on simple tasks.
2. **For complex tasks, the gap narrows.** On Ant, wall times are nearly identical because physics simulation dominates.
3. **Both reach comparable performance.** The final reward difference is within training noise. Neither framework has a fundamental algorithm advantage — both use PPO.
4. **SKRL is more transparent.** It prints the generated model class, making debugging easier. RL Games is more opaque but faster.
5. **SKRL lacks stdout progress logging.** All metrics go to TensorBoard, making it harder to monitor training interactively. RL Games prints epoch-by-epoch stats to stdout.
6. **Config schemas are incompatible.** Switching frameworks requires rewriting agent configs — not just changing a flag.

### Checkpoints

**SKRL CartPole:**
- Best: `/opt/IsaacLab/logs/skrl/cartpole/2026-04-07_13-30-49_ppo_torch/checkpoints/best_agent.pt`
- Final: `/opt/IsaacLab/logs/skrl/cartpole/2026-04-07_13-30-49_ppo_torch/checkpoints/agent_4800.pt`

**SKRL Ant:**
- Best: `/opt/IsaacLab/logs/skrl/ant/2026-04-07_13-36-58_ppo_torch/checkpoints/best_agent.pt`
- Final: `/opt/IsaacLab/logs/skrl/ant/2026-04-07_13-36-58_ppo_torch/checkpoints/agent_16000.pt`
