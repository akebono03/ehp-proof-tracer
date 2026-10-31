# Phase 172 R2 — Verified Suspension-Relation Display

This package removes **only redundant prose** for verified generator-suspension equations and their immediate symmetry equations. It does not change backward proof search, the Proof Tree, citations, mathematical inference rules, databases, or existing mathematical goals.

The reviewed source is `phase168_r3_5_model_renderer.py` (Git blob `94996b403f1c01f81319824565db422463714f02`). The existing function `render_model_backed_narrative_markdown` receives a single presentation-only projection call. A new, source-backed projection lives in `phase172_r2_suspension_relation_display/projection.py`.

The installer checks the current `develop` branch, reviewed HEAD source blob, unchanged worktree source, exact renderer insertion anchor and Python syntax. It tolerates LF/CRLF differences. It refuses unexpected sources instead of guessing or overwriting local changes.

From the repository root on Windows PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase172_R2_VERIFIED_SUSPENSION_DISPLAY.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase172_r2_suspension_relation_display\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase172_r2_suspension_relation_display\run.ps1" -RunFocusedTests
git status -sb
git diff --stat
```

The dry run writes complete prospective renderer and function files **outside the repository**, under `%LOCALAPPDATA%\EHPProofTracerRecovery\phase172_r2_<UTC timestamp>\`. It does not modify tracked files. The regular run backs up the renderer externally, inserts the guarded projection, runs five separate focused pytest groups, and restores the original renderer if any test fails. There is **no full pytest** in this package.

See `AUDIT_PLAN_JA.md` for scope and completion criteria, and `CODE_FULL_JA.md` for all new code and the complete replacement-function output procedure.
