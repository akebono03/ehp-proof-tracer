# Phase 176 R3R55 — Isolated equality display projection

This package adds a presentation-only projection and tests. The existing public Renderer is **not modified**. R54 and R53 preflight and trust checks run unchanged. An isolated copy of the reviewed rendering function is executed in memory against exactly the same completed model and partial prefix. The package contains no new mathematical inference, source, GIVEN, or target-specific display logic.

The supplied R54 report identifies nine notation identities, two symmetry repetitions, two notation-transport repetitions, and a final cyclic-structure duplication. These fourteen expected indices are used only in the integration audit. The projection checks actual typed premise edges, retained witnesses, citation ownership, and the completed root. Matching LaTeX is a final appearance guard only, not evidence of typed equality. The separate GeneratorImage/Relation suspension display with different notation is outside this slice.

## Run

Run `run.ps1 -DryRun`, then `run.ps1` from the develop worktree with the R54 package present. The script checks reviewed source blobs, runs four focused pytest files in separate processes, and runs the real public proof audit plus the in-memory rendering comparison. Full pytest is not run. It checks no existing repository file has changed.

## Evidence and gate

`%LOCALAPPDATA%/EHPProofTracerAudit/phase176_r3r55_equality_display_isolated/` receives `before.md`, `shadow.md`, `narrative.diff`, `plan.json`, `shadow_renderer_FULL.py.txt`, and on success `report.json`. The full shadow function is exported from the pinned local source, not a manually abbreviated replacement. A mismatch stops with evidence; no production patch is applied. The gate is `PASS_R3R55_ISOLATED_EQUALITY_PROJECTION`. On success the next step is reviewing the shadow output and regression impact before connecting the shared renderer.
