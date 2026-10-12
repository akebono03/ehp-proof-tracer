# Phase 163 R4-R50 — Scoped Source Context Review

This package reviews a deliberately bounded selection of the TeX candidates identified in Phase 163 R4-R49. It preserves all 316 review records, marks previously excluded lexical artifacts, and assigns context-based provisional roles to a manually selected set of passages. Every remaining mathematical passage is explicitly pending.

Prerequisites: R4-R49 `phase163_r4_r49_output/triage.json`, R4-R47 `phase163_r4_r47_output/catalog.json`, and the five immutable TeX source files under `phase163_r4_r42_tex_extract/inputs`.

Extract the ZIP into the project root. Run `powershell -ExecutionPolicy Bypass -File .\phase163_r4_r50_semantic_review\run.ps1` from the root directory. It runs only focused tests and writes `phase163_r4_r50_output/review.json`, `review_queue.csv`, and `report.md`.

This is a read-only audit. No mathematical statement is certified, no reference ID is allocated, and no production registry, source, or catalog is updated.

Repair note: the focused test fixture reads the same phase output paths as `run.ps1`; the earlier archive incorrectly looked for `triage.json` and `catalog.json` directly in the project root.
