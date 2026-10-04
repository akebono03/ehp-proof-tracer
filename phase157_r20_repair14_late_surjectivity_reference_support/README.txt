Phase157-R20 repair14

Purpose
-------
Run surjectivity Reference support only after all late dependency insertions.

Runtime audit result
--------------------
At the original surjectivity-support call:
- H:pi_7^3 -> pi_7^5 surjective is not yet present.
- only H:pi_6^3 -> pi_6^5 surjective is visible.

Later dependency insertion creates the pi_7^3 -> pi_7^5 map-property paragraph.
By body-filter time it is incorrectly prefixed with [R1], while Proposition 5.3
has no marker and is therefore removed.

Generic repair
--------------
1. Move order_toda_group_proof_narrative_surjectivity_support() from its early
   position to immediately after late unmarked-Reference linking.

2. When the late support pass sees a surjective H map-property paragraph, strip
   any pre-existing direct Reference prefix from the map-property itself.

3. Use the map target group to find the unique selected public Reference
   statement `target_group = ...` and place that statement immediately before
   the surjectivity conclusion.

For the current regression target this yields:
  [R3]より, pi_7^5 = Z/2{eta_5^2}
  H: pi_7^3 -> pi_7^5 は全射である.

The rule does not inspect proposition number, generator name, n=3, or pi_6^3.

Changed files
-------------
- toda_group_proof_narrative_contribution_renderer.py
  - order_toda_group_proof_narrative_surjectivity_support()
  - call order in render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()
- tests/test_phase157_r20_repair14_late_surjectivity_reference_support.py

No documentation changes.
No repository-wide pytest.
