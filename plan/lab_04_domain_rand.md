# Lab 04: Domain Randomization & Sim2Real

## Objectives

- Implement systematic domain randomization for robust policy transfer
- Use Isaac Lab's EventManager for physics, visual, and dynamics randomization
- Train a grasp policy that generalizes across object shapes, masses, and friction
- Benchmark: policy trained WITH randomization vs WITHOUT on held-out test configs
- Understand the sim2real gap and strategies to bridge it

## Prerequisites

- Lab 03 complete (working grasp policy, Manager-Based workflow)
- Understanding of sim2real transfer challenges
- Domain randomization literature (Tobin et al. 2017, OpenAI Rubik's Cube)

## Capstone Demo

A grasp policy that:
1. Picks up cubes, cylinders, and spheres of varying size (3-8cm)
2. Succeeds under ±30% mass variation, ±50% friction variation
3. Handles observation noise injection (joint encoder noise, pose estimation noise)
4. Quantitative comparison: DR policy vs vanilla policy on 100 randomized test episodes

## Theory

### Domain Randomization Categories
- **Physics randomization** — mass, friction, restitution, joint damping, actuator gains
- **Visual randomization** — textures, lighting, camera pose (for future camera-based policies)
- **Dynamics randomization** — action delay, observation noise, external force perturbations
- **Geometric randomization** — object shape, size, initial position variation

### Isaac Lab EventManager
- Events triggered at: `startup`, `reset`, `interval`
- `startup` — one-time scene randomization (lighting, textures)
- `reset` — per-episode randomization (object pose, mass, friction)
- `interval` — periodic perturbation during episode (external forces, noise)

### Automatic Domain Randomization (ADR)
- Start with narrow randomization ranges
- Widen ranges as policy performance improves
- Prevents early training collapse from too-hard randomization

## Architecture

```
lab_04_domain_rand/
├── __init__.py
├── robust_grasp/
│   ├── __init__.py
│   ├── robust_grasp_env_cfg.py        # Extended grasp cfg with DR
│   │   ├── RobustGraspSceneCfg        # Scene with multiple object types
│   │   ├── EventsCfg                  # Randomization events
│   │   │   ├── physics_randomization  # Mass, friction, restitution
│   │   │   ├── dynamics_randomization # Action noise, obs noise, ext force
│   │   │   └── geometry_randomization # Object type, size, pose
│   │   ├── ObservationsCfg            # Same as Lab 03 + noise injection
│   │   ├── RewardsCfg                 # Same as Lab 03
│   │   ├── TerminationsCfg
│   │   └── CurriculumCfg             # ADR: widen ranges over training
│   └── mdp/
│       ├── events.py                  # Custom event terms
│       ├── observations.py            # Noisy observation wrappers
│       └── rewards.py
├── eval/
│   ├── eval_robustness.py             # Run 100 test episodes, log metrics
│   └── eval_configs/
│       ├── nominal.yaml               # Default physics
│       ├── heavy_objects.yaml          # 2x mass
│       ├── slippery.yaml              # 0.3 friction
│       └── noisy.yaml                 # High observation noise
└── agents/
    └── skrl_ppo_cfg.py
```

## Implementation Notes for Claude Code

### Phase 1: EventManager Setup
- Physics randomization (at `reset`):
  - Object mass: uniform(0.05, 0.3) kg
  - Object friction: uniform(0.4, 1.2)
  - Joint damping: scale factor uniform(0.8, 1.2)
  - Actuator stiffness: scale factor uniform(0.9, 1.1)
- Implementation via `EventTermCfg`:
```
events = EventsCfg(
    randomize_mass=EventTermCfg(
        func=mdp.randomize_rigid_body_mass,
        mode="reset",
        params={"mass_distribution_params": (0.05, 0.3), "operation": "abs"}
    ),
    ...
)
```

### Phase 2: Observation Noise
- Joint position noise: Gaussian σ=0.01 rad
- Joint velocity noise: Gaussian σ=0.05 rad/s
- Object pose noise: Gaussian σ=0.005 m (simulating vision-based estimation)
- Implementation: add noise AFTER computing clean observation, BEFORE returning to agent
- Noise levels configurable in env cfg

### Phase 3: Geometric Randomization
- Multiple object types: cube, cylinder, sphere (all from Isaac Lab primitives)
- Size range: 3-8 cm characteristic dimension
- At reset: randomly select object type AND size for each env
- Object spawning: use `RigidObjectCfg` with randomized spawn

### Phase 4: External Perturbation
- At `interval` (every 50 steps): apply random external force to object
- Force magnitude: uniform(0, 2) N, random direction
- Simulates bumps, air currents, imprecise robot motion

### Phase 5: ADR Curriculum
- Track grasp success rate over rolling window of 100 episodes
- When success > 80%: widen randomization ranges by 10%
- When success < 50%: narrow randomization ranges by 10%
- Log current DR ranges to TensorBoard

### Phase 6: Evaluation
- Evaluation script runs trained policy on fixed test configurations
- 100 episodes per config, report success rate + mean reward
- Compare: DR policy vs vanilla (Lab 03) policy on same test configs
- Generate comparison bar chart

### Critical Constraints
- VRAM WARNING: Multiple object types in scene increases memory
- If VRAM tight: use only cube + cylinder (skip sphere), reduce to 32 envs
- All randomization must be BATCHED (tensor ops, not per-env loops)
- EventManager terms use `env_ids` parameter — only randomize resetting envs
- Keep clean (non-noisy) observations available for critic (asymmetric actor-critic)

## Success Criteria

| Metric | Target |
|--------|--------|
| DR policy: grasp success > 70% on nominal config | Pass |
| DR policy: grasp success > 50% on heavy objects | Pass |
| DR policy: grasp success > 50% on slippery config | Pass |
| DR policy outperforms vanilla policy on all test configs | Pass |
| ADR curriculum widens ranges at least 2x during training | Pass |
| Trains on local RTX 4050 (32-64 envs, headless) | Pass |
| VRAM usage | < 6 GB |

## References

- [Isaac Lab — EventManager](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.managers.html)
- [Isaac Lab — Domain Randomization How-To](https://isaac-sim.github.io/IsaacLab/main/source/how-to/domain_randomization.html)
- [Tobin et al. — Domain Randomization for Transfer (2017)](https://arxiv.org/abs/1703.06907)
- [OpenAI — Solving Rubik's Cube with a Robot Hand (2019)](https://arxiv.org/abs/1910.07113)
