# Phase 144-6 R25-10-R6 — Combined UTF-8 and Argument API Audit Runner

## Purpose

R25-10-R5 correctly repaired the audit harness to use the current
`TodaGroupProofNarrativeArgument.conclusion_block` API, but its runner
accidentally dropped the UTF-8 execution settings introduced in R25-10-R4.

As a result, Windows CP932 stdout failed while printing mathematical Unicode
such as `₂` before the audit could reach Section F.

R25-10-R6 combines both already-established audit requirements:

1. the R5 `conclusion_block` API repair must already be present;
2. Python audit stdout/stderr must run as UTF-8.

## Changed files

This package adds only:

- `run_phase144_6_r25_10_r6.ps1`
- `README.md`

It does not change the audit Python script, production code, or existing tests.

## Environment

The runner sets:

- repository root and `tests` on `PYTHONPATH`;
- `PYTHONIOENCODING=utf-8`;
- `PYTHONUTF8=1`.

The audit is executed through `cmd /c` with stdout and stderr redirected to the
audit output file, then displayed with `Get-Content -Encoding UTF8`.

## Full suite

Not run. This remains an audit-only step.

## Completion condition

The runner must reach:

`R25-10-R6 RESULT: PASS`

and the audit must complete through Sections A-G.
