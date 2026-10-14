# Phase 165 R27-R57 — Legacy Retirement Gate

This is an intentionally fail-closed, non-destructive migration gate. The last four `repository_*` modules cannot be deleted safely solely because the new group entry exists: `toda_calculation.py` still imports them, and legacy tests exercise that API.

`run.ps1` writes `phase165_r27_r57_audit.json` and runs seven targeted installer tests. It does **not** delete or rewrite production code, does **not** execute the full test suite, and does not claim mathematical proof completion. Inspect `production_legacy_importers`, `test_legacy_importers`, and `typed_entry_legacy_imports` before replacing the old report and calculation API in a subsequent phase.

This scanner handles static imports and literal dynamic imports. Dynamically constructed module names and runtime plugin loading require separate review.
