Phase 159 R1-7c R4 map-property "である" repair1

Purpose
-------
Normalize confirmed public proof-body map-property prose:

  は単射である. -> は単射.
  は全射である. -> は全射.

Design
------
Do not change the internal renderer contracts used by:
- contribution ordering;
- trimming;
- dependency matching;
- reference-value insertion.

Instead, normalize only the final public Narrative proof body after the
Phase158 public-shell contract is assembled.

Reference sections are intentionally left unchanged.

Production change
-----------------
toda_group_proof_narrative_renderer.py

New helper:
  _phase159_r1_7c_r4_normalize_public_map_property_prose

Changed function:
  render_toda_group_proof_narrative_markdown

Test
----
New:
  tests/test_phase159_r1_7c_r4_map_property_dearu_public_normalization.py

No eta_2 wording changes.
No Reference semantic changes.
No exact-sequence changes.
No stable-range changes.
No full pytest.
