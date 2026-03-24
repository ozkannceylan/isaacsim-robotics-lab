# Lab 04 Domain Randomization — TODO

## Status Legend
- [x] Done
- [ ] Pending

## Phase 0 — Planning
- [x] Read `CLAUDE.md`, `plan/MASTER_PLAN.md`, and `plan/lab_04_domain_rand.md` before coding.
- [x] Create the Lab 04 package structure around robust grasp, evaluation, and agent config modules.

## Phase 1 — Core Implementation
- [x] Add typed YAML config loading for the Lab 04 training and randomization settings.
- [x] Implement deterministic event sampling for mass, friction, damping, stiffness, object type, size, and perturbation.
- [x] Implement observation noise injection and deterministic episode scoring.
- [x] Implement a vanilla baseline and ADR-enabled DR training loop.
- [x] Add fixed evaluation configs for nominal, heavy, slippery, and noisy robustness checks.
- [x] Generate summary, CSV, and SVG comparison artifacts.

## Phase 2 — Verification
- [x] Add and run tests for config validation, randomization determinism, ADR widening, and end-to-end evaluation.
- [x] Run the one-command phase check script successfully.

## Phase 3 — Handoff
- [x] Update project status docs after Lab 04 verification passes.
- [x] Record Lab 04 limitations and next steps.
