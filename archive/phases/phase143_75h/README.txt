Phase 143-75H
=============

Purpose
-------
Audit semantic field shapes for the three remaining
Whitehead-square / Hopf-invariant statement types.

Targets
-------
- TodaPi32WhiteheadSquareUpToSignStatement
- TodaProp27HopfInvariantUpToSignStatement
- Toda58WhiteheadSquareUpToSignStatement

Scope
-----
n=2..15
k=0..7
max_depth=7

This phase is audit-only.
No production code, tests, or documentation are modified.

The audit records:
- occurrence counts
- number of groups
- dataclass field names
- runtime field value shapes
- inference rule names
- representative statement repr samples

Expected counts from Phase 143-75G:
- TodaPi32WhiteheadSquareUpToSignStatement: 60
- TodaProp27HopfInvariantUpToSignStatement: 53
- Toda58WhiteheadSquareUpToSignStatement: 33
