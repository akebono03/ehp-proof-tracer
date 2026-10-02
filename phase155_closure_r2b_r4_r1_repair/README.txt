Phase 155 Closure-R2B-R4-R1 — focused repair

Repairs the three issues exposed by the R2B-R4 focused verification:

1. Boundary test still expected 23 audit-only nodeids.
   It now checks the exact final two-nodeid set.

2. Phase42 lightweight replacement still took about 35 seconds because it
   built heavy `(8,7)` and `(9,7)` contexts.
   It now checks the deterministic production tie-break implementation
   directly in `_topological_order`.

3. Phase43-10 replacement still expected a literal rendered connector that is
   no longer present in the current Narrative.
   It now checks the underlying pi_6^3 production transport semantics:
   TRANSPORT role, Proposition 5.3 reference identity, and at least one
   SUSPENSION_STABILIZATION operation.

No production code changes.
No audit-only manifest changes.
No repository-wide pytest.
