# Lab 01 Foundations — Architecture

> Fallback context: source brief files were not present in repository (`plan/lab_01_foundations.md`, `MASTER_PLAN.md`). This architecture establishes a practical baseline for Lab 1.

## 1) Module Map

- `lab_01_foundations/src/`
  - Purpose: core python modules for Lab 1 logic.
  - Implemented modules:
    - `models.py` — typed dataclasses for config and simulation context.
    - `main.py` — top-level entrypoint.
    - `config_loader.py` — config parsing/validation.
    - `simulation_setup.py` — simulation bootstrap and asset loading.
    - `task_loop.py` — deterministic per-step control/update loop.
    - `logging_utils.py` — summary and trajectory artifact writers.

- `lab_01_foundations/configs/`
  - Purpose: runtime configuration files (e.g., yaml/json) for environment and parameters.

- `lab_01_foundations/models/`
  - Purpose: robot/environment model assets or references (URDF/USD/etc.).

- `lab_01_foundations/data/`
  - Purpose: generated run data, cached artifacts, or sample inputs.

- `lab_01_foundations/scripts/`
  - Purpose: helper scripts for launching, formatting, and validation.

- `lab_01_foundations/tests/`
  - Purpose: unit/integration tests for baseline modules.

- `lab_01_foundations/docs/`
  - Purpose: lab usage notes and onboarding docs.

- `lab_01_foundations/tasks/`
  - Purpose: planning artifacts (`PLAN.md`, `ARCHITECTURE.md`, `TODO.md`, `LESSONS.md`).

## 2) Data Flow

1. User/runner invokes entrypoint (`src/main.py`) with config path.
2. `config_loader` reads and validates config schema.
3. `simulation_setup` initializes scene, robot assets, and optional sensors from `models/` references.
4. `task_loop` executes control/simulation steps and emits metrics/logs.
5. Outputs are written to `data/` and summarized by `logging_utils`.

## 3) Key Interfaces

- **Config interface**
  - Input: path to config file under `configs/`.
  - Output: validated in-memory config object/dict.
  - Errors: schema violations, missing model references.

- **Simulation setup interface**
  - Input: validated config + model paths.
  - Output: initialized simulation context/handles.

- **Task loop interface**
  - Input: sim context + task parameters.
  - Output: run status, performance metrics, optional trajectory data.

- **Logging/metrics interface**
  - Input: structured events and scalar metrics.
  - Output: human-readable logs + machine-readable summary artifact.

## 4) Model and File Expectations

- Model files expected under `models/`:
  - Robot model (e.g., `robot.urdf` or `robot.usd`).
  - Environment model (e.g., floor/obstacle world asset).

- Config files expected under `configs/`:
  - `default.yaml` (base runtime parameters).
  - `dev.yaml` (local overrides).

- Output files expected under `data/`:
  - `run_summary.json` (metrics, duration, status).
  - Optional per-step logs/trajectory artifacts.

## 5) Non-Functional Baseline

- Deterministic startup path via explicit config.
- Clear separation between config, setup, runtime loop, and logging.
- Testable interfaces with minimal cross-module coupling.
