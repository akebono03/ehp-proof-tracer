Phase157-R20 repair12

Purpose
-------
Fix the exact runtime defect found by repair11.

Audit result
------------
- Proposition 5.3 is correctly selected as:
    pi_7^5 = Z/2{eta_5^2}
- it is removed only because the proof body has no [R3] marker;
- restore brings R3 back, but the second body-usage filter removes it again;
- H:pi_7^3->pi_7^5 surjective is incorrectly attributed to [R1].

Generic repair
--------------
1. Unmarked Reference linking no longer assigns a literature Reference
   directly to a MAP_PROPERTY consumer. Map properties must be supported by
   their actual dependency statements.

2. Surjectivity support receives the already-selected public Reference
   statement lines. For a visible
       H: A -> B is surjective
   it searches for exactly one public Reference statement beginning with
       B = ...
   and inserts
       [Rk]より, B = ...
   immediately before the map-property statement.

This is driven only by the map target group and selected Reference statements.
No proposition number, generator, or pi_6^3 target is hard-coded.

Changed files
-------------
- toda_group_proof_narrative_contribution_renderer.py
  - link_toda_group_proof_narrative_unmarked_reference_consumers()
  - order_toda_group_proof_narrative_surjectivity_support()
  - call site in render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()
- tests/test_phase157_r20_repair12_map_property_reference_support.py (new)

No documentation changes.
No repository-wide pytest.
