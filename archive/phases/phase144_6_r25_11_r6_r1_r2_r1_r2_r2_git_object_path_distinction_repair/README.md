# Phase 144-6 R25-11-R6-R1-R2-R1-R2-R2 Git Object/Path Distinction Repair

## Scope

This repair changes only the historical localization audit function
`Test-FoundationAtCommit` and adds one audit-only focused test file.

Production changes: none.

Existing project test changes: none.

The six-group collector is unchanged.

The expected historical selected population remains 190.

The existing population cache is preserved.

## Changed function

### `Test-FoundationAtCommit`

The function now performs two explicit Git object checks.

First it checks:

`<sha>^{commit}`

A failure here is treated as a real Git/audit error.

Only after the commit object is confirmed does it check:

`<sha>:<FoundationPath>`

A failure of this second check means that the retained foundation file does not
exist at that valid commit, so the function returns `false`. The caller can
therefore classify the candidate as `UNAVAILABLE:foundation`.

This deliberately avoids assuming that Git for Windows uses a particular exit
code for a missing path.

## Transactional installation

The successful R2-R1-R2-R1 transactional parser design is retained.

The installer:

1. reads the current locator;
2. replaces only the complete `Test-FoundationAtCommit` function in memory;
3. writes a temporary candidate;
4. parses the complete candidate;
5. installs only after parser success;
6. parses the installed locator again.

## Added audit-only test

`test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2.py` verifies:

- commit-object check occurs before path check;
- commit-object failure is a real error;
- foundation-path failure returns unavailable;
- error-action restoration remains present;
- historical target 190 is unchanged.

## Completion conditions

1. candidate and installed locator parser preflights pass;
2. focused audit-runner tests pass;
3. commit `9af09b257c...` is classified as `UNAVAILABLE:foundation`;
4. localization continues beyond that commit;
5. no production or existing project test changes occur.

No full pytest is run.
