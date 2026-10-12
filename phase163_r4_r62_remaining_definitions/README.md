# Phase 163 R4-R62 — Remaining Definition Candidate Inventory

This package performs a read-only, evidence-preserving inventory of the 16 Definition candidates not previously reviewed in R4-R55 through R4-R61.

## Prerequisites

Run from the EHP Proof Tracer project root using the bundled `run.ps1`. The following output files must exist:

- `phase163_r4_r52_output/crosswalk.json`
- `phase163_r4_r53_output/overlap_audit.json`
- `phase163_r4_r61_output/registration_gate.json`

The script runs nine focused pytest tests before writing `phase163_r4_r62_output/remaining_definitions.json`, `.csv`, and `report.md`.

No production code, registry, IDs, or proof search is changed. Editorial candidate names are **not verified mathematical symbols**, and source order is **not** a verified publication position.
