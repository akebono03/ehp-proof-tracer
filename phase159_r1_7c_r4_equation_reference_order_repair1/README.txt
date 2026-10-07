Phase 159 R1-7c R4 equation-reference order repair1

Purpose
-------
Fix the confirmed public proof-order defect where an equation-reference
conclusion appears before the equations it cites.

Confirmed defect:
  pi_5^3

Current order:
  (1), (2) より, E は同型.
  ...
  E\tag{1} は単射.
  ...
  E\tag{2} は全射.

Desired order:
  E\tag{1} は単射.
  ...
  E\tag{2} は全射.
  (1), (2) より, E は同型.

General rule
------------
In the final public proof body:

- detect a conclusion paragraph beginning with equation references;
- locate every referenced \tag{n} paragraph;
- if the conclusion occurs before any referenced paragraph, move only that
  conclusion paragraph to immediately after the last referenced paragraph;
- if all referenced paragraphs are already earlier, leave the proof unchanged;
- if any referenced tag is missing, leave the proof unchanged.

This is independent of group identity and map name.

Production change
-----------------
toda_group_proof_narrative_renderer.py

New helper:
  _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions

Changed function:
  render_toda_group_proof_narrative_markdown

Imports:
  no import changes

Test
----
New:
  tests/test_phase159_r1_7c_r4_equation_reference_order_repair1.py

No semantic inference changes.
No Reference changes.
No Delta isomorphism rule.
No eta_2 wording changes.
No full pytest.
