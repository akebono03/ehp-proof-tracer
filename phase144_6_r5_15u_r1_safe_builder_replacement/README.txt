Phase 144-6-R5-15U-R1
=======================

Safe builder replacement for 15U.

Cause of original 15U failure
-----------------------------
The original apply script obtained the builder AST line number before inserting
a new import. The import changed source line positions, but the stale line
number was then used for helper insertion. The generated source was invalid and
ast.parse failed.

Because the parse failed before write_text, the production file was not
modified. The later unexpected-keyword test failure was therefore secondary.

R1 strategy
-----------
R1 does not edit by stale AST line positions.

It validates the known 15P structure and replaces the complete builder region
from build_toda_group_proof_narrative_evidence_contribution_sidecar to EOF.

The existing _contribution_for_premise_block(block, edge) function is preserved.

Changed production file
-----------------------
toda_group_proof_narrative_evidence_contributions.py

New helper
----------
_aggregate_semantic_contribution_for_edge

Changed function
----------------
build_toda_group_proof_narrative_evidence_contribution_sidecar

New test
--------
tests/test_phase144_6_r5_15u_r1_evidence_integration.py

Boundary
--------
No change to R4 visibility, renderer, CLI, Web, proof core, Narrative depth
policy, or project documents.

No n/k production checks.
No inference-rule-name parsing.
No statement-class inspection in EvidenceContribution integration.

Focused pytest only.
Full pytest remains deferred until the end of Phase 144.
