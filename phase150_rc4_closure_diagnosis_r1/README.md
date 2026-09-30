# Phase 150 / RC4 Closure Diagnosis R1

Audit-only diagnostic package. No production code or existing tests are
changed.

The closure audit exposed an invariant violation while building the reason
sidecar for `pi_10^4`: at least one reason referenced a proof step that was
not present in the presentation nodes.

This package reconstructs each reason candidate before the sidecar validation
step and reports:

- reason kind;
- conclusion step identity, rule and conclusion;
- premise step identities, rules and conclusions;
- whether each step belongs to the presentation;
- the exact invalid reason kinds.

The purpose is to distinguish a semantic-dependency/presentation-boundary
case from a node-derived classifier bug before making any production change.

Repository-wide tests are intentionally deferred until the end of Phase 150.
