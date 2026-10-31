# Phase 171 R20R2R2 — Pytest-context citation diagnostic

This is a **read-only**, focused test-context diagnostic. It does not edit any existing Python source, existing tests, database records, or cited evidence.

## What the previous logs establish

The R20R2R1 standalone Python audit finds one eligible ordered `GIVEN` and proves the test goal. The same two tests fail when run in pytest. This package inspects the *actual pytest process* before each test to classify the mismatch.

## Installation and execution

Extract the ZIP at the root of `akebono03/ehp-proof-tracer`, on `develop`.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r20r2r2_pytest_context_probe\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r20r2r2_pytest_context_probe\run.ps1"
```

The script executes **only two existing ordered-citation tests**, in three isolated pytest processes: `prepend`, `importlib`, and `prepend` with third-party pytest autoload disabled. Every run prints a diagnostic snapshot before the test call. Failures are reported without aborting the remaining diagnostic modes. No full test suite is run.

Output snapshots are written to `output/<timestamp>/<mode>.jsonl`. Compare `classification`, `eligibility`, `loaded_module_paths`, and `test_and_backend_function_identical` across modes.

The run does not approve an unverified citation and does not change the first-successful search implementation. `R20R2` remains installed. No conclusion about the mathematical proof of $\pi_6^3$ can be drawn from this diagnostic.
