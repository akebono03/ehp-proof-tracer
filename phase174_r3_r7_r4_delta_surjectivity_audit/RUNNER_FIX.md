# Phase 174 R3-R7-R4R1 — pytest module-name collision correction

## Scope

A read-only runner correction only. No mathematical inference, GIVEN, source
registry, Proof Tree, renderer, Web route, or existing test is changed.

The previous single pytest invocation collected two files named `test_audit.py`
under `--import-mode=prepend`. Pytest imported the first file into the
module name `test_audit` and rejected the second with `import file mismatch`.

Changing back to `--import-mode=importlib` is not appropriate: earlier R3-R7-R2
runs failed with same-named production Python files and package directories.

The runner now invokes pytest in two **separate Python processes**: first the
R4 tests, then the unchanged R3 and EHP regression files. Both keep
`--import-mode=prepend`, `-B`, and `-p no:cacheprovider`. Every test remains
covered, and both invocation exit codes must succeed before the audit runs.

## Files in this patch

- `phase174_r3_r7_r4_delta_surjectivity_audit/run.ps1`: whole-file replacement.
- `phase174_r3_r7_r4_delta_surjectivity_audit/tests/test_r4_runner_split.py`:
  new focused test, adjacent to the existing `tests/test_audit.py`.

## Run

Extract at repository root. Run DryRun first and then normal execution:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r4_delta_surjectivity_audit\run.ps1' -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r4_delta_surjectivity_audit\run.ps1'
```

The existing `audit.py` and its source/HEAD guards are unchanged. The full
project pytest suite is deferred to the end of Phase 174. R3-R7-R5 must not
infer Delta-surjectivity or the zero target from this runner-only change.
