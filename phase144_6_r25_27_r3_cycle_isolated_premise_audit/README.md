# Phase 144-6 R25-27-R3 Cycle-Isolated Premise Audit

## Purpose

R25-27-R2 showed that excluding only other argument conclusions is insufficient
for a direct-premise ownership audit.

A proof-edge cycle can return from a direct premise to the current argument
conclusion. If the audit continues through that conclusion, it can enter sibling
premises and incorrectly attribute their blocks to the original premise.

R25-27-R3 isolates each direct premise by treating the current argument
conclusion as an additional audit-only exclusion boundary.

## Production changes

None.

The production local-body traversal is not changed in this package.

## Audit changes

`_closure_from_block` gains an audit-only `excluded_indices` parameter.

When measuring one direct premise, the current argument conclusion is excluded.
Other argument conclusions remain ownership boundaries as before.

This makes the measured subtree answer the intended question:

> Which blocks are reachable from this direct premise before returning to the
> owning argument conclusion or entering another argument?

## Validation

The runner executes focused cycle-isolation tests, the original R25-27 audit
contract, existing Phase 143 local-body regressions, and the six-group audit.

Repository-wide pytest remains deferred until the end of Phase 144-6.
