Phase 144-6-R5-43-7 hidden bridge semantic classification foundation

Production changes:
- Add toda_group_proof_narrative_hidden_bridge_semantics.py

Production API:
- TodaGroupProofNarrativeHiddenBridgeSemanticRole
- TodaGroupProofNarrativeHiddenBridgeSemantic
- classify_toda_group_proof_narrative_hidden_bridge_step
- build_toda_group_proof_narrative_hidden_bridge_semantics

Scope:
- Promote the four stable R5-43-6 signatures into two production semantic roles:
  TRANSPORT and INTEGRATION_PROVENANCE.
- Keep the existing narrative semantic sidecar API unchanged.
- Do not connect the new semantics to any renderer.
- Do not change contribution selection, ordering, placement, connectors, CLI, Web,
  or public renderer routing.

Tests:
- Reproduce all 64 R5-43-6 hidden bridge occurrences by signature.
- Reproduce the 48 transport / 16 integration-provenance split.
- Verify deterministic presentation order.
- Verify no audit import from production.
- Verify renderer remains disconnected.

No full test suite is run.
