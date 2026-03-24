#!/usr/bin/env bash
set -euo pipefail

required=(
  "lab_07_finalization/src/main.py"
  "lab_07_finalization/src/models.py"
  "lab_07_finalization/src/config_loader.py"
  "lab_07_finalization/src/finalization_setup.py"
  "lab_07_finalization/src/repo_audit.py"
  "lab_07_finalization/src/release_report.py"
  "lab_07_finalization/src/logging_utils.py"
  "lab_07_finalization/configs/default.json"
  "lab_07_finalization/configs/dev.json"
  "lab_07_finalization/models/release_manifest.json"
  "lab_07_finalization/tasks/PLAN.md"
  "lab_07_finalization/tasks/ARCHITECTURE.md"
  "lab_07_finalization/tasks/TODO.md"
  "lab_07_finalization/tasks/LESSONS.md"
  "plan/lab_07_finalization.md"
)

for p in "${required[@]}"; do
  [[ -f "$p" ]] || { echo "Missing required file: $p"; exit 1; }
done

echo "Lab 7 structure validation passed."
