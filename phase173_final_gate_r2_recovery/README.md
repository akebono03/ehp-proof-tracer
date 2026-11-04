# EHP Proof Tracer — Phase 173 Corrective Final Gate R2

This package re-runs the current active `tests/` suite **only after** the Phase 167 reference-layout test-contract repair has passed its focused verification.

## Review baseline

- Reviewed `develop` base: `ac9149beaf91eeef382bc816234bd2d895398667`.
- First phase-end full suite: `3541 passed, 5 failed` (exit code 1). The failure and its original reports **must be preserved**, not overwritten or erased.
- The three Phase 167 test files were corrected by R1, and six focused tests passed. Their exact normalized UTF-8 digests are checked before another full run.
- All fifteen previously reviewed source and documentation Git blobs are checked. No unrelated tracked changes are permitted.
- Full-suite command: `python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider tests`.
- Expected active-suite count: **3546 passed**; exit code must be zero.

## Execution

Extract this ZIP at the repository root, then use:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_final_gate_r2_recovery\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_final_gate_r2_recovery\run.ps1"
```

DryRun executes only the new gate's focused tests and read-only checks. It does not launch the active full suite.

Normal execution verifies previous failure evidence and creates an exclusive R2 attempt before running the active full suite once. Test output and the new R2 report are written to `%LOCALAPPDATA%\EHPProofTracerRecovery\phase173_final_gate_r2\`. The original report remains under `%LOCALAPPDATA%\EHPProofTracerRecovery\phase173_final_gate\` and is never modified. A recorded R2 success prevents another full execution; an incomplete or failed R2 attempt requires explicit review before any retry.

The gate does not stage, reset, clean, or commit Git changes, and does not modify application source files. The only allowed existing tracked worktree changes are the three reviewed Phase 167 test fixes. Nonrelated changes or mismatched HEAD/Blob evidence fail closed.

Even a successful R2 result does not by itself formally close Phase 173. The phase-end result and scope must still be recorded in the five project documents. Browser content for four representative cases was reviewed; independent pixel-level MathJax/layout verification remains unconfirmed.
