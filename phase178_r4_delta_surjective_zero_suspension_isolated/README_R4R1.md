# Phase 178 R4R1 — pytest cache guard fix

Replace only the R4 audit runner `phase178_r4_delta_surjective_zero_suspension_isolated/audit.py`. Keep R4 rule.py, tests/test_rule.py, and run.ps1 unchanged. Disable pytest cacheprovider to prevent mutation of tracked `.pytest_cache` files; retain the strict tracked-tree pre/post guard and display dirty paths on failure. The R4 gate names and the 10-test scope are unchanged.

Inspect local staged and unstaged changes before extraction; only restore confirmed generated cache changes, never unrelated work. If other tracked changes exist, stop and inspect. No automatic restore is performed by the package.

Run the existing R4 run.ps1 with -DryRun and then normally. Full pytest is not part of this recovery.
