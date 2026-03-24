# Lab 06 Operations — Architecture

## Module Map
- `src/models.py`: typed config, thresholds, operations context, and deployment checklist models.
- `src/config_loader.py`: parse and validate Lab 6 JSON config.
- `src/operations_setup.py`: resolve operations manifest and dependent Lab 5 config.
- `src/operations_pipeline.py`: run Lab 5 and normalize mission outputs into operations metrics.
- `src/report_builder.py`: compute deployment readiness, risk, and recommended actions.
- `src/logging_utils.py`: write summary JSON and deployment checklist CSV artifacts.
- `src/main.py`: CLI entrypoint.

## Data Flow
1. Load Lab 6 config from `configs/`.
2. Resolve the operations manifest and the dependent Lab 5 config.
3. Execute Lab 5 integration deterministically.
4. Translate mission metrics into operations/deployment readiness metrics.
5. Build a deployment report with readiness score, risk tier, and checklist rows.
6. Write summary JSON and optional deployment checklist CSV to `data/`.

## Key Interfaces
- Config loader returns typed `Lab6Config`.
- Setup returns typed `OperationsContext`.
- Operations pipeline returns mission summary + normalized operations metrics.
- Report builder computes readiness status and checklist rows.
- Logging utilities persist machine-readable and spreadsheet-friendly outputs.

## Expected Files
- `configs/default.json`, `configs/dev.json`
- `models/operations_manifest.json`
- `data/run_summary.json`, optional `data/deployment_checklist.csv`
- `tasks/PLAN.md`, `tasks/ARCHITECTURE.md`, `tasks/TODO.md`, `tasks/LESSONS.md`
