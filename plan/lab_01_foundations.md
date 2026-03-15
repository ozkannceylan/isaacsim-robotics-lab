# Lab 01: Isaac Sim Foundations

## Objectives

- Install Isaac Sim + Isaac Lab on Ubuntu 24 (local RTX 4050)
- Understand the USD scene graph, PhysX simulation loop, and asset pipeline
- Spawn a robot (UR5e), apply joint position commands, read joint states
- Render a camera sensor image (headless) and save to disk
- Run Isaac Lab's Cartpole example to verify full pipeline

## Prerequisites

- Ubuntu 24.04 with NVIDIA driver 535+ installed
- Conda (Miniforge recommended)
- NGC account + API key for container access
- Basic Python, basic robotics concepts (joint space, task space)

## Capstone Demo

A standalone Python script that:
1. Launches Isaac Sim headless
2. Spawns a UR5e on a table in a warehouse scene
3. Sends a joint-space sine trajectory to all 6 joints
4. Records 30 frames from a mounted camera
5. Saves joint state log as CSV + camera frames as PNG sequence

## Theory

### Isaac Sim Architecture
- **Omniverse Kit** — the application framework
- **USD (Universal Scene Description)** — scene graph format, everything is a prim
- **PhysX 5** — GPU-accelerated rigid body + articulation physics
- **Isaac Lab** — robot learning framework on top of Isaac Sim

### Key Concepts
- **SimulationContext** — controls physics stepping, render mode, device
- **AppLauncher** — configures headless/GUI, enables cameras
- **Articulation** — physics handle for a jointed robot (joints, links, DOFs)
- **RigidObject** — physics handle for a free-floating body
- **Spawners** — factory functions that create USD prims programmatically

### Asset Pipeline
- NVIDIA provides robot assets via Nucleus server or Isaac Lab built-ins
- UR5e available as `isaaclab.sim.schemas` USD asset
- Custom assets: import URDF/MJCF via Isaac Sim importers

## Architecture

```
lab_01_foundations/
├── __init__.py
├── foundations_standalone.py     # Standalone script (NOT an RL env)
│   ├── launch_sim()             # AppLauncher + SimulationContext setup
│   ├── build_scene()            # Ground plane + UR5e + table + camera
│   ├── run_trajectory()         # Sine wave joint commands, state logging
│   └── main()                   # Orchestrator
├── config/
│   ├── scene_cfg.py             # Scene configuration (assets, positions)
│   └── sim_cfg.py               # Simulation params (dt, substeps, device)
└── assets/                      # Any custom USD files (if needed)
```

This lab does NOT create an RL environment. It is a standalone script that exercises Isaac Sim APIs directly.

## Implementation Notes for Claude Code

### Phase 1: Environment Setup
- Create conda env with Python 3.11
- `pip install isaacsim[all,extscache] --extra-index-url https://pypi.nvidia.com`
- Clone Isaac Lab, `pip install -e .` from source
- Run compatibility checker: `omni.isaac.sim.compatibility_check.sh`
- Run hello world: `isaaclab -p source/standalone/tutorials/00_sim/create_empty.py --headless`

### Phase 2: Scene Building
- Use `sim_utils.GroundPlaneCfg` for ground
- Use `ArticulationCfg` pointing to UR5e USD from Isaac Lab assets
- Position UR5e at (0, 0, table_height)
- Add `CameraCfg` with 640x480 resolution, mounted at fixed world position

### Phase 3: Joint Control
- Access articulation via `Articulation` class
- Set joint position targets via `articulation.set_joint_position_target()`
- Log `articulation.data.joint_pos` and `articulation.data.joint_vel` per step
- Run for 300 steps at 60 Hz

### Phase 4: Camera Capture
- Enable camera via `AppLauncher(headless=True, enable_cameras=True)`
- Use `Camera` sensor class to get RGB data
- Save frames via `PIL` or `cv2`

### Key API Patterns
```
# These are the core patterns Claude Code needs to know:

# 1. App launch
app_launcher = AppLauncher(headless=True, enable_cameras=True)
simulation_app = app_launcher.app

# 2. Scene design via InteractiveScene
scene_cfg = InteractiveSceneCfg(...)
scene = InteractiveScene(scene_cfg)

# 3. Simulation loop
sim = SimulationContext(sim_params)
sim.reset()
while simulation_app.is_running():
    scene.write_data_to_sim()
    sim.step()
    scene.update(sim.get_physics_dt())

# 4. Always cleanup
simulation_app.close()
```

### Critical Constraints
- `--headless` flag is mandatory on local RTX 4050
- `enable_cameras=True` adds ~500MB VRAM — only enable when actually capturing
- First run downloads assets from NVIDIA servers (may take 10+ minutes)
- All Isaac Lab scripts use `isaaclab -p script.py` runner (not bare `python`)

## Success Criteria

| Metric | Target |
|--------|--------|
| Isaac Sim launches headless without errors | Pass |
| UR5e spawns and responds to joint commands | Pass |
| Joint state CSV has 300 rows, 6 joints each | Pass |
| Camera captures 30 PNG frames | Pass |
| Isaac Lab Cartpole example trains for 100 iterations | Pass |
| Total VRAM usage during run | < 5 GB |

## References

- [Isaac Lab Tutorials — Simulation](https://isaac-sim.github.io/IsaacLab/main/source/tutorials/index.html)
- [Isaac Lab Quickstart](https://isaac-sim.github.io/IsaacLab/main/source/setup/quickstart.html)
- [Isaac Sim Getting Started](https://docs.isaacsim.omniverse.nvidia.com/latest/introduction/quickstart_index.html)
- [Isaac Lab API — Articulation](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.assets.html)
