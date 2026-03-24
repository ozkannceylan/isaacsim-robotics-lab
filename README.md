# Isaac Sim Robotics Lab

This checkout contains a deterministic, locally runnable scaffold for the implemented labs, plus several advanced Isaac Lab / humanoid planning briefs that are not yet implemented in code.

## Implemented Status
- ✅ `lab_01_foundations`: deterministic runtime/config/testing foundation.
- ✅ `lab_02_navigation`: deterministic waypoint planning and path artifact export.
- ✅ `lab_03_perception`: deterministic sensor simulation and feature extraction.
- ✅ `lab_04_domain_rand`: deterministic domain-randomization and robustness-evaluation scaffold for the advanced grasp brief.
- ✅ `lab_05_integration`: cross-lab mission integration and subsystem scoring.
- ✅ `lab_06_operations`: deployment-readiness and operational checklist generation.
- ✅ `lab_07_finalization`: repo audit and final release-readiness reporting.

## Plan-Only Briefs
The following briefs exist in `plan/` but do not have corresponding implementation folders in this checkout:
- `plan/lab_02_rl_env.md`
- `plan/lab_03_arm_control.md`
- `plan/lab_04_manipulation.md`
- `plan/lab_05_locomotion.md`
- `plan/lab_06_loco_manip.md`
- `plan/lab_07_vla.md`

## Local Prerequisites
- `python3` 3.12+.
- `pip install -r requirements.txt`
- No Isaac Sim, ROS, or robotics firmware is required for the implemented deterministic scaffold in this checkout.

## Planning Briefs
All planning briefs are stored in `plan/`:
- `plan/MASTER_PLAN.md`
- `plan/lab_01_foundations.md`
- `plan/lab_02_navigation.md`
- `plan/lab_02_rl_env.md`
- `plan/lab_03_arm_control.md`
- `plan/lab_03_perception.md`
- `plan/lab_04_domain_rand.md`
- `plan/lab_04_manipulation.md`
- `plan/lab_05_integration.md`
- `plan/lab_05_locomotion.md`
- `plan/lab_06_loco_manip.md`
- `plan/lab_06_operations.md`
- `plan/lab_07_finalization.md`
- `plan/lab_07_vla.md`

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
- The repository has an `origin` remote configured; push/pull still depend on local SSH credentials and network access.
- Lab 7 provides the final local release-readiness report for the implemented labs in this checkout.
- Root documentation should be updated whenever additional planned labs gain real implementations.
