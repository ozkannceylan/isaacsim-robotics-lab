#!/usr/bin/env bash
set -euo pipefail

bash lab_06_operations/scripts/validate_structure.sh
python3 -m unittest discover -s lab_06_operations/tests -p 'test_*.py'
bash lab_06_operations/scripts/run_lab.sh

echo "All Lab 6 phase checks completed."
