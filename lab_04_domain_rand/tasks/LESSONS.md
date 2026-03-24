# Lessons Learned

## Context
Lab 04 is the first new lab created directly from the detailed Isaac Lab brief rather than from the earlier lightweight scaffold briefs.

## Expected Constraints
- The repo does not currently contain the live Lab 03 grasp environment the brief assumes.
- The local workspace does not provide Isaac Lab itself, so the implementation must stay locally testable.

## Follow-up
- Replace the deterministic grasp-scoring scaffold with a real Isaac Lab manager-based environment once Lab 03 exists in that form.
- Swap the synthetic ADR logic for real EventManager terms when Isaac Lab training is available.

## Verification Snapshot
- `scripts/run_phase_checks.sh` passed.
- DR max range scale reached `2.8x`, satisfying the ADR-expansion target.
- DR success rate exceeded the target thresholds on the nominal, heavy, slippery, and noisy evaluation configs in the deterministic scaffold.
