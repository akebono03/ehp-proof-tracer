# Phase 165 Reference-Stop R2 — Runner Repair

This package performs a read-only audit of the actual pi43 backward-search execution. It checks whether the pi32 fixed GIVEN reference survives screening and whether the resulting proof steps include that source and GeneratorSuspension. It does not change the repository's proof engine, source registry, or renderer, and it does not independently certify publication order.

## Installation and execution

Extract this ZIP into the repository root, overwriting the previous `phase165_reference_stop_r2` audit package. From the root run `powershell -ExecutionPolicy Bypass -File ".\phase165_reference_stop_r2\run.ps1"`.

## Runner correction

`run.ps1` temporarily adds the repository root to `PYTHONPATH`, preserving any existing paths and restoring the previous value on exit. This fixes imports of root modules when `audit.py` is executed by pathname from a subdirectory.

## Scope and completion

Only the packaged runner and explanatory files changed. `audit.py` and `test_audit.py` remain unchanged. The runtime audit writes `audit_result.json`, followed by two focused pytest checks. A successful runner does not by itself establish that source GIVEN reuse stopped all unnecessary ancestry expansion. Full pytest is not run.
