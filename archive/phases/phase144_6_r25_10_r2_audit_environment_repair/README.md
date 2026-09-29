# Phase 144-6 R25-10-R2 — Audit Execution-Environment Repair

## Purpose

Repair only the execution environment of the R25-10 ownership audit.

R25-10-R1 successfully changed the top-level local-test loading from package
imports to file-path loading. The loaded historical audit helpers, however,
contain bare imports such as:

`test_phase144_6_r5_18_production_generic_proof_chain_foundation`

Those imports require the repository's `tests` directory itself to be present
on `PYTHONPATH`.

## Changed file

Only the R25-10-R2 runner contained in this package is new.

No production source file is changed.

No existing test file is changed.

The R25-10 audit Python file is not changed by R2.

## Execution environment

The runner sets:

- repository root on `PYTHONPATH`;
- repository `tests` directory on `PYTHONPATH`.

It performs two import preflights before running the ownership audit.

## Error capture

The audit is executed through `cmd /c`, with stdout and stderr redirected to
`phase144_6_r25_10_output.txt`.

This avoids PowerShell converting Python stderr into a terminating
`NativeCommandError` before the complete traceback can be recorded.

## Full suite

Not run. This package is audit-only.

## Completion condition

The runner must reach:

`R25-10-R2 RESULT: PASS`

The populated R25-10 output can then be used to identify the ownership of the
remaining Phase 144-6 regressions.
