# Phase 165 R27-R37 — Legacy dependency batch sweep

This installer removes unused imports from the migrated Web/CLI entry modules, recomputes top-level repository dependencies and deletes unreachable `repository_*.py` implementation files in one transaction with backups. It does not delete the core proof repository representations or live renderers. It does not change typed mathematical inference rules, execute the full test suite, or establish applicability/execution proof completeness.

The audit output is `phase165_r27_r37_audit.json` and the backups are placed in `phase165_r27_r37_backup/`. Run `run.ps1` from PowerShell after extracting the ZIP in the repository root. The audit may legitimately show no changes if dependencies remain live.
