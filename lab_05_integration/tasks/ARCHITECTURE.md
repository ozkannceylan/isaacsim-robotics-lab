# Lab 05 Integration — Architecture

## Module Map
- `src/models.py`: typed config, thresholds, subsystem results, and integration context models.
- `src/config_loader.py`: parse and validate integration JSON config.
- `src/integration_setup.py`: resolve manifest/config assets and construct typed integration context.
- `src/integration_pipeline.py`: orchestrate Labs 1–3 and normalize subsystem metrics.
- `src/evaluation.py`: compute deterministic scorecards and overall mission assessment.
- `src/logging_utils.py`: write integration summary JSON and subsystem scoreboard CSV.
- `src/main.py`: CLI entrypoint.

## Data Flow
1. Load Lab 5 config from `configs/`.
2. Resolve the integration manifest and dependent Lab 1/2/3 config files.
3. Run Lab 1 foundations for runtime metrics.
4. Run Lab 2 navigation for path execution metrics.
5. Run Lab 3 perception for sensing/feature metrics.
6. Evaluate integrated mission health against thresholds.
7. Write summary JSON and optional subsystem scoreboard CSV to `data/`.

## Key Interfaces
- Config loader returns typed `Lab5Config`.
- Setup returns typed `IntegrationContext` with all resolved file paths.
- Integration pipeline returns `SubsystemResult` entries plus aggregated rollups.
- Evaluation computes pass/fail per subsystem and overall mission score.
- Logging utilities persist machine-readable and spreadsheet-friendly artifacts.

## Expected Files
- `configs/default.json`, `configs/dev.json`
- `models/integration_manifest.json`
- `data/run_summary.json`, optional `data/subsystem_scoreboard.csv`
- `tasks/PLAN.md`, `tasks/ARCHITECTURE.md`, `tasks/TODO.md`, `tasks/LESSONS.md`
