#!/usr/bin/env bash
set -euo pipefail

python3 -m lab_02_navigation.src.main \
  --config lab_02_navigation/configs/default.json \
  --output lab_02_navigation/data/run_summary.json \
  --path-output lab_02_navigation/data/path.csv \
  --save-path
