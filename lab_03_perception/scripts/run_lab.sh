#!/usr/bin/env bash
set -euo pipefail

python -m lab_03_perception.src.main \
  --config lab_03_perception/configs/default.json \
  --output lab_03_perception/data/run_summary.json \
  --features-output lab_03_perception/data/frame_features.csv \
  --save-features
