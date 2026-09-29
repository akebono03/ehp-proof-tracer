# Phase 144-6 R25-28 Proof-Edge Fan-Out / Block Aggregation Audit

## Purpose

R25-27 showed that a single direct proof premise can reach almost the entire
proof graph for several representative groups.

R25-28 tests whether NarrativeBlock aggregation is artificially increasing
proof connectivity.

`build_toda_group_proof_narrative_blocks` groups same-role ProofSteps into
connected components. A block-level dependency graph can therefore connect an
incoming edge to dependencies of a different step in the same block.

## Production changes

None.

## Audit

For the largest arguments and direct premise blocks, R25-28 compares:

- block-level proof closure;
- step-level closure starting only from the actual premise entry steps;
- step-level closure starting from every step contained in the premise block;
- projected block counts for both step-level closures;
- blocks reachable only through block aggregation;
- EXACTNESS counts and role distribution of aggregation-only blocks;
- direct child block fan-out and each child's closure size.

## Interpretation

A large difference between block closure and entry-step projected closure is
evidence that block aggregation is introducing artificial connectivity.

If both are already similarly large, the underlying step-level proof graph is
itself highly connected and the next repair must not target block aggregation.

## Validation

The runner executes focused audit-contract tests and the existing Phase 143
argument-local-body regression tests before the six-group audit.

Repository-wide pytest remains deferred until the end of Phase 144-6.
