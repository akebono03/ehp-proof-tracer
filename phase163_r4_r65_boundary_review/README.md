# Phase 163 R4-R65 Boundary Review

This read-only package creates a review packet for the 16 pending definition boundaries produced by R4-R64. It cross-checks source text and source SHA-256 against R4-R63 data, preserves all pending semantic decisions, and groups the 16 candidates into source-local (9), external-context (5), and adjacent-notation (2) categories.

## Run

Extract this archive into the repository root, then run `powershell -ExecutionPolicy Bypass -File .\phase163_r4_r65_boundary_review\run.ps1` from PowerShell.

Requires `phase163_r4_r63_output/source_boundaries.json`, `phase163_r4_r64_output/split_proposals.json`, Python and pytest. Generates `phase163_r4_r65_output/review_packets.json` and `review_packets.md`.

No production source is changed. No mathematical verification or original-edition verification is claimed. No Statement IDs are issued. Only the four focused tests run; the full suite is reserved for the end of Phase 163.
