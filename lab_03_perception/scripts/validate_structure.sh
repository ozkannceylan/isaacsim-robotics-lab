#!/usr/bin/env bash
set -euo pipefail

required=(
  "lab_03_perception/src/main.py"
  "lab_03_perception/src/models.py"
  "lab_03_perception/src/config_loader.py"
  "lab_03_perception/src/perception_setup.py"
  "lab_03_perception/src/sensor_sim.py"
  "lab_03_perception/src/feature_extractor.py"
  "lab_03_perception/src/logging_utils.py"
  "lab_03_perception/configs/default.json"
  "lab_03_perception/configs/dev.json"
  "lab_03_perception/models/camera.json"
  "lab_03_perception/tasks/PLAN.md"
  "lab_03_perception/tasks/ARCHITECTURE.md"
  "lab_03_perception/tasks/TODO.md"
  "lab_03_perception/tasks/LESSONS.md"
)

for p in "${required[@]}"; do
  [[ -f "$p" ]] || { echo "Missing required file: $p"; exit 1; }
done

echo "Lab 3 structure validation passed."
