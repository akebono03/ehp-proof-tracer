# Phase 144-6 R25-11-R6-R1-R1 Runner Repair

## Scope

This repair changes only the R25-11-R6-R1 audit runner.

Production changes: none.

Existing project test changes: none.

## Changed audit files

### `locate_historical_190.ps1`

The whole script is replaced.

Changes:

- replaces the Windows PowerShell parser-sensitive parenthesized pipeline usage;
- captures Python output in an explicit array;
- selects the final error/output line outside the array expression;
- checks Git worktree command exit codes;
- preserves the original historical-190 localization logic.

### `run_phase144_6_r25_11_r6_r1.ps1`

The whole script is replaced.

Changes:

- adds a PowerShell parser preflight for `locate_historical_190.ps1`;
- checks the lightweight pytest exit code;
- invokes the child PowerShell process explicitly;
- captures and propagates the child exit code;
- prints `completed` only after localization exits successfully.

### `test_phase144_6_r25_11_r6_r1_r1.py`

New audit-only test file.

It verifies:

- the repaired output-capture form;
- child exit-code propagation;
- parser-preflight presence.

## Unchanged

The following are unchanged:

- all production Python modules;
- all existing project tests;
- the six-group target set;
- expected historical population 190;
- historical localization candidate policy;
- population cache format.

## Run

Extract this ZIP into the repository root and run
`run_phase144_6_r25_11_r6_r1_r1.ps1`.

The installer replaces only the two broken audit scripts and adds one audit-only
test, then immediately runs the repaired localization audit.

## Completion condition

This repair is complete when:

1. PowerShell parser preflight passes;
2. runner-repair focused tests pass;
3. localization begins without the previous parser error;
4. a non-zero localization exit is propagated rather than followed by a false
   `completed` message.

No full pytest is run.
