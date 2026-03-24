# Lab 07 Finalization — Architecture

## Module Map
- `src/models.py`: typed config, thresholds, finalization context, and audit models.
- `src/config_loader.py`: parse and validate Lab 7 JSON config.
- `src/finalization_setup.py`: resolve release manifest and dependent Lab 6 config.
- `src/repo_audit.py`: audit required repo assets and lab directories.
- `src/release_report.py`: combine Lab 6 operations output with repo audit into a final release report.
- `src/logging_utils.py`: write final summary JSON and audit CSV artifacts.
- `src/main.py`: CLI entrypoint.

## Data Flow
1. Load Lab 7 config from `configs/`.
2. Resolve the release manifest and the dependent Lab 6 config.
3. Execute Lab 6 operations deterministically.
4. Audit repository-level release artifacts and required lab directories.
5. Build a final release report with readiness score, repo status, and audit findings.
6. Write summary JSON and optional audit CSV to `data/`.

## Key Interfaces
- Config loader returns typed `Lab7Config`.
- Setup returns typed `FinalizationContext`.
- Repo audit returns audit rows for required files and directories.
- Release report merges operations output with audit results into final status.
- Logging utilities persist machine-readable and spreadsheet-friendly outputs.

## Expected Files
- `configs/default.json`, `configs/dev.json`
- `models/release_manifest.json`
- `data/run_summary.json`, optional `data/repo_audit.csv`
- `tasks/PLAN.md`, `tasks/ARCHITECTURE.md`, `tasks/TODO.md`, `tasks/LESSONS.md`
