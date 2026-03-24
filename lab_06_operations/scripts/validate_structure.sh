#!/usr/bin/env bash
set -euo pipefail

required=(
  "lab_06_operations/src/main.py"
  "lab_06_operations/src/models.py"
  "lab_06_operations/src/config_loader.py"
  "lab_06_operations/src/operations_setup.py"
  "lab_06_operations/src/operations_pipeline.py"
  "lab_06_operations/src/report_builder.py"
  "lab_06_operations/src/logging_utils.py"
  "lab_06_operations/configs/default.json"
  "lab_06_operations/configs/dev.json"
  "lab_06_operations/models/operations_manifest.json"
  "lab_06_operations/tasks/PLAN.md"
  "lab_06_operations/tasks/ARCHITECTURE.md"
  "lab_06_operations/tasks/TODO.md"
  "lab_06_operations/tasks/LESSONS.md"
  "plan/lab_06_operations.md"
)

for p in "${required[@]}"; do
  [[ -f "$p" ]] || { echo "Missing required file: $p"; exit 1; }
done

echo "Lab 6 structure validation passed."
