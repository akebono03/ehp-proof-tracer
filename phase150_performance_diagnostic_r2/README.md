# Phase 150 Performance Diagnostic R2

This package measures recomputation in the Phase 144-6 R5-37 through R5-41
audit builders.

It makes no production, test, or documentation changes and does not run the
full regression suite.

Measured builders:

- R5-37 semantic-equivalence/rendering inventory
- R5-38 visibility occurrences
- R5-38 explanatory contribution groups
- R5-39 narrative necessity inventory
- R5-40 placement inventory
- R5-41 topological-order audit

Each builder is run twice in the same Python process. This distinguishes
one-time import/process effects from repeated expensive reconstruction.

Run from the repository root with the provided PowerShell script.
