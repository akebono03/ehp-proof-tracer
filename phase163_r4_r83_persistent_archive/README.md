# Phase 163 R4-R83: Opt-in Persistent Source Archive

Adds a source-backed archive catalog and a callable `build_registry_with_source_archive()` function to the repository root. This **does not** alter the existing `build_registry_bridge` API, change theorem facts, auto-register source text on import, or authorize proof search.

The JSON corpus contains 8 exact translated-TeX excerpts from R80 and R81, with checksum, original file, line spans, preserved scope descriptions and unresolved boundaries. One existing reference is reused, three are added to a new in-memory Registry. Source text is not a verified mathematical theorem; this is an opt-in storage/registry integration, **not** semantic production deployment.

## Run

Extract ZIP into the repository root and invoke `run.ps1` from PowerShell. It installs only three explicitly named new files into the root and tests folder, refuses to overwrite differing files, runs focused pytest and prints a summary. No full pytest is run. All five root documents remain unchanged.

## Changed files

- New `phase163_source_archive_registry.py`: functions `load_source_archive_catalog`, `build_registry_with_source_archive`, constants `CATALOG_PATH`, `OWNERS`.
- New `phase163_source_archive_catalog.json`: immutable source transcription snapshot.
- New `tests/test_phase163_r4_r83_source_archive_registry.py`: eight focused tests.
- New `run.ps1` and this README in the distribution directory.

## Limitations

Original edition verification, mathematical semantic validation, canonical/permanent Statement IDs and proof-search integration are outside R83. Registered entries carry `proof_eligible=False`, `mathematics_verified=False`. `AssertionKind.STATEMENT` is a storage schema category, not proof eligibility.
