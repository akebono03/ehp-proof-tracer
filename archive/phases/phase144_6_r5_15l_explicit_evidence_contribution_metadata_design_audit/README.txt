Phase 144-6-R5-15L
====================

Design audit only.

Purpose
-------
R5-15K showed that 107 of 109 visible residual SUPPORT_ONLY edges can be
described by an evidence-contribution category, but contribution + consumer
purpose + structural overlap still leaves mixed visible/hidden collisions.

15L does not add another graph heuristic. It compares where explicit typed
evidence-contribution metadata should live.

Candidates
----------
1. ProofStep
2. InferenceRule premise metadata
3. TodaProofEdge
4. TodaGroupProofNarrativePremiseSemantic / Narrative semantic sidecar

Questions
---------
- Is the metadata node-specific or edge-specific?
- Is it proof-core semantics or Narrative-only semantics?
- Does the location require broad producer/rule changes?
- Is the location authoritative or reconstructed?
- Does an existing validation mechanism already fit it?
- What is the compatibility surface in existing tests?

Expected design boundary
------------------------
This audit only selects a storage layer and granularity.
It does not implement contribution metadata.
It does not change production Narrative visibility.
It does not change tests or project documents.
No pytest is required because production code is unchanged.
