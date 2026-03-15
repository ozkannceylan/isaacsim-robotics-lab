# Lessons Learned

## Context
Lab 3 was completed using the same workflow as prior labs: PLAN → ARCHITECTURE → TODO → IMPLEMENT.

## What Worked
- Reusing the prior lab scaffold pattern accelerated delivery.
- Deterministic frame generation made tests stable and reproducible.
- Splitting sensor simulation and feature extraction improved modularity.

## What Didn't Work
- Placeholder camera model is enough for scaffold validation only.
- Current synthetic sensor model is simplistic and not physics-based.

## Open Questions
- Should Lab 3 include depth/rgb channels with separate feature heads?
- Should feature extraction include thresholded event detection metrics?

## Follow-up Actions
- Replace placeholder camera model with canonical Lab 3 assets.
- Extend sensor simulator and feature set once official brief is available.
