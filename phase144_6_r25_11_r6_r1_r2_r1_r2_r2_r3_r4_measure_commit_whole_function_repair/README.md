# Phase 144-6 R25-11-R6-R1-R2-R1-R2-R2-R3-R4 Measure-Commit Whole-Function Repair

## Evidence used

The current local historical locator was inspected directly around lines
300-470.

Its complete `Measure-Commit` function starts at line 310 and ends at line 412.
`Parse-Total` starts immediately afterward at line 414.

The current worktree-add action is inside the outer prompt-restoration
`try/finally` and the collector begins in a separate `try` block.

This confirms that substring-based partial replacement is unnecessarily fragile.

## Changed historical-audit functions

### `Remove-TemporaryWorktree`

The complete PowerShell-5.1-safe R3-R3 function is installed.

Native worktree remove/prune operations temporarily use
`$ErrorActionPreference = "Continue"`, redirect native output away from the
success stream, capture `$LASTEXITCODE` in scalar variables, restore the prior
preference, and decide success from those scalar exit codes.

### `Measure-Commit`

The complete function is replaced.

All current behavior is preserved:

- cache lookup;
- foundation availability check;
- `UNAVAILABLE:foundation`;
- cache writes;
- temporary worktree lifecycle;
- collector copy and execution;
- `TOTAL=*` extraction;
- `UNAVAILABLE:no-total`;
- final cleanup;
- returned status/result object.

Only the existing worktree-add native command handling changes:

- native stdout/stderr is redirected away from the PowerShell success stream;
- `$LASTEXITCODE` is immediately copied to scalar `$addExitCode`;
- the previous `$ErrorActionPreference` is restored;
- retry failure is raised only when `$addExitCode` is non-zero.

## Installer change

The installer no longer searches backward for an `Invoke-WithRetry` block.

It replaces complete functions using explicit adjacent function markers:

- `Remove-TemporaryWorktree` through `Write-PopulationCache`;
- `Measure-Commit` through `Parse-Total`.

Before copying the candidate locator over the installed locator, it verifies:

- exactly one `Measure-Commit`;
- exactly one `Parse-Total`;
- scalar `$addExitCode` assignment exists;
- historical expected population remains 190;
- the complete candidate parses successfully.

## Tests

A new audit-only test verifies:

- one complete `Measure-Commit`;
- scalar worktree-add exit-code handling;
- preservation of collector/cache/foundation flow;
- expected historical population 190.

Production changes: none.

Existing project test changes: none.

Collector changes: none.

Existing population cache is preserved.

No full project pytest is run.

## Completion boundary

This repair is complete when the installed locator parses, focused audit tests
pass, commit `a2d9a492...` is actually measured, and historical localization
continues toward an exact population of 190.
