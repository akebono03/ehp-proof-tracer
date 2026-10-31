# Phase 171 R20R9R4: E-image target-typing repair

This patch fixes two closely related type-confusions in the source-bound public double-image expansion: a cited equality `2*x=y` must be checked at the suspension target, and `GeneratorImage.target_generator` must be that cited target `y`, not the unsuspended input `z` in the requested goal `2*x=E(z)`.

The single existing production function is replaced. The original typed inference rule and the shared provider remain unchanged. The full R20R9R2 state is reconstructed from a reviewed baseline, verified against the worktree, backed up, and upgraded without accepting unknown edits. The installer preserves line endings and does not duplicate changes on reruns.

Use PowerShell from the EHP Proof Tracer repository root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r20r9_public_cited_double_image\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r20r9_public_cited_double_image\run.ps1"
```

The runner invokes focused tests in separate pytest processes (the R20R8 and R20R9 suites both contain a `test_source.py`), followed by a genuine read-only public search audit. The full test suite is reserved for Phase closeout. No new mathematical GIVEN or pre-built proof tree is supplied to the search.
