Phase157-R20 repair30

Purpose
-------
Apply public-display normalization to the final reflexive-equality suppression
stage.

Finding from repair29
---------------------
The eta_5 bridge proof step is correctly classified as rendered-reflexive by
the argument-body helper, but eta_5 = eta_5 is present again before
`insert_toda_group_proof_narrative_adjacent_eta_suspension_bridges()` and
survives the existing final suppression.

The existing suppression only checks:
  statement.lhs == statement.rhs

That misses proof steps whose source expressions differ but whose public
generic rendering becomes reflexive.

Generic repair
--------------
For every equality Relation in the presentation:
1. render lhs and rhs with the generic expression renderer;
2. apply the same eta-family normalization used by the public renderer;
3. if normalized lhs == normalized rhs, add the rendered step key to the
   suppression set;
4. remove matching public paragraphs.

This does not inspect rule names, generators, group dimensions, or pi_6^3.

Changed production file
-----------------------
- toda_group_proof_narrative_contribution_renderer.py

Import change
-------------
Add:
- `_render_generic_narrative_expression_latex`

Changed function
----------------
- suppress_toda_group_proof_narrative_reflexive_equalities()

New test
--------
- tests/test_phase157_r20_repair30_final_reflexive_suppression.py

Phase boundary
--------------
This repair only closes rendered-reflexive equality leakage.
It does not address the remaining prose ordering, duplication, or explicit
eta_3^3 nonzero/order reasoning.

Repository-wide pytest is not run.
