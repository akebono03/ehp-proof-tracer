Phase 144-6-R5-39
explanatory contribution narrative-necessity audit

Production changes: none.

Purpose:
Classify the 194 Phase-38 explanatory contribution groups into structural
Narrative-role candidates without changing production display behavior.

Candidate roles:
- explicit_prerequisite_candidate:
  the diagnostic owner is a direct provider anchor.
- bridge_candidate:
  the owner is not an anchor, but its ProofStep reaches another visibility
  contribution in the same Argument.
- derivation_detail_candidate:
  neither of the above.

For pi_6^3 only, the dedicated Narrative is used as a comparison baseline by
checking whether the owner's current generic single-step rendering occurs in
the dedicated Narrative. This comparison does not define a generic rule.

Boundary:
- no production visibility rule;
- no production ownership rule;
- no renderer change;
- no ProofChain change;
- no production deduplication change;
- no expression-to-membership rule;
- no parity matcher change;
- no public route change;
- no dedicated pi_6^3 renderer removal.
