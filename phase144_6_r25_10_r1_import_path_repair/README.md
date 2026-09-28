# Phase 144-6 R25-10-R1 — Audit Import-Path Repair

## Purpose

Repair only the R25-10 diagnostic harness.

The original R25-10 audit attempted to import local test files as
`tests.<module>`. In the user's environment those files are executable by
pytest but are not importable through that package path, producing
`ModuleNotFoundError`.

## Changes

Only:

`phase144_6_r25_10_final_regression_ownership_audit/audit_phase144_6_r25_10.py`

is changed.

The repair:

- adds `importlib.util`, `Path`, and `sys`;
- adds `load_test_module()`;
- resolves `tests.<name>` to the actual `tests/<name>.py` path;
- loads the file with `importlib.util.spec_from_file_location()`;
- caches loaded audit modules in `sys.modules`;
- replaces direct `importlib.import_module("tests....")` calls with the file
  loader.

## Production changes

None.

## Existing test changes

None.

## Full suite

Not run. R25-10-R1 only repairs and executes the ownership audit.

## Completion condition

The runner must reach:

`R25-10-R1 RESULT: PASS`

and produce a populated:

`phase144_6_r25_10_output.txt`

The resulting ownership data is then used to choose the minimal production
repair boundary.
