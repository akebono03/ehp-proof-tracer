# Phase 144-6 R25-11-R6-R1-R2-R1-R2-R1 PowerShell 5.1 Native Git Syntax Repair

## Scope

This repair changes only the historical audit locator function
`Test-FoundationAtCommit` and adds one audit-only focused test file.

Production changes: none.

Existing project test changes: none.

The six-group collector is unchanged.

The expected historical selected population remains 190.

The existing population cache is preserved.

## Changed function

### `Test-FoundationAtCommit`

The complete function is replaced with a Windows PowerShell 5.1-compatible
version.

The function avoids multiline parenthesized expressions. Temporary stderr
filenames and error messages are built with simple assignments.

Native Git behavior remains:

- exit code `0`: foundation exists;
- exit code `1`: foundation is absent and returns `false`;
- any other exit code: raise a real audit error with captured stderr.

## Transactional installation

The installer does not modify the installed locator immediately.

It:

1. reads the current locator;
2. replaces only the complete `Test-FoundationAtCommit` function in memory;
3. writes a temporary candidate locator;
4. parses that complete candidate with the Windows PowerShell parser;
5. installs it only after the candidate passes;
6. parses the installed locator again.

A syntax-invalid candidate therefore cannot replace the installed locator.

## Added audit-only test

`test_phase144_6_r25_11_r6_r1_r2_r1_r2_r1.py` verifies:

- simple stderr-path construction;
- simple error-message construction;
- retained native Git exit-code semantics;
- retained historical target 190.

## Completion conditions

1. candidate locator parser preflight passes;
2. installed locator parser preflight passes;
3. focused audit-runner tests pass;
4. commit `9af09b257c...` is passed as an expected missing-foundation candidate;
5. localization continues toward an exact selected-total-190 commit;
6. no production or existing project test changes occur.

No full pytest is run.
