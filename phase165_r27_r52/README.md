# Phase 165 R27-R52: Isolated Typed Group Facade

Introduces `toda_typed_group_facade.py`, a group-search entry point that does not import the legacy calculation facade, ProofRepository, or repository specialization modules. The two R50 compatibility functions in `toda_calculation_facade.py` delegate to the independent entry point. Existing legacy calculation and report functions remain unchanged, and the four remaining legacy specialization modules are retained until their consumers have been migrated safely.

Run from the repository root with `powershell -ExecutionPolicy Bypass -File .\phase165_r27_r52\run.ps1`. The script runs targeted tests only. Backups are stored in `phase165_r27_r52_backup`; audit output is `phase165_r27_r52_audit.json`.
