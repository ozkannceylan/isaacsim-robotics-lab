#!/usr/bin/env bash
set -euo pipefail

python3 -m lab_06_operations.src.main   --config lab_06_operations/configs/default.json   --output lab_06_operations/data/run_summary.json   --checklist-output lab_06_operations/data/deployment_checklist.csv   --save-checklist
