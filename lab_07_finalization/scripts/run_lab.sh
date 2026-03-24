#!/usr/bin/env bash
set -euo pipefail

python3 -m lab_07_finalization.src.main   --config lab_07_finalization/configs/default.json   --output lab_07_finalization/data/run_summary.json   --audit-output lab_07_finalization/data/repo_audit.csv   --save-audit
