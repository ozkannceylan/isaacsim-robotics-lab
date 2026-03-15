#!/usr/bin/env bash
set -euo pipefail

required=(
  "lab_02_navigation/src/main.py"
  "lab_02_navigation/src/models.py"
  "lab_02_navigation/src/config_loader.py"
  "lab_02_navigation/src/navigation_setup.py"
  "lab_02_navigation/src/planner.py"
  "lab_02_navigation/src/logging_utils.py"
  "lab_02_navigation/configs/default.json"
  "lab_02_navigation/configs/dev.json"
  "lab_02_navigation/models/map.json"
  "lab_02_navigation/tasks/PLAN.md"
  "lab_02_navigation/tasks/ARCHITECTURE.md"
  "lab_02_navigation/tasks/TODO.md"
  "lab_02_navigation/tasks/LESSONS.md"
)

for p in "${required[@]}"; do
  [[ -f "$p" ]] || { echo "Missing required file: $p"; exit 1; }
done

echo "Lab 2 structure validation passed."
