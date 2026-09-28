# Phase 144-6 R25-11-R6-R1-R2-R1-R2-R2-R3-R1 Installer Syntax Repair

## Reason for this repair

The R3 package stopped before installation because Windows PowerShell 5.1 could
not parse multiline parenthesized string concatenations in the installer.

The scalar exit-code repair itself was therefore not installed, residual
worktree cleanup was not run, and historical localization did not resume.

## Changed files

Only the repair harness is changed:

- `install_r25_11_r6_r1_r2_r1_r2_r2_r3.ps1`
- `run_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r3_r1.ps1`

The R3 locator payload is unchanged.

The R3 cleanup script is unchanged.

The R3 audit-only test is unchanged.

Production changes: none.

Existing project test changes: none.

## PowerShell 5.1 repair

The installer no longer uses multiline parenthesized concatenation to rebuild
the locator source. It uses simple sequential assignments instead.

The runner now parses both the installer and cleanup script before executing
either one.

## Intended R3 locator changes

After the installer parser preflight passes, the unchanged R3 payload replaces:

- the complete `Remove-TemporaryWorktree` function;
- only the worktree-add action inside `Measure-Commit`.

Native Git stdout/stderr is redirected away from the success stream, and
`$LASTEXITCODE` is stored in scalar local variables before success/failure is
decided.

## Historical boundary

Expected selected population remains 190.

The existing population cache is preserved.

No full project pytest is run.

## Completion conditions

1. installer parser preflight passes;
2. cleanup parser preflight passes;
3. candidate locator parser preflight passes;
4. installed locator parser preflight passes;
5. verified residual `a2d9a492...` worktrees are removed;
6. focused historical-localization tests pass;
7. localization measures `a2d9a492...` and continues toward the historical
   population of 190.
