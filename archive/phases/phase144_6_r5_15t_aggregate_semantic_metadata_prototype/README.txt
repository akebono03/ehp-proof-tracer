Phase 144-6-R5-15T
====================

Aggregate semantic metadata prototype.

Changed files
-------------
New:
1. toda_group_proof_narrative_aggregate_semantics.py
2. tests/test_phase144_6_r5_15t_aggregate_semantics.py

Package-only:
3. audit_phase144_6_r5_15t.py
4. apply_phase144_6_r5_15t.py
5. run_phase144_6_r5_15t.ps1

No existing production file is modified.

Prototype model
---------------
Statement meaning:
  ProofStep
  -> explicit AggregateSemanticKind metadata

Consumer-specific use:
  AggregateSemanticKind
  + consumer MathematicalBlockRole
  + consumer ArgumentRole
  -> candidate EvidenceContribution

Semantic vocabulary:
- GROUP_ORDER_TRANSPORT
- MAP_TRANSPORT
- GROUP_DECOMPOSITION_TRANSPORT
- RELATION_AGGREGATE

Important boundary
------------------
Statement classes are used only at the explicit metadata registration boundary.
The 9-edge contribution candidate classifier does not inspect statement classes,
n/k values, inference-rule names, or statement field names.

This Phase does NOT connect aggregate metadata to the production
EvidenceContribution mapper.

This Phase does NOT change:
- existing Narrative semantic sidecar,
- MathematicalBlockRole,
- R4 visibility,
- renderer,
- CLI,
- Web,
- proof core,
- project documents.

Completion condition
--------------------
- focused tests pass,
- exactly 9 edge-local visible unresolved edges are found,
- all 9 have explicit aggregate semantic metadata,
- all 9 receive exactly one candidate contribution using metadata plus consumer
  block/Argument purpose,
- no full pytest is run.

Next boundary
-------------
Only after 15T proves 9/9 classification should a later Phase consider
production integration with EvidenceContribution.

Full pytest remains deferred until the end of Phase 144.
