# Phase 168 R3-39D import-scope fix

This package corrects the installer that failed with `UnboundLocalError: ScalarSymbol`.
It removes the duplicate function-local import while preserving the existing module-level import.
The same four production files and three focused tests are used. No full suite is run.

Extract at repository root and execute `run.ps1` in PowerShell. A backup is taken
before any changes, and all four files are restored if the limited tests fail.
The installer writes the full resulting source files into `full_files/`.
