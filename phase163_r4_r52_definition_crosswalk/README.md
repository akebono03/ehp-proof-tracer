# Phase 163 R4-R52 Definition Crosswalk

This standalone read-only audit compares the 19 definition candidates from R4-R51 with the 23 existing reference IDs and 67 assertion IDs in the frozen R4-R47 registry snapshot. It checks chapter source checksums, recorded candidate anchors, review roles, and catalog identity. It does **not** claim live-registry verification, mathematical equivalence, source-edition verification, or confirmation that 19 new definitions must be registered.

## Windows execution

Extract this package at the EHP Proof Tracer project root, then run `powershell -ExecutionPolicy Bypass -File .\phase163_r4_r52_definition_crosswalk\run.ps1`.

Prerequisites: `phase163_r4_r51_output/review.json`, `phase163_r4_r47_output/catalog.json`, and `phase163_r4_r42_tex_extract/inputs/` (all five TeX chapters).

Outputs: `phase163_r4_r52_output/crosswalk.json`, `crosswalk.csv`, and `report.md`.

The package does not modify production modules, source TeX, catalog, IDs, or proof-search logic. It runs only its nine focused tests, not the complete test suite.
