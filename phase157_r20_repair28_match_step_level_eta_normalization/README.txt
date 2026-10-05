Phase157-R20 repair28

Purpose
-------
Make the rendered-reflexive equality helper use the same eta-family
normalization that the public generic step renderer uses.

repair27 finding
----------------
For the target step:
- expression-level lhs normalization:
  eta_3 eta_4 eta_5
- expression-level rhs normalization:
  eta_3^3
- public rendered step:
  eta_3^3 = eta_3^3

The difference is `_normalize_generic_eta_family_latex()`, which runs during
generic statement rendering and compresses consecutive eta-family factors.

Generic repair
--------------
After `_render_generic_narrative_expression_latex()`:
- apply `_normalize_generic_eta_family_latex()` to lhs;
- apply `_normalize_generic_eta_family_latex()` to rhs;
- compare the two final public-display-normalized sides.

The two repair26 filter locations remain unchanged:
- display_steps;
- relocated_direct_premises.

Changed production file
-----------------------
- toda_group_proof_narrative_argument_body_renderer.py

Import change
-------------
Add:
- `_normalize_generic_eta_family_latex`

Changed helper
--------------
- `_is_toda_group_proof_narrative_rendered_reflexive_equality_step()`

New test
--------
- tests/test_phase157_r20_repair28_match_step_level_eta_normalization.py

No documentation changes.
No repository-wide pytest.
