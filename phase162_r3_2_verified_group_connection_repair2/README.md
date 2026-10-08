# Phase 162 R3-2 repair2

## Cause

The original R3-2 ZIP bundled its new focused test under `phase162_r3_2_verified_group_connection_repair1/tests/`, but the PowerShell script incorrectly executed `pytest tests/test_phase162_r3_2_verified_group_connection.py` relative to the repository root. Pytest consequently reported `file or directory not found`.

## Scope

Only the PowerShell runner and this README differ from repair1. The R3-2 Python implementation, installer and existing focused test remain unchanged. The installer handles an already-updated lower-panel heading and makes backups before applying the integration code.

## Run

Extract into the repository root and run `run_phase162_r3_2.ps1` from the new folder. The R3-2 test is called by its actual path inside the bundle. R2 and R3 tests remain pointed at the repository `tests` directory. The full suite is not run.
