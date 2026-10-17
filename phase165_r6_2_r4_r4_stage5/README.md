# Phase 165 R6-2 R4-4 Stage 5

This package adds a single general inference rule: injective and surjective implies isomorphism. It does not add group-specific adapters, certify a homotopy group proof, or run the full test suite.

Run from the repository root via `powershell -ExecutionPolicy Bypass -File .\phase165_r6_2_r4_r4_stage5\run.ps1` after extracting the ZIP.

The installer checks that the previous stages' statement classes exist, then appends the new rule to `map_property_rules.py`, keeping a backup. The install is idempotent. It runs unit tests first, then targeted integration and regression tests.
