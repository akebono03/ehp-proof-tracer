Phase157-R20 repair53-r4b
fixed-boundary-aware pi_15^8 Reference consistency audit

Why r4b is needed
-----------------
repair53-r4a passed its hard numbering/marker checks, but exposed two
audit limitations / unresolved candidates.

1. Exact body parsing

r4a split on "## 証明", which also matches the prefix of
"## 証明対象". Therefore its PUBLIC BODY contained the Reference
section and counted one Reference header marker as a body marker.

r4b splits only on the exact section marker:

  "\n## 証明\n"

2. Proposition 5.15 step / statement alignment

After root exclusion r4a showed:

  remaining proof step:
    Toda Proposition 5.15 pi_14^7 finite cyclic

but statement lines:

  pi_15^8 decomposition

The expected fixed component for that remaining step may instead be:

  pi_14^7 = Z/8{sigma'}

r4b does not repair this. It inspects the Phase157
toda_literature_statement_boundary API and prints:

- classify_toda_literature_statement_step() result for every pi_15^8
  Reference proof step
- fixed component catalog for Proposition 5.15 and Proposition 4.4
- non-empty cross-reference component selections
- root-excluded entry/statement alignment
- exact public proof-body markers
- targeted Proposition 5.15 classification

Changes
-------
Production code: none
Tests: none
Documents: none

pytest
------
Not run.

Repository-wide pytest remains reserved for the end of Phase 157.
