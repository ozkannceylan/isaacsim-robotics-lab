#!/usr/bin/env bash
set -euo pipefail

python3 -m lab_04_domain_rand.main \
  --config lab_04_domain_rand/configs/local.yaml \
  --eval-config-dir lab_04_domain_rand/eval/eval_configs \
  --output-dir outputs/lab_04
