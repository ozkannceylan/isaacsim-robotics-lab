#!/usr/bin/env bash
set -euo pipefail

required=(
  "lab_05_integration/src/main.py"
  "lab_05_integration/src/models.py"
  "lab_05_integration/src/config_loader.py"
  "lab_05_integration/src/integration_setup.py"
  "lab_05_integration/src/integration_pipeline.py"
  "lab_05_integration/src/evaluation.py"
  "lab_05_integration/src/logging_utils.py"
  "lab_05_integration/configs/default.json"
  "lab_05_integration/configs/dev.json"
  "lab_05_integration/models/integration_manifest.json"
  "lab_05_integration/tasks/PLAN.md"
  "lab_05_integration/tasks/ARCHITECTURE.md"
  "lab_05_integration/tasks/TODO.md"
  "lab_05_integration/tasks/LESSONS.md"
  "plan/lab_05_integration.md"
)

for p in "${required[@]}"; do
  [[ -f "$p" ]] || { echo "Missing required file: $p"; exit 1; }
done

echo "Lab 5 structure validation passed."
