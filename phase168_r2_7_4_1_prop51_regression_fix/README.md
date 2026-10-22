# Phase 168 R2-7(4)-1 — Proposition 5.1 Regression Repair

This package changes **only** the previously installed R2-7(4) connector. It keeps the existing shared Bridge patch, original Proposition 5.1 source assertions and migration records, and all original proof links. It retains typed mathematical Proposition 5.3 and 5.6 registrations. It never imports completed proofs.

`apply.py` creates a backup and outputs the full modified function. `run.ps1` runs scoped regressions, including the previously failing Phase 167 test. Do not run the full pytest suite until the end of Phase 168.

This fix assumes the previous R2-7(4) ZIP has already been applied. If the scoped regression still fails, restore the original shared module from the prior ZIP's backup before further diagnosis.
