Phase 144-6-R5-18 production Generic ProofChain foundation.

Production change:
- add toda_group_proof_narrative_proof_chains.py

The new production representation is Argument-first:
NarrativeArgument + semantic providers -> ProofChain.

ProofChain preserves:
- one chain per NarrativeArgument
- supporting-block provider identity and order
- child-Argument provider indices and order
- aggregate semantic kinds as provider annotations

It does not:
- change Narrative rendering
- remove or bypass the pi_6^3 legacy renderer
- use EvidenceContribution as the top-level skeleton
- recursively expand providers
- introduce new mathematical block roles

Run only the targeted Phase 18 tests. The whole suite remains reserved for the
end of the Phase.
