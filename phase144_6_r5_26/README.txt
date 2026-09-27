Phase 144-6-R5-26
step-level deduplication + derivation-path relevance audit

Production changes: none.

Audit A:
Across the six representative groups, compare the current block-identity
deduplication with a hypothetical visible-step-identity deduplication.
Only non-EXACTNESS blocks are measured. No renderer is changed.

Audit B:
For the four pi_6^3 frontier-hidden facts, measure whether each fact lies on
a reverse premise path from each NarrativeArgument conclusion. Report both:
- raw presentation-edge paths;
- paths augmented by the existing semantic dependency sidecar.

This tests whether derivation-path relevance can explain visibility better
than coarse statement/block signatures.

Boundary:
- no deduplication implementation change;
- no frontier implementation change;
- no ProofChain change;
- no embedded expression-to-membership rule;
- no public route change;
- no dedicated pi_6^3 renderer removal.
