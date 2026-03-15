#!/usr/bin/env bash
set -euo pipefail

bash lab_03_perception/scripts/validate_structure.sh
python -m unittest discover -s lab_03_perception/tests -p 'test_*.py'
bash lab_03_perception/scripts/run_lab.sh

echo "All Lab 3 phase checks completed."
