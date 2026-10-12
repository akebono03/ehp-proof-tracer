# Phase 163 R4-R85 — Explicit Archival Bridge Integration

This package adds an opt-in `build_registry_bridge_with_source_archive()` function. It reuses a single existing Bridge, appends exactly eight `SOURCE_ARCHIVE` assertions and eight `METADATA_ONLY` migration records, and leaves all existing proof links intact. The default `build_registry_bridge()` is unchanged.

Run `run.ps1` from the project root after Phase 163 R4-R84. The runner verifies the exact R84 source module before modifying it, creates a backup, installs two new files, and runs focused tests only. It refuses conflicting existing new files.

This phase does not verify Toda's original edition, construct mathematical semantic assertions, allocate production Statement IDs, connect to proof search, or run the full test suite.
