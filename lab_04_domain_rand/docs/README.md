# Lab 04 Domain Randomization

This lab implements a deterministic scaffold for the `plan/lab_04_domain_rand.md` brief: domain randomization, ADR, and robustness evaluation for a simulated grasp policy.

## Run

```bash
bash lab_04_domain_rand/scripts/run_lab.sh
```

## Run All Checks

```bash
bash lab_04_domain_rand/scripts/run_phase_checks.sh
```

## Outputs

- `outputs/lab_04/summary.json`
- `outputs/lab_04/curriculum_history.csv`
- `outputs/lab_04/evaluation_results.csv`
- `outputs/lab_04/robustness_comparison.svg`

## Notes

- The implementation is deterministic and local-testable.
- The structure mirrors the EventManager/ADR plan even though this workspace does not include a live Isaac Lab grasp environment.
