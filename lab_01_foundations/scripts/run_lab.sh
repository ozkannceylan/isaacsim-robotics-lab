#!/usr/bin/env bash
set -euo pipefail

python -m lab_01_foundations.src.main \
  --config lab_01_foundations/configs/default.json \
  --output lab_01_foundations/data/run_summary.json \
  --trajectory-output lab_01_foundations/data/trajectory.csv \
  --save-trajectory
