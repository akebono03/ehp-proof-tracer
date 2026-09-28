Phase 144-6 Final Regression Repair
===================================

Purpose
-------
Repair only the 36 stale regression failures exposed by the Phase 144-6
canonical full-suite run.

Production changes
------------------
None.

Persistent test changes
-----------------------
Nine existing test files are replaced.

Eight legacy pi_6^3 Narrative test modules no longer pin the retired
Phase 133-136 dedicated renderer wording, numbering, tags, section layout,
or punctuation. They now verify the Phase 144-6 public contract:

1. the public pi_6^3 Narrative equals the generic contribution-aware renderer;
2. the mathematical target pi_6^3 = Z/4{nu'} remains present.

The Phase 134-16 presentation catalog test is updated to the current
production definition catalog, which includes TodaLemma513Statement.

Boundary
--------
This package does not modify production code, CLI/Web routing, generic
Narrative behavior, contribution selection, or any other group route.
It does not implement a future Phase feature.

Testing
-------
Run the focused regression script first. If it passes, run the canonical
Phase-end full suite separately with the existing R4 runner.
