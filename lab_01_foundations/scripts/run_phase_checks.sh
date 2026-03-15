#!/usr/bin/env bash
set -euo pipefail

bash lab_01_foundations/scripts/validate_structure.sh
python3 -m unittest discover -s lab_01_foundations/tests -p 'test_*.py'
python3 -m lab_01_foundations.src.main \
  --mock-runtime \
  --config lab_01_foundations/configs/mock.yaml \
  --output-dir lab_01_foundations/data/runs/mock_validation

echo "Lab 01 structure, tests, and mock artifact checks completed."
