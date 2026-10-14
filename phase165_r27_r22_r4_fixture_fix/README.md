# Phase 165 R27-R22-R4 — Typed Fixture Correction

This package corrects the **test fixture only**: the finite cyclic group generator must be an `Expression`, not a string. It uses an `HomotopyElement` with the existing `ETA_3_GENERATOR` symbol. No production code, registry, or mathematical claims are changed.

Run `run.ps1` in the repository root after extracting this ZIP. The script executes the prior R3 installer tests and three corrected Group Query regression tests. All are targeted tests; the full suite is not run.

The earlier R3 package's `test_patch.py` is intentionally not modified. This R4 package supersedes it for R27-R22 verification.
