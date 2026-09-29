Phase 144-6-R5-15P
====================

Generic EvidenceContribution vocabulary extension.

Changed project files
---------------------
1. toda_group_proof_narrative_evidence_contributions.py
   - TodaGroupProofNarrativeEvidenceContribution
   - _contribution_for_premise_block

2. tests/test_phase144_6_r5_15p_evidence_contribution_vocabulary.py
   - new focused tests

Production mapping
------------------
EXACTNESS  -> ESTABLISH_EXACTNESS
DEFINITION -> ESTABLISH_DEFINITION
MEMBERSHIP -> ESTABLISH_MEMBERSHIP

The mapping uses only the existing generic mathematical block role.
It does not inspect statement class, n/k, or inference-rule name.

Boundary
--------
R4 visibility is unchanged.
Renderer, CLI, and Web are unchanged.
ProofStep, InferenceRule, and TodaProofEdge are unchanged.
No future visibility-selection policy is implemented.
The full pytest suite is deferred until the end of Phase 144.
