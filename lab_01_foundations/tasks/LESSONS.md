# Lessons Learned

## Context
Lab 1 completion executed in phases after plan/architecture approval.

## Step Log
1. Completed Phase 1 code scaffold (`src/`, configs, models, scripts, tests, docs).
2. Completed Phase 2 hardening (typed models, stricter config checks, seeded loop metrics, trajectory export).
3. Completed Phase 3 verification (pipeline test + one-command check script).
4. Completed Phase 4 documentation refresh and retrospective update.

## What Worked
- Typed dataclasses reduced ambiguity between config parsing and runtime setup.
- Seeded loop behavior made output deterministic and test-friendly.
- `run_phase_checks.sh` simplifies local validation and future CI wiring.

## What Didn't Work
- Canonical brief files are still absent from this repo snapshot.
- Placeholder model assets are sufficient for scaffold tests but not for real simulation quality checks.

## Open Questions
- Should output schema include additional metrics (latency, control error, episode score)?
- What canonical asset set should replace `robot.usd` and `environment.usd` placeholders?

## Follow-up Actions
- Replace placeholder models with official Lab 1 assets when available.
- Align config schema and module boundaries with canonical lab brief once provided.
