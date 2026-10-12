Phase 165 R2 — Verified, ordered registry candidate lookup

Additions in repository root:
  phase165_r2_registry_lookup.py
  tests/test_phase165_r2_registry_lookup.py

This is a shared registry-to-goal lookup stage, not a pi_5^3-specific solver.
It checks typed exact matching, Phase 164 citation eligibility, and a verified proof link.
It never manufactures a GIVEN fact, and does not restore the legacy fallback.
The Phase 165 R1 public entry point is not modified because that local file is
not on the currently accessible GitHub branch. The full backward solver remains
unimplemented and its error path remains intact.

Unzip to project root and run:
  powershell -ExecutionPolicy Bypass -File ".\phase165_r2_registry_lookup\run.ps1"

Only targeted pytest is run. Full pytest is deferred until phase closure.
