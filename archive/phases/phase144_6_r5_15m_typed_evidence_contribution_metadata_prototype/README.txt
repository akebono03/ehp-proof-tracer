Phase 144-6-R5-15M
====================

Typed evidence-contribution metadata prototype.

Production files added
----------------------
- toda_group_proof_narrative_evidence_contributions.py

Tests added
-----------
- tests/test_phase144_6_r5_15m_evidence_contributions.py

Existing files changed
----------------------
None.

Prototype boundary
------------------
This phase adds a separate Narrative semantic sidecar at premise-edge
granularity. It does not modify:
- ProofStep
- InferenceRule
- TodaProofEdge
- the existing Narrative semantic sidecar
- R4 production visibility
- renderers
- CLI
- Web

The first prototype classifies evidence from existing generic mathematical
block roles and RelationType. Statements that cannot be classified safely are
kept as UNRESOLVED. No inference-rule-name parsing and no n/k-specific rule is
used.

Focused tests only
------------------
The runner executes the new tests plus the directly related Phase 141
semantic/block tests. It does not run the full test suite because Phase 144 is
not complete.
