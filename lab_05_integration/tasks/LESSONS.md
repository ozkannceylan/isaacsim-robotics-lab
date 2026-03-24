# Lessons Learned

## Issues Encountered
- The repository referenced `plan/lab_05_integration.md`, but the brief file was missing before this lab was started.
- Integration currently relies on scaffold-level outputs from Labs 1–3 rather than a full Isaac Sim deployment.

## Decisions Made
- Added a canonical `plan/lab_05_integration.md` brief before implementation so planning artifacts resolve correctly.
- Reused Lab 1/2/3 runtime modules directly to create a genuine cross-lab integration pipeline.
- Scored subsystems with transparent deterministic thresholds so tests remain stable.

## Follow-up Actions
- Replace scaffold-level evaluation thresholds with official rubric values if provided.
- Expand integration to include Lab 4 manipulation/control once that lab exists.
- Add artifact comparisons against golden outputs if future requirements demand stricter regression checks.
