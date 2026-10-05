# Phase 158-R4 — 112-group prose formatting / continuity audit

This package is audit-only.

## Scope

Population:

- `n = 2..15`
- `k = 0..7`
- 112 groups
- proof replay depth: 2
- public Narrative renderer

The audit checks:

1. standalone `.` lines;
2. equation tags that are emitted but never cited elsewhere;
3. equation references without a matching tag;
4. ambiguous anaphoric prose such as `この群構造と`;
5. adjacent math-only calculation paragraphs that may need to be merged.

Items 2, 4, and 5 are review candidates. They are not automatically treated as production defects.

## Non-goals

- No production code is modified.
- No existing test is modified.
- Full `pytest` is not run.
- No Phase 158-R4 repair is performed yet.

## Outputs

`audit_output/summary.txt`
: human-readable summary.

`audit_output/summary.json`
: machine-readable summary.

`audit_output/findings.csv`
: all findings with group, category, line number, and excerpt.

`audit_output/exceptions.json`
: rendering exceptions.

`audit_output/group_outputs/*.md`
: rendered Narrative for all 112 groups.

## Completion condition for this audit step

- 112 groups rendered;
- 0 exceptions;
- findings classified into common causes before any production repair.
