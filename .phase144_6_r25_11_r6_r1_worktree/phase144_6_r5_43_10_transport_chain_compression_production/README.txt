Phase 144-6-R5-43-10 transport-chain compression production connection

Production changes:
1. toda_group_proof_narrative_hidden_bridge_semantics.py
   - Preserve the existing role classifier API.
   - Add reference_identity metadata.
   - Add operation_kind metadata for suspension stabilization.
2. toda_group_proof_narrative_contribution_renderer.py
   - Detect the audited 3-step hidden TRANSPORT chain through the Proof graph.
   - Read production semantic metadata, not inference-rule strings.
   - Render:
     Proposition 5.3 を順次適用し、suspension による安定化を用いると、
   - Preserve the existing direct dependency connector: これより、

Tests:
- New R5-43-10 focused tests.
- R5-43-7 semantic regression.
- R5-43-4 direct connector regression.

Boundaries:
- No pi_6^3-specific renderer branch.
- No public CLI/Web route switch.
- No integration-provenance prose change.
- No full test suite.
- R5-43-11 remains the cross-group connected Narrative completion audit.
