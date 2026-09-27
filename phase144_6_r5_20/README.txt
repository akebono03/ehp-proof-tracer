Phase 144-6-R5-20 pi_6^3 dedicated <-> ProofChain generic Narrative parity audit.

Production changes: none.

This audit freezes the existing dedicated pi_6^3 Narrative as the reference
quality specification and checks the ProofChain generic Narrative against
mathematical, ordering, discourse, and structural requirements.

The audit intentionally does not require literal string equality. Literal
equality would encourage copying pi_6^3-specific prose into the generic
renderer. Instead, missing requirements are reported and must later be solved
by generic ProofChain/Narrative rules.

This phase does not:
- change the public Narrative route
- remove or bypass the dedicated pi_6^3 renderer
- add pi_6^3-specific branches to the generic renderer
- claim parity when requirements remain missing

If semantic_parity_ready=False, the next work is to resolve each missing item
through general rules. If semantic_parity_ready=True, route replacement and
dedicated-renderer removal safety can be audited next.
