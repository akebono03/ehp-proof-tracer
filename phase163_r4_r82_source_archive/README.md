# Phase 163 R4-R82: Source Archive Registration

This package uses the live `UnifiedStatementRegistry` through `build_registry_bridge` and registers eight **unverified source-text** entries into the in-memory registry. It reuses the existing Proposition 2.5 reference and creates three missing references. It neither alters proof search nor declares mathematical verification. No production ID is assigned, and the generated catalog is not automatically connected to the application.

## Requirements

Run from the repository root after R80 and R81. The files `phase163_r4_r80_output/registration_preflight.json` and `phase163_r4_r81_output/duplicate_audit.json` must exist. Run `powershell -ExecutionPolicy Bypass -File .\phase163_r4_r82_source_archive\run.ps1`.

The output is `phase163_r4_r82_output/source_archive.json` and `report.md`. Only focused tests run; no full test suite.
