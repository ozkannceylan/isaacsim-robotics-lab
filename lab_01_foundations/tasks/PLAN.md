# Lab 01 Foundations — Implementation Plan

> Context: this plan aligns to the canonical brief at `plan/lab_01_foundations.md` and the process in `plan/MASTER_PLAN.md`.

## Goal
Implement the actual Lab 01 capstone as a standalone Isaac Lab script instead of a generic scaffold.

## Concrete Implementation Steps

1. **Replace the placeholder loop with a real standalone runner**
   - Use `isaaclab -p lab_01_foundations/foundations_standalone.py`.
   - Keep all Isaac Lab imports isolated so tests can still run without Isaac Lab installed.

2. **Model the lab config explicitly**
   - Add typed scene and runtime dataclasses.
   - Encode the UR5e, warehouse, table, camera, 300-step run, and 30-frame capture targets in YAML.

3. **Implement the capstone runtime**
   - Spawn the warehouse backdrop, static table, UR5e articulation, and RGB camera.
   - Drive the six arm joints with a sine trajectory at 60 Hz.
   - Log joint positions and velocities for every step.

4. **Persist the required artifacts**
   - Save `joint_states.csv`.
   - Save RGB frames as PNG sequence.
   - Save a summary JSON with counts and runtime metadata.

5. **Keep a fast validation path**
   - Provide a deterministic mock backend for unit tests and local validation.
   - Preserve the real run path as the default operational mode.
