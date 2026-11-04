# Phase 173 — Final Active-Suite Gate

This package executes the Phase 173 end-of-phase active `tests/` suite **only on a normal run**, once per reviewed Git HEAD. It does not change proof search, mathematical source statements, the Narrative renderer, existing tests, Git staging, or official documentation.

## Scope and evidence

The user-provided Web output for `(n,k) = (4,8), (4,9), (5,3), (4,4)` matches the reviewed incomplete/complete statuses, abstract certificates, and pending-goal presentation. The actual Flask HTML gate previously passed four cases. This does **not** independently verify pixel-level MathJax layout in a browser.

The gate confirms the `develop` checkout equals `origin/develop`, descends from reviewed commit `ac9149beaf91eeef382bc816234bd2d895398667`, has clean tracked files, and retains 15 reviewed Git blobs, including the shared Renderer, relevant Web and test files, active test configuration, and all five updated official documents.

`run.ps1 -DryRun` runs only the gate's focused contract tests and Git source guards. It **does not** run the active full suite. Normal `run.ps1` executes exactly this command:

```powershell
python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider tests
```

The suite output and JSON report are stored outside the repository under `%LOCALAPPDATA%\EHPProofTracerRecovery\phase173_final_gate\`. A successful result prevents accidental repetition on the same commit. Failed attempts require review before another full-suite run.

The active `tests/` scope retains the project's Phase 155 audit-only deselection boundary. The archive of historical tests is not silently treated as part of the active full suite.

## Workflow

Extract `EHP_Phase173_FINAL_ACTIVE_PYTEST_GATE.zip` into the repository root. First run `powershell -NoProfile -ExecutionPolicy Bypass -File .\phase173_final_gate\run.ps1 -DryRun`; then run without `-DryRun`. Inspect `PHASE173_FINAL_FULL_PYTEST=PASS` and the saved report. Do not claim formal Phase 173 closure until the full-suite result has been reviewed and final documentation has recorded the outcome.

## Files

- `run.ps1` — Windows PowerShell gate, no production writes.
- `gate.py` — Git integrity guards, pytest summary validation, and evidence writer.
- `tests/test_gate_contract.py` — focused preflight tests, never the full suite.
- `design.md` — scope, trust, and next-phase boundaries (Japanese).
