# Phase 144-6 R25-11-R6-R1-R2-R1-R2-R2-R3-R3 Payload PowerShell 5.1 Syntax Repair

## Observed boundary

R3-R2 established that both the installer and cleanup script parse under the
user's Windows PowerShell 5.1 environment.

Installation then stopped at the transactional candidate-locator parser
preflight. The candidate was not copied over the installed historical locator.

Therefore:

- the R3 scalar exit-code repair is still not installed;
- residual worktree cleanup has still not run;
- historical localization has still not resumed;
- production remains untouched.

## Changed files

This package changes only historical-audit repair artifacts:

- complete `Remove-TemporaryWorktree` payload;
- complete existing `Measure-Commit` worktree-add action payload;
- complete installer `Assert-PowerShellParses` function as part of the installer
  file.

The audit-only R3 test is unchanged.

The R3-R2 cleanup script is unchanged.

Production changes: none.

Existing project test changes: none.

Collector changes: none.

Expected historical population remains 190.

## PowerShell 5.1 compatibility

The payload no longer uses multiline parenthesized `throw (...)` expressions.

Error messages are built using sequential scalar assignments and then thrown.

The installer parser diagnostic now prints each parser error's line, column,
extent text, and message. This makes any remaining candidate-locator syntax
boundary directly observable instead of requiring another blind repair.

## Execution

The runner still performs:

1. installer parser preflight;
2. cleanup parser preflight;
3. transactional candidate locator construction and parser preflight;
4. installed locator parser preflight;
5. verified residual worktree cleanup;
6. focused historical-localization tests;
7. historical 190 localization.

No full project pytest is run.
