# Lab 07 Finalization

## Overview
Lab 7 produces the final project release-readiness report by combining Lab 6 operations results with a repository audit.

## Run

```bash
bash lab_07_finalization/scripts/run_lab.sh
```

## Run all checks

```bash
bash lab_07_finalization/scripts/run_phase_checks.sh
```

## Run tests only

```bash
python3 -m unittest discover -s lab_07_finalization/tests -p 'test_*.py'
```

## Outputs
- `lab_07_finalization/data/run_summary.json`
- `lab_07_finalization/data/repo_audit.csv`
