#!/usr/bin/env bash
set -euo pipefail

bash lab_05_integration/scripts/validate_structure.sh
python3 -m unittest discover -s lab_05_integration/tests -p 'test_*.py'
bash lab_05_integration/scripts/run_lab.sh

echo "All Lab 5 phase checks completed."
