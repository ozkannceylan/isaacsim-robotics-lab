# Lab 1: TODO

## Current Focus

Phase 3 - Ant Locomotion training

## Blockers

None

---

## Phase 1: Architecture Study and Documentation
- [x] Study InteractiveScene, manager-based env, direct env
- [x] Document the 4 managers (Observation, Action, Reward, Termination)
- [x] Understand USD scene composition and asset loading
- [x] Study num_envs GPU parallelism and tensor batching
- [x] Write docs/isaac_lab_architecture.md
- [ ] Create architecture concept diagram (deferred to Phase 6)

## Phase 2: CartPole Training and num_envs Benchmark
- [x] Train CartPole with RL Games (2048 envs, 300 iterations, headless) -- converged, best reward 4.93
- [x] Verify training converges -- yes, reward ~4.9/5.0
- [x] Run num_envs benchmark: [512, 1024, 2048, 4096, 8192] (min 512 for rl_games config)
- [x] Measure steps/sec for each num_envs -- saved to labs/lab_1/src/benchmark_results.csv
- [x] Fix HEADLESS env var conflict in all training scripts
- [ ] Generate throughput scaling chart (deferred to Phase 6 docs)
- [x] Save TensorBoard logs and training curves -- logs/rl_games/cartpole/2026-04-07_11-23-54/
- [ ] Compare wall-clock with MuJoCo CartPole (deferred to Phase 6 docs)

## Phase 3: Ant Locomotion
- [ ] Train Ant with RL Games (default, 2048 envs, headless)
- [ ] Train to convergence
- [ ] Record evaluation video
- [ ] Inspect reward components in TensorBoard
- [ ] Reward experiment: increase energy penalty (2x)
- [ ] Reward experiment: remove alive bonus
- [ ] Reward experiment: increase forward velocity weight
- [ ] Document reward experiment results

## Phase 4: RL Framework Comparison
- [ ] Train CartPole with SKRL (PPO)
- [ ] Train Ant with SKRL
- [ ] Measure: steps/sec, time-to-convergence, final reward
- [ ] Document API differences
- [ ] Write comparison table

## Phase 5: Headless vs GUI and Logging
- [ ] Train CartPole with GUI — measure FPS
- [ ] Train CartPole headless — measure FPS
- [ ] Document FPS difference
- [ ] Checkpoint save/load cycle
- [ ] TensorBoard training curve screenshots
- [ ] Record evaluation video from checkpoint

## Phase 6: Documentation and Portfolio
- [x] Write docs/isaac_lab_architecture.md
- [x] Write docs/benchmark_results.md (filled with Phase 2 data)
- [ ] Write Turkish documentation (docs-turkish/)
- [ ] Collect all media artifacts
- [ ] Update LESSONS.md
- [ ] Git push all results
