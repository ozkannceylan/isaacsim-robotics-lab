#!/usr/bin/env bash
set -euo pipefail

bash lab_07_finalization/scripts/validate_structure.sh
python -m unittest discover -s lab_07_finalization/tests -p 'test_*.py'
bash lab_07_finalization/scripts/run_lab.sh

echo "All Lab 7 phase checks completed."
