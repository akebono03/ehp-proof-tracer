Phase 144-6-R5-35
hidden anchored contribution necessity audit

Production changes: none.

Purpose:
Measure whether hidden steps on provider-anchored contribution chains are
structurally necessary for a direct SUPPORTING_BLOCK provider anchor to
reach the NarrativeArgument conclusion.

Necessity criterion:
For each currently reachable provider anchor, remove one hidden chain step.
The hidden step is structurally necessary when that removal destroys all
remaining anchor-to-conclusion paths for at least one provider anchor.

Direct anchors are not declared necessary merely because deleting the anchor
deletes its own path. This audit focuses on intermediary explanatory
necessity rather than tautological anchor self-necessity.

The audit reports:
- the four pi_6^3 genuine visibility gaps;
- six-group hidden-anchored population;
- necessary versus nonnecessary counts;
- semantic distribution of necessary hidden steps;
- Argument/block/statement classifications.

Boundary:
- no production frontier change;
- no renderer change;
- no ProofChain change;
- no ownership/dedup change;
- no expression-to-membership rule;
- no parity matcher change;
- no public route change;
- no dedicated pi_6^3 renderer removal.
