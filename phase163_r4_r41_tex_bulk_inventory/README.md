# Phase 163 R4-R41 — TeX Bulk Registration Preflight

This package performs a read-only inventory of Toda_01.tex through Toda_05.tex and the existing unified registry bridge. It does **not** perform bulk registration, modify IDs, modify repository sources, or connect anything to proof search.

Extract this directory into the repository and run `powershell -ExecutionPolicy Bypass -File .\phase163_r4_r41_tex_bulk_inventory\run.ps1` from its root. The focused pytest tests run before the inventory; the full suite is deliberately not invoked.

The output `phase163_r4_r41_output/inventory.json` records TeX hashes, raw labels, repeated labels, basic heading counts, and existing registry identifiers. TeX source conventions, semantic theorem boundaries, and ID equivalences must be confirmed before adding a writer in a later step.
