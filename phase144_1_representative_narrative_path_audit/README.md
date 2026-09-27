# Phase 144-1 Representative Narrative Generation Path Audit

This package performs an audit only. It does not modify EHP Proof Tracer production code or tests.

Targets:

- pi_6^3: n=3, k=3
- pi_8^5: n=5, k=3
- pi_10^4: n=4, k=6
- pi_12^5: n=5, k=7
- pi_15^8: n=8, k=7
- pi_16^9: n=9, k=7

For every target it prints:

- root proof rule
- presentation node/edge counts
- block count and block-role inventory
- argument count and argument-role inventory
- root argument indices
- arguments reachable from the final target
- ordered/source argument indices
- conclusion block role
- discourse role
- root reachability
- purpose subject
- supporting block count
- child argument indices
- detached argument count
- final multi-argument Narrative

Purpose:

Determine the first layer at which the representative proofs structurally diverge:

Proof graph -> semantic sidecar -> Blocks -> Arguments -> dependency/order/discourse -> renderer

Phase 144-1 is complete when the output is sufficient to explain why pi_6^3 forms a coherent Narrative and where the other representative proofs differ.

No production implementation belongs to Phase 144-1.
