Phase 144-6-R5-22 missing 4 facts statement-structure audit.

Production changes: none.

This audit follows the four Phase 21 facts reported as
not_found_in_presentation by comparing the current pi_6^3 presentation against
canonical Phase 65 proof objects.

It classifies each fact as:
- exact_presentation_conclusion
- embedded_in_presentation_conclusion
- embedded_in_presentation_premise
- absent_from_presentation_closure

The comparison uses object equality and recursive dataclass/container field
containment rather than rendered-text matching.

The canonical objects are taken from the existing Phase 65 test builder:
- H(nu-prime)=eta_5
- H(nu-prime eta_6)=eta_5^2
- nu-prime eta_6 as the expression inside the latter relation
- the pi_7^5 group fact used by the same inference chain

No renderer, ProofChain, presentation, or public-route code is changed.
