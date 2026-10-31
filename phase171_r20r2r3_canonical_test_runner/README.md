# Phase 171 R20R2R3 — Canonical Ordered-Citation Pytest Runner

This package fixes **test invocation only**. It does not alter the recursive proof engine, source eligibility, any existing test, or the R20R2 patch.

## Root cause

The repository has two Python modules with the same basename:

- `phase165_r52_r15_ordered_citation.py` at the repository root (canonical, order-only citation policy).
- `phase165_r52_r15_ordered_citation/phase165_r52_r15_ordered_citation.py` inside the historical test directory (legacy, reviewed-assertion citation policy).

When pytest prepends the test directory to `sys.path`, the legacy copy can shadow the canonical module. The two failing tests were executing against the wrong module. Switching to `--import-mode=importlib` is not a reliable fix for this same-name module/directory collision.

## Usage

Extract `R20R2R3_canonical_pytest.zip` into the repository root and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase171_r20r2r3_canonical_test_runner\run.ps1' -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase171_r20r2r3_canonical_test_runner\run.ps1' -Quick
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase171_r20r2r3_canonical_test_runner\run.ps1'
```

The runner explicitly inserts the repository root at the front of the Python import path and loads the canonical module **before** initializing pytest. It validates the source filename and required canonical globals, so an unexpected module causes an error instead of changing citation policy.

`-Quick` runs just the two previously failing tests. The default run executes the same four focused test modules as R20R2. It disables pytest's cache provider, avoids bytecode writes, and does not execute the full test suite. It makes no Git commit and does not reset files.

## Limitations

The earlier R20R2 patch must already be installed. Passing these tests would validate the first-successful search's focused regression baseline, not prove that the web result for the 2-primary component of `pi_6(S^3)` is complete.
