# Phase 175 R13R8R7R1 — Pre-Closeout HEAD Guard Fix

This is a **read-only, focused audit**. It does not change application code, mathematical rules, GIVEN statements, or documentation in the repository.

The previous audit incorrectly required the local HEAD to match one GitHub commit exactly and resolved the repository root one directory too high. This corrected script resolves the repository root relative to the audit folder and checks the **committed, staged, and working** content of both audited production files against their Git blobs verified on GitHub's `develop` branch (commit `b5a0b13884f6f0af527034d8c8bcd47b90c7cc97`). It reports line endings, checks staged and unstaged diffs, and optionally runs one focused pytest module.

From the repository root, extract the ZIP into the repository root, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File '.\R13R8R7R1_precloseout_head_fix\run.ps1' -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File '.\R13R8R7R1_precloseout_head_fix\run.ps1'
```

This does not prove that the local unpublished HEAD is a descendant of the GitHub baseline. It only establishes that the two audited production files have the verified content and that the focused tests pass. Additional proof-display and mathematics review is needed before final closeout. No full test suite is run.
