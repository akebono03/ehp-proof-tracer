Phase157-R20 repair22

Purpose
-------
Suppress equality steps that become reflexive only after generic expression
normalization.

Audit evidence
--------------
repair21 identified:
- eta_3^3 = eta_3^3
  from `equality preserved under left composition`;
- eta_5 = eta_5
  from the source relation E^2 eta_3 = eta_5.

Both source proof steps are structurally meaningful, but their public generic
rendering becomes lhs == rhs.

Generic rule
------------
At argument-body display-step selection:
1. require an equality Relation;
2. verify both sides are generically renderable;
3. normalize lhs and rhs with the same generic expression normalization used by
   public rendering;
4. if normalized lhs == normalized rhs, keep the proof step in the graph but do
   not display it in the argument body.

Changed production file
-----------------------
- toda_group_proof_narrative_argument_body_renderer.py

Changed imports
---------------
- from toda_group_proof_generic_narrative_renderer:
  add `_render_generic_narrative_expression_latex`
  and `_try_render_generic_narrative_expression_latex`
- from proof:
  add `Relation` and `RelationType`

New helper
----------
- `_is_toda_group_proof_narrative_rendered_reflexive_equality_step()`
  inserted immediately before
  `render_toda_group_proof_narrative_argument_body_markdown()`.

New test
--------
- tests/test_phase157_r20_repair22_hide_rendered_reflexive_steps.py

Phase boundary
--------------
This repair only removes rendered-reflexive display steps.
It does not yet perform the remaining Phase157 prose de-duplication or complete
the explicit eta_3^3 nonzero/order reasoning.

Repository-wide pytest is not run.
