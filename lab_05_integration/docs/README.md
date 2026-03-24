# Lab 05 Integration

## Overview
Lab 5 composes Labs 1–3 into a deterministic integration and evaluation pipeline.

## Run

```bash
bash lab_05_integration/scripts/run_lab.sh
```

## Run all checks

```bash
bash lab_05_integration/scripts/run_phase_checks.sh
```

## Run tests only

```bash
python -m unittest discover -s lab_05_integration/tests -p 'test_*.py'
```

## Outputs
- `lab_05_integration/data/run_summary.json`
- `lab_05_integration/data/subsystem_scoreboard.csv`
