#!/usr/bin/env bash
set -euo pipefail

bash lab_01_foundations/scripts/validate_structure.sh
python -m unittest discover -s lab_01_foundations/tests -p 'test_*.py'
bash lab_01_foundations/scripts/run_lab.sh

echo "All Lab 1 phase checks completed."
