# Phase 144-6 R25-11-R6-R1-R2-R1-R2-R2-R3-R4-R1 Focused Test Manifest Repair

## Observed result from R3-R4

R3-R4 successfully completed the important audit-harness repair:

- installer parser preflight passed;
- cleanup parser preflight passed;
- candidate structural preflight passed;
- candidate locator parser preflight passed;
- installed locator parser preflight passed;
- the whole-function repair was installed;
- both verified residual `a2d9a492...` worktrees were removed.

The run stopped only because the R3 audit-only test file named explicitly by
the runner did not exist in the historical audit directory. Pytest therefore
returned exit code 4 before running tests.

## Scope of this repair

Production changes: none.

Historical locator changes: none.

Collector changes: none.

Population cache changes: none.

Expected historical population remains 190.

No worktree cleanup is repeated.

## Audit-only files

This package explicitly installs both tests required by the latest harness
state:

- the R3 scalar native exit-code test;
- the R4 complete `Measure-Commit` function test.

This removes dependence on whether a previous repair package happened to copy
an audit-only test before stopping.

## Focused test manifest

The runner no longer hard-codes a long list of historical audit test filenames.

It enumerates the actual `test_*.py` files in the historical localization audit
directory and then runs pytest on that directory.

This keeps the test scope focused on the historical localization harness while
avoiding path failures caused by optional/intermediate repair test files.

## Preflight before pytest

The runner verifies that the already-installed locator:

- parses successfully;
- contains scalar `$addExitCode = $LASTEXITCODE`;
- still contains `$Expected = 190`.

Only then are focused tests run.

## Completion boundary

If the focused audit directory passes, the runner immediately resumes the
historical population localization. The next useful result should therefore be
an actual measurement at or after commit `a2d9a492...`, rather than another
worktree-harness failure.

No full project pytest is run.
