Phase 159 R1-7c R4 numbered map-property reasoning repair1

Purpose
-------
Normalize existing public proof-body reasoning of the form:

  map is injective
  map is surjective
  map is isomorphism

into:

  map\tag{n} is injective
  map\tag{m} is surjective
  (n), (m) より, map は同型.

Scope
-----
This repair formats only an isomorphism conclusion that already exists in the
public Narrative for the exact same normalized map.

It does NOT infer a new isomorphism.

Therefore the current Delta pairs in pi_9^3 and pi_10^3 remain unchanged:
they have injective and surjective statements, but no semantic/public
isomorphism conclusion.

The repair also preserves already-numbered reasoning such as pi_3^2.

Production change
-----------------
toda_group_proof_narrative_renderer.py

New helper:
  _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning

Changed function:
  render_toda_group_proof_narrative_markdown

Imports:
  no import changes

Test
----
New:
  tests/test_phase159_r1_7c_r4_map_property_numbered_reasoning_repair1.py

No semantic inference-rule changes.
No Delta isomorphism rule.
No Reference changes.
No eta_2 wording changes.
No stable-range changes.
No full pytest.
