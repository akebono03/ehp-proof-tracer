Phase 144-6-R5-15G
====================

Audit only. No production code, tests, or project documents are modified.

Purpose
-------
R5-15F showed that semantic eligibility explains most currently visible nested
evidence, but semantic role alone over-promotes thousands of recursively nested
proof steps.

R5-15G measures locality relative to selected final-claim Arguments and typed
providers.

For every reachable evidence step it records:
- shortest selected-owner premise distance
- whether the path crosses another non-selected Argument/provider conclusion
- existing mathematical block role
- structured LiteratureReference eligibility
- current R4 visibility

Distance interpretation
-----------------------
1
  Direct premise of selected claim/provider.

2
  One supporting layer below direct evidence.

3+
  Recursive proof expansion.

Boundary interpretation
-----------------------
crossed_boundary=Y means the ownership path passes through another non-selected
Argument/provider conclusion. Such evidence is a candidate for belonging to the
nested subproof rather than the selected final claim/provider.

Important
---------
This is not a production threshold audit. The goal is to determine whether a
generic locality/ownership relation can explain useful evidence without falling
back to global replay depth.

No n/k-specific visibility rule is used.
No inference-rule-name parsing is used.
No pytest is run because production code is unchanged.
