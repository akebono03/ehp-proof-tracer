# Phase 168 R3-25 — General Exactness Chain Rendering

Replaces only `render_model_backed_narrative_markdown()` in `phase168_r3_5_model_renderer.py`. This package requires that R3-24 has already been applied.

Typed EHP exactness windows are merged by exact equality of adjoining `(source group, map, target group)` arrows. The algorithm accepts any number of consecutive windows and does not hard-code the Δ–E–H sequence. Cyclic or branched graphs fail closed: their individual windows are retained.

No search rules, Proof Tree steps, citation model, or existing imports are changed. The script backs up the current file and refuses to apply unless it detects R3-24.

The focused tests check π₃² (three windows into one sequence), π₄³ (two windows into one sequence), and the existing R3-23 and R3-24 regressions. Full pytest is deferred until the end of Phase 168.

## Run

Unpack this ZIP in the repository root and run `powershell -ExecutionPolicy Bypass -File .\phase168_r3_25_general_exactness\run.ps1`.

Tests have not been run in this environment because the full local repository is not mounted.
