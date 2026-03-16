# Isaac Sim Robotics Lab

This repository tracks staged lab development.

## Current Status
- ✅ **Lab 1 (`lab_01_foundations`) is finished**: planning, architecture, implementation phases, runtime scaffold, scripts, tests, and docs are complete.
- ✅ **Lab 2 (`lab_02_navigation`) is finished**: planning artifacts, navigation scaffold implementation, scripts, tests, and docs are complete.
- ✅ **Lab 3 (`lab_03_perception`) is finished**: planning artifacts, perception scaffold implementation, scripts, tests, and docs are complete.
- ✅ **Lab 4 (`lab_04_domain_rand`) is finished**: domain-randomization scaffold, ADR loop, evaluation configs, reporting artifacts, scripts, tests, and docs are complete.

## Labs Overview
- `lab_01_foundations/`: completed baseline runtime/configuration/testing foundation.
- `lab_02_navigation/`: completed navigation scaffold with waypoint planning, artifact outputs, scripts, tests, and documentation.
- `lab_03_perception/`: completed perception scaffold with deterministic sensor simulation, feature extraction, artifact outputs, scripts, tests, and documentation.
- `lab_04_domain_rand/`: completed deterministic domain-randomization scaffold with ADR, robustness evaluation, report artifacts, scripts, tests, and documentation.

## Next Labs
Planned upcoming labs (subject to official brief alignment):
- Lab 5: system integration + evaluation pipeline.

## Completion Rule
After finishing each lab, update this root `README.md` status section so progress is always current.

## Planning Briefs
Canonical planning briefs are stored in `plan/`:
- `plan/MASTER_PLAN.md`
- `plan/lab_01_foundations.md`
- `plan/lab_02_navigation.md`
- `plan/lab_03_perception.md`
- `plan/lab_04_domain_rand.md`


## Quick Commands
### Lab 1
```bash
bash lab_01_foundations/scripts/run_phase_checks.sh
```

### Lab 2
```bash
bash lab_02_navigation/scripts/run_phase_checks.sh
```

### Lab 3
```bash
bash lab_03_perception/scripts/run_phase_checks.sh
```

### Lab 4
```bash
bash lab_04_domain_rand/scripts/run_phase_checks.sh
```
