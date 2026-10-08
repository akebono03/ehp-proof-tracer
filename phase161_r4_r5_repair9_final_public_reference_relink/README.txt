Phase 161-R4-R5 repair9
Final public Reference-body relink

Established facts
=================
The previous audits proved:

1. Proposition 5.1 has the correct fixed general statement.
2. The proof graph is correct:
     Prop.5.1 general -> pi_4^3 specialization -> pi_4^2.
3. The graph-backed consumer search returns pi_4^3.
4. The linkage helper directly transforms:
     [R3] general Prop.5.1
   into:
     [R3] pi_4^3.
5. The final public render still displays the general statement in the body.
6. Reference filtering/restoration changes the final public numbering:
     internal R3 -> public R2.

Repair
======
Do not modify the helper again.

After all of the following are complete:
- body-usage filtering
- fixed-reference restoration
- second body-usage filtering
- final reference pruning
- final ordering

run the existing graph-backed:

  link_toda_group_proof_narrative_reference_body_consumers()

one final time using the final public reference entries and final public body.

This makes the linkage operate on the same numbering and body that will actually
be emitted to the user.

Files
=====
Modified:
- toda_group_proof_narrative_contribution_renderer.py
  - render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()

New:
- tests/test_phase161_r4_r5_repair9_final_public_reference_relink.py

Imports
=======
No production import changes.

Expected final public form
==========================
Reference:
- R1: Toda (5.2)
- R2: Proposition 5.1 general higher-eta group relation

Body:
- [R2]より, pi_4^3 = Z/2{eta_3}.
- [R1]を i=4 に適用すると, eta_2 o -: pi_4^3 -> pi_4^2 は同型.
- eta_3 -> eta_2 eta_3.
- pi_4^2 = Z/2{eta_2^2}.
- QED

No full test suite is run.
