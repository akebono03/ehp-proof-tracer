Phase 148 RC2-4 Repair R5-R3
Six-group raw-exactness invariant repair

Conclusion from R5-R1 / R5-R2
------------------------------
The remaining generic "is exact" phrase in pi_10^4 and pi_12^5 is not the
normalized rendering of the TodaProp42ExactnessStatement ProofStep.

For both groups:
- exactness ProofStep exists in proof data,
- RC2 exposure classification is present,
- normalized raw exactness rendering is not visible,
- another Narrative sentence still contains "is exact".

Therefore the original six-group audit invariant was too broad. Counting the
phrase alone conflated raw exactness ProofStep exposure with other Narrative
prose.

R5-R3 change
------------
Production changes: none.

Audit-only test change:
tests/test_phase148_rc2_4_post_repair_six_group.py

The old condition:
- count all "is exact" phrases and require zero

is replaced by:
- enumerate actual TodaProp42ExactnessStatement ProofSteps,
- normalize each raw rendering exactly as the renderer does,
- require that none of those raw renderings appears in the final Web
  Narrative.

This matches the RC2 requirement and the existing Phase 148 R2 test contract.

GitHub develop re-inspection
----------------------------
Before this audit-test repair, the current develop source was re-inspected:
- toda_group_proof_narrative_argument_body_renderer.py
- toda_group_proof_narrative_exactness_exposure.py
- toda_group_proof_narrative_exactness_contribution_ownership.py
- toda_group_proof_narrative_method_evidence.py
- tests/test_phase148_rc2_4_repair_r2.py

In particular, the existing R2 contract already checks raw exactness by
normalizing actual TodaProp42ExactnessStatement rendering rather than by
counting every generic exactness phrase.

Completion criteria
-------------------
All six representative groups must satisfy:
1. bounded semantic closure remains smaller than complete replay where
   complete replay is deeper,
2. R4.2 semantic closure adds no exactness ProofStep,
3. no actual raw exactness ProofStep rendering is visible,
4. no AMBIGUOUS_RELEVANT exposure appears.

pi_6^3 must additionally retain:
- numbered equations (1), (2), (3),
- the (1)+(2) connector,
- the group conclusion,
- the derived short exact sequence.

Repository-wide pytest
----------------------
Not run. It remains reserved for RC2-5, the end of Phase 148.

Next boundary
-------------
If R5-R3 passes and all four printed audit invariants are True, RC2-4 is
complete. Proceed to RC2-5 final regression and documentation closure.
Narrative ordering remains Phase 149 / RC3.
