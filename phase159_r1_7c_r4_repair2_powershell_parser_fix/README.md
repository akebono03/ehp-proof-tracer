# Phase 159 R1-7c R4 repair2

## Problem

`repair1` did not reach the R4 audit.

Windows PowerShell reported parser errors in the helper script around multi-line
parenthesized `throw` expressions.

## Fix

This package changes only the R4 PowerShell runner/helper.

- all `throw` statements use single-line interpolated strings,
- the repository root is prepended to `PYTHONPATH`,
- a non-zero Python exit code stops execution,
- `output/summary.md` must exist before it is displayed,
- the original `PYTHONPATH` is restored in `finally`.

## Scope

Production code changes: none.

Audit Python changes: none.

Existing test changes: none.

Repository-wide pytest: not run.
