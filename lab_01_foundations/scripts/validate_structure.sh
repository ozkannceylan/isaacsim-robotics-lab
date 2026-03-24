#!/usr/bin/env bash
set -euo pipefail

required=(
  "lab_01_foundations/src/main.py"
  "lab_01_foundations/src/models.py"
  "lab_01_foundations/src/config_loader.py"
  "lab_01_foundations/src/simulation_setup.py"
  "lab_01_foundations/src/task_loop.py"
  "lab_01_foundations/src/logging_utils.py"
  "lab_01_foundations/configs/default.json"
  "lab_01_foundations/configs/dev.json"
  "lab_01_foundations/models/robot.usd"
  "lab_01_foundations/models/environment.usd"
  "lab_01_foundations/tasks/PLAN.md"
  "lab_01_foundations/tasks/ARCHITECTURE.md"
  "lab_01_foundations/tasks/TODO.md"
  "lab_01_foundations/tasks/LESSONS.md"
)

for p in "${required[@]}"; do
  [[ -f "$p" ]] || { echo "Missing required file: $p"; exit 1; }
done

echo "Structure validation passed."
