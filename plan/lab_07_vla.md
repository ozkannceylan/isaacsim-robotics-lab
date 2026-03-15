# Lab 07: VLA Integration

## Objectives

- Close the loop: natural language → perception → action on a humanoid
- Generate synthetic training data using Isaac Sim Replicator
- Train or fine-tune a Vision-Language-Action model
- Deploy end-to-end: "Pick up the red cup" → G1 executes the task
- Connect to the humanoid_vla project as validation/comparison

## Prerequisites

- Lab 06 complete (whole-body loco-manipulation policy)
- Understanding of VLA architectures (RT-2, Octo, ACT)
- Experience with the humanoid_vla MuJoCo project
- Lambda Labs A100 for training (40+ GB VRAM for vision model + sim)

## Capstone Demo

End-to-end pipeline:
1. User types: "Pick up the red cup and place it on the shelf"
2. Vision model identifies the red cup in the scene
3. Language model generates a task plan (approach, grasp, navigate, place)
4. Policy executes each sub-task on G1 in Isaac Sim
5. Success evaluated automatically via object pose checking

## Theory

### VLA Architecture Options

**Option A: Modular Pipeline (recommended for this lab)**
```
Language Command → Task Planner (LLM) → Sub-task sequence
                                            ↓
Camera Image → Object Detector → Object pose
                                            ↓
                              Low-level Policy (Lab 06) ← target pose
```

**Option B: End-to-End VLA (stretch goal)**
```
Language Command + Camera Image → VLA Model → Action tokens → Joint commands
```

This lab implements Option A first (modular, debuggable), then attempts Option B using the humanoid_vla ACT model architecture.

### Synthetic Data Pipeline
- Isaac Sim Replicator: programmatic scene generation with annotations
- Generate: RGB images + segmentation masks + bounding boxes + object poses
- Randomize: object colors, positions, lighting, camera angles, backgrounds
- Use for training object detection / VLA model

### Connection to humanoid_vla Project
- The existing MuJoCo humanoid_vla project trained a 15.6M ACT model
- Here we validate: does the same architecture work in Isaac Sim?
- Key difference: Isaac Sim provides richer synthetic data (photorealistic rendering)
- Goal: demonstrate that Isaac Sim synthetic data improves VLA performance

## Architecture

```
lab_07_vla/
├── __init__.py
├── vla_pipeline/
│   ├── __init__.py
│   ├── task_planner.py                # LLM-based task decomposition
│   │   ├── parse_command()            # NL → structured task
│   │   └── plan_subtasks()            # Task → sequence of (action, target)
│   ├── perception/
│   │   ├── object_detector.py         # Detect + localize objects
│   │   └── scene_understanding.py     # Object-pose-from-camera pipeline
│   ├── controller/
│   │   ├── high_level_controller.py   # State machine: plan → policy calls
│   │   └── policy_loader.py           # Load Lab 05/06 policies
│   └── vla_env_cfg.py                 # Isaac Lab env with camera + objects
│       ├── VLASceneCfg                # G1 + table + multiple objects + camera
│       ├── ObservationsCfg            # Proprioception + camera image
│       └── CommandsCfg                # Language command injection
├── synthetic_data/
│   ├── replicator_config.py           # Isaac Replicator scene randomization
│   ├── generate_dataset.py            # Run data generation pipeline
│   └── data_format.py                 # Dataset format (HDF5 or RLDS)
├── training/
│   ├── train_detector.py              # Object detection model training
│   └── train_vla.py                   # End-to-end VLA training (stretch)
├── eval/
│   ├── eval_pipeline.py               # End-to-end evaluation
│   └── benchmark_configs/
│       ├── single_object.yaml
│       ├── multi_object.yaml
│       └── novel_object.yaml          # Zero-shot generalization test
└── agents/
    └── configs.py
```

## Implementation Notes for Claude Code

### Phase 1: Rich Scene Setup
- Scene: G1 at origin, table at (1.5, 0), 3-5 objects on table
- Objects: cup (red, blue), bowl, can — varying colors and sizes
- Camera: mounted on G1 head (egocentric) + fixed overhead (third-person)
- Lighting: dome light + point lights (for visual diversity)
- All objects as `RigidObject` with contact physics

### Phase 2: Task Planner (Modular Path)
- Input: natural language string (e.g., "pick up the red cup")
- LLM call (Claude API or local model) to extract:
  - Target object: "red cup"
  - Action type: "pick_up"
  - Target location: None (implicit)
- Output: sequence of sub-tasks:
  1. `walk_to(table_position)`
  2. `reach(red_cup_position)`
  3. `grasp(red_cup)`
  4. `lift(red_cup, height=0.3)`
- Each sub-task maps to a Lab 06 policy call with specific target

### Phase 3: Perception Pipeline
- Camera sensor outputs RGB tensor (640x480)
- Object detection: fine-tuned YOLOv8-nano or similar lightweight detector
- Trained on synthetic data from Isaac Replicator
- Output: bounding boxes + class labels
- Pose estimation: use depth + known object models for 6D pose
- Isaac Sim provides ground-truth segmentation for training data

### Phase 4: Synthetic Data Generation
- Isaac Replicator pipeline:
  - 10K images with randomized scenes
  - Objects: random positions on table, random colors, random lighting
  - Annotations: bounding box, segmentation mask, 6D pose
  - Format: COCO format for detection, custom HDF5 for VLA
- Domain randomization: textures, distractors, camera noise
- Generate in headless mode on Lambda Labs

### Phase 5: Integration Controller
- State machine orchestrating the full pipeline:
```
IDLE → PLANNING → NAVIGATING → REACHING → GRASPING → LIFTING → PLACING → DONE
```
- Each state calls appropriate policy with appropriate observations
- Transitions based on success criteria (distance thresholds, contact detection)
- Fallback: if sub-task fails, retry with perturbed target

### Phase 6: End-to-End VLA (Stretch Goal)
- Architecture: same ACT model from humanoid_vla (15.6M params)
- Input: RGB image (224x224) + language embedding (CLIP or similar)
- Output: action chunk (sequence of joint positions)
- Training data: demonstration trajectories from Phase 5 modular pipeline
- Compare: modular pipeline success rate vs end-to-end VLA success rate

### Training Config (Lambda Labs)
- Synthetic data generation: A10G, headless, ~2 hours for 10K images
- Object detector training: A10G, ~1 hour
- VLA training (if attempted): A100, ~4-8 hours
- Full pipeline evaluation: A10G, 100 episodes

### Critical Constraints
- **A100 REQUIRED** for VLA training (vision model + sim GPU sharing)
- Camera rendering adds significant VRAM — reduce envs to 64-128
- RGB observation at full resolution is expensive — downsample to 224x224 for model
- LLM task planner can be called offline (not in sim loop) — no latency issue
- Synthetic data must be diverse enough to generalize — minimum 5K unique scenes
- Connect results back to humanoid_vla project README for portfolio coherence

## Success Criteria

| Metric | Target |
|--------|--------|
| Synthetic data: 10K annotated images generated | Pass |
| Object detection: mAP > 0.7 on validation set | Pass |
| Modular pipeline: single object pick success > 50% | Pass |
| Modular pipeline: multi-object pick correct object > 40% | Pass |
| Language understanding: correct object identified > 80% | Pass |
| End-to-end demo video produced | Pass |
| VLA training (stretch): action prediction MSE competitive with humanoid_vla | Stretch |

## References

- [Isaac Sim Replicator](https://docs.isaacsim.omniverse.nvidia.com/latest/replicator_tutorials/index.html)
- [Isaac Lab — Imitation Learning](https://isaac-sim.github.io/IsaacLab/main/source/overview/environments.html)
- [Brohan et al. — RT-2: Vision-Language-Action Models (2023)](https://arxiv.org/abs/2307.15818)
- [Octo — Open-Source Generalist Robot Policy (2024)](https://octo-models.github.io/)
- [humanoid_vla Project](https://github.com/ozkannceylan/humanoid_vla)
