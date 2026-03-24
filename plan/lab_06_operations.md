# Lab 06 — Operations Brief

## Objective
Package Lab 5 integration results into an operations-oriented deployment readiness report with deterministic health checks and artifact generation.

## Required Deliverables
- Operations config and manifest placeholders.
- Modules for config validation, operations setup, deployment-readiness evaluation, and artifact logging.
- Run and validation scripts.
- Unit and pipeline tests.
- Planning artifacts in `tasks/` following the repository workflow.

## Exit Criteria
- `scripts/run_phase_checks.sh` passes.
- A default run executes the Lab 5 integration pipeline through the Lab 6 operations workflow.
- Operations summary JSON and deployment checklist CSV are produced deterministically for a fixed seed/config.
