# Phase 144-6 R25-11-R6-R1-R2-R1 PowerShell 5.1 Syntax Repair

## Scope

This repair changes only the R25-11-R6-R1 audit locator and adds an audit-only
focused test.

Production changes: none.

Existing project test changes: none.

The expected historical selected population remains 190.

The six-group collector is unchanged.

The R2 Windows worktree/cache robustness design is preserved.

## Changed audit files

### `locate_historical_190.ps1`

The whole script is replaced with a Windows PowerShell 5.1-compatible form.

The repair avoids embedding pipelines in parenthesized expressions and uses
simple intermediate variables for pipeline results.

It retains:

- bounded retry/backoff;
- noninteractive Git worktree handling;
- cache read/write retry;
- temporary-file cache replacement;
- `git cat-file` foundation prefiltering;
- existing cache reuse;
- expected total 190.

### `test_phase144_6_r25_11_r6_r1_r2_r1.py`

New audit-only focused tests verify that the syntax repair preserves the R2
behavior and the six-group boundary.

## Installer safety

Before replacing the installed locator, the runner parses the ZIP payload
itself with the Windows PowerShell parser.

After installation, it parses the installed locator again.

Localization starts only after both parser checks and focused tests pass.

## Completion conditions

1. payload parser preflight passes;
2. installed locator parser preflight passes;
3. focused audit-only tests pass;
4. historical localization resumes;
5. no production file or existing project test is changed.

No full pytest is run.
