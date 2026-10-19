# Phase 165 R6 — Phase 49/56 dependency root diagnostic

This ZIP runs four focused tests in the repository root, saves the complete log, and changes no production source or tests. A pytest nonzero status is preserved in `report.json` without interrupting report creation. The four tests are selected from the first failure in Phase 49 and downstream Phase 56 symptoms. This does **not** resolve or retire the tests.

Run `powershell -ExecutionPolicy Bypass -File .\phase165_r6_phase49_56_root_check\run.ps1` from the project root.
