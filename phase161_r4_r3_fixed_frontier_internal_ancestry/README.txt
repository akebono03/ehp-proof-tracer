Phase 161-R4-R3
fixed-statement frontier internal ancestry

Confirmed by R4-R2 audit
========================
For pi_4^2:

- `(5.2)` fixed statement:
  frontier=True, owned=True, internal=False
- Proposition 4.4:
  frontier=False, owned=True, internal=False
- Proposition 4.4 second-summand restriction:
  frontier=False, owned=False, internal=False

The specialization plan is valid and the final body already contains:

  [R1] applied at i=4
  eta_2 o - : pi_4^3 -> pi_4^2 is an isomorphism

Therefore the remaining defect is not specialization.
It is internal-ancestry suppression.

Rule
====
A FIXED_STATEMENT on the public Reference frontier is the visible literature
boundary.

Proof steps upstream of that fixed statement are internal to the fixed
literature result when all of their visible consumers remain inside that fixed
statement's dependency closure.

This includes explicitly referenced steps such as Proposition 4.4 when they
are used only to prove the fixed `(5.2)` statement.

Shared steps with consumers outside that closure are not suppressed.

Files
=====
Modified:
- toda_group_proof_narrative_contribution_renderer.py
- tests/test_phase161_r4_pi4_2_specialization_frontier.py
- tests/test_phase161_r4_repair1_pi4_2_semantic_frontier.py

New:
- tests/test_phase161_r4_r3_fixed_frontier_internal_ancestry.py

Imports
=======
No production import changes.

Test expectation refinement
===========================
The R4-R2 audit proved that the specialized sentence is present.
The old tests compared the entire prose sentence literally.

R4-R3 instead checks semantic display components:
- [R1]
- i=4
- pi_4^3 -> pi_4^2
- isomorphism

This follows the project policy of semantic comparison instead of prose
comparison where possible.

Completion criteria
===================
- `(5.2)` remains the sole public literature boundary for this transport.
- Proposition 4.4 is absent from Reference.
- Proposition 4.4 general decomposition prose is absent from body.
- second-summand restriction prose is absent from body.
- specialized i=4 map remains.
- pi_4^3 source group, generator transport, target conclusion, and QED remain.
- focused regressions pass.

Full suite is not run until the end of Phase 161.
