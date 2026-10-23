# Phase 168 R3-29 — Narrative Order Projection

This small patch extracts existing quotient-placement logic from the new model-backed renderer into a pure model projection, without changing public APIs or the order itself. It does not change proof search, typed statement prose, EHP chain merging, or references.

## Requirements

R3-28 applied after R3-27 and R3-26a. The patch refuses to modify an unexpected renderer and creates a backup.

## Changes

- Replace the whole `render_model_backed_narrative_markdown()` function in `phase168_r3_5_model_renderer.py` (no top-level imports changed).
- Add `phase168_r3_29_order_projection.py`: `NarrativeOrderEntry` and `project_narrative_order()`.
- Add two focused tests. Existing focused tests from R3-23 through R3-28 also run.

## Run

From the repository root, expand this ZIP into `.` and execute `powershell -ExecutionPolicy Bypass -File .\phase168_r3_29_order_projection\run.ps1`.

Only syntax parsing has been performed in the packaging environment; integration tests are to be run in the user's repository. Full pytest remains deferred until the end of Phase 168.
