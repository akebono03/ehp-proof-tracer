# Phase 144-6 R25-11-R6-R1-R2-R1-R1 Audit Test Compatibility Repair

## Scope

This repair changes only one audit-only test file.

Production changes: none.

Locator changes: none.

Existing project test changes: none.

Expected historical selected population remains 190.

## Changed file

### `test_phase144_6_r25_11_r6_r1_r1.py`

The whole audit-only test file is replaced.

The previous test required the exact implementation text:

`$collectorOutput = @(`

That implementation detail belonged to R1-R1 and is no longer valid after the
PowerShell 5.1 syntax repair.

The replacement checks the actual invariant:

- collector output is captured;
- the collector exit code is captured and checked;
- the last error line is obtained through an intermediate variable;
- `TOTAL=*` lines are filtered through an intermediate variable;
- the final total line is selected from that intermediate variable.

The existing parent-runner exit-code and parser-preflight checks are retained.

## Unchanged

- all production modules;
- the historical locator;
- the six-group collector;
- all existing project tests;
- expected historical total 190;
- worktree/cache robustness logic;
- population cache.

## Completion conditions

1. installed locator still passes the Windows PowerShell parser;
2. all focused R1/R1-R1/R2/R2-R1 audit tests pass;
3. historical localization resumes;
4. no production or existing project test changes occur.

No full pytest is run.
