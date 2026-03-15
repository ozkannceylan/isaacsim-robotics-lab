#!/usr/bin/env bash
set -euo pipefail

bash lab_02_navigation/scripts/validate_structure.sh
python -m unittest discover -s lab_02_navigation/tests -p 'test_*.py'
bash lab_02_navigation/scripts/run_lab.sh

echo "All Lab 2 phase checks completed."
