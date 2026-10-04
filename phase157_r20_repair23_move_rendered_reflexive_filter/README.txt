Phase157-R20 repair23

Purpose
-------
Correct the placement mistake in repair22.

Cause
-----
repair22 used a first-match text replacement. The filter expression intended
for `display_steps` matched an earlier comprehension in
`relocated_direct_premises` first.

Therefore:
- the generic rendered-reflexive helper was added correctly;
- but argument-body display-step selection never called it;
- eta_3^3 = eta_3^3 and eta_5 = eta_5 remained visible.

Repair
------
1. Remove the accidental helper call from the relocated-direct-premise
   comprehension.
2. Add the helper call only to the `display_steps = tuple(...)` selection in
   `render_toda_group_proof_narrative_argument_body_markdown()`.

Changed production file
-----------------------
- toda_group_proof_narrative_argument_body_renderer.py

Changed function
----------------
- render_toda_group_proof_narrative_argument_body_markdown()
  Only the display-step predicate changes.

Existing helper retained
------------------------
- _is_toda_group_proof_narrative_rendered_reflexive_equality_step()

New test
--------
- tests/test_phase157_r20_repair23_move_rendered_reflexive_filter.py

No documentation changes.
No repository-wide pytest.
