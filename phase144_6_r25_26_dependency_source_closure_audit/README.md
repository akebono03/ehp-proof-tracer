# Phase 144-6 R25-26 Dependency-Source Closure Audit

## Purpose

R25-25 showed that the excessive Narrative population already exists in the
argument local-body closure. It is not primarily created by the later ordered
contribution insertion stage.

R25-26 separates the dependency graph used by argument local-body ownership
into two sources:

1. presentation proof edges;
2. semantic-sidecar dependency edges.

It then measures proof-only, semantic-only, and combined closures for the
largest arguments in each of the six representative groups.

## Production changes

None.

## Expected decision

The audit determines whether the next ownership-boundary repair should target
proof-edge traversal, semantic dependency traversal, or their interaction.

No suppression rule is introduced in this package.

## Regression scope

Only focused audit tests and the existing Phase 143 argument-local-body tests
are run. Repository-wide pytest remains deferred until the end of Phase 144-6.
