Phase157-R20 repair47

Purpose
-------
Expose the missing mathematical reason for an exact-order conclusion that is
derived from:
1. a finite cyclic source group with a known generator and order;
2. an injective suspension map from that source group.

repair46 finding
----------------
For ord(eta_3^3)=2:
- aggregate semantic: none
- reason: none
- direct premises:
  - pi_5^2 = Z/2{eta_2^3}
  - E: pi_5^2 -> pi_6^3 is injective

The proof graph is sufficient; only reason prose is missing.

Changed production files
------------------------
1. toda_group_proof_narrative_reasons.py
   - TodaGroupProofNarrativeReasonKind
   - new _injective_image_order_reason()
   - build_toda_group_proof_narrative_reason_sidecar()

2. toda_group_proof_narrative_reason_renderer.py
   - render_toda_group_proof_narrative_reason_sentence()

Import changes
--------------
None.

Generic rule
------------
Build INJECTIVE_IMAGE_ORDER when:
- conclusion is RelationType.ORDER;
- exactly one finite-cyclic group equality premise is compatible;
- exactly one TodaSuspensionInjectiveStatement has that group as source;
- the finite cyclic group order equals the target exact order.

Public reason prose
-------------------
The reason states that the generator image under injective E is nonzero and
that an injective map preserves the element's exact order. The conclusion
itself remains the existing ORDER statement.

No pi_6^3, eta_3, nu-prime, or phase-specific target condition is used.

New focused test
----------------
- tests/test_phase157_r20_repair47_injective_image_order_reason.py

Completion conditions
---------------------
- the new reason is built from the existing two premises;
- E(eta_2^3)=eta_3^3 != 0 appears before ord(eta_3^3)=2;
- the existing multiple-relation-to-order reason for nu' remains;
- repair42-45 focused contracts remain passing;
- Phase157 Narrative and Phase156 Reference regressions remain passing.

No documentation changes.
No repository-wide pytest.
