# Phase 163 R4-R91 — Import Fix

This archive replaces the original R91 folder. It adds a package `__init__.py` exporting the existing public functions and runs the script as a Python module from the repository root. No extraction, mathematical certification, or registry logic has been changed.

Run `run.ps1` from PowerShell after extracting to the repository root. Only R91 targeted pytest tests run; no full-suite pytest.
