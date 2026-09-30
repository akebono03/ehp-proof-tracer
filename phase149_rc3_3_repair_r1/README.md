# Phase 149 RC3-3 Repair R1

This repair corrects the first RC3-3 minimal implementation without expanding Phase scope.

## Diagnosed cause

`extract_toda_group_proof_narrative_argument_local_body_blocks()` places the Argument conclusion last, but the multi-Argument renderer later merges local-body blocks and method-evidence blocks in global block order.

For `pi_6^3`, the TARGET conclusion block therefore appears before the OWNED_PRIMARY EXACTNESS block during body rendering. The first RC3-3 implementation deferred exactness only after encountering that exactness block, which was too late to insert it before the already-rendered conclusion.

## Repair

Before the body loop:

1. Collect visible `OWNED_PRIMARY` exactness display lines using the existing RC2 renderer and filter.
2. Suppress those lines at their original exactness-block location.
3. Insert the collected lines immediately before the owning Argument conclusion block.
4. Preserve the existing end fallback only when no conclusion insertion point is available.

## Scope boundary

No changes are made to:

- RC2 ownership or exposure classification
- exactness component construction
- proof graph
- Argument ordering
- step-transition types
- existing tests

Repository-wide tests remain deferred to RC3-5.
