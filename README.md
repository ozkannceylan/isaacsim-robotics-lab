# Isaac Sim Robotics Lab

This repository is the finalized scaffolded robotics-lab project for the currently available briefs in this checkout. It packages deterministic planning, implementation, testing, and release-readiness workflows across the implemented labs.

## Final Project Status
- ✅ Lab 1 (`lab_01_foundations`) complete for scaffold scope.
- ✅ Lab 2 (`lab_02_navigation`) complete for scaffold scope.
- ✅ Lab 3 (`lab_03_perception`) complete for scaffold scope.
- ⏳ Lab 4 (`plan/lab_04_manipulation.md`) has a canonical brief placeholder but no implementation folder yet.
- ✅ Lab 5 (`lab_05_integration`) complete for scaffold scope.
- ✅ Lab 6 (`lab_06_operations`) complete for scaffold scope.
- ✅ Lab 7 (`lab_07_finalization`) complete for scaffold scope.

## Implemented Labs Overview
- `lab_01_foundations/`: deterministic runtime/config/testing foundation.
- `lab_02_navigation/`: deterministic waypoint planning and path artifact export.
- `lab_03_perception/`: deterministic sensor simulation and feature extraction.
- `lab_05_integration/`: cross-lab mission integration and subsystem scoring.
- `lab_06_operations/`: deployment-readiness and operational checklist generation.
- `lab_07_finalization/`: repo audit and final release-readiness reporting.

## Planning Briefs
Canonical lab briefs are stored in `plan/`:
- `plan/MASTER_PLAN.md`
- `plan/lab_01_foundations.md`
- `plan/lab_02_navigation.md`
- `plan/lab_03_perception.md`
- `plan/lab_04_manipulation.md`
- `plan/lab_05_integration.md`
- `plan/lab_06_operations.md`
- `plan/lab_07_finalization.md`

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

### Lab 5
```bash
bash lab_05_integration/scripts/run_phase_checks.sh
```

### Lab 6
```bash
bash lab_06_operations/scripts/run_phase_checks.sh
```

### Lab 7
```bash
bash lab_07_finalization/scripts/run_phase_checks.sh
```

## Finalization Notes
- The repository has no git remote configured in this environment, so “push” can only be finalized locally unless a remote is added later.
- Lab 7 provides the final local release-readiness report for the implemented labs.
- Root documentation should be updated whenever additional canonical lab briefs or implementations are added.
