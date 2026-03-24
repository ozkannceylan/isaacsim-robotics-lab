# Lab 01 Foundations

This lab now includes planning + full scaffold implementation phases:

- **Phase 0**: Plan/architecture/task artifacts.
- **Phase 1**: Source scaffold, configs, model placeholders.
- **Phase 2**: Typed config/runtime models and deterministic loop metrics.
- **Phase 3**: Validation scripts and test coverage.
- **Phase 4**: Execution docs and lessons log.

## Run (default config)

```bash
bash lab_01_foundations/scripts/run_lab.sh
```

## Validate structure + tests + run (all phase checks)

```bash
bash lab_01_foundations/scripts/run_phase_checks.sh
```

## Run tests only

```bash
python -m unittest discover -s lab_01_foundations/tests -p 'test_*.py'
```

## Direct CLI usage

```bash
python -m lab_01_foundations.src.main \
  --config lab_01_foundations/configs/dev.json \
  --output lab_01_foundations/data/run_summary.json \
  --trajectory-output lab_01_foundations/data/trajectory.csv \
  --save-trajectory
```

## Notes

- JSON config support is built-in.
- YAML config support is optional and requires `pyyaml`.
