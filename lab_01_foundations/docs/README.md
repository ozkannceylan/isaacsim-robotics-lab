# Lab 01 Foundations

Lab 01 is now aligned to `plan/lab_01_foundations.md` instead of the earlier placeholder scaffold.

## What this lab delivers

- A standalone Isaac Lab script launched with `isaaclab -p`
- A warehouse scene with a support table, UR5e spawn, and RGB camera
- A 300-step, 60 Hz sine-wave joint command across the six UR5e arm joints
- Joint-state CSV logging plus a 30-frame PNG capture sequence
- A mock runtime path for CI and local verification when Isaac Lab is not installed

## Real capstone run

```bash
bash lab_01_foundations/scripts/run_lab.sh
```

This invokes:

```bash
isaaclab -p lab_01_foundations/foundations_standalone.py \
  --config lab_01_foundations/configs/local.yaml \
  --headless \
  --enable_cameras
```

## Verification without Isaac Lab

```bash
bash lab_01_foundations/scripts/run_phase_checks.sh
```

This validates structure, runs the unit tests, and executes the deterministic mock backend using `configs/mock.yaml`.

## Direct mock CLI

```bash
python3 -m lab_01_foundations.src.main \
  --mock-runtime \
  --config lab_01_foundations/configs/mock.yaml \
  --output-dir /tmp/lab_01_mock_run
```

## Outputs

- `run_summary.json`
- `joint_states.csv`
- `frames/frame_000.png` ... `frames/frame_029.png` for the real local profile

## Asset note

The default local config points at Isaac Nucleus assets using `${ISAAC_NUCLEUS_DIR}`:

- `Environments/Simple_Warehouse/warehouse.usd`
- `Robots/UniversalRobots/ur5e/ur5e.usd`

Run this lab from the Isaac Lab environment so those assets resolve correctly.
