Phase 144-6-R5-37
genuinely-missing semantic-equivalence and rendering audit

Production changes: none.

Purpose:
Refine the Phase-36 genuinely-missing population into:
1. semantic_equivalent_present
2. rendering_gap
3. visibility_gap

semantic_equivalent_present:
An equal conclusion statement occurs on another ProofStep whose current
generic single-step rendering is present in the final multi-Argument Narrative.

rendering_gap:
The missing necessary ProofStep currently renders only as its inference-rule
name or statement-type placeholder.

visibility_gap:
Neither exact-statement coverage nor renderer fallback explains the missing
necessary contribution.

This is deliberately conservative. Equality of conclusion statement objects
is used; the audit does not attempt unrestricted mathematical equivalence.

Boundary:
- no production frontier change;
- no renderer change;
- no ProofChain change;
- no ownership/dedup change;
- no expression-to-membership rule;
- no parity matcher change;
- no public route change;
- no dedicated pi_6^3 renderer removal.
