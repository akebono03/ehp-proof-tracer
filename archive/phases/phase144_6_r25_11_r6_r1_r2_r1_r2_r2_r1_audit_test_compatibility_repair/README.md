# Phase 144-6 R25-11-R6-R1-R2-R1-R2-R2-R1 Audit Test Compatibility Repair

## Scope

This repair changes only two audit-only tests that still asserted the obsolete
single-object `git cat-file` implementation.

Production changes: none.

Locator changes: none.

Existing project test changes: none.

The six-group collector is unchanged.

The expected historical selected population remains 190.

The existing population cache is preserved.

## Changed audit-only test files

### `test_phase144_6_r25_11_r6_r1_r2_r1_r2.py`

The complete file is replaced. Its assertions now verify the current two-stage
Git semantics:

1. check the commit object;
2. check the foundation path only after the commit exists.

A commit-object failure remains a real audit error. A foundation-path failure
returns `false`.

### `test_phase144_6_r25_11_r6_r1_r2_r1_r2_r1.py`

The complete file is replaced. Its PowerShell 5.1 syntax assertions now check
the current commit/foundation stderr variables and simple message
construction, rather than the obsolete `$objectName`, `$stderrPath`, and
`$exitCode` variables.

## Tests

The runner executes only the focused historical-localization audit tests.

After they pass, the existing locator resumes historical selected-population
localization using the existing cache.

## Completion conditions

1. installed locator parser preflight passes;
2. all focused audit-runner tests pass;
3. commit `9af09b257c...` is classified as `UNAVAILABLE:foundation`;
4. localization continues beyond that commit;
5. production, locator, and existing project tests remain unchanged.

No full pytest is run.
