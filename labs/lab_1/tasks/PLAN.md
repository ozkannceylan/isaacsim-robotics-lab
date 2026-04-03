# Lab 1: Isaac Lab RL Fundamentals - Implementation Plan

## Overview

Master Isaac Lab's core abstractions by training RL policies on built-in environments. Understand GPU-parallelized simulation, the manager-based workflow, and how it differs from MuJoCo/Gymnasium.

## Deliverables

1. Trained CartPole policy with training curves (TensorBoard)
2. Trained Ant locomotion policy with evaluation video
3. Comparison document: Isaac Lab vs MuJoCo workflow
4. num_envs throughput benchmark data
5. RL framework comparison (RL Games vs SKRL)

---

## Phase 1: Architecture Study and Documentation

**Goal:** Understand Isaac Lab's core abstractions before writing code.

**Steps:**
1. Study Isaac Lab source: `InteractiveScene`, manager-based env, direct env
2. Document the 4 managers: Observation, Action, Reward, Termination
3. Understand USD scene composition and how assets are loaded
4. Study `num_envs` GPU parallelism — how tensor batching replaces Python loops
5. Write architecture doc (`docs/isaac_lab_architecture.md`)
6. Create concept diagram for `media/`

**Gate:** Architecture doc written. Can explain manager-based workflow from memory.

---

## Phase 2: CartPole Training and num_envs Benchmark

**Goal:** Train CartPole and measure GPU parallelism scaling.

**Steps:**
1. Run CartPole with RL Games, default config, headless, 2048 envs
2. Verify training converges (reward plateau)
3. Run benchmark: num_envs in [64, 256, 1024, 2048, 4096, 8192]
4. Measure steps/sec and wall-clock time for each
5. Plot throughput scaling curve
6. Save TensorBoard logs and training curves to media/
7. Compare wall-clock with MuJoCo CartPole data (from mujoco-robotics-lab)

**Gate:** CartPole converges in <5 min. Throughput chart generated.

---

## Phase 3: Ant Locomotion

**Goal:** Train a more complex environment and understand reward engineering.

**Steps:**
1. Run Ant with RL Games, default config, headless, 2048 envs
2. Train to convergence (may need 500-1000 iterations)
3. Record evaluation video using Isaac Lab video wrapper
4. Inspect reward components in TensorBoard: forward velocity, energy penalty, alive bonus
5. Experiment with reward weight modifications:
   - Increase energy penalty (2x) — expect slower but more efficient gait
   - Remove alive bonus — observe effect on episode length
   - Increase forward velocity weight — expect faster but less stable
6. Document reward experiment results with before/after metrics

**Gate:** Ant walks stably. Video recorded. Reward experiments documented.

---

## Phase 4: RL Framework Comparison

**Goal:** Test RL Games vs SKRL on the same task.

**Steps:**
1. Train CartPole with SKRL (PPO), same num_envs as RL Games baseline
2. Train Ant with SKRL, compare convergence speed
3. Measure: steps/sec, time-to-convergence, final reward
4. Document API differences (config style, callback hooks, logging)
5. Write comparison table with recommendation per use case

**Gate:** Both frameworks tested. Comparison table complete.

---

## Phase 5: Headless vs GUI and Logging

**Goal:** Understand training modes and experiment management.

**Steps:**
1. Train CartPole with GUI (256 envs) — measure FPS
2. Train CartPole headless (256 envs) — measure FPS
3. Document FPS difference
4. Practice checkpoint save/load cycle
5. Set up TensorBoard and capture training curve screenshots
6. Record evaluation video from trained checkpoint

**Gate:** FPS comparison documented. Checkpoint save/load works.

---

## Phase 6: Documentation and Portfolio

**Goal:** Produce portfolio-ready artifacts.

**Steps:**
1. Write English documentation: `docs/isaac_lab_architecture.md`, `docs/benchmark_results.md`
2. Write Turkish documentation in `docs-turkish/`
3. Collect all media: training curves, throughput chart, Ant video, architecture diagram
4. Update TODO.md — mark all phases complete
5. Update LESSONS.md with accumulated insights
6. Git push all results

**Gate:** All docs and media in place. Git pushed.
