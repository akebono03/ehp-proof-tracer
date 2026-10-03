Phase157-R5-R3 repair1 — aggregate boundary correction

原因:
R5-R3 initial implementation added:
  finite_dimensional_aggregate
as a new fixed component to:
- Proposition 5.1
- Proposition 5.3
- Proposition 5.6
- Proposition 5.11

This was incorrect.

The aggregate ProofStep represents the whole fixed literature statement, but it is not
an additional component alongside the theorem's individual fixed statement components.

Consequences of the incorrect implementation:
- existing component inventories gained one extra component
- same-theorem component ordering included the synthetic aggregate
- R2/R4 contract tests failed

Repair:
1. Remove the four synthetic finite_dimensional_aggregate components.
2. Remove the four forced aggregate rule -> component mappings.
3. Preserve the existing behavior:
   aggregate step -> FIXED_STATEMENT with component_key=None.
4. Keep all R5-R3 fixed/internal classifications for the 13 UNTRACKED locators.
5. Update the R5-R3 lightweight test to expect None for aggregate component keys.

Changed files:
- toda_literature_statement_boundary.py
- tests/test_phase157_r5_r3_boundary_catalog_expansion.py

Import changes:
- none

Class changes:
- none

Function changes in production:
- none in this repair; only R5-R3 catalog data is corrected.

Tests:
- lightweight focused only
- no 112-group replay
- no full Narrative rendering
- no repository-wide pytest

Completion condition:
- existing R2/R4 component inventory tests pass again
- R5-R3 candidate classification test passes
