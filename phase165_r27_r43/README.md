# Phase 165 R27-R43 — Typed Applicability Core

Adds `toda_typed_applicability.py`, a registry-independent rule matching API over **verified ProofStep objects only**. It reuses the production rule discovery and inference matching APIs and does not execute an inference rule.

## Changes

- New `TypedApplicableRule` dataclass and `find_typed_applicable_rules` function.
- No existing production files edited and no legacy repository modules deleted.
- Targeted tests check parsing, import boundary, empty and invalid inputs, actual matching, and overwrite safety.
- Full pytest intentionally not run.

## Run

Expand the ZIP in the project root and run `powershell -ExecutionPolicy Bypass -File .\phase165_r27_r43\run.ps1`.

## Boundary

The previous `standard_production_applicability_catalog` and `toda_calculation` implementations remain unchanged; migrating their public contracts requires separately verified typed semantics. This step is **not** a completed web applicability or inference execution implementation.
