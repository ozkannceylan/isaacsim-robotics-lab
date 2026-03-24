#!/usr/bin/env bash
set -euo pipefail

python3 -m lab_05_integration.src.main   --config lab_05_integration/configs/default.json   --output lab_05_integration/data/run_summary.json   --scoreboard-output lab_05_integration/data/subsystem_scoreboard.csv   --save-scoreboard
