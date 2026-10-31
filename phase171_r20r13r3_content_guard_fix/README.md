# Phase 171 R20R13R3 — Content-guarded installer correction

The R20R13R2 installer incorrectly required one exact Git commit even when the
reviewed files had been committed unchanged on a newer `develop` HEAD.

This archive contains the complete original R20R13R2 package with its installer
corrected. It also adds a small R20R13R3 wrapper, regression tests, and a
read-only final report. Extract with overwrite at the existing repository root.

The corrected installer checks the current branch, the exact tracked
`projection.py` bytes in HEAD, the worktree's `projection.py` bytes, and the
existing renderer hook. It accepts only the two reviewed projection states.
No `git reset`, checkout, pull, or source substitution is performed.

Run `phase171_r20r13r3_content_guard_fix/run.ps1 -DryRun`, then run the same
script without `-DryRun`. Focused tests and the actual canonical public-proof
narrative audit are included; no full-suite test is run.
