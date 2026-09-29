# Phase 144-6 R25-30-R3 Argument-Boundary Entry Classification Audit

## Purpose

R25-30-R2 exposed an important ownership case: some direct entry steps of a
group-structure or definition Argument already belong to another Argument's
conclusion block.

Such an entry is an Argument boundary. Its descendants must not be traversed
as though the entry were locally owned by the current Argument.

## Production changes

None.

## Existing repository test changes

None.

## Classification

Every direct step-level entry is classified as one of:

- `owned`: the entry does not belong to another Argument conclusion block;
- `argument_boundary`: the entry belongs to another Argument conclusion block.

An `argument_boundary` entry records its owner Argument index and role and
stops traversal immediately.

Only `owned` entries are expanded into child branches.

## Existing Argument contract

The production Argument builder already separates direct dependencies whose
blocks are Argument conclusions into `child_argument_indices`.

R25-30-R3 checks whether the step-level boundary classification agrees with
that existing block-level child-Argument contract.

## Interpretation

If the classified boundary pairs match `child_argument_indices`, the audit
confirms that these entries are not missing proof material: they are already
owned by child Arguments.

Any remaining giant `owned` entry is then the correct target for deeper branch
ownership analysis.

No production repair is attempted in R25-30-R3.

Repository-wide pytest remains deferred until the end of Phase 144-6.
