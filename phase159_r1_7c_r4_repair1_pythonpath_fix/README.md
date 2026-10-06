# Phase 159 R1-7c R4 repair1

This repair changes only the R4 audit runner.

## Problem

The R4 audit script lives in a subdirectory. When Python executed that file directly,
the repository root was not present on `sys.path`, so importing repository modules such as
`toda_calculation_facade` failed.

## Fix

The repaired PowerShell runner follows the repository's established execution pattern:

- save the original `PYTHONPATH`,
- prepend the repository root,
- run the audit,
- fail immediately if Python returns a non-zero exit code,
- verify that `output/summary.md` was created,
- restore the original `PYTHONPATH` in `finally`.

## Scope

Production code changes: none.

Audit Python changes: none.

Existing test changes: none.

Repository-wide pytest: not run.
