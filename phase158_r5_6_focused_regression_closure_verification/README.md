# Phase 158-R5-6 — R5 focused regression / closure verification

## Purpose

Phase 158-R5-6 is verification only.

It does not modify production code or existing tests. It combines the focused regression tests that protect the public Narrative contracts established through R5-1 to R5-5.

## Verified contracts

- Public Narrative shell
- Reference / Proof boundary
- Root target followed by QED
- Depth-2 public Narrative uses the generic route
- Legacy/dedicated routes are not used where the current contract forbids them
- Common equation numbering
- Generic proof ordering
- Web Narrative depth=2 ordering
- Representative public/Web generic-route behavior

## Scope boundary

Repository-wide pytest is intentionally excluded. The full suite is reserved for the final Phase 158 closure.

## Completion condition

All focused tests pass and `git diff --check` succeeds.
