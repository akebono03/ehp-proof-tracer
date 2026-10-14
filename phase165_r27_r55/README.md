# Phase 165 R27-R55 — Isolate Legacy Calculation Imports

This patch moves four repository-specialization imports from module level into the legacy calculation functions that actually use them. It also defers the legacy `toda_calculation` import in `toda_calculation_report.py`.

It preserves all existing calculation functions, their signatures, and their bodies. It **does not** remove the four remaining repository modules or claim mathematical equivalence between the old calculation format and `PartialProofResult`.

Run `run.ps1` from the extracted project directory. The installer records its changes in `phase165_r27_r55_audit.json`, keeps original files under `phase165_r27_r55_backup`, and runs only its targeted tests. The complete test suite is reserved for the end of Phase 165.
