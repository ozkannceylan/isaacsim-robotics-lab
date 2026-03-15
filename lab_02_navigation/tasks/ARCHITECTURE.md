# Lab 02 Navigation — Architecture

## Module Map
- `src/models.py`: typed dataclasses for navigation config/context/state.
- `src/config_loader.py`: config parsing + validation.
- `src/navigation_setup.py`: map/world setup and sanity checks.
- `src/planner.py`: deterministic waypoint planner.
- `src/logging_utils.py`: write summary/path artifacts.
- `src/main.py`: CLI entrypoint.

## Data Flow
1. Load config from `configs/`.
2. Build navigation context from map/model references.
3. Run planner to generate waypoints/path metrics.
4. Write summary JSON and optional path CSV to `data/`.

## Key Interfaces
- Config interface returns typed `Lab2Config`.
- Setup interface returns `NavigationContext`.
- Planner interface returns summary dict with status/path_length/waypoints.
- Logging interface writes machine-readable artifacts.

## Expected Files
- `configs/default.json`, `configs/dev.json`
- `models/map.json` placeholder map
- `data/run_summary.json`, optional `data/path.csv`
