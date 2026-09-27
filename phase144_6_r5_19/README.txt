Phase 144-6-R5-19 Generic ProofChain -> Narrative integration.

Production change:
- add toda_group_proof_narrative_proof_chain_renderer.py

The new production entrypoint requires and validates one ProofChain for every
NarrativeArgument, then delegates to the existing generic multi-Argument
renderer.

This is intentionally a narrow integration phase. It proves that ProofChain can
sit on the production Narrative path without changing current generic output.

It does not:
- change local-body selection from Argument traversal to ProofChain providers
- change the public Narrative route
- remove or bypass the dedicated pi_6^3 renderer
- claim parity between the dedicated pi_6^3 renderer and generic Narrative
- recursively expand ProofChain providers

Phase 20 remains responsible for parity and route-replacement decisions.
