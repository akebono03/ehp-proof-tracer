# Phase 144-6 R25-11-R6-R1-R2-R1-R2-R2-R3-R2 Cleanup Syntax Repair

## Reason

R3-R1 successfully parsed the installer, but its preflight correctly detected
that the residual-worktree cleanup script still contained PowerShell 5.1
parser-incompatible multiline parenthesized expressions.

Because the preflight stopped execution, the R3 locator repair was not
installed, cleanup was not executed, and historical localization was not
resumed.

## Changed files

Only this repair package's complete cleanup script is changed:

`cleanup_verified_a2d9_worktrees.ps1`

The R3-R1 installer is unchanged.

The R3 locator payload is unchanged.

The R3 audit-only test is unchanged.

Production changes: none.

Existing project test changes: none.

## Cleanup syntax change

The cleanup script now avoids multiline parenthesized expressions for exception
messages. Messages are assembled through sequential assignments and then
thrown as scalar strings.

The two candidate worktree paths remain:

- repository `.phase144_6_r25_11_r6_r1_worktree`;
- the dedicated R2-R2 diagnostic worktree under `%TEMP%`.

A path is removed only if it exists and `git -C <path> rev-parse HEAD` exactly
matches `a2d9a4922bb728494d01ece912595aca93b835a6`.

Removal uses normal `git worktree remove --force`.

No manual `.git/worktrees` deletion is performed.

## Execution order

1. parser-check the unchanged R3-R1 installer;
2. parser-check the repaired cleanup script;
3. install the unchanged R3 scalar exit-code locator repair transactionally;
4. clean only verified residual worktrees;
5. run focused historical-localization tests;
6. resume historical population localization.

## Boundary

Expected population remains 190.

Existing population cache is preserved.

No full project pytest is run.
