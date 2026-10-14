# Phase 165 R27-R46-R1: CLI installer guard correction

This package corrects the R46 installer guard for `main.py` previously modified in earlier phases.
It replaces only `_run_execute_command`, after checking its positional signature, and leaves all other definitions unchanged.
It refuses to overwrite if the signature differs, backs up the original file, and runs focused tests only.

Run `run.ps1` from PowerShell after extracting this archive into the repository root.
No full test suite runs.
