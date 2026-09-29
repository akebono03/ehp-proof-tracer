# Phase 144-6 R25-11-R6-R1-R2-R1-R2-R2-R3 Native Command Scalar Exit-Code Repair

## Objective

Resume historical localization of the retained six-group selected contribution
population, whose expected historical value is 190 and whose current value is
192.

The preceding diagnostic established that Git successfully created the
worktree for commit `a2d9a4922bb728494d01ece912595aca93b835a6`, while PowerShell
native stderr/output handling caused the audit harness to classify the
operation as failed.

## Current code inspected before this repair

The historical locator and its related audit tests were inspected before
building this package. The current GitHub `develop` production files and
retained foundation/order tests were also checked and were unchanged from the
previous audit.

## Changed historical-audit code

### `Remove-TemporaryWorktree`

The complete function is replaced.

For `git worktree remove` and `git worktree prune`, it now:

1. temporarily sets `$ErrorActionPreference` to `Continue`;
2. redirects native stdout and stderr away from the PowerShell success stream;
3. immediately stores `$LASTEXITCODE` in a scalar local variable;
4. restores the prior error-action preference;
5. throws only when that scalar exit code is non-zero.

### `Measure-Commit`

Only its existing worktree-add action is replaced.

The action applies the same scalar exit-code discipline to:

`git worktree add --detach $Worktree $Sha`

No other part of `Measure-Commit` is changed.

## Added audit-only test

`test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r3.py`

It verifies scalar exit-code handling for add, remove, and prune, and confirms
that the historical target remains 190.

## Residual worktree cleanup

The previous diagnostic left two worktrees pointing at
`a2d9a4922bb728494d01ece912595aca93b835a6`.

Before localization resumes, the runner checks each candidate path with
`git -C <path> rev-parse HEAD`.

It removes a worktree with the normal:

`git worktree remove --force`

only when the HEAD exactly equals the expected `a2d9a492...` commit.

It does not manually delete `.git/worktrees` metadata.

## Scope boundary

Production changes: none.

Existing project test changes: none.

Collector changes: none.

Expected population: still 190.

Existing population cache: preserved.

No full project pytest is run.

## Completion conditions

1. candidate and installed locator parser preflights pass;
2. only verified residual `a2d9a492...` worktrees are removed;
3. focused historical-localization tests pass;
4. historical localization measures `a2d9a492...` instead of reporting a false
   worktree-creation failure;
5. localization continues toward an `EXACT_190_SHA` result or produces a new
   concrete semantic/runtime boundary.
