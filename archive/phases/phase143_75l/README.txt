Phase 143-75L
=============

Purpose
-------
Audit whether the four Toda finite-dimensional aggregate
statement types can be rendered from their existing semantic
fields without parsing inference-rule names or adding
proposition-specific prose.

Targets
-------
- TodaProp53FiniteDimensionalStatement
- TodaProp58FiniteDimensionalStatement
- TodaProp59FiniteDimensionalStatement
- TodaProp511NuSquaredFiniteDimensionalStatement

Scope
-----
n=2..15
k=0..7
max_depth=7

Design candidate
----------------
For each aggregate statement:
- Relation fields:
  render lhs with render_toda_primary_group_latex()
  render rhs with render_toda_raw_group_structure_latex()
  render relation_type semantically.
- TodaPrimaryGroupZeroStatement fields:
  render group = 0.
- ScalarGreaterEqualStatement fields:
  reuse the common scalar LaTeX renderer.
- literature_statements:
  treat as provenance metadata, not mathematical content
  duplicated in the Narrative fact.

Expected count
--------------
76 + 25 + 20 + 14 = 135 occurrences.

This phase is audit-only.
No production code, tests, or project documents are changed.
No full pytest run is required.
