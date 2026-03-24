#!/usr/bin/env bash
set -euo pipefail

bash lab_04_domain_rand/scripts/validate_structure.sh
python3 -m unittest discover -s lab_04_domain_rand/tests -p 'test_*.py'
python3 -m lab_04_domain_rand.main \
  --config lab_04_domain_rand/configs/local.yaml \
  --eval-config-dir lab_04_domain_rand/eval/eval_configs \
  --output-dir outputs/lab_04_phase_check

echo "All Lab 4 phase checks completed."
