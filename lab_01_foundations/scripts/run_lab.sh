#!/usr/bin/env bash
set -euo pipefail

if ! command -v isaaclab >/dev/null 2>&1; then
  echo "isaaclab command not found. Activate the Isaac Lab environment before running Lab 01."
  exit 1
fi

isaaclab -p lab_01_foundations/foundations_standalone.py \
  --config lab_01_foundations/configs/local.yaml \
  --headless \
  --enable_cameras \
  "$@"
