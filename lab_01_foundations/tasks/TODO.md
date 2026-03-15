# Lab 01 Foundations — TODO

## Status Legend
- [x] Done
- [ ] Pending

## Review Against `plan/lab_01_foundations.md`
- [x] Confirm the prior Lab 01 scaffold did not launch Isaac Sim, spawn UR5e, capture camera frames, or use `isaaclab -p`.
- [x] Replace placeholder runtime logic with a real Isaac Lab standalone entrypoint.

## Runtime Implementation
- [x] Add typed config models for runtime, scene, and output artifacts.
- [x] Encode the plan-aligned local profile: headless, 300 steps, 30 PNG frames, 640x480 RGB.
- [x] Implement the UR5e sine-wave joint trajectory logic.
- [x] Implement real Isaac Lab scene assembly for warehouse, table, UR5e, and camera.
- [x] Write joint states to CSV and captured RGB frames to PNG.

## Verification Path
- [x] Add a deterministic mock backend that preserves the artifact contract.
- [x] Update the scripts to use `python3` for local verification where Isaac Lab is unavailable.
- [x] Add unit tests for config validation, capture scheduling, and mock artifact generation.
- [x] Update the phase-check script to run structure checks, tests, and the mock backend.

## Remaining
- [ ] Execute the real Isaac Lab run in a configured environment and confirm the UR5e asset behaves as expected.
