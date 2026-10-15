# Phase 165 Renderer R5-R1: Audit Scope Fix

This is a read-only correction to the R5 final audit. The previous auditor recursively counted archived installer folders and rollback backups as active sources, causing 608 apparent legacy imports across 5,820 Python files. This version examines Python files directly at the project root plus the official `tests/` subtree. Historical or backup files in other folders are excluded deliberately, without claiming their imports were removed.

The same canonical Renderer and shared-model checks remain in place. The report includes its scan scope; it inventories helper functions for manual review. It does not certify arbitrary mathematical proofs, dynamic import behavior, or that every helper is part of a single Narrative construction. No application source is changed. The full test suite is not run.

Unzip into the repository root and run `phase165_renderer_r5_r1_scope_fix/run.ps1` from Windows PowerShell. Reports are created in `phase165_renderer_r5_r1_scope_fix/audit_output/`. The script executes the corrected auditor, its targeted tests, and the existing `test_phase165_r56_common_renderer.py`.
