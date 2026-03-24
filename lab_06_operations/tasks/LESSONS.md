# Lessons Learned

## Issues Encountered
- Lab 6 had no canonical brief in `plan/`, so one had to be added before implementation.
- Operations reporting depends on scaffold-level outputs from Lab 5 rather than a live deployment environment.

## Decisions Made
- Added `plan/lab_06_operations.md` to keep planning artifacts canonical and traceable.
- Reused the Lab 5 integration pipeline directly so operations readiness is based on actual cross-lab mission results.
- Kept checklist scoring deterministic for stable tests and reproducible reports.

## Follow-up Actions
- Replace placeholder deployment checklist items with environment-specific requirements if they become available.
- Extend the operations pipeline to include artifact publication hooks once a remote destination is configured.
