# Lab 1: TODO

## Current Focus

Phase 1 - Architecture study and documentation

## Blockers

- Lab 0 must be complete (working Isaac Sim + Isaac Lab on Vast.ai)

---

## Phase 1: Architecture Study and Documentation
- [ ] Study InteractiveScene, manager-based env, direct env
- [ ] Document the 4 managers (Observation, Action, Reward, Termination)
- [ ] Understand USD scene composition and asset loading
- [ ] Study num_envs GPU parallelism and tensor batching
- [ ] Write docs/isaac_lab_architecture.md
- [ ] Create architecture concept diagram

## Phase 2: CartPole Training and num_envs Benchmark
- [ ] Train CartPole with RL Games (default, 2048 envs, headless)
- [ ] Verify training converges
- [ ] Run num_envs benchmark: [64, 256, 1024, 2048, 4096, 8192]
- [ ] Measure steps/sec for each num_envs
- [ ] Generate throughput scaling chart
- [ ] Save TensorBoard logs and training curves
- [ ] Compare wall-clock with MuJoCo CartPole

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
- [ ] Write docs/isaac_lab_architecture.md
- [ ] Write docs/benchmark_results.md
- [ ] Write Turkish documentation (docs-turkish/)
- [ ] Collect all media artifacts
- [ ] Update LESSONS.md
- [ ] Git push all results
