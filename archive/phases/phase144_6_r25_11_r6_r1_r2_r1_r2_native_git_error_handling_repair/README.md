# Phase 144-6 R25-11-R6-R1-R2-R1-R2 Native Git Error Handling Repair

## Scope

This repair changes only the historical-localization audit locator function
`Test-FoundationAtCommit` and adds focused audit-only tests.

Production changes: none.

Existing project test changes: none.

The six-group collector is unchanged.

The expected historical selected population remains 190.

The existing population cache is preserved.

## Changed function

### `Test-FoundationAtCommit`

The function now handles Windows PowerShell 5.1 native-command stderr without
allowing an expected missing Git object to terminate the audit.

During `git cat-file -e` only:

- `$ErrorActionPreference` is temporarily changed from `Stop` to `Continue`;
- Git stderr is redirected to a temporary file;
- the native exit code is captured;
- the original error-action preference is restored in `finally`.

Exit codes are interpreted as follows:

- `0`: the retained foundation file exists at the commit;
- `1`: the object/path is absent and the function returns `false`;
- any other exit code: a real audit error is raised with captured Git stderr.

This preserves the foundation prefilter while distinguishing expected absence
from unexpected Git failures.

## Added audit-only tests

`test_phase144_6_r25_11_r6_r1_r2_r1_r2.py` verifies:

- temporary native-error handling;
- stderr capture;
- exit-code distinction;
- retained expected total 190 and foundation prefilter.

## Completion conditions

1. the installed locator passes the Windows PowerShell parser;
2. focused audit-runner tests pass;
3. missing foundation objects are classified as `UNAVAILABLE:foundation`;
4. historical localization continues past commit `9af09b257c...`;
5. no production or existing project test changes occur.

No full pytest is run.
