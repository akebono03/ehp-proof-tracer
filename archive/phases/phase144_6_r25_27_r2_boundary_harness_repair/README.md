# Phase 144-6 R25-27-R2 Boundary Harness Repair

## Purpose

The original R25-27 focused audit test exposed a mismatch inside the audit
helper itself.

The production argument-local-body traversal stops before another argument's
conclusion block. The R25-27 `_closure_from_block` helper did not explicitly
exclude the starting block when that starting direct premise was itself an
argument boundary.

R25-27-R2 repairs only that audit helper and reruns the original R25-27 audit.

## Production changes

None.

## Existing test changes

None.

## Repair

`_closure_from_block` now returns an empty closure when its starting direct
premise is an argument boundary, matching the production local-body ownership
rule.

## Validation

The runner executes:

1. two focused boundary-helper tests;
2. the original R25-27 audit-contract tests;
3. the existing Phase 143 argument-local-body regressions;
4. the six-group R25-27 ownership audit.

Repository-wide pytest remains deferred until the end of Phase 144-6.
