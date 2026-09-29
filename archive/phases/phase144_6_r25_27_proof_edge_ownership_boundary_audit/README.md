# Phase 144-6 R25-27 Proof-Edge Ownership Boundary Audit

## Purpose

R25-26 established that the oversized argument local-body closures are created
primarily by presentation proof edges, not semantic-sidecar dependencies.

R25-27 isolates every direct proof premise of the largest arguments and measures
the proof subtree owned by each premise separately.

## Production changes

None.

## Measurements

For each large argument, the audit reports:

- conclusion block role and statement types;
- direct proof-premise count;
- union closure size and EXACTNESS count;
- each direct premise block, role, and statement types;
- each premise subtree size;
- percentage of the argument closure covered by that premise;
- EXACTNESS count;
- blocks unique to that premise;
- role distribution;
- immediate child count;
- immediate hits on another argument conclusion boundary.

## Decision boundary

The audit distinguishes two cases:

1. one direct premise imports almost the entire oversized proof subtree;
2. the oversized closure appears only through the union of several premises.

The next production repair must be based on this result. This package does not
introduce a new ownership or suppression rule.

Repository-wide pytest remains deferred until the end of Phase 144-6.
