# Phase 144-6 R25-30-R2 Cycle-Consistent Entry-Branch Ownership Audit

## Purpose

R25-30 correctly targeted the remaining giant group-structure and definition
entry branches, but its focused audit contract used inconsistent cycle
boundaries for entry and child closures.

The child traversal excluded the entry step while the entry traversal did not.
In a dependency graph containing cycles, this means the two closures were not
measured on the same graph and simple size comparison was not a valid
invariant.

## Production changes

None.

## Existing repository test changes

None.

## Audit repair

R25-30-R2 measures both entry and child closures with the same boundary:

- other Argument conclusion steps are excluded;
- the current Argument conclusion steps are excluded;
- the entry step is not specially excluded from child traversal.

The focused contract now verifies actual set inclusion:

- every child step closure is a subset of its entry step closure;
- every child block projection is a subset of its entry block projection.

This preserves cycle behavior instead of comparing closure counts produced
under different traversal conditions.

## Scope

The diagnostic purpose remains unchanged: identify whether the remaining giant
group-structure and definition entry branches are dominated by one immediate
child or by several independently giant children.

No production ownership rule is changed in R25-30-R2.

Repository-wide pytest remains deferred until the end of Phase 144-6.
