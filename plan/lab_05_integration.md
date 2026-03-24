# Lab 05 — Integration Brief

## Objective
Integrate the foundation, navigation, and perception scaffolds into a deterministic end-to-end evaluation pipeline with reproducible scoring and artifact generation.

## Required Deliverables
- Integration-specific config and manifest/model placeholders.
- Modules for config validation, integration setup, subsystem orchestration, evaluation, and artifact logging.
- Run and validation scripts.
- Unit and pipeline tests.
- Planning artifacts in `tasks/` following the repository workflow.

## Exit Criteria
- `scripts/run_phase_checks.sh` passes.
- A default run executes the Lab 1, Lab 2, and Lab 3 scaffolds through the Lab 5 integration pipeline.
- Integration summary JSON and subsystem scoreboard CSV are produced deterministically for a fixed seed/config.
