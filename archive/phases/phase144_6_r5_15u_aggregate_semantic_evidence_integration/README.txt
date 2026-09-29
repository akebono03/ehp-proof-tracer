Phase 144-6-R5-15U
====================

Aggregate semantic metadata -> EvidenceContribution integration.

Changed production file
-----------------------
toda_group_proof_narrative_evidence_contributions.py

Changed function
----------------
build_toda_group_proof_narrative_evidence_contribution_sidecar

New private helper
------------------
_aggregate_semantic_contribution_for_edge

New test
--------
tests/test_phase144_6_r5_15u_evidence_integration.py

Integration
-----------
The builder receives an optional aggregate semantic sidecar.

For a premise carrying explicit aggregate semantic metadata:
- consumer TARGET -> ESTABLISH_GROUP
- consumer DEFINITION -> ESTABLISH_DEFINITION

If aggregate metadata does not apply, the existing premise-block mapper remains
the fallback.

Existing callers remain valid because the new sidecar parameter is optional.

Boundary
--------
No n/k checks.
No inference-rule-name parsing.
No statement-class inspection in EvidenceContribution integration.
No production field-name inference.

Not changed:
- R4 visibility
- renderer
- CLI
- Web
- proof core
- Narrative depth policy
- project documents

Focused pytest only. Full pytest remains deferred until the end of Phase 144.

Completion condition
--------------------
Across the six representative groups:
edge-local visible unresolved EvidenceContribution edges = 0.

Next Phase boundary
-------------------
After 15U succeeds, return to the R5 depth/relevance objective and use typed
contribution metadata to design Narrative evidence selection. Do not modify
depth policy in 15U.
