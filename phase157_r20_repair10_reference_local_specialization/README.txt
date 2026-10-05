Phase157-R20 repair10

Purpose
-------
Use the semantic-closure proof graph to render only the concrete fixed
literature statement needed by an external proof consumer.

Audit evidence
--------------
After semantic closure, Proposition 5.3, Proposition 5.1, and Proposition 2.2
all exist in the Reference pipeline.

The defect is statement selection:
- Proposition 5.3 exposes pi_5^3 plus the whole symbolic aggregate;
- Proposition 5.1 exposes the whole symbolic aggregate;
- Proposition 2.2's generic fixed statement is malformed as `lpha` / `eta`.

Generic repair
--------------
1. Reference-local specialization only:
   - inspect symbolic TodaPrimaryGroup relations in an aggregate;
   - inspect concrete TodaPrimaryGroup occurrences in descendants;
   - bind exactly one ScalarSymbol when the group dimensions match;
   - honor a matching ScalarGreaterEqualStatement range;
   - accept the specialization only when it is unique.

2. When one aggregate specialization is uniquely relevant, use only that
   aggregate step for the public Reference statement.

3. Body Reference markers use the same specialized public statement.

4. The fixed component key `hopf_right_composition_formula` renders canonically
   as:
     H(alpha o E beta) = H(alpha) o E beta.

Scope
-----
This is not a general theorem substitution engine. The substitution helper is
private to Reference rendering and handles only the scalar forms needed here.

Changed files
-------------
- toda_group_proof_narrative_contribution_renderer.py
- tests/test_phase157_r20_repair10_reference_local_specialization.py

No pi_6^3-specific branch.
No documentation changes.
No repository-wide pytest.
