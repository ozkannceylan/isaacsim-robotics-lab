# Lab 01 Foundations — Architecture

> Context: architecture aligned to `plan/lab_01_foundations.md` and `plan/MASTER_PLAN.md`.

## 1) Module Map

- `lab_01_foundations/foundations_standalone.py`
  - Purpose: file entrypoint used by `isaaclab -p`.
  - Responsibility: add repo root to `sys.path` and hand off to the Python package entrypoint.

- `lab_01_foundations/config/`
  - `scene_cfg.py` — typed scene configuration for warehouse, UR5e, table, and camera.
  - `sim_cfg.py` — runtime and artifact output configuration.

- `lab_01_foundations/src/`
  - Purpose: core Lab 01 runtime logic.
  - Implemented modules:
    - `main.py` — compatibility module that forwards to the standalone runner.
    - `foundations_standalone.py` — CLI orchestration, backend selection, and artifact writing.
    - `config_loader.py` — YAML/JSON loading plus Lab 01 contract validation.
    - `control.py` — joint trajectory generation and frame capture schedule.
    - `isaaclab_runtime.py` — real Isaac Lab execution path.
    - `mock_runtime.py` — deterministic CI/local validation backend.
    - `artifact_writers.py` — CSV, PNG, and summary JSON writers.
    - `models.py` — typed run-result models.

- `lab_01_foundations/configs/`
  - Purpose: run profiles.
  - Files:
    - `local.yaml` — plan-aligned capstone profile (300 steps, 30 PNG frames, 640x480 RGB).
    - `mock.yaml` — reduced validation profile for tests and phase checks.

- `lab_01_foundations/models/`
  - Purpose: optional local USD asset storage if Nucleus references are replaced later.

- `lab_01_foundations/data/`
  - Purpose: generated run artifacts.

- `lab_01_foundations/scripts/`
  - Purpose: real run, structure validation, and mock verification.

- `lab_01_foundations/tests/`
  - Purpose: config, trajectory, and artifact-contract verification.

- `lab_01_foundations/docs/`
  - Purpose: Lab 01 runbook and plan-alignment notes.

- `lab_01_foundations/tasks/`
  - Purpose: task tracking and retrospective notes.

## 2) Data Flow

1. User invokes `isaaclab -p lab_01_foundations/foundations_standalone.py --config ... --headless --enable_cameras`.
2. `config_loader` parses YAML and validates the Lab 01 capstone contract.
3. `foundations_standalone.py` selects either the real Isaac Lab backend or the mock backend.
4. The selected runtime emits typed joint-state samples and camera frames.
5. `artifact_writers.py` persists `joint_states.csv`, PNG frames, and `run_summary.json`.

## 3) Key Interfaces

- **Config interface**
  - Input: path to `configs/local.yaml` or `configs/mock.yaml`.
  - Output: `Lab01Config`.
  - Errors: missing sections, non-headless runtime, bad joint definitions, bad frame/step counts.

- **Runtime interface**
  - Input: validated config + runtime mode.
  - Output: `LabRunResult`.
  - Real backend: launches Isaac Lab and records actual robot/camera outputs.
  - Mock backend: validates the same output contract without Isaac Lab.

- **Artifact interface**
  - Input: `LabRunResult`.
  - Output: summary JSON, joint-state CSV, PNG frame sequence.

## 4) Model and File Expectations

- Config files expected under `configs/`:
  - `local.yaml` — the real capstone profile.
  - `mock.yaml` — reduced validation profile.

- External USD assets expected from Isaac Nucleus by default:
  - `${ISAAC_NUCLEUS_DIR}/Environments/Simple_Warehouse/warehouse.usd`
  - `${ISAAC_NUCLEUS_DIR}/Robots/UniversalRobots/ur5e/ur5e.usd`

- Output files expected under `data/`:
  - `run_summary.json`
  - `joint_states.csv`
  - `frames/frame_XXX.png`

## 5) Non-Functional Baseline

- Headless-only on the local profile.
- Real Isaac Lab path and fast mock-validation path share the same artifact contract.
- Pure-stdlib PNG writing keeps tests independent of Pillow/OpenCV.
