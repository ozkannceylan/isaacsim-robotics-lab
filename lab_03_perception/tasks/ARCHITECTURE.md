# Lab 03 Perception — Architecture

## Module Map
- `src/models.py`: typed configs/context for sensor and feature pipeline.
- `src/config_loader.py`: parse and validate JSON config.
- `src/perception_setup.py`: resolve model assets and initialize context.
- `src/sensor_sim.py`: deterministic synthetic sensor frame generation.
- `src/feature_extractor.py`: compute lightweight frame features.
- `src/logging_utils.py`: write summary and frame-feature CSV artifacts.
- `src/main.py`: CLI entrypoint.

## Data Flow
1. Load config from `configs/`.
2. Build perception context using model/sensor settings.
3. Generate synthetic frames deterministically.
4. Extract features per frame and aggregate metrics.
5. Write summary JSON and optional per-frame CSV.

## Key Interfaces
- Config loader returns typed `Lab3Config`.
- Setup returns typed `PerceptionContext`.
- Sensor sim returns list of `FrameSample`.
- Feature extractor returns summary dict + per-frame rows.
- Logging utilities persist artifacts.

## Expected Files
- `configs/default.json`, `configs/dev.json`
- `models/camera.json` placeholder sensor model
- `data/run_summary.json`, optional `data/frame_features.csv`
