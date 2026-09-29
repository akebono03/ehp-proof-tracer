# Phase 144-6 R25-10-R4 — UTF-8 Audit Runner Repair

## Purpose

Repair only the console/output encoding used by the R25-10 ownership audit.

R25-10-R3 reached the ordered-contribution inspection successfully, but the
Windows Python stdout encoding was CP932. Printing a contribution containing
Unicode mathematical subscripts such as `₂` raised `UnicodeEncodeError`.

## Changes

Only this new runner is added.

The runner sets:

- `PYTHONPATH` to the repository root and `tests` directory;
- `PYTHONIOENCODING=utf-8`;
- `PYTHONUTF8=1`.

The audit output file is read back with PowerShell `Get-Content -Encoding UTF8`.

## Production changes

None.

## Existing test changes

None.

## Audit Python changes

None.

## Full suite

Not run. This remains an ownership audit.

## Completion condition

The runner must reach:

`R25-10-R4 RESULT: PASS`

and the output must include the later ownership sections needed to diagnose the
remaining Phase 144-6 regressions.
