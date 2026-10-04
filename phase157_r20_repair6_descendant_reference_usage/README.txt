Phase157-R20 repair6

Purpose
-------
Recover fixed literature References through generic descendant usage.

Problem
-------
The existing restoration rule only kept a fixed literature Reference when the
exact Reference-owned ProofStep ID was present in `used_step_ids`.

That is too strict for real proof graphs such as:

  fixed literature statement
      -> specialization / integration
      -> map-property proof

The visible proof uses the descendant, not necessarily the exact fixed
statement node.

Generic repair
--------------
`restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage()`
now follows `presentation.edges` forward from each fixed Reference-owned step.

A Reference is retained when a path reaches:
- the root step, or
- a used non-Reference-internal step.

The traversal is independent of proposition number, group dimension, sphere
dimension, and generator name.

The renderer also removes the redundant second body-usage filter after
Reference restoration. Otherwise a graph-restored Reference could immediately
be deleted again merely because the body did not already contain its marker.

Changed files
-------------
- toda_group_proof_narrative_references.py
  - restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage()
- toda_group_proof_narrative_contribution_renderer.py
  - render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()
    (remove redundant post-restore body filter)
- tests/test_phase157_r20_repair6_descendant_reference_usage.py (new)

No pi_6^3-specific branch is added.
No documentation changes.
No repository-wide pytest.
