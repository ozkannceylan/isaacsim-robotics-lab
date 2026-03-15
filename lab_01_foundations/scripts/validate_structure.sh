#!/usr/bin/env bash
set -euo pipefail

required=(
  "lab_01_foundations/foundations_standalone.py"
  "lab_01_foundations/config/scene_cfg.py"
  "lab_01_foundations/config/sim_cfg.py"
  "lab_01_foundations/src/main.py"
  "lab_01_foundations/src/config_loader.py"
  "lab_01_foundations/src/control.py"
  "lab_01_foundations/src/artifact_writers.py"
  "lab_01_foundations/src/mock_runtime.py"
  "lab_01_foundations/src/isaaclab_runtime.py"
  "lab_01_foundations/src/models.py"
  "lab_01_foundations/configs/local.yaml"
  "lab_01_foundations/configs/mock.yaml"
  "lab_01_foundations/tasks/PLAN.md"
  "lab_01_foundations/tasks/ARCHITECTURE.md"
  "lab_01_foundations/tasks/TODO.md"
  "lab_01_foundations/tasks/LESSONS.md"
)

for p in "${required[@]}"; do
  [[ -f "$p" ]] || { echo "Missing required file: $p"; exit 1; }
done

echo "Structure validation passed."
