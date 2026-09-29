Phase 144-6-R5-17E production ProofChain architecture decision audit.

Production code is unchanged.

Decision candidates:
1. evidence-first
   EvidenceContribution / raw evidence closure -> ProofChain -> Narrative
2. argument-first
   NarrativeArgument + semantic providers -> ProofChain -> Narrative

The audit checks six representative groups and uses the conclusions established
in 17A through 17D-R1:
- NarrativeArgument already owns direct supporting blocks and child Arguments.
- semantic-only direct support exists.
- child-Argument composition exists and must remain first-class.
- Argument local-body traversal stops at other Argument conclusions.
- all nine OTHER direct providers are already explained by aggregate or
  provenance-only semantic catalogs.
- no new mathematical block role is required for those OTHER providers.

The expected architecture decision is ARGUMENT_FIRST.

EvidenceContribution may remain useful as supporting annotation/classification
data, but it is not selected as the top-level Narrative skeleton.

No production ProofChain class is introduced and no renderer is changed.
