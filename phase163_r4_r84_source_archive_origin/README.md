# Phase 163 R4-R84 — Separate Source Archive Origin

This narrowly changes the unified registry's `AssertionOrigin` enum by adding `SOURCE_ARCHIVE = "source_archive"` and changes the R83 source archive builder to use it for its eight transcribed TeX statements. The fixed mathematical assertions and proof-internal assertions retain their existing origins.

The package applies guarded replacements and saves originals as `unified_statement_registry.phase163_r84_before.py.bak` and `phase163_source_archive_registry.phase163_r84_before.py.bak`. It refuses to run when current source differs from the expected R83 and R2 shapes, or when backups already exist. Run from the project root using `powershell -ExecutionPolicy Bypass -File .\phase163_r4_r84_source_archive_origin\run.ps1`.

The runner executes only focused pytest tests covering R84, R83, and the unified registry. It does not create final statement identifiers, turn on proof eligibility, modify proof search, or run the full suite. The package includes the entire replacement R83 module and the exact replacement enum in the migration script. All other existing functions and classes are unchanged.
