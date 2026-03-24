# Lab 06 Operations

## Overview
Lab 6 packages Lab 5 integration results into an operations-oriented deployment readiness report.

## Run

```bash
bash lab_06_operations/scripts/run_lab.sh
```

## Run all checks

```bash
bash lab_06_operations/scripts/run_phase_checks.sh
```

## Run tests only

```bash
python -m unittest discover -s lab_06_operations/tests -p 'test_*.py'
```

## Outputs
- `lab_06_operations/data/run_summary.json`
- `lab_06_operations/data/deployment_checklist.csv`
