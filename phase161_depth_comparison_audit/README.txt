Phase 161 — depth comparison audit

This package changes no project source or tests.
It uses the Phase 59 test builder to construct a deliberately seeded repository
and rule catalog, then compares max_depth=2,3,4 for the same isomorphism goal.
It does NOT test unseeded production goal-only search.

Run from the repository root:
  powershell -ExecutionPolicy Bypass -File ".\phase161_depth_comparison_audit\run_phase161_depth_comparison.ps1"

Output: phase161_depth_comparison_audit.json
